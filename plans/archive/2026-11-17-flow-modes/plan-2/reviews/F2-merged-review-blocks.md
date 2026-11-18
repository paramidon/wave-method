# F2 · Merged features shown with their review block

- Branch: `feat/flow-modes-p2/F2-merged-review-blocks` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p2-F2`
- 👀 review since 2026-11-17 20:30

## Essence

After an autonomous wave, each feature merged into integration gets a full review block with its changes, how to test them, the merge hash, and the reason for approval. Wave-status shows these blocks until the feature reaches main.

## How to test

1. Finish an autonomous wave that merges one feature and leaves another for review. The report shows the merged feature with its integration branch, hash, test steps, and approval. The other feature gets its review block.
2. Run wave-status for that plan before and after merging integration into main. The merged feature appears under “Merged, not in main” before the merge and disappears from that section afterward.

## Worth a look

The review brief retains the approval reason for both automatic approval and approval by the user in autonomous flow.

## Tasks

- F (wave 2) — Defined the full merged review block and added integration merge and approval details to the review brief template.
- G (wave 2) — Updated autonomous reports and wave-status to show full merged review blocks and recorded approvals in feature briefs.

## Check

- `python skills/wave-plan/scripts/test_status_check.py` passed all 20 tests.
- `python skills/wave-plan/scripts/status_check.py` passed on `examples/01-greenfield-todo-cli` and `examples/02-bugfix-batch`.
- `git diff --check` and `git diff --check main...HEAD` passed.
- Four instruction walkthroughs passed.
