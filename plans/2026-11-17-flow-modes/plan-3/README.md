# Flow modes, part 3: overnight driver

- Plan: `plans/2026-11-17-flow-modes/plan-3/` · slug: `flow-modes-p3` · tracking branch: `plan/flow-modes-p3` · created 2026-11-17 · base: 79e9d9c · planned 2026-11-17 23:43 – 2026-11-17 23:56
- Index: `plans/2026-11-17-flow-modes/index.md` part 3
- Re-plans:
  - 2026-11-18 at 790870a, 00:08 – 00:11: I1 → wave 1's check split into a baseline check and the task check; no new P, task or wave; details in `history.md`

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `overnight-driver` | Overnight driver with rails and a morning report | P6 | A (1), B (1), C (1), D (1), E (2), F (2), G (3), H (3) | the tests of acceptance items A–G pass, including the nine end-to-end scenarios of task G against the fake claude; `docs/wave-driver.md` has its nine sections; the check command is green | 🔄 in progress | wave 1 | `feat/flow-modes-p3/F1-overnight-driver` | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C, D | 🔄 since 2026-11-18 01:19 |
| 2 | `waves/w02.md` | E, F | ⬜ |
| 3 | `waves/w03.md` | G, H | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `driver-git-state` | F1 | 1 | medium | 🔄 |
| B | `claude-call-runner` | F1 | 1 | medium | 🔄 |
| C | `driver-rails-guard` | F1 | 1 | medium | 🔄 |
| D | `fake-claude-stub` | F1 | 1 | medium | 🔄 |
| E | `next-action-choice` | F1 | 2 | medium | ⬜ |
| F | `morning-report-render` | F1 | 2 | medium | ⬜ |
| G | `driver-loop-cli` | F1 | 3 | medium | ⬜ |
| H | `driver-doc-ci` | F1 | 3 | low | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/flow-modes-p3` and reach the
main branch with each feature merge.

## User problems

- P6 — a cross-platform driver (Python 3.9+, stdlib only) in `scripts/` plus a short doc: reads plan state from git
  (reusing the status check), picks the next step (plan a part, run a wave) or stops, runs each step as a fresh
  headless Claude session with the model of its tier, parses the stop line to continue, skip to independent work or
  halt, has rails (max calls, failures in a row, deadline, usage-limit stop, a lock, a log), never pushes, never
  touches the main branch, and writes a morning report with the exact review and merge commands → F1 ·
  `solutions/P6-overnight-driver.md`

## How to try

- F1 — in a project with an autonomous index or plan, run `python <wave-method>/scripts/wave_driver.py <index or plan folder> --repo <project> --dry-run` → it prints the next call (`/wave-plan flow autonomous … part <K>` or `/wave-run <plan folder> <N>`) with its model and caps and calls nothing; without `--dry-run` it runs the calls one after another and ends with `Report: <path>`, whose `report.md` shows merged features as merged blocks, features under review, blocked ones with their entries, halts with their `next:`, a table of every call with cost, and the exact `git diff <main>...integration/<name>` and `git merge --no-ff integration/<name>` commands; a second driver on the same repository exits 3 naming the first; before: every step was a session the user started by hand.

## Known test failures before start

- none (`main` at 79e9d9c, 2026-11-17: `test_status_check.py` 20 tests OK, both examples pass `status_check.py`, `git diff --check` clean)
- `python -m unittest discover -s scripts/tests -v` cannot run before wave 1: `scripts/tests/` does not exist on
  `feat/flow-modes-p3/F1-overnight-driver` until tasks A–D add it, so wave 1's baseline check leaves it out
  (`waves/w01.md`, re-plan 1)

## Assumptions

- P6 is one feature: the modules are useless apart; they are split into tasks only so they can run in parallel.
- The driver lives in the repository root `scripts/` (the user's words) and runs against a project with `--repo`;
  it imports `status_check.py` from the same wave-method folder. The plugin ships the whole repository, so plugin
  installs have it; the installers stay unchanged, and part 4 (P8) documents installation in README.
- The driver starts from an existing index or plan folder (index answer, 2026-11-17); it never runs `wave-triage`,
  a re-plan, the merge form or the flow form: those are the user's decisions, and the report gives their commands.
- Plans in manual flow are halted, not switched: the driver plans index parts with `flow autonomous`, so the parts it
  plans are autonomous; a plan the user planned in manual flow needs the user's flow form first.
- Permission mode defaults to `auto` (passed every step in `docs/claude-print-mode.md`, Q-a), because the driver runs
  in the user's own repository; `bypassPermissions` is an option for isolated clones. Part 4's end-to-end test (P9)
  runs it for real.
- "Never push, never touch the main branch" is enforced by a guard: `refs/heads/<main branch>`, every
  `refs/remotes/*` and the main checkout's branch and tracked status must be unchanged after each call, else the run
  ends.
- A deadline stops new calls and never cuts a running one; the per-call timeout (default 120 min) does.
- Tasks waiting for task mode are run by the driver only when they have no `Needs` (headless sessions may lack the
  tool); the model is the task's tier from `DEFAULT_MODELS` or the options.
- The tests use a fake `claude` (task D); real `claude -p` runs of the driver are part 4's end-to-end test (P9).
- No task needs a high-tier model: the design decisions are in the solution file, every task implements a fixed API.
