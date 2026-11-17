from __future__ import annotations

import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wavedriver import rails


class AsciiConsole(io.StringIO):
    def write(self, text: str) -> int:
        text.encode("ascii")
        return super().write(text)


class LockAndLogTests(unittest.TestCase):
    def test_existing_lock_reports_holder_and_owner_can_release(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "driver.lock"
            owner = rails.Lock(path)
            holder = owner.acquire()
            self.assertRegex(holder, rf"^pid {os.getpid()} host .+ started .+ token [a-f0-9]{{8}}$")
            self.assertEqual(path.read_text(encoding="utf-8"), holder + "\n")

            with self.assertRaises(rails.LockHeld) as error:
                rails.Lock(path).acquire()
            self.assertEqual(error.exception.holder, holder)
            owner.release()
            self.assertFalse(path.exists())

    def test_release_leaves_replacement_lock(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "driver.lock"
            owner = rails.Lock(path)
            owner.acquire()
            path.unlink()
            replacement = rails.Lock(path)
            holder = replacement.acquire()
            owner.release()
            self.assertEqual(path.read_text(encoding="utf-8"), holder + "\n")
            replacement.release()

    def test_log_preserves_unicode_when_console_cannot_encode_it(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "driver.log"
            console = AsciiConsole()
            with redirect_stdout(console):
                log = rails.Log(path)
                log.write("✅ Ready")
                log.write("Next")
            content = path.read_text(encoding="utf-8")
            self.assertRegex(content, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} ✅ Ready\n")
            self.assertEqual(console.getvalue(), content.replace("✅", "?"))


class DeadlineAndCounterTests(unittest.TestCase):
    def test_deadline_formats_and_rollover(self):
        day = datetime(2026, 11, 18, 5)
        self.assertEqual(rails.parse_deadline("06:30", day), datetime(2026, 11, 18, 6, 30))
        for hour, minute in [(6, 30), (7, 0)]:
            self.assertEqual(
                rails.parse_deadline("06:30", day.replace(hour=hour, minute=minute)),
                datetime(2026, 11, 19, 6, 30),
            )
        self.assertEqual(
            rails.parse_deadline("2026-11-17 21:30", day), datetime(2026, 11, 17, 21, 30)
        )
        for invalid in ["tomorrow", "6:30", "24:00", "2026-11-31 06:30"]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                rails.parse_deadline(invalid, day)

    def test_counters_accumulate_and_reset_failure_streak(self):
        counters = rails.Counters()
        for outcome in ("failed", "timeout", "limit", "auth"):
            counters.record(outcome, 0.25, 2, 0.5)
        self.assertEqual(counters, rails.Counters(4, 4, 4, 1.0, 8, 2.0))
        counters.record("ok", 0.5, 3, 1.0)
        self.assertEqual(counters, rails.Counters(5, 4, 0, 1.5, 11, 3.0))
        counters.record("failed", 0.25, 2, 0.5)
        counters.record("stop", 0.25, 2, 0.5)
        self.assertEqual(counters, rails.Counters(7, 5, 0, 2.0, 15, 4.0))

    def test_rails_in_priority_order(self):
        now = datetime(2026, 11, 18, 6, 30)
        limits = rails.Limits(max_calls=2, max_failures=1, deadline=now, max_usd=1.25)
        counters = rails.Counters(calls=2, failures_in_row=1, cost=1.25)
        self.assertEqual(rails.rail_reason(limits, counters, now), "max-calls: 2 calls made")
        limits.max_calls += 1
        self.assertEqual(
            rails.rail_reason(limits, counters, now), "max-failures: 1 failed calls in a row"
        )
        limits.max_failures += 1
        self.assertEqual(rails.rail_reason(limits, counters, now), "deadline: 2026-11-18 06:30 reached")
        self.assertEqual(
            rails.rail_reason(limits, counters, now.replace(minute=29)), "max-usd: 1.25 USD spent"
        )
        self.assertIsNone(rails.rail_reason(rails.Limits(), counters, now))


class GuardTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.repo = Path(folder.name)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Guard Test")
        self.git("config", "user.email", "guard@example.org")
        self.tracked = self.repo / "tracked.txt"
        self.tracked.write_text("original\n", encoding="utf-8")
        self.git("add", self.tracked.name)
        self.git("commit", "-m", "Initial commit")

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        ).stdout.strip()

    def snapshot(self) -> dict[str, str]:
        return rails.guard_snapshot(self.repo, "main")

    def test_commit_on_main_is_detected(self):
        before = self.snapshot()
        self.git("commit", "--allow-empty", "-m", "Advance main")
        after = self.snapshot()
        self.assertEqual(
            rails.guard_violations(before, after),
            [f"refs/heads/main changed: {before['refs/heads/main']} -> {after['refs/heads/main']}"],
        )

    def test_remote_ref_creation_and_removal_are_detected(self):
        before = self.snapshot()
        self.git("update-ref", "refs/remotes/origin/x", "HEAD")
        after = self.snapshot()
        self.assertEqual(rails.guard_violations(before, after), ["refs/remotes/origin/x added"])
        self.git("update-ref", "-d", "refs/remotes/origin/x")
        self.assertEqual(rails.guard_violations(after, self.snapshot()), ["refs/remotes/origin/x removed"])

    def test_tracks_checkout_status_and_detached_head(self):
        before = self.snapshot()
        (self.repo / "untracked.txt").touch()
        self.assertEqual(rails.guard_violations(before, self.snapshot()), [])
        self.tracked.write_text("edited\n", encoding="utf-8")
        self.assertEqual(
            rails.guard_violations(before, self.snapshot()),
            ["checkout:status changed:  ->  M tracked.txt"],
        )

        before = self.snapshot()
        self.git("checkout", "--detach")
        sha = self.git("rev-parse", "HEAD")
        self.assertEqual(
            rails.guard_violations(before, self.snapshot()),
            [f"checkout:HEAD changed: refs/heads/main -> detached {sha}"],
        )

    def test_other_branch_commit_in_linked_worktree_is_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            linked = Path(folder) / "linked"
            self.git("worktree", "add", "-b", "feature", str(linked))
            before = self.snapshot()
            self.git("-C", str(linked), "commit", "--allow-empty", "-m", "Advance feature")
            self.assertEqual(rails.guard_violations(before, self.snapshot()), [])


if __name__ == "__main__":
    unittest.main()
