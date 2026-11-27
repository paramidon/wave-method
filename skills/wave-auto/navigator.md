# wave-auto — navigator

Read only by the navigator subagent that `wave-auto/SKILL.md` starts for its `navigate` step. You are read-only: use
only git commands that read (`git show`, `git cat-file -e`, `git branch --list`, `git rev-parse`,
`git merge-base --is-ancestor`, `git worktree list`) and read files of the triage worktree. Run no build or test, and
make no edit, commit, checkout, merge or ref change. Input: `start <start> · skip <units>`, where `<start>` is an index
path or a plan folder and `<units>` are plan folders or an index path separated by spaces or commas, or `none`. Output:
the return of the `navigate` step (`wave-plan/layout.md`, "Coordinated runs"), nothing else: no Markdown, no
explanation, nothing before the first line.

Paths of skill files are relative to the wave skills folder, the parent of this skill's folder
(`wave-plan/layout.md`, "Skill paths"). Every plan fact below is read from git, never from memory or from earlier
answers.

## Sources

- `<main branch>`: `main` when `git rev-parse --verify --quiet refs/heads/main` succeeds, else `master`.
- A plan's README: from the first source where `git cat-file -e <source>:<plan folder>/README.md` succeeds, read with
  `git show <source>:<plan folder>/README.md`. The sources, in order:
  - a plan of an index part: `plan/<slug>` (the slug is the `Plan slug` cell of the index "Parts" table; only when the
    branch exists), `<main branch>`, `integration/<topic>` (the `target:` of the index's `Flow:` line when it names
    another branch; only when the branch exists);
  - a plan start: every `plan/*` branch (it counts only when the README's slug, the `slug: ` field of its header, is
    that branch's name after `plan/`), `<main branch>`, every `integration/*` branch.

  The plan's other files (`problems.md`, wave files) are read from the same source.
- "Tracking branch exists": `refs/heads/plan/<slug>` exists, `<slug>` from the README header. A README found on the
  tracking branch itself has it by definition.
- README tables are read by their header names: "Features" (`ID`, `Status`, `Waiting for`, `Merged`), "Waves" (`Wave`,
  `File`, `Status`), "Tasks" (`ID`, `Complexity`). A status is its first symbol: ⬜, 🔄, ✅, ❌, ⚠️, 👀 or ➖; a
  feature is `✅ merged` when its `Status` cell reads that.
- A wave file is `<plan folder>/<the File cell of the wave's row>`. Its task table is the table under `## Tasks`
  (column `Needs`); its dependencies are the line that starts `Depends on:` and the lines after it up to the next blank
  line; its Execution is the text under `## Execution`.
- The triage worktree is `../<repo-folder>.worktrees/<topic>-triage` beside the main checkout
  (`git worktree list` names it when it was placed elsewhere); `<topic>` is the index folder name without its
  `YYYY-MM-DD-` prefix.

## Index start

`<start>` ends with `index.md`. A start in `skip` yields `done` before anything is read.

1. `git show <main branch>:<index path>` fails → try `triage/<topic>` (`git show triage/<topic>:<index path>`). Found
   there → the triage rules below. Found nowhere → print
   `halt <index path>: index not found — next: /wave-auto <list> · $wave-auto <list>` and `done`.
2. Triage rules (the index exists only on `triage/<topic>`), the first that applies:
   - the index header (the lines before its first `## ` heading) has the line `- Triage: waiting for answers` →
     `next: ask <index path>`;
   - the index has more than 8 problems (its `## Problems` section is an overview table with the header
     `| P | Summary | Cluster | …`) and, for some problem of that table, the file
     `plans/<date>-<topic>/triage/P<n>.md` exists neither in the triage worktree nor on `triage/<topic>`
     (`git cat-file -e triage/<topic>:<path>`) → `next: triage-cluster <index path> <cluster> …`, naming the `Cluster`
     cell of every such problem once, in the order of the overview;
   - otherwise → `next: triage-finish <index path>`.
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
      - not found, `Plan when` is `after part <J> merged` (every part number in the cell counts) → part J is merged when
        its README is found (Sources, with the Plan slug of part J) and every feature of it is ➖, or is `✅ merged` with
        a `Merged` hash that is an ancestor of `<main branch>` or, when the branch exists, of `integration/<topic>`
        (`git merge-base --is-ancestor <hash> <branch>`). This is check 3 of `wave-plan/layout.md`, "Chained parts and
        the integration branch". All parts named are merged → `next: plan <index path> part <K>`; otherwise the part
        waits, and the row yields nothing.

      The first row that yields a `next:` line ends the reading: print the `halt` lines found before it, then that
      line. No row yields one → print the `halt` lines found, then `done`.

## Plan rules

`<start>` is a plan folder (a plan start): its unit is the folder, and these rules are all there is; a unit in `skip`
yields `done`, and a folder found in no source yields
`halt <plan folder>: plan not found on any branch — next: /wave-auto <list> · $wave-auto <list>`, then `done`. For an
index part, a rule that yields no line leaves the unit finished or halted, and the reading goes on with the next row
of "Parts".

In this order; the first rule that applies decides the unit:

1. No tracking branch. Every feature is `✅ merged` or ➖ → the unit is finished (no line). Otherwise
   `halt <unit>: tracking branch plan/<slug> is missing — next: /wave-status <unit> · $wave-status <unit>`.
2. The README header has no `- Flow: autonomous` line (a missing `Flow:` line or `- Flow: manual`): the unit is in
   manual flow → `next: ask-flow <unit> <branch>`. `<branch>` is the integration branch the plan merges into once the
   flow form switches it (`wave-plan/layout.md`, "Names"): `integration/<topic>` when the README header has a line
   `- Index: plans/<date>-<topic>/index.md part <K>` (the path in backticks or not; `<topic>` is the index folder name
   without its `YYYY-MM-DD-` prefix), else `integration/<slug>` with `<slug>` from the README's `slug: ` field. In an
   index start only step 3.1 of "Index start" reaches this rule, and it lists every such unit in one line.
3. A wave is 🔄 (the first one, when several are). The last non-empty line of its wave file's Execution starts with
   `Waiting: task mode ` → `next: tasks <unit> <N> <ID>:<tier>[ needs <Needs>]; …`, with one `<ID>:<tier>` for every
   task ID in that line before its ` — ` (a mark `(fix <k>/2)` after an ID is dropped), in the order of the line. The
   `<tier>` is the `Complexity` cell of the ID's row in the README "Tasks" (`medium` when there is no such row). Add
   ` needs <Needs>` when the `Needs` cell of the ID's row in the wave file's task table is not `—`. Otherwise
   `halt <unit>: wave <N> is 🔄 since <time> with no task-mode wait — next: wait for the run that holds it, or release
   the lock (wave-plan/layout.md, "Running waves")`, where `<time>` is the time in the wave's status cell.
4. A wave is ❌ (the first one). Take the last `Stop <code>: …` line of its Execution. The reason is that line up to
   its ` — next: `, the next part is what follows it. With no stop line the reason is `wave <N> ❌`; with no ` — next: `
   part the next part is `/wave-plan <unit> · $wave-plan <unit>`. Print `halt <unit>: <reason> — next: <next part>`.
5. The first wave that is ⬜, wave N: for each `F<k> merged` of its `Depends on:` lines, in order, the README feature
   `F<k>` must be `✅ merged`; a feature missing from the README counts as not merged. For the first one that is not:
   - rule 6 applies → follow it, and print nothing for this rule;
   - `F<k>` is `👀 review` →
     `halt <unit>: wave <N> needs F<k> merged; F<k> waits for review — next: review F<k>, then /wave-run <unit> merge F<k> · $wave-run <unit> merge F<k>`;
   - otherwise
     `halt <unit>: wave <N> needs F<k> merged; F<k> is <its status cell>, waiting for <its Waiting for> — next: /wave-status <unit> · $wave-status <unit>`
     (`missing` for the status cell of a missing feature).

   Every dependency merged (or the wave has none) → `next: wave <unit> <N>`.
6. Re-plan. `problems.md` (read from the same source) has an entry with `status: open` and no wave can run: rule 5
   found a dependency that is not merged, or no wave is ⬜. An entry starts `- **[I<n> · <scope>] …` and runs to the
   next such line; its status is the text after the last `status:` in it, and `→ task …` is not `open`. It counts
   only when the feature it names (`feature F<k>` in its scope) does not have `Waiting for: user: re-plan limit` in
   the README; an entry that names no feature counts. Counts → `next: re-plan <unit>`.
7. No wave is ⬜ and rule 6 does not apply → the unit is finished (no line).

## Return grammar

```
halt <unit>: <reason> — next: <command or action>      (0 or more lines, one per halted unit)
next: <action>                                          (or: done)
```

Print one `halt` line for every unit the reading halts, in the order the units are read, with no limit on their number; a unit never gets two. In the `— next:` part of a `halt` line, every command is given in both forms, Claude
Code first: `/wave-run …` · `$wave-run …`. `done` means that no unit has a step to run: print it after the `halt`
lines when no `next:` line follows. Print exactly one `next:` line or `done`, last.

`<action>` is one of:

- `next: ask <index path>` — the triage questions have to be asked;
- `next: triage-cluster <index path> <cluster> …` — the clusters whose records are missing, as named in the index;
- `next: triage-finish <index path>` — the index waits for its re-judging and merge;
- `next: plan <index path> part <K>` — part K is ready to be planned;
- `next: ask-flow <plan folder> <branch>; …` — the plans in manual flow, each with the integration branch it merges
  into once switched ("Plan rules", rule 2); entries are joined by `; `, and an index start lists every plan of its
  index that is in manual flow, at once;
- `next: wave <plan folder> <N>` — wave N is ready to run;
- `next: tasks <plan folder> <N> <ID>:<tier>[ needs <Needs>]; …` — wave N waits for these tasks, each with its
  complexity and, when it has one, the tool it needs; entries are joined by `; `;
- `next: re-plan <plan folder>` — open problems have to be re-planned.
