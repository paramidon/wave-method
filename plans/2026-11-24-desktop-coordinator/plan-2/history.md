# History

## Re-plan 2026-11-26 (round 1 of F1)

- Open entries of wave 1: I1, I2, I3 (task A) and I5, I6 (task B), all of F1; I4 and I7 were closed in wave 1.
- I1, I5, I6 are text fixes: task H (low), `solutions/P2-codex-coordinator.md`, "Text fixes (task H)". H also adds the
  GPT high-tier model to the `wave-plan` and `wave-triage` descriptions, which I1 did not name.
- I2 cannot be fixed before the rehearsals run: task I (medium, wave 4) reads the records of D and E and makes the
  README Limitations bullet, the "Vendors" row "starting a session" and the changelog claim exactly what they show.
- I3: task I runs both `codex plugin` commands with a scratch `CODEX_HOME` (the wave 1 task refused to run them because
  they change the user's Codex settings) and records the result in the CLI rehearsal record; the rendered view is left
  to the user's review.
- Order: `wave-run` starts a wave only when every earlier wave is ✅, ⚠️ or ➖, and wave 3 needs F1 merged, which now
  needs wave 4. Wave 3 is dropped; F and G return unchanged as J and K in wave 5. Wave 2 (D, E) is unchanged.
- Checks run at the re-plan: F1 at bbfbe18 and F2 at abfd0a5 green (status-check tests, driver tests on F1, three
  examples, `git diff --check main`).
