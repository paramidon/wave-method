---
name: wave-status
description: Read-only status of the wave-triage → wave-plan → wave-run pipeline. For every plan in plans/ (not archived) — or one given plan folder — lead with each feature's status, task progress and what it waits for, then show which wave is running, why the last wave stopped, ready features waiting for the user's review (their essence, how to test them, branch, merge command), leftover worktrees and branches, unplanned index parts, and the next command. Never writes, commits or deletes anything. Use when the user runs "/wave-status [<plan folder>]", asks "что с планами", "почему волна встала", "почему фича не смержилась", or before starting a wave. Recommended model: low complexity (Haiku 5.5 or any stronger model).
---

# wave-status — read-only pipeline status

Language: talk to the user in the language of their messages; write everything into the repository in English,
always (`wave-plan/layout.md`, "Language"). Start and end time of the run: `wave-plan/layout.md`, "Run times".

Skill paths such as `wave-plan/layout.md` are relative to the wave skills folder, the parent of this skill's
folder (`wave-plan/layout.md`, "Skill paths").

## Hard rule

Read only. No file edits, no commits, no worktree or branch deletion, no builds, no tests. Cleanup is only
suggested as commands for the user in the report; never execute those commands.

## Input

The argument is an optional plan folder. Without it, inspect every plan folder under `plans/` except
`plans/archive/`, plus every index (`plans/<date>-<topic>/index.md`).

Also inspect every plan that exists only on its
tracking branch (a plan of autonomous flow lives on the integration branch until the user merges it, `layout.md`,
"Planning in autonomous flow"): for each branch `plan/<slug>` of `git branch --list "plan/*"` whose plan is not
among those folders, its README is the path of
``git grep -l -F 'slug: `<slug>`' plan/<slug> -- "plans/*README.md" ":!plans/archive"``;
read it and its files from that branch.

## What to read

Read only the following, according to `layout.md`, "Who reads what":

- Each plan's `README.md` from the tracking branch when `plan/<plan>` exists
  (`git show plan/<plan>:<plan folder>/README.md`), otherwise from the main checkout. Use its Features columns
  `| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |` and Waves
  columns `| Wave | File | Tasks | Status |`, and its Tasks columns `| ID | Slug | Feature | Wave | Complexity | Status |`.
  Also its `Flow:` header line (`layout.md`, "Flow"). For a plan in autonomous flow, `<main>` below is its
  integration branch and `<main checkout>` its integration worktree (`layout.md`, "Names"); also read
  `git rev-list --count <main branch>..integration/<name>`
  when that branch exists.
- Each plan's `problems.md`: entry headers only (`**[I<n> · …] essence**`).
- The wave file of a wave that is 🔄, ❌ or ⚠️: only its "Execution" section, for the last
  `Stop <code>: … — next: …` or `Waiting: task mode <IDs> — next: …` line.
- For each `👀 review` feature: its review brief `reviews/<feature>.md`. Only when it has none: the README's
  "User problems" lines of its P and its "How to try" line, its commit subjects
  (`git log --oneline --no-merges <main>..<branch>`), and the "Execution" section of the wave file of its last wave
  (the last wave in its "Tasks (wave)" cell), for what was checked by hand.
- Autonomous flow: for each `✅ merged` feature whose `Merged` hash is not in `<main branch>`
  (`git merge-base --is-ancestor <hash> <main branch>` fails): its brief, from the tracking branch. If it has no
  brief, read the same fallback sources listed above for a feature under review.
- Each index's "Parts" table.
- `git worktree list --porcelain`, `git branch --list "plan/*" "feat/*" "task/*"`,
  `git status --porcelain --untracked-files=no` of the main checkout, and
  `git branch --merged <main> "feat/*"`.

Do not read solutions, task prompts, other sections of wave files, history or archived plans. The tracking
branch is authoritative for plan status; read its problem headers and Execution sections there as well when
it exists. Use `git show plan/<plan>:<plan folder>/<file>` and retain only the allowed portions.

## Report

The user asked for this report by running the command, and its format is part of that request. Print it as the
template in "Template" shows; the bullets below say what each line holds. The environment's default answer style
(short prose, no tables) does not shorten it. Keep a blank line before and after every table and every block.
Feature status comes first: the user reads it before anything about waves.

- Header: plan folder, slug, tracking branch present or absent, and the flow: `manual`, or `autonomous` with its
  target and manual-review list.
- `Features:` one line with the count per status, for example `5 — 2 ✅ merged · 1 👀 review · 1 🔄 · 1 ⚠️`
  (omit statuses with a count of 0).
- The feature table below, one row per feature of the README's Features table, in its order, using the README's
  `Status`, `Waiting for`, `Branch` and `Merged` values. `Branch` is the feature branch `feat/<plan>/<feature>`
  (`—` when it does not exist yet); for a `👀 review` feature it is the branch the user reviews. Show an old
  `✅ ready` as `👀 review` (`layout.md`, "Statuses"). `Tasks` is `<done>/<total>`: tasks of the feature with
  status ✅, over its tasks that are not ➖ (`—` when none). Add the failing task IDs after it for ⚠️ and ❌ tasks
  (`2/4 · ⚠️ B`).
- `Waves:` the wave statuses on one line (`1 ✅ · 2 🔄 since <date time> · 3 ⬜`); the 🔄 wave is the running one.
  `none running` when no wave is 🔄.
- `Merged, not in <main branch>:` autonomous flow only ("Results of an autonomous run" of `layout.md`): the
  merged block of `layout.md`, "Feature review", for every `✅ merged` feature whose `Merged` hash is not in
  `<main branch>` yet, from its brief, in full; `none` when there is no such feature. These are what the user tests
  before merging `integration/<name>`. A feature without a brief gets the block built as `Ready for review:`
  builds one, with the merged block's header and `Approved:` line. In the label, `<main branch>` is replaced by
  the branch name alone, as `git branch` prints it: `Merged, not in main:` or `Merged, not in master:`. Never the
  plan slug, the integration branch, `<main>`, quotes, a possessive or a second rendering of the name; the label
  appears once per plan.
- `Ready for review:` the review block of `layout.md`, "Feature review", for every `👀 review` feature, with its
  `Merge:` line, from its brief; never shortened to the title and branch, and nothing else about the feature.
  For `main-dirty` add its reason (`not on <main>`, `staged changes`, or the overlapping paths); the three read-only
  commands of `layout.md`, "Main readiness", may be run to find it. A feature without a brief (a plan run by an
  older `wave-run`) gets the same block, built from what "What to read" lists: the essence from its title, P lines
  and commit subjects; "How to test" from its "How to try" line, otherwise from what the Execution section says was
  checked by hand, as feature-specific steps; otherwise `not recorded — <Done when>`. Do not say where the text
  came from.
- `Integration:` autonomous flow only: `integration/<name>` — `<N>` commits not in `<main branch>`; review
  `git diff <main branch>...integration/<name>`, then merge it yourself in the main checkout
  (`git merge --no-ff integration/<name>`); or `in <main branch>` when N is 0, or `not created yet`. When
  `refs/wave-method/claims/integration/<name>` exists, add `· claimed by <holder line>` (`git cat-file -p <that ref>`,
  `layout.md`, "Target claim").
- `Merged, not recorded:` a feature branch merged into `<main>` whose row is not `✅ merged` (the user merged it);
  the next `/wave-run <plan folder>` · `$wave-run <plan folder>` records it.
- `Last stop:` the last `Stop <code>: … — next: …` line, or `Waiting: task mode <IDs> — next: …`.
- `Inconsistencies:` a ⚠️/❌ item that names no open entry; an open entry whose items are all ✅ or ➖ (the
  status check of `layout.md`, "Statuses").
  May run the script read-only on a plan folder of the tracking branch's worktree; otherwise check by reading.
- `Leftovers:` task branches or worktrees of waves that are not 🔄; feature worktrees of merged features; a
  tracking branch of an archived plan. Give a suggested cleanup command for each, as described below. In autonomous
  flow the kept branches of auto-merged features are leftovers only once the integration branch is in
  `<main branch>`. A target claim whose holder line names a wave that is not 🔄 on that plan's tracking branch:
  suggest `git update-ref -d refs/wave-method/claims/integration/<name>`, once the user is sure no run holds it.
- `Next:` one command, following the first applicable next-command rule. For task mode, include each required
  task-mode command.

| Feature | Status | Tasks | Waiting for | Branch | Merged |
|---|---|---|---|---|---|
| F1 <Title> | <README status> | <done>/<total> | <README Waiting for> | <feature branch> | <README Merged> |

Then report each index's parts without a plan folder, whether their "Plan when" condition is met, and their
`/wave-plan <index> part <K>` · `$wave-plan <index> part <K>` commands. Also count a part as planned when its plan
folder exists on its tracking branch `plan/<topic>-p<K>`. For an index with a `Flow: autonomous` line, use check 3 of
`layout.md`, "Chained parts and the integration branch", to decide whether the condition is met.

### Template

````
## <plan folder> · `<plan>` · <flow>

- Tracking branch: `plan/<plan>` <present · absent>
- Features: <count per status>

| Feature | Status | Tasks | Waiting for | Branch | Merged |
|---|---|---|---|---|---|
| F1 <Title> | <README status> | <done>/<total> | <README Waiting for> | <feature branch> | <README Merged> |

- Waves: <1 ✅ · 2 🔄 since <date time> · 3 ⬜ · or: none running>

Merged, not in <main branch>:

<merged block of every such feature, each followed by a blank line · or: none>

Ready for review:

<review block of every 👀 review feature, each followed by a blank line>

- Integration: <as the bullet says>
- Merged, not recorded: <F-IDs and branches>
- Last stop: <the line>
- Inconsistencies: <one item per line>
- Leftovers: <one item and its suggested command per line>
- Next: <one command, both forms>

## Index parts

| Index | Part | Plan when | Met | Command |
|---|---|---|---|---|
| `<index path>` | <K> | <Plan when> | <yes · no: why> | `/wave-plan <index> part <K>`<br>`$wave-plan <index> part <K>` |

Started: <YYYY-MM-DD HH:MM> · Finished: <YYYY-MM-DD HH:MM> (<duration>)
````

- One `## ` block per plan: plan folders under `plans/` first, then plans found only on their tracking branch.
  `<flow>` is `manual`, or `autonomous · target: integration/<name>` followed by ` · manual review: <F-IDs>` when
  that list is not empty.
- Always printed: the plan header, `Tracking branch`, `Features`, the table, `Waves`, `Next`, the times line.
  `Merged, not in <main branch>:` and `Integration:`: autonomous flow only, always there (`none`, `not created
  yet`). `Ready for review:`: when a feature is `👀 review`. `Merged, not recorded`, `Last stop`,
  `Inconsistencies`, `Leftovers`: only when they have content. `## Index parts`: when an index has a part
  without a plan folder.
- Labels and column names are written exactly as the template writes them; when the user's language is not
  English, they are translated, and statuses, IDs, branch names, paths and commands stay as written.
- A merged block and a review block are printed in full, never retold as one line.

### Suggested commands

The commands in this subsection are suggestions for the user's report only. Do not execute them.

- Leftover worktree: `git worktree remove <absolute worktree path>`.
- Leftover task, feature or tracking branch: `git branch -d <branch>`; suggest removing an attached worktree
  first. Do not suggest forced deletion.
- A ready feature: `/wave-run <plan folder> merge <F-ID>` · `$wave-run <plan folder> merge <F-ID>`, for use after
  the user has reviewed it; for `main-dirty`, once `<main checkout>` is ready (`layout.md`, "Main readiness").
- A finished plan that has not been archived: suggest the applicable `git mv` command from
  `layout.md`, "Archive". For an index part, the whole index folder is eligible only when every part is merged.

### Before sending

Compare the report with "Template": every plan has its header, `Tracking branch`, `Features`, the table, `Waves`
and `Next` lines, in this order. In autonomous flow the `Merged, not in <main branch>:` label appears exactly once
per plan, with the branch name alone (`Merged, not in main:`), followed by one full merged block per feature or
`none`. If something is missing, merged into prose, or the label differs, rewrite the report before sending it.

## Next-command rules

Use the first rule that applies:

1. A wave is 🔄 waiting for task mode: give its task-mode commands
   `/wave-run <plan folder> <N> task <ID>` · `$wave-run <plan folder> <N> task <ID>`.
   Otherwise a 🔄 wave means `wait: wave N is running`.
2. The last wave is ❌: use the `next:` command of its stop line.
3. Open entries not marked `→ task …`: `/wave-plan <plan folder>` · `$wave-plan <plan folder>`.
4. A feature `👀 review`: "review `<branch>`, then" and its merge command (see "Suggested commands"). If rule 5 also
   applies, give its command on a second line: a wave waits for a review only when its `Depends on:` names the
   feature (`wave-run` then stops `feature-unmerged`).
5. The first ⬜ wave whose earlier waves are ✅, ⚠️ or ➖:
   `/wave-run <plan folder> <N>` · `$wave-run <plan folder> <N>`.
6. Autonomous flow, no wave ⬜ or 🔄, and the integration branch has commits `<main branch>` lacks: review
   `git diff <main branch>...integration/<name>`, then merge it yourself: `git merge --no-ff integration/<name>`.
7. Every feature merged: `finished; archived by the last wave-run`, or the suggested archive command if the
   plan is not archived. In autonomous flow only once the integration branch is in `<main branch>`.

The report ends with the `Started: … · Finished: …` line (`layout.md`, "Run times").

Write commands in both forms (`layout.md`, "Commands"). Running-wave locks and task-mode
waiting follow `layout.md`, "Running waves".
