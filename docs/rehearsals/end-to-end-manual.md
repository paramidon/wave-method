# Rehearsal: manual flow end to end

2026-11-18 · Claude Code 2.1.326 · source `dfc40cd` · baseline `v2.12.0`.

## Setup

In Git Bash the P21 launcher used the following isolation setup. The venv installed pytest 9.2.0 and PyYAML 6.0.3.

~~~bash
scratch=$(mktemp -d)
ws=$(cygpath -m "$scratch" 2>/dev/null || printf '%s' "$scratch")
mkdir -p "$scratch/logs" "$scratch/tmp" "$scratch/userbase" "$scratch/pip-cache"
gpy=$(command -v python); usersite=$("$gpy" -m site --user-site)
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
~~~

Each fresh launcher shell sourced `env.sh` and exported `CLAUDE_ENV_FILE` before running a step.

Both repositories used the current example 01. The baseline used the release's skills and installer.

~~~bash
working='<working folder>'
mkdir "$scratch/v2120"
git -C "$working" archive v2.12.0 skills install.sh | tar -x -C "$scratch/v2120"
for repo in cur base; do
  source="$working"; [ "$repo" = cur ] || source="$scratch/v2120"
  git init -b main "$scratch/$repo"
  git -C "$scratch/$repo" config user.name "wave e2e"
  git -C "$scratch/$repo" config user.email "e2e@example.invalid"
  printf 'MIT\n' > "$scratch/$repo/LICENSE"
  git -C "$scratch/$repo" add LICENSE
  git -C "$scratch/$repo" commit -qm init
  sh "$source/install.sh" "$scratch/$repo" --no-codex
  git -C "$scratch/$repo" add .claude
  git -C "$scratch/$repo" commit -qm "install wave skills"
  mkdir -p "$scratch/$repo/plans"
  cp -r "$working/examples/01-greenfield-todo-cli" "$scratch/$repo/plans/2026-11-02-todo-cli"
  git -C "$scratch/$repo" add plans
  git -C "$scratch/$repo" commit -qm "add plan"
  git -C "$scratch/$repo" branch plan/todo-cli
done
git -C "$working" for-each-ref --format='%(refname) %(objectname)' > "$scratch/logs/working-before.refs"
~~~

Before and after each command the launcher wrote `<tag>.<before|after>.refs` and
`<tag>.<before|after>.worktrees` with `git for-each-ref --format='%(refname) %(objectname)'` and
`git worktree list --porcelain`. The tag was `P0` or `<repo>-<step>`. After each command it checked

~~~bash
{ find "$usersite" -maxdepth 1 -newer "$scratch/logs/start.stamp" 2>/dev/null
  [ -d /c/tmp ] && find /c/tmp -maxdepth 1 -newer "$scratch/logs/start.stamp"; } > "$scratch/logs/$tag.outside"
~~~

The user approvals were M3 and M5. Their additional evidence files, `<tag>.main.before`,
`<tag>.main.after` and `<tag>.main.nonmerges`, came from `git rev-parse main` on either side of
the call and `git rev-list --no-merges --first-parent <before>..main` afterwards.

## Runs

### P0

~~~bash
cd "$scratch/cur"
probe='Run this one command with the Bash tool: command -v python; python -c "import sys, tempfile; print(sys.prefix); print(tempfile.gettempdir())"; echo "pathconv=${MSYS_NO_PATHCONV-unset}". Then launch one subagent and have it run the same command with its Bash tool. Reply with both outputs verbatim.'
MSYS_NO_PATHCONV=1 timeout 600 claude -p "$probe" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 8 --max-budget-usd 0.3 < /dev/null > "$scratch/logs/P0.jsonl" 2> "$scratch/logs/P0.err"; echo $? > "$scratch/logs/P0.exit"
~~~

- Pass. Both Bash `tool_result` events gave `<scratch>/venv/Scripts/python`, `<scratch>/venv`,
  `<scratch>/tmp` and `pathconv=unset`. Exit 0 and `P0.outside` was empty.
- The last result from `claude-haiku-5-5` had 1 turn and reported $0.00660152.
  Its first line was “Both runs printed the same output.” and its last line closed the subagent output fence.
  No stop line. Approximate session wall time was 0.18 min from log creation to exit-file creation.

### cur-M0

~~~bash
cd "$scratch/cur"
python "$working/skills/wave-plan/scripts/status_check.py" plans/2026-11-02-todo-cli > "$scratch/logs/cur-M0.out" 2> "$scratch/logs/cur-M0.err"; echo $? > "$scratch/logs/cur-M0.exit"
~~~

- Exit 0. Watch empty in `cur-M0.outside`. Elapsed 0.00 min.
- Pass. Exit 0 with empty stdout and stderr (`cur-M0.out` and `cur-M0.err`).

### cur-M1

~~~bash
cd "$scratch/cur"
python "$working/scripts/wave_driver.py" plans/2026-11-02-todo-cli --repo . --dry-run > "$scratch/logs/cur-M1.out" 2> "$scratch/logs/cur-M1.err"; echo $? > "$scratch/logs/cur-M1.exit"
~~~

- Exit 0. Watch empty in `cur-M1.outside`. Elapsed 0.00 min.
- Pass. Exit 0. `cur-M1.out` contains `next: nothing — plans/2026-11-02-todo-cli: manual flow: the driver runs autonomous plans only`. `<scratch>/cur.wave-driver` did not exist.

### cur-M2

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 1" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/cur-M2.jsonl" 2> "$scratch/logs/cur-M2.err"; echo $? > "$scratch/logs/cur-M2.exit"
~~~

- Exit 0. Watch empty in `cur-M2.outside`. Elapsed 1.42 min.
- Last result from `claude-sonnet-5-5` had 5 turns and reported $0.485852345. It opened with `Started: 2026-11-18 18:36` and ended with `Started: 2026-11-18 18:36 · Finished: 2026-11-18 18:38 (2 min)`. No stop line.
- Pass. `cur-M2.jsonl` opens with `Started:` and shows `Flow: manual`, wave 1 and A/C ✅, F1 🔄 waiting for wave 2, and an F2 👀 review block and merge question.
- Finding. Expected the result to end with the F2 merge question. The question appears immediately before a `Started: … · Finished: …` timing footer in `cur-M2.jsonl`.
- Pass. `main` stayed at `e1df2eb`; `cur-M2.after.refs` contains neither integration branches nor claims. `cur-M2.readme` contains no `Flow:` line.

### cur-M3

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/cur-M3.jsonl" 2> "$scratch/logs/cur-M3.err"; echo $? > "$scratch/logs/cur-M3.exit"
~~~

- Exit 0. Watch empty in `cur-M3.outside`. Elapsed 0.65 min.
- Last result from `claude-sonnet-5-5` had 12 turns and reported $0.2882269. It opened with `Started: 2026-11-18 18:39` and ended with `Started: 2026-11-18 18:39 · Finished: 2026-11-18 18:39 (under 1 min)`. No stop line.
- `main` before `e1df2eb` and after `c5c2596`. First-parent merges: `c5c2596 Plan todo-cli: status after merging F2`, `f7e85fd Feature F2 (todo-cli): README with install and usage`. First-parent non-merges: ``.
- Pass. `cur-M3.main.merges` shows F2 merge `f7e85fd` and tracking status merge `c5c2596`. The first-parent non-merge list is empty. `cur-M3.readme` marks F2 ✅ merged at `f7e85fd`.

### cur-M4

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/cur-M4.jsonl" 2> "$scratch/logs/cur-M4.err"; echo $? > "$scratch/logs/cur-M4.exit"
~~~

- Exit 0. Watch empty in `cur-M4.outside`. Elapsed 1.55 min.
- Last result from `claude-sonnet-5-5` had 4 turns and reported $0.48243357. It opened with `Started: 2026-11-18 18:39` and ended with `Started: 2026-11-18 18:39 · Finished: 2026-11-18 18:41 (2 min)`. No stop line.
- Pass. `cur-M4.jsonl` and `cur-M4.readme` show wave 2 and B/D ✅ and F1/F3 👀 review. The report asks for both merges. Main stayed at `c5c2596` (`cur-M4.before.refs` and `cur-M4.after.refs`).
- Finding. Expected a Git-recognized `Wave-Model` trailer. In task D commit `82fd76b`, a blank line separated `Wave-Model` from `Co-Authored-By`. `git show -s --format='%(trailers)' 82fd76b` omitted `Wave-Model`. D was low-tier and completed (`cur-M4.jsonl`).

### cur-M5

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/cur-M5.jsonl" 2> "$scratch/logs/cur-M5.err"; echo $? > "$scratch/logs/cur-M5.exit"
~~~

- Exit 0. Watch empty in `cur-M5.outside`. Elapsed 1.25 min.
- Last result from `claude-sonnet-5-5` had 19 turns and reported $0.3842641. It opened with `Started: 2026-11-18 18:42` and ended with `Started: 2026-11-18 18:42 · Finished: 2026-11-18 18:43 (1 min)`. No stop line.
- `main` before `c5c2596` and after `bf50762`. First-parent merges: `bf50762 Plan todo-cli: status after merging F1 F3`, `8973c7e Feature F3 (todo-cli): Tests run on every push`, `f8bc5fe Feature F1 (todo-cli): Tasks stored in todo.json, commands add, list, done`. First-parent non-merges: ``.
- Pass. `cur-M5.main.merges` shows F1 `f8bc5fe`, F3 `8973c7e` and plan status `bf50762`; `cur-M5.main.nonmerges` is empty. All features are ✅ merged in the archive README (`cur-M5.archive`).
- Pass. `cur-M5.archive` was captured from `main:plans/archive/2026-11-02-todo-cli/README.md`. The final snapshot shows only the main worktree and branch.

### cur-M6-pytest

~~~bash
cd "$scratch/cur"
python -m pytest -q > "$scratch/logs/cur-M6-pytest.out" 2> "$scratch/logs/cur-M6-pytest.err"; echo $? > "$scratch/logs/cur-M6-pytest.exit"
~~~

- Exit 0. Watch empty in `cur-M6-pytest.outside`. Elapsed 0.02 min.
- Pass. `cur-M6-pytest.out` reports 11 passed (exit 0).

### cur-M6

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$scratch/logs/cur-M6.jsonl" 2> "$scratch/logs/cur-M6.err"; echo $? > "$scratch/logs/cur-M6.exit"
~~~

- Exit 0. Watch empty in `cur-M6.outside`. Elapsed 0.25 min.
- Last result from `claude-haiku-5-5` had 6 turns and reported $0.005692180000000001. It opened with `Started: 2026-11-18 18:43` and ended with `Started: 2026-11-18 18:43 · Finished: 2026-11-18 18:44 (1 min)`. No stop line.
- Pass. `cur-M6.jsonl` reports `## No active plans` and `Next: no open plan`.

### base-M0

~~~bash
cd "$scratch/base"
python "$working/skills/wave-plan/scripts/status_check.py" plans/2026-11-02-todo-cli > "$scratch/logs/base-M0.out" 2> "$scratch/logs/base-M0.err"; echo $? > "$scratch/logs/base-M0.exit"
~~~

- Exit 0. Watch empty in `base-M0.outside`. Elapsed 0.00 min.
- Pass. Exit 0 with empty stdout and stderr (`base-M0.out` and `base-M0.err`).

### base-M2

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 1" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/base-M2.jsonl" 2> "$scratch/logs/base-M2.err"; echo $? > "$scratch/logs/base-M2.exit"
~~~

- Exit 0. Watch empty in `base-M2.outside`. Elapsed 1.43 min.
- Last result from `claude-sonnet-5-5` had 8 turns and reported $0.40579500999999996. It opened with `Started: 2026-11-18 18:44` and ended with `Started: 2026-11-18 18:44 · Finished: 2026-11-18 18:45 (1 min)`. No stop line.
- Pass. `base-M2.jsonl` opens with `Started:` and shows wave 1 and A/C ✅, F1 🔄 waiting for wave 2, and an F2 👀 review block and merge question.
- Finding. Expected the result to end with the F2 merge question. The question appears immediately before a `Started: … · Finished: …` timing footer in `base-M2.jsonl`.
- Pass. `main` stayed at `0bbe792`; `base-M2.after.refs` contains neither integration branches nor claims. `base-M2.readme` contains no `Flow:` line.
- Finding. Expected task A's commit to contain only its declared files and scope violations to be logged. `f1d10b6` added three `__pycache__` files. Cleanup `1ac1aa5` removed them and added `.gitignore`. The report counted A as done and listed no new problem (`base-M2.jsonl`).

### base-M3

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/base-M3.jsonl" 2> "$scratch/logs/base-M3.err"; echo $? > "$scratch/logs/base-M3.exit"
~~~

- Exit 0. Watch empty in `base-M3.outside`. Elapsed 0.58 min.
- Last result from `claude-sonnet-5-5` had 11 turns and reported $0.22059769999999998. It opened with `Started: 2026-11-18 18:46` and ended with `Started: 2026-11-18 18:46 · Finished: 2026-11-18 18:46 (under 1 min)`. No stop line.
- `main` before `0bbe792` and after `bb9031b`. First-parent merges: `bb9031b Plan todo-cli: status after merging F2`, `5985de8 Feature F2 (todo-cli): README with install and usage`. First-parent non-merges: ``.
- Pass. `base-M3.main.merges` shows F2 merge `5985de8` and tracking status merge `bb9031b`. The first-parent non-merge list is empty. `base-M3.readme` marks F2 ✅ merged at `5985de8`.

### base-M4

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/base-M4.jsonl" 2> "$scratch/logs/base-M4.err"; echo $? > "$scratch/logs/base-M4.exit"
~~~

- Exit 1. Watch empty in `base-M4.outside`. Elapsed 0.13 min.
- Last result from `claude-sonnet-5-5` had 3 turns and reported $0.066606. It opened with `You've hit your 5-hour limit · resets 8:30pm (Asia/Tbilisi)` and ended with `You've hit your 5-hour limit · resets 8:30pm (Asia/Tbilisi)`. This CLI usage-limit message is the stop line.
- Finding. Expected wave 2 and B/D ✅, F1/F3 👀 review and the merge questions. Claude exited 1 with `You've hit your 5-hour limit · resets 8:30pm (Asia/Tbilisi)` in `base-M4.jsonl`. The tracking README stayed at its post-M3 status and the watch was empty. The rehearsal stopped per the procedure-failure rule.
- Pass. `base-M4.before.refs` and `base-M4.after.refs` both put `main` at `bb9031b`.

### base-M5

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/base-M5.jsonl" 2> "$scratch/logs/base-M5.err"; echo $? > "$scratch/logs/base-M5.exit"
~~~

- Not run. The baseline M4 call hit the Claude usage limit.
- Not run. The baseline M4 call hit the Claude usage limit.

### base-M6-pytest

~~~bash
cd "$scratch/base"
python -m pytest -q > "$scratch/logs/base-M6-pytest.out" 2> "$scratch/logs/base-M6-pytest.err"; echo $? > "$scratch/logs/base-M6-pytest.exit"
~~~

- Not run. The baseline M4 call hit the Claude usage limit.

### base-M6

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$scratch/logs/base-M6.jsonl" 2> "$scratch/logs/base-M6.err"; echo $? > "$scratch/logs/base-M6.exit"
~~~

- Not run. The baseline M4 call hit the Claude usage limit.

The sum of the last reported costs was $2.346069325. The 20 USD launch threshold was not reached. The CLI's subscription usage limit stopped the baseline independently.

## Results

| Expectation | Result | Evidence |
|---|---|---|
| P0 launcher and subagent use scratch Python and temp paths with path conversion unset | Pass | Both Bash `tool_result` events in `P0.jsonl`, exit 0 |
| Watch after each command | Pass | All 13 written `.outside` files were empty, including `P0.outside`. |
| cur-M0 status checker exits 0 without output | Pass | Exit 0 with empty stdout and stderr (`cur-M0.out` and `cur-M0.err`). |
| cur-M1 manual dry run declines the plan without driver output | Pass | Exit 0. `cur-M1.out` contains `next: nothing — plans/2026-11-02-todo-cli: manual flow: the driver runs autonomous plans only`. `<scratch>/cur.wave-driver` did not exist. |
| cur-M2 wave 1 succeeds and F2 requests review | Pass | `cur-M2.jsonl` opens with `Started:` and shows `Flow: manual`, wave 1 and A/C ✅, F1 🔄 waiting for wave 2, and an F2 👀 review block and merge question. |
| cur-M2 F2 merge question is the final line | Finding | Expected the result to end with the F2 merge question. The question appears immediately before a `Started: … · Finished: …` timing footer in `cur-M2.jsonl`. |
| cur-M2 main, integration, claims and implicit flow remain as expected | Pass | `main` stayed at `e1df2eb`; `cur-M2.after.refs` contains neither integration branches nor claims. `cur-M2.readme` contains no `Flow:` line. |
| cur-M3 approval merges F2 and records its hash using merge-only main history | Pass | `cur-M3.main.merges` shows F2 merge `f7e85fd` and tracking status merge `c5c2596`. The first-parent non-merge list is empty. `cur-M3.readme` marks F2 ✅ merged at `f7e85fd`. |
| cur-M4 wave 2 succeeds, keeps main fixed and requests both approvals | Pass | `cur-M4.jsonl` and `cur-M4.readme` show wave 2 and B/D ✅ and F1/F3 👀 review. The report asks for both merges. Main stayed at `c5c2596` (`cur-M4.before.refs` and `cur-M4.after.refs`). |
| cur-M4 task D's machine-readable model trailer | Finding | Expected a Git-recognized `Wave-Model` trailer. In task D commit `82fd76b`, a blank line separated `Wave-Model` from `Co-Authored-By`. `git show -s --format='%(trailers)' 82fd76b` omitted `Wave-Model`. D was low-tier and completed (`cur-M4.jsonl`). |
| cur-M5 approval merges F1 and F3 using merge-only main history | Pass | `cur-M5.main.merges` shows F1 `f8bc5fe`, F3 `8973c7e` and plan status `bf50762`; `cur-M5.main.nonmerges` is empty. All features are ✅ merged in the archive README (`cur-M5.archive`). |
| cur-M5 finished plan is archived and worktrees are removed | Pass | `cur-M5.archive` was captured from `main:plans/archive/2026-11-02-todo-cli/README.md`. The final snapshot shows only the main worktree and branch. |
| cur-M6-pytest all 11 P1 and P2 tests pass on main after M5 | Pass | `cur-M6-pytest.out` reports 11 passed (exit 0). |
| cur-M6 status names no plan in progress | Pass | `cur-M6.jsonl` reports `## No active plans` and `Next: no open plan`. |
| base-M0 status checker exits 0 without output | Pass | Exit 0 with empty stdout and stderr (`base-M0.out` and `base-M0.err`). |
| base-M2 wave 1 succeeds and F2 requests review | Pass | `base-M2.jsonl` opens with `Started:` and shows wave 1 and A/C ✅, F1 🔄 waiting for wave 2, and an F2 👀 review block and merge question. |
| base-M2 F2 merge question is the final line | Finding | Expected the result to end with the F2 merge question. The question appears immediately before a `Started: … · Finished: …` timing footer in `base-M2.jsonl`. |
| base-M2 main, integration, claims and implicit flow remain as expected | Pass | `main` stayed at `0bbe792`; `base-M2.after.refs` contains neither integration branches nor claims. `base-M2.readme` contains no `Flow:` line. |
| base-M2 baseline task commit scope and problem logging | Finding | Expected task A's commit to contain only its declared files and scope violations to be logged. `f1d10b6` added three `__pycache__` files. Cleanup `1ac1aa5` removed them and added `.gitignore`. The report counted A as done and listed no new problem (`base-M2.jsonl`). |
| base-M3 approval merges F2 and records its hash using merge-only main history | Pass | `base-M3.main.merges` shows F2 merge `5985de8` and tracking status merge `bb9031b`. The first-parent non-merge list is empty. `base-M3.readme` marks F2 ✅ merged at `5985de8`. |
| base-M4 wave 2 succeeds and requests both approvals | Finding | Expected wave 2 and B/D ✅, F1/F3 👀 review and the merge questions. Claude exited 1 with `You've hit your 5-hour limit · resets 8:30pm (Asia/Tbilisi)` in `base-M4.jsonl`. The tracking README stayed at its post-M3 status and the watch was empty. The rehearsal stopped per the procedure-failure rule. |
| base-M4 main remains fixed | Pass | `base-M4.before.refs` and `base-M4.after.refs` both put `main` at `bb9031b`. |
| base-M5 approval merges F1 and F3 using merge-only history | Not run | The baseline M4 call hit the Claude usage limit. |
| base-M5 all features merge and the finished plan is archived | Not run | The baseline M4 call hit the Claude usage limit. |
| base-M6-pytest all 11 P1 and P2 tests pass on main after M5 | Not run | The baseline M4 call hit the Claude usage limit. |
| base-M6 status names no plan in progress | Not run | The baseline M4 call hit the Claude usage limit. |
| Source refs and objects | Pass | `working-before.refs` and `working-after.refs` each contained 57 identical ref/object pairs. `diff -u` exited 0. The snapshots precede the task commit. |

### Manual flow comparison

Worktree lists omit the checkout on `main`, which was present throughout. Commit counts are first-parent merge/non-merge counts. Statuses come from the README, or the archived README when the tracking branch was removed.

| Step | Repository | Branches created | Worktrees left | Commits on main (merge / non-merge) | README statuses | Report asked a question | Stop line |
|---|---|---|---|---|---|---|---|
| M2 | cur | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F2-usage-readme | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F2-usage-readme, plan/todo-cli | 0 / 0 | F1 🔄, F2 👀 review, F3 ⬜, 1 ✅, 2 ⬜, A ✅, B ⬜, C ✅, D ⬜ | Yes | None |
| M2 | base | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F2-usage-readme | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F2-usage-readme, plan/todo-cli | 0 / 0 | F1 🔄, F2 👀 review, F3 ⬜, 1 ✅, 2 ⬜, A ✅, B ⬜, C ✅, D ⬜ | Yes | None |
| M3 | cur | None | feat/todo-cli/F1-todo-store-and-cli, plan/todo-cli | 2 / 0 | F1 🔄, F2 ✅ merged, F3 ⬜, 1 ✅, 2 ⬜, A ✅, B ⬜, C ✅, D ⬜ | No | None |
| M3 | base | None | feat/todo-cli/F1-todo-store-and-cli, plan/todo-cli | 2 / 0 | F1 🔄, F2 ✅ merged, F3 ⬜, 1 ✅, 2 ⬜, A ✅, B ⬜, C ✅, D ⬜ | No | None |
| M4 | cur | feat/todo-cli/F3-ci-tests | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F3-ci-tests, plan/todo-cli | 0 / 0 | F1 👀 review, F2 ✅ merged, F3 👀 review, 1 ✅, 2 ✅, A ✅, B ✅, C ✅, D ✅ | Yes | None |
| M4 | base | None | feat/todo-cli/F1-todo-store-and-cli, plan/todo-cli | 0 / 0 | F1 🔄, F2 ✅ merged, F3 ⬜, 1 ✅, 2 ⬜, A ✅, B ⬜, C ✅, D ⬜ | No | You've hit your 5-hour limit · resets 8:30pm (Asia/Tbilisi) |
| M5 | cur | None | None | 3 / 0 | F1 ✅ merged, F2 ✅ merged, F3 ✅ merged, 1 ✅, 2 ✅, A ✅, B ✅, C ✅, D ✅ | No | None |
| M5 | base | Not run | Not run | Not run | Not run | Not run | Not run |

M2 and M3 agree across all six comparison columns. The current reports also show `Flow: manual`.

Finding. **Manual flow differs from v2.12.0 in the observed M4 row.** The Claude account limit cut the baseline step short (`base-M4.jsonl`), so its branch, worktree, status, question and stop cells differ from the completed current call. The limit leaves successful baseline M4 behavior and the M5 comparison unverified.

## Not verified

The watch covered the global Python user site and `/c/tmp`. Other paths were outside its coverage.
The successful baseline M4 outcome and the M5 comparison could not be established after the CLI usage limit.

- base-M5 approval merges F1 and F3 using merge-only history. The baseline M4 call hit the Claude usage limit.

- base-M5 all features merge and the finished plan is archived. The baseline M4 call hit the Claude usage limit.

- base-M6-pytest all 11 P1 and P2 tests pass on main after M5. The baseline M4 call hit the Claude usage limit.

- base-M6 status names no plan in progress. The baseline M4 call hit the Claude usage limit.

## Repeat

1. In Git Bash from the source worktree, run both Setup blocks.
2. Run P0 in `cur`. Check its Bash tool results and the watch.
3. Run the listed steps in order, each in its own foreground shell command with its snapshots and watch. Stop after a non-empty watch or before the next Claude call once the reported total reaches 20 USD.
4. Snapshot the source refs again with the Setup command, writing `working-after.refs`, and compare the two snapshots.
