# History

## Re-plan 2026-11-18 at 02d9c4a

- Input: open entries I1–I4 of wave 1 (tasks B and C). Wave 1 ❌ stopped `plan-defect`, wave 2 not run, no wave 🔄.
  `main` (71d1161) merged into the tracking branch first (02d9c4a); it brought no file change to the plan folder.
- Checked on `feat/flow-modes-p4/F1-flow-docs-and-checks` at 6a2931a (A, C, D merged): 32 status-check tests and 59
  driver tests OK, examples 01 and 02 pass, `git diff --check` clean. So wave 3 starts with no known failures.
- I4 confirmed as a plan error, not a code defect: example 01's header is title, blank, `- Plan:`, `- Re-plans:`, so a
  line inserted after `- Re-plans:` is line 5. A scratch copy on 6a2931a gives exit 1 and exactly one
  `README.md:5: flow-line` line. Closed as won't fix in wave 1's "Closed problems"; task C ✅. P8's acceptance test 3
  (example 03, line 5) was already right.
- I1 confirmed: pytest exits 5 when it collects nothing; F3 of example 03 adds only `README.md` and is under manual
  review, so its branch never gets tests; `wave-run` step 3 also runs the check on the new F1 and F3 branches of the
  seed. P17 makes the example's check `if [ -d tests ]; then python -m pytest -q; else echo "no tests yet"; fi`.
- I2 accepted from setuptools' flat-layout discovery (`plans` is a valid identifier and not on its exclude list); not
  reproduced here because no setuptools is installed offline. P17 lists the package explicitly; task H builds the
  wheel with and without the list in a scratch repository.
- I3: slug `wordstat-cli`. Unlike I3's proposal, the target follows the slug (`integration/wordstat-cli`), because
  `wave-plan` writes `integration/<slug>` for a raw-list plan. `solutions/P9-end-to-end-runs.md` was updated in place
  (paths only, and task E → I, F → J); P8 section B got a pointer to P17.
- Task B never wrote a file (it stopped before edits), so it is ➖ superseded by G, which reads P8 section B plus P17.
  `examples/README.md` moved from B to the new low task H, which also runs the closing checks of F1 (P8 tests 1–6,
  P17 tests 1–6) and pairs with G, so wave 3 is not a solo wave.
- Wave 2 (E, F) depends on `F1 merged`, which now needs wave 3; a re-plan appends waves, so wave 2 is ➖ dropped and
  rebuilt as wave 4 with the same prompts: E → I, F → J, new example paths and section names.
- I1–I3 stay open with `→` wave 3 tasks; wave 1 stays ⚠️ until wave 3 closes them. F1 is 🔄 (no task ⚠️ or ❌ left).

## Re-plan 2026-11-18 at 1e7214e

- Input: open entries I5–I9 of wave 4 (tasks I and J). Wave 4 ⚠️, no wave 🔄. `main` (6a8bc07, F1 merged) was merged
  into the tracking branch first (1e7214e).
- Checked on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 1635ef1: 32 status-check tests and 59 driver tests OK,
  all three examples pass `status_check.py`, `git diff --check` clean. Wave 5 starts with no known failures.
- I5 confirmed in the fixture, not in the skills: P3 of example 01 asks for a session that adds two tasks, its check
  and task C's prompt require every output to be a row of the P2 table, which shows only the first task. Both `cur`
  and `base` copy the fixture from the working folder, so fixing it (P20) keeps the comparison fair.
- I6: the scratch venv was only on the launcher's `PATH`; nested Bash resolved the global Python. The `C:/tmp/...`
  directories match `MSYS_NO_PATHCONV=1` being inherited by nested shells, so a native Python got `/tmp/...`
  unconverted. P21 uses `CLAUDE_ENV_FILE` (sourced before every Bash command) and a preflight; a probe of it from
  this session was refused by the permission classifier, so the preflight is the first real test.
- I7 has no cause of its own: the launcher ran the chain as one script and was stopped after M5. P21 runs one call per
  shell command and writes each exit code at once.
- I8 confirmed at three places of the prose (`SKILL.md` header "commit all your changes", step 5's net-diff scope
  check, no scope condition in auto-approval) → P18. Test path: a post-commit hook in the scratch repository forces
  `stray.txt` into task B's first commit (task O).
- I9: the `merge.md` "Record" does not say that other rows stay, and `status_check.py` checks `Merged` only for
  merged features → P19 (rule `merged-fields` extended, one test).
- Tasks I and J are ➖ superseded by N and O, which rewrite the same records. All five entries stay open with `→`
  tasks of waves 5 and 6; wave 4 stays ⚠️ until wave 6 closes them. F2 is 🔄, waiting for wave 5. All fixes are F2
  tasks: the entries block F2, and F2's records are only meaningful with the fixes in place.

## Re-plan 2026-11-18 at e3cf9f7

- Input: open entries I7, I8 (wave 4) and I12–I17 (wave 6, tasks N and O). Wave 6 ⚠️, no wave 🔄. `main` (8c69f63, the
  merge of the second re-plan, no file change) was merged into the tracking branch first (e3cf9f7).
- Checked on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 30dc1db: 33 status-check tests and 59 driver tests OK, all
  three examples pass `status_check.py`, `git diff --check` clean. Wave 7 starts with no known failures.
- I12 and I7: base M4 ended at Claude's 5-hour usage message; cur had run its whole chain first, so nothing after M3 is
  comparable. P22 makes a usage limit a recorded `Not run (usage limit)` and interleaves `cur` and `base` step by step.
- I13 confirmed as a plan error (closed in wave 6's "Closed problems"), like I4: `layout.md` "Run times" puts the timing
  line last, and both versions did so.
- I14: `v2.12.0` cleaning up task A's bytecode is the behaviour P18 replaced; the third run marks such a difference
  `intended (P18)`. It stays open until that record exists.
- I15 confirmed with git here: `-m x -m "Wave-Model: m" -m "Co-Authored-By: …"` gives an empty
  `%(trailers:key=Wave-Model,valueonly)`; the same two trailers in one paragraph give `m`. The `Co-Authored-By`
  paragraph comes from Claude Code's commit attribution. The header allowed it, and step 5 did not name the git command
  that `layout.md` gives → P23 (low, task P).
- I16: instead of injecting after the executor's last amend (no hook point for that in git), the hook now fires on every
  commit of task B whose parent lacks `stray.txt`. Tried here in a throwaway repository: the first commit gets the file
  with its message unchanged; an amend that drops it gets it back; a new commit of B that deletes it is kept and the
  scope command still lists the file; another subject adds nothing; `git revert --no-edit H..HEAD` exits 0 and leaves
  no net change. P21's one-shot marker version is replaced in P22.
- I17: P22 makes `mktemp -d` the first command and every file of the run start under scratch; the watch is unchanged
  (watching the whole system temp folder would catch other processes' files).
- Tasks N and O are ➖ superseded by Q and R, which rewrite the same records. Q and R both run after P, in parallel; the
  entries stay open with `→` wave 7 tasks; waves 4 and 6 stay ⚠️ until wave 7 closes them. F2 is 🔄, waiting for wave 7.

## Re-plan 2026-11-18 at a257e9d

- Input: open entries I18–I22 (wave 7, task Q). Wave 7 ⚠️, no wave 🔄. `main` (6819ca2, the merge of the third re-plan,
  no file change) was merged into the tracking branch first (a257e9d).
- Checked on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 942c4b1: 33 status-check tests and 59 driver tests OK, all
  three examples pass `status_check.py`, `git diff --check` clean. Wave 8 starts with no known failures.
- I18 read from the scratch repositories of the run: in `cur`, task D's executor reported that `pip install -e .`
  needs F1's `pyproject.toml`, and the coordinator opened I1 and blocked F3; in `base` the executor did not report it
  and the coordinator wrote it into F3's brief. Both coordinators followed their rules; the example had a hidden
  dependency between features → P24 (low, task S). Tried here: a flat `todo/` package with a test passes under
  `python -m pytest -q` without an install, and `python -m pytest -q || [ $? -eq 5 ]` exits 0 in an empty folder.
- I20 follows from I18: `wave-run/merge.md` ("Entry points") stops `not-ready` before merging anything when a named
  feature is not `👀 review`. It stays open until the fourth run merges F1 and F3 (task U).
- I19 confirmed as a plan error (closed in wave 7's "Closed problems"): `wave-run/report.md` puts one question per
  ready feature before the timing footer, and the baseline did exactly that. P26 corrects the expectation.
- I21: the baseline's merge commits are at 21:05:26 and the archived lines say 21:08, later than the run's own
  `Finished 21:05`; `merge.md` names no source for the time → P25 (low, task T): the merge commit's committer time.
- I22: P26 makes every command after Setup run with `env.sh` sourced, the source checks included.
- Task Q is ➖ superseded by U, which rewrites the same record; R stays ✅ and its record is not rerun. F2 is 🔄,
  waiting for wave 8; wave 7 stays ⚠️ until wave 8 closes I18, I20–I22.
- To keep the README within its size goal, these lines moved here from it.

  Known test failures recorded by earlier re-plans:

  - none (`main` at a47af8a, 2026-11-18: `test_status_check.py` 20 tests OK, `python -m unittest discover -s
    scripts/tests` 59 tests OK, both examples pass `status_check.py`, `git diff --check` clean)
  - none on `feat/flow-modes-p4/F1-flow-docs-and-checks` at 6a2931a (re-plan, 2026-11-18: 32 status-check tests and 59
    driver tests OK, examples 01 and 02 pass, `git diff --check` clean); `main` at 71d1161 is green as at a47af8a
  - none on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 1635ef1 (second re-plan, 2026-11-18: 32 status-check tests and
    59 driver tests OK, all three examples pass, `git diff --check` clean); after task L, 33 status-check tests
  - none on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 30dc1db (third re-plan, 2026-11-18: 33 status-check tests and
    59 driver tests OK, all three examples pass, `git diff --check` clean)
  - none on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 942c4b1 (fourth re-plan, 2026-11-18: 33 status-check tests
    and 59 driver tests OK, all three examples pass, `git diff --check` clean)

  Assumptions about F1 (merged) and the earlier waves:

  - P8 is one feature: the changelog line names the Flow checks and example 03, and the README links the example, so
    none of the four edits is complete on `main` without the others.
  - `status_check.py` requires the exact `Flow:` form that `wave-plan` and the flow form write, because
    `layout.md` finds the plans of a target with `git grep` on that form; the driver keeps its own parser.
  - The release archive gains `scripts/` (one word in `.github/workflows/release.yml`), so a release ships the driver
    that its README documents; plugin installs already get the whole repository.
  - Example 03 is runnable, not only illustrative: task J of wave 4 runs it in a scratch repository; its fictional
    dates and hashes stay fictional.
  - Example 03's target is `integration/wordstat-cli`, not the `integration/wordstat` of I3's proposal: `wave-plan`
    names the target of a raw-list plan after its slug, and the example must look as `wave-plan` writes it.
  - The re-plan's new solution is P17, above every P number of the index's plans (plan 2 uses up to P16).
  - Wave 4 depends on `F1 merged`: task J runs example 03 and the new check, which reach I and J's branch only through
    `main`. Review F1 after wave 3.
  - I13 and I14 are errors of the expectations, not of the skills: the timing line is last by `layout.md`, and
    `v2.12.0`'s cleanup commit is what P18 replaced. I13 is closed; I14 stays open until the third run marks it intended.

## Re-plan 2026-11-19 at 5f4bbc3

- Input: open entries I20, I21 (wave 7) and I23 (wave 8, task U). Wave 8 ⚠️, no wave 🔄. `main` (11d24b5, the merge of
  the fourth re-plan, no file change) was merged into the tracking branch first (5f4bbc3).
- Checked on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 6aece72: 33 status-check tests and 59 driver tests OK, all
  three examples pass `status_check.py`, `git diff --check` clean. Wave 9 starts with no known failures.
- I23 is a usage stop, not a defect: `cur-M5` exited 1 with the 5-hour limit message after 8 turns and changed no ref;
  no later call started, as P22 says. Task U's scratch folder is still on the machine; both repositories are exactly
  at their M4 snapshots (refs, worktrees, clean main checkouts, installed skills equal to F2's `skills/` and to
  `v2.12.0`'s). So P27 continues the run from M4 instead of a fifth full run (about 3 USD and most of a usage window
  just to reach the same state, with the same risk of a stop).
- Read from the scratch repositories: `cur`'s M3 `Merged` line (22:11) equals its merge commit's time; `base`'s says
  22:15 for a commit at 22:14. P27 records this before M5 deletes the tracking branch, so I21 is verified on `cur` even
  if M5 stops again.
- I20, I21 and I23 → task V (wave 9). U stays ⚠️ I23: V completes U's record, it does not replace it. Wave 7 stays ⚠️
  until V closes I20 and I21. F2 is 🔄, waiting for wave 9.
- Wave 9 has one medium task, an exception to "no solo medium wave": nothing else in the plan is open, and the
  continuation's steps share one record file and one scratch state, so no split gives tasks with disjoint files.
- To keep the README within its size goal, these assumptions moved here from it:

  - The forced red is a test that skips until `wordstat/export.py` exists, so the run reaches wave 2 and only F4 turns
    red; F4 staying ⚠️ after the night, after the user's merge and after a second dry run of the driver is "the
    feature that must stay blocked".
  - I8's fix enforces the existing rule (entry, revert, blocked feature) instead of letting the coordinator delete
    generated files: a cleanup commit hides history from the review. The cause, `git add -A` in a project without a
    `.gitignore`, is closed in the task header; auto-approval gets the same scope test as a second gate.
  - The forced out-of-scope edit is a git hook in the scratch repository, not a prompt instruction an executor may
    refuse; since wave 7 it re-adds `stray.txt` to every commit of task B whose parent lacks it (B amended away P21's
    one-shot version, I16). `CLAUDE_ENV_FILE` isolation passed P0 in both second runs.
  - Known test failures: none on `feat/flow-modes-p4/F2-end-to-end-rehearsal` at 942c4b1 (fourth re-plan, 2026-11-18:
    33 status-check tests and 59 driver tests OK, all three examples pass, `git diff --check` clean).
