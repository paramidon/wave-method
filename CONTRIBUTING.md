# Contributing

Thanks for helping. The skills are prompts, so a small wording change can change behaviour; please keep changes
focused and explain the failure they fix.

## Before you open a pull request

1. **Describe the run that went wrong**: which skill, which step, what the agent did, what it should have done.
   A link to a plan folder or an excerpt of its "Execution" section helps most.
2. **Keep the single sources of truth.** Layout, statuses, reading rules, model tiers, names, commands and Markdown
   rules live in `skills/wave-plan/layout.md`; the difficulty scale lives in `skills/wave-triage/difficulty.md`;
   templates live in `skills/wave-plan/templates.md`. Other files refer to them instead of repeating them.
3. **Raise the version.** Every file of the set carries `Wave skill set version N` (the script:
   `SKILL_SET_VERSION`). Any change raises N in all of them and adds one line to `skills/wave-plan/CHANGELOG.md`.
   Set `version` in `.claude-plugin/plugin.json` to `N.0.0` too, or plugin users will not get the update.
   Refer to other skill files by paths relative to the skills folder (`wave-plan/layout.md`), never
   `.claude/skills/...`.
4. **Write skill text in English**, in short imperative sentences, with a blank line before and after every table,
   list and fenced block.
5. **Run the checks**:

   ```bash
   python skills/wave-plan/scripts/test_status_check.py
   python skills/wave-plan/scripts/status_check.py examples/01-greenfield-todo-cli
   git diff --check
   ```

## Releasing

1. Make sure `version` in `.claude-plugin/plugin.json` is the release version and its major number equals the skill
   set version.
2. Tag the commit on `main` and push the tag:

   ```bash
   git tag v2.0.0
   git push origin v2.0.0
   ```

The `Release` workflow runs only for tags `vMAJOR.MINOR.PATCH`. It checks the versions, runs the checks, and
publishes a GitHub release with `.zip` and `.tar.gz` archives and `SHA256SUMS`. Plugin users get the update from the
default branch whatever the tag; the tag and archives are for pinned and manual installs.

## Dogfooding

The skill set is maintained with itself: larger changes are planned with `/wave-plan` and executed with
`/wave-run`, and small, self-contained example plans live under `examples/`.
