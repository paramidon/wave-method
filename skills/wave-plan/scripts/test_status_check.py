"""Run with python <wave skills folder>/wave-plan/scripts/test_status_check.py."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("status_check.py")
README = """# Test plan

## Features

| ID | Status | Waiting for | Merged |
|---|---|---|---|
| F1 | ✅ merged | | abc123 |

## Waves

| Wave | Status |
|---|---|
| 1 | ✅ |

## Tasks

| ID | Status |
|---|---|
| A | ✅ |
"""
PROBLEMS = "# Open problems\nNext ID: I3\n"


class StatusCheckTest(unittest.TestCase):
    def run_check(self, readme=README, problems=PROBLEMS):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            if readme is not None:
                (folder / "README.md").write_text(readme, encoding="utf-8")
            if problems is not None:
                (folder / "problems.md").write_text(problems, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), directory], capture_output=True,
                encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
        if result.returncode != 2:
            self.assertEqual("", result.stderr)
        return result

    def assert_rule(self, rule, readme=README, problems=PROBLEMS):
        result = self.run_check(readme, problems)
        self.assertEqual(1, result.returncode, result.stdout)
        lines = result.stdout.splitlines()
        self.assertEqual(1, len(lines), result.stdout)
        self.assertRegex(lines[0], r"(README|problems)\.md:\d+: " + rule + r": .+")

    def test_clean(self):
        result = self.run_check()
        self.assertEqual((0, ""), (result.returncode, result.stdout))

    def test_red_without_entry(self):
        self.assert_rule("red-without-entry", README.replace("| A | ✅ |", "| A | ⚠️ |"))

    def test_entry_names_closed(self):
        problems = PROBLEMS + (
            "- **[I1 · task A]** status: open\n"
            "- **[I2 · task A]** status: closed\n")
        self.assert_rule("entry-names-closed",
                         README.replace("| A | ✅ |", "| A | ⚠️ I1, I2 |"), problems)

    def test_entry_all_done(self):
        self.assert_rule("entry-all-done", problems=PROBLEMS + (
            "- **[I1 · wave 1, task A, feature F1]** status: open\n"))

    def test_merged_fields(self):
        self.assert_rule("merged-fields", README.replace("| | abc123 |", "| pending | |"))

    def test_waiting_missing(self):
        self.assert_rule("waiting-missing", README.replace("✅ merged", "⬜"))

    def test_review_feature(self):
        readme = README.replace("| F1 | ✅ merged | | abc123 |", "| F1 | 👀 review | review | |")
        result = self.run_check(readme)
        self.assertEqual((0, ""), (result.returncode, result.stdout))
        self.assert_rule("waiting-missing", readme.replace("| review | |", "| | |"))

    def test_next_id(self):
        self.assert_rule("next-id", problems=PROBLEMS + (
            "- **[I3 · task A]** status: closed\n"))

    def test_row_cells(self):
        self.assert_rule("row-cells", README.replace("| A | ✅ |", "| A | ✅ | extra |"))

    def test_missing_readme(self):
        result = self.run_check(None)
        self.assertEqual(2, result.returncode)

    def test_extra_columns_without_waiting_for(self):
        readme = README.replace(" | Waiting for", "").replace(
            "|---|---|---|---|", "|---|---|---|").replace(
            "| F1 | ✅ merged | | abc123 |", "| F1 | ✅ merged | abc123 |")
        readme = readme.replace("| Wave | Status |", "| Wave | Notes | Status |").replace(
            "| 1 | ✅ |", "| 1 | first wave | ✅ |")
        readme = readme.replace("## Waves\n\n| Wave | Notes | Status |\n|---|---|",
                                "## Waves\n\n| Wave | Notes | Status |\n|---|---|---|")
        result = self.run_check(readme)
        self.assertEqual((0, ""), (result.returncode, result.stdout))

    def test_missing_required_table(self):
        result = self.run_check(README.replace("## Tasks", "## Something else"))
        self.assertEqual(2, result.returncode)

    def test_invalid_separator(self):
        result = self.run_check(README.replace("|---|---|", "|not a separator|---|"))
        self.assertEqual(2, result.returncode)

    def test_escaped_pipe(self):
        result = self.run_check(README.replace("abc123", r"abc\|123"))
        self.assertEqual((0, ""), (result.returncode, result.stdout))

    def test_open_arrow_and_last_continuation_status(self):
        problems = PROBLEMS + (
            "- **[I1 · task Z]** status: closed\n"
            "  status: → tasks A, B\n")
        result = self.run_check(README.replace("| A | ✅ |", "| A | ⚠️ I1 |"), problems)
        self.assertEqual((0, ""), (result.returncode, result.stdout))

    def test_arrow_concerned_items(self):
        self.assert_rule("entry-all-done", problems=PROBLEMS + (
            "- **[I1 · review]** status: → task A\n"))

    def test_missing_concerned_item(self):
        result = self.run_check(problems=PROBLEMS + (
            "- **[I1 · task Z]** status: open\n"))
        self.assertEqual((0, ""), (result.returncode, result.stdout))

    def test_rerun_wave_exempt(self):
        result = self.run_check(README.replace("| 1 | ✅ |", "| 1 | ❌ re-run |"))
        self.assertEqual((0, ""), (result.returncode, result.stdout))

    def test_first_status_mark(self):
        result = self.run_check(README.replace("| A | ✅ |", "| A | ✅ (was ⚠️ I99) |"))
        self.assertEqual((0, ""), (result.returncode, result.stdout))

    def test_optional_problems(self):
        result = self.run_check(problems=None)
        self.assertEqual((0, ""), (result.returncode, result.stdout))


if __name__ == "__main__":
    unittest.main()
