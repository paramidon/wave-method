# P9. End-to-end runs of both flows on scratch repositories
User problem: on a throwaway repository, never a real project, one run in manual flow (must behave as before) and
one in autonomous flow with a forced red task and a feature that must stay blocked; report what actually happened,
including what could not be verified · feature F2

**Cause:** the skills are prose; only `status_check.py` and the driver (`scripts/tests/`, a fake `claude`) have
tests. Part 2's rehearsals (`docs/rehearsals/*.md`) ran single skills and chains in print mode, and part 3 tested
the driver against a stub. Nothing has run the merged skills and the real driver end to end, and nothing has
compared manual flow with the release before flow modes (`v2.12.0`).

**Approach:** two independent runs, one task each, each in its own scratch folder outside every repository, each
writing one record in `docs/rehearsals/`:

- **Manual (task E)** runs `examples/01-greenfield-todo-cli/` by hand-typed `claude -p` calls, the way a user
  works in manual flow, twice: with the skills of the task's working folder ("current") and with the skills of tag
  `v2.12.0` ("baseline"), and compares the observable results step by step.
- **Autonomous (task F)** runs `examples/03-autonomous-night-run/` (F1 of this plan) with the real driver,
  `scripts/wave_driver.py`, after seeding a forced failure that makes task D red, then plays the user's morning.

A step whose result differs from the expectation below is a **finding**, not a failure of the task: record it with
what was expected, what happened and where (log file, commit, line). The task changes no skill, script or example to
make a step pass; its report lists every finding as a problem for the coordinator.

## Common rules

- **Scratch only.** `scratch=$(mktemp -d)`; every repository, venv, log and driver output lives under it. Never run
  a skill, the driver or a git write command in the task's own working folder or in any other repository on the
  machine. Before the first call and after the last one, record
  `git -C <working folder> for-each-ref --format='%(refname) %(objectname)'`: the two lists must be equal except
  for the task's own branch.
- **Shell.** Git Bash on Windows (POSIX `sh` elsewhere). Every `claude` call:

  ```bash
  MSYS_NO_PATHCONV=1 timeout 3600 claude -p "<prompt>" --output-format stream-json --verbose \
    --permission-mode bypassPermissions --setting-sources project,local --model <model> \
    --max-turns <turns> --max-budget-usd <usd> < /dev/null > "$scratch/logs/<step>.jsonl" 2> "$scratch/logs/<step>.err"
  ```

  `MSYS_NO_PATHCONV=1` keeps Git Bash from rewriting `/wave-run` into a Windows path; `--setting-sources
  project,local` keeps the user's installed `wave-method` plugin (an older release) out, so only the skills installed
  in the scratch repository load (`docs/claude-print-mode.md`). Read the **last** `result` event of the stream: the
  CLI may print an earlier interim result (`docs/rehearsals/print-mode-fixture-chain.md`, C2).
- **Per call, record:** the command, exit code, model, `num_turns`, `total_cost_usd` of the last result, wall
  minutes, the first and the last line of the last result's text, its stop line if any, and a snapshot before and
  after: `git -C "$scratch/<repo>" for-each-ref --format='%(refname) %(objectname)'` and
  `git -C "$scratch/<repo>" worktree list --porcelain`.
- **Costs.** Sum the last `total_cost_usd` of every call. Task E stops starting calls at 20 USD, task F at 25 USD
  (the driver's own `--max-usd` included); a step not run for this reason is recorded as not run.
- **Seeding a repository** `<repo>` from a plan folder `<example>` with skills from `<skills source>`:

  ```bash
  git init -b main "$scratch/<repo>"
  git -C "$scratch/<repo>" config user.name "wave e2e"
  git -C "$scratch/<repo>" config user.email "e2e@example.invalid"
  printf 'MIT\n' > "$scratch/<repo>/LICENSE"; git -C "$scratch/<repo>" add LICENSE; git -C "$scratch/<repo>" commit -qm init
  sh "<skills source>/install.sh" "$scratch/<repo>" --no-codex
  git -C "$scratch/<repo>" add .claude; git -C "$scratch/<repo>" commit -qm "install wave skills"
  mkdir -p "$scratch/<repo>/plans"; cp -r "<example>" "$scratch/<repo>/plans/<plan folder name>"
  git -C "$scratch/<repo>" add plans; git -C "$scratch/<repo>" commit -qm "add plan"
  git -C "$scratch/<repo>" branch plan/<slug>
  ```

  The branch `plan/<slug>` stands for the tracking branch that `wave-plan` keeps; `wave-run` creates its worktree.
- **Python for the projects:** `python -m venv "$scratch/venv"`, then `"$scratch/venv/Scripts/python" -m pip install
  pytest pyyaml` (`bin/` instead of `Scripts/` outside Windows); prepend that folder to `PATH` for every call.

## Manual run (task E)

Plan: `examples/01-greenfield-todo-cli/` → `plans/2026-11-02-todo-cli`, slug `todo-cli`, no `Flow:` line. Two
repositories, seeded as above: `cur` with skills source = the task's working folder, `base` with skills source =
`$scratch/v2120`, made by `git -C <working folder> archive v2.12.0 skills install.sh | tar -x -C "$scratch/v2120"`.
Run the chain on `cur` first, then on `base`; models and caps are the same for both.

| Step | Command (in the repository's main checkout) | Model, turns, USD |
|---|---|---|
| M0 | `python <working folder>/skills/wave-plan/scripts/status_check.py plans/2026-11-02-todo-cli` | — |
| M1 | `python <working folder>/scripts/wave_driver.py plans/2026-11-02-todo-cli --repo . --dry-run` (`cur` only) | — |
| M2 | `/wave-run plans/2026-11-02-todo-cli 1` | sonnet, 400, 8 |
| M3 | `/wave-run plans/2026-11-02-todo-cli merge F2` | sonnet, 100, 3 |
| M4 | `/wave-run plans/2026-11-02-todo-cli 2` | sonnet, 400, 8 |
| M5 | `/wave-run plans/2026-11-02-todo-cli merge F1 F3` | sonnet, 100, 3 |
| M6 | `python -m pytest -q` in the main checkout, then `/wave-status` | haiku, 60, 0.5 |

M3 and M5 are the user's approvals; nothing else may merge into `main`.

Expectations (each a Pass or a Finding in the record):

- M0: exit 0, no output. M1: exit 0, one line
  `next: nothing — plans/2026-11-02-todo-cli: manual flow: the driver runs autonomous plans only`, and no folder
  `$scratch/cur.wave-driver`.
- M2: the last result opens with `Started:`; wave 1 ✅, A and C ✅, F2 `👀 review` with its review block, F1 🔄
  waiting for wave 2; the result ends with a question about merging F2 (manual flow asks). `main` is unchanged,
  no `integration/*` branch and no `refs/wave-method/claims/*` ref exist, and the README on `plan/todo-cli` has no
  `Flow:` line. Current only: the report shows `Flow: manual`.
- M3: `main` gained only merge commits (`git rev-list --no-merges --first-parent <main before>..main` is empty), one
  of which merges `feat/todo-cli/F2-usage-readme`; F2 `✅ merged` with that hash.
- M4: wave 2 ✅, B and D ✅, F1 and F3 `👀 review`, a question about merging them; `main` unchanged by M4.
- M5: as M3 for both features; every feature `✅ merged`; the plan is archived as `wave-plan/layout.md`
  ("Archive") says; `python -m pytest -q` passes (the 11 cases of P1 and P2 of the example).
- M6: `/wave-status` names no plan in progress, or only the archived one as finished.
- **Comparison.** A table with one row per step and the columns: branches created, worktrees left, commits on `main`
  (merge / non-merge), README statuses on the tracking branch after the step, whether the report asked a question,
  stop line. `cur` and `base` must agree in every cell, except the report's `Flow: manual` line and wording; any
  other difference is a finding marked "manual flow differs from v2.12.0". Model nondeterminism is named as the
  likely cause only when the differing cell is a choice the skills leave to the model (wording, order of tasks in a
  launch group).

## Autonomous run (task F)

Plan: `examples/03-autonomous-night-run/` → `plans/2026-11-04-wordstat`, slug `wordstat`,
`- Flow: autonomous · target: integration/wordstat · manual review: F3`. One repository `night`, seeded as above
from the task's working folder, then:

1. **Forced failure.** Commit on `main` the file `tests/test_forced_red.py`:

   ```python
   """Forced failure of the end-to-end run: red as soon as wordstat.export exists."""
   import pytest


   def test_forced_red():
       pytest.importorskip("wordstat.export")
       assert False, "forced red: end-to-end run"
   ```

   Before task D the module is missing and the test is skipped, so every check before wave 2 and the check of F2 are
   green; once D adds `wordstat/export.py` the check of F4 is red whatever D does. D may not change the test (it is
   outside its files), so F4 must end blocked.
2. **A remote that must stay untouched.** `git init --bare "$scratch/origin.git"`,
   `git -C "$scratch/night" remote add origin "$scratch/origin.git"`, `git -C "$scratch/night" push -q -u origin main`
   (the only push of the run, made by the setup). Record `git -C "$scratch/origin.git" for-each-ref` now and at the
   end.
3. Check: `python -m pytest -q` in `night` → `1 skipped`, exit 0; `status_check.py` on the plan folder → exit 0.

| Step | Command | Model, caps |
|---|---|---|
| A1 | `python <working folder>/scripts/wave_driver.py plans/2026-11-04-wordstat --repo "$scratch/night" --dry-run --claude-arg=--setting-sources --claude-arg=project,local` | — |
| A2 | the same without `--dry-run`, plus `--max-usd 20 --max-calls 12` | driver defaults |
| A3 | `/wave-run plans/2026-11-04-wordstat merge F3` (the user approves the manual-review feature) | sonnet, 100, 3 |
| A4 | in `$scratch/night`: `git merge --no-ff integration/wordstat -m "Merge integration/wordstat"`, then `python -m pytest -q` | — |
| A5 | A1 again | — |
| A6 | `/wave-status plans/2026-11-04-wordstat` | haiku, 60, 0.5 |

A2 uses the driver's default permission mode `auto`. If its report or a call log shows permission denials that kept
a wave from finishing, record that as a finding, seed a fresh repository `night2` the same way and repeat A1–A6 there
with `--permission-mode bypassPermissions`; both runs go into the record.

Expectations:

- A1: exit 0; the line `next: wave plans/2026-11-04-wordstat — wave 1 is ready` and a `claude` command line with
  `/wave-run plans/2026-11-04-wordstat 1`, `--model sonnet` and `--setting-sources project,local`.
- A2: the driver prints `Report: <path>` and exits 0 (nothing left to run) or 1 (a rail), and its calls are: wave 1,
  wave 2, possibly resumes or task-mode calls, and the final `wave-status`. After it:
  - F1 `✅ merged` and F2 `✅ merged`, their `Merged` hashes ancestors of `integration/wordstat`, their briefs saying
    `auto-approved`; wave 2 started without a `feature-unmerged` stop (auto-approval of F1 unblocked it);
  - F3 `👀 review`, `Waiting for: review`, not in `integration/wordstat`;
  - F4 ⚠️ blocked with `Waiting for: I<n>`, task D ⚠️, entry I<n> open in `problems.md` on `plan/wordstat`, and
    `git merge-base --is-ancestor feat/wordstat/F4-csv-export integration/wordstat` fails (or the branch does not
    exist). Which path led there (red after two attempts, an out-of-scope edit, the executor's stop) is recorded,
    not judged;
  - `main` and `refs/remotes/origin/main` at their seed commits; the bare remote's refs unchanged; no
    `refs/wave-method/claims/*` ref; no `wave-driver.lock` in `git rev-parse --git-common-dir`;
  - `report.md` names `integration/wordstat`; shows F1 and F2 under "Merged, not in `main`" with their blocks, F3
    under "Ready for review" with `/wave-run plans/2026-11-04-wordstat merge F3` and `$wave-run … merge F3`, F4
    under "Blocked and waiting" as `F4 … — ⚠️ I<n>: …`; "Next" gives `git diff main...integration/wordstat` and
    `git merge --no-ff integration/wordstat`; "Calls" lists every call with its cost.
- A3: F3 `✅ merged` into `integration/wordstat`, its brief `approved by the user`; `main` unchanged.
- A4: the merge succeeds; `python -m pytest -q` → `12 passed, 1 skipped` (7 + 5 cases; the forced test is skipped
  because F4 never reached `main`).
- A5: exit 0, `next: nothing — …` naming no call for the blocked F4: the blocked feature stays blocked.
- A6: F4 ⚠️ with I<n>; no feature under `Merged, not in main:` (all merged features are in `main` now).

Paste the driver's `report.md` of A2 into the record in a fenced block, unchanged.

## Record format

`docs/rehearsals/end-to-end-manual.md` (task E) and `docs/rehearsals/end-to-end-autonomous.md` (task F), in the
style of `docs/rehearsals/print-mode-fixture-chain.md`:

1. `# Rehearsal: <manual flow end to end | autonomous flow end to end>`, then one line: date, `claude --version`,
   the source commit (`git rev-parse --short HEAD` of the working folder).
2. `## Setup` — every command of the seeding, with `<scratch>` in place of the real temporary path.
3. `## Runs` — one `### <step>` per step: the command in a fenced block, then bullet lines `Pass. …` or
   `Finding. Expected … Observed … (<log, commit or line>)`.
4. `## Results` — a table: expectation, result (Pass / Finding / Not run), evidence. Task E adds the comparison table.
5. `## Not verified` — every expectation that could not be checked, and why (a cap reached, a step not run, a value
   the logs do not show). Write `nothing` only when every expectation has a result.
6. `## Repeat` — the shortest command list that repeats the run from an empty scratch folder.

Real paths of the user's machine (home folder, user name) are replaced by `<scratch>`, `<home>` or
`<working folder>`. Costs are written as reported (`total_cost_usd`); on a subscription they count toward usage
limits and are not billed.

## Limits

- No call in a repository other than the scratch ones; no push except the seeding push into the scratch bare
  remote.
- Neither task fixes a skill, a script or an example: a defect is a finding, and the coordinator turns findings into
  problem entries for a re-plan.
- A step that cannot start (no `claude`, no network for `pip`, a cap reached) is recorded as not run with its reason,
  and the task goes on with the steps that do not depend on it.
- The scratch folder is left in place; its path appears in the task report, not in the record.

## Acceptance tests

1. Each record exists and has the six sections; every expectation above appears in its "Results" table as Pass,
   Finding or Not run.
2. Task E's comparison table covers M2–M5 for `cur` and `base`.
3. Task F's record contains the A2 `report.md` and the final statuses of F1–F4.
4. `git diff --check` is clean, and the working folder's refs (except the task's own branch) are unchanged by the
   task.
