# F1 · README, autonomous example, Flow checks and changelog for both flows

- Branch: `feat/flow-modes-p4/F1-flow-docs-and-checks` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p4-F1`
- 👀 review since 2026-11-18 17:16

## Essence

The project documents manual and autonomous flow, including the overnight driver's integration branch and morning review. The example catalog includes a complete autonomous Wordstat CLI plan, and the plan validator checks the optional Flow header.

## How to test

1. Open “Overnight runs (autonomous flow)” in the project README → it describes both flows, the driver commands and morning review.
2. Open the example catalog and follow example 03 → the plan targets `integration/wordstat-cli`, schedules four features in two waves and keeps F3 for manual review.
3. Change the Flow line in a copy of example 03 to `- Flow: autonomus` and run `python skills/wave-plan/scripts/status_check.py <copy>` → exit 1 with a single `flow-line` diagnostic.
4. Open the changelog → `Unreleased` is the first entry.

## Worth a look

The example's empty baseline has a successful check, so the README-only F3 can reach manual review. The packaging configuration explicitly selects `wordstat` so a checkout that also contains `plans/` can build the wheel.

## Tasks

- A (wave 1) — Documented both flows, the overnight driver and morning review of its integration branch.
- B — ➖ superseded by G in wave 3.
- C (wave 1) — Validated the optional Flow header and added coverage for valid and malformed flow declarations.
- D (wave 1) — Documented the changes, included the driver in release archives and expanded the contributor checks.
- G (wave 3) — Added a complete four-feature Wordstat CLI plan for an autonomous night run with manual review for F3.
- H (wave 3) — Added the night-run plan to the example catalog and verified its empty-baseline check and wheel build in a scratch repository.

## Check

`python skills/wave-plan/scripts/test_status_check.py` → 32 passed. `python -m unittest discover -s scripts/tests` → 59 passed. `status_check.py` on all three examples and `git diff --check main...HEAD` → exit 0. Tests changed in `skills/wave-plan/scripts/test_status_check.py`. P8 and P17 acceptance checks passed.
