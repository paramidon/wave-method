"""Exercise the Claude print-mode runner with Python stand-ins."""

from __future__ import annotations

import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wavedriver import claude


class ClaudeTest(unittest.TestCase):
    call = claude.Call("wave-run", "plans/x 2", "sonnet", 110, 3.0)
    stop_line = "Stop wave-running: x — next: y"

    def test_command(self):
        settings = claude.Settings(
            claude=["claude"], add_dirs=["plugin folder", "second dir"],
            extra_args=["--verbose"],
        )
        self.assertEqual(
            claude.command(self.call, settings),
            ["claude", "-p", "/wave-run plans/x 2",
             "--output-format", "json", "--permission-mode", "auto",
             "--model", "sonnet", "--max-turns", "110", "--max-budget-usd", "3",
             "--add-dir", "plugin folder", "--add-dir", "second dir", "--verbose"],
        )

    def test_prompt(self):
        settings = claude.Settings(claude=["claude"], skill_prefix="wave-method:")
        self.assertEqual(claude.prompt(self.call, settings), "/wave-method:wave-run plans/x 2")
        call = claude.Call("wave-status", "", "haiku", 60, 0.5)
        self.assertEqual(claude.prompt(call, settings), "/wave-method:wave-status")
        self.assertEqual(claude.both("wave-run plans/x 2"), "`/wave-run plans/x 2` · `$wave-run plans/x 2`")

    def test_parse_stop(self):
        self.assertEqual(
            claude.parse_stop(f"\nStarted: 23:00\n\n{self.stop_line}\n"),
            ("wave-running", self.stop_line, "y"),
        )
        plain_stop = "Stop wave-running: x"
        self.assertEqual(claude.parse_stop(plain_stop), ("wave-running", plain_stop, ""))
        self.assertIsNone(claude.parse_stop("Started: 23:00\nReport\n" + self.stop_line))

    def test_parse_output(self):
        first = {"type": "result", "result": "first"}
        last = {"type": "result", "result": "last"}
        self.assertEqual(claude.parse_output(json.dumps(first)), first)
        self.assertEqual(
            claude.parse_output(f"notice\n{json.dumps(first)}\n{json.dumps(last)}\n{{}}\n"),
            last,
        )
        self.assertEqual(claude.parse_output("[]"), {})

    def test_run_ok_and_raw_output(self):
        code = """
import json, os, sys
assert sys.argv[1:3] == ["-p", "/wave-run plans/x 2"]
assert not sys.stdin.read()
assert os.environ["MSYS_NO_PATHCONV"] == "1"
print(json.dumps({
    "type": "result", "subtype": "success", "is_error": False,
    "result": "Started: 23:00\\nDone", "num_turns": 3, "total_cost_usd": 0.25,
}))
print("diagnostic", file=sys.stderr)
"""
        settings = claude.Settings(claude=[sys.executable, "-c", code])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "raw" / "call.txt"
            result = claude.run(self.call, settings, Path(tmp), raw_path=path)
            raw = path.read_text(encoding="utf-8")
        self.assertEqual(result.outcome, "ok")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.text, "Started: 23:00\nDone")
        self.assertEqual((result.turns, result.cost, result.denials), (3, 0.25, 0))
        self.assertEqual(result.warnings, [])
        self.assertIn("\n--- stderr ---\ndiagnostic\n", raw)

    def test_run_stop(self):
        result = self._run_json(result=f"Started: 23:00\n{self.stop_line}")
        self.assertEqual(result.outcome, "stop")
        self.assertEqual((result.stop_code, result.stop_line, result.next),
                         ("wave-running", self.stop_line, "y"))

    def test_run_errors(self):
        for data, outcome in (
            ({"subtype": "error_max_turns", "errors": ["Reached maximum number of turns"]}, "failed"),
            ({"api_error_status": 429}, "limit"),
            ({"errors": ["Usage limit reached"]}, "limit"),
            ({"api_error_status": 401}, "auth"),
        ):
            with self.subTest(data=data):
                result = self._run_json(exit_code=1, is_error=True, **data)
                self.assertEqual(result.outcome, outcome)
                self.assertEqual(result.exit_code, 1)
                if outcome == "failed":
                    self.assertIn("error_max_turns: Reached maximum number of turns", result.detail)
        self.assertEqual(self._run_json().outcome, "failed")

    def test_run_warnings(self):
        result = self._run_json(result="Continue with the quota report?", permission_denials=[{}, {}])
        self.assertEqual(result.outcome, "ok")
        self.assertEqual(result.denials, 2)
        self.assertEqual(result.warnings, [
            "no Started: line", "2 permission denials", "ends with a question",
        ])

    def test_run_timeout(self):
        code = """
import subprocess, sys, time
subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
print("child started", flush=True)
time.sleep(60)
"""
        settings = claude.Settings(claude=[sys.executable, "-c", code], timeout_s=1)
        with tempfile.TemporaryDirectory() as tmp:
            start = time.monotonic()
            result = claude.run(self.call, settings, Path(tmp))
            elapsed = time.monotonic() - start
        self.assertLess(elapsed, 15)
        self.assertEqual(result.outcome, "timeout")
        self.assertTrue(result.detail.startswith("timeout after "))

    def _run_json(self, exit_code=0, **data):
        payload = {"type": "result", "subtype": "success", "is_error": False, **data}
        code = f"print({json.dumps(payload)!r}); raise SystemExit({exit_code})"
        settings = claude.Settings(claude=[sys.executable, "-c", code])
        with tempfile.TemporaryDirectory() as tmp:
            return claude.run(self.call, settings, Path(tmp))


if __name__ == "__main__":
    unittest.main()
