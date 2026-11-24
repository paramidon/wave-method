# Rehearsal: wave-auto in the Claude Code CLI

2026-11-24 · Claude Code 2.1.326 · source checkout `b11b85f` (the working folder before this record).

Rehearsal H of feature F1 (in-session coordinator `wave-auto`): one fixture project, from a list to merged features,
through the questions round, a rail, a resume in a new session and a claim takeover.

## Setup

- Made `<scratch>` with `mktemp -d`. Calls are saved as `<scratch>/calls/<run>.jsonl` (stream), `.err`, `.exit` and
  `<run>.evidence.txt` (branches, `refs/wave-method/`, `git log --oneline -3 main` after the run).
- Fixture repository `<scratch>/textkit` on `main`, local user `rehearsal` / `rehearsal@example.invalid`:
  `textkit/__init__.py` (empty), `tests/test_smoke.py` (`def test_import(): import textkit`), `README.md` (one line,
  "textkit — small text helpers. Check: python -m pytest -q"), `.gitignore` (`__pycache__/`, `.pytest_cache/`). Commit
  `Seed textkit`.
- Virtual environment `<scratch>/venv` (Python 3.14, `pip install pytest` gave pytest 9.2.0). Every call ran with
  `<scratch>/venv/Scripts` first on `PATH`.
- `sh <working folder>/install.sh <scratch>/textkit --no-codex` installed the five skills, then `git add -A` and
  commit `Seed textkit with wave skills` (`c25f075`). `main` was clean at that commit before P0.
- Every call: `claude -p "<prompt>" --output-format stream-json --verbose --permission-mode auto`, run in
  `<scratch>/textkit` with `MSYS_NO_PATHCONV=1` (Git Bash on Windows), stdin from `/dev/null`, no `--model` (the
  coordinator ran on the CLI default, `claude-opus-5-5` in every `system/init`). C2 and C4 add `--continue`.
- The list (one argument, verbatim):

  ```
  1. Add textkit/slug.py with slugify(text): lowercase, words joined by "-", only letters and digits kept. 2. Add textkit/count.py with count_words(text) returning a dict word -> count, words compared without case. 3. Add a command "python -m textkit top <file>" that prints the top words of the file with their counts.
  ```

- Every `system/init` listed the project skills `wave-auto`, `wave-plan`, `wave-run`, `wave-status`, `wave-triage`
  and also the four user-level plugin skills `wave-method:wave-plan` … `wave-method:wave-triage` (a plugin installed
  for the account; it has no `wave-auto`). `/wave-auto` resolved to the project skill; every step prompt carried
  `Skills folder: <scratch>/textkit/.claude/skills`, so the plugin copies were not read.
- Permission denials: none in any run (`permission_denials` empty), so the `bypassPermissions` repeat was not needed.
- Cost: the six calls cost 6.98 USD in total (cap 30 USD); nothing was skipped for cost. P0b is an extra probe, not
  in the plan.

## Runs

### P0 · can a subagent start subagents

```bash
claude -p "Launch one subagent. Ask it to list the names of all its tools that can start another agent, subagent or session, or to answer 'none'. Reply with its answer verbatim." ...
```

- Exit 0, 12 s, 0.3414 USD, 2 turns. The coordinator's tools: `Task` (agent tool), `SendMessage`, `Monitor`, … ; the
  subagent's prompt was "List the names of all your tools that can start another agent, subagent or session. If you
  have none, answer exactly 'none'. …".
- Deciding line (the subagent's `SubagentHandback`, and the result text): `Agent, RemoteTrigger`.
- Differs from the expectation (`none` or no agent tool): finding F-1 below.
- Extra probe P0b (`<scratch>/calls/P0b.jsonl`, 12 s, 0.4160 USD): the main session launched subagent A with the
  instruction to launch one more subagent B that replies `nested-ok`. The stream shows A's own `Agent` call (the event
  carries `parent_tool_use_id`) and B's reply; the result text was `nested-ok`. So in this version a subagent can start
  a subagent.

### C1 · start from the list

```bash
claude -p "/wave-auto steps 4 <list>" ...
```

- Exit 0, 85 s, 0.8160 USD, 7 turns, model `claude-opus-5-5`.
- Stream: the coordinator printed `Started: 2026-11-24 22:56` and `Capabilities: subagents · parallel · model choice
  (low haiku, medium sonnet, high opus) · session start no`, launched one `Agent` call (model `opus`, step line
  `Coordinated run · step triage-ask · unit list · return: wave-plan/layout.md, "Coordinated runs"`), took the claim,
  read the `- Q<n>` lines with `git show triage/slug-word-count:…`, and asked.
- Result text, first lines: `22:57 · triage-ask · list → questions 6 · index plans/2026-11-24-slug-word-count/index.md`
  and ``Resume command for this run: `/wave-auto plans/2026-11-24-slug-word-count/index.md` · `$wave-auto …` ``. It
  listed Q1 to Q6 with readings; Q5 (`top` count: "(a) 10 by default, with an option `-n/--number N` …") and Q6
  (output format and ties) concern item 3. It ended: "I'm waiting for your answers before I go on."
- State after (`C1.evidence.txt`): branches `main` and `+ triage/slug-word-count`; ref
  `47ce836c… refs/wave-method/claims/auto/slug-word-count`; `main` still `c25f075`.
  `git show triage/slug-word-count:plans/2026-11-24-slug-word-count/index.md` has `- Triage: waiting for answers`
  right after `- Flow: autonomous · target: integration/slug-word-count`, and six `- Q<n> · P<k>: …` lines.
  `git cat-file -p` of the claim: `wave-auto plans/2026-11-24-slug-word-count/index.md 2026-11-24 22:57 run 77bd0c7f`.

### C2 · answer, rail ends the run

```bash
claude -p "Top 10 words, most frequent first." --continue ...
```

- Exit 0, 318 s, 2.7816 USD, 9 turns, no denials. One `result` event.
- Steps and models (from the `Agent` calls of the stream):

  | Step | Model of the call |
  |---|---|
  | `triage-answers` (prompt ends with the `Answers:` block) | opus |
  | `triage-finish` | opus |
  | `navigate` | haiku |
  | `plan` (unit `plans/2026-11-24-slug-word-count/plan-1`) | opus |
  | `status` | haiku |

- Return lines in the final table: `answers recorded · clusters none`,
  `parts 1 · index plans/2026-11-24-slug-word-count/index.md · merged 01c2820`,
  `planned plans/2026-11-24-slug-word-count/plan-1 · waves 1 · tasks low 2, medium 1, high 0`.
- Final report: header `## wave-auto · plans/2026-11-24-slug-word-count/index.md`, then
  `Run: 4 steps · ended by rail: steps 4 · Capabilities: …`, sections `### Steps`, `### Halts` (`none`), `### Status`,
  `### Next` with ``Continue: `/wave-auto plans/2026-11-24-slug-word-count/index.md` · `$wave-auto …` ``, and
  `Started: 2026-11-24 22:56 · Finished: 2026-11-24 23:03 (7 min)`. The text says the user's answer "covered Q5 and Q6"
  and the other questions used the triage's defaults.
- State after (`C2.evidence.txt`): `git log --oneline -3 main`: `01c2820 Index slug-word-count`,
  `69e6cc2 Index slug-word-count: 3 problems in 1 parts`, `f82f721 Index slug-word-count: answers`; branches
  `integration/slug-word-count`, `main`, `plan/slug-word-count-p1`; `git for-each-ref refs/wave-method/` empty.
  `git cat-file -e plan/slug-word-count-p1:plans/2026-11-24-slug-word-count/plan-1/README.md` and the same on
  `integration/slug-word-count` both succeed (integration tip `78b4b6a`, plan tip `0b65082`).
  Index on `main`: P3 Clarifications `Top 10 words, most frequent first. (user's answer, 2026-11-24); tie order
  assumed under Assumptions`; P1 and P2 `no answer from the user; assumed readings …`.
- Coordinator session usage at the end of C2 (last `result` event): `input_tokens 22`, `output_tokens 4547`,
  `cache_read_input_tokens 492192`, `cache_creation_input_tokens 10257`; the last request of the coordinator held
  75,484 tokens of context (input 2 + cache read 75,212 + cache creation 270). An empty session of P0 ended at 43,888,
  so the pipeline so far added about 31,600 tokens to the coordinator's context. These counts are the coordinator
  only; the subagents' tokens appear in `modelUsage` (opus 2.761 USD, haiku 0.020 USD).
- Progress lines: the coordinator printed no `<HH:MM> · <step> · <unit> → <return line>` line for `triage-answers`,
  `triage-finish` or `navigate`; the only text between the calls was `Step 4 of 4: plan (rail check: 3 steps used).`
  Finding F-2.

### C3 · stale claim

```bash
oid=$(printf 'wave-auto stale 2026-01-01 00:00 run deadbeef\n' | git hash-object -w --stdin)
git update-ref refs/wave-method/claims/auto/slug-word-count $oid     # 0092cbd…
claude -p "/wave-auto plans/2026-11-24-slug-word-count/index.md" ...  # new session, no --continue
```

- Exit 0, 17 s, 0.4188 USD, 5 turns, no `Agent` call.
- The coordinator read the clock and `layout.md`, tried to take the claim (`git update-ref … 0000…` against the zero oid
  failed with exit 128, `update_ref failed`), read the holder and printed:
  ``The coordinator claim for this index is already held: … `wave-auto stale 2026-01-01 00:00 run deadbeef` … Is that
  holder gone, meaning no other `wave-auto` session is running on `slug-word-count`?`` with the two answers
  "Yes: I'll take over the claim and continue the run" and "No: I'll stop with `wave-running` and change nothing".
- State after (`C3.evidence.txt`): ref still `0092cbdd… refs/wave-method/claims/auto/slug-word-count`; `main` still
  `01c2820`; no new branch, no commit.

### C4 · takeover, waves to the end

```bash
claude -p "Yes, it is gone." --continue ...
```

- Exit 0, 446 s wall time (one process), 2.2070 USD in total, no denials. The stream holds three `result` events: when
  tasks A and B were launched together, the coordinator ended its turn with a text line while they ran, and the CLI
  re-invoked it as each finished; the process stayed alive until the last one. The last event has the final report.
- Takeover (coordinator Bash call): `git update-ref refs/wave-method/claims/auto/slug-word-count "$oid" "$held"` with
  `held=0092cbdd…`; reply `Claim taken over. Now navigating.` The new holder line was
  `wave-auto plans/2026-11-24-slug-word-count/index.md 2026-11-24 23:04 run f56ac4a5`.
- Steps and models:

  | Time | Step | Model | Return line |
  |---|---|---|---|
  | 23:04 | `navigate` | haiku | `next: wave plans/2026-11-24-slug-word-count/plan-1 1` |
  | 23:05 | `wave` | sonnet | `waiting A:low; B:low` |
  | 23:07 | `task` A (low) | haiku | `task A: committed add85c7` |
  | 23:07 | `task` B (low) | haiku | `task B: committed a197541` |
  | 23:08 | `wave` (resume) | sonnet | `waiting C:medium` |
  | 23:08 | `task` C (medium) | sonnet | `task C: committed a22530f` |
  | 23:10 | `wave` (resume) | sonnet | `wave 1 ✅ · merged F1, F2 · review none · blocked none` |
  | 23:10 | `navigate` | haiku | `done` |
  | | `status` | haiku | its report |

  Tasks A and B were launched back to back as asynchronous agents (the tool result was "Async agent launched"), so they ran in parallel. Every step line of the prompts started
  `Coordinated run · step <step> · unit … · return: wave-plan/layout.md, "Coordinated runs"`; the `medium` steps began
  with `Required tier: medium — Sonnet 5.5 / GPT-6.1 SOL (or stronger). …`.
- The plan's wave file (on `plan/slug-word-count-p1`, `waves/w01.md`, Execution): `Capabilities: coordinated run
  (every task in task mode)`; `… Wave-Model claude-haiku-5-5 (low tier), check green (F1 8 passed, F2 6 passed)`;
  `… Wave-Model claude-sonnet-5-5 (medium tier), report block read from its commit, check green (F2 14 passed)`;
  `Merged 2026-11-24 23:09: F1 707e359 (auto-approved)`, `Merged … F2 60b7271 (auto-approved)`; `Finished 2026-11-24
  23:10.` The README has both features `✅ merged`, wave 1 `✅`, tasks A, B, C `✅`.
- Final report: `Run: 6 steps · ended by done · Capabilities: …`, `### Steps` with the seven wave/task rows above,
  `### Halts` (`- none`), `### Status`, `### Next`, `Started: 2026-11-24 23:04 · Finished: 2026-11-24 23:11 (7 min)`.
  The status table: `F1 … ✅ merged … 707e359`, `F2 … ✅ merged … 60b7271`. The report adds that nothing went into
  `main`.
- State after (`C4.evidence.txt`): `git log --oneline -3 main` unchanged (`01c2820`, `69e6cc2`, `f82f721`);
  `git for-each-ref refs/wave-method/` empty (the coordinator released with
  `git update-ref -d … 94c8af9c…`, its own oid); branches `feat/slug-word-count-p1/F1-slugify-helper`,
  `feat/slug-word-count-p1/F2-top-words-command`, `integration/slug-word-count`, `main`, `plan/slug-word-count-p1`;
  integration tip `972f67d Plan slug-word-count-p1: status after merging F1, F2`.
- Coordinator session usage at the end of C4 (last `result` event): `input_tokens 32`, `output_tokens 5276`,
  `cache_read_input_tokens 839347`, `cache_creation_input_tokens 8887`; the last request of the coordinator held
  89,292 tokens of context (input 2 + cache read 88,981 + cache creation 309), 45,400 above the empty session of P0.
  `modelUsage` of the process (coordinator and subagents): opus 1.003 USD, sonnet 1.132 USD, haiku 0.072 USD.
- The status step ran while the run still held its claim, so its report listed the coordinator's own claim under
  Leftovers with "suggested `git update-ref -d …`"; the coordinator appended a note that the claim was released
  afterwards (in C2 as a sentence before the table, in C4 after the report's `Started … Finished` line). Observation O-1.

### C5 · merge and use

```bash
cd <scratch>/textkit
git merge --no-ff integration/slug-word-count -m "Merge integration/slug-word-count"
python -m pytest -q
python -m textkit top README.md
```

- Merge commit `272b047`. `python -m pytest -q` → `21 passed in 0.17s`. `python -m textkit top README.md` exit 0, ten
  lines `word<TAB>count`, each count 1: `textkit`, `—`, `small`, `text`, `helpers.`, `check:`, `python`, `-m`, `pytest`,
  `-q` (output has Windows line ends). Words are whitespace-separated tokens, the reading the plan recorded under
  Assumptions for Q3.

## Results

| Expectation | Result | Evidence |
|---|---|---|
| P0: the answer is `none` or names no agent tool | Finding | `P0.jsonl`: `SubagentHandback {"message": "Agent, RemoteTrigger"}`; `P0b.jsonl`: A launched B (nested `Agent` call with `parent_tool_use_id`), reply `nested-ok` (F-1) |
| C1: one `triage-ask` step | Pass | `C1.jsonl`: one `Agent` call, step line `… step triage-ask · unit list …`; line `22:57 · triage-ask · list → questions 6 · …` |
| C1: the result asks at least one question about item 3 | Pass | Q5 (how many top words, option `-n`) and Q6 (format and ties) in the result text |
| C1: branch `triage/<topic>` with `- Triage: waiting for answers` | Pass | `C1.evidence.txt` (`+ triage/slug-word-count`); `git show triage/slug-word-count:plans/…/index.md` |
| C1: claim `refs/wave-method/claims/auto/<topic>` exists | Pass | `47ce836c… refs/wave-method/claims/auto/slug-word-count` in `C1.evidence.txt` |
| C2: steps `triage-answers`, `triage-finish`, `plan`, rail `ended by rail: steps 4` | Pass | `C2.jsonl` `Agent` calls (plus `navigate` and `status`, which do not count); `Run: 4 steps · ended by rail: steps 4` |
| C2: index merged into `main` | Pass | `01c2820 Index slug-word-count` on `main` (`C2.evidence.txt`); `git show main:plans/…/index.md` |
| C2: plan folder on `plan/<slug>` and `integration/<topic>` | Pass | `git cat-file -e <branch>:plans/2026-11-24-slug-word-count/plan-1/README.md` succeeds on both |
| C2: claim released | Pass | `git for-each-ref refs/wave-method/` empty in `C2.evidence.txt` |
| C2: final report has Steps, Halts, Status, Next and the resume command | Pass | final text of `C2.jsonl`: four sections and ``Continue: `/wave-auto plans/2026-11-24-slug-word-count/index.md` · `$wave-auto …` `` |
| C3: asks whether the holder is gone, quoting the holder line; nothing else happens | Pass | `C3.jsonl` result text quotes `wave-auto stale 2026-01-01 00:00 run deadbeef`; no `Agent` call; ref and `main` unchanged (`C3.evidence.txt`) |
| C4: per wave a `wave` step, `task` steps and a resume | Pass | table of C4: `wave` (waiting A:low; B:low), tasks A, B, resume (waiting C:medium), task C, resume (wave 1 ✅) |
| C4: every feature `✅ merged` into `integration/<topic>` (auto-approved) or a finding | Pass | F1 `707e359`, F2 `60b7271`, `Approved: auto` in the status report; wave file Execution |
| C4: `main` unchanged since C2 | Pass | `01c2820` in `C2.evidence.txt` and `C4.evidence.txt` |
| C4: no 🔄 wave | Pass | README `Waves`: `1 … ✅`; status `Waves: 1 ✅ … none running` |
| C4: claim released; final report | Pass | refs empty in `C4.evidence.txt`; final report in `C4.jsonl` |
| C4: the takeover works (the holder is replaced, the run goes on) | Pass | `git update-ref <ref> <new> <held>` in the coordinator's Bash call; holder line `… 23:04 run f56ac4a5` in the status report |
| C5: tests green | Pass | `21 passed in 0.17s` after merge `272b047` |
| C5: `python -m textkit top README.md` prints at most 10 lines `word count` | Pass | ten lines, `word<TAB>count` |
| Models: `navigate` haiku | Pass | `Agent` model `haiku` in C2 and C4 |
| Models: `triage-*` and `plan` opus | Pass | `Agent` model `opus` for `triage-ask`, `triage-answers`, `triage-finish`, `plan` |
| Models: `triage-cluster` sonnet | Not run | the list has 3 problems; the cluster step exists only for more than 8 |
| Models: `wave` sonnet; `task` by the task's complexity | Pass | `wave` calls `sonnet`; A and B (low) `haiku`; C (medium) `sonnet`; trailers `Wave-Model claude-haiku-5-5`, `claude-sonnet-5-5` |
| The coordinator's context stays small | Pass | last request 75,484 tokens at the end of C2 and 89,292 at the end of C4, against 43,888 for an empty session; the coordinator read no plan, wave or solution file (its own Bash and Read calls touch only `layout.md`, the index's open questions and git refs) |
| No step's subagent asked a question | Pass | every return line of C1 to C4 has the form of its step; no `Stop` line; no question in a result |
| Hard rule: one progress line per step | Finding | C2: none for three of four steps (F-2); C1 and C4: present |

Observation O-1 (not an expectation of the plan): see the end of C4 and Problems in the report.

### Findings

- **F-1 · P0 differs.** Expected `none`; observed `Agent, RemoteTrigger`, and the probe P0b showed a subagent can start
  a subagent. The premise of the plan ("A subagent cannot start subagents", `solutions/P1-in-session-coordinator.md`,
  "Cause") does not hold for Claude Code 2.1.326 with these settings. The skills still behave as designed, because the
  coordinated-run rule is written in the prompt (`wave-auto/SKILL.md`, "Step prompt": "start no subagent"; `layout.md`,
  "Coordinated runs"); nothing in this rehearsal failed because of it. What changes is the justification (a
  subagent could run a whole wave) and the fallback text.
- **F-2 · progress lines missing in C2.** `wave-auto/SKILL.md`, "Hard rules", last bullet, asks for one line
  `<HH:MM> · <step> · <unit> → <return line>` per step. C2 printed none for `triage-answers`, `triage-finish` and
  `navigate`, and `Step 4 of 4: plan (rail check: 3 steps used).` for `plan`; C4 printed all. The loop section
  ("Loop") does not say when the line is printed, so it depends on the model.

## Not verified

- `triage-cluster` steps and the model of that tier (needs more than 8 problems).
- The session fallback (`session start no` in every `Capabilities:` line), a `tier-mismatch` stop, a task whose
  `Needs` names a tool the session lacks.
- The rails `until <time>` (only `steps 4` was run) and a wave left waiting by a rail, then resumed.
- A run killed mid-step (closed window, usage limit); C3 and C4 show only a resume after a clean end plus a stale claim.
- Re-plan, a `halt` line, `manual-flow`, a plan with several parts and `after part <J> merged`.
- The interactive form (a person typing in the TUI); every call here was `claude -p`. In the stream, text between tool
  calls was visible, but a person's terminal was not observed.
- `--permission-mode auto` ran without denials; no other mode was tried.
- The four user-level plugin skills were loaded next to the project ones in every call; a run without them was not made.

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
run() { n=$1; shift; claude -p "$@" --output-format stream-json --verbose --permission-mode auto \
  < /dev/null > "$S/calls/$n.jsonl"; }
run P0 "Launch one subagent. Ask it to list the names of all its tools that can start another agent, subagent or session, or to answer 'none'. Reply with its answer verbatim."
run C1 "/wave-auto steps 4 <the list above>"
run C2 "Top 10 words, most frequent first." --continue
oid=$(printf 'wave-auto stale 2026-01-01 00:00 run deadbeef\n' | git hash-object -w --stdin)
git update-ref refs/wave-method/claims/auto/<topic> "$oid"
run C3 "/wave-auto plans/<date>-<topic>/index.md"
run C4 "Yes, it is gone." --continue
git merge --no-ff integration/<topic> && python -m pytest -q && python -m textkit top README.md
```

After each call: `git branch --list`, `git for-each-ref refs/wave-method/`, `git log --oneline -3 main`; from the stream,
every `Agent` call's `model` and the `Coordinated run · step …` line of its `prompt`, the last `result` event's `result`,
`usage` and `total_cost_usd`. The `<topic>` is chosen by the triage (here `slug-word-count`), so it can differ between
repetitions. Stop starting calls when the summed `total_cost_usd` reaches 30 USD.
