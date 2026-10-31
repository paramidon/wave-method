# wave-method

**Plan once with a strong model, execute in parallel with cheaper ones, merge only what is finished.**

wave-method is a set of four agent skills for **Claude Code** and **OpenAI Codex** that turn a list of problems
into merged commits: triage → design → waves of parallel subagent tasks in git worktrees → feature-gated merges.
All state lives as plain Markdown in your repository, so any session (or any person) can pick up where the last
one stopped.

> Status: experimental (see [releases](https://github.com/paramidon/wave-method/releases)). MIT licensed.

![Plan with a strong model, review, run waves with cheaper models, merge finished features](docs/images/workflow-simple.svg)

## Contents

- [Install](#install)
- [Quick start](#quick-start)
- [Is this another SDLC?](#is-this-another-sdlc)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [When to use it](#when-to-use-it)
- [When not to use it](#when-not-to-use-it)
- [Safety rules](#safety-rules)
- [Customising](#customising)
- [Limitations](#limitations)
- [Versioning and contributing](#versioning-and-contributing)

## Install

You need git, and Claude Code or Codex (see [Requirements](#requirements)).

### Claude Code plugin (recommended for Claude Code)

In Claude Code, add this repository as a plugin marketplace and install the plugin:

```
/plugin marketplace add paramidon/wave-method
/plugin install wave-method@wave-method
```

The skills are then available in every project; update them from `/plugin`. Plugin skills may also be called
with the plugin prefix (`/wave-method:wave-plan`), which you need only if another skill has the same name. To
share the plugin with your team, commit the marketplace and plugin to the project's `.claude/settings.json`
(`extraKnownMarketplaces` and `enabledPlugins`).

### Installer (Codex, or a copy inside the project)

Clone this repository and run the installer against your project. It copies the skills into `<project>/.claude/skills/` and links them into
`<project>/.agents/skills/` for Codex.

Windows (PowerShell):

```powershell
git clone https://github.com/paramidon/wave-method.git
.\wave-method\install.ps1 -Target C:\path\to\your-project
```

macOS / Linux:

```bash
git clone https://github.com/paramidon/wave-method.git
./wave-method/install.sh /path/to/your-project
```

Options: `-Force` / `--force` replaces existing `wave-*` skill folders (use it to upgrade); `-NoCodex` /
`--no-codex` skips the Codex links. Add `.agents/` to your project's `.gitignore` if you use the links.

Manual install: copy the four folders of `skills/` into one skills folder that your agent reads (for example
`<project>/.claude/skills/` or `<project>/.agents/skills/`). Keep them side by side: the skills refer to each other
by paths relative to that folder (`wave-plan/layout.md`).

## Quick start

Commands are shown for Claude Code (`/…`); in Codex type the same command with `$` (`$wave-plan …`). Every skill
ends by printing the next command in both forms. Start each step in a **fresh session**.

### 1. Plan

Give `wave-plan` your list in one message (a high-tier model is recommended for planning):

```
/wave-plan fix the flaky LoginTest; add CSV export to the reports page; rename the config key cache_ttl to cache_ttl_s
```

It reads the code, asks its questions once, writes a plan folder `plans/<date>-<slug>/` on the branch
`plan/<slug>`, merges it into `main` and prints the plan:

| Feature | Problems | Tasks (wave) |
|---|---|---|
| F1 `login-test-stability` | P1 | A (1) |
| F2 `reports-csv-export` | P2 | B (1), D (2) |
| F3 `cache-ttl-unit` | P3 | C (1) |

### 2. Review

Open `plans/<date>-<slug>/README.md` and the files under `solutions/` and `waves/`. Change anything you disagree
with — it is plain Markdown.

### 3. Run each wave

A medium-tier model is enough for running:

```
/wave-run plans/2026-11-02-csv-export 1
```

Wave 1 runs A, B and C at the same time, each in its own git worktree. When it ends, F1 and F3 are merged into
`main`; F2 waits for its task D. Then:

```
/wave-run plans/2026-11-02-csv-export 2
```

![Wave 1 runs tasks A, B, C in parallel; F1 and F3 merge; F2 waits for task D in wave 2](docs/images/waves-example.svg)

### 4. Check progress, fix problems

```
/wave-status
```

shows running waves, what each feature is waiting for, and the next command. If a wave reports problems, re-plan
them with `/wave-plan plans/2026-11-02-csv-export`.

### A long backlog

For more than one plan's worth of work (dozens of issues), start with triage:

```
/wave-triage <paste 45 issues>
```

It writes `plans/<date>-<topic>/index.md` with parts sized for one plan each, and prints one command per part, for
example `/wave-plan plans/<date>-<topic>/index.md part 1`. Parts without dependencies can be planned in parallel.

### Example plans

[`examples/`](examples/) has two complete plans written from scratch, as `wave-plan` produces them:

- [`01-greenfield-todo-cli`](examples/01-greenfield-todo-cli/) — a new Python tool from an empty repository: two
  waves, a contract between them, design files with acceptance tests.
- [`02-bugfix-batch`](examples/02-bugfix-batch/) — three small fixes in an existing app: one wave, three features.

## Is this another SDLC?

No. A software development life cycle (waterfall, Scrum, Kanban, or an agent framework with "analyst", "architect"
and "developer" roles) answers *what* to build, *who* decides and *when* it ships: requirements, roles, ceremonies,
releases, operations.

wave-method sits one layer lower. It answers a single question: **given a batch of work items that someone has
already chosen, how do AI agents design, slice, execute and merge them without stepping on each other or on you?**
Think of it as an execution protocol — closer to a build scheduler than to a process. It fits inside any SDLC: a
sprint backlog, a set of user stories or a bug list is its input; merged, tested feature commits are its output.

| | SDLC / process frameworks | wave-method |
|---|---|---|
| Scope | the whole life of a product: idea → requirements → design → build → release → operate | one batch of chosen work items: design → build → merge |
| Unit of work | epic, story, sprint | problem → feature → task → wave |
| Who works | people in roles (or agents playing roles) | one strong model designs; cheaper models implement; a coordinator dispatches and records |
| Output | a product increment, a release | merged feature commits on your main branch |
| Artifacts | backlog, specs, boards | a plan folder in `plans/`: README, solutions, one file per wave, problem log |
| Time horizon | weeks to years | minutes to days |
| Decides priorities | yes | no — it takes the list as given |

What it adds compared with "agent, please do these ten things":

- **Design before execution.** A high-tier model writes every design decision (API, algorithm, acceptance tests
  with numbers) into the plan, so tasks are sized for medium-tier models that implement well but design poorly.
- **File-disjoint waves.** Tasks of one wave touch no common file, so they run in parallel in separate git
  worktrees and merge without conflicts.
- **Feature-gated merges.** A feature reaches the main branch only when all of its tasks — possibly across
  several waves — are done and its full check is green. Nothing half-wired lands on `main`.
- **Durable, readable state.** Statuses, a problem log and an execution log per wave live in Markdown on a
  tracking branch. A fresh session reads only what it needs; finished waves are never re-read.
- **Model-tier routing.** Every task is `low`, `medium` or `high`; it never runs below its tier.
- **A closed problem loop.** Whatever a subagent could not check, or found broken, becomes a problem entry that
  the next planning run turns into fix tasks.

## How it works

![Full workflow: triage, plan, review, run waves in worktrees, feature gate, merge, re-plan loop](docs/images/workflow-full.svg)

| Skill | Role | Recommended model |
|---|---|---|
| `wave-triage` | Splits a long list (up to 40–80 problems) into parts that fit one plan each: clarifies once, locates each problem in the code, judges difficulty, finds dependencies. Clusters large lists and runs one read-only subagent per cluster. | high (Opus-class) |
| `wave-plan` | Designs the solutions and slices them into features, tasks and waves with ready-to-paste task prompts. Also re-plans open problems of an existing plan. | high (Opus-class) |
| `wave-run` | Executes one wave: worktrees, subagents, merges, checks, statuses, feature merges into `main`, archive. | medium |
| `wave-status` | Read-only report: status and task progress of every feature first, then running waves, blocked features and why, leftovers, the next command. | low |

Key terms:

| Term | Meaning |
|---|---|
| problem `P<n>` | one item of your list |
| feature `F<n>` | the smallest set of changes that makes sense on `main` on its own; the unit that gets merged |
| task `A`, `B`, … | one prompt for one subagent, with an exact list of files it may change |
| wave | tasks that can run at the same time (no shared files); only a scheduling unit |
| tiers | `low` (Haiku-class), `medium` (Sonnet-class / GPT / Gemini), `high` (Opus-class) |
| tracking branch | `plan/<slug>`: the only place where plan status is committed |

A plan folder looks like this:

```
plans/2026-11-02-csv-export/
  README.md          features, waves, tasks, statuses (≤ 150 lines)
  solutions/         one design file per medium/high problem, lite.md for low ones
  waves/w01.md       task table, full prompts; later its execution log
  problems.md        open problem entries only (created on the first one)
  history.md         re-plan notes (created on the first re-plan)
```

Finished plans move to `plans/archive/`.

## Requirements

- **Git** with `worktree` support, and a main branch called `main` or `master`.
- **Claude Code** (plugin, or skills in `.claude/skills/`) and/or **OpenAI Codex** (skills discovered in `.agents/skills/`).
  Subagents with a choice of model work best; without them the skills degrade to "one task per fresh session"
  (task mode).
- **Python 3.9+** (optional) for the status-check script `wave-plan/scripts/status_check.py`; without Python the
  same check is done by reading.
- A **check command** for your project (build + tests). Every task prompt names it; merges depend on it.

## When to use it

- You have **several related or unrelated changes** (roughly 3–40 items) and want them done in parallel without
  merge chaos.
- The work is **implementation-heavy**: once designed, it can be done by a medium-tier model.
- You want a **reviewable plan** before any code changes, and an **audit trail** afterwards.
- You run **long sessions across days or machines** and need state that survives the chat.
- You mix **vendors or model tiers** and want cheap models to do the bulk of the work safely.

## When not to use it

- **One small change.** Ask the agent directly; the plan costs more than the change.
- **Exploration or research** with no clear target. Design cannot be fixed upfront, so the plan would be guesswork.
- **Everything touches the same file.** Waves need file-disjoint tasks; a single hot file serialises everything.
- **No reliable check command.** Merges are gated on build + tests; without them the gate means little.
- **You cannot let an agent create branches and worktrees** in your repository.
- **Prioritisation, roadmap or release management.** wave-method executes a given list; it does not decide what
  is worth building.

## Safety rules

The skills follow these rules on every run:

- Nothing is ever committed directly on `main`; it only receives `merge --no-ff` of complete features and of the
  plan's tracking branch.
- Your uncommitted work in the main checkout is never staged, unstaged, stashed or reset. If it blocks a merge (a
  staged change, or an edit to a file the feature also changes), the skill tells you why and waits, or leaves the
  feature for the next run.
- Nothing is ever pushed.
- A task never runs on a model below its tier.
- A wave in progress is a lock: no re-plan or second wave of the same plan starts until it finishes.
- Every stop prints a stop code and the next command.

## Customising

| What | Where |
|---|---|
| Models per tier | `wave-plan/layout.md`, "Model tiers" (or a `Models:` line in one plan's README) |
| Difficulty scale and the size of one plan | `wave-triage/difficulty.md` |
| Plan layout, statuses, reading rules, Markdown rules | `wave-plan/layout.md` (single source of truth) |
| File templates | `wave-plan/templates.md` |
| Language | the skills talk in the language you write in; everything written to the repository is English |

Your project's own rules (for example an `AGENTS.md` or `CLAUDE.md` with coding conventions) keep working: the
agents load them as usual, and the planner takes them into account when it writes the task prompts.

## Limitations

- **Experimental.** Tested so far on one Java project with Claude Code and Codex on Windows.
- **Model names** in the tier table are examples; adjust them to the models you have.
- **Codex links** on Windows are junctions (`.agents/skills/`); git does not keep them, so run the installer again
  after a fresh clone.
- **Cost.** Planning uses a high-tier model and reads code; it pays off for batches, not single edits.
- **Checks are only as good as your tests.** Acceptance criteria in plans are concrete, but the gate is the check
  command you provide.

## Versioning and contributing

The version is written only as a git tag `vMAJOR.MINOR.PATCH`. For each tag the release workflow publishes a
[GitHub release](https://github.com/paramidon/wave-method/releases) with archives and copies the version into
`version` of [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) on `main`; Claude Code offers plugin users an
update when that field changes, so they get releases, not every commit.
[`skills/wave-plan/CHANGELOG.md`](skills/wave-plan/CHANGELOG.md) lists what each release changed.

Issues and pull requests are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 paramidon
