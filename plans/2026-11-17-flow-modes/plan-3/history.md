# History

## Re-plan 2026-11-18 (at 790870a): I1

Wave 1 stopped `red-before-wave` at `wave-run` step 3, before any task launched: the check command of wave 1 runs
`python -m unittest discover -s scripts/tests -v`, and `scripts/tests/` does not exist on F1's branch until tasks
A–D create it (`ImportError: Start directory is not importable`). F1's head stayed at 790870a; no task branch or
task worktree was created.

- The defect is in the plan's check, not in the code, so the fix is a plan edit: wave 1 gets a baseline check
  (status tests and `git diff --check`) for F1's branch while no task of the wave is merged; the full check stays the
  check of every task and of F1 after each task merge. Verified on F1's branch at 790870a: 20 tests OK, diff check
  clean. I1 is closed by that verification and moved to wave 1's "Closed problems".
- Not taken: an empty `scripts/tests/` (git keeps no empty folder, and on Python 3.12+ discovery of a folder without
  tests exits 5, `NO TESTS RAN`, measured on Python 3.14.6); a placeholder test on F1's branch (a code change, and a
  task in an earlier wave would be needed); dropping wave 1 and moving A–D to a new wave 4 (waves 2 and 3 would then
  have to move too, because `wave-run` refuses a wave while an earlier one is ⬜ or ❌, and every prompt and solution
  section names tasks A–H).
- Wave 1 changes only in its check section; its prompts, tasks and files stay as they are. The wave stays ❌ with a
  re-run note; tasks A–D go back to ⬜, since none of them started; F1 is 🔄 in progress, waiting for wave 1.
- Waves 2 and 3 are unchanged: F1's branch holds `scripts/tests/` with tests after wave 1, so their check runs as
  written.
