# P1. Flow field, manual-review override and the decision table in layout.md

User problem: a per-plan flow (`manual` default / `autonomous`), switchable between waves, overridable per feature,
with one decision table in `wave-plan/layout.md` · feature F1

## Cause

No flow concept exists. Every point where `wave-run` asks or waits is hard-coded in `skills/wave-run/SKILL.md`
(step 1 leftover branches l.145-147, open entries l.148-149, `feature-unmerged` l.153-154; step 3 red before the wave
l.173-177; step 5 out-of-scope edits l.227-229 and l.238-240; step 6 design conflict l.254; step 10 l.332-344) and in
`skills/wave-run/merge.md` (step 1 "ask again" l.29-30, step 2 main readiness l.31-35). `skills/wave-plan/layout.md`
has no place for a mode; "Feature review" (l.252-255) says "No skill merges a feature on its own".

## Approach

- The flow is a README header field, read by `wave-run` only. No field = manual = today's behaviour, unchanged: every
  new rule in the skills is conditioned on "autonomous flow" and leaves the manual text path as it is.
- The override is a list in the same header line (`manual review: F2, F5`), not a new Features column: old READMEs,
  `status_check.py` and `wave-status` keep their table formats.
- The flow is switched by a new `wave-run` form, `flow <manual|autonomous> [review <F-IDs>]`, which commits the line on
  the tracking branch. Why a form and not "edit the README": the tracking branch is written only by skills, the form
  takes the lock (`wave-running`) and checks the integration target before it records the switch.
- A flow never changes inside a running wave: the form is refused while a wave is 🔄, and `wave-run` reads the flow
  once in step 1 and keeps it for the run (also across a task-mode resume, which happens while the wave is 🔄).
- Switching autonomous → manual is refused while the integration branch has commits the main branch does not have
  (stop `target-unmerged`). Why: after the switch `<main>` is the main branch again, and a feature branch that took
  in the integration branch would then differ from the main branch by other features' code, breaking "a feature
  branch holds only its own feature".
- Scope of part 1: the table covers the points of `wave-run`. The questions of `wave-triage`/`wave-plan` and "plan
  after part K is merged" are added to the same table by part 2 of the index (P4, P10); until then those skills
  ignore the flow.

## Exact text for `skills/wave-plan/layout.md`

### New section `## Flow`, placed after "Feature review" and before "Archive"

`<…>` in the text below are the layout's own placeholders and stay as written. The inner fence is three backticks.

````markdown
## Flow

A plan runs in one of two flows. The flow decides only who approves a `👀 review` feature and where an approved
feature is merged. Merge mechanics (`wave-run/merge.md`), the tier gate, never pushing, never committing directly on
`<main branch>` and never merging a feature partially are the same in both.

| Flow | Who approves a `👀 review` feature | Merged into | Questions to the user |
|---|---|---|---|
| `manual` (default) | the user ("Feature review") | `<main branch>` | at the points of the decision table |
| `autonomous` | `wave-run` when "Auto-approval" holds; the user for a feature under manual review | the integration branch ("Integration target") | none |

The flow is a header field of the plan README:

```
- Flow: autonomous · target: integration/<name> · manual review: F2, F5
```

- A README without a `Flow:` line, or with `- Flow: manual`, is in manual flow and behaves exactly as if this section
  did not exist.
- `target:` names the integration branch; without it the target is `integration/<plan>`.
- `manual review: <F-IDs>` is optional: these features are never auto-approved. Each stays `👀 review` with
  `Waiting for: review` until the user approves it ("Feature review"), and every wave whose `Depends on:` names it
  stops `feature-unmerged` until then.
- `wave-plan` writes the line only when the user asks for autonomous flow while planning. Afterwards it is changed only
  by the flow form `/wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` ·
  `$wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` (`wave-run/autonomous.md`, "Flow form"), and
  only while no wave of the plan is 🔄: a flow never changes inside a running wave.
- `wave-run` reads the flow from the README on the tracking branch in its step 1 and keeps it for the whole run,
  including the resume of a task-mode wait. `wave-plan` and `wave-triage` do not act on it.
- Switching to manual is refused while the integration branch has commits `<main branch>` does not have (stop
  `target-unmerged`): the user merges it first, so every feature branch again differs from `<main branch>` only by
  its own feature.

### Integration target

<the subsection of `solutions/P2-integration-target.md`, "Exact text for layout.md", "Integration target">

### Auto-approval

In autonomous flow `wave-run` approves a `👀 review` feature itself only when all of these hold. It checks them right
before the merge (`wave-run/autonomous.md`, "Auto-approval"):

1. every task of the feature, in every wave, is ✅ or ➖;
2. its full check is green after `<main>` was merged into its branch, and that merge changed none of the feature's own
   lines (`wave-run/merge.md`, "Merge one feature", step 1);
3. no open entry of `problems.md` concerns the feature or one of its tasks;
4. the tier gate is clean: every commit of the feature branch whose subject names one of its tasks
   (`<plan> <feature-id> / <task-id>: …`) has a `Wave-Model` trailer naming a model of that task's tier or higher
   ("Tier gate");
5. the feature is not listed under `manual review:`.

| Condition that fails | The feature |
|---|---|
| 5 | stays `👀 review`, `Waiting for: review`, until the user approves it |
| 1, 2, 3 or 4 | becomes ⚠️ blocked, `Waiting for: I<n>`, naming its open entry (a new entry for 2 and 4) |
| `<main checkout>` is not ready ("Main readiness") | stays `👀 review`, `Waiting for: main-dirty` |

The run goes on with everything that does not depend on a feature left unmerged.

### Decision table

Every point where `wave-run` asks the user or waits for them. Manual flow is the behaviour of `wave-run/SKILL.md` and
`wave-run/merge.md`; autonomous flow follows `wave-run/autonomous.md`. To **skip** a task (`wave-run/autonomous.md`,
"Skipped tasks") is to not launch it and mark it ⚠️ with the entry that blocks it.

| Point | Where | Manual flow | Autonomous flow |
|---|---|---|---|
| a feature is `👀 review` | step 10; merge form without a wave | ask per feature; merge only what the user approves | "Auto-approval"; no question |
| open entries concern this wave | step 1 | show them and ask whether to proceed; no → stop `open-problems` | proceed; skip the tasks of a feature that has an entry with `status: open` |
| task branches of this wave exist | step 1 | ask: continue from them, delete them, or stop `leftover-branches` | never reuse or delete them: stop `leftover-branches` |
| `Depends on: F<k> merged` and F<k> is not `✅ merged` | step 1 | stop `feature-unmerged` | the same stop; "Auto-approval" has usually merged F<k> before |
| a feature check is red before the wave | step 3 | stop `red-before-wave` | new entry; the feature is ⚠️ blocked; skip its tasks; the wave goes on |
| an out-of-scope edit, or unusable direct work | step 5 | entry; ask the user | entry; do not merge the task (a direct task is reverted); the task is ⚠️ and the feature ⚠️ blocked; skip its dependants |
| a merge conflict would change a plan solution | step 6 | stop `design-conflict` | abort the merge; entry; the task is ⚠️ and the feature ⚠️ blocked; skip its dependants; the wave goes on |
| a task stays red after 2 attempts | fix loop | the task is ⚠️; stop `red-after-merge` if no other task can continue | the same |
| no model of a task's tier; a session or work below its tier | steps 1 and 5, task mode | stop `tier-missing` or `tier-mismatch`; the work runs again on its tier | the same; never waived |
| a task needs task mode | step 4 | `Waiting: task mode` with one command per task | the same; whoever drives the run starts those sessions |
| merging `<main>` into a ready feature changed its own lines | `merge.md` step 1 | show the resolution and ask again | not merged: entry, the feature ⚠️ blocked |
| `<main checkout>` is not ready for a merge | `merge.md` step 2 | ask the user to clear it; `main-dirty` if left for later | `main-dirty`; no question |
| every feature is merged | step 8; `merge.md` "Record" | archive the plan ("Archive") | no archive: the tracking branch stays until the user merged the integration branch |
````

### Other edits of `skills/wave-plan/layout.md`

1. "Who reads what", row `wave-run` coordinator (l.10): after "`wave-run/task-mode.md` and `wave-run/merge.md` only
   when its step 1 says so" add "; `wave-run/autonomous.md` only when the plan's flow is autonomous or the arguments
   are `flow …` ("Flow")".
2. "Names" (l.137): replace the `<main>` bullet with the three bullets of `solutions/P2-integration-target.md`,
   "Exact text for layout.md", "Names", and add the integration row to the branch table there.
3. "Statuses" (l.165): after "it is merged only after the user's review ("Feature review")" add "or, in autonomous
   flow, after auto-approval ("Flow")"; append the sentence "In autonomous flow `✅ merged` means merged into the
   integration branch."
4. "Main readiness" (l.205-217): as `solutions/P2-integration-target.md`, "Exact text for layout.md", "Main readiness".
5. "Feature review", "Approval" (l.252-255): replace "No skill merges a feature on its own." with "In autonomous flow
   the auto-approval of `wave-run` ("Flow", "Auto-approval") is the approval too; it merges into the integration
   branch only. No skill merges a feature into `<main branch>` on its own."
6. "Archive" (l.261-267): add the bullet "In autonomous flow `wave-run` does not archive and keeps the tracking
   branch: the plan is finished for the user only once they merged the integration branch into `<main branch>`;
   `wave-status` then suggests the archive."

## Edits of the other skill files (pointers)

### `skills/wave-plan/templates.md`

README template header (l.8-11): after the `- Re-plans:` line add this line verbatim:

```
- Flow: (omit for manual flow; `autonomous · target: integration/<slug> · manual review: <F-IDs>` only when the user asks for it: `layout.md`, "Flow")
```

### `skills/wave-plan/SKILL.md`

In "Output", after the paragraph "**Nothing is committed directly on the main branch.** …" (l.42-45) add this
paragraph verbatim:

```
The flow (`layout.md`, "Flow") is a README header line: write `- Flow: autonomous · target: integration/<slug>` only
when the user asks for autonomous flow; otherwise write none (manual). A re-plan keeps the line as it is. A plan is
always created from, and merged into, the main branch, whatever its flow.
```

Nothing else changes: `wave-plan` keeps `<main>` = the main branch (`layout.md`, "Names").

### `skills/wave-status/SKILL.md`

1. "What to read", first bullet (l.28-31): append "Also its `Flow:` header line (`layout.md`, "Flow"). For a plan in
   autonomous flow, `<main>` below is its integration branch (`layout.md`, "Names"); also read
   `git rev-list --count <main branch>..integration/<name>` when that branch exists."
2. "Report", Header bullet (l.53): "Header: plan folder, slug, tracking branch present or absent." → "Header: plan
   folder, slug, tracking branch present or absent, and the flow: `manual`, or `autonomous` with its target and
   manual-review list."
3. "Report": after the `Ready for review:` bullet add "- `Integration:` autonomous flow only: `integration/<name>` —
   `<N>` commits not in `<main branch>`; review `git diff <main branch>...integration/<name>`, then merge it yourself
   in the main checkout (`git merge --no-ff integration/<name>`); or `in <main branch>` when N is 0, or `not created
   yet`."
4. "Leftovers" bullet (l.78-79): append "In autonomous flow the kept branches of auto-merged features are leftovers
   only once the integration branch is in `<main branch>`."
5. "Next-command rules": insert before rule 6 a new rule "6. Autonomous flow, no wave ⬜ or 🔄, and the integration
   branch has commits `<main branch>` lacks: review `git diff <main branch>...integration/<name>`, then merge it
   yourself: `git merge --no-ff integration/<name>`." and renumber the old rule 6 to 7, appending to it "In
   autonomous flow only once the integration branch is in `<main branch>`."

## Limits

- Every changed sentence that is not inside the new "Flow" section keeps its manual-flow meaning word for word, with
  the autonomous case added as a clause or a separate sentence.
- No new status and no new `Waiting for` value; no new README table or column.
- The decision table is the only place that says what autonomous flow does at a point; `wave-run/autonomous.md` says
  how and does not repeat the table.

## Acceptance tests

- `git grep -n -e "^## Flow" -e "^### Integration target" -e "^### Auto-approval" -e "^### Decision table" -- skills/wave-plan/layout.md`
  → 4 lines, in this order, between "## Feature review" and "## Archive".
- The decision table has 13 rows of 4 cells; `python skills/wave-plan/scripts/status_check.py examples/01-greenfield-todo-cli`
  still exits 0 (README format unchanged).
- Walkthrough "old plan": a README without `Flow:` → manual flow; every sentence changed outside "Flow" still says
  what it said for manual flow.
- Walkthrough "risky feature": `Flow: autonomous · manual review: F2`, F2 ready → F2 stays `👀 review`, `Waiting for:
  review`; a wave with `Depends on: F2 merged` stops `feature-unmerged`; other features are auto-approved.
- Walkthrough "switch": wave 3 is 🔄 → the flow form stops `wave-running`; integration branch 2 commits ahead of the
  main branch → `flow manual` stops `target-unmerged`.
