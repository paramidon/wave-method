# Rehearsal: autonomous flow end to end

> History: these runs used the Python overnight driver (`scripts/wave_driver.py`), which has since been removed from
> the repository; `/wave-auto` replaces it (`skills/wave-auto/SKILL.md`). Its commands are kept as a record and no
> longer run.

2026-11-18 · Claude Code 2.1.326 · source commit 47e212d · third run

## Setup

Git Bash created scratch before any run file. The repositories, worktrees and bare remote were created under `<scratch>`. The venv, package cache, Python user base, subprocess temp directory and environment file were created there as well. The launcher helpers were created in `<scratch>/launch`, the ref snapshots, watch results, notes and direct call logs in `<scratch>/logs`, and the driver's report and call logs in `<scratch>/night.wave-driver`.

~~~bash
scratch=$(mktemp -d)
ws=$(cygpath -m "$scratch" 2>/dev/null || printf '%s' "$scratch")
mkdir -p "$scratch/logs" "$scratch/tmp" "$scratch/userbase" "$scratch/pip-cache" "$scratch/launch"
gpy=$(command -v python); usersite=$("$gpy" -m site --user-site)
printf '%s\n%s\n' "$gpy" "$usersite" > "$scratch/logs/global-python.txt"
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
export PYTHONDONTWRITEBYTECODE=1
"$bin/python" -m pip install pytest pyyaml > "$scratch/logs/pip.log" 2>&1
touch "$scratch/logs/start.stamp"
claude --version

working='<working folder>'
night="$scratch/night"
logs="$scratch/logs"
plan=plans/2026-11-04-wordstat-cli
git init -b main "$night"
git -C "$night" config user.name "wave e2e"
git -C "$night" config user.email "e2e@example.invalid"
printf 'MIT\n' > "$night/LICENSE"; git -C "$night" add LICENSE; git -C "$night" commit -qm init
sh "$working/install.sh" "$night" --no-codex
git -C "$night" add .claude; git -C "$night" commit -qm "install wave skills"
mkdir -p "$night/plans"; cp -r "$working/examples/03-autonomous-night-run" "$night/$plan"
git -C "$night" add plans; git -C "$night" commit -qm "add plan"
git -C "$night" branch plan/wordstat-cli
mkdir -p "$night/tests"
cat > "$night/tests/test_forced_red.py" <<'PYTHON'
"""Forced failure of the end-to-end run: red as soon as wordstat.export exists."""
import pytest


def test_forced_red():
    pytest.importorskip("wordstat.export")
    assert False, "forced red: end-to-end run"
PYTHON
git -C "$night" add tests/test_forced_red.py
git -C "$night" commit -qm "add forced red test"
cat > "$night/.git/hooks/post-commit" <<'HOOK'
#!/bin/sh
# End-to-end run: task B of F2 always hands over a history in which stray.txt, outside its file list, was added.
case "$(git log -1 --format=%s)" in
  "wordstat-cli F2 / B:"*) ;;
  *) exit 0 ;;
esac
git cat-file -e HEAD:stray.txt 2>/dev/null && exit 0
git cat-file -e HEAD~1:stray.txt 2>/dev/null && exit 0
printf 'forced out-of-scope file of the end-to-end run\n' > stray.txt
git add stray.txt
git commit -q --amend --no-edit --no-verify
HOOK
chmod +x "$night/.git/hooks/post-commit"

cat > "$scratch/launch/hookprobe.sh" <<'PROBE'
set -e
git init -q -b main "$scratch/hookprobe"
cd "$scratch/hookprobe"
git config user.name "wave e2e"
git config user.email "e2e@example.invalid"
git config core.autocrlf false
cp "$night/.git/hooks/post-commit" .git/hooks/post-commit
echo 'Step 1: initial commit'
git commit -q --allow-empty -m init
H=$(git rev-parse HEAD)
printf '%s\n' "$H"
echo 'Step 2: add a.txt and inject stray.txt'
printf '1\n' > a.txt; git add a.txt; git commit -q -m "wordstat-cli F2 / B: probe"
files=$(git show --name-only --format= HEAD)
printf '%s\n' "$files"
test "$files" = "$(printf 'a.txt\nstray.txt')"
subject=$(git log -1 --format=%s)
printf '%s\n' "$subject"
test "$subject" = 'wordstat-cli F2 / B: probe'
echo 'Step 3: amend without stray.txt'
git rm -q --cached stray.txt; rm stray.txt; git commit -q --amend --no-edit
git cat-file -e HEAD:stray.txt
echo 'HEAD has stray.txt'
echo 'Step 4: remove stray.txt in a later commit'
git rm -q stray.txt; git commit -q -m "wordstat-cli F2 / B: remove"
if git cat-file -e HEAD:stray.txt 2>/dev/null; then exit 1; fi
echo 'HEAD lacks stray.txt'
files=$(git log --no-merges --name-only --format= $H..HEAD | sort -u)
printf '%s\n' "$files"
test "$files" = "$(printf 'a.txt\nstray.txt')"
echo 'Step 5: non-B commit'
git commit -q --allow-empty -m "other: probe"
files=$(git show --name-only --format= HEAD)
printf '%s\n' "$files"
test -z "$files"
git reset -q --hard HEAD~1
echo 'Step 6: revert the range'
git revert --no-edit $H..HEAD
echo 'git revert exit 0'
git diff --quiet "$H" HEAD
echo 'git diff --quiet exit 0'
PROBE
env scratch="$scratch" night="$night" bash "$scratch/launch/hookprobe.sh" > "$logs/hookprobe.txt" 2>&1

git init --bare "$scratch/origin.git"
git -C "$night" remote add origin "$scratch/origin.git"
git -C "$night" push -q -u origin main
git -C "$scratch/origin.git" for-each-ref > "$logs/origin-before.refs"
git -C "$night" for-each-ref --format='%(refname) %(objectname)' > "$logs/seed.refs"
(cd "$night" && python -m pytest -q)
(cd "$night" && python "$working/skills/wave-plan/scripts/status_check.py" "$plan")
~~~

An initial launcher assertion expected an extra blank line in the Step 4 path list. The actual list contained exactly the two prescribed paths, so the assertion was corrected before continuing the probe.

The scratch `main`, remote-tracking and bare remote `main` refs pointed to 3f86168ed1e8a7dcdeb0d7a43be92c656f984e79. The seed tests returned `1 skipped`, exit 0. The seed status check returned exit 0.

## Runs

Before the first call and after the last, the working folder's refs were captured with the following command. For each step the scratch refs and worktrees were captured before and after with the same ref format and `git worktree list --porcelain`.

~~~bash
git -C "$working" for-each-ref --format='%(refname) %(objectname)' > "$logs/working-before.refs"
git -C "$working" for-each-ref --format='%(refname) %(objectname)' > "$logs/working-after.refs"
~~~

After a direct Claude call the usage test searched its `.jsonl` and `.err` files. For A2 it also searched all driver call files. Exit 1 from grep means no usage match. After the snapshots, the watch wrote its result to the step's `.outside` file.

~~~bash
grep -l -i -E "hit your .*limit|usage limit" <call-output-files>
{ find "$usersite" -maxdepth 1 -newer "$logs/start.stamp" 2>/dev/null
  [ -d /c/tmp ] && find /c/tmp -maxdepth 1 -newer "$logs/start.stamp"; } > "$logs/<step>.outside"
~~~

### P0

~~~bash
cd "$night"
probe='Run this one command with the Bash tool: command -v python; python -c "import sys, tempfile; print(sys.prefix); print(tempfile.gettempdir())"; echo "pathconv=${MSYS_NO_PATHCONV-unset}". Then launch one subagent and have it run the same command with its Bash tool. Reply with both outputs verbatim.'
MSYS_NO_PATHCONV=1 timeout 600 claude -p "$probe" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 8 --max-budget-usd 0.3 < /dev/null > "$logs/P0.jsonl" 2> "$logs/P0.err"; echo $? > "$logs/P0.exit"
~~~

- Pass. Both tool results show `<scratch>/venv/Scripts/python`, prefix `<scratch>/venv`, temp directory `<scratch>/tmp` and `pathconv=unset` (P0.jsonl).
- Exit 0, usage test exit 1, empty watch. Model claude-haiku-5-5, 1 turn, $0.00493746, 0.13 wall minutes, stop reason end_turn, no wave stop line. The last result begins “The subagent finished. Its output, verbatim:” and ends “Both runs match: the Bash tool and the subagent's Bash tool give the same Python path, prefix, temp directory, and `MSYS_NO_PATHCONV` value.” (P0.jsonl, P0.exit, P0.usage-exit, P0.outside, P0.before.*, P0.after.*).

### A1

~~~bash
python "$working/scripts/wave_driver.py" "$plan" --repo "$night" --dry-run \
  --claude-arg=--setting-sources --claude-arg=project,local > "$logs/night-A1.txt" 2> "$logs/night-A1.err"; echo $? > "$logs/night-A1.exit"
~~~

- Pass. Exit 0. The dry run printed `next: wave plans/2026-11-04-wordstat-cli — wave 1 is ready` and the expected `/wave-run … 1` command with `--model sonnet` and `--setting-sources project,local` (night-A1.txt).
- No Claude call. The watch was empty and the before and after refs and worktrees were unchanged (night-A1.outside, night-A1.before.*, night-A1.after.*).


### A2

~~~bash
python "$working/scripts/wave_driver.py" "$plan" --repo "$night" \
  --claude-arg=--setting-sources --claude-arg=project,local --max-usd 20 --max-calls 12 \
  > "$logs/night-A2.txt" 2> "$logs/night-A2.err"; echo $? > "$logs/night-A2.exit"
~~~

- Pass. Exit 0. The driver printed its report path and ended with “nothing left to run.” Its three calls used the default auto permission mode. All exited 0 with zero permission denials, zero wave stop lines and stop reason `end_turn`. The usage test exited 1 across the driver output and all three call logs. The watch was empty (`night-A2.exit`, `night-A2.usage-exit`, `night-A2.outside`, `night-A2.before.*`, `night-A2.after.*`).
- Pass. F1 auto-merged, F3 reached manual review and F2 and F4 blocked for the two forced failures. The A2 report and raw call logs were preserved with `driver.log` in `night.wave-driver/2026-11-18-2054/`.

| Call log | Task or role model | Turns | Exact total_cost_usd | Wall minutes | First and last result lines |
| --- | --- | ---: | ---: | ---: | --- |
| `calls/01-wave.json` | `claude-sonnet-5-5` with `claude-haiku-5-5` | 8 | 0.6749763550000001 | 2.5 | `Started: 2026-11-18 20:54` / `Started: 2026-11-18 20:54 · Finished: 2026-11-18 20:57 (3 min)` |
| `calls/02-wave.json` | `claude-sonnet-5-5` with `claude-haiku-5-5` | 10 | 0.7051283150000002 | 4.7 | `Started: 2026-11-18 20:57` / `Started: 2026-11-18 20:57 · Finished: 2026-11-18 21:01 (4 min)` |
| `calls/03-status.json` | `claude-haiku-5-5` | 10 | 0.013562830000000001 | 0.8 | `Started: 2026-11-18 21:01` / `Started: 2026-11-18 21:01 · Finished: 2026-11-18 21:02 (1 min)` |

The A2 report follows with machine paths replaced.

~~~~~markdown
# Wave driver report · 2026-11-18 21:02

- Repository: `<scratch>\night` · main branch: `main` · start: `plans/2026-11-04-wordstat-cli`
- Run: 2026-11-18 20:54 – 2026-11-18 21:02 (8 min) · ended: nothing left to run
- Calls: 3 (plan 0, wave 2, task 0, resume 0, status 1) · failed: 0 · turns: 28 · cost: 1.39 USD (total_cost_usd) · Claude minutes: 8.0
- Options: plan-model: opus · run-model: sonnet · status-model: haiku · low-model: haiku · medium-model: sonnet · high-model: opus · cap: [] · max-calls: 12 · max-failures: 3 · max-usd: 20.0 · call-timeout-min: 120 · permission-mode: auto · skill-prefix:  · add-dir: [] · claude-arg: ['--setting-sources', 'project,local'] · no-status: False · dry-run: False
- Log: `<scratch>\night.wave-driver\2026-11-18-2054\driver.log`

## Integration targets

- `integration/wordstat-cli` · worktree `<scratch>\night.worktrees\integration-wordstat-cli` · 6 commits not in `main`

## Merged, not in main

**F1 · Count the words of a text** · merged into `integration/wordstat-cli` `1f428b4` · `<scratch>\night.worktrees\integration-wordstat-cli`
Before: no package. After: `wordstat.core` counts the words of a text case-insensitively and ranks them by count, ties alphabetically.
How to test:
1. `python -c "from wordstat.core import count_words, top_words; print(top_words(count_words('b a b c a b'), 2))"` → `[('b', 3), ('a', 2)]`
2. `top_words(count_words('x'), 0)` → `ValueError: n must be at least 1`
Worth a look: - Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review

## Ready for review

**F3 · README with install and usage** · `feat/wordstat-cli/F3-usage-readme` · `<scratch>/night.worktrees/wordstat-cli-F3`
Before: the repository has only `LICENSE`. After: `README.md` explains install, the `wordstat <file> [--top N]` command, an example session and the library calls.
How to test:
1. Open `README.md` → install, the command with its output table, the poem example (`the 3`, `and 2`, `sea 1`) and a Library section with `count_words`, `top_words`, `to_csv`.
Worth a look: - The README was written before the CLI and the CSV export exist (wave 2); its examples were not run. Verify them after F2 and F4 land. - The README says to run `pip install .`, but no packaging file exists in this plan yet.
Merge: `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`

## Blocked and waiting

- `plans/2026-11-04-wordstat-cli` F2 Command `wordstat <file> --top N` — ⚠️ I1: out of scope: stray.txt (5c3b6c9)
- `plans/2026-11-04-wordstat-cli` F4 Word counts as CSV — ⚠️ I2: check red: tests/test_forced_red.py::test_forced_red
- `plans/2026-11-04-wordstat-cli` — finished

## Halts

none

## Open problems

- `plans/2026-11-04-wordstat-cli` I1 · wave 2 / task B / feature F2: out of scope: stray.txt (5c3b6c9) — open
- `plans/2026-11-04-wordstat-cli` I2 · wave 2 / task D / feature F4: check red: tests/test_forced_red.py::test_forced_red — open

## Status check

none

## Calls

| # | Time | Kind | Unit | Prompt | Model | Outcome | Exit | Turns | USD | Min | Denials | Stop or detail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 20:54:18 | wave | plans/2026-11-04-wordstat-cli | /wave-run plans/2026-11-04-wordstat-cli 1 | sonnet | ok | 0 | 8 | 0.67 | 2.5 | 0 |  |
| 2 | 20:56:49 | wave | plans/2026-11-04-wordstat-cli | /wave-run plans/2026-11-04-wordstat-cli 2 | sonnet | ok | 0 | 10 | 0.71 | 4.7 | 0 |  |
| 3 | 21:01:34 | status | plans/2026-11-04-wordstat-cli | /wave-status plans/2026-11-04-wordstat-cli | haiku | ok | 0 | 10 | 0.01 | 0.8 | 0 |  |

## Next

1. review `git diff main...integration/wordstat-cli`, then merge it in the main checkout: `git merge --no-ff integration/wordstat-cli`
2. review `feat/wordstat-cli/F3-usage-readme`, then `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`
3. re-plan the open problems I1, I2: `/wave-plan plans/2026-11-04-wordstat-cli` · `$wave-plan plans/2026-11-04-wordstat-cli`

## wave-status

````
Started: 2026-11-18 21:01

## plans/2026-11-04-wordstat-cli · `wordstat-cli` · autonomous · target: integration/wordstat-cli · manual review: F3

- Tracking branch: `plan/wordstat-cli` present
- Features: 4 — 1 ✅ merged · 1 👀 review · 2 ⚠️

| Feature | Status | Tasks | Waiting for | Branch | Merged |
|---|---|---|---|---|---|
| F1 Count the words of a text | ✅ merged | 1/1 | | `feat/wordstat-cli/F1-word-counter` | 1f428b4 |
| F2 Command `wordstat <file> --top N` | ⚠️ blocked I1 | 0/1 · ⚠️ B | I1 | `feat/wordstat-cli/F2-top-words-cli` | |
| F3 README with install and usage | 👀 review | 1/1 | review | `feat/wordstat-cli/F3-usage-readme` | |
| F4 Word counts as CSV | ⚠️ blocked I2 | 0/1 · ⚠️ D | I2 | `feat/wordstat-cli/F4-csv-export` | |

- Waves: 1 ✅ · 2 ⚠️ (open problems I1, I2) · none running

Merged, not in main:

**F1 · Count the words of a text** · merged into `integration/wordstat-cli` `1f428b4` · `<scratch>/night.worktrees/integration-wordstat-cli`
Before: no package. After: `wordstat.core` counts the words of a text case-insensitively and ranks them by count, ties alphabetically.
How to test:
1. `python -c "from wordstat.core import count_words, top_words; print(top_words(count_words('b a b c a b'), 2))"` → `[('b', 3), ('a', 2)]`
2. `top_words(count_words('x'), 0)` → `ValueError: n must be at least 1`
Worth a look: Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review

Ready for review:

**F3 · README with install and usage** · `feat/wordstat-cli/F3-usage-readme` · `<scratch>/night.worktrees/wordstat-cli-F3`
Before: the repository has only `LICENSE`. After: `README.md` explains install, the `wordstat <file> [--top N]` command, an example session and the library calls.
How to test:
1. Open `README.md` → install, the command with its output table, the poem example (`the 3`, `and 2`, `sea 1`) and a Library section with `count_words`, `top_words`, `to_csv`.
Worth a look: The README was written before the CLI and the CSV export exist (wave 2); its examples were not run. Verify them after F2 and F4 land.
Worth a look: The README says to run `pip install .`, but no packaging file exists in this plan yet.
Merge: `/wave-run plans/2026-11-04-wordstat-cli merge F3` · `$wave-run plans/2026-11-04-wordstat-cli merge F3`

- Integration: `integration/wordstat-cli` — 6 commits not in main; review `git diff main...integration/wordstat-cli`, then merge it yourself in the main checkout (`git merge --no-ff integration/wordstat-cli`)
- Inconsistencies: none
- Next: `/wave-plan plans/2026-11-04-wordstat-cli` · `$wave-plan plans/2026-11-04-wordstat-cli`

Started: 2026-11-18 21:01 · Finished: 2026-11-18 21:02 (1 min)
````
~~~~~

### A3

~~~bash
cd "$night"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-04-wordstat-cli merge F3" \
  --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local \
  --model sonnet --max-turns 100 --max-budget-usd 3 < /dev/null > "$logs/night-A3.jsonl" 2> "$logs/night-A3.err"; echo $? > "$logs/night-A3.exit"
tracking=$(git worktree list --porcelain | awk '/^worktree / { sub(/^worktree /, ""); path=$0 } /^branch refs\/heads\/plan\/wordstat-cli$/ { print path }')
(cd "$tracking" && python "$working/skills/wave-plan/scripts/status_check.py" "$plan")
~~~

- Pass. Exit 0, usage test exit 1, empty watch. Model `claude-sonnet-5-5`, 16 turns, $0.3177897, 0.78 wall minutes, stop reason `end_turn`, no wave stop line. The last result begins `## Merge · wordstat-cli` and ends `Started: 2026-11-18 21:03 · Finished: 2026-11-18 21:03 (<1 min)` (`night-A3.jsonl`, `night-A3.exit`, `night-A3.usage-exit`, `night-A3.outside`, `night-A3.before.*`, `night-A3.after.*`).
- Pass. The F3 brief marked merge `eedee9f` “approved by the user.” The tracking worktree's status check exited 0, and F2 and F4 still had empty `Merged` cells (`night-A3.F3-brief.md`, `night-A3.status-check-exit`, `night-A3.README.md`).

### A4

~~~bash
cd "$night"
git merge --no-ff integration/wordstat-cli -m "Merge integration/wordstat-cli"
python -m pytest -q
~~~

- Pass. Merge exit 0 and pytest exit 0 with `7 passed, 1 skipped`. Scratch `main` advanced to `d98daab` and contained the integration tip. No Claude call. The watch was empty (`night-A4.merge-exit`, `night-A4.pytest-exit`, `night-A4.pytest`, `night-A4.outside`, `night-A4.before.*`, `night-A4.after.*`).

### A5

~~~bash
python "$working/scripts/wave_driver.py" "$plan" --repo "$night" --dry-run \
  --claude-arg=--setting-sources --claude-arg=project,local > "$logs/night-A5.txt" 2> "$logs/night-A5.err"; echo $? > "$logs/night-A5.exit"
~~~

- Pass. Exit 0 and `next: nothing — plans/2026-11-04-wordstat-cli: finished`. No Claude call. The watch was empty (`night-A5.txt`, `night-A5.exit`, `night-A5.outside`, `night-A5.before.*`, `night-A5.after.*`).

### A6

~~~bash
cd "$night"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status plans/2026-11-04-wordstat-cli" \
  --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local \
  --model haiku --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$logs/night-A6.jsonl" 2> "$logs/night-A6.err"; echo $? > "$logs/night-A6.exit"
~~~

- Pass. Exit 0, usage test exit 1, empty watch. Model `claude-haiku-5-5`, 8 turns, $0.01236797, 0.68 wall minutes, stop reason `end_turn`, no wave stop line. The last result begins `Started: 2026-11-18 21:04` and ends `Started: 2026-11-18 21:04 · Finished: 2026-11-18 21:05 (1 min)` (`night-A6.jsonl`, `night-A6.exit`, `night-A6.usage-exit`, `night-A6.outside`, `night-A6.before.*`, `night-A6.after.*`).
- Pass. The status report shows F2 blocked under I1, F4 blocked under I2 and `none` under `Merged, not in main:` (`night-A6.jsonl`).

The final feature rows from `plan/wordstat-cli:plans/2026-11-04-wordstat-cli/README.md` were:

~~~~~markdown
| F1 | `word-counter` | Count the words of a text | P1 | A (1) | `python -m pytest -q` green: `tests/test_core.py` (7 cases) | ✅ merged | | `feat/wordstat-cli/F1-word-counter` | 1f428b4 |
| F2 | `top-words-cli` | Command `wordstat <file> --top N` | P2 | B (2) | `tests/test_cli.py` (5 cases) green | ⚠️ blocked I1 | I1 | `feat/wordstat-cli/F2-top-words-cli` | |
| F3 | `usage-readme` | README with install and usage | P3 | C (1) | README shows install, the command, an example session and the library calls | ✅ merged | | `feat/wordstat-cli/F3-usage-readme` | eedee9f |
| F4 | `csv-export` | Word counts as CSV | P4 | D (2) | `tests/test_export.py` (3 cases) green | ⚠️ blocked I2 | I2 | `feat/wordstat-cli/F4-csv-export` | |
~~~~~

## Results

| Expectation | Result | Evidence |
| --- | --- | --- |
| Scratch and launcher isolation | Pass | Scratch was created first. `launch/`, `logs/`, `env.sh`, `venv/`, `userbase/`, `pip-cache/`, `tmp/`, the repositories, their worktrees and `night.wave-driver/` all live under `<scratch>`. The source test suite also inherited the scratch temp variables. |
| Hook probe 1 creates a base commit | Pass | `hookprobe.txt` records `fa1f2ec7b72d895f1361829843a4533b49bab88f`. |
| Hook probe 2 adds `a.txt` and `stray.txt` while preserving the subject | Pass | `hookprobe.txt` lists both files and `wordstat-cli F2 / B: probe`. |
| Hook probe 3 restores `stray.txt` when a B commit is amended | Pass | `hookprobe.txt` records `HEAD has stray.txt`. |
| Hook probe 4 preserves a later deletion and scope history | Pass | `hookprobe.txt` records `HEAD lacks stray.txt` and lists `a.txt` and `stray.txt` over the range. |
| Hook probe 5 leaves the non-B commit empty, then resets it | Pass | Empty path output and successful reset in `hookprobe.txt`. |
| Hook probe 6 can revert both commits with no net effect | Pass | `85fa0e0` and `97c829e`, with revert exit 0 and diff exit 0 (`hookprobe.txt`). |
| Seed pytest skips the forced failure and the seed plan is valid | Pass | `setup-pytest.txt` reports `1 skipped`. `setup-pytest.exit` and `setup-status-check.exit` are both 0. |
| P0 confirms scratch Python, prefix and temp directory and clears path conversion | Pass | Two matching Bash tool results in `P0.jsonl`, one from the main session and one from the subagent. |
| Every step's watch is empty | Pass | `watch-summary.txt` records zero bytes in `P0.outside` and in each of `night-A1.outside` through `night-A6.outside`. |
| Call budgets and usage test | Pass | The usage test exited 1 for P0, A2 (including all three driver call files), A3 and A6. The last result costs sum to 1.728762630000000301 USD, below 25 USD (`call-metadata.txt`, `*.usage-exit`). |
| A1 chooses wave 1 with Sonnet and project/local settings | Pass | Exit 0 and the proposed command in `night-A1.txt`. |
| A2 exits on completion and writes the morning report | Pass | `night-A2.exit` is 0. `night-A2.txt` starts wave 1, wave 2 and wave-status, prints `Report: …` and records `Ended: nothing left to run`. No permission denial kept a wave from finishing. |
| A2 auto-approves F1, and wave 2 starts without `feature-unmerged` | Pass | `1f428b4` is in integration (ancestry exit 0 in `ancestry-and-approval.txt`). A2 `report.md` includes the full auto approval line with `scope clean`. `driver.log` starts wave 2 directly after wave 1. |
| A2 integration has no generated paths | Pass | `night-A2.integration-paths` lists project source, tests and plan Markdown. It contains no `__pycache__` or other generated file. |
| A2 scope blocks B and F2 with an open problem naming `stray.txt` | Pass | `night-A2.README.md` marks B ⚠️ I1, F2 `⚠️ blocked I1` and F2 waiting for I1. `night-A2.problems.md` records open `I1` with `out of scope: stray.txt (5c3b6c9)`. Wave 2's task scope check (step 5) marked B out of scope before auto-approval (`calls/02-wave.json`, `final-w02.md`). |
| A2 one revert for each B commit, no other change to `stray.txt`, empty net diff and F2 unmerged | Pass | `night-A2.F2-subjects` and `night-A2.F2-stray` show only B's commit `5c3b6c9` and its revert `3231f16`. The three-dot diff exits 0 and the F2 ancestry check exits 1 (`night-A2.invariants`). |
| A2 F3 is in review and outside integration | Pass | `night-A2.README.md` marks F3 `👀 review` and waiting for review. The F3 ancestry check exits 1 (`night-A2.invariants`). |
| A2 forced red blocks D and F4 with an open problem | Pass | `night-A2.README.md` marks D ⚠️ I2 and F4 `⚠️ blocked I2`, waiting for I2. Open I2 names `tests/test_forced_red.py::test_forced_red` and `10 passed, 1 failed`. D's own three cases passed. The F4 ancestry check exits 1 (`night-A2.problems.md`, `night-A2.invariants`, `calls/02-wave.json`). |
| A2 preserves scratch main, remote-tracking main and bare remote refs and releases lock and claims | Pass | `night-A2.after.refs` shows both main refs at `3f86168`. Bare remote ref diff exit 0, claims 0 and lock absent (`night-A2.invariants`). |
| A2 morning report shows the integration, review, blockers, next commands and costs | Pass | The pasted report shows F1 alone under Merged, not in main, F3 under Ready for review with both merge commands, and F2/I1 and F4/I2 under Blocked and waiting. Next gives the integration diff and merge commands. Calls lists all three calls and their costs. |
| A2 task commit models in integration | Pass | `night-A2.integration-trailers` contains A at `e0a33a9` with `claude-sonnet-5-5`. The wider audit is in `night-A2.trailers` and `night-A2.paths`. |
| A3 records F3's manual approval and leaves scratch main unchanged | Pass | `night-A3.F3-brief.md` marks `eedee9f` “approved by the user.” Its integration ancestry exits 0. `night-A3.after.refs` leaves main at `3f86168`. |
| A3 keeps the Merged cells empty for F2 and F4 and the tracking plan valid | Pass | Both final cells are empty in `night-A3.README.md` and in the final rows reproduced above. `night-A3.status-check-exit` is 0 in the worktree named in `night-A3.after.worktrees`. |
| A3 task commit models in integration | Pass | `night-A3.integration-trailers` shows A at `e0a33a9` with `claude-sonnet-5-5` and C at `32cb1c2` with `claude-haiku-5-5`. The wider audit is in `night-A3.trailers` and `night-A3.paths`. |
| A4 merges integration and pytest reports 7 passed, 1 skipped | Pass | Scratch main `d98daab` contains integration (ancestry exit 0). Merge and pytest exit 0 (`night-A4.merge-exit`, `night-A4.pytest-exit`, `night-A4.pytest`). |
| A5 schedules no call for F2 or F4 | Pass | Exit 0 and `next: nothing — plans/2026-11-04-wordstat-cli: finished` (`night-A5.txt`). |
| A6 still shows F2 and F4 blocked and no feature merged outside main | Pass | `night-A6.jsonl` shows `⚠️ blocked I1`, `⚠️ blocked I2`, `none` under Merged, not in main, and zero integration commits outside main. |
| Final bare remote refs equal the seed refs | Pass | `origin-before.refs` and `origin-after.refs` are identical (`origin-refs.diff`, exit 0). |
| Working folder refs and objects are stable across the calls | Pass | `working-before.refs` and `working-after.refs` have the same 60 ref/object pairs, including this task branch (`working-refs.diff`, exit 0). The record commit follows the second snapshot. |
| Wave check commands are green | Pass | Status-check suite 33 passed, driver suite 59 passed, all three example status checks exit 0 (`source-checks.txt`), and `git diff --check` exits 0. |

## Not verified

The watch covers only modifications at depth 1 in the global Python user site and `/c/tmp` since the start stamp. Other filesystem locations were outside the watch.

## Repeat

From an empty scratch directory, use the Setup commands in Git Bash. Keep the scratch environment and `CLAUDE_ENV_FILE` exported. Capture the initial source refs, run P0, then run A1 through A6 individually using the commands under Runs. Save each exit code, run the usage test for each Claude result, capture the before and after scratch refs and worktrees, and run the watch. Stop on a failed probe, a failed P0, a nonempty watch, a usage limit or the 25 USD total threshold, as applicable. Finally capture the bare remote refs and the source refs again, and read the feature rows from `plan/wordstat-cli`.
