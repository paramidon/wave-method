# The coordinator in Codex, and no more Python driver

- Plan: `plans/2026-11-24-desktop-coordinator/plan-2/` · slug: `desktop-coordinator-p2` · tracking branch: `plan/desktop-coordinator-p2` · created 2026-11-25 · base: 56cd0f9 · planned 2026-11-25 23:19 – 2026-11-25 23:46
- Index: `plans/2026-11-24-desktop-coordinator/index.md` part 2
- Re-plans: none

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `codex-coordinator` | `$wave-auto` and the wave skills run in the Codex CLI and desktop app: GPT models per tier, a model lookup for the tier gate, the parallel limit | P2 | A (1), B (1), D (2), E (2) | acceptance tests 1–7 of `solutions/P2-codex-coordinator.md` hold: the texts of tasks A and B are in place, both lookup commands print `unknown model` for a missing thread, the checks pass, and the Codex CLI (D) and desktop app (E) rehearsals are recorded with every expectation Pass, a finding with an open entry or Not run with its reason | ⚠️ blocked (I1, I2, I3, I5, I6) | I1, I2, I3, I5, I6 | `feat/desktop-coordinator-p2/F1-codex-coordinator` | |
| F2 | `driver-removal-docs` | The Python overnight driver is removed; the README shows where to start an unattended run in Claude Code and Codex | P3, P4 | C (1), F (3), G (3) | acceptance tests 1–4 of `solutions/P4-driver-removal.md` and the check of `solutions/lite.md`, "P3" | 🔄 | wave 3 | `feat/desktop-coordinator-p2/F2-driver-removal-docs` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C | ⚠️ I1, I2, I3, I5, I6 |
| 2 | `waves/w02.md` | D, E | ⬜ |
| 3 | `waves/w03.md` | F, G (needs F1 merged) | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `codex-tiers-vendors-layout` | F1 | 1 | medium | ⚠️ I1, I2, I3 |
| B | `codex-launch-rules` | F1 | 1 | medium | ⚠️ I5, I6 |
| C | `remove-driver-files` | F2 | 1 | low | ✅ |
| D | `codex-cli-rehearsal` | F1 | 2 | medium | ⬜ |
| E | `codex-desktop-rehearsal` | F1 | 2 | medium | ⬜ |
| F | `unattended-runs-readme` | F2 | 3 | medium | ⬜ |
| G | `driver-mentions-cleanup` | F2 | 3 | low | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/desktop-coordinator-p2`
and reach the main branch with each feature merge.

## User problems

- P2 — The same coordinator, `$wave-auto`, should work from the Codex CLI and the Codex desktop app → F1 ·
  `solutions/P2-codex-coordinator.md`
- P3 — One place in the docs says how to start an unattended run from the console and from the desktop apps of
  Claude Code and Codex → F2 · `solutions/lite.md` (low)
- P4 — Remove the Python overnight driver, now that the coordinator replaces it → F2 ·
  `solutions/P4-driver-removal.md`

## How to try

- F1 — in a scratch project with the skills installed (installer with the Codex links, or the Codex plugin), start
  `codex -m gpt-6.2-astra` or a new thread of the Codex desktop app with GPT-6.2-Astra and type `$wave-auto` and a
  list of two small changes → it prints `Capabilities:` with a GPT model ID per tier, asks its questions once, prints
  one line per step and ends with the features merged into `integration/<topic>`; `git log integration/<topic>`
  shows task commits with `Wave-Model: gpt-6.2-sol` or another GPT ID of the task's tier; before: a Codex agent could
  not name its model, so the tier gate stopped every medium and high step, and `wave-auto` named only Claude models.
- F2 — open `README.md`, section "Overnight runs" → "Unattended runs: wave-auto" has a table of where to start it
  (Claude Code CLI and desktop app, Codex CLI and desktop app), two lines for a start from a script, and "In the
  morning" without a driver; the folder `scripts/` is gone; before: the README taught `python scripts/wave_driver.py`
  and its morning `report.md`.

## Known test failures before start

- none (`main` at 56cd0f9, 2026-11-25: 39 status-check tests and 59 driver tests OK, all three examples pass,
  `git diff --check` clean); every task of waves 1 and 2 starts from it or from its feature branch

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
- Wave 3 waits for F1 merged: F2 edits `README.md`, `layout.md` and `CHANGELOG.md` on top of F1, and its README takes
  the Codex sandbox and permission mode from F1's rehearsal records.
- Codex shows no cost in USD; each rehearsal is capped at 3 hours instead.
- The plan runs in manual flow (no `Flow:` line): the user reviews F1 and F2.
