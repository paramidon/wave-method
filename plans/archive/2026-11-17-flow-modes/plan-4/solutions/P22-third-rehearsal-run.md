# P22. Third run of both end-to-end rehearsals

User problem: (re-plan, I7, I8, I12–I17) the second runs (tasks N and O) left the `v2.12.0` chain unfinished at a Claude
usage limit, judged the M2 report against a wrong expectation, counted the baseline's old scope cleanup as a parity
finding, found an unreadable `Wave-Model` trailer, never exercised the scope gate because task B amended the forced
file away, and staged two launcher files outside scratch · feature F2

This file amends `solutions/P21-rehearsal-isolation-rerun.md`, which amends `solutions/P9-end-to-end-runs.md`.
Everything in P9 and P21 holds unless a section below replaces it. Tasks Q and R read P9, then P21, then this file.

## Cause

- **I7, I12.** Base M4 exited 1 with Claude's 5-hour usage message after 3 turns; P21 had no rule for it, so the task
  treated it as a procedure failure and stopped with base M4–M6 unrun. Cur ran its whole chain first, so the stop
  left no comparable `base` row after M3.
- **I13.** P9 expects the merge question as the final line, but `layout.md` ("Run times") makes the
  `Started: … · Finished: …` line the last line of every report. Both versions followed `layout.md`: a plan error.
- **I14.** Under `v2.12.0` task A committed `__pycache__` files and the coordinator removed them with a cleanup commit.
  That is the old behaviour P18 replaced, so it is an intended difference, not a "manual flow differs" finding.
- **I15.** The executor wrote `Wave-Model: …` after a blank line and Claude Code appended its own
  `Co-Authored-By: …` paragraph after another blank line. Git reads trailers only in the message's last paragraph,
  so `%(trailers:key=Wave-Model,valueonly)` printed nothing (checked: the same message with both trailers in one
  paragraph prints the model). The coordinator accepted the commit anyway: step 5 says "read the trailer" without the
  command. Fixed by P23; the reruns show it.
- **I16.** P21's hook amended `stray.txt` into B's first commit only (a marker stopped it after that); B amended its
  commit again without the file, so no commit that the scope command sees ever held it.
- **I17.** The executor wrote its launcher script and the first ref snapshot of the working folder into the system
  temp folder before it made the scratch folder, then moved them in.

## Approach

1. **Usage stop.** A Claude usage limit is neither a finding about the skills nor a procedure failure: the step is
   `Not run (usage limit)`, no further `claude` call starts, and the record keeps everything run so far.
2. **Interleaved manual chain.** `cur` and `base` alternate step by step, so any stop leaves both sides compared up to
   the same step.
3. **Corrected expectations** for the report's last lines (I13) and for scope and trailers, where `cur` and `base`
   are expected to differ (I14, I15).
4. **A sticky hook** (I16): every commit of task B whose parent lacks `stray.txt` gets it, so no amend or new commit of
   B hands over a history without it; a commit of B that deletes the file is kept, and the scope command still lists
   the file.
5. **Every file of the run in scratch** (I17).

## Files of the run (amends P21 "Isolation")

The scratch folder is the first thing the task makes: `scratch=$(mktemp -d)` is the first command, before any file of
the run exists. Every file the task writes, other than its record, is created directly under `$scratch`: launcher
scripts in `$scratch/launch/`, the working folder's ref snapshots as `$scratch/logs/working-before.refs` and
`working-after.refs`, notes and evidence in `$scratch/logs/`. Never write a file of the run anywhere else (the system
temp folder outside `$scratch`, the home folder, the working folder) and then move it. The task report names the
scratch path; the record writes `<scratch>`.

## Usage stop (amends P21 "Call form")

After every `claude` call, before its snapshots, test the call's output:

```bash
grep -l -i -E "hit your .*limit|usage limit" "$scratch/logs/<repo>-<step>.jsonl" "$scratch/logs/<repo>-<step>.err"
```

Any file printed → the call is a **usage stop**: record its exit code, the snapshots and the watch as usual, then the
step is `Not run (usage limit)`, and every later step that needs `claude` is `Not run (usage limit)` without a call.
Steps without `claude` (pytest, `status_check.py`) still run when their inputs exist. It is not a Finding and not a
procedure failure; the record's "Not verified" lists each step it left, and the task report lists them as one problem
`usage limit: <steps not run>` with the scratch path, so a later task can continue from that folder. In the record,
quote the limit message with its reset time and time zone replaced by `<reset>`.

## Manual run (task Q)

Amends P21 "Manual rerun (task N)".

**Order.** Isolation, seeding `cur` and `base` (as P21), P0 in `$scratch/cur`, then one call at a time in this order:
`cur-M0`, `base-M0`, `cur-M1`, `cur-M2`, `base-M2`, `cur-M3`, `base-M3`, `cur-M4`, `base-M4`, `cur-M5`, `base-M5`,
`cur-M6-pytest`, `base-M6-pytest`, `cur-M6`, `base-M6`.

**Report lines (replaces P9's "ends with a question" for M2 and M4).** The last non-empty line of the last result
is the `Started: … · Finished: …` line; the last non-empty line before it asks whether to merge F2 (M2) or F1 and F3
(M4). Both `cur` and `base`.

**Task commits.** After M2 and after M4, in both repositories:

```bash
git -C "$scratch/<repo>" log --all --no-merges --grep="^todo-cli F[0-9]* / [A-Z]*:" \
  --format="%h %s | %(trailers:key=Wave-Model,valueonly,separator=%x2C)" > "$scratch/logs/<repo>-<step>.trailers"
git -C "$scratch/<repo>" log --all --no-merges --grep="^todo-cli F[0-9]* / [A-Z]*:" --name-only \
  --format="== %h %s" > "$scratch/logs/<repo>-<step>.paths"
```

- `cur`: every line of `.trailers` names a model after `|`, or the task of a line without one is ⚠️ with a
  `below tier` entry and its commit is in no merged feature (P23). `.paths` lists only the task's `Files` paths
  (`waves/w0<N>.md` of the example), or the task is ⚠️ with an `out of scope` entry and the report asks the user (P18).
- `base`: recorded, not judged. A difference from `cur` in these two checks is an **intended difference** (P18 for
  scope, P23 for trailers): write it in the comparison table as `intended (P18)` or `intended (P23)`, never as
  "manual flow differs from v2.12.0".

**Comparison table.** P9's columns plus two: `Task commits: out-of-scope paths and what happened`, `Task commits
without a readable Wave-Model`. Every other cell difference stays a finding "manual flow differs from v2.12.0", as
P9 says. A row whose step was `Not run (usage limit)` on one side shows `Not run` in every cell of that side and is
not a finding.

## Autonomous run (task R)

Amends P21 "Autonomous rerun (task O)".

**Hook (replaces P21's hook).** Same place, `$scratch/night/.git/hooks/post-commit`, `chmod +x`, not committed:

```sh
#!/bin/sh
# End-to-end run: task B of F2 always hands over a history in which stray.txt, outside its file list, was added.
case "$(git log -1 --format=%s)" in
  "wordstat-cli F2 / B:"*) ;;
  *) exit 0 ;;
esac
git cat-file -e HEAD:stray.txt 2>/dev/null && exit 0
git cat-file -e HEAD~1:stray.txt 2>/dev/null && exit 0
printf 'forced out-of-scope file of the end-to-end run\n' > stray.txt
git add stray.txt
git commit -q --amend --no-edit --no-verify
```

The amend runs the hook again; `HEAD` then has the file, so it exits. A commit of B whose parent has the file (B
deleting it in a new commit) is left alone: the earlier commit still adds it.

**Probe (replaces P21's probe).** In `$scratch/hookprobe` (`git init -q -b main`, the run's identity,
`core.autocrlf false`, the hook copied in), each result written to `$scratch/logs/hookprobe.txt`:

1. `git commit -q --allow-empty -m init`; `H=$(git rev-parse HEAD)`.
2. `printf '1\n' > a.txt; git add a.txt; git commit -q -m "wordstat-cli F2 / B: probe"` →
   `git show --name-only --format= HEAD` prints `a.txt` and `stray.txt`; `git log -1 --format=%s` is unchanged.
3. `git rm -q --cached stray.txt; rm stray.txt; git commit -q --amend --no-edit` → `HEAD` still has `stray.txt`.
4. `git rm -q stray.txt; git commit -q -m "wordstat-cli F2 / B: remove"` → `HEAD` has no `stray.txt`, and
   `git log --no-merges --name-only --format= $H..HEAD | sort -u` prints `a.txt` and `stray.txt`.
5. `git commit -q --allow-empty -m "other: probe"` → `git show --name-only --format= HEAD` prints nothing; then
   `git reset -q --hard HEAD~1`.
6. `git revert --no-edit $H..HEAD` exits 0 and `git diff --quiet $H HEAD` exits 0.

Any step failing is a procedure failure: stop as for P0. The probe repository has its own hook copy; nothing to
clean up in `night`.

**Expectations that replace P21's for A2 (the others stay):**

- F2 `⚠️ blocked I<a>`, `Waiting for: I<a>`, task B ⚠️; I<a> is open in `problems.md` on `plan/wordstat-cli` and names
  `stray.txt`. Which gate made it (step 5 "Scope" or auto-approval condition 6) is recorded, not judged.
- `git log --format=%s integration/wordstat-cli..feat/wordstat-cli/F2-top-words-cli` shows B's commits and one
  `Revert "wordstat-cli F2 / B: …"` per B commit; `git log --format="%h %s" -- stray.txt` on that range names only
  B's commits and those reverts; `git diff --quiet integration/wordstat-cli...feat/wordstat-cli/F2-top-words-cli`
  exits 0; `git merge-base --is-ancestor feat/wordstat-cli/F2-top-words-cli integration/wordstat-cli` fails.
- Task commits: the two commands of "Manual run" with `wordstat-cli` in place of `todo-cli`, after A2 and after A3
  (`night-A2.trailers`, `night-A2.paths`, …): every task commit in `integration/wordstat-cli` names a model.

## Record (amends P21 "Record")

Task Q rewrites `docs/rehearsals/end-to-end-manual.md`, task R `docs/rehearsals/end-to-end-autonomous.md`, as new
records of the new runs. "Setup" shows the scratch-first order and, for R, the new hook and its probe; "Runs" keeps
P9's per-call lines plus the usage test result; "Results" has one row per expectation of P9, P21 and this file, and
Q's comparison table has the two new columns. No real path, user name, time zone or reset time in the record.

## Limits

- The usage stop cannot be avoided by the task: wave 7 should start in a fresh Claude usage window with no other
  Claude work running (the second runs reported about 4.2 USD together before base M4 stopped).
- The watch and its limits are P21's. The rule "files of the run in scratch" is followed by the task, not checked by a
  command; the record states where every file of the run was created.
- Costs and caps as P9: Q stops starting calls at 20 USD, R at 25 USD.

## Acceptance tests

1. Each record has the six sections; P0, the watch and (R) the six probe steps have a result; every expectation of
   P9, P21 and this file is Pass, Finding, Not run or Not run (usage limit), with evidence.
2. Task Q: the comparison table covers M2–M5 for `cur` and `base` with the two new columns; every call has an exit
   code and a usage test result; the last two report lines of M2 and M4 are quoted for both sides.
3. Task Q: the `.trailers` of `cur` after M4 show a model on every task commit, or the record shows the `below tier`
   entry; `base` differences in scope or trailers are marked `intended (P18)` / `intended (P23)`.
4. Task R: F2 blocked by an entry naming `stray.txt`, the reverts, the empty `Merged` cells of F2 and F4 after A3,
   `status_check.py` exit 0 at A3 and the trailers of every task commit in `integration/wordstat-cli` are each shown
   with evidence.
5. The record says where each file of the run was created, and every one is under `<scratch>` (or the record names the
   exception as a finding).
6. The check command of the wave file is green; the working folder's refs are unchanged except the task's own branch.
