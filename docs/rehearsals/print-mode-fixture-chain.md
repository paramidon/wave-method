# Rehearsal: fixture-plan print-mode chain

2026-11-17 · Claude Code 2.1.326 · source checkout `0e3cb44`.

## Setup

- Created `<scratch>` with `mktemp -d`. Ran `git init -b master` in `<scratch>/repo` and committed one line, `MIT`, in `LICENSE` as `init`.
- Created `<scratch>/venv` with `python -m venv`. Ran `<scratch>/venv/Scripts/python -m pip install pytest pyyaml` and installed pytest 9.2.0 and PyYAML 6.0.3. Prepended `<scratch>/venv/Scripts` to `PATH` for every call.
- Ran `sh install.sh <scratch>/repo --no-codex` from the source worktree and committed the four project skills as `install wave skills`. Copied `examples/01-greenfield-todo-cli/` unchanged to `plans/2026-11-02-todo-cli/` and committed it as `add fixture plan` on `master` at `3a1bcae`. The source `status_check.py` exited 0 on the plan. The fixture gives wave 1 tasks A and C and wave 2 tasks B and D, with two features per wave and both tasks' `After` fields set to `—`.
- Ran each command in Git Bash from `<scratch>/repo`, with stdin closed and stdout and stderr logged separately. Counted processes using `MSYS_NO_PATHCONV=1 tasklist /FI "IMAGENAME eq claude.exe" /NH | grep -c claude.exe` before the call and 120 seconds after `wait`. Captured `git for-each-ref --format='%(refname) %(objectname)'` and `git worktree list --porcelain` at exit and again after 120 seconds. The check passed when both snapshots matched and the process count stayed at or below its starting value. Wall minutes cover start to exit. Stream minutes use `duration_ms`.

The sum of all reported cost fields was USD 3.350261010 against the USD 30 chain cap. Counting just the last result per call gives USD 1.772189025.

## Runs

### C1 · wave-run

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli flow autonomous" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 2 < /dev/null > "<scratch>/logs/C1.jsonl" 2> "<scratch>/logs/C1.err" &
wait $!
```

- Exit `0`, model `claude-sonnet-5-5`. Wall time 0.283 min.
- Result 1. `subtype: success`, `is_error: false`, `num_turns: 7`, `total_cost_usd: 0.2366536`. Stream duration 0.230 min. Permission denials 0. Lines after `result` 0.
  First line `Started: 2026-11-17 23:10`. Last line `Started: 2026-11-17 23:10 · Finished: 2026-11-17 23:10 (under 1 min)`.
- Stop line none.
- Pass. One `system/init` event listed the four project wave skills and no plugin wave skills.
- Post-exit pass. Refs matched, worktree lists matched, and `claude.exe` count was 17 before and 17 at +120 s.
- Pass. On tracking commit `07f0b7b`, `- Flow: autonomous · target: integration/todo-cli` directly followed `- Re-plans: none`. Both wave rows were ⬜.
- Pass. `master` stayed at `3a1bcae` and no `refs/wave-method/claims/` ref remained at exit.

### C2 · wave-run

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "<scratch>/logs/C2.jsonl" 2> "<scratch>/logs/C2.err" &
wait $!
```

- Exit `0`, model `claude-sonnet-5-5`. Wall time 1.683 min.
- Result 1. `subtype: success`, `is_error: false`, `num_turns: 13`, `total_cost_usd: 0.63740612`. Stream duration 0.742 min. Permission denials 0. Lines after `result` 1.
  First line interim prose confirming the worktrees and active claim. Last line interim prose saying both tasks were pending and no merge had occurred.
- Finding. C2, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 1 trailing stream line after result 1.
- Result 2. `subtype: success`, `is_error: false`, `num_turns: 12`, `total_cost_usd: 0.63740612`. Stream duration 0.889 min. Permission denials 0. Lines after `result` 0.
  First line `Started: 2026-11-17 23:12`. Last line `Started: 2026-11-17 23:12 · Finished: 2026-11-17 23:14 (2 min)`.
- Stop line none.
- Pass. Both `system/init` events listed the four project wave skills and no plugin wave skills.
- Post-exit pass. Refs matched, worktree lists matched, and `claude.exe` count was 17 before and 17 at +120 s.
- Pass. The final result opened with `Started: 2026-11-17 23:12`.
- Pass. The final result ended with `Started: 2026-11-17 23:12 · Finished: 2026-11-17 23:14 (2 min)`.
- Pass. The final result ended without a question.
- Pass. Tracking commit `6f0b3a3` marked wave 1 ✅, with F1 🔄 waiting for wave 2. F2 was ✅ merged and its recorded merge `788fc19` was an ancestor of integration exit tip `1644997`.
- Pass. `master` stayed at `3a1bcae` and no claim ref remained at exit.
- Pass. A and C shared one assistant message ID. Both had completion notifications before either result. The CLI split their tool calls across stream lines.
- Finding. C2, skill execution defect. Expected task A to commit within its file list. Its commit `8104158` included bytecode caches. Coordinator commit `b744b7d` removed them before process exit.

### C3 · wave-run

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null > "<scratch>/logs/C3.jsonl" 2> "<scratch>/logs/C3.err" &
wait $!
```

- Exit `0`, model `claude-sonnet-5-5`. Wall time 2.550 min.
- Result 1. `subtype: success`, `is_error: false`, `num_turns: 15`, `total_cost_usd: 0.734344065`. Stream duration 0.728 min. Permission denials 0. Lines after `result` 1.
  One interim message that both tasks were running and the coordinator was waiting.
- Finding. C3, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 1 trailing stream line after result 1.
- Result 2. `subtype: success`, `is_error: false`, `num_turns: 19`, `total_cost_usd: 0.734344065`. Stream duration 1.617 min. Permission denials 0. Lines after `result` 0.
  First line `Started: 2026-11-17 23:16`. Last line `Started: 2026-11-17 23:16 · Finished: 2026-11-17 23:18 (2 min)`.
- Stop line none.
- Pass. Both `system/init` events listed the four project wave skills and no plugin wave skills.
- Post-exit pass. Refs matched, worktree lists matched, and `claude.exe` count was 17 before and 17 at +120 s.
- Pass. The final result opened with `Started: 2026-11-17 23:16`.
- Pass. The final result ended with `Started: 2026-11-17 23:16 · Finished: 2026-11-17 23:18 (2 min)`.
- Pass. The final result ended without a question.
- Pass. Tracking commit `16eb4f3` marked wave 2 ✅. F1 and F3 were ✅ merged, and their commits `037188a` and `677a875` were ancestors of integration exit tip `5833462`.
- Pass. An independent `python -m pytest -q` with the scratch venv in the integration worktree returned `11 passed`.
- Pass. `master` stayed at `3a1bcae`, no claim ref remained, and the plan remained under `plans/` on its tracking branch.
- Pass. B and D shared one assistant message ID. Both had completion notifications before either result. D initially supplied a plain model line and amended it to a valid Git trailer in the fix loop.

### C4 · background probe

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "Probe of background subagents; no skill is involved. In one message, call the Agent tool twice, both with run_in_background set to true. The first subagent runs the shell command: sleep 90 && date +%s > <scratch>/probe/bg-1.txt . The second runs the same command with bg-2.txt. Right after launching them, without waiting for their results, answer with the single line: launched" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 30 --max-budget-usd 2 < /dev/null > "<scratch>/logs/C4.jsonl" 2> "<scratch>/logs/C4.err" &
wait $!
```

Before the call, ran `mkdir <scratch>/probe`.

- Exit `0`, model `claude-sonnet-5-5`. Wall time 0.300 min.
- Result 1. `subtype: success`, `is_error: false`, `num_turns: 3`, `total_cost_usd: 0.1031609`. Stream duration 0.052 min. Permission denials 0. Lines after `result` 10.
  First line `launched`. Last line `launched`.
- Finding. C4, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 10 trailing stream lines after result 1.
- Result 2. `subtype: success`, `is_error: false`, `num_turns: 1`, `total_cost_usd: 0.1031609`. Stream duration 0.017 min. Permission denials 0. Lines after `result` 9.
  One continuation about the first nested sleep and a pending second report.
- Finding. C4, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 9 trailing stream lines after result 2.
- Result 3. `subtype: success`, `is_error: false`, `num_turns: 1`, `total_cost_usd: 0.1096771`. Stream duration 0.024 min. Permission denials 0. Lines after `result` 6.
  One continuation saying both Agents reported and the two Bash jobs were pending.
- Finding. C4, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 6 trailing stream lines after result 3.
- Stop line none.
- Pass. All three `system/init` events listed the four project wave skills and no plugin wave skills.
- Post-exit pass. Refs matched, worktree lists matched, and `claude.exe` count was 17 before and 17 at +120 s.
- Pass. Both Agent launches carried `run_in_background: true`. Both probes lacked marker files at exit and +120 s. See Background probe for the shutdown sequence.
- Finding. The prompt requested only `launched`. It was the first result, followed by two continuation results.

### C5 · wave-status

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "<scratch>/logs/C5.jsonl" 2> "<scratch>/logs/C5.err" &
wait $!
```

- Exit `0`, model `claude-haiku-5-5`. Wall time 0.733 min.
- Result 1. `subtype: success`, `is_error: false`, `num_turns: 11`, `total_cost_usd: 0.01627296`. Stream duration 0.700 min. Permission denials 0. Lines after `result` 0.
  First line `Started: 2026-11-17 23:23`. Last line `Started: 2026-11-17 23:23 · Finished: 2026-11-17 23:24 (1 min)`.
- Stop line none.
- Pass. One `system/init` event listed the four project wave skills and no plugin wave skills.
- Post-exit pass. Refs matched, worktree lists matched, and `claude.exe` count was 17 before and 17 at +120 s.
- Pass. The final result opened with `Started: 2026-11-17 23:23`.
- Pass. The final result ended with `Started: 2026-11-17 23:23 · Finished: 2026-11-17 23:24 (1 min)`.
- Pass. The plan header, `Tracking branch`, `Features`, feature table, `Waves`, and `Next` appeared in order.
- Pass. `Merged, not in master:` appeared exactly once, with no alternate spelling. F1, F2, and F3 each had a merged header, essence, test steps and `Approved:`. Both diff commands used `master...integration/todo-cli`.
- Pass. The exit refs and worktrees matched C4's +120 s snapshots.

### C6 · wave-status

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status plans/2026-11-02-todo-cli" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "<scratch>/logs/C6.jsonl" 2> "<scratch>/logs/C6.err" &
wait $!
```

- Exit `0`, model `claude-haiku-5-5`. Wall time 0.417 min.
- Result 1. `subtype: success`, `is_error: false`, `num_turns: 6`, `total_cost_usd: 0.01219479`. Stream duration 0.369 min. Permission denials 0. Lines after `result` 0.
  First line `Started: 2026-11-17 23:26`. Last line `Started: 2026-11-17 23:26 · Finished: 2026-11-17 23:26 (under 1 min)`.
- Stop line none.
- Pass. One `system/init` event listed the four project wave skills and no plugin wave skills.
- Post-exit pass. Refs matched, worktree lists matched, and `claude.exe` count was 17 before and 17 at +120 s.
- Pass. The final result opened with `Started: 2026-11-17 23:26`.
- Pass. The final result ended with `Started: 2026-11-17 23:26 · Finished: 2026-11-17 23:26 (under 1 min)`.
- Pass. The plan header, `Tracking branch`, `Features`, feature table, `Waves`, and `Next` appeared in order.
- Pass. `Merged, not in master:` appeared exactly once, with no alternate spelling. F1, F2, and F3 each had a merged header, essence, test steps and `Approved:`. Both diff commands used `master...integration/todo-cli`.
- Pass. The exit refs and worktrees matched C5's +120 s snapshots.

### C7 · wave-status

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status plans/2026-11-02-todo-cli" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "<scratch>/logs/C7.jsonl" 2> "<scratch>/logs/C7.err" &
wait $!
```

Before the call, ran `git branch -m master main`.

- Exit `0`, model `claude-haiku-5-5`. Wall time 0.617 min.
- Result 1. `subtype: success`, `is_error: false`, `num_turns: 11`, `total_cost_usd: 0.01356698`. Stream duration 0.587 min. Permission denials 0. Lines after `result` 0.
  First line `Started: 2026-11-17 23:29`. Last line `Started: 2026-11-17 23:29 · Finished: 2026-11-17 23:29 (under 1 min)`.
- Stop line none.
- Pass. One `system/init` event listed the four project wave skills and no plugin wave skills.
- Post-exit pass. Refs matched, worktree lists matched, and `claude.exe` count was 17 before and 17 at +120 s.
- Pass. The final result opened with `Started: 2026-11-17 23:29`.
- Pass. The final result ended with `Started: 2026-11-17 23:29 · Finished: 2026-11-17 23:29 (under 1 min)`.
- Pass. The plan header, `Tracking branch`, `Features`, feature table, `Waves`, and `Next` appeared in order.
- Pass. `Merged, not in main:` appeared exactly once. The report never named `master`. F1, F2, and F3 each had a merged header, essence, test steps and `Approved:`. Both diff commands used `main...integration/todo-cli`.
- Pass. The exit refs and worktrees matched the C6 snapshots after accounting for the single rename from `master` to `main`.

### C8 · wave-status

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null > "<scratch>/logs/C8.jsonl" 2> "<scratch>/logs/C8.err" &
wait $!
```

Before the call, ran `git merge --no-ff integration/todo-cli -m "Merge integration/todo-cli"`.

- Exit `0`, model `claude-haiku-5-5`. Wall time 0.533 min.
- Result 1. `subtype: success`, `is_error: false`, `num_turns: 5`, `total_cost_usd: 0.01207341`. Stream duration 0.501 min. Permission denials 0. Lines after `result` 0.
  First line `Started: 2026-11-17 23:31`. Last line `Started: 2026-11-17 23:31 · Finished: 2026-11-17 23:31 (under 1 min)`.
- Stop line none.
- Pass. One `system/init` event listed the four project wave skills and no plugin wave skills.
- Post-exit pass. Refs matched, worktree lists matched, and `claude.exe` count was 17 before and 17 at +120 s.
- Pass. The final result opened with `Started: 2026-11-17 23:31`.
- Pass. The final result ended with `Started: 2026-11-17 23:31 · Finished: 2026-11-17 23:31 (under 1 min)`.
- Pass. The switch from the C7 snapshot was the explicit two-parent merge `ce6fb55` on `main`. Its parents were `3a1bcae` and `5833462`. The integration branch had zero commits outside `main`.
- Pass. `Merged, not in main:` appeared exactly once and the next nonblank line was `none`. `Integration:` reported `in main` and the response never named `master`.
- Pass. The plan header, `Tracking branch`, `Features`, feature table, `Waves`, and `Next` appeared in order.

## Subagents

| Run | Wave | Task | Requested model | run_in_background | Same assistant message as another Agent call | Final output before result | Commit in feature branch at exit |
|---|---:|---|---|---|---|---|---|
| C2 | 1 | A | `sonnet` | omitted | yes | yes | `8104158` |
| C2 | 1 | C | `haiku` | omitted | yes | yes | `b16997e` |
| C3 | 2 | B | `sonnet` | omitted | yes | yes | `83819fc` |
| C3 | 2 | D | `haiku` | omitted | yes | yes | `ead6053` |
| C4 | — | probe 1 | omitted | `true` | yes | yes | — |
| C4 | — | probe 2 | omitted | `true` | yes | yes | — |

Matched the tool calls to their completed `task_notification` events. Every listed Agent completed before the first result event in its call. In each run, the two tool uses share the same assistant message ID even though each use has its own JSON line. C2 and C3 Agent acknowledgments say async even though the input flag was omitted. C3 D's row gives its amended task commit, reachable from the F3 tip `5d16464` at exit.

## Background probe

**Outcome (c) under the fixture's file-and-time rule.** Both Agent calls were accepted with `run_in_background: true` in one assistant message. The clock started at epoch `1794943278` and the process exited at `1794943296` (18 seconds, below 90 seconds). The `launched` result's `duration_ms` was 3094, so its `result_time` by the specified formula was `1794943281.094`. The continuation results had durations 1047 and 1415 ms, which are local to those results.

| Marker | At exit | At exit +120 s |
|---|---|---|
| `bg-1.txt` | absent, no epoch | absent, no epoch |
| `bg-2.txt` | absent, no epoch | absent, no epoch |

The stream provides the shutdown detail. Both Agents first tried foreground Bash commands starting with `sleep`, and both tool results rejected them. They then launched the same sleeps as background Bash tasks and returned completion notifications. After the last result, the CLI reported `stopped` for the two Bash tasks. This measures termination of the nested jobs at exit. Both outer Agents had already completed.

## Findings

- C2, skill execution defect. Expected task A to commit within its file list. Its commit `8104158` included bytecode caches, which coordinator commit `b744b7d` removed before exit.
- C3, skill execution defect. Expected task D to record a parseable model trailer in its first commit. It used a plain model line, which the fix loop replaced with a valid trailer.
- C4, CLI effect. Expected each requested 90-second sleep command to run in its Agent. Both foreground Bash calls starting with `sleep` returned errors. The Agents moved them into background Bash jobs, completed, and the CLI stopped those jobs before either file appeared.
- C4, CLI effect. Expected the response to be the single line `launched`. The first result matched, then two continuation results reported on the probe.
- C2 and C3, CLI effect. The first result still described work as pending, although both matched Agent completion notifications had already appeared in the stream. In each case a second result supplied the final wave report. Both waves used the parallel launch group and satisfied their repository checks.

- C2, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 1 trailing stream line after result 1.
- C3, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 1 trailing stream line after result 1.
- C4, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 10 trailing stream lines after result 1.
- C4, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 9 trailing stream lines after result 2.
- C4, CLI effect. Expected one terminal result with zero trailing stream lines. Observed 6 trailing stream lines after result 3.

## Caps

Maxima use R1–R3 and R6 from [the first chain](print-mode-chain.md), M1–M3, M9 and M10 from [the multi-wave chain](print-mode-multiwave.md), and the skill calls above. C1 counts as wave-run. C4 is a probe. Each maximum is tripled, then turns round up to a multiple of ten and costs round up to whole dollars. The wave-run values are per call. In C2 the two init-delimited segments had 12 and 11 top-level user events, with 13 and 12 reported turns. In C3 they had 14 and 18, with 15 and 19 reported turns. Top-level assistant message IDs were disjoint across the two segments of each call. The cap adds the segment turn counts and uses the highest cost field per call. In each of C2 and C3 both results share a session and report identical cost and API duration. Using only the largest single result's turn field would yield 22 turns in M3 and a rounded cap of 70.

| Skill | Largest turns | Largest cost (USD) | Rounded 3× turns | Rounded 3× cost (USD) |
|---|---:|---:|---:|---:|
| wave-triage | 9 (M1) | 0.4521856 (M1) | 30 | 2 |
| wave-plan | 16 (R2) | 1.0327658 (M2) | 50 | 4 |
| wave-run | 34 (C3) | 0.734344065 (C3) | 110 | 3 |
| wave-status | 11 (C5, C7) | 0.01627296 (C5) | 40 | 1 |

The status allowance of 60 turns and USD 0.50 covers the tripled, unrounded status measurements (33 turns and USD 0.04881888).
