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
  - 2026-11-27 at 3af7fb8, 03:26 – 03:27 (start: the first clock reading of the run): I24, I25 → P5, task AC; task AD
    rewraps two lines; new wave 15; I26–I28 accepted by the user · fixes: F2 (I24, I25)
  - 2026-11-27 at 5999f53, 21:03 – 21:05: I33 → P2, task AE (high, wave 16) · fixes: F3 (I33) · escalated: F3

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `codex-coordinator` | `$wave-auto` and the wave skills run in the Codex CLI and desktop app: GPT models per tier, a model lookup for the tier gate, the parallel limit, a permission profile | P2 | A (1), B (1), D (2) ➖, E (2) ➖, H (4) ➖, I (4) ➖, L (6), M (6), N (7) ➖, O (7) ➖, P (7) ➖, S (9), T (9), U (10) ➖, X (12) | acceptance tests 1–5, 9, 10, 13, 14 and 16 of `solutions/P2-codex-coordinator.md` hold: the texts of tasks A, B, L, M and S are in place, both lookup commands print `unknown model` for a missing thread, the checks pass, the Codex CLI rehearsal (T) is recorded as it ran (up to the start of a wave; the end of a wave not verified, accepted by the user), and X's claims match that record and call the Codex desktop app not rehearsed | ✅ merged | | `feat/desktop-coordinator-p2/F1-codex-coordinator` | 8b97145 |
| F2 | `driver-removal-docs` | The Python overnight driver is removed; the README shows where to start an unattended run in Claude Code and Codex | P3, P4, P5 | C (1), F (3) ➖, G (3) ➖, J (5) ➖, K (5) ➖, Q (8) ➖, R (8) ➖, V (11) ➖, W (11) ➖, Y (13), Z (13), AC (15), AD (15) | acceptance tests 1–4 of `solutions/P4-driver-removal.md` the check of `solutions/lite.md`, "P3", as "P5" changes its text, and the checks of tasks AC and AD | ⚠️ blocked (I24, I25) | wave 15 | `feat/desktop-coordinator-p2/F2-driver-removal-docs` | |
| F3 | `codex-coordinator-polish` | Codex polish found by the CLI rehearsal: the coordinator's first line and own sentences, questions as text in `codex exec`, sandbox-owned worktrees on Windows | P2 | AA (14), AB (14), AE (16) | acceptance tests 17 and 18 of `solutions/P2-codex-coordinator.md`: the texts of tasks AA, AB and AE are in place and the check passes; the behaviour in Codex is not rehearsed in this plan | ⚠️ blocked (I33) | wave 16 | `feat/desktop-coordinator-p2/F3-codex-coordinator-polish` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C | ✅ (fixed by X, wave 12) |
| 2 | `waves/w02.md` | D, E | ✅ (fixed by AA, wave 14) |
| 3 | `waves/w03.md` | F, G (needs F1 merged) | ➖ dropped (tasks → wave 5) |
| 4 | `waves/w04.md` | H, I | ➖ dropped (tasks → waves 6, 7) |
| 5 | `waves/w05.md` | J, K (needs F1 merged) | ➖ dropped (tasks → wave 8) |
| 6 | `waves/w06.md` | L, M | ✅ |
| 7 | `waves/w07.md` | N, O, P (after N, O) | ✅ (fixed by X, wave 12) |
| 8 | `waves/w08.md` | Q, R (needs F1 merged) | ➖ dropped (tasks → wave 11) |
| 9 | `waves/w09.md` | S, T (after S) | ✅ (fixed by AA, AB, wave 14) |
| 10 | `waves/w10.md` | U | ➖ dropped (tasks → wave 12) |
| 11 | `waves/w11.md` | V, W (needs F1 merged) | ➖ dropped (tasks → wave 13) |
| 12 | `waves/w12.md` | X | ✅ |
| 13 | `waves/w13.md` | Y, Z (needs F1 merged) | ⚠️ I24, I25 |
| 14 | `waves/w14.md` | AA, AB (needs F1 merged) | ⚠️ I33 |
| 15 | `waves/w15.md` | AC, AD (needs F1 merged) | ⬜ |
| 16 | `waves/w16.md` | AE (needs F1 merged) | ⬜ |

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
| Y | `unattended-runs-readme-v5` | F2 | 13 | medium | ⚠️ I24, I25 |
| Z | `driver-mentions-cleanup-v5` | F2 | 13 | low | ✅ |
| AA | `wave-auto-codex-output` | F3 | 14 | low | ✅ |
| AB | `codex-sandbox-ownership` | F3 | 14 | low | ⚠️ I33 |
| AC | `unattended-runs-script-lines` | F2 | 15 | low | ⬜ |
| AD | `cleanup-line-wrapping` | F2 | 15 | low | ⬜ |
| AE | `safe-directory-path` | F3 | 16 | high | ⬜ |

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
- P5 — The "Unattended runs" text names guidance that does not exist and script lines that fail on Windows → F2 ·
  `solutions/lite.md` (low)

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
  (Claude Code and Codex, CLI and desktop app; the Codex desktop app marked not rehearsed), script lines for bash or
  zsh and for PowerShell with a Git Bash note, said to be not run yet, and "In the morning" without a driver; the
  folder `scripts/` is gone; before: the README taught `python scripts/wave_driver.py` and its morning `report.md`.
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
- none at the re-plan of 2026-11-27: F2 at e2df989 (39 tests, three examples, `git diff --check main`); wave 15
  starts from it
- none at the re-plan of 2026-11-27, round 2 of F3: F3 at 884adf9 (39 tests, three examples, `git diff --check
  main`); wave 16 starts from it

## Assumptions

- P3's clarification "the Python driver as an optional tool" is superseded by P4, the user's later decision: the docs
  describe no driver. P3 and P4 are one feature: removing the driver's docs without the new ones would leave the
  README with no unattended path.
- The `- Unreleased` changelog item announced the driver, which never reached a release; its sentence is deleted there.
- The end-to-end rehearsal records stay, with a history note; the driver docs and print-mode records are deleted (git
  history keeps them).
- Wave 3 waited for F1 merged: F2 edits `README.md`, `layout.md` and `CHANGELOG.md` on top of F1, and its README takes
  the Codex sandbox and permission mode from F1's rehearsal records.
- The plan runs in manual flow (no `Flow:` line): the user reviews F1, F2 and F3.
- The assumptions of F1's design (Codex capabilities, the model lookup, the GPT tiers, the split) are in `history.md`.
- Re-plan 2026-11-27, round 1 of F2: the user chose not to run the README's script lines; the README says they were
  not run, and the unrepeated starts and the unviewed GitHub rendering are accepted (I26–I28).
