# Flow modes, part 1: autonomous flow in wave-run

- Plan: `plans/2026-11-17-flow-modes/plan-1/` · slug: `flow-modes-p1` · tracking branch: `plan/flow-modes-p1` · created 2026-11-17 · base: 5a69c15 · planned 2026-11-17 15:33 – 2026-11-17 15:45
- Index: `plans/2026-11-17-flow-modes/index.md` part 1
- Re-plans:
  - 2026-11-17 at e83a4f1, 16:06 – 16:12: I1, I2 → P12, P13; wave 2 dropped, E → G and F → I in wave 3, new task H

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `autonomous-flow` | Autonomous flow with an integration branch | P1, P2, P3, P5, P12, P13 | A (1), B (1), C (1), D (1), E (2) ➖, F (2) ➖, G (3), H (3), I (3) | task I's four scenario walkthroughs hold and the check command is green | 🔄 | wave 3 | `feat/flow-modes-p1/F1-autonomous-flow` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D | ⚠️ I1, I2 → task H (wave 3) |
| 2 | `waves/w02.md` | E, F (after E) | ➖ dropped (tasks → wave 3) |
| 3 | `waves/w03.md` | G, H, I (after G, H) | 🔄 since 2026-11-17 16:15 |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `layout-flow-section` | F1 | 1 | medium | ⚠️ I1, I2 → task H |
| B | `autonomous-procedures` | F1 | 1 | medium | ✅ |
| C | `report-flow-lines` | F1 | 1 | low | ✅ |
| D | `status-plan-flow-pointers` | F1 | 1 | low | ✅ |
| E | `wave-run-flow-pointers` | F1 | 2 | medium | ➖ superseded by G |
| F | `flow-consistency-pass` | F1 | 2 | medium | ➖ superseded by I |
| G | `wave-run-flow-wiring` | F1 | 3 | medium | 🔄 |
| H | `main-dirty-name-wording` | F1 | 3 | low | 🔄 |
| I | `flow-closing-check` | F1 | 3 | medium | 🔄 |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/flow-modes-p1` and reach the
main branch with each feature merge.

## User problems

- P1 — a per-plan flow (`manual` default, `autonomous`), switchable between waves, overridable per feature, with one decision table in `layout.md` → F1 · `solutions/P1-flow-field.md`
- P2 — autonomous merges go to an integration branch the user reviews as one diff and merges; refuse to start when that cannot be guaranteed → F1 · `solutions/P2-integration-target.md`
- P3 — `wave-run` in autonomous flow never asks: auto-approval under five conditions and a defined answer per ask point, in a new `wave-run/autonomous.md` → F1 · `solutions/P3-autonomous-wave-run.md`
- P5 — the final reports show the active flow and, in autonomous flow, what was auto-merged and why → F1 · `solutions/lite.md` (low)
- P12 — `main-dirty` and the readiness sentences say "the main checkout" where autonomous flow means `<main checkout>`, the integration worktree (I1) → F1 · `solutions/lite.md` (low)
- P13 — `<name>` of `integration/<name>` is defined nowhere; add it to `layout.md` "Names" (I2) → F1 · `solutions/lite.md` (low)

## How to try

- F1 — in a scratch repository with a small one-feature plan, run `/wave-run <plan folder> flow autonomous`, then `/wave-run <plan folder> 1` → the ready feature is merged into `integration/<plan>` without a question, the report shows `Flow: autonomous` and an "Auto-merged" line with the reason, and `main` is unchanged; a plan without a `Flow:` line still asks `Merge F1 …?` and its report shows `Flow: manual`; before: every ready feature waited for the user's merge approval.

## Known test failures before start

- none (`main` at 5a69c15: `test_status_check.py` 20 tests OK, both examples pass `status_check.py`)
- none (`feat/flow-modes-p1/F1-autonomous-flow` at e83a4f1, after wave 1: the same check green, `git diff --check` clean)

## Assumptions

- The feature is one: the flow field, the integration branch, wave-run's autonomous answers and the report lines are useless or misleading without each other.
- Integration target = an integration branch `integration/<name>` (default `<name>` = plan slug) with its own worktree; in autonomous flow `<main>`/`<main checkout>` resolve to it, so `merge.md` mechanics stay unchanged. Night clone rejected (see `solutions/P2-integration-target.md`); a driver may still run inside a clone.
- `wave-plan` and `wave-triage` ignore the flow in this part; their questions and "plan after part K is merged" join the decision table in part 2 (P4, P10). Sharing one integration branch across index parts is part 2's design (P10).
- The flow is switched with a new `wave-run` form, `flow <manual|autonomous> [review <F-IDs>]`; manual-review features are a list in the `Flow:` line, not a Features column.
- In autonomous flow a feature with an unplanned open entry (`status: open`) gets no new tasks in later waves (they are skipped, ⚠️); planned entries (`→ task`) do not block.
- In autonomous flow the plan is not archived and feature branches are kept until the user merged the integration branch.
- The `CHANGELOG.md` "Unreleased" line for flow modes is written in part 4 (P8), as the index assigns it; this part does not touch `CHANGELOG.md`.
- The index's 2–3-task estimate for P2 held: `<main>` keeps meaning "the merge target", so P5 stays in this part.
- Re-plan 2026-11-17: P12 and P13 are found problems of F1, numbered after the index's P11. Every other bare "the main checkout" in `skills/` means the repository's real main checkout and stays (`solutions/lite.md`, P12).
