# Rehearsal: manual flow end to end

2026-11-18 · Claude Code 2.1.326 · source `c07cbe7` · continued 2026-11-19 from M4

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

**Continuation.** The first `cur-M5` call hit the usage limit. All 11 checks of the preserved M4 state passed
(`<scratch>/logs/continue-state.txt`). The stopped attempt's `cur-M5.*` files and both pytest main-tree snapshots
are in `<scratch>/logs/limit-stop/`. The continuation used `<scratch>/launch/continue.sh` and a fresh
`<scratch>/logs/continue.stamp`. The watch's two path checks use the new stamp, the only launcher change
(`<scratch>/logs/continue-launcher.diff`). Only the `scratch=` assignment ran before sourcing `env.sh`.

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

- Launcher exit 0, CLI exit 0. Usage test: no match. Model `claude-sonnet-5-5`, 15 turns, `total_cost_usd` 0.34299980, 0.75 wall minutes (`cur-M5.jsonl`, `cur-M5.err`, `cur-M5.exit`, `cur-M5.usage`).
- First non-empty line: `## Merge · todo-cli`
- Last non-empty line: “Started: 2026-11-19 02:23 · Finished: 2026-11-19 02:24 (1 min)”
- Stop line: none.
- Main `cb90eaa` → `c0b79e7` (`cur-M5.before.main`, `cur-M5.after.main`, `cur-M5.main-commits`, `cur-M5.nonmerges`).
- Watch: empty (`cur-M5.outside`). Ref and worktree snapshots: `cur-M5.before.*` and `cur-M5.after.*`.
- The stopped attempt remains in `limit-stop/` (`cur-M5.*`, including the stream, stderr, exit 1, usage match, watch, snapshots and both `M6-pytest.main-tree` files). Its limit message ended with `resets <reset>`.
- Pass (I21, I24). F1 and F3 merged and the plan was archived. The archived `waves/w02.md` writes both lines as list items (`- Merged`, lines 63–64); the first scan, anchored at `^Merged `, matched neither, and its files are kept in `anchored-scan/`. The corrected scan gives both lines at 02:24, equal to Git for `2177196` and `a5f9730` (`cur-M5.merge-times`).

### base-M5

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/base-M5.jsonl" 2> "$scratch/logs/base-M5.err"; \
  echo $? > "$scratch/logs/base-M5.exit"
```

- Launcher exit 0, CLI exit 0. Usage test: no match. Model `claude-sonnet-5-5`, 15 turns, `total_cost_usd` 0.29660340, 0.90 wall minutes (`base-M5.jsonl`, `base-M5.err`, `base-M5.exit`, `base-M5.usage`).
- First non-empty line: `Started: 2026-11-19 02:24`
- Last non-empty line: “Started: 2026-11-19 02:24 · Finished: 2026-11-19 02:25 (1 min)”
- Stop line: none.
- Main `382347a` → `93291f0` (`base-M5.before.main`, `base-M5.after.main`, `base-M5.main-commits`, `base-M5.nonmerges`).
- Watch: empty (`base-M5.outside`). Ref and worktree snapshots: `base-M5.before.*` and `base-M5.after.*`.
- Pass. F1 and F3 merged, the plan was archived and the two recorded times match their commits.

### cur-M6-pytest

```bash
python -m pytest -q
```

- Launcher exit 0, pytest exit 0, 0.00 wall minutes. Pass. Observed `11 passed in 0.07s` (`cur-M6-pytest.txt`, `cur-M6-pytest.exit`).
- Main `c0b79e7` → `c0b79e7` (`cur-M6-pytest.before.main`, `cur-M6-pytest.after.main`, `cur-M6-pytest.main-commits`, `cur-M6-pytest.nonmerges`).
- Watch: empty (`cur-M6-pytest.outside`). Ref and worktree snapshots: `cur-M6-pytest.before.*` and `cur-M6-pytest.after.*`.

### base-M6-pytest

```bash
python -m pytest -q
```

- Launcher exit 0, pytest exit 0, 0.02 wall minutes. Pass (I25). Observed `13 passed in 0.10s` (`base-M6-pytest.txt`, `base-M6-pytest.exit`): the 11 acceptance tests and two tests the baseline's task B added for the empty-text and corrupt-file rows (`tests/test_cli.py:52,56`).
- Main `93291f0` → `93291f0` (`base-M6-pytest.before.main`, `base-M6-pytest.after.main`, `base-M6-pytest.main-commits`, `base-M6-pytest.nonmerges`).
- Watch: empty (`base-M6-pytest.outside`). Ref and worktree snapshots: `base-M6-pytest.before.*` and `base-M6-pytest.after.*`.

### cur-M6

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$scratch/logs/cur-M6.jsonl" 2> "$scratch/logs/cur-M6.err"; \
  echo $? > "$scratch/logs/cur-M6.exit"
```

- Launcher exit 0, CLI exit 0. Usage test: no match. Model `claude-haiku-5-5`, 5 turns, `total_cost_usd` 0.00976163, 0.28 wall minutes (`cur-M6.jsonl`, `cur-M6.err`, `cur-M6.exit`, `cur-M6.usage`).
- First non-empty line: `Started: 2026-11-19 02:26`
- Last non-empty line: “Started: 2026-11-19 02:26 · Finished: 2026-11-19 02:26 (under 1 min)”
- Stop line: none.
- Main `c0b79e7` → `c0b79e7` (`cur-M6.before.main`, `cur-M6.after.main`, `cur-M6.main-commits`, `cur-M6.nonmerges`).
- Watch: empty (`cur-M6.outside`). Ref and worktree snapshots: `cur-M6.before.*` and `cur-M6.after.*`.
- Pass (I26). The report says there is no active plan and that `plans/` holds only `archive/`, which it did not read, as `wave-status` "Input" and "What to read" say in both versions.

### base-M6

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$scratch/logs/base-M6.jsonl" 2> "$scratch/logs/base-M6.err"; \
  echo $? > "$scratch/logs/base-M6.exit"
```

- Launcher exit 0, CLI exit 0. Usage test: no match. Model `claude-haiku-5-5`, 6 turns, `total_cost_usd` 0.00546442, 0.23 wall minutes (`base-M6.jsonl`, `base-M6.err`, `base-M6.exit`, `base-M6.usage`).
- First non-empty line: `Started: 2026-11-19 02:26`
- Last non-empty line: “Finished: 2026-11-19 02:27”
- Stop line: none.
- Main `93291f0` → `93291f0` (`base-M6.before.main`, `base-M6.after.main`, `base-M6.main-commits`, `base-M6.nonmerges`).
- Watch: empty (`base-M6.outside`). Ref and worktree snapshots: `base-M6.before.*` and `base-M6.after.*`.
- Pass. The report names archived plan `2026-11-02-todo-cli` and reports no active plan.

## Results

Evidence filenames below are relative to `<scratch>/logs/`.
Reported usage through the continuation totalled $3.86445314 in the last results' `total_cost_usd` values against a $20 cap.

Three expectations of the plan were corrected after the run (P28). A `Merged` line is a list item (`- Merged`)
when its Execution is a list, so the M5 scan accepts both forms (I24). The example's 11 acceptance tests must pass
and an executor may add more, so the pytest check is exit 0 with at least 11 passed (I25). `wave-status` does not
read `plans/archive/`, so M6 must report no active plan and may name the archived one (I26).

| Expectation | Result | Evidence |
| --- | --- | --- |
| P0 isolates the session and subagent | Pass | `P0.jsonl` has 2 matching Bash tool results: venv Python, prefix and temp under `<scratch>`, `pathconv=unset`. `P0.exit` is 0 |
| P21 watch after every executed step | Pass | All 17 `.outside` files are empty, including six continuation watches |
| P22 usage scan, snapshots and exit result for each Claude command | Pass | 12 calls have `.exit`, `.usage`, `.before.*` and `.after.*` evidence. The sole match was the original `cur-M5` |
| P22 usage stop prevents every later Claude call | Pass | `limit-stop/cur-M5.usage`, `limit-stop/cur-M5.exit`, `limit-stop/cur-M5.after.refs`, `limit-stop/cur-M5.outside`. Calls resumed after the preserved state check |
| I22 scratch isolation for source checks and generated files | Pass | `env.sh` was sourced before source checks; final check files in `<scratch>/logs`; see Setup |
| Working folder refs unchanged across the calls | Pass | `working-before.refs` / `working-after.refs` and `working-before-continue.refs` / `working-after-continue.refs`. Each pair matches |
| Final wave check passes under the scratch environment | Pass | 33 status-check tests, 59 driver tests, all example status checks, and `git diff --check` pass (`continue-check.txt`) |
| I23 continuation from the preserved M4 state | Pass | All 11 checks exited 0 in `continue-state.txt`. See `continue-launcher.diff` and `limit-stop/` |
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
| cur-M3 I21 Merged line time equals its merge commit | Pass | F2 line 22:11, commit 22:11 (`cur-M3.merge-times`) |
| cur-M5 I20 approved merges only, with their hashes in feature statuses | Pass | `cb90eaa` → `c0b79e7` (3 merges, 0 non-merges). F1 `2177196`, F3 `a5f9730` (`cur-M5.archive-readme`, `cur-M5.main-commits`, `cur-M5.nonmerges`) |
| cur-M5 I20 merge finishes without a stop line | Pass | Launcher and CLI exit 0, no usage match or stop line (`cur-M5.exit`, `cur-M5.usage`, `cur-M5.jsonl`) |
| cur-M5 I20 all features merged and the plan is archived | Pass | F1, F2 and F3 merged. Plan at `plans/archive/2026-11-02-todo-cli/` (`cur-M5.archive-readme`) |
| cur-M5 I21 both Merged lines equal their commit times | Pass | I24: F1 and F3 lines 02:24, commits 02:24 by the corrected scan; the anchored first scan is in `anchored-scan/` (`cur-M5.merge-times`, archived `waves/w02.md:63–64`) |
| cur-M6-pytest I20 the 11 acceptance tests pass on main | Pass | 11 passed, exit 0 (`cur-M6-pytest.txt`) |
| cur-M6 I20 status shows no active plan | Pass | I26: no active plan; `archive/` named, not read (`cur-M6.jsonl`) |
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
| base-M3 I21 baseline Merged line time recorded | Pass | F2 line 22:15, commit 22:14 · intended (P25) (`base-M3.merge-times`) |
| base-M5 I20 approved merges only, with their hashes in feature statuses | Pass | `382347a` → `93291f0` (3 merges, 0 non-merges). F1 `7b5c535`, F3 `c6d3af4` (`base-M5.archive-readme`, `base-M5.main-commits`, `base-M5.nonmerges`) |
| base-M5 I20 merge finishes without a stop line | Pass | Launcher and CLI exit 0, no usage match or stop line (`base-M5.exit`, `base-M5.usage`, `base-M5.jsonl`) |
| base-M5 I20 all features merged and the plan is archived | Pass | F1, F2 and F3 merged. Plan at `plans/archive/2026-11-02-todo-cli/` (`base-M5.archive-readme`) |
| base-M5 I21 baseline Merged line times and commit times recorded | Pass | F1 and F3 lines and commit times all 02:25 (`base-M5.merge-times`) |
| base-M6-pytest I20 the 11 acceptance tests pass on main | Pass | I25: 13 passed, exit 0: the 11 acceptance tests and two extra tests (`base-M6-pytest.txt`, `tests/test_cli.py:52,56`) |
| base-M6 I20 status shows no active plan | Pass | No active plan; archived plan `2026-11-02-todo-cli` also named (`base-M6.jsonl`) |
| M2 manual flow matches v2.12.0 in the comparison | Pass | Paired comparison rows and their ref, worktree, main and report evidence |
| M3 manual flow matches v2.12.0 in the comparison | Pass | Paired comparison rows and their ref, worktree, main and report evidence |
| M4 manual flow matches v2.12.0 in the comparison | Pass | Paired comparison rows and their ref, worktree, main and report evidence |
| M5 manual flow matches v2.12.0 in the comparison | Pass | Paired comparison rows and their ref, worktree, main and report evidence |

The comparison counts commits added to `main` by each step. Worktrees listed are in addition to the main
checkout. M5 statuses come from the archived README if the tracking branch was removed. Hashes and wording
are recorded in the logs and are expected to vary across repositories.

| Step | Branches created | Worktrees left | Commits on main (merge / non-merge) | README statuses after the step | Report asked a merge question | Stop line | Task commits: out-of-scope paths and what happened | Task commits without a readable Wave-Model | Merged line times vs merge commits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cur-M2 | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F2-usage-readme | todo-cli-F1, todo-cli-F2, todo-cli-plan | 0 / 0 | W1 ✅, W2 ⬜, A ✅, B ⬜, C ✅, D ⬜, F1 🔄, F2 👀 review, F3 ⬜ | F2 | None | None | None | No merge |
| base-M2 | feat/todo-cli/F1-todo-store-and-cli, feat/todo-cli/F2-usage-readme | todo-cli-F1, todo-cli-F2, todo-cli-plan | 0 / 0 | W1 ✅, W2 ⬜, A ✅, B ⬜, C ✅, D ⬜, F1 🔄, F2 👀 review, F3 ⬜ | F2 | None | None | None | No merge |
| cur-M3 | None | todo-cli-F1, todo-cli-plan | 2 / 0 | W1 ✅, W2 ⬜, A ✅, B ⬜, C ✅, D ⬜, F1 🔄, F2 ✅ merged, F3 ⬜ | No | None | No task commits | No task commits | equal |
| base-M3 | None | todo-cli-F1, todo-cli-plan | 2 / 0 | W1 ✅, W2 ⬜, A ✅, B ⬜, C ✅, D ⬜, F1 🔄, F2 ✅ merged, F3 ⬜ | No | None | No task commits | No task commits | 22:15 vs 22:14 · intended (P25) |
| cur-M4 | feat/todo-cli/F3-ci-tests | todo-cli-F1, todo-cli-F3, todo-cli-plan | 0 / 0 | W1 ✅, W2 ✅, A ✅, B ✅, C ✅, D ✅, F1 👀 review, F2 ✅ merged, F3 👀 review | F1, F3 | None | None | None | No merge |
| base-M4 | feat/todo-cli/F3-ci-tests | todo-cli-F1, todo-cli-F3, todo-cli-plan | 0 / 0 | W1 ✅, W2 ✅, A ✅, B ✅, C ✅, D ✅, F1 👀 review, F2 ✅ merged, F3 👀 review | F1, F3 | None | None | D eb791ec · intended (P23) | No merge |
| cur-M5 | None | None | 3 / 0 | W1 ✅, W2 ✅, A ✅, B ✅, C ✅, D ✅, F1 ✅ merged, F2 ✅ merged, F3 ✅ merged | No | None | No task commits | No task commits | equal (F1 and F3 at 02:24) |
| base-M5 | None | None | 3 / 0 | W1 ✅, W2 ✅, A ✅, B ✅, C ✅, D ✅, F1 ✅ merged, F2 ✅ merged, F3 ✅ merged | No | None | No task commits | No task commits | equal (F1 and F3 at 02:25) |

## Not verified

- The watch checked the Python user site and `/c/tmp`. The run did not check other host paths or Claude Code's global application state.
- F3's GitHub Actions job was exercised locally against its feature tree. It was not dispatched on GitHub.
- The autonomous rehearsal was not repeated. The merge-time rule is shared with the autonomous flow.

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
git show main:plans/archive/2026-11-02-todo-cli/waves/w02.md | grep -E '^(- )?Merged ' | sed 's/^- //' \
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

**Resume after a usage stop.** In each shell resolve the preserved `<scratch>`, source its `env.sh` and export
`CLAUDE_ENV_FILE`, `scratch` and `working`. Compare both live ref and worktree lists to M4 and check both clean
main checkouts, installed skill trees, the original launcher and the absence of baseline M5 and `limit-stop/`.
After the state check passes, move the stopped files to `limit-stop/`, use a fresh stamp in the continuation
launcher and capture the source refs. Record M3 times, run current and baseline M5, capture the archive and M5
time evidence, run current and baseline M6 pytest, then current and baseline M6 status, and compare the source
refs. Check the accumulated cost before each Claude call and stop future calls on a usage match.
