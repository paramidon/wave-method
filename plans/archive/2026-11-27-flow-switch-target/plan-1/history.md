# History

## Re-plan 2026-11-27 at 638bcc5 (round 1 for F2)

- Input: open entry I4 of wave 1 / task C. Wave 1 ⚠️ I4, wave 2 not run, no wave 🔄. F1 was merged into `main`
  (`c2fed10`); `main` (`3ba0015`) was merged into the tracking branch first (`638bcc5`).
- I4 confirmed against `skills/wave-auto/navigator.md` on F2's branch at `c74bf9c`: step 3.1 (line 61) promises that
  "the next reading" prints a held-back `halt`; step 3.2 (lines 72–73) ends the reading at the first row that yields
  a `next:` line, so in P3 acceptance test 4 row 1 (`next: wave …/plan-1 1`) ends it before plan-2's `halt`.
- Of I4's proposal both parts were taken: the behaviour stays, the navigator's wording is corrected
  (`solutions/lite.md` P4) and P3 acceptance test 4 was rewritten in place with three readings, one with plan-1 in
  `skip`. Not chosen: printing every `halt` before the `next:` line (it changes the reading order of every index
  start, which no problem asked for).
- Checked by a probe merge of `main` into F2's branch (throwaway worktree, removed): no conflict, 43 status-check tests
  OK, examples silent, `git diff --check main...HEAD` clean. So wave 3 starts with no known failures.
- A re-plan appends waves and a lone low task cannot form one, so wave 2 was dropped and rebuilt as wave 3: D → F (the
  same prompt), E → G (the same edits plus the P4 navigator line, since G is the low task and the navigator is not a
  file of F). New slugs, because slugs stay distinct in the plan.
- I4 stays open with `→ task G (wave 3)`; task C and wave 1 stay ⚠️ I4 and F2 stays ⚠️ blocked, waiting for wave 3.
- Round: F2's first re-plan from a wave entry, so no escalation.
