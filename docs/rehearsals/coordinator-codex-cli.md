# Rehearsal: wave-auto in the Codex CLI

2026-11-26 · `codex-cli 0.167.0-alpha.3.2` (Windows, the copy that ships with the Codex desktop app) · source checkout
`a3e09d6` (the working folder before this record).

Rehearsal D of feature F1 (the wave skills run in Codex). **The pipeline did not run in Codex CLI under the
`workspace-write` sandbox**: that sandbox keeps `.git` read-only, so `$wave-auto` stopped in its first step, before any
branch, claim, question or plan. The fallback the procedure names for this case
(`--dangerously-bypass-approvals-and-sandbox`) was forbidden by the restriction of this run, so X3, X4 and X5 were not
run.

## Setup

- `<codex>` is `~/.codex/plugins/.plugin-appserver/codex.exe` (`command -v codex` finds nothing). Signed in.
- Restriction of this run, stricter than the procedure: the sandbox stays on in every call (at most `workspace-write`,
  with `<scratch>` as the writable root), no bypass or full-access option, no change of the user's Codex settings, no
  desktop control.
- `<scratch>` was made with `mktemp -d` in a temp folder below the user profile, outside every repository.
- Fixture repository `<scratch>/textkit` on `main`, local user `rehearsal` / `rehearsal@example.invalid`:
  `textkit/__init__.py` (empty), `tests/test_smoke.py`, `README.md` (one line), `.gitignore` (`__pycache__/`,
  `.pytest_cache/`, `.agents/`). Virtual environment `<scratch>/venv` (Python 3.14.6, pytest 9.2.0).
- Skills: `<working folder>\install.ps1 -Target <scratch>\textkit` (with the Codex links). `.agents/skills/` held the
  five `wave-*` junctions. Commit `Seed textkit with wave skills` (`a8b5a02`); `python -m pytest -q` passed (1 test).
- The account also has the plugin `wave-method` 2.12.0 enabled (four skills, no `wave-auto`), so the skill list of each
  thread held both the project skills and `wave-method:wave-*`. The files read in X2 were the project copies under
  `<scratch>/textkit/.claude/skills/`.
- Every `exec` call ran in `<scratch>/textkit` with stdin closed (`< /dev/null`), without `--ephemeral`, with `--json`
  saved to `<scratch>/calls/<run>.jsonl`, `-o <scratch>/calls/<run>.txt`, `-m gpt-6.2-astra` and these options
  (`<mode>`):

  ```
  -c 'sandbox_mode="workspace-write"' -c 'sandbox_workspace_write.writable_roots=["<scratch>"]' -c 'approval_policy="never"'
  ```

- Additions to the procedure, all narrowing what a call can touch: `approval_policy="never"` (no command may leave the
  sandbox on approval); `TEMP`, `TMP` and `TMPDIR` set to `<scratch>/tmp` (so the temp folders that `workspace-write`
  also opens lie inside `<scratch>`); the `CLAUDE*` and `ANTHROPIC*` variables of the driving shell unset.
  `<scratch>/venv` was first on `PATH`.
- The `turn_context` record of every thread of X1 and X2 says `sandbox_policy` `workspace-write`, `approval_policy`
  `never`, network access off.
- The user's settings were `[windows] sandbox = "elevated"`; every stream starts with two warnings about one
  unrecognized setting of the user's `config.toml`.
- **Side effect:** the first `exec` call in the new folder (X1) made Codex itself append to `~/.codex/config.toml`:
  `[projects.'<scratch, lower case>\textkit']` with `trust_level = "trusted"` (finding D6). The entry was left in
  place; the user may delete it.
- The list (one argument, verbatim):

  ```
  1. Add textkit/slug.py with slugify(text): lowercase, words joined by "-", only letters and digits kept. 2. Add textkit/count.py with count_words(text) returning a dict word -> count, words compared without case. 3. Add a command "python -m textkit top <file>" that prints the top words of the file with their counts.
  ```

## Runs

Codex calls ran from 01:34 to 01:37 (cap 3 hours, not reached).

### X0 · version and features

```bash
<codex> --version
<codex> features list
```

- Exit 0. `codex-cli 0.167.0-alpha.3.2`.
- `multi_agent  stable  true`; `multi_agent_v2  stable  false`.
- Files: `<scratch>/calls/X0.version.txt`, `X0.features.txt`.

### X1 · can the sandbox create a worktree and commit

```bash
<codex> exec -m gpt-6.2-astra <mode> "Run: git worktree add -b probe ../textkit.worktrees/probe main; then create probe.txt in that worktree and commit it there with message probe. Report each command and its output." < /dev/null
```

- Exit 0, 28 s. Thread `01a214a2-0216-7651-b4f5-a1b2297e2123`.
- The first command failed with `fatal: not a git repository (or any of the parent directories): .git`: the shell was in
  `C:\`, not in the folder of the session (`Get-Location` printed `C:\`; finding D2).
- Codex repeated it with `git -C <scratch>/textkit`:

  ```
  Preparing worktree (new branch 'probe')
  fatal: cannot lock ref 'refs/heads/probe': Unable to create '<scratch>/textkit/.git/refs/heads/probe.lock': Permission denied
  ```

- No branch, worktree, `probe.txt` or commit exists (`X1.evidence.txt`: only `main` at `a8b5a02`). Finding D1. The
  thread's permission profile lists `<scratch>\textkit\.git` with access `read` although `<scratch>` is a writable root.
- The procedure's `<mode>` for this outcome is the bypass option; it was not used. `<mode>` stayed as above, and no
  other way to open `.git` was tried.
- Cleanup: `git worktree remove --force ../textkit.worktrees/probe` → `fatal: '…' is not a working tree`;
  `git branch -D probe` → `error: branch 'probe' not found`. Nothing was left to remove.
- Files: `<scratch>/calls/X1.jsonl`, `X1.txt`, `X1.evidence.txt`.

### X2 · start from the list

```bash
<codex> exec -m gpt-6.2-astra <mode> "\$wave-auto steps 4 <list>" < /dev/null
```

- Exit 0, 2 min 10 s. Thread `01a214a2-d272-7991-b54c-3d9e3092599b`.
- The coordinator first tried relative paths (`C:\.claude\skills\wave-auto\SKILL.md` not found), then read
  `layout.md` and `wave-auto/SKILL.md` by full path and used `git -C` (finding D2).
- Its first three messages and the progress line, from the stream:

  ```
  I’ll use `wave-auto` with the four-step limit you requested.

  Started: 2026-11-26 01:35
  Capabilities: subagents · parallel 3 · model choice (low and medium gpt-6.2-sol, high gpt-6.2-astra) · session start no

  01:37 · triage-ask · list → Stop repository-read-only: Creating the triage branch and worktree requires writing to the repository’s read-only `.git` directory — next: run the triage step with writable Git metadata.
  ```

- Spawn calls (the `--json` stream shows only the `wait` calls, so these are read from the `response_item` records of
  the coordinator's rollout file `~/.codex/sessions/2026/11/26/rollout-*-01a214a2-d272-….jsonl`; the `message`
  argument is encrypted there):

  | `task_name` | `fork_turns` | `model` | model in the thread's `turn_context` | thread |
  |---|---|---|---|---|
  | `triage_ask` | `none` | `gpt-6.2-astra` | `gpt-6.2-astra` | `01a214a3-7fdd-…` |
  | `status` | `none` | `gpt-6.2-sol` | `gpt-6.2-sol` | `01a214a4-1f03-…` |

- The `spawn_agent` tool description of the coordinator lists as model overrides `gpt-6.2-sol`, `gpt-6.2-astra`,
  `gpt-6.1-terra`, `gpt-6.1-sol`, `gpt-6-astra`; `gpt-6-luna` is not among them (finding D3).
- The `triage-ask` subagent (tier high) read `wave-triage/SKILL.md`, ran `git branch --show-current` and one search of
  `layout.md`, and returned the stop. It ran no model lookup and named no model (finding D4). It also got
  `Set-Location : Access is denied` for `<scratch>/textkit` (finding D2).
- The run ended after `triage-ask` and `status`. Final message, deciding lines:

  ```
  Started: 2026-11-26 01:35
  Stop repository-read-only: `wave-auto` requires a triage branch and worktree. This checkout grants read-only access to `.git` — next: rerun the original command in a checkout with writable Git metadata.

  ## wave-auto · slugify, word counts, and top words
  Run: 1 step · ended by stop `repository-read-only` · subagents · parallel 3 · …
  | 01:37 | `triage-ask` | list | Stopped before creating the triage index. All three features remain unimplemented. |
  - List — read-only Git metadata prevents triage.
  - Continue: `/wave-auto steps 4 <original list>` · `$wave-auto steps 4 <original list>` in a checkout with writable Git metadata.
  Started: 2026-11-26 01:35 · Finished: 2026-11-26 01:37 (2 min)
  ```

- No question was asked, no `Resume:` line was printed. State after (`X2.evidence.txt`): only `main` at `a8b5a02`, no
  `triage/*` branch, no ref under `refs/wave-method/`, one worktree, clean status.
- Usage of the `turn.completed` event: input 447,266, cached input 422,272, output 1,881 tokens (the coordinator's
  thread only). The rollout totals of the subagents: `triage_ask` 147,418 / 118,656 / 416; `status`
  201,115 / 179,840 / 692.
- Files: `<scratch>/calls/X2.jsonl`, `X2.txt`, `X2.evidence.txt`, the three rollout files.

### X3 · answer the questions

Not run. X2 ended with a stop before it made an index or asked a question, so there was nothing to answer or resume,
and the sandbox that would be used cannot write what X3 expects. `codex exec resume` was not called.

### X4 · run the waves from the index

Not run. No index exists (X2).

### X5 · merge and test

Not run. No `integration/<topic>` branch exists (X2).

## Results

| Expectation | Result | Evidence |
|---|---|---|
| X0: the version | Pass | `codex-cli 0.167.0-alpha.3.2` |
| X0: `multi_agent` … `true` | Pass | `X0.features.txt` |
| X1: the worktree and commit exist under `workspace-write` | Finding (D1, D2) | `cannot lock ref … Permission denied`; `X1.evidence.txt` |
| X1: otherwise `<mode>` is the bypass option | Not run | forbidden by the restriction of this run |
| X1: the probe is removed afterwards | Pass | nothing was created; no `probe` branch or worktree |
| X2: first lines `Started:` and `Capabilities:` | Finding (D5) | a preamble line comes before `Started:` |
| X2: `Capabilities:` names `parallel` | Pass | `parallel 3` |
| X2: `Capabilities:` names the three model IDs | Finding (D3) | `gpt-6.2-sol` and `gpt-6.2-astra` only |
| X2: one `triage-ask` step | Pass | one `spawn_agent` `triage_ask`; it ended in a stop |
| X2: the `Resume:` line in both forms | Finding (D1) | not printed; no index path |
| X2: at least one question about item 3 | Finding (D1) | no question |
| X2: branch `triage/<topic>` exists | Finding (D1) | `X2.evidence.txt`: only `main` |
| X2: claim `refs/wave-method/claims/auto/<topic>` exists | Finding (D1) | never taken; no ref |
| X3: steps `triage-answers`, `triage-finish`, `plan`, `ended by rail: steps 4` | Not run | no index, no question (D1) |
| X3: index merged into `main` | Not run | same |
| X3: plan folder on `plan/<slug>` and `integration/<topic>` | Not run | same |
| X3: claim released | Not run | same |
| X3: final report with Steps, Halts, Status, Next | Not run | same |
| X4: no question | Not run | no index (D1) |
| X4: waves run to the end (`wave`, `task`, resume) | Not run | same |
| X4: every feature merged into `integration/<topic>` or under Halts | Not run | same |
| X4: no `tier-mismatch` | Not run | same |
| X4: `main` unchanged since X3 | Not run | same |
| X4: claim released | Not run | same |
| X4: `ended by done` | Not run | same |
| X5: tests green | Not run | no integration branch (D1) |
| X5: `python -m textkit top README.md` prints at most 10 lines `word count` | Not run | same |
| Check 1: every `spawn_agent` has `fork_turns` `none` and a model of its step's tier | Finding (D3) | rollout: both `none`; `status` (low) got `gpt-6.2-sol`, expected `gpt-6-luna`; only X2's two steps seen |
| Check 2: no more than 3 subagents at once | Not run | two spawns one after the other; no parallel launch point was reached |
| Check 3: every task commit has a `Wave-Model` trailer of its tier | Not run | no task commit |
| Check 4: the coordinator wrote no file and ran no test | Pass (X2 only) | its shell calls: reading the skill files, `git rev-parse`, `git branch --show-current`, the clock |
| Check 4: after X4 no ref under `refs/wave-method/claims/` | Not run | X4 not run (after X2 there is none) |
| Check 5: usage of X2 | Pass | 447,266 / 422,272 / 1,881 (input / cached / output) |
| Check 5: usage of X3 and X4 | Not run | calls not made |

### Findings

- **D1 · `workspace-write` cannot run the pipeline.** Codex keeps `.git` of a writable root read-only, so no branch,
  worktree, commit or claim ref can be made. Expected (X1): worktree and commit. Got: `Permission denied` on
  `.git/refs/heads/probe.lock`; in X2 the first step returned `Stop repository-read-only`, a code no skill defines.
  `skills/wave-plan/layout.md:148-162` ("Vendors") says nothing about the permissions Codex needs, and its
  non-interactive form (`:162`) names no sandbox option. `README.md` does not either.
- **D2 · Windows sandbox: shells do not start in the project.** In the root and in subagents, commands ran in `C:\`,
  also when a working directory was given to the tool, and `Set-Location` into the project was denied once. Relative
  paths and `git` without `-C` fail until the agent switches to full paths. The cause was not examined; the project
  lies below the user profile.
- **D3 · `gpt-6-luna` is not chosen for `low`.** Expected: `Capabilities:` with three IDs and `gpt-6-luna` for `low`
  steps. Got: `gpt-6.2-sol` for `low` and `medium`; the `spawn_agent` description does not list `gpt-6-luna`.
  Text: `skills/wave-plan/layout.md:156`, `skills/wave-auto/SKILL.md:61-63`. Whether a `gpt-6-luna` spawn would be
  accepted was not tried here (the planning evidence of this feature records successful ones).
- **D4 · No tier check in a high step.** Expected: the step's subagent determines its model by the lookup before it
  reads or changes anything (`skills/wave-plan/layout.md:122-125`, `:693-694`). Got: `triage_ask` ran no lookup and
  named no model; its developer messages state no model ID. Whether its prompt carried the gate line
  (`skills/wave-auto/SKILL.md:79`) cannot be read: the spawn message is encrypted.
- **D5 · The coordinator's output leaves the fixed texts.** A preamble before `Started:`
  (`skills/wave-auto/SKILL.md:51-53`); the report title is not `## wave-auto · <start>` (`:225`); the Steps table
  retells the result instead of the return line (`:232`, `:41`); the Halts line has no `next:` (`:236`); `Continue:`
  holds the placeholder `<original list>` instead of the start (`:244`).
- **D6 · A call writes to the user's Codex settings.** `codex exec` in a new folder appended a trust entry for it to
  `~/.codex/config.toml`. The procedure of this rehearsal does not foresee it. This is Codex behaviour, not a skill.

## Not verified

- Everything after the first step of the pipeline in Codex CLI: triage questions and answers, `exec resume`, plans,
  waves, parallel spawns and the limit of 3, task commits and trailers, claim take and release, merge and tests.
- Whether the pipeline runs with other permissions. Neither the bypass option nor an extra writable root for `.git`
  was tried.
- The model lookup of `layout.md` "Vendors" inside this sandbox: no thread ran it.
- Whether D2 also happens for a project outside the user profile, or on macOS or Linux.
- The text of the step prompts (encrypted in the rollout files, absent from the stream).
- Windows PowerShell read the UTF-8 skill files as mojibake when an agent omitted `-Encoding utf8`; no plan file was
  written, so the effect on status symbols is unknown.

## Repeat

In Git Bash on Windows, with `<scratch>` from `mktemp -d` and the fixture of "Setup":

```bash
codex=~/.codex/plugins/.plugin-appserver/codex.exe
powershell.exe -ExecutionPolicy Bypass -File '<working folder>\install.ps1' -Target '<scratch>\textkit'
cd <scratch>/textkit
printf '.agents/\n' >> .gitignore && git add -A && git commit -m "Seed textkit with wave skills"
"$codex" --version
"$codex" features list
mode=(-c 'sandbox_mode="workspace-write"' -c 'sandbox_workspace_write.writable_roots=["<scratch>"]' -c 'approval_policy="never"')
"$codex" exec -m gpt-6.2-astra "${mode[@]}" "Run: git worktree add -b probe ../textkit.worktrees/probe main; then create probe.txt in that worktree and commit it there with message probe. Report each command and its output." --json -o <scratch>/calls/X1.txt < /dev/null > <scratch>/calls/X1.jsonl
"$codex" exec -m gpt-6.2-astra "${mode[@]}" "\$wave-auto steps 4 <list>" --json -o <scratch>/calls/X2.txt < /dev/null > <scratch>/calls/X2.jsonl
git branch -a; git for-each-ref refs/wave-method/; git worktree list
```

Spawn arguments and models: the `response_item` and `turn_context` records of
`~/.codex/sessions/YYYY/MM/DD/rollout-*-<thread id>.jsonl`.
