"""Exercise the driver's full CLI against a real repository and scripted Claude calls."""

from __future__ import annotations

import ast
from contextlib import redirect_stdout
from datetime import datetime, timedelta
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wavedriver import gitstate
import wave_driver


FAKE = Path(__file__).with_name("fake_claude.py")
FOLDER = "plans/2026-11-17-t"
INDEX = FOLDER + "/index.md"
P1 = FOLDER + "/plan-1"
P2 = FOLDER + "/plan-2"
FLOW = "- Flow: autonomous · target: integration/t"
INDEX_TEXT = f"""# Example index

{FLOW}

## Parts

| Part | Problems | Points | Plan slug | Plan when | Command |
|---|---|---|---|---|---|
| 1 | P1 | 2 | t-p1 | now | plan part 1 |
| 2 | P2 | 1 | t-p2 | after part 1 merged | plan part 2 |
"""


def plan(part=1, waves=("⬜", "⬜"), merged=""):
    folder = f"{FOLDER}/plan-{part}"
    slug = f"t-p{part}"
    feature = "✅ merged" if merged else "⬜"
    lines = [
        "# Example plan", "",
        f"- Plan: `{folder}/` · slug: `{slug}` · tracking branch: `plan/{slug}`",
        FLOW, "", "## Features", "",
        "| ID | Slug | Title | Done when | Status | Waiting for | Branch | Merged |",
        "|---|---|---|---|---|---|---|---|",
        f"| F1 | example | Example feature | Works | {feature} | | | {merged} |",
        "", "## Waves", "", "| Wave | File | Tasks | Status |", "|---|---|---|---|",
    ]
    tasks = ["B", "C"]
    for n, mark in enumerate(waves, 1):
        lines.append(f"| {n} | `waves/w{n:02}.md` | {tasks[n-1]} | {mark} |")
    lines.extend(["", "## Tasks", "", "| ID | Slug | Feature | Wave | Complexity | Status |",
                  "|---|---|---|---|---|---|"])
    for n, mark in enumerate(waves, 1):
        lines.append(f"| {tasks[n-1]} | example-{n} | F1 | {n} | high | {mark} |")
    return "\n".join(lines) + "\n"


def wave(n, task, execution=""):
    return (f"# Wave {n}\n\nDepends on: —\n\n## Tasks\n\n| ID | Needs |\n"
            f"|---|---|\n| {task} | — |\n\n## Execution\n\n{execution}\n")


def commit(branch, files):
    return {"branch": branch, "base": "main", "files": files, "message": "Advance scenario"}


def step(prompt, model="sonnet", **kwargs):
    return {"expect": "^" + re.escape(prompt) + "$", "args": {"--model": model},
            "result": "Started: example\nFinished.", **kwargs}


W1 = f"/wave-run {P1} 1"
STATUS = step("/wave-status", "haiku", result="Status summary")


class DriverTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.repo = root / "repo"
        self.repo.mkdir()
        self.out = root / "out"
        self.scenario = root / "scenario.json"
        self.lock = self.repo / ".git" / "wave-driver.lock"
        self.git = gitstate.Git(self.repo).run
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Driver Test")
        self.git("config", "user.email", "driver@example.test")
        self.write(INDEX, INDEX_TEXT)
        self.save()
        self.git("switch", "-c", "plan/t-p1")
        self.write(P1 + "/README.md", plan())
        self.write(P1 + "/waves/w01.md", wave(1, "B"))
        self.write(P1 + "/waves/w02.md", wave(2, "C"))
        self.save()
        self.git("switch", "main")

    def write(self, name, content):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def save(self):
        self.git("add", ".")
        self.git("commit", "-m", "Set up driver fixture")

    def drive(self, steps, *args):
        self.scenario.write_text(json.dumps({"steps": steps}), encoding="utf-8")
        output = io.StringIO()
        with patch.dict(os.environ, {"FAKE_CLAUDE_SCENARIO": str(self.scenario)}), redirect_stdout(output):
            code = wave_driver.main([INDEX, "--repo", str(self.repo), "--out", str(self.out), *args],
                                    claude_prefix=[sys.executable, str(FAKE)])
        self.output = output.getvalue()
        log = Path(str(self.scenario) + ".calls")
        self.calls = [json.loads(line)["argv"] for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
        if code != 3:
            self.assertFalse(self.lock.exists())
        path = self.out / "report.md"
        self.report = path.read_text(encoding="utf-8") if path.exists() else ""
        return code

    def test_chain(self):
        head = self.git("rev-parse", "main")
        stop = "Stop red-after-merge: check failed — next: inspect the check"
        steps = [
            step(W1, commits=[commit("plan/t-p1", {P1 + "/README.md": plan(waves=("✅", "⬜"))})]),
            step(f"/wave-run {P1} 2", commits=[
                commit("integration/t", {"feature.txt": "ready"}),
                commit("plan/t-p1", {P1 + "/README.md": plan(waves=("✅", "✅"), merged="{{rev:integration/t}}")})]),
            step(f"/wave-plan flow autonomous {INDEX} part 2", "opus", commits=[
                commit("plan/t-p2", {P2 + "/README.md": plan(2, ("⬜",)), P2 + "/waves/w01.md": wave(1, "B")})]),
            step(f"/wave-run {P2} 1", result=stop, commits=[
                commit("plan/t-p2", {P2 + "/README.md": plan(2, ("❌",)), P2 + "/waves/w01.md": wave(1, "B", stop)})]),
            STATUS,
        ]
        self.assertEqual(self.drive(steps), 0, self.output)
        self.assertEqual([a[a.index("--model") + 1] for a in self.calls],
                         ["sonnet", "sonnet", "opus", "sonnet", "haiku"])
        self.assertIn("**F1 · Example feature** · merged into `integration/t`", self.report)
        self.assertIn(stop, self.report.split("## Halts")[1].split("##")[0])
        self.assertIn("git diff main...integration/t", self.report.split("## Next")[1])
        self.assertIn("Status summary", self.report)
        self.assertEqual(self.git("rev-parse", "main"), head)

    def test_usage_limit(self):
        self.assertEqual(self.drive([step(W1, exit=1, api_error_status=429)]), 1)
        self.assertEqual(len(self.calls), 1)
        self.assertIn("ended: usage limit", self.report)

    def test_lock_held(self):
        self.lock.write_text("another holder", encoding="utf-8")
        self.assertEqual(self.drive([]), 3)
        self.assertEqual(self.calls, [])
        self.assertIn("another holder", self.output)
        self.assertEqual(self.lock.read_text(encoding="utf-8"), "another holder")

    def test_guard(self):
        self.assertEqual(self.drive([step(W1, commits=[commit("main", {"unexpected": "edit"})])]), 1)
        self.assertIn("ended: guard:", self.report)
        self.assertIn("refs/heads/main", self.report)
        self.assertEqual(len(self.calls), 1)

    def test_no_progress(self):
        self.assertEqual(self.drive([step(W1), step(W1), STATUS]), 0)
        self.assertEqual(len(self.calls), 3)
        self.assertIn("no progress after 2", self.report)
        self.assertIn("Status summary", self.report)

    def test_dry_run(self):
        self.assertEqual(self.drive([], "--dry-run"), 0)
        self.assertIn(W1, self.output)
        self.assertFalse(self.out.exists())
        self.assertEqual(self.calls, [])

    def test_deadline(self):
        past = (datetime.now() - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
        self.assertEqual(self.drive([STATUS], "--deadline", past), 1)
        self.assertIn("ended: deadline", self.report)
        self.assertEqual(len(self.calls), 1)
        self.assertIn("Status summary", self.report)
        section = self.report.split("## Calls")[1].split("##")[0]
        self.assertEqual(len(re.findall(r"^\| \d+ \|", section, re.M)), 1)

    def test_failure_rail(self):
        failure = step(W1, exit=1, subtype="error_max_turns")
        self.assertEqual(self.drive([failure, failure, STATUS], "--max-failures", "2"), 1)
        self.assertIn("ended: max-failures", self.report)
        self.assertEqual(len(self.calls), 3)

    def test_task_mode(self):
        self.git("switch", "plan/t-p1")
        self.write(P1 + "/README.md", plan(waves=("🔄", "⬜")))
        self.write(P1 + "/waves/w01.md", wave(1, "B", "Waiting: task mode B"))
        self.save()
        self.git("switch", "main")
        steps = [step(W1 + " task B", "opus"), step(W1, result="Stop wave-running: busy"), STATUS]
        self.assertEqual(self.drive(steps), 0, self.output)
        self.assertEqual([a[a.index("-p") + 1] for a in self.calls], [W1 + " task B", W1, "/wave-status"])
        self.assertEqual(self.calls[0][self.calls[0].index("--model") + 1], "opus")
        self.assertIn("Stop wave-running: busy", self.report)


class CompatibilityTests(unittest.TestCase):
    def test_python_39_syntax(self):
        scripts = Path(wave_driver.__file__).parent
        for path in [*sorted((scripts / "wavedriver").glob("*.py")), scripts / "wave_driver.py"]:
            with self.subTest(path=path):
                ast.parse(path.read_text(encoding="utf-8"), feature_version=(3, 9))


if __name__ == "__main__":
    unittest.main()
