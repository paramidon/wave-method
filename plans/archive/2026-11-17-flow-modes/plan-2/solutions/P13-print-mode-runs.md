# P13. Real print-mode runs of every skill, and the driver form checked against F1
User problem: re-plan of I5–I6: run `wave-triage`, `wave-plan`, `wave-run` and `wave-status` for real under
`claude -p` in the driver form, test the `auto` and `dontAsk` modes and PowerShell, and make the prompt table of
`docs/claude-print-mode.md` match F1's merged argument forms · feature F3

## Cause

- I5: task H (wave 2) probed only `wave-status` (`docs/claude-print-mode.md`, "Open points" on
  `feat/flow-modes-p2/F3-headless-skill-probe` at `07200f3`). Unknown: how long real `wave-triage`, `wave-plan` and
  `wave-run` calls are (turns, cost, minutes), whether `wave-run` launches subagents under `-p`, whether a call ends
  before background subagents finish, whether `--permission-mode auto`, `dontAsk` or `--permission-prompts none` let
  the skills work, and how PowerShell passes the prompt and stdin.
- I6: the prompt table was written against F1 before its merge. On F1's branch at `1c65676`:
  - `wave-triage` and `wave-plan` take `flow autonomous` as the first two words (`skills/wave-plan/layout.md:386-389`):
    the table's rows match.
  - A plan written by `wave-plan` in autonomous flow already has `- Flow: autonomous · target: integration/<name>`
    in its README (`skills/wave-plan/layout.md:399`), and `wave-run` takes the flow from there
    (`skills/wave-run/autonomous.md:3-4`). The flow form (`skills/wave-run/autonomous.md:11-28`) only switches a plan's
    flow. So the table's "Once per plan: `/wave-run <plan folder> flow autonomous`" is wrong for plans of an
    autonomous index: the flow form is needed only for a plan planned in manual flow.
  - `/wave-run <plan folder>` without a number takes the first ⬜ or ❌ wave (`skills/wave-run/SKILL.md:20`).
  - Wave 3 (tasks I, J, K) still changes these texts. Task N reads them again on its branch, where F1 is merged.

## Approach

Two tasks of F3, in wave 4, after F1 is merged into `main` (and `main` into F3's branch, which `wave-run` does before
the wave):

- **N** runs one real autonomous chain in a scratch toy repository with `claude -p`, exactly in the driver form of the
  doc: triage → plan → `wave-run` until no wave is left or a run stops → status. Its record
  `docs/rehearsals/print-mode-chain.md` keeps every command, the result fields and the repository checks after each
  run.
- **O** (after N) runs the cheap probes Q-a … Q-d (permission modes, PowerShell), then rewrites "Result", "Prompt form
  for the driver" and "Open points" of `docs/claude-print-mode.md` from N's record and its own probes.

Why real runs and not another walkthrough: tasks L and M of wave 3 follow the skill texts by hand. Only `claude -p`
shows what the CLI does with them: skill expansion with arguments, subagents, permission denials, turn counts. Why
after F1 is merged: the forms to check are F1's, and the installer must install skill texts that contain F1. Why two
tasks: a medium task may not form a wave alone, and the work splits cleanly by file (N's record, O's doc).

Neither task changes anything under `skills/`. A skill defect a run shows is a finding of the record and of the
task's report (it becomes a problem entry and a re-plan), never a fix.

## Algorithm

### Scratch and toy project (both tasks)

- `<scratch>`: a new folder in the system temp folder (`mktemp -d`), outside this repository. Never run a probe in
  this repository or in any other project of the user. Delete `<scratch>` at the end of the task; delete nothing else.
- Toy repository `<scratch>/repo`: `git init -b main repo`; in it
  - `todo.py`: `VERSION = "0.1.0"`; `add(items, text)` returns `items + [{"text": text, "done": False}]`;
    `rm(items, n)` returns the list without item `n` (1-based); `list_items(items)` returns the lines
    `"<n>. <text>"` of the items that are not done;
  - `test_todo.py`: `unittest` tests for the three functions, one each. Check: `python -m unittest` in the folder;
  - commit `init`.
- Skills: from the task's worktree, `sh install.sh <scratch>/repo --no-codex` (project install into
  `.claude/skills/wave-*`); commit them in the toy repository as `install wave skills`.
- In every record and doc, write `claude` for the binary path, `<scratch>` for the temp folder and `~` for the home
  folder: no user name or absolute user path.

### Call form (N, and O where it says so)

From `<scratch>/repo`, in Git Bash:

```
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "<prompt>" --output-format stream-json --verbose --permission-mode bypassPermissions --setting-sources project,local --model <model> --max-turns <turns> --max-budget-usd <usd> < /dev/null > <scratch>/logs/<run>.jsonl 2> <scratch>/logs/<run>.err; echo "exit $?"
```

- `stream-json` instead of the doc's `json`: the events show the tool calls and subagents; its last event is the
  same result object (`subtype`, `is_error`, `num_turns`, `total_cost_usd`, `duration_ms`, `permission_denials`,
  `result`).
- `--setting-sources project,local` keeps the user's installed plugin (an older version without F1) out. The
  `system/init` event of every run must list the project skills `wave-triage`, `wave-plan`, `wave-run`,
  `wave-status` and no `wave-method:` skill; otherwise stop the chain and record it.
- `timeout 3600`: exit 124 means the wall-clock cap hit. Run each call in the background and wait for it: a
  `wave-run` call may take most of an hour.

### Runs of task N

| Run | Prompt | `--model` | `--max-turns` | `--max-budget-usd` |
|---|---|---|---|---|
| R1 | `/wave-triage flow autonomous 1. add a --version option that prints VERSION 2. show done items differently in list 3. rename rm to delete` | `opus` | 150 | 5 |
| R2 | `/wave-plan flow autonomous <index path from R1> part 1` | `opus` | 200 | 8 |
| R3, R4, R5 | `/wave-run <plan folder from R2>` | `sonnet` | 400 | 8 |
| R6 | `/wave-status` | `haiku` | 60 | 0.5 |

- R1's list has one ambiguous item (2), so autonomous triage must assume instead of asking.
- If R1's index has more than one part, R2 plans part 1 only; record the other parts.
- R3 to R5: one call per wave, the next only when the previous call's README shows a wave still ⬜ or ❌ and the
  call ended without a stop line. A stop line ends the chain; record it (code and `next:`), then run R6.
- Spend cap of the whole task: when the sum of `total_cost_usd` passes 30, run R6 and stop the chain.
- Do not run the flow form: the plan from R2 must already be in autonomous flow. That is the point of I6.

After every run record: the command; exit code; `subtype`, `is_error`, `num_turns`, `total_cost_usd`, minutes
(`duration_ms`); the number and the tools of `permission_denials`; the first line of `result`; the stop line or
"none"; and these checks (pass, or a finding with expected / got):

- every run: the `result` starts with `Started:` and ends with a `Started: … · Finished: …` line; it does not end with
  a question to the user; `git for-each-ref refs/wave-method/claims/` prints nothing after the run.
- R1: the index is committed and merged into `main`; its header has `- Flow: autonomous · target: integration/<topic>`
  right after `- Index:`; "Assumptions" has an `Assumed (autonomous, not asked)` line; "Open questions" is `none`.
- R2: `git rev-parse main` equals its value after R1; branch `integration/<topic>` exists and
  `git cat-file -e integration/<topic>:<plan folder>/README.md` succeeds; that README has the `Flow:` line; the
  tracking branch `plan/<slug>` exists; `status_check.py` (from the task's worktree, on the plan folder in the
  tracking worktree) exits 0.
- R3–R5: the wave's status on the tracking branch is ✅ or ⚠️, or ❌ with a stop line; every feature it finished is
  either merged into `integration/<topic>` (its merge commit there) or `👀 review`; `git rev-parse main` unchanged;
  `python -m unittest` green in the integration worktree; subagents: the number of subagent tool calls in the stream,
  the `model` each asked for (when the call names one), and whether any subagent was still running when the result
  event came (a tool call without its tool result).
- R6: the report lists every feature merged into `integration/<topic>` under `Merged, not in main:` with its block.

### Probes of task O

Each in a fresh small scratch repository (`git init -b main`, one commit with a `README.md`), without the wave skills,
`--model haiku --max-turns 15 --max-budget-usd 0.5 --output-format json`, Git Bash form with `MSYS_NO_PATHCONV=1` and
`< /dev/null`, except Q-d. The step prompt:

`Do these steps as separate commands and report each as done or refused: 1. create probe.txt containing x; 2. git add probe.txt; 3. git commit -m probe; 4. git worktree add -b feat/probe ../wt-probe; 5. in ../wt-probe create b.txt and commit it; 6. back in this folder run git merge --no-ff feat/probe -m merge-probe; 7. python -c "print(1)".`

- **Q-a** `--permission-mode auto`.
- **Q-b** `--permission-mode dontAsk`; then `--permission-mode dontAsk --allowedTools "Write,Edit,Bash(git *),Bash(python *)"`.
- **Q-c** `--permission-prompts none` without a mode, only if `claude --help` or the CLI reference lists the flag
  (else "not available" with the reason); with `stream-json --verbose`, also record whether `system/init` lists
  `AskUserQuestion`.
- **Q-d** PowerShell (Windows PowerShell 5.1, `powershell -NoProfile -File <scratch>/q-d.ps1`; also `pwsh` if
  installed, else "not available"), in the toy repository of the common setup (skills installed):
  1. `/wave-status` with stdin closed by `$null | claude -p "/wave-status" …`: does the `Started:` line appear, does
     the "no stdin data received" warning appear on stderr;
  2. a non-skill prompt `Repeat the text after the colon exactly, nothing else:` followed by three lines that
     contain `"`, `$HOME`, a backtick and `|`, passed from a single-quoted here-string `@'…'@`: is the reply
     identical;
  3. `$LASTEXITCODE` after a `--max-turns 1` call, and `($out | ConvertFrom-Json).subtype` of a `json` call.

Record per probe: the command, exit code, the step table (done / refused) or the observed result, and
`permission_denials`. A mode this CLI version or account refuses: record the error text.

### Edits of `docs/claude-print-mode.md` (task O)

The six `## ` sections keep their names and order.

- "## Environment": one bullet for the re-run: date, `claude --version`, skills installed from the branch with F1.
- "## Probes": after "### P-f", the subsections "### Q-a …" to "### Q-d …" in the form of P-a to P-f; then
  "### Chain runs (R1–R<n>)": one table (run, skill, exit, `subtype`, turns, cost, minutes, denials, stop line) and a
  link to `rehearsals/print-mode-chain.md` for the details.
- "## Result": rewritten for all four skills.
- "## Prompt form for the driver":
  - the `wave-run` row: `/wave-run <plan folder> <N>`, or `/wave-run <plan folder>` for the next ⬜ or ❌ wave; the
    flow form `/wave-run <plan folder> flow autonomous [review <F-IDs>]` only for a plan planned in manual flow, or to
    change the manual-review list;
  - every prompt of the table appears in N's record as it was run (same form, only the arguments differ), or the row
    says why it was not run;
  - `--max-turns` and `--max-budget-usd` per skill: three times the largest value N measured for that skill, turns
    rounded up to a multiple of 10, dollars up to a whole number; `wave-status` keeps 60 and 0.5 unless N measured
    more;
  - permission mode: keep `bypassPermissions` as the tested default; add `auto` as the alternative only if Q-a did
    every step, and `dontAsk` with its `--allowedTools` list only if Q-b's second run did every step;
  - a PowerShell block of the call, from Q-d (stdin, quoting, exit code, JSON parsing);
  - the reading rules stay, changed only where N or Q showed a case they get wrong.
- "## Open points": remove the points settled by N and Q (the `wave-run`/`wave-triage`/`wave-plan` runs, `auto`,
  `dontAsk`, `--permission-prompts none`, F1's argument forms, PowerShell); keep or add only what is still unsettled,
  each with what would settle it.

## Limits

- Nothing under `skills/` changes; a skill defect is a finding (record and report), never an edit.
- The chain runs only in `<scratch>`; nothing is pushed; the scratch folder is deleted at the end.
- No user path or user name in the docs: `git grep -n -e "C:/Users" -e "C:\\\\Users" -e "/home/" -e "/Users/" -- docs`
  prints nothing.
- Quote at most one sentence (under 15 words) per docs page.
- If the whole chain cannot start (R1 fails before triage starts, `claude` not signed in), stop and report; do not
  write a record of probes that did not run.

## Acceptance tests

- N: `docs/rehearsals/print-mode-chain.md` has `## Setup`, `## Runs` (one `### R<n>` per run) and `## Findings`;
  every run has its command, exit code, the result fields and the checks; the chain ran R1, R2 and at least one
  `wave-run` call, and R6; every failed check is a finding with expected / got.
- O: `git grep -n "^## " -- docs/claude-print-mode.md` lists the six sections in order; Q-a to Q-d each have a
  command, an exit code and a result, or "not available" with the reason;
  `git grep -n "Once per plan" -- docs/claude-print-mode.md` prints nothing; "Open points" no longer says that F1 is
  not merged or that PowerShell was not probed.
- Both: `git diff --stat main...HEAD` lists only the two docs; the check command is green.
