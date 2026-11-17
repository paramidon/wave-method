"""Tests for the driver's read-only Git state."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wavedriver import gitstate


INDEX = """# Topic index

## Parts

| Part | Problems | Points | Plan slug | Plan when | Command |
|---|---|---|---|---|---|
| 1 | P1 | 4 | `t-p1` | now | plan part 1 |
| 2 | P2 | 2 | `t-p2` | after part 1 merged | plan part 2 |
"""

README = """# Test plan

- Plan: `plans/2026-11-17-t/plan-1/` · slug: `t-p1` · tracking branch: `plan/t-p1`
{flow}

## Features

| ID | Slug | Title | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|
| F1 | `first` | First feature | Check passes | ✅ merged | | `feat/t-p1/F1-first` | `{merged}` |
| F2 | `second` | Second feature | Reviewed | {second} | {waiting} | | |

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A | 🔄 task mode |
| — | `waves/malformed.md` | X | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `first-task` | F1 | 1 | medium | ⬜ |
| X | `malformed-task` | F1 | — | low | ⬜ |
"""

WAVE = """# Wave 1

## Tasks

| ID | Needs |
|---|---|
| A | — |
| B | browser session |
| C | - |

Depends on: `F1 merged`, then
`F2 merged` and wave 2.

## Execution
Started 2026-11-17 22:00.
Stop old-result: earlier
Stop wave-running: locked — next: wait
Waiting: task mode B, C — next: resume
"""

AUTONOMOUS = "- Flow: autonomous · target: integration/t"
INDEX_PATH = "plans/2026-11-17-t/index.md"
PLAN_FOLDER = "plans/2026-11-17-t/plan-1"


def readme(flow="", merged="abcd", second="👀 review", waiting="review"):
    return README.format(flow=flow, merged=merged, second=second, waiting=waiting)


class ParserTests(unittest.TestCase):
    def test_readme_autonomous(self):
        parsed = gitstate.parse_readme(readme(AUTONOMOUS + " · manual review: F2"))
        self.assertEqual(parsed.slug, "t-p1")
        self.assertEqual(parsed.flow, "autonomous")
        self.assertEqual(parsed.target, "integration/t")
        self.assertEqual(parsed.manual_review, ["F2"])
        self.assertEqual(parsed.features[0], gitstate.Feature(
            "F1", "first", "First feature", "Check passes", "✅", "✅ merged", "",
            "feat/t-p1/F1-first", "abcd",
        ))
        self.assertTrue(parsed.features[0].is_merged)
        self.assertFalse(parsed.features[1].is_merged)
        self.assertEqual(parsed.waves, [
            gitstate.Wave(1, "waves/w01.md", "🔄", "🔄 task mode"),
        ])
        self.assertEqual(parsed.tasks, [
            gitstate.Task("A", "first-task", "F1", 1, "medium", "⬜", "⬜"),
        ])

    def test_readme_without_flow(self):
        parsed = gitstate.parse_readme(readme())
        self.assertEqual((parsed.flow, parsed.target, parsed.manual_review), ("manual", None, []))

    def test_readme_explicit_manual(self):
        parsed = gitstate.parse_readme(readme("- Flow: manual"))
        self.assertEqual((parsed.flow, parsed.target, parsed.manual_review), ("manual", None, []))

    def test_wave_with_waiting_last(self):
        parsed = gitstate.parse_wave_file(WAVE + "\n## Closed problems\n\nLater section\n")
        self.assertEqual(parsed, gitstate.WaveFile(
            ["F1", "F2"], {"A": "", "B": "browser session", "C": ""}, ["B", "C"],
            "Stop wave-running: locked — next: wait",
        ))

    def test_wave_with_execution_after_waiting(self):
        parsed = gitstate.parse_wave_file(WAVE + "\nResumed 2026-11-17 22:01.\n")
        self.assertEqual(parsed.waiting_ids, [])

    def test_problems_open_and_fixed(self):
        text = """# Open problems
Next ID: I3

- **[I1 · wave 1 / feature F1] Failed to start** — where: `run.py:15`; expected / got;
  proposal: fix setup; status: open

- **[I2 · wave 2 / task B / feature F2] Stale output** — where: `run.py:20`;
  status: fixed in abcd (task B)
"""
        self.assertEqual(gitstate.parse_problems(text), [
            gitstate.Entry("I1", "wave 1 / feature F1", "Failed to start", "open", True, ["F1"]),
            gitstate.Entry("I2", "wave 2 / task B / feature F2", "Stale output",
                           "fixed in abcd (task B)", False, ["F2"]),
        ])

    def test_index_parts_and_dependency(self):
        parsed = gitstate.parse_index(INDEX, INDEX_PATH)
        self.assertEqual(parsed, gitstate.Index(
            INDEX_PATH, "plans/2026-11-17-t", "t", "integration/t", [
                gitstate.Part(1, "t-p1", "now", []),
                gitstate.Part(2, "t-p2", "after part 1 merged", [1]),
            ],
        ))


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.run_git("init", "-b", "main")
        self.run_git("config", "user.name", "Git State Test")
        self.run_git("config", "user.email", "gitstate@example.test")
        self.write(INDEX_PATH, INDEX)
        self.commit("Add index")
        self.git = gitstate.Git(self.repo)

    def run_git(self, *args):
        result = subprocess.run(
            ["git", "-C", str(self.repo), *args], check=True, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
        )
        return result.stdout.rstrip("\n")

    def write(self, relative_path, value):
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")

    def commit(self, message):
        self.run_git("add", ".")
        self.run_git("commit", "-m", message)

    def add_part(self, second, waiting):
        self.run_git("switch", "-c", "integration/t")
        self.write("integrated.txt", "Feature F1\n")
        self.commit("Integrate F1")
        self.write("integrated.txt", "Feature F1 and its follow-up\n")
        self.commit("Integrate the follow-up")
        merged = self.run_git("rev-parse", "--short", "HEAD")

        self.run_git("switch", "-c", "plan/t-p1", "main")
        self.write(f"{PLAN_FOLDER}/README.md", readme(AUTONOMOUS, merged, second, waiting))
        self.write(f"{PLAN_FOLDER}/waves/w01.md", WAVE)
        self.write(f"{PLAN_FOLDER}/reviews/F2.md", "# F2 review\n")
        self.commit("Add tracked plan")
        # The Git snapshot must ignore edits in the checked-out plan.
        self.write(f"{PLAN_FOLDER}/README.md", "Uncommitted edit\n")

    def test_index_snapshot_ready_after_prior_part(self):
        self.add_part("➖ dropped", "")
        snapshot = gitstate.read_snapshot(self.git, INDEX_PATH, "main")
        part1, part2 = snapshot.parts
        self.assertIs(part1.plan, snapshot.plans[0])
        self.assertTrue(part1.plan.tracking)
        self.assertEqual(part1.plan.source, "plan/t-p1")
        self.assertEqual(part1.plan.wave_files[1].waiting_ids, ["B", "C"])
        self.assertEqual(part1.plan.merged_not_in_main, ["F1"])
        self.assertIsNone(part2.plan)
        self.assertTrue(part2.ready)
        self.assertEqual(part2.ready_reason, "")
        self.assertEqual(snapshot.targets["integration/t"].ahead, 2)

    def test_index_snapshot_blocked_by_earlier_review(self):
        self.add_part("👀 review", "review")
        snapshot = gitstate.read_snapshot(self.git, INDEX_PATH, "main")
        self.assertFalse(snapshot.parts[1].ready)
        self.assertEqual(snapshot.parts[1].ready_reason, "part 1 — F2 👀 review (review)")
        self.assertIn("F2", snapshot.plans[0].briefs)

    def test_plan_folder_not_on_any_branch(self):
        with self.assertRaisesRegex(gitstate.GitError, "not found on any branch"):
            gitstate.read_snapshot(self.git, PLAN_FOLDER, "main")


if __name__ == "__main__":
    unittest.main()
