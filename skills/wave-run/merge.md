# wave-run — feature review and merge

Read by the `wave-run` coordinator only when `SKILL.md` step 1 says so.

A feature is merged into `<main>` only after the user approves that feature. The one-feature-per-branch rule, the
review commands and what counts as approval: `layout.md`, "Feature review".

## Entry points

| Entry | What runs |
|---|---|
| `SKILL.md` step 10: the user's answer after a wave | "Merge one feature" for each approved feature, "Rejection" for each rejected one, then "Record" |
| `/wave-run <plan folder> merge <F-IDs>`<br>`$wave-run <plan folder> merge <F-IDs>` | "Checks", then "Merge one feature" for each named feature in "Features" order, then "Record". Naming a feature in this command is the approval. |
| `/wave-run <plan folder>`<br>`$wave-run <plan folder>` with no wave ⬜ or ❌ | "Checks"; then the "Ready for review" blocks of `SKILL.md` step 9 for every `👀 review` feature and the questions of step 10; merge only what the user approves. No feature `👀 review` → stop `nothing-to-run`. |

## Checks

- `SKILL.md` step 1, only the lock (`wave-running`) and the record of features the user merged. Its records go
  into the commit of "Record", not into a "started" commit.
- `SKILL.md` step 2: the tracking worktree, without a "started" commit.
- Every feature the merge command names is `👀 review`, or merged by the user (then it is only recorded). Otherwise
  stop `not-ready` before merging anything, naming the feature, its status and its `Waiting for`.

## Merge one feature

1. In its feature worktree (if it is gone: `git worktree add <feature worktree path> feat/<plan>/<feature>`, path
   from `layout.md`, "Names"): `git merge <main>` if `<main>` moved since the feature became ready, resolve
   conflicts as in `SKILL.md` step 6, run the **full** check command. Red → the feature becomes ⚠️ blocked with a
   new problem entry; do not merge. If resolving a conflict changed lines of the feature's own changes, show the
   resolution to the user and ask again before merging: they approved a different diff.
2. Check main readiness for `feat/<plan>/<feature>` (`layout.md`, "Main readiness"). Not ready → tell the user
   the reason (the staged files, the overlapping paths, or the branch) and ask them to clear it and answer when
   done; on the answer check again. Never stage, unstage, stash or reset anything yourself. If the user leaves it
   for later, the feature keeps `👀 review` with `Waiting for: main-dirty`; `/wave-run <plan folder> merge <F-ID>` ·
   `$wave-run <plan folder> merge <F-ID>` merges it later.
3. `git -C <main checkout> merge --no-ff feat/<plan>/<feature> -m "Feature <feature-id> (<plan>): <title>"`,
   body: one line per task of the feature. Note the merge hash.

Several features are merged one at a time, each with its own merge commit. A later one gets the earlier ones from
`<main>` in its step 1.

## Rejection

The user answers `problems F<k>: <findings>`, or says what is wrong with a ready feature:

- each finding becomes one entry of `problems.md`, `**[I<n> · review / feature F<k>] <essence>**`, close to the
  user's words, with `status: open`;
- the feature becomes `⚠️ blocked I<n>` with `Waiting for: I<n>`; its branch and worktree stay;
- the next command is `/wave-plan <plan folder>` · `$wave-plan <plan folder>`: the re-plan adds fix tasks to the
  same feature, and a later wave makes it ready again.

## Record

In the tracking worktree, after the merges and rejections of this run:

- README "Features": a merged feature gets `✅ merged`, an empty `Waiting for` and the short merge hash in
  "Merged"; a rejected one as in "Rejection"; a feature left for later keeps its row.
- The Execution of the wave file of the feature's last wave (the last wave in its "Tasks (wave)" cell) gets one line
  per feature: `Merged <YYYY-MM-DD HH:MM>: <feature-id> <hash>` or `Rejected <YYYY-MM-DD HH:MM>: <feature-id> → I<n>`.
- New entries: as `SKILL.md` step 8 ("New problems").
- Run the status check (`layout.md`, "Statuses"); archive if eligible (`layout.md`, "Archive").
- Make **one** commit `Plan <plan>: merge — <parts>`, where `<parts>` joins with `; ` only the parts that apply,
  in this order: `<IDs> merged`, `<IDs> blocked`, `archived` (for example `merge — F1 merged; archived`,
  `merge — F2 blocked`). If nothing changed, write nothing and report why.
- If a feature was merged or recorded as merged: **one**
  `git -C <main checkout> merge --no-ff plan/<plan> -m "Plan <plan>: status after merging <IDs>"`, under the
  same main-readiness rule (for `plan/<plan>`).
- Remove the worktrees of merged features and `git branch -d feat/<plan>/<feature>`. When the plan is archived,
  remove the tracking worktree and `git branch -d plan/<plan>`.

## Report

- Per feature: merged (hash), left for later (`review`, or `main-dirty` with the reason), or rejected (its entries).
- Conflicts resolved while merging `<main>` into a feature branch, and the check result.
- The next command, as in `SKILL.md` step 9 (another ready feature, a later wave, open problems), or
  `finished; archived` when the plan was archived.
