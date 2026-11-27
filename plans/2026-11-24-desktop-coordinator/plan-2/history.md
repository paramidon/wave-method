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

## Re-plan 2026-11-26, 18:57 (round 3 of F1, override)

- F1 was at the re-plan limit (round 3, held). The user typed the override; the direction, verbatim:
  `доверить только тестовый проект: разрешаю добавлять запись о нём в ~/.codex/config.toml (при планировании и
  проверке) и удалять её после; описать в документации, как сделать проект доверенным, и повторить проверку в
  консольном Codex; приложение не проверять и так и записать`
  (trust only the test project: adding its entry to `~/.codex/config.toml` is allowed during planning and the check,
  and it is removed afterwards; document how a project becomes trusted and repeat the check in the Codex CLI; do not
  check the desktop app, and record that).
- Open entries: I2, I8–I12, I14–I19 (planned in round 2 as N, O, P; N stopped at X1, O was not run, P changed
  nothing) and I21 (found by N). All concern F1, so the re-plan is escalated and recorded under `override:`.
- Evidence, run in this session on task N's fixture: without trust the thread is read-only (N1 reproduces); with the
  test project's trust entry the profile applies and X1 makes a worktree and a commit; `-c "projects=…"` trusts for
  one run; a profile given with `-c` applies without trust, and Codex then writes the trust entry itself. Details and
  the `trust_entry.py` helper: `solutions/P2-codex-coordinator.md`, "Evidence (re-plan 2026-11-26, round 3)".
- `~/.codex/config.toml` during planning: one entry for the test project added and removed (T1), and one that Codex
  added itself (T3) removed; a first T1 attempt wrote a malformed key and the file was restored from a copy taken
  before T0. The hash at the end equals the hash before T0. The fixture `~/wave-rehearsal-20261126-0319` is left as
  task N left it (no probe branch or worktree).
- New tasks, all high: S (wave 9) documents trust; T (wave 9, after S) rehearses the CLI in a trusted test project;
  U (wave 10) makes the claims match the records and records the desktop app as not rehearsed (I2, I19). N and P are
  superseded by T and U; O is dropped by the direction.
- Order: wave 8 (Q, R of F2) waits for F1 merged and would block waves 9 and 10, so it is dropped; Q and R return
  unchanged as V and W in wave 11.
- Checks run at the re-plan: F1 at 89a4ecb and F2 at abfd0a5 green (39 status-check tests, 59 driver tests on F1,
  three examples, `git diff --check main`).

## Re-plan 2026-11-26, 20:36 (round 4 of F1, override: split)

- F1 was held at the re-plan limit (round 4). Asked for ways to stop the loop, the user got three options (A: split
  F1 — merge it with the rehearsal as recorded, accept the unverified end of a wave, move the remaining findings to a
  new feature; B: finish the rehearsal inside F1; C: drop the rehearsal from F1) and answered, verbatim:
  `А: разделить F1` (A: split F1). That answer is the override's direction.
- Why F1 looped: its done-when required a live Codex rehearsal, and every rehearsal found the next layer (git
  read-only under `workspace-write`, the untrusted project, then the usage limit and four small findings); each finding
  blocked F1 and forced a re-plan, and F2's wave was dropped each time because it waits for F1 merged. The split makes
  F1's done-when take task T's record as it is, and F3 has no rehearsal, so no new live run can block either feature.
- Open entries: I2, I19 (→ task X), I14 (accepted by the user: the end of a wave in Codex is not verified), I12, I22,
  I23 (moved to F3). F1 is escalated and recorded under `override:`; F3 is a new feature at round 1, so its tasks are
  `low`.
- Evidence, run in this session: task U's definitions applied to T's record by a script give "CLI rehearsed: False",
  so U would have written "in Codex it is not rehearsed yet"; X writes fixed texts instead. The F1 and F2 checks are
  green; `git -c safe.directory=…` and a review from the main checkout both work for a sandbox-made worktree (I23).
  Details: `solutions/P2-codex-coordinator.md`, "Evidence (re-plan 2026-11-26, round 4)".
- Order: X (F1, wave 12) first; wave 11 (V, W of F2) waits for F1 merged and would block wave 12, so it is dropped and
  V, W return unchanged as Y, Z in wave 13; F3's AA, AB in wave 14 also wait for F1 merged, and do not wait for F2.
- Left for the user: the rehearsal folder `~/wave-rehearsal-20261126-1955` (claim refs and uncommitted task files in
  its `textkit` repository) is no longer needed by the plan.
- Moved here from README "Known test failures before start":

  - none on the feature branches at the re-plan of 2026-11-26: F1 at bbfbe18 (status-check and driver tests, three
    examples, `git diff --check main`) and F2 at abfd0a5 (the same without the driver tests); waves 4 and 5 start from
    them
  - none at the re-plan of 2026-11-26, round 2: F1 at 4d0d1f7 and F2 at abfd0a5, the same checks; waves 6 and 7 start
    from F1, wave 8 from F2 after `main` (with F1) is merged in
  - none at the re-plan of 2026-11-26, round 3: F1 at 89a4ecb (39 status-check and 59 driver tests, three examples,
    `git diff --check main`) and F2 at abfd0a5 (39 tests, three examples, `git diff --check main`); waves 9 and 10
    start from F1, wave 11 from F2 after `main` (with F1) is merged in

- Moved here from README "Assumptions":

  - Re-plan 2026-11-26: F1's fixes need a wave after wave 2, and `wave-run` starts a wave only when every earlier wave
    is ✅, ⚠️ or ➖; wave 3 waits for F1 merged, so it is dropped, and its tasks F and G return unchanged as J and K in
    wave 5.
  - I3's "Markdown viewed rendered" is left to the user's review of F1; task I checks the section by the Markdown rules
    and runs both plugin commands with a scratch `CODEX_HOME`, so the user's Codex settings stay untouched.
  - Task H also adds "or GPT-6.2-Astra" to the `wave-plan` and `wave-triage` descriptions (not in I1), as `wave-auto`'s
    already has it.
  - Re-plan 2026-11-26, round 2 of F1 (escalated; evidence in `solutions/P2-codex-coordinator.md`): the user chose the
    Codex permission profile (sandbox on, writes only below the folder that holds the repository) with full access as
    the documented fallback; rehearsals use the profile only. The user chose to rehearse the desktop app again (task O);
    a full-access mode there still needs the user's separate permission. I13 was accepted by the user.
  - Every new F1 task is high (escalated re-plan, round 2): waves 6 and 7 need Opus 5.5 or GPT-6.2-Astra. Waves 4 and 5
    are dropped for the reason of the first re-plan; their tasks return in waves 6–8 (details in `history.md`).
  - Re-plan 2026-11-26, round 3 of F1, by the user's override (direction in `history.md`; evidence in
    `solutions/P2-codex-coordinator.md`): Codex applies a project's profile only in a trusted project. Task T trusts
    only its test project, with one entry in `~/.codex/config.toml` that it removes afterwards; the Codex desktop app is
    not rehearsed, and task U records that. S, T and U are high (waves 9 and 10 need Opus 5.5 or GPT-6.2-Astra); wave 8
    is dropped because F1 needs waves 9 and 10 first, and Q, R return unchanged as V, W in wave 11.

## Re-plan 2026-11-27 (round 1 of F2)

- Open entries of wave 13: I24 and I25 (task Y) → task AC, `solutions/lite.md`, "P5". I26, I27 and I28 were accepted
  by the user, who chose not to run the script lines against Claude Code or Codex.
- I24's cause: the desktop-app sentence the table pointed to was to be written by task P, which was superseded.
- Found while planning: Git Bash on Windows rewrites `/wave-auto …` into a Windows path, so the bash form of the
  `claude` line needed a note too.
- AD rewraps two places task Z left (a line over 120 characters, a split code span); it fixes no entry and gives the
  new wave its second task.
- Order: wave 15 starts only after wave 14 (F3) has run.
- Check run at the re-plan: F2 at e2df989 green.

## Assumptions of F1, moved from the README on 2026-11-27 (F1 is merged)

- Codex's capabilities were found by running the Codex CLI 0.167 that ships with the desktop app, in planning
  (evidence in `solutions/P2-codex-coordinator.md`): `spawn_agent` with a `model` per subagent, at most 3 subagents at
  once, no tool to start a session, and no model ID the agent can name. So the probe the index planned for P2 is done,
  and F1's tasks are medium; the desktop app and whole runs are rehearsed by D and E.
- A Codex agent takes its model from its thread's rollout file (`CODEX_THREAD_ID`, record `turn_context`), written by
  Codex itself: this counts as "its own environment" of the tier gate, not as the prompt. No file → `unknown model` →
  the gate stops, as before.
- GPT models per tier, from Codex's model list on 2026-11-25: `gpt-6-luna` low, `gpt-6.2-sol` and `gpt-6.1-sol`
  medium, `gpt-6.2-astra` high. Like the Claude names they are examples; a README `Models:` line can name others.
- Codex shows no cost in USD; each rehearsal is capped at 3 hours instead.
- Re-plan 2026-11-26, round 4 of F1, by the user's override "split F1" (direction in `history.md`; evidence in
  `solutions/P2-codex-coordinator.md`): F1 is merged with task T's rehearsal as recorded; the unverified end of a wave
  in Codex (I14) is accepted and named in README Limitations by task X (high, wave 12; needs Opus 5.5 or
  GPT-6.2-Astra), which replaces U because U's definitions would call the Codex CLI not rehearsed. I12, I22 and I23
  move to the new feature F3 (tasks AA, AB, low, wave 14, after F1 is merged), whose acceptance is the text only: no
  Codex run. F3 is round 1 of its own. Wave 11 is dropped because F1 needs wave 12 first; V and W return unchanged as
  Y and Z in wave 13.

## Re-plan 2026-11-27 (round 2 of F3, escalated)

- Open entry of wave 14: I33 (task AB): README "Codex permissions" gives `git config --global --add safe.directory`
  without a path. I24 and I25 already wait for task AC (wave 15); nothing else was open.
- F3's first round was the split of F1 (re-plan of 2026-11-26, round 4 of F1, `fixes: … F3 (I12, I22, I23)`), so this
  re-plan is round 2 of F3: escalated. The disputed assumption was checked by running git 2.52 in a scratch folder,
  with `GIT_TEST_ASSUME_DIFFERENT_OWNER=1` standing in for the Codex sandbox account; evidence in
  `solutions/P2-codex-coordinator.md`, "Evidence (re-plan 2026-11-27, round 2)".
- Task AE (wave 16) adds the worktree path to the command. It is `high` only because the escalation rule makes every
  new task of the feature high; the edit itself is one line. A single-task wave: AE cannot join wave 15, whose task AC
  also edits `README.md`.
- The cause: AB copied the solution's own text (`solutions/P2-codex-coordinator.md`, "Polish", task AB, edit 1); the
  slip was in planning, not in the task.
- A third round of F3 would hold it (`user: re-plan limit`) until the user's override.
- Check run at the re-plan: F3 at 884adf9 green (39 tests, three examples, `git diff --check main`).
