# P16. wave-status opening line and branch name, and a two-wave chain on a fixed plan
User problem: re-plan of I9–I11: `wave-status` opens with `Started:` like every other skill, writes the real main
branch name once and never appends a correction, and a chain whose plan surely has two waves with parallel launch
groups, plus a probe of background subagents, is measured under `claude -p` through process exit · feature F4

## Cause

- I11: `skills/wave-plan/layout.md`, "Run times", makes `Started: <YYYY-MM-DD HH:MM>` the first line every run
  prints. The template that task U added (`skills/wave-status/SKILL.md:127-161`) starts with the plan header, and
  the closing sentence (`:213`) mentions only the times line. In print mode the result is the one final message, so
  M9 and M10 (`docs/rehearsals/print-mode-multiwave.md`, "## Findings") opened with the plan header. The template is
  wrong, not the shared rule: `wave-run` reports open with `Started:` (M3).
- I9: in M10 the scratch repository's branch was `main`, but the report wrote `Merged, not in master:` and
  `master...` commands, then appended a "correction" heading with `main` below the report. The skill never says
  how to find the main branch name: the label bullet (`skills/wave-status/SKILL.md:85-88`) only lists both spellings
  as examples, so a small model picked one. It also does not forbid text after the times line.
- I10: the toy list of P15 left the plan's shape to `wave-plan`, which merged five `todo.py` requests into one task
  with `After` on the other (M2): one wave, no launch group of two. Changing the list again would still not guarantee
  a shape. Background subagents were never exercised: no `wave-run` coordinator chose `run_in_background`, and no
  call asked for it.

## Approach

Three tasks in one wave on F4's branch, one after another (F4 is not merged; its fixes stay in F4):

- **X** (low) makes four exact edits of `skills/wave-status/SKILL.md`: the main branch name is resolved from git
  before writing; the template opens with `Started:`; the report is one message that ends with the times line; and
  "Before sending" checks the first line, the branch name and "no appended correction".
- **Y** (after X) runs a deterministic chain: the plan is not planned by a model but copied from
  `examples/01-greenfield-todo-cli/` of the source worktree — two waves, each with two tasks of different features and
  `After` `—`, so each wave has one launch group of two. The flow form switches it to autonomous flow, two
  `wave-run` calls run both waves, one separate call probes background subagents, and four `wave-status` calls check
  X's template on both branch names and with no merged feature left. A new record:
  `docs/rehearsals/print-mode-fixture-chain.md`, runs C1–C8.
- **Z** (after Y) updates `docs/claude-print-mode.md` from Y's record.

Why the example plan and not a new list: it is maintained with the skills, its status check runs in the check
command, it has exactly the shape I10 needs, and the chain no longer depends on what `wave-plan` decides. Why a
separate background probe: `wave-run` does not tell the coordinator to use background subagents, and changing the
skill to force it is not what I10 asks; the driver needs to know what the CLI does with a background subagent when
the main agent ends, which only a direct call shows. Why not append to `print-mode-multiwave.md`: it records a
different chain; a new record keeps each chain's runs, findings and caps together.

Nothing under `skills/` changes except `skills/wave-status/SKILL.md` (task X). A skill defect Y finds is a finding,
never an edit.

## Model/API changes

### `skills/wave-status/SKILL.md` (task X)

Four exact edits on F4's branch (line numbers of 3351459); no other line changes.

1. In "## What to read", append this bullet after the last bullet (the one starting
   `` - `git worktree list --porcelain` ``, which ends with `` `git branch --merged <main> "feat/*"`. ``):

   ```
   - The main branch name, once, before writing anything: `main` when
     `git rev-parse --verify --quiet refs/heads/main` succeeds, else `master` when
     `git rev-parse --verify --quiet refs/heads/master` succeeds (`layout.md`, "Names"). This name is
     `<main branch>` in every label and command of the report. Never take it from an example in this file, from
     another repository or from memory.
   ```

2. In the bullet `` - `Merged, not in <main branch>:` `` (lines 81-88), replace the two sentences from
   `In the label, <main branch> is replaced` to the end of the bullet with:

   ```
   In the label, `<main branch>` is the name resolved in "What to read", alone: never the plan slug, the
   integration branch, `<main>`, quotes, a possessive or a second rendering of the name; the label appears once
   per plan.
   ```

   (So `Merged, not in main:` or `Merged, not in master:` no longer appear as two examples to choose from.)

3. In "### Template", make the first two lines inside the four-backtick fence:

   ```
   Started: <YYYY-MM-DD HH:MM>

   ```

   followed by the existing `## <plan folder> · …` line. Then, in the bullets under the fence, replace the bullet
   starting `- Always printed:` so that it starts `- Always printed: the opening `Started:` line, the plan
   header, …` (the rest unchanged), and add this bullet after the last bullet of that list:

   ```
   - The report is one message, from the `Started:` line to the times line; nothing follows the times line. A
     mistake found before sending is fixed by rewriting the report, never by a correction appended below it.
   ```

4. Replace the paragraph of "### Before sending" with:

   ```
   Compare the report with "Template": the first line is `Started: <YYYY-MM-DD HH:MM>`; every plan has its header,
   `Tracking branch`, `Features`, the table, `Waves` and `Next` lines, in this order; the last line is the
   `Started: … · Finished: …` line. In autonomous flow the `Merged, not in <main branch>:` label appears exactly
   once per plan, with the name resolved in "What to read" (`Merged, not in master:` in a repository whose main
   branch is `master`), followed by one full merged block per feature or `none`, and every command of the report
   names that same branch. If something is missing, merged into prose, or a label or a branch name differs,
   rewrite the whole report before sending it; never send a correction after it.
   ```

   and replace the sentence `The report ends with the `Started: … · Finished: …` line (`layout.md`, "Run times").`
   (line 213) with:

   ```
   The report starts with the `Started:` line and ends with the `Started: … · Finished: …` line (`layout.md`,
   "Run times").
   ```

### `docs/claude-print-mode.md` (task Z)

- "Reading the result", rule 2: the expectation `Started: <time>` on the first line covers all four skills; remove
  the sentence that says the `wave-status` template puts the plan header first. Rule 3: a missing opening `Started:`
  in any skill's result calls for inspection.
- A rule 5, only from Y's C4 outcome (see "Background probe"): outcome (b) → before the next call, the driver waits
  until the `claude.exe` process count is back at its value before the call and the refs are stable for 120 s;
  outcome (a) or (c) → no rule 5, one sentence in "## Result" says that the process ends only after (a) or kills (c)
  background subagents. Outcome (d) → no rule 5.

## Algorithm

### Scratch and fixture (task Y)

1. `<scratch>` = `mktemp -d`; `<scratch>/repo` = `git init -b master`; a `LICENSE` file with one line `MIT`;
   commit `init`. The branch is `master` on purpose: M10 wrote `master` where the branch was `main`; C5–C6 test the
   other direction, C7–C8 test `main` after a rename.
2. `python -m venv <scratch>/venv`; `<scratch>/venv/Scripts/python -m pip install pytest pyyaml` (on a system where
   the folder is `bin`, use `bin`). Every later call runs with `PATH="<scratch>/venv/Scripts:$PATH"` exported, so
   `python -m pytest` works for the subagents. pip failing → stop the task, record nothing (see "Limits").
3. From the source worktree: `sh install.sh <scratch>/repo --no-codex` (read its usage line first); commit
   `install wave skills` in the toy repository.
4. Copy `examples/01-greenfield-todo-cli/` of the source worktree to `<scratch>/repo/plans/2026-11-02-todo-cli/`
   (the folder that its README names), unchanged; commit `add fixture plan` on `master`. This stands for
   `wave-plan`'s merge of a plan; no tracking branch is created by hand.
5. Check: `python <source worktree>/skills/wave-plan/scripts/status_check.py plans/2026-11-02-todo-cli` exits 0.

### Call form and post-exit check

Every call, in Git Bash, from `<scratch>/repo`:

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "<prompt>" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model <model> \
  --max-turns <turns> --max-budget-usd <usd> < /dev/null > "<scratch>/logs/<run>.jsonl" 2> "<scratch>/logs/<run>.err" &
wait $!
```

1. Before: `MSYS_NO_PATHCONV=1 tasklist /FI "IMAGENAME eq claude.exe" /NH | grep -c claude.exe` → `procs_before`;
   `start=$(date +%s)`.
2. After `wait`: `end=$(date +%s)`; wall minutes = `(end - start) / 60`. At once
   `git for-each-ref --format='%(refname) %(objectname)'` → `<run>.refs-exit`, `git worktree list --porcelain` →
   `<run>.wt-exit`.
3. Wait 120 seconds; the same two commands → `<run>.refs-120`, `<run>.wt-120`; the process count → `procs_after`.
4. Post-exit check passes when both pairs of files are identical and `procs_after` ≤ `procs_before`.
5. From the stream: the `system/init` event lists the four project `wave-*` skills and no `wave-method:` skill;
   the number of lines after the `type: result` line (expected 0); `subtype`, `is_error`, `num_turns`,
   `total_cost_usd`, `duration_ms` (as minutes), `permission_denials`; the first and last line of `result`.

### Runs C1–C8 (task Y)

| Run | Before the call | Prompt | `--model` | `--max-turns` | `--max-budget-usd` |
|---|---|---|---|---:|---:|
| C1 | — | `/wave-run plans/2026-11-02-todo-cli flow autonomous` | `sonnet` | 100 | 2 |
| C2 | — | `/wave-run plans/2026-11-02-todo-cli` | `sonnet` | 400 | 8 |
| C3 | C2 ended without a stop line | `/wave-run plans/2026-11-02-todo-cli` | `sonnet` | 400 | 8 |
| C4 | `mkdir <scratch>/probe` | the background probe below, with `<scratch>` written as the absolute path | `sonnet` | 30 | 2 |
| C5 | — | `/wave-status` | `haiku` | 60 | 0.5 |
| C6 | — | `/wave-status plans/2026-11-02-todo-cli` | `haiku` | 60 | 0.5 |
| C7 | `git branch -m master main` in `<scratch>/repo` | `/wave-status plans/2026-11-02-todo-cli` | `haiku` | 60 | 0.5 |
| C8 | `git merge --no-ff integration/todo-cli -m "Merge integration/todo-cli"` in `<scratch>/repo` (the user's merge) | `/wave-status` | `haiku` | 60 | 0.5 |

- A stop line in C1, C2 or C3 (`Stop <code>: … — next: …`) ends the `wave-run` part: record it, skip the rest of
  C1–C3, run C4–C8 anyway (C8's merge only when `integration/todo-cli` exists; otherwise skip C8 and say so).
- Spend cap of the whole task: 30 USD by the sum of `total_cost_usd`; when passed, run only the `wave-status` calls
  left, then stop.

Checks after each run (each pass, or a finding with expected / got):

- C1: exit 0; the README on `plan/todo-cli` has `- Flow: autonomous · target: integration/todo-cli` right after
  `- Re-plans: none`; no wave is 🔄; `master` unchanged; no `refs/wave-method/claims/` ref at exit.
- C2: wave 1 ✅ on `plan/todo-cli`; F2 `✅ merged` with a hash that is an ancestor of `integration/todo-cli`; F1 🔄
  waiting for wave 2; `master` unchanged; no claim ref at exit; the result opens with `Started:` and ends with the
  times line, without a question.
- C3: wave 2 ✅; F1 and F3 `✅ merged` into `integration/todo-cli`; `python -m pytest -q` passes in the integration
  worktree (independent run, venv Python); `master` unchanged; no claim ref; the plan is not archived; the result
  opens with `Started:` and ends with the times line, without a question.
- C2 and C3, subagents: one row per `Agent` tool call in "## Subagents" (columns below). The wave has one launch
  group of two tasks, so the expected outcome is both `Agent` calls in one assistant message; two messages is a
  finding `no parallel launch`, naming the `wave-run` rule it breaks (`skills/wave-run/SKILL.md`, step 4, "Launch
  groups": "A group launches at once").
- C4: see "Background probe".
- C5, C6, C7: the first line is `Started: <YYYY-MM-DD HH:MM>`; the last line is the times line, nothing after it;
  the plan has the header, `Tracking branch`, `Features`, the table, `Waves` and `Next` lines; the label is exactly
  `Merged, not in master:` (C5, C6) or `Merged, not in main:` (C7), once, and the other spelling appears nowhere;
  three full merged blocks follow it (F1, F2, F3: header with `merged into`, essence, how to test, `Approved:`);
  every command names the branch of that label.
- C8: the same first and last line; `Merged, not in main:` once, followed by `none`; `Integration:` says
  `in main`; no `master` anywhere.

### Background probe (C4)

Prompt (one line; `<scratch>` replaced by the absolute path in the call, written as `<scratch>` in the record):

```
Probe of background subagents; no skill is involved. In one message, call the Agent tool twice, both with run_in_background set to true. The first subagent runs the shell command: sleep 90 && date +%s > <scratch>/probe/bg-1.txt . The second runs the same command with bg-2.txt. Right after launching them, without waiting for their results, answer with the single line: launched
```

Record: whether both `Agent` tool calls carry `run_in_background: true` in the stream (or the tool rejected it);
`result_time` = `start + duration_ms / 1000`; for each file, whether it exists at exit and 120 s after exit, and the
epoch it holds. Outcome, exactly one:

- (a) both files exist at exit and hold epochs ≤ `result_time` + 5: the process ends only after its background
  subagents end;
- (b) a file appears only after exit: background subagents outlive the process;
- (c) no file exists 120 s after exit, and the process ended before 90 s: background subagents are killed at exit;
- (d) the calls did not run in the background (parameter absent or rejected): background launch is not available in
  print mode.

Do not repeat the probe with another prompt; an unexpected stream (for example no `Agent` call) is recorded as is
under (d) with what the stream shows.

### Record `docs/rehearsals/print-mode-fixture-chain.md` (task Y)

- Title `# Rehearsal: fixture-plan print-mode chain`; one line: date, `claude --version`, source commit.
- `## Setup`: scratch, fixture, venv, install, call form, post-exit procedure, as above.
- `## Runs`: one `### C<n> · <skill or probe>` per run: command (in a `bash` block); exit code; model; `subtype`,
  `is_error`, `num_turns`, `total_cost_usd`; stream and wall minutes; lines after `result`; denials; first and last
  result line; stop line or none; post-exit check; the run's checks.
- `## Subagents`: `| Run | Wave | Task | Requested model | run_in_background | Same assistant message as another Agent call | Final output before result | Commit in feature branch at exit |`,
  one row per `Agent` call of C2 and C3 (and C4's two calls, wave `—`, task `probe`).
- `## Background probe`: C4's outcome letter and its evidence.
- `## Findings`: each with run, expected / got, and whether it is a CLI effect or a skill defect.
- `## Caps`: per skill, the largest turns and cost over R1–R3 and R6 (`print-mode-chain.md`), M1–M3, M9 and M10
  (`print-mode-multiwave.md`) and C1–C8 (C1 counts as `wave-run`; C4 is not a skill and is left out), then three
  times each, turns rounded up to a multiple of 10 and dollars up to a whole number; `wave-run` per call.

### Edits of `docs/claude-print-mode.md` (task Z)

The six `## ` sections keep their names and order.

- "## Environment": one bullet: date, `claude --version`, skills from F4's branch, link to
  `rehearsals/print-mode-fixture-chain.md`.
- "## Probes": after "### Multi-wave chain runs (M1–M10)", a subsection "### Fixture chain runs (C1–C8)" with the
  same table columns (C4 in the table with `probe` as its skill), one sentence on the launch groups of C2 and C3
  (parallel or not) and one on C4's outcome letter and what it means.
- "## Result": one paragraph: two waves run by two calls, parallel launch observed or not, C4's outcome, and
  whether the repository changed after exit.
- "## Prompt form for the driver": the caps of the prompt table from Y's "## Caps", and the sentence on how they
  were derived names all three chains; `wave-status` keeps 60 turns and 0.50 USD unless Y measured more than a
  third of them. Reading rules 2 and 3 and rule 5 as in "Model/API changes". The `wave-run` row's "Rehearsal" cell
  names C2 and C3.
- "## Open points": remove the multi-wave point when C2 and C3 both ran and at least one had a parallel launch
  group, and the background part of it when C4 gave (a), (b) or (c); remove the M10 heading point when C5–C8 passed
  their label checks, and the `Started:` point when C5–C8 passed their first-line checks. Keep the turn-cap
  enforcement point. Add only what Y left open, each with what would settle it.

## Limits

- Only `skills/wave-status/SKILL.md` changes under `skills/` (task X). Y and Z change only their docs files.
- The chain runs only in `<scratch>`; nothing is pushed; `<scratch>` is deleted at the end; nothing else is
  deleted.
- `claude` missing or not signed in, or pip failing in step 2 of the setup → stop at once and report; no record of
  runs that did not happen.
- No user path or user name in the docs:
  `git grep -n -e "C:/Users" -e "C:\\\\Users" -e "/home/" -e "/Users/" -- docs` prints nothing.
- Quote at most one sentence (under 15 words) per docs page.

## Acceptance tests

- X: `git grep -n -e "^Started: <YYYY-MM-DD HH:MM>$" -e "refs/heads/master" -e "nothing follows the times line"
  -e "never send a correction" -- skills/wave-status/SKILL.md` → the template's first line, the resolve bullet,
  the one-message bullet and the "Before sending" sentence; `git grep -n "Merged, not in main:" --
  skills/wave-status/SKILL.md` → nothing; `git diff --stat main...HEAD` lists, besides the three earlier F4 files,
  nothing new.
- Y: `git grep -n -e "^## " -e "^### C" -- docs/rehearsals/print-mode-fixture-chain.md` → `## Setup`, `## Runs`
  with C1–C8 (or the runs that took place and a finding for each skipped one), `## Subagents`,
  `## Background probe`, `## Findings`, `## Caps`; every run has its fields, its post-exit check and its checks.
- Z: `git grep -n "^## " -- docs/claude-print-mode.md` → the six sections in order;
  `git grep -n "^### Fixture chain runs" -- docs/claude-print-mode.md` → one line;
  `git grep -n "template puts the plan header first" -- docs/claude-print-mode.md` → nothing; the prompt table's
  caps equal Y's "## Caps".
- All: `git diff --stat main...HEAD` lists only `skills/wave-status/SKILL.md`,
  `docs/rehearsals/print-mode-multiwave.md`, `docs/rehearsals/print-mode-fixture-chain.md` and
  `docs/claude-print-mode.md`; the check command is green.
