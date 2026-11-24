# In-session coordinator: one command runs triage, plans and waves

- Plan: `plans/2026-11-24-desktop-coordinator/plan-1/` · slug: `desktop-coordinator-p1` · tracking branch: `plan/desktop-coordinator-p1` · created 2026-11-24 · base: 2abe5b3 · planned 2026-11-24 21:52 – 2026-11-24 22:08
- Index: `plans/2026-11-24-desktop-coordinator/index.md` part 1
- Re-plans: none

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `in-session-coordinator` | One command, `/wave-auto`, runs triage, plans and waves in the current session, delegating every step to subagents | P1 | A (1), B (1), C (1), D (1), E (1), F (2), G (2), H (2), I (2) | acceptance tests 1–7 of `solutions/P1-in-session-coordinator.md` hold: the contract texts of tasks A–G are in place, status-check and driver tests and the three examples pass, and the CLI (H) and desktop (I) rehearsals are recorded with every expectation Pass or a finding with an open entry | 🔄 | wave 1 | `feat/desktop-coordinator-p1/F1-in-session-coordinator` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D, E | ⚠️ I1 |
| 2 | `waves/w02.md` | F, G, H (after F, G), I (after F, G) | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `coordinated-runs-layout` | F1 | 1 | medium | ✅ |
| B | `coordinated-wave-run` | F1 | 1 | medium | ✅ |
| C | `coordinated-triage-phases` | F1 | 1 | medium | ✅ |
| D | `navigator-rules` | F1 | 1 | medium | ⚠️ I1 |
| E | `coordinator-skill` | F1 | 1 | medium | ✅ |
| F | `coordinated-plan-status` | F1 | 2 | low | ⬜ |
| G | `coordinator-install-docs` | F1 | 2 | low | ⬜ |
| H | `coordinator-cli-rehearsal` | F1 | 2 | medium | ⬜ |
| I | `coordinator-desktop-rehearsal` | F1 | 2 | medium | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/desktop-coordinator-p1`
and reach the main branch with each feature merge.

## User problems

- P1 — Autonomous runs work only from the CLI through the Python driver; a new skill started in an interactive
  Claude Code session (CLI or desktop app) should itself be the coordinator: ask the triage questions once, then
  triage, plan and run the waves in subagents, handing work between them → F1 ·
  `solutions/P1-in-session-coordinator.md`

## How to try

- F1 — in the Claude Code desktop app (Code tab) or an interactive `claude`, in a scratch project with the skills
  installed, type `/wave-auto` and a list of two or three small changes → it asks its clarifying questions once,
  then prints one line per step (triage, plan, each wave, each task) and ends with a status report in which the
  features are merged into `integration/<topic>`; close the session mid-run and type
  `/wave-auto plans/<date>-<topic>/index.md` in a new one → it continues where it stopped; before: only
  `python scripts/wave_driver.py` chained the steps, from a terminal, and it never triaged.

## Known test failures before start

- none (`main` at 2abe5b3, 2026-11-24: 39 status-check tests and 59 driver tests OK, all three examples pass)

## Assumptions

- Skill name `wave-auto` (the index's working name); the coordinator always runs in autonomous flow and asks only
  in its start phase: the triage questions, a takeover of a stale coordinator claim, a switch of a manual plan to
  autonomous flow (user's answers in the index, P1 clarifications).
- A wave runs through task mode — prepare, one task subagent per task, resume — instead of a `wave-run` subagent with
  task subagents, because a subagent cannot start subagents (to be confirmed by probe P0 of task H; the design works
  either way).
- Task mode is improved for every user, not only the coordinator: the report block in the last commit's body, no
  redo of a committed task, fix requests through the wave file.
- The coordinator re-plans open entries found by its waves (`wave-plan <plan folder>`), bounded by "Re-plan
  escalation": at most two automatic re-plans per feature, the third waits for the user. The driver left re-plans to
  the user.
- The driver's guard on `main` is not carried over (the user may work on `main` during an interactive run); a
  coordinator claim `refs/wave-method/claims/auto/<name>` replaces its lock.
- One feature: the coordinator, the coordinated modes of the four skills, installers and docs make sense only
  together. README and docs get only what F1 needs; the full docs are P3, the driver's removal P4 and Codex P2, all
  in part 2.
- The plan runs in manual flow (no `Flow:` line): the user reviews F1 before it reaches `main`.
