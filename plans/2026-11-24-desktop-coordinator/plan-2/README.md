# The coordinator in Codex, and no more Python driver

- Plan: `plans/2026-11-24-desktop-coordinator/plan-2/` · slug: `desktop-coordinator-p2` · tracking branch: `plan/desktop-coordinator-p2` · created 2026-11-25 · base: 56cd0f9 · planned 2026-11-25 23:19 – 2026-11-25 23:46
- Index: `plans/2026-11-24-desktop-coordinator/index.md` part 2
- Re-plans:
  - 2026-11-26 at 376b527, 01:01 – 01:08: I1, I5, I6 → P2, task H; I2, I3 → P2, task I; new wave 4 (H, I);
    wave 3 dropped, F and G superseded by J and K in wave 5 · fixes: F1 (I1, I2, I3, I5, I6)
  - 2026-11-26 at 827b64d, 02:02 – 02:34: I1, I5, I6, I8, I10, I11, I12, I15, I16 → L, M (wave 6); I2, I3, I9,
    I14, I17, I18, I19 → N, O, P (wave 7); I13 accepted; waves 4, 5 dropped, H, I, J, K, E superseded; Q, R in wave 8 ·
    fixes: F1 (I1, I2, I3, I5, I6, I8, I9, I10, I11, I12, I14, I15, I16, I17, I18, I19) · escalated: F1
  - 2026-11-26 at addada4, 18:57 – 19:10: override of F1 (trust only the test project; no desktop app): I8, I21 →
    S, T (wave 9); I9–I12, I14–I18 → T; I2, I19 → U (wave 10); N, O, P superseded; wave 8 dropped, Q, R → V, W in
    wave 11 · fixes: F1 (I2, I8, I9, I10, I11, I12, I14, I15, I16, I17, I18, I19, I21) · escalated: F1 · override: F1
  - 2026-11-26 at a97d73e, 20:36 – 20:43: override of F1 (split F1): I14 accepted; I2, I19 → X (wave 12); I12, I22,
    I23 → new F3, AA and AB (wave 14); U superseded by X, wave 10 dropped; wave 11 dropped, V, W → Y, Z in wave 13 ·
    fixes: F1 (I2, I19), F3 (I12, I22, I23) · escalated: F1 · override: F1

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `codex-coordinator` | `$wave-auto` and the wave skills run in the Codex CLI and desktop app: GPT models per tier, a model lookup for the tier gate, the parallel limit, a permission profile | P2 | A (1), B (1), D (2) ➖, E (2) ➖, H (4) ➖, I (4) ➖, L (6), M (6), N (7) ➖, O (7) ➖, P (7) ➖, S (9), T (9), U (10) ➖, X (12) | acceptance tests 1–5, 9, 10, 13, 14 and 16 of `solutions/P2-codex-coordinator.md` hold: the texts of tasks A, B, L, M and S are in place, both lookup commands print `unknown model` for a missing thread, the checks pass, the Codex CLI rehearsal (T) is recorded as it ran (up to the start of a wave; the end of a wave not verified, accepted by the user), and X's claims match that record and call the Codex desktop app not rehearsed | ✅ merged | | `feat/desktop-coordinator-p2/F1-codex-coordinator` | 8b97145 |
| F2 | `driver-removal-docs` | The Python overnight driver is removed; the README shows where to start an unattended run in Claude Code and Codex | P3, P4 | C (1), F (3) ➖, G (3) ➖, J (5) ➖, K (5) ➖, Q (8) ➖, R (8) ➖, V (11) ➖, W (11) ➖, Y (13), Z (13) | acceptance tests 1–4 of `solutions/P4-driver-removal.md` and the check of `solutions/lite.md`, "P3" | 🔄 | wave 13 | `feat/desktop-coordinator-p2/F2-driver-removal-docs` | |
| F3 | `codex-coordinator-polish` | Codex polish found by the CLI rehearsal: the coordinator's first line and own sentences, questions as text in `codex exec`, sandbox-owned worktrees on Windows | P2 | AA (14), AB (14) | acceptance test 17 of `solutions/P2-codex-coordinator.md`: the texts of tasks AA and AB are in place and the check passes; the behaviour in Codex is not rehearsed in this plan | ⬜ | wave 14 | `feat/desktop-coordinator-p2/F3-codex-coordinator-polish` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C | ✅ (fixed by X, wave 12) |
| 2 | `waves/w02.md` | D, E | ⚠️ I12 |
| 3 | `waves/w03.md` | F, G (needs F1 merged) | ➖ dropped (tasks → wave 5) |
| 4 | `waves/w04.md` | H, I | ➖ dropped (tasks → waves 6, 7) |
| 5 | `waves/w05.md` | J, K (needs F1 merged) | ➖ dropped (tasks → wave 8) |
| 6 | `waves/w06.md` | L, M | ✅ |
| 7 | `waves/w07.md` | N, O, P (after N, O) | ✅ (fixed by X, wave 12) |
| 8 | `waves/w08.md` | Q, R (needs F1 merged) | ➖ dropped (tasks → wave 11) |
| 9 | `waves/w09.md` | S, T (after S) | ⚠️ I12, I22, I23 |
| 10 | `waves/w10.md` | U | ➖ dropped (tasks → wave 12) |
| 11 | `waves/w11.md` | V, W (needs F1 merged) | ➖ dropped (tasks → wave 13) |
| 12 | `waves/w12.md` | X | ✅ |
| 13 | `waves/w13.md` | Y, Z (needs F1 merged) | ⬜ |
| 14 | `waves/w14.md` | AA, AB (needs F1 merged) | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `codex-tiers-vendors-layout` | F1 | 1 | medium | ✅ (fixed by X, wave 12) |
| B | `codex-launch-rules` | F1 | 1 | medium | ✅ (fixed by L, M, wave 6) |
| C | `remove-driver-files` | F2 | 1 | low | ✅ |
| D | `codex-cli-rehearsal` | F1 | 2 | medium | ➖ superseded by T |
| E | `codex-desktop-rehearsal` | F1 | 2 | medium | ➖ superseded by O |
| F | `unattended-runs-readme` | F2 | 3 | medium | ➖ superseded by J |
| G | `driver-mentions-cleanup` | F2 | 3 | low | ➖ superseded by K |
| H | `codex-text-fixes` | F1 | 4 | low | ➖ superseded by L, M |
| I | `codex-claims-plugin-check` | F1 | 4 | medium | ➖ superseded by N, P |
| J | `unattended-runs-readme-v2` | F2 | 5 | medium | ➖ superseded by Q |
| K | `driver-mentions-cleanup-v2` | F2 | 5 | low | ➖ superseded by R |
| L | `codex-permissions-gate` | F1 | 6 | high | ✅ |
| M | `wave-auto-codex-rules` | F1 | 6 | high | ✅ |
| N | `codex-cli-rehearsal-v2` | F1 | 7 | high | ➖ superseded by T |
| O | `codex-desktop-rehearsal-v2` | F1 | 7 | high | ➖ dropped (the user's override: the desktop app is not rehearsed; U records it) |
| P | `codex-claims-after-rehearsals` | F1 | 7 | high | ➖ superseded by U |
| Q | `unattended-runs-readme-v3` | F2 | 8 | medium | ➖ superseded by V |
| R | `driver-mentions-cleanup-v3` | F2 | 8 | low | ➖ superseded by W |
| S | `codex-trust-docs` | F1 | 9 | high | ✅ |
| T | `codex-cli-rehearsal-v3` | F1 | 9 | high | ✅ (I14 accepted; I12, I22, I23 → F3) |
| U | `codex-claims-final` | F1 | 10 | high | ➖ superseded by X |
| V | `unattended-runs-readme-v4` | F2 | 11 | medium | ➖ superseded by Y |
| W | `driver-mentions-cleanup-v4` | F2 | 11 | low | ➖ superseded by Z |
| X | `codex-claims-split` | F1 | 12 | high | ✅ |
| Y | `unattended-runs-readme-v5` | F2 | 13 | medium | ⬜ |
| Z | `driver-mentions-cleanup-v5` | F2 | 13 | low | ⬜ |
| AA | `wave-auto-codex-output` | F3 | 14 | low | ⬜ |
| AB | `codex-sandbox-ownership` | F3 | 14 | low | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/desktop-coordinator-p2`
and reach the main branch with each feature merge.

## User problems

- P2 — The same coordinator, `$wave-auto`, should work from the Codex CLI and the Codex desktop app → F1, F3 ·
  `solutions/P2-codex-coordinator.md`
- P3 — One place in the docs says how to start an unattended run from the console and from the desktop apps of
  Claude Code and Codex → F2 · `solutions/lite.md` (low)
- P4 — Remove the Python overnight driver, now that the coordinator replaces it → F2 ·
  `solutions/P4-driver-removal.md`

## How to try

- F1 — in a scratch project with the skills installed (installer with the Codex links, or the Codex plugin), the
  profile of README "Codex permissions" in `<project>/.codex/config.toml` and the project's trust entry from that
  section in `~/.codex/config.toml`, start `codex -m gpt-6.2-astra` in the project and type `$wave-auto` and a list of
  two small changes → it prints `Capabilities:` with a GPT model ID per tier, asks its questions once, prints one line
  per step through triage and planning and starts the first wave; README Limitations says the Codex CLI was
  rehearsed up to the start of a wave and the Codex desktop app is not rehearsed; remove the trust entry afterwards;
  before: a Codex agent could not name its model, so the tier gate stopped every medium and high step, `wave-auto`
  named only Claude models, and without the profile and the trust entry `$wave-auto` stopped at its first step (`.git`
  read-only).
- F2 — open `README.md`, section "Overnight runs" → "Unattended runs: wave-auto" has a table of where to start it
  (Claude Code CLI and desktop app, Codex CLI and desktop app), two lines for a start from a script, and "In the
  morning" without a driver; the folder `scripts/` is gone; before: the README taught `python scripts/wave_driver.py`
  and its morning `report.md`.
- F3 — `git grep -n -E "request_user_input_async|dubious ownership" -- skills README.md` → the step 4 rule in
  `skills/wave-auto/SKILL.md` and the sandbox-ownership paragraph in README "Codex permissions" and layout
  "Permissions in Codex"; before: nothing. The behaviour in Codex is not rehearsed in this plan: a later Codex run
  shows it, and its findings go to a new plan.

## Known test failures before start

- none (`main` at 56cd0f9, 2026-11-25: 39 status-check tests and 59 driver tests OK, all three examples pass,
  `git diff --check` clean); every task of waves 1 and 2 starts from it or from its feature branch
- none at the re-plan of 2026-11-26, round 4: F1 at bcd3b0d (39 status-check and 59 driver tests, three examples,
  `git diff --check main`) and F2 at abfd0a5 (39 tests, three examples, `git diff --check main`); wave 12 starts from
  F1, waves 13 and 14 from F2 and F3 after `main` (with F1) is merged in

## Assumptions

- Codex's capabilities were found by running the Codex CLI 0.167 that ships with the desktop app, in planning
  (evidence in `solutions/P2-codex-coordinator.md`): `spawn_agent` with a `model` per subagent, at most 3 subagents at
  once, no tool to start a session, and no model ID the agent can name. So the probe the index planned for P2 is done,
  and F1's tasks are medium; the desktop app and whole runs are rehearsed by D and E.
- A Codex agent takes its model from its thread's rollout file (`CODEX_THREAD_ID`, record `turn_context`), written by
  Codex itself: this counts as "its own environment" of the tier gate, not as the prompt. No file → `unknown model` →
  the gate stops, as before.
- GPT models per tier, from Codex's model list on 2026-11-25: `gpt-6-luna` low, `gpt-6.2-sol` and `gpt-6.1-sol`
  medium, `gpt-6.2-astra` high. Like the Claude names they are examples; a README `Models:` line can name others.
- P3's clarification "the Python driver as an optional tool" is superseded by P4, the user's later decision: the docs
  describe no driver. P3 and P4 are one feature: removing the driver's docs without the new ones would leave the
  README with no unattended path.
- The `- Unreleased` changelog item announced the driver, which never reached a release; its sentence is deleted there.
- The end-to-end rehearsal records stay, with a history note; the driver docs and print-mode records are deleted (git
  history keeps them).
- Wave 3 waited for F1 merged: F2 edits `README.md`, `layout.md` and `CHANGELOG.md` on top of F1, and its README takes
  the Codex sandbox and permission mode from F1's rehearsal records.
- Codex shows no cost in USD; each rehearsal is capped at 3 hours instead.
- The plan runs in manual flow (no `Flow:` line): the user reviews F1, F2 and F3.
- Re-plan 2026-11-26, round 4 of F1, by the user's override "split F1" (direction in `history.md`; evidence in
  `solutions/P2-codex-coordinator.md`): F1 is merged with task T's rehearsal as recorded; the unverified end of a wave
  in Codex (I14) is accepted and named in README Limitations by task X (high, wave 12; needs Opus 5.5 or
  GPT-6.2-Astra), which replaces U because U's definitions would call the Codex CLI not rehearsed. I12, I22 and I23
  move to the new feature F3 (tasks AA, AB, low, wave 14, after F1 is merged), whose acceptance is the text only: no
  Codex run. F3 is round 1 of its own. Wave 11 is dropped because F1 needs wave 12 first; V and W return unchanged as
  Y and Z in wave 13.
