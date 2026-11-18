# Rehearsal: manual flow end to end

2026-11-18 · Claude Code 2.1.326 · source `c07cbe7`

## Setup

The two scratch repositories used the same corrected example, with no `Flow:` line. Current skills came from
`<working folder>` and baseline skills came from the `v2.12.0` archive.

The first attempt was stopped immediately after `cur-M2`. The shell launcher lost a continuation while passing
the command through the tool transport. Claude returned a result, but Bash did not write the exit code. Its scratch
evidence was kept in the first scratch directory. Its P0 exited 0, and both Claude usage tests and all five watches
were empty. A fresh `<scratch>` was created for the documented run. Its Bash launcher passed `bash -n` and captured
17 from a dummy process. The $20 cap includes the first attempt's $0.517246515.

Before the retry's `env.sh` existed, the launcher ran `mktemp -d`, printed the scratch location, and ran the
setup lines through creation of `env.sh`. The first attempt also resolved the scratch path with `cygpath -am`
and read the specified plan sections before creating its environment. Neither attempt ran a source check before
sourcing `env.sh`.

```bash
scratch=$(mktemp -d)
printf '%s\n' "$scratch"
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
"$bin/python" -m pip install pytest pyyaml > "$scratch/logs/setup-pip.txt" 2>&1
pip_status=$?
touch "$scratch/logs/start.stamp"
printf '%s\n' "$pip_status" > "$scratch/logs/setup-pip.exit"
printf '%s\n%s\n' "$gpy" "$usersite" > "$scratch/logs/setup-host.txt"
claude --version > "$scratch/logs/claude-version.txt"

working='<working folder>'
mkdir -p "$scratch/v2120" "$scratch/launch"
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
```

The venv, dependencies, Python temp and user base, and pip cache lived under `<scratch>/venv`, `tmp`, `userbase`
and `pip-cache`. The baseline source archive was extracted to `<scratch>/v2120`. The rehearsal repositories,
installed skills, plans, linked worktrees and any extracted F3 trees lived directly under `<scratch>`. The launcher,
log reader and record generator lived in `<scratch>/launch`. Session streams, exit codes, elapsed times, watch,
usage, snapshots, Git and test evidence lived in `<scratch>/logs`. The public record is the only changed source
file. The watch covers the global Python user site and `/c/tmp`. The source checks also set `PYTHONDONTWRITEBYTECODE=1`.

On Git Bash, the M4 workflow read initially exited 128 in each repository. MSYS rewrote the Git revision
and file argument `feat/todo-cli/F3-ci-tests:.github/workflows/test.yml` as a Windows path list. The original
files and errors are retained as `cur-M4.workflow*.msys-original` and `base-M4.workflow*.msys-original` in
`<scratch>/logs`. A command-scoped `MSYS2_ARG_CONV_EXCL='feat/todo-cli/F3-ci-tests:'` passed the argument to Git
intact. Both workflow reads then exited 0 and produced content. The Claude calls and standalone CI checks had
already completed and were not repeated.

## Runs

### P0

```bash
probe='Run this one command with the Bash tool: command -v python; python -c "import sys, tempfile; print(sys.prefix); print(tempfile.gettempdir())"; echo "pathconv=${MSYS_NO_PATHCONV-unset}". Then launch one subagent and have it run the same command with its Bash tool. Reply with both outputs verbatim.'
MSYS_NO_PATHCONV=1 timeout 600 claude -p "$probe" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 8 --max-budget-usd 0.3 < /dev/null > "$scratch/logs/P0.jsonl" 2> "$scratch/logs/P0.err"; \
  echo $? > "$scratch/logs/P0.exit"
```

- Exit 0. Usage test: no match. Model `claude-haiku-5-5`, 1 turns, `total_cost_usd` 0.00493779, 0.15 wall minutes (`P0.jsonl`, `P0.err`, `P0.exit`, `P0.usage`).
- First non-empty line: The subagent finished. Its output, verbatim:
- Last non-empty line: It matches my own run above.
- Stop line: none.
- Watch: empty (`P0.outside`). Ref and worktree snapshots: `P0.before.*` and `P0.after.*`.
- Pass. The main session and subagent used the scratch venv and temp directory.

### cur-M0

```bash
python "<working folder>/skills/wave-plan/scripts/status_check.py" plans/2026-11-02-todo-cli
```

- Exit 0, 0.00 wall minutes. No output (`cur-M0.txt`, `cur-M0.exit`).
- Watch: empty (`cur-M0.outside`). Ref and worktree snapshots: `cur-M0.before.*` and `cur-M0.after.*`.
- Pass. The status check was silent.

### base-M0

```bash
python "<working folder>/skills/wave-plan/scripts/status_check.py" plans/2026-11-02-todo-cli
```

- Exit 0, 0.00 wall minutes. No output (`base-M0.txt`, `base-M0.exit`).
- Watch: empty (`base-M0.outside`). Ref and worktree snapshots: `base-M0.before.*` and `base-M0.after.*`.
- Pass. The status check was silent.

### cur-M1

```bash
python "<working folder>/scripts/wave_driver.py" plans/2026-11-02-todo-cli --repo . --dry-run
```

- Exit 0, 0.00 wall minutes. next: nothing — plans/2026-11-02-todo-cli: manual flow: the driver runs autonomous plans only (`cur-M1.txt`, `cur-M1.exit`).
- Watch: empty (`cur-M1.outside`). Ref and worktree snapshots: `cur-M1.before.*` and `cur-M1.after.*`.
- Pass. The driver skipped the manual plan and left no driver folder.

### cur-M2

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 1" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/cur-M2.jsonl" 2> "$scratch/logs/cur-M2.err"; \
  echo $? > "$scratch/logs/cur-M2.exit"
```

- Exit 0. Usage test: no match. Model `claude-sonnet-5-5`, 10 turns, `total_cost_usd` 0.51191196, 1.60 wall minutes (`cur-M2.jsonl`, `cur-M2.err`, `cur-M2.exit`, `cur-M2.usage`).
- First non-empty line: Started: 2026-11-18 22:07
- Last non-empty line: Started: 2026-11-18 22:07 · Finished: 2026-11-18 22:09 (2 min)
- Stop line: none.
- Watch: empty (`cur-M2.outside`). Ref and worktree snapshots: `cur-M2.before.*` and `cur-M2.after.*`.
- Pass. Wave 1 completed and F2 was offered for review.

```text
Merge F2 "README with install and usage" — adds the user README (`feat/todo-cli/F2-usage-readme`) into main? Answer: merge F2 · later · problems F2: <what is wrong>
Started: 2026-11-18 22:07 · Finished: 2026-11-18 22:09 (2 min)
```

### base-M2

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 1" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/base-M2.jsonl" 2> "$scratch/logs/base-M2.err"; \
  echo $? > "$scratch/logs/base-M2.exit"
```

- Exit 0. Usage test: no match. Model `claude-sonnet-5-5`, 6 turns, `total_cost_usd` 0.41872633, 1.52 wall minutes (`base-M2.jsonl`, `base-M2.err`, `base-M2.exit`, `base-M2.usage`).
- First non-empty line: Started: 2026-11-18 22:09
- Last non-empty line: Started: 2026-11-18 22:09 · Finished: 2026-11-18 22:10 (1 min)
- Stop line: none.
- Watch: empty (`base-M2.outside`). Ref and worktree snapshots: `base-M2.before.*` and `base-M2.after.*`.
- Pass. Wave 1 completed and F2 was offered for review.

```text
Merge F2 "README with install and usage" — adds a README with install steps, the three commands and an example session (feat/todo-cli/F2-usage-readme) into main? Answer: merge F2 · later · problems F2: <what is wrong>
Started: 2026-11-18 22:09 · Finished: 2026-11-18 22:10 (1 min)
```

### cur-M3

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/cur-M3.jsonl" 2> "$scratch/logs/cur-M3.err"; \
  echo $? > "$scratch/logs/cur-M3.exit"
```

- Exit 0. Usage test: no match. Model `claude-sonnet-5-5`, 14 turns, `total_cost_usd` 0.31501240, 0.73 wall minutes (`cur-M3.jsonl`, `cur-M3.err`, `cur-M3.exit`, `cur-M3.usage`).
- First non-empty line: Started: 2026-11-18 22:11
- Last non-empty line: Started: 2026-11-18 22:11 · Finished: 2026-11-18 22:13 (2 min)
- Stop line: none.
- Watch: empty (`cur-M3.outside`). Ref and worktree snapshots: `cur-M3.before.*` and `cur-M3.after.*`.
- Pass. F2 merged with its tracking status update.

### base-M3

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/base-M3.jsonl" 2> "$scratch/logs/base-M3.err"; \
  echo $? > "$scratch/logs/base-M3.exit"
```

- Exit 0. Usage test: no match. Model `claude-sonnet-5-5`, 12 turns, `total_cost_usd` 0.21804060, 0.57 wall minutes (`base-M3.jsonl`, `base-M3.err`, `base-M3.exit`, `base-M3.usage`).
- First non-empty line: Started: 2026-11-18 22:14
- Last non-empty line: One correction: the `Merged 2026-11-18 22:15` line in `waves/w01.md` Execution has a time one minute later than the clock at the end of the run. I typed the time by hand instead of reading it from the clock.
- Stop line: none.
- Watch: empty (`base-M3.outside`). Ref and worktree snapshots: `base-M3.before.*` and `base-M3.after.*`.
- Pass. F2 merged with its tracking status update.

### cur-M4

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/cur-M4.jsonl" 2> "$scratch/logs/cur-M4.err"; \
  echo $? > "$scratch/logs/cur-M4.exit"
```

- Exit 0. Usage test: no match. Model `claude-sonnet-5-5`, 6 turns, `total_cost_usd` 0.55906840, 1.73 wall minutes (`cur-M4.jsonl`, `cur-M4.err`, `cur-M4.exit`, `cur-M4.usage`).
- First non-empty line: Started: 2026-11-18 22:15
- Last non-empty line: Started: 2026-11-18 22:15 · Finished: 2026-11-18 22:17 (2 min)
- Stop line: none.
- Watch: empty (`cur-M4.outside`). Ref and worktree snapshots: `cur-M4.before.*` and `cur-M4.after.*`.
- Pass. Wave 2 completed and F1 and F3 were offered for review.

```text
Merge F1 "Tasks stored in todo.json, commands add, list, done" — adds the `todo` tool with `add`, `list` and `done` (feat/todo-cli/F1-todo-store-and-cli) into main? Answer: merge F1 · later · problems F1: <what is wrong>
Merge F3 "Tests run on every push" — adds a GitHub Actions workflow that runs pytest on Python 3.10 and 3.12 (feat/todo-cli/F3-ci-tests) into main? Answer: merge F3 · later · problems F3: <what is wrong>
Started: 2026-11-18 22:15 · Finished: 2026-11-18 22:17 (2 min)
```

### base-M4

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/base-M4.jsonl" 2> "$scratch/logs/base-M4.err"; \
  echo $? > "$scratch/logs/base-M4.exit"
```

- Exit 0. Usage test: no match. Model `claude-sonnet-5-5`, 7 turns, `total_cost_usd` 0.43396740, 1.55 wall minutes (`base-M4.jsonl`, `base-M4.err`, `base-M4.exit`, `base-M4.usage`).
- First non-empty line: Started: 2026-11-18 22:18
- Last non-empty line: Started: 2026-11-18 22:18 · Finished: 2026-11-18 22:19 (1 min)
- Stop line: none.
- Watch: empty (`base-M4.outside`). Ref and worktree snapshots: `base-M4.before.*` and `base-M4.after.*`.
- Pass. Wave 2 completed and F1 and F3 were offered for review.

```text
Merge F1 "Tasks stored in `todo.json`, commands `add`, `list`, `done`" — adds the `todo` command with `add`, `list` and `done` (feat/todo-cli/F1-todo-store-and-cli) into main? Answer: merge F1 · later · problems F1: <what is wrong>
Merge F3 "Tests run on every push" — adds the CI workflow for Python 3.10 and 3.12 (feat/todo-cli/F3-ci-tests) into main? Answer: merge F3 · later · problems F3: <what is wrong>
Started: 2026-11-18 22:18 · Finished: 2026-11-18 22:19 (1 min)
```

### cur-M5

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/cur-M5.jsonl" 2> "$scratch/logs/cur-M5.err"; \
  echo $? > "$scratch/logs/cur-M5.exit"
```

- Exit 1. Usage test: match. Model `claude-sonnet-5-5`, 8 turns, `total_cost_usd` 0.23071250, 0.33 wall minutes (`cur-M5.jsonl`, `cur-M5.err`, `cur-M5.exit`, `cur-M5.usage`).
- Not run (usage limit). You've hit your 5-hour limit · resets <reset>
- Stop line: none.
- Main cb90eaa → cb90eaa. No first-parent commits were added (`cur-M5.before.main`, `cur-M5.after.main`, `cur-M5.main-commits`, `cur-M5.nonmerges`).
- Watch: empty (`cur-M5.outside`). Ref and worktree snapshots: `cur-M5.before.*` and `cur-M5.after.*`.

### base-M5

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/base-M5.jsonl" 2> "$scratch/logs/base-M5.err"; \
  echo $? > "$scratch/logs/base-M5.exit"
```

- Not run (usage limit). Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.

### cur-M6-pytest

```bash
python -m pytest -q
```

- Not run. The F1 test suite is absent from main after the usage stop (`cur-M6-pytest.main-tree`).

### base-M6-pytest

```bash
python -m pytest -q
```

- Not run. The F1 test suite is absent from main after the usage stop (`base-M6-pytest.main-tree`).

### cur-M6

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$scratch/logs/cur-M6.jsonl" 2> "$scratch/logs/cur-M6.err"; \
  echo $? > "$scratch/logs/cur-M6.exit"
```

- Not run (usage limit). Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.

### base-M6

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$scratch/logs/base-M6.jsonl" 2> "$scratch/logs/base-M6.err"; \
  echo $? > "$scratch/logs/base-M6.exit"
```

- Not run (usage limit). Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.

## Results

Evidence filenames below are relative to `<scratch>/logs/`.
Reported usage for both attempts totalled $3.20962390 in the last results' `total_cost_usd` values against a $20 cap.
The usage limit stopped the last Claude call at cur-M5.

| Expectation | Result | Evidence |
| --- | --- | --- |
| P0 isolates the session and subagent | Pass | `P0.jsonl` has 2 matching Bash tool results: venv Python, prefix and temp under `<scratch>`, `pathconv=unset`. `P0.exit` is 0 |
| P21 watch after every executed step | Pass | All 11 `.outside` files are empty |
| P22 usage scan, snapshots and exit result for each Claude command | Pass | 8 calls have `.exit`, `.usage`, `.before.*` and `.after.*` evidence; usage matches: cur-M5 |
| P22 usage stop prevents every later Claude call | Pass | `cur-M5.usage`, `cur-M5.exit`, `cur-M5.after.refs`, `cur-M5.outside`. Later Claude steps have no call logs |
| I22 scratch isolation for source checks and generated files | Pass | `env.sh` was sourced before source checks; final check files in `<scratch>/logs`; see Setup |
| Working folder refs unchanged across the calls | Pass | `working-before.refs` and `working-after.refs` |
| Final wave check passes under the scratch environment | Pass | Exit codes for `final-check-status-suite.txt` = 0, `final-check-unit-suite.txt` = 0, `final-check-examples.txt` = 0, `final-check-diff.txt` = 0 |
| cur-M0 status check is silent and exits 0 | Pass | Exit 0, output empty (`cur-M0.exit`, `cur-M0.txt`) |
| base-M0 status check is silent and exits 0 | Pass | Exit 0, output empty (`base-M0.exit`, `base-M0.txt`) |
| cur-M1 driver skips manual flow and creates no driver folder | Pass | `next: nothing — plans/2026-11-02-todo-cli: manual flow: the driver runs autonomous plans only`, driver folder absent (`cur-M1.exit`, `cur-M1.txt`, `cur-M1.driver-dir`) |
| cur-M2 wave 1 and tasks A/C done, F2 in review, and F1 waits for wave 2 | Pass | W1 ✅, A ✅, C ✅, F1 🔄, F2 👀 review (`cur-M2.tracking-readme`) |
| cur-M2 last result opens with Started | Pass | Expected `Started:`, observed `Started: 2026-11-18 22:07` (`cur-M2.jsonl`) |
| cur-M2 F2 review block present | Pass | F2 review block present (`cur-M2.jsonl`) |
| cur-M2 no integration/claim refs or tracking Flow line | Pass | Integration/claims absent, tracking Flow absent (`cur-M2.after.refs`, `cur-M2.tracking-readme`) |
| cur-M2 current report says Flow: manual | Pass | `Flow: manual` present (`cur-M2.jsonl`) |
| cur-M2 main stays unchanged without approval | Pass | 2a6fae8 → 2a6fae8 (`cur-M2.before.main`, `cur-M2.after.main`) |
| cur-M2 I19 report ends with questions for F2 then the footer | Pass | Observed F2. The lines are quoted above (`cur-M2.jsonl`) |
| cur-M2 current task commits satisfy scope and Wave-Model checks | Pass | Commits A c3c5029, C 72198eb. Scope exceptions none. Unreadable trailers none (`cur-M2.trailers`, `cur-M2.paths`) |
| cur-M4 I18 wave 2 and tasks B/D done and F1 and F3 in review | Pass | W2 ✅, B ✅, D ✅, F1 👀 review, F3 👀 review (`cur-M4.tracking-readme`) |
| cur-M4 main stays unchanged without approval | Pass | cb90eaa → cb90eaa (`cur-M4.before.main`, `cur-M4.after.main`) |
| cur-M4 I19 report ends with questions for F1, F3 then the footer | Pass | Observed F1, F3. The lines are quoted above (`cur-M4.jsonl`) |
| cur-M4 current task commits satisfy scope and Wave-Model checks | Pass | Commits A c3c5029, B 7376142, C 72198eb, D baf06c8. Scope exceptions none. Unreadable trailers none (`cur-M4.trailers`, `cur-M4.paths`) |
| cur-M4 I18 no open problem on plan/todo-cli | Pass | Open entries none (`cur-M4.tracking-problems`) |
| cur-M4 I18 F3 runs its own test command and needs no F1 files | Pass | Workflow show exit 0, dependency count 0, F3 extract exit 0, CI command exit 0 (`cur-M4.workflow`, `cur-M4.workflow-deps`, `cur-M4.ci-alone`, `cur-M4.ci-alone.exit`) |
| cur-M3 approved merges only, with their hashes in feature statuses | Pass | 2a6fae8 → cb90eaa. F2 e1cdad7. 2 first-parent commits, 0 non-merges (`cur-M3.main-commits`, `cur-M3.nonmerges`) |
| cur-M5 I20 approved merges only, with their hashes in feature statuses | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| cur-M5 I20 merge finishes without a stop line | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| cur-M5 I20 all features merged and the plan is archived | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| cur-M5 I21 both Merged lines equal their commit times | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| cur-M6-pytest I20 all 11 tests pass on main | Not run | The F1 test suite is absent from main after the usage stop (`cur-M6-pytest.main-tree`) |
| cur-M6 I20 status shows no active plan and names the archived plan | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| base-M2 wave 1 and tasks A/C done, F2 in review, and F1 waits for wave 2 | Pass | W1 ✅, A ✅, C ✅, F1 🔄, F2 👀 review (`base-M2.tracking-readme`) |
| base-M2 last result opens with Started | Pass | Expected `Started:`, observed `Started: 2026-11-18 22:09` (`base-M2.jsonl`) |
| base-M2 F2 review block present | Pass | F2 review block present (`base-M2.jsonl`) |
| base-M2 no integration/claim refs or tracking Flow line | Pass | Integration/claims absent, tracking Flow absent (`base-M2.after.refs`, `base-M2.tracking-readme`) |
| base-M2 main stays unchanged without approval | Pass | 59df659 → 59df659 (`base-M2.before.main`, `base-M2.after.main`) |
| base-M2 I19 report ends with questions for F2 then the footer | Pass | Observed F2. The lines are quoted above (`base-M2.jsonl`) |
| base-M2 baseline task scope and trailer evidence recorded | Pass | Commits A f1781f0, C 051c25b. Scope exceptions none. Unreadable trailers none (`base-M2.trailers`, `base-M2.paths`) |
| base-M4 I18 wave 2 and tasks B/D done and F1 and F3 in review | Pass | W2 ✅, B ✅, D ✅, F1 👀 review, F3 👀 review (`base-M4.tracking-readme`) |
| base-M4 main stays unchanged without approval | Pass | 382347a → 382347a (`base-M4.before.main`, `base-M4.after.main`) |
| base-M4 I19 report ends with questions for F1, F3 then the footer | Pass | Observed F1, F3. The lines are quoted above (`base-M4.jsonl`) |
| base-M4 baseline task scope and trailer evidence recorded | Pass | Commits A f1781f0, B 21bf99d, C 051c25b, D eb791ec. Scope exceptions none. Unreadable trailers D eb791ec (`base-M4.trailers`, `base-M4.paths`) |
| base-M4 I18 no open problem on plan/todo-cli | Pass | Open entries none (`base-M4.tracking-problems`) |
| base-M4 I18 F3 runs its own test command and needs no F1 files | Pass | Workflow show exit 0, dependency count 0, F3 extract exit 0, CI command exit 0 (`base-M4.workflow`, `base-M4.workflow-deps`, `base-M4.ci-alone`, `base-M4.ci-alone.exit`) |
| base-M3 approved merges only, with their hashes in feature statuses | Pass | 59df659 → 382347a. F2 591b296. 2 first-parent commits, 0 non-merges (`base-M3.main-commits`, `base-M3.nonmerges`) |
| base-M5 I20 approved merges only, with their hashes in feature statuses | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| base-M5 I20 merge finishes without a stop line | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| base-M5 I20 all features merged and the plan is archived | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| base-M5 I21 baseline Merged line times and commit times recorded | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| base-M6-pytest I20 all 11 tests pass on main | Not run | The F1 test suite is absent from main after the usage stop (`base-M6-pytest.main-tree`) |
| base-M6 I20 status shows no active plan and names the archived plan | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |
| M2 manual flow matches v2.12.0 in the comparison | Pass | Paired comparison rows and their ref, worktree, main and report evidence |
| M3 manual flow matches v2.12.0 in the comparison | Pass | Paired comparison rows and their ref, worktree, main and report evidence |
| M4 manual flow matches v2.12.0 in the comparison | Pass | Paired comparison rows and their ref, worktree, main and report evidence |
| M5 manual flow matches v2.12.0 in the comparison | Not run (usage limit) | Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit` |

The comparison counts commits added to `main` by each step. Worktrees listed are in addition to the main
checkout. M5 statuses come from the archived README if the tracking branch was removed. Hashes and wording
are recorded in the logs and are expected to vary across repositories.

| Step | Branches created | Worktrees left | Commits on main (merge / non-merge) | README statuses after the step | Report asked a merge question | Stop line | Task commits: out-of-scope paths and what happened | Task commits without a readable Wave-Model | Merged line times vs merge commits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cur-M2 | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F2-usage-readme | todo-cli-F1, todo-cli-F2, todo-cli-plan | 0 / 0 | W1 ✅, W2 ⬜, A ✅, B ⬜, C ✅, D ⬜, F1 🔄, F2 👀 review, F3 ⬜ | F2 | None | None | None | No merge |
| base-M2 | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F2-usage-readme | todo-cli-F1, todo-cli-F2, todo-cli-plan | 0 / 0 | W1 ✅, W2 ⬜, A ✅, B ⬜, C ✅, D ⬜, F1 🔄, F2 👀 review, F3 ⬜ | F2 | None | None | None | No merge |
| cur-M3 | None | todo-cli-F1, todo-cli-plan | 2 / 0 | W1 ✅, W2 ⬜, A ✅, B ⬜, C ✅, D ⬜, F1 🔄, F2 ✅ merged, F3 ⬜ | No | None | No task commits | No task commits | No merge |
| base-M3 | None | todo-cli-F1, todo-cli-plan | 2 / 0 | W1 ✅, W2 ⬜, A ✅, B ⬜, C ✅, D ⬜, F1 🔄, F2 ✅ merged, F3 ⬜ | No | None | No task commits | No task commits | No merge |
| cur-M4 | feat/todo-cli/F3-ci-tests | todo-cli-F1, todo-cli-F3, todo-cli-plan | 0 / 0 | W1 ✅, W2 ✅, A ✅, B ✅, C ✅, D ✅, F1 👀 review, F2 ✅ merged, F3 👀 review | F1, F3 | None | None | None | No merge |
| base-M4 | feat/todo-cli/F3-ci-tests | todo-cli-F1, todo-cli-F3, todo-cli-plan | 0 / 0 | W1 ✅, W2 ✅, A ✅, B ✅, C ✅, D ✅, F1 👀 review, F2 ✅ merged, F3 👀 review | F1, F3 | None | None | D eb791ec · intended (P23) | No merge |
| cur-M5 | Not run | Not run | Not run | Not run | Not run | Not run | Not run | Not run | Not run |
| base-M5 | Not run | Not run | Not run | Not run | Not run | Not run | Not run | Not run | Not run |

## Not verified

- The watch checked the Python user site and `/c/tmp`. The run did not check other host paths or Claude Code's global application state.
- F3's GitHub Actions job was exercised locally against its feature tree. It was not dispatched on GitHub.
- The autonomous rehearsal was not repeated. The merge-time rule is shared with the autonomous flow.

- Not run (usage limit). cur-M5 I20 approved merges only, with their hashes in feature statuses. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run (usage limit). cur-M5 I20 merge finishes without a stop line. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run (usage limit). cur-M5 I20 all features merged and the plan is archived. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run (usage limit). cur-M5 I21 both Merged lines equal their commit times. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run. cur-M6-pytest I20 all 11 tests pass on main. The F1 test suite is absent from main after the usage stop (`cur-M6-pytest.main-tree`).
- Not run (usage limit). cur-M6 I20 status shows no active plan and names the archived plan. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run (usage limit). base-M5 I20 approved merges only, with their hashes in feature statuses. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run (usage limit). base-M5 I20 merge finishes without a stop line. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run (usage limit). base-M5 I20 all features merged and the plan is archived. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run (usage limit). base-M5 I21 baseline Merged line times and commit times recorded. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run. base-M6-pytest I20 all 11 tests pass on main. The F1 test suite is absent from main after the usage stop (`base-M6-pytest.main-tree`).
- Not run (usage limit). base-M6 I20 status shows no active plan and names the archived plan. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.
- Not run (usage limit). M5 manual flow matches v2.12.0 in the comparison. Usage stop in `cur-M5.jsonl`, `cur-M5.usage`, `cur-M5.exit`.

## Repeat

Use Git Bash. Run the setup commands above in an empty scratch directory. In each new shell, run the following
before its command. Set `repo` to `cur` or `base` and `step` to the named run.

```bash
. "$scratch/env.sh"
export CLAUDE_ENV_FILE="$(cygpath -m "$scratch")/env.sh"
cd "$scratch/$repo"
```

Take `git for-each-ref --format='%(refname) %(objectname)'` and `git worktree list --porcelain` snapshots before
and after each command. Run P0 first, then run the commands under **Runs** in order, one per foreground shell.
After every Claude command, before the second snapshot, check usage. After the snapshot, run the watch.

```bash
grep -l -i -E "hit your .*limit|usage limit" "$scratch/logs/$step.jsonl" "$scratch/logs/$step.err"
{ find "$usersite" -maxdepth 1 -newer "$scratch/logs/start.stamp" 2>/dev/null
  [ -d /c/tmp ] && find /c/tmp -maxdepth 1 -newer "$scratch/logs/start.stamp"; } > "$scratch/logs/$step.outside"
```

Stop before the skill calls if P0 fails, after the first non-empty watch, or before the next Claude command at
$20 summed `total_cost_usd`. A usage match ends subsequent Claude calls. Read the last `result` event of each
stream. Verify the task commits after both M2 calls and after both M4 calls.

```bash
git log --all --no-merges --grep='^todo-cli F[0-9]* / [A-Z]*:' \
  --format="%h %s | %(trailers:key=Wave-Model,valueonly,separator=%x2C)"
git log --all --no-merges --grep='^todo-cli F[0-9]* / [A-Z]*:' --name-only --format='== %h %s'
```

At M3 and M5, record `git rev-parse main` before and after. Compare with
`git rev-list --no-merges --first-parent <before>..main` and the first-parent merge log. At M4 inspect F3's
workflow and run its test command against the F3 branch alone. At M5 compare recorded merge times against
the merge commits.

```bash
MSYS2_ARG_CONV_EXCL='feat/todo-cli/F3-ci-tests:' git show feat/todo-cli/F3-ci-tests:.github/workflows/test.yml > "$scratch/logs/$repo-M4.workflow"
grep -c -e '-e \.' -e 'pyproject' "$scratch/logs/$repo-M4.workflow" > "$scratch/logs/$repo-M4.workflow-deps"
mkdir "$scratch/$repo-F3-alone"
git archive feat/todo-cli/F3-ci-tests | tar -x -C "$scratch/$repo-F3-alone"
(cd "$scratch/$repo-F3-alone" && bash -c 'python -m pytest -q || [ $? -eq 5 ]') \
  > "$scratch/logs/$repo-M4.ci-alone" 2>&1; echo $? > "$scratch/logs/$repo-M4.ci-alone.exit"
git show main:plans/archive/2026-11-02-todo-cli/waves/w02.md | grep -E '^Merged ' \
  > "$scratch/logs/$repo-M5.merged-lines"
while read -r _ day hm id hash _; do
  at=$(git log -1 --format=%cd --date=format:'%Y-%m-%d %H:%M' "$hash")
  printf '%s line=%s %s commit=%s\n' "$id" "$day" "${hm%:}" "$at"
done < "$scratch/logs/$repo-M5.merged-lines" > "$scratch/logs/$repo-M5.merge-times"
```

After the last call, compare the source ref snapshot with `working-before.refs`. Source the environment again
and run the final check in `<working folder>` before committing the record.

```bash
. "$scratch/env.sh"
cd "<working folder>"
export PYTHONDONTWRITEBYTECODE=1
python skills/wave-plan/scripts/test_status_check.py
python -m unittest discover -s scripts/tests
for p in examples/*/; do python skills/wave-plan/scripts/status_check.py "${p%/}"; done
git diff --check
```
