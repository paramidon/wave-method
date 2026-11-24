# History

## Re-plan 1 · 2026-11-24 at 01bfa8c

- Open entry: I1 (wave 1, task D) — `skills/wave-auto/navigator.md`, "Return grammar", allowed at most four `halt`
  lines. When the reading ends with `done`, the coordinator lists only the `halt` lines it got and never skips the
  other units, so a fifth halted unit would be neither reported nor dispatched.
- Fix: no limit, one `halt` line per halted unit (a unit never gets two, because the first rule that applies decides
  it). Two text edits: the navigator's "Return grammar" and the `navigate` row of `layout.md`, "Coordinated runs",
  "Steps". The design is in `solutions/P1-in-session-coordinator.md`, "Return grammar" of the navigator section, and
  acceptance test 3. Difficulty low; it stays in P1 (a defect of P1's solution, not a new user problem), so it gets no
  new P number, which also keeps the P numbers of index part 2 (P2–P4) unambiguous.
- Placement: wave 2 had not run. A wave of the fix alone would be a solo `low` wave, and after wave 2 it would leave
  the rehearsals exercising the unfixed navigator. So wave 2 is dropped before it ran and wave 3 takes its tasks with
  new IDs: J = F plus the I1 fix (its four files stay disjoint from K's), K = G, L = H, M = I, prompts otherwise
  unchanged (the solution sections they cite keep their names "(task F)", "(task G)", "(tasks H and I)").
- Feature branch `feat/desktop-coordinator-p1/F1-in-session-coordinator` at 01bfa8c checked green before writing:
  39 status-check tests, 59 driver tests, the three examples, `git diff --check main`.
- `reviews/F1-in-session-coordinator.md` is left to `wave-run`.
