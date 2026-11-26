# Rehearsal: wave-auto in the Codex CLI

2026-11-26 · `codex-cli 0.167.0-alpha.3.2` (Windows, the copy that ships with the Codex desktop app) · source checkout
`c7e712f` (the working folder before this record).

Rehearsal D3 of feature F1 (the wave skills run in Codex): rehearsal D2 again, now in a test project that
`~/.codex/config.toml` trusts, so that the permission profile of README "Codex permissions" applies. **The profile
applied**: the thread ran `workspace-write` with `writable_roots` `["<scratch>"]` and profile `wave`, and the
worktree and commit probe passed. `$wave-auto` then ran triage with its questions, the answers, the index merge and
the plan (X2, X3), and in X4 the wave step and two task steps started in their worktrees, until the Codex account hit
its usage limit at 20:12 (finding T1). The limit reset after the 3-hour cap, so the rest of X4 and X5 were not run.
The trust entry was removed afterwards and `~/.codex/config.toml` has its hash from before. The last section,
"Plugin install", is kept unchanged from the previous record (rehearsal D2; its `<scratch>` was that rehearsal's
folder).

## Earlier attempts (2026-11-26)

- Under the `workspace-write` sandbox the pipeline stopped at its first step: `.git` was read-only (findings D1–D6;
  full record in commit 7bcdaf1).
- With the project's profile in a project Codex did not trust, the thread ran with the built-in `:read-only` profile
  and the X1 probe failed (finding N1; full record in commit d794ad8).

## Setup

- `<codex>` is `~/.codex/plugins/.plugin-appserver/codex.exe` (`command -v codex` finds nothing). Signed in.
- `<scratch>` is `~/wave-rehearsal-20261126-1955`: a new empty folder, outside every repository and outside the temp
  folder, never used by Codex before.
- Fixture repository `<scratch>/textkit` on `main`, local user `rehearsal` / `rehearsal@example.invalid`:
  `textkit/__init__.py` (empty), `tests/test_smoke.py`, `README.md` (one line), `.gitignore` (`__pycache__/`,
  `.pytest_cache/`, `.agents/`). Virtual environment `<scratch>/venv` (Python 3.14.6, pytest 9.2.0), first on `PATH`
  of every call.
- Skills: `<working folder>\install.ps1 -Target <scratch>\textkit` (with the Codex links). `.agents/skills/` held the
  five `wave-*` junctions. Commit `Seed textkit with wave skills` (`da01544`); `python -m pytest -q` passed (1 test).
- Profile `<scratch>/textkit/.codex/config.toml` (README "Codex permissions", `<parent>` = `<scratch>`, `<project>` =
  `<scratch>/textkit`, absolute Windows paths as TOML literal keys); `.codex/` added to
  `<scratch>/textkit/.git/info/exclude`:

  ```toml
  default_permissions = "wave"

  [permissions.wave]
  filesystem = { ":root" = "read", '<scratch>' = "write", ":tmpdir" = "write", '<scratch>\textkit\.codex' = "read" }
  ```

- Before X0: `~/.codex/config.toml` copied to `<scratch>/calls/config.before.toml` (a safety copy, not committed), its
  SHA-256 saved to `<scratch>/calls/config.sha.before.txt`, its `[projects.` lines (12 entries) listed to
  `<scratch>/calls/config.projects.before.txt`. `trust_entry.py` of the plan written to `<scratch>/trust_entry.py`
  (tested first on a copy of the file: `add` then `remove` gave the same hash).
- Trust entry, the only change to `~/.codex/config.toml` the user permitted for this rehearsal, added with
  `python <scratch>/trust_entry.py add ~/.codex/config.toml '<scratch>\textkit'` (the Windows form from `cygpath -w`):

  ```toml
  [projects.'<scratch>\textkit']
  trust_level = "trusted"
  ```

- Every `exec` call: from `<scratch>/textkit`, `-C <scratch>\textkit -c 'approval_policy="never"'` (`exec resume`
  has no `-C`: it ran from `<scratch>/textkit` with the `-c` option only), stdin closed (`< /dev/null`), without
  `--ephemeral`, `-m gpt-6.2-astra` on the first call of a session, `--json` saved to `<scratch>/calls/<run>.jsonl`,
  `-o <scratch>/calls/<run>.txt`. No `-s`, no `sandbox_mode`, no bypass, no `danger-full-access`, no
  `-c "projects=…"`. The `CLAUDE*` and `ANTHROPIC*` variables of the driving shell were unset. The driver is
  `<scratch>/run.sh`; the rollout readers are `<scratch>/analyze.py`, `lookup.py`, `cmds.py` and `stream.py`.
- Every stream starts with two warnings about one unrecognized setting of the user's `config.toml`
  (`computer_use.windows.always_allowed_app_ids`), unrelated to this rehearsal.
- The list (one argument, verbatim), used in X2:

  ```
  1. Add textkit/slug.py with slugify(text): lowercase, words joined by "-", only letters and digits kept. 2. Add textkit/count.py with count_words(text) returning a dict word -> count, words compared without case. 3. Add a command "python -m textkit top <file>" that prints the top words of the file with their counts.
  ```

## Runs

Codex calls ran from 19:56 to 20:12 (cap 3 hours, until 22:56). Prompt texts of `spawn_agent` are encrypted in the
rollout files, so the subagents' prompts are judged by their behaviour (checks 6 and 7). Thread list:
`<scratch>/calls/threads.txt`; agent calls: `<scratch>/calls/agentcalls.txt`.

### X0 · version and features

```bash
<codex> --version
<codex> features list
```

- Exit 0 both. `codex-cli 0.167.0-alpha.3.2`.
- `multi_agent  stable  true`; `multi_agent_v2  stable  false`.
- Files: `<scratch>/calls/X0.version.txt`, `X0.features.txt`.

### X1 · can the profile create a worktree and commit

```bash
<codex> exec -m gpt-6.2-astra -C <scratch>\textkit -c 'approval_policy="never"' "First run Get-Location (bash: pwd) and report its output. Then run: git worktree add -b probe ../textkit.worktrees/probe main; then create probe.txt in that worktree and commit it there with message probe. Report each command and its output." < /dev/null
```

- Exit 0, 37 s. Thread `01a21892-665f-7e82-a8ec-da7760a44744`.
- `Get-Location` printed `<scratch>\textkit`. Deciding lines of the final message:

  ```
  Preparing worktree (new branch 'probe')
  HEAD is now at da01544 Seed textkit with wave skills
  [probe bb4a65b] probe
   1 file changed, 1 insertion(+)
  ```

- The thread's last `turn_context` (rollout `~/.codex/sessions/2026/11/26/rollout-*-01a21892-665f-….jsonl`):

  ```
  "cwd": "<scratch>\\textkit",
  "approval_policy": "never",
  "sandbox_policy": {"type": "workspace-write", "writable_roots": ["<scratch>"], "network_access": false,
    "exclude_tmpdir_env_var": true, "exclude_slash_tmp": true},
  "active_permission_profile": {"id": "wave"},
  "model": "gpt-6.2-astra",
  ```

- `git worktree list` afterwards: `<scratch>/textkit.worktrees/probe  bb4a65b [probe]`.
- Side note: every git command in the thread warned `unable to access '~/.config/git/ignore': Permission denied` (the
  profile reads `:root`, but the sandbox account cannot read that file); no command failed because of it.
- Cleanup: `git worktree remove --force ../textkit.worktrees/probe` → exit 0; `git branch -D probe` → exit 0. Only
  `main` at `da01544` and one worktree remained.
- Files: `<scratch>/calls/X1.jsonl`, `X1.txt`, `X1.meta`.

### X2 · start from the list

```bash
<codex> exec -m gpt-6.2-astra -C <scratch>\textkit -c 'approval_policy="never"' "\$wave-auto steps 4 <list>" < /dev/null
```

- Exit 0, 276 s (19:57–20:01). Root thread `01a21893-32b3-78c0-8260-bcf0a8b5dce6`.
- The agent messages, in order (`<scratch>/calls/X2.stream.txt`):

  ```
  Started: wave-auto · steps 4
  Started: 2026-11-26 19:57
  Capabilities: subagents · parallel 3 · model choice (low gpt-6-luna, medium gpt-6.2-sol, high gpt-6.2-astra) · session start no
  19:58 · triage-ask · list → questions 6 · index plans/2026-11-26-text-utilities/index.md
  Resume: `/wave-auto plans/2026-11-26-text-utilities/index.md` · `$wave-auto plans/2026-11-26-text-utilities/index.md`
  Q1. Which letters and digits should slugify keep? … Q6. How should each output line separate the word from its count?
  ```

  The first message holds a `Started:` line without the time; the clock line comes in the second message (finding
  T2). The six questions, each with two options: Q1 and Q2 about item 1, Q3 about items 2 and 3, Q4 (how many words
  `top` prints), Q5 (tie order) and Q6 (separator) about item 3.
- The coordinator first asked the questions with the tool `request_user_input_async`, then called `sleep` twice with
  60000 ms, and only then ended the turn with the questions as text (finding T4). Its final message, which `-o`
  saved, begins with a sentence of its own and repeats the questions as a table (finding T3):

  ```
  `wave-auto` is waiting for your answers after step 1 of 4. You can reply `all A` or list your choices by number.
  | # | Question | A | B |
  …
  Resume: `/wave-auto plans/2026-11-26-text-utilities/index.md` · `$wave-auto plans/2026-11-26-text-utilities/index.md`

  Started: 2026-11-26 19:57 · Finished: 2026-11-26 20:01 (4 min)
  ```

- Spawn: `spawn_agent {"task_name": "triage_ask", "fork_turns": "none", "model": "gpt-6.2-astra", …}`.
- Repository after X2: branch `triage/text-utilities` (worktree `<scratch>/textkit.worktrees/text-utilities-triage`,
  commits `Index text-utilities: original list`, `… pass 1, 3 problems in 1 clusters`, `… questions`); ref
  `refs/wave-method/claims/auto/text-utilities` (blob `5287cda`), taken by one command that wrote the holder object
  and printed its oid.
- Usage of the turn: input 571215, cached input 543616, output 2095 tokens.

### X3 · answer the questions

```bash
cd <scratch>/textkit && <codex> exec resume --last -c 'approval_policy="never"' "Top 10 words, most frequent first." < /dev/null
```

- Exit 0, 374 s (20:02–20:08). Same root thread.
- First agent message, a sentence of its own (finding T3):
  `I’ll continue the four-step wave-auto run with your answer. …`
- Progress lines:

  ```
  20:03 · triage-answers · plans/2026-11-26-text-utilities/index.md → answers recorded · clusters none
  20:04 · triage-finish · plans/2026-11-26-text-utilities/index.md → parts 1 · index plans/2026-11-26-text-utilities/index.md · merged a4ab07c
  20:05 · navigate · plans/2026-11-26-text-utilities/index.md → next: plan plans/2026-11-26-text-utilities/index.md part 1
  20:07 · plan · plans/2026-11-26-text-utilities/plan-1 → planned plans/2026-11-26-text-utilities/plan-1 · waves 1 · tasks low 1, medium 1, high 0
  ```

- Claim released: `git update-ref -d refs/wave-method/claims/auto/text-utilities 5287cda27a08…` (the oid written out).
- Final report (`<scratch>/calls/X3.txt`), deciding lines:

  ```
  ## wave-auto · plans/2026-11-26-text-utilities/index.md
  Run: 4 steps · ended by rail: steps 4 · subagents · parallel 3 · model choice (low gpt-6-luna, medium gpt-6.2-sol, high gpt-6.2-astra) · session start no
  ### Steps            (4 rows: triage-ask, triage-answers, triage-finish, plan; Result cells equal the return lines)
  ### Halts
  - none
  ### Status           (the status step's report: plan text-utilities-p1, autonomous, target integration/text-utilities, F1 and F2 ⬜)
  ### Next
  - Continue: `/wave-auto plans/2026-11-26-text-utilities/index.md` · `$wave-auto plans/2026-11-26-text-utilities/index.md`

  Started: 2026-11-26 19:57 · Finished: 2026-11-26 20:08 (11 min)
  ```

- Spawns: `triage_answers` `gpt-6.2-astra`, `triage_finish` `gpt-6.2-astra`, `navigator` `gpt-6-luna`, `plan_part_1`
  `gpt-6.2-astra`, `run_status` `gpt-6-luna`; every one `fork_turns` `none`.
- Repository after X3: `main` at `a4ab07c` (merge `Index text-utilities`); branches `plan/text-utilities-p1` and
  `integration/text-utilities` with the plan commit; `triage/text-utilities` deleted; no ref under
  `refs/wave-method/`.
- The plan took the answer for Q4 and Q5; the other questions were left to the triage step's assumptions (the plan's
  features are "Count words and print the top ten" and "Generate slugs", branch `…/unicode-slugs`).
- Usage of the turn: input 1397816, cached input 1367808, output 5207 tokens.

### X4 · run the waves from the index

```bash
<codex> exec -m gpt-6.2-astra -C <scratch>\textkit -c 'approval_policy="never"' "\$wave-auto plans/2026-11-26-text-utilities/index.md" < /dev/null
```

- Exit 1, 240 s (20:08–20:12). Root thread `01a2189d-d205-78b2-9b63-24b6b7347c79`.
- Agent messages:

  ```
  Started: `wave-auto plans/2026-11-26-text-utilities/index.md`
  Started: 2026-11-26 20:08
  Capabilities: subagents · parallel 3 · model choice (low gpt-6-luna, medium gpt-6.2-sol, high gpt-6.2-astra) · session start no · git writes enabled
  20:10 · navigate · plans/2026-11-26-text-utilities/index.md → next: wave plans/2026-11-26-text-utilities/plan-1 1
  20:11 · wave · plans/2026-11-26-text-utilities/plan-1 → waiting A:medium; B:low
  ```

  No question. The first line again lacks the time (finding T2).
- Spawns: `navigate_1` `gpt-6-luna`, `wave_1` `gpt-6.2-sol`, then `task_a` `gpt-6.2-sol` and `task_b` `gpt-6-luna`
  launched together; every one `fork_turns` `none`.
- The wave step created `feat/text-utilities-p1/word-frequency` and `feat/text-utilities-p1/unicode-slugs` in
  `<scratch>/textkit.worktrees/text-utilities-p1-f1` and `-f2`, recorded `wave 1 started` and
  `wave 1 waiting for task mode` on `plan/text-utilities-p1`, and took
  `refs/wave-method/claims/integration/text-utilities`. Task A wrote `textkit/count.py`, `textkit/__main__.py` and two
  test files in `-f1` and ran its tests; task B wrote `textkit/slug.py` and `tests/test_slug.py` in `-f2`. Neither
  committed.
- Then the stream ended (finding T1):

  ```
  {"type": "turn.failed", "error": {"message": "You’ve hit your usage limit. … try again at 11:09 PM."}}
  ```

  The limit reset at 23:09, after the cap (22:56), so no further Codex call was started.
- State left by the cut run: `main` at `a4ab07c` (unchanged since X3); claims `refs/wave-method/claims/auto/text-utilities`
  (`wave-auto … 2026-11-26 20:08 run b952d4e3`) and `refs/wave-method/claims/integration/text-utilities`
  (`text-utilities-p1 wave 1 waiting 2026-11-26 20:11 …`) remain; uncommitted task files in both feature worktrees.
- The worktrees the sandboxed thread created are owned by the Windows account `CodexSandboxOffline`; git in the
  user's own shell refuses them: `fatal: detected dubious ownership in repository at
  '<scratch>/textkit.worktrees/text-utilities-p1-f1'` (finding T5). Read here with `git -c safe.directory='*'`.
- Usage (last `token_count` of the root rollout, no `turn.completed`): input 677471, cached input 637568, output 2175.

### X5 · merge and test

Not run: X4 did not finish (T1), and no task commit reached `integration/text-utilities`.

### Removal of the trust entry

Right after X4, the last Codex call:

```bash
python <scratch>/trust_entry.py remove ~/.codex/config.toml '<scratch>'
```

- Printed `removed [projects.'<scratch>\textkit']`; no other entry lay below `<scratch>` (Codex added none for the
  worktrees). The SHA-256 after equals the one before (`f9ddd9b9…`), and the file is byte-identical to the safety copy.
  `grep -c "wave-rehearsal" ~/.codex/config.toml` prints 0.

## Results

| Expectation | Result | Evidence |
|---|---|---|
| X0: the version | Pass | `codex-cli 0.167.0-alpha.3.2` |
| X0: `multi_agent` … `true` | Pass | `X0.features.txt` |
| X1: `Get-Location` is the project | Pass | `<scratch>\textkit` |
| X1: `sandbox_policy` `workspace-write`, `writable_roots` `["<scratch>"]`, `active_permission_profile` `wave` | Pass | `turn_context` of thread `01a21892-…` |
| X1: the worktree and commit exist | Pass | `[probe bb4a65b] probe`; `git worktree list` |
| X1: the probe is removed afterwards | Pass | both cleanup commands exit 0 |
| X2: first lines `Started:` and `Capabilities:` (parallel, three model IDs) | Finding (T2) | `Capabilities: … parallel 3 · model choice (low gpt-6-luna, medium gpt-6.2-sol, high gpt-6.2-astra)` correct; the first `Started:` line has no time, a second one follows |
| X2: one `triage-ask` step | Pass | one `spawn_agent` `triage_ask`; one progress line |
| X2: the `Resume:` line in both forms | Pass | right after the `triage-ask` progress line |
| X2: at least one question about item 3 | Pass | Q3–Q6 (six questions in all) |
| X2: branch `triage/<topic>` exists | Pass | `triage/text-utilities` |
| X2: claim `refs/wave-method/claims/auto/<topic>` exists | Pass | `refs/wave-method/claims/auto/text-utilities` |
| X3: steps `triage-answers`, `triage-finish`, `plan`, `ended by rail: steps 4` | Pass | progress lines; `Run: 4 steps · ended by rail: steps 4` |
| X3: index merged into `main` | Pass | `main` `a4ab07c` `Index text-utilities` |
| X3: plan folder on `plan/<slug>` and `integration/<topic>` | Pass | `plan/text-utilities-p1`, `integration/text-utilities` |
| X3: claim released | Pass | `git update-ref -d …`; no ref under `refs/wave-method/` |
| X3: final report with Steps, Halts, Status, Next | Pass | `<scratch>/calls/X3.txt` |
| X4: no question | Pass | no question in `X4.stream.txt` |
| X4: waves run to the end (`wave`, `task`, resume) | Finding (T1) | `wave` and two `task` steps started; the turn failed on the usage limit before any task returned |
| X4: every feature merged into `integration/<topic>` or under Halts | Not run | cut by T1 |
| X4: no `tier-mismatch` | Pass (up to the cut) | no stop line; task A's lookup printed `gpt-6.2-sol` |
| X4: `main` unchanged since X3 | Pass | `a4ab07c` before and after |
| X4: claim released; `ended by done` | Not run | cut by T1; both claims remain |
| X5: tests green | Not run | X4 did not finish |
| X5: `python -m textkit top README.md` prints at most 10 lines `word count` | Not run | same |
| Check 1: every `spawn_agent` has `fork_turns` `none` and a model of its step's tier | Pass | 11 spawns: `triage_ask`, `triage_answers`, `triage_finish`, `plan_part_1` `gpt-6.2-astra`; `navigator`, `navigate_1`, `run_status` `gpt-6-luna`; `wave_1` `gpt-6.2-sol`; `task_a` (medium) `gpt-6.2-sol`; `task_b` (low) `gpt-6-luna` (rollout `response_item` records, `agentcalls.txt`) |
| Check 2: no more than 3 subagents at once | Pass (up to the cut) | at most 2 at once (`task_a`, `task_b`); every other step was waited for before the next spawn |
| Check 3: every task commit has a `Wave-Model` trailer of its tier | Not run | no task commit before the cut |
| Check 4: the coordinator wrote no file and ran no test; no claim ref after X4 | Pass (commands) / Not run (claim) | its shell calls read the clock, git and the skill files, and took and released the claim (`git hash-object -w`, `git update-ref`); after the cut two claim refs remain |
| Check 5: usage of X2–X4 | Pass | X2 571215 / 543616 cached / 2095 out; X3 1397816 / 1367808 / 5207; X4 677471 / 637568 / 2175 (no `turn.completed`: last `token_count`) |
| Check 6: every `medium` and `high` step subagent runs the model lookup first and gets its model | Pass | `triage_ask`, `triage_answers`, `triage_finish`, `plan_part_1` → `gpt-6.2-astra`; `wave_1`, `task_a` → `gpt-6.2-sol`; the first `custom_tool_call` of each is the PowerShell lookup (`threads.txt`); prompts judged by this behaviour only (encrypted) |
| Check 7: the first shell of the root and of every subagent starts in the project or its worktree | Pass | every thread's first `turn_context` `cwd` is `<scratch>\textkit`; wave and task shells passed the worktree as `workdir` |
| Check 8: the coordinator's texts | Finding (T2, T3) | title, Result cells, Halts and `Continue:` right in X3; the first `Started:` line lacks the time (X2, X4); own sentences in X2 and X3 |
| Check 9: trust entries; nothing else of `~/.codex/config.toml` changed | Pass | added during the run: only `[projects.'<scratch>\textkit']` (ours); removed; the SHA-256 after equals the one before, and the file is identical to the safety copy |

### Findings

- **T1 · X4 cut by the Codex account's usage limit.** Expected (Rehearsal D3, X4): the waves run to the end and the
  run ends `ended by done`. Got: at 20:12 the turn failed with `You’ve hit your usage limit … try again at 11:09 PM`
  (`<scratch>/calls/X4.jsonl`, last two events) while tasks A and B were running; the limit reset after the 3-hour
  cap. Not a defect of the skills; X4's end, X5 and check 3 are unverified. The state left (claims, uncommitted task
  files) is the input for a resume with `$wave-auto plans/2026-11-26-text-utilities/index.md`.
- **T2 · The first line is `Started:` without the time.** Expected (`skills/wave-plan/layout.md:48-49`,
  `skills/wave-auto/SKILL.md:53`): the very first line is `Started: <YYYY-MM-DD HH:MM>`, read from the clock. Got: X2
  and X4 printed `Started: wave-auto · steps 4` and ``Started: `wave-auto plans/…/index.md` `` before reading the
  clock, then a second message `Started: 2026-11-26 19:57` (`20:08`) (`X2.stream.txt`, `X4.stream.txt`).
- **T3 · The coordinator adds sentences of its own.** Expected (`skills/wave-auto/SKILL.md:51-54`): only the named
  lines, no summary or comment. Got: X2's last message begins `` `wave-auto` is waiting for your answers after step 1
  of 4. … `` and repeats the questions as a table; X3 begins `I’ll continue the four-step wave-auto run with your
  answer. …` (`X2.txt`, `X3.stream.txt`).
- **T4 · In `codex exec` the questions first go to `request_user_input_async`.** Expected
  (`skills/wave-auto/SKILL.md:129`): ask them all in one message and wait. Got: the coordinator called
  `request_user_input_async` with the six questions, then `sleep` twice with `duration_ms` 60000, and only then wrote
  the questions as text and ended the turn: two minutes lost in a non-interactive run (root rollout `01a21893-32b3-…`).
- **T5 · Worktrees made in the sandbox are refused by git outside it.** Expected (README "Codex permissions",
  `README.md:62-87`; `skills/wave-plan/layout.md:211`): the sandbox only limits where Codex writes; the user reviews
  the feature branches afterwards. Got: the worktrees `<scratch>/textkit.worktrees/*` created by the thread belong to
  the Windows account `CodexSandboxOffline`, and `git status` there in the user's shell stops with `fatal: detected
  dubious ownership` (the main checkout, created by the user, is not affected). Neither text mentions it or
  `safe.directory`.

## Not verified

- The Codex desktop app: not rehearsed, by the user's decision of 2026-11-26.
- The end of a wave in Codex: task returns and commits, `Wave-Model` trailers (check 3), the wave's merge and
  auto-approval into `integration/<topic>`, `ended by done`, the claim release after X4, and X5 (merge and tests):
  cut by the usage limit (T1).
- More than two parallel subagents (the plan had two tasks).
- macOS and Linux.

## Repeat

In Git Bash on Windows, with `<scratch>` = `~/wave-rehearsal-<YYYYMMDD-HHMM>` (new, empty), the fixture and profile of
"Setup", and `trust_entry.py` of the plan's solution in `<scratch>`:

```bash
codex=~/.codex/plugins/.plugin-appserver/codex.exe
mkdir -p <scratch>/calls; cp ~/.codex/config.toml <scratch>/calls/config.before.toml
sha256sum ~/.codex/config.toml; grep -n '^\[projects\.' ~/.codex/config.toml
powershell.exe -ExecutionPolicy Bypass -File '<working folder>\install.ps1' -Target '<scratch>\textkit'
cd <scratch>/textkit
printf '.agents/\n' >> .gitignore && git add .gitignore README.md tests textkit .claude && git commit -m "Seed textkit with wave skills"
mkdir .codex   # write .codex/config.toml as in "Setup"
printf '.codex/\n' >> .git/info/exclude
python <scratch>/trust_entry.py add ~/.codex/config.toml "$(cygpath -w <scratch>/textkit)"
"$codex" --version
"$codex" features list
mode=(-C "$(cygpath -w <scratch>/textkit)" -c 'approval_policy="never"')
"$codex" exec -m gpt-6.2-astra "${mode[@]}" "First run Get-Location (bash: pwd) and report its output. Then run: git worktree add -b probe ../textkit.worktrees/probe main; then create probe.txt in that worktree and commit it there with message probe. Report each command and its output." --json -o <scratch>/calls/X1.txt < /dev/null > <scratch>/calls/X1.jsonl
git worktree remove --force ../textkit.worktrees/probe; git branch -D probe
"$codex" exec -m gpt-6.2-astra "${mode[@]}" "\$wave-auto steps 4 <list>" --json -o <scratch>/calls/X2.txt < /dev/null > <scratch>/calls/X2.jsonl
"$codex" exec resume --last -c 'approval_policy="never"' "Top 10 words, most frequent first." --json -o <scratch>/calls/X3.txt < /dev/null > <scratch>/calls/X3.jsonl
"$codex" exec -m gpt-6.2-astra "${mode[@]}" "\$wave-auto plans/<date>-<topic>/index.md" --json -o <scratch>/calls/X4.txt < /dev/null > <scratch>/calls/X4.jsonl
git merge --no-ff integration/<topic>; python -m pytest -q; python -m textkit top README.md
python <scratch>/trust_entry.py remove ~/.codex/config.toml "$(cygpath -w <scratch>)"
sha256sum ~/.codex/config.toml; grep -c "wave-rehearsal" ~/.codex/config.toml
```

The sandbox and model of a thread: the `turn_context` records (`sandbox_policy`, `active_permission_profile`,
`model`) of `~/.codex/sessions/YYYY/MM/DD/rollout-*-<thread id>.jsonl`; spawn arguments: its `response_item` records
of type `function_call` named `spawn_agent`. Run the trust removal also before any early stop.

## Plugin install

`codex-cli 0.167.0-alpha.3.2`, run 03:21 with `CODEX_HOME=<scratch>/codex-home` (a new folder), every call with stdin
closed:

| Command | Exit | Deciding output |
|---|---|---|
| `<codex> plugin marketplace add paramidon/wave-method` | 0 | ``Added marketplace `wave-method` from https://github.com/paramidon/wave-method.git.`` |
| `<codex> plugin add wave-method@wave-method` | 0 | ``Added plugin `wave-method` from marketplace `wave-method`.``; root `<scratch>\codex-home\plugins\cache\wave-method\wave-method\2.12.0` |
| `<codex> plugin list` | 0 | `wave-method@wave-method  installed, enabled  2.12.0  <scratch>\codex-home\.tmp\marketplaces\wave-method` |

- `~/.codex/config.toml`: the hash before the rehearsal and after the last plugin command are equal.
- Markdown of README "Codex plugin (recommended for Codex)" (`README.md:50-60`): heading `###` like
  `### Claude Code plugin (recommended for Claude Code)`; a blank line before and after the fenced block and each
  paragraph. Its rendered view is left to the user's review of F1.

Result: Pass
