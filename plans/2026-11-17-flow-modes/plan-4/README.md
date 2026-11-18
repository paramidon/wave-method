# Flow modes, part 4: docs, an autonomous example, Flow checks and end-to-end runs

- Plan: `plans/2026-11-17-flow-modes/plan-4/` · slug: `flow-modes-p4` · tracking branch: `plan/flow-modes-p4` · created 2026-11-18 · base: a47af8a · planned 2026-11-18 03:07 – 2026-11-18 03:20
- Index: `plans/2026-11-17-flow-modes/index.md` part 4
- Re-plans:
  - 2026-11-18 at 02d9c4a, 15:31 – 15:40: I1–I3 → P17; I4 closed (plan error); B → G and new H in wave 3; wave 2 dropped, E → I and F → J in wave 4
  - 2026-11-18 at 1e7214e, 17:45 – 17:56: I5–I9 → P18–P21; new K, L, M in wave 5 and N, O in wave 6; I → N, J → O
  - 2026-11-18 at e3cf9f7, 20:33 – 20:42: I7, I8, I12, I14–I17 → P22, P23; I13 closed (plan error); new P, Q, R in wave 7;
    N → Q, O → R
  - 2026-11-18 at a257e9d, 21:16 – 21:23: I18, I20–I22 → P24–P26; I19 closed (plan error); new S, T, U in wave 8; Q → U
  - 2026-11-19 at 5f4bbc3, 01:39 – 01:45: I23 → P27; I20, I21, I23 → new V in wave 9, which continues U's run from its
    preserved M4 state
  - 2026-11-19 at 566fbdf, 02:37 – 02:43: I24–I26 → P28 (wrong expectations of P26, not skill defects); new W in
    wave 10, which rescans and corrects V's record without a Claude call

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `flow-docs-and-checks` | README, autonomous example, Flow checks and changelog for both flows | P8, P17 | A (1), B (1) ➖, C (1), D (1), G (3), H (3) | the six acceptance tests of `solutions/P8-flow-docs.md` and of `solutions/P17-example-03-fixes.md` hold (task H): 32 status-check tests and 59 driver tests OK, all three examples pass `status_check.py`, one `Unreleased` line, README links resolve, example 03 has slug `wordstat-cli`, its check passes on an empty baseline and its package builds | ✅ merged | | `feat/flow-modes-p4/F1-flow-docs-and-checks` | 1fc60af |
| F2 | `end-to-end-rehearsal` | End-to-end runs of both flows on scratch repositories, and the fixes they found | P9, P18–P28 | E (2) ➖, F (2) ➖, I (4) ➖, J (4) ➖, K (5), L (5), M (5), N (6) ➖, O (6) ➖, P (7), Q (7) ➖, R (7), S (8), T (8), U (8), V (9), W (10) | the acceptance tests of `solutions/P18-task-scope-enforcement.md` (task K) and the P19, P20, P23, P24 and P25 checks of `solutions/lite.md` (L, M, P, S, T) hold; `docs/rehearsals/end-to-end-autonomous.md` meets `solutions/P22-third-rehearsal-run.md` "Acceptance tests" (R) and `end-to-end-manual.md` meets `solutions/P26-fourth-manual-run.md` "Acceptance tests" as completed by `solutions/P27-fourth-run-continuation.md` and corrected by `solutions/lite.md` P28 (U, V, W): P0 and the hook probe Pass, nothing written outside scratch, the manual comparison of `cur` and `base` complete through M6 with F1 and F3 merged and the plan archived on both, `cur`'s `Merged` times equal to its merge commits, readable `Wave-Model` trailers, F2 of the scratch night run blocked by its forced out-of-scope file with empty `Merged` cells; the check command green (33 status-check tests, 59 driver tests) | 🔄 | wave 10 | `feat/flow-modes-p4/F2-end-to-end-rehearsal` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D | ✅ (fixed by G and H, wave 3) |
| 2 | `waves/w02.md` | E, F | ➖ dropped (tasks → wave 4) |
| 3 | `waves/w03.md` | G, H (after G) | ✅ |
| 4 | `waves/w04.md` | I, J | ✅ (verified by Q and R, wave 7) |
| 5 | `waves/w05.md` | K, L, M | ✅ |
| 6 | `waves/w06.md` | N, O | ✅ (verified by P, Q and R, wave 7) |
| 7 | `waves/w07.md` | P, Q (after P), R (after P) | ✅ (verified by V, wave 9) |
| 8 | `waves/w08.md` | S, T, U (after S, T) | ✅ (verified by V, wave 9) |
| 9 | `waves/w09.md` | V | ⚠️ I24, I25, I26 |
| 10 | `waves/w10.md` | W | 🔄 since 2026-11-19 02:53 |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `readme-flow-sections` | F1 | 1 | medium | ✅ |
| B | `autonomous-example` | F1 | 1 | medium | ➖ superseded by G |
| C | `status-check-flow` | F1 | 1 | medium | ✅ (I4 closed at the re-plan: the plan's expected line was wrong) |
| D | `changelog-release-files` | F1 | 1 | low | ✅ |
| E | `manual-flow-run` | F2 | 2 | medium | ➖ superseded by I |
| F | `autonomous-flow-run` | F2 | 2 | medium | ➖ superseded by J |
| G | `night-example-plan` | F1 | 3 | medium | ✅ |
| H | `example-index-check` | F1 | 3 | low | ✅ |
| I | `manual-flow-rehearsal` | F2 | 4 | medium | ➖ superseded by N |
| J | `autonomous-flow-rehearsal` | F2 | 4 | medium | ➖ superseded by O |
| K | `task-scope-enforcement` | F2 | 5 | medium | ✅ |
| L | `merged-cell-check` | F2 | 5 | low | ✅ |
| M | `example-session-fixture` | F2 | 5 | low | ✅ |
| N | `manual-flow-rerun` | F2 | 6 | medium | ➖ superseded by Q |
| O | `autonomous-flow-rerun` | F2 | 6 | medium | ➖ superseded by R |
| P | `trailer-block-rule` | F2 | 7 | low | ✅ |
| Q | `manual-flow-third-run` | F2 | 7 | medium | ➖ superseded by U |
| R | `autonomous-flow-third-run` | F2 | 7 | medium | ✅ |
| S | `example-ci-independence` | F2 | 8 | low | ✅ |
| T | `merge-time-from-git` | F2 | 8 | low | ✅ |
| U | `manual-flow-fourth-run` | F2 | 8 | medium | ✅ (verified by V, wave 9) |
| V | `manual-run-continuation` | F2 | 9 | medium | ⚠️ I24, I25, I26 |
| W | `record-expectation-fixes` | F2 | 10 | low | 🔄 |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/flow-modes-p4` and reach the
main branch with each feature merge.

## User problems

- P8 — README, `examples/` (a new autonomous example), `status_check.py` (the README `Flow:` line) and an
  `Unreleased` line in `skills/wave-plan/CHANGELOG.md` describe both flows and the driver; no version bump, no tag
  → F1 · `solutions/P8-flow-docs.md`
- P9 — on throwaway repositories, never a real project: one run in manual flow (compared with `v2.12.0`), one in
  autonomous flow with the driver, a forced red task and a feature that stays blocked; report what happened and what
  could not be verified → F2 · `solutions/P9-end-to-end-runs.md`
- P17 — (re-plan, I1–I3) example 03 as P8 specified it cannot run: a README-only feature never passes `pytest`,
  `pip install .` refuses the repository, the slug breaks the layout → F1 · `solutions/P17-example-03-fixes.md`
- P18 — (re-plan, I8) a task committed bytecode outside its files; the coordinator cleaned it up and auto-approved the
  feature: scope must be checked in every commit and never cleaned up → F2 · `solutions/P18-task-scope-enforcement.md`
- P19 — (re-plan, I9) approving F3 wrote its merge hash into the blocked F4's row → F2 · `solutions/lite.md` (low)
- P20 — (re-plan, I5) example 01's README session contradicts its own check, so its F2 is blocked → F2 ·
  `solutions/lite.md` (low)
- P21 — (re-plan, I6, I7) the manual run wrote outside scratch and stopped before M6 and the `v2.12.0` chain; rerun both
  rehearsals isolated, and show the P18–P20 fixes working → F2 · `solutions/P21-rehearsal-isolation-rerun.md`
- P22 — (re-plan, I7, I8, I12, I14, I16, I17) the reruns stopped at a usage limit, never let the scope gate see the forced
  file and staged files outside scratch: run both a third time, interleaved, with a sticky hook → F2 ·
  `solutions/P22-third-rehearsal-run.md`
- P23 — (re-plan, I15) a `Wave-Model` trailer in its own paragraph is invisible to git and was accepted: one trailer
  block, and the tier gate reads it with git → F2 · `solutions/lite.md` (low)
- P24 — (re-plan, I18, I20) example 01's CI feature needed F1's `pyproject.toml`, so the current version blocked F3 and
  the user's `merge F1 F3` stopped → F2 · `solutions/lite.md` (low)
- P25 — (re-plan, I21) an archived `Merged` line showed a time no merge commit has: it takes the merge commit's time →
  F2 · `solutions/lite.md` (low)
- P26 — (re-plan, I18–I22) run the manual rehearsal a fourth time with the fixed example, the corrected report
  expectation, merge times checked against git and every command in the scratch environment → F2 ·
  `solutions/P26-fourth-manual-run.md`
- P27 — (re-plan, I23) the fourth manual run stopped at a usage limit at M5: continue it from its preserved M4 state
  and complete the record → F2 · `solutions/P27-fourth-run-continuation.md`
- P28 — (re-plan, I24–I26) the continuation's three Findings came from wrong expectations (the merge-line scan, an
  exact test count, a named archived plan): rescan and correct the record → F2 · `solutions/lite.md` (low)

## How to try

- F1 — open `README.md` → a section "Overnight runs (autonomous flow)" with the two flows, how to choose one, the
  integration branch, the driver commands and the morning steps; `examples/03-autonomous-night-run/` is a plan with
  `- Flow: autonomous · target: integration/wordstat-cli · manual review: F3` and slug `wordstat-cli`; run
  `python skills/wave-plan/scripts/status_check.py examples/03-autonomous-night-run` → exit 0, and on a copy whose
  `Flow:` line reads `- Flow: autonomus` → one `flow-line` line; the changelog starts with `- Unreleased — …`; before:
  the README and examples knew only manual flow and the check ignored the `Flow:` line.
- F2 — open `docs/rehearsals/end-to-end-manual.md` → example 01 run in manual flow with the current skills and
  with `v2.12.0`, step by step side by side through M6, F1 and F3 in review after M4 on both, all three features
  merged and the plan archived on both, the current `Merged` times equal to `git log` of the merge commits, scope,
  trailer and merge-time differences marked `intended (P18)` / `intended (P23)` / `intended (P25)`, nothing written
  outside scratch; open `docs/rehearsals/end-to-end-autonomous.md` → the driver's morning report of example 03: F1 merged into
  `integration/wordstat-cli` with "scope clean", F2 blocked by its forced out-of-scope `stray.txt` (reverted, not
  cleaned up), F3 merged after approval, F4 blocked by the forced red test, the `Merged` cells of F2 and F4 empty;
  in `skills/wave-run/SKILL.md` the task header asks for one trailer block and step 5 reads `Wave-Model` with
  `git log`; example 01's P4 workflow installs only `pytest`; before: the runs never finished `v2.12.0`, auto-approved
  out-of-scope work, accepted a trailer git could not read, and example 01's CI needed F1's file.

## Known test failures before start

- none (`main` at a47af8a, 2026-11-18: 20 status-check tests and 59 driver tests OK, both examples pass, `git diff
  --check` clean; `main` stayed green through F1's merge)
- none on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 23d15d1 (sixth re-plan, 2026-11-19: 33 status-check tests
  and 59 driver tests OK, all three examples pass, `git diff --check` clean); earlier checks of F1 and F2: `history.md`

## Assumptions

- P9 is `high` in the index; its design (fixture, forced failure, expectations, record format) is fixed in
  `solutions/P9-end-to-end-runs.md`, so its two tasks are `medium`: they run fixed commands and record.
- "Behave as before" in manual flow is checked by running the same chain with the skills of tag `v2.12.0` (the last
  release before flow modes) and comparing observable results; the report's `Flow: manual` line is the intended
  difference.
- Waves 4, 6, 7, 8 and 9 need the Claude Code CLI, signed in, and network for `pip install`; if the `wave-run` session's
  subagents cannot run `claude`, the rehearsal tasks run in task mode. Caps by `total_cost_usd`: manual 20 USD,
  autonomous 25 USD; on a claude.ai subscription that counts toward usage limits. The second runs reported about 2.3
  and 1.8 USD and hit the 5-hour limit: start wave 9 in a fresh usage window. Task H of wave 3 needs network for `pip`.
- Findings of the rehearsal tasks are recorded, not fixed; they become problem entries and a re-plan of this plan.
- The fixes of I5–I9 and I12–I17 belong to F2, the feature the entries block: F2 then ships the rules and the records
  that show them working, in one review, with no wait for another feature's merge.
- I23 was a usage stop, not a defect: P27 continued task U's run from the M4 state its scratch folder kept, in
  wave 9, one medium task on the machine that ran wave 8 (`history.md`).
- I24–I26 are errors of P26's expectations: the skills behaved as their rules say (`solutions/lite.md`, P28).
  Wave 10 has one low task that needs only the scratch folder of wave 9 on this machine (`history.md`).
