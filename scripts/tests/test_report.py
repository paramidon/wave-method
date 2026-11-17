"""Tests for the overnight driver's Markdown report."""

from __future__ import annotations

import re
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wavedriver import gitstate, report


class MorningReportTest(unittest.TestCase):
    def setUp(self):
        started = datetime(2026, 11, 17, 22)
        self.run_info = report.RunInfo(started, started + timedelta(minutes=65),
                                       "repo", "plans/x", "main", "complete", [], "out", "out/log")
        self.merged = gitstate.Feature("F1", "a", "Alpha", "see A", "✅", "✅ merged", "", "", "abc123")
        self.review = gitstate.Feature("F2", "b", "Beta", "see B", "👀", "👀 review", "", "", "")
        blocked = gitstate.Feature("F3", "c", "Gamma", "see C", "⚠️", "⚠️ I7", "", "", "")
        readme = gitstate.Readme("x", "autonomous", "integration/x", [],
                                 [self.merged, self.review, blocked], [], [])
        briefs = {
            "F1": "# Alpha\n## Essence\nShow Alpha.\n## How to test\n1. Open A.\n## Worth a look\nnothing",
            "F2": "- Branch: feat/x/F2-b · worktree: /w/x-F2\n## Worth a look\nLine one\nline two",
        }
        entry = gitstate.Entry("I7", "F3", "Missing input", "open", True, ["F3"])
        self.plan = gitstate.PlanState("plans/x", "plan/x", True, readme, [entry], {}, ["F1"], briefs, ["green"])
        target = gitstate.TargetState("integration/x", True, 3, "/w/x")
        self.snapshot = gitstate.Snapshot(Path("/src/repo"), "main", None, [], [self.plan], {target.name: target}, {})
        self.halt = SimpleNamespace(unit="wave 2", reason="locked", next="release lock")

    def test_complete_report(self):
        calls = [
            report.CallRecord(1, "22:00", "wave", "x", "/wave-run", "model", "ok", 0, "",
                              5, 0.32, 3, 0, warnings=["slow", "retry"]),
            report.CallRecord(2, "22:10", "task", "F3", "implement", "model", "failed", 1, "",
                              2, 0.10, 1.5, 1, detail="input | missing"),
        ]
        wait = SimpleNamespace(unit="part 4", reason="needs part 3", next="")
        status = "Status snapshot\n\n  indented\n"
        output = report.render(self.run_info, self.snapshot, calls, [self.halt], [wait], status)
        headings = re.findall(r"^## (.+)$", output, re.M)
        self.assertEqual(headings, ["Integration targets", "Merged, not in main", "Ready for review",
                                    "Blocked and waiting", "Halts", "Open problems", "Status check",
                                    "Calls", "Next", "wave-status"])
        sections = report.brief_sections(output)
        merged = sections["Merged, not in main"]
        self.assertEqual(merged.splitlines()[0], "**F1 · Alpha** · merged into `integration/x` `abc123` · `/w/x`")
        self.assertIn("Show Alpha.\nHow to test:\n1. Open A.", merged)
        self.assertNotIn("Worth a look", merged)
        review = sections["Ready for review"]
        self.assertIn("**F2 · Beta** · `feat/x/F2-b` · `/w/x-F2`", review)
        self.assertIn("Worth a look: Line one line two", review)
        self.assertEqual(review.splitlines()[-1], "Merge: `/wave-run plans/x merge F2` · `$wave-run plans/x merge F2`")
        self.assertIn("⚠️ I7: Missing input", sections["Blocked and waiting"])
        self.assertIn("`part 4` — needs part 3", sections["Blocked and waiting"])
        self.assertIn("locked — next: release lock", sections["Halts"])
        self.assertIn("I7 · F3: Missing input — open", sections["Open problems"])
        self.assertIn("`plans/x`: green", sections["Status check"])
        self.assertIn("(1 h 5 min)", output)
        self.assertIn("failed: 1 · turns: 7 · cost: 0.42 USD (total_cost_usd) · Claude minutes: 4.5", output)
        rows = sections["Calls"].splitlines()
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertEqual(len(re.split(r"(?<!\\)\|", row.strip("|"))), 13)
        self.assertIn(r"input \| missing", rows[-1])
        self.assertIn("slow; retry", rows[-2])
        self.assertEqual(sections["wave-status"], "````\n" + status + "````")
        self.assertEqual(report.next_commands(self.snapshot, [self.halt]), [
            "review `git diff main...integration/x`, then merge it in the main checkout: `git merge --no-ff integration/x`",
            "review `feat/x/F2-b`, then `/wave-run plans/x merge F2` · `$wave-run plans/x merge F2`",
            "wave 2: release lock",
            "re-plan the open problems I7: `/wave-plan plans/x` · `$wave-plan plans/x`",
        ])

    def test_missing_brief_and_manual_approval(self):
        block = report.review_block(self.snapshot, self.plan, self.review, None)
        self.assertIn("`feat/x/F2-b` · `/src/repo.worktrees/x-F2`", block)
        self.assertIn("Beta\nHow to test: not recorded — see B", block)
        self.review.branch = "feat/override"
        self.assertIn("`feat/override`", report.review_block(self.snapshot, self.plan, self.review, None))
        block = report.merged_block(self.snapshot, self.plan, self.merged, "# Alpha\n- approved by the user")
        self.assertTrue(block.endswith("Approved: by the user"))

    def test_empty_report(self):
        self.snapshot.targets.clear()
        self.snapshot.plans.clear()
        sections = report.brief_sections(report.render(self.run_info, self.snapshot, [], [], [], None))
        self.assertEqual(sections.pop("wave-status"), "not run")
        self.assertIn("Calls: 0", sections.pop("header"))
        self.assertEqual(set(sections.values()), {"none"})
