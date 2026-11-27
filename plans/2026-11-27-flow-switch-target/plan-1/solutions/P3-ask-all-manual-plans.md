# P3. Every manual plan of an index is asked about at the start

User problem: only the first manual plan of an index is asked about at the start; every later manual plan halts
`questions-late` and has to be run by hand · feature F2

## Cause

- `skills/wave-auto/navigator.md:55`–`69` (Index start, step 3): the first row that yields a `next:` line ends the
  reading. A manual plan in a later row is reported only after the earlier parts are finished.
- `skills/wave-auto/SKILL.md:139`–`140` (start phase 5): `ask-flow` is legal only in the start phase, which ends with
  the first step that is not `triage-ask` or `navigate`; a manual plan found later halts `questions-late`
  (`skills/wave-auto/SKILL.md:299`).

Every plan that `wave-auto` itself plans is in autonomous flow (step `plan` passes `flow autonomous`), so every manual
plan of an index already exists when the run starts. Listing all of them in the first navigator answer therefore
removes the late question, except for a plan the user plans by hand during the run.

## Approach

- The navigator looks for manual plans first, over every row of the index's "Parts" table, and returns all of them in
  one `ask-flow` line (format: `solutions/P2-flow-question-template.md`, "Navigator return line"). Only when there is
  none does it read the rows for the usual `next:` line.
- The coordinator asks one question for all of them (`solutions/P2-flow-question-template.md`, "Flow question"). The
  user's clarification (2026-11-27): one answer covers every listed plan — yes switches all, no switches none; a
  single plan can still be switched later with `/wave-run <plan folder> flow autonomous`.
- Yes → one `flow` step per listed plan, in order (`wave-run <plan folder> flow autonomous`; the steps table of
  `wave-plan/layout.md`, "Coordinated runs", is unchanged). Any other answer → each listed plan is halted with the new
  halt code `manual-flow`, whose `next:` is the flow form, so the run goes on with the other units.

Not chosen: asking per plan (the user chose one answer for all), and keeping the first-`next:` reading with a second
question later (the coordinator asks only in the start phase, so the run could no longer be unattended).

## Navigator (`skills/wave-auto/navigator.md`)

### Index start, step 3

Replace step 3 (lines 55–69) with:

```
3. The index is on `<main branch>`. The unit of a row of its "Parts" table is `plans/<date>-<topic>/plan-<K>` (the
   index folder, then `plan-<K>`); a unit in `skip` is passed over. An index whose "Parts" table has no rows yields
   `done`.
   1. Manual plans first. Go through every row in order and, for each unit whose README is found (Sources), apply
      "Plan rules" 1 and 2 only. When rule 2 applies to one or more units, print the one line
      `next: ask-flow <unit> <branch>; <unit> <branch>; …` with every such unit, in the order of the rows, and nothing
      else: no `halt` line, not even one that rule 1 found (the next reading prints it). That ends the reading.
   2. Otherwise go through the rows again, in order. For each row:
      - its README is found → apply "Plan rules" to that unit;
      - not found, `Plan when` is `now` → `next: plan <index path> part <K>`;
      - not found, `Plan when` is `after part <J> merged` (every part number in the cell counts) → <unchanged text of
        the current bullet, from "part J is merged when" to "the row yields nothing.">

      The first row that yields a `next:` line ends the reading: print the `halt` lines found before it, then that
      line. No row yields one → print the `halt` lines found, then `done`.
```

Keep the text of the `after part <J> merged` bullet word for word; only its indentation changes.

### Plan rules, rule 2

Replace rule 2 (lines 83–84) with:

```
2. The README header has no `- Flow: autonomous` line (a missing `Flow:` line or `- Flow: manual`): the unit is in
   manual flow → `next: ask-flow <unit> <branch>`. `<branch>` is the integration branch the plan merges into once the
   flow form switches it (`wave-plan/layout.md`, "Names"): `integration/<topic>` when the README header has a line
   `- Index: plans/<date>-<topic>/index.md part <K>` (the path in backticks or not; `<topic>` is the index folder name
   without its `YYYY-MM-DD-` prefix), else `integration/<slug>` with `<slug>` from the README's `slug: ` field. In an
   index start only step 3.1 of "Index start" reaches this rule, and it lists every such unit in one line.
```

### Return grammar

Replace the bullet `` - `next: ask-flow <plan folder>` — the plan is in manual flow; `` (line 129) with:

```
- `next: ask-flow <plan folder> <branch>; …` — the plans in manual flow, each with the integration branch it merges
  into once switched ("Plan rules", rule 2); entries are joined by `; `, and an index start lists every plan of its
  index that is in manual flow, at once;
```

## Coordinator (`skills/wave-auto/SKILL.md`)

### Start phase 4

Replace its last sentence, from `When the navigator returns` to `no → halt the unit.` (lines 137–138), with:

```
   When the navigator returns `next: ask-flow <plan folder> <branch>; …`: ask the flow question ("Flow question") once
   for every plan of that line, as the text of your answer, and wait (end the turn). One answer covers every plan of
   the line. A plain yes, in any language → one `flow` step per plan of the line, in its order, each with its progress
   line, then navigate. Any other answer → halt every plan of the line `manual-flow` ("Stops"), then navigate.
```

### Start phase 5

Replace item 5 (lines 139–140) with:

```
5. The start phase ends with the first step that is not `triage-ask`, `navigate` or a `flow` step of the answer to
   the flow question. From then on a navigator line `next: ask …` halts its unit, and a line `next: ask-flow …` halts
   every plan it lists, instead (`questions-late`, `next:` the manual command).
```

### Dispatch table

Replace the row of `next: ask-flow <plan folder>` (line 160) with:

```
| `next: ask-flow <plan folder> <branch>; …` | start phase only: 4 of the start phase (the flow question, then one `flow` step per plan or one `manual-flow` halt per plan); later `questions-late` for every plan of the line |
```

### Halts table ("Stops", second table)

Replace the `questions-late` row (line 299) with the first row below and add the second row right after it:

```
| `questions-late` | the navigator returns `next: ask …` or `next: ask-flow …` after the start phase; one halt per plan of an `ask-flow` line | the manual command of the unit, for example `/wave-triage flow autonomous answers <index path>`<br>`$wave-triage flow autonomous answers <index path>`; for a plan in manual flow `/wave-run <plan folder> flow autonomous`<br>`$wave-run <plan folder> flow autonomous`, then `/wave-auto <start>`<br>`$wave-auto <start>` |
| `manual-flow` | the answer to the flow question is not a plain yes; one halt per plan of the line, reason `manual-flow: kept in manual flow by the user's answer` | `/wave-run <plan folder> flow autonomous`<br>`$wave-run <plan folder> flow autonomous`, then `/wave-auto <start>`<br>`$wave-auto <start>` |
```

The flow question subsection itself and the hard-rule change: `solutions/P2-flow-question-template.md`, "Flow
question".

## Docs

### `README.md`, "Unattended runs: wave-auto"

Add this bullet after the bullet that starts `Start from a list, an index`:

```
- Plans of the index that were planned earlier in manual flow are asked about once, at the start: one question lists
  every such plan with the integration branch it would merge into. Yes switches all of them to autonomous flow; no
  keeps them all manual, and the run skips them. Switch one later with `/wave-run <plan folder> flow autonomous`.
```

### `skills/wave-plan/CHANGELOG.md`

Append to the end of the existing `- Unreleased — …` item (feature F1 creates it; if it is missing, create it before
the `- v2.13.0` item as `- Unreleased — ` followed by this text without its leading `; `), lines at most 120
characters, continuation lines indented by two spaces:

```
; `wave-auto` asks one fixed, plain question about every plan of its start that is in manual flow (the navigator's
`next: ask-flow` line lists each plan with its integration branch): yes switches them all, any other answer halts
them `manual-flow`, and a later manual plan no longer halts `questions-late`.
```

## Limits

- A plan planned by hand during the run, after the start phase, still halts `questions-late`: the coordinator asks
  only in the start phase.
- A listed plan with a 🔄 wave makes its `flow` step stop `wave-running` (`wave-run/autonomous.md`, "Flow form",
  step 1): that plan is halted, the other `flow` steps still run.
- The navigator stays read-only; the `navigate` row of `wave-plan/layout.md`, "Coordinated runs", is unchanged
  (`next: <action>` covers the longer line).

## Acceptance tests

Index `plans/2026-11-22-cozy-cooking-slice/index.md` with four parts: part 1 in autonomous flow with wave 1 ⬜, parts 2
and 3 planned in manual flow with tracking branches, part 4 not planned, `Plan when` `now`.

1. `start <index> · skip none` → the navigator prints exactly
   `next: ask-flow plans/2026-11-22-cozy-cooking-slice/plan-2 integration/cozy-cooking-slice; plans/2026-11-22-cozy-cooking-slice/plan-3 integration/cozy-cooking-slice`.
2. After both plans are switched (their READMEs have `- Flow: autonomous · target: integration/cozy-cooking-slice`)
   → `next: wave plans/2026-11-22-cozy-cooking-slice/plan-1 1`.
3. Answer "no": the coordinator halts plan-2 and plan-3 `manual-flow`; `start <index> · skip plans/…/plan-2,
   plans/…/plan-3` → `next: wave plans/2026-11-22-cozy-cooking-slice/plan-1 1`; the final report's Halts lists both
   with `— next: /wave-run <plan folder> flow autonomous · $wave-run <plan folder> flow autonomous`.
4. Part 2 has no tracking branch and an unmerged feature; plan-3's wave 1 is ⬜ with no `Depends on: F<k> merged`.
   Corrected by the re-plan of 2026-11-27 (open entry I4, `solutions/lite.md` P4): a held-back `halt` is printed only
   by a reading that reaches its row.
   - `start <index> · skip none` → exactly
     `next: ask-flow plans/2026-11-22-cozy-cooking-slice/plan-3 integration/cozy-cooking-slice`, with no `halt` line.
   - After plan-3 is switched, `start <index> · skip none` → exactly
     `next: wave plans/2026-11-22-cozy-cooking-slice/plan-1 1`, with no `halt` line: row 1 ends the reading before
     row 2.
   - After plan-3 is switched, `start <index> · skip plans/2026-11-22-cozy-cooking-slice/plan-1` → exactly two lines,
     `halt plans/2026-11-22-cozy-cooking-slice/plan-2: tracking branch plan/cozy-cooking-slice-p2 is missing — next: /wave-status plans/2026-11-22-cozy-cooking-slice/plan-2 · $wave-status plans/2026-11-22-cozy-cooking-slice/plan-2`,
     then `next: wave plans/2026-11-22-cozy-cooking-slice/plan-3 1`.
5. Checks: `git grep -n "Manual plans first" -- skills/wave-auto/navigator.md` → one line;
   `git grep -n "manual-flow" -- skills/wave-auto/SKILL.md` → at least the start-phase line and the halts row;
   `git diff --check` → no output; `python skills/wave-plan/scripts/test_status_check.py` → OK.
