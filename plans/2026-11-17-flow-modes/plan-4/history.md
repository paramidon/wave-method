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
