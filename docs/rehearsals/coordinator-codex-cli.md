# Rehearsal: wave-auto in the Codex CLI

2026-11-26 · `codex-cli 0.167.0-alpha.3.2` (Windows, the copy that ships with the Codex desktop app) · source checkout
`edc415b` (the working folder before this record).

Rehearsal D2 of feature F1 (the wave skills run in Codex): rehearsal D again, now with the permission profile of README
"Codex permissions" in the project's `.codex/config.toml` and no sandbox option on the command line. **The profile was
not applied**: the thread ran with the built-in `:read-only` profile, so the worktree and commit probe (X1) made
nothing, and X2–X5 were not run. The plugin install commands of README "Codex plugin" passed.

## First attempt (2026-11-26)

Under the `workspace-write` sandbox the pipeline stopped at its first step: `.git` was read-only, so `$wave-auto`
returned a stop before any branch, claim, question or plan. Findings D1 (no git writes), D2 (shells start in `C:\`),
D3 (no `gpt-6-luna` for `low`), D4 (no model lookup in a high step), D5 (coordinator texts) and D6 (a trust entry
added to `~/.codex/config.toml`). The full record is commit 7bcdaf1.

## Setup

- `<codex>` is `~/.codex/plugins/.plugin-appserver/codex.exe` (`command -v codex` finds nothing). Signed in.
- `<scratch>` is `~/wave-rehearsal-20261126-0319`: a new empty folder, outside every repository and outside the temp
  folder, never used by Codex before.
- Fixture repository `<scratch>/textkit` on `main`, local user `rehearsal` / `rehearsal@example.invalid`:
  `textkit/__init__.py` (empty), `tests/test_smoke.py`, `README.md` (one line), `.gitignore` (`__pycache__/`,
  `.pytest_cache/`, `.agents/`). Virtual environment `<scratch>/venv` (Python 3.14.6, pytest 9.2.0), first on `PATH`
  of every call.
- Skills: `<working folder>\install.ps1 -Target <scratch>\textkit` (with the Codex links). `.agents/skills/` held the
  five `wave-*` junctions. Commit `Seed textkit with wave skills` (`16e1c6c`); `python -m pytest -q` passed (1 test).
- Profile `<scratch>/textkit/.codex/config.toml` (README "Codex permissions", `<parent>` = `<scratch>`, `<project>` =
  `<scratch>/textkit`, absolute Windows paths written as TOML literal keys); `.codex/` added to
  `<scratch>/textkit/.git/info/exclude`:

  ```toml
  default_permissions = "wave"

  [permissions.wave]
  filesystem = { ":root" = "read", '<scratch>' = "write", ":tmpdir" = "write", '<scratch>\textkit\.codex' = "read" }
  ```

- Before X0: the SHA-256 of `~/.codex/config.toml` was saved, and its `[projects.` lines (11 entries) were listed to
  `<scratch>/calls/config.projects.before.txt`.
- Every `exec` call: from `<scratch>/textkit`, `-C <scratch>/textkit -c 'approval_policy="never"'`, stdin closed
  (`< /dev/null`), without `--ephemeral`, `-m gpt-6.2-astra`, `--json` saved to `<scratch>/calls/<run>.jsonl`,
  `-o <scratch>/calls/<run>.txt`. No `-s`, no `sandbox_mode`, no bypass, no `danger-full-access` (the user's
  decision). The `CLAUDE*` and `ANTHROPIC*` variables of the driving shell were unset. The driver is
  `<scratch>/run.sh`.
- Every stream starts with two warnings about one unrecognized setting of the user's `config.toml`
  (`computer_use.windows.always_allowed_app_ids`), unrelated to this rehearsal.
- The list (one argument, verbatim), prepared for X2:

  ```
  1. Add textkit/slug.py with slugify(text): lowercase, words joined by "-", only letters and digits kept. 2. Add textkit/count.py with count_words(text) returning a dict word -> count, words compared without case. 3. Add a command "python -m textkit top <file>" that prints the top words of the file with their counts.
  ```

## Runs

Codex calls ran from 03:20 to 03:21 (cap 3 hours, not reached).

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
<codex> exec -m gpt-6.2-astra -C <scratch>/textkit -c 'approval_policy="never"' "First run Get-Location (bash: pwd) and report its output. Then run: git worktree add -b probe ../textkit.worktrees/probe main; then create probe.txt in that worktree and commit it there with message probe. Report each command and its output." < /dev/null
```

- Exit 0, 15 s. Thread `01a21502-7952-7fa1-9edf-4a02142e4cf0`.
- `Get-Location` printed `<scratch>\textkit` (the shell started in the project).
- Codex then ran nothing more. Final message, deciding line:

  ```
  The session has read-only filesystem access. The remaining commands were not run and produced no output.
  ```

- The thread's `turn_context` (rollout `~/.codex/sessions/2026/11/26/rollout-*-01a21502-7952-….jsonl`):

  ```
  "cwd": "<scratch>\\textkit",
  "approval_policy": "never",
  "sandbox_policy": {"type": "read-only"},
  "permission_profile": {"type": "managed", "file_system": {"type": "restricted",
    "entries": [{"path": {"type": "special", "value": {"kind": "root"}}, "access": "read"}]}, "network": "restricted"},
  "active_permission_profile": {"id": ":read-only"},
  "model": "gpt-6.2-astra",
  ```

  The profile `wave` of `<scratch>/textkit/.codex/config.toml` was not used: no `<scratch>` write entry, active profile
  `:read-only` (finding N1).
- No trust entry was added to `~/.codex/config.toml` (unlike D6 of the first attempt): the hash and the `[projects.`
  lines are unchanged after the call.
- Cleanup: `git worktree remove --force ../textkit.worktrees/probe` → exit 128, `is not a working tree`;
  `git branch -D probe` → exit 1, `branch 'probe' not found`. Only `main` at `16e1c6c`, one worktree, no ref under
  `refs/wave-method/`, clean status.
- Files: `<scratch>/calls/X1.jsonl`, `X1.txt`, `X1.evidence.txt`, `X1.meta`.

### X2 · start from the list

Not run. X1 failed, and the procedure marks X2–X5 Not run then: the thread cannot write `.git`.

### X3 · answer the questions

Not run (X1).

### X4 · run the waves from the index

Not run (X1).

### X5 · merge and test

Not run (X1).

## Results

| Expectation | Result | Evidence |
|---|---|---|
| X0: the version | Pass | `codex-cli 0.167.0-alpha.3.2` |
| X0: `multi_agent` … `true` | Pass | `X0.features.txt` |
| X1: `Get-Location` is the project | Pass | `<scratch>\textkit` |
| X1: the worktree and commit exist under the profile | Finding (N1) | `sandbox_policy` `read-only`, `active_permission_profile` `:read-only`; nothing created (`X1.evidence.txt`) |
| X1: the probe is removed afterwards | Pass | nothing was created; no `probe` branch or worktree |
| X2: first lines `Started:` and `Capabilities:` (parallel, three model IDs) | Not run | X1 failed |
| X2: one `triage-ask` step | Not run | same |
| X2: the `Resume:` line in both forms | Not run | same |
| X2: at least one question about item 3 | Not run | same |
| X2: branch `triage/<topic>` exists | Not run | same |
| X2: claim `refs/wave-method/claims/auto/<topic>` exists | Not run | same |
| X3: steps `triage-answers`, `triage-finish`, `plan`, `ended by rail: steps 4` | Not run | same |
| X3: index merged into `main` | Not run | same |
| X3: plan folder on `plan/<slug>` and `integration/<topic>` | Not run | same |
| X3: claim released | Not run | same |
| X3: final report with Steps, Halts, Status, Next | Not run | same |
| X4: no question | Not run | same |
| X4: waves run to the end (`wave`, `task`, resume) | Not run | same |
| X4: every feature merged into `integration/<topic>` or under Halts | Not run | same |
| X4: no `tier-mismatch` | Not run | same |
| X4: `main` unchanged since X3 | Not run | same |
| X4: claim released; `ended by done` | Not run | same |
| X5: tests green | Not run | same |
| X5: `python -m textkit top README.md` prints at most 10 lines `word count` | Not run | same |
| Check 1: every `spawn_agent` has `fork_turns` `none` and a model of its step's tier | Not run | no coordinator ran |
| Check 2: no more than 3 subagents at once | Not run | same |
| Check 3: every task commit has a `Wave-Model` trailer of its tier | Not run | no task commit |
| Check 4: the coordinator wrote no file and ran no test; no claim ref after X4 | Not run | no coordinator ran |
| Check 5: usage of X2–X4 | Not run | calls not made |
| Check 6: every `medium` and `high` step subagent runs the model lookup first | Not run | no subagent ran; prompt texts would be judged by behaviour only (encrypted in the rollout) |
| Check 7: the first shell of the root and of every subagent starts in the project or its worktree | Pass (X1 root only) | X1 `Get-Location` → `<scratch>\textkit`; no subagent ran |
| Check 8: the coordinator's texts (`Started:`, title, Result cells, Halts `— next:`, `Continue:`) | Not run | no coordinator ran |
| Check 9: trust entries added to `~/.codex/config.toml`; nothing else changed | Pass | no `[projects.` line added; the hash after the last call equals the one before |

### Findings

- **N1 · The project's permission profile is not applied.** Expected (X1, README "Codex permissions",
  `README.md:62-78`; `skills/wave-plan/layout.md:183-202`): with `<project>/.codex/config.toml` holding
  `default_permissions = "wave"`, the thread writes below `<scratch>`, so the worktree and commit exist. Got: the
  thread ran with `sandbox_policy` `read-only` and `active_permission_profile` `:read-only`; Codex refused to run the
  git commands. `layout.md:185-186` says Codex reads the file "for a trusted project", but neither it nor the README
  says how a project becomes trusted; `codex exec` with only `-C` and `approval_policy` added no trust entry for the new
  folder (check 9), so the project file was ignored and the default for an untrusted folder applied. Whether a trust
  entry (or the profile in `~/.codex/config.toml`) makes the profile work was not tried: both change the user's
  settings, outside this procedure.

## Not verified

- Everything after the probe: the pipeline itself in Codex CLI (triage questions and answers, `exec resume`, plans,
  waves, parallel spawns, task commits and trailers, claims, merge and tests) and checks 1–6 and 8.
- Whether the profile works once the project is trusted, or when it stands in `~/.codex/config.toml`.
- The model lookup of `layout.md` "Vendors" inside a Codex thread: no thread ran it.
- macOS and Linux.

## Repeat

In Git Bash on Windows, with `<scratch>` = `~/wave-rehearsal-<YYYYMMDD-HHMM>` (new, empty) and the fixture of "Setup":

```bash
codex=~/.codex/plugins/.plugin-appserver/codex.exe
sha256sum ~/.codex/config.toml; grep -n '^\[projects\.' ~/.codex/config.toml
powershell.exe -ExecutionPolicy Bypass -File '<working folder>\install.ps1' -Target '<scratch>\textkit'
cd <scratch>/textkit
printf '.agents/\n' >> .gitignore && git add .gitignore README.md tests textkit .claude && git commit -m "Seed textkit with wave skills"
mkdir .codex   # write .codex/config.toml as in "Setup"
printf '.codex/\n' >> .git/info/exclude
"$codex" --version
"$codex" features list
mode=(-C '<scratch>\textkit' -c 'approval_policy="never"')
"$codex" exec -m gpt-6.2-astra "${mode[@]}" "First run Get-Location (bash: pwd) and report its output. Then run: git worktree add -b probe ../textkit.worktrees/probe main; then create probe.txt in that worktree and commit it there with message probe. Report each command and its output." --json -o <scratch>/calls/X1.txt < /dev/null > <scratch>/calls/X1.jsonl
"$codex" exec -m gpt-6.2-astra "${mode[@]}" "\$wave-auto steps 4 <list>" --json -o <scratch>/calls/X2.txt < /dev/null > <scratch>/calls/X2.jsonl
"$codex" exec resume --last -c 'approval_policy="never"' "Top 10 words, most frequent first." --json -o <scratch>/calls/X3.txt < /dev/null > <scratch>/calls/X3.jsonl
git branch -a; git for-each-ref refs/wave-method/; git worktree list
sha256sum ~/.codex/config.toml; grep -n '^\[projects\.' ~/.codex/config.toml
```

The sandbox of a thread: the `turn_context` records (`sandbox_policy`, `active_permission_profile`) of
`~/.codex/sessions/YYYY/MM/DD/rollout-*-<thread id>.jsonl`.

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
