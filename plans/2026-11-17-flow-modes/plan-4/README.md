# Flow modes, part 4: docs, an autonomous example, Flow checks and end-to-end runs

- Plan: `plans/2026-11-17-flow-modes/plan-4/` · slug: `flow-modes-p4` · tracking branch: `plan/flow-modes-p4` · created 2026-11-18 · base: a47af8a · planned 2026-11-18 03:07 – 2026-11-18 03:20
- Index: `plans/2026-11-17-flow-modes/index.md` part 4
- Re-plans:
  - 2026-11-18 at 02d9c4a, 15:31 – 15:40: I1–I3 → P17; I4 closed (plan error); B → G and new H in wave 3; wave 2 dropped, E → I and F → J in wave 4
  - 2026-11-18 at 1e7214e, 17:45 – 17:56: I5–I9 → P18–P21; new K, L, M in wave 5 and N, O in wave 6; I → N, J → O

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `flow-docs-and-checks` | README, autonomous example, Flow checks and changelog for both flows | P8, P17 | A (1), B (1) ➖, C (1), D (1), G (3), H (3) | the six acceptance tests of `solutions/P8-flow-docs.md` and of `solutions/P17-example-03-fixes.md` hold (task H): 32 status-check tests and 59 driver tests OK, all three examples pass `status_check.py`, one `Unreleased` line, README links resolve, example 03 has slug `wordstat-cli`, its check passes on an empty baseline and its package builds | ✅ merged | | `feat/flow-modes-p4/F1-flow-docs-and-checks` | 1fc60af |
| F2 | `end-to-end-rehearsal` | End-to-end runs of both flows on scratch repositories, and the fixes they found | P9, P18–P21 | E (2) ➖, F (2) ➖, I (4) ➖, J (4) ➖, K (5), L (5), M (5), N (6), O (6) | the acceptance tests of `solutions/P18-task-scope-enforcement.md` (task K) and the P19 and P20 checks of `solutions/lite.md` (L, M) hold; `docs/rehearsals/end-to-end-manual.md` and `end-to-end-autonomous.md` meet `solutions/P21-rehearsal-isolation-rerun.md` "Acceptance tests" (N, O): P0 Pass, nothing written outside scratch, the manual comparison of `cur` and `base` complete, F2 of the scratch night run blocked by its forced out-of-scope file with empty `Merged` cells; the check command green (33 status-check tests, 59 driver tests) | 🔄 | wave 6 | `feat/flow-modes-p4/F2-end-to-end-rehearsal` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D | ✅ (fixed by G and H, wave 3) |
| 2 | `waves/w02.md` | E, F | ➖ dropped (tasks → wave 4) |
| 3 | `waves/w03.md` | G, H (after G) | ✅ |
| 4 | `waves/w04.md` | I, J | ⚠️ I5, I6, I7, I8, I9 |
| 5 | `waves/w05.md` | K, L, M | ✅ |
| 6 | `waves/w06.md` | N, O | ⬜ |

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
| N | `manual-flow-rerun` | F2 | 6 | medium | ⬜ |
| O | `autonomous-flow-rerun` | F2 | 6 | medium | ⬜ |

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

## How to try

- F1 — open `README.md` → a section "Overnight runs (autonomous flow)" with the two flows, how to choose one, the
  integration branch, the driver commands and the morning steps; `examples/03-autonomous-night-run/` is a plan with
  `- Flow: autonomous · target: integration/wordstat-cli · manual review: F3` and slug `wordstat-cli`; run
  `python skills/wave-plan/scripts/status_check.py examples/03-autonomous-night-run` → exit 0, and on a copy whose
  `Flow:` line reads `- Flow: autonomus` → one `flow-line` line; the changelog starts with `- Unreleased — …`; before:
  the README and examples knew only manual flow and the check ignored the `Flow:` line.
- F2 — open `docs/rehearsals/end-to-end-manual.md` → example 01 run in manual flow with the current skills and
  with `v2.12.0` side by side, every step M0–M6 on both, all three features merged and the plan archived, and nothing
  written outside scratch; open `docs/rehearsals/end-to-end-autonomous.md` → the driver's morning report of example 03:
  F1 merged into `integration/wordstat-cli` with "scope clean", F2 blocked by its forced out-of-scope `stray.txt`
  (reverted, not cleaned up), F3 merged after approval, F4 blocked by the forced red test, the `Merged` cells of F2 and
  F4 empty; run `python skills/wave-plan/scripts/status_check.py` on a copy of example 03 with `abc123` in F4's `Merged`
  cell → one `merged-fields` line; before: the first runs wrote outside scratch, never ran `v2.12.0`, auto-approved a
  cleaned-up out-of-scope commit and put F3's hash on F4.

## Known test failures before start

- none (`main` at a47af8a, 2026-11-18: `test_status_check.py` 20 tests OK, `python -m unittest discover -s
  scripts/tests` 59 tests OK, both examples pass `status_check.py`, `git diff --check` clean)
- none on `feat/flow-modes-p4/F1-flow-docs-and-checks` at 6a2931a (re-plan, 2026-11-18: 32 status-check tests and 59
  driver tests OK, examples 01 and 02 pass, `git diff --check` clean); `main` at 71d1161 is green as at a47af8a
- none on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 1635ef1 (second re-plan, 2026-11-18: 32 status-check tests and
  59 driver tests OK, all three examples pass, `git diff --check` clean); after task L, 33 status-check tests

## Assumptions

- P8 is one feature: the changelog line names the Flow checks and example 03, and the README links the example, so
  none of the four edits is complete on `main` without the others.
- `status_check.py` requires the exact `Flow:` form that `wave-plan` and the flow form write, because
  `layout.md` finds the plans of a target with `git grep` on that form; the driver keeps its own parser.
- The release archive gains `scripts/` (one word in `.github/workflows/release.yml`), so a release ships the driver
  that its README documents; plugin installs already get the whole repository.
- Example 03 is runnable, not only illustrative: task J of wave 4 runs it in a scratch repository; its fictional
  dates and hashes stay fictional.
- Example 03's target is `integration/wordstat-cli`, not the `integration/wordstat` of I3's proposal: `wave-plan`
  names the target of a raw-list plan after its slug, and the example must look as `wave-plan` writes it.
- The re-plan's new solution is P17, above every P number of the index's plans (plan 2 uses up to P16).
- P9 is `high` in the index; its design (fixture, forced failure, expectations, record format) is fixed in
  `solutions/P9-end-to-end-runs.md`, so its two tasks are `medium`: they run fixed commands and record.
- "Behave as before" in manual flow is checked by running the same chain with the skills of tag `v2.12.0` (the last
  release before flow modes) and comparing observable results; the report's `Flow: manual` line is the intended
  difference.
- The forced red is a test that skips until `wordstat/export.py` exists, so the run reaches wave 2 and only F4 turns
  red; F4 staying ⚠️ after the night, after the user's merge and after a second dry run of the driver is "the
  feature that must stay blocked".
- Wave 4 needs the Claude Code CLI, signed in, and network for `pip install`; if the `wave-run` session's subagents
  cannot run `claude`, run I and J in task mode. Together they spend at most 45 USD by `total_cost_usd` (I 20, J 25);
  on a claude.ai subscription that counts toward usage limits. Task H of wave 3 needs network for `pip`.
- Wave 4 depends on `F1 merged`: task J runs example 03 and the new check, which reach I and J's branch only through
  `main`. Review F1 after wave 3.
- Findings of I and J are recorded, not fixed; they become problem entries and a re-plan of this plan.
- The fixes of I5–I9 belong to F2, the feature the entries block: F2 then ships the rules and the records that show them
  working, in one review, with no wait for another feature's merge.
- I8's fix enforces the existing rule (entry, revert, blocked feature) instead of letting the coordinator delete
  generated files: a cleanup commit hides history from the review. The cause, `git add -A` in a project without a
  `.gitignore`, is closed in the task header; auto-approval gets the same scope test as a second gate.
- The forced out-of-scope edit of task O is a git hook in the scratch repository, not an instruction in a task prompt:
  an executor told to change only its files may refuse a contrary instruction, the hook always fires.
- `CLAUDE_ENV_FILE` is the isolation for wave 6; the re-plan could not try it (a nested headless call was refused
  here), so tasks N and O prove it with preflight P0 and stop before any skill call if it fails.
- Wave 6 needs the Claude Code CLI, signed in, and network for `pip install`, as wave 4 did; same caps (N 20 USD, O 25
  USD). The first runs cost about 1.7 and 1.8 USD.
