# Flow modes, part 2: autonomous planning, chained parts, merged review blocks, print-mode probe

- Plan: `plans/2026-11-17-flow-modes/plan-2/` · slug: `flow-modes-p2` · tracking branch: `plan/flow-modes-p2` · created 2026-11-17 · base: fc815cd · planned 2026-11-17 16:34 – 2026-11-17 16:45
- Index: `plans/2026-11-17-flow-modes/index.md` part 2
- Re-plans:
  - 2026-11-17 at ff668d6, 17:43 – 17:52: I1–I4 → P12, wave 3 (tasks I–M); details in `history.md`
  - 2026-11-17 at 855d09b, 20:33 – 20:38: I5–I6 → P13, wave 4 (tasks N, O); details in `history.md`
  - 2026-11-17 at 06e0731, 20:56 – 21:02: I7–I8 → P14, wave 5 (tasks P, Q); wave 4 dropped, N, O → wave 6 (S, T); details in `history.md`

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `autonomous-planning` | Triage and planning in autonomous flow, chained parts on one integration branch | P4, P10, P12 | A (1), B (1), C (1), D (1), E (1), I (3), J (3), K (3), L (3), M (3), P (5), Q (5) | task E's 12 walkthroughs hold, the rehearsal scenarios 1–6 of tasks L and M and 7–8 of task Q hold, and the check command is green | ✅ merged | | `feat/flow-modes-p2/F1-autonomous-planning` | bbd2449 |
| F2 | `merged-review-blocks` | Merged features shown with their review block | P11 | F (2), G (2) | task G's 4 walkthroughs hold and the check command is green | ✅ merged | | `feat/flow-modes-p2/F2-merged-review-blocks` | 47d69de |
| F3 | `headless-skill-probe` | Print-mode findings for the driver | P7, P13 | H (2), N (4), O (4), S (6), T (6) | `docs/claude-print-mode.md` has all six sections, probes P-a…P-f and Q-a…Q-d recorded and a prompt table that matches the merged skill texts; `docs/rehearsals/print-mode-chain.md` records a real triage → plan → wave-run → status chain | ⚠️ blocked (I5, I6) | wave 6 | `feat/flow-modes-p2/F3-headless-skill-probe` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D, E (after A, B, C, D) | ✅ (fixed by I–M, wave 3) |
| 2 | `waves/w02.md` | F, G (after F), H | ⚠️ I5, I6 |
| 3 | `waves/w03.md` | I, J, K, L (after I, J, K), M (after I, J, K) | ✅ (fixed by P, Q, wave 5) |
| 4 | `waves/w04.md` | N, O (after N) | ➖ dropped (tasks → wave 6) |
| 5 | `waves/w05.md` | P, Q (after P) | ✅ |
| 6 | `waves/w06.md` | S, T (after S) | 🔄 since 2026-11-17 21:35 |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `layout-planning-rules` | F1 | 1 | medium | ✅ (fixed by I, J, wave 3) |
| B | `wave-plan-autonomous` | F1 | 1 | medium | ✅ |
| C | `triage-status-autonomous` | F1 | 1 | medium | ✅ |
| D | `wave-run-plan-lookup` | F1 | 1 | low | ✅ |
| E | `planning-closing-check` | F1 | 1 | medium | ✅ (fixed by I–M, wave 3) |
| F | `merged-block-layout` | F2 | 2 | medium | ✅ |
| G | `merged-block-readers` | F2 | 2 | medium | ✅ |
| H | `print-mode-probe` | F3 | 2 | medium | ⚠️ I5, I6 |
| I | `target-claim-layout` | F1 | 3 | medium | ✅ (fixed by P, Q, wave 5) |
| J | `wave-plan-claim-order` | F1 | 3 | low | ✅ |
| K | `run-status-claim` | F1 | 3 | medium | ✅ |
| L | `autonomous-index-rehearsal` | F1 | 3 | medium | ✅ |
| M | `chain-safety-rehearsal` | F1 | 3 | medium | ✅ (fixed by P, Q, wave 5) |
| N | `print-mode-chain-runs` | F3 | 4 | medium | ➖ superseded by S |
| O | `print-mode-doc-update` | F3 | 4 | medium | ➖ superseded by T |
| P | `claim-handoff-texts` | F1 | 5 | low | ✅ |
| Q | `claim-handoff-rehearsal` | F1 | 5 | medium | ✅ |
| S | `print-mode-chain-runs` | F3 | 6 | medium | 🔄 |
| T | `print-mode-doc-update` | F3 | 6 | medium | 🔄 |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/flow-modes-p2` and reach the
main branch with each feature merge.

## User problems

- P4 — in autonomous flow `wave-triage` and `wave-plan` proceed on stated assumptions, recorded in the index and README "Assumptions", instead of asking → F1 · `solutions/P4-planning-assumptions.md`
- P7 — verify against the docs and real runs whether `claude -p` runs skills from a slash command or needs the skill named in words; design the driver prompts around it → F3 · `solutions/lite.md` (low)
- P10 — in autonomous flow "plan after part J is merged" checks the integration target; the part's tracking branch is created from and merged into it; an unmerged part J feature stops the part with a clear line → F1 · `solutions/P10-chained-parts.md`
- P12 — re-plan of I1–I4: part J's README found also on the main branch, no write before `plan-exists`, an atomic claim of the shared integration branch, a live rehearsal of autonomous triage and chained planning → F1 · `solutions/P12-chain-safety.md`
- P13 — re-plan of I5–I6: real `claude -p` runs of `wave-triage`, `wave-plan`, `wave-run` and `wave-status` in the driver form, the `auto` and `dontAsk` modes and PowerShell probed, and the driver prompt table checked against F1's merged forms → F3 · `solutions/P13-print-mode-runs.md`
- P14 — re-plan of I7–I8: a wave waiting for task mode marks its claim as waiting, exactly one resume takes it over by compare-and-swap, every holder line carries a run token, and "nothing written" after a refused claim is stated for refs, worktrees and commits (one unreachable blob may remain) → F1 · `solutions/P14-claim-handoff.md`
- P11 — after an autonomous run every merged and every `👀 review` feature is shown with its review block (essence, how to test, no how-to-build) → F2 · `solutions/P11-merged-review-blocks.md`

## How to try

- F1 — run `/wave-triage flow autonomous <a list with one ambiguous item>` in a scratch repository → no question; the index has `- Flow: autonomous · target: integration/<topic>` and an `Assumed (autonomous, not asked)` line; then `/wave-plan <index> part 2` while part 1 has a feature still `👀 review` → `Stop part-unmerged: part 1 — F… 👀 review (review) — next: …`, nothing created; once part 1 is merged into `integration/<topic>`, the same command plans part 2 on that branch and `main` stays unchanged; a second planning or wave run on that branch while one runs → `Stop wave-running: … <holder line>`, and `/wave-status` shows `claimed by <holder line>`; two resumes of a wave waiting for task mode at once → exactly one goes on, the other stops `wave-running` naming it; `docs/rehearsals/*.md` list the commands that repeat every scenario; before: both skills asked questions, and part 2 waited for part 1 on `main`.
- F2 — after an autonomous wave that merged a feature, the wave report's "Auto-merged" shows its full block (merged into `integration/<name>` with the hash, essence, how to test, `Approved: auto — …`), and `/wave-status <plan>` shows it under `Merged, not in main:` until you merge the integration branch; before: one line with the essence only, and nothing in `wave-status`.
- F3 — open `docs/claude-print-mode.md` → it says, from real `claude -p` runs of all four skills, how print mode runs them, and gives the prompt, flags, turn and budget caps per skill (Git Bash and PowerShell) for the driver; `/wave-run <plan folder>` with no flow form for a plan of an autonomous index; `docs/rehearsals/print-mode-chain.md` shows the measured chain; before: an unverified guess, probed on `wave-status` only.

## Known test failures before start

- none (`main` at fc815cd: `test_status_check.py` 20 tests OK, both examples pass `status_check.py`, `git diff --check` clean)
- none on `feat/flow-modes-p2/F1-autonomous-planning` at 1c65676 (re-plan, 2026-11-17: the same check green)
- none on `main` at 0d9c78d and on `feat/flow-modes-p2/F3-headless-skill-probe` at 07200f3 (re-plan 2, 2026-11-17: the same check green)
- none on `main` at 50583bc, on `feat/flow-modes-p2/F1-autonomous-planning` at 6206f9d and on F3's branch at 07200f3 (re-plan 3, 2026-11-17: the same check green)

## Assumptions

- P4 and P10 are one feature: both define how `wave-plan` behaves in autonomous flow and edit the same files; P10's chain check needs P4's flow of planning to know the flow at all.
- The flow of planning comes from `flow <manual|autonomous>` as the first two words of the arguments, else the index's `Flow:` line, else manual; a driver (part 3) states it in the command.
- In autonomous flow a guessed reading does not put its feature under manual review: it is shown under "Worth a look" in the review block, so the night still makes progress and the user sees every guess on the integration branch.
- All parts of an index in autonomous flow share `integration/<topic>`; plans sharing it never run waves at the same time (lock via `wave-running`). A plan of autonomous flow then lives on the integration branch until the user merges it, so `wave-run` and `wave-status` learn to find it on its tracking branch.
- `wave-triage` keeps merging the index into the main branch in both flows: it writes no code and the index must be visible to the part commands.
- P11 adds no new file: the review brief, kept on the tracking branch after the merge, is the source of the "merged block" in the report, in `wave-status` and in the part 3 driver's summary.
- P7's result is a doc in the repository (`docs/claude-print-mode.md`), the input for part 3's plan; its task is medium, not low (see wave 2). It needs the Claude Code CLI, which is not installed on 2026-11-17: install and sign in before wave 2, or run task H in task mode from a session that has it.
- No `CHANGELOG.md` or README change here: part 4 (P8) documents the whole flow.
- Re-plan: I1–I4 are one solution (P12) in F1: they all concern the checks of "Chained parts and the integration branch" and F1 is not merged yet.
- Re-plan: the target claim is a git ref `refs/wave-method/claims/integration/<name>` (atomic create with the zero ID, measured on git 2.52); the read of other plans' 🔄 marks stays as a second guard.
- Re-plan: the rehearsals (L, M) only record; a defect they find becomes a problem entry and a re-plan, so they share no files with each other or with I–K. Their records in `docs/rehearsals/` stay in the repository as the way to repeat the scenarios (input for part 4, P9).
- Re-plan: wave 3 runs after wave 2 (`earlier-wave-open`); wave 2 does not touch F1.
- Re-plan 2: I5 and I6 are one solution (P13) in F3; wave 4 depends on `F1 merged`, because the forms to check are F1's and the installed skills must contain F1.
- Re-plan 2: the chain of task N runs with `bypassPermissions` in a scratch repository and spends at most 30 USD by `total_cost_usd`; on a claude.ai subscription that figure is not billed but counts toward usage limits.
- Re-plan 2: wave 4 needs the Claude Code CLI (signed in) for both tasks; if the `wave-run` session's subagents lack it, run them in task mode.
- Re-plan 3: I7 and I8 are one solution (P14) in F1, both about "Target claim"; the fix of the claim text is an exact replacement (task P, low), the rehearsal appends to the existing record (task Q).
- Re-plan 3: wave 4 waited for `F1 merged`, and wave 5 (F1's fixes) could not start while wave 4 was ⬜ (`earlier-wave-open`); so wave 4 is dropped and its tasks run unchanged as S and T in wave 6.
- Re-plan 3: a refused claim keeps writing its holder blob (git needs the object before the ref); the text states that refs, worktrees and commits stay unchanged, not the object store.
