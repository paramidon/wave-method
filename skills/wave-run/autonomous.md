# wave-run — autonomous flow

Read by the `wave-run` coordinator only when `SKILL.md` step 1 says so: the plan's flow is autonomous, or the
arguments are `flow …`. What autonomous flow does at each point where manual flow asks or waits, the auto-approval
conditions and the integration branch: `layout.md`, "Flow". This file says how; it does not repeat the decision
table.

Never ask the user a question in autonomous flow. A situation the decision table does not cover stops the wave with
the closest code of `SKILL.md`, "Stops"; its `next:` says what the user must decide.

## Flow form

`/wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` ·
`$wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]`

1. A wave of the plan is 🔄 (also one waiting for task mode) → stop `wave-running`.
2. `autonomous`: `<name>` is the `<name>` of the current `target:`, else `<plan>`; run the checks of "Integration
   target", step 1. `manual`: the integration branch of the current `Flow:` line exists and
   `git rev-list --count <main branch>..integration/<name>` is not 0 → stop `target-unmerged`.
3. Tracking worktree as `SKILL.md` step 2, without preparing the integration target or making a "started" commit.
   In the README header write the `Flow:` line,
   replacing an existing `Flow:` line, else right after the `- Re-plans:` line. For `autonomous`:
   `- Flow: autonomous · target: integration/<name> · manual review: <F-IDs>`, where the last part is present only
   when the list is not empty (`review <F-IDs>` replaces the list; `review none` empties it; without `review` the
   list stays). For `manual`: `- Flow: manual`.
4. Commit `Plan <plan>: flow <manual|autonomous>` on the tracking branch. Nothing else changes: features already
   `👀 review` stay so; the next run applies the new flow to them.
5. Report: `wave-run/report.md`, "Flow report".

## Integration target

Step 1, right after the README is read; it writes nothing but the target claim.
`<name>` comes from `target:`, else it is `<plan>`. Stop
`target-unsafe` (nothing written), naming the check that failed, when:

1. `target:` is present and is not `integration/<name>` with a kebab-case `<name>`;
2. `git worktree list --porcelain` shows `refs/heads/integration/<name>` at a path other than the integration worktree
   (`layout.md`, "Names"), the main checkout included;
3. the integration worktree path exists and is not a worktree of this repository;
4. the integration worktree exists and is not on `integration/<name>`
   (`git -C <integration worktree> branch --show-current`), or has tracked changes
   (`git -C <integration worktree> status --porcelain --untracked-files=no`), or an unfinished merge
   (`git -C <integration worktree> rev-parse -q --verify MERGE_HEAD` succeeds).

Then take the target claim (`layout.md`, "Target claim"), holder line `<plan> wave <N> <YYYY-MM-DD HH:MM>`, or
`<plan> merge <YYYY-MM-DD HH:MM>` in the merge form; refused → stop `wave-running`, naming the holder, nothing
written, unless this run resumes the holder's own wave (it takes the claim over). The flow form runs the checks
above and takes no claim. Then: another plan of the same target (`layout.md`, "Integration target") has a 🔄
wave on its tracking branch → stop `wave-running`, naming that plan and wave. From the claim on, every stop
releases the claim before its report.

For the merge-record check of `SKILL.md` step 1, read `<main>` as `integration/<name>`, or as `<main branch>`
if that branch is missing and will be created at its head.

Step 2, before the tracking worktree and the "wave started" commit:

1. Branch missing: `git worktree add -b integration/<name> <integration worktree> <main branch>`. Branch without a
   worktree: `git worktree add <integration worktree> integration/<name>`.
2. `git merge-base --is-ancestor <main branch> integration/<name>` fails →
   `git -C <integration worktree> merge --no-ff <main branch> -m "Integration <name>: bring in <main branch>"`. A
   conflict → `git -C <integration worktree> merge --abort`, stop `target-conflict`; the wave stays ⬜.
3. From here on `<main>` is `integration/<name>` and `<main checkout>` the integration worktree, in every step.

Step 3, release: right after the run's last write to the integration worktree (the end of "Auto-approval", in a
wave and in the merge form), release the target claim (`layout.md`, "Target claim"). A run that ends with
`Waiting: task mode …` keeps it; the resume takes it over.

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
- **Step 1, leftover task branches or worktrees:** neither reuse nor delete them. Stop `leftover-branches`: the line is
  `Stop leftover-branches: wave <N> has <branches> — next: …`, where `next:` says the user continues from them or
  deletes them, then runs `/wave-run <plan folder> <N>` · `$wave-run <plan folder> <N>`.
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

1. Apply condition 5 of `layout.md`, "Auto-approval", and its outcome on failure.
2. Conditions 1, 3 and 4 of `layout.md`, "Auto-approval". For 4 run
   `git log --no-merges --format="%h %s%n%(trailers:key=Wave-Model,valueonly)" <main>..feat/<plan>/<feature>` and
   use `layout.md`, "Model tiers", or the README `Models:` line to evaluate the trailers. A failure → the feature is
   `⚠️ blocked I<n>`; for 4 a new entry `below tier: <model> ran a <tier> task (<hash>)`.
3. `merge.md`, "Merge one feature", step 1. Red → the feature is `⚠️ blocked I<n>` with a new entry, as in 2; do not
   merge. When resolving a conflict changed lines of the feature's own changes: do not merge; a new entry
   `merging <main> changed F<k>'s own lines in <files>: needs the user's review`; the feature is `⚠️ blocked I<n>`.
4. Step 2 of the same: apply the "Auto-approval" outcome for `<main checkout>` readiness in `layout.md`;
   record the reason in the report.
5. Step 3 of the same, with one more body line after the task lines: `Approved-By: wave-run autonomous flow`.

Then `merge.md`, "Record", with these differences:

- the Execution line is `Merged <YYYY-MM-DD HH:MM>: <feature-id> <hash> (auto-approved)`; a feature left unmerged gets
  `Not merged <YYYY-MM-DD HH:MM>: <feature-id> — <manual review · I<n> · main-dirty>`;
- the brief `reviews/<feature>.md` of every merged feature gets the header line
  ``- Merged <YYYY-MM-DD HH:MM> into `integration/<name>` `<hash>`, auto-approved`` after its `👀 review since` line;
- remove the worktree of a merged feature but keep its branch; `wave-status` lists it as a leftover once the
  integration branch is in `<main branch>`;
- no archive: the tracking branch and its worktree stay (`layout.md`, "Archive");
- the tracking branch is merged into `<main checkout>`, the integration worktree.

A feature under manual review that the user approves with the merge form is merged into the integration branch by
`merge.md` as in manual flow; its brief gets the same header line ending `approved by the user`.

## Report

`wave-run/report.md`: the `Flow:` line and the "Auto-merged" section; no merge questions.
