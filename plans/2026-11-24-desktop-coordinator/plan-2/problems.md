# Open problems
Next ID: I24

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
