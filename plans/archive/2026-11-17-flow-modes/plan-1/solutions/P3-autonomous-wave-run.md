# P3. wave-run in autonomous flow: `autonomous.md`, auto-approval, an answer for each interactive point

User problem: in autonomous flow `wave-run` never asks; it auto-approves a feature under the five conditions and has
a defined, safe answer for each interactive point; its specifics live in a new `wave-run/autonomous.md` · feature F1

## Cause

The ask points of `skills/wave-run/SKILL.md` (step 1 l.145-149, step 3 l.176, step 5 l.227-229 and l.238-240, step 6
l.254, step 10 l.332-344) and `skills/wave-run/merge.md` (step 1 l.29-30, step 2 l.31-35) have only the manual
answer. The extra-file pattern to follow is `SKILL.md` step 1, "Extra files" (l.128-132): `task-mode.md` and
`merge.md` are read only on a condition.

## Approach

- `wave-run/autonomous.md` holds the procedures (how). What autonomous flow does at each point is the decision table
  of `layout.md`, "Flow" (P1); the integration branch is `layout.md`, "Integration target" (P2). `autonomous.md`
  points to them and never restates the table.
- `SKILL.md` and `merge.md` get one conditional pointer per ask point ("Autonomous flow: `wave-run/autonomous.md`,
  "<section>"."). The manual text stays as it is.
- Auto-approval runs after step 8's commit and before the report (step 9), and replaces step 10. It reuses
  `merge.md` ("Merge one feature", "Record") with `<main>` = the integration branch.
- Conservative skipping: in autonomous flow no new work is built on a feature that has an unanswered question
  (`status: open` entry). Entries already planned (`→ task Y`) do not block: their fix tasks must run.
- Feature branches of auto-merged features are kept (their worktrees removed): the user may look at each feature
  before merging the integration branch.

## Exact text of the new file `skills/wave-run/autonomous.md`

The task writes this file; it may only fix wording and Markdown. Inner fences are three backticks.

````markdown
# wave-run — autonomous flow

Read by the `wave-run` coordinator only when `SKILL.md` step 1 says so: the plan's flow is autonomous, or the
arguments are `flow …`. What autonomous flow does at each point where manual flow asks or waits, the auto-approval
conditions and the integration branch: `layout.md`, "Flow". This file says how; it does not repeat the decision
table.

Never ask the user a question in autonomous flow. A situation the decision table does not cover stops the wave with
the closest code of `SKILL.md`, "Stops"; its `next:` says what the user must decide.

## Flow form

`/wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` · `$wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]`

1. A wave of the plan is 🔄 (also one waiting for task mode) → stop `wave-running`.
2. `autonomous`: `<name>` is the `<name>` of the current `target:`, else `<plan>`; run the checks of "Integration
   target", step 1. `manual`: the integration branch of the current `Flow:` line exists and
   `git rev-list --count <main branch>..integration/<name>` is not 0 → stop `target-unmerged`.
3. Tracking worktree as `SKILL.md` step 2, without a "started" commit. In the README header write the line, replacing
   an existing `Flow:` line, else right after the `- Re-plans:` line:
   - `- Flow: autonomous · target: integration/<name>`, plus ` · manual review: <F-IDs>` when the list is not
     empty. `review <F-IDs>` replaces the list; `review none` empties it; without `review` the list stays.
   - `- Flow: manual`.
4. Commit `Plan <plan>: flow <manual|autonomous>` on the tracking branch. Nothing else changes: features already
   `👀 review` stay so; the next run applies the new flow to them.
5. Report: `wave-run/report.md`, "Flow report".

## Integration target

Step 1, read-only, right after the README is read. `<name>` comes from `target:`, else it is `<plan>`. Stop
`target-unsafe` (nothing written), naming the check that failed, when:

1. `target:` is present and is not `integration/<name>` with a kebab-case `<name>`;
2. `git worktree list --porcelain` shows `refs/heads/integration/<name>` at a path other than the integration worktree
   (`layout.md`, "Names"), the main checkout included;
3. the integration worktree path exists and is not a worktree of this repository;
4. the integration worktree exists and is not on `integration/<name>`
   (`git -C <integration worktree> branch --show-current`), or has tracked changes
   (`git -C <integration worktree> status --porcelain --untracked-files=no`), or an unfinished merge
   (`git -C <integration worktree> rev-parse -q --verify MERGE_HEAD` succeeds).

Step 2, before the tracking worktree and the "wave started" commit:

1. Branch missing: `git worktree add -b integration/<name> <integration worktree> <main branch>`. Branch without a
   worktree: `git worktree add <integration worktree> integration/<name>`.
2. `git merge-base --is-ancestor <main branch> integration/<name>` fails →
   `git -C <integration worktree> merge --no-ff <main branch> -m "Integration <name>: bring in <main branch>"`. A
   conflict → `git -C <integration worktree> merge --abort`, stop `target-conflict`; the wave stays ⬜.
3. From here on `<main>` is `integration/<name>` and `<main checkout>` the integration worktree, in every step.

## Skipped tasks

Before each launch group of step 4, skip every task of the group when:

- its feature has an open entry in `problems.md` with `status: open` (existing before the run or added during it);
  an entry `→ task <ID>` does not block: its fix tasks run;
- a task of its `After` was skipped or is ⚠️ or ❌.

A skipped task is not launched and gets no worktree. README "Tasks": `⚠️ I<n> (skipped)`, naming the entry that
blocks it (for an `After` task without an entry of its own: the entry of that task). The wave becomes ⚠️ with those
entries (`SKILL.md` step 8). A re-plan reschedules skipped tasks.

## Points of steps 1–6

- **Step 1, open entries:** no question. The Execution gets `Open entries: I<n>, … — proceeding (autonomous flow).`
- **Step 1, leftover task branches or worktrees:** neither reuse nor delete them. Stop `leftover-branches`:
  `Stop leftover-branches: wave <N> has <branches> — next: the user continues from them or deletes them, then /wave-run <plan folder> <N>`.
- **Step 3, a feature check red before the wave:** a new entry
  `[I<n> · wave <N> / feature F<k>] check red before the wave: <failing tests>` with `status: open`; the feature is
  `⚠️ blocked I<n>`; its tasks of this wave are skipped; no stop.
- **Step 5, an out-of-scope edit or unusable direct work:** a new entry naming the files; do not merge the task: keep
  a task branch and its worktree unmerged, undo a direct task with `git revert --no-edit H..HEAD` (never
  `git reset --hard`); the task is ⚠️, the feature `⚠️ blocked`; its dependants are skipped.
- **Step 6, a conflict that would change a plan solution:** `git merge --abort` in the feature worktree; a new entry
  naming the solution file and both tasks; the task being merged is ⚠️ (its branch and worktree kept), the feature
  `⚠️ blocked`; its dependants are skipped; the wave goes on.

Unchanged in autonomous flow: the fix loop and `red-after-merge`, the tier gate with `tier-missing` and
`tier-mismatch`, task mode, `feature-unmerged` and every other stop.

## Auto-approval

Run after step 8's commit and before the report; it replaces step 10. In the merge form it runs after "Checks" of
`merge.md` when no wave is ⬜ or ❌. For every `👀 review` feature of the plan, in "Features" order (this run's and
earlier ones):

1. Listed under `manual review:` → leave it `👀 review`, `Waiting for: review`.
2. Conditions 1, 3 and 4 of `layout.md`, "Auto-approval". For 4 run
   `git log --no-merges --format="%h %s%n%(trailers:key=Wave-Model,valueonly)" <main>..feat/<plan>/<feature>`: every
   commit whose subject starts with `<plan> <feature-id> / <task-id>:` has a `Wave-Model` trailer naming a model of
   that task's tier or higher (`layout.md`, "Model tiers", or the README `Models:` line). A failure → the feature is
   `⚠️ blocked I<n>`; for 4 a new entry `below tier: <model> ran a <tier> task (<hash>)`.
3. `merge.md`, "Merge one feature", step 1. Red → as there. When resolving a conflict changed lines of the feature's
   own changes: do not merge; a new entry `merging <main> changed F<k>'s own lines in <files>: needs the user's
   review`; the feature is `⚠️ blocked I<n>`.
4. Step 2 of the same: not ready → `👀 review`, `Waiting for: main-dirty`, with the reason in the report; no question.
5. Step 3 of the same, with one more body line after the task lines: `Approved-By: wave-run autonomous flow`.

Then `merge.md`, "Record", with these differences:

- the Execution line is `Merged <YYYY-MM-DD HH:MM>: <feature-id> <hash> (auto-approved)`; a feature left unmerged gets
  `Not merged <YYYY-MM-DD HH:MM>: <feature-id> — <manual review · I<n> · main-dirty>`;
- remove the worktree of a merged feature but keep its branch; `wave-status` lists it as a leftover once the
  integration branch is in `<main branch>`;
- no archive: the tracking branch and its worktree stay (`layout.md`, "Archive");
- the tracking branch is merged into `<main checkout>`, the integration worktree.

## Report

`wave-run/report.md`: the `Flow:` line and the "Auto-merged" section; no merge questions.
````

## Edits of `skills/wave-run/SKILL.md`

Quote: "Autonomous flow: `wave-run/autonomous.md`, "<section>"." Each edit adds a clause or sentence; manual text stays.

1. Frontmatter `description`: after "merge it into the main branch only when the user approves that feature (in the
   same session, or later with "/wave-run <plan> merge <F-ID>")" add ", or, in a plan whose flow is autonomous,
   approve it itself under fixed conditions and merge it into an integration branch the user merges later".
2. Arguments (l.21-27): add the sentence "Flow form (switches the plan's flow between waves, `layout.md`, "Flow"):
   `/wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` · `$wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]`
   (see `wave-run/autonomous.md`)."
3. Model of work (l.37-38): "It reaches `<main>` only when the user approves that feature (step 10,
   `wave-run/merge.md`)" → add ", or, in autonomous flow, when `wave-run` auto-approves it (`layout.md`, "Flow")".
4. Hard rules: after the first rule (l.44-45) add "In autonomous flow it receives nothing: `<main>` is the
   integration branch (`layout.md`, "Integration target")." The fourth rule (l.50-51): after "(`layout.md`, "Feature
   review")" add ", or, in autonomous flow, by the auto-approval of `wave-run/autonomous.md`, which merges into the
   integration branch only".
5. Stops table (l.92-107): add the three rows of `solutions/P2-integration-target.md`, "Stop codes", after
   `capability-missing`.
6. Step 1, "Extra files" (l.128-132): add "Read `autonomous.md` when the README on the tracking branch (else on
   `<main branch>`) has `Flow: autonomous`, or the arguments are `flow …`. Read the flow here, once, and keep it for
   the whole run." And a new bullet after the lock bullet (l.133-135): "Autonomous flow: the integration-target
   checks of `autonomous.md`, "Integration target", step 1."
7. Step 1 leftover bullet (l.145-147) and open-entries bullet (l.148-149): append "Autonomous flow:
   `wave-run/autonomous.md`, "Points of steps 1–6"." to each.
8. Step 2 (l.157-165): first bullet "Autonomous flow: first `autonomous.md`, "Integration target", step 2." Last
   bullet: append "Autonomous flow: they go to "Auto-approval" of `autonomous.md` after step 8."
9. Step 3 (l.173-177): after "stop `red-before-wave` for the user's decision" add "(autonomous flow:
   `autonomous.md`, "Points of steps 1–6")".
10. Step 4: after the "Launch groups" table add "Autonomous flow: before each launch group, skip tasks as
    `autonomous.md`, "Skipped tasks", says."
11. Step 5 (l.227-229, l.238-240) and step 6 (l.254): append "Autonomous flow: `autonomous.md`, "Points of steps
    1–6"." to the out-of-scope bullet, the "unusable direct work" bullet and the conflicts bullet.
12. Step 8: a last bullet "Autonomous flow: then run "Auto-approval" of `autonomous.md`."
13. Step 10 (l.332): first line "Autonomous flow: skip this step; "Auto-approval" of `autonomous.md` ran after
    step 8."

## Edits of `skills/wave-run/merge.md`

1. l.5: after "only after the user approves that feature" add ", or, in autonomous flow, after auto-approval
   (`layout.md`, "Flow"; `wave-run/autonomous.md`, "Auto-approval")".
2. Entry points, third row (l.14): append "Autonomous flow: "Checks", then "Auto-approval" of `autonomous.md`; no
   questions; features under manual review are shown with their merge command."
3. "Merge one feature" step 1 (l.29-30) and step 2 (l.31-35): append "Autonomous flow: `autonomous.md`,
   "Auto-approval"." to each.
4. "Record": first line "Autonomous flow: with the differences of `autonomous.md`, "Auto-approval"."

## Limits

- The manual path of `SKILL.md` and `merge.md` keeps every sentence; only conditional clauses are added.
- Never `git reset --hard`, never push, never delete a branch with `-D`, never touch `<main branch>`.
- A merge form naming a feature under manual review is the user's approval; it merges into the integration branch.

## Acceptance tests

- `git grep -c "Autonomous flow" -- skills/wave-run/SKILL.md` ≥ 9 and `git grep -c "Autonomous flow" -- skills/wave-run/merge.md` ≥ 4.
- `git grep -n "autonomous.md" -- skills/wave-run/SKILL.md skills/wave-run/merge.md skills/wave-plan/layout.md`: every
  section name it quotes ("Flow form", "Integration target", "Skipped tasks", "Points of steps 1–6", "Auto-approval",
  "Report") is a `##` heading of `skills/wave-run/autonomous.md`.
- Walkthrough "night": wave 2 of an autonomous plan, F1 ready, F2 red before the wave, task D of F3 out of scope →
  F1 auto-merged into the integration branch with `Approved-By:`; F2 ⚠️ with a new entry and its tasks skipped; D ⚠️,
  not merged, its `After` dependants skipped; no question; the report lists F1 under "Auto-merged" and why.
- Walkthrough "manual unchanged": a plan without `Flow:` → no step reads `autonomous.md`; step 10 asks as before.
