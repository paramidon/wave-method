# F2 · End-to-end runs of both flows on scratch repositories, and the fixes they found

- Branch: `feat/flow-modes-p4/F2-end-to-end-rehearsal` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p4-F2`
- 👀 review since 2026-11-19 02:59

## Essence

The isolated rehearsal records show manual flow through archiving with both the current skills and v2.12.0, and show how the autonomous driver handles clean tasks, out-of-scope commits, and a forced test failure. The accompanying fixes enforce task scope and readable model trailers, record merge times from Git, and let example 01's CI run independently of its application package.

## How to test

1. Open `docs/rehearsals/end-to-end-manual.md` and follow both runs through M6 → both archive the plan after merging F1 and F3. The current F1 and F3 M5 timestamps match their Git merge commits.
2. Read M6 in the same record → the baseline passes 13 tests, including two extra cases, and the current status report confirms there are no active plans.
3. Open `docs/rehearsals/end-to-end-autonomous.md` → F1 and F3 merge into the integration branch. F2's out-of-scope file and F4's forced red test leave both features blocked with empty merge cells.
4. In a scratch autonomous task, commit an out-of-scope file and delete it in a second commit → the coordinator detects it in the commit history and holds back auto-approval. Use Git's trailer parser on an in-scope task commit → it returns the declared `Wave-Model` value.
5. Run example 01's CI command on F3 before F1 merges → the check succeeds when no tests are collected.

## Worth a look

The M5 rescan accepts merge records written as plain lines or as Markdown list items. It recovered both current timestamps and gave the same baseline output as the first scan.

## Tasks

- K (wave 5) — Check every task commit for out-of-scope files and require clean scope for auto-approval.
- L (wave 5) — Reject merge hashes on unmerged features and limit merge records to the affected feature rows.
- M (wave 5) — Supply the full README session for example 01 and record the fixes in the changelog.
- P (wave 7) — Require a single trailer block and verify the model with Git.
- R (wave 7) — Complete the isolated autonomous rehearsal and verify that the scope gate reverts out-of-scope work and holds the feature back.
- S (wave 8) — Make example 01's CI independent of the application package so F3 can pass in isolation.
- T (wave 8) — Take Merged entry times from their merge commits in manual and autonomous flow.
- U (wave 8) — Preserve the isolated manual run through M4. V verified the continuation from that state.
- V (wave 9) — Continue the preserved manual run through M6 for both skill versions and record the archives and Git evidence.
- W (wave 10) — Recover the current M5 timestamps and correct the M6 expectations for baseline tests and archived-plan status.

## Check

`python skills/wave-plan/scripts/test_status_check.py`, `python -m unittest discover -s scripts/tests`, `python skills/wave-plan/scripts/status_check.py` for each example, and `git diff --check` → 33 status-check tests and 59 driver tests passed, all three examples passed, and whitespace checks were clean. The feature extends `skills/wave-plan/scripts/test_status_check.py` to cover merge fields.
