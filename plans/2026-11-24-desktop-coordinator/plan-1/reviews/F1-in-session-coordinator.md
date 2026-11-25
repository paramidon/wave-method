# F1 · In-session coordinator

- Branch: `feat/desktop-coordinator-p1/F1-in-session-coordinator` · worktree: `D:/Documents/orbits/wave-method.worktrees/desktop-coordinator-p1-F1`
- 👀 review since 2026-11-25 22:53

## Essence

Before: only `python scripts/wave_driver.py` chained the pipeline steps, from a terminal, and it never triaged. After:
`/wave-auto <list>` in an interactive Claude Code session asks its questions once, then triages, plans and runs the
waves through subagents and merges the features into an integration branch.

## How to test

1. Type `/wave-auto` and a list of two or three small changes → the questions come once (or not at all), then the steps
   run on their own and a status report shows the features `✅ merged` into `integration/<topic>`; `main` is unchanged.
2. Close the session mid-run and type `/wave-auto plans/<date>-<topic>/index.md` in a new one → it continues where it
   stopped.
3. Type `/wave-auto steps 1 <list>` → it ends with `ended by rail: steps 1`, and the status shows a triage in progress
   with the `/wave-auto <index path>` command.

## Worth a look

- Accepted limits: some progress lines are skipped and extra remarks appear; no `Resume:` line after a triage without
  questions, so after closing early take the command from `/wave-status`.
- Task mode of `wave-run` changed for every user, not only for the coordinator.
- The last rehearsal ran in the CLI with a Sonnet 5.5 coordinator only; the desktop app was not rehearsed again after
  the later fixes.

## Tasks

- A (wave 1) — the contract between the coordinator and the skills it starts is now in `layout.md` ("Coordinated runs": eleven steps with their return lines, the coordinator claim), and six places of `layout.md` name `wave-auto`.
- B (wave 1) — `wave-run` can run as a coordinated step (every task in task mode, a one-line return, the new stop `manual-flow`), and task mode keeps the report block in the last commit, skips an already committed task and takes fix requests through the wave file.
- C (wave 1) — `wave-triage` is split into four coordinated phases (ask, answers, cluster, finish) so the coordinator asks the user once and launches the cluster subagents itself.
- D (wave 1) — the rules of the navigator, a read-only low-tier subagent that reads the pipeline state from git and returns the next action in one line, are written (`skills/wave-auto/navigator.md`).
- E (wave 1) — the skill `wave-auto`, the coordinator that runs triage, plans and waves from one command in one session through subagents, is written (`skills/wave-auto/SKILL.md`).
- J (wave 3) — the navigator now reports every halted unit instead of at most four, `wave-plan` knows that a coordinated run ends with a return line, and `wave-status` shows coordinator claims and offers `/wave-auto` for an index.
- K (wave 3) — the installers and the plugin files install the fifth skill `wave-auto`, and the README and the changelog describe `/wave-auto`.
- L (wave 3) — the rehearsal of `/wave-auto` in the Claude Code CLI on a small fixture project is recorded in `docs/rehearsals/coordinator-cli.md`: questions asked once, a rail, a resume in a new session, a claim takeover, two merged features and green tests; it found three issues (I2–I4).
- M (wave 3) — the desktop-app rehearsal of `/wave-auto` is recorded in `docs/rehearsals/coordinator-desktop.md`: from a list to both features merged into the integration branch in a separate session, and a second session that found nothing left to run; it found two new issues (I7, I8) and repeated I4.
- N (wave 4) — the wording of `wave-auto` and `layout.md` was tightened: progress lines with a clock time, the claim released before the final status, a final report that is the template only; the rehearsals show that progress lines are still skipped (I3).
- O (wave 4) — the CLI rehearsal of the flow (rail, resume, already committed tasks, re-plan, two merged features) is recorded in `docs/rehearsals/coordinator-cli-flow.md`: the pipeline works, six deviations from the skill texts (I10–I15).
- P (wave 4) — the CLI rehearsal of early stops (missing tool, halted unit, `until` rail, killed session and resume without the plugin) is recorded in `docs/rehearsals/coordinator-cli-stops.md`: stops and resume work, eight findings (I16–I23).
- Q (wave 4) — a ten-problem triage with clusters and the Codex links of both installers are recorded in `docs/rehearsals/coordinator-cli-triage.md`: triage and installers work, three findings (I24–I26).
- R (wave 5) — the coordinator keeps its claim oid in the conversation only, counts steps from its own agent calls, does not end the run on a halt of one unit and runs the tasks of a wave in a fixed order; it is also told to write the `Resume:` line, which it still skips (I28, accepted).
- S (wave 5) — the waiting line of task mode now needs both command forms for each task, and `wave-status` shows a triage in progress instead of offering to remove its worktree.
- T (wave 5) — the fixes of R and S were checked in real CLI runs and recorded in `docs/rehearsals/coordinator-cli-fixes.md`, with one finding.

## Check

`python skills/wave-plan/scripts/test_status_check.py; python -m unittest discover -s scripts/tests; status_check.py on
examples/*/; git diff --check` → green on 5ec38bd (39 status-check tests, 59 driver tests, three examples); tests added
or changed: none
