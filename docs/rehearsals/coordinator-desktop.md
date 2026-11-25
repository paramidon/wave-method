# Rehearsal I — `/wave-auto` in the Claude Code desktop app

Rehearsal of the in-session coordinator `wave-auto` (plan `desktop-coordinator-p1`, feature F1, task M) in the
Claude Code desktop app (Code tab), on 2026-11-25. Procedure: `solutions/P1-in-session-coordinator.md` of the plan,
"Rehearsals (tasks H and I)". The CLI rehearsal is `coordinator-cli.md`.

**Form: D1–D2 ran in a separate desktop session**, started from the rehearsal session with the app's session tool
(folder `<scratch>/textkit`, model `claude-opus-5-5`, permission mode `auto`); the answer of D2 was sent to it with
the app's cross-session messaging. D3 ran in a second separate desktop session started the same way. The fallback
(following `skills/wave-auto/SKILL.md` in the rehearsal session itself) was not needed and not run.

## Setup

- Skills: from `<working folder>` at `b11b85f` (feature branch `feat/desktop-coordinator-p1/F1-in-session-coordinator`
  after tasks J and K of wave 3).
- Scratch: `<scratch>` made with `mktemp -d` outside every repository; repository `<scratch>/textkit` exactly as
  "Fixture (both)" says: `git init -b main`, local user `rehearsal` / `rehearsal@example.invalid`,
  `textkit/__init__.py` (empty), `tests/test_smoke.py`, one-line `README.md`, `.gitignore`.
- Virtual environment `<scratch>/venv` with `pip install pytest` (pytest 9.2.0). The desktop sessions cannot be given
  an environment, so they ran with the app's own `PATH`; its Python 3.14 also has pytest 9.2.0, so the check command
  `python -m pytest -q` worked in both. D4 ran with the venv first on `PATH`.
- Install on Windows with the PowerShell installer:
  `<working folder>\install.ps1 -Target <scratch>\textkit -NoCodex` → five lines `installed …\.claude\skills\wave-*`;
  `.claude/skills` then held `wave-auto`, `wave-plan`, `wave-run`, `wave-status`, `wave-triage`.
- Commit: `f9a3b44 Seed textkit with wave skills` (git warned only about LF → CRLF in the working copy).
- Environment: Windows 11, Claude Code desktop app (Code tab), the rehearsal session on `claude-opus-5-5`. The account
  also has the `wave-method` plugin (v2.12.0, without `wave-auto`) loaded; the coordinated sessions read every skill
  file by its absolute path under `<scratch>/textkit/.claude/skills`, so the project copies were the ones used.
- Caps: 30 USD for the coordinator session, or 3 hours. The app shows plan usage in percent, not USD, for this
  account, so the cost cap could not be measured; the whole rehearsal took 17 min (D1–D2) and 2 min (D3).

## Runs

### D1 — start a desktop session with `/wave-auto <list>`

Action: the app's session tool started a new local session in `<scratch>/textkit`, model `claude-opus-5-5`,
permission mode `auto`, first message `/wave-auto` followed by the list of "Fixture (both)" verbatim. The app put a
short "Background (from the session that started this one)" paragraph before the command in that first message; the
session still invoked the `wave-auto` skill with the list as its arguments.

Deciding lines (session transcript):

```
Started: 2026-11-25 16:19
Capabilities: subagents · parallel · model choice (low haiku, medium sonnet, high opus) · session start yes
16:21 · triage-ask · list → questions 4 · index plans/2026-11-25-textkit-word-tools/index.md
```

It took the claim `refs/wave-method/claims/auto/textkit-word-tools` (holder line
`wave-auto plans/2026-11-25-textkit-word-tools/index.md 2026-11-25 16:21 run <token>`, written with the zero old value),
read the `- Q<n> · …` lines with `git show triage/textkit-word-tools:plans/2026-11-25-textkit-word-tools/index.md`
and asked all four in one message, then ended its turn:

```
Q1 · slugify: what separates words? (a) any run of non-letters/digits ("don't" → "don-t"); (b) whitespace only …
Q2 · slugify: non-ASCII letters like "é"? (a) keep them ("Café" → "café"); (b) transliterate ("cafe"); (c) drop ("caf")
Q3 · count_words: what is one word? (a) a run of letters/digits, same as slugify …; (b) whitespace token …
Q4 · top: how many words are printed? (a) 10 by default, -n N to change; (b) always 10; (c) all of them, sorted by count
```

The session sent the questions to the session that started it (the app's cross-session message), because its first
message came from that session; they also stood in its own transcript.

Evidence after D1 (16:21): `git branch --list` → `main`, `triage/textkit-word-tools`;
`git for-each-ref refs/wave-method/` → `19a4b1f… blob refs/wave-method/claims/auto/textkit-word-tools`.

### D2 — send `Top 10 words, most frequent first.`

Action: sent verbatim with the app's cross-session messaging at 16:21; the app queued it and delivered it as the
session's next message. The session ran to the end without another question; it finished its turn after every step
it started in the background and was woken by each subagent's return.

Progress lines (one per step, each printed when the step returned):

```
16:22 · triage-answers · plans/2026-11-25-textkit-word-tools/index.md → answers recorded · clusters none
16:23 · triage-finish · plans/2026-11-25-textkit-word-tools/index.md → parts 1 · index plans/2026-11-25-textkit-word-tools/index.md · merged 6bc2d4d
16:23 · navigate · plans/2026-11-25-textkit-word-tools/index.md → next: plan plans/2026-11-25-textkit-word-tools/index.md part 1
16:28 · plan · plans/2026-11-25-textkit-word-tools/plan-1 → planned plans/2026-11-25-textkit-word-tools/plan-1 · waves 1 · tasks low 2, medium 1, high 0
16:28 · navigate · plans/2026-11-25-textkit-word-tools/index.md → next: wave plans/2026-11-25-textkit-word-tools/plan-1 1
16:29 · wave · plans/2026-11-25-textkit-word-tools/plan-1 → waiting A:low; C:low
16:30 · task A · plans/2026-11-25-textkit-word-tools/plan-1 → task A: committed 116c60c
16:30 · task C · plans/2026-11-25-textkit-word-tools/plan-1 → task C: committed 1145ea0
16:32 · wave · plans/2026-11-25-textkit-word-tools/plan-1 → waiting B:medium
16:32 · task B · plans/2026-11-25-textkit-word-tools/plan-1 → task B: committed 248788d
16:35 · wave · plans/2026-11-25-textkit-word-tools/plan-1 → wave 1 ✅ · merged F1, F2 · review none · blocked none
16:35 · navigate · plans/2026-11-25-textkit-word-tools/index.md → done
```

Subagent models seen (the agent tool's `model` of each step, from the session transcript):

| Step | Model | Tier expected |
|---|---|---|
| `triage-ask`, `triage-answers`, `triage-finish` | opus | high |
| `navigate` (4 calls) | haiku | low |
| `plan` | opus | high |
| `wave` (3 calls: start, two resumes) | sonnet | medium |
| `task` A, C (low, in parallel) | haiku | low |
| `task` B (medium) | sonnet | medium |
| `status` | haiku | low |

The final report (deciding lines):

```
## wave-auto · 1. Add textkit/slug.py … 3. Add a command "python -m textkit top <file>" …
Run: 10 steps · ended by done · Capabilities: subagents · parallel · model choice (low haiku, medium sonnet, high opus) · session start yes
### Halts
- none
### Status
**plan-1** (`textkit-word-tools-p1`, autonomous flow, target `integration/textkit-word-tools`): wave 1 ✅, none running, no re-plans, no inconsistencies.
| F1 Word counts and `python -m textkit top <file>` | ✅ merged | 2/2 | `feat/textkit-word-tools-p1/F1-word-count-top` | b5a0c4d |
| F2 `slugify(text)` helper | ✅ merged | 1/1 | `feat/textkit-word-tools-p1/F2-slugify-helper` | 3529b52 |
Started: 2026-11-25 16:19 · Finished: 2026-11-25 16:36 (17 min)
```

Between the `Run:` line and "Steps" the coordinator wrote a paragraph of its own ("All three items are built … I also
ran the `top` command and `slugify` by hand in the integration worktree"); after releasing the claim it had run
`python -m textkit top` and `slugify` itself in the integration worktree. The Status section ended with a note that
the claim listed under Leftovers was its own and was released since. "Next" held review and merge instructions and
no Continue line (correct: nothing halted or waiting).

Triage kept the user's answer for Q4 and chose readings (a) for Q1–Q3 itself; the review blocks name them under
"Worth a look" ("don't" → "don-t"; "é" kept; "don't" counts as "don" and "t"). With "Top 10 words, most frequent
first." the `top` command always prints ten words, with no `-n` option.

Evidence after D2 (16:36): `git branch --list` → `feat/textkit-word-tools-p1/F1-word-count-top`,
`feat/textkit-word-tools-p1/F2-slugify-helper`, `integration/textkit-word-tools`, `main`, `plan/textkit-word-tools-p1`;
`git for-each-ref refs/wave-method/` → nothing; `git log --oneline -3 main` → `6bc2d4d Index textkit-word-tools`,
`00fbd15 Index textkit-word-tools: 3 problems in 1 parts`, `5114237 Index textkit-word-tools: answers`.
Coordinator context at the end (the app's context view): 142 516 tokens, of them 84 257 messages, 8 996 skills; the
last request read 142 299 cached input tokens and wrote 1 941 output tokens.

### D3 — a second session with `/wave-auto plans/2026-11-25-textkit-word-tools/index.md`

Action: a new local session started the same way, first message `/wave-auto plans/2026-11-25-textkit-word-tools/index.md`.

```
Started: 2026-11-25 17:31
17:3x · navigate · plans/2026-11-25-textkit-word-tools/index.md → done
## wave-auto · plans/2026-11-25-textkit-word-tools/index.md
Run: 0 steps · ended by done · Capabilities: subagents · parallel · model choice (low haiku, medium sonnet, high opus) · session start yes
### Steps
None. The first navigate returned `done`, so nothing was triaged, planned or run in this run.
### Halts
- none
Started: 2026-11-25 17:31 · Finished: 2026-11-25 17:33 (2 min)
```

No question was asked. It took and released the claim; its subagents were `navigate` (haiku) and `status` (haiku).
The Status section had the same features, statuses, merge hashes and review blocks as D2. Its Leftovers line again
listed the run's own claim (`held by wave-auto plans/2026-11-25-textkit-word-tools/index.md 2026-11-25 17:31 run …,
set minutes ago, so it is likely live`), with the coordinator's note after the status report's own `Started … Finished`
line. The progress line has `17:3x` where the clock time belongs.

Evidence after D3 (17:33): the same branches as after D2; `git for-each-ref refs/wave-method/` → nothing;
`git log --oneline -3 main` unchanged (`6bc2d4d`, `00fbd15`, `5114237`). Coordinator context at the end: 107 369 input
tokens on the last request, 2 068 output tokens.

### D4 — merge and test as C5

In `<scratch>/textkit`, with `<scratch>/venv/Scripts` first on `PATH`:

```
git merge --no-ff integration/textkit-word-tools -m "Merge integration/textkit-word-tools"  → exit 0, aa9ecb8
python -m pytest -q                                                                         → 27 passed
python -m textkit top README.md                                                             → 9 lines `word count`, exit 0
```

A second file `b a b c b a` printed `b 3`, `a 2`, `c 1`. The merge brought `textkit/slug.py`, `textkit/count.py`,
`textkit/__main__.py`, three test files and the plan folder.

## Results

| Expectation | Result | Evidence |
|---|---|---|
| D1 runs in a new desktop session in `<scratch>/textkit` on an Opus model | Pass | session model `claude-opus-5-5`, folder `<scratch>/textkit` (app session metadata) |
| D1 asks ≥ 1 question about item 3 | Pass | `Q4 · top: how many words are printed?` among four questions; `questions 4` |
| D1 waits after asking | Pass | turn ended after the questions; claim and `triage/textkit-word-tools` present, nothing else at 16:21 |
| D2 runs to the end without another question | Pass | no question after the answer; final report `ended by done` at 16:36 |
| D2: one progress line per step | Pass | twelve lines in D2 (ten counted steps and the navigate lines), each `HH:MM · step · unit → return line` |
| D2: final report with every feature merged into `integration/<topic>` or under Halts with a next command | Pass | F1 `✅ merged` `b5a0c4d`, F2 `✅ merged` `3529b52`; Halts `none` |
| D2: final report follows "End of the run" | Finding (F-c) | extra paragraph after `Run:`; own smoke test after the claim's release; see Problems |
| D2: no leftover of the run in the Status | Finding (I4 again) | Leftovers listed the run's own claim; the note is inside Status, before "Next" |
| Steps run on their tier's model | Pass | table under D2 |
| D3: no question | Pass | no question in the session |
| D3: the navigator finds nothing to run | Pass | `navigate … → done` as the first and only navigate |
| D3: report says `ended by done` | Pass | `Run: 0 steps · ended by done` |
| D3: the same Status | Pass | same features, statuses, merge hashes `b5a0c4d`, `3529b52`, same review blocks |
| D3: progress line with the clock time | Finding (F-a) | `17:3x · navigate · … → done` |
| D3: own claim not reported as a leftover | Finding (I4 again) | Leftovers and "Coordinator claims" named the run's own claim; note after the status report's closing line |
| `main` receives only the triage index | Pass | `git log --oneline -3 main` after D2 and D3: `6bc2d4d Index textkit-word-tools` on top |
| Claim released at the end of D2 and D3 | Pass | `git for-each-ref refs/wave-method/` empty after each |
| D4: merge, tests green | Pass | merge `aa9ecb8`; `27 passed` |
| D4: `python -m textkit top README.md` prints at most 10 lines `word count` | Pass | 9 lines, exit 0 |
| `install.ps1` installs the five skills (entry I6) | Pass | five `installed` lines, `.claude/skills` lists five folders |
| Cost cap 30 USD | Not run | the app shows plan usage in percent for this account; no USD figure; the time cap (3 h) was kept: 19 min |

## Not verified

- The answer of D2 typed by a person into the coordinator session's own message box: it was sent by the rehearsal
  session through the app's cross-session messaging, and the coordinator took it as the user's answer.
- The first message exactly `/wave-auto <list>`: the app prepended a "Background" paragraph to it.
- Closing the desktop session mid-run and resuming from a new one with a step half done (D3 resumed only a finished
  run), the `until` and `steps` rails, `halt` lines, a re-plan, the session fallback, the `triage-cluster` step (the
  list has three problems).
- A run without the account-level `wave-method` plugin loaded beside the project skills.
- Permission modes other than `auto`; the cost in USD.
- `install.ps1` without `-NoCodex` (junctions for Codex).

## Repeat

```bash
S=$(mktemp -d); cd "$S" && mkdir textkit && cd textkit
git init -q -b main && git config user.name rehearsal && git config user.email rehearsal@example.invalid
mkdir textkit tests && : > textkit/__init__.py
printf 'def test_import():\n    import textkit\n' > tests/test_smoke.py
printf 'textkit — small text helpers. Check: python -m pytest -q\n' > README.md
printf '__pycache__/\n.pytest_cache/\n' > .gitignore
cd "$S" && python -m venv venv && venv/Scripts/python -m pip install pytest
```

```powershell
& "<working folder>\install.ps1" -Target "<scratch>\textkit" -NoCodex
```

```bash
cd <scratch>/textkit && git add .gitignore README.md textkit tests .claude && git commit -m "Seed textkit with wave skills"
```

Then, from a Claude Code desktop session that has the app's session tools:

1. D1: start a new session, folder `<scratch>/textkit`, model Opus, first message `/wave-auto <list>` (the list of
   "Fixture (both)" verbatim); wait for its questions.
2. D2: send it `Top 10 words, most frequent first.`; wait until it ends its turn with the final report.
3. After D2 and D3: `git branch --list`, `git for-each-ref refs/wave-method/`, `git log --oneline -3 main`, and the
   session's last message.
4. D3: start a second session there with `/wave-auto plans/<date>-<topic>/index.md`.
5. D4, with `<scratch>/venv/Scripts` first on `PATH`:

```bash
git merge --no-ff integration/<topic> && python -m pytest -q && python -m textkit top README.md
```
