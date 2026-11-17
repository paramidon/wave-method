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
