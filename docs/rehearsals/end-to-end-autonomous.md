# Rehearsal: autonomous flow end to end

2026-11-18 · Claude Code 2.1.326 · source commit 6a8bc07

## Setup

Run from the source worktree in Git Bash. Claude Code was signed in. All targets of the commands below are disposable.

```bash
scratch=$(mktemp -d) # <scratch>
working=$PWD # <working folder>
plan=plans/2026-11-04-wordstat-cli
mkdir "$scratch/logs"
git -C "$working" for-each-ref --format='%(refname) %(objectname)' > "$scratch/logs/working.before.refs"
python -m venv "$scratch/venv"
"$scratch/venv/Scripts/python" -m pip install pytest pyyaml
export PATH="$scratch/venv/Scripts:$PATH"
git init -b main "$scratch/night"
git -C "$scratch/night" config user.name "wave e2e"
git -C "$scratch/night" config user.email "e2e@example.invalid"
printf 'MIT\n' > "$scratch/night/LICENSE"
git -C "$scratch/night" add LICENSE
git -C "$scratch/night" commit -qm init
sh "$working/install.sh" "$scratch/night" --no-codex
git -C "$scratch/night" add .claude
git -C "$scratch/night" commit -qm "install wave skills"
mkdir -p "$scratch/night/plans"
cp -r "$working/examples/03-autonomous-night-run" "$scratch/night/$plan"
git -C "$scratch/night" add plans
git -C "$scratch/night" commit -qm "add plan"
git -C "$scratch/night" branch plan/wordstat-cli
mkdir "$scratch/night/tests"
cat > "$scratch/night/tests/test_forced_red.py" <<'PY'
"""Forced failure of the end-to-end run: red as soon as wordstat.export exists."""
import pytest


def test_forced_red():
    pytest.importorskip("wordstat.export")
    assert False, "forced red: end-to-end run"
PY
git -C "$scratch/night" add tests/test_forced_red.py
git -C "$scratch/night" commit -qm "Seed forced red test"
git init --bare "$scratch/origin.git"
git -C "$scratch/night" remote add origin "$scratch/origin.git"
git -C "$scratch/night" push -q -u origin main
git -C "$scratch/origin.git" for-each-ref > "$scratch/logs/origin.before.refs"
cd "$scratch/night"
python -m pytest -q
python "$working/skills/wave-plan/scripts/status_check.py" "$plan"
```

The seed test produced 1 skipped (exit 0), and the plan's status checker exited 0 without output. The wave 1 result reports that a nested shell resolved system Python without pytest and that the coordinator used the seeded scratch venv for its checks.

## Runs

### A1

```bash
python "<working folder>/scripts/wave_driver.py" plans/2026-11-04-wordstat-cli \
  --repo "<scratch>/night" --dry-run --claude-arg=--setting-sources --claude-arg=project,local
```

- Pass. Exit 0. The driver selected wave 1 and printed a Claude command for `/wave-run plans/2026-11-04-wordstat-cli 1` with `--model sonnet` and `--setting-sources project,local`.

### A2

```bash
python "<working folder>/scripts/wave_driver.py" plans/2026-11-04-wordstat-cli \
  --repo "<scratch>/night" --claude-arg=--setting-sources --claude-arg=project,local \
  --max-usd 20 --max-calls 12
```

- Pass. Exit 0. The driver printed `Report: <scratch>/night.wave-driver/2026-11-18-1726/report.md` and made three calls in `auto`: wave 1, wave 2, and `wave-status`. All calls reported zero permission denials.
- Pass. F1 (`22a272d`) and F2 (`2e3ea57`) were auto-approved. F3 waited for review. F4 and task D remained blocked on open entry I1. Task D's three tests passed on their own. The full F4 check returned 1 failed and 10 passed because `tests/test_forced_red.py::test_forced_red` ran once `wordstat.export` existed (`calls/02-wave.json`).
- Finding. The autonomous step 5 rule calls for recording out-of-scope direct work, reverting it and blocking the feature. The coordinator instead reported that task A committed `wordstat/__pycache__/*.pyc` (`3d2f31f`), removed those files in `274b554`, omitted a problem entry and auto-approved F1 (`calls/01-wave.json`, `skills/wave-run/autonomous.md:91`).
- Intermediate recovery. Wave 2 reported correcting nested scratch worktree paths before dispatching its tasks (`calls/02-wave.json`).

The saved A2 `report.md`, with machine paths replaced by `<scratch>`.

`````markdown
# Wave driver report · 2026-11-18 17:33

- Repository: `<scratch>/night` · main branch: `main` · start: `plans/2026-11-04-wordstat-cli`
- Run: 2026-11-18 17:26 – 2026-11-18 17:33 (6 min) · ended: nothing left to run
- Calls: 3 (plan 0, wave 2, task 0, resume 0, status 1) · failed: 0 · turns: 32 · cost: 1.45 USD (total_cost_usd) · Claude minutes: 6.3
- Options: plan-model: opus · run-model: sonnet · status-model: haiku · low-model: haiku · medium-model: sonnet · high-model: opus · cap: [] · max-calls: 12 · max-failures: 3 · max-usd: 20.0 · call-timeout-min: 120 · permission-mode: auto · skill-prefix:  · add-dir: [] · claude-arg: ['--setting-sources', 'project,local'] · no-status: False · dry-run: False
- Log: `<scratch>/night.wave-driver/2026-11-18-1726/driver.log`

## Integration targets

- `integration/wordstat-cli` · worktree `<scratch>/night.worktrees/integration-wordstat-cli` · 12 commits not in `main`

## Merged, not in main

**F1 · Count the words of a text** · merged into `integration/wordstat-cli` `22a272d` · `<scratch>/night.worktrees/integration-wordstat-cli`
Before: no package. After: `wordstat.core` counts words of a text case-insensitively and ranks the most frequent ones.
How to test:
1. `python -c "from wordstat.core import count_words, top_words; print(top_words(count_words('b a b c a b'), 2))"` → `[('b', 3), ('a', 2)]`
Worth a look: Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, not under manual review

**F2 · Command `wordstat <file> --top N`** · merged into `integration/wordstat-cli` `2e3ea57` · `<scratch>/night.worktrees/integration-wordstat-cli`
Before: no command. After: `wordstat <file> --top N` (or `python -m wordstat`) prints the N most frequent words as `<word> <count>` lines, default 10, with clear errors for an unreadable file or a bad `--top`.
How to test:
1. Put `the cat the` in `notes.txt`, run `python -m wordstat notes.txt --top 1` → `the 2`
2. `python -m wordstat missing.txt` → `error: cannot read missing.txt` on stderr, exit code 1
3. `python -m wordstat notes.txt --top 0` → `error: --top must be at least 1` on stderr, exit code 2
Worth a look: Assumed (autonomous, not asked) · F2: what does --top default to? → 10; not chosen: every word
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, not under manual review

## Ready for review

**F3 · README with install and usage** · `feat/wordstat-cli/F3-usage-readme` · `<scratch>/night.worktrees/wordstat-cli-F3`
Before: only `LICENSE`. After: a README with install, the `wordstat <file> [--top N]` command, an example session and the library calls.
How to test:
1. Open `README.md` → install, the command with its output table, the `poem.txt` example (`the 3`, `and 2`, `sea 1`) and the Library section
Worth a look: The README documents the command (feature F2) and `to_csv` (feature F4), which land in wave 2; the library example was not executed and its output was written by hand. The README does not define what a "word" is. Manual review was requested by the user.
Merge: `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`

## Blocked and waiting

- `plans/2026-11-04-wordstat-cli` F4 Word counts as CSV — ⚠️ I1: Seeded `tests/test_forced_red.py::test_forced_red` fails as soon as `wordstat.export` exists, so F4's full check is red (1 failed, 10 passed) although D's own 3 tests pass
- `plans/2026-11-04-wordstat-cli` — finished

## Halts

none

## Open problems

- `plans/2026-11-04-wordstat-cli` I1 · wave 2 / task D / feature F4: Seeded `tests/test_forced_red.py::test_forced_red` fails as soon as `wordstat.export` exists, so F4's full check is red (1 failed, 10 passed) although D's own 3 tests pass — open

## Status check

none

## Calls

| # | Time | Kind | Unit | Prompt | Model | Outcome | Exit | Turns | USD | Min | Denials | Stop or detail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 17:27:00 | wave | plans/2026-11-04-wordstat-cli | /wave-run plans/2026-11-04-wordstat-cli 1 | sonnet | ok | 0 | 12 | 0.72 | 2.8 | 0 |  |
| 2 | 17:29:46 | wave | plans/2026-11-04-wordstat-cli | /wave-run plans/2026-11-04-wordstat-cli 2 | sonnet | ok | 0 | 13 | 0.72 | 2.9 | 0 |  |
| 3 | 17:32:42 | status | plans/2026-11-04-wordstat-cli | /wave-status plans/2026-11-04-wordstat-cli | haiku | ok | 0 | 7 | 0.01 | 0.6 | 0 |  |

## Next

1. review `git diff main...integration/wordstat-cli`, then merge it in the main checkout: `git merge --no-ff integration/wordstat-cli`
2. review `feat/wordstat-cli/F3-usage-readme`, then `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`
3. re-plan the open problems I1: `/wave-plan plans/2026-11-04-wordstat-cli` · `$wave-plan plans/2026-11-04-wordstat-cli`

## wave-status

````
Started: 2026-11-18 17:32

## plans/2026-11-04-wordstat-cli · `wordstat-cli` · autonomous · target: integration/wordstat-cli · manual review: F3

- Tracking branch: `plan/wordstat-cli` present
- Features: 4 — 2 ✅ merged · 1 👀 review · 1 ⚠️

| Feature | Status | Tasks | Waiting for | Branch | Merged |
|---|---|---|---|---|---|
| F1 Count the words of a text | ✅ merged | 1/1 | | `feat/wordstat-cli/F1-word-counter` | 22a272d |
| F2 Command `wordstat <file> --top N` | ✅ merged | 1/1 | | `feat/wordstat-cli/F2-top-words-cli` | 2e3ea57 |
| F3 README with install and usage | 👀 review | 1/1 | review | `feat/wordstat-cli/F3-usage-readme` | |
| F4 Word counts as CSV | ⚠️ blocked I1 | 0/1 · ⚠️ D | I1 | `feat/wordstat-cli/F4-csv-export` | |

- Waves: 1 ✅ · 2 ⚠️ (done, open problems) · none running

Merged, not in main:

**F1 · Count the words of a text** · merged into `integration/wordstat-cli` `22a272d` · `<scratch>/night.worktrees/integration-wordstat-cli`
Before: no package. After: `wordstat.core` counts words of a text case-insensitively and ranks the most frequent ones.
How to test:
1. `python -c "from wordstat.core import count_words, top_words; print(top_words(count_words('b a b c a b'), 2))"` → `[('b', 3), ('a', 2)]`
Worth a look: Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only
Approved: auto

**F2 · Command `wordstat <file> --top N`** · merged into `integration/wordstat-cli` `2e3ea57` · `<scratch>/night.worktrees/integration-wordstat-cli`
Before: no command. After: `wordstat <file> --top N` (or `python -m wordstat`) prints the N most frequent words as `<word> <count>` lines, default 10, with clear errors for an unreadable file or a bad `--top`.
How to test:
1. Put `the cat the` in `notes.txt`, run `python -m wordstat notes.txt --top 1` → `the 2`
2. `python -m wordstat missing.txt` → `error: cannot read missing.txt` on stderr, exit code 1
3. `python -m wordstat notes.txt --top 0` → `error: --top must be at least 1` on stderr, exit code 2
Worth a look: Assumed (autonomous, not asked) · F2: what does --top default to? → 10; not chosen: every word
Approved: auto

Ready for review:

**F3 · README with install and usage** · `feat/wordstat-cli/F3-usage-readme` · `<scratch>/night.worktrees/wordstat-cli-F3`
Before: only `LICENSE`. After: a README with install, the `wordstat <file> [--top N]` command, an example session and the library calls.
How to test:
1. Open `README.md` → install, the command with its output table, the `poem.txt` example (`the 3`, `and 2`, `sea 1`) and the Library section
Worth a look: The README documents the command (feature F2) and `to_csv` (feature F4), which land in wave 2; the library example was not executed and its output was written by hand. The README does not define what a "word" is. Manual review was requested by the user.
Merge: `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`

- Integration: `integration/wordstat-cli` — 12 commits not in `main`; review `git diff main...integration/wordstat-cli`, then merge it yourself in the main checkout (`git merge --no-ff integration/wordstat-cli`)
- Last stop: none recorded
- Next: `/wave-plan plans/2026-11-04-wordstat-cli` · `$wave-plan plans/2026-11-04-wordstat-cli` (open entry I1 needs a re-plan: F4's seeded `tests/test_forced_red.py` fails once `wordstat.export` exists)

Started: 2026-11-18 17:32 · Finished: 2026-11-18 17:33 (1 min)
````
`````

### A3

```bash
cd "<scratch>/night"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-04-wordstat-cli merge F3" \
  --output-format stream-json --verbose --permission-mode bypassPermissions \
  --setting-sources project,local --model sonnet --max-turns 100 --max-budget-usd 3 \
  < /dev/null > "<scratch>/logs/night.A3.jsonl" 2> "<scratch>/logs/night.A3.err"
```

- Pass. Exit 0. F3 merged into `integration/wordstat-cli` at `6a83b81`, its brief says `approved by the user`, and scratch `main` stayed at `705a4d6` (`night.A3.jsonl`, `night.A3.after.refs`).
- Finding. F4's `Merged` cell should have stayed empty. The F3 approval put `6a83b81` into F4's cell too (`ed0b8de`, tracking README line 16). F4's branch still failed the integration ancestry check.
- Intermediate recovery. The Claude result reports that the first F3 worktree removal and claim release failed from the wrong working directory. It removed the scratch worktree, pruned Git's worktree record and released the claim before returning (`night.A3.jsonl`, post-call snapshots).

### A4

```bash
cd "<scratch>/night"
git merge --no-ff integration/wordstat-cli -m "Merge integration/wordstat-cli"
python -m pytest -q
```

- Pass. The merge created `bc13c94` with parents `705a4d6` and `0028b2f`. Pytest exited 0 with `12 passed, 1 skipped`. The F4 tip `db25ab8` was outside `main` (`night.A4.merge`, `night.A4.pytest`, `night.A4.after.refs`).

### A5

```bash
python "<working folder>/scripts/wave_driver.py" plans/2026-11-04-wordstat-cli \
  --repo "<scratch>/night" --dry-run --claude-arg=--setting-sources --claude-arg=project,local
```

- Pass. Exit 0 with `next: nothing — plans/2026-11-04-wordstat-cli: finished`. F4 still waited on I1 (`night.A5.stdout`, `night.A5.after.README.md`).

### A6

```bash
cd "<scratch>/night"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status plans/2026-11-04-wordstat-cli" \
  --output-format stream-json --verbose --permission-mode bypassPermissions \
  --setting-sources project,local --model haiku --max-turns 60 --max-budget-usd 0.5 \
  < /dev/null > "<scratch>/logs/night.A6.jsonl" 2> "<scratch>/logs/night.A6.err"
```

- Pass. Exit 0. F4 remained `⚠️ blocked I1`. `Merged, not in main:` showed `none`, and the integration branch had 0 commits outside `main` (`night.A6.jsonl`). The status output flagged the bad F4 `Merged` cell and displayed it as `—`.

### Claude call records

The driver issued `claude -p "<prompt>" --output-format json --permission-mode auto --model <model> --max-turns <turns> --max-budget-usd <budget> --setting-sources project,local`. A3 and A6 used the exact stream commands above. The timing column is measured wall time. The opening and closing lines are from each final result, and the times in those lines are Claude's own report.

| Call and log | Prompt | Model | Turns/USD cap | Exit | Turns | `total_cost_usd` | Wall min | First line | Last line | Stop line |
|---|---|---|---|---:|---:|---:|---:|---|---|---|
| A2.1 `calls/01-wave.json` | `/wave-run plans/2026-11-04-wordstat-cli 1` | sonnet (`claude-sonnet-5-5`) | 110 / 3 | 0 | 12 | 0.7152610300000002 | 2.8 | `Started: 2026-11-18 17:27` | `Started: 2026-11-18 17:27 · Finished: 2026-11-18 17:29 (2 min)` | none |
| A2.2 `calls/02-wave.json` | `/wave-run plans/2026-11-04-wordstat-cli 2` | sonnet (`claude-sonnet-5-5`) | 110 / 3 | 0 | 13 | 0.724373175 | 2.9 | `Started: 2026-11-18 17:29` | `Started: 2026-11-18 17:29 · Finished: 2026-11-18 17:34 (5 min)` | none |
| A2.3 `calls/03-status.json` | `/wave-status plans/2026-11-04-wordstat-cli` | haiku (`claude-haiku-5-5`) | 60 / 0.5 | 0 | 7 | 0.014815090000000001 | 0.6 | `Started: 2026-11-18 17:32` | `Started: 2026-11-18 17:32 · Finished: 2026-11-18 17:33 (1 min)` | none |
| A3 `night.A3.jsonl` | `/wave-run plans/2026-11-04-wordstat-cli merge F3` | sonnet (`claude-sonnet-5-5`) | 100 / 3 | 0 | 18 | 0.336079 | 1.12 | `Started: 2026-11-18 17:33` | `Started: 2026-11-18 17:33 · Finished: 2026-11-18 17:36 (3 min)` | none |
| A6 `night.A6.jsonl` | `/wave-status plans/2026-11-04-wordstat-cli` | haiku (`claude-haiku-5-5`) | 60 / 0.5 | 0 | 8 | 0.01299457 | 0.70 | `Started: 2026-11-18 17:35` | `Started: 2026-11-18 17:35 · Finished: 2026-11-18 17:35 (<1 min)` | none |

Total reported cost was about 1.803523 USD. A repeat in `night2` was unnecessary because `auto` finished without permission denials.

Git snapshot names below refer to pairs of files in `<scratch>/logs/` ending in `.refs` (`git for-each-ref --format='%(refname) %(objectname)'`) and `.worktrees` (`git worktree list --porcelain`). The A2 internal boundaries come from polling the driver log once per second when it announced the next call.

| Call | Before | After | Git change |
|---|---|---|---|
| A2.1 | `A2.before` | `A2.call-2` | Integration created at `37fe8db`, tracking `42225c1`; main, integration, F3, and tracking worktrees remained. |
| A2.2 | `A2.call-2` | `A2.call-3` | Integration advanced to `c4fd630` and tracking to `34d6738`; F4's worktree joined the remaining worktrees, F2's branch was retained. |
| A2.3 | `A2.call-3` | `A2.after` | Refs and worktrees were unchanged. |
| A3 | `night.A3.before` | `night.A3.after` | Integration advanced to `0028b2f` and tracking to `ed0b8de`; the F3 worktree was removed. |
| A6 | `night.A6.before` | `night.A6.after` | Refs and worktrees were unchanged. |

## Results

| Expectation | Result | Evidence |
|---|---|---|
| Seeded test skips and plan validates | Pass | `1 skipped` and two exit codes of 0. |
| A1 exits 0, announces `next: wave plans/2026-11-04-wordstat-cli — wave 1 is ready`, and previews the prescribed Sonnet command and settings | Pass | A1 stdout and exit 0. |
| A2 prints `Report: <path>` and exits 0 or 1 with wave 1, wave 2, and final status, with optional retries | Pass | `A2.stdout`, `A2.exit` = 0 and `driver.log`, calls 1–3. |
| A2 F1 and F2 merged, both hashes in integration ancestry, both briefs `auto-approved`, and wave 2 starts without `feature-unmerged` | Pass | `merge-base --is-ancestor` exit 0 for `22a272d` and `2e3ea57` against `c4fd630`. Both tracking briefs say `auto-approved`. `driver.log` starts wave 2 and has no stop. |
| A2 F3 in review, waiting for review, outside integration | Pass | Tracking `34d6738`, `night.A3.before.README.md`, and `merge-base --is-ancestor 4b5e4d3 c4fd630` exit 1. |
| A2 F4 and D blocked on an open problem, F4 outside integration | Pass | Tracking `34d6738` marks F4 and D with I1. `problems.md` lists I1 as open. `merge-base --is-ancestor db25ab8 c4fd630` exited 1. `calls/02-wave.json` identifies the forced test. |
| A2 scratch `main`, `origin/main`, and bare remote refs match seed, with no target claim or driver lock | Pass | Both branches at `705a4d6` in `A2.before.refs` and `A2.after.refs`. `origin.before.refs` and `night.A3.before.origin.refs` match. No `refs/wave-method/claims/*` at A2 exit. No `wave-driver.lock` in scratch `.git`. |
| A2 morning report names the integration target, shows both merged feature blocks, F3 review commands, F4 with I1, the two next git commands, and a cost for every call | Pass | The saved `report.md` reproduced above shows each item. |
| A2 respects the direct task out-of-scope rule | Finding | `calls/01-wave.json` acknowledges A wrote tracked bytecode outside its file list and says no entry was opened. `274b554` removed the files, and the coordinator still auto-approved F1. `skills/wave-run/autonomous.md:91–93` calls for an entry, revert, blocked feature and skipped dependents. |
| A3 explicitly approves and merges F3 into integration while leaving `main` at seed | Pass | Tracking F3 brief line 5 says `6a83b81`, `approved by the user`. `night.A3.after.refs` records integration at `0028b2f` and main at `705a4d6`. |
| A3 updates F3's approval metadata and preserves F4's empty `Merged` field | Finding | `git diff 34d6738 ed0b8de -- plans/2026-11-04-wordstat-cli/README.md` shows `6a83b81` written to both F3 and F4. F4 remains blocked, and `db25ab8` is outside both final integration and final `main`. |
| A4 user merge succeeds and tests are `12 passed, 1 skipped` | Pass | `night.A4.merge.exit` and `night.A4.exit` = 0, merge `bc13c94`, `night.A4.pytest`. |
| A5 exits 0 with `next: nothing`, with F4 still blocked | Pass | `night.A5.exit`, `night.A5.stdout` and `night.A5.after.README.md`. |
| A6 shows F4 blocked on I1 and an empty `Merged, not in main:` section | Pass | Last result of `night.A6.jsonl` reports `⚠️ blocked I1` and `none`. |
| Bare remote refs stay unchanged through A6 | Pass | `origin.before.refs` and `night.A6.after.origin.refs` are identical. |
| Source refs before the first call and after the last are equal apart from the task's own branch | Pass | Both `working.before.refs` and `working.after.refs` list 53 ref/object pairs and have SHA-256 `b59f9984fc5af0fc6cece031ea21879fa85f0fbfe2e0a65f07947586e8b79141`. `diff -u` is empty, including the task branch at the time of capture. |

Final tracking README on `plan/wordstat-cli` at `ed0b8de` after A6.

| Feature | Status | Waiting for | `Merged` cell as written |
|---|---|---|---|
| F1 | ✅ merged | | `22a272d` |
| F2 | ✅ merged | | `2e3ea57` |
| F3 | ✅ merged | | `6a83b81` |
| F4 | ⚠️ blocked I1 | I1 | `6a83b81` (F3's hash, recorded in error) |

The wave validation passed: 32 status-check tests, 59 driver tests, validation of all example plans, and `git diff --check`.

## Not verified

nothing

## Repeat

Run the Setup block once in Git Bash to create the scratch environment. Record the same Git snapshots around the calls, then run the commands in A1–A6 in order from `<scratch>/night`. Review the driver's `report.md` and `total_cost_usd` before sending the A3 approval. After A6, capture and compare the source and origin refs.

```bash
git -C "$working" for-each-ref --format='%(refname) %(objectname)' > "$scratch/logs/working.after.refs"
diff -u "$scratch/logs/working.before.refs" "$scratch/logs/working.after.refs"
git -C "$scratch/origin.git" for-each-ref > "$scratch/logs/origin.after.refs"
diff -u "$scratch/logs/origin.before.refs" "$scratch/logs/origin.after.refs"
```
