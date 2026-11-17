# F1 · Autonomous flow with an integration branch

- Branch: `feat/flow-modes-p1/F1-autonomous-flow` · worktree: `D:\Documents\orbits\wave-method.worktrees\flow-modes-p1-F1`

## How to test

- B: `git grep -n "^## " -- skills/wave-run/autonomous.md` → six headings in order: Flow form, Integration target, Skipped tasks, Points of steps 1–6, Auto-approval, Report
- C: read `skills/wave-run/report.md` → the wave report has a `Flow:` line and an "### Auto-merged" block, the section table has "Flow" and "Auto-merged" rows, and a "## Flow report" section exists
- D: run `/wave-status` on a plan whose README has `- Flow: autonomous · target: integration/<slug>` → a `Flow:` line in the header and an `Integration:` bullet with the commit count and the merge commands; no merge is run

## Tasks

- A (wave 1) — The plan-layout reference now describes a plan's flow: in autonomous flow approved features go into an integration branch that the user reviews and merges, and one decision table shows where manual and autonomous flow differ.
- B (wave 1) — `wave-run` has a new file of autonomous-flow procedures: switching the flow, preparing the integration branch, skipping tasks, the safe answer at each ask point of steps 1–6, auto-approval and the report pointer.
- C (wave 1) — The final reports of `wave-run` show the active flow and, in autonomous flow, list what was auto-merged and why; a new flow report is added for the flow form.
- D (wave 1) — `wave-status` shows a plan's flow and the integration branch waiting for the user's merge; `wave-plan` and the README template know the optional `Flow:` header line.
