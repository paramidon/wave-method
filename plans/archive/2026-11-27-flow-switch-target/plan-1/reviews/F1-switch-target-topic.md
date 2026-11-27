# F1 · Switched index parts share the index's integration branch

- Branch: `feat/flow-switch-target-p1/F1-switch-target-topic` · worktree: `D:\Documents\orbits\wave-method.worktrees\flow-switch-target-p1-F1`
- 👀 review since 2026-11-27 23:51

## Essence

An index part switched to autonomous flow with `/wave-run <plan folder> flow autonomous` now merges into the index's
shared `integration/<topic>`, as parts planned that way do; before, it got its own `integration/<topic>-p<K>`. The
status check reports a wrong target as `flow-target`.

## How to test

1. In a repository with an index part planned in manual flow, run
   `/wave-run plans/<date>-<topic>/plan-<K> flow autonomous` → the plan README header reads
   `- Flow: autonomous · target: integration/<topic>`.
2. In such a README change the target to `integration/<topic>-p<K>` and run
   `python skills/wave-plan/scripts/status_check.py <plan folder>` → one `flow-target` line.

## Worth a look

- Step 1 shows the new behaviour only with the new skill text: the installed copy in `.claude/skills/` is not changed
  by this feature.
- A part already switched to `integration/<plan slug>` is not migrated; the status check now reports it.
- The switch was rehearsed only by the coordinator, by hand, not by a separate agent session.

## Tasks

- A (wave 1) — The skill texts, the README and the changelog say that an index part, also one switched later, merges
  into `integration/<topic>`.
- B (wave 1) — The status check reports `flow-target` for an index part in autonomous flow whose target is another
  branch; a missing target is not reported.

## Check

`python skills/wave-plan/scripts/test_status_check.py` → 43 tests OK; `status_check.py` on `examples/*/` → no output;
`git diff --check main...HEAD` → no output; tests added: `skills/wave-plan/scripts/test_status_check.py` (4).
