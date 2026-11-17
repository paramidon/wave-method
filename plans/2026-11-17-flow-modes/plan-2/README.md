# Flow modes, part 2: autonomous planning, chained parts, merged review blocks, print-mode probe

- Plan: `plans/2026-11-17-flow-modes/plan-2/` · slug: `flow-modes-p2` · tracking branch: `plan/flow-modes-p2` · created 2026-11-17 · base: fc815cd · planned 2026-11-17 16:34 – 2026-11-17 16:45
- Index: `plans/2026-11-17-flow-modes/index.md` part 2
- Re-plans: none

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `autonomous-planning` | Triage and planning in autonomous flow, chained parts on one integration branch | P4, P10 | A (1), B (1), C (1), D (1), E (1) | task E's 12 walkthroughs hold and the check command is green | ⬜ | wave 1 | | |
| F2 | `merged-review-blocks` | Merged features shown with their review block | P11 | F (2), G (2) | task G's 4 walkthroughs hold and the check command is green | ⬜ | wave 2 | | |
| F3 | `headless-skill-probe` | Print-mode findings for the driver | P7 | H (2) | `docs/claude-print-mode.md` has all six sections and every probe P-a…P-f recorded | ⬜ | wave 2 | | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D, E (after A, B, C, D) | ⬜ |
| 2 | `waves/w02.md` | F, G (after F), H | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `layout-planning-rules` | F1 | 1 | medium | ⬜ |
| B | `wave-plan-autonomous` | F1 | 1 | medium | ⬜ |
| C | `triage-status-autonomous` | F1 | 1 | medium | ⬜ |
| D | `wave-run-plan-lookup` | F1 | 1 | low | ⬜ |
| E | `planning-closing-check` | F1 | 1 | medium | ⬜ |
| F | `merged-block-layout` | F2 | 2 | medium | ⬜ |
| G | `merged-block-readers` | F2 | 2 | medium | ⬜ |
| H | `print-mode-probe` | F3 | 2 | medium | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/flow-modes-p2` and reach the
main branch with each feature merge.

## User problems

- P4 — in autonomous flow `wave-triage` and `wave-plan` proceed on stated assumptions, recorded in the index and README "Assumptions", instead of asking → F1 · `solutions/P4-planning-assumptions.md`
- P7 — verify against the docs and real runs whether `claude -p` runs skills from a slash command or needs the skill named in words; design the driver prompts around it → F3 · `solutions/lite.md` (low)
- P10 — in autonomous flow "plan after part J is merged" checks the integration target; the part's tracking branch is created from and merged into it; an unmerged part J feature stops the part with a clear line → F1 · `solutions/P10-chained-parts.md`
- P11 — after an autonomous run every merged and every `👀 review` feature is shown with its review block (essence, how to test, no how-to-build) → F2 · `solutions/P11-merged-review-blocks.md`

## How to try

- F1 — run `/wave-triage flow autonomous <a list with one ambiguous item>` in a scratch repository → no question; the index has `- Flow: autonomous · target: integration/<topic>` and an `Assumed (autonomous, not asked)` line; then `/wave-plan <index> part 2` while part 1 has a feature still `👀 review` → `Stop part-unmerged: part 1 — F… 👀 review (review) — next: …`, nothing created; once part 1 is merged into `integration/<topic>`, the same command plans part 2 on that branch and `main` stays unchanged; before: both skills asked questions, and part 2 waited for part 1 on `main`.
- F2 — after an autonomous wave that merged a feature, the wave report's "Auto-merged" shows its full block (merged into `integration/<name>` with the hash, essence, how to test, `Approved: auto — …`), and `/wave-status <plan>` shows it under `Merged, not in main:` until you merge the integration branch; before: one line with the essence only, and nothing in `wave-status`.
- F3 — open `docs/claude-print-mode.md` → it says, from real `claude -p` runs, whether `/wave-status` runs the skill in print mode, and gives the prompt and flags per skill for the driver; before: an unverified guess.

## Known test failures before start

- none (`main` at fc815cd: `test_status_check.py` 20 tests OK, both examples pass `status_check.py`, `git diff --check` clean)

## Assumptions

- P4 and P10 are one feature: both define how `wave-plan` behaves in autonomous flow and edit the same files; P10's chain check needs P4's flow of planning to know the flow at all.
- The flow of planning comes from `flow <manual|autonomous>` as the first two words of the arguments, else the index's `Flow:` line, else manual; a driver (part 3) states it in the command.
- In autonomous flow a guessed reading does not put its feature under manual review: it is shown under "Worth a look" in the review block, so the night still makes progress and the user sees every guess on the integration branch.
- All parts of an index in autonomous flow share `integration/<topic>`; plans sharing it never run waves at the same time (lock via `wave-running`). A plan of autonomous flow then lives on the integration branch until the user merges it, so `wave-run` and `wave-status` learn to find it on its tracking branch.
- `wave-triage` keeps merging the index into the main branch in both flows: it writes no code and the index must be visible to the part commands.
- P11 adds no new file: the review brief, kept on the tracking branch after the merge, is the source of the "merged block" in the report, in `wave-status` and in the part 3 driver's summary.
- P7's result is a doc in the repository (`docs/claude-print-mode.md`), the input for part 3's plan; its task is medium, not low (see wave 2). It needs the Claude Code CLI, which is not installed on 2026-11-17: install and sign in before wave 2, or run task H in task mode from a session that has it.
- No `CHANGELOG.md` or README change here: part 4 (P8) documents the whole flow.
