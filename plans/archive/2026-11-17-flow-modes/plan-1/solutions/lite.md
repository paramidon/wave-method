# Lite solutions (low problems)

## P5. Final reports show the flow and what was auto-merged and why

User problem: the final reports show the active flow; in autonomous flow they list what was auto-merged and why · feature F1

**Edit:** `skills/wave-run/report.md` only. `<…>` are the template's placeholders; the inner fences are three or four
backticks as in the file.

1. Wave report template (l.27-76): right after the title line `## Wave <N> · <plan> — <wave status from README "Waves">`
   insert a blank line and
   `Flow: <manual · or: autonomous · target integration/<name> · manual review <F-IDs>>`.
   After the "Problems" section (l.56-59) insert:

   ```
   ### Auto-merged

   - **F<k> <title>** → `integration/<name>` `<hash>`: <"Essence" of its brief> — why: tasks <done>/<total> ✅ or ➖, check green after merging `<main>` in, no open entries, tier gate clean, not under manual review
   - **F<m> <title>** not merged: <manual review · ⚠️ I<n>: <the condition that failed> · `main-dirty`: <reason>>
   ```

2. Section table (l.78-91):
   - after the "Title" row add `| Flow | always | the `Flow:` line of the README as the run read it ("manual" when the README has none); `layout.md`, "Flow" |`;
   - after the "Problems" row add `| Auto-merged | autonomous flow | one line per `👀 review` feature that "Auto-approval" of `wave-run/autonomous.md` looked at in this run: merged (target, hash, "Essence", and why: the five conditions of `layout.md`, "Auto-approval", held) or not merged (manual review, the failed condition with its entry, or `main-dirty` with the reason); `none` when no feature was `👀 review` |`;
   - "Ready for review" row: after "without the `Merge:` line" add "(autonomous flow: with it, since no question is asked)";
   - "Merge question" row: When → `a feature is `👀 review`, manual flow only`.
3. "The next command" table (l.95-101): add a last row
   `| autonomous flow, `integration/<name>` has commits `<main branch>` lacks | review `git diff <main branch>...integration/<name>`, then merge it yourself in the main checkout: `git merge --no-ff integration/<name>` |`.
4. "Stop before the wave started" (l.103-107): after "the stop line," add "the `Flow:` line,".
5. Merge report template (l.113-138): after `## Merge · <plan>` insert a blank line and the same `Flow:` line; in the
   paragraph after it (l.140) add the sentence "The `Flow:` line is always printed."
6. New section before "## Before sending":

   ````
   ## Flow report

   Used at the end of the flow form (`wave-run/autonomous.md`, "Flow form").

   ```
   ## Flow · <plan> — <manual|autonomous>

   Flow: <the new `Flow:` line>

   ### Features

   | Feature | Status | Tasks | Waiting for | Branch |
   |---|---|---|---|---|

   ### Next

   <next command, both forms>

   Started: <YYYY-MM-DD HH:MM> · Finished: <YYYY-MM-DD HH:MM> (<duration>)
   ```

   A stop of the flow form (`wave-running`, `target-unsafe`, `target-unmerged`) is reported as "Stop before the wave
   started".
   ````

**Check:** `git grep -n -e "^Flow: " -e "### Auto-merged" -e "## Flow report" -- skills/wave-run/report.md` → three
`Flow:` template lines (wave, merge, flow report), one "Auto-merged" heading and one "Flow report" heading; every
table of the file keeps one cell count per row; `git diff --check` is clean.

## P12. `main-dirty` and readiness sentences name `<main checkout>`

User problem: in autonomous flow `main-dirty` means the integration worktree is not ready, but the sentences about it
still say "the main checkout" (problem-log entry I1) · feature F1

**Edit:** line numbers are those of `feat/flow-modes-p1/F1-autonomous-flow` at e83a4f1; find each place by its text.
Replace only the quoted words; keep the rest of each sentence and rewrap to about 120 characters.

1. `skills/wave-plan/layout.md:177`, the `Waiting for` paragraph of "Statuses" (task H):
   "`main-dirty` (approved, the main checkout was not ready for the merge)" →
   "`main-dirty` (approved, `<main checkout>` was not ready for the merge)".
2. `skills/wave-status/SKILL.md:31-32`, "What to read", the `Flow:` bullet (task H):
   "`<main>` below is its integration branch (`layout.md`, "Names")" →
   "`<main>` below is its integration branch and `<main checkout>` its integration worktree (`layout.md`, "Names")".
   Reason: line 70-71 runs the "Main readiness" commands, which use `<main checkout>`.
3. `skills/wave-status/SKILL.md:107`, the next-command suggestions (task H):
   "for `main-dirty`, once the main checkout is ready" → "for `main-dirty`, once `<main checkout>` is ready".
4. `skills/wave-run/SKILL.md:109-111`, the paragraph after the "Stops" table (task G):
   "merges it once the main checkout is ready (see `wave-run/merge.md`)" →
   "merges it once `<main checkout>` is ready (see `wave-run/merge.md`)".

Every other "the main checkout" in `skills/` means the repository's real main checkout, in both flows, and stays:
`layout.md` "Flow" / "Integration target" ("never changes `<main branch>` or the main checkout"; "in the main
checkout. No skill does."); `wave-run/SKILL.md` hard rules ("never works in the main checkout"; "touched only for
reading and for the final merges", which stays true in autonomous flow, where it makes no merges), step 1
("Uncommitted changes in the main checkout"), the task header ("do not touch other worktrees or the main checkout");
`wave-run/autonomous.md` "Integration target" ("the main checkout included"); `wave-run/report.md` and
`wave-status/SKILL.md` where the user merges the integration branch "in the main checkout"; `wave-status/SKILL.md`
"What to read" (the README "otherwise from the main checkout"; `git status … of the main checkout`); every use in
`wave-plan/SKILL.md` and `wave-triage/SKILL.md`.

**Check:** `git grep -n -e "main checkout was not ready" -e "main checkout is ready" -- skills/wave-plan/layout.md
skills/wave-run/SKILL.md skills/wave-status/SKILL.md` → no output (before the edits: three lines);
`git grep -n "<main checkout>. \(was not\|is\) ready" -- skills/wave-plan/layout.md skills/wave-run/SKILL.md
skills/wave-status/SKILL.md` → the three edited lines (1, 3, 4) and the first line of `layout.md` "Main readiness"
(`` `<main checkout>` is ready for a merge of branch `B` ``). Keep each new phrase ("`<main checkout>` was not ready",
"`<main checkout>` is ready") on one line, so the checks find it.

## P13. Define `<name>` of `integration/<name>` in "Names"

User problem: `integration/<name>` is used in `layout.md` (branch table, `Flow:` example, "Integration target") and in
`wave-run/autonomous.md`, `wave-run/report.md`, `wave-status/SKILL.md`, but `<name>` is defined nowhere, while
`wave-status/SKILL.md:32` points to `layout.md`, "Names" for the integration branch (problem-log entry I2) · feature F1

**Edit:** `skills/wave-plan/layout.md`, "Names": right after the `<main checkout>` bullet (l.141-142), before the
`<plan>` bullet, add (task H):

```
- `<name>` — the name of the plan's integration branch after `integration/`: from `target:` of the README `Flow:`
  line, else `<plan>` ("Flow"). Used in autonomous flow only.
```

The other places that say where `<name>` comes from (`layout.md` "Flow", "`target:` names the integration branch …";
`wave-run/autonomous.md` "Flow form" step 2 and "Integration target" step 1) agree with it and stay.

**Check:** `git grep -n "<name>. —" -- skills/wave-plan/layout.md` → one line, in "Names", between the
`<main checkout>` and `<plan>` bullets.
