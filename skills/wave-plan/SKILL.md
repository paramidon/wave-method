---
name: wave-plan
description: Turn the user's list of problems/features into an implementation plan for parallel subagents — code analysis, architecture, grouping into features, slicing into low/medium/high complexity tasks, waves with disjoint files, and ready-to-paste task prompts, all in one plan folder (README, solution files, one file per wave, problem log) on its own tracking branch. Second stage of the wave-triage → wave-plan → wave-run pipeline. Use when the user runs "/wave-plan <index> part <K>" for a part of a triage index, brings a short list of tasks and wants them split into waves for subagents ("нарежь на волны", "/wave-plan"), or wants open problems from a plan's problem log re-planned. Recommended model: high complexity (Opus-class), because this skill does the design work so the executors don't have to.
---

# wave-plan — design and slice tasks into waves

Language: `wave-plan/layout.md`, "Language".

Skill paths such as `wave-plan/layout.md` are relative to the wave skills folder, the parent of this skill's
folder (`wave-plan/layout.md`, "Skill paths").

## Layout
Read `wave-plan/layout.md` first: plan folder layout, which file holds what and when it is
created, who reads what, model tiers, branch names, status rules, the problem-log format and the Markdown
rules. It is the single source of truth; this skill does not repeat it.

## Input
Pipeline: `wave-triage` → `wave-plan` (one run per part, fresh session each) → `wave-run`.
- **A part of an index** — both forms (`layout.md`, "Commands"):
  `/wave-plan plans/<date>-<topic>/index.md part <K>` · `$wave-plan plans/<date>-<topic>/index.md part <K>`.
  Read `index.md` and, when they exist, the records `triage/P<n>.md` of part K's problems only. The index and
  those records already hold the user's words, clarifications, code locations, difficulty and dependencies:
  start from them, verify them, do not re-ask answered questions. The plan slug is the one in the index's
  "Parts" table; the plan folder is `plans/<date>-<topic>/plan-<K>/`. If the part is marked "plan after part J
  is merged" and part J's features are not all `✅ merged` on the main branch, stop and tell the user.
- **A raw list** from the user — allowed without `wave-triage` when it fits one part. First read
  `wave-triage/difficulty.md` (difficulty scale and part budget; the single source of truth, do
  not guess the numbers). Judge each problem's difficulty from a quick look at the code (find where it lives,
  no design). If the list exceeds the "Part budget", **stop** before the deep analysis: tell the user the
  list is too big for one plan and give both forms of the command:
  `/wave-triage <the list>` · `$wave-triage <the list>`. Otherwise go on with step 1.
  The plan folder is `plans/<YYYY-MM-DD>-<slug>/`.
- **An existing plan folder** with open entries in its `problems.md` — re-planning (see below).

## Output
One plan folder with the files of `layout.md`, each created only when it has content. The `wave-run` skill
executes waves from it.
No project code is changed at this stage: only reading code and writing the plan folder.
The plan slug (`<slug>`, 2–4 kebab-case words) must differ from every other plan slug in `plans/`, including
`plans/archive/`: branch names are built from it.

**Nothing is committed directly on the main branch.** The plan is written in a worktree on its tracking
branch `plan/<slug>`, which lives as long as the plan; it reaches the main branch only by merges (step 9).
Do not edit files in the main checkout.

Core idea: executors are medium-complexity models (Sonnet 5.5, GPT-6.1 SOL, Gemini 4 Argon). They implement
a given solution well and design poorly. So every design decision is made here and written into the plan.
If a task prompt says "figure out how", the design is not finished.

Delivery unit: a **feature** reaches the main branch only as a whole, when all its tasks are done, even if its
tasks are spread over several waves, and only after the user reviewed and approved it (`layout.md`, "Feature
review"). A wave is only a scheduling unit.

**Re-planning.** If the input is a plan folder with open entries in `problems.md`, do not create a new plan.
Before writing, check the lock: if a wave of the plan is 🔄 on the tracking branch (`layout.md`, "Running
waves"), report `Stop wave-running: wave <N> is running — next: wait, or the user releases the lock` and stop
without writing. Read only what `layout.md` allows for a re-plan. In its tracking worktree add new solutions
(next P numbers: new files, new sections of `lite.md`), new tasks (IDs continue) and new wave files after the
last one; add them to the README tables and add one line to the README header (`re-planned <date> at <hash>:
<what>`); put the longer re-plan notes into `history.md` (create it at the first re-plan). Mark the entries `→
task Y (wave M)`; apply the status rules of `layout.md` (superseded tasks and dropped waves become ➖ now). Fix
tasks for a blocked feature (also one the user rejected in review) belong to that same feature. Fixes for a
feature that is already merged go into a new feature. Run the status check (script, `layout.md`, "Statuses") before committing.

## Steps

### 1. Read the list
- Number the user's problems (P1, P2, …; a re-plan continues the numbers) and restate each in one line, close
  to the user's words (in English).
- If a problem can be read two ways that lead to different work, ask all such questions once, as one list,
  before designing. Decide small things yourself and record them as assumptions.

### 2. Analyse the code (per problem)
- Find where the behaviour lives and the cause of the problem. Cite `file:line`.
- Find what already exists and can be reused (functions, classes, utilities, test examples).
  Verify every function you cite in a prompt: it exists and its signature is what you write.
- Run the tests once and record which ones already fail (known failures).

### 3. Architecture (the most important step)
For each `medium` or `high` problem write its solution file `solutions/P<n>-<slug>.md`:
- **Approach** — what we do and why (and why not the obvious alternative, if there is one).
- **Model/API changes** — new and changed types, fields, method signatures verbatim, in the project's language.
  Compatibility: how existing callers keep working (overload, default value).
- **Algorithm** — formulas, steps, iterations, convergence criterion, degenerate cases.
  Not "tune it iteratively" but "scan X from a to b with step c, take the minimum of Y".
- **Invariants and limits** — what must stay true; what to do when there is no solution (which error to return).
- **Acceptance tests** — concrete scenarios with numbers and tolerances.

If without this a task would need a high-complexity model, make the decision here so the task becomes medium.

**Lite mode** for `low` problems: no Approach/Algorithm sections — a one- or two-line solution with the exact
edit and one acceptance check is enough. Every `low` problem is a section `## P<n>. <short>` of
`solutions/lite.md`, never its own file; every `medium`/`high` problem has its own file, never a section of
`lite.md`. The choice follows the difficulty only. Spend the depth on the hard problems.

### 4. Features
- Group the problems into features F1, F2, …: a feature is the smallest set of changes that makes sense in the
  main branch on its own — working, tested, nothing half-wired. Usually one P = one feature; several P go
  into one feature when one is useless or broken without the other.
- Each feature has an ID unique in the plan, a slug of 2–4 kebab-case words, a title and its acceptance
  criterion (which acceptance tests prove the whole feature works).
- **No hidden dependencies between features.** If a task of F2 needs code of F1, then either all tasks of F1
  are in waves before that task and the wave file of that task names `F1 merged` in its `Depends on:` line, or
  F1 and F2 are one feature. F1 reaches the main branch only after the user's review, so `wave-run` stops that
  wave (`feature-unmerged`) until F1 is merged, then merges the main branch into F2's branch. Never let F2's
  branch take F1's code any other way: each feature branch holds only its own feature.

### 5. Slice into tasks
Task = one prompt for one subagent; every task belongs to exactly one feature.
- **Complexity** `low` / `medium` / `high`, with its meaning and model tier from `layout.md` ("Model tiers").
  Use high only with a one-sentence justification in the plan; try to slice it first. A high task is never
  run on a medium model: `wave-run` stops the wave if no high-tier model is available (for example, on a
  vendor without one). So every high task you leave makes the plan unrunnable there — say so to the user.
- How to cut a hard task into medium steps (all steps stay in the same feature, so nothing half-done reaches
  the main branch):
  1) pure function/algorithm with unit tests, not wired in;
  2) data model and plumbing (types, serialisation, call sites) — the new value is ignored for now;
  3) wiring into the main logic + integration tests;
  4) special cases as a separate step.
- **Contract first**: if B depends on an API from A, put the signatures and stubs into A (or a separate low task),
  so the dependent tasks can run in parallel in the next wave.
- Merge small tasks into one prompt when they are in the same area or the same files.
- Every task has an exact list of files it may change, never anything under `plans/`.
- Every task has an ID unique within the whole plan (letters continue across waves and across re-plans
  appended later: A, B, …, Z, AA, …; never reuse an ID) and a slug of 2–4 kebab-case words naming its
  essence (`signed-speed-readouts`). Branches are named after both.

### 6. Waves
- Each task runs in its feature worktree, or in a task worktree when another task of its feature runs at the
  same time (`wave-run` decides); tasks in one wave still share no files and do not depend on each other
  except through `After`.
- A wave may mix tasks of different features. Tasks of one feature in later waves start from the feature
  branch, so they see the earlier tasks of that feature.
- 2–5 tasks per wave; tasks of one wave share no files (merges and parallel builds stay conflict-free).
- A wave with one task is allowed only for a `high` task that cannot be paired or sliced.
- A low/medium task left alone is attached to another wave or merged into an adjacent prompt. Never a solo wave.
- A closing task (final integration, cleanup, docs, checks) is a task whose `After` lists every other task of
  its wave. Its prompt starts with: "This task runs after tasks <IDs> of this wave; their changes are already
  in your working folder."
- The coordinator is always `medium`. A task that needs a tool subagents may lack (for example desktop control
  for GUI checks) gets it in the `Needs` column; `wave-run` handles it (see "Environment capabilities").
- Order: hard first, easy at the tail — `high` work in the earliest waves (its risk surfaces early),
  `low` tasks last, where they also fill waves. Dependencies win over this: contracts and pure functions
  before wiring, wiring before UI. Prefer orders that finish a feature early, so it is ready for review
  without waiting for the whole plan. Put a wave that needs `F<k> merged` as late as the order allows: the
  user reviews F<k> in between.
- Each wave gets its file `waves/w<NN>.md` with its task table (including `After`, `Needs` and files), the
  dependencies on earlier waves, why its files are disjoint, and the full prompts of its tasks.

### 7. Task prompts
A task with `After` starts with: "This task runs after tasks <IDs> of this wave; their changes are already
in your working folder." A task with `Needs` says what the tool is for.
Each prompt is self-contained (the subagent starts with an empty context) and contains:
- Project, stack. Do not write a folder path, a branch name or the plan folder path: the coordinator prepends a
  header with the task's worktree, branch, the plan folder path and the commit rule. "Other agents work in
  parallel on other branches: change only <files>."
- "Write code, comments and docs in English; write the report in the language the header names."
- The goal in 1–2 sentences, the feature it belongs to, and the solution file and section to read, relative to
  the plan folder (`solutions/P3-atmospheric-flight.md`, "Algorithm D"). Name only the files the task needs:
  the subagent reads nothing else in the plan folder.
- Key solution details right in the prompt: signatures, formulas, which functions to reuse (`file:line`).
- Acceptance tests with numbers, the check command, known failures.
- "If the plan's solution does not work (contradicts the code, does not converge), do not invent another one:
  stop and describe the problem in the report: what was expected, what you saw, where."
- The report format comes from the `wave-run` header; do not repeat it in the prompt.
Write prompts without tying them to a specific vendor's model or tools.

### 8. Self-check
- Every P is covered by a feature and a solution (`low` → a section of `lite.md`, others → own file); every
  feature by tasks and an acceptance criterion; every task has an acceptance test.
- No empty files: `problems.md` and `history.md` exist only when they have content.
- No file overlaps inside a wave; dependencies cross waves or use `After`; no hidden cross-feature dependency:
  every one is `F<k> merged` in the `Depends on:` line of the wave that needs it.
- No single-task waves except an unpairable `high` task; no solo `low`/`medium` task anywhere.
- Every high task is justified.
- `After` names only tasks of the same wave, without cycles; every `Needs` is explained in its prompt.
- Feature IDs and task IDs are unique in the plan; slugs are distinct; the plan slug is unique in `plans/`.
- Every prompt names solution files that exist, and sections that exist in them.
- README stays within its size goal; long text moved to solution files or `history.md`.
- Re-plan: the status check (script, `layout.md`, "Statuses") passes.

### 9. Write, commit on the tracking branch, merge
1. Tracking worktree from the main branch (`<main>` = `master` or `main`):
   ```bash
   git worktree add -b plan/<slug> ../<repo-folder>.worktrees/<slug>-plan <main>
   ```
   If the branch or the folder already exists for a new plan, ask the user. For a re-plan, use the existing
   tracking worktree (create it from the existing `plan/<slug>` branch if the folder is gone; if the branch is
   gone too, create it from `<main>` with `-b plan/<slug>`; merge `<main>` into it first).
2. Write the plan folder from `templates.md` and commit only that folder: `Plan <slug>: <short>`
   (or `Plan <slug>: re-plan`).
3. Merge into the main branch so the plan is visible there: the main checkout must be ready for the merge of
   `plan/<slug>` (`layout.md`, "Main readiness"); then
   `git -C <main checkout> merge --no-ff plan/<slug> -m "Plan <slug>: <short>"`.
   If the main checkout is not ready, do not touch it: give the user the merge command.
4. **Keep** the tracking branch and its worktree: `wave-run` records statuses there and deletes them when
   every feature is merged. Never push.

Answer the user briefly: feature table, wave table, how many tasks of each complexity (and which
waves need a high-tier model for their tasks), after which wave each feature is ready for review (and which
waves wait for a merge, `Depends on: F<k> merged`), assumptions, remaining questions, and **the next command**,
in both forms (`layout.md`, "Commands"):
`/wave-run <plan folder> 1` · `$wave-run <plan folder> 1`, in a fresh session. The coordinator is always medium.
Say which tasks may need task mode (`Needs`, or a tier the environment may lack). If the plan came from an
index, also list the index's other parts and their commands, saying which can be planned now and which
wait for a merge.

Templates: `wave-plan/templates.md` — read it when writing the plan folder (step 9).
