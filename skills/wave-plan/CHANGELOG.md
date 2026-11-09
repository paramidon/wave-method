# Wave skill set changelog

Releases are git tags `vMAJOR.MINOR.PATCH`; the release workflow copies the tag into `.claude-plugin/plugin.json`,
and no other file carries a version. Changes since the last tag go into a line
`- Unreleased — …` at the top; a release renames it to the tag and date.

- v2.11.0 (2026-11-09) — everything written to the repository is English, always, whatever language the user, the list or the
  existing project uses (`layout.md`, "Language"): each skill states the rule up front, the triage subagent prompt and
  the task header say it explicitly, and a non-English doc that a task changes is translated as a whole; only the
  user's verbatim words and product text the user asked for stay in another language. The chat stays in the user's
  language.
- v2.10.0 (2026-11-05) — a tier gate keeps tasks off weaker models (`layout.md`, "Tier gate"): every `medium` and `high` task
  prompt starts with `Required tier: …`; the executor names its own model first and, below the tier or unknown,
  stops `tier-mismatch` without touching anything (no one can waive it; only a re-plan lowers a task's complexity);
  task commits carry a `Wave-Model:` trailer and reports a `Model:` line; `wave-run` merges nothing whose commits
  lack the trailer or name a weaker model — the task becomes ⚠️ and runs again on its tier.
- v2.9.0 (2026-11-05) — every run of a wave skill shows its start and end time, read from the system clock (`layout.md`,
  "Run times"): the first line is `Started: <date time>`, the last line of the final report is
  `Started: … · Finished: … (<duration>)`; `wave-run` writes `Started` / `Finished` into the wave's Execution,
  `wave-plan` writes `planned <start> – <end>` into the README header (a re-plan into its `Re-plans:` item) and
  `wave-triage` writes `triaged <start> – <end>` into the index header.
- v2.8.0 (2026-11-04) — support for Google Antigravity and Gemini CLI is removed: no Antigravity plugin manifest, Gemini
  CLI extension or `commands/`; Gemini models are gone from the model tiers; the installers' Codex links option is
  `--no-codex` / `-NoCodex` again (`--no-agents` / `-NoAgents` no longer exist). A feature waiting for review is
  shown in a short review block (`layout.md`, "Feature review"), in `wave-run` and `/wave-status` alike: its
  essence and up to five feature-specific test steps with expected results, plus anything worth a look; no task
  list, check counts, diff statistics, review commands or build and launch steps. "How to try" lines and task
  `Try:` lines name only feature-specific actions.
- v2.7.0 (2026-11-04) — `/wave-status` shows each feature waiting for review with the same full brief as `wave-run`: what
  and why, what was done, how it was checked, how to test it, what is worth a look, commits and diff summary; for
  a plan run before v2.6.0 it builds the brief read-only from the README, the branch's commits and diff and the
  last wave's Execution.
- v2.6.0 (2026-11-04) — a finished feature is reported with what was done and how to test it, not only its title and
  branch: `wave-plan` writes a "How to try" line per feature (commands, actions, expected result); task reports add
  `Done:` and `Try:`; `wave-run` keeps each feature's review brief in `reviews/<feature>.md` on the tracking branch,
  wave by wave, adds numbered "How to test" steps, and prints the brief in full; `wave-status` and the `merge` form
  show the same brief.
- v2.5.0 (2026-11-03) — a re-plan that leaves a feature branch red no longer leaves earlier tasks of that feature
  with `Known failures: none`: it reads every wave file not run yet of the affected features, runs the tests on
  their branches, prefers fixing first, otherwise lists the red tests per branch in the README, the wave files and
  the prompts; `wave-run` does not count known failures from the wave file either, and stops `plan-defect` on an
  unlisted red test that an open entry names. Every search in a check names its paths, because the plan folder is
  on every branch.
- v2.4.0 (2026-11-01) — the skills also run in Google Antigravity and Gemini CLI: the repository installs as an
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
