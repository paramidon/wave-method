# F1 · Re-plan escalation

- Branch: `feat/replan-escalation/F1-replan-escalation` · worktree: `D:/Documents/orbits/wave-method.worktrees/replan-escalation-F1`
- ⚠️ blocked on I2

## How to test

- C: Run the status checker on a scratch copy of the bugfix example with two re-plans for F1. The second re-plan triggers `replan-escalation` until it is marked `escalated: F1`.
- D: Check a status report for a feature with one re-plan and another with two. Expect `escalated` and `held` respectively, with the override command for the held feature. An escalated feature stays on the autonomous manual-review list.
- E: Read the re-plan escalation section linked from the README and check the steps for the second and third re-plans.

## Tasks

- A (wave 1) — Defined the escalation rule, evidence requirements and README record format.
- C (wave 1) — Added validation of re-plan records and six tests.
- D (wave 1) — Added re-plan counts and next-round guidance to reports and retained manual review for escalated features.
- E (wave 1) — Documented the workflow and verified the seven feature acceptance checks.
