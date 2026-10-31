---
name: wave-run
description: Third stage of the wave-triage → wave-plan → wave-run pipeline. Execute one wave of a plan folder written by wave-plan — run the tasks as subagents (in parallel where the environment allows; a task worktree only for concurrent tasks of one feature), merge each task branch into its feature branch, resolve conflicts, run the tests, record task, wave and feature status plus found problems on the plan's tracking branch, keep earlier statuses current when problems close, offer each feature whose tasks (possibly spread over several waves) are all done for the user's review on its own branch, merge it into the main branch only when the user approves that feature (in the same session, or later with "/wave-run <plan> merge <F-ID>"), and archive the plan when it is finished. Uses a run lock and stop codes. Waves of different plans may run at the same time. Use when the user says "/wave-run <plan> <N>", "запусти волну N", "/wave-run <plan> merge F1", "смержи фичу", or asks to run the next wave of a plan in plans/ or to merge a reviewed feature. Recommended model: medium complexity (Sonnet 5.5 / GPT-6.1 SOL / Gemini 4 Argon) — the coordinator only dispatches, merges, checks and records; but a wave with high tasks needs access to a high-complexity model for its tasks.
---

# wave-run — execute one wave of a plan

Language: `wave-plan/layout.md`, "Language".

Skill paths such as `wave-plan/layout.md` are relative to the wave skills folder, the parent of this skill's
folder (`wave-plan/layout.md`, "Skill paths").

## Layout

Read `wave-plan/layout.md` first: plan folder layout, **what the coordinator reads**, model
tiers, branch and worktree names, status rules, "Running waves", the problem-log format and the Markdown
rules, "Main readiness", "Feature review" and "Archive". It is the single source of truth; this skill does not
repeat it.

Arguments: the plan folder and the wave number. Without a number, take the first wave with status ⬜ or ❌; if
there is none but a feature is `✅ ready`, offer the ready features for review (see `wave-run/merge.md`).
Without a folder, take the most recent plan folder in `plans/` (not under `archive/`) that has unfinished waves
or a `✅ ready` feature, and name it to the user. Task-mode forms:
`/wave-run <plan folder> <N> task <ID>` · `$wave-run <plan folder> <N> task <ID>`. Merge form (the user approves
the named features after review): `/wave-run <plan folder> merge <F-IDs>` · `$wave-run <plan folder> merge <F-IDs>`
(see `wave-run/merge.md`).

The coordinator does not write task code itself (except merge-conflict resolution) and does not change the
plan's solutions.

## Model of work

- A **feature** is one deliverable; its tasks may span waves. A **wave** only schedules tasks that can run together.
- Tasks run on the **feature branch** (direct) or on task branches merged back into it (step 4). A feature branch
  holds only its own feature, so it is the branch the user reviews (`layout.md`, "Feature review").
- A feature whose tasks are all ✅ or ➖ and whose full check is green becomes `✅ ready` and waits for the user's
  review. It reaches `<main>` only when the user approves that feature (step 10, `wave-run/merge.md`).
- Statuses and problem entries live on the **tracking branch** `plan/<plan>`; task and feature branches never edit
  `plans/`. The tracking branch is merged into `<main>` once per run that merges a feature.

## Hard rules

- **Nothing is ever committed directly on the main branch** (`master`/`main`). It only receives
  `merge --no-ff` of an approved feature branch and of the tracking branch (`wave-run/merge.md`).
- **The coordinator never works in the main checkout.** All edits, git commands and builds run in the
  worktrees below (use `git -C <path>` or set the working folder there). The main checkout is touched only
  for reading and for the final merges.
- **A feature is never merged into the main branch partially**: not while any of its tasks is ⬜, 🔄, ⚠️ or ❌.
- **A feature is never merged without the user's approval** of that feature (`layout.md`, "Feature review"). A
  wave only makes it `✅ ready`; there is no "merge all" default.
- **A task is never run on a model below its tier** (see "Environment capabilities").
- Never push.

## Environment capabilities

Tiers: `layout.md`, "Model tiers" (a README `Models:` line may name concrete models of the same tier or higher).
The coordinator is always `medium`.
In step 1 determine the capabilities of `layout.md`, "Environment capabilities", and write them into the wave
file's Execution (`Capabilities: …`).

| Capability | Used for | If missing |
|---|---|---|
| subagents | every task | every task runs in task mode |
| parallel subagents | one launch group at once | launch the group's tasks one after another; same worktrees and checks |
| model choice per subagent | tiers | a task whose tier is at most the default subagent model's tier runs as usual; a higher task runs in task mode on a model of its tier; no such model in the environment → stop `tier-missing` |
| continuing a subagent | commit requests, fixes, conflicts | a new subagent of the same tier gets the original prompt, the previous report, the diff of its work and the error text; it counts as an attempt |
| a tool from the task's `Needs` | that task | the task runs in task mode, in a session that has the tool |
| built-in worktree isolation | optional | `git worktree add` as in step 4 (the default) |

A task that cannot run as a subagent runs in **task mode** (one task in one fresh session):
`wave-run/task-mode.md`.

## Names

`<main>`, `<plan>`, `<plan folder>`, `<feature>`, `<task>` and the branch and worktree of each: `layout.md`,
"Names". Every name carries the plan, the feature and the task, so branches of different plans, features and
waves never look alike.

## Stops

Every stop prints `Stop <code>: <one line> — next: <command or action>` as the first line of the report.
A stop after the wave started is also the last line of the wave file's "Execution" and is committed with
`Plan <plan>: wave <N> stopped`. A stop before the wave started writes nothing, except `plan-defect`: its entry is
appended to `problems.md` on the tracking branch (tracking worktree as in step 2) and committed as
`Plan <plan>: plan defect I<n>`; the wave stays ⬜.

| Code | When | Next |
|---|---|---|
| `wave-running` | a wave of this plan is 🔄, unless it is this wave waiting for task mode | wait for it, or the user releases the lock |
| `earlier-wave-open` | an earlier wave is ⬜, 🔄 or ❌ | run or re-plan that wave |
| `feature-unmerged` | the wave file's `Depends on:` names `F<k> merged` and F<k> is not `✅ merged` | review F<k> (`layout.md`, "Feature review"), then `/wave-run <plan folder> merge F<k>`<br>`$wave-run <plan folder> merge F<k>` |
| `leftover-branches` | task branches or worktrees of this wave exist | the user: continue from them, delete them, or stop |
| `open-problems` | open entries concern this wave and the user said stop | `/wave-plan <plan folder>`<br>`$wave-plan <plan folder>` |
| `plan-defect` | the wave file lacks something the wave needs | `/wave-plan <plan folder>`<br>`$wave-plan <plan folder>` |
| `tier-missing` | no model of a task's tier exists in this environment | re-slice, or run from an environment that has it |
| `capability-missing` | a needed capability is missing and task mode cannot help | see "Environment capabilities" |
| `red-before-wave` | a feature check is red after merging `<main>` in, before the wave | the user decides: fix or re-plan |
| `red-after-merge` | a task stays red after 2 attempts | `/wave-plan <plan folder>`<br>`$wave-plan <plan folder>` (the task is ⚠️) |
| `design-conflict` | a merge conflict would change a plan solution | the user decides |
| `not-ready` | the merge form names a feature that is not `✅ ready` and not merged by the user | `/wave-status <plan folder>`<br>`$wave-status <plan folder>` |
| `nothing-to-run` | no wave is ⬜ or ❌ and no feature is `✅ ready` | `/wave-status <plan folder>`<br>`$wave-status <plan folder>` |

`main-dirty` is not a stop: the approved feature keeps `✅ ready` with `Waiting for: main-dirty`; the report gives
the reason, and `/wave-run <plan folder> merge <F-ID>` · `$wave-run <plan folder> merge <F-ID>` merges it once the
main checkout is ready (see `wave-run/merge.md`).

## Fix loop

When a task's work must change — uncommitted changes, a red check, a conflict that needs the task's logic, a
missing report block — send the request (what to commit, the error text, or the conflict description) to the
same subagent, or its replacement ("Environment capabilities", row "continuing a subagent"). It commits on its
branch (a direct task: on the feature branch); merge a task branch again, then repeat the check that failed. A red
check gets at most 2 attempts per task; then the task is ⚠️ with a problem entry, and if no other task can
continue, stop `red-after-merge`.

## Steps

### 1. Readiness check (read-only, except a plan-defect entry)

- Find the tracking worktree: `git worktree list`. If `plan/<plan>` exists, read the plan folder there;
  otherwise read it from `<main>`.
- **Extra files.** Read `task-mode.md` when the arguments are `… task <ID>`, when this wave's Execution ends with
  `Waiting: task mode …`, or when the capability check below sends a task to task mode. Read `merge.md` when the
  arguments are `merge <F-IDs>`, when no wave is ⬜ or ❌, or in step 10 when the user approves a feature. Read
  nothing else of the `wave-run` folder.
- A wave of this plan is 🔄 → stop `wave-running`, unless it is this wave and its Execution ends with
  `Waiting: task mode …` (resume, see `wave-run/task-mode.md`). A task-mode session uses the checks of
  `task-mode.md` instead and does not start another coordinator.
- Read `README.md`, `waves/w<NN>.md` of this wave and `problems.md` (if it exists). Nothing else of the plan:
  the wave file holds everything the wave needs. If something is missing (a prompt, a file list, a dependency),
  that is a defect of the plan — stop `plan-defect` (see "Stops") and do not search other wave
  files, `history.md` or `archive/` for it.
- All earlier waves of this plan are ✅, ⚠️ or ➖ on the tracking branch. Otherwise stop `earlier-wave-open` and
  say which one. Waves of the same plan never run in parallel; waves of different plans may.
- Detect the environment capabilities above and check every task's tier and `Needs`. A task that cannot use
  a subagent uses task mode. If no model of its tier exists in the environment, stop `tier-missing` before
  creating anything. If a needed capability is missing and task mode cannot help, stop `capability-missing`.
- Task branches or task worktrees of this wave already exist (`git branch --list "task/<plan>/*-w<N>-*"`) →
  show them and ask whether to continue from them, delete them, or stop `leftover-branches`. Never reuse them
  silently. A task-mode resume expects its prepared branches and checks them in step 5 instead.
- Open entries in `problems.md` (if any) that concern this wave's tasks or their features (and are not `→` a task
  of this wave): show them and ask whether to proceed. If the user declines, stop `open-problems`.
- A feature branch merged into `<main>` (`git branch --merged <main> "feat/<plan>/*"`) whose README row is not
  `✅ merged` (the user merged it, or a run was interrupted): write `✅ merged`, an empty `Waiting for` and the hash
  of the merge (`layout.md`, "Feature review") into the README in the "wave N started" commit.
- Every feature that the wave file's `Depends on:` line names as `F<k> merged` is `✅ merged` (counting the repair
  above). Otherwise stop `feature-unmerged`, name the feature and its branch, and give its merge command.
- Uncommitted changes in the main checkout do not matter at this step; do not touch them.

### 2. Tracking worktree

- If there is no `plan/<plan>` branch: `git worktree add -b plan/<plan> ../<repo-folder>.worktrees/<plan>-plan <main>`.
- If the branch exists without a worktree: `git worktree add ../<repo-folder>.worktrees/<plan>-plan plan/<plan>`.
- In the README set the wave to `🔄 since <YYYY-MM-DD HH:MM>` in "Waves", its tasks to 🔄 in "Tasks", their
  features to 🔄 in "Features" (if ⬜), and apply the interrupted-run repair from step 1. The wave file's
  "Execution" gets `Started <YYYY-MM-DD HH:MM>.` and `Capabilities: …` in the same commit on the tracking
  branch: `Plan <plan>: wave <N> started`. A task-mode resume keeps the existing start record.
- Do not merge features that are `✅ ready` from earlier runs: they wait for the user (step 9 offers them again).

### 3. Feature worktrees

For each feature that has a task in this wave:

- No feature branch yet: `git worktree add -b feat/<plan>/<feature> ../<repo-folder>.worktrees/<plan>-<feature-id> <main>`.
- Branch exists without a worktree: `git worktree add <path> feat/<plan>/<feature>`.
- Bring it up to date: in the feature worktree `git merge <main>` (this brings in features merged since,
  which later tasks may rely on), resolve conflicts as in step 6, run the check command. A red check here is
  a problem of the feature before the wave: record it and stop `red-before-wave` for the user's decision.
- Write the feature branch into the "Branch" column of "Features".

### 4. Launch groups and placement

| Rule | What it says |
|---|---|
| Launch groups | Group 1 is every task whose `After` is `—`. A task starts when every task in its `After` is in its feature branch and the check command is green. A group launches at once; without parallel subagents, its tasks run one after another with the same worktrees and checks. |
| Placement | A task runs **direct** (feature worktree, feature branch) unless another task of its feature is in the same group; then each such task gets a task worktree and branch (`layout.md`, "Names"). Direct tasks of different features may share a group. |
| Task mode | A task that step 1 sent to task mode is prepared in its worktree but not launched (`task-mode.md`). |

For every task that needs a task worktree:

```bash
git worktree add -b task/<plan>/<feature-id>-w<N>-<task> ../<repo-folder>.worktrees/<plan>-w<N>-<task-id> feat/<plan>/<feature>
```

Built-in worktree isolation may be used instead, as long as the task starts from its feature branch head and
ends committed on its own branch named as above. For a direct task, note `H = git -C <feature worktree> rev-parse HEAD` before launch.
Model = the task's complexity tier. Launch each task as a subagent with this header followed by its code block from the wave file **verbatim**:

```
Working folder: <absolute task worktree path, or the feature worktree for a direct task>.
Branch: <task branch, or the feature branch for a direct task> (already checked out).
Report language: <the language of the user's messages in this session>.
Plan folder (read-only): <absolute path of the plan folder in the tracking worktree>. Read only the files of
it that the task names (paths are relative to the plan folder); do not read other waves, history or archive.
Work only in the working folder. Do not edit anything under plans/. When done, commit all your changes on
this branch with the message "<plan> <feature-id> / <task-id>: <short>". Do not switch branches, do not
merge, do not push, do not touch other worktrees or the main checkout.
End your report with exactly this block (one item per line, "none" when empty):
Changed: <files>
Checked: <command> → <result>
Not checked: <what, and why>
Problems: **[wave <N> / task <ID> / feature <F>] <essence>** — where: <file:line>; expected / got; proposal: <…>
```

- Tasks needing task mode: record the direct-task head `H` or the task branch, finish and check other runnable tasks, then commit the waiting record and give commands as in `task-mode.md`; only tasks whose `After` is satisfied may run, and after resume continue with the next ready group, waiting for a task-mode dependency before its dependants.
- Wait for all tasks of the group without summarising or predicting results before they arrive, then check them in step 5 and merge and check in step 6 before starting dependent tasks.

### 5. Check each task

- Task branch: `git log feat/<plan>/<feature>..<task branch>` shows the work is committed. Uncommitted changes left in a task worktree: use the fix loop and ask it to commit.
- Task branch: `git diff --stat feat/<plan>/<feature>...<task branch>` shows only its files from the wave
  file's task table and nothing under `plans/`. Out-of-scope edits go to the problem log; if such an edit
  conflicts with another task, ask the user.
- Direct task: `git -C <feature worktree> status --porcelain` is empty (otherwise use the fix loop and ask it to commit); `git log H..HEAD` is not empty; `git diff --stat H HEAD` shows only the task's files from the wave file and nothing under `plans/`.
- Run the direct task's check command. A failure: use the fix loop.
- Out-of-scope edits or unusable direct work: record it in `problems.md` and ask the user. Never
  `git reset --hard` the feature branch without the user's explicit OK; the default undo is
  `git revert --no-edit H..HEAD`.
- Read the report's final block, ignoring `none` values. Every `Not checked:` line not covered by a later task, and
  every `Problems:` line, becomes one entry of `problems.md` (add the ID, `status: open`). A report without the
  block: ask the same subagent for it once (fix loop); still missing → one entry `report block missing`.

### 6. Merge task branches and check features

In each feature worktree, merge only task branches, in task-table order. Direct tasks have nothing to merge.

```bash
git merge --no-ff <task branch> -m "Merge <plan> <feature-id> / <task-id>"
```

- Conflicts: resolve them yourself when the resolution is mechanical (both sides added independent lines, imports, list entries). When it needs understanding of either task's logic, use the fix loop for the later task with the conflict description (it merges the feature branch into its branch and resolves), then merge again. A conflict that changes a plan solution → stop `design-conflict` and ask the user.
- Run the check command from the prompts (build + tests) in every feature worktree touched. Known failures
  from the README do not count.
- A new failure: find by files whose task it is and use the fix loop, passing the error text.
- A failure that appears only after merging (each task branch is green alone) is an integration problem: fix it yourself on the feature branch if it is small and mechanical; otherwise use the fix loop for the task whose files are involved; record it in the log either way.
- After a task branch is merged and green: `git worktree remove` its worktree and `git branch -d` its branch.
  Keep the worktree and branch of a ⚠️ or ❌ task.

### 7. Prepare ready features for review

Determine each feature's current outcome: all its tasks in all waves must be ✅ or ➖ and its feature check must
be green. Otherwise it remains 🔄 in progress, or ⚠️ blocked if a task is ⚠️ or ❌. For each feature whose tasks
are now all ✅ or ➖:

1. In its feature worktree (if it is gone: `git worktree add <feature worktree path> feat/<plan>/<feature>`, path
   from `layout.md`, "Names"): `git merge <main>` if `<main>` moved, resolve conflicts as in step 6, run the
   **full** check command. With `<main>` merged in, the review diff shows only this feature.
2. Green → the feature becomes `✅ ready` with `Waiting for: review`. Red → it becomes ⚠️ blocked with a new
   problem entry.

Merge nothing into `<main>` in this step: a ready feature waits for the user's approval (step 10).

### 8. Record and commit on the tracking branch

After a task-mode wait, reach this step on resume once the waiting tasks are checked and merged.

- README "Tasks": ✅, or ⚠️ with its entry IDs (open problem), or ❌ (not done).
- README "Waves": ✅ — all tasks ✅ and checks green; ⚠️ — done but with open problems (name them);
  ❌ — a check red or a task not done (the wave must be re-run or re-planned).
- README "Features":
  - 🔄 in progress — some of its tasks are not ✅/➖ yet (later waves, or ⚠️/❌ now);
  - ✅ ready — all its tasks in all waves are ✅ or ➖ and the feature check is green (step 7); it waits for the
    user's review;
  - ✅ merged — merged by `wave-run/merge.md`, or merged by the user and recorded in step 1; write the short
    merge hash into "Merged";
  - ⚠️ blocked — one of its tasks is ⚠️ or ❌, or the user rejected it in review: it is not merged until the
    problem is fixed (re-plan adds fix tasks to the same feature) or the user explicitly says to merge it as is.
- Update `Waiting for` of every feature with a task in this wave: `wave <N>` (its next tasks), `I<n>` (an open
  entry), `review` (ready, waits for the user's review and approval), or `user: <question>`. Empty once merged.
- New problems: append entries to `problems.md` with the next IDs (update `Next ID`), in the format of
  `layout.md`; create the file with the first entry.
- Closed problems: every open entry this wave fixed or verified (its `→ task Y` tasks are now ✅, or a check of
  this wave verified it) gets its closing status and moves to "Closed problems" of the wave file where it was
  found. Then update every earlier task, wave and feature it concerned, as `layout.md` says
  (`⚠️` → `✅ (fixed by Y, wave N)`).
- Wave file "Execution": date, feature heads before and after, merge commits, check results, conflicts and how
  they were resolved, anything a later reader needs. Keep it factual and short. A stopped wave ends with its
  `Stop <code>: … — next: …` line as specified in "Stops".
- Run the **status check** (script, `layout.md`, "Statuses") over the README; fix what it finds. Archive if eligible (`layout.md`, "Archive").
- Make **one** commit: `Plan <plan>: wave <N> done`, adding `; <feature IDs> ready` when any became ready,
  `; <feature IDs> merged` when step 1 recorded a merge by the user, and `; archived` when archived. A stopped wave
  uses `Plan <plan>: wave <N> stopped`.
- Only if step 1 recorded a merge, make **one**
  `git -C <main checkout> merge --no-ff plan/<plan> -m "Plan <plan>: status after wave <N>"`.
  The tracking branch only changes `plans/`, so this merge has no code conflicts.
- Remove the worktrees of features recorded as merged and `git branch -d feat/<plan>/<feature>`. Keep the worktree
  and branch of a ready feature: the user reviews and checks it there.
- When the plan is archived: remove the tracking worktree and `git branch -d plan/<plan>`. A plan whose features are
  all merged but which has open entries keeps its tracking branch and worktree (it waits for a re-plan).

### 9. Report to the user

- First line if the wave stopped: `Stop <code>: <one line> — next: <command or action>`.
- Task table: status, what was done in one line, feature.
- Feature table: status, branch, which tasks are still missing, its `Waiting for`.
- Task merges: conflicts and how they were resolved.
- Check result (what passed, what failed).
- New problem-log entries — the essence of each; entries closed by this wave and the statuses that changed.
- What to check by hand (UI and anything tests do not cover) for features that are not ready yet, in their
  feature worktree.
- **Ready for review**: one block per `✅ ready` feature, both those this wave made ready and those still waiting
  from earlier runs. A feature branch holds only its own feature (`layout.md`, "Feature review"), so every block
  stands alone. Each block gives:
  - the feature ID, title and "Done when";
  - its branch `feat/<plan>/<feature>` and its worktree path;
  - the number of its commits and the `git diff --stat <main>...feat/<plan>/<feature>` summary;
  - the review commands of `layout.md`, "Feature review", filled in;
  - what to check by hand in its worktree;
  - for `main-dirty`, the reason.
- When two ready features change the same paths (`git diff --name-only <main>...<branch>` of each), name the
  paths and say that the second merge brings the first one in from `<main>` and may need conflict resolution.
- End the report with the questions of step 10.

**The next command**, always for a fresh session, in both forms (`layout.md`, "Commands"):

| Situation | Next command |
|---|---|
| a feature is `✅ ready` | review it, then `/wave-run <plan folder> merge <F-ID>`<br>`$wave-run <plan folder> merge <F-ID>` (for `main-dirty`, clear the reason first) |
| a later wave is ⬜ | `/wave-run <plan folder> <N+1>`<br>`$wave-run <plan folder> <N+1>`; it waits for a review only if its `Depends on:` names the feature |
| waiting for task mode | one per task, in launch-group order: `/wave-run <plan folder> <N> task <ID>`<br>`$wave-run <plan folder> <N> task <ID>` — fresh session, `<tier>` model, needs `<tool>` |
| open problems | `/wave-plan <plan folder>`<br>`$wave-plan <plan folder>`, listing them |
| last wave done, plan from an index | the index parts plannable now: `/wave-plan <index> part <K>`<br>`$wave-plan <index> part <K>` |

### 10. Ask about each ready feature

Ask once per `✅ ready` feature, at the end of the report:
`Merge F<k> "<title>" (feat/<plan>/<feature>) into <main>? Answer: merge F<k> · later · problems F<k>: <what is wrong>`.
Then wait for the answer. Read `wave-run/merge.md` before acting on it.

| Answer | What happens |
|---|---|
| approves the merge of named features (`merge F1`, `merge F1 F3`; "yes" when one feature was offered) | "Merge one feature" of `wave-run/merge.md` for each, in "Features" order, then its "Record" |
| `problems F<k>: …` | "Rejection" of `wave-run/merge.md`, then its "Record" |
| `later`, no answer, or an answer about something else | nothing changes: the feature keeps `✅ ready`, `Waiting for: review` |
| "yes" or "ok" when several features were offered | ask which features |

Never treat silence or a general approval of the wave as approval of a merge.

The coordinator is always medium.
