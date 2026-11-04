---
name: wave-status
description: Read-only status of the wave-triage → wave-plan → wave-run pipeline. For every plan in plans/ (not archived) — or one given plan folder — lead with each feature's status, task progress and what it waits for, then show which wave is running, why the last wave stopped, ready features waiting for the user's review with their full review brief (what and why, what was done, how it was checked, how to test it, what is worth a look, branch, diff summary, review commands, merge command), leftover worktrees and branches, unplanned index parts, and the next command. Never writes, commits or deletes anything. Use when the user runs "/wave-status [<plan folder>]", asks "что с планами", "почему волна встала", "почему фича не смержилась", or before starting a wave. Recommended model: low complexity (Haiku 5.5 / Gemini 3.5 Flash-Lite or any stronger model).
---

# wave-status — read-only pipeline status

Language: `wave-plan/layout.md`, "Language".

Skill paths such as `wave-plan/layout.md` are relative to the wave skills folder, the parent of this skill's
folder (`wave-plan/layout.md`, "Skill paths").

## Hard rule

Read only. No file edits, no commits, no worktree or branch deletion, no builds, no tests. Cleanup is only
suggested as commands for the user in the report; never execute those commands.

## Input

The argument is an optional plan folder. Without it, inspect every plan folder under `plans/` except
`plans/archive/`, plus every index (`plans/<date>-<topic>/index.md`).

## What to read

Read only the following, according to `layout.md`, "Who reads what":

- Each plan's `README.md` from the tracking branch when `plan/<plan>` exists
  (`git show plan/<plan>:<plan folder>/README.md`), otherwise from the main checkout. Use its Features columns
  `| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |` and Waves
  columns `| Wave | File | Tasks | Status |`, and its Tasks columns `| ID | Slug | Feature | Wave | Complexity | Status |`.
- Each plan's `problems.md`: entry headers only (`**[I<n> · …] essence**`).
- The wave file of a wave that is 🔄, ❌ or ⚠️: only its "Execution" section, for the last
  `Stop <code>: … — next: …` or `Waiting: task mode <IDs> — next: …` line.
- For each `👀 review` feature: its review brief `reviews/<feature>.md`, the README's "User problems" lines of its
  P and its "How to try" line; `git log --oneline --no-merges <main>..<branch>`, `git diff --stat <main>...<branch>`
  and `git diff --name-only <main>...<branch>` of its branch. Only when it has no brief: also the "Execution"
  section of the wave file of its last wave (the last wave in its "Tasks (wave)" cell), for the check result.
- Each index's "Parts" table.
- `git worktree list --porcelain`, `git branch --list "plan/*" "feat/*" "task/*"`,
  `git status --porcelain --untracked-files=no` of the main checkout, and
  `git branch --merged <main> "feat/*"`.

Do not read solutions, task prompts, other sections of wave files, history or archived plans. The tracking
branch is authoritative for plan status; read its problem headers and Execution sections there as well when
it exists. Use `git show plan/<plan>:<plan folder>/<file>` and retain only the allowed portions.

## Report

For each plan, report the following in order. Keep a blank line before and after every table. Feature status
comes first: the user reads it before anything about waves.

- Header: plan folder, slug, tracking branch present or absent.
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
- `Ready for review:` one block per `👀 review` feature, the same block `wave-run` shows after a wave, so the user
  can review the feature from this report alone. Write it in the user's language and plain words; the user may
  not remember the plan. Each block gives, from the brief (see "Without a brief" below):
  - the feature ID and title;
  - **What and why**: the user problems it solves (its P lines) and what changes once it is merged, before →
    after, in one to three sentences;
  - **What was done**: every "What was done" line (task ID, what it did), ➖ tasks with their reason;
  - **How it was checked**: "Done when", the full check result, and the tests the feature added or changed;
  - **How to test**: the numbered steps with the worktree path, exact commands and the expected result of each
    step, and what tests do not cover;
  - **Worth a look**: the brief's section, "nothing" when it says so;
  - `Review branch: feat/<plan>/<feature>` on its own line, its worktree path (from `git worktree list`, or `—` with
    the `git worktree add` command of `layout.md`, "Names", as a suggestion), and its `Waiting for`;
  - the number of its commits and the `git diff --stat` summary line;
  - the merge command (see "Suggested commands"); for `main-dirty`, its reason (`not on <main>`,
    `staged changes`, or the overlapping paths) — the three read-only commands of `layout.md`, "Main
    readiness", may be run to find it.

  Below the blocks, the review commands of `layout.md`, "Feature review", once, with `<branch>`. Print every block
  in full, also when several features are ready; never shorten one to its title and branch.

  **Without a brief** (a plan run by an older `wave-run`, which kept no `reviews/` files): say so in one line and
  build the block read-only from what "What to read" lists: "What and why" from the title, the P lines and "Done
  when"; "What was done" from the commit subjects (`<plan> <feature-id> / <task-id>: <short>`); "How it was checked"
  from "Done when", the check result in the Execution section, and the test files among the changed paths; "How to
  test" from the README "How to try" line, otherwise `cd <worktree>` and the check command from the Execution section,
  saying that manual test steps were not recorded; "Worth a look": `not recorded`. Suggest `/wave-run <plan folder>` ·
  `$wave-run <plan folder>`, which builds the brief from the code as well.
- `Merged, not recorded:` a feature branch merged into `<main>` whose row is not `✅ merged` (the user merged it);
  the next `/wave-run <plan folder>` · `$wave-run <plan folder>` records it.
- `Last stop:` the last `Stop <code>: … — next: …` line, or `Waiting: task mode <IDs> — next: …`.
- `Inconsistencies:` a ⚠️/❌ item that names no open entry; an open entry whose items are all ✅ or ➖ (the
  status check of `layout.md`, "Statuses").
  May run the script read-only on a plan folder of the tracking branch's worktree; otherwise check by reading.
- `Leftovers:` task branches or worktrees of waves that are not 🔄; feature worktrees of merged features; a
  tracking branch of an archived plan. Give a suggested cleanup command for each, as described below.
- `Next:` one command, following the first applicable next-command rule. For task mode, include each required
  task-mode command.

| Feature | Status | Tasks | Waiting for | Branch | Merged |
|---|---|---|---|---|---|
| F1 <Title> | <README status> | <done>/<total> | <README Waiting for> | <feature branch> | <README Merged> |

Then report each index's parts without a plan folder, whether their "Plan when" condition is met, and their
`/wave-plan <index> part <K>` · `$wave-plan <index> part <K>` commands.

### Suggested commands

The commands in this subsection are suggestions for the user's report only. Do not execute them.

- Leftover worktree: `git worktree remove <absolute worktree path>`.
- Leftover task, feature or tracking branch: `git branch -d <branch>`; suggest removing an attached worktree
  first. Do not suggest forced deletion.
- A ready feature: `/wave-run <plan folder> merge <F-ID>` · `$wave-run <plan folder> merge <F-ID>`, for use after
  the user has reviewed it; for `main-dirty`, once the main checkout is ready (`layout.md`, "Main readiness").
- A finished plan that has not been archived: suggest the applicable `git mv` command from
  `layout.md`, "Archive". For an index part, the whole index folder is eligible only when every part is merged.

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
6. Every feature merged: `finished; archived by the last wave-run`, or the suggested archive command if the
   plan is not archived.

Write commands in both forms (`layout.md`, "Commands"). Running-wave locks and task-mode
waiting follow `layout.md`, "Running waves".
