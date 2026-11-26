# Plan folders, files, names and statuses

Single source of truth for the wave skills: layout, reading rules, model tiers and the tier gate, names, status rules and Markdown rules are changed here only.

## Who reads what
Read only what the table lists. A file that does not exist means there is nothing of that kind yet.

| Reader | Reads |
|---|---|
| `wave-run` coordinator | `README.md`, `waves/w<NN>.md` of its wave, `problems.md`, `reviews/<feature>.md` of the features with a task in its wave or `👀 review`; a solution file only to resolve a conflict or a failure; `wave-run/task-mode.md` and `wave-run/merge.md` only when its step 1 says so; `wave-run/autonomous.md` only when the plan's flow is autonomous or the arguments are `flow …` ("Flow"); `wave-run/report.md` right before every final report |
| task subagent | its prompt, the solution files (and sections) the prompt names |
| task-mode session | `README.md`, its wave file, the solution files its prompt names; `wave-run/task-mode.md` |
| `wave-plan`, new plan | the index (`index.md`; for a large index also the `triage/P<n>.md` records of its part's problems), `wave-plan/templates.md` when writing files; the README of part J of the index when the part is marked "plan after part J is merged"; in autonomous flow of planning use the README source in "Chained parts and the integration branch" and also read `wave-run/autonomous.md`, "Integration target" |
| `wave-plan`, re-plan | `README.md`, `problems.md`, solution files of the affected P, the wave files where the open entries were found, every wave file not run yet that has a task of an affected feature |
| `wave-triage` coordinator | its `index.md`; the `triage/P<n>.md` records only of problems it re-judges or whose dependency candidates it confirms |
| triage subagent | its prompt; it writes only its assigned `triage/P<n>.md` records |
| `wave-status` | see its skill (READMEs, problem headers, Execution of 🔄/❌/⚠️ waves, review briefs of `👀 review` features and, in autonomous flow, of features merged into the integration branch but not yet into `<main branch>`, index "Parts") |
| `wave-auto` coordinator | `wave-auto/SKILL.md`; of `plans/` only the "Open questions" section of an index on its triage branch, when it asks them; everything else reaches it as return lines ("Coordinated runs") |
| navigator subagent | `wave-auto/navigator.md` and the git state it names; it changes nothing |
| coordinated step subagent | what the row of its skill says; its prompt names the skill and arguments ("Coordinated runs") |
| nobody | `CHANGELOG.md`; `wave-plan/scripts/` (skills run the script, they do not read it) |

A wave file holds everything its wave needs. If something is missing, that is a defect of the plan: record it in `problems.md` and do not look for it in other waves, `history.md` or `archive/`.

## Language

- Talk to the user in the language of the user's messages in this session (the language they write their
  prompts in); if it changes, follow the latest message.
- Everything written to the repository is in English, always: code, comments, docs (README, design and lore
  documents, guides), plan and index files, problem records, task prompts, commit messages, branch names. The
  language of the user's messages, of the user's list or of the existing project does not change this.
- The only non-English text in a written file: the user's words quoted verbatim (`User's words:`, the source
  list), and product text (UI strings, in-game text) that the user asked to be in another language.
- A doc in another language that a task changes is translated to English as a whole by that task: no file
  ends up in two languages. `wave-plan` counts the translation in the task's size; `wave-triage` notes
  "non-English doc" in the problem's **Where**.
- Every subagent prompt that may write to the repository says "write everything in English"; its
  `Report language:` line names only the language of its report.
- A subagent writes its report in the language that its header's `Report language:` line names.

## Run times

Every run of a wave skill (`wave-triage`, `wave-plan`, `wave-run`, `wave-status`, `wave-auto`, including a task-mode session and
the `merge` form) shows when it started and when it ended. Take both times from the system clock with a shell
command (`date "+%Y-%m-%d %H:%M"`, or `Get-Date -Format "yyyy-MM-dd HH:mm"` in PowerShell); never guess or reuse
a time from a file.

- **Start:** read the clock before anything else; the very first line the run prints is
  `Started: <YYYY-MM-DD HH:MM>`. A rule that makes another line "the first line of the report" (a stop line) means
  the first line after it.
- **End:** read the clock again right before the final report; its last line is
  `Started: <YYYY-MM-DD HH:MM> · Finished: <YYYY-MM-DD HH:MM> (<duration, e.g. 1 h 12 min>)`. A stop and a run that
  waits for the user's answer end the same way; a run continued after the user's answer prints a new `Finished`
  line at its next final report, with the original start.
- Skills that write to the repository also record both times where they already record the run, read from the
  clock right before that commit: `wave-run` in the wave file's "Execution" (`Started <…>.` in step 2,
  `Finished <…>.` in step 8, just before a stop line, which stays last; a `merge` run only in its report);
  `wave-plan` in the README header (`planned <start> – <end>`; a re-plan in its `Re-plans:` item); `wave-triage` in the index header
  (`triaged <start> – <end>`). `wave-status` writes nothing. `wave-auto` writes nothing of its own; its steps record
  their times.

## Skill paths
Paths of skill files (`wave-plan/layout.md`, `wave-run/task-mode.md`, `wave-plan/scripts/...`) are relative to the wave skills folder: the folder that holds `wave-triage/`, `wave-plan/`, `wave-run/`, `wave-status/` and `wave-auto/`, which is the parent of the loaded skill's own folder (`.claude/skills/` or `.agents/skills/` for a project install, the plugin's `skills/` for a plugin install). It is not the repository root. Resolve it once from the skill's base directory and use absolute paths when running a script from another folder.

## Version
The skill files carry no version number. A release is a git tag `vMAJOR.MINOR.PATCH` of the wave-method repository; `wave-plan/CHANGELOG.md` (agents do not read it) lists what each release changed.

## Folders

```
plans/
  <date>-<topic>/              a triage index and the plans of its parts
    index.md
    triage/                   records `P<n>.md` of a large index; absent for at most 8 problems
    plan-1/  plan-2/  …        one plan folder per part K of the index (plan slug <topic>-p<K>)
  <date>-<slug>/               a plan made from a raw list (no index)
  archive/                     finished plans and indexes, moved here unchanged
```

- `<date>` is `YYYY-MM-DD` of creation. A plan is addressed by its folder: `plans/2026-11-02-hop-tuning`, `plans/2026-11-02-viewer-polish/plan-2`.
- Plan slugs (2–4 kebab-case words) are unique across `plans/` including `archive/`: branch names are built from them.

## Files of a plan folder
A file is created only when it has content. The smallest plan is `README.md` plus its wave files.

| File | Holds | Created |
|---|---|---|
| `README.md` | header, Features / Waves / Tasks tables, one line per user problem, how to try each feature, known failures, assumptions; ≤ 150 lines | always |
| `waves/w<NN>.md` | one wave (`w01`, `w02`, …): its task table, dependencies, full task prompts; after it ran: its execution log and the closed problems found in it | one per wave |
| `solutions/P<n>-<slug>.md` | the design of one `medium` or `high` user problem (Cause, Approach, API, Algorithm, Limits, Acceptance tests) | one per such problem |
| `solutions/lite.md` | every `low` problem of the plan, one section `## P<n>. <short>` each: the exact edit and one acceptance check | with the first `low` problem |
| `reviews/<feature>.md` | the review brief of one feature (`wave-plan/templates.md`): what each of its tasks did and how to see it, added wave by wave; the full brief once the feature is `👀 review` (`wave-run` step 7) | by `wave-run`, with the feature's first ✅ task |
| `problems.md` | **open** problem-log entries only | with the first entry |
| `history.md` | re-plan and migration notes, audits, anything kept only as history | at the first re-plan |

- Which solution file a problem gets depends only on its difficulty: `low` → a section of `lite.md`, always; `medium`/`high` → its own file, always. A re-plan appends new sections to `lite.md` and new files for the rest.
- A re-plan adds new wave files (new numbers after the last one). It never rewrites a wave file of a wave that ran, except its statuses, "Execution" and "Closed problems". It updates a wave file not run yet when the re-plan changes what that wave's tasks start from (known failures, a check).
- Known failures are written per branch, by exact test name, in README "Known test failures before start" and in every wave file and task prompt that starts from that branch: `<test> — <branch>, until task <ID>`. A check is green when exactly the listed tests fail; one more failure is a problem.
- Design facts belong in solution files, not in `history.md`: a measurement that a solution relies on goes into that solution.

## Model tiers

| Complexity | Meaning | Model tier |
|---|---|---|
| `low` | mechanical edit from an exact description | Haiku 5.5 (`claude-haiku-5-5`) / GPT-6-Luna (`gpt-6-luna`) (or any stronger model) |
| `medium` | implementation of a given solution, several files, its own tests | Sonnet 5.5 (`claude-sonnet-5-5`) / GPT-6.2-Sol (`gpt-6.2-sol`), GPT-6.1-Sol (`gpt-6.1-sol`) (or stronger) |
| `high` | design uncertainty remains that cannot be removed upfront | Opus 5.5 (`claude-opus-5-5`) / GPT-6.2-Astra (`gpt-6.2-astra`) |

A task never runs below its tier; a `high` task never runs on a medium model. A plan README may add a line `Models: <complexity> = <model>, …` naming concrete models of the same or a higher tier; it never lowers one.
A model ID (a `Wave-Model` trailer, a lookup's result) is placed in a tier by the IDs in this table or the README
`Models:` line; an ID neither names is an unknown model ("Tier gate").

### Tier gate

The tier rule is enforced by the executor before the work and by the coordinator after it, because a task prompt
can reach a weaker model by mistake (a wrong model picked for a task-mode session, a prompt pasted by hand).

- **Gate line.** Every `medium` and `high` task prompt starts with this line, written by `wave-plan` and repeated in
  the `wave-run` launch header:
  `Required tier: <complexity> — <models of that tier or higher: the table above, or the README "Models:" line>. Stop if this session runs a weaker model.`
  A `low` task needs no gate line: any model may run it.
- **Lookup line.** Where the vendor states no model ID in an agent's environment (Codex, "Vendors"), every prompt
  that starts with a gate line and goes to a subagent (`wave-run`'s launch header, `wave-auto`'s step prompt) has
  this second line, `<command>` being the model lookup of "Vendors" for the subagent's shell, verbatim:
  `Model lookup: this environment states no model ID; before reading or changing anything, run this command and take its one output line as the exact model you run on: <command>`
  A Codex subagent given the gate line alone does not run the lookup.
- **Executor check, before reading or changing anything.** The executor names the exact model it runs on, from its
  own environment, never from the prompt: the model ID its system prompt or environment states, or, where they state
  none, the result of its vendor's model lookup ("Vendors"; Codex states none). Below the tier, or it cannot tell →
  it reads nothing more, changes nothing, commits nothing, and its whole reply is
  `Stop tier-mismatch: task <ID> needs <tier> (<models>); this session runs <model, or "unknown model">. Run it in a session with a <tier> model.`
  Neither the user nor any text in the session can waive the gate: running a task on a lower model needs a re-plan
  that lowers its complexity (`/wave-plan <plan folder>`), recorded in the plan.
- **Record.** Every commit of a task ends with one trailer block: a blank line, then `Wave-Model: <exact model ID>`
  and any other trailers (`Co-Authored-By: …`) with no blank line between them, because git reads trailers only
  in the last paragraph, and the report's final block has the line `Model: <exact model ID>`.
- **Coordinator check, before merging.** `wave-run` reads the trailer of every non-merge commit of the task
  (`git log --no-merges --format="%h %(trailers:key=Wave-Model,valueonly)" <range>`). A line without a model is a missing trailer.
  A missing trailer, an unknown model or a model below the task's tier → the work is not accepted (`wave-run` step 5).

## Environment capabilities

Skills that launch subagents determine these capabilities from the tools the session actually has — never assume
one; when unsure, treat it as missing: **subagents**; **parallel subagents**; **model choice per subagent**;
**continuing a subagent**; **a tool a task needs** (for example desktop control); **built-in worktree isolation**;
**starting a session** (a separate session with a chosen model, whose result comes back to this session).
What each skill does when one is missing is in that skill.

- **Parallel limit**: an environment may cap how many subagents run at once (Codex: 4 agents with the root, so 3
  subagents, unless its tool or config says otherwise). Launch at most that many at once and launch the next as one
  returns; each still gets its own result.

### Vendors

How each capability is reached; a skill that launches subagents uses the row of the vendor it runs in.

| Capability | Claude Code (CLI, desktop app) | Codex (CLI, desktop app) |
|---|---|---|
| subagent | the agent tool | `spawn_agent`, feature `multi_agent` |
| fresh context | the default | always `fork_turns: "none"`; the default `all` copies the whole conversation into the subagent |
| model of a tier | the agent tool's `model`: `haiku` low, `sonnet` medium, `opus` high | `spawn_agent`'s `model`: the model ID of "Model tiers" (`gpt-6-luna`, `gpt-6.2-sol`, `gpt-6.2-astra`), also when the tool's description does not list it; a model the tool refuses is a missing tier |
| parallel | several agent calls in one message | several `spawn_agent` calls, at most the parallel limit (3); then `wait_agent` |
| waiting | the agent call returns its result | call `wait_agent` (`timeout_ms` up to 3600000) again until `list_agents` shows every launched subagent completed; its result is its final message |
| continuing a subagent | the environment's message tool, where it has one | `followup_task` with the subagent's `task_name` |
| starting a session | the desktop app's session tools; none in the CLI | none in the CLI; the desktop app as its rehearsal recorded (`docs/rehearsals/coordinator-codex-desktop.md`) |
| own model ID | stated in the system prompt | not stated: the model lookup below |
| git writes | a permission mode that allows git and file writes in the repository and in `../<repo-folder>.worktrees/` (`auto` does) | the permission profile of "Permissions in Codex", in a trusted project; the default `workspace-write` keeps `.git` read-only |
| non-interactive run | `claude -p "<prompt>"`, then `claude -p --continue "<answer>"` | `codex exec "<prompt>" < /dev/null`, then `codex exec resume --last "<answer>" < /dev/null` |

**Model lookup in Codex.** Codex records every thread in
`<CODEX_HOME>/sessions/YYYY/MM/DD/rollout-<time>-<thread id>.jsonl` (`CODEX_HOME` defaults to `~/.codex`); every shell
of a thread has its ID in `CODEX_THREAD_ID`, and the thread's last `turn_context` record names its model. Run one of
these; its one output line is the model ID, or `unknown model` (no thread ID, no rollout file: an `--ephemeral` run):

```bash
m=$(f=$(find "${CODEX_HOME:-$HOME/.codex}/sessions" -name "rollout-*-${CODEX_THREAD_ID:-none}.jsonl" 2>/dev/null | head -1); [ -n "$f" ] && grep '"type":"turn_context"' "$f" | tail -1 | grep -o '"model":"[^"]*"' | head -1 | cut -d'"' -f4); echo "${m:-unknown model}"
```

```powershell
$h = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }; $f = Get-ChildItem (Join-Path $h 'sessions') -Recurse -Filter "rollout-*-$env:CODEX_THREAD_ID.jsonl" -ErrorAction SilentlyContinue | Select-Object -First 1; $l = if ($f) { Select-String -LiteralPath $f.FullName -Pattern '"type":"turn_context"' | Select-Object -Last 1 }; if ($l -and $l.Line -match '"model":"([^"]+)"') { $Matches[1] } else { 'unknown model' }
```

**Permissions in Codex.** The wave skills write branches, refs and commits in `.git` and create worktrees next to
the repository (`../<repo-folder>.worktrees/`). Codex's `workspace-write` sandbox keeps the `.git` of every writable
folder read-only, so they need this permission profile, in `<repository>/.codex/config.toml` of a trusted project
("Trust" below) or in `~/.codex/config.toml`. Paths are absolute (`~/…` allowed); `<parent>` is the folder that
holds the repository:

```toml
default_permissions = "wave"

[permissions.wave]
filesystem = { ":root" = "read", "<parent>" = "write", ":tmpdir" = "write", "<repository>/.codex" = "read" }
```

**Trust.** Codex applies a project's `.codex/config.toml` only when `~/.codex/config.toml` trusts the project: an
entry under the absolute path of the repository root, in single quotes (Windows paths with backslashes, any letter
case):

```toml
[projects.'<repository>']
trust_level = "trusted"
```

In a project without it Codex runs the thread with its built-in `:read-only` profile, and every git write stops
`git-read-only`. For one `codex exec` run, `-c "projects={'<repository>'={trust_level=\"trusted\"}}"` (bash quoting)
trusts it without changing the file. A profile given on the command line (`-c 'default_permissions="wave"'` with
`-c 'permissions.wave.filesystem={…}'`) applies without trust; Codex then adds the entry itself, as it does when a
run in a new folder gets write access.

The sandbox stays on: the agent reads everything, writes only below `<parent>` and in the temp folder, and cannot
change its own profile. Subagents inherit it. Keep the file out of git (`.git/info/exclude`): its paths belong to
one machine. On Windows the sandbox keeps denying `.git` to a folder that was a writable folder of an earlier
`workspace-write` session holding that repository, the temp folder included: keep the repository out of the temp
folder and do not use such a folder as `<parent>`. Where the profile cannot be used, full access works
(`codex -s danger-full-access`). Every wave skill whose git write is refused stops `git-read-only`:
`Stop git-read-only: <the refused path> — next: grant the permissions of wave-plan/layout.md, "Vendors", "Permissions in Codex", then run the same command again`.

## Names

- `<main branch>` — the repository's main branch (`master` or `main`), in every flow.
- `<main>` — where approved features are merged: `<main branch>` in manual flow, the plan's integration branch in
  autonomous flow ("Flow"). `wave-run` and `wave-status` resolve it by the flow, `wave-plan` by its
  flow of planning ("Planning in autonomous flow"); `wave-triage` always uses `<main branch>`.
- `<main checkout>` — the checkout where those merges are made: the repository's main checkout in manual flow, the
  integration worktree in autonomous flow.
- `<name>` — the name of the plan's integration branch after `integration/`: from `target:` of the README `Flow:`
  line, else `<plan>` ("Flow"). Used in autonomous flow only.
- `<plan>` — the plan slug from the README header (`slug: …`).
- `<plan folder>` — the plan folder's path relative to the repository root (`plans/2026-11-02-hop-tuning`).
- `<feature>` — `<feature-id>-<feature-slug>` from the "Features" table (e.g. `F1-cheap-interbody-omega`).
- `<task>` — `<task-id>-<task-slug>` from the "Tasks" table (e.g. `D-signed-speed-readouts`).

| What | Branch | Worktree (outside the repository) |
|---|---|---|
| tracking | `plan/<plan>` | `../<repo-folder>.worktrees/<plan>-plan` |
| feature | `feat/<plan>/<feature>` | `../<repo-folder>.worktrees/<plan>-<feature-id>` |
| task | `task/<plan>/<feature-id>-w<N>-<task>` | `../<repo-folder>.worktrees/<plan>-w<N>-<task-id>` — only when another task of the same feature runs at the same time (`wave-run` step 4) |
| integration (autonomous flow) | `integration/<name>` | `../<repo-folder>.worktrees/integration-<name>` |

Example: plan `interbody-periapsis`, feature F1, wave 2, task D → `feat/interbody-periapsis/F1-cheap-interbody-omega`, `task/interbody-periapsis/F1-w2-D-signed-speed-readouts`.

## Commands

Every command a skill gives the user is printed in both forms, Claude Code first:
`/wave-run <args>` · `$wave-run <args>`. In a table cell both forms are separated by `<br>`. The arguments
are identical; only the first character differs.

## Statuses

| Item | Statuses |
|---|---|
| Task | ⬜ not started · 🔄 in progress · ✅ done · ⚠️ open problem · ❌ not done · ➖ superseded by X / dropped |
| Wave | ⬜ not started · 🔄 since <date time> · ✅ done · ⚠️ done, open problems · ❌ stopped · ➖ dropped (never ran) |
| Feature | ⬜ not started · 🔄 in progress · 👀 review · ✅ merged · ⚠️ blocked · ➖ dropped |

A feature is `👀 review` when all its tasks are ✅ or ➖ and its full check is green; it is merged only after the
user's review ("Feature review") or, in autonomous flow, after auto-approval ("Flow"). 👀 is not ✅: the feature is
finished but not in `<main>` yet. A README written by v2.1.0 may still say `✅ ready`; read it as `👀 review`, and the
next commit that touches the row writes `👀 review`. In autonomous flow `✅ merged` means merged into the integration
branch.

Every feature that is not `✅ merged` or ➖ has a `Waiting for` cell: `wave <N>` (its next tasks), `I<n>` (an open entry), `review` (ready, waits for the user's review and approval), `main-dirty` (approved, `<main checkout>` was not ready for the merge), `user: <question>`. The cell is empty once the feature is merged.

**A status shows the current outcome, not the history.**

- ⚠️ and ❌ mean "action needed now". Each ⚠️/❌ item names at least one open entry of `problems.md` (`⚠️ I4`), or, for a ❌ wave, says that it must be re-run.
- When the last open entry concerning an item is closed, the item becomes ✅ with a short note: `✅ (fixed by AB, wave 6)`. A task that will never run because another replaces it is `➖ superseded by AA`; a wave whose tasks all moved elsewhere is `➖ dropped (tasks → wave 7)`. ➖ is final and is not a problem.
- Whoever closes an entry updates the items it concerns in the same commit: `wave-run` (step 8 of the wave that fixed it, or when the user accepts it), `wave-plan` at a re-plan (an item superseded by new tasks becomes ➖ at once; an item waiting for fix tasks stays ⚠️ with `→ task Y`).
- **Status check** (run by `wave-run` in step 8 and before archiving, by `wave-plan` before committing): no ⚠️/❌
  item without an open entry or a re-run note, and no open entry whose items are all ✅ or ➖. It also checks the
  README `Flow:` line ("Flow"): `flow-line` for a malformed line, `flow-review-unknown` for a `manual review:`
  ID that is not a feature. It also reports `merged-fields` for a feature that is ✅ merged without a `Merged`
  hash or with a `Waiting for`, and for a feature that is not ✅ merged but has a `Merged` hash.
  It checks the README `Re-plans:` record ("Re-plan escalation"): `replan-fixes` for a malformed part or an unknown
  feature, `replan-escalation` for a round recorded without its escalation, override or manual review.
  History (what failed, how it was fixed) lives in the wave files and `history.md`, never in a red mark. Run it
  with `python <wave skills folder>/wave-plan/scripts/status_check.py <plan folder>` (absolute script path, see
  "Skill paths"; in the tracking worktree); fix every printed line. Without Python, check by hand by this rule.

## Running waves
A wave is running while its status in README "Waves" is `🔄 since <YYYY-MM-DD HH:MM>` on the tracking branch (`git show plan/<plan>:<plan folder>/README.md`). This mark is the lock: `wave-run` commits it when the wave starts and removes it with the wave's "done" or "stopped" commit.

- While a wave runs, only its coordinator (and the task sessions it asked for) changes the plan folder, its tracking worktree and its feature and task worktrees: no re-plan, no other wave, no renames, no manual fixes. Reading is fine. Any other skill or agent that wants to change them tells the user and stops.
- A wave whose Execution ends with `Waiting: task mode <IDs>` is resumed by `/wave-run <plan folder> <N>` · `$wave-run <plan folder> <N>` (`wave-run`, "Environment capabilities").
- A lock left by a session that is gone is released only by the user's decision.
  So is a target claim of autonomous flow ("Target claim") and a coordinator claim ("Coordinated runs").

## Problem log
`problems.md` is created with the first entry:

```
# Open problems
Next ID: I2

- **[I1 · wave 4 / task E / feature F3] <one-line essence>** — where: `file:line`; expected / got;
  proposal: …; status: open | → task Y (wave M)
```

IDs `I1, I2, …` are unique in the plan and never reused; `Next ID` stays in the file even when it has no entries. Write the essence so the next planner understands it without reading transcripts. An entry is **closed** when its status becomes `fixed in <commit> (task Y)`, `verified by <task> on <commit>`, `accepted by the user on <date>` or `won't fix: <reason>`. A closed entry leaves `problems.md` in the same commit: it moves to "Closed problems" of the wave file where it was found (`history.md` if it came from a re-plan or audit, not from a wave). `→ task Y` is still open.

## Re-plan escalation

A feature whose fixes keep failing must not cycle between `wave-run` and `wave-plan` without limit. The count lives in
the README header, which every skill reads.

- **Record.** Every re-plan adds one sub-item to the README `Re-plans:` item (`wave-plan/templates.md`). Its text ends
  with these parts, in this order, each only when it has content:
  - `· fixes: F<k> (I<n>, …), …` — every feature for which this re-plan planned new tasks from open entries found in a
    wave (an entry whose header starts `[I<n> · wave`), each with those entries. Entries from the user's review
    (`[I<n> · review / …]`) do not count; a feature with only such entries is not listed;
  - `· escalated: F<k>, …` — the features of `fixes:` at round 2 or later;
  - `· override: F<k>, …` — the features of `fixes:` re-planned past the limit by the user's direction.

  A sub-item written before this rule has no parts and names no feature.
- **Round.** The round of a feature at a re-plan is 1 + the number of earlier `Re-plans:` sub-items whose `fixes:`
  names it.
- **Round 1:** a normal re-plan.
- **Round 2 or later: escalated.** For every open entry of the feature that the re-plan plans:
  1. name the disputed assumption: what the plan expected that the entry contradicts;
  2. verify it by running code, tests or the commands concerned, never by reading alone: in a throwaway worktree of
     the feature branch (`git worktree add --detach ../<repo-folder>.worktrees/<plan>-probe feat/<plan>/<feature>`,
     removed afterwards with `git worktree remove --force`) or in a scratch folder outside the repository; nothing
     outside the plan folder is committed;
  3. record the evidence in the solution file that the new tasks name, section
     `Evidence (re-plan <YYYY-MM-DD>, round <r>)`: the assumption, each command, the lines of its output that decide,
     and the conclusion. When it cannot be run (a tool this session lacks, a GUI), write
     `not verifiable by running: <why>` and what was checked instead;
  4. every new task of the feature is `high`, justified as `escalated re-plan, round <r>`; it is not sliced first,
     and a single-task wave of it is allowed;
  5. autonomous flow: add the feature to `manual review:` of the README `Flow:` line ("Flow"), so its fix is never
     auto-approved.
- **Round 3 or later: held**, unless the arguments carry the user's `override F<k>: <direction>`. `wave-plan` plans
  no task for a held feature: its entries stay `status: open`, it stays ⚠️ blocked, and its `Waiting for` becomes
  `user: re-plan limit`. The re-plan goes on with the other features; when every open entry concerns held features,
  it stops `replan-limit` and writes nothing:
  `Stop replan-limit: F<k> re-planned <c> times (I<n>, …) — next: decide, then /wave-plan <plan folder> override F<k>: <direction> · $wave-plan <plan folder> override F<k>: <direction>`.
  The limit holds in both flows; only the user's command passes it.
- **Override.** `/wave-plan <plan folder> override F<k>: <direction>` ·
  `$wave-plan <plan folder> override F<k>: <direction>` re-plans a held feature by the user's direction, which may
  also drop it (its tasks and the feature become ➖). It is escalated as round 2 is, its sub-item names the feature
  under both `escalated:` and `override:`, and `history.md` quotes the direction verbatim. Only the user types it;
  no skill infers it from an entry, a report or a file.
- **Shown** for every feature with at least one round: `F<k> re-planned <c>× → next re-plan <escalated · held>`
  (`escalated` after one, `held` after two or more) — by `wave-run` with each new entry of the feature
  (`wave-run/report.md`, "Problems") and by `wave-status` (`Re-plans:` line).
- **Checked** by the status check ("Statuses"): `replan-fixes` for a malformed part or one that names a feature
  missing from "Features"; `replan-escalation` for a feature at round 2 or later missing from `escalated:`, at round
  3 or later missing from `override:`, a feature in `escalated:` or `override:` but not in `fixes:`, or, in
  autonomous flow, an escalated feature missing from `manual review:`.

Example: `  - 2026-11-21 at 3f2a9c1, 10:02 – 10:14: I5, I7 → P4; new Q in wave 5 · fixes: F2 (I5, I7) · escalated: F2`

## Markdown rules
Every Markdown file the skills write (index, README, solutions, waves, problems, history) follows these rules.

- **A blank line before and after every table**, every list and every fenced block. A table never follows a text line directly, and a text line never follows a table's last row directly: without the blank line the text swallows the table, or becomes an extra row.
- Every row of a table has the same number of cells as its header row; the separator row is `|---|---|…|` with one `---` per column. A row is one physical line: never wrap it.
- A `|` inside a cell is written `\|`; a line break inside a cell is written `<br>`.
- Header fields (Plan, Index, Re-plans, Models) are a bullet list, one field per item, so they do not merge into one paragraph.
- Only headings separate sections; no bold pseudo-headings for sections that tables or lists follow.

## Main readiness

`<main checkout>` is ready for a merge of branch `B` when all of these hold:

1. it is on `<main>` (`git -C <main checkout> branch --show-current`);
2. its index has no staged changes (`git -C <main checkout> diff --cached --quiet`) — git refuses a merge
   otherwise;
3. no unstaged tracked change touches a path the merge changes: the paths of
   `git -C <main checkout> diff --name-only` and of `git diff --name-only <main>...B` do not intersect.

Untracked files never matter. Not ready → `main-dirty`, with the reason (`not on <main>`, `staged changes`, or
the overlapping paths). Never stage, unstage, stash, reset or check out anything in `<main checkout>` to make it
ready.

## Feature review

A feature branch `feat/<plan>/<feature>` holds only its own feature: its tasks run on it or on task branches merged
back into it, every other feature has its own branch, and `<main>` (merged in before each wave and before review)
brings in only merged features. So the feature branch is the branch the user reviews; each ready feature is offered
on its own and can be merged alone, in any order. Its brief `reviews/<feature>.md` on the tracking branch
(`wave-run/SKILL.md` steps 7 and 8) keeps the record: the essence, how to test it, what each task did, the check
result. The user sees only the short **review block** below — in the `wave-run` report, in `wave-status` and in
the `merge` form — so they can review the feature without reading the plan.

Review block, in the user's language and plain words, at most about ten lines:

```
**F1 · <title>** · `feat/<plan>/<feature>` · `<feature worktree path>`
<Essence: what changes for the user once it is merged, before → after, one or two sentences.>
How to test:
1. <an action specific to this feature> → <what the user should see>
2. …
Worth a look: <only when there is something the user may not expect; otherwise no such line>
Merge: `/wave-run <plan folder> merge F1` · `$wave-run <plan folder> merge F1`
```

- "How to test" holds only the steps specific to this feature, at most five, each with its expected result. Never
  how to build, start or test the project, `cd`, the test suite or its counts: the user knows their project. A
  feature with nothing to see by hand (a refactoring, CI, a library change) gets one step: the command that shows
  it works and what its output proves. Nothing recorded → `How to test: not recorded — <Done when>`.
- Not in the block: the task list, the check result, test counts, commits, diff statistics, where the text came
  from. They stay in the brief and the git history.
- `wave-run` leaves out the `Merge:` line: its step 10 asks instead. `main-dirty` adds one line with the reason.

A feature merged into an integration branch (autonomous flow, "Flow") is shown with its **merged block**: the review
block with two lines changed, built from the same brief, so the user can test it in the integration worktree, where
it sits together with the other features merged since the user's last merge:

```
**F1 · <title>** · merged into `integration/<name>` `<hash>` · `<integration worktree path>`
<Essence>
How to test:
1. <an action specific to this feature> → <what the user should see>
Worth a look: <as in the review block>
Approved: <auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review · by the user>
```

The brief stays on the tracking branch after the merge, in every flow; nothing deletes it, and archiving moves it
with the plan.

The user reviews the code with `git log --oneline --no-merges <main>..<branch>` and `git diff <main>...<branch>`
when they want to; skills do not print these commands in the block.

- **Approval** is one of: an answer in the `wave-run` session that names the feature (`merge F1`); the command
  `/wave-run <plan folder> merge <F-IDs>` · `$wave-run <plan folder> merge <F-IDs>`; the user's own `git merge` of
  the branch into `<main>` (a merge commit or a fast-forward; a squash merge is not detected). Silence, `later`
  or a general "ok" for several features is not an approval. In autonomous flow the auto-approval of `wave-run`
  ("Flow", "Auto-approval") is the approval too; it merges into the integration branch only. In manual flow no
  skill merges a feature on its own.
- **Merge hash** of a branch the user merged: the last line of
  `git log --merges --ancestry-path --format=%h <branch>..<main>`; none → the branch head (a fast-forward).
- **Rejection**: the user's findings become open entries `[I<n> · review / feature F<k>]`, and the feature becomes
  ⚠️ blocked; a re-plan adds fix tasks to the same feature.

## Flow

A plan runs in one of two flows. The flow decides only who approves a `👀 review` feature and where an approved
feature is merged. Merge mechanics (`wave-run/merge.md`), the tier gate, never pushing, never committing directly on
`<main branch>` and never merging a feature partially are the same in both.

| Flow | Who approves a `👀 review` feature | Merged into | Questions to the user |
|---|---|---|---|
| `manual` (default) | the user ("Feature review") | `<main branch>` | at the points of the decision table |
| `autonomous` | `wave-run` when "Auto-approval" holds; the user for a feature under manual review | the integration branch ("Integration target") | none |

The flow is a header field of the plan README:

```
- Flow: autonomous · target: integration/<name> · manual review: F2, F5
```

- A README without a `Flow:` line, or with `- Flow: manual`, is in manual flow and behaves exactly as if this section
  did not exist.
- `target:` names the integration branch; without it the target is `integration/<plan>`. A plan of an index part in
  autonomous flow names `integration/<topic>`: all parts of an index share one integration branch
  ("Planning in autonomous flow").
- `manual review: <F-IDs>` is optional: these features are never auto-approved. Each stays `👀 review` with
  `Waiting for: review` until the user approves it ("Feature review"), and every wave whose `Depends on:` names it
  stops `feature-unmerged` until then.
- `wave-plan` writes the line only when its flow of planning is autonomous ("Planning in autonomous flow").
  Afterwards it is changed only by the flow form `/wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` ·
  `$wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` (`wave-run/autonomous.md`, "Flow form") and by
  an escalated re-plan, which adds a feature to `manual review:` ("Re-plan escalation"); both only while no wave of
  the plan is 🔄: a flow never changes inside a running wave.
- `wave-run` reads the flow from the README on the tracking branch in its step 1 and keeps it for the whole run,
  including the resume of a task-mode wait. `wave-plan` and `wave-triage` follow their flow of planning instead
  ("Planning in autonomous flow").
- Switching to manual is refused while the integration branch has commits `<main branch>` does not have (stop
  `target-unmerged`): the user merges it first, so every feature branch again differs from `<main branch>` only by
  its own feature.

### Integration target

In autonomous flow `<main>` is the integration branch and `<main checkout>` the integration worktree ("Names"). Every
merge that manual flow makes into `<main branch>` goes there instead; autonomous flow never changes `<main branch>` or
the main checkout.

- `wave-run`, and `wave-plan` in autonomous flow of planning, create the integration branch from the head of
  `<main branch>`, in the integration worktree, when it is missing, and merge `<main branch>` into it before a wave or
  before planning when `<main branch>` has commits it lacks
  (`wave-run/autonomous.md`, "Integration target"). Nothing else checks it out.
- It receives only `merge --no-ff`: approved feature branches, the tracking branches of its plans and `<main branch>`.
  Nothing is committed on it directly.
- **Plans of a target** are the plans whose own README, on their tracking branch, has a `Flow:` line naming
  `integration/<name>` — for each branch of `git branch --list "plan/*"`,
  `git grep -l -E "^- Flow: autonomous · target: integration/<name>( ·|$)" <branch> -- "plans/*README.md" ":!plans/archive"`.
  Use a result only if its README slug is that of the tracking branch; inherited READMEs are not authoritative.
  They write the same worktree, so their waves never run at the same time: while a wave of one of them is 🔄,
  `wave-run` and `wave-plan` of another stop `wave-running`.
  The atomic guard is the target claim ("Target claim"); this read of 🔄 marks stays as a second guard.
- The user reviews it as one diff, `git diff <main branch>...integration/<name>`, and merges it into `<main branch>`
  themselves (`git merge --no-ff integration/<name>` in the main checkout). No skill does.
- Autonomous flow refuses to start a wave when it cannot guarantee this: stop `target-unsafe` before anything is
  written, when `target:` is not `integration/<name>`; the integration branch is checked out anywhere but the
  integration worktree; or the integration worktree is not on that branch, has tracked changes, or has an unfinished
  merge.

#### Target claim

Every run that writes the integration worktree claims the target first and holds the claim until its last write: a
wave and the merge form of `wave-run` in autonomous flow, and `wave-plan` in autonomous flow of planning (a new plan or
a re-plan). The flow form of `wave-run`, a task-mode session (`… task <ID>`) and `wave-status` write nothing there and
take no claim.

- The claim is the ref `refs/wave-method/claims/integration/<name>`, which every worktree of the repository shares. It
  points to a blob whose one line names the holder, in ASCII only: `<plan> wave <N> <YYYY-MM-DD HH:MM> run <token>`,
  `<plan> wave <N> waiting <YYYY-MM-DD HH:MM> run <token>` (a wave waiting for task mode),
  `<plan> merge <YYYY-MM-DD HH:MM> run <token>` or `<plan> planning <YYYY-MM-DD HH:MM> run <token>`. Where another
  text names a holder line without ` run <token>`, the run appends it. `<token>` is eight random hex characters,
  chosen once per run, so no two runs hold the same oid:

  ```bash
  token=$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n')
  ```

  PowerShell: `$token = [guid]::NewGuid().ToString('N').Substring(0, 8)`.
- **Take** it by creating the ref with the zero object ID as its expected old value. Git creates the ref only when it
  does not exist, so of two runs that start together exactly one gets it:

  ```bash
  oid=$(printf '%s\n' "<holder line>" | git hash-object -w --stdin)
  git update-ref refs/wave-method/claims/integration/<name> "$oid" 0000000000000000000000000000000000000000
  ```

  PowerShell: `$oid = "<holder line>" | git hash-object -w --stdin`, then the same `git update-ref`. When
  `git rev-parse --show-object-format` prints `sha256`, the zero ID has 64 zeros. Keep the oid: every later step of
  the claim needs it. Print it (`echo "$oid"`; PowerShell `$oid`), keep it in the conversation and
  write it out literally in each later command (wait, takeover, release): shell variables do not survive from one
  command to the next, and a file is shared by every run on the machine, so a second run would overwrite it and the
  first could no longer release its claim. Never store the token or the oid in a file, not even in a temp folder. A lost oid is
  recomputed from the exact holder line by the take's first command without `-w`
  (`printf '%s\n' "<holder line>" | git hash-object --stdin`).
- **Refused** (the ref exists): read the holder with `git cat-file -p refs/wave-method/claims/integration/<name>` and
  stop `wave-running`, naming the holder line; nothing written. Only a resume takes over a held claim ("Take over"
  below).
- **Nothing written** by a refused claim, wait or takeover means: the attempt changed no ref, branch, worktree, commit
  or worktree file. `git hash-object -w` stores the holder blob before `git update-ref` tries the ref (git refuses a ref to a
  missing object), so each refused attempt may leave one unreachable loose blob in the object store; `git gc` prunes
  it later (after `gc.pruneExpire`, two weeks by default). Check that a stop wrote nothing by comparing refs and
  worktrees, not the object store.
- **Wait**: a wave that ends with `Waiting: task mode …` keeps the claim (it is still 🔄) and marks it as waiting,
  right after its "waiting for task mode" commit: store the line `<plan> wave <N> waiting <YYYY-MM-DD HH:MM> run
  <token>` with `git hash-object -w --stdin` as above, as `$wait`, then
  `git update-ref refs/wave-method/claims/integration/<name> "$wait" "$oid"`. Exit 0 → the claim now has the oid
  `$wait`. Otherwise the claim is no longer this run's: stop `wave-running`, naming the holder, instead of the
  waiting report.
- **Take over**: a `wave-run` that resumes a wave waiting for task mode (`wave-run/task-mode.md`) reads
  `cur=$(git rev-parse -q --verify refs/wave-method/claims/integration/<name>)` (PowerShell: `$cur = …`, the same
  command), then:
  - no ref: take the claim as above;
  - the holder line (`git cat-file -p "$cur"`) is the waiting line of this plan and wave: store this run's own line
    `<plan> wave <N> <YYYY-MM-DD HH:MM> run <token>` as `$oid`, then
    `git update-ref refs/wave-method/claims/integration/<name> "$oid" "$cur"`. Git moves the ref only while it still
    points to `$cur`, so of two resumes exactly one takes it over. Exit 0 → this run holds the claim with `$oid`;
    otherwise read the holder again and stop `wave-running`, naming it;
  - any other holder line, the running line of this same wave included (another resume runs it): stop
    `wave-running`, naming it.
- **Release** it right after the run's last write, and before the report of any stop after the claim:
  `git update-ref -d refs/wave-method/claims/integration/<name> "$oid"`. The expected old value, unique by its token,
  keeps a run from deleting a claim that is not its own. A run that did not get the claim releases nothing.
- A claim left by a session that is gone is released only by the user's decision ("Running waves"), with
  `git update-ref -d refs/wave-method/claims/integration/<name>` once no run holds it. `wave-status` shows every claim.

### Auto-approval

In autonomous flow `wave-run` approves a `👀 review` feature itself only when all of these hold. It checks them right
before the merge (`wave-run/autonomous.md`, "Auto-approval"):

1. every task of the feature, in every wave, is ✅ or ➖;
2. its full check is green after `<main>` was merged into its branch, and that merge changed none of the feature's own
   lines (`wave-run/merge.md`, "Merge one feature", step 1);
3. no open entry of `problems.md` concerns the feature or one of its tasks;
4. the tier gate is clean: every commit of the feature branch whose subject names one of its tasks
   (`<plan> <feature-id> / <task-id>: …`) has a `Wave-Model` trailer naming a model of that task's tier or higher
   ("Tier gate");
5. the feature is not listed under `manual review:`.
6. its scope is clean: every path that a non-merge commit of `<main>..feat/<plan>/<feature>` touched
   (`git log --no-merges --name-only --format=`) is in scope for one of the feature's tasks as `wave-run/SKILL.md`
   step 5, "Scope", defines it.

| Condition that fails | The feature |
|---|---|
| 5 | stays `👀 review`, `Waiting for: review`, until the user approves it |
| 1, 2, 3, 4 or 6 | becomes ⚠️ blocked, `Waiting for: I<n>`, naming its open entry (a new entry for 2, 4 and 6) |
| `<main checkout>` is not ready ("Main readiness") | stays `👀 review`, `Waiting for: main-dirty` |

The run goes on with everything that does not depend on a feature left unmerged.

### Results of an autonomous run

What the user is shown after an unattended run, by every reader (the `wave-run` report, `wave-status`, the `wave-auto`
final report, a driver's summary): per plan in autonomous flow, from its README and briefs on the tracking branch:

| Feature | Shown as |
|---|---|
| `✅ merged`, and its `Merged` hash is not in `<main branch>` yet (`git merge-base --is-ancestor <hash> <main branch>` fails) | its merged block ("Feature review") |
| `👀 review` | its review block, with the `Merge:` line |
| ⚠️ blocked | one line: `F<k> <title> — ⚠️ I<n>: <essence of the entry>` |
| 🔄 or ⬜ | one line: `F<k> <title> — <status>, waiting for <Waiting for>` |

Merged features drop out of this view once the user has merged the integration branch into `<main branch>`. A feature
without a brief (a plan run by an older `wave-run`) is shown as `wave-status` builds a missing brief.

### Decision table

Every point where `wave-run` asks the user or waits for them. Manual flow is the behaviour of `wave-run/SKILL.md` and
`wave-run/merge.md`; autonomous flow follows `wave-run/autonomous.md`. To **skip** a task (`wave-run/autonomous.md`,
"Skipped tasks") is to not launch it and mark it ⚠️ with the entry that blocks it.

| Point | Where | Manual flow | Autonomous flow |
|---|---|---|---|
| a feature is `👀 review` | step 10; merge form without a wave | ask per feature; merge only what the user approves | "Auto-approval"; no question |
| open entries concern this wave | step 1 | show them and ask whether to proceed; no → stop `open-problems` | proceed; skip the tasks of a feature that has an entry with `status: open` |
| task branches of this wave exist | step 1 | ask: continue from them, delete them, or stop `leftover-branches` | never reuse or delete them: stop `leftover-branches` |
| `Depends on: F<k> merged` and F<k> is not `✅ merged` | step 1 | stop `feature-unmerged` | the same stop; "Auto-approval" has usually merged F<k> before |
| a feature check is red before the wave | step 3 | stop `red-before-wave` | new entry; the feature is ⚠️ blocked; skip its tasks; the wave goes on |
| an out-of-scope edit, or unusable direct work | step 5 | entry; ask the user; never cleaned up by a new commit | entry; do not merge the task (a direct task is reverted, never cleaned up by a new commit); the task is ⚠️ and the feature ⚠️ blocked; skip its dependants |
| a merge conflict would change a plan solution | step 6 | stop `design-conflict` | abort the merge; entry; the task is ⚠️ and the feature ⚠️ blocked; skip its dependants; the wave goes on |
| a task stays red after 2 attempts | fix loop | the task is ⚠️; stop `red-after-merge` if no other task can continue | the same |
| no model of a task's tier; a session or work below its tier | steps 1 and 5, task mode | stop `tier-missing` or `tier-mismatch`; the work runs again on its tier | the same; never waived |
| a task needs task mode | step 4 | `Waiting: task mode` with one command per task | the same; whoever drives the run starts those sessions |
| merging `<main>` into a ready feature changed its own lines | `merge.md` step 1 | show the resolution and ask again | not merged: entry, the feature ⚠️ blocked |
| `<main checkout>` is not ready for a merge | `merge.md` step 2 | ask the user to clear it; `main-dirty` if left for later | `main-dirty`; no question |
| every feature is merged | step 8; `merge.md` "Record" | archive the plan ("Archive") | no archive: the tracking branch stays until the user merged the integration branch |

### Planning in autonomous flow

`wave-triage` and `wave-plan` run before a plan README exists, so they take their **flow of planning** from, in this
order:

1. the arguments: `flow autonomous` or `flow manual` as their first two words, for example
   `/wave-plan flow autonomous plans/<date>-<topic>/index.md part <K>` ·
   `$wave-plan flow autonomous plans/<date>-<topic>/index.md part <K>`, or
   `/wave-triage flow autonomous <list>` · `$wave-triage flow autonomous <list>`;
2. for `wave-plan` of an index part: the index header line `- Flow: autonomous · target: integration/<topic>`, which
   `wave-triage` writes when its flow of planning is autonomous;
3. otherwise manual: both skills behave exactly as if this subsection did not exist.

A re-plan's flow is its README `Flow:` line; a `flow` argument that differs from it stops `flow-mismatch` (the flow
form of `wave-run` changes the line).
A re-plan in autonomous flow takes the target claim ("Target claim"), holder line
`<plan> planning <YYYY-MM-DD HH:MM>`, after its lock check and before it writes anything, and releases it after its
merge into the integration worktree; refused → stop `wave-running`, nothing written.

In autonomous flow of planning:

- `wave-plan` writes `- Flow: autonomous · target: integration/<name>` into the README, where `<name>` is the index
  `<topic>` for an index part and the plan slug for a raw list.
- Neither skill asks the user a question. Each point where it would ask has the answer of the table below. A
  situation the table does not cover stops with the closest code; its `next:` says what the user must decide.
- A stop is the first line of the answer after `Started:`: `Stop <code>: <one line> — next: <command or action>`.

| Point | Where | Manual flow | Autonomous flow |
|---|---|---|---|
| a problem can be read two ways that lead to different work | `wave-triage` step 3; `wave-plan` step 1, also for an index's "Open questions" | ask all such questions once | "Assumed readings"; no question |
| one problem alone exceeds the part budget | `wave-triage` step 5 | tell the user and ask | the problem goes into no part; "Open questions" gets `P<n>: needs a research step first (not planned, autonomous flow)`; the other parts are written |
| the tracking branch or folder of a new plan already exists | `wave-plan` step 9; autonomous flow: check 0 of "Chained parts and the integration branch", before anything is written | ask the user | stop `plan-exists`; nothing written |
| a re-plan's `flow` argument differs from its README `Flow:` line | `wave-plan` re-planning | — | stop `flow-mismatch`; nothing written |
| a feature is re-planned a second time | `wave-plan` re-planning ("Re-plan escalation") | escalate it | escalate it and add it to `manual review:` |
| a feature would be re-planned a third time | `wave-plan` re-planning ("Re-plan escalation") | hold it; stop `replan-limit` when only held features have open entries | the same; nothing overrides the limit but the user's command |

#### Assumed readings

Of two or more readings, take the first rule that decides:

1. the reading closer to the user's own words (the verbatim list and the clarifications already given);
2. the reading that changes less existing behaviour (it adds rather than replaces, and leaves defaults as they are);
3. the reading with less work.

Record every choice in the Assumptions list of the file being written: the index (with the problem) or the README
(with the feature built on it):

```
- Assumed (autonomous, not asked) · P3: <the question> → <the chosen reading>; not chosen: <the other reading>
```

`wave-plan` copies the assumed lines of its part's problems from the index into the README, with the feature ID in
place of the P. `wave-run` copies a feature's assumed lines into "Worth a look" of its review brief
(`wave-run/SKILL.md` step 7), so the user meets them in the review block.

#### Chained parts and the integration branch

In autonomous flow `wave-plan` uses `<main>` = the integration branch and `<main checkout>` = the integration worktree
("Names"). All plans of an index share `integration/<topic>`, so a later part is planned and run against the code of
the earlier parts before the user has merged them. In order, before step 1 of `wave-plan`; a stop in checks 0 to 3
leaves no branch, worktree, commit or claim behind:

0. A new plan of an index part, whose slug the index "Parts" table fixes: stop `plan-exists`, nothing written, when
   the branch `plan/<slug>` exists, the folder `../<repo-folder>.worktrees/<slug>-plan` exists, or the plan folder
   exists on `<main branch>` or, when that branch exists, on `integration/<topic>`
   (`git cat-file -e <branch>:<plan folder>/README.md`). A raw list chooses its slug so that none of these exists, and
   never stops here.
1. Take the target claim ("Target claim"), holder line `<slug> planning <YYYY-MM-DD HH:MM>`; refused → stop
   `wave-running`, naming the holder. Then stop `wave-running`, naming the plan and wave, when a plan with the same
   target has a 🔄 wave ("Integration target"). Every stop from here on releases the claim first.
2. The checks of `wave-run/autonomous.md`, "Integration target", step 1, without its claim (stop `target-unsafe`).
3. The part is marked "plan after part J is merged": read part J's README,
   `git show <source>:plans/<date>-<topic>/plan-<J>/README.md`, from the first source that has it: part J's tracking
   branch `plan/<slug of part J>` (the slug in the index "Parts" table); else `<main branch>` (a part J run in manual
   flow loses its tracking branch at its last merge); else `integration/<topic>`, when that branch exists. Part J is
   merged when every feature of that README is `✅ merged` or ➖ and each of their `Merged` hashes is in
   `integration/<topic>` (only when that branch exists) or in `<main branch>`
   (`git merge-base --is-ancestor <hash> <branch>`). Otherwise stop:

   ```
   Stop part-unmerged: part <J> — F<k> <status> (<Waiting for>), … — next: …
   ```

   `next:` names, per feature, what it waits for: a `👀 review` feature its review and its merge command, a ⚠️ or 🔄
   feature its `Waiting for`. Give each command in both forms ("Commands"). When no source has the README:
   `part <J> is not planned`, with its `/wave-plan` command. Whoever drives an unattended run moves on and reports
   the waiting part with that line.
4. `wave-run/autonomous.md`, "Integration target", step 2 (create the branch and worktree, bring in `<main branch>`;
   stop `target-conflict`): the first write to the integration worktree.

Then `wave-plan` reads the code and runs the tests in the integration worktree, creates the tracking branch from the
integration branch, merges it into the integration worktree, never into the main checkout, and releases the claim
right after that merge (`wave-plan` step 9). The plan folder is on the integration branch only, until the user merges
it into `<main branch>`.

## Coordinated runs

`wave-auto` runs the whole pipeline from one session: it delegates every step to a subagent that runs one skill and
returns one line (`wave-auto/SKILL.md`). It reads no plan file; git and `plans/` are its only memory, so the same
command in a new session continues where the last one stopped. This section is the contract between the coordinator
and the skills it starts.

- A **coordinated run** is a skill run whose prompt contains the line
  `Coordinated run · step <step> · unit <unit> · return: wave-plan/layout.md, "Coordinated runs"`.
  It is in autonomous flow ("Flow"), asks the user nothing, starts no subagent and ends with only its return line
  (table below), instead of the report the skill gives the user. Everything else it records where the skill always
  records it: in files under `plans/` and in git.
- The prompt of a `medium` or `high` step starts with the gate line of "Tier gate", and the subagent applies the gate
  before anything else.
- A role that launches subagents stays with the coordinator: the cluster subagents of `wave-triage` step 4 and the task
  subagents of `wave-run`. In a coordinated run such a skill ends where it would launch them and returns what the
  coordinator must launch (`wave-triage`, "Coordinated phases"; `wave-run/task-mode.md`). This holds whether or not a
  subagent could start subagents of its own, which depends on the environment and its version: the pipeline never relies
  on it.
- A return line has no Markdown and nothing before it. Any step may return a stop instead, as its first line:
  `Stop <code>: <one line> — next: <command or action>`. The coordinator reads nothing after the return line.

### Steps

| Step | Skill and arguments | Tier | Return line |
|---|---|---|---|
| `navigate` | `wave-auto/navigator.md` with `start <start> · skip <units, or none>` | low | 0 or more lines `halt <unit>: <reason> — next: <command or action>` (one per halted unit, no limit), then one line `next: <action>` or `done` |
| `triage-ask` | `wave-triage flow autonomous ask <list>` | high | `questions <n> · index <index path>` |
| `triage-answers` | `wave-triage flow autonomous answers <index path>`, with an `Answers:` block | high | `answers recorded · clusters <cluster names, or none>` |
| `triage-cluster` | `wave-triage cluster <cluster> <index path>` | medium | `cluster <cluster>: <n> records · high <h> · unsure <u>` |
| `triage-finish` | `wave-triage flow autonomous finish <index path>` | high | `parts <k> · index <index path> · merged <short hash>` |
| `plan` | `wave-plan flow autonomous <index path> part <K>` | high | `planned <plan folder> · waves <w> · tasks low <l>, medium <m>, high <h>` |
| `re-plan` | `wave-plan <plan folder>` | high | `re-planned <plan folder> · new waves <numbers> · escalated <F-IDs, or none> · held <F-IDs, or none>` |
| `flow` | `wave-run <plan folder> flow autonomous` | medium | `flow autonomous · <plan folder>` |
| `wave` | `wave-run <plan folder> <N>`, also its resume | medium | `waiting <ID>:<tier>[ needs <Needs>]; …` while tasks wait for task mode; else `wave <N> <status> · merged <F-IDs, or none> · review <F-IDs, or none> · blocked <F-IDs, or none>` |
| `task` | `wave-run <plan folder> <N> task <ID>` | the task's complexity | `task <ID>: committed <short hash>`, `task <ID>: already committed <short hash>` or `task <ID>: no commit — <reason>` |
| `status` | `wave-status`, with the plan folder when the start is a plan folder | low | its full report; the only step whose return is not one line |

`<unit>` is a plan folder, or for an index part not planned yet the folder its plan will have
(`plans/<date>-<topic>/plan-<K>`); before the index has parts it is the index path.

### Coordinator claim

Two coordinators of one start would launch the same tasks into the same worktrees. A coordinator therefore holds the ref
`refs/wave-method/claims/auto/<name>` for its whole run, where `<name>` is the index topic, or the plan slug when it
starts from a plan folder. Holder line, in ASCII only: `wave-auto <start> <YYYY-MM-DD HH:MM> run <token>`. Take, refusal
and release work as in "Target claim". A refused claim is the one point of a run where the coordinator offers a
takeover: at the start it asks the user once whether the holder is gone; yes → it moves the ref from the held oid to its
own (`git update-ref <ref> <new oid> <held oid>`); no → stop `wave-running`, naming the holder. It releases the claim
after its last step that can write and before the final `status` step, so that the status report does not list the run's
own claim; a stop that ends the run releases it before the report. A coordinator claim and a target claim are
independent: each step takes the target claim its skill takes.

## Archive

When every feature of a plan is `✅ merged` (or ➖), and the status check passes:

- a plan without an index: `git mv plans/<date>-<slug> plans/archive/<date>-<slug>` on its tracking branch (by `wave-run` when it records the last merge);
- a plan of an index part: archive the whole index folder only when every part in the index's "Parts" table has
  a plan folder whose features are all merged; otherwise leave it in place.
- In autonomous flow `wave-run` does not archive and keeps the tracking branch: the plan is finished for the user only
  once they merged the integration branch into `<main branch>`; `wave-status` then suggests the archive.

Archived folders are never read unless the user asks.
