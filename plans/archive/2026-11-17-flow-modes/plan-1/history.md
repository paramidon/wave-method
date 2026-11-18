# History

## Re-plan 2026-11-17 at e83a4f1

- Input: open entries I1 and I2 of wave 1 / task A, both on `skills/wave-plan/layout.md`. Wave 1 ⚠️, wave 2 not run,
  no wave 🔄. `main` (d6d2d98) merged into the tracking branch first; it brought no file change.
- Checked on `feat/flow-modes-p1/F1-autonomous-flow` at e83a4f1: the wave check is green (`test_status_check.py` 20
  tests OK, both examples exit 0, `git diff --check` clean), so wave 3 starts with no known failures.
- I1 confirmed at `layout.md:177`. The same wording is in `wave-status/SKILL.md:107` and `wave-run/SKILL.md:111`; none
  of the three is in an edit list of P1–P3. `wave-status/SKILL.md` ran the "Main readiness" commands for `main-dirty`
  but said only that `<main>` resolves by the flow, not `<main checkout>`. All four edits are P12.
- I2 confirmed: `integration/<name>` is used in `layout.md` (branch table, `Flow:` example, "Integration target"),
  `wave-run/autonomous.md`, `wave-run/report.md` and `wave-status/SKILL.md`; `wave-status/SKILL.md:32` points to
  `layout.md`, "Names", for the integration branch, and `autonomous.md` "Flow form" defines `<name>` circularly ("the
  `<name>` of the current `target:`"). Of I2's two proposals the Names bullet was taken (P13).
- A re-plan appends waves and a lone low task cannot form one, so wave 2 was dropped and rebuilt as wave 3: E → G (the
  same P3 edits plus P12 edit 4, because G owns `wave-run/SKILL.md`), F → I (the same closing check plus the P12
  wording check and the P13 `<name>` check), and the new low task H (P12 edits 1-3 and P13, in `layout.md` and
  `wave-status/SKILL.md`), parallel to G. New slugs, because slugs stay distinct in the plan.
- I1 and I2 stay open with `→ task H (wave 3)`; task A and wave 1 stay ⚠️ until wave 3 closes them.
