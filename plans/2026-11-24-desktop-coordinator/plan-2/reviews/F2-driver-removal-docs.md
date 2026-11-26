# F2 · The Python overnight driver is removed; the README shows where to start an unattended run

- Branch: `feat/desktop-coordinator-p2/F2-driver-removal-docs` · worktree:
  `D:\Documents\orbits\wave-method.worktrees\desktop-coordinator-p2-F2`

## How to test

- C: open `docs/rehearsals/end-to-end-autonomous.md` and `docs/rehearsals/end-to-end-manual.md` → a "History:" note
  under the title says the driver was removed and `/wave-auto` replaces it; there is no top-level `scripts/` folder.

## Tasks

- C (wave 1) — removed the Python driver, its tests and the docs that existed only for it; CI and the release archives
  no longer use it, and the two end-to-end rehearsal records are marked as history.
