from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wavedriver import claude, decide, gitstate


FOLDER = "plans/example"
UNIT = f"{FOLDER}/plan-1"
TARGET = "integration/example"


def plan(folder=UNIT, *, tracking=True, flow="autonomous", target=TARGET, features=(), waves=(),
         tasks=(), wave_files=None):
    readme = gitstate.Readme("example-p1", flow, target, [], list(features), list(waves), list(tasks))
    return gitstate.PlanState(folder, "plan/example-p1", tracking, readme, [], wave_files or {}, [], {}, [])


def snapshot(*plans, parts=None):
    index = None
    if parts is not None:
        index = gitstate.Index(f"{FOLDER}/index.md", FOLDER, "Example", TARGET, [row.part for row in parts])
    return gitstate.Snapshot(Path("."), "main", index, parts or [], list(plans), {}, {})


def part(number, planned=None, ready=True):
    return gitstate.PartState(gitstate.Part(number, f"example-p{number}", "now", []),
                              f"{FOLDER}/plan-{number}", planned, ready, "dependency")


def feature(status, cell):
    return gitstate.Feature("F1", "feature", "Feature", "Done", status, cell, "review", "", "")


def wave(status):
    return gitstate.Wave(2, "waves/w02.md", status, f"{status} status")


class ChooseTest(unittest.TestCase):
    def setUp(self):
        self.cfg = decide.DecideConfig()

    def choose(self, planned, task_runs=()):
        return decide.choose(snapshot(planned), {}, set(task_runs), self.cfg)

    def test_index_picks_first_action_and_collects_later_waits_and_halts(self):
        manual = plan(f"{FOLDER}/plan-3", flow="manual")
        state = snapshot(manual, parts=[part(1), part(2, ready=False), part(3, manual), part(4)])
        choice = decide.choose(state, {}, set(), self.cfg)
        self.assertEqual(choice.action.kind, "plan")
        self.assertEqual(choice.action.unit, UNIT)
        self.assertEqual(choice.action.call, claude.Call(
            "wave-plan", f"flow autonomous {FOLDER}/index.md part 1", "opus", *self.cfg.caps["wave-plan"],
        ))
        self.assertEqual(choice.waits, [decide.Halt(f"{FOLDER}/plan-2", "part 2 waits: dependency")])
        self.assertEqual(choice.halts[0].unit, manual.folder)
        skipped = decide.choose(state, {UNIT: decide.Halt(UNIT, "stopped")}, set(), self.cfg)
        self.assertEqual(skipped.action.unit, f"{FOLDER}/plan-4")

    def test_missing_tracking_with_finished_and_unfinished_features(self):
        finished = plan(tracking=False, features=[feature("✅", "✅ merged"), feature("➖", "➖")])
        self.assertEqual(self.choose(finished).waits, [decide.Halt(UNIT, "finished")])
        unfinished = plan(tracking=False, features=[feature("👀", "👀 review")])
        self.assertEqual(self.choose(unfinished).halts, [decide.Halt(
            UNIT, "tracking branch plan/example-p1 is missing", claude.both(f"wave-status {UNIT}"),
        )])

    def test_manual_flow_and_finished_plan(self):
        self.assertEqual(self.choose(plan(flow="manual")).halts, [decide.Halt(
            UNIT, "manual flow: the driver runs autonomous plans only",
            claude.both(f"wave-run {UNIT} flow autonomous"),
        )])
        self.assertEqual(self.choose(plan()).waits, [decide.Halt(UNIT, "finished")])

    def test_running_wave_waiting_for_task_then_resume(self):
        task = gitstate.Task("A", "task", "F1", 2, "high", "🔄", "🔄")
        wave_file = gitstate.WaveFile([], {}, ["A"], "")
        planned = plan(waves=[wave("🔄")], tasks=[task], wave_files={2: wave_file})
        action = self.choose(planned).action
        self.assertEqual((action.kind, action.wave, action.task), ("task", 2, "A"))
        self.assertEqual(action.call, claude.Call(
            "wave-run", f"{UNIT} 2 task A", "opus", *self.cfg.caps["task"],
        ))
        resumed = self.choose(planned, [(UNIT, 2, "A")]).action
        self.assertEqual(resumed.kind, "resume")
        self.assertEqual(resumed.call, claude.Call("wave-run", f"{UNIT} 2", "sonnet", *self.cfg.caps["wave-run"]))

    def test_running_wave_checks_needs_for_all_waiting_tasks_first(self):
        wave_file = gitstate.WaveFile([], {"B": "a token"}, ["A", "B"], "")
        choice = self.choose(plan(waves=[wave("🔄")], wave_files={2: wave_file}))
        self.assertIsNone(choice.action)
        self.assertEqual(choice.halts, [decide.Halt(
            UNIT, "wave 2 waits for task mode B, which needs a token",
            claude.both(f"wave-run {UNIT} 2 task B") + " in a session that has it, then "
            + claude.both(f"wave-run {UNIT} 2"),
        )])

    def test_running_wave_without_wait_precedes_failed_wave(self):
        choice = self.choose(plan(waves=[wave("❌"), wave("🔄")]))
        self.assertIsNone(choice.action)
        self.assertIn("another run holds it", choice.halts[0].reason)

    def test_failed_wave_uses_stop_line_and_next(self):
        next_command = claude.both(f"wave-plan {UNIT}")
        stop = f"Stop red-after-merge: tests failed — next: {next_command}"
        wave_file = gitstate.WaveFile([], {}, [], stop)
        choice = self.choose(plan(waves=[wave("❌")], wave_files={2: wave_file}))
        self.assertEqual(choice.halts, [decide.Halt(UNIT, stop, next_command)])

    def test_pending_wave_requires_merged_feature(self):
        wave_file = gitstate.WaveFile(["F1"], {}, [], "")
        review = plan(features=[feature("👀", "👀 review")], waves=[wave("⬜")], wave_files={2: wave_file})
        self.assertEqual(self.choose(review).halts, [decide.Halt(
            UNIT, "wave 2 depends on F1 merged; F1 is 👀 review, waiting for review",
            "review F1, then " + claude.both(f"wave-run {UNIT} merge F1"),
        )])
        merged = plan(features=[feature("✅", "✅ merged")], waves=[wave("⬜")], wave_files={2: wave_file})
        action = self.choose(merged).action
        self.assertEqual(action.kind, "wave")
        self.assertEqual(action.call, claude.Call("wave-run", f"{UNIT} 2", "sonnet", *self.cfg.caps["wave-run"]))

    def test_status_scope(self):
        self.assertEqual(decide.status_call(snapshot(plan()), self.cfg).args, UNIT)
        self.assertEqual(decide.status_call(snapshot(parts=[part(1)]), self.cfg).args, "")


class AfterCallTest(unittest.TestCase):
    def setUp(self):
        self.action = decide.Action("wave", UNIT, claude.Call("wave-run", f"{UNIT} 2", "sonnet", 110, 3), "")
        self.attempts = {}

    def after(self, outcome, *, state=None, progressed=False, **fields):
        result = claude.Result(outcome, 0, {}, "", "", 0, 0, 0, 0, **fields)
        return decide.after_call(self.action, result, state or snapshot(plan()), progressed, self.attempts)

    def test_target_stop_affects_only_units_with_the_same_target(self):
        first = plan()
        other = plan(f"{FOLDER}/plan-3", target="integration/other")
        state = snapshot(first, other, parts=[part(1, first), part(2), part(3, other)])
        for code in decide.TARGET_CODES:
            with self.subTest(code=code):
                stop = f"Stop {code}: details"
                self.assertEqual(self.after("stop", state=state, stop_code=code, stop_line=stop, next="repair"), [
                    decide.Halt(UNIT, stop, "repair"), decide.Halt(f"{FOLDER}/plan-2", stop, "repair"),
                ])

    def test_no_progress_twice(self):
        self.assertEqual(self.after("ok"), [])
        self.assertEqual(self.after("ok"), [decide.Halt(
            UNIT, "no progress after 2 successful calls of " + claude.both(f"wave-run {UNIT} 2"),
            claude.both(f"wave-status {UNIT}"),
        )])

    def test_progress_clears_previous_failure(self):
        self.assertEqual(self.after("failed", detail="error"), [])
        self.assertTrue(self.attempts)
        self.assertEqual(self.after("ok", progressed=True), [])
        self.assertEqual(self.attempts, {})
