# F2 · The Python overnight driver is removed; the README shows where to start an unattended run

- Branch: `feat/desktop-coordinator-p2/F2-driver-removal-docs` · worktree:
  `D:\Documents\orbits\wave-method.worktrees\desktop-coordinator-p2-F2`

## How to test

- C: open `docs/rehearsals/end-to-end-autonomous.md` and `docs/rehearsals/end-to-end-manual.md` → a "History:" note
  under the title says the driver was removed and `/wave-auto` replaces it; there is no top-level `scripts/` folder.
- Z: open `examples/README.md`, section "03 — a night run in autonomous flow" → the one line
  `/wave-auto until 07:00 plans/2026-11-04-wordstat-cli` stands where the two driver commands were.

## Tasks

- C (wave 1) — removed the Python driver, its tests and the docs that existed only for it; CI and the release archives
  no longer use it, and the two end-to-end rehearsal records are marked as history.
- Z (wave 13) — the last mentions of the deleted overnight driver are gone from the layout, the examples README and the
  unreleased changelog item, and the changelog says where to start an unattended run.
