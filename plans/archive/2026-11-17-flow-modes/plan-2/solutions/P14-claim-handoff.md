# P14. Claim handoff: a waiting claim, an atomic takeover, a run token, and what a refused claim leaves

Re-plan of the open entries I7 and I8 (wave 3, tasks I and M) · feature F1. It changes the "Target claim" text that
`solutions/P12-chain-safety.md` put on the F1 branch; where this file gives a text, it replaces that one.

## Cause

Line numbers are of `feat/flow-modes-p2/F1-autonomous-planning` at `6206f9d`; find each place by its text.

- **I7.** `skills/wave-plan/layout.md:374-377` lets "a `wave-run` that resumes the wave the holder line names" take the
  claim over by reading its oid (`git rev-parse <ref>`); `skills/wave-run/autonomous.md:45-47` and `:64-66` point to
  it. The takeover is a read, not a write: two resumes started together both read the same oid and both go on, and
  either one's guarded release (`git update-ref -d <ref> <oid>`) deletes the claim the other still uses. The holder
  line also does not tell a waiting wave from a running one, so a resume started while another resume already runs
  takes the claim over from it too.
- **Same oid for two runs.** The holder line is `<plan> wave <N> <YYYY-MM-DD HH:MM>`; two runs of one plan and wave in
  the same minute store the same blob, so their oids are equal and the guarded release cannot tell them apart.
  Measured 2026-11-17 on git 2.52.0.windows.1: `printf 'p wave 2 2026-11-17 03:10\n' | git hash-object -w --stdin`
  twice gives one oid.
- **I8.** `layout.md:374-375` and `autonomous.md:46-47` say a refused claim writes nothing, but the take command runs
  `git hash-object -w` before `git update-ref`, so the holder blob is stored even when the ref is refused. The blob is
  required: `git update-ref <ref> <oid of a missing object> <zero ID>` exits 128 with `trying to write ref … with
  nonexistent object` (measured, same git). So the blob cannot be avoided; the promise must be stated precisely.

## Approach

- **A waiting form of the claim.** A wave that ends with `Waiting: task mode …` keeps the claim but rewrites it, with
  a compare-and-swap from its own oid, to a holder line with the word `waiting`. A running wave, a merge and a
  planning run hold an "active" line. So a resume can tell "nobody runs this wave now" (waiting) from "another resume
  already runs it" (active).
- **Takeover is a compare-and-swap.** A resume reads the current oid `cur`; only when its holder line is the waiting
  line of its own plan and wave does it run `git update-ref <ref> <own oid> <cur>`. Git moves the ref only while it
  still points to `cur`, under its ref lock, so of two resumes exactly one succeeds; the other stops `wave-running`
  naming the winner. Measured 2026-11-17, git 2.52.0.windows.1: 10 rounds of two concurrent takeovers from one
  waiting oid → 1 success in every round; a CAS from a wrong old value exits 128 with `is at <oid> but expected
  <oid>` and leaves the ref.
- **A run token** makes every run's oid its own: every holder line ends with ` run <token>`, eight random hex
  characters chosen once per run. Two runs never share an oid, so the guarded release deletes only its own claim.
  ASCII only: Windows PowerShell 5.1 pipes text to a native program in its `$OutputEncoding` (ASCII by default), which
  would turn a non-ASCII character such as `·` into `?`.
  - bash: `od -An -N4 -tx1 /dev/urandom | tr -d ' \n'` (coreutils; present in Git Bash and macOS);
  - PowerShell: `[guid]::NewGuid().ToString('N').Substring(0, 8)` (measured on PowerShell 5.1).
- **I8: the guarantee is about refs, worktrees and commits.** "Nothing written" after a refusal means no ref, branch,
  worktree, commit or worktree file changed; the object store may gain one unreachable loose blob, which `git gc`
  prunes later. Rehearsals compare refs and worktrees, not objects. Alternatives not taken: pointing the claim at an
  existing object (the holder could no longer be named) and checking the ref before writing the blob (a race between
  the check and the claim stays, and the blob is still needed to claim).

## Exact text for `skills/wave-plan/layout.md`

Replace the whole subsection "#### Target claim" — from its heading to the last line before "### Auto-approval" —
with this text. The inner fences are three backticks.

````markdown
#### Target claim

Every run that writes the integration worktree claims the target first and holds the claim until its last write: a
wave and the merge form of `wave-run` in autonomous flow, and `wave-plan` in autonomous flow of planning (a new plan or
a re-plan). The flow form of `wave-run`, a task-mode session (`… task <ID>`) and `wave-status` write nothing there and
take no claim.

- The claim is the ref `refs/wave-method/claims/integration/<name>`, which every worktree of the repository shares. It
  points to a blob whose one line names the holder, in ASCII only: `<plan> wave <N> <YYYY-MM-DD HH:MM> run <token>`,
  `<plan> wave <N> waiting <YYYY-MM-DD HH:MM> run <token>` (a wave waiting for task mode),
  `<plan> merge <YYYY-MM-DD HH:MM> run <token>` or `<plan> planning <YYYY-MM-DD HH:MM> run <token>`. Where another
  text names a holder line without ` run <token>`, the run appends it. `<token>` is eight random hex characters,
  chosen once per run, so no two runs hold the same oid:

  ```bash
  token=$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n')
  ```

  PowerShell: `$token = [guid]::NewGuid().ToString('N').Substring(0, 8)`.
- **Take** it by creating the ref with the zero object ID as its expected old value. Git creates the ref only when it
  does not exist, so of two runs that start together exactly one gets it:

  ```bash
  oid=$(printf '%s\n' "<holder line>" | git hash-object -w --stdin)
  git update-ref refs/wave-method/claims/integration/<name> "$oid" 0000000000000000000000000000000000000000
  ```

  PowerShell: `$oid = "<holder line>" | git hash-object -w --stdin`, then the same `git update-ref`. When
  `git rev-parse --show-object-format` prints `sha256`, the zero ID has 64 zeros. Keep the oid: every later step of
  the claim needs it.
- **Refused** (the ref exists): read the holder with `git cat-file -p refs/wave-method/claims/integration/<name>` and
  stop `wave-running`, naming the holder line; nothing written. Only a resume takes over a held claim ("Take over"
  below).
- **Nothing written** by a refused claim, wait or takeover means: the attempt changed no ref, branch, worktree, commit
  or worktree file. `git hash-object -w` stores the holder blob before `git update-ref` tries the ref (git refuses a ref to a
  missing object), so each refused attempt may leave one unreachable loose blob in the object store; `git gc` prunes
  it later (after `gc.pruneExpire`, two weeks by default). Check that a stop wrote nothing by comparing refs and
  worktrees, not the object store.
- **Wait**: a wave that ends with `Waiting: task mode …` keeps the claim (it is still 🔄) and marks it as waiting,
  right after its "waiting for task mode" commit: store the line `<plan> wave <N> waiting <YYYY-MM-DD HH:MM> run
  <token>` with `git hash-object -w --stdin` as above, as `$wait`, then
  `git update-ref refs/wave-method/claims/integration/<name> "$wait" "$oid"`. Exit 0 → the claim now has the oid
  `$wait`. Otherwise the claim is no longer this run's: stop `wave-running`, naming the holder, instead of the
  waiting report.
- **Take over**: a `wave-run` that resumes a wave waiting for task mode (`wave-run/task-mode.md`) reads
  `cur=$(git rev-parse -q --verify refs/wave-method/claims/integration/<name>)` (PowerShell: `$cur = …`, the same
  command), then:
  - no ref: take the claim as above;
  - the holder line (`git cat-file -p "$cur"`) is the waiting line of this plan and wave: store this run's own line
    `<plan> wave <N> <YYYY-MM-DD HH:MM> run <token>` as `$oid`, then
    `git update-ref refs/wave-method/claims/integration/<name> "$oid" "$cur"`. Git moves the ref only while it still
    points to `$cur`, so of two resumes exactly one takes it over. Exit 0 → this run holds the claim with `$oid`;
    otherwise read the holder again and stop `wave-running`, naming it;
  - any other holder line, the running line of this same wave included (another resume runs it): stop
    `wave-running`, naming it.
- **Release** it right after the run's last write, and before the report of any stop after the claim:
  `git update-ref -d refs/wave-method/claims/integration/<name> "$oid"`. The expected old value, unique by its token,
  keeps a run from deleting a claim that is not its own. A run that did not get the claim releases nothing.
- A claim left by a session that is gone is released only by the user's decision ("Running waves"), with
  `git update-ref -d refs/wave-method/claims/integration/<name>` once no run holds it. `wave-status` shows every claim.
````

## Edits of `skills/wave-run/autonomous.md` and `skills/wave-plan/SKILL.md`

Find each place by its text on the F1 branch.

1. `skills/wave-run/autonomous.md`, "## Integration target", the claim paragraph after the numbered checks of step 1:
   the words "refused → stop `wave-running`, naming the holder, nothing written, unless this run resumes the holder's
   own wave (it takes the claim over)." become "refused → stop `wave-running`, naming the holder, nothing written. A
   resume of a wave waiting for task mode takes the claim over instead (`layout.md`, \"Target claim\", \"Take
   over\")." The rest of the paragraph stays.
2. `skills/wave-run/autonomous.md`, the paragraph that starts "Step 3, release:": its last sentence "A run that ends
   with `Waiting: task mode …` keeps it; the resume takes it over." becomes "A run that ends with `Waiting: task mode
   …` keeps it and marks it as waiting right after its \"waiting for task mode\" commit (`layout.md`, \"Target
   claim\", \"Wait\"); the resume takes it over."
3. `skills/wave-plan/SKILL.md`, step 9, item 3: the words "(`git cat-file -p refs/wave-method/claims/integration/<name>`
   prints this run's holder line;" become "(`git rev-parse refs/wave-method/claims/integration/<name>` prints this
   run's oid;". The rest of the sentence stays.

Nothing else changes: `wave-run/SKILL.md`, `wave-run/merge.md`, `wave-run/task-mode.md` and `wave-status/SKILL.md`
already point to "Target claim" and stay valid (`wave-status` prints the holder line as it is, `waiting` included).

## Invariants and limits

- Manual flow: no claim; nothing of this file applies.
- At any time at most one run holds the claim of a target, and only that run's oid deletes it.
- A waiting claim is taken over only by a resume of the same plan and wave; every other run is refused as before.
- A run that crashes before "Wait" leaves an active line of a wave whose Execution ends with `Waiting: task mode …`;
  the resume is refused (`wave-running`, naming it) and the user releases the claim ("Running waves").
- The claim ref is never pushed; nothing in the skills pushes.

## Rehearsal (task Q)

A new folder `<scratch>` in the system temp folder, outside the wave-method repository; `git init -b main repo` there
and one empty commit `init` (`git commit --allow-empty -m init`). `R=refs/wave-method/claims/integration/todo`. Every
claim step uses the commands of the "Target claim" text of the working folder, as written; times are fixed strings.
Snapshots: `git for-each-ref --format="%(refname) %(objectname)"`, `git worktree list --porcelain`,
`git status --porcelain`.

### Scenario 7. Claim handoff (I7)

1. **Wait.** Take a claim with holder `todo-p2 wave 1 2026-11-17 03:00 run <token>` (oid A); apply "Wait" with time
   `2026-11-17 03:20` (oid W). Expected: exit 0; `git cat-file -p "$R"` prints `todo-p2 wave 1 waiting 2026-11-17
   03:20 run <token>`; `git update-ref -d "$R" "$A"` fails and the ref stays at W.
2. **Two resumes, 10 rounds.** Each round: `git update-ref "$R" "$W"` (setup), then two background subshells that each
   follow "Take over" for plan `todo-p2` wave 1 with its own token and time `2026-11-17 03:30`, each writing its oid
   and exit code to a file; `wait`. Expected per round: exactly one exit 0; the two oids differ; `git rev-parse "$R"`
   is the winner's oid; the loser's `git update-ref -d "$R" <loser oid>` fails and the ref stays at the winner's oid.
   Record the line `Takeover race: <successes per round>`.
3. **Resume while another resume runs.** The ref holds the winner's running line from round 10. A third resume follows
   "Take over". Expected: it stops `wave-running`, naming `todo-p2 wave 1 2026-11-17 03:30 run <winner token>`; the
   ref is unchanged.
4. **Wait after losing the claim.** With the ref at the winner's oid, a run holding oid A applies "Wait". Expected:
   `git update-ref` fails; per the text the run stops `wave-running`, naming the winner; the ref is unchanged.
5. **PowerShell**, when the environment has it: generate a token and take a fresh claim (after releasing the
   winner's with its oid) with the PowerShell forms of the text; `git cat-file -p "$R"` prints the ASCII holder line
   (record whether it ends with a carriage return); release it with its oid. Not available → record why.

### Scenario 8. Refused-claim objects (I8)

Take a claim with holder `todo-p1 wave 2 2026-11-17 03:00 run <token>` (oid H). Snapshot, and list unreachable objects
with `git fsck --unreachable --no-reflogs`. A second run tries "Take" with holder
`todo-p3 planning 2026-11-17 03:05 run <token>` (candidate oid C). Expected: refused (exit 128, `reference already
exists`); the three snapshots are identical; `git fsck --unreachable --no-reflogs` lists C as an unreachable blob;
`git -c gc.pruneExpire=now gc` then `git cat-file -e "$C"` fails and `git cat-file -e "$H"` succeeds; the ref is
still at H. This matches the "Nothing written" item, so the result is `holds`.

## Acceptance tests

- `layout.md` "Target claim" has the items Take, Refused, Nothing written, Wait, Take over, Release, in this order,
  and every holder-line form ends with ` run <token>`.
- Scenario 7 holds in all five parts, with `Takeover race: 1 1 1 1 1 1 1 1 1 1`; scenario 8 holds.
- The check command of the wave is green.
