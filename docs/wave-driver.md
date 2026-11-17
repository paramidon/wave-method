# Overnight wave driver

## What it does

The driver runs a triage index or a plan folder unattended in autonomous flow.
It starts one fresh headless Claude Code session per step.
It reads the index and plan state from git.
It never pushes or changes the main branch.
It ends by writing a morning report.

## Requirements

- Python 3.9 or later and git.
- The Claude Code CLI, signed in. Check that the executable responds with `claude --version`.
- Wave skills installed in the project, or installed as a plugin. For a plugin install, pass `--skill-prefix wave-method: --add-dir <plugin folder>`.
- An index created by `/wave-triage` or an existing plan folder. To run a manual-flow plan, first switch it with `/wave-run <plan folder> flow autonomous`.

## Run

```bash
python <wave-method>/scripts/wave_driver.py plans/<date>-<topic>/index.md --repo <project> --dry-run
python <wave-method>/scripts/wave_driver.py plans/<date>-<topic>/index.md --repo <project>
```

To start from a single plan, replace the index path with the plan folder path.

## Options

| Option | Default | Meaning |
|---|---|---|
| `<start>` | — | `plans/<date>-<topic>/index.md`, or a plan folder; relative to the repository root (an absolute path inside it is made relative; `\` becomes `/`; a trailing `/` is removed) |
| `--repo PATH` | current folder | the project repository (its top level is used) |
| `--main BRANCH` | `main`, else `master` | the main branch |
| `--plan-model`, `--run-model`, `--status-model`, `--low-model`, `--medium-model`, `--high-model` | `DEFAULT_MODELS` | models per role and per task tier |
| `--cap SKILL=TURNS:USD` (repeatable) | `DEFAULT_CAPS` | SKILL is `wave-plan`, `wave-run`, `task` or `wave-status` |
| `--max-calls N` | 60 | rail |
| `--max-failures N` | 3 | rail: failed calls in a row |
| `--deadline TIME` | none | `HH:MM` or `YYYY-MM-DD HH:MM`: no call starts after it |
| `--max-usd X` | none | rail on the sum of `total_cost_usd` |
| `--call-timeout-min N` | 120 | per call |
| `--permission-mode MODE` | `auto` | passed to `claude` |
| `--claude PATH` | `shutil.which("claude")` | the CLI |
| `--skill-prefix TEXT` | `""` | `wave-method:` for a plugin install |
| `--add-dir PATH` (repeatable) | none | passed as `--add-dir` (the plugin folder for a plugin install) |
| `--claude-arg ARG` (repeatable, write `--claude-arg=--setting-sources`) | none | extra arguments |
| `--out DIR` | `<repo.parent>/<repo.name>.wave-driver/<YYYY-MM-DD-HHMM>` | report, log and raw call output |
| `--no-status` | off | skip the final `wave-status` call |
| `--dry-run` | off | print the snapshot's next action and its command line; no lock, no call, no files |

The driver uses the following exit codes.

- `0` means nothing is left to run or the dry run completed.
- `1` means a run limit, usage limit, authentication error, guard violation, interrupt, or driver error ended the run.
- `2` means invalid arguments or a setup error, such as a missing start path, an invalid git repository, or a missing or failing Claude CLI.
- `3` means another driver holds the repository lock.

See [Claude Code print mode](claude-print-mode.md#prompt-form-for-the-driver) for the call form and caps.

## What it runs

| Action | Prompt | Model role (default) |
|---|---|---|
| Plan an unplanned part | `/wave-plan flow autonomous <index> part <K>` | Plan (`opus`) |
| Run the first pending wave | `/wave-run <plan folder> <N>` | Run (`sonnet`) |
| Run a waiting task in task mode | `/wave-run <plan folder> <N> task <ID>` | Task tier (low `haiku`, medium `sonnet`, high `opus`) |
| Resume the wave | `/wave-run <plan folder> <N>` | Run (`sonnet`) |

The driver can finish with a `/wave-status` call using the status model (`haiku`).
Triage, re-planning, the merge form and the flow form are user actions.

Each plan folder is a unit. A skill stop normally halts its unit, and a target-related stop halts all units sharing
that target. Manual flow, blocked dependencies and two failed or unproductive attempts can also halt a unit.
The driver continues with independent units. A dependent index part waits for git to show that its prerequisite
part is merged.

## Rails and guard

The driver checks the call count, consecutive failures, deadline and accumulated USD before starting another work
call. The deadline leaves a running call alone. The per-call timeout can cut it short. The final status call is
outside these run limits. Usage limits and authentication errors end the run immediately.

The lock at `<git common dir>/wave-driver.lock` allows one driver per repository across worktrees. The guard
compares the main branch ref, remote-tracking refs, and the main checkout's branch and tracked status before and
after each call. A change ends the run and appears in the report.

## Files

The output folder contains these files.

- `report.md` holds the morning report.
- `driver.log` records the run.
- `calls/NN-<kind>.json` holds raw call output.

## Morning report

After the run summary, the report shows these sections in order.

1. Integration targets
2. Merged, not in `<main>`
3. Ready for review
4. Blocked and waiting
5. Halts
6. Open problems
7. Status check
8. Calls
9. Next
10. wave-status

**Next** gives the exact `git diff <main>...integration/<name>` and `git merge --no-ff integration/<name>`
commands for integration targets ahead of main. For features awaiting review, it lists both merge forms,
`/wave-run <plan folder> merge <F-ID>` and `$wave-run <plan folder> merge <F-ID>`.

## Limits

- The driver's own git commands are read-only. It writes its output and lock file and leaves branches, worktrees and claims to the skills.
- A timeout can leave a wave running with its claim still held. The next run halts that unit and reports it.
- The guard detects changes after the call and reports them for manual recovery.
- The driver runs calls sequentially. The skills' target claim still controls access to the integration target.
- A task waiting for task mode with a populated `Needs` cell requires a session with that capability.
- The driver reads plans and index parts within the selected start scope.
