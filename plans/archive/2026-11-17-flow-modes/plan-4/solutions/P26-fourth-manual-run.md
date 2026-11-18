# P26. Fourth run of the manual rehearsal

User problem: (re-plan, I18–I22) the third manual run diverged at M4 because example 01's CI feature needed a file of
F1 (I18), so the current version never merged F1 and F3 and never archived the plan (I20); it judged the M4 report
against a wrong expectation (I19); the `v2.12.0` archive showed merge times that no merge commit has (I21); and the
early source checks wrote test fixtures to the host's temp folder (I22). Run the manual rehearsal again with the
fixed example and the merge-time rule · feature F2

This file amends `solutions/P22-third-rehearsal-run.md`, which amends `solutions/P21-rehearsal-isolation-rerun.md`,
which amends `solutions/P9-end-to-end-runs.md`. Everything in P9, P21 and P22 for the manual run holds unless a
section below replaces it. Task U reads P9, then P21, then P22, then this file. The autonomous run is not repeated:
task R's record stays (it met every expectation).

## Cause

- **I18, I20.** Example 01 had a hidden dependency between features: P4's workflow ran `pip install -e . pytest`, and
  only F1 adds `pyproject.toml`. In the current run task D's executor reported it, the coordinator opened an entry
  and blocked F3; in the `v2.12.0` run the executor did not, and the coordinator noted it in the review brief. Which
  executor reports a real defect is chance, so the comparison diverged on the fixture, not on the skills. The
  combined approval `merge F1 F3` then stopped `not-ready` before merging anything, as `wave-run/merge.md` ("Entry
  points") says for a named feature that is not `👀 review`: I20 is a consequence of I18. Fixed by P24 (task S).
- **I19.** P22 expected one line asking about F1 and F3. `wave-run/report.md` asks one question per feature in
  review, each on its own line before the timing footer, and the baseline did exactly that: a plan error, closed at
  this re-plan.
- **I21.** The baseline's archived wave 2 says `Merged 2026-11-18 21:08` for F1 and F3, while both merge commits are
  at 21:05 and the run finished at 21:05: the coordinator wrote a time that it did not read. `merge.md` gives no source
  for that time. Fixed by P25 (task T): the time comes from the merge commit.
- **I22.** Task Q ran its first source checks in a shell that had not sourced `$scratch/env.sh`, so pytest's fixtures
  went to the host's temp folder; only the final check ran with the scratch temp folder.

## Approach

1. The fixture loses its hidden dependency (P24), so both versions see the same, correct plan and M4 and M5 are
   comparable again.
2. The report expectation follows `wave-run/report.md`: one merge question per ready feature.
3. The current version's `Merged` lines are checked against `git log`; the baseline's are recorded, and a difference
   is intended (P25).
4. Every command of the task runs with the scratch environment, the source checks included.

## Files of the run (amends P22 "Files of the run")

P22's rule stands, plus: every command of the task after the Setup block — each step, each evidence command and
every run of the wave's check command in the working folder, a preliminary one included — runs in a shell that has
sourced `$scratch/env.sh`, so Python, pip, pytest and their temporary files resolve under `$scratch`. Only
`scratch=$(mktemp -d)` and the Setup block's own lines run before `env.sh` exists. Before the record is committed,
run the check command once more in such a shell and keep its output in `$scratch/logs/final-check-*.txt`. The record
lists every command that ran without `env.sh` (expected: only Setup's lines) and where every file of the run was
created.

## Manual run (task U)

Setup, seeding, P0, the order of calls, the usage stop, the snapshots, the watch, the task-commit evidence after M2
and M4 and the cost cap are P22's ("Manual run (task Q)", "Usage stop"). Both `cur` and `base` are seeded from the
working folder's `examples/01-greenfield-todo-cli`, which now carries P24.

**Report lines (replaces P22 "Report lines").** The last non-empty line of the last result is the
`Started: … · Finished: …` line. The non-empty lines right before it are the merge questions of
`wave-run/report.md` (`Merge F<k> "<title>" — … ? Answer: merge F<k> · later · problems F<k>: …`), one per feature in
`👀 review`, in feature ID order, with no other line between them: M2 → F2; M4 → F1, then F3. Both `cur` and `base`.
Quote the question lines and the footer of both sides.

**M4 (replaces P9's M4 expectation where it differs).** In both repositories: wave 2 ✅, tasks B and D ✅, F1 and F3
`👀 review`, `problems.md` on `plan/todo-cli` without an open entry, `main` unchanged. Evidence after M4, in both:

```bash
git -C "$scratch/$repo" show feat/todo-cli/F3-ci-tests:.github/workflows/test.yml > "$scratch/logs/$repo-M4.workflow"
grep -c -e '-e \.' -e 'pyproject' "$scratch/logs/$repo-M4.workflow" > "$scratch/logs/$repo-M4.workflow-deps"
mkdir "$scratch/$repo-F3-alone"
git -C "$scratch/$repo" archive feat/todo-cli/F3-ci-tests | tar -x -C "$scratch/$repo-F3-alone"
(cd "$scratch/$repo-F3-alone" && bash -c 'python -m pytest -q || [ $? -eq 5 ]') \
  > "$scratch/logs/$repo-M4.ci-alone" 2>&1; echo $? > "$scratch/logs/$repo-M4.ci-alone.exit"
```

`.workflow-deps` is `0` and `.ci-alone.exit` is `0` (F3's branch alone passes its own test command). An entry that
still ties F3 to F1 is a Finding naming the entry.

**M5 (replaces P9's M5 expectation where it differs).** `merge F1 F3` merges both features in both repositories, with
no stop line: `main` gains the F1 merge, the F3 merge and the tracking status merge, `git rev-list --no-merges
--first-parent <before>..main` is empty, and the plan is archived under `plans/archive/2026-11-02-todo-cli/`.

**Merge times (new, after M5, both repositories):**

```bash
git -C "$scratch/$repo" show main:plans/archive/2026-11-02-todo-cli/waves/w02.md | grep -E '^Merged ' \
  > "$scratch/logs/$repo-M5.merged-lines"
while read -r _ day hm id hash _; do
  at=$(git -C "$scratch/$repo" log -1 --format=%cd --date=format:'%Y-%m-%d %H:%M' "$hash")
  printf '%s line=%s %s commit=%s\n' "$id" "$day" "${hm%:}" "$at"
done < "$scratch/logs/$repo-M5.merged-lines" > "$scratch/logs/$repo-M5.merge-times"
```

- `cur`: two lines, F1 and F3, and on each the `line=` time equals the `commit=` time (P25). Otherwise a Finding.
- `base`: recorded, not judged. A difference is `intended (P25)`, never "manual flow differs from v2.12.0".
- The plan not archived → `Not run` with the reason, and the M5 expectation above is the Finding.

**M6.** `cur` and `base`: `pytest -q` on `main` gives `11 passed`; `/wave-status` reports no active plan and names the
archived one.

**Comparison table.** P22's columns plus one: `Merged line times vs merge commits` (M5 rows: `equal`, or the two
times; other rows: `No merge`). A difference marked `intended (P18)`, `intended (P23)` or `intended (P25)` is not a
finding; every other cell difference is a finding "manual flow differs from v2.12.0", as P9 says.

## Record (amends P22 "Record")

Task U rewrites `docs/rehearsals/end-to-end-manual.md` as the record of the new run, six sections as before. "Results"
has one row per expectation of P9's manual run, P21, P22 and this file; the rows of I18–I22 name the entry they verify
(`I18`, `I19`, …). "Setup" says which commands ran before `env.sh` existed. No real path, user name, time zone or reset
time in the record.

## Limits

- Costs and the usage stop as P22: stop starting calls at 20 USD; start the wave in a fresh usage window (the third
  run cost about 2.9 USD).
- The workflow is not run on GitHub; `.ci-alone` runs its test command locally on F3's tree, which is what CI would
  run.
- P25 also changes the autonomous flow's `Merged` lines (`autonomous.md` refers to `merge.md`); no autonomous run
  repeats here, so that path is shown only by the shared rule.

## Acceptance tests

1. The record has the six sections; P0 and the watch have a result; every expectation of P9's manual run, P21, P22
   and this file is Pass, Finding, Not run or Not run (usage limit), with evidence (log file, commit hash or quoted
   line).
2. The comparison table covers M2–M5 for `cur` and `base` with P22's columns and the new one; every call has an exit
   code and a usage test result; the question lines and the footer of M2 and M4 are quoted for both sides.
3. M4: both sides have F1 and F3 in `👀 review` and no open entry, `.workflow-deps` is `0` and `.ci-alone.exit` is `0`
   on both (or each difference is a Finding with its evidence).
4. M5–M6: both sides merged F1 and F3 and archived the plan; `cur-M5.merge-times` shows equal times on both lines;
   `pytest` gives 11 passed on both `main` branches (or each difference is a Finding with its evidence).
5. The record says where each file of the run was created and which commands ran before `env.sh`; every file is under
   `<scratch>` (or the record names the exception as a finding).
6. The check command of the wave file is green; the working folder's refs are unchanged except the task's own branch.
