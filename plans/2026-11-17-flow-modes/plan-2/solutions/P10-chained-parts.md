# P10. Chained parts in autonomous flow: one integration branch per index

User problem: in autonomous flow "plan after part J is merged" checks the integration target, not the main branch;
part K's tracking branch is created from and merged into the integration target; a part J feature left `👀 review`
or ⚠️ stops the planning of part K with a clear line · feature F1

## Cause

- `skills/wave-plan/SKILL.md:26-27`: "part J's features are not all `✅ merged` on the main branch" — in autonomous
  flow part J's features are merged into `integration/<name>` (`layout.md`, "Integration target"), so a part
  planned at night always stops, and its `file:line` references would point at code without part J.
- `skills/wave-plan/SKILL.md:213-225`: the tracking branch is created from and merged into the main branch;
  `layout.md:137-140` ("Names") says `wave-plan` always uses `<main branch>`.
- Part 1 gives every plan its own `integration/<plan>` (`layout.md`, "Flow", `target:` bullet), so part K could not
  see part J's code even if the check passed.

## Approach

- **One integration branch per index**: every plan of an index part in autonomous flow writes
  `target: integration/<topic>`. Part K's feature branches then start from code that holds part J, and the user
  reviews and merges one branch for the whole night. A raw-list plan keeps `integration/<slug>`.
- **`wave-plan` resolves `<main>` by its flow of planning** (P4): in autonomous flow it prepares the integration
  branch exactly as `wave-run` does (`wave-run/autonomous.md`, "Integration target", steps 1 and 2: same checks, same
  stops), reads code and runs the tests in the integration worktree, creates the tracking branch from the
  integration branch and merges it into the integration worktree. Why not keep merging the plan into the main
  branch: the tracking branch is created from the integration branch, so merging it into the main branch would carry
  every feature of the night along. The plan folder therefore lives only on the integration branch (and its tracking
  branch) until the user merges the integration branch; `wave-run` and `wave-status` learn to find it there.
- **The chain check** reads part J's README from its tracking branch (autonomous flow keeps it) and accepts a merge
  that is in the integration branch or in the main branch (a part J run in manual flow and merged by the user counts).
  It is read-only and runs before anything is created.
- **No parallel writers on a shared integration branch**: two plans of an index may otherwise run waves at the same
  time (waves of different plans may, `wave-run` step 1) and both merge into the one integration worktree. A wave of
  any plan with the same target holds the lock: `wave-run` and `wave-plan` stop `wave-running` while it is 🔄.

## Chained parts (text)

Appended to the new `layout.md` subsection "Planning in autonomous flow" (`solutions/P4-planning-assumptions.md`),
at its end. The inner fence is three backticks.

````markdown
#### Chained parts and the integration branch

In autonomous flow `wave-plan` uses `<main>` = the integration branch and `<main checkout>` = the integration worktree
("Names"). All plans of an index share `integration/<topic>`, so a later part is planned and run against the code of
the earlier parts before the user has merged them. In order, before step 1 of `wave-plan`:

1. Stop `wave-running` when a plan with the same target has a 🔄 wave ("Integration target", plans of a target).
2. The checks of `wave-run/autonomous.md`, "Integration target", step 1 (stop `target-unsafe`).
3. The part is marked "plan after part J is merged": part J is merged when every feature in part J's README (from its
   tracking branch `plan/<topic>-p<J>`, else from `<main>`) is `✅ merged` or ➖, and the integration branch or
   `<main branch>` contains each of their `Merged` hashes (`git merge-base --is-ancestor <hash> <branch>`). Otherwise
   stop before anything is written:

   ```
   Stop part-unmerged: part <J> — F<k> <status> (<Waiting for>), … — next: …
   ```

   `next:` names, per feature, what it waits for: a `👀 review` feature its review and its merge command, a ⚠️ or 🔄
   feature its `Waiting for`; part J without a plan folder or tracking branch: `part <J> is not planned`, with its
   `/wave-plan` command. Whoever drives an unattended run moves on and reports the waiting part with that line.
4. `wave-run/autonomous.md`, "Integration target", step 2 (create the branch and worktree, bring in `<main branch>`;
   stop `target-conflict`).

Then `wave-plan` reads the code and runs the tests in the integration worktree, creates the tracking branch from the
integration branch and merges it into the integration worktree, never into the main checkout. The plan folder is on
the integration branch only, until the user merges it into `<main branch>`.
````

## Edits of `skills/wave-plan/layout.md` for P10 (task A)

1. "Who reads what", row `wave-plan`, new plan: append "; the README of part J of the index (from its tracking branch)
   when the part is marked \"plan after part J is merged\"; in autonomous flow of planning also
   `wave-run/autonomous.md`, \"Integration target\"".
2. "Names", the `<main>` bullet: "Only `wave-run` and `wave-status` resolve it by the flow; `wave-plan` and
   `wave-triage` always use `<main branch>`." → "`wave-run` and `wave-status` resolve it by the flow, `wave-plan` by its
   flow of planning (\"Planning in autonomous flow\"); `wave-triage` always uses `<main branch>`."
3. "Flow", the `target:` bullet: "`target:` names the integration branch; without it the target is
   `integration/<plan>`." → append " A plan of an index part in autonomous flow names `integration/<topic>`: all
   parts of an index share one integration branch (\"Planning in autonomous flow\")."
4. "Integration target", first bullet: "`wave-run` creates the integration branch …" → "`wave-run`, and `wave-plan` in
   autonomous flow of planning, create the integration branch …" (rest unchanged, grammar adjusted: "merge
   `<main branch>` into it").
5. "Integration target", second bullet: "approved feature branches, the tracking branch and `<main branch>`" →
   "approved feature branches, the tracking branches of its plans and `<main branch>`".
6. "Integration target", new bullet after the second one:

   ```markdown
   - Plans of a target: the plans whose README, on their tracking branch, has a `Flow:` line naming
     `integration/<name>` — for each branch of `git branch --list "plan/*"`,
     `git grep -l -E "^- Flow: autonomous · target: integration/<name>( ·|$)" <branch> -- "plans/*README.md" ":!plans/archive"`.
     They write the same worktree, so their waves never run at the same time: while a wave of one of them is 🔄,
     `wave-run` and `wave-plan` of another stop `wave-running`.
   ```

## Edits of `skills/wave-plan/SKILL.md` for P10 (task B)

Line numbers are of `main` at fc815cd; find each place by its text. P4's edits to this file are in
`solutions/P4-planning-assumptions.md`.

1. "## Input", "A part of an index" bullet, after "…stop and tell the user." add: "In autonomous flow of planning run
   the four checks of `layout.md`, \"Chained parts and the integration branch\", before step 1 instead (stops
   `wave-running`, `target-unsafe`, `part-unmerged`, `target-conflict`)." A raw list in autonomous flow runs checks 1,
   2 and 4 of the same list: add to the "A raw list" bullet: "In autonomous flow of planning, before step 1: checks 1,
   2 and 4 of `layout.md`, \"Chained parts and the integration branch\"."
2. "## Output", the Flow paragraph (l.48-50) becomes:

   ```markdown
   The flow (`layout.md`, "Flow") is a README header line: in autonomous flow of planning write
   `- Flow: autonomous · target: integration/<name>` (`<name>`: the index topic for an index part, else the plan slug;
   `layout.md`, "Planning in autonomous flow"); in manual flow write none. A re-plan keeps the line as it is. A plan is
   created from, and merged into, `<main>`: the main branch in manual flow, the integration branch in autonomous flow.
   ```

3. Step 2, new last bullet: "- Autonomous flow: read the code and run the tests in the integration worktree
   (`<main checkout>`), which holds the parts merged before this one; record known failures for it."
4. Step 9, item 1: "Tracking worktree from the main branch (`<main>` = `master` or `main`):" → "Tracking worktree from
   `<main>` (`master` or `main`; the integration branch in autonomous flow):". The command stays.
5. Step 9, item 3, append: "Autonomous flow: first check 1 of `layout.md`, \"Chained parts and the integration
   branch\", again (a wave may have started meanwhile; stop `wave-running`, the plan stays on its tracking branch);
   then merge into `<main checkout>`, the integration worktree, with the same readiness rule; never into the main
   checkout."
6. The answer paragraph: after "wait for a merge." add: "Autonomous flow: say that the plan is on `integration/<name>`
   until the user merges that branch, and mark the other parts by the chain check, not by the main branch."

## Edits of `skills/wave-triage/SKILL.md` for P10 (task C)

None beyond P4's: triage only writes the index `Flow:` line, from which every part takes `integration/<topic>`.

## Edits of `skills/wave-status/SKILL.md` (task C)

1. "## Input", "Without it, inspect every plan folder under `plans/` except `plans/archive/`, plus every index
   (`plans/<date>-<topic>/index.md`)." → append: " Also every plan that exists only on its tracking branch (a plan of
   autonomous flow lives on the integration branch until the user merges it, `layout.md`, \"Planning in autonomous
   flow\"): for each branch `plan/<slug>` of `git branch --list \"plan/*\"` whose plan is not among those folders, its
   README is the path of `git grep -l -F \"slug: \\`<slug>\\`\" plan/<slug> -- \"plans/*README.md\" \":!plans/archive\"`;
   read it and its files from that branch."
   (In the file this is: ``git grep -l -F "slug: `<slug>`" plan/<slug> -- "plans/*README.md" ":!plans/archive"``.)
2. "## Report", the sentence "Then report each index's parts without a plan folder, whether their \"Plan when\"
   condition is met, and their …" → "Then report each index's parts without a plan folder (in the main checkout or on
   the tracking branch `plan/<topic>-p<K>`), whether their \"Plan when\" condition is met (for an index with a
   `Flow: autonomous` line: check 3 of `layout.md`, \"Chained parts and the integration branch\"), and their …".

## Edits of `skills/wave-run` for P10 (task D)

1. `SKILL.md` step 1, first bullet, append: "When the plan folder is missing in the main checkout (a plan of autonomous
   flow, `layout.md`, \"Planning in autonomous flow\"), its tracking branch is the `plan/*` branch where
   `git cat-file -e <branch>:<plan folder>/README.md` succeeds."
2. `autonomous.md`, "Integration target", step 1: after the numbered list (before "For the merge-record check …") add:

   ```markdown
   Another plan of the same target ("Plans of a target" in `layout.md`, "Integration target") has a 🔄 wave on its
   tracking branch → stop `wave-running`, naming that plan and wave; nothing written.
   ```

3. `SKILL.md`, "Stops", row `wave-running`: "a wave of this plan is 🔄, unless it is this wave waiting for task mode"
   → append "; in autonomous flow also a wave of another plan with the same integration branch".

## Invariants and limits

- Manual flow: `wave-plan` still creates the tracking branch from, and merges it into, the main branch; the chain
  check still reads "`✅ merged` on the main branch"; `wave-status` and `wave-run` find every manual plan where they
  find it today (the new lookups apply only when the folder is missing in the main checkout).
- Autonomous flow never writes `<main branch>` or the main checkout, also while planning; the index itself is merged
  by `wave-triage` into the main branch, as in manual flow.
- Never push; never delete the integration branch.
- A part that waits (`part-unmerged`) writes nothing: no tracking branch, no worktree, no integration branch.

## Acceptance tests

Walkthroughs, checked by reading the changed texts.

1. **Night, part 2 after part 1:** index `flow-modes` with `Flow: autonomous`; part 1's README on
   `plan/flow-modes-p1` has F1 `✅ merged` `abc1234`, and `abc1234` is in `integration/flow-modes` → checks 1–4 pass;
   code is read in `../<repo>.worktrees/integration-flow-modes`; `plan/flow-modes-p2` starts at
   `integration/flow-modes`; the plan merge goes into the integration worktree; `git rev-parse main` unchanged.
2. **Part 1 waits for the user:** part 1's F2 is `👀 review` with `Waiting for: review` (manual review) →
   `Stop part-unmerged: part 1 — F2 👀 review (review) — next: review F2, then /wave-run <part 1 folder> merge F2 · $wave-run …`;
   no branch, worktree or commit created.
3. **Part 1 run by hand:** part 1 was manual and its merges are in `main` only → check 3 passes through
   `<main branch>`; check 4 brings `main` into the integration branch.
4. **Shared lock:** part 1's wave 3 is 🔄 → `/wave-run <part 2 folder> 1` stops `wave-running` naming part 1's wave;
   `/wave-plan … part 3` stops the same way.
5. **Finding the plan:** `plans/2026-11-17-flow-modes/plan-2/` is missing in the main checkout → `wave-run` finds
   `plan/flow-modes-p2` by `git cat-file -e`; `wave-status` lists the plan and shows part 2 as planned.
6. **Manual unchanged:** an index without a `Flow:` line → `wave-plan` uses the main branch for the base, the merge
   and the chain check, exactly as before.
