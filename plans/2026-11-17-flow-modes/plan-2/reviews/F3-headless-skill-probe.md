# F3 · Print-mode findings for the driver

- Branch: `feat/flow-modes-p2/F3-headless-skill-probe` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p2-F3`
- 👀 review since 2026-11-17 21:55

## Essence

The driver has measured Claude Code print-mode results for triage, planning, wave execution and status. The guide specifies the prompt forms, observed permission behavior, shell quoting and trial caps for each skill.

## How to test

1. Open `docs/claude-print-mode.md` → the driver table gives slash prompts and measured starting caps, and Q-a through Q-d give the behavior on Git Bash and both PowerShell versions.
2. Open `docs/rehearsals/print-mode-chain.md` → the four runs show exit codes, costs, turns and Git checks from an autonomous chain that merged its feature into the integration branch.

## Worth a look

The status report included the full merged-feature block with a changed heading. The caps are based on a one-wave run; I9 and I10 track both follow-up checks.

## Tasks

- H (wave 2) — Recorded P-a through P-f for skill invocation, JSON results, and permission handling.
- N — ➖ superseded by S: moved to wave 6 after F1's review.
- O — ➖ superseded by T: moved to wave 6 after F1's review.
- S (wave 6) — Ran and recorded the four-stage autonomous chain in a scratch repository.
- T (wave 6) — Measured permission modes and PowerShell behavior, verified the prompt forms, and updated the driver guide.

## Check

`python skills/wave-plan/scripts/test_status_check.py` → all 20 tests passed.
`python skills/wave-plan/scripts/status_check.py examples/01-greenfield-todo-cli` and
`python skills/wave-plan/scripts/status_check.py examples/02-bugfix-batch` → both passed.
`git diff --check` and `git diff --check main...HEAD` → clean. The doc acceptance checks passed.
