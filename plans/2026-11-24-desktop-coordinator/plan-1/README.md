# In-session coordinator: one command runs triage, plans and waves

- Plan: `plans/2026-11-24-desktop-coordinator/plan-1/` · slug: `desktop-coordinator-p1` · tracking branch: `plan/desktop-coordinator-p1` · created 2026-11-24 · base: 2abe5b3 · planned 2026-11-24 21:52 – 2026-11-24 22:08
- Index: `plans/2026-11-24-desktop-coordinator/index.md` part 1
- Re-plans:
  - 2026-11-24 at 01bfa8c, 22:40 – 22:43: entry I1 (navigator capped `halt` lines at four) → task J; wave 2 dropped
    before it ran, its tasks F, G, H, I moved to wave 3 as J, K, L, M so the rehearsals exercise the fixed navigator;
    details in `history.md`
  - 2026-11-25 at b3b69ff, 18:17 – 18:45: entries I2–I9 → tasks N, O, P, Q in new wave 4; the user chose a
    second CLI rehearsal (30 USD cap) and accepted the limits it cannot reach; details in `history.md` · fixes: F1 (I2, I3, I4, I5, I6, I7, I8, I9)
  - 2026-11-25 at be54998, 21:08 – 21:16: entries I13–I15, I18–I20, I26 → tasks R, S, T in new wave 5 (all high:
    round 2 of F1, evidence in the solution); the user chose a short CLI rehearsal of the fixes (8 USD cap); details
    in `history.md` · fixes: F1 (I13, I14, I15, I18, I19, I20, I26) · escalated: F1

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `in-session-coordinator` | One command, `/wave-auto`, runs triage, plans and waves in the current session, delegating every step to subagents | P1 | A (1), B (1), C (1), D (1), E (1), J (3), K (3), L (3), M (3), N (4), O (4), P (4), Q (4), R (5), S (5), T (5) | acceptance tests 1–10 of `solutions/P1-in-session-coordinator.md` hold: the contract texts of tasks A–E, J, K, N, R and S are in place, status-check and driver tests and the three examples pass, and the CLI (L, O, P, Q, T) and desktop (M) rehearsals are recorded with every expectation Pass, a finding with an open entry or Not run with its reason | ✅ merged | | `feat/desktop-coordinator-p1/F1-in-session-coordinator` | 8ce481d |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D, E | ✅ (I1 fixed by J, wave 3) |
| 2 | `waves/w02.md` | F, G, H, I | ➖ dropped (tasks → wave 3) |
| 3 | `waves/w03.md` | J, K, L (after J, K), M (after J, K) | ✅ (I3 accepted by the user) |
| 4 | `waves/w04.md` | N, O (after N), P (after N), Q (after N) | ✅ (I13–I15, I19, I20, I26 fixed in wave 5; I18 accepted by the user) |
| 5 | `waves/w05.md` | R, S, T (after R, S) | ✅ (I18, I27, I28 accepted by the user) |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `coordinated-runs-layout` | F1 | 1 | medium | ✅ |
| B | `coordinated-wave-run` | F1 | 1 | medium | ✅ |
| C | `coordinated-triage-phases` | F1 | 1 | medium | ✅ |
| D | `navigator-rules` | F1 | 1 | medium | ✅ (I1 fixed by J, wave 3) |
| E | `coordinator-skill` | F1 | 1 | medium | ✅ |
| F | `coordinated-plan-status` | F1 | 2 | low | ➖ superseded by J |
| G | `coordinator-install-docs` | F1 | 2 | low | ➖ superseded by K |
| H | `coordinator-cli-rehearsal` | F1 | 2 | medium | ➖ superseded by L |
| I | `coordinator-desktop-rehearsal` | F1 | 2 | medium | ➖ superseded by M |
| J | `coordinated-plan-status-halts` | F1 | 3 | low | ✅ |
| K | `wave-auto-install-docs` | F1 | 3 | low | ✅ (I6 verified by Q, wave 4) |
| L | `coordinator-cli-record` | F1 | 3 | medium | ✅ (I2, I4, I5 closed in wave 4; I3 accepted by the user) |
| M | `coordinator-desktop-record` | F1 | 3 | medium | ✅ (I4, I7, I8 fixed by N; I9 verified by O, P, Q; wave 4) |
| N | `coordinator-report-rules` | F1 | 4 | low | ✅ (I3 accepted by the user) |
| O | `coordinator-flow-rehearsal` | F1 | 4 | medium | ✅ (I13, I15 fixed by R, I14 by S, wave 5) |
| P | `coordinator-stops-rehearsal` | F1 | 4 | medium | ✅ (I19, I20 fixed by R, wave 5; I18 accepted by the user) |
| Q | `coordinator-triage-rehearsal` | F1 | 4 | medium | ✅ (I26 fixed by S, wave 5) |
| R | `coordinator-halt-claim-fixes` | F1 | 5 | high | ✅ (I18, I27 accepted by the user) |
| S | `status-triage-waiting-forms` | F1 | 5 | high | ✅ |
| T | `coordinator-fix-rehearsal` | F1 | 5 | high | ✅ (I28 accepted by the user) |

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
- none on `feat/desktop-coordinator-p1/F1-in-session-coordinator` at 01bfa8c (re-plan 1, 2026-11-24: the same
  checks green, `git diff --check main` clean); wave 3 starts from it
- none on the same branch at b3b69ff (re-plan 2, 2026-11-25: the same checks green); wave 4 starts from it
- none on the same branch at be54998 (re-plan 3, 2026-11-25: the same checks green); wave 5 starts from it

## Assumptions

- Skill name `wave-auto` (the index's working name); the coordinator always runs in autonomous flow and asks only
  in its start phase: the triage questions, a takeover of a stale coordinator claim, a switch of a manual plan to
  autonomous flow (user's answers in the index, P1 clarifications).
- A wave runs through task mode — prepare, one task subagent per task, resume — instead of a `wave-run` subagent with
  task subagents. Whether a subagent can start subagents depends on the environment (the CLI can, rehearsal H, entry
  I2), so the pipeline does not rely on it (re-plan 2; the user may ask for the other design).
- Known limits accepted by the user on 2026-11-25: the interactive TUI, an answer typed by a person, a first message
  of exactly `/wave-auto <list>`, permission modes other than `auto`, the cost in USD in the desktop app. Also not
  rehearsed: second desktop-app runs, a session fallback that starts a session, a `tier-mismatch` of a coordinated
  task.
- Task mode is improved for every user, not only the coordinator: the report block in the last commit's body, no
  redo of a committed task, fix requests through the wave file.
- The coordinator re-plans open entries found by its waves (`wave-plan <plan folder>`), bounded by "Re-plan
  escalation": at most two automatic re-plans per feature, the third waits for the user. The driver left re-plans to
  the user.
- The driver's guard on `main` is not carried over (the user may work on `main` during an interactive run); a
  coordinator claim `refs/wave-method/claims/auto/<name>` replaces its lock.
- Accepted by the user on 2026-11-25 as known limits of the coordinator's output (I3, I10–I12, I16, I17, I21–I25):
  skipped progress lines, extra remarks, the task ID as the unit of `task` lines, a changed `### Next` after an `until`
  rail, a `status` report not copied verbatim, end times a minute or two off. Seen with a `claude-sonnet-5-5`
  coordinator; an Opus-class one was not checked. A re-plan does not plan them.
- Re-plan 3 (round 2 of F1, escalated): the seven entries are fixed by wording (tasks R, S) and checked by a short
  CLI rehearsal (task T, 8 USD cap), the user's choice on 2026-11-25; all three tasks need an Opus-class model. A
  further entry of F1 makes its next re-plan round 3: held until the user gives `override F1: <direction>`.
- Accepted by the user on 2026-11-25 after wave 5 as known limits (I18, I27, I28): no `Resume:` line after a
  `triage-ask` without questions, and one table row of `wave-auto/SKILL.md` over 120 characters. F1 goes to review
  without a third re-plan.
- One feature: the coordinator, the coordinated modes of the four skills, installers and docs make sense only
  together. README and docs get only what F1 needs; the full docs are P3, the driver's removal P4 and Codex P2, all
  in part 2.
- The plan runs in manual flow (no `Flow:` line): the user reviews F1 before it reaches `main`.
