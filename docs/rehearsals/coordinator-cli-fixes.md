# Rehearsal: the fixes of tasks R and S in real wave-auto runs (Claude Code CLI)

2026-11-25 · Claude Code 2.1.326 · source commit `36c4a54` (the working folder before this record).

Task T of feature F1, the third CLI rehearsal: the `Resume:` line after a `triage-ask` without questions, the status
report during a triage, the step count, a task whose tool is missing halting only its unit after the other task ran,
both command forms in the waiting line, and a claim kept without files.

Outcome: every expectation of runs T2, T-copy, T3 and T4 and every report check holds. T1 misses its `Resume:` line
(finding TF-1); its other expectations hold.

## Setup

- `<scratch>` made with `mktemp -d` outside every repository. Per call: `<scratch>/calls/<run>.jsonl` (stream), `.err`,
  `.exit`, `.start`, `.end`, `<run>.coord.txt` (the coordinator's events: those with no `parent_tool_use_id`) and
  `<run>.evidence.txt` (`git branch --list`, `git for-each-ref refs/wave-method/`, `git log --oneline -3 main`,
  `git worktree list`, the unit's README "Waves" and "Tasks").
- Fixture `<scratch>/textkit` on `main`, local user `rehearsal` / `rehearsal@example.invalid`, with
  `textkit/__init__.py`, `tests/test_smoke.py`, `README.md` and `.gitignore` as in "Fixture (both)"; commits
  `Seed textkit` and `Seed textkit with wave skills` (`e5d4b84`).
- Skills: `sh <working folder>/install.sh <scratch>/textkit --no-codex` (five skills under `.claude/skills`).
  `<scratch>/venv`: Python 3.14, pytest 9.2.0, first on `PATH`.
- Calls: `claude -p "<prompt>" --output-format stream-json --verbose --permission-mode auto --max-budget-usd <rest>`,
  stdin from `/dev/null`, `MSYS_NO_PATHCONV=1`, no `--model`, the run's repository as the current folder. Cap 8 USD.
- Every `system/init` names `claude-sonnet-5-5` as the coordinator's model (the CLI default here) and also lists the
  four skills of the account-level `wave-method` plugin. `wave-auto` recommends an Opus-class coordinator, so TF-1 is
  a finding for a Sonnet coordinator.
- Every step's agent call but T1's `status` ran in the background (`is_backgrounded: true`); the coordinator got each
  return as a task notification, so one call has several `result` events with the same `total_cost_usd`.
- Permission denials: none in any call. No run asked the user a question.
- List (one argument), the list of "Task P — stops":

  ```
  1. Add textkit/slug.py with slugify(text): ASCII letters and digits only, lower case, words joined by "-"; every other character separates words. 2. Add textkit/count.py with count_words(text) returning a dict word -> count; a word is a run of ASCII letters and digits, compared in lower case.
  ```

### Models per step

The model of each agent call is the `message.model` of its subagent's events.

| Step | Model | Runs |
|---|---|---|
| coordinator | `claude-sonnet-5-5` | T1, T2, T3, T4 |
| `triage-ask`, `triage-answers`, `triage-finish`, `plan` | `claude-opus-5-5` | T1, T2 |
| `wave` | `claude-sonnet-5-5` | T3, T4 |
| `task` (both tasks low) | `claude-haiku-5-5` | T3, T4 |
| `navigate`, `status` | `claude-haiku-5-5` | T1 to T4 |

### Cost

| Call | Files | Time | USD |
|---|---|---|---|
| T1 | `T1.*` | 1 min 35 s | 0.91 |
| T2 | `T2.*` | 4 min 50 s | 1.90 |
| T3 | `T3.*` | 4 min 17 s | 0.82 |
| T4 | `T4.*` | 5 min 31 s | 1.18 |

Summed `total_cost_usd`: **4.81 USD** of the 8 USD cap.

## Runs

### T1 · `triage-ask` of the list, rail at one step

```bash
claude -p "/wave-auto steps 1 <list>" ...      # in <scratch>/textkit
```

- Exit 0. One counted step: `triage-ask` (opus) → `questions 0 · index plans/2026-11-25-slug-and-count/index.md`.
  Then the claim, its release, and `status` (haiku). No `navigate`.
- Coordinator text, in full besides the final report: `Started: 2026-11-25 21:38`, the `Capabilities:` line, and
  `The triage-ask step is running. I'm waiting for it to return before continuing.` After the step returned the
  coordinator ran `date +%H:%M` (→ `21:39`), took the claim and wrote no text: **no progress line and no `Resume:`
  line** (TF-1). The only `/wave-auto <index path>` lines are under `### Status` and `### Next` of the final report.
- Final report: `Run: 1 steps · ended by rail: steps 1 · …`; one Steps row
  `| 21:39 | triage-ask | list | questions 0 · index plans/2026-11-25-slug-and-count/index.md |`; `### Halts` `- none`;
  `### Next` ``- Continue: `/wave-auto plans/2026-11-25-slug-and-count/index.md` · `$wave-auto plans/2026-11-25-slug-and-count/index.md` ``.
- The Status part holds a block for the triage:

  ```
  ## plans/2026-11-25-slug-and-count · triage in progress · autonomous

  - Triage branch: `triage/slug-and-count` · `<scratch>/textkit.worktrees/slug-and-count-triage`
  - Phase: waiting for answers
  - Next: `/wave-auto plans/2026-11-25-slug-and-count/index.md` · `$wave-auto plans/2026-11-25-slug-and-count/index.md`
  ```

  and no `git worktree remove` or `git branch -d` anywhere; `Coordinator claims: none`.
- State (`T1.evidence.txt`): `main` at `e5d4b84`; branch `triage/slug-and-count` with its worktree;
  `refs/wave-method/` empty.

### T2 · answers, finish, plan, rail at three steps

```bash
claude -p "/wave-auto steps 3 plans/2026-11-25-slug-and-count/index.md" ...      # in <scratch>/textkit
```

- Exit 0. No question to the user. The coordinator took the claim, read "Open questions" from
  `triage/slug-and-count` (`- none`), and launched `triage-answers` without a `navigate` first.
- Agent calls, in order:

  | Step | Model | Return |
  |---|---|---|
  | `triage-answers` | opus | `answers recorded · clusters none` |
  | `triage-finish` | opus | `parts 1 · index plans/2026-11-25-slug-and-count/index.md · merged 593b560` |
  | `navigate` | haiku | `next: plan plans/2026-11-25-slug-and-count/index.md part 1` |
  | `plan` | opus | `planned plans/2026-11-25-slug-and-count/plan-1 · waves 1 · tasks low 2, medium 0, high 0` |
  | `status` | haiku | (the report) |

- The `triage-answers` prompt ends with the line `Answers: none`.
- Final report: `Run: 3 steps · ended by rail: steps 3 · …`; the Steps table has three rows (`triage-answers`,
  `triage-finish`, `plan`); `### Halts` `- none`; `### Next` `Continue:` with both forms.
- State (`T2.evidence.txt`): `main` at `593b560 Index slug-and-count`; branches `integration/slug-and-count`
  (`f9ccdbf`) and `plan/slug-and-count-p1` (`67d31e7`); `refs/wave-method/` empty; wave 1 `⬜` with tasks A
  (`slugify-module`, F1, low) and B (`count-words-module`, F2, low), both `After` `—`.

### T-copy · copy the planned state

```bash
git -C <scratch>/textkit worktree list            # integration-slug-and-count and slug-and-count-p1-plan, both clean
git -C <scratch>/textkit worktree remove <each>
cp -r <scratch>/textkit <scratch>/textkit-needs
```

- `git worktree list` in each repository names only itself. Both hold the same refs: `f9ccdbf`
  `integration/slug-and-count`, `593b560` `main`, `67d31e7` `plan/slug-and-count-p1`.

### T3 · task A needs a missing tool

Setup in `<scratch>/textkit-needs` ("P2 setup"): `git worktree add <scratch>/edit plan/slug-and-count-p1`; the `Needs`
cell of task A (the first task with `After` `—`) in `plans/2026-11-25-slug-and-count/plan-1/waves/w01.md` set to
``the `labelprint` command-line tool of a label printer``; commit `5ac3f72 rehearsal: task needs a missing tool`;
`git worktree remove <scratch>/edit`. `command -v labelprint` finds nothing, and the coordinator's own `which labelprint`
exits 1.

```bash
claude -p "/wave-auto plans/2026-11-25-slug-and-count/index.md" ...      # in <scratch>/textkit-needs
```

- Exit 0. Agent calls, in order:

  | Step | Model | Return |
  |---|---|---|
  | `navigate` (skip none) | haiku | `next: wave plans/2026-11-25-slug-and-count/plan-1 1` |
  | `wave` | sonnet | ``waiting A:low needs the `labelprint` command-line tool of a label printer; B:low`` |
  | `task` B | haiku | `task B: committed cf5b830` |
  | `navigate` (skip `plans/2026-11-25-slug-and-count/plan-1`) | haiku | `done` |
  | `status` | haiku | (the report) |

- **Tasks that ran: B only.** No `task` step for A; no `wave` step after B's task; no `Stop` line anywhere. The
  coordinator's text after launching B: `Task B is running. Task A will wait for the session fallback, which isn't
  available here because no session can be started.`
- Final report: `Run: 2 steps · ended by done · …`; Steps rows `wave` and `task` (`task B: committed cf5b830`). Halts:

  ```
  - plans/2026-11-25-slug-and-count/plan-1 — capability-missing (task A needs `labelprint`; no session can be started) — next: `/wave-run plans/2026-11-25-slug-and-count/plan-1 1 task A` · `$wave-run plans/2026-11-25-slug-and-count/plan-1 1 task A`, then `/wave-auto plans/2026-11-25-slug-and-count/index.md` · `$wave-auto plans/2026-11-25-slug-and-count/index.md`
  ```

- Wave file Execution on `plan/slug-and-count-p1` (commit `18ee16c Plan slug-and-count-p1: wave 1 waiting for task
  mode`) ends:

  ```
  Waiting: task mode A, B — next: /wave-run plans/2026-11-25-slug-and-count/plan-1 1 task A · $wave-run plans/2026-11-25-slug-and-count/plan-1 1 task A; /wave-run plans/2026-11-25-slug-and-count/plan-1 1 task B · $wave-run plans/2026-11-25-slug-and-count/plan-1 1 task B
  ```

- State (`T3.evidence.txt`): `refs/wave-method/` holds only `claims/integration/slug-and-count` (the waiting wave);
  `feat/slug-and-count-p1/F2-count-words-module` at `cf5b830`, `…/F1-slugify-module` at `f9ccdbf`; wave 1 `🔄`.

### T4 · the whole wave in the original repository

```bash
claude -p "/wave-auto plans/2026-11-25-slug-and-count/index.md" ...      # in <scratch>/textkit
```

- Exit 0. Agent calls, in order:

  | Step | Model | Return |
  |---|---|---|
  | `navigate` | haiku | `next: wave plans/2026-11-25-slug-and-count/plan-1 1` |
  | `wave` | sonnet | `waiting A:low; B:low` |
  | `task` A, `task` B (one message) | haiku | `task A: committed 6ed8fc0`, `task B: committed b1bf765` |
  | `wave` | sonnet | `wave 1 ✅ · merged F1, F2 · review none · blocked none` |
  | `navigate` | haiku | `done` |
  | `status` | haiku | (the report) |

- Final report: `Run: 4 steps · ended by done · …`; four Steps rows (`wave`, `task` B, `task` A, `wave`);
  `### Halts` `- none`; `### Next` `- none`.
- F1 `✅ merged` `a41969e`, F2 `✅ merged` `ed67310` in README "Features", both `Approved: auto`; both feature branches
  are ancestors of `integration/slug-and-count` (`014c8b1`); `main` still `593b560`; `refs/wave-method/` empty.
- The tracking branch has one "waiting for task mode" commit, `2f25b0c`; its waiting line names both forms for A and B,
  the same text as in T3.

## Results

### Expectations of the runs

| Expectation | Result | Evidence |
|---|---|---|
| T1: one `triage-ask` step | Pass | `T1.coord.txt`: one counted agent call, `step triage-ask · unit list` |
| T1: right after its progress line, in the same text, `Resume: /wave-auto <index path> · $wave-auto <index path>` | Finding | no `Resume:` line in any coordinator text of `T1.jsonl` (TF-1) |
| T1: `Run: 1 steps · ended by rail: steps 1` | Pass | `Run:` line of `T1.jsonl` |
| T1: the Status part has a block for the index as a triage in progress, with `Next:` `/wave-auto <index path>` in both forms | Pass | block quoted under T1 |
| T1: no `git worktree remove` or `git branch -d` suggested for the triage worktree or branch | Pass | neither appears in the final report of `T1.jsonl` |
| T2: no question to the user | Pass | `T2.coord.txt`: no question text; one call |
| T2: steps `triage-answers` (with `Answers: none`), `triage-finish`, `plan` | Pass | agent calls under T2; `Answers: none` is the prompt's last line |
| T2: `Run: 3 steps · ended by rail: steps 3` | Pass | `Run:` line of `T2.jsonl` |
| T2: the Steps table has three rows | Pass | final report of `T2.jsonl` |
| T-copy: both repositories hold the same branches | Pass | the same three refs in `textkit` and `textkit-needs` |
| T3: `wave` returns `waiting A:<tier> needs …; B:<tier>` | Pass | ``waiting A:low needs the `labelprint` … ; B:low`` (`T3.coord.txt`) |
| T3: a `task` step for B, launched before the unit halts, returns `committed …` | Pass | `task B: committed cf5b830`; the halt follows in the report only |
| T3: no `task` step for A | Pass | the only `task` prompt names `task B` |
| T3: no `Stop` line | Pass | no `Stop` in any coordinator text of `T3.jsonl` |
| T3: Halts lists the unit with `capability-missing` and `/wave-run <plan folder> 1 task A` in both forms, then `/wave-auto <index path>` | Pass | Halts line quoted under T3 |
| T3: no `wave` step after B's task | Pass | the call after B's task is `navigate` |
| T3: a later `navigate` returns `done` | Pass | second `navigate`, `skip plans/2026-11-25-slug-and-count/plan-1` → `done` |
| T3: `ended by done` | Pass | `Run: 2 steps · ended by done` |
| T3: the wave file's Execution ends with a `Waiting: task mode A, B — next: …` line with both forms for each ID | Pass | line quoted under T3, commit `18ee16c` |
| T3: record which tasks ran | Pass | B ran (`cf5b830`); A did not |
| T4: runs to the end, `ended by done` | Pass | `Run: 4 steps · ended by done` |
| T4: every feature `✅ merged` into `integration/<topic>` | Pass | F1 `a41969e`, F2 `ed67310`; both ancestors of `integration/slug-and-count` |
| T4: `Run: <n> steps` equals the rows of the Steps table and the agent calls of counted steps | Pass | 4 = 4 rows = 4 calls (`wave`, `task`, `task`, `wave`) |
| T4: every "waiting for task mode" commit has both forms for each ID | Pass | `2f25b0c`, the only one; line as under T3 |

### Report checks

Applied to T1, T2, T3 and T4, which all ended with a final report.

| Check | Run | Result | Evidence |
|---|---|---|---|
| 1 claim: no coordinator Bash call writes a file | T1, T2, T3, T4 | Pass | no `>`, `>>`, `tee`, `Out-File`, `Set-Content` or `Add-Content` in any `BASH:` line of `T1.coord.txt` to `T4.coord.txt`; the claim command prints the oid (`git hash-object -w` writes only the object) |
| 1 claim: the release has the oid as 40 literal hex characters | T1, T2, T3, T4 | Pass | `git update-ref -d refs/wave-method/claims/auto/slug-and-count 4cccdb3f…c478ef` (T1), `8d18599d…a8d8b4` (T2), `a24ef16f…003d66` (T3), `5c73121b…bda0c2ddef` (T4), each written out in full |
| 1 claim: `git for-each-ref refs/wave-method/claims/auto/` prints nothing after the run | T1, T2, T3, T4 | Pass | `T<n>.evidence.txt`; checked again after T4 in both repositories |
| 1 claim: the Status part names no `claims/auto` ref | T1, T2, T3, T4 | Pass | each Status part says `Coordinator claims: none` |
| 2 count: `Run: <n> steps` = Steps rows = counted agent calls | T1 | Pass | 1 = 1 = 1 (`triage-ask`) |
| 2 count | T2 | Pass | 3 = 3 = 3 (`triage-answers`, `triage-finish`, `plan`) |
| 2 count | T3 | Pass | 2 = 2 = 2 (`wave`, `task`) |
| 2 count | T4 | Pass | 4 = 4 = 4 |
| 3 template: `Run:`, `### Steps`, `### Halts`, `### Status`, `### Next`, the times line last | T1, T2, T3, T4 | Pass | final reports; the last line is `Started: … · Finished: …` in each; no coordinator command runs `python` or the tests |

### Findings

Nothing was changed in a skill.

- **TF-1 · no `Resume:` line after a `triage-ask` without questions.** `skills/wave-auto/SKILL.md`, "Start phase",
  item 2 (and "Resume"). Expected, right after the progress line of `triage-ask` and before anything else,
  `Resume: /wave-auto plans/2026-11-25-slug-and-count/index.md · $wave-auto plans/2026-11-25-slug-and-count/index.md`.
  Observed in T1 (coordinator `claude-sonnet-5-5`): after `triage-ask` returned `questions 0 · …` the coordinator ran
  `date +%H:%M`, then the claim command, and wrote no text until the final report; neither the progress line (an
  accepted limit) nor the `Resume:` line appeared. The line is tied to the progress line, so it is skipped together
  with it. The command reaches the user only through `### Next` and the Status block.

Observations, not judged:

- T2 dispatched `triage-answers` without a `navigate` before it, after reading the index header
  (`git show … | head -5`) besides "Open questions" (`skills/wave-auto/SKILL.md`, "Hard rules", item 2: it reads
  nothing of `plans/` but "Open questions"). The steps and their returns were right.
- In T3 the coordinator checked the `Needs` tool itself with `which labelprint` before launching B.

## Not verified

- The coordinator on an Opus-class model: every call here ran it on `claude-sonnet-5-5`.
- The `Resume:` line after a `triage-ask` that asks questions (this list gives `questions 0`).
- A halt of one unit while another unit of the same run goes on: the fixture has one unit.
- The resume of the halted wave in `textkit-needs` (task A would need `labelprint`).

## Repeat

```bash
S=$(mktemp -d); test -n "$S" || exit 1; mkdir -p "$S/calls" "$S/textkit/textkit" "$S/textkit/tests"
python -m venv "$S/venv" && "$S/venv/Scripts/python" -m pip install pytest      # venv/bin on Linux and macOS
cd "$S/textkit" && git init -q -b main
git config user.name rehearsal && git config user.email rehearsal@example.invalid
: > textkit/__init__.py
printf 'def test_import(): import textkit\n' > tests/test_smoke.py
printf 'textkit — small text helpers. Check: python -m pytest -q\n' > README.md
printf '__pycache__/\n.pytest_cache/\n' > .gitignore
git add -A && git commit -q -m "Seed textkit"
sh <working folder>/install.sh "$S/textkit" --no-codex
git add -A && git commit -q -m "Seed textkit with wave skills"

export PATH="$S/venv/Scripts:$PATH"
run() { n=$1; repo=$2; shift 2; (cd "$S/$repo" && MSYS_NO_PATHCONV=1 claude -p "$@" --output-format stream-json \
  --verbose --permission-mode auto --max-budget-usd <cap left> < /dev/null > "$S/calls/$n.jsonl"); }
run T1 textkit "/wave-auto steps 1 <the list above>"
run T2 textkit "/wave-auto steps 3 plans/<date>-<topic>/index.md"      # <topic> chosen by the triage (here slug-and-count)
# T-copy
git -C "$S/textkit" worktree list        # git worktree remove every clean worktree but the main one
cp -r "$S/textkit" "$S/textkit-needs"
# T3 setup, in textkit-needs: `git worktree add "$S/edit" plan/<topic>-p1`; in
#   plans/<date>-<topic>/plan-1/waves/w01.md set the Needs cell of task A to
#   "the `labelprint` command-line tool of a label printer"; commit "rehearsal: task needs a missing tool";
#   `git worktree remove "$S/edit"`; `command -v labelprint` must find nothing
run T3 textkit-needs "/wave-auto plans/<date>-<topic>/index.md"
run T4 textkit "/wave-auto plans/<date>-<topic>/index.md"
```

After each call: `git branch --list`, `git for-each-ref refs/wave-method/`, `git log --oneline -3 main`, the unit's
"Waves" and "Tasks" rows. From each stream: the events without `parent_tool_use_id` (the coordinator's text, shell
commands and agent calls with the `Coordinated run · step …` line of their prompts), the `message.model` of each
subagent's events, and the last `result` event's `result` and `total_cost_usd`. For T3 and T4:
`git show <commit>:plans/<date>-<topic>/plan-1/waves/w01.md | grep '^Waiting:'` for each commit of
`git log --grep='waiting for task mode' plan/<topic>-p1`.
