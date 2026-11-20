# History

## Re-plan 2026-11-20 (round 1 for F1)

- Open entry: I2 (wave 1, task B) — the step 8 "Re-plan rounds" self-check of `skills/wave-plan/SKILL.md` demands an
  `Evidence` section with a command run in the session, while `skills/wave-plan/layout.md`, "Re-plan escalation",
  step 3 allows `not verifiable by running: <why>` and the alternative check.
- Verified on `feat/replan-escalation/F1-replan-escalation` at 7c6595d: `layout.md:243-245` states both paths; three
  texts state only the first — `SKILL.md:126-128` (step 2), `SKILL.md:252-255` (step 8, the one I2 names) and
  `templates.md:72` (the `Evidence` line of the solution template). `layout.md` is the source of truth and stays.
- Solution: P2 in `solutions/lite.md` (low: three verbatim text edits). Tasks F (`SKILL.md`) and G (`templates.md`)
  in wave 2, disjoint files, both start from the feature branch; I2 is `→ tasks F, G (wave 2)`; F1 stays ⚠️ blocked
  and waits for wave 2; task B and wave 1 stay ⚠️ I2 until it closes.
- Round: F1's first re-plan from a wave entry, so no escalation. The sub-item already carries `· fixes: F1 (I2)`,
  the record F1 itself introduces, so the next re-plan of F1 counts this one.
- Check on the feature branch before the re-plan: 39 status-check tests and 59 driver tests OK, all three examples
  pass, `git diff --check` clean.
