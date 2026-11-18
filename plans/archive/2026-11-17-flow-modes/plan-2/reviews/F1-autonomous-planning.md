# F1 · Triage and planning in autonomous flow, chained parts on one integration branch

- Branch: `feat/flow-modes-p2/F1-autonomous-planning` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p2-F1`
- 👀 review since 2026-11-17 21:31

## Essence

Autonomous triage and planning use recorded assumptions and put chained parts on one integration branch. Each run has a distinct claim, and exactly one session can take over when a wave resumes from task mode.

## How to test

1. Run `/wave-triage flow autonomous` with an ambiguous item in a scratch repository → the index records the autonomous flow and its assumption.
2. Try to plan part 2 while part 1 has a feature under review → planning stops with `part-unmerged`. Merge part 1 into the integration branch and retry → part 2 starts from that branch and `main` stays unchanged.
3. Start a competing run on a held target → it stops with `wave-running`, and `wave-status` names the holder. Resume a wave waiting for task mode from two sessions → exactly one gets the claim.

## Worth a look

A refused claim leaves refs, worktrees, and commits unchanged. Its contender blob can remain unreachable in Git's object store (I8, rehearsal scenario 8).

## Tasks

- A (wave 1) — Set the rules for autonomous planning and chained parts.
- B (wave 1) — Enabled autonomous planning with recorded assumptions and a shared integration branch.
- C (wave 1) — Made autonomous triage record its decisions and status find plans on their tracking branches.
- D (wave 1) — Taught wave-run to find off-main plans, detect already-running waves on a shared target and surface assumptions in review.
- E (wave 1) — Walked through the autonomous planning rules and recorded check results.
- I (wave 3) — Defined integration target claims with guarded updates.
- J (wave 3) — Moved the existing-plan check ahead of writes and documented when planning takes and releases the integration claim.
- K (wave 3) — Made autonomous wave instructions claim the integration branch and made status show the holder.
- L (wave 3) — Rehearsed autonomous triage and two-part planning in scratch repositories.
- M (wave 3) — Rehearsed plan safety and target claim behavior in scratch repositories.
- P (wave 5) — Specified the waiting claim, atomic takeover, per-run token, and refused-claim guarantees.
- Q (wave 5) — Rehearsed claim handoff and checked what a refusal leaves in Git.

## Check

`python skills/wave-plan/scripts/test_status_check.py` → 20 passed. `status_check.py` → both examples passed. `git diff --check` and `git diff --check main...HEAD` → clean. Scratch scenarios 7 and 8 held; the PowerShell form passed in PowerShell 7 and Windows PowerShell 5.1. No test files changed.
