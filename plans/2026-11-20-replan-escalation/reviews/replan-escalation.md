# F1 · Re-plan escalation

- Branch: `feat/replan-escalation/F1-replan-escalation` · worktree: `D:/Documents/orbits/wave-method.worktrees/replan-escalation-F1`
- 👀 review since 2026-11-21 00:33

## Essence

Re-plans used to repeat without a per-feature limit. The planner now escalates the second round and holds the third
until the user gives direction. When verification by running a command is unavailable, the planner records why and
describes the check it performed.

## How to test

1. Copy `examples/02-bugfix-batch` to a scratch folder. Replace `- Re-plans: none` with `- Re-plans:` and two indented
   entries ending in ` · fixes: F1 (I1)` and ` · fixes: F1 (I2)`. Run `skills/wave-plan/scripts/status_check.py` on that
   copy → it reports one `replan-escalation` issue, which disappears after you append ` · escalated: F1` to the second
   entry.
2. Check the status report for features with one and two recorded re-plans → it shows `escalated` and `held` as the
   respective next rounds, with the override command for the held feature. An escalated feature in autonomous flow
   appears on the manual review list.
3. Read step 3 of `Re-plan escalation` in the layout, steps 2 and 8 in the planner skill, and the solution template's
   `Evidence` line → they accept `not verifiable by running: <why>` with the alternative check performed.

## Worth a look

The re-plan count is per feature and includes fixes for problems found during waves.

## Tasks

- A (wave 1) — Defined the escalation rule, evidence requirements and README record format.
- B (wave 1) — Added planner instructions for escalated and held re-plans and autonomous manual review.
- C (wave 1) — Added validation of re-plan records and six tests.
- D (wave 1) — Added re-plan counts and next-round guidance to reports and retained manual review for escalated features.
- E (wave 1) — Documented the workflow and verified the seven feature acceptance checks.
- F (wave 2) — Allowed the evidence fallback in both the planner's code analysis and its self-check.
- G (wave 2) — Added the fallback and alternative-check instruction to the solution template.

## Check

`python skills/wave-plan/scripts/test_status_check.py` → 39 passed.
`python -m unittest discover -s scripts/tests` → 59 passed.
`python skills/wave-plan/scripts/status_check.py <example>` → all three examples passed.
`git diff --check` and `git diff --check main...HEAD` → clean.
Tests added in wave 1: `skills/wave-plan/scripts/test_status_check.py`.
