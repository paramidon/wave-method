# P27. Continue the fourth manual run from its preserved M4 state

User problem: (re-plan, I23) Claude Code's 5-hour usage limit stopped task U's manual rehearsal at `cur-M5`, before
`main` changed, so the merge of F1 and F3 (I20), the merge times against git (I21), the archive and the 11 tests were
never seen on either side. Run the remaining steps from the state U left, in a fresh usage window, and complete the
record · feature F2

This file amends `solutions/P26-fourth-manual-run.md`, which amends P22, P21 and P9. Everything P26 says about M5, M6,
the merge times, the comparison table and the record holds unless a section below replaces it. Task V reads P26
("Manual run (task U)", "Record", "Limits", "Acceptance tests"), then this file. P26's Setup, seeding, P0 and M0–M4
are not repeated.

## Cause

- The usage stop worked as P22 says: `cur-M5` exited 1 with the limit message after 8 turns, changed no ref, and no
  later `claude` call started. Nothing in the skills failed; the run lacked usage, not a fix.
- The scratch folder of task U is still on the machine that ran wave 8, and its state is exactly the M4 state
  (checked at this re-plan, 2026-11-19): in both repositories the live `git for-each-ref` equals
  `logs/<repo>-M4.after.refs` (for `cur` also `cur-M5.after.refs`), the live `git worktree list --porcelain` equals
  `logs/<repo>-M4.after.worktrees`, `main` is `cb90eaa` (`cur`) and `382347a` (`base`), `plan/todo-cli` is `c5b96db`
  (`cur`) and `3df09db` (`base`), the main checkouts are clean (only untracked `__pycache__` folders in the F1
  worktrees), the installed skills of `cur` equal `skills/` of F2's branch at `6aece72` and those of `base` equal
  `<scratch>/v2120/skills`.
- Already visible at M3, without any new call: `cur`'s wave 1 line `Merged 2026-11-18 22:11: F2-usage-readme e1cdad7`
  has the time of commit `e1cdad7` (22:11); `base`'s line says 22:15 for commit `591b296` at 22:14. So P25 already
  shows on the M3 merge, and P26 only checked M5.

## Approach

1. **Continue, do not restart.** Every step is a separate headless session whose only input is the repository state,
   so M5 on the preserved M4 state is the same experiment as M5 right after M4. A full fifth run would repeat
   P0–M4 (about 3 USD and most of a usage window) to reach the same state, and could stop at the limit again.
2. **Prove the state first.** No `claude` call starts unless the state check below passes; a lost or changed state is
   a procedure stop, not a finding, and a later re-plan decides about a full run.
3. **Keep the stopped attempt.** Its files move to `logs/limit-stop/` unchanged, so the new step files can use the
   same names and the evidence of the usage stop stays.
4. **A fresh watch stamp.** The watch of P21 lists files newer than `logs/start.stamp`; after a night, other programs
   may have written there. The continuation's watch uses a new stamp made right before its first call.
5. **M3 merge times now.** Both repositories still have `plan/todo-cli`, so the M3 `Merged` line is checked against
   git before M5 archives the plan. This verifies I21 on `cur` even if M5 stops again.

## Scratch folder

The folder is `tmp.10B4rFz0kw` in the system temp folder of the machine that ran wave 8 (Git Bash `/tmp`):

```bash
scratch="$(dirname "$(mktemp -u)")/tmp.10B4rFz0kw"
. "$scratch/env.sh"
export CLAUDE_ENV_FILE="$(cygpath -m "$scratch")/env.sh"
export scratch working="$(pwd)"
```

`working` is the task's working folder (the shell starts there). Only the first line runs before `env.sh` is
sourced. Every later command of the task, the check command included, runs in a shell that ran these four lines.
The record writes `<scratch>` and `<working folder>`, never the real paths.

## State check (before any call)

All of these hold, otherwise stop with `state lost: <the failed item>` before moving any file and before any `claude`
call:

```bash
for repo in cur base; do
  diff <(git -C "$scratch/$repo" for-each-ref --format='%(refname) %(objectname)') "$scratch/logs/$repo-M4.after.refs"
  diff <(git -C "$scratch/$repo" worktree list --porcelain) "$scratch/logs/$repo-M4.after.worktrees"
  test -z "$(git -C "$scratch/$repo" status --porcelain)"
done
diff -rq -x __pycache__ "$scratch/cur/.claude/skills" "$working/skills"
diff -rq -x __pycache__ "$scratch/base/.claude/skills" "$scratch/v2120/skills"
test -f "$scratch/launch/call.sh" && test ! -e "$scratch/logs/base-M5.jsonl" && test ! -e "$scratch/logs/limit-stop"
```

Every `diff` prints nothing and every `test` exits 0. Save the output of the whole block, with its exit codes, as
`$scratch/logs/continue-state.txt`. A difference in `skills` means the working folder no longer carries the skills
that ran M0–M4 (for example, `main` brought a skill change into F2's branch): stop, do not reinstall.

## Continuation steps

One shell command per item, in this order; after each, read its result before the next.

1. Keep the stopped attempt and start the new watch:

   ```bash
   mkdir "$scratch/logs/limit-stop"
   mv "$scratch/logs"/cur-M5.* "$scratch/logs"/cur-M6-pytest.main-tree "$scratch/logs"/base-M6-pytest.main-tree \
     "$scratch/logs/limit-stop/"
   sed 's/start\.stamp/continue.stamp/' "$scratch/launch/call.sh" > "$scratch/launch/continue.sh"
   diff "$scratch/launch/call.sh" "$scratch/launch/continue.sh" > "$scratch/logs/continue-launcher.diff"
   touch "$scratch/logs/continue.stamp"
   git -C "$working" for-each-ref --format='%(refname) %(objectname)' > "$scratch/logs/working-before-continue.refs"
   claude --version > "$scratch/logs/claude-version-continue.txt"
   ```

   `continue-launcher.diff` shows exactly the one changed watch line. Read `continue.sh` whole before the first call:
   it is the launcher that ran M0–M4 (P21's call form, P22's usage test, the snapshots, the watch, `.main-commits`,
   `.nonmerges`, the tracking README and problems after M5), and it exits 72 after a non-empty watch and 73 after a
   usage match.
2. M3 merge times, both repositories (no `claude`):

   ```bash
   for repo in cur base; do
     git -C "$scratch/$repo" show plan/todo-cli:plans/2026-11-02-todo-cli/waves/w01.md | grep -E '^Merged ' \
       > "$scratch/logs/$repo-M3.merged-lines"
     while read -r _ day hm id hash _; do
       at=$(git -C "$scratch/$repo" log -1 --format=%cd --date=format:'%Y-%m-%d %H:%M' "$hash")
       printf '%s line=%s %s commit=%s\n' "$id" "$day" "${hm%:}" "$at"
     done < "$scratch/logs/$repo-M3.merged-lines" > "$scratch/logs/$repo-M3.merge-times"
   done
   ```

   Expected: `cur-M3.merge-times` is one line `F2-usage-readme line=2026-11-18 22:11 commit=2026-11-18 22:11` (equal
   times, P25); `base-M3.merge-times` is recorded (`22:15` against `22:14`), a difference `intended (P25)`.
3. `bash "$scratch/launch/continue.sh" cur M5; echo "launcher $?"`
4. `bash "$scratch/launch/continue.sh" base M5; echo "launcher $?"`
5. After M5, in both repositories: P26's "Merge times" block (`<repo>-M5.merged-lines`, `<repo>-M5.merge-times`), and

   ```bash
   git -C "$scratch/$repo" show main:plans/archive/2026-11-02-todo-cli/README.md \
     > "$scratch/logs/$repo-M5.archive-readme"
   ```
6. `bash "$scratch/launch/continue.sh" cur M6-pytest`, then the same for `base`.
7. `bash "$scratch/launch/continue.sh" cur M6`, then the same for `base`.
8. `git -C "$working" for-each-ref --format='%(refname) %(objectname)' > "$scratch/logs/working-after-continue.refs"`

Launcher exit 73 is a usage stop (P22 "Usage stop"): no later `claude` call, the pytest steps still run when `main`
has the tests. Exit 72 is a non-empty watch: stop the run there, as P21 says. Before each `claude` call add the
`total_cost_usd` of the last `result` event of every `.jsonl` in `logs/` and `logs/limit-stop/` (the record's
3.20962390 USD plus the new calls); at 20 USD start no further call.

Expectations of M5 and M6 are P26's, unchanged: no stop line, `main` gains the F1 merge, the F3 merge and the
tracking status merge, `.nonmerges` is empty, the plan is under `plans/archive/2026-11-02-todo-cli/` on both sides,
`cur-M5.merge-times` has two lines (F1, F3) with equal times, `base` times recorded (`intended (P25)` when they
differ), `pytest -q` on `main` gives `11 passed` on both, `/wave-status` reports no active plan and names the
archived one. Statuses after M5 come from `<repo>-M5.archive-readme`, because the tracking branch is gone.

## Record (amends P26 "Record")

Task V edits `docs/rehearsals/end-to-end-manual.md`; it does not rewrite M0–M4:

- Title block: append `· continued 2026-11-19 from M4` (the actual date) after the source, and the Claude Code
  version of the continuation if it differs from 2.1.326.
- "Setup": one new closing paragraph "Continuation": why (the usage stop at `cur-M5`), the state check and its result
  (`continue-state.txt`), the stopped attempt's files in `<scratch>/logs/limit-stop/`, the new stamp and launcher
  (`continue-launcher.diff`), and that only `scratch=` ran before `env.sh`.
- "Runs": the sections `cur-M5` through `base-M6` are replaced by the new runs, in the format of the earlier sections
  (command, exit, usage test, model, turns, `total_cost_usd`, minutes, first and last non-empty line, stop line,
  watch, snapshots, `main` before and after, Pass or Finding). `cur-M5` keeps one line naming the stopped attempt and
  its files under `limit-stop/`. The last non-empty lines of `cur-M5` and `base-M5` are quoted.
- "Results": the rows that say `Not run (usage limit)` or `Not run` for M5 and M6 get their result; new rows
  `cur-M3 I21 Merged line time equals its merge commit` (Pass or Finding), `base-M3 I21 baseline Merged line time
  recorded` and `I23 continuation from the preserved M4 state` (the state check); the cost sentence gives the new
  total; the working-refs row names both snapshot pairs. Rows of I20, I21 and I23 name their entry.
- Comparison table: rows `cur-M5` and `base-M5` filled with P22's and P26's columns. The column `Merged line times vs
  merge commits` now also has a value on the M3 rows (`equal`, or the two times with `intended (P25)` on `base`); this
  replaces P26's "other rows: `No merge`" for M3.
- "Not verified": the usage-stop items leave; anything still not run stays with its reason.
- "Repeat": one paragraph "Resume after a usage stop": the state check, moving the stopped step's files, the new stamp,
  then the remaining calls in order.

No real path, user name, time zone or reset time in the record (the limit message keeps `<reset>`).

## Limits

- The continuation needs the machine and user account that ran wave 8: the scratch folder is not in git. If the
  folder is gone (a temp cleanup, another machine), the state check fails and the task stops; no partial rebuild.
- The usage stop can repeat. Start wave 9 in a fresh usage window with no other Claude work running: the remaining
  calls are two merges (at most 3 USD each) and two status calls (at most 0.5 USD each).
- The installed skills are those of M0–M4; the state check proves they still equal the working folder's `skills/`.

## Acceptance tests

1. `continue-state.txt` shows every item of the state check passing; `continue-launcher.diff` shows only the watch
   line changed; the stopped attempt's files are in `logs/limit-stop/` and the record names them.
2. `cur-M3.merge-times` shows equal times on its F2 line; `base-M3.merge-times` is recorded and the record marks a
   difference `intended (P25)`.
3. M5 on both sides: launcher exit 0, no usage match, no stop line, F1 and F3 merged with their hashes in
   `<repo>-M5.archive-readme`, plan archived, `.nonmerges` empty; `cur-M5.merge-times` has two lines with equal times
   (I20, I21), or each difference is a Finding with evidence.
4. M6 on both sides: `11 passed` in `<repo>-M6-pytest.txt`; `/wave-status` names the archived plan and no active
   plan; or each difference is a Finding with evidence.
5. The record keeps P26's six sections; its M0–M4 run sections are unchanged (`git diff` of the record touches only
   the title line, Setup's new paragraph, the `cur-M5`–`base-M6` sections, "Results", the M3 and M5 rows of the
   comparison table, "Not verified" and "Repeat"); no `Not run (usage limit)` row is left unless a new usage stop
   happened, and then it names the step.
6. `working-before-continue.refs` and `working-after-continue.refs` are equal except the task's own branch; every
   new `.outside` file is empty; the check command is green in a shell that ran the four lines of "Scratch folder".
