# P12. Safe chained planning: predecessor lookup, no write before plan-exists, an atomic target claim, live rehearsal

Re-plan of the open entries I1–I4 (wave 1, tasks A and E) · feature F1. It changes the texts that
`solutions/P4-planning-assumptions.md` and `solutions/P10-chained-parts.md` put on the F1 branch; where this file
gives a text, it replaces theirs.

## Cause

Line numbers are of `feat/flow-modes-p2/F1-autonomous-planning` at `1c65676`; find each place by its text.

- **I1.** `skills/wave-plan/layout.md:439-441`, "Chained parts and the integration branch", check 3: part J's README
  is read "from its tracking branch `plan/<topic>-p<J>`, else from `<main>`", and in autonomous flow `<main>` is the
  integration branch. Check 3 runs before check 4, so that branch may be missing or lack the newest commits of
  `<main branch>`. A part J run in manual flow loses its tracking branch at its last merge (`wave-run` deletes it), so
  its README exists only on `<main branch>`, and the check wrongly says "part J is not planned".
- **I2.** The `plan-exists` stop sits in `wave-plan` step 9, item 1 (`skills/wave-plan/SKILL.md:240`) and in the
  table row of `layout.md:409`, but check 4 (`layout.md:452`) has already created the integration branch and worktree
  or merged `<main branch>` into it. "Nothing written" does not hold.
- **I3.** The only guard of a shared target is a read of other plans' 🔄 marks (`skills/wave-run/autonomous.md:44`,
  `layout.md:437`). `wave-run` commits its 🔄 mark only in step 2, and `wave-plan` writes no mark at all, so two runs
  started together both read "nothing running" and both write the integration worktree.
- **I4.** Task E checked the texts by reading them; no run followed them in a repository.

## Approach

- **I1:** a fixed source order for part J's README: its tracking branch, else `<main branch>`, else the integration
  branch when it exists. The `Merged` hashes are checked against the integration branch only when it exists, and
  against `<main branch>`.
- **I2:** a read-only check 0 before anything else; step 9 points to it. Manual flow is unchanged (it writes nothing
  before step 9 and still asks there).
- **I3: the target claim**, an atomic ref creation. `git update-ref <ref> <new> <zero ID>` creates the ref only when it
  does not exist, under git's own ref lock, so of two runs exactly one gets it. Refs outside `refs/heads`,
  `refs/bisect`, `refs/worktree` are shared by all worktrees of a repository, need no commit and change no branch.
  The ref points to a blob naming the holder, so a refused run can say who holds the target.
  - Why not a file in `.git/`: worktrees have their own git dirs, and an atomic "create if missing" differs between
    bash and PowerShell. Why not a commit on a tracking branch: two plans have two tracking branches, so there is no
    single place to commit to.
  - The claim covers every run that writes the integration worktree: a wave and the merge form of `wave-run`, and
    `wave-plan` (new plan or re-plan). It is held from before the first check that reads the integration worktree to
    right after the run's last write; a wave waiting for task mode keeps it.
  - The read of 🔄 marks stays as a second guard (it catches a run of an older skill text that takes no claim).
  - Measured on git 2.52.0.windows.1, 2026-11-17: six claims started at the same time → exactly one succeeds; a
    refused claim exits 128 with `cannot lock ref '<ref>': reference already exists`; `git update-ref -d <ref> <wrong
    oid>` exits 1 and keeps the ref; the right oid deletes it; a claim made in one worktree is read from another; the
    blob survives `git gc --prune=now` while the ref points to it.
- **I4:** two rehearsal tasks run the skill texts of the F1 branch in scratch repositories, scenario by scenario
  ("Rehearsal"), and record what they ran and saw in `docs/rehearsals/`. A defect they find is reported, not fixed:
  the report becomes a problem entry and a re-plan.

## Exact text for `skills/wave-plan/layout.md` (task I)

### 1. New subsection at the end of "### Integration target"

After the bullet that starts "Autonomous flow refuses to start a wave when it cannot guarantee this" and before
"### Auto-approval". The inner fence is three backticks.

````markdown
#### Target claim

Every run that writes the integration worktree claims the target first and holds the claim until its last write: a
wave and the merge form of `wave-run` in autonomous flow, and `wave-plan` in autonomous flow of planning (a new plan or
a re-plan). The flow form of `wave-run` and `wave-status` write nothing there and take no claim.

- The claim is the ref `refs/wave-method/claims/integration/<name>`, which every worktree of the repository shares. It
  points to a blob whose one line names the holder: `<plan> wave <N> <YYYY-MM-DD HH:MM>`,
  `<plan> merge <YYYY-MM-DD HH:MM>` or `<plan> planning <YYYY-MM-DD HH:MM>`.
- **Take** it by creating the ref with the zero object ID as its expected old value. Git creates the ref only when it
  does not exist, so of two runs that start together exactly one gets it:

  ```bash
  oid=$(printf '%s\n' "<holder line>" | git hash-object -w --stdin)
  git update-ref refs/wave-method/claims/integration/<name> "$oid" 0000000000000000000000000000000000000000
  ```

  PowerShell: `$oid = "<holder line>" | git hash-object -w --stdin`, then the same `git update-ref`. When
  `git rev-parse --show-object-format` prints `sha256`, the zero ID has 64 zeros. Keep the oid: the release needs it.
- **Refused** (the ref exists): read the holder with `git cat-file -p refs/wave-method/claims/integration/<name>` and
  stop `wave-running`, naming the holder line; nothing written. One exception: a `wave-run` that resumes the wave the
  holder line names (same plan and wave, its Execution ends with `Waiting: task mode …`) takes the claim over; its
  oid is `git rev-parse refs/wave-method/claims/integration/<name>`.
- **Release** it right after the run's last write, and before the report of any stop after the claim:
  `git update-ref -d refs/wave-method/claims/integration/<name> "$oid"`. The expected old value keeps a run from
  deleting a claim that is not its own. A wave that ends with `Waiting: task mode …` keeps the claim: it is still 🔄.
- A claim left by a session that is gone is released only by the user's decision ("Running waves"), with
  `git update-ref -d refs/wave-method/claims/integration/<name>` once no run holds it. `wave-status` shows every claim.
````

### 2. "Plans of a target" bullet of "### Integration target"

Its last sentence "They write the same worktree, so their waves never run at the same time: while a wave of one of
them is 🔄, `wave-run` and `wave-plan` of another stop `wave-running`." stays; append: "The atomic guard is the target
claim (\"Target claim\"); this read of 🔄 marks stays as a second guard."

### 3. "### Planning in autonomous flow"

- The sentence "A re-plan's flow is its README `Flow:` line; a `flow` argument that differs from it stops
  `flow-mismatch` (the flow form of `wave-run` changes the line)." stays; append: "A re-plan in autonomous flow takes
  the target claim (\"Target claim\"), holder line `<plan> planning <YYYY-MM-DD HH:MM>`, after its lock check and
  before it writes anything, and releases it after its merge into the integration worktree; refused → stop
  `wave-running`, nothing written."
- Table row "the tracking branch or folder of a new plan already exists": its `Where` cell becomes
  `` `wave-plan` step 9; autonomous flow: check 0 of "Chained parts and the integration branch", before anything is written ``.
  The other cells stay. The row stays on one line with four cells.

### 4. "#### Chained parts and the integration branch": the new body

Replace everything from the line that starts "In autonomous flow `wave-plan` uses `<main>` = the integration branch"
to the end of the subsection (the last line before "## Archive") with this text. The inner fence is three backticks.

````markdown
In autonomous flow `wave-plan` uses `<main>` = the integration branch and `<main checkout>` = the integration worktree
("Names"). All plans of an index share `integration/<topic>`, so a later part is planned and run against the code of
the earlier parts before the user has merged them. In order, before step 1 of `wave-plan`; a stop in checks 0 to 3
leaves no branch, worktree, commit or claim behind:

0. A new plan of an index part, whose slug the index "Parts" table fixes: stop `plan-exists`, nothing written, when
   the branch `plan/<slug>` exists, the folder `../<repo-folder>.worktrees/<slug>-plan` exists, or the plan folder
   exists on `<main branch>` or, when that branch exists, on `integration/<topic>`
   (`git cat-file -e <branch>:<plan folder>/README.md`). A raw list chooses its slug so that none of these exists, and
   never stops here.
1. Take the target claim ("Target claim"), holder line `<slug> planning <YYYY-MM-DD HH:MM>`; refused → stop
   `wave-running`, naming the holder. Then stop `wave-running`, naming the plan and wave, when a plan with the same
   target has a 🔄 wave ("Integration target"). Every stop from here on releases the claim first.
2. The checks of `wave-run/autonomous.md`, "Integration target", step 1, without its claim (stop `target-unsafe`).
3. The part is marked "plan after part J is merged": read part J's README,
   `git show <source>:plans/<date>-<topic>/plan-<J>/README.md`, from the first source that has it: part J's tracking
   branch `plan/<slug of part J>` (the slug in the index "Parts" table); else `<main branch>` (a part J run in manual
   flow loses its tracking branch at its last merge); else `integration/<topic>`, when that branch exists. Part J is
   merged when every feature of that README is `✅ merged` or ➖ and each of their `Merged` hashes is in
   `integration/<topic>` (only when that branch exists) or in `<main branch>`
   (`git merge-base --is-ancestor <hash> <branch>`). Otherwise stop:

   ```
   Stop part-unmerged: part <J> — F<k> <status> (<Waiting for>), … — next: …
   ```

   `next:` names, per feature, what it waits for: a `👀 review` feature its review and its merge command, a ⚠️ or 🔄
   feature its `Waiting for`. Give each command in both forms ("Commands"). When no source has the README:
   `part <J> is not planned`, with its `/wave-plan` command. Whoever drives an unattended run moves on and reports
   the waiting part with that line.
4. `wave-run/autonomous.md`, "Integration target", step 2 (create the branch and worktree, bring in `<main branch>`;
   stop `target-conflict`): the first write to the integration worktree.

Then `wave-plan` reads the code and runs the tests in the integration worktree, creates the tracking branch from the
integration branch, merges it into the integration worktree, never into the main checkout, and releases the claim
right after that merge (`wave-plan` step 9). The plan folder is on the integration branch only, until the user merges
it into `<main branch>`.
````

### 5. "## Running waves", last bullet

"A lock left by a session that is gone is released only by the user's decision." stays; append: "So is a target
claim of autonomous flow (\"Target claim\")."

## Edits of `skills/wave-plan/SKILL.md` (task J)

Find each place by its text on the F1 branch.

1. "## Input", "A part of an index" bullet: the sentence "In autonomous flow of planning run the four checks of
   `layout.md`, \"Chained parts and the integration branch\", before step 1 instead (stops `wave-running`,
   `target-unsafe`, `part-unmerged`, `target-conflict`)." becomes "In autonomous flow of planning run checks 0 to 4 of
   `layout.md`, \"Chained parts and the integration branch\", before step 1 instead (stops `plan-exists`,
   `wave-running`, `target-unsafe`, `part-unmerged`, `target-conflict`); they take the target claim, which step 9
   releases."
2. "## Input", "A raw list" bullet: the sentence "In autonomous flow of planning, before step 1: checks 1, 2 and 4 of
   `layout.md`, \"Chained parts and the integration branch\"." becomes "In autonomous flow of planning, before step 1:
   choose the plan slug so that check 0 of `layout.md`, \"Chained parts and the integration branch\", finds nothing,
   then run its checks 1, 2 and 4; they take the target claim, which step 9 releases."
3. "Re-planning" paragraph: after the sentence that ends "…report `Stop wave-running: wave <N> is running — next:
   wait, or the user releases the lock` and stop without writing." add: "Autonomous flow: then take the target claim,
   holder line `<plan> planning <YYYY-MM-DD HH:MM>` (`layout.md`, \"Target claim\"); refused → stop `wave-running`,
   naming the holder, without writing; step 9 releases it."
4. Step 9, item 1: the sentence "Autonomous flow: for a new plan with an existing branch or folder, stop
   `plan-exists`; do not write the plan." becomes "Autonomous flow: a new plan already passed check 0 of
   `layout.md`, \"Chained parts and the integration branch\", before step 1 (stop `plan-exists`, nothing written)."
5. Step 9, item 3: the sentences "Autonomous flow: first check 1 of `layout.md`, \"Chained parts and the integration
   branch\", again (a wave may have started meanwhile; stop `wave-running`, the plan stays on its tracking branch);
   then merge into `<main checkout>`, the integration worktree, with the same readiness rule; never into the main
   checkout." become "Autonomous flow: the run still holds its target claim
   (`git cat-file -p refs/wave-method/claims/integration/<name>` prints this run's holder line; otherwise stop
   `wave-running`, the plan stays on its tracking branch); merge into `<main checkout>`, the integration worktree,
   with the same readiness rule, never into the main checkout; then release the claim (`layout.md`, \"Target
   claim\"), also when the integration worktree was not ready and the user got the merge command."

## Edits of `skills/wave-run` and `skills/wave-status` (task K)

1. `skills/wave-run/autonomous.md`, "## Integration target":
   - "Step 1, read-only, right after the README is read." → "Step 1, right after the README is read; it writes
     nothing but the target claim."
   - The paragraph "Another plan of the same target (`layout.md`, \"Integration target\") has a 🔄 wave on its
     tracking branch → stop `wave-running`, naming that plan and wave; nothing written." is replaced by:

     ```markdown
     Then take the target claim (`layout.md`, "Target claim"), holder line `<plan> wave <N> <YYYY-MM-DD HH:MM>`, or
     `<plan> merge <YYYY-MM-DD HH:MM>` in the merge form; refused → stop `wave-running`, naming the holder, nothing
     written, unless this run resumes the holder's own wave (it takes the claim over). The flow form runs the checks
     above and takes no claim. Then: another plan of the same target (`layout.md`, "Integration target") has a 🔄
     wave on its tracking branch → stop `wave-running`, naming that plan and wave. From the claim on, every stop
     releases the claim before its report.
     ```

   - After the numbered list of "Step 2" (its item 3) and before "## Skipped tasks", a new paragraph:

     ```markdown
     Step 3, release: right after the run's last write to the integration worktree (the end of "Auto-approval", in a
     wave and in the merge form), release the target claim (`layout.md`, "Target claim"). A run that ends with
     `Waiting: task mode …` keeps it; the resume takes it over.
     ```

2. `skills/wave-run/SKILL.md`:
   - "## Stops" table, row `wave-running`, the `When` cell: append "; in autonomous flow also a target claim held by
     another run (`layout.md`, \"Target claim\")". The row stays one line with three cells.
   - Step 1, the bullet "Autonomous flow: the integration-target checks of `autonomous.md`, \"Integration target\",
     step 1." → append " They take the target claim."
3. `skills/wave-run/merge.md`, "## Checks", first bullet: "In autonomous flow first run the read-only checks of
   `autonomous.md`, \"Integration target\", step 1." → "In autonomous flow first run the checks of `autonomous.md`,
   \"Integration target\", step 1 (they take the target claim; its step 3 releases it)."
4. `skills/wave-status/SKILL.md`, "## Report" list:
   - The `Integration:` bullet: append "When `refs/wave-method/claims/integration/<name>` exists, add
     `· claimed by <holder line>` (`git cat-file -p <that ref>`, `layout.md`, \"Target claim\")."
   - The `Leftovers:` bullet: append "A target claim whose holder line names a wave that is not 🔄 on that plan's
     tracking branch: suggest `git update-ref -d refs/wave-method/claims/integration/<name>`, once the user is sure no
     run holds it."

## Invariants and limits

- Manual flow: no claim, no check 0; every manual sentence stays as it is.
- A stop in checks 0 to 3 of `wave-plan` leaves the refs (`git for-each-ref`) and `git worktree list` exactly as
  before the run.
- Only the run whose oid the ref holds deletes the claim; a user deletes it by hand only when no run holds it.
- The claim ref is never pushed; nothing in the skills pushes.

## Rehearsal

Both rehearsal tasks run the skill texts of their working folder (the F1 branch with tasks I, J and K), not any
installed wave skill: they read `skills/<skill>/SKILL.md` and `skills/wave-plan/layout.md` there and do what the texts
say, as the coordinator of that skill would. A point where a text tells them to ask the user in autonomous flow is a
defect: they record it and take the first reading instead.

### Toy project

A new folder `<scratch>` in the system temp folder, outside the wave-method repository. `git init -b main repo`
there; in `repo`:

- `todo.py`: `VERSION = "0.1.0"`; `add(items, text)` returns `items + [{"text": text, "done": False}]`;
  `rm(items, n)` returns the list without item `n`; `list_items(items)` returns the lines `"<n>. <text>"` of the
  items that are not done.
- `test_todo.py`: `unittest` tests for the three functions (one each). Check: `python -m unittest` in `repo`.
- One commit `init`.

### Chain fixture

On `main` of the toy repo, one commit `Index todo` with `plans/2026-11-17-todo/index.md` in the index format of
`skills/wave-triage/SKILL.md` step 6 (small index, no `triage/` records):

- header: `- Index: plans/2026-11-17-todo/index.md · created 2026-11-17 · base: <init hash>`, then
  `- Flow: autonomous · target: integration/todo`;
- problems, all `low`: P1 "`--version` prints `VERSION`" (part 1); P2 "`list` prints a header line with the version"
  (part 2, depends on P1); P3 "`list --all` also shows done items" (part 2); P4 "`done <n>` marks an item done" (part 3);
- parts: 1 `todo-p1` now; 2 `todo-p2` after part 1 merged; 3 `todo-p3` now;
- Assumptions: none; Open questions: none.

Part 1 (fixture, not planned for real): the branch `feat/todo-p1/F1-version-option` from `main` with one commit that
adds a `__main__` block with `--version` to `todo.py`; and a part 1 README at `plans/2026-11-17-todo/plan-1/README.md`
with the header lines `- Plan: … · slug: \`todo-p1\` · tracking branch: \`plan/todo-p1\` …`,
`- Index: plans/2026-11-17-todo/index.md part 1`, `- Re-plans: none`,
`- Flow: autonomous · target: integration/todo`, and a "Features" table in the README template's columns with one row
F1 `version-option`, whose `Status`, `Waiting for` and `Merged` the scenario sets. Where the README lives (the branch
`plan/todo-p1`, or `main`) the scenario says too.

### Scenarios of task L (autonomous index, `docs/rehearsals/autonomous-planning.md`)

1. **Triage assumes.** A second toy repo `<scratch>/triage-repo` (same toy project, no index). Run `wave-triage` with
   the arguments `flow autonomous 1. add a --version option 2. show done items differently in list 3. rename rm to delete`.
   Expected: no question; the index header has `- Flow: autonomous · target: integration/<topic>` right after the
   `- Index:` line; "Assumptions" has an `Assumed (autonomous, not asked) · P2: …` line (strike-through or hide);
   "Open questions" is `none`; the index is committed and merged into `main`.
2. **Part 1 waits for review.** Chain fixture; part 1 README on `plan/todo-p1` with F1 `👀 review`, `Waiting for`
   `review`, `Merged` empty. Snapshot `git for-each-ref --format="%(refname) %(objectname)"` and
   `git worktree list --porcelain`. Run `wave-plan` with `plans/2026-11-17-todo/index.md part 2`. Expected: the first
   line after `Started:` is `Stop part-unmerged: part 1 — F1 👀 review (review) — next: …`, naming the merge command
   of F1 in both forms; both snapshots unchanged (no `integration/todo`, no `plan/todo-p2`, no claim ref).
3. **Part 2 on the integration branch.** Continue from 2: `git worktree add -b integration/todo
   ../repo.worktrees/integration-todo main`; in that worktree `git merge --no-ff feat/todo-p1/F1-version-option`
   (hash H1); on `plan/todo-p1` set F1 to `✅ merged`, empty `Waiting for`, `Merged` H1. Note `git rev-parse main`.
   Run `wave-plan` with `plans/2026-11-17-todo/index.md part 2` to the end (a real plan of P2 and P3). Expected: no
   question; the README has `- Flow: autonomous · target: integration/todo`;
   `git merge-base --is-ancestor H1 plan/todo-p2` succeeds;
   `git cat-file -e integration/todo:plans/2026-11-17-todo/plan-2/README.md` succeeds and the same for `main` fails;
   `git rev-parse main` unchanged; `git for-each-ref refs/wave-method/claims/` prints nothing; `status_check.py` on the
   plan folder (in the tracking worktree) exits 0.

### Scenarios of task M (chain safety, `docs/rehearsals/chained-parts-safety.md`)

4. **Manual predecessor without a tracking branch (I1).** Chain fixture with part 1 run "by hand":
   `git merge --no-ff feat/todo-p1/F1-version-option` on `main` (hash H1), then the part 1 README committed on `main`
   with F1 `✅ merged`, `Merged` H1. No `plan/todo-p1`, no `integration/todo`. Run `wave-plan` with
   `plans/2026-11-17-todo/index.md part 2` to the end. Expected: check 3 finds the README on `main` and passes; check 4
   creates `integration/todo` from `main` (`../repo.worktrees/integration-todo`); the plan is merged there;
   `git rev-parse main` unchanged by the run; no claim ref left.
5. **plan-exists writes nothing (I2).** Continue from 4: one more commit on `main` (any file outside `plans/`); note
   X = `git rev-parse integration/todo` and the snapshots of scenario 2. Run `wave-plan` with
   `plans/2026-11-17-todo/index.md part 2` again. Expected: `Stop plan-exists: …` as the first line after `Started:`;
   `integration/todo` still at X (the new `main` commit not merged in); snapshots unchanged; no claim ref.
6. **Claim (I3).** Continue from 5. Take a claim by hand with the commands of `layout.md`, "Target claim", holder line
   `todo-p1 wave 2 2026-11-17 03:00`; note its oid.
   - Run `wave-plan` with `plans/2026-11-17-todo/index.md part 3`. Expected:
     `Stop wave-running: … todo-p1 wave 2 2026-11-17 03:00 …`; the claim ref still points to the noted oid; no
     `plan/todo-p3`; snapshots otherwise unchanged.
   - Run `wave-run` with `plans/2026-11-17-todo/plan-2 1`. Expected: it stops `wave-running` naming the same holder
     before "wave started": wave 1 is still ⬜ on `plan/todo-p2`, no feature branch of `todo-p2` exists.
   - `git update-ref -d <claim ref> <some other oid>` fails and keeps the ref; with the noted oid it deletes it.
   - Race, 10 rounds: start two claims at the same time (two background subshells running the commands of "Target
     claim" with holder lines `race-a` and `race-b`, then `wait`); exactly one succeeds in every round; release the
     winner's claim with its oid before the next round.
