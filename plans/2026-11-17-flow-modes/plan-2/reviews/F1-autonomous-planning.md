# F1 · Triage and planning in autonomous flow, chained parts on one integration branch

- Branch: `feat/flow-modes-p2/F1-autonomous-planning` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p2-F1`

## How to test

- B: Plan an index part with an inherited autonomous flow and an ambiguous item → the README records the assumption and the plan starts from the integration branch.
- C: Triage an ambiguous item in autonomous flow → the index records its flow and the chosen reading. Check status for an off-main plan → status finds it through its tracking branch.
- D: Check a plan whose README exists only on its tracking branch → wave-run finds it. Start a wave when another plan on the same target is already running → wave-running names the active plan and wave.

- K: Hold the integration target before starting a second wave → it stops with `wave-running` and identifies the holder; status shows the claim.
- L: Rehearse an ambiguous item and a two-part index → triage records the assumption, planning waits for part 1, and part 2 starts on the integration branch once part 1 is merged.

## Tasks

- B (wave 1) — Enabled autonomous planning with recorded assumptions and a shared integration branch.
- C (wave 1) — Made autonomous triage record its decisions and status find plans on their tracking branches.
- D (wave 1) — Taught wave-run to find off-main plans, detect already-running waves on a shared target and surface assumptions in review.
- J (wave 3) — Moved the existing-plan check ahead of writes and documented when planning takes and releases the integration claim.
- K (wave 3) — Made autonomous wave instructions claim the integration branch and made status show the holder.
- L (wave 3) — Rehearsed autonomous triage and two-part planning in scratch repositories.
