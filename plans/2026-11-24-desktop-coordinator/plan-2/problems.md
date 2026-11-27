# Open problems
Next ID: I36

- **[I33 · wave 14 / task AB / feature F3] README gives a git command without the path, and it fails** — where:
  `README.md:93` on `feat/desktop-coordinator-p2/F3-codex-coordinator-polish`;
  expected / got: `git config --global --add safe.directory` works as written / git 2.52 stops with
  `error: wrong number of arguments, should be 2` (probed by the coordinator with `--file` on a scratch config); the
  text is the solution's own (`solutions/P2-codex-coordinator.md`, "Polish", "Task AB", edit 1);
  proposal: add `'<worktree path>'` at the end of the command;
  re-plan 2026-11-27 (round 2 of F3): confirmed by running git, and the `-c` form works
  (`solutions/P2-codex-coordinator.md`, "Evidence (re-plan 2026-11-27, round 2)");
  status: → task AE (wave 16)
