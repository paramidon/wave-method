# Rehearsal: wave-auto in the Codex desktop app

2026-11-26 · Codex desktop app, listed as "ChatGPT" on this Windows computer (package `OpenAI.Codex`
26.1120.6357.0, read from the package list, not from the app) · source checkout `edc415b` (the working folder before
this record).

Rehearsal E2 of feature F1 (the wave skills run in Codex), with the permission profile of README "Codex permissions".
**Not run: desktop control of the app was denied.** The setup was built, then the request to control the app
("ChatGPT") was answered `user_denied`. By the task's rule no other way was tried (no Codex CLI in its place, no second
request), so E0–E4 and every check are Not run, and nothing is known yet about whether the desktop app applies the
project's profile.

## Setup

- `<scratch>`: `~/wave-rehearsal-desktop-20261126-0416`, a new empty folder outside every repository and outside the
  temp folder, never used by Codex before. It is left in place.
- Fixture as "Fixture (both)" of the plan: `<scratch>/textkit` with `git init -b main`, user name and e-mail set
  locally, `textkit/__init__.py`, `tests/test_smoke.py`, `README.md`, `.gitignore`; `<scratch>/venv` with pytest 9.2.0.
- Skills with the Codex links: `<working folder>\install.ps1 -Target <scratch>\textkit` → five `wave-*` folders in
  `.claude/skills/` and five junctions in `.agents/skills/`; `.agents/` added to `.gitignore`; one commit
  `137ccf0 Seed textkit with wave skills`.
- Profile in `<scratch>/textkit/.codex/config.toml` (absolute paths, written as `<scratch>` here):

  ```toml
  default_permissions = "wave"

  [permissions.wave]
  filesystem = { ":root" = "read", "<scratch>" = "write", ":tmpdir" = "write", "<scratch>\\textkit\\.codex" = "read" }
  ```

  `.codex/` added to `<scratch>/textkit/.git/info/exclude`; `git status --short --ignored` shows `!! .agents/` and
  `!! .codex/` only.
- Before E0 (04:16): SHA-256 of `~/.codex/config.toml` and its 11 `[projects.` lines saved in `<scratch>/evidence/`,
  with the list of the 98 rollout files under `~/.codex/sessions/`.

## Runs

### E0 — open the app, note its version and tools

Not run. The request for desktop control of "ChatGPT" (the Codex desktop app) returned
`{"granted":[],"denied":[{"bundleId":"OpenAI.Codex_2p2nqsd0c76g0!App","reason":"user_denied"}]}`. The app was not
opened, clicked or typed into. The version in the header comes from the package list, not from the app's About page.

### E1 — open `<scratch>/textkit` as a project, new thread with GPT-6.2-Astra, `$wave-auto <list>`

Not run (no desktop control). No permission setting was seen or chosen; no thread was started: the rollout files under
`~/.codex/sessions/` are the same 98 files after the denial, the newest from 03:20, before this rehearsal.

### E2 — reply `Top 10 words, most frequent first.`

Not run (no desktop control).

### E3 — second thread `$wave-auto plans/<date>-<topic>/index.md`

Not run (no desktop control).

### E4 — merge `integration/<topic>` into `main` and test

Not run: E1–E3 made no integration branch. `<scratch>/textkit` has one commit on `main` and no other branch.

## Results

| Expectation | Result | Evidence |
|---|---|---|
| E0: the app's version from About or settings; the tools a new thread lists | Not run | desktop control denied (`user_denied`); package version 26.1120.6357.0 only |
| E1: the permission setting the app shows for the project (exact name); a setting that names the profile `wave` | Not run | desktop control denied; the app was not opened |
| E1: `sandbox_policy` of the thread's `turn_context`, writable roots | Not run | no thread: no new rollout file after 04:16 |
| E1: `Capabilities:` line, value of `session start` | Not run | no thread |
| E1: ≥ 1 question about item 3; it waits | Not run | no thread |
| E1: git writes allowed under the profile (no `git-read-only`, no `Permission denied`) | Not run | no thread |
| E2: runs to the end without another question; one progress line per step; final report | Not run | no thread |
| E2: every feature merged into `integration/<topic>` or under Halts with a next command | Not run | no thread |
| E2: permission prompts of the app (each one a finding) | Not run | no thread |
| E3: no question; `ended by done` with the same Status | Not run | no thread |
| E4: tests green; `python -m textkit top README.md` prints at most 10 lines `word count` | Not run | no integration branch |
| Check 1: `spawn_agent` with `fork_turns` `none` and the model of the step's tier | Not run | no rollout file |
| Check 3: every task commit has a `Wave-Model` trailer of its tier or higher | Not run | no task commit |
| Check 4: the coordinator wrote no file and ran no test; no claim left | Not run | no coordinator ran |
| Check 6: every `medium` and `high` step subagent runs the model lookup first | Not run | no rollout file |
| Check 7: the first shell of the root and of every subagent starts in the project or its worktree | Not run | no rollout file |
| Check 8: `Started:` first; title `## wave-auto · <start>`; Result cells, Halts `— next:`, `Continue:` | Not run | no output |
| Check 9: trust entries added to `~/.codex/config.toml` during the run; nothing else changed | Not run | no run; the file did change at 04:17:22, see "Not verified" |

## Not verified

- Everything this rehearsal was for: whether the Codex desktop app applies `<project>/.codex/config.toml` (the profile
  `wave`), which permission setting it shows for a new project, whether it asks to trust the folder, whether
  `$wave-auto` runs to the end there, and whether the app can start a session (`session start`).
- `~/.codex/config.toml` changed between the snapshot (04:16) and the check (04:22): its SHA-256 differs and its last
  write is 04:17:22, while its 11 `[projects.` lines are the same. This rehearsal started no Codex call and did not
  touch the app, and no rollout file appeared; the Codex desktop app was already running (since 02:11) and its
  background processes are the likely writer. Not examined further: the file holds the user's own settings.
- macOS and Linux.

## Repeat

The fixture is in place in `~/wave-rehearsal-desktop-20261126-0416`; to start from scratch, build it again
(PowerShell; `<scratch>` is a new folder outside every repository and outside the temp folder):

```powershell
$s = "$HOME\wave-rehearsal-desktop-$(Get-Date -Format yyyyMMdd-HHmm)"; $t = "$s\textkit"
New-Item -ItemType Directory "$t\textkit", "$t\tests", "$s\evidence" | Out-Null
git -C $t init -b main; git -C $t config user.name rehearsal; git -C $t config user.email rehearsal@example.invalid
# files of "Fixture (both)": textkit/__init__.py, tests/test_smoke.py, README.md, .gitignore
python -m venv "$s\venv"; & "$s\venv\Scripts\python.exe" -m pip install pytest
& "<working folder>\install.ps1" -Target $t
Add-Content "$t\.gitignore" ".agents/"; git -C $t add -A; git -C $t commit -m "Seed textkit with wave skills"
# write $t\.codex\config.toml with the profile of README "Codex permissions" (<parent> = $s, <project> = $t)
Add-Content "$t\.git\info\exclude" ".codex/"
(Get-FileHash "$HOME\.codex\config.toml").Hash > "$s\evidence\config-hash-before.txt"
Select-String "$HOME\.codex\config.toml" -Pattern '^\[projects\.' > "$s\evidence\projects-before.txt"
```

Then, with desktop control of the app "ChatGPT" granted to the agent that runs the rehearsal: E0–E4 as in
"Rehearsal E" and "Rehearsal E2" of the plan (`solutions/P2-codex-coordinator.md`), and the checks from the newest
rollout files under `~/.codex/sessions/`.
