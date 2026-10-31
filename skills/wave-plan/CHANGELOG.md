# Wave skill set changelog

Releases are git tags `vMAJOR.MINOR.PATCH`; the release workflow copies the tag into `.claude-plugin/plugin.json`,
and no other file carries a version. Changes since the last tag go into a line
`- Unreleased — …` at the top; a release renames it to the tag and date.

- Unreleased — the skills also run in Google Antigravity and Gemini CLI: the repository installs as an
  Antigravity plugin (`plugin.json`) and a Gemini CLI extension (`gemini-extension.json`, `/wave-*` commands in
  `commands/`), the installers' `.agents/skills/` links serve Codex, Antigravity and Gemini CLI (`--no-agents` /
  `-NoAgents`, the old `--no-codex` still works), and the model tiers name Gemini models for every tier.
- v2.3.0 (2026-10-31) — `wave-run` offers each feature under review with a review brief: what the feature is and
  which user problems it solves (before → after), what each task did, how it was checked, and what is worth a look;
  the merge question names what the feature changes in one line.
- v2.2.0 (2026-10-31) — a feature waiting for the user's review is `👀 review` instead of the green `✅ ready`, so it no
  longer looks like a merged one (an old `✅ ready` reads as `👀 review`); the `wave-status` feature table gains a
  `Branch` column, and the `wave-run` report shows the branch in its feature table and a `Review branch:` line
  per feature under review.
- v2.1.0 (2026-10-31) — `wave-run` no longer merges features on its own: a finished feature becomes `✅ ready`
  (`Waiting for: review`) and is offered on its own branch with review commands; it is merged only when the user
  approves it (`merge F1` in the session, `/wave-run <plan> merge <F-IDs>`, or their own `git merge`); review
  findings become problem entries. `deferred-merges.md` is replaced by `merge.md`; a wave that needs another
  feature names `F<k> merged` in `Depends on:` and stops `feature-unmerged` until it is merged.
- v2.0.5 (2026-10-31) — `wave-status` leads with feature status (a count per status, a table with task progress and
  merge hash) before the wave line.
- v2.0.4 (2026-10-29) — the release workflow writes the tag's version into `version` of `.claude-plugin/plugin.json`
  on `main` and into the archives, so Claude Code shows the release version and offers the update.
- v2.0.3 (2026-10-29) — the changelog no longer lists the deleted tag v2.0.1.
- v2.0.2 (2026-10-29) — the version lives only in the release tag: version lines, `skills: vN` in plan and index
  headers, `SKILL_SET_VERSION` and the plugin `version` field are removed.
- v2.0.0 (2026-10-29) — skill file paths are relative to the wave skills folder instead of `.claude/skills/`, so the
  set also works as a Claude Code plugin.
- v1 (2026-10-29) — first public version (untagged).
