# Lite solutions (low problems)

## P19. A Merged hash only on a merged feature

User problem: (re-plan, I9) approving F3 with the merge form wrote F3's merge hash `6a83b81` into the `Merged` cell of
the blocked F4 too (scratch tracking commit `ed0b8de`); the status check passed, so nothing caught it · feature F2

**Cause:** `merge.md`, "Record", says what a merged row gets but not that no other row changes, and
`status_check.py:147-153` checks the `Merged` cell only for `✅ merged` features.

**Edit:**

1. `skills/wave-plan/scripts/status_check.py`, in `check()`, the `if kind == "feature":` block: after the
   `merged-fields` report for merged features add

   ```python
                if not merged and row["Merged"]:
                    report(readme, line, "merged-fields",
                           item + " is not ✅ merged but has a Merged hash")
   ```

   (`row["Merged"]` always exists: `COLUMNS` requires the column.)
2. `skills/wave-plan/scripts/test_status_check.py`, after `test_merged_fields`, add

   ```python
       def test_merged_hash_on_unmerged(self):
           self.assert_rule("merged-fields", README.replace(
               "| F1 | ✅ merged | | abc123 |", "| F1 | 👀 review | review | abc123 |"))
   ```

3. `skills/wave-run/merge.md`, "Record", the first bullet (`README "Features": a merged feature gets …`): append
   `Change only the rows of the features this run merged, rejected or recorded, each found by its own ID cell,
   never with a replacement that can match another row; afterwards git diff of README.md changes no other row.`
   (`ID` and the command in backticks).

**Check:** `python skills/wave-plan/scripts/test_status_check.py` → 33 tests OK; the three examples still pass
`status_check.py`; a copy of `examples/03-autonomous-night-run` whose F4 row has `abc123` in `Merged` gives exit 1 and
exactly one line, ending in `README.md:<n>: merged-fields: feature F4 is not ✅ merged but has a Merged hash`.

## P20. Example 01's README session is part of its solution

User problem: (re-plan, I5) in the manual rehearsal the coordinator blocked task C of example 01 because the README's
example session prints `added 2: call Bob`, which is not a row of the P2 "Behaviour" table that the check requires
verbatim · feature F2

**Cause:** `examples/01-greenfield-todo-cli/solutions/lite.md` P3 asks for an example session that adds two tasks, but
its check (and task C's prompt in `waves/w01.md:47-51`) requires every output to appear in the P2 table, which shows
only the first task's lines. The fixture contradicts itself; any careful coordinator stops on it.

**Edit:**

1. `examples/01-greenfield-todo-cli/solutions/P2-cli-commands.md`, "Behaviour": after the `**Limits:**` line, before
   `**Acceptance tests**`, add a paragraph `**Example session** (an empty folder; the README copies it verbatim):`
   and, after a blank line, a fenced `text` block with exactly these lines, then a blank line:

   ```text
   $ todo add "buy milk"
   added 1: buy milk
   $ todo add "call Bob"
   added 2: call Bob
   $ todo list
   [ ] 1 buy milk
   [ ] 2 call Bob
   $ todo done 1
   done 1: buy milk
   $ todo list
   [x] 1 buy milk
   [ ] 2 call Bob
   ```

2. `examples/01-greenfield-todo-cli/solutions/lite.md`, P3: `an example session (add two tasks, list, done 1, list)`
   → `the example session of solutions/P2-cli-commands.md, "Example session", verbatim`; its **Check:** becomes
   `every command and output in the README appears verbatim in the P2 "Behaviour" table or in its "Example session"
   block.` (path in backticks).
3. `examples/01-greenfield-todo-cli/waves/w01.md`, task C's prompt: `section "Behaviour", of the plan folder` →
   `sections "Behaviour" and "Example session", of the plan folder`; `copy commands and outputs from the P2 table
   verbatim.` → `copy the commands and outputs of the P2 table and the example session verbatim.`; its `Check:` line
   → `Check: every command and output in README.md appears in the P2 "Behaviour" table or in its "Example session"
   block; Markdown renders (a blank line before and after every code block and table).` Keep the prompt's line
   width under 120 characters.
4. `skills/wave-plan/CHANGELOG.md`, the `- Unreleased — …` item: before its last sentence `A plan without a Flow: line
   behaves as before.` insert (wrapped like the item, two-space indent):
   `Fixes from the end-to-end runs: a task adds its own files by name and never commits generated files; wave-run
   finds out-of-scope paths in every commit of a task, never cleans them up with a new commit, and auto-approval
   also needs a clean scope; status_check.py reports a Merged hash on a feature that is not ✅ merged
   (merged-fields); example 01's README session is part of its P2 solution.` (file and rule names in backticks).

**Check:** `python skills/wave-plan/scripts/status_check.py examples/01-greenfield-todo-cli` → exit 0, no output;
`git grep -n "added 2: call Bob" examples/01-greenfield-todo-cli` prints one line, in `P2-cli-commands.md`;
`git grep -n "Example session" examples/01-greenfield-todo-cli` prints the P2 heading line, the P3 lines of
`lite.md` and task C's prompt; the changelog still has exactly one `- Unreleased` line; `git diff --check` clean.

## P23. One trailer block for Wave-Model

User problem: (re-plan, I15) task D's commit `82fd76b` had `Wave-Model` in its own paragraph and Claude Code's
`Co-Authored-By` in a later one, so git read no `Wave-Model` trailer, and the coordinator accepted the low task anyway
· feature F2

**Cause:** git reads trailers only in the last paragraph of a message. The header (`skills/wave-run/SKILL.md:235`)
says "ending with a blank line and the trailer", which allows a second trailer paragraph after it; step 5's tier gate
(`SKILL.md:263`) says "read the trailer" without the git command that `layout.md` ("Tier gate") gives.

**Edit** (text in quotes is new, verbatim; keep the header block's lines under 120 characters):

1. `skills/wave-run/SKILL.md`, step 4 header: the words `ending with a blank line and the trailer
   "Wave-Model: <the exact model ID you run on>".` become
   `ending with one trailer block: a blank line, then "Wave-Model: <the exact model ID you run on>" and any other
   trailer (Co-Authored-By …) on the lines right after it, with no blank line between them.`
2. `skills/wave-run/SKILL.md`, step 5, the **Tier gate** bullet: `read the Wave-Model trailer of every non-merge
   commit of the task` → `read the Wave-Model trailer of every non-merge commit of the task with
   git log --no-merges --format="%h %(trailers:key=Wave-Model,valueonly)" <range>`, and after `(task branch: …;
   direct task: H..HEAD).` insert `A commit whose line shows no model has no trailer, even when its message shows a
   Wave-Model line outside the last paragraph.` (commands and the trailer name in backticks, as the bullet writes them).
3. `skills/wave-run/task-mode.md`: `with the trailer` + `` `Wave-Model: <exact model ID>` `` → the same followed by
   `in one trailer block with any other trailer`.
4. `skills/wave-plan/layout.md`, "Tier gate", **Record**: `ends with the trailer `Wave-Model: <exact model ID>` (after
   a blank line)` → `ends with one trailer block: a blank line, then `Wave-Model: <exact model ID>` and any other
   trailers (`Co-Authored-By: …`) with no blank line between them, because git reads trailers only in the last
   paragraph`; **Coordinator check**: after the command add `A line without a model is a missing trailer.`
5. `skills/wave-plan/CHANGELOG.md`, the `- Unreleased` item: after `(`merged-fields`);` insert
   `a task keeps `Wave-Model` in one trailer block with any other trailer, and the tier gate reads it with git;`
   (wrapped like the item, two-space indent).

**Check:** `git grep -n "one trailer block" skills` prints the lines of `SKILL.md`, `task-mode.md`, `layout.md` and the
changelog; `git grep -n "trailers:key=Wave-Model" skills/wave-run/SKILL.md` prints the step 5 line; in a scratch
repository, a commit made with `-m "x" -m "Wave-Model: m" -m "Co-Authored-By: C <c@d>"` prints nothing and one made
with the message `x`, blank line, `Wave-Model: m`, `Co-Authored-By: C <c@d>` prints `m` for
`git log -1 --format="%(trailers:key=Wave-Model,valueonly)"`; the check command of the wave file is green.

## P24. Example 01's CI needs no file of another feature

User problem: (re-plan, I18, I20) in the third manual run task D's executor reported that example 01's workflow runs
`pip install -e . pytest`, which needs the `pyproject.toml` that only F1 adds; the current coordinator opened an entry
and blocked F3, the `v2.12.0` one kept it as a review caveat, and the user's `merge F1 F3` then stopped `not-ready`
· feature F2

**Cause:** a hidden dependency between features in the example (`layout.md`: a feature must work on `main` on its
own). Whether an executor reports it is chance, so the two versions diverged on the fixture. The workflow does not
need an install: `python -m pytest` puts the checkout on `sys.path`, so the tests import `todo` (a flat package with
`todo/__init__.py`), and on F3's branch alone pytest finds no tests and exits 5. Checked here: a flat `todo/` package
with a test passes under `python -m pytest -q` without an install, and `bash -ec 'python -m pytest -q || [ $? -eq 5 ]'`
exits 0 in an empty folder.

**Edit** (text in quotes is new, verbatim; keep every line under 120 characters):

1. `examples/01-greenfield-todo-cli/solutions/lite.md`, section P4, **Edit:** the words
   ``steps `actions/checkout@v4`, `actions/setup-python@v5`, `pip install -e . pytest`, `pytest -q` `` become
   ``steps `actions/checkout@v4`, `actions/setup-python@v5`, `python -m pip install pytest`,
   `python -m pytest -q || [ $? -eq 5 ]`; no install of the project: `python -m` puts the checkout on `sys.path`, and
   exit 5 ("no tests collected") passes while F1 is not merged, so the workflow needs no file of another feature``;
   its **Check:** gains, before the final period, ``; the file contains neither `-e .` nor `pyproject` ``.
2. `examples/01-greenfield-todo-cli/waves/w02.md`, task D's prompt: `with pytest tests; it will have a
   pyproject.toml.` → `(package todo/, tests in tests/); the workflow must not need any file it does not add
   itself.` (rewrap the prompt's first lines under 120 characters); its `Check:` line → `Check: the YAML check of
   P4; the file contains "3.10" and "3.12" and neither "-e ." nor "pyproject".`
3. `examples/01-greenfield-todo-cli/README.md`: F3's "Done when" cell → `the workflow file is valid YAML, runs
   `pytest` on Python 3.10 and 3.12 and needs no file of F1`; in "Assumptions", after the bullet `P1 and P2 are one
   feature: …`, a new bullet `- F3's workflow installs only `pytest` and runs `python -m pytest` from the checkout,
   so it needs no file of F1 and can be merged before or after it; with no tests yet, pytest's exit 5 counts as a
   pass.`

**Check:** `python skills/wave-plan/scripts/status_check.py examples/01-greenfield-todo-cli` → exit 0, no output;
`git grep -n -F "pip install -e . pytest" examples` prints nothing; `git grep -n -F "it will have a pyproject" examples`
prints nothing; `git grep -n -F "python -m pip install pytest" examples/01-greenfield-todo-cli` prints the P4 line of
`lite.md`; the check command of the wave file is green.

## P25. A Merged line takes its time from the merge commit

User problem: (re-plan, I21) the `v2.12.0` archive of the third manual run says `Merged 2026-11-18 21:08` for F1 and
F3, while both merge commits are at 21:05 and the run finished at 21:05 · feature F2

**Cause:** `skills/wave-run/merge.md` ("Record", line 67) prescribes `Merged <YYYY-MM-DD HH:MM>: <feature-id> <hash>`
without saying where the time comes from, so a coordinator may write one it did not read. The merge commit already
holds the true time, and git prints it.

**Edit** (text in quotes is new, verbatim; commands and file names in backticks; keep lines under 120 characters):

1. `skills/wave-run/merge.md`, "Record", the bullet `The Execution of the wave file of the feature's last wave …`:
   after `` `Rejected <YYYY-MM-DD HH:MM>: <feature-id> → I<n>`. `` append `The time of a Merged line is the committer
   time of the commit its hash names, from git log -1 --format=%cd --date=format:"%Y-%m-%d %H:%M" <hash>, never a
   clock reading or an estimate; the time of a Rejected line is read from the clock (layout.md, "Run times").`
2. `skills/wave-run/autonomous.md`, the list after "Then `merge.md`, "Record", with these differences": after
   `` `Merged <YYYY-MM-DD HH:MM>: <feature-id> <hash> (auto-approved)` `` insert ` (its time from the merge commit, as
   in merge.md, "Record")`; after `after its `👀 review since` line` insert `, with the same time`.
3. `skills/wave-plan/CHANGELOG.md`, the `- Unreleased` item: after `and the tier gate reads it with git;` insert
   `a Merged line of a wave file takes its time from the merge commit, not from the clock; example 01's CI workflow
   needs no file of another feature;` (wrapped like the item, two-space indent, lines under 120 characters).

**Check:** `git grep -n "committer" skills/wave-run/merge.md` prints the new sentence; `git grep -n "its time from
the merge commit" skills/wave-run/autonomous.md` prints one line; the changelog's `- Unreleased` item contains the
inserted words, and the changelog still has exactly one `- Unreleased` line; in a scratch repository a commit's `git log -1 --format=%cd --date=format:"%Y-%m-%d %H:%M"`
prints its time in that form; the check command of the wave file is green.
