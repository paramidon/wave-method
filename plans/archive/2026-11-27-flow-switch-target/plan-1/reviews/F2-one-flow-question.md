# F2 · One plain flow question for all manual plans

- Branch: `feat/flow-switch-target-p1/F2-one-flow-question` · worktree: `D:\Documents\orbits\wave-method.worktrees\flow-switch-target-p1-F2`
- 👀 review since 2026-11-28 00:05

## Essence

Before, `wave-auto` asked only about the first plan still in manual flow, in the model's own words with internal step
names, and skipped a later one. Now one plain question at the start lists every such plan with the branch it would
merge into: yes switches them all, any other answer skips them and shows the command to switch later.

## How to test

1. In a repository whose index has two parts planned in manual flow, run `/wave-auto plans/<date>-<topic>/index.md` →
   at the start, one question in your language lists both plans with `integration/<topic>`, says why they are manual and
   that you review and merge that branch yourself, with no step names.
2. Answer "yes" → one `flow` progress line per plan, then the run goes on; no `questions-late` halt.
3. In another such run answer "no" → both plans appear under "Halts" as `manual-flow` with the
   `/wave-run <plan folder> flow autonomous` command, and the run goes on with the other plans.

## Worth a look

- The question has not been tried in a live run: it was checked by reading, and the navigator by hand.
- The command for switching one plan later shows the literal `<plan folder>`, as the plan's template writes it.
- The sentence describing the final report's "Halts" section still names only two sources, as before this feature,
  although the "Stops" table sends `manual-flow` halts there too.

## Tasks

- C (wave 1) — the navigator lists every manual plan of an index in one line, each with its integration branch.
- D (wave 2) — ➖ superseded by F
- E (wave 2) — ➖ superseded by G
- F (wave 3) — `wave-auto` asks one fixed, plain question for all manual plans; a plain yes switches them all, any
  other answer halts them `manual-flow` and the run goes on.
- G (wave 3) — the README and changelog describe the one question; the navigator's promise about a held-back halt now
  matches its reading order.

## Check

`python skills/wave-plan/scripts/test_status_check.py` → 43 tests OK; `status_check.py` on `examples/*/` → no output;
`git diff --check main...HEAD` → clean; tests added or changed: none
