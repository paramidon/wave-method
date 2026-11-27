# Flow switch target — one integration branch and one plain flow question

- Plan: `plans/2026-11-27-flow-switch-target/plan-1/` · slug: `flow-switch-target-p1` · tracking branch: `plan/flow-switch-target-p1` · created 2026-11-27 · base: 217a674 · planned 2026-11-27 23:37 – 2026-11-27 23:44
- Index: `plans/2026-11-27-flow-switch-target/index.md` part 1
- Re-plans: none

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `switch-target-topic` | Switched index parts share the index's integration branch | P1 | A (1), B (1) | `solutions/lite.md` P1 "Check" green: 43 checker tests OK, examples clean, old default sentences gone | ⬜ | wave 1 | | |
| F2 | `one-flow-question` | One plain flow question for all manual plans | P2, P3 | C (1), D (2), E (2) | acceptance tests of `solutions/P2-flow-question-template.md` and `solutions/P3-ask-all-manual-plans.md` hold; checker tests OK; `git diff --check` clean | ⬜ | wave 1 | | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C | ⬜ |
| 2 | `waves/w02.md` | D, E (needs F1 merged) | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `index-part-target-rule` | F1 | 1 | low | ⬜ |
| B | `flow-target-check` | F1 | 1 | low | ⬜ |
| C | `navigator-manual-plans` | F2 | 1 | medium | ⬜ |
| D | `coordinator-flow-question` | F2 | 2 | medium | ⬜ |
| E | `flow-question-docs` | F2 | 2 | low | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/flow-switch-target-p1` and
reach the main branch with each feature merge.

## User problems

- P1 — the flow form names an index part's integration branch after the plan slug, not the index topic → F1 ·
  `solutions/lite.md` (low)
- P2 — the `ask-flow` question of `wave-auto` needs a fixed, plain template → F2 · `solutions/P2-flow-question-template.md`
- P3 — every manual plan of an index should be asked about at the start, not only the first → F2 ·
  `solutions/P3-ask-all-manual-plans.md`

## How to try

- F1 — in a repository with an index part planned in manual flow, run
  `/wave-run plans/<date>-<topic>/plan-<K> flow autonomous` → the plan README header reads
  `- Flow: autonomous · target: integration/<topic>`; before: `integration/<topic>-p<K>`. Also: a README with an
  `- Index: …/<date>-<topic>/index.md part <K>` line and `target: integration/<topic>-p<K>` makes
  `python skills/wave-plan/scripts/status_check.py <plan folder>` print one `flow-target` line.
- F2 — in a repository whose index has two parts planned in manual flow, run `/wave-auto plans/<date>-<topic>/index.md`
  → at the start, one question in your language lists both plans with `integration/<topic>`, says why they are manual
  and that you review and merge that branch yourself, with no step names; "yes" → two `flow` progress lines and no
  `questions-late` halt, "no" → both halted `manual-flow` with the `/wave-run … flow autonomous` command; before: only
  the first plan was asked about, in free words with step names, and the second halted `questions-late`.

## Known test failures before start

- none — `python skills/wave-plan/scripts/test_status_check.py` → 39 tests OK on `main` at 217a674; `status_check.py`
  on every `examples/*/` → no output.

## Assumptions

- The canonical skill text is under `skills/`; `.claude/skills/` is a local installed copy and is not edited
  (`CONTRIBUTING.md`, item 3).
- A plan of an index part already switched to `integration/<slug>` before the fix is not migrated: none is known to
  exist. After F1 the status check reports such a plan as `flow-target`.
- F2 depends on F1 for correctness, not for code: the navigator computes `integration/<topic>` itself, but the flow
  form writes that branch only after F1. So wave 2 waits for `F1 merged`, and F2 cannot reach `main` before F1.
- The flow question says, in plain words, why the plans are manual, the exact integration branch, and that the user
  reviews and merges that branch into `<main branch>` themselves; any answer other than a plain yes keeps every listed
  plan manual (halt `manual-flow`), and the run goes on with the other units.
- A plan planned by hand during a run still halts `questions-late`: the coordinator asks only in the start phase.
- `docs/rehearsals/` records past runs and is not changed; no rehearsal with two manual plans is part of this plan.
- Out of scope: `README.md` says "all five auto-approval conditions" while `skills/wave-plan/layout.md` lists six.
