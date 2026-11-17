"""Exercise the fake Claude CLI in a temporary Git repository."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

SCRIPT = Path(__file__).with_name("fake_claude.py").resolve()


class FakeClaudeTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.repo = Path(directory.name) / "repo"
        self.repo.mkdir()
        self.scenario = Path(directory.name) / "test.json"
        self.state = self.scenario.with_suffix(".json.state")
        self.calls = self.scenario.with_suffix(".json.calls")
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test Author")
        self.git("config", "user.email", "test@example.com")
        (self.repo / "tracked").write_text("initial content", encoding="utf-8")
        self.git("add", "tracked")
        self.git("commit", "-m", "Initial commit")

    def run_command(self, *args, env=None, check=False):
        return subprocess.run(
            args, cwd=self.repo, env=env, check=check, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
        )

    def git(self, *args):
        return self.run_command("git", *args, check=True).stdout.rstrip("\n")

    def invoke(self, *args):
        return self.run_command(
            sys.executable, str(SCRIPT), *args,
            env={**os.environ, "FAKE_CLAUDE_SCENARIO": str(self.scenario)},
        )

    def steps(self, *steps):
        self.scenario.write_text(json.dumps({"steps": steps}), encoding="utf-8")

    def test_version_leaves_scenario_untouched(self):
        completed = self.invoke("--version")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "0.0.0 (fake claude)\n")
        self.assertFalse(self.calls.exists())
        self.assertFalse(self.state.exists())

    def test_steps_commit_update_refs_and_record_calls(self):
        self.steps(
            {
                "expect": "^/wave-run plans/x/plan-1 1$",
                "args": {"--model": "sonnet"},
                "commits": [{
                    "branch": "plan/x-p1", "base": "main", "message": "Update plan",
                    "files": {"plans/x/plan-1/README.md": "main = {{rev:main}}\n"},
                }],
                "refs": {"refs/heads/integration/x": "plan/x-p1"},
                "result": "integration = {{rev:integration/x}}",
                "cost": 0.25,
                "turns": 12,
                "denials": 2,
            },
            {"expect": "^/wave-status$", "result": "second response"},
        )
        first_args = ["-p", "/wave-run plans/x/plan-1 1", "--model", "sonnet"]
        self.assertFalse(self.state.exists())
        (self.repo / "tracked").write_text("staged content", encoding="utf-8")
        self.git("add", "tracked")
        first = self.invoke(*first_args)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.state.read_text(encoding="utf-8"), "1")
        self.assertEqual(self.git("rev-parse", "plan/x-p1^"), self.git("rev-parse", "main"))
        self.assertEqual(self.git("rev-parse", "plan/x-p1"), self.git("rev-parse", "integration/x"))
        main = self.git("rev-parse", "--short", "main")
        integration = self.git("rev-parse", "--short", "integration/x")
        self.assertEqual(self.git("show", "plan/x-p1:plans/x/plan-1/README.md"), f"main = {main}")
        self.assertEqual(self.git("show", "plan/x-p1:tracked"), "initial content")
        self.assertEqual(self.git("show", ":tracked"), "staged content")
        self.assertEqual(self.git("symbolic-ref", "--short", "HEAD"), "main")
        identity = self.git("show", "-s", "--format=%an <%ae>%n%cn <%ce>", "plan/x-p1")
        self.assertEqual(identity, "fake <fake@example.com>\nfake <fake@example.com>")
        self.assertEqual(json.loads(first.stdout), {
            "type": "result", "subtype": "success", "is_error": False,
            "result": f"integration = {integration}", "num_turns": 12,
            "total_cost_usd": 0.25, "permission_denials": [{}, {}], "api_error_status": None,
        })

        second_args = ["-p", "/wave-status"]
        second = self.invoke(*second_args)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(second.stdout)["result"], "second response")
        self.assertEqual(self.state.read_text(encoding="utf-8"), "2")
        calls = [json.loads(line) for line in self.calls.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(calls, [
            {"argv": first_args, "cwd": str(self.repo.resolve())},
            {"argv": second_args, "cwd": str(self.repo.resolve())},
        ])

    def assert_rejected(self, completed, reason):
        self.assertEqual(completed.returncode, 1, completed.stderr)
        message = json.loads(completed.stdout)
        self.assertEqual(message["type"], "result")
        self.assertEqual(message["subtype"], "error_during_execution")
        self.assertIs(message["is_error"], True)
        self.assertRegex(message["errors"][0], "^fake: " + reason)

    def test_prompt_mismatch_and_exhausted_scenario(self):
        self.steps({"expect": "^/wave-status$", "refs": {"refs/heads/unexpected": "main"}})
        self.assert_rejected(self.invoke("-p", "/wave-run"), "expected prompt")
        self.assertEqual(self.git("branch", "--list", "unexpected"), "")
        self.assert_rejected(self.invoke("-p", "/wave-status"), "no scenario step left")

    def test_flag_mismatch_or_missing(self):
        step = {"expect": "^/wave-status$", "args": {"--model": "haiku"}}
        self.steps(step, step)
        self.assert_rejected(self.invoke("-p", "/wave-status", "--model", "sonnet"), "expected --model")
        self.assert_rejected(self.invoke("-p", "/wave-status"), "expected --model")

    def test_error_subtype_omits_result(self):
        self.steps({
            "expect": "^/wave-status$", "subtype": "error_max_turns",
            "is_error": True, "exit": 1, "result": "unused {{rev:missing}}",
        })
        completed = self.invoke("-p", "/wave-status")
        self.assertEqual(completed.returncode, 1, completed.stderr)
        output = json.loads(completed.stdout)
        self.assertEqual(output["subtype"], "error_max_turns")
        self.assertIs(output["is_error"], True)
        self.assertNotIn("result", output)


if __name__ == "__main__":
    unittest.main()
