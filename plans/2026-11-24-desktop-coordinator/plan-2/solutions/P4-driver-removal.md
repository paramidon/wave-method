# P4. Remove the Python overnight driver

User problem: the Python driver is no longer needed once `/wave-auto` runs in every app; remove it · feature F2

## Cause

Before part 1 the driver `scripts/wave_driver.py` (with `scripts/wavedriver/*.py`, tests `scripts/tests/*.py`) was the
only unattended path. Part 1's `wave-auto` replaces it in the Claude Code CLI and desktop app, part 2's F1 in Codex.
The repository still ships, tests and documents the driver: `.github/workflows/release.yml:41` (its unit tests) and
`:48` (`scripts` in the archives), `CONTRIBUTING.md:24`, `README.md` (lines 161-162, 225-260, 313-314, 348-351,
392-393, 405, 420-421, 424-425), `examples/README.md:72-79, 92`, `skills/wave-plan/layout.md:510-511`
("a driver's summary"), `skills/wave-plan/CHANGELOG.md:17-22` (its `- Unreleased` item announces it), the docs
`docs/wave-driver.md`, `docs/claude-print-mode.md`, `docs/rehearsals/print-mode-chain.md`,
`print-mode-fixture-chain.md`, `print-mode-multiwave.md`, and the records `docs/rehearsals/end-to-end-autonomous.md`
and `end-to-end-manual.md`, which ran it.

Checked on `main` at 56cd0f9: no skill file and nothing under `skills/` refers to `scripts/` other than
`skills/wave-plan/scripts/` (status check, stays); no other doc links to the files deleted here except each other.

## Approach

Delete the driver, its tests and the docs that exist only for it; keep the two end-to-end rehearsal records as history
with a note at the top (they also record the skills' behaviour, not only the driver's); rewrite the README's
unattended-run docs around `/wave-auto` (with P3's "where to run it"); drop the driver from the CI checks and release
archives. The `- Unreleased` changelog item announced the driver, which never reached a release (the last release is
v2.12.0), so its driver sentence is removed there instead of adding "removed" to the changelog.

Not chosen: moving the driver docs to an archive folder (git history keeps them, and an archive invites links to a tool
that no longer exists); keeping the driver as an optional tool (the user's decision, index P4).

## Removal (task C, wave 1)

1. `git rm -r scripts` (the whole folder: `wave_driver.py`, `wavedriver/`, `tests/`). `.github/scripts/` and
   `skills/wave-plan/scripts/` stay.
2. `git rm docs/wave-driver.md docs/claude-print-mode.md docs/rehearsals/print-mode-chain.md docs/rehearsals/print-mode-fixture-chain.md docs/rehearsals/print-mode-multiwave.md`.
3. `.github/workflows/release.yml`: delete line 41 (`python -m unittest discover -s scripts/tests -v`); line 48
   `paths="skills scripts install.sh install.ps1 LICENSE README.md docs .claude-plugin"` →
   `paths="skills install.sh install.ps1 LICENSE README.md docs .claude-plugin"`.
4. `CONTRIBUTING.md`: delete line 24 (`   python -m unittest discover -s scripts/tests`) from the checks block.
5. `docs/rehearsals/end-to-end-autonomous.md` and `docs/rehearsals/end-to-end-manual.md`: after the first line (the
   H1 title) insert a blank line and:

   ```
   > History: these runs used the Python overnight driver (`scripts/wave_driver.py`), which has since been removed from
   > the repository; `/wave-auto` replaces it (`skills/wave-auto/SKILL.md`). Its commands are kept as a record and no
   > longer run.
   ```

   Nothing else in these two files changes.

## README after the removal (task F, wave 3, after F1 is merged)

F1 has already edited `README.md` (Codex plugin install, tiers row, Requirements, the `wave-auto` section, Limitations);
start from that text. Line numbers below are those of `main` at 56cd0f9; find each place by its quoted text.

1. Example list, `` [`03-autonomous-night-run`](examples/03-autonomous-night-run/) — a plan written in autonomous flow and run
   overnight by the driver, with … `` → `… — a plan written in autonomous flow and run overnight with `/wave-auto`, with …`.
2. Replace the three subsections from `### One command in one session: wave-auto` through the end of `### In the
   morning` (up to, not including, `## Is this another SDLC?`) with:

   ````
   ### Unattended runs: wave-auto

   `/wave-auto <list>` (Codex: `$wave-auto <list>`) runs the whole pipeline in the session you type it in. It asks the
   triage questions once, at the start, then triages, plans every part and runs every wave in autonomous flow, each step
   as a subagent on a model of the step's tier, printing one line per step. It ends with the `wave-status` report:
   features merged into `integration/<topic>`, features waiting for your review, blocked features and what each waits
   for.

   - Start from a list, an index (`/wave-auto plans/<date>-<topic>/index.md`) or a plan folder.
   - Bound it with `until 07:00` or `steps 40` before the start: `/wave-auto until 07:00 plans/<…>/index.md`.
   - Nothing is kept in the chat: if the window closes or a usage limit stops the session, run
     `/wave-auto plans/<date>-<topic>/index.md` in a new session and it continues where it stopped.
   - A step that cannot run as a subagent of its tier runs in a separate session where the app can start one;
     otherwise the run stops with the command to run by hand.

   <P3 table and paragraphs: `solutions/lite.md`, "P3">

   ### In the morning

   1. Read the final report of `/wave-auto`, or run `/wave-status`: features merged into the integration branch with
      their review blocks, features waiting for your review, blocked features with their problem entries, and halted
      units with their next commands.
   2. Review the night's changes with `git diff main...integration/<name>`.
   3. In the main checkout, merge the integration branch with `git merge --no-ff integration/<name>`.
   4. To approve a feature under manual review, run `/wave-run <plan folder> merge F3`. That merges the feature
      into the integration branch. Merge that branch into `main` again.
   5. Re-plan blocked features with `/wave-plan <plan folder>`.

   `/wave-status` shows the same state, including `Merged, not in main:` until you merge the integration branch.
   You can also run `/wave-run <plan folder> <N>` yourself for each wave. Autonomous flow asks nothing either way.
   ````

   Keep the four bullets as F1 left them if F1 changed their wording; the first paragraph names no app any more (the
   table does).
3. "How it works", the skills table: add a last row
   `| `wave-auto` | Runs triage, plans and waves from one command in one session, each step as a subagent on a model of its tier; asks the triage questions once, at the start; autonomous flow. | high (Opus-class or GPT-6.2-Astra) |`
   and delete the paragraph after the table, `The separate overnight driver `scripts/wave_driver.py` chains … (see
   [Overnight runs](#overnight-runs-autonomous-flow)).`
4. Requirements: delete the bullet `- **The Claude Code CLI** (`claude`, signed in) for the overnight driver. …` (two
   lines), and replace the Python bullet with
   `- **Python 3.9+** is optional: only the status-check script `wave-plan/scripts/status_check.py` uses it. Without it,
   the check is done by reading.`
5. Safety rules, last bullet `- A claim ref allows one writer at a time on an integration branch. A lock file allows one
   driver per repository. The driver stops if `main`, a remote-tracking ref, or the main checkout changes.` →
   `- A claim ref allows one writer at a time on an integration branch, and another one `wave-auto` coordinator per
   index or plan.`
6. Customising: delete the row `| Driver models, caps and rails | … |`.
7. Limitations: `- **Autonomous flow and the driver** were rehearsed with Claude Code on Windows ([rehearsals](docs/rehearsals/)).
   The driver requires the Claude Code CLI and has no Codex counterpart.` → `- **Autonomous flow** was rehearsed with
   Claude Code on Windows ([rehearsals](docs/rehearsals/)).`; and `- **An overnight run consumes usage.** Set
   `--max-usd`, `--deadline`, or `--max-calls`. On a subscription, the run counts toward usage limits.` →
   `- **An unattended run consumes usage.** Bound it with `until` or `steps` of `/wave-auto`. On a subscription, the
   run counts toward usage limits.`

Lines stay at most 120 characters; a blank line before and after every table, list and fenced block.

## Last edits (task G, wave 3)

1. `skills/wave-plan/layout.md`, "Results of an autonomous run": `(the `wave-run` report, `wave-status`, the `wave-auto`
   final report, a driver's summary):` → `(the `wave-run` report, `wave-status`, the `wave-auto` final report):`
   (rewrap the paragraph to at most 120 characters).
2. `examples/README.md`, section "03 — a night run in autonomous flow":
   - `For the night run, preview the driver calls and then start the run with a $10 limit:` and the fenced block of two
     `python <wave-method>/scripts/wave_driver.py …` lines → `For the night run, start the coordinator in a Claude Code
     or Codex session (Codex: `$wave-auto …`) and bound it by time:` and a fenced block with the one line
     `/wave-auto until 07:00 plans/2026-11-04-wordstat-cli`.
   - `In the morning, `report.md` shows review blocks for …` → `In the morning, the final report of `/wave-auto` (or
     `/wave-status`) shows review blocks for …` (the rest of the sentence stays).
   - `To run without the driver, enter each command in a fresh session.` → `To run without `wave-auto`, enter each
     command in a fresh session.`
3. `skills/wave-plan/CHANGELOG.md`, the `- Unreleased` item: delete the sentence that starts
   `New `scripts/wave_driver.py` (Python 3.9+, standard library only)` and ends `print-mode findings in
   `docs/claude-print-mode.md`).`; in the next sentence delete `; release archives include `scripts/``, so it reads
   `` `status_check.py` checks the `Flow:` line (`flow-line`, `flow-review-unknown`); new example `examples/03-autonomous-night-run/`. ``;
   rewrap the item's lines to at most 120 characters, two-space continuation indent. Then append to the end of the
   item (after F1's Codex sentences):

   ```
     README shows where to start an unattended run: the CLI or desktop app of Claude Code or Codex, interactive or
     from a script.
   ```

## Limits

- Old releases' archives still contain `scripts/`; a user of an old release keeps the driver of that release.
- The two end-to-end records keep driver commands that no longer run; their note says so.

## Acceptance tests

1. `test ! -e scripts` and `test ! -e docs/wave-driver.md`; the three `print-mode-*.md` and `docs/claude-print-mode.md`
   are gone (task C).
2. `git grep -n -E "wave_driver|wavedriver|wave-driver|claude-print-mode|print-mode-|scripts/tests|max-usd|max-calls" -- README.md CONTRIBUTING.md examples skills .github docs install.sh install.ps1 .claude-plugin`
   prints lines only of `docs/rehearsals/end-to-end-autonomous.md` and `docs/rehearsals/end-to-end-manual.md`, each of
   which starts with the history note (after task G).
3. `python skills/wave-plan/scripts/test_status_check.py` OK; the three example status checks exit 0;
   `git diff --check main` clean.
4. Every relative link in `README.md` and `examples/README.md` points to a file that exists:
   `grep -o -E '\]\([^)#]+' README.md examples/README.md` → each target exists relative to its file (task F, G).
