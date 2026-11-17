# Rehearsal: multi-wave print-mode chain

2026-11-17 · Claude Code 2.1.326 · source checkout `bb08040`.

## Setup

- Created `<scratch>` with `mktemp -d` and initialized `<scratch>/repo` on `main` with no remote. The `init` commit added `todo.py` with `VERSION = "0.1.0"`, `add`, one-based `rm` and `list_items`, plus one unittest per function. All three tests passed.
- Ran `sh install.sh <scratch>/repo --no-codex` from the source worktree and committed the four project skills as `install wave skills`.
- Ran each command in Git Bash from `<scratch>/repo`, with stdin closed and separate stream and stderr logs. Used `MSYS_NO_PATHCONV=1 tasklist /FI "IMAGENAME eq claude.exe" /NH | grep -c claude.exe` before starting the background command and 120 seconds after waiting for it. Captured `git for-each-ref --format='%(refname) %(objectname)'` and `git worktree list --porcelain` at exit and after the wait. The post-exit check passed when both snapshots matched and the process count stayed at or below its initial value. Wall time covers command start to exit. Stream duration comes from the final event's `duration_ms`.

The five calls cost USD 2.187255865 in total. No stop line was emitted.

## Runs

### M1 · wave-triage

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-triage flow autonomous 1. add a storage module store.py with load(path) and save(path, items) that keep the items as JSON 2. add a command line to todo.py (python todo.py add TEXT, rm N, list) that loads and saves todo.json through store.py 3. add a --version option that prints VERSION 4. add a done N command that marks item N done 5. show done items in list with an [x] marker instead of hiding them 6. rename rm to delete and keep rm as an alias" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model opus --max-turns 150 --max-budget-usd 6 < /dev/null > "<scratch>/logs/M1.jsonl" 2> "<scratch>/logs/M1.err" &
wait $!
```

- Exit `0`, model `claude-opus-5-5`, `subtype: success`, `is_error: false`, `num_turns: 9`, `total_cost_usd: 0.4521856`. Permission denials: 0.
- Stream duration 1.118 min, wall time 1.167 min. The wall measurement was 2.928 s longer. Lines after `result`: 0.
- First result line `Started: 2026-11-17 22:21`. Stop line: none.
- Pass. `system/init` listed the four project wave skills and no `wave-method:` plugin skill.
- Post-exit pass. At exit and +120 s refs were identical and worktree lists were identical. The `claude.exe` count was 15 before launch and 15 at +120 s.
- Pass. No claim ref remained at exit.
- Pass. The result opened with `Started:` and ended with the `Started: … · Finished: …` times line. It ended without a question.
- Pass. The index reached `main` in merge `524719a`. `Flow: autonomous · target: integration/todo-cli` directly followed `Index:`. The assumptions used `Assumed (autonomous, not asked)` and `Open questions` was `none`.
- Part 1 held all six problems.

### M2 · wave-plan

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-plan flow autonomous plans/2026-11-17-todo-cli/index.md part 1" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model opus --max-turns 200 --max-budget-usd 10 < /dev/null > "<scratch>/logs/M2.jsonl" 2> "<scratch>/logs/M2.err" &
wait $!
```

- Exit `0`, model `claude-opus-5-5`, `subtype: success`, `is_error: false`, `num_turns: 15`, `total_cost_usd: 1.0327658`. Permission denials: 0.
- Stream duration 3.024 min, wall time 3.067 min. The wall measurement was 2.568 s longer. Lines after `result`: 0.
- First result line `Started: 2026-11-17 22:25`. Stop line: none.
- Pass. `system/init` listed the four project wave skills and no `wave-method:` plugin skill.
- Post-exit pass. At exit and +120 s refs were identical and worktree lists were identical. The `claude.exe` count was 15 before launch and 15 at +120 s.
- Pass. No claim ref remained at exit.
- Pass. The result opened with `Started:` and ended with the `Started: … · Finished: …` times line. It ended without a question.
- Pass. `main` remained at `524719a`. `git cat-file -e` found the README on `integration/todo-cli` at `393944d`. The README declared autonomous flow and the intended integration target.
- Pass. `plan/todo-cli-p1` existed at `1d4b6ea`. The source worktree's `status_check.py` returned `0` for the plan in its tracking worktree.
- Finding. The plan had one wave, one feature and two tasks. Its largest launch group with `After` set to `—` had one task. See Findings.

### M3 · wave-run

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-17-todo-cli/plan-1" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model sonnet --max-turns 400 --max-budget-usd 8 < /dev/null > "<scratch>/logs/M3.jsonl" 2> "<scratch>/logs/M3.err" &
wait $!
```

- Exit `0`, model `claude-sonnet-5-5`, `subtype: success`, `is_error: false`, `num_turns: 22`, `total_cost_usd: 0.674513175`. Permission denials: 0.
- Stream duration 2.444 min, wall time 2.483 min. The wall measurement was 2.374 s longer. Lines after `result`: 0.
- First result line `Started: 2026-11-17 22:30`. Stop line: none.
- Pass. `system/init` listed the four project wave skills and no `wave-method:` plugin skill.
- Post-exit pass. At exit and +120 s refs were identical and worktree lists were identical. The `claude.exe` count was 15 before launch and 15 at +120 s.
- Pass. No claim ref remained at exit.
- Pass. The result opened with `Started:` and ended with the `Started: … · Finished: …` times line. It ended without a question.
- Pass. Wave 1 was ✅ on `plan/todo-cli-p1` at `cf162f6`. F1 was ✅ merged, and its merge commit `f7ef991` was an ancestor of the exit tip `ebc26c5` on `integration/todo-cli`.
- Pass. `main` remained at `524719a`. An independent `python -m unittest` on the integration worktree passed all 16 tests.
- Pass. Both Agent results arrived before `result` and the corresponding commits were reachable from the exit tip of the feature branch. See Subagents.
- Finding. The two Agent calls launched in separate messages with `run_in_background: false`. There was no pending wave at exit, so calls M4–M8 were unused.

### M9 · wave-status

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model haiku --max-turns 60 --max-budget-usd 0.5 < /dev/null > "<scratch>/logs/M9.jsonl" 2> "<scratch>/logs/M9.err" &
wait $!
```

- Exit `0`, model `claude-haiku-5-5`, `subtype: success`, `is_error: false`, `num_turns: 6`, `total_cost_usd: 0.01507618`. Permission denials: 0.
- Stream duration 0.688 min, wall time 0.717 min. The wall measurement was 1.702 s longer. Lines after `result`: 0.
- First result line ``## plans/2026-11-17-todo-cli/plan-1 · `todo-cli-p1` · autonomous · target: integration/todo-cli``. Stop line: none.
- Pass. `system/init` listed the four project wave skills and no `wave-method:` plugin skill.
- Post-exit pass. At exit and +120 s refs were identical and worktree lists were identical. The `claude.exe` count was 15 before launch and 15 at +120 s.
- Pass. No claim ref remained at exit.
- Finding. The result ended with the `Started: … · Finished: …` times line and no closing question. The first line was the plan header, so the inherited check for an opening `Started:` line failed.
- Pass. The report included the plan header, Tracking branch, Features, the feature table, Waves and Next. The exact `Merged, not in main:` label appeared once, with the complete F1 block beneath it, including the integration merge, what changed, how to test and `Approved:`.
- Pass. Refs and worktrees matched the M3 post-exit snapshot.

### M10 · wave-status

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status plans/2026-11-17-todo-cli/plan-1" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model haiku --max-turns 60 --max-budget-usd 0.5 < /dev/null > "<scratch>/logs/M10.jsonl" 2> "<scratch>/logs/M10.err" &
wait $!
```

- Exit `0`, model `claude-haiku-5-5`, `subtype: success`, `is_error: false`, `num_turns: 6`, `total_cost_usd: 0.01271511`. Permission denials: 0.
- Stream duration 0.396 min, wall time 0.450 min. The wall measurement was 3.228 s longer. Lines after `result`: 0.
- First result line ``## plans/2026-11-17-todo-cli/plan-1 · `todo-cli-p1` · autonomous · target: integration/todo-cli``. Stop line: none.
- Pass. `system/init` listed the four project wave skills and no `wave-method:` plugin skill.
- Post-exit pass. At exit and +120 s refs were identical and worktree lists were identical. The `claude.exe` count was 15 before launch and 15 at +120 s.
- Pass. No claim ref remained at exit.
- Finding. The result ended with the `Started: … · Finished: …` times line and no closing question. The first line was the plan header, so the inherited check for an opening `Started:` line failed.
- Pass. The report included the plan header, Tracking branch, Features, the feature table, Waves and Next.
- Finding. The full F1 block appeared under `Merged, not in master:`. A separate correction used `Merged, not in main:` and referred back to the block. The exact label and its block failed the format check.
- Pass. Refs and worktrees matched the M9 post-exit snapshot.

## Subagents

| Run | Wave | Task | Requested model | `run_in_background` | Shared assistant message with another Agent call | Final output before `result` | Commit in feature branch at exit |
|---|---:|---|---|---|---|---|---|
| M3 | 1 | A | `haiku` | false | no | yes | yes, `db527a4` |
| M3 | 1 | B | `sonnet` | false | no | yes | yes, `e9d00b1` |

Matched each final tool result by the Agent call ID. A's final result preceded the launch of B. Both commits were ancestors of the F1 ref recorded at process exit.

## Findings

- M2, skill planning outcome, **multi-wave not reached**. Expected several waves because five requests touched the CLI in `todo.py`. The planner combined those requests into task B and scheduled it after the separate storage task A within the same wave. The run therefore covered one wave.
- M3, skill execution coverage, **no parallel launch**. Expected a launch group of at least two tasks. Both calls used separate launch groups with `run_in_background: false`. The run measured foreground completion. I10 remains open for a chain with several waves, a parallel launch group and background subagents.
- M9 and M10, report format. The shared check carried over from the first chain expected an opening `Started:` line. Both results opened with the plan header specified by the new `wave-status` template and printed the times line at the end.
- M10, skill output defect. Expected one `Merged, not in main:` heading immediately followed by the full F1 block. The main report used `Merged, not in master:` and commands with `master...`. The reply then added a corrective `Merged, not in main:` heading with a reference to the block above and repeated the Integration and Next lines with `main...`. The scratch repository's branch was `main`. The CLI delivered the resulting text successfully and the heading issue remains open.

## Caps

Maxima use the completed R-series calls in [the first chain](print-mode-chain.md) and the five M-series calls above. The derived caps triple each maximum, rounding turns up to a multiple of ten and costs up to a whole dollar. Wave-run values are per call.

| Skill | Largest turns | Largest cost (USD) | Rounded 3× turns | Rounded 3× cost (USD) |
|---|---:|---:|---:|---:|
| wave-triage | 9 (M1) | 0.4521856 (M1) | 30 | 2 |
| wave-plan | 16 (R2) | 1.0327658 (M2) | 50 | 4 |
| wave-run | 22 (M3) | 0.674513175 (M3) | 70 | 3 |
| wave-status | 6 (R6, M9, M10) | 0.01507618 (M9) | 20 | 1 |

Each call's observed turns and cost fit the previous driver caps. The triage, plan and run calls used the larger rehearsal limits recorded above. These measurements cover the two single-wave plans tested. The status driver allowance of 60 turns and USD 0.50 covers three times the observed unrounded maximum.
