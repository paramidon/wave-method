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

## Re-plan 2 · 2026-11-25 at b3b69ff

- Open entries: I2–I9 (wave 3). All are defects or gaps of P1, so they stay in P1 and get no new P number. F1 is at
  round 1 of "Re-plan escalation" (re-plan 1 recorded no `fixes:` part), so this is a normal re-plan.
- I2, I3, I4, I7, I8 → task N, wording of `wave-auto/SKILL.md` and `layout.md`; design in the solution, "Fixes after
  the rehearsals". I2 keeps the design: the launching roles stay with the coordinator in every environment. Moving the
  tasks of a wave into nested subagents was not chosen: nesting was seen only in the CLI.
- I5, I9: a re-plan of rehearsals alone would turn every behaviour left out into a new entry again, so the user was
  asked: (A) a second rehearsal in the CLI, cap 30 USD (the first cost 6.98), with what needs a person or other
  settings accepted as known limits; or (B) accept everything as known limits and only try the fixes (about 5 USD).
  The user's answer, relayed by the session that started the re-plan, 2026-11-25: «выбираю А». The accepted limits are
  in the solution, "Limits"; the covered behaviours are tasks O, P, Q.
- The question named the interactive TUI, a typed answer, the exact first message, other permission modes and the
  desktop cost as the accepted limits. Desktop-app repetitions of the CLI runs, a session fallback that starts a
  session and a `tier-mismatch` of a coordinated task are not planned; the report of the re-plan says so to the user.
- I6 → task Q. Tried once during the re-plan on b3b69ff, to fix the expectations: `install.sh` (Git Bash) and
  `install.ps1` with Codex links gave five skills under `.agents/skills`, and WSL gave five symlinks.
- Outside this plan, the same on `main` (not an entry): in Git Bash for Windows `ln -s` copies, so a second
  `install.sh` run there stops "exists and is not a symlink"; `install.sh` with an empty target installs into the
  current folder.
- Feature branch at b3b69ff checked green before writing: 39 status-check tests, 59 driver tests, the three examples,
  `git diff --check main`.

## Re-plan 3 · 2026-11-25 at be54998

- Open entries: I13, I14, I15, I18, I19, I20, I26 (wave 4). The other entries of wave 4 were accepted by the user as
  known limits before this re-plan (commit 99a7ba1). All seven are defects of P1's texts, so they stay in P1.
- F1 is at round 2 of "Re-plan escalation" (re-plan 2 named it under `fixes:`): escalated. Every disputed assumption
  was checked by running commands in a scratch folder and on the feature branch; the evidence is in the solution,
  "Fixes after the second rehearsal", "Evidence" (E1–E7). Every new task is `high`. The plan stays in manual flow, so
  there is no `manual review:` list to extend.
- I13, I15, I18, I19, I20 → task R (`wave-auto/SKILL.md`, `layout.md`); I14, I26 → task S (`task-mode.md`,
  `wave-status/SKILL.md`). Two design choices beyond the entries' proposals: the run-ending `capability-missing` of the
  coordinator is renamed `no-subagents`, so no code appears in both tables of "Stops"; the step count follows the
  coordinator's agent calls, not its progress lines, because skipped progress lines are an accepted limit. One gap
  closed in passing: Start phase 4 now says to ask nothing when the index has no question.
- The user was asked whether to check the fixes in real runs; the answer, 2026-11-25: «Fixes + short rehearsal
  (Recommended)» → task T, a CLI rehearsal of four runs, 8 USD cap for its `claude -p` calls. A finding of T is a new
  entry of F1 and makes the next re-plan round 3: held until the user's `override F1: <direction>`.
- Feature branch at be54998 checked green before writing: 39 status-check tests, 59 driver tests, the three examples,
  `git diff --check main`.
