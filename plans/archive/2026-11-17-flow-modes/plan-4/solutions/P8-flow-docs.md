# P8. Docs, an autonomous example, Flow checks and the changelog for both flows
User problem: README, `examples/` (an autonomous example), `status_check.py` (the new fields) and an `Unreleased`
line in the changelog describe both flows; no version bump, no tag · feature F1

**Cause:** parts 1–3 changed the skills (`skills/wave-plan/layout.md` "Flow", `skills/wave-run/autonomous.md`) and
added the driver (`scripts/wave_driver.py`, `docs/wave-driver.md`), but the user-facing texts know only the manual
flow: `README.md` (Quick start :73, Example plans :149, How it works :195, Requirements :230, Safety rules :259,
Customising :275, Limitations :288), `examples/README.md` (two examples), `status_check.py:8-12` (it reads the three
tables only, not the README header), `skills/wave-plan/CHANGELOG.md:7` (no `Unreleased` line). The release archive
(`.github/workflows/release.yml`, step "Build archives", `paths=…`) leaves out `scripts/`, so a release ships
`docs/wave-driver.md` without the driver.

**Approach:** four disjoint edits, one task each: the README (section A), the example (B), the status check (C),
the changelog with the release files (D). Every fact they state comes from the merged texts named below; they add
no rule. The driver keeps its own `Flow:` parser (`scripts/wavedriver/gitstate.py` `_flow_header`): the check only
reports, and changing the driver is out of scope.

## A. README

Sources to read (facts only, do not copy long passages): `skills/wave-plan/layout.md` sections "Names", "Flow",
"Integration target", "Auto-approval", "Results of an autonomous run", "Decision table", "Planning in autonomous
flow"; `skills/wave-run/autonomous.md` "Flow form"; `docs/wave-driver.md` (all); `docs/claude-print-mode.md`
section "Prompt form for the driver" (title only, for the link).

Edits, in this order of the file; keep the existing style (short sentences, tables with blank lines around them):

1. Intro (lines 5–9): after "→ merges you approve." add one sentence: "In the default manual flow you approve every
   merge; in autonomous flow a whole plan runs unattended, for example overnight, into an integration branch that
   you review and merge in the morning."
2. Contents: add `- [Overnight runs (autonomous flow)](#overnight-runs-autonomous-flow)` right after
   "Quick start".
3. Quick start, "Example plans" (:149): "two complete plans" → "three complete plans"; add a third item:
   `- [`03-autonomous-night-run`](examples/03-autonomous-night-run/) — a plan written in autonomous flow and run
   overnight by the driver: one feature under manual review, a wave that waits for an auto-merged feature.`
4. New section `## Overnight runs (autonomous flow)` between "Quick start" and "Is this another SDLC?", with these
   subsections and content (about 60–80 lines in total):
   - `### Two flows` — a table with columns Flow / Who approves a ready feature / Merged into / Questions, rows
     `manual` (default): you / `main` / at each review point and stop; `autonomous`: `wave-run`, when the five
     conditions of auto-approval hold; you for features under manual review / `integration/<name>` / none. One
     sentence: a plan without a `Flow:` line is in manual flow and behaves exactly as before.
   - `### Choosing the flow` — the commands, each in a fenced block or inline code, Claude Code form only (as the
     rest of the README): `/wave-triage flow autonomous <list>` (the index gets
     `- Flow: autonomous · target: integration/<topic>`, and its parts are planned in autonomous flow);
     `/wave-plan flow autonomous <list>`; `/wave-plan flow autonomous plans/<date>-<topic>/index.md part 2`;
     switching a planned plan between waves: `/wave-run plans/<…> flow autonomous review F2` (F2 stays under
     manual review) and back with `flow manual`, which is refused (`target-unmerged`) while the integration branch
     has commits `main` lacks. In autonomous flow `wave-triage` and `wave-plan` ask nothing: they pick a reading by
     fixed rules and record it as an `Assumed (autonomous, not asked)` line, which you later see under "Worth a
     look" of the feature's review block.
   - `### The integration branch` — `<name>` is the index topic, or the plan slug for a plan from a raw list; all
     parts of an index share it; worktree `../<repo>.worktrees/integration-<name>`; autonomous flow never changes
     `main` or your main checkout; one run at a time writes the branch (a claim ref
     `refs/wave-method/claims/integration/<name>`; a second run stops `wave-running` naming the holder). Then the
     auto-approval list, numbered, in plain words: (1) every task of the feature is done, (2) its check is green after
     the integration branch was merged into it, without changing the feature's own lines, (3) no open problem entry
     concerns it, (4) every task commit names a model of the task's tier, (5) it is not under manual review. A feature
     failing 1–4 becomes ⚠️ blocked with a problem entry; one failing 5 waits for your review. Every other question
     of `wave-run` has a fixed answer: link `skills/wave-plan/layout.md` ("Decision table").
   - `### Running overnight with the driver` — what it is (a Python 3.9+ script, standard library only, that starts
     one headless Claude Code session per step: plan an unplanned index part, run the next wave, run a task waiting
     for task mode, resume); where it is: `scripts/wave_driver.py` of a clone of this repository, or of the plugin
     folder (for example `~/.claude/plugins/cache/wave-method/wave-method/<version>/`) — the installers copy only
     the skills; then the two commands of `docs/wave-driver.md` "Run" (`--dry-run` first), with `--repo`; for a
     plugin install add `--skill-prefix wave-method: --add-dir <plugin folder>`; rails worth setting:
     `--max-usd`, `--deadline`, `--max-calls`; permission mode `auto` by default, `bypassPermissions` only in an
     isolated clone; exit codes 0 / 1 / 2 / 3 as in `docs/wave-driver.md`; it never pushes and ends the run when
     `main`, a remote-tracking ref or the main checkout changes. Links: `docs/wave-driver.md` (all options) and
     `docs/claude-print-mode.md` (how print mode runs the skills).
   - `### In the morning` — numbered steps: 1. open `report.md` in `<repo>.wave-driver/<YYYY-MM-DD-HHMM>/` (its
     last line printed by the driver is `Report: <path>`): merged features with their review blocks, features
     waiting for review, blocked features with their problem entry, halts with their next command, a table of calls
     with their cost; 2. review the whole night as one diff: `git diff main...integration/<name>`; 3. merge it
     yourself in the main checkout: `git merge --no-ff integration/<name>`; 4. a feature under manual review:
     `/wave-run <plan folder> merge F3` (it is merged into the integration branch; merge that branch again);
     5. blocked features: re-plan with `/wave-plan <plan folder>`. `/wave-status` shows the same state, with
     `Merged, not in main:` until you merge. Without the driver, run the same `/wave-run <plan folder> <N>` commands
     yourself: autonomous flow asks nothing in either case.
5. How it works (:195): after the skills table add one sentence: "The overnight driver `scripts/wave_driver.py` is
   not a skill: it chains `wave-plan` and `wave-run` calls in headless sessions (see
   [Overnight runs](#overnight-runs-autonomous-flow))." In the `wave-run` row: "merges the ones you approve into
   `main`" → "merges the ones you approve into `main` (in autonomous flow: approves them itself under fixed
   conditions and merges them into an integration branch)". Key terms table: add rows `flow` (`manual`, the default:
   you approve every merge; `autonomous`: unattended, into an integration branch) and `integration branch`
   (`integration/<name>`: where autonomous flow merges; you review it as one diff and merge it into `main`).
6. Requirements (:230): Python item → "**Python 3.9+** for the overnight driver (standard library only), and
   optionally for the status-check script `wave-plan/scripts/status_check.py`; without Python the check is done by
   reading." Add an item: "**The Claude Code CLI** (`claude`, signed in) for the overnight driver. Autonomous flow
   itself also works in Codex and in interactive sessions; only the driver needs the CLI."
7. Safety rules (:259): bullet 1 → "Nothing is ever committed directly on `main`; it only receives `merge --no-ff`
   of complete features you approved and of the plan's tracking branch. In autonomous flow nothing at all reaches
   `main`: features go to the integration branch, which you merge yourself." Bullet 2 → "A feature is never merged
   into `main` without your approval of that feature: …" (rest unchanged). Add bullets: "Autonomous flow approves a
   feature only under the five conditions of auto-approval, never one under manual review, and never waives the tier
   gate." · "One run at a time writes an integration branch (a claim ref); the driver allows one driver per
   repository (a lock file) and stops when `main`, a remote-tracking ref or the main checkout changes."
8. Customising (:275): add rows `Flow of a plan` → "the README `Flow:` line, written by `wave-plan` and changed with
   `/wave-run <plan folder> flow …`" and `Driver models, caps and rails` → "options of `scripts/wave_driver.py`
   ([docs/wave-driver.md](docs/wave-driver.md))".
9. Limitations (:288): add bullets: "**Autonomous flow and the driver** were rehearsed with Claude Code on Windows
   (`docs/rehearsals/`); the driver needs the Claude Code CLI and has no Codex counterpart." · "**A night run spends
   real usage.** Set `--max-usd`, `--deadline` or `--max-calls`; on a subscription the cost counts toward usage
   limits."

Limits: no other section changes; no version number; `docs/images/*.svg` stay unchanged; the README stays English.
Links are relative and point to files that exist on the branch after F1 (`examples/03-autonomous-night-run/` is
created by task B of the same wave; write the link anyway).

## B. Example 03

Corrected by `solutions/P17-example-03-fixes.md` (re-plan of 2026-11-18): the plan slug and its paths, the check
command and the packaging of `pyproject.toml`. Read both; where they differ, P17 wins.

Folder `examples/03-autonomous-night-run/`, the plan exactly as `/wave-plan flow autonomous` writes it before any
wave ran, in the current templates (`skills/wave-plan/templates.md`): `README.md`, `solutions/P1-word-counter.md`,
`solutions/P2-top-words-cli.md`, `solutions/lite.md`, `waves/w01.md`, `waves/w02.md`. It must be runnable: the
end-to-end test (task F of this plan) copies it into an empty repository and runs it, so every prompt must be
complete and exact.

### The user's list (for `examples/README.md`)

```
/wave-plan flow autonomous a Python package "wordstat" that counts the words of a text file, case-insensitive; a
command "wordstat <file> --top N" that prints the most frequent words; a README with install and usage, which I want
to read myself before it lands; export the counts as CSV for spreadsheets
```

### README header

```
# Word statistics in Python, planned for a night run

- Plan: `plans/2026-11-04-wordstat/` · slug: `wordstat` · tracking branch: `plan/wordstat` · created 2026-11-04 · base: 7d2e9b1 · planned 2026-11-04 18:02 – 2026-11-04 18:14
- Re-plans: none
- Flow: autonomous · target: integration/wordstat · manual review: F3
```

### Features, waves, tasks

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for |
|---|---|---|---|---|---|---|---|
| F1 | `word-counter` | Count the words of a text | P1 | A (1) | `python -m pytest -q` green: `tests/test_core.py` (7 cases) | ⬜ | wave 1 |
| F2 | `top-words-cli` | Command `wordstat <file> --top N` | P2 | B (2) | `tests/test_cli.py` (5 cases) green | ⬜ | wave 2 |
| F3 | `usage-readme` | README with install and usage | P3 | C (1) | README shows install, the command, an example session and the library calls | ⬜ | wave 1 |
| F4 | `csv-export` | Word counts as CSV | P4 | D (2) | `tests/test_export.py` (3 cases) green | ⬜ | wave 2 |

The README Features table has the template's ten columns (Branch and Merged empty). Waves: 1 → A, C; 2 → B, D.
Tasks: A `word-counter-core` F1 wave 1 medium; B `top-words-command` F2 wave 2 medium; C `usage-readme` F3 wave 1
low; D `csv-export` F4 wave 2 low. All ⬜.

User problems: P1 count the words of a text, case-insensitive → F1 · `solutions/P1-word-counter.md`; P2 a command
`wordstat <file> --top N` printing the most frequent words → F2 · `solutions/P2-top-words-cli.md`; P3 a README with
install and usage, which the user reads before it lands → F3 · `solutions/lite.md` (low); P4 the counts as CSV →
F4 · `solutions/lite.md` (low).

How to try: F1 — `python -c "from wordstat.core import count_words, top_words; print(top_words(count_words('b a b c a b'), 2))"`
→ `[('b', 3), ('a', 2)]`; before: no package. F2 — `wordstat poem.txt --top 3` → three lines `<word> <count>`;
before: no command. F3 — open `README.md` → install, the command with its output, an example session and the
library calls; before: only `LICENSE`. F4 — `python -c "from wordstat.export import to_csv; print(to_csv([('the', 2)]), end='')"`
→ `word,count` and `the,2`; before: no export.

Known test failures before start: `- None: the repository is empty except for LICENSE.`

Assumptions (in this order):

- Python 3.10+, standard library only at run time; `pytest` for tests.
- `- Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only`
- `- Assumed (autonomous, not asked) · F2: what does --top default to? → 10; not chosen: every word`
- F3 is under manual review because the user asked to read it first: after the night it waits as `👀 review`.
- Wave 2 depends on `F1 merged` (B uses `wordstat.core`, D adds a module to the `wordstat` package). In autonomous
  flow `wave-run` merges F1 into `integration/wordstat` after wave 1 without asking, so wave 2 runs the same night;
  in manual flow it would stop `feature-unmerged` until the user merged F1.

### `solutions/P1-word-counter.md` (medium)

- Cause: new code. Approach: one module `wordstat/core.py`, pure functions, no I/O; `wordstat/__init__.py` is a
  one-line docstring `"""Word statistics."""`.
- API (verbatim):

  ```python
  WORD = re.compile(r"[^\W_]+(?:'[^\W_]+)*")

  def count_words(text: str) -> Counter[str]: ...
  def top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]: ...
  ```

  with `from collections import Counter` and `from __future__ import annotations`.
- Algorithm: `count_words` returns `Counter(WORD.findall(text.lower()))`. `top_words` raises
  `ValueError("n must be at least 1")` when `n < 1`, else returns `sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]`.
- Limits: apostrophes inside a word stay (`don't`); leading and trailing ones are dropped; underscores split words.
- Acceptance tests (`tests/test_core.py`, 7 cases): 1. `count_words("The cat and the hat.")` == `Counter({"the": 2, "cat": 1, "and": 1, "hat": 1})`;
  2. `count_words("Don't stop: don't!")` == `Counter({"don't": 2, "stop": 1})`; 3. `count_words("")` == `Counter()`;
  4. `count_words("route 66, Route 66")` == `Counter({"route": 2, "66": 2})`; 5. `top_words(count_words("b a b c a b"), 2)`
  == `[("b", 3), ("a", 2)]`; 6. `top_words(Counter({"y": 1, "x": 1}), 5)` == `[("x", 1), ("y", 1)]`;
  7. `top_words(Counter(), 0)` raises `ValueError`.

### `solutions/P2-top-words-cli.md` (medium)

- Approach: `wordstat/cli.py` with argparse, `wordstat/__main__.py` for `python -m wordstat`, `pyproject.toml` for
  the console script; it reads the file and calls `wordstat.core` only.
- API: `def main(argv: list[str] | None = None) -> int` (with `from __future__ import annotations`); argparse
  `prog="wordstat"`, positional `file`, option `--top` (`type=int`, `default=10`). `wordstat/__main__.py`:
  `import sys` / `from wordstat.cli import main` / `sys.exit(main())`. `pyproject.toml`: `[project]` name
  `"wordstat"`, version `"0.1.0"`, `requires-python = ">=3.10"`; `[project.scripts]` `wordstat = "wordstat.cli:main"`;
  `[build-system]` `requires = ["setuptools>=61"]`, `build-backend = "setuptools.build_meta"`.
- Behaviour table:

  | Input | stdout | stderr | Exit |
  |---|---|---|---|
  | `wordstat notes.txt`, the file holds `the cat the` | `the 2` and `cat 1`, one per line | — | 0 |
  | `wordstat notes.txt --top 1` | `the 2` | — | 0 |
  | `wordstat empty.txt`, an empty file | nothing | — | 0 |
  | `wordstat missing.txt` | nothing | `error: cannot read missing.txt` | 1 |
  | `wordstat notes.txt --top 0` | nothing | `error: --top must be at least 1` | 2 |

- Algorithm: check `--top` first (`< 1` → the stderr line, return 2); read with
  `Path(args.file).read_text(encoding="utf-8")`; `OSError` or `UnicodeDecodeError` → the stderr line with the path as
  given, return 1; print `f"{word} {count}"` for each pair of `top_words(count_words(text), args.top)`; return 0.
- Acceptance tests (`tests/test_cli.py`, 5 cases, one per table row): `tmp_path`, `monkeypatch.chdir(tmp_path)`,
  `capsys`; call `main([...])` directly.

### `solutions/lite.md` (low)

- `## P3. README with install and usage` — **Edit:** new `README.md`: one-line description; install
  `pip install .`; usage `wordstat <file> [--top N]` (default 10) with the outputs of `solutions/P2-top-words-cli.md`
  "Behaviour"; an example session: a file `poem.txt` holding `the sun and the sea and the sky`, then
  `wordstat poem.txt --top 3` printing `the 3`, `and 2`, `sea 1`; a "Library" part with `count_words`, `top_words`
  (`wordstat.core`) and `to_csv` (`wordstat.export`). · **Check:** the README contains `pip install .`,
  `wordstat poem.txt --top 3`, `count_words` and `to_csv`, and the example output matches P1's ordering rule.
- `## P4. Counts as CSV` — **Edit:** new `wordstat/export.py` with
  `def to_csv(pairs: list[tuple[str, int]]) -> str` (with `from __future__ import annotations`): `csv.writer` on an
  `io.StringIO` with `lineterminator="\n"`, header row `word,count`, one row per pair; new `tests/test_export.py`
  with 3 cases: `to_csv([])` == `"word,count\n"`; `to_csv([("the", 2), ("cat", 1)])` == `"word,count\nthe,2\ncat,1\n"`;
  `to_csv([("a,b", 1)])` == `'word,count\n"a,b",1\n'`. · **Check:** `python -m pytest -q tests/test_export.py` → 3 passed.

### Waves

- `waves/w01.md`: tasks A (files new `wordstat/__init__.py`, new `wordstat/core.py`, new `tests/test_core.py`) and C
  (new `README.md`); `Depends on: nothing.`; disjoint: A writes under `wordstat/` and `tests/`, C only `README.md`.
- `waves/w02.md`: tasks B (new `wordstat/cli.py`, new `wordstat/__main__.py`, new `tests/test_cli.py`, new
  `pyproject.toml`) and D (new `wordstat/export.py`, new `tests/test_export.py`); `Depends on: wave 1, F1 merged
  (B calls wordstat.core; D adds a module to the wordstat package that A creates).`; disjoint: no common file.
- Prompts follow `skills/wave-plan/SKILL.md` step 7 and the style of `examples/01-greenfield-todo-cli/waves/`: A and B
  start with the gate line `Required tier: medium — Sonnet 5.5 / GPT-6.1 SOL or stronger. Stop if this session runs a
  weaker model.`; C and D have none (low). Every prompt names its files ("change only …"), the English rule line, the
  goal with its feature, the solution file and section to read, the API and formulas above, the acceptance cases, the
  check command `python -m pytest -q` with "no known failures", and the stop rule ("If the plan's solution does not
  work …, do not invent another one: stop and describe the problem in the report").
- Each wave file ends with the template's `## Execution` and `## Closed problems` sections, unfilled.

### `examples/README.md`

- Intro: "Two small plans" → "Three small plans"; table row
  `| [`03-autonomous-night-run/`](03-autonomous-night-run/) | an empty repository, autonomous flow | the `Flow:` line, assumed readings, a feature under manual review, a wave that waits for an auto-merged feature |`.
- New section `## 03 — a night run in autonomous flow` after section 02: the user's list above; what `wave-plan`
  writes (the `Flow:` line, the two `Assumed` lines, four features, two waves); the night:
  `python <wave-method>/scripts/wave_driver.py plans/2026-11-04-wordstat --repo . --dry-run` and the same without
  `--dry-run` with `--max-usd 10`; what happens: wave 1 runs A and C; F1 is auto-approved and merged into
  `integration/wordstat`; F3 waits for review (manual review); wave 2 starts because F1 is merged, runs B and D; F2
  and F4 are auto-merged; `main` is unchanged. The morning: `report.md` shows F1, F2, F4 as merged blocks and F3 with
  its merge command; then `/wave-run plans/2026-11-04-wordstat merge F3`, `git diff main...integration/wordstat`,
  `git merge --no-ff integration/wordstat`. Without the driver: `/wave-run plans/2026-11-04-wordstat 1` and `2`,
  each in a fresh session; no question is asked.
- "Checking an example": "Both plans" → "All three plans", and add
  `python skills/wave-plan/scripts/status_check.py examples/03-autonomous-night-run`.

## C. Status check

`skills/wave-plan/scripts/status_check.py` learns the README header field `Flow:` (`layout.md`, "Flow"). The line
must have exactly the form that `wave-plan` and the flow form write, because `layout.md` ("Integration target",
"Plans of a target") finds the plans of a target with
`git grep -E "^- Flow: autonomous · target: integration/<name>( ·|$)"`: a line with backticks, another order or
other spacing hides its plan from that search. New code, Python 3.9-compatible like the rest of the file:

```python
FLOW = re.compile(r"- Flow: (manual|autonomous(?: · target: (integration/[A-Za-z0-9][A-Za-z0-9._-]*))?"
                  r"(?: · manual review: (F\d+(?:, F\d+)*))?)")


def flow(lines, report):
    """Return (flow, target, manual_review, line) of the README header; report malformed Flow lines."""
```

Algorithm:

1. The header is `lines` up to the first line that starts with `## `. Flow lines are header lines that start with
   `- Flow:` (after `rstrip()`). None → return `("manual", None, [], 0)`.
2. Every Flow line after the first: `report(line, "flow-line", "more than one Flow line")`. Only the first is read.
3. The first Flow line fullmatches `FLOW` → return `("manual", None, [], line)` for `manual`, else
   `("autonomous", <group 2 or None>, <IDs of group 3 split on ", ", or []>, line)`.
4. Otherwise `report(line, "flow-line", "expected '- Flow: manual' or '- Flow: autonomous · target:
   integration/<name> · manual review: <F-IDs>', found '<the line>'")` and return `("manual", None, [], line)`.

`line` is 1-based, like every other reported line. In `check()`: call `flow()` on the README lines with the same
`report` lambda as `tables()`; then for each ID of `manual_review` that is not an `ID` of the Features table:
`report(readme, line, "flow-review-unknown", "manual review names missing feature <ID>")`. Return codes stay:
violations → 1. The driver keeps its own parser and does not call `flow()`.

Tests in `skills/wave-plan/scripts/test_status_check.py`, in its style (`run_check`, `assert_rule` expects exactly
one violation line). README fixtures get a header line by replacing `"# Test plan\n"` with
`"# Test plan\n\n- Flow: …\n"`:

| Test | Flow line | Expected |
|---|---|---|
| `test_flow_manual` | `- Flow: manual` | exit 0, no output |
| `test_flow_autonomous` | `- Flow: autonomous · target: integration/test-plan · manual review: F1` | exit 0, no output |
| `test_flow_autonomous_default_target` | `- Flow: autonomous` | exit 0 |
| `test_flow_backticks` | ``- Flow: autonomous · target: `integration/test-plan` `` | `flow-line` |
| `test_flow_unknown` | `- Flow: autonomus` | `flow-line` |
| `test_flow_bad_target` | `- Flow: autonomous · target: main` | `flow-line` |
| `test_flow_manual_fields` | `- Flow: manual · target: integration/x` | `flow-line` |
| `test_flow_unknown_field` | `- Flow: autonomous · target: integration/x · colour: blue` | `flow-line` |
| `test_flow_order` | `- Flow: autonomous · manual review: F1 · target: integration/x` | `flow-line` |
| `test_flow_twice` | `- Flow: manual` and `- Flow: autonomous` on two lines | `flow-line` (one line) |
| `test_flow_review_unknown` | `- Flow: autonomous · manual review: F9` | `flow-review-unknown` |
| `test_flow_outside_header` | `- Flow: autonomus` in a `## Assumptions` section at the end | exit 0 |

`skills/wave-plan/layout.md`, "Statuses", the paragraph "**Status check**": after its first sentence ("… no open
entry whose items are all ✅ or ➖.") add: "It also checks the README `Flow:` line (\"Flow\"): `flow-line` for a
malformed line, `flow-review-unknown` for a `manual review:` ID that is not a feature." Nothing else in `layout.md`.

## D. Changelog and release files

1. `skills/wave-plan/CHANGELOG.md`: insert right before the `- v2.12.0 (2026-11-16) — …` item (after the
   introductory paragraph and its blank line), keeping the two-space continuation indent and lines of at most 118
   characters:

   ```
   - Unreleased — a second flow, `autonomous`, next to the default `manual` one (`layout.md`, "Flow"). A README line
     `- Flow: autonomous · target: integration/<name> · manual review: <F-IDs>` lets `wave-run` approve a ready
     feature itself when all its tasks are done, its check is green after merging the target, no open entry
     concerns it, its commits pass the tier gate and it is not under manual review, and merge it into the
     integration branch `integration/<name>` instead of the main branch, which autonomous flow never changes. Every
     question of `wave-run` has a fixed answer (new `wave-run/autonomous.md`); the flow form
     `/wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` switches it between waves. `wave-triage`
     and `wave-plan` take `flow autonomous` as their first words and record assumed readings instead of asking; the
     parts of an index share one integration branch, a later part is planned against it, and a claim ref
     `refs/wave-method/claims/integration/<name>` lets one run at a time write it. Reports and `wave-status` show
     the flow and every merged feature with its review block until the integration branch is merged. New
     `scripts/wave_driver.py` (Python 3.9+, standard library only) runs an index or a plan overnight as headless
     Claude Code sessions with rails, a lock and a guard, never pushes, and writes a morning report
     (`docs/wave-driver.md`; print-mode findings in `docs/claude-print-mode.md`). `status_check.py` checks the
     `Flow:` line (`flow-line`, `flow-review-unknown`); new example `examples/03-autonomous-night-run/`; release
     archives include `scripts/`. A plan without a `Flow:` line behaves as before.
   ```

2. `.github/workflows/release.yml`, step "Build archives": `paths="skills install.sh install.ps1 LICENSE README.md
   docs .claude-plugin"` → `paths="skills scripts install.sh install.ps1 LICENSE README.md docs .claude-plugin"`.
   Nothing else in the file.
3. `CONTRIBUTING.md`, "Run the checks": replace the fenced block's lines with

   ```bash
   python skills/wave-plan/scripts/test_status_check.py
   python -m unittest discover -s scripts/tests
   for plan in examples/*/; do python skills/wave-plan/scripts/status_check.py "${plan%/}"; done
   git diff --check
   ```

No version is bumped and no tag is created (`.claude-plugin/plugin.json` stays unchanged).

## Acceptance tests

1. `python skills/wave-plan/scripts/test_status_check.py` → 32 tests OK (20 existing + 12 of section C).
2. `for p in examples/*/; do python skills/wave-plan/scripts/status_check.py "${p%/}"; done` → every call exits 0
   on the feature branch with all four tasks merged (example 03 with the new Flow rules).
3. Example 03 with its Flow line changed to `- Flow: autonomus` (a scratch copy) → exit 1 and exactly one line
   `…README.md:5: flow-line: expected …, found '- Flow: autonomus'`.
4. `python -m unittest discover -s scripts/tests` → 59 tests OK (the driver still imports `status_check`).
5. `git diff --check` clean; `git grep -n "^- Unreleased" -- skills/wave-plan/CHANGELOG.md` → exactly one line,
   before `v2.12.0`; `git diff main -- .claude-plugin` empty.
6. README: `git grep -n -e "integration/<name>" -e "wave_driver.py" -e "03-autonomous-night-run" -- README.md`
   finds each; every relative link of the new section resolves to an existing path on the feature branch.
