# wave-run — the final report

Read by the `wave-run` coordinator right before it prints a final report: at the end of a wave (`SKILL.md` step 9),
at a stop, at a task-mode wait, and at the end of the merge form (`wave-run/merge.md`). Read it again before every
final report, also when it was read earlier in the session: the report is written long after step 1, and this file
is its only source.

## The format is part of the user's request

The user asked for this report by running the command, and its format is part of that request. Print it as the
template below shows.

- Every section marked "always" is printed in every report, in this order, even when it has one row, repeats what
  an earlier message said, or everything in it is green. Commentary is collapsed when the answer arrives, so the
  report is the user's whole view of the plan.
- Tables stay tables and lists stay lists. Never retell a section in a paragraph and never merge two sections.
- A review block is printed in full. A link to `reviews/<feature>.md` may follow it and never replaces it.
- Headings, column names and plain words are in the user's language. Statuses (the emoji), IDs, branch names,
  paths, commands and the date-time format are written exactly as the plan and the template write them.
- The environment's default answer style (short prose, no tables, no repeated facts) does not shorten this report.
  A section marked "when …" is printed only when its condition holds.

## Wave report

Used after step 8 of a wave: a finished wave, a stopped wave and a wave waiting for task mode.

````
Stop <code>: <one line> — next: <command or action>

## Wave <N> · <plan> — <wave status from README "Waves">

### Waves

| Wave | Status | Tasks |
|---|---|---|
| 1 | ✅ | A, B |
| … | … | … |

### Tasks of wave <N>

| Task | Status | Done | Feature |
|---|---|---|---|
| E | ✅ | <the task's Done:, one line> | F1 |

### Features

| Feature | Status | Tasks | Waiting for | Branch |
|---|---|---|---|---|
| F1 <title> | 👀 review | 7/7 | review | `feat/<plan>/<feature>` |

### Merges and checks

- Task merges: <each conflict and how it was resolved, or "no conflicts">
- Check: `<command>` in `<feature worktree>` → <result>; <known failures that did not count, if any>

### Problems

- New: **I<n>** <essence> (<task, feature>)
- Closed: **I<n>** → <closing status>; changed statuses: <item: old → new>

### Check by hand

- F<k> in `<feature worktree>`: <action> → <what one should see>

### Ready for review

<review block of every `👀 review` feature>

### Next

<next command, both forms>

Merge F<k> "<title>" — <what it changes, one line> (feat/<plan>/<feature>) into <main>? Answer: merge F<k> · later · problems F<k>: <what is wrong>

Started: <YYYY-MM-DD HH:MM> · Finished: <YYYY-MM-DD HH:MM> (<duration>)
````

| Section | When | Content |
|---|---|---|
| Stop line | the wave stopped | `SKILL.md`, "Stops"; it is the first line of the report |
| Title | always | the wave's status as README "Waves" now has it: ✅, ⚠️ with its entry IDs, ❌, or `🔄 waiting for task mode` |
| Waves | always | one row per wave of the plan, from README "Waves"; `Tasks` lists the wave's task IDs |
| Tasks of wave N | always | one row per task of this wave; `Done` is the task's `Done:` line in one line, or the reason it is ⚠️, ❌ or waiting |
| Features | always | one row per feature of the plan, from README "Features"; `Tasks` is `<done>/<total>` followed by the IDs of the tasks still missing; `Branch` is `feat/<plan>/<feature>`, for a `👀 review` feature the branch to review |
| Merges and checks | always | task merges with their conflicts, then the check result of every feature worktree touched (what passed, what failed) |
| Problems | always | new entries of `problems.md` (the essence of each), entries this wave closed and the statuses that changed; `none` when there is nothing |
| Check by hand | a feature that is not `👀 review` has something tests do not cover (UI, visuals) | one line per check, in its feature worktree |
| Ready for review | a feature is `👀 review` | the review block of `layout.md`, "Feature review", for every `👀 review` feature (this wave's and earlier ones), from its `reviews/<feature>.md`, without the `Merge:` line; nothing else about a ready feature (no task list, check result, test counts, commits or diff statistics). When two ready features change the same paths (`git diff --name-only <main>...<branch>` of each), add one line naming the paths: the second merge brings the first one in from `<main>` and may need conflict resolution. |
| Next | always | the next command from the table below, for a fresh session, in both forms (`layout.md`, "Commands") |
| Merge question | a feature is `👀 review` | one line per `👀 review` feature, as in the template (`SKILL.md` step 10) |
| Times | always | the last line (`layout.md`, "Run times") |

**The next command:**

| Situation | Next command |
|---|---|
| a feature is `👀 review` | review it, then `/wave-run <plan folder> merge <F-ID>`<br>`$wave-run <plan folder> merge <F-ID>` (for `main-dirty`, clear the reason first) |
| a later wave is ⬜ | `/wave-run <plan folder> <N+1>`<br>`$wave-run <plan folder> <N+1>`; it waits for a review only if its `Depends on:` names the feature |
| waiting for task mode | one per task, in launch-group order: `/wave-run <plan folder> <N> task <ID>`<br>`$wave-run <plan folder> <N> task <ID>` — fresh session, model: `<models of the task's tier>` (`<tier>`), needs `<tool>`; a weaker model stops `tier-mismatch` |
| open problems | `/wave-plan <plan folder>`<br>`$wave-plan <plan folder>`, listing them |
| last wave done, plan from an index | the index parts plannable now: `/wave-plan <index> part <K>`<br>`$wave-plan <index> part <K>` |

## Stop before the wave started

Nothing was changed except, for `plan-defect`, the problem entry. The report is the stop line, one or two lines on
what was found (the wave, feature or file it concerns), the "Waves" and "Features" tables of the wave report, and the
times line.

## Merge report

Used at the end of the merge form (`wave-run/merge.md`).

````
## Merge · <plan>

### Features

| Feature | Status | Tasks | Waiting for | Branch |
|---|---|---|---|---|

### Merged

- **F<k> <title>** → `<main>` `<hash>`: <"Essence" of its brief>

### Not merged

- **F<k>**: <later (`review`) · `main-dirty`: <reason> · rejected → I<n>, I<m>>

### Checks

- `<command>` in `<feature worktree>` after merging `<main>` in → <result>; conflicts: <how resolved, or "none">

### Next

<next command, both forms, or "finished; archived">

Started: <YYYY-MM-DD HH:MM> · Finished: <YYYY-MM-DD HH:MM> (<duration>)
````

"Features" is always printed with every feature of the plan as README "Features" has it after "Record". "Merged",
"Not merged" and "Checks" are printed when they have a line. "Next" follows the table of the wave report, or says
`finished; archived` when the plan was archived. The merge form with no wave ⬜ or ❌ first shows the "Ready for
review" section and the merge questions of the wave report (`wave-run/merge.md`, "Entry points").

## Before sending

Compare the report with the template: every "always" section is there, in order, as a table or list. If one is
missing or retold as prose, rewrite the report before sending it.
