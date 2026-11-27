# wave-method

**Plan once with a strong model, execute in parallel with cheaper ones, merge only what is finished and reviewed.**

wave-method is a set of five agent skills for **Claude Code** and **OpenAI Codex** that turn a list of problems
into merged commits: triage → design → waves of parallel subagent tasks in git worktrees → one review branch per
finished feature → merges you approve.
In the default manual flow you approve every merge, while in autonomous flow a whole plan runs
unattended, for example overnight, into an integration branch that you review and merge in the morning.
All state lives as plain Markdown in your repository, so any session (or any person) can pick up where the last
one stopped.

> Status: experimental (see [releases](https://github.com/paramidon/wave-method/releases)). MIT licensed.

![Plan with a strong model, review, run waves with cheaper models, review and merge finished features](docs/images/workflow-simple.svg)

## Contents

- [Install](#install)
- [Quick start](#quick-start)
- [Overnight runs (autonomous flow)](#overnight-runs-autonomous-flow)
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

### Codex plugin (recommended for Codex)

In a terminal, add this repository as a Codex plugin marketplace and install the plugin; the Codex CLI and the
Codex desktop app share it:

```
codex plugin marketplace add paramidon/wave-method
codex plugin add wave-method@wave-method
```

Type the commands with `$` in Codex (`$wave-plan …`).

### Codex permissions

The skills write branches and commits in `.git` and create worktrees next to the project
(`../<project>.worktrees/`). Codex's default `workspace-write` sandbox keeps `.git` read-only, so give Codex this
permission profile in `<project>/.codex/config.toml` (absolute paths; `<parent>` is the folder that holds the
project):

```toml
default_permissions = "wave"

[permissions.wave]
filesystem = { ":root" = "read", "<parent>" = "write", ":tmpdir" = "write", "<project>/.codex" = "read" }
```

Codex reads this file only in a project it trusts; in any other folder it runs read-only and the skills stop
`git-read-only`. To trust the project, add its entry to `~/.codex/config.toml`, with the absolute path of the
project folder in single quotes (on Windows with backslashes, as `'C:\Users\me\textkit'`):

```toml
[projects.'<project>']
trust_level = "trusted"
```

The sandbox stays on: Codex reads everything and writes only below `<parent>` and in the temp folder. Keep
`.codex/config.toml` out of git (add it to `.git/info/exclude`). Where the profile cannot be used, full access works
too (`codex -s danger-full-access`). The Codex desktop app is not rehearsed with it yet. Details:
`skills/wave-plan/layout.md`, "Vendors".

On Windows the worktrees that Codex creates in its sandbox belong to the sandbox account (`CodexSandboxOffline`),
and git in your own shell refuses them with `detected dubious ownership`. Review the branches from the main
checkout (`git log <branch>`, `git diff main...<branch>`), or allow one worktree for a command with
`git -c safe.directory='<worktree path>' …` (or for good with
`git config --global --add safe.directory '<worktree path>'`).

### Installer (a copy inside the project)

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

Manual install: copy the five folders of `skills/` into one skills folder that your agent reads (for example
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

Wave 1 runs A, B and C at the same time, each in its own git worktree. When it ends, F1 and F3 are ready; F2 waits
for its task D. Nothing is merged yet: `wave-run` shows each ready feature on its own branch
(`feat/csv-export/F1-login-test-stability`, `feat/csv-export/F3-cache-ttl-unit`) in a short block — what changes
for you, and a few steps to test it by hand with what you should see — and asks about each one. The full brief is
kept in the plan folder (`reviews/<feature>.md`). Answer `merge F1`, `later`, or `problems F1: …` (which go to the
next re-plan). A feature
you leave for later is merged with:

```
/wave-run plans/2026-11-02-csv-export merge F3
```

A feature branch holds only its own feature, so each one can be reviewed and merged alone, in any order. Then:

```
/wave-run plans/2026-11-02-csv-export 2
```

![Wave 1 runs tasks A, B, C in parallel; F1 and F3 are ready for review; F2 waits for task D in wave 2](docs/images/waves-example.svg)

### 4. Check progress, fix problems

```
/wave-status
```

shows what each feature is waiting for (features waiting for your review come with the same short block), running
waves, and the next command. If a wave reports problems, re-plan them with `/wave-plan plans/2026-11-02-csv-export`.
A feature whose fixes keep failing is escalated at its second re-plan and held at its third until you give a direction
(`/wave-plan plans/2026-11-02-csv-export override F2: <what to do>`); see
[Re-plan escalation](skills/wave-plan/layout.md#re-plan-escalation).

### A long backlog

For more than one plan's worth of work (dozens of issues), start with triage:

```
/wave-triage <paste 45 issues>
```

It writes `plans/<date>-<topic>/index.md` with parts sized for one plan each, and prints one command per part, for
example `/wave-plan plans/<date>-<topic>/index.md part 1`. Parts without dependencies can be planned in parallel.

### Example plans

[`examples/`](examples/) has three complete plans written from scratch, as `wave-plan` produces them:

- [`01-greenfield-todo-cli`](examples/01-greenfield-todo-cli/) — a new Python tool from an empty repository: two
  waves, a contract between them, design files with acceptance tests.
- [`02-bugfix-batch`](examples/02-bugfix-batch/) — three small fixes in an existing app: one wave, three features.
- [`03-autonomous-night-run`](examples/03-autonomous-night-run/) — a plan written in autonomous flow and run
  overnight with `/wave-auto`, with one feature under manual review and a wave that waits for an auto-merged feature.

## Overnight runs (autonomous flow)

### Two flows

| Flow | Who approves a ready feature | Merged into | Questions |
|---|---|---|---|
| `manual` (default) | you | `main` | at each review point and stop |
| `autonomous` | `wave-run` when all five auto-approval conditions hold, or you for features under manual review | `integration/<name>` | none |

A plan without a `Flow:` line is in manual flow and behaves exactly as before.

### Choosing the flow

- `/wave-triage flow autonomous <list>` writes `- Flow: autonomous · target: integration/<topic>` in the index.
  Its parts are planned in autonomous flow by default.
- `/wave-plan flow autonomous <list>` plans a raw list. Use
  `/wave-plan flow autonomous plans/<date>-<topic>/index.md part 2` to select the flow for one index part.
- Between waves, `/wave-run <plan folder> flow autonomous review F2` switches an existing plan and keeps F2
  under manual review. A plan of an index part then merges into the index's `integration/<topic>`, as the parts
  planned in autonomous flow do. Switch back with `/wave-run <plan folder> flow manual`. It stops with
  `target-unmerged` while the integration branch has commits that `main` lacks.

In autonomous flow, `wave-triage` and `wave-plan` resolve ambiguous readings using fixed rules without asking
you. Each choice is recorded as `Assumed (autonomous, not asked)` and appears under “Worth a look” in the
feature's review block.

### The integration branch

All parts of an index share `integration/<name>`, where `<name>` is the index topic, also a part switched later with the
flow form. A plan from a raw list uses its slug. The worktree is `../<repo>.worktrees/integration-<name>`. Autonomous
flow never changes `main` or the main checkout. The claim ref `refs/wave-method/claims/integration/<name>` allows one
writer at a time. A second run stops with `wave-running` and names the holder.

Auto-approval requires all five conditions.

1. Every task in the feature is marked ✅ or ➖.
2. The full feature check passes after merging the integration branch into the feature branch, and that merge
   changes none of the feature's own lines.
3. No open problem entry concerns the feature or any of its tasks.
4. Every task commit has a `Wave-Model` trailer naming a model of the task's tier or higher.
5. The feature is outside the manual review list.

If any of the first four conditions fails, the feature becomes ⚠️ blocked with a problem entry. A feature
outside auto-approval solely because of condition 5 waits for your review. The
[decision table](skills/wave-plan/layout.md#decision-table) gives the fixed answers for the other points where
`wave-run` asks or waits.

### Unattended runs: wave-auto

`/wave-auto <list>` (Codex: `$wave-auto <list>`) runs the whole pipeline in the session you type it in. It asks the
triage questions once, at the start, then triages, plans every part and runs every wave in autonomous flow, each step
as a subagent on a model of the step's tier, printing one line per step. It ends with the `wave-status` report:
features merged into `integration/<topic>`, features waiting for your review, blocked features and what each waits
for.

- Start from a list, an index (`/wave-auto plans/<date>-<topic>/index.md`) or a plan folder.
- Plans of the index that were planned earlier in manual flow are asked about once, at the start: one question lists
  every such plan with the integration branch it would merge into. Yes switches all of them to autonomous flow; no
  keeps them all manual, and the run skips them. Switch one later with `/wave-run <plan folder> flow autonomous`.
- Bound it with `until 07:00` or `steps 40` before the start: `/wave-auto until 07:00 plans/<…>/index.md`.
- Nothing is kept in the chat: if the window closes or a usage limit stops the session, run
  `/wave-auto plans/<date>-<topic>/index.md` in a new session and it continues where it stopped.
- A step that cannot run as a subagent of its tier runs in a separate session where the app can start one;
  otherwise the run stops with the command to run by hand.

#### Where to run it

| Where | Start | The questions | Continue after a closed window or a limit |
|---|---|---|---|
| Claude Code CLI | `claude` in the project, an Opus-class model, permission mode `auto`; type `/wave-auto <list>` | answer in the same session | `/wave-auto plans/<date>-<topic>/index.md` in a new session |
| Claude Code desktop app | a new session (Code tab) in the project folder, an Opus-class model, permission mode `auto`; type `/wave-auto <list>` | answer in the same session | the same, in a new session |
| Codex CLI | `codex -m gpt-6.2-astra` in the project, with the permission profile of [Codex permissions](#codex-permissions); type `$wave-auto <list>` | answer in the same session | `$wave-auto plans/<date>-<topic>/index.md` in a new session |
| Codex desktop app | a new thread in the project, GPT-6.2-Astra; type `$wave-auto <list>`. Not rehearsed, the profile of [Codex permissions](#codex-permissions) included | answer in the same thread | the same, in a new thread |

The worktrees live next to the project (`../<repo>.worktrees/`), so the agent needs write access there. Claude Code's
`auto` mode allows it. In Codex use the permission profile of [Codex permissions](#codex-permissions).

To start a run from a script, with nobody at the keyboard, start from an index whose questions are answered (or answer
them in a second call). In bash or zsh:

```bash
claude -p "/wave-auto plans/<date>-<topic>/index.md"
codex exec -m gpt-6.2-astra "\$wave-auto plans/<date>-<topic>/index.md" < /dev/null
```

In PowerShell:

```powershell
claude -p "/wave-auto plans/<date>-<topic>/index.md"
$null | codex exec -m gpt-6.2-astra '$wave-auto plans/<date>-<topic>/index.md'
```

Git Bash on Windows rewrites an argument that starts with `/` into a Windows path: there, put
`MSYS_NO_PATHCONV=1` before the `claude` command, or use PowerShell.

A list start asks its questions first; answer with `claude -p --continue "<answers>"` or
`codex exec resume --last "<answers>"`, run in the project folder; give Codex the same `< /dev/null` (bash, zsh) or
`$null |` (PowerShell) as above. None of these script lines has been run as written yet.

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
- **Feature-gated, reviewed merges.** A feature is offered for review only when all of its tasks — possibly
  across several waves — are done and its full check is green, on its own branch that holds no other feature. It
  reaches `main` only when you approve it. Nothing half-wired or unreviewed lands on `main`.
- **Durable, readable state.** Statuses, a problem log and an execution log per wave live in Markdown on a
  tracking branch. A fresh session reads only what it needs; finished waves are never re-read.
- **Model-tier routing.** Every task is `low`, `medium` or `high`; it never runs below its tier. Each task prompt
  starts with its required tier, so a weaker model given it by mistake stops instead of doing the work, and the
  coordinator merges a task only when its commits name a model of its tier.
- **A closed problem loop.** Whatever a subagent could not check, or found broken, becomes a problem entry that
  the next planning run turns into fix tasks. A feature re-planned a second time is escalated: the planner verifies
  its assumption by running code, its fix tasks need a high-tier model and, in autonomous flow, it waits for your
  review; a third re-plan waits for your direction.

## How it works

![Full workflow: triage, plan, review, run waves in worktrees, feature gate, your review, merge, re-plan loop](docs/images/workflow-full.svg)

| Skill | Role | Recommended model |
|---|---|---|
| `wave-triage` | Splits a long list (up to 40–80 problems) into parts that fit one plan each: clarifies once, locates each problem in the code, judges difficulty, finds dependencies. Clusters large lists and runs one read-only subagent per cluster. | high (Opus-class) |
| `wave-plan` | Designs the solutions and slices them into features, tasks and waves with ready-to-paste task prompts. Also re-plans open problems of an existing plan. | high (Opus-class) |
| `wave-run` | Executes one wave: worktrees, subagents, merges, checks, statuses; offers each finished feature for review and merges the ones you approve into `main` (in autonomous flow it approves them under fixed conditions and merges them into an integration branch). Archives finished plans. | medium |
| `wave-status` | Read-only report: status and task progress of every feature first, then running waves, blocked features and why, leftovers, the next command. | low |
| `wave-auto` | Runs triage, plans and waves from one command in one session, each step as a subagent on a model of its tier; asks the triage questions once, at the start; autonomous flow. | high (Opus-class or GPT-6.2-Astra) |

Key terms:

| Term | Meaning |
|---|---|
| problem `P<n>` | one item of your list |
| feature `F<n>` | the smallest set of changes that makes sense on `main` on its own; the unit that gets reviewed and merged, on its own branch `feat/<plan>/<feature>` |
| task `A`, `B`, … | one prompt for one subagent, with an exact list of files it may change |
| wave | tasks that can run at the same time (no shared files); only a scheduling unit |
| tiers | `low` (Haiku-class / GPT-6-Luna), `medium` (Sonnet-class / GPT-6.2-Sol), `high` (Opus-class / GPT-6.2-Astra) |
| tracking branch | `plan/<slug>`: the only place where plan status is committed |
| flow | `manual` (the default) requires you to approve every merge. `autonomous` runs unattended and merges into an integration branch. |
| integration branch | `integration/<name>` receives autonomous merges. You review it as one diff and merge it into `main`. |

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
  (task mode). `wave-auto` needs subagents with a choice of model: Claude Code or Codex, CLI or desktop app.
- **Python 3.9+** is optional: only the status-check script `wave-plan/scripts/status_check.py` uses it. Without it,
  the check is done by reading.
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

- Nothing is ever committed directly on `main`. In manual flow, it receives only `merge --no-ff` of complete
  features you approved and of the plan's tracking branch. In autonomous flow, features go to the integration
  branch, which you merge yourself.
- A feature is never merged into `main` without your approval of that feature: an answer in the `wave-run` session
  (`merge F1`), `/wave-run <plan> merge F1`, or your own `git merge` of its branch.
- Your uncommitted work in the main checkout is never staged, unstaged, stashed or reset. If it blocks a merge (a
  staged change, or an edit to a file the feature also changes), the skill tells you why and waits, or leaves the
  feature for a later `/wave-run <plan> merge <F-ID>`.
- Nothing is ever pushed.
- A task never runs on a model below its tier.
- A feature is re-planned at most twice on its own; a third re-plan needs your `override` direction.
- A wave in progress is a lock: no re-plan or second wave of the same plan starts until it finishes.
- Every stop prints a stop code and the next command.
- Autonomous flow approves a feature only under the five auto-approval conditions. Features under manual
  review always need your approval, and the tier gate always applies.
- A claim ref allows one writer at a time on an integration branch, and another one `wave-auto` coordinator per
  index or plan.

## Customising

| What | Where |
|---|---|
| Models per tier | `wave-plan/layout.md`, "Model tiers" (or a `Models:` line in one plan's README) |
| Difficulty scale and the size of one plan | `wave-triage/difficulty.md` |
| Plan layout, statuses, reading rules, Markdown rules | `wave-plan/layout.md` (single source of truth) |
| File templates | `wave-plan/templates.md` |
| Language | the skills talk in the language you write in; everything written to the repository is English, always (a non-English doc a task changes is translated) |
| Flow of a plan | the README `Flow:` line, written by `wave-plan` and changed with `/wave-run <plan folder> flow …` |
| Rails of an in-session run | `until` and `steps` of `/wave-auto` (`wave-auto/SKILL.md`) |

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
- **Autonomous flow** was rehearsed with Claude Code on Windows ([rehearsals](docs/rehearsals/)).
- **wave-auto** was rehearsed in the Claude Code CLI and desktop app ([rehearsals](docs/rehearsals/)), and in the
  Codex CLI up to the start of a wave: triage, the questions, the plan and the launch of a wave's tasks passed,
  while the end of a wave in Codex (task commits, the merge into `integration/<topic>`, auto-approval) is not
  verified yet. The Codex desktop app is not rehearsed. Its rails (`until`, `steps`) are rules of the skill, not
  enforced limits.
- **An unattended run consumes usage.** Bound it with `until` or `steps` of `/wave-auto`. On a subscription, the
  run counts toward usage limits.

## Versioning and contributing

The version is written only as a git tag `vMAJOR.MINOR.PATCH`. For each tag the release workflow publishes a
[GitHub release](https://github.com/paramidon/wave-method/releases) with archives and copies the version into
`version` of [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) on `main`; Claude Code offers plugin users an
update when that field changes, so they get releases, not every commit.
[`skills/wave-plan/CHANGELOG.md`](skills/wave-plan/CHANGELOG.md) lists what each release changed.

Issues and pull requests are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 paramidon
