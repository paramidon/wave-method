# Rehearsal: the ways a wave-auto run stops short (Claude Code CLI)

2026-11-25 · Claude Code 2.1.326 · source commit `ca9de6a` (the working folder before this record).

Task P of the second rehearsal of feature F1: a task whose tool is missing, a halted unit, the `until` rail, and a
session killed in the middle of a step and resumed by a new one, the last without the account-level plugin.

Outcome: every expectation of runs P1 to P5b holds (stop, halt, rail, takeover and resume work). The report checks and
some rules of the coordinator's output do not hold in every run (findings PF-1 to PF-8).

## Setup

- `<scratch>` made with `mktemp -d` outside every repository. Per call: `<scratch>/calls/<run>.jsonl` (stream), `.err`,
  `.exit`, `.start`, `.end` and `<run>.evidence.txt` (`git branch --list`, `git for-each-ref refs/wave-method/`,
  `git log --oneline -3 main`, the unit's README "Waves" and "Tasks").
- Fixture `<scratch>/textkit` on `main`, local user `rehearsal` / `rehearsal@example.invalid`, with
  `textkit/__init__.py`, `tests/test_smoke.py`, `README.md` and `.gitignore` as in the first rehearsal
  (`coordinator-cli.md`); commits `Seed textkit` and `Seed textkit with wave skills`.
- Skills: `sh <working folder>/install.sh <scratch>/textkit --no-codex`. `<scratch>/venv`: Python 3.14, pytest 9.2.0,
  first on `PATH`.
- Calls: `claude -p "<prompt>" --output-format stream-json --verbose --permission-mode auto --max-budget-usd <rest>`,
  stdin from `/dev/null`, `MSYS_NO_PATHCONV=1`, no `--model`. P5b adds `--setting-sources project,local`. The calls
  were started from a shell of a desktop-app session and inherited its environment variables.
- The coordinator ran on `claude-sonnet-5-5` in every `system/init` (the CLI default here; the first rehearsal's
  default was `claude-opus-5-5`). `wave-auto` recommends an Opus-class model for it, so the findings about the
  coordinator's output are findings for a Sonnet coordinator.
- Except in P5b, every `system/init` also listed the four skills of the account-level `wave-method` plugin.
- List (one argument):

  ```
  1. Add textkit/slug.py with slugify(text): ASCII letters and digits only, lower case, words joined by "-"; every other character separates words. 2. Add textkit/count.py with count_words(text) returning a dict word -> count; a word is a run of ASCII letters and digits, compared in lower case.
  ```

- Permission denials: none in any call that has a result event.

### Interruptions

- **Account usage limit, during the first P2 call** (five-hour window). The harness put
  `[Usage limit reached; a short grace allowance remains, …]` into the coordinator's session after task B returned. The
  coordinator released its claim, skipped `status` and ended with `ended by usage limit`. The call could not judge P2,
  so P2 was repeated after the reset on a fresh copy of the planned state (run "P2"). The limit also cut off the session
  that drove this rehearsal while it waited; no other call was running then.
- **First P5a call, discarded.** The driver's kill script ran `taskkill //F //T //PID …` with `MSYS_NO_PATHCONV=1`
  exported, so `taskkill` got `//F` literally (`Invalid argument/option - '//F'`). The call went on: both tasks
  committed and the wave resume started before it was killed by hand (same PID, 84 s late). This was an error of the
  driver, not of a skill. P5a was repeated in `<scratch>/textkit-cut`, a copy of the planned state, with the kill run
  without `MSYS_NO_PATHCONV`.

### Cost

| Call | Files | Time | USD |
|---|---|---|---|
| P1 | `P1.*` | 4 min 56 s | 2.33 |
| P2, cut by the usage limit | `P2.*` | 2 min 18 s | 0.60 |
| P2 | `P2r.*` | 2 min 42 s | 0.72 |
| P3 | `P3.*` | 1 min 21 s | 0.28 |
| P4 | `P4.*` | 1 min 19 s | 0.26 |
| P5a, discarded | `P5a.*` | 3 min 31 s | about 1.0 (estimate) |
| P5a | `P5a2.*` | 1 min 55 s | about 0.65 (estimate) |
| P5b, question | `P5b1.*` | 18 s | 0.17 |
| P5b, takeover and resume | `P5b2.*` | 4 min 24 s | 0.85 |

Summed: **about 6.9 USD** of the 12 USD cap (5.20 USD from the result events, about 1.65 USD for the two killed calls).
A killed call has no result event; its cost is estimated from the token usage in its stream, at per-token rates fitted
to the result events of other calls (its output tokens are only partly in the stream).

## Runs

### P1 · plan the list, stop at the rail

```bash
claude -p "/wave-auto steps 4 <list>" ...      # in <scratch>/textkit
```

- Exit 0. No question (`questions 0`). Steps: `triage-ask` (opus), `triage-answers` (opus), `triage-finish` (opus),
  `plan` (opus), plus `navigate` and `status` (haiku).
- Final report: `Run: 4 steps · ended by rail: steps 4`, `### Halts` `- none`, `### Next` with
  ``Continue: `/wave-auto plans/2026-11-25-slug-word-count/index.md` · `$wave-auto …` ``. Last Steps row:
  `planned plans/2026-11-25-slug-word-count/plan-1 · waves 1 · tasks low 2, medium 0, high 0`.
- State: `main` at `d540ab1 Index slug-word-count`; branches `integration/slug-word-count`, `plan/slug-word-count-p1`;
  `refs/wave-method/` empty; README "Waves" `1 … ⬜`, tasks A (`slugify`, low) and B (`count_words`, low), both with
  `After` `—` and `Needs` `—`.
- Progress lines in the coordinator's text: only `triage-answers` (18:53) and `navigate` (18:55). None for `triage-ask`,
  `triage-finish` and `plan`, and no resume command after `triage-ask` (PF-1, PF-3).

### P-copy · copy the planned state

```bash
git -C <scratch>/textkit worktree list            # two worktrees besides the main one, both clean
git -C <scratch>/textkit worktree remove <each>
cp -r <scratch>/textkit <scratch>/textkit-needs
cp -r <scratch>/textkit <scratch>/textkit-halt
```

- Each of the three repositories: `git worktree list` names only itself; the same refs (`000e62d`
  `integration/slug-word-count`, `d540ab1` `main`, `85a1db3` `plan/slug-word-count-p1`).
- For the repeat of P2 the same copy and setup were made once more (`<scratch>/textkit-needs2`).

### P2 · a task whose tool is missing

Setup in `<scratch>/textkit-needs2`: on `plan/slug-word-count-p1`, the `Needs` cell of task A in `waves/w01.md` set to
``the `labelprint` command-line tool of a label printer``; commit `rehearsal: task needs a missing tool`.
`labelprint` is not on `PATH`.

```bash
claude -p "/wave-auto plans/2026-11-25-slug-word-count/index.md" ...
```

- Exit 0. `navigate` → `next: wave plans/2026-11-25-slug-word-count/plan-1 1`. `wave` (sonnet) →
  ``waiting A:low needs the `labelprint` command-line tool of a label printer; B:low``.
- **Tasks that ran: none.** No `task` step for A and none for B. The coordinator's reasoning summary: "I'm halting that
  unit as capability-missing and ending the run." (PF-5)
- First line of the report: ``Stop capability-missing: task A of plan-1 needs the `labelprint` command-line tool, which
  this session lacks and cannot start a session to get — next: run task A by hand, then resume.`` Then
  `Run: 1 steps · ended by stop capability-missing` (PF-4).
- Halts: ``plans/2026-11-25-slug-word-count/plan-1 — capability-missing: task A needs `labelprint`, and no session can
  be started — next: `/wave-run plans/2026-11-25-slug-word-count/plan-1 1 task A` · `$wave-run … 1 task A`, then
  `/wave-auto plans/2026-11-25-slug-word-count/index.md` · `$wave-auto …` ``.
- State: `refs/wave-method/` holds only `claims/integration/slug-word-count`
  (`slug-word-count-p1 wave 1 waiting …`); wave 1 `🔄` with `Waiting: task mode A, B`; both feature branches still at
  `000e62d`.
- No progress line for `wave` (PF-1). The Status part lacks a "Notes on the run" block that the `status` step returned
  (PF-7).

**The first P2 call** (`<scratch>/textkit-needs`, cut by the usage limit): the same `wave` return, no `task` step for A,
one `task` step for B (haiku), which returned `task B: committed be59503`. So task B ran in one of the two calls. Its
report also listed the unit under Halts with `capability-missing` and the same commands, and `refs/wave-method/claims/auto/`
was empty afterwards.

### P3 · a navigator `halt` line

Setup in `<scratch>/textkit-halt`: README "Waves" row of wave 1 set to `🔄 since 2026-01-01 00:00`; commit
`rehearsal: a wave left running` (`59504a2` on `plan/slug-word-count-p1`).

```bash
claude -p "/wave-auto plans/2026-11-25-slug-word-count/index.md" ...
```

- Exit 0. `navigate` returned:

  ```
  halt plans/2026-11-25-slug-word-count/plan-1: wave 1 is 🔄 since 2026-01-01 00:00 with no task-mode wait — next: wait for the run that holds it, or release the lock (wave-plan/layout.md, "Running waves")
  done
  ```

- Report: `Run: 0 steps · ended by done`; Halts lists the unit with that reason and `next:` part.
- State: `plan/slug-word-count-p1` still at `59504a2`; `refs/wave-method/` empty.
- No progress line for `navigate` (PF-1). The Status part lacks the `status` report's own `Started … Finished` line
  (PF-7). The coordinator ran its closing clock command while `status` was still running (result `20:10`) and printed
  `Finished: 2026-11-25 20:11` (PF-8).

### P4 · the `until` rail

```bash
claude -p "/wave-auto until 2026-01-01 00:00 plans/2026-11-25-slug-word-count/index.md" ...   # textkit-halt
```

- Exit 0. One agent call only, `status` (haiku); no `navigate` and no other step.
- `Run: 0 steps · ended by rail: until 2026-01-01 00:00`; `refs/wave-method/` empty; the plan branch unchanged.
- `### Next`: ``Continue: `/wave-auto until <later time> plans/2026-11-25-slug-word-count/index.md` · `$wave-auto until
  <later time> …` (the `until` time given was already in the past, so pick a later one or omit it)`` (PF-6).

### P5a · kill the session during its first task step

In `<scratch>/textkit-cut` (the planned state; see "Interruptions"):

```bash
claude -p "/wave-auto plans/2026-11-25-slug-word-count/index.md" ... &     # watch the stream for "step task ·"
taskkill //F //T //PID "$(cat /proc/$!/winpid)"                            # 20 s later, without MSYS_NO_PATHCONV
```

- `navigate`, then `wave` → `waiting A:low; B:low`, then the `task` steps A and B (haiku) launched together. Killed 21 s
  after they appeared; `taskkill` exit 0, call exit 1. Of the 5 processes of the call's tree listed before the kill,
  none was left, and no process named the repository in its command line.
- **What stayed:** `claims/auto/slug-word-count`
  (`wave-auto plans/2026-11-25-slug-word-count/index.md 2026-11-25 20:17 run 18ad073e`) and
  `claims/integration/slug-word-count` (`slug-word-count-p1 wave 1 waiting …`); wave 1 `🔄 since 2026-11-25 20:18` with
  `Waiting: task mode A, B — next: …`; tasks A and B `🔄`.
- **What the killed tasks left behind:** nothing of their own. By the stream they had only read skills and plan files.
  The prepared worktrees `slug-word-count-p1-F1` and `…-F2` were at `000e62d`, with no changed or untracked file (only an
  ignored `.pytest_cache/`), and the feature branches had no task commit.

### P5b · a new session without the plugin takes over

```bash
claude -p "/wave-auto plans/2026-11-25-slug-word-count/index.md" ... --setting-sources project,local
claude -p "Yes, it is gone." --continue ... --setting-sources project,local
```

- Both `system/init` events list the skills `wave-auto`, `wave-plan`, `wave-run`, `wave-status`, `wave-triage` and no
  `wave-method:` skill; no `wave-method` plugin.
- First call (exit 0, no agent call): ``The coordinator claim is held by another run: `wave-auto
  plans/2026-11-25-slug-word-count/index.md 2026-11-25 20:17 run 18ad073e` … Is its holder gone, meaning no other
  `wave-auto` session is running for this index? If yes, I'll take over the claim and continue. If no, I'll stop with
  `wave-running`.`` Refs unchanged.
- Second call (exit 0): takeover by `git update-ref <ref> <new> <held>`. Steps:

  | Line | Model | Return |
  |---|---|---|
  | `navigate` | haiku | `next: tasks plans/2026-11-25-slug-word-count/plan-1 1 A:low; B:low` |
  | `task` A | haiku | `task A: committed d9f4a56` |
  | `task` B | haiku | `task B: committed 665e5ba` |
  | `wave` | sonnet | `wave 1 ✅ · merged F1, F2 · review none · blocked none` |
  | `navigate` | haiku | `done` |

- **Tasks that ran: A and B, both anew** (`committed`, not `already committed`: the killed call had committed nothing).
- `Run: 3 steps · ended by done`; F1 `✅ merged` `fa5d6f7`, F2 `✅ merged` `64dec83`, both `Approved: auto`, both
  ancestors of `integration/slug-word-count`; `main` still `d540ab1`; `refs/wave-method/` empty; the feature worktrees
  removed. Wave file Execution: `Resumed after task mode; claim taken over.`, trailers `Wave-Model:
  claude-haiku-5-5`, `F1 -> 7 passed`, `F2 -> 6 passed`.
- The `status` report inside the final report ends `Finished: 2026-11-25 20:26`; its only clock command had returned
  `20:24`, and the whole call had ended at 20:25 (PF-8).

## Results

### Expectations of the runs

| Expectation | Result | Evidence |
|---|---|---|
| P1: ends with the plan written and wave 1 ⬜ | Pass | `P1.evidence.txt`: `plan/slug-word-count-p1`, "Waves" `1 … ⬜` |
| P1: `ended by rail: steps 4` | Pass | final report of `P1.jsonl`; no question came first |
| P-copy: `textkit-needs` and `textkit-halt` hold the same branches | Pass | the same three refs in all three; each `git worktree list` names only itself |
| P2: `wave` returns `waiting … needs …` | Pass | ``waiting A:low needs the `labelprint` … ; B:low`` (`P2r.jsonl`, and `P2.jsonl`) |
| P2: no `task` step for that ID | Pass | no agent call for task A in `P2r.jsonl` or `P2.jsonl` |
| P2: Halts: the unit, `capability-missing`, with `/wave-run <plan folder> 1 task <ID>` in both forms and `/wave-auto` again | Pass | Halts line quoted under P2; how the run ended is PF-4 |
| P2: no `claims/auto` ref left | Pass | `P2r.evidence.txt`: only `claims/integration/slug-word-count` |
| P2: record whether other tasks of the wave ran | Finding | B did not run in P2, ran in the cut first call (PF-5) |
| P3: `navigate` returns `halt <unit>: wave 1 is 🔄 since … with no task-mode wait — next: …` and `done` | Pass | hand-back quoted under P3 |
| P3: Halts lists it | Pass | final report of `P3.jsonl` |
| P3: 0 steps | Pass | `Run: 0 steps · ended by done`; agent calls only `navigate` and `status` |
| P3: the tracking branch is unchanged | Pass | `59504a2` before and after |
| P4: `ended by rail: until 2026-01-01 00:00` | Pass | `Run:` line of `P4.jsonl` |
| P4: no step other than `navigate` and `status` | Pass | the only agent call is `status` |
| P4: the claim is released | Pass | `git update-ref -d` before `status`; refs empty in `P4.evidence.txt` |
| P4: `### Next` has `Continue:` | Pass | present; its text is PF-6 |
| P5a: the `claims/auto` ref stays | Pass | `P5a2.evidence.txt`: `claims/auto/slug-word-count` |
| P5a: wave 1 is 🔄 with its `Waiting: task mode` line | Pass | `🔄 since 2026-11-25 20:18`; `Waiting: task mode A, B` in `waves/w01.md` |
| P5b: `system/init` lists no `wave-method:` skill | Pass | `P5b1.jsonl`, `P5b2.jsonl` |
| P5b: asks whether the holder is gone, quoting it | Pass | result of `P5b1.jsonl` |
| P5b: takes over | Pass | `git update-ref` with the held oid in `P5b2.jsonl` |
| P5b: `next: tasks …` | Pass | `next: tasks … 1 A:low; B:low` |
| P5b: the killed task is done or `already committed` | Pass | `task A: committed d9f4a56`, `task B: committed 665e5ba` |
| P5b: every feature `✅ merged` into `integration/<topic>` | Pass | F1 `fa5d6f7`, F2 `64dec83` |
| P5b: `ended by done` | Pass | `Run:` line of `P5b2.jsonl` |

### Report checks

Applied to the runs that ended with a final report: P1, P2, P3, P4, P5b (the cut P2 call is not judged).

| Check | Run | Result | Evidence |
|---|---|---|---|
| 1 progress lines | P1 | Finding | lines for `triage-answers` and `navigate` only; none for `triage-ask`, `triage-finish`, `plan` (PF-1) |
| 1 progress lines | P2 | Finding | `navigate` has its line, `wave` has none (PF-1) |
| 1 progress lines | P3 | Finding | no line for `navigate` (PF-1) |
| 1 progress lines | P4 | Pass | the run had no counted step and no `navigate`, so no line was due |
| 1 progress lines | P5b | Pass | `20:21 · navigate`, `· task … A`, `· task … B`, `20:23 · wave`, `20:23 · navigate`, each after a clock command and before the next agent call |
| 2 claim | P1, P2, P3, P4, P5b | Pass | the claim is deleted before the `status` call; no Status part lists a `claims/auto/` ref or a note about one |
| 3 template | P1, P2, P3, P5b | Pass | the five parts in order, `### Next` is `Continue:` or `- none`, the times line is last; no coordinator shell command runs the project, its tests or `python` |
| 3 template | P4 | Finding | `### Next` holds a changed command and a note in brackets (PF-6) |

### Findings

Each names the skill text that decides the behaviour. Nothing was changed in a skill.

- **PF-1 · progress lines are still skipped.** `skills/wave-auto/SKILL.md`, "Loop", "Progress lines" (and "Hard rules").
  Expected a line for every step but `status`, written before the next step. Observed no line for: `triage-ask`,
  `triage-finish`, `plan` (P1); `wave` (P2, both calls); `navigate` (P3). In each case the clock command ran and no
  text followed.
- **PF-2 · text the skill does not name.** `skills/wave-auto/SKILL.md`, "Hard rules" ("It writes the user only what this
  skill names"). Expected only the named lines. Observed explanations in P1 to P5b, for example ``Running `triage-ask`
  for the list start.``, ``No clusters, so the next step is `triage-finish`. …``, `Rail reached: … Releasing the claim
  and running the status step.`, `Done. Release the claim, then run status.`
- **PF-3 · no resume command after `triage-ask`.** `skills/wave-auto/SKILL.md`, "Start phase", item 3. Expected, for a
  list start, the `/wave-auto <index>` · `$wave-auto <index>` lines right after `triage-ask`. Observed none in P1; the
  command appears only under `### Next` of the final report.
- **PF-4 · a unit halt ended the run as a stop.** `skills/wave-auto/SKILL.md`, "Stops" (a task's `Needs` →
  `capability-missing` is a halt of one unit; "the run goes on with the other units") and "Loop". Expected: halt the
  unit, `navigate` again with it skipped, `ended by done`. Observed in P2: `Stop capability-missing: …` as a run-ending
  stop with `next: run task A by hand, then resume` (no command), `ended by stop capability-missing`, no further
  `navigate`. The fixture has one unit, so no other work was lost. (The cut first call's ending is not judged.)
- **PF-5 · the other tasks of the wave run or not, by chance.** `skills/wave-auto/SKILL.md`, "Wave" ("one `task` step
  per listed task … a task whose `Needs` names a tool this session lacks goes to the session fallback") and "Session
  fallback" (halt the unit). Expected: task B, which needs nothing, gets its `task` step. Observed: it did in the cut
  first call (`task B: committed be59503`) and did not in P2. The text does not say whether the halt of the unit comes
  before or after the other tasks of the launch group.
- **PF-6 · `### Next` after an `until` rail.** `skills/wave-auto/SKILL.md`, "End of the run" (`### Next` holds only the
  `Continue:` line with `<start>`). Observed in P4 a command with an added `until <later time>` placeholder and a note
  in brackets. The template does not say what `Continue:` carries when the command had options.
- **PF-7 · the status report is not always copied verbatim.** `skills/wave-auto/SKILL.md`, "End of the run". Observed:
  P2 dropped a closing "Notes on the run" block of the `status` step's return; P3 dropped its last
  `Started … Finished` line. P1, P4 and P5b copied it unchanged.
- **PF-8 · end times not read from the clock.** `skills/wave-plan/layout.md`, "Run times" ("never guess"). Observed: P3's
  coordinator read the clock before `status` returned (`20:10`) and printed `Finished: … 20:11`; P5b's `status` step
  (`skills/wave-status/SKILL.md`) printed `Finished: … 20:26` after a single clock command that returned `20:24`, in a
  call that ended at 20:25.

Observations, not judged: under the usage limit the coordinator released its claim and ended with `ended by usage
limit`, an ending the template does not have; in P4 it wrote its claim's object id to a file in its own session scratch
folder, outside the repository.

## Not verified

- The coordinator on an Opus-class model: every call here ran it on `claude-sonnet-5-5`.
- A killed task that had already committed (`already committed <hash>` after a kill): both killed tasks of P5a had
  committed nothing.
- A kill during another step than `task` (the discarded call was killed late, in the wave resume, and not resumed).
- A halt of one unit while another unit of the same run goes on: the fixture has one unit.
- `until` as a bare `HH:MM`, and an `until` time reached in the middle of a run.

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
run P1 textkit "/wave-auto steps 4 <the list above>"
# P-copy: <topic> is chosen by the triage (here slug-word-count)
git -C "$S/textkit" worktree list        # git worktree remove every clean worktree but the main one
cp -r "$S/textkit" "$S/textkit-needs"; cp -r "$S/textkit" "$S/textkit-halt"; cp -r "$S/textkit" "$S/textkit-cut"
# P2: in textkit-needs, `git worktree add "$S/edit" plan/<topic>-p1`, set the Needs cell of task A in
#     plans/<date>-<topic>/plan-1/waves/w01.md, commit, `git worktree remove "$S/edit"`
run P2 textkit-needs "/wave-auto plans/<date>-<topic>/index.md"
# P3: the same way in textkit-halt: README "Waves", wave 1 -> "🔄 since 2026-01-01 00:00", commit
run P3 textkit-halt "/wave-auto plans/<date>-<topic>/index.md"
run P4 textkit-halt "/wave-auto until 2026-01-01 00:00 plans/<date>-<topic>/index.md"
# P5a: textkit or an untouched copy of it (textkit-cut)
cd "$S/textkit-cut"
MSYS_NO_PATHCONV=1 claude -p "/wave-auto plans/<date>-<topic>/index.md" --output-format stream-json --verbose \
  --permission-mode auto --max-budget-usd <cap left> < /dev/null > "$S/calls/P5a.jsonl" &
pid=$!
until grep -qE '"name":"(Agent|Task)".*step task ·' "$S/calls/P5a.jsonl"; do sleep 1; done; sleep 20
taskkill //F //T //PID "$(cat /proc/$pid/winpid)"     # this call only; the shell must not have MSYS_NO_PATHCONV set
git for-each-ref refs/wave-method/; git worktree list # then `git status` in each prepared worktree
run P5b1 textkit-cut "/wave-auto plans/<date>-<topic>/index.md" --setting-sources project,local
run P5b2 textkit-cut "Yes, it is gone." --continue --setting-sources project,local
```

After each call: `git branch --list`, `git for-each-ref refs/wave-method/`, `git log --oneline -3 main`, the unit's
"Waves" and "Tasks" rows. From each stream: the events without `parent_tool_use_id` (the coordinator's text, shell
commands and agent calls), each `SubagentHandback` and the last `result` event. Check for no running call before and
after P5a; never kill by process name.
