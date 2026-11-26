# Open problems
Next ID: I30

- **[I12 · wave 2 / task D / feature F3] The Codex coordinator leaves the fixed output texts** — where: `skills/wave-auto/SKILL.md:41`, `:51-53`, `:225`, `:232`, `:236`, `:244`; run X2;
  expected / got: `Started:` first, the given title, return lines, `next:` in Halts, the real start in `Continue:` / a preamble, an invented title, a retold result, no `next:`, a placeholder `<original list>`;
  proposal: tighten these rules at the next `wave-auto` edit and check them again in Codex;
  wave 7: not verified, no coordinator ran (I21);
  wave 9 (task T, check 8): title, Result cells, Halts and `Continue:` are now right; still: the first `Started:`
  line has no time and a second one follows (T2; `skills/wave-plan/layout.md:48-49`, `skills/wave-auto/SKILL.md:53`),
  and the coordinator adds sentences of its own and repeats the questions as a table (T3;
  `skills/wave-auto/SKILL.md:51-54`); proposal: forbid any output before the clock is read, show a first line with a
  date, and forbid text of its own;
  re-plan round 4: moved from F1 to the new feature F3 by the user's direction;
  status: → task AA (wave 14)
- **[I22 · wave 9 / task T / feature F3] In `codex exec` the coordinator's questions first go to
  `request_user_input_async`** — where: `skills/wave-auto/SKILL.md:129`; finding T4 in
  `docs/rehearsals/coordinator-codex-cli.md`; expected / got: all questions in one message, then wait / the tool call
  and two 60 s sleeps first, two minutes lost in a non-interactive run;
  proposal: say in the Codex column of "Vendors" that questions are asked as the text of the answer, without an input
  tool; re-plan round 4: moved from F1 to the new feature F3 by the user's direction;
  status: → task AA (wave 14)
- **[I23 · wave 9 / task T / feature F3] Git in the user's own shell refuses the worktrees Codex made in its Windows
  sandbox** — where: `README.md:62-87`, `skills/wave-plan/layout.md:211`; finding T5 in
  `docs/rehearsals/coordinator-codex-cli.md`; expected / got: the user reviews the feature branches in those worktrees
  / they belong to the account `CodexSandboxOffline` and `git status` stops with `detected dubious ownership`;
  proposal: describe it in "Codex permissions" and "Permissions in Codex" (`safe.directory`, or review through the
  main checkout), or check whether it can be avoided; re-plan round 4: moved from F1 to the new feature F3 by the user's direction;
  status: → task AB (wave 14)
- **[I24 · wave 13 / task Y / feature F2] The Codex desktop app row of "Where to run it" points to permissions guidance
  that does not exist** — where: `README.md:272` (target `README.md:87`); expected / got: the row says "permissions as
  Codex permissions says for the desktop app" / that section only says the desktop app is not rehearsed with the
  profile and says nothing about what to set there (`skills/wave-plan/layout.md`, "Permissions in Codex", neither);
  the text is the solution's own (`solutions/lite.md`, "P3"); proposal: reword the cell to say the desktop app's
  permissions are not rehearsed, or add one sentence to "### Codex permissions";
  status: open
- **[I25 · wave 13 / task Y / feature F2] The script lines of "Unattended runs" work only in a POSIX shell** — where:
  `README.md:279-290`; expected / got: a reader on Windows can start a run from a script / in PowerShell
  `< /dev/null` is a parse error and `\$` does not escape `$`, and the README names no shell; proposal: say "bash or
  zsh" before the block, or add a PowerShell form of the Codex lines after trying it;
  status: open
- **[I26 · wave 13 / task Y / feature F2] The script lines of the README were not run** — where: `README.md:279-290`;
  expected / got: `claude -p`, `claude -p --continue`, `codex exec` and `codex exec resume --last` work as written /
  none was run, since each would start a real run; proposal: try them once in a scratch project, or accept;
  status: open
- **[I27 · wave 13 / task Y / feature F2] The starts of the "Where to run it" table were not repeated** — where:
  `README.md:267-272`; expected / got: each of the four starts behaves as its row says / not repeated by this task
  (README "Limitations" says what earlier rehearsals covered; the Codex desktop app never was); proposal: accept;
  status: open
- **[I28 · wave 13 / task Y / feature F2] The new README section was not viewed as GitHub renders it** — where:
  `README.md`, "Unattended runs: wave-auto"; expected / got: table, links and code blocks render / the branch is not
  pushed; proposal: look at it after the user pushes, or accept;
  status: open
