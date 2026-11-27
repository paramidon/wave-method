# Open problems
Next ID: I34

- **[I24 · wave 13 / task Y / feature F2] The Codex desktop app row of "Where to run it" points to permissions guidance
  that does not exist** — where: `README.md:272` (target `README.md:87`); expected / got: the row says "permissions as
  Codex permissions says for the desktop app" / that section only says the desktop app is not rehearsed with the
  profile and says nothing about what to set there (`skills/wave-plan/layout.md`, "Permissions in Codex", neither);
  the text is the solution's own (`solutions/lite.md`, "P3"); proposal: reword the cell to say the desktop app's
  permissions are not rehearsed, or add one sentence to "### Codex permissions";
  status: → task AC (wave 15)
- **[I25 · wave 13 / task Y / feature F2] The script lines of "Unattended runs" work only in a POSIX shell** — where:
  `README.md:279-290`; expected / got: a reader on Windows can start a run from a script / in PowerShell
  `< /dev/null` is a parse error and `\$` does not escape `$`, and the README names no shell; proposal: say "bash or
  zsh" before the block, or add a PowerShell form of the Codex lines after trying it;
  re-plan 2026-11-27: Git Bash on Windows also turns the argument `/wave-auto …` into a Windows path, so the POSIX
  `claude` line fails there too (`solutions/lite.md`, "P5");
  status: → task AC (wave 15)
- **[I33 · wave 14 / task AB / feature F3] README gives a git command without the path, and it fails** — where:
  `README.md:93` on `feat/desktop-coordinator-p2/F3-codex-coordinator-polish`;
  expected / got: `git config --global --add safe.directory` works as written / git 2.52 stops with
  `error: wrong number of arguments, should be 2` (probed by the coordinator with `--file` on a scratch config); the
  text is the solution's own (`solutions/P2-codex-coordinator.md`, "Polish", "Task AB", edit 1);
  proposal: add `'<worktree path>'` at the end of the command;
  status: open
