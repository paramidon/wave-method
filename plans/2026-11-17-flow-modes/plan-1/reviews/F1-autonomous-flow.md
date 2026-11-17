# F1 · Autonomous flow with an integration branch

- Branch: `feat/flow-modes-p1/F1-autonomous-flow` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p1-F1`
- 👀 review since 2026-11-17 16:28

## Essence

Autonomous flow lets `wave-run` approve eligible features and merge them into an integration branch for the user to review. Manual approval is the default, and a plan can require it for selected features.

## How to test

1. In a scratch repository with a one-feature plan, run `/wave-run <plan folder> flow autonomous` · `$wave-run <plan folder> flow autonomous`, then `/wave-run <plan folder> 1` · `$wave-run <plan folder> 1` → the eligible feature lands on `integration/<plan>` and the report shows `Flow: autonomous` and the reason under `Auto-merged`.
2. Run a wave that completes a feature in a plan without a `Flow:` line → the report shows `Flow: manual` and asks whether to merge the feature.
3. Run `/wave-status <plan folder>` · `$wave-status <plan folder>` for the autonomous plan → the report names the integration branch, lists its commit count, and shows the handoff commands.

## Worth a look

The flow switch accepts `review <F-IDs>` to require manual approval for selected features. I1 and I2 clarify that `main-dirty` refers to the active merge target and define the integration branch name.

## Tasks

- A (wave 1) — The plan-layout reference now describes a plan's flow: in autonomous flow approved features go into an integration branch that the user reviews and merges, and one decision table shows where manual and autonomous flow differ.
- B (wave 1) — `wave-run` has a new file of autonomous-flow procedures: switching the flow, preparing the integration branch, skipping tasks, the safe answer at each ask point of steps 1–6, auto-approval and the report pointer.
- C (wave 1) — The final reports of `wave-run` show the active flow and, in autonomous flow, list what was auto-merged and why; a new flow report is added for the flow form.
- D (wave 1) — `wave-status` shows a plan's flow and the integration branch waiting for the user's merge; `wave-plan` and the README template know the optional `Flow:` header line.
- E — ➖ superseded by G.
- F — ➖ superseded by I.
- G (wave 3) — Connected the flow command, integration safety checks, and auto-approval to the wave and merge procedures.
- H (wave 3) — Clarified which worktree `main-dirty` refers to and defined the integration branch name.
- I (wave 3) — Matched the merge-target checks and report wording across the skills and walked through the four planned scenarios.

## Check

- `python skills/wave-plan/scripts/test_status_check.py` → 20 passed.
- `python skills/wave-plan/scripts/status_check.py examples/01-greenfield-todo-cli` → passed.
- `python skills/wave-plan/scripts/status_check.py examples/02-bugfix-batch` → passed.
- `git diff --check main...HEAD` → clean.
- Scratch smoke test passed: the feature merge `be51a0a` included `Approved-By: wave-run autonomous flow`, integration HEAD `2e62de3` included the tracking branch, and scratch main stayed at `df39024`. The report recorded the auto-approval reason.
