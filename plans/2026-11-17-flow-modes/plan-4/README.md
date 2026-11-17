# Flow modes, part 4: docs, an autonomous example, Flow checks and end-to-end runs

- Plan: `plans/2026-11-17-flow-modes/plan-4/` · slug: `flow-modes-p4` · tracking branch: `plan/flow-modes-p4` · created 2026-11-18 · base: a47af8a · planned 2026-11-18 03:07 – 2026-11-18 03:20
- Index: `plans/2026-11-17-flow-modes/index.md` part 4
- Re-plans: none

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `flow-docs-and-checks` | README, autonomous example, Flow checks and changelog for both flows | P8 | A (1), B (1), C (1), D (1) | the six acceptance tests of `solutions/P8-flow-docs.md` hold: 32 status-check tests and 59 driver tests OK, all three examples pass `status_check.py`, one `Unreleased` line, README links resolve | ⬜ | wave 1 | | |
| F2 | `end-to-end-rehearsal` | End-to-end runs of both flows on scratch repositories | P9 | E (2), F (2) | `docs/rehearsals/end-to-end-manual.md` and `end-to-end-autonomous.md` have the six sections of `solutions/P9-end-to-end-runs.md` "Record format", every expectation is Pass, Finding or Not run, and the check command is green | ⬜ | wave 2 | | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D | ⬜ |
| 2 | `waves/w02.md` | E, F | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `readme-flow-sections` | F1 | 1 | medium | ⬜ |
| B | `autonomous-example` | F1 | 1 | medium | ⬜ |
| C | `status-check-flow` | F1 | 1 | medium | ⬜ |
| D | `changelog-release-files` | F1 | 1 | low | ⬜ |
| E | `manual-flow-run` | F2 | 2 | medium | ⬜ |
| F | `autonomous-flow-run` | F2 | 2 | medium | ⬜ |

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

## How to try

- F1 — open `README.md` → a section "Overnight runs (autonomous flow)" with the two flows, how to choose one, the
  integration branch, the driver commands and the morning steps; `examples/03-autonomous-night-run/` is a plan with
  `- Flow: autonomous · target: integration/wordstat · manual review: F3`; run
  `python skills/wave-plan/scripts/status_check.py examples/03-autonomous-night-run` → exit 0, and on a copy whose
  `Flow:` line reads `- Flow: autonomus` → one `flow-line` line; the changelog starts with `- Unreleased — …`; before:
  the README and examples knew only manual flow and the check ignored the `Flow:` line.
- F2 — open `docs/rehearsals/end-to-end-manual.md` → each step of example 01 run by hand in manual flow, with the
  current skills and with `v2.12.0` side by side, and their differences; open `docs/rehearsals/end-to-end-autonomous.md`
  → the driver's morning report of a night run of example 03: F1 and F2 merged into `integration/wordstat`, F3
  waiting for review, F4 blocked by the forced red test with its problem entry, `main` and the remote untouched;
  "Repeat" lists the commands to run it again; before: no run of both flows end to end.

## Known test failures before start

- none (`main` at a47af8a, 2026-11-18: `test_status_check.py` 20 tests OK, `python -m unittest discover -s
  scripts/tests` 59 tests OK, both examples pass `status_check.py`, `git diff --check` clean)

## Assumptions

- P8 is one feature: the changelog line names the Flow checks and example 03, and the README links the example, so
  none of the four edits is complete on `main` without the others.
- `status_check.py` requires the exact `Flow:` form that `wave-plan` and the flow form write, because
  `layout.md` finds the plans of a target with `git grep` on that form; the driver keeps its own parser.
- The release archive gains `scripts/` (one word in `.github/workflows/release.yml`), so a release ships the driver
  that its README documents; plugin installs already get the whole repository.
- Example 03 is runnable, not only illustrative: task F of wave 2 runs it in a scratch repository; its fictional
  dates and hashes stay fictional.
- P9 is `high` in the index; its design (fixture, forced failure, expectations, record format) is fixed in
  `solutions/P9-end-to-end-runs.md`, so its two tasks are `medium`: they run fixed commands and record.
- "Behave as before" in manual flow is checked by running the same chain with the skills of tag `v2.12.0` (the last
  release before flow modes) and comparing observable results; the report's `Flow: manual` line is the intended
  difference.
- The forced red is a test that skips until `wordstat/export.py` exists, so the run reaches wave 2 and only F4 turns
  red; F4 staying ⚠️ after the night, after the user's merge and after a second dry run of the driver is "the
  feature that must stay blocked".
- Wave 2 needs the Claude Code CLI, signed in, and network for `pip install`; if the `wave-run` session's subagents
  cannot run `claude`, run E and F in task mode. Together they spend at most 45 USD by `total_cost_usd` (E 20, F 25);
  on a claude.ai subscription that counts toward usage limits.
- Wave 2 depends on `F1 merged`: task F runs example 03 and the new check, which reach E and F's branch only through
  `main`. Review F1 after wave 1.
- Findings of E and F are recorded, not fixed; they become problem entries and a re-plan of this plan.
