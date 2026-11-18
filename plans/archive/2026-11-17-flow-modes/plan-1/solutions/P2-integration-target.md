# P2. Integration target: autonomous merges never reach the main branch

User problem: autonomous merges go to an integration target the user reviews as one diff and merges themselves;
autonomous flow refuses to start (clear stop code) when it cannot guarantee this · feature F1

## Cause

`<main>` means both "the repository's main branch" and "where an approved feature is merged"
(`skills/wave-plan/layout.md:137`). Every merge of `wave-run` targets it: `skills/wave-run/merge.md:36` (feature),
`merge.md:66` and `skills/wave-run/SKILL.md:317` (tracking branch), and every feature branch starts from and takes in
`<main>` (`SKILL.md:171`, `:173`, `:269`). "Main readiness" (`layout.md:205-217`) assumes the main checkout.

## Approach

**An integration branch in the same repository, with its own worktree; in autonomous flow `<main>` and
`<main checkout>` resolve to it.** Every existing rule that uses `<main>` (feature branches start from it and take it
in, features merge into it, the tracking branch merges into it, main readiness, merge-hash detection) then works on
the integration branch unchanged, so the merge mechanics of `merge.md` do not change. `<main branch>` is the new name
for the repository's main branch in every flow; nothing in autonomous flow writes it.

Alternatives considered:

- **A `Main:` override in the README** pointing at any branch: the same mechanism without its rails. The user could
  name a branch they work on or keep checked out in the main checkout. The integration branch is that override with
  a fixed name pattern, a dedicated worktree and the safety checks below.
- **A night clone** (a throwaway clone where the plan runs): isolates even the refs, but the plan's tracking branch,
  feature branches and statuses then live in another repository; `wave-status` in the main checkout cannot see them;
  results come back only by a fetch from a local path; and every rule that names `<repo-folder>.worktrees` needs a
  second meaning. That is the 4+ task variant. The integration branch does not prevent it: a driver (part 3) may still
  run everything inside a clone, where the same rules apply.

Why the main branch is merged into the integration branch before each wave: the user keeps working on the main branch
during the day and merges the integration branch in the morning. Without this, a second night would build features on
a stale base and the morning merge would conflict more. The merge only reads the main branch.

## Exact text for layout.md

### Names (replaces the `<main>` bullet, `layout.md:137`)

```markdown
- `<main branch>` — the repository's main branch (`master` or `main`), in every flow.
- `<main>` — where approved features are merged: `<main branch>` in manual flow, the plan's integration branch in
  autonomous flow ("Flow"). Only `wave-run` and `wave-status` resolve it by the flow; `wave-plan` and `wave-triage`
  always use `<main branch>`.
- `<main checkout>` — the checkout where those merges are made: the repository's main checkout in manual flow, the
  integration worktree in autonomous flow.
```

Add a row to the branch table of "Names", after the "task" row:

```markdown
| integration (autonomous flow) | `integration/<name>` | `../<repo-folder>.worktrees/integration-<name>` |
```

### Integration target (subsection of "Flow", after its bullet list)

```markdown
### Integration target

In autonomous flow `<main>` is the integration branch and `<main checkout>` the integration worktree ("Names"). Every
merge that manual flow makes into `<main branch>` goes there instead; autonomous flow never changes `<main branch>` or
the main checkout.

- `wave-run` creates the integration branch from the head of `<main branch>`, in the integration worktree, when it is
  missing, and merges `<main branch>` into it before a wave when `<main branch>` has commits it lacks
  (`wave-run/autonomous.md`, "Integration target"). Nothing else checks it out.
- It receives only `merge --no-ff`: approved feature branches, the tracking branch and `<main branch>`. Nothing is
  committed on it directly.
- The user reviews it as one diff, `git diff <main branch>...integration/<name>`, and merges it into `<main branch>`
  themselves (`git merge --no-ff integration/<name>` in the main checkout). No skill does.
- Autonomous flow refuses to start a wave when it cannot guarantee this: stop `target-unsafe` before anything is
  written, when `target:` is not `integration/<name>`; the integration branch is checked out anywhere but the
  integration worktree; or the integration worktree is not on that branch, has tracked changes, or has an unfinished
  merge.
```

### Main readiness (`layout.md:205-217`)

- First sentence: "The main checkout is ready for a merge of branch `B` when all of these hold:" →
  "`<main checkout>` is ready for a merge of branch `B` when all of these hold:".
- Last sentence: "Never stage, unstage, stash, reset or check out anything in the main checkout to make it ready." →
  "… in `<main checkout>` to make it ready." The three numbered checks stay as they are (they already use
  `<main>` and `<main checkout>`).

## Procedure (text of `skills/wave-run/autonomous.md`, "Integration target")

Step 1 of `wave-run`, read-only, after the README is read and the flow is autonomous. `<name>` comes from `target:`,
else it is `<plan>`. Stop `target-unsafe` (a stop before the wave started: nothing written), naming the check that
failed, when:

1. `target:` is present and is not `integration/<name>` with `<name>` in kebab-case;
2. `git worktree list --porcelain` shows `refs/heads/integration/<name>` checked out at a path other than the
   integration worktree (`layout.md`, "Names"), including the main checkout;
3. the integration worktree path exists and is not a worktree of this repository;
4. the integration worktree exists and `git -C <integration worktree> branch --show-current` is not
   `integration/<name>`, or `git -C <integration worktree> status --porcelain --untracked-files=no` is not empty, or
   `git -C <integration worktree> rev-parse -q --verify MERGE_HEAD` succeeds.

Step 2 of `wave-run`, before the tracking worktree and the "wave started" commit:

1. Branch missing: `git worktree add -b integration/<name> <integration worktree> <main branch>`. Branch without a
   worktree: `git worktree add <integration worktree> integration/<name>`.
2. `git merge-base --is-ancestor <main branch> integration/<name>` fails →
   `git -C <integration worktree> merge --no-ff <main branch> -m "Integration <name>: bring in <main branch>"`. A
   conflict → `git -C <integration worktree> merge --abort` and stop `target-conflict` (before the wave started;
   the wave stays ⬜).
3. From here on `<main>` is `integration/<name>` and `<main checkout>` the integration worktree, in every step.

## Stop codes (rows for the table of `skills/wave-run/SKILL.md`, "Stops")

```markdown
| `target-unsafe` | autonomous flow cannot guarantee that merges stay on the integration branch (`layout.md`, "Integration target"); the line names the failed check | fix what the line names (free the integration branch, clean or remove its worktree), then run the same command again |
| `target-conflict` | merging `<main branch>` into the integration branch conflicts (`wave-run/autonomous.md`) | merge `integration/<name>` into `<main branch>`, or `<main branch>` into it, yourself; then run the same command again |
| `target-unmerged` | the flow form switches to manual while the integration branch has commits `<main branch>` lacks | review `git diff <main branch>...integration/<name>`, merge it yourself, then run the flow form again |
```

## Limits

- No command of autonomous flow writes `<main branch>` or runs in the main checkout; the main checkout is only read
  (`git worktree list`, `merge-base`, `rev-list`).
- Never push; never delete the integration branch (the user does that after merging it).
- The integration branch belongs to one plan in part 1. Sharing one branch across the parts of an index (`target:`
  naming the index topic) is part 2's design (P10).

## Acceptance tests

- Walkthrough "first night": plan with `Flow: autonomous`, no integration branch → step 2 creates `integration/<plan>`
  at the head of `main` in `../<repo>.worktrees/integration-<plan>`; feature branches start from it; an auto-approved
  feature is merged there; `git rev-parse main` is the same before and after the run.
- Walkthrough "unsafe": the user checked out `integration/<plan>` in the main checkout → stop `target-unsafe` naming
  check 2; no branch, worktree or commit was created.
- Walkthrough "main moved": `main` got 3 commits since the last night → step 2 merges `main` into the integration
  branch; a conflict → `merge --abort`, stop `target-conflict`, the wave stays ⬜.
- `git grep -n -e "<main branch>" -e "integration/<name>" -- skills/wave-plan/layout.md` shows the Names bullets, the
  branch-table row and the "Integration target" subsection.
