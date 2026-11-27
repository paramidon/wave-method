# F2 · The Python overnight driver is removed; the README shows where to start an unattended run

- Branch: `feat/desktop-coordinator-p2/F2-driver-removal-docs` · worktree:
  `D:\Documents\orbits\wave-method.worktrees\desktop-coordinator-p2-F2`
- 👀 review since 2026-11-27 22:03

## Essence

The Python overnight driver is removed: before, the README taught `scripts/wave_driver.py` and its morning report;
after, an unattended run is `/wave-auto` (`$wave-auto` in Codex), and the README shows where to start it.

## How to test

1. Open `README.md`, "Unattended runs: wave-auto", "Where to run it" → a table of four starts (Claude Code and Codex,
   CLI and desktop app); the Codex desktop app row says it is not rehearsed.
2. Read on below that table → separate script lines for bash or zsh and for PowerShell, a note for Git Bash on Windows,
   and the sentence that none of these lines has been run.
3. Go to "In the morning" in the same section → five steps that start from the `/wave-auto` report, with no driver.
4. Open `docs/rehearsals/end-to-end-autonomous.md` and `end-to-end-manual.md` → a "History:" note under the title says
   the driver was removed; the top-level `scripts/` folder is gone.
5. Open `examples/README.md`, "03 — a night run in autonomous flow" → one `/wave-auto until 07:00 …` line stands where
   the two driver commands were.

## Worth a look

- The script lines were never run in Claude Code or Codex (your choice at the re-plan of 2026-11-27); the starts of the
  table were not repeated and the section was not viewed as GitHub renders it (accepted the same day).
- The release workflow no longer runs the driver tests, and release archives no longer hold `scripts/`.

## Tasks

- C (wave 1) — removed the Python driver, its tests and the docs that existed only for it; CI and the release archives
  no longer use it, and the two end-to-end rehearsal records are marked as history.
- Z (wave 13) — the last mentions of the deleted overnight driver are gone from the layout, the examples README and the
  unreleased changelog item, and the changelog says where to start an unattended run.
- Y (wave 13) — the README describes unattended runs with `/wave-auto` instead of the driver: where to start one, the
  script lines and the steps for the morning (its two text defects were fixed by AC).
- AC (wave 15) — fixed the Codex desktop app row and gave script lines for bash or zsh and for PowerShell.
- AD (wave 15) — rewrapped the examples README paragraph and the changelog item; no word changed.
- F, G, J, K, Q, R, V, W — ➖ superseded by later tasks of this feature.

## Check

`python skills/wave-plan/scripts/test_status_check.py`; `status_check.py` on each of `examples/*/`;
`git diff --check main` → on 992c6e7: 39 tests OK, three examples pass, diff check clean; tests added or changed: none
(the driver's tests are deleted with the driver).
