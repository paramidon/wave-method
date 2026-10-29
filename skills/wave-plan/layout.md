# Plan folders, files, names and statuses

Single source of truth for the wave skills: layout, reading rules, model tiers, names, status rules and Markdown rules are changed here only.

## Who reads what
Read only what the table lists. A file that does not exist means there is nothing of that kind yet.

| Reader | Reads |
|---|---|
| `wave-run` coordinator | `README.md`, `waves/w<NN>.md` of its wave, `problems.md`; a solution file only to resolve a conflict or a failure; `wave-run/task-mode.md` and `wave-run/deferred-merges.md` only when its step 1 says so |
| task subagent | its prompt, the solution files (and sections) the prompt names |
| task-mode session | `README.md`, its wave file, the solution files its prompt names; `wave-run/task-mode.md` |
| `wave-plan`, new plan | the index (`index.md`; for a large index also the `triage/P<n>.md` records of its part's problems), `wave-plan/templates.md` when writing files |
| `wave-plan`, re-plan | `README.md`, `problems.md`, solution files of the affected P, the wave files where the open entries were found |
| `wave-triage` coordinator | its `index.md`; the `triage/P<n>.md` records only of problems it re-judges or whose dependency candidates it confirms |
| triage subagent | its prompt; it writes only its assigned `triage/P<n>.md` records |
| `wave-status` | see its skill (READMEs, problem headers, Execution of 🔄/❌/⚠️ waves, index "Parts") |
| nobody | `CHANGELOG.md`; `wave-plan/scripts/` (skills run the script, they do not read it) |

A wave file holds everything its wave needs. If something is missing, that is a defect of the plan: record it in `problems.md` and do not look for it in other waves, `history.md` or `archive/`.

## Language

- Talk to the user in the language of the user's messages in this session (the language they write their
  prompts in); if it changes, follow the latest message.
- Everything written to the repository is in English: code, comments, docs, plan and index files, task
  prompts, commit messages, branch names.
- A subagent writes its report in the language that its header's `Report language:` line names.

## Version
Wave skill set version 1. All files of the set (`wave-triage/SKILL.md`, `wave-triage/difficulty.md`, `wave-plan/SKILL.md`, `wave-plan/layout.md`, `wave-plan/templates.md`, `wave-plan/scripts/status_check.py` (constant `SKILL_SET_VERSION`), `wave-run/SKILL.md`, `wave-run/task-mode.md`, `wave-run/deferred-merges.md`, `wave-status/SKILL.md`) carry the same version. Any change to any of them raises it in all of them and adds a line to `wave-plan/CHANGELOG.md`, which agents do not read. A plan README records the version it was written with (`skills: v<N>`).

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
| `README.md` | header, Features / Waves / Tasks tables, one line per user problem, known failures, assumptions; ≤ 150 lines | always |
| `waves/w<NN>.md` | one wave (`w01`, `w02`, …): its task table, dependencies, full task prompts; after it ran: its execution log and the closed problems found in it | one per wave |
| `solutions/P<n>-<slug>.md` | the design of one `medium` or `high` user problem (Cause, Approach, API, Algorithm, Limits, Acceptance tests) | one per such problem |
| `solutions/lite.md` | every `low` problem of the plan, one section `## P<n>. <short>` each: the exact edit and one acceptance check | with the first `low` problem |
| `problems.md` | **open** problem-log entries only | with the first entry |
| `history.md` | re-plan and migration notes, audits, anything kept only as history | at the first re-plan |

- Which solution file a problem gets depends only on its difficulty: `low` → a section of `lite.md`, always; `medium`/`high` → its own file, always. A re-plan appends new sections to `lite.md` and new files for the rest.
- A re-plan adds new wave files (new numbers after the last one). It never rewrites a wave file of a wave that ran, except its statuses, "Execution" and "Closed problems".
- Design facts belong in solution files, not in `history.md`: a measurement that a solution relies on goes into that solution.

## Model tiers

| Complexity | Meaning | Model tier |
|---|---|---|
| `low` | mechanical edit from an exact description | Haiku 5.5 (or any stronger model) |
| `medium` | implementation of a given solution, several files, its own tests | Sonnet 5.5 / GPT-6.1 SOL / Gemini 4 Argon (or stronger) |
| `high` | design uncertainty remains that cannot be removed upfront | Opus 5.5 |

A task never runs below its tier; a `high` task never runs on a medium model. A plan README may add a line `Models: <complexity> = <model>, …` naming concrete models of the same or a higher tier; it never lowers one.

## Environment capabilities

Skills that launch subagents determine these capabilities from the tools the session actually has — never assume
one; when unsure, treat it as missing: **subagents**; **parallel subagents**; **model choice per subagent**;
**continuing a subagent**; **a tool a task needs** (for example desktop control); **built-in worktree isolation**.
What each skill does when one is missing is in that skill.

## Names

- `<main>` — the main branch (`master` or `main`).
- `<plan>` — the plan slug from the README header (`slug: …`).
- `<plan folder>` — the plan folder's path relative to the repository root (`plans/2026-11-02-hop-tuning`).
- `<feature>` — `<feature-id>-<feature-slug>` from the "Features" table (e.g. `F1-cheap-interbody-omega`).
- `<task>` — `<task-id>-<task-slug>` from the "Tasks" table (e.g. `D-signed-speed-readouts`).

| What | Branch | Worktree (outside the repository) |
|---|---|---|
| tracking | `plan/<plan>` | `../<repo-folder>.worktrees/<plan>-plan` |
| feature | `feat/<plan>/<feature>` | `../<repo-folder>.worktrees/<plan>-<feature-id>` |
| task | `task/<plan>/<feature-id>-w<N>-<task>` | `../<repo-folder>.worktrees/<plan>-w<N>-<task-id>` — only when another task of the same feature runs at the same time (`wave-run` step 4) |

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
| Feature | ⬜ not started · 🔄 in progress · ✅ ready · ✅ merged · ⚠️ blocked · ➖ dropped |

Every feature that is not `✅ merged` or ➖ has a `Waiting for` cell: `wave <N>` (its next tasks), `I<n>` (an open entry), `main-dirty` (ready, the main checkout was not ready for the merge), `user: <question>`. The cell is empty once the feature is merged.

**A status shows the current outcome, not the history.**

- ⚠️ and ❌ mean "action needed now". Each ⚠️/❌ item names at least one open entry of `problems.md` (`⚠️ I4`), or, for a ❌ wave, says that it must be re-run.
- When the last open entry concerning an item is closed, the item becomes ✅ with a short note: `✅ (fixed by AB, wave 6)`. A task that will never run because another replaces it is `➖ superseded by AA`; a wave whose tasks all moved elsewhere is `➖ dropped (tasks → wave 7)`. ➖ is final and is not a problem.
- Whoever closes an entry updates the items it concerns in the same commit: `wave-run` (step 8 of the wave that fixed it, or when the user accepts it), `wave-plan` at a re-plan (an item superseded by new tasks becomes ➖ at once; an item waiting for fix tasks stays ⚠️ with `→ task Y`).
- **Status check** (run by `wave-run` in step 8 and before archiving, by `wave-plan` before committing): no ⚠️/❌ item without an open entry or a re-run note, and no open entry whose items are all ✅ or ➖. History (what failed, how it was fixed) lives in the wave files and `history.md`, never in a red mark. Run it with `python .claude/skills/wave-plan/scripts/status_check.py <plan folder>` (in the tracking worktree); fix every printed line. Without Python, check by hand by this rule.

## Running waves
A wave is running while its status in README "Waves" is `🔄 since <YYYY-MM-DD HH:MM>` on the tracking branch (`git show plan/<plan>:<plan folder>/README.md`). This mark is the lock: `wave-run` commits it when the wave starts and removes it with the wave's "done" or "stopped" commit.

- While a wave runs, only its coordinator (and the task sessions it asked for) changes the plan folder, its tracking worktree and its feature and task worktrees: no re-plan, no other wave, no renames, no manual fixes. Reading is fine. Any other skill or agent that wants to change them tells the user and stops.
- A wave whose Execution ends with `Waiting: task mode <IDs>` is resumed by `/wave-run <plan folder> <N>` · `$wave-run <plan folder> <N>` (`wave-run`, "Environment capabilities").
- A lock left by a session that is gone is released only by the user's decision.

## Problem log
`problems.md` is created with the first entry:

```
# Open problems
Next ID: I2

- **[I1 · wave 4 / task E / feature F3] <one-line essence>** — where: `file:line`; expected / got;
  proposal: …; status: open | → task Y (wave M)
```

IDs `I1, I2, …` are unique in the plan and never reused; `Next ID` stays in the file even when it has no entries. Write the essence so the next planner understands it without reading transcripts. An entry is **closed** when its status becomes `fixed in <commit> (task Y)`, `verified by <task> on <commit>`, `accepted by the user on <date>` or `won't fix: <reason>`. A closed entry leaves `problems.md` in the same commit: it moves to "Closed problems" of the wave file where it was found (`history.md` if it came from a re-plan or audit, not from a wave). `→ task Y` is still open.

## Markdown rules
Every Markdown file the skills write (index, README, solutions, waves, problems, history) follows these rules.

- **A blank line before and after every table**, every list and every fenced block. A table never follows a text line directly, and a text line never follows a table's last row directly: without the blank line the text swallows the table, or becomes an extra row.
- Every row of a table has the same number of cells as its header row; the separator row is `|---|---|…|` with one `---` per column. A row is one physical line: never wrap it.
- A `|` inside a cell is written `\|`; a line break inside a cell is written `<br>`.
- Header fields (Plan, Index, Re-plans, Models) are a bullet list, one field per item, so they do not merge into one paragraph.
- Only headings separate sections; no bold pseudo-headings for sections that tables or lists follow.

## Main readiness

The main checkout is ready for a merge of branch `B` when all of these hold:

1. it is on `<main>` (`git -C <main checkout> branch --show-current`);
2. its index has no staged changes (`git -C <main checkout> diff --cached --quiet`) — git refuses a merge
   otherwise;
3. no unstaged tracked change touches a path the merge changes: the paths of
   `git -C <main checkout> diff --name-only` and of `git diff --name-only <main>...B` do not intersect.

Untracked files never matter. Not ready → `main-dirty`, with the reason (`not on <main>`, `staged changes`, or
the overlapping paths). Never stage, unstage, stash, reset or check out anything in the main checkout to make it
ready.

## Archive

When every feature of a plan is `✅ merged` (or ➖), and the status check passes:

- a plan without an index: `git mv plans/<date>-<slug> plans/archive/<date>-<slug>` on its tracking branch (by `wave-run` step 8);
- a plan of an index part: archive the whole index folder only when every part in the index's "Parts" table has
  a plan folder whose features are all merged; otherwise leave it in place.

Archived folders are never read unless the user asks.
