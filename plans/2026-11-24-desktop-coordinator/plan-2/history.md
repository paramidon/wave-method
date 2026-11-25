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

## Re-plan 2026-11-26, 02:02 (round 2 of F1, escalated)

- Open entries: I1, I2, I3, I5, I6 of wave 1 (planned in round 1 as H and I, never run) and I8–I19 of wave 2 (task D's
  Codex CLI rehearsal stopped at its first step; task E never ran). All concern F1, so F1 is at round 2: escalated.
- Every disputed assumption was checked by running Codex 0.167 in scratch folders (sandbox commands and three
  `codex exec` runs); the table is `solutions/P2-codex-coordinator.md`, "Evidence (re-plan 2026-11-26, round 2)". Main
  results: a permission profile whose writable folder is the repository's parent lets git write (the default
  `workspace-write` never does); a project's `.codex/config.toml` applies it in the CLI; a Codex subagent checks its
  model only when the prompt carries the lookup command; `gpt-6-luna` is accepted although the tool does not list it.
- The user's decisions (2026-11-26): the permission profile, with full access as the documented fallback; rehearse the
  desktop app again; accept I13 (Codex writes a trust entry per new project folder); remove the probe folder and the
  trust entries of D and of the probes. The two entries were removed from `~/.codex/config.toml`; deleting the probe
  folder `D:\wave-probe` was refused by the session's safety check and is left to the user.
- New tasks, all high: L and M (wave 6) write the fixes; N and O (wave 7) rehearse the CLI and the desktop app with the
  profile, N also checks the plugin commands (I3); P (wave 7, after N and O) makes the claims match the records (I2).
- Order: wave 4 (H, I) is dropped because I needs E's record and both would block the new waves; wave 5 (J, K) is
  dropped because it waits for F1 merged. Q and R in wave 8 replace J and K; P3's Codex placeholders were resolved in
  `solutions/lite.md` (the README links to "Codex permissions").
- Task E's prepared worktree and branch (`task/desktop-coordinator-p2/F1-w2-E-codex-desktop-rehearsal`, no commits) are
  no longer needed; the user may remove them.
- Checks run at the re-plan: F1 at 4d0d1f7 and F2 at abfd0a5 green (status-check tests, driver tests on F1, three
  examples, `git diff --check main`).
