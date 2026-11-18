# Rehearsal: autonomous flow end to end

2026-11-18 · Claude Code 2.1.326 · source commit dfc40cd

## Setup

The commands below created the virtual environment and seeded a scratch repository from example 03. Pytest 9.2.0 and PyYAML 6.0.3 installed in that environment.

```bash
set -e
scratch=$(mktemp -d)
echo "SCRATCH=$scratch"
ws=$(cygpath -m "$scratch" 2>/dev/null || printf '%s' "$scratch")
echo "WS=$ws"
mkdir -p "$scratch/logs" "$scratch/tmp" "$scratch/userbase" "$scratch/pip-cache"
gpy=$(command -v python); usersite=$("$gpy" -m site --user-site)
printf '%s\n' "$gpy" "$usersite" > "$scratch/logs/site"
python -m venv "$scratch/venv"
bin="$scratch/venv/Scripts"; [ -d "$bin" ] || bin="$scratch/venv/bin"
cat > "$scratch/env.sh" <<EOF
unset MSYS_NO_PATHCONV
export VIRTUAL_ENV="$ws/venv"
export PATH="$bin:\$PATH"
export PIP_REQUIRE_VIRTUALENV=true
export PYTHONUSERBASE="$ws/userbase" PIP_CACHE_DIR="$ws/pip-cache"
export TMPDIR="$ws/tmp" TMP="$ws/tmp" TEMP="$ws/tmp"
EOF
. "$scratch/env.sh"
export CLAUDE_ENV_FILE="$ws/env.sh"
"$bin/python" -m pip install pytest pyyaml
touch "$scratch/logs/start.stamp"
w=<working folder>
n="$scratch/night"
git init -b main "$n"
git -C "$n" config user.name "wave e2e"
git -C "$n" config user.email "e2e@example.invalid"
printf 'MIT\n' > "$n/LICENSE"
git -C "$n" add LICENSE
git -C "$n" commit -qm init
sh "$w/install.sh" "$n" --no-codex
git -C "$n" add .claude
git -C "$n" commit -qm "install wave skills"
mkdir -p "$n/plans"
cp -r "$w/examples/03-autonomous-night-run" "$n/plans/2026-11-04-wordstat-cli"
git -C "$n" add plans
git -C "$n" commit -qm "add plan"
git -C "$n" branch plan/wordstat-cli
mkdir -p "$n/tests"
cat > "$n/tests/test_forced_red.py" <<'EOF'
"""Forced failure of the end-to-end run: red as soon as wordstat.export exists."""
import pytest


def test_forced_red():
    pytest.importorskip("wordstat.export")
    assert False, "forced red: end-to-end run"
EOF
git -C "$n" add tests/test_forced_red.py
git -C "$n" commit -qm 'Force red when wordstat.export exists'
cat > "$n/.git/hooks/post-commit" <<'EOF'
#!/bin/sh
# End-to-end run: task B's first commit also adds stray.txt, outside its file list.
marker="$(git rev-parse --git-common-dir)/stray-done"
[ -e "$marker" ] && exit 0
case "$(git log -1 --format=%s)" in
  "wordstat-cli F2 / B:"*) ;;
  *) exit 0 ;;
esac
touch "$marker"
printf 'forced out-of-scope file of the end-to-end run\n' > stray.txt
git add stray.txt
git commit -q --amend --no-edit --no-verify
EOF
chmod +x "$n/.git/hooks/post-commit"
p="$scratch/hookprobe"
git init "$p"
git -C "$p" config user.name "wave e2e"
git -C "$p" config user.email "e2e@example.invalid"
cp -p "$n/.git/hooks/post-commit" "$p/.git/hooks/post-commit"
git -C "$p" commit -q --allow-empty -m "wordstat-cli F2 / B: probe"
git -C "$p" show --name-only --format= HEAD | tee "$scratch/logs/hook-first"
test "$(cat "$scratch/logs/hook-first")" = stray.txt
git -C "$p" commit -q --allow-empty -m "wordstat-cli F2 / B: again"
test -z "$(git -C "$p" show --name-only --format= HEAD)"
test "$(git -C "$p" log -1 --format=%s HEAD^)" = "wordstat-cli F2 / B: probe"
rm "$p/.git/stray-done"
git init --bare "$scratch/origin.git"
git -C "$n" remote add origin "$scratch/origin.git"
git -C "$n" push -q -u origin main
git -C "$scratch/origin.git" for-each-ref > "$scratch/logs/origin-before.refs"
cd "$n"
python -m pytest -q
python "$w/skills/wave-plan/scripts/status_check.py" plans/2026-11-04-wordstat-cli
```

The hook probe added only stray.txt to the first commit, added no files to the second, and preserved the first commit subject. The initial pytest check reported 1 skipped and exited 0. The plan status check exited 0 with no output. The initial main, remote-tracking main, and bare remote main all pointed to 1f4d74368ca746efff8a2d91bc131f4fb24abfc0.

## Runs

### P0

```bash
scratch=<scratch>
ws=$(cygpath -m "$scratch")
. "$scratch/env.sh"
export CLAUDE_ENV_FILE="$ws/env.sh"
usersite=$(sed -n '2p' "$scratch/logs/site")
cd "$scratch/night"
git for-each-ref --format='%(refname) %(objectname)' > "$scratch/logs/P0.before.refs"
git worktree list --porcelain > "$scratch/logs/P0.before.worktrees"
probe='Run this one command with the Bash tool: command -v python; python -c "import sys, tempfile; print(sys.prefix); print(tempfile.gettempdir())"; echo "pathconv=${MSYS_NO_PATHCONV-unset}". Then launch one subagent and have it run the same command with its Bash tool. Reply with both outputs verbatim.'
MSYS_NO_PATHCONV=1 timeout 600 claude -p "$probe" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model haiku --max-turns 8 --max-budget-usd 0.3 < /dev/null > "$scratch/logs/P0.jsonl" 2> "$scratch/logs/P0.err"; echo $? > "$scratch/logs/P0.exit"
git for-each-ref --format='%(refname) %(objectname)' > "$scratch/logs/P0.after.refs"
git worktree list --porcelain > "$scratch/logs/P0.after.worktrees"
{ find "$usersite" -maxdepth 1 -newer "$scratch/logs/start.stamp" 2>/dev/null
  [ -d /c/tmp ] && find /c/tmp -maxdepth 1 -newer "$scratch/logs/start.stamp"; } > "$scratch/logs/P0.outside"
```

- Pass. The main session and subagent Bash tool results each returned <scratch>/venv/Scripts/python, <scratch>/venv, <scratch>/tmp, and pathconv=unset (logs/P0.jsonl). Exit 0, Haiku, 1 turn and USD 0.004986335 in the last result. Wall time was about 0.15 minutes. The final reply began with “The subagent finished and returned the same output as my Bash run, verbatim” and ended at the closing code fence. The watch was empty.
- The P0 before and after ref and worktree snapshots matched. Both show the initial scratch branches and just the night checkout.

### A1

```bash
python "<working folder>/scripts/wave_driver.py" plans/2026-11-04-wordstat-cli --repo "<scratch>/night" --dry-run --claude-arg=--setting-sources --claude-arg=project,local
```

- Pass. Exit 0. The dry run selected wave 1 and printed the Sonnet Claude command with --setting-sources project,local (logs/night-A1.log). No model call or charge. The watch was empty and the ref and worktree snapshots matched.


### A2

```bash
python "<working folder>/scripts/wave_driver.py" plans/2026-11-04-wordstat-cli --repo "<scratch>/night" --claude-arg=--setting-sources --claude-arg=project,local --max-usd 20 --max-calls 12; echo $? > "<scratch>/logs/night-A2.exit"
```

- Pass. The driver ran waves 1 and 2 and then status. Exit 0, elapsed 6.4 minutes, stop “nothing left to run”, empty watch. The driver printed the report path and logged zero permission denials. Its three calls cost USD 1.413700820 at full precision.
- Finding. The hook added `stray.txt` in `0aee877`, as confirmed by the F2 reflog and `git show --name-only 0aee877`. B amended again to `ac885bb`, dropping the path from reachable history before scope validation. The coordinator accepted B and auto-merged F2 at `508ee75`. The expected scope entry and revert were absent. See `calls/02-wave.json` and `logs/night-A2.evidence`.
- The before/after snapshots in `logs/night-A2.*.refs` and `logs/night-A2.*.worktrees` show the integration and feature branches and the remaining F3, F4, integration, and plan worktrees. Main and its remote-tracking ref stayed at the seed.
- The original report, driver log and call logs are in `<scratch>/night.wave-driver/2026-11-18-1837/`. The report below preserves its content with machine paths replaced.

| Call | Model | Turns | USD | Wall min | First and last result lines |
| --- | --- | --- | --- | --- | --- |
| Wave 1 | Sonnet with Haiku subagent | 11 | 0.687170115 | 2.7 | “Wave 1 of `wordstat-cli` is done. F1 is merged into `integration/wordstat-cli` (`aa70528`), and F3 is waiting for your review. I didn't re-read `report.md` before writing this, so it is shorter than that template asks for.” “Started: 2026-11-18 18:38 · Finished: 2026-11-18 18:41 (3 min)” |
| Wave 2 | Sonnet with Haiku subagent | 9 | 0.711629175 | 2.9 | “Started: 2026-11-18 18:40”. “Started: 2026-11-18 18:40 · Finished: 2026-11-18 18:43 (3 min)” |
| Status | Haiku | 10 | 0.01490153 | 0.8 | “Started: 2026-11-18 18:43”. “Started: 2026-11-18 18:43 · Finished: 2026-11-18 18:44 (1 min)” |

~~~~~markdown
# Wave driver report · 2026-11-18 18:44

- Repository: `<scratch>\night` · main branch: `main` · start: `plans/2026-11-04-wordstat-cli`
- Run: 2026-11-18 18:37 – 2026-11-18 18:44 (6 min) · ended: nothing left to run
- Calls: 3 (plan 0, wave 2, task 0, resume 0, status 1) · failed: 0 · turns: 30 · cost: 1.41 USD (total_cost_usd) · Claude minutes: 6.4
- Options: plan-model: opus · run-model: sonnet · status-model: haiku · low-model: haiku · medium-model: sonnet · high-model: opus · cap: [] · max-calls: 12 · max-failures: 3 · max-usd: 20.0 · call-timeout-min: 120 · permission-mode: auto · skill-prefix:  · add-dir: [] · claude-arg: ['--setting-sources', 'project,local'] · no-status: False · dry-run: False
- Log: `<scratch>\night.wave-driver\2026-11-18-1837\driver.log`

## Integration targets

- `integration/wordstat-cli` · worktree `<scratch>\night.worktrees\integration-wordstat-cli` · 12 commits not in `main`

## Merged, not in main

**F1 · Count the words of a text** · merged into `integration/wordstat-cli` `aa70528` · `<scratch>\night.worktrees\integration-wordstat-cli`
Before: no package. After: `wordstat.core` counts words case-insensitively (digits count, inner apostrophes kept) and ranks them by count, then alphabetically.
How to test:
1. `from wordstat.core import count_words, top_words; top_words(count_words('b a b c a b'), 2)` → `[('b', 3), ('a', 2)]`
2. `count_words("Don't stop: don't!")` → `Counter({"don't": 2, 'stop': 1})`
3. `top_words(count_words(''), 0)` → `ValueError: n must be at least 1`
Worth a look: - Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review

**F2 · Command `wordstat <file> --top N`** · merged into `integration/wordstat-cli` `508ee75` · `<scratch>\night.worktrees\integration-wordstat-cli`
Before: no command. After: `wordstat <file> --top N` prints the N most frequent words (default 10) as `<word> <count>` lines; an unreadable file exits 1 and `--top` below 1 exits 2, each with an `error:` message on stderr.
How to test:
1. `wordstat notes.txt --top 1` with `notes.txt` holding `the cat the` → `the 2`
2. `wordstat notes.txt --top 0` → `error: --top must be at least 1` on stderr, exit code 2
3. `wordstat missing.txt` → `error: cannot read missing.txt` on stderr, exit code 1
Worth a look: - Assumed (autonomous, not asked) · F2: what does --top default to? → 10; not chosen: every word - `pyproject.toml` is new: it defines the `wordstat` console script and packages only `wordstat`.
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review

## Ready for review

**F3 · README with install and usage** · `feat/wordstat-cli/F3-usage-readme` · `<scratch>\night.worktrees\wordstat-cli-F3`
Before: only LICENSE. After: README.md explains install, the `wordstat <file> --top N` command with its outputs, an example session and the library calls.
How to test:
1. Open `README.md` → install, command table, the `poem.txt` example (`the 3`, `and 2`, `sea 1`) and a Library section with count_words, top_words and to_csv
Worth a look: - Manual review: the README describes the command and `to_csv`, which come from F2 and F4 and are not on this branch yet.
Merge: `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`

## Blocked and waiting

- `plans/2026-11-04-wordstat-cli` F4 Word counts as CSV — ⚠️ I1: full check red: `tests/test_forced_red.py::test_forced_red` fails as soon as `wordstat/export.py` exists
- `plans/2026-11-04-wordstat-cli` — finished

## Halts

none

## Open problems

- `plans/2026-11-04-wordstat-cli` I1 · wave 2 / task D / feature F4: full check red: `tests/test_forced_red.py::test_forced_red` fails as soon as `wordstat/export.py` exists — open

## Status check

none

## Calls

| # | Time | Kind | Unit | Prompt | Model | Outcome | Exit | Turns | USD | Min | Denials | Stop or detail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 18:37:50 | wave | plans/2026-11-04-wordstat-cli | /wave-run plans/2026-11-04-wordstat-cli 1 | sonnet | ok | 0 | 11 | 0.69 | 2.7 | 0 | no Started: line |
| 2 | 18:40:29 | wave | plans/2026-11-04-wordstat-cli | /wave-run plans/2026-11-04-wordstat-cli 2 | sonnet | ok | 0 | 9 | 0.71 | 2.9 | 0 |  |
| 3 | 18:43:24 | status | plans/2026-11-04-wordstat-cli | /wave-status plans/2026-11-04-wordstat-cli | haiku | ok | 0 | 10 | 0.01 | 0.8 | 0 |  |

## Next

1. review `git diff main...integration/wordstat-cli`, then merge it in the main checkout: `git merge --no-ff integration/wordstat-cli`
2. review `feat/wordstat-cli/F3-usage-readme`, then `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`
3. re-plan the open problems I1: `/wave-plan plans/2026-11-04-wordstat-cli` · `$wave-plan plans/2026-11-04-wordstat-cli`

## wave-status

````
Started: 2026-11-18 18:43

## plans/2026-11-04-wordstat-cli · `wordstat-cli` · autonomous · target: integration/wordstat-cli · manual review: F3

- Tracking branch: `plan/wordstat-cli` present
- Features: 4 — 2 ✅ merged · 1 👀 review · 1 ⚠️

| Feature | Status | Tasks | Waiting for | Branch | Merged |
|---|---|---|---|---|---|
| F1 Count the words of a text | ✅ merged | 1/1 | | `feat/wordstat-cli/F1-word-counter` | aa70528 |
| F2 Command `wordstat <file> --top N` | ✅ merged | 1/1 | | `feat/wordstat-cli/F2-top-words-cli` | 508ee75 |
| F3 README with install and usage | 👀 review | 1/1 | review | `feat/wordstat-cli/F3-usage-readme` | |
| F4 Word counts as CSV | ⚠️ blocked I1 | 0/1 · ⚠️ D | I1 | `feat/wordstat-cli/F4-csv-export` | |

- Waves: 1 ✅ · 2 ⚠️ I1 · none running

Merged, not in main:

**F1 · Count the words of a text** · merged into `integration/wordstat-cli` `aa70528` · `<scratch>/night.worktrees/integration-wordstat-cli`
Before: no package. After: `wordstat.core` counts words case-insensitively (digits count, inner apostrophes kept) and ranks them by count, then alphabetically.
How to test:
1. `from wordstat.core import count_words, top_words; top_words(count_words('b a b c a b'), 2)` → `[('b', 3), ('a', 2)]`
2. `count_words("Don't stop: don't!")` → `Counter({"don't": 2, 'stop': 1})`
3. `top_words(count_words(''), 0)` → `ValueError: n must be at least 1`
Worth a look: Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review

**F2 · Command `wordstat <file> --top N`** · merged into `integration/wordstat-cli` `508ee75` · `<scratch>/night.worktrees/integration-wordstat-cli`
Before: no command. After: `wordstat <file> --top N` prints the N most frequent words (default 10) as `<word> <count>` lines; an unreadable file exits 1 and `--top` below 1 exits 2, each with an `error:` message on stderr.
How to test:
1. `wordstat notes.txt --top 1` with `notes.txt` holding `the cat the` → `the 2`
2. `wordstat notes.txt --top 0` → `error: --top must be at least 1` on stderr, exit code 2
3. `wordstat missing.txt` → `error: cannot read missing.txt` on stderr, exit code 1
Worth a look: Assumed (autonomous, not asked) · F2: what does --top default to? → 10; not chosen: every word. `pyproject.toml` is new: it defines the `wordstat` console script and packages only `wordstat`.
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review

Ready for review:

**F3 · README with install and usage** · `feat/wordstat-cli/F3-usage-readme` · `<scratch>/night.worktrees/wordstat-cli-F3`
Before: only LICENSE. After: README.md explains install, the `wordstat <file> --top N` command with its outputs, an example session and the library calls.
How to test:
1. Open `README.md` → install, command table, the `poem.txt` example (`the 3`, `and 2`, `sea 1`) and a Library section with count_words, top_words and to_csv
Worth a look: Manual review: the README describes the command and `to_csv`, which come from F2 and F4 and are not on this branch yet.
Merge: `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`

- Integration: `integration/wordstat-cli` — 12 commits not in `main`; review `git diff main...integration/wordstat-cli`, then merge it yourself in the main checkout (`git merge --no-ff integration/wordstat-cli`). Claim: none.
- Inconsistencies: none
- Next: `/wave-plan plans/2026-11-04-wordstat-cli` · `$wave-plan plans/2026-11-04-wordstat-cli` (open entry I1 is not yet marked `→ task`; F3 also waits for your review, see its Merge line above)

Started: 2026-11-18 18:43 · Finished: 2026-11-18 18:44 (1 min)
````
~~~~~


### A3

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-04-wordstat-cli merge F3" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model sonnet --max-turns 100 --max-budget-usd 3 < /dev/null > "<scratch>/logs/night-A3.jsonl" 2> "<scratch>/logs/night-A3.err"; echo $? > "<scratch>/logs/night-A3.exit"
```

- Pass. Exit 0, Sonnet, 17 turns, USD 0.37850139999999993, about 1 minute. The result opened with “Started: 2026-11-18 18:44” and closed with “Started: 2026-11-18 18:44 · Finished: 2026-11-18 18:45 (1 min)”. The merged brief says “Approved: by the user”. The watch was empty.
- Pass. F3 merged as `51b867a` into integration. Main stayed at `1f4d743`. The ref and worktree snapshots record the disappearance of the F3 worktree and the update of the plan and integration refs.
- Pass. From the tracking worktree `<scratch>/night.worktrees/wordstat-cli-plan`, `python "<working folder>/skills/wave-plan/scripts/status_check.py" plans/2026-11-04-wordstat-cli` exited 0 (`logs/night-A3.status.exit`). F4's Merged cell remained empty. F2's existing `508ee75` stayed unchanged from A2.

### A4

```bash
git merge --no-ff integration/wordstat-cli -m "Merge integration/wordstat-cli"
python -m pytest -q
```

- Finding. Merge and tests exited 0. Pytest reported `12 passed, 1 skipped` instead of `7 passed, 1 skipped` because the unexpectedly merged F2 contributed five tests (`logs/night-A4.log`). The watch was empty. Only main moved in the ref and worktree snapshots. No model call or charge.

### A5

```bash
python "<working folder>/scripts/wave_driver.py" plans/2026-11-04-wordstat-cli --repo "<scratch>/night" --dry-run --claude-arg=--setting-sources --claude-arg=project,local
```

- Pass. Exit 0, “next: nothing — plans/2026-11-04-wordstat-cli: finished”. The watch was empty and both snapshot pairs matched. No model call or charge.

### A6

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status plans/2026-11-04-wordstat-cli" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model haiku --max-turns 60 --max-budget-usd 0.5 < /dev/null > "<scratch>/logs/night-A6.jsonl" 2> "<scratch>/logs/night-A6.err"; echo $? > "<scratch>/logs/night-A6.exit"
```

- Pass. Exit 0, Haiku, 8 turns, USD 0.018032199999999998, about 1 minute. It opened with “Started: 2026-11-18 18:46” and closed with “Started: 2026-11-18 18:46 · Finished: 2026-11-18 18:47 (1 min)”. It reported no stop line for wave 2. The snapshots matched and the watch was empty.
- Finding. Status showed F2 merged and F4 blocked with I1. “Merged, not in main” showed “none”, and integration was in main (`d38883c`). The bare remote's final ref matched its setup ref. Total reported usage for P0, A2, A3 and A6 was USD 1.815220755, below the USD 25 cap.

Final feature rows from the tracking README at `5f1092c`:

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
| F1 | `word-counter` | Count the words of a text | P1 | A (1) | `python -m pytest -q` green: `tests/test_core.py` (7 cases) | ✅ merged | | `feat/wordstat-cli/F1-word-counter` | aa70528 |
| F2 | `top-words-cli` | Command `wordstat <file> --top N` | P2 | B (2) | `tests/test_cli.py` (5 cases) green | ✅ merged | | `feat/wordstat-cli/F2-top-words-cli` | 508ee75 |
| F3 | `usage-readme` | README with install and usage | P3 | C (1) | README shows install, the command, an example session and the library calls | ✅ merged | | `feat/wordstat-cli/F3-usage-readme` | 51b867a |
| F4 | `csv-export` | Word counts as CSV | P4 | D (2) | `tests/test_export.py` (3 cases) green | ⚠️ blocked I1 | I1 | `feat/wordstat-cli/F4-csv-export` | |


## Results

| Expectation | Result | Evidence |
| --- | --- | --- |
| Setup: forced-red test initially skips; seeded plan passes status check | Pass | Setup pytest: `1 skipped`, exit 0. Seeded plan status check exited 0. |
| Hook probe: first subject unchanged, `stray.txt` only in first commit | Pass | `logs/hook-first` and the probe's first and second commits. |
| P0: Bash in the session and subagent resolves scratch Python, prefix and temp, with path conversion unset | Pass | Both Bash tool results in `logs/P0.jsonl`. |
| Watch: no new paths in the watched locations after any invocation | Pass | All seven `logs/*.outside` files had zero bytes. |
| A1: selects wave 1 with the Sonnet command and isolated setting sources | Pass | `logs/night-A1.log`, exit 0. |
| A2: driver emits report; wave 1, wave 2 and final status | Pass | `driver.log` and three logs under `calls/`. There was no `feature-unmerged` stop. |
| A2: F1 auto-approved with “scope clean”; merged hash in integration | Pass | `aa70528` and `report.md`. |
| A2: no generated path merged | Pass | `logs/night-A2.evidence`: no generated path in the non-merge commit file list. |
| A2: B is ⚠️ and F2 is blocked by an open problem naming `stray.txt` | Finding | `0aee877` contained `stray.txt`. B amended to `ac885bb`, and neither gate encountered it. `problems.md` held only F4's I1. F2 auto-merged at `508ee75`. |
| A2: F2 feature history contains B's commit and a revert, with no other deleting commit | Finding | Range from integration to F2 was empty after auto-merge. The F2 reflog shows the two amendments `0aee877` and `ac885bb`; there was no revert or deleting commit. |
| A2: F2 triple-dot diff exits 0 after the revert | Finding | `logs/night-A2.evidence`: exit 0 because the F2 tip was already in integration. It does not demonstrate a revert. |
| A2: F2 tip is outside integration | Finding | `logs/night-A2.evidence`: ancestry check exited 0. |
| A2: F3 waits for review, outside integration | Pass | F3 row and ancestor check exit 1 in `logs/night-A2.evidence`. |
| A2: F4 and D blocked by forced red, F4 outside integration | Pass | I1 open in `problems.md` at `fc5ba15`: 10 passed, 1 failed, `tests/test_forced_red.py:7`. Task D ⚠️, ancestor check exit 1. |
| A2: main, remote-tracking main and bare remote unchanged, no claim refs or driver lock | Pass | `logs/night-A2.*.refs` and `logs/night-A2.evidence`: main refs at `1f4d743`, remote ref comparison exit 0, no claims refs and lock absence check exit 0. |
| A2: driver report names integration and review commands, lists each cost, and gives the morning diff and merge commands | Pass | The pasted `report.md`. |
| A2: report has only F1 under merged and has F2 and F4 under blocked | Finding | The report includes F1 and F2 under “Merged, not in main” and F4 under “Blocked and waiting”. |
| A3: F3 merged into integration by user approval; main unchanged | Pass | `51b867a`, “Approved: by the user” in `logs/night-A3.jsonl`, and `logs/night-A3.*.refs`. |
| A3: F2 Merged cell remains empty | Finding | F2 already had `508ee75` at A2 and its value stayed unchanged. |
| A3: F4 Merged cell remains empty | Pass | Tracking README at `5f1092c`, F4 row below. |
| A3: status check exits 0 in tracking worktree | Pass | `logs/night-A3.status.exit` is 0. |
| A4: merge succeeds | Pass | `logs/night-A4.log` and `logs/night-A4.after.refs`. |
| A4: pytest gives `7 passed, 1 skipped` | Finding | `logs/night-A4.log` gives `12 passed, 1 skipped`, including the five F2 tests. |
| A5: exit 0, next nothing, no call for F2 or F4 | Pass | `logs/night-A5.log`, dry run only. |
| A6: F2 and F4 are blocked with their open entries | Finding | `logs/night-A6.jsonl` shows F2 merged and F4 blocked by I1. |
| A6: no feature under “Merged, not in main” | Pass | `logs/night-A6.jsonl` and the final refs. |
| Working source refs match before and after the rehearsal | Pass | `logs/source-before.refs` and `logs/source-after.refs` were identical before the record commit. |
| Wave checks are green | Pass | 33 status-check unit tests, 59 driver tests, all example status checks, and `git diff --check`. |

## Not verified

- The run did not exercise a gate-driven revert for F2. B's second amendment removed the stray path from reachable history before either gate could see it.
- The A3 check exercised an empty merge cell for F4. F2 was already merged at A2, so A3 could not exercise an empty F2 cell.
- The watch covers the Python user site and C:/tmp only. The setup launcher and initial source-ref list were initially staged in the system temporary directory and moved into scratch. The watch does not establish where every process wrote on disk.

## Repeat

1. In Git Bash, run the Setup block and then P0 in the seeded checkout. Stop if the hook probe or P0 fails.
2. In the shell that sourced the scratch env file and exported `CLAUDE_ENV_FILE`, run A1 through A6 separately in order. Capture each exit code immediately. Before and after each command, save `git for-each-ref --format='%(refname) %(objectname)'` and `git worktree list --porcelain` in the scratch logs. Take the two source repository snapshots around the whole run.
3. After each invocation, run the P0 watch with the corresponding step name and stop at the first non-empty watch. Track the last reported cost of each invocation and start no further calls once they total USD 25 or more. If auto permission denials prevent completion, preserve the first run, seed a separate night2 checkout in scratch, and repeat A1 through A6 with A2 using bypassPermissions.
4. After A3, run the plan status checker in the tracking worktree and capture the README rows. Before A4, review the integration diff. After A6, compare the bare remote refs with the setup snapshot.
