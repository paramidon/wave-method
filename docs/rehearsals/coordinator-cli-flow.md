# Rehearsal: wave-auto flow in the Claude Code CLI

2026-11-25 · Claude Code 2.1.326 · source checkout `ca9de6a` (the working folder before this record).

Second rehearsal of feature F1 (in-session coordinator `wave-auto`), the flow run: progress lines, claim order and
final report, a wave left waiting by the `steps` rail and its resume, tasks already committed, and an open problem that
is re-planned and fixed. Procedure: `solutions/P1-in-session-coordinator.md` of the plan, "Second rehearsal (tasks O,
P, Q)", "Task O — flow". The first CLI rehearsal is `coordinator-cli.md`.

Outcome: the pipeline did what the runs expect (rail, resume, `already committed`, open entry, re-plan, fix wave,
auto-approval, `done`, green merge). Six findings, F-1 to F-6: mostly what the coordinator prints and keeps still
differs from its skill.

## Setup

- Windows 11, Git Bash, Python 3.14.6, git 2.52.0 (`core.autocrlf=true`).
- Made `<scratch>` with `mktemp -d`, outside every repository. Fixture repository `<scratch>/textkit` as "Fixture
  (both)" says: `main`, local user `rehearsal` / `rehearsal@example.invalid`, commits `2a4a8c3 Seed textkit` and
  `e3fceb2 Seed textkit with wave skills`; `python -m pytest -q` → 1 passed.
- Virtual environment `<scratch>/venv` (`pip install pytest`, pytest 9.2.0), first on `PATH` in every call.
- Skills: `sh <working folder>/install.sh <scratch>/textkit --no-codex` (five skills).
- Every call, in `<scratch>/textkit`, with `MSYS_NO_PATHCONV=1`, in the background:
  `claude -p "<prompt>" --output-format stream-json --verbose --permission-mode auto --max-budget-usd <rest>
  < /dev/null`. No `--model`. The calls were started from the shell of a Claude Code desktop-app session and inherited
  its environment.
- **The coordinator ran on `claude-sonnet-5-5`** in every call (`system/init`), the CLI default here. The `wave-auto`
  description recommends an Opus-class model, and the first CLI rehearsal's coordinator ran on `claude-opus-5-5`.
- The account's `wave-method` plugin skills were listed next to the project ones; every step prompt named
  `<scratch>/textkit/.claude/skills`, and no tool call read a plugin copy.
- Saved per call: `<scratch>/calls/<run>.jsonl`, `.err`, `.exit`, `.cmd`, `.evidence.txt` (branches,
  `refs/wave-method/` with holder lines, `git log --oneline -3 main`, worktrees, plan README rows). O5 is `O5.txt`.
- Permission denials: none in any call.

### Interruption by the account usage limit

The first O3 call (saved as `O3-cut.*`) ended with exit 1: after its `wave` step returned `waiting A:low; B:medium`,
the coordinator got `You've hit your 5-hour limit` (a `rate_limit_event` with `rateLimitType: five_hour`,
`status: rejected`) and printed no `wave` line, no release and no final report. The rehearsal session itself was cut
off too and continued after the limit reset. It left the wave 🔄 with its waiting line, the integration claim marked
waiting, and the coordinator claim `... 2026-11-25 19:00 run 91417c6b` still held.

To repeat O3 from the state O2 left (a copy of the cut state is in `<scratch>/snap-O3-cut`), by hand in the scratch
repository: deleted both refs under `refs/wave-method/claims/`, removed the two feature worktrees, deleted the two
`feat/textkit-words-p1/*` branches (no commits of their own) and reset `plan/textkit-words-p1` from `65c2f2a` to
`b917cc1`. The resulting branches, refs and worktrees matched `O2.evidence.txt`. O3 below is the repeated call.

### Cost

| Call | Exit | Duration | USD of this call |
|---|---|---|---|
| O1 | 0 | 69 s | 0.6722 |
| O2 | 0 | 277 s | 1.6403 |
| O3-cut | 1 | 80 s | 0.5225 |
| O3 | 0 | 131 s | 0.6597 |
| O4 | 0 | 624 s | 3.1089 |
| **Sum** | | | **6.60** (cap 12) |

A `--continue` call reports the session's total: O2's last `total_cost_usd` is 2.3125 and includes O1's 0.6722, so
the table shows the difference. Adding the raw values of O1 and O2 would count O1 twice.

### Models seen per step

The model of the coordinator's agent call, and the model of the subagent's messages in the stream (they agreed in
every call).

| Step | Runs | Model |
|---|---|---|
| coordinator | all | `claude-sonnet-5-5` |
| `triage-ask`, `triage-answers`, `triage-finish`, `plan` | O1, O2 | `opus` → `claude-opus-5-5` |
| `re-plan` | O4 | `opus` → `claude-opus-5-5` |
| `wave` and its resumes | O3-cut, O3, O4 | `sonnet` → `claude-sonnet-5-5` |
| `task`, low (A, C, D) | O4 | `haiku` → `claude-haiku-5-5` |
| `task`, medium (B) | O4 | `sonnet` → `claude-sonnet-5-5` |
| `navigate`, `status` | O2, O3-cut, O3, O4 | `haiku` → `claude-haiku-5-5` |
| O-hand (no call) | by hand | `claude-sonnet-5-5` |

## Runs

The list (one argument, verbatim) is that of "Fixture (both)". The triage chose the topic `textkit-words`, so the
index is `plans/2026-11-25-textkit-words/index.md` and the plan slug `textkit-words-p1`.

### O1 · start from the list

```bash
claude -p "/wave-auto steps 4 <list>" ...
```

- Exit 0. One agent call: `step triage-ask · unit list`, model `opus`.
- Coordinator text: `18:53 · triage-ask · list → questions 5 · index plans/2026-11-25-textkit-words/index.md`, the
  resume command in both forms, then Q1 to Q5 (Q4 and Q5 are about item 3: how many top words, format and tie order).
- `O1.evidence.txt`: branch `+ triage/textkit-words`; `refs/wave-method/claims/auto/textkit-words` with holder
  `wave-auto plans/2026-11-25-textkit-words/index.md 2026-11-25 18:53 run ad4e9185`; `main` at `e3fceb2`.

### O2 · answer, rail ends the run

```bash
claude -p "Top 10 words, most frequent first." --continue ...
```

- Exit 0. Agent calls: `triage-answers`, `triage-finish`, `navigate`, `plan`, `status`.
- Progress lines in the coordinator's text:

  ```
  18:54 · triage-answers · plans/2026-11-25-textkit-words/index.md → answers recorded · clusters none
  18:55 · triage-finish · plans/2026-11-25-textkit-words/index.md → parts 1 · index plans/2026-11-25-textkit-words/index.md · merged d461b66
  18:56 · navigate · plans/2026-11-25-textkit-words/index.md → next: plan plans/2026-11-25-textkit-words/index.md part 1
  ```

- **No line for `plan`.** After its return the coordinator ran `date +%H:%M; ... git update-ref -d <claim>` in one
  command (`O2.jsonl`, line 198), wrote no text and called `status` (finding F-1).
- Final report: `Run: 4 steps · ended by rail: steps 4`; Steps has four rows, `plan` at 18:58 with
  `planned plans/2026-11-25-textkit-words/plan-1 · waves 1 · tasks low 1, medium 1, high 0`; Halts `none`;
  `### Next` is the `Continue:` line; last line `Started: 2026-11-25 18:52 · Finished: 2026-11-25 18:58 (6 min)`.
- `O2.evidence.txt`: no ref under `refs/wave-method/`; `main` at `d461b66 Index textkit-words`;
  `plan/textkit-words-p1` at `b917cc1`, `integration/textkit-words` at `2e68326`; wave 1 ⬜ with A (low) and B (medium).
- Coordinator context at its last request: 86,330 tokens (75,785 at the end of O1).

### O3 · one wave step, rail leaves the wave waiting

```bash
claude -p "/wave-auto steps 1 plans/2026-11-25-textkit-words/index.md" ...   # new session
```

- Exit 0 (repeated call, see "Interruption"). Agent calls: `navigate`, `wave` (`sonnet`), `status`; no `task`.
- `navigate` returned `next: wave plans/2026-11-25-textkit-words/plan-1 1`. The coordinator ran `date +%H:%M`
  (20:07) and called `wave` **without writing the `navigate` line** (`O3.jsonl`, lines 42 to 55; finding F-1).
- `20:08 · wave · plans/2026-11-25-textkit-words/plan-1 → waiting A:low; B:medium`, followed in the same message by
  `The steps rail (1) is reached, so the run ends here. I'm releasing the claim and running the status step.`
  (finding F-3).
- Claim: taken with `echo $token > /tmp/wa_token; ... echo $oid > /tmp/wa_oid; git update-ref ...` and released with
  `git update-ref -d <ref> "$(cat /tmp/wa_oid)"` (finding F-4). The release ran before the `status` call.
- Final report: `Run: 1 steps · ended by rail: steps 1`, one Steps row, Halts `none`, `Continue:` line.
- `O3.evidence.txt`: `plan/textkit-words-p1` at `3c966a3 ... wave 1 waiting for task mode`; README wave 1
  `🔄 since 2026-11-25 20:08`; Execution ends `Waiting: task mode A, B — next: ...`; the only ref is
  `refs/wave-method/claims/integration/textkit-words`, holder `textkit-words-p1 wave 1 waiting 2026-11-25 20:08 run
  36c47219`; feature worktrees `textkit-words-p1-F1` and `-F2` at `2e68326`.
- The commands in that waiting line are in the Claude Code form only (finding F-5).

### O-hand · the two tasks by hand

- The waiting line names A (low, F1) and B (medium, F2); no `high` task. Both are direct tasks in their feature
  worktrees. Each was written from its prompt in `waves/w01.md`; `python -m pytest -q` → 7 passed (F1), 16 passed (F2).
- Commits: `0861755 textkit-words-p1 F1 / A: add slugify` and `e6ee657 textkit-words-p1 F2 / B: add count_words and the
  top command`, each with the `Done:`/`Try:`/`Not checked:`/`Problems:` paragraph and the trailer
  `Wave-Model: claude-sonnet-5-5`.
- Neither feature had a task left for a later launch group, so the problem went to the first ID, A; no task is skipped:
  `**[wave 1 / task A / feature F1] a missing argument raises AttributeError instead of a ValueError with a message** —
  where: textkit/slug.py:6; expected / got: ValueError / AttributeError; proposal: check the argument, add a test`.
  B has `Problems: none`. `slugify(None)` indeed raised `AttributeError`.

### O4 · resume, open entry, re-plan, fix wave

```bash
claude -p "/wave-auto plans/2026-11-25-textkit-words/index.md" ...           # new session
```

- Exit 0, one process, 15 `result` events (the coordinator ended its turn while subagents ran and was re-invoked).
- Progress lines, each after its step returned and a `date +%H:%M` call, before the next step:

  ```
  20:11 · navigate · plans/2026-11-25-textkit-words/index.md → next: tasks plans/2026-11-25-textkit-words/plan-1 1 A:low; B:medium
  20:11 · task · A → task A: already committed 0861755
  20:11 · task · B → task B: already committed e6ee657
  20:13 · wave · plans/2026-11-25-textkit-words/plan-1 → wave 1 ⚠️ · merged F2 · review none · blocked F1
  20:13 · navigate · plans/2026-11-25-textkit-words/index.md → next: re-plan plans/2026-11-25-textkit-words/plan-1
  20:14 · re-plan · plans/2026-11-25-textkit-words/plan-1 → re-planned plans/2026-11-25-textkit-words/plan-1 · new waves 2 · escalated none · held none
  20:15 · navigate · plans/2026-11-25-textkit-words/index.md → next: wave plans/2026-11-25-textkit-words/plan-1 2
  20:16 · wave · plans/2026-11-25-textkit-words/plan-1 → waiting C:low
  20:16 · task · C → task C: committed 51f12fc
  20:17 · wave · plans/2026-11-25-textkit-words/plan-1 → waiting D:low
  20:18 · task · D → task D: committed e04afbb
  20:19 · wave · plans/2026-11-25-textkit-words/plan-1 → wave 2 ✅ · merged F1 · review none · blocked none
  20:19 · navigate · plans/2026-11-25-textkit-words/index.md → done
  ```

  The `task` lines carry the task ID where the unit (the plan folder) belongs (finding F-2).
- Other text of the coordinator, besides the lines that say it waits (finding F-3): `Claim taken (oid 7f6ce88, token
  d93d7e64). Navigating.`, `Dispatching the two tasks in parallel.`, `Both tasks are committed. Resuming the wave
  step.`, `Navigating again.`, `Dispatching the re-plan (high tier).`, `Claim released. Running the status step.`
- Wave 1 resume (`2748bf8`): `problems.md` has `I1 ... status: open`; F1 `⚠️ blocked I1`, wave 1 `⚠️ I1`, F2
  `👀 review`, then auto-approved: `08d1ce1`.
- Re-plan (`f0b9e20`): README `Re-plans:` `I1 → P4; new C, D in wave 2 · fixes: F1 (I1)`; wave 2 has C (low) and D
  (low, after C), so the one gap became two tasks.
- Wave 2: C `51f12fc`, D `e04afbb` (both `Wave-Model: claude-haiku-5-5`), F1 auto-approved: `c1a17a6`; I1 moved to
  "Closed problems": `fixed in 51f12fc (task C), verified by task D on e04afbb`; wave 1 `✅ (I1 fixed by C, D, wave 2)`.
- Release: `git update-ref -d <ref> 7f6ce88...` after the last `navigate`, before `status`.
- Final report: **`Run: 6 steps`** · `ended by done`, while its Steps table has **nine** rows: A, B, `wave`,
  `re-plan`, `wave`, C, `wave`, D, `wave` (finding F-6). Halts `none`; status: F1 and F2 `✅ merged` (`c1a17a6`,
  `08d1ce1`), waves `1 ✅ · 2 ✅`; `### Next` `- none`; last line
  `Started: 2026-11-25 20:10 · Finished: 2026-11-25 20:20 (10 min)`.
- `O4.evidence.txt`: no ref under `refs/wave-method/`; `main` still `d461b66`; `integration/textkit-words` at
  `3a2aa9a`; the feature worktrees are gone.
- Coordinator context at its last request: 102,480 tokens.

### O5 · merge and test

```bash
cd <scratch>/textkit
git merge --no-ff integration/textkit-words -m "Merge integration/textkit-words"
python -m pytest -q
```

- Merge commit `b37fb06`; `24 passed in 0.24s`. Beyond the procedure: `slugify(None)` now raises
  `ValueError: slugify() expects a str, got NoneType`. (The first line of `O5.txt`, `fatal: Needed a single
  revision`, comes from a logging command of the rehearsal, not from the procedure.)

## Results

| Expectation | Result | Evidence |
|---|---|---|
| O1: one `triage-ask` step | Pass | `O1.jsonl`: one agent call, `step triage-ask · unit list` |
| O1: at least one question | Pass | five questions in the result text, Q4 and Q5 about item 3 |
| O1: claim and `triage/<topic>` exist | Pass | `O1.evidence.txt`: `+ triage/textkit-words`, `73ac662... refs/wave-method/claims/auto/textkit-words` |
| O2: steps `triage-answers`, `triage-finish`, `plan` | Pass | three agent calls in `O2.jsonl`; Steps table rows |
| O2: `ended by rail: steps 4` | Pass | `Run: 4 steps · ended by rail: steps 4` |
| O2: progress lines for all of them and for `navigate` | Finding | lines for `triage-answers`, `triage-finish`, `navigate`; none for `plan` (`O2.jsonl` lines 195 to 214; F-1) |
| O3: one `wave` step returning `waiting …` | Pass | `waiting A:low; B:medium` (also in `O3-cut.jsonl`) |
| O3: no `task` step | Pass | agent calls of `O3.jsonl`: `navigate`, `wave`, `status` |
| O3: `ended by rail: steps 1` | Pass | `Run: 1 steps · ended by rail: steps 1` (repeated call; the first one was cut by the usage limit) |
| O3: the wave stays 🔄 with its `Waiting: task mode` line | Pass | `3c966a3`; `O3.evidence.txt`: `🔄 since 2026-11-25 20:08` |
| O3: the integration claim holds a waiting line | Pass | `textkit-words-p1 wave 1 waiting 2026-11-25 20:08 run 36c47219` |
| O-hand: every task of the waiting line has its commit | Pass | `0861755` (A), `e6ee657` (B); `O-hand.evidence.txt` |
| O4: `next: tasks …` | Pass | `next: tasks plans/2026-11-25-textkit-words/plan-1 1 A:low; B:medium` |
| O4: each `task` step returns `already committed <hash>` | Pass | `task A: already committed 0861755`, `task B: already committed e6ee657`; no new commit |
| O4: the resume records the `Problems:` line as an open entry and blocks its feature | Pass | `2748bf8`: `I1 ... status: open`, F1 `⚠️ blocked I1` |
| O4: a later `navigate` returns `next: re-plan <unit>` | Pass | `next: re-plan plans/2026-11-25-textkit-words/plan-1` |
| O4: the `re-plan` step returns `re-planned …` | Pass | `re-planned ... · new waves 2 · escalated none · held none`; `f0b9e20` |
| O4: its new wave runs | Pass | wave 2: `51f12fc` (C), `e04afbb` (D), `wave 2 ✅` |
| O4: every feature ends `✅ merged` into `integration/<topic>` | Pass | F1 `c1a17a6`, F2 `08d1ce1`; `main` unchanged |
| O4: `ended by done` | Pass | `Run: 6 steps · ended by done` (the count is wrong, see below) |
| O5: `git merge --no-ff integration/<topic>`, `python -m pytest -q` green | Pass | `O5.txt`: `b37fb06`, `24 passed` |
| Report check 1 (progress lines), O2 | Finding | no line for `plan` (F-1) |
| Report check 1, O3 | Finding | no line for `navigate`; the `wave` line is right (F-1) |
| Report check 1, O4 | Finding | a line with a clock command for all 9 counted steps and 4 `navigate`; the four `task` lines name the task ID instead of the unit (F-2) |
| Report check 2 (no `claims/auto` ref or note in Status), O2, O3, O4 | Pass | Status parts of the three final reports; the release precedes the `status` call (`O2.jsonl` 198, `O3.jsonl` 104, `O4.jsonl` 731) |
| Report check 3 (template; `Next`; nothing after the times line; no run of the project), O2, O3, O4 | Pass | final texts: the five parts, `Continue:` (O2, O3) or `- none` (O4); `status` copied verbatim; no coordinator command runs `python`, `pytest` or the project |
| Report content: `Run: <n> steps` counts the steps of the Steps table, O4 | Finding | `Run: 6 steps` above nine rows (F-6); O2 and O3 count right |
| `wave-auto` hard rule: the coordinator writes only what the skill names | Finding | `O3.jsonl` line 102, six lines of `O4.jsonl` (F-3); O1 and O2 are clean |
| `wave-auto` hard rule: the coordinator changes no file | Finding | `/tmp/wa_token`, `/tmp/wa_oid` in O3 (F-4) |
| Commands are given in both forms (`layout.md`, "Commands") | Finding | waiting line of `3c966a3` (F-5) |

The report checks do not apply to O1, which ends with the questions, nor to the cut O3 call.

### Findings

- **F-1 · a step without its progress line** (O2 `plan`, O3 `navigate`). Expected: every counted step and every
  `navigate` gets `<HH:MM> · <step> · <unit> → <return line>` as soon as it returns (`wave-auto/SKILL.md`, "Hard
  rules" and "Loop", "Progress lines"). Observed: the clock was read and the next action started with no text. In O2
  the skipped line belongs to the last step before the rail (the clock command was joined with the claim release); in
  O3 to a `navigate` followed at once by a dispatch.
- **F-2 · `task` lines name the task instead of the unit** (O4, four lines). Expected `<unit>` = the plan folder
  ("Step prompt", `<unit>`); observed `· task · A →`. "Progress lines" gives steps launched together one line each
  and says nothing of how they differ; the return line already names the task. The Steps table has the plan folder.
- **F-3 · commentary between the progress lines** (O3, O4; two lines of the cut O3 call too). Expected: "It writes
  the user only what this skill names" (`wave-auto/SKILL.md`, "Hard rules", last bullet). Observed sentences that
  announce the next action, the claim's oid and token, and the rail.
- **F-4 · the coordinator keeps its claim oid in files** (O3). Expected: "The coordinator changes no file"
  ("Hard rules", first bullet). Observed `/tmp/wa_token` and `/tmp/wa_oid`. Shell state does not survive between
  commands, `layout.md`, "Target claim", says "Keep the oid" without saying where, and the names are fixed: two
  coordinators on one machine would overwrite each other's oid, the release (which checks the old value) would fail
  and the claim would stay. The other calls kept the oid in the conversation.
- **F-5 · waiting line in one command form** (O3). Expected both forms (`wave-run/task-mode.md`, "Coordinator";
  `layout.md`, "Commands"). `3c966a3` has `/wave-run` only, and the status report copies it as "Last stop". The cut O3
  call (`65c2f2a`) and wave 2 (`5a25d72`, `0edd6b9`) gave both forms.
- **F-6 · wrong step count** (O4). Expected `Run: <n> steps` to be the counted steps, as in the Steps table
  (`wave-auto/SKILL.md`, "End of the run", "Rails"); observed 6 for 9. The skill does not say that the count is the
  table's row count, and the same count drives the `steps` rail.

## Not verified

- Whether the findings depend on the coordinator's model: every coordinator here ran on `claude-sonnet-5-5`.
- How often each finding happens: one run of each step of the procedure.
- A `steps` rail that falls between the tasks of a launch group, or between a `task` and its resume.
- A task step that does the work of wave 1 itself: A and B were done by hand (C and D were real `task` steps).
- Re-plan escalation (a second re-plan of one feature) and skipped tasks.

## Repeat

```bash
S=$(mktemp -d); mkdir -p "$S/calls" "$S/textkit/textkit" "$S/textkit/tests"
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

export PATH="$S/venv/Scripts:$PATH" MSYS_NO_PATHCONV=1
# on Windows give python Windows paths (cygpath -m "$S"): MSYS_NO_PATHCONV stops the conversion
run() { n=$1; shift; claude -p "$@" --output-format stream-json --verbose --permission-mode auto \
  --max-budget-usd <cap left> < /dev/null > "$S/calls/$n.jsonl"; }
run O1 "/wave-auto steps 4 <the list of the fixture>"
run O2 "Top 10 words, most frequent first." --continue
run O3 "/wave-auto steps 1 plans/<date>-<topic>/index.md"
# O-hand: in each worktree of the waiting line, write the task of waves/w01.md, run python -m pytest -q, then
git add <the task's files>
git commit -m "<slug> <F-ID> / <ID>: <short>" -m "Done: …
Try: …
Not checked: none
Problems: <none, or one entry for one task>" -m "Wave-Model: <exact model ID>"
run O4 "/wave-auto plans/<date>-<topic>/index.md"
cd "$S/textkit" && git merge --no-ff integration/<topic> && python -m pytest -q
```

After each call: `git branch --list`, `git for-each-ref refs/wave-method/`, `git log --oneline -3 main`, the plan
README's "Waves" and "Tasks" rows on `plan/<slug>`; from the stream, the events without `parent_tool_use_id` (texts,
shell commands, agent calls with their `model`) and the last `result` event. A `--continue` call's `total_cost_usd`
includes the earlier calls of its session. The `<topic>` is chosen by the triage, so it can differ between repetitions.
