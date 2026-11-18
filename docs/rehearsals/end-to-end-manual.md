# Rehearsal: manual flow end to end

2026-11-18 · Claude Code 2.1.326 · source `47e212d` · baseline `v2.12.0`.

## Setup

Git Bash created the scratch folder first. Claude Code reported 2.1.326. The shared scratch venv installed pytest 9.2.0 and PyYAML 6.0.3.

~~~bash
scratch=$(mktemp -d)
ws=$(cygpath -m "$scratch" 2>/dev/null || printf '%s' "$scratch")
mkdir -p "$scratch/logs" "$scratch/tmp" "$scratch/userbase" "$scratch/pip-cache" "$scratch/launch"
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

Every fresh step shell sourced the same env file and exported `CLAUDE_ENV_FILE`. The M-step launchers also inherited PYTHONDONTWRITEBYTECODE=1 on both sides. The scratch repositories, their worktrees, the tag archive, venv, temp directory, userbase and pip cache were created directly under <scratch>. The step and inspection launchers were created in <scratch>/launch. Setup output, notes, exit codes, usage checks, snapshots, reports and other evidence were created in <scratch>/logs. The only file written in the working folder was this record.

The early supplemental source checks used the host's default temporary directory under `<home>` for their transient test fixtures. The final source check rerun used `<scratch>/tmp` for `TMPDIR`, `TMP` and `TEMP`. The preliminary test output and the final check logs were both written directly to `<scratch>/logs`.

Before and after each step the launcher captured refs, worktrees and main in <tag>.<before|after>.refs, <tag>.<before|after>.worktrees and <tag>.<before|after>.main using git for-each-ref, git worktree list --porcelain and git rev-parse main. The <tag>.<before|after>.readme files came from the tracking branch. M3 and M5 were user approvals, and their first-parent records came from git log --merges --first-parent and git rev-list --no-merges --first-parent <before>..main. After each Claude call the usage test ran before the after-snapshots. Every executed step then ran the watch.

~~~bash
grep -l -i -E 'hit your .*limit|usage limit' "$scratch/logs/$tag.jsonl" "$scratch/logs/$tag.err"
{ find "$usersite" -maxdepth 1 -newer "$scratch/logs/start.stamp" 2>/dev/null
  [ -d /c/tmp ] && find /c/tmp -maxdepth 1 -newer "$scratch/logs/start.stamp"; } > "$scratch/logs/$tag.outside"
~~~

After M2 and M4, each repository produced its task commit evidence with these commands.

~~~bash
git -C "$scratch/$repo" log --all --no-merges --grep="^todo-cli F[0-9]* / [A-Z]*:" \
  --format="%h %s | %(trailers:key=Wave-Model,valueonly,separator=%x2C)" > "$scratch/logs/$tag.trailers"
git -C "$scratch/$repo" log --all --no-merges --grep="^todo-cli F[0-9]* / [A-Z]*:" --name-only \
  --format="== %h %s" > "$scratch/logs/$tag.paths"
~~~

## Runs

### P0

~~~bash
cd "$scratch/cur"
probe='Run this one command with the Bash tool: command -v python; python -c "import sys, tempfile; print(sys.prefix); print(tempfile.gettempdir())"; echo "pathconv=${MSYS_NO_PATHCONV-unset}". Then launch one subagent and have it run the same command with its Bash tool. Reply with both outputs verbatim.'
MSYS_NO_PATHCONV=1 timeout 600 claude -p "$probe" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 8 --max-budget-usd 0.3 < /dev/null > "$scratch/logs/P0.jsonl" 2> "$scratch/logs/P0.err"; \
  echo $? > "$scratch/logs/P0.exit"
~~~

- Exit 0, wall 0.15 min, `P0.outside` empty. Usage test exit 1, no match.
- Last result: `claude-haiku-5-5`, 1 turns, $0.00634888. First line: `The subagent finished and its output matches mine:`. Last line: ```` ``` ````. No stop line.
- Pass. The coordinator and subagent Bash `tool_result` events show `<scratch>/venv/Scripts/python`, prefix `<scratch>/venv`, temp `<scratch>/tmp` and `pathconv=unset`.

### cur-M0

~~~bash
cd "$scratch/cur"
python "$working/skills/wave-plan/scripts/status_check.py" plans/2026-11-02-todo-cli > "$scratch/logs/cur-M0.out" 2> "$scratch/logs/cur-M0.err"; \
  echo $? > "$scratch/logs/cur-M0.exit"
~~~

- Exit 0, wall 0.00 min, `cur-M0.outside` empty. Usage test does not apply to Python steps.
- Pass. `cur-M0.out` and `cur-M0.err` were empty.

### base-M0

~~~bash
cd "$scratch/base"
python "$working/skills/wave-plan/scripts/status_check.py" plans/2026-11-02-todo-cli > "$scratch/logs/base-M0.out" 2> "$scratch/logs/base-M0.err"; \
  echo $? > "$scratch/logs/base-M0.exit"
~~~

- Exit 0, wall 0.00 min, `base-M0.outside` empty. Usage test does not apply to Python steps.
- Pass. `base-M0.out` and `base-M0.err` were empty.

### cur-M1

~~~bash
cd "$scratch/cur"
python "$working/scripts/wave_driver.py" plans/2026-11-02-todo-cli --repo . --dry-run > "$scratch/logs/cur-M1.out" 2> "$scratch/logs/cur-M1.err"; \
  echo $? > "$scratch/logs/cur-M1.exit"
~~~

- Exit 0, wall 0.00 min, `cur-M1.outside` empty. Usage test does not apply to Python steps.
- Pass. `cur-M1.out` contained the single line `next: nothing — plans/2026-11-02-todo-cli: manual flow: the driver runs autonomous plans only`. `cur-M1.driver-dir` recorded that `<scratch>/cur.wave-driver` was absent.

### cur-M2

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 1" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/cur-M2.jsonl" 2> "$scratch/logs/cur-M2.err"; \
  echo $? > "$scratch/logs/cur-M2.exit"
~~~

- Exit 0, wall 1.73 min, `cur-M2.outside` empty. Usage test exit 1, no match.
- Last result: `claude-sonnet-5-5`, 9 turns, $0.537097135. First line: `Started: 2026-11-18 20:53`. Last line: `Started: 2026-11-18 20:53 · Finished: 2026-11-18 20:54 (1 min)`. No stop line. Penultimate non-empty line: `Merge F2 "README with install and usage" — adds the user README (feat/todo-cli/F2-usage-readme) into main? Answer: merge F2 · later · problems F2: <what is wrong>`.
- Pass. Wave 1 and tasks A and C completed, F1 waited for wave 2, and F2 entered review with a merge question. The report showed `Flow: manual`.
- Pass. `main` stayed at `d619577`. No integration branch or claim ref appeared and the tracking README had no `Flow:` line.
- Pass. Task A `d146338` recorded `claude-sonnet-5-5` and task C `1a87ba3` recorded `claude-haiku-5-5`. Their changed files matched the task scopes.

### base-M2

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 1" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/base-M2.jsonl" 2> "$scratch/logs/base-M2.err"; \
  echo $? > "$scratch/logs/base-M2.exit"
~~~

- Exit 0, wall 1.52 min, `base-M2.outside` empty. Usage test exit 1, no match.
- Last result: `claude-sonnet-5-5`, 7 turns, $0.41255662. First line: `Started: 2026-11-18 20:55`. Last line: `Started: 2026-11-18 20:55 · Finished: 2026-11-18 20:56 (1 min)`. No stop line. Penultimate non-empty line: `Merge F2 "README with install and usage" — adds a README with install steps and an example session (feat/todo-cli/F2-usage-readme) into main? Answer: merge F2 · later · problems F2: <what is wrong>`.
- Pass. Wave 1 and tasks A and C completed, F1 waited for wave 2, and F2 entered review with a merge question.
- Pass. `main` stayed at `7903881`. No integration branch or claim ref appeared and the tracking README had no `Flow:` line.
- Baseline evidence. Task A `8aa3ed0` recorded `claude-sonnet-5-5` and task C `7c9bc9b` recorded `claude-haiku-5-5`. Their changed files matched the task scopes.

### cur-M3

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/cur-M3.jsonl" 2> "$scratch/logs/cur-M3.err"; \
  echo $? > "$scratch/logs/cur-M3.exit"
~~~

- Exit 0, wall 0.62 min, `cur-M3.outside` empty. Usage test exit 1, no match.
- Last result: `claude-sonnet-5-5`, 11 turns, $0.2862987. First line: `Started: 2026-11-18 20:57`. Last line: `Started: 2026-11-18 20:57 · Finished: 2026-11-18 20:57 (under 1 min)`. No stop line.
- Pass. Main advanced from d619577 to 1d4c550. The F2 merge was b16f4d0 and the tracking status merge was 1d4c550. There were no first-parent non-merges. The tracking README records F2 as merged at b16f4d0.

### base-M3

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/base-M3.jsonl" 2> "$scratch/logs/base-M3.err"; \
  echo $? > "$scratch/logs/base-M3.exit"
~~~

- Exit 0, wall 0.53 min, `base-M3.outside` empty. Usage test exit 1, no match.
- Last result: `claude-sonnet-5-5`, 10 turns, $0.2149266. First line: `## Merge · todo-cli`. Last line: `Started: 2026-11-18 20:58 · Finished: 2026-11-18 20:58 (under 1 min)`. No stop line.
- Pass. Main advanced from 7903881 to 671ea48. The F2 merge was 8cddee5 and the tracking status merge was 671ea48. There were no first-parent non-merges. The tracking README records F2 as merged at 8cddee5.

### cur-M4

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/cur-M4.jsonl" 2> "$scratch/logs/cur-M4.err"; \
  echo $? > "$scratch/logs/cur-M4.exit"
~~~

- Exit 0, wall 1.75 min, `cur-M4.outside` empty. Usage test exit 1, no match.
- Last result: `claude-sonnet-5-5`, 8 turns, $0.527655285. First line: `Started: 2026-11-18 20:59`. Last line: `Started: 2026-11-18 20:59 · Finished: 2026-11-18 21:00 (1 min)`. No stop line. Penultimate non-empty line: ``Merge F1 "Tasks stored in `todo.json`, commands `add`, `list`, `done`" — adds the `todo` command with `add`, `list` and `done` (feat/todo-cli/F1-todo-store-and-cli) into main? Answer: merge F1 · later · problems F1: <what is wrong>``.
- Finding. Expected wave 2 and B/D complete, F1 and F3 in review and a question about both approvals. B completed and F1 entered review. The report asked only about F1 and marked wave 2, D and F3 with I1. Task D's workflow at fc205c8 requires an editable install, and that branch has no pyproject.toml. The coordinator's entry is in cur-M4.problems (tracking commit 50ed7ad).
- Pass. Main stayed at 1d4c550. All four task commits had readable model trailers and only their declared files. The P4 YAML and version check passed and the F1 worktree's pytest run reported 11 passed.

### base-M4

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "$scratch/logs/base-M4.jsonl" 2> "$scratch/logs/base-M4.err"; \
  echo $? > "$scratch/logs/base-M4.exit"
~~~

- Exit 0, wall 1.40 min, `base-M4.outside` empty. Usage test exit 1, no match.
- Last result: `claude-sonnet-5-5`, 7 turns, $0.403701265. First line: `Started: 2026-11-18 21:01`. Last line: `Started: 2026-11-18 21:01 · Finished: 2026-11-18 21:02 (1 min)`. No stop line. Penultimate non-empty line: ``Merge F3 "Tests run on every push" — adds the GitHub Actions workflow that runs `pytest` on Python 3.10 and 3.12 (feat/todo-cli/F3-ci-tests) into main? Answer: merge F3 · later · problems F3: <what is wrong>``. Immediately preceding F1 question: ``Merge F1 "Tasks stored in `todo.json`, commands `add`, `list`, `done`" — adds the `todo` command with `add`, `list` and `done` (feat/todo-cli/F1-todo-store-and-cli) into main? Answer: merge F1 · later · problems F1: <what is wrong>``.
- Pass. Wave 2 and B/D completed, both F1 and F3 entered review and main stayed at 671ea48. The review brief acknowledged that the editable CI install needs F1's pyproject.toml.
- Finding. Expected the penultimate non-empty line to ask about both merges. The report put the F1 and F3 questions on consecutive lines, with F3 immediately before the footer. Runs quotes both questions from the same last result.
- Baseline evidence. Four task commits carried readable models and changed only their declared paths. The P4 YAML and version check passed and the F1 worktree's pytest run reported 11 passed.

### cur-M5

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/cur-M5.jsonl" 2> "$scratch/logs/cur-M5.err"; \
  echo $? > "$scratch/logs/cur-M5.exit"
~~~

- Exit 0, wall 0.28 min, `cur-M5.outside` empty. Usage test exit 1, no match.
- Last result: `claude-sonnet-5-5`, 6 turns, $0.2185975. First line: `Started: 2026-11-18 21:03`. Last line: `Started: 2026-11-18 21:03 · Finished: 2026-11-18 21:03 (under 1 min)`. Stop line: `` Stop not-ready: F3 is ⚠️ blocked (I1), not 👀 review, so nothing was merged, F1 included — next: `/wave-run plans/2026-11-02-todo-cli merge F1` · `$wave-run plans/2026-11-02-todo-cli merge F1` ``.
- Finding. Expected the approval to merge F1 and F3 and archive the plan. The command stopped at not-ready because F3 was blocked by I1. Neither feature merged. Main stayed at 1d4c550 and both first-parent lists were empty. F1 stayed in review and the plan remained active.

### base-M5

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null > "$scratch/logs/base-M5.jsonl" 2> "$scratch/logs/base-M5.err"; \
  echo $? > "$scratch/logs/base-M5.exit"
~~~

- Exit 0, wall 0.85 min, `base-M5.outside` empty. Usage test exit 1, no match.
- Last result: `claude-sonnet-5-5`, 18 turns, $0.28554029999999997. First line: `Started: 2026-11-18 21:05`. Last line: `Started: 2026-11-18 21:05 · Finished: 2026-11-18 21:05 (0 min)`. No stop line.
- Pass. Main advanced from 671ea48 to 35a75d8 through F1 1ca1b3e, F3 b04b69b and the tracking status merge. The first-parent non-merge list was empty. Base-M5 archived the plan and left just the main checkout.
- Finding. The archived wave 2 merge lines record 21:08 while both merge commits show 21:05. The run also reports the discrepancy. See base-M5.archive-wave2, lines 60-61, and base-M5.merge-times.

### cur-M6-pytest

~~~bash
cd "$scratch/cur"
python -m pytest -q > "$scratch/logs/cur-M6-pytest.out" 2> "$scratch/logs/cur-M6-pytest.err"; \
  echo $? > "$scratch/logs/cur-M6-pytest.exit"
~~~

- Exit 5, wall 0.02 min, `cur-M6-pytest.outside` empty. Usage test does not apply to Python steps.
- Finding. Expected 11 passing tests on main. Pytest collected no tests because cur-M5 left F1 unmerged. The same suite passed in the F1 worktree during cur-M4.

### base-M6-pytest

~~~bash
cd "$scratch/base"
python -m pytest -q > "$scratch/logs/base-M6-pytest.out" 2> "$scratch/logs/base-M6-pytest.err"; \
  echo $? > "$scratch/logs/base-M6-pytest.exit"
~~~

- Exit 0, wall 0.00 min, `base-M6-pytest.outside` empty. Usage test does not apply to Python steps.
- Pass. Pytest reported 11 passed on main.

### cur-M6

~~~bash
cd "$scratch/cur"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$scratch/logs/cur-M6.jsonl" 2> "$scratch/logs/cur-M6.err"; \
  echo $? > "$scratch/logs/cur-M6.exit"
~~~

- Exit 0, wall 0.55 min, `cur-M6.outside` empty. Usage test exit 1, no match.
- Last result: `claude-haiku-5-5`, 7 turns, $0.0129501. First line: `Started: 2026-11-18 21:06`. Last line: `Started: 2026-11-18 21:06 · Finished: 2026-11-18 21:06 (under 1 min)`. No stop line.
- Finding. Expected a finished or archived plan. The status still lists the active todo-cli plan with F1 in review, F2 merged and F3 blocked by I1.

### base-M6

~~~bash
cd "$scratch/base"
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "$scratch/logs/base-M6.jsonl" 2> "$scratch/logs/base-M6.err"; \
  echo $? > "$scratch/logs/base-M6.exit"
~~~

- Exit 0, wall 0.23 min, `base-M6.outside` empty. Usage test exit 1, no match.
- Last result: `claude-haiku-5-5`, 5 turns, $0.00546584. First line: `Started: 2026-11-18 21:07`. Last line: `Started: 2026-11-18 21:07 · Finished: 2026-11-18 21:07 (under 1 min)`. No stop line.
- Pass. The status reports no active plans and names the archived todo-cli plan.

The sum of the last reported costs was $2.91113822499999997. The launch threshold was $20.

## Results

| Expectation | Result | Evidence |
|---|---|---|
| Scratch-first setup and one foreground command per step in interleaved order | Pass | Both copies of the current example are under `<scratch>`. `cur` uses `47e212d`. `base` uses the `v2.12.0` archive. The commands, `.exit` files and `.elapsed` files cover the order in Runs. |
| P0 isolates the coordinator and subagent Bash environments | Pass | Both Bash `tool_result` events in `P0.jsonl` resolve Python, prefix and temp under `<scratch>` and report `pathconv=unset`. |
| M0 exits 0 without output in both repositories | Pass | `cur-M0.exit` and `base-M0.exit` are 0. Both stdout and stderr pairs are empty. |
| cur-M1 declines the manual plan without producing a driver directory | Pass | Exit 0 and the expected one-line explanation in `cur-M1.out`. `cur-M1.driver-dir` says `absent`. |
| M2 opens with `Started:`, completes wave 1 and A/C, and gives F1 the wave 2 wait and F2 a review block | Pass | `cur-M2.jsonl`, `base-M2.jsonl` and the tracking READMEs. The current report also shows `Flow: manual`. |
| M2 asks to merge F2 immediately before the run-time footer | Pass | Both lines from each report are quoted in Runs. |
| M2 leaves `main` fixed and does not create integration or claim refs or a `Flow:` line | Pass | `.before.main`, `.after.main`, `.after.refs` and `.after.readme` for both M2 steps. |
| M2 task scope and readable models in current | Pass | `cur-M2.paths` and `.trailers` show only declared paths and readable models for A `d146338` and C `1a87ba3`. The baseline evidence is in `base-M2.paths` and `.trailers`. |
| M3 applies user approval for F2 and records the merge-only increment on `main` | Pass | Current `d619577` to `1d4c550` via F2 `b16f4d0`. Baseline `7903881` to `671ea48` via F2 `8cddee5`. Both `.main-non-merges` files are empty. |
| M3 tracks F2 as merged at the feature merge hash | Pass | Both `.after.readme` files have F2 ✅ merged with the matching hash. |
| M4 completes wave 2 and B/D and puts F1 and F3 in review | Finding | In `cur-M4.jsonl` and `cur-M4.after.readme`, B completed and F1 entered review. Wave 2, D and F3 carried I1. `base-M4.jsonl` and `base-M4.after.readme` show wave 2 and both tasks complete and both features in review. |
| M4 asks about F1 and F3 on the penultimate non-empty line and ends with the run-time footer | Finding | Both reports end with the timing footer. Current asks only about F1. Baseline asks about F1 and F3 on consecutive lines and ends the question block with F3. Runs quotes the lines from both logs. |
| M4 leaves `main` fixed | Pass | `.before.main` and `.after.main` match at `1d4c550` for `cur` and `671ea48` for `base`. |
| M4 current tasks have readable model trailers and remain within scope | Pass | `cur-M4.trailers` reports Sonnet for A `d146338` and B `00cda05`, Haiku for C `1a87ba3` and D `fc205c8`. `cur-M4.paths` lists only declared files. Both baseline files are retained and show the same scope and trailer outcomes. |
| cur-M5 merges F1 and F3 on first-parent `main` under the user approval | Finding | `cur-M5.jsonl` gives `Stop not-ready` for F3 (I1). `main` stayed at `1d4c550` and both first-parent lists are empty. |
| cur-M5 leaves all features merged and archives the plan | Finding | `cur-M5.after.readme` keeps F1 in review and F3 blocked. `cur-M5.main-plans` still has the active plan folder. |
| base-M5 merges F1 and F3 as first-parent merges only under the user approval | Pass | `main` advanced from `671ea48` to `35a75d8` via F1 `1ca1b3e`, F3 `b04b69b` and the tracking status merge. `base-M5.main-non-merges` is empty. |
| base-M5 leaves all features merged and archives the plan | Pass | `base-M5.archive` is the final README at `main:plans/archive/2026-11-02-todo-cli/README.md` and shows all features merged. `base-M5.after.worktrees` lists only the main checkout. |
| base-M5 archive records the actual merge time | Finding | The two archived wave log entries say `21:08` in `base-M5.archive-wave2`, lines 60–61. Both merge commits are at `21:05` in `base-M5.merge-times`. The last result reports the discrepancy. |
| No merge into `main` outside the authorized steps | Pass | Every other step has matching `.before.main` and `.after.main`. |
| cur-M6-pytest passes all 11 P1/P2 tests on `main` | Finding | `cur-M6-pytest.out` says `no tests ran` and `.exit` is 5. `cur-M5` never merged the test files from F1. The `cur-M4` F1 worktree run passed all 11 tests. |
| base-M6-pytest passes all 11 P1/P2 tests on `main` | Pass | `base-M6-pytest.out` says `11 passed` and `.exit` is 0. |
| cur-M6 status shows no plan in progress | Finding | `cur-M6.jsonl` lists `todo-cli` as active, with F1 in review, F2 merged, and F3 blocked by I1. |
| base-M6 status shows no plan in progress | Pass | `base-M6.jsonl` says `No active plans.` and names the archived plan. |
| M2 and M3 manual flow parity | Pass | All comparison cells agree. The current report includes `Flow: manual`. |
| M4 manual flow parity | Finding | The README statuses differ. Both F3 worktrees used the same dependency on F1 for the editable install. Current opened I1 while baseline kept it as a review caveat. |
| M5 manual flow parity | Finding | Current returned `Stop not-ready` and kept the review and tracking worktrees. Baseline made three merges, archived the plan and removed those worktrees. |
| Watch after every executed step | Pass | All 16 `.outside` files are empty. |
| Usage test and cost limit | Pass | All 11 `.usage.exit` files are 1. The sum reported in Runs stayed below the $20 launch limit. |
| All transient run and verification files in scratch | Finding | The early source suite ran with the host's temporary directory for its temporary test fixtures. The final scoped rerun used `<scratch>/tmp`. Launchers, retained evidence, snapshots and scratch repositories were created directly in scratch. |
| Source refs and objects match before and after the chain | Pass | `working-before.refs` and `working-after.refs` each contain 60 identical ref/object pairs. `diff -u` exited 0. The task branch pointed to `47e212d` in both snapshots, before the record commit. |
| Source wave checks | Pass | `final-check-status.txt`: 33 tests. `final-check-driver.txt`: 59 tests. All three example status checks exited 0. `git diff --check` exited 0. |

### Manual flow comparison

F1, F2 and F3 refer to `feat/todo-cli/F1-todo-store-and-cli`, `feat/todo-cli/F2-usage-readme`
and `feat/todo-cli/F3-ci-tests`. The worktree list omits the main checkout, which was present
throughout. Commit counts are first-parent only. The base-M5 statuses come from its archive.


| Step | Repository | Branches created | Worktrees left | Commits on main (merge / non-merge) | README statuses | Report asked a question | Stop line | Task commits: out-of-scope paths and what happened | Task commits without a readable Wave-Model |
|---|---|---|---|---|---|---|---|---|---|
| M2 | cur | F1, F2 | F1, F2, plan/todo-cli | 0 / 0 | F1 🔄, F2 👀 review, F3 ⬜, A ✅, B ⬜, C ✅, D ⬜, 1 ✅, 2 ⬜ | Yes | None | None | None |
| M2 | base | F1, F2 | F1, F2, plan/todo-cli | 0 / 0 | F1 🔄, F2 👀 review, F3 ⬜, A ✅, B ⬜, C ✅, D ⬜, 1 ✅, 2 ⬜ | Yes | None | None | None |
| M3 | cur | None | F1, plan/todo-cli | 2 / 0 | F1 🔄, F2 ✅ merged, F3 ⬜, A ✅, B ⬜, C ✅, D ⬜, 1 ✅, 2 ⬜ | No | None | No task run | No task run |
| M3 | base | None | F1, plan/todo-cli | 2 / 0 | F1 🔄, F2 ✅ merged, F3 ⬜, A ✅, B ⬜, C ✅, D ⬜, 1 ✅, 2 ⬜ | No | None | No task run | No task run |
| M4 | cur | F3 | F1, F3, plan/todo-cli | 0 / 0 | F1 👀 review, F2 ✅ merged, F3 ⚠️ blocked I1, A ✅, B ✅, C ✅, D ⚠️ I1, 1 ✅, 2 ⚠️ I1 | Yes | None | None | None |
| M4 | base | F3 | F1, F3, plan/todo-cli | 0 / 0 | F1 👀 review, F2 ✅ merged, F3 👀 review, A ✅, B ✅, C ✅, D ✅, 1 ✅, 2 ✅ | Yes | None | None | None |
| M5 | cur | None | F1, F3, plan/todo-cli | 0 / 0 | F1 👀 review, F2 ✅ merged, F3 ⚠️ blocked I1, A ✅, B ✅, C ✅, D ⚠️ I1, 1 ✅, 2 ⚠️ I1 | No | Stop not-ready | No task run | No task run |
| M5 | base | None | None | 3 / 0 | F1 ✅ merged, F2 ✅ merged, F3 ✅ merged, A ✅, B ✅, C ✅, D ✅, 1 ✅, 2 ✅ | No | None | No task run | No task run |

Manual flow differed from v2.12.0 at M4 and M5. The current runner recorded the missing
packaging metadata as a blocking issue while the baseline flagged the same dependency in its
review brief. The run shows how each report handled the dependency. It did not run CI on
GitHub or isolate a runner change that caused the difference.

## Not verified

The watch covered the Python user site and /c/tmp. Other host locations were outside its
coverage. All planned commands ran. The current repository did not reach a post-merge test or
archived state because M5 refused the combined approval. Neither scratch repository was pushed
to GitHub, so CI checks were limited to YAML and version validation.

## Repeat

1. In Git Bash from the working folder, run Setup to create an empty scratch folder, set up the
   venv, seed the repositories and take the source ref snapshot.
2. Run P0 in cur and judge both Bash tool results, then check its watch.
3. Run the remaining commands in Runs in order, one at a time. Check usage, capture snapshots
   and run the watch before proceeding. Stop at the first non-empty watch. Stop Claude calls
   after a usage match or before the next call once reported cost reaches $20. Run the remaining
   non-Claude checks when their inputs exist.
4. Read the task commit audits after M2 and M4. Compare the source refs against a fresh
   working-after.refs snapshot taken after the last call and before committing the record.
