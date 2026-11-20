# Re-plan escalation: count re-plans per feature, escalate the second, hold the third

- Plan: `plans/2026-11-20-replan-escalation/` · slug: `replan-escalation` · tracking branch: `plan/replan-escalation` · created 2026-11-20 · base: 6c73979 · planned 2026-11-20 19:58 – 2026-11-20 20:34
- Re-plans: none

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `replan-escalation` | Re-plans of a feature are counted; the second is escalated, the third waits for the user | P1 | A (1), B (1), C (1), D (1), E (1) | acceptance tests 1–7 of `solutions/P1-replan-escalation.md` hold (task E): 39 status-check tests and 59 driver tests OK, all three examples pass, the escalated/held rules and the override command are in `layout.md`, `wave-plan`, `wave-run` and `wave-status` | ⚠️ blocked (I2) | I2 | `feat/replan-escalation/F1-replan-escalation` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D, E (after A, B, C, D) | ⚠️ I2 |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `escalation-rule-layout` | F1 | 1 | medium | ✅ |
| B | `escalation-in-wave-plan` | F1 | 1 | medium | ⚠️ I2 |
| C | `replan-record-check` | F1 | 1 | medium | ✅ |
| D | `replan-count-shown` | F1 | 1 | medium | ✅ |
| E | `escalation-docs` | F1 | 1 | low | ✅ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/replan-escalation` and
reach the main branch with each feature merge.

## User problems

- P1 — An executor that meets a plan error sends the plan back to `wave-plan`, and the same feature can cycle
  between planner and executor many times; count re-plans per feature, escalate the second (verify by running code,
  high tasks, manual review in autonomous flow), hold the third until the user decides, and show the count in
  `wave-run` and `wave-status` → F1 · `solutions/P1-replan-escalation.md`

## How to try

- F1 — copy `examples/02-bugfix-batch` to a scratch folder, replace its `- Re-plans: none` with `- Re-plans:` and the
  sub-items `  - 2026-11-21 at abc1234, 10:00 – 10:10: t · fixes: F1 (I1)` and
  `  - 2026-11-22 at abc1235, 10:00 – 10:10: t · fixes: F1 (I2)`, run `skills/wave-plan/scripts/status_check.py` on
  it → one `replan-escalation` line; append ` · escalated: F1` to the second sub-item → no output; before: no check
  of re-plans at all. Then read `skills/wave-plan/layout.md`, "Re-plan escalation".

## Known test failures before start

- none (`main` at 6c73979: 33 status-check tests and 59 driver tests OK, all three examples pass)

## Assumptions

- Counted per feature, not per problem entry: an error that shifts to another task of the same feature still counts
  (decided with the user, 2026-11-20).
- Only entries found in a wave count; the user's review rejections (`[I<n> · review / …]`) do not (decided with the
  user).
- Round 3 is a hard limit in both flows; only `/wave-plan <plan folder> override F<k>: <direction>` passes it
  (decided with the user).
- Autonomous flow, round 2: the re-plan goes on and adds the feature to `manual review:` (decided with the user).
- The count lives in the README `Re-plans:` sub-items, not in a new "Features" column, so READMEs, the table parser
  and the examples keep their format; old sub-items without parts count as zero.
- The overnight driver never re-plans (re-planning is a user action), so it is not changed.
