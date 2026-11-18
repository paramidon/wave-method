# P18. A task's scope is checked in every commit and never cleaned up

User problem: (re-plan, I8) in autonomous flow, task A of the scratch example committed `wordstat/__pycache__/*.pyc`
outside its file list; the coordinator deleted the files in a follow-up commit, opened no entry and auto-approved
F1, so the bytecode stayed in the integration history · feature F2

**Cause:** three gaps in the prose, each enough to let the case through:

1. The task header (`skills/wave-run/SKILL.md:232`) says "commit all your changes". In a project without a
   `.gitignore` an executor that runs `pytest` and then `git add -A` commits bytecode and caches.
2. Step 5 (`SKILL.md:252` and `:256`) checks scope with `git diff --stat`, the net change. A file added in one commit
   and removed in a later one leaves no trace in the net diff, so a cleanup commit makes the check pass. Nothing
   forbids that cleanup: the rule says what to record, not that the record is the only outcome.
3. Auto-approval (`skills/wave-plan/layout.md`, "Auto-approval") has no scope condition; it trusts step 5.

**Approach:** close all three. (1) The header tells the executor to add its files by name and never commit generated
files. (2) Step 5 lists every path that any non-merge commit of the task touched (`git log --no-merges --name-only`),
which sees a file added and removed again, and states that an out-of-scope path is never cleaned up: its only
outcomes are the entry plus the flow's answer (manual: ask the user; autonomous: revert and block). (3) Auto-approval
gets condition 6, the same scope test over the whole feature branch, so a slip in step 5 cannot reach the integration
branch. The obvious alternative, letting the coordinator delete generated files, is rejected: it hides history from
the review and was exactly the failure.

## Edits

All edits are prose except one string in the driver. Text in quotes is the new text, verbatim.

### A. Task header — `skills/wave-run/SKILL.md`, step 4

Replace the sentence that starts `When done, commit all your changes on` and ends with the trailer line, so the
header block reads:

```
Work only in the working folder. Do not edit anything under plans/. When done, commit your changes on this
branch: add every file you created or changed for the task by name (git add <file> …; never git add -A, git add .
or git commit -a), and never commit generated files (bytecode, caches, build or test output). Use the message
"<plan> <feature-id> / <task-id>: <short>", ending with a blank line and the trailer
"Wave-Model: <the exact model ID you run on>". Do not switch branches, do not
merge, do not push, do not touch other worktrees or the main checkout.
```

`skills/wave-run/task-mode.md` (the task-mode session, the line `prepared worktree, commit there (...)`): after
`commit there` insert `, adding the task's files by name and no generated files (as the header of `SKILL.md` step 4
says)`.

### B. Scope check — `skills/wave-run/SKILL.md`, step 5

1. Replace the bullet `Task branch: git diff --stat feat/<plan>/<feature>...<task branch> shows only its files …
   if such an edit conflicts with another task, ask the user.` (with its `Autonomous flow:` line) by:

   ```
   - **Scope.** List every path that any commit of the task touched, including a file added and removed again:
     task branch `git log --no-merges --name-only --format= feat/<plan>/<feature>..<task branch> | sort -u`;
     direct task `git -C <feature worktree> log --no-merges --name-only --format= H..HEAD | sort -u`. A path is in
     scope when it equals a path in backticks of the task's `Files` cell in the wave file's task table, or lies
     under such a path that ends with `/`; a path under `plans/` is never in scope. Any other path is an
     out-of-scope edit.
   ```

2. In the bullet `Direct task: git -C <feature worktree> status --porcelain is empty (…); git log H..HEAD is not
   empty; git diff --stat H HEAD shows only the task's files …`, replace it by:

   ```
   - Direct task: `git -C <feature worktree> status --porcelain` shows no change to a tracked file and no untracked
     path that is one of the task's files (otherwise use the fix loop and ask it to commit its files); untracked
     generated files (bytecode, caches) stay uncommitted. `git log H..HEAD` is not empty.
   ```

3. Replace the bullet `Out-of-scope edits or unusable direct work: record it in problems.md and ask the user. …
   the default undo is git revert --no-edit H..HEAD.` (with its `Autonomous flow:` line) by:

   ```
   - Out-of-scope edits or unusable direct work: one entry in `problems.md`,
     `out of scope: <paths> (<commit hashes>)` for a scope failure, then ask the user. An out-of-scope path is
     never cleaned up instead: no commit that deletes or restores it, no amend or rebase, no fix loop for it. The only undo
     is `git revert --no-edit H..HEAD` for a direct task (never `git reset --hard` the feature branch without the
     user's explicit OK) and leaving a task branch unmerged.
     Autonomous flow: `autonomous.md`, "Points of steps 1–6".
   ```

### C. Autonomous flow — `skills/wave-run/autonomous.md`

1. "Points of steps 1–6", the bullet `Step 5, an out-of-scope edit or unusable direct work:` — append after
   `its dependants are skipped.`:
   `The paths come from the scope command of SKILL.md step 5, so a file added and removed again counts. The revert
   is the only undo: never a commit that deletes the paths, and the feature stays ⚠️ blocked even when the revert
   leaves its branch clean.` (Put `SKILL.md` in backticks as the file does.)
2. "Auto-approval", item 2: `Conditions 1, 3 and 4` → `Conditions 1, 3, 4 and 6`; after the sentence about the
   trailers add: `For 6 run git log --no-merges --name-only --format= <main>..feat/<plan>/<feature> | sort -u and
   compare it with the Files cells of the feature's tasks in every wave file, as SKILL.md step 5 "Scope" does.`
   (commands in backticks); and `for 4 a new entry below tier: …` gets `; for 6 a new entry
   out of scope at approval: <paths> (<commit hashes>)` (in backticks like the existing entry text).

### D. Rules — `skills/wave-plan/layout.md`

1. "Auto-approval": after condition 5 add
   `6. its scope is clean: every path that a non-merge commit of <main>..feat/<plan>/<feature> touched
   (git log --no-merges --name-only --format=) is in scope for one of the feature's tasks as wave-run/SKILL.md
   step 5, "Scope", defines it.` (paths and commands in backticks). In the table below, `1, 2, 3 or 4` →
   `1, 2, 3, 4 or 6` and `(a new entry for 2 and 4)` → `(a new entry for 2, 4 and 6)`.
2. "Feature review", the merged-block template line `Approved: <auto — every task ✅ or ➖, check green, no open
   entry, tier gate clean, not under manual review · by the user>`: insert `scope clean, ` before
   `not under manual review`.
3. "Decision table", row `an out-of-scope edit, or unusable direct work`: the autonomous cell becomes
   `entry; do not merge the task (a direct task is reverted, never cleaned up by a new commit); the task is ⚠️ and
   the feature ⚠️ blocked; skip its dependants`; the manual cell becomes `entry; ask the user; never cleaned up by a
   new commit`.
4. "Statuses", the **Status check** bullet: after the sentence that names `flow-line` and `flow-review-unknown`
   add `It also reports merged-fields for a feature that is ✅ merged without a Merged hash or with a Waiting for,
   and for a feature that is not ✅ merged but has a Merged hash.` (rule name and column names in backticks; this
   documents P19's script rule).

### E. Driver — `scripts/wavedriver/report.py:81`

The auto-approval string becomes
`"auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review"`,
the same words as D.2.

## Limits

- A coordinator's own non-merge commit on a feature branch (step 6, "fix it yourself … small and mechanical") is
  checked by condition 6 like any other: if it touches a path outside every task of the feature, the feature is
  blocked for the user's review. That is intended.
- Merge commits are excluded (`--no-merges`): they bring `<main>` and the plan folder, which are not the feature's.
- Old plans whose `Files` cells hold folder names without a trailing `/` are matched only by equality; such a plan
  may block at condition 6 and is then reviewed by the user, the safe side.

## Acceptance tests

1. `git grep -n "commit all your changes" skills` prints nothing; `git grep -n "git add -A" skills/wave-run/SKILL.md`
   prints the header line.
2. `git grep -n -e "--name-only --format=" skills/wave-run/SKILL.md skills/wave-run/autonomous.md
   skills/wave-plan/layout.md` prints at least 4 lines (two in step 5, one in autonomous "Auto-approval", one in
   layout condition 6).
3. `git grep -n "scope clean" skills/wave-plan/layout.md scripts/wavedriver/report.py` prints exactly one line per
   file; `git grep -n "1, 2, 3, 4 or 6" skills/wave-plan/layout.md` prints one line.
4. `git grep -n "never cleaned up\|never a commit that deletes" skills/wave-run skills/wave-plan/layout.md` prints
   the step 5 bullet, the autonomous point and both decision-table cells.
5. `python -m unittest discover -s scripts/tests` → 59 tests OK; `git diff --check` clean; every table row changed in
   `layout.md` has the same cell count as its header.
6. Behaviour: task O (wave 6) forces an out-of-scope file into task B's commit and expects an entry, a revert and
   F2 ⚠️ blocked (`solutions/P21-rehearsal-isolation-rerun.md`).
