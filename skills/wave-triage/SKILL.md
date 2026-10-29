---
name: wave-triage
description: First stage of the wave-triage → wave-plan → wave-run pipeline. Take the user's whole list of problems/features, ask all clarifying questions once, look into the code just deep enough to locate each problem and judge its difficulty, find dependencies, and split the work into parts small enough for one wave-plan run each. It clusters large lists and runs one read-only subagent per cluster. Writes an index and, for more than 8 problems, separate problem records in its own folder under plans/ and prints a short wave-plan command per part. Use when the user brings a list of tasks to analyse ("/wave-triage", "$wave-triage", "разбери задачи", "проанализируй список"), especially a long or hard one. Recommended model: high complexity (Opus-class) — misjudged difficulty or dependencies break every later stage; the session itself stays short because it does not design.
---

# wave-triage — analyse a task list and split it into plannable parts

Wave skill set version 1 (see `.claude/skills/wave-plan/layout.md`, "Version"). Folder layout and branch names
also come from that file.

Language: `.claude/skills/wave-plan/layout.md`, "Language".

## Pipeline
`wave-triage` → (user confirms) → `wave-plan` once per part, each in a fresh session → `wave-run` per wave.
Each skill ends by telling the user the exact next command(s).
Command form: `/wave-triage`, `/wave-plan`, `/wave-run` in Claude Code; `$wave-triage`, `$wave-plan`, `$wave-run`
in Codex. Print every command in both forms (`layout.md`, "Commands").

## What triage does and does not do
- Does: restate, clarify, locate, judge difficulty, find dependencies, split into parts, write the index.
- Does not: design solutions, write API signatures, slice into tasks, change project code. That is wave-plan.
  Code reading is shallow: enough to name the files/classes involved and the likely cause, not to prove it.

## Output
The index is `plans/<YYYY-MM-DD>-<topic>/index.md` (`<topic>`: 2–4 kebab-case words, unique in `plans/`
including `plans/archive/`). There are two sizes:
- At most 8 problems: everything stays in `index.md`, with the full problem records inline (template in
  step 6); no `triage/`.
- More than 8 problems: one record per problem in `triage/P<n>.md` beside the index. `index.md` keeps only the
  overview table, clusters, parts, assumptions and open questions, with no full problem records. Move the
  verbatim list saved in step 1 into the records once they exist; later findings update the overview and the
  assigned records, so the index remains external memory without holding full records.

The folder also receives the plans of the parts (`plan-1/`, `plan-2/`, …), see
`.claude/skills/wave-plan/layout.md`. A part's command must work in an empty session with only the index and,
for a large list, the `triage/P<n>.md` records of that part's problems, besides the code.
Branch `triage/<topic>`, worktree `../<repo-folder>.worktrees/<topic>-triage`.

**Nothing is committed directly on the main branch.** Write the index and any records in a worktree on branch
`triage/<topic>` and merge them (step 8).

## Steps

### 1. Create the index immediately
Before any analysis, create the worktree and the index file with the user's list **verbatim** (numbered
P1…Pn) and commit it on `triage/<topic>`:
```bash
git worktree add -b triage/<topic> ../<repo-folder>.worktrees/<topic>-triage <main>
```
From now on the index is your external memory: write each finding into it as soon as you have it, so your
context holds only the problem you are working on.

### 2. Pass 1 — restate and cluster (no code reading)
Restate every problem in one line. Group the problems into clusters of 5–10 by area: the module, screen or
subsystem the user's words name; use `git ls-files` and a name search only to put a problem into a cluster,
not to analyse it. A problem that fits nowhere goes to a cluster `misc` (also at most 10; split `misc-1`,
`misc-2` if needed). Write the overview table and the cluster table into `index.md` and commit:
`Index <topic>: pass 1, <n> problems in <c> clusters`.

Clusters are a scheduling device of triage only; parts still follow dependencies and the budget (step 5).

### 3. Clarify once, grouped by cluster
Collect every ambiguity that leads to different work. Ask all clarifying questions in one message, grouped
under cluster headings; problems without questions are not mentioned. Decide small things yourself and record
them as assumptions. Write the answers into the problem records (in `triage/P<n>.md` for more than 8 problems,
or inline in the index for at most 8).

### 4. Pass 2 — shallow analysis per cluster
Read `.claude/skills/wave-triage/difficulty.md` before judging the first problem. For each problem, record:
- **Where**: files/classes/functions involved (`file:line` when cheap to get), what already exists to reuse.
- **Likely cause / gap**, one or two sentences, marked "unverified" when it is a guess.
- **Difficulty**: `low` / `medium` / `high`, as defined in `difficulty.md`.
- **Estimated size**: number of files/modules, rough task count (1, 2–3, 4+).
- **Depends on**: other problems whose code it needs, or which change the same code.

For at most 8 problems, write the records inline in `index.md`. The separate-file
subagent, re-judging and dependency procedure below applies to lists of more than 8 problems. For the small
mode, use the same checklist, difficulty criteria and dependency checks on the inline records.

For more than 8 problems, when the environment has subagents (`layout.md`, "Environment capabilities"), run
one read-only subagent per cluster, tier `medium`, all at once where the environment allows parallel
subagents, otherwise one after another. Read-only applies to project code; the only permitted writes
are that subagent's assigned `triage/P<n>.md` records. Its prompt must include:
- The cluster's problems with their one-line restatements, the user's words and the answers.
- The checklist above (Where, Likely cause, Difficulty with `difficulty.md`, Size, Depends on).
- `Report language: <the language of the user's messages in this session>.`
- The record-file format from step 6 and the instruction: "Write one file `triage/P<n>.md` per problem in the
  given format; do not read or change other files under `plans/`; do not commit. Do not modify project code."
- "Return only, per problem, one line:
  `P<n> · <difficulty> · <size> · files: <paths> · depends: <P…> · unsure: <yes/no>`."

A subagent that cannot judge a problem returns `unsure: yes`; it never guesses silently. Without subagents,
the coordinator does the same cluster by cluster, writing each cluster's records before reading code for the
next. The coordinator's context per problem stays one returned line, except records needed for re-judging or
confirming dependency candidates below.

**Re-judging:** the coordinator (high tier) reads the record files only of problems returned `high` or
`unsure: yes`, and confirms or changes their difficulty (a quick code look is allowed). Update the overview
with the confirmed difficulty. Other records are not read again except to confirm dependency candidates.

**Dependencies:** two problems whose returned `files:` share a path are a dependency candidate, even when they
belong to different clusters. The coordinator confirms or rejects each candidate from the two records (no
code reading unless unclear) and writes the result into both records' **Depends on** and into the overview
table.

### 5. Split into parts
A part = one wave-plan run in a fresh session = one plan folder. Every part stays within the
"Part budget" of `.claude/skills/wave-triage/difficulty.md` (points, `high` limits, expected features and tasks).

Use this deterministic procedure:
1. Dependency groups = connected components of confirmed dependencies.
2. Sort groups: groups containing a `high` problem first (by number of `high`, then points, descending), then
   by points descending.
3. Fill parts in that order: a group goes into the first part where it fits the part budget of `difficulty.md`;
   otherwise a new part. A group larger than one part is split at the dependency with the fewest shared files;
   the later piece is marked **"plan after part K is merged"**. It goes only into a part numbered after part K:
   the first such part where it fits, otherwise a new part. Its plan must be written against code that
   already contains part K, or its `file:line` references will be stale.
4. Fill the remaining room of each part with `low` problems that have no dependencies.
5. Part numbers follow the final order.

Give each part a plan slug, unique in `plans/`: `<topic>-p<K>`. Its plan folder will be
`plans/<date>-<topic>/plan-<K>/`. A problem that alone exceeds the budget: follow the last rule of "Part budget"
and ask the user.

### 6. Index and record templates
For at most 8 problems, keep full problem records in the index:

````markdown
# <Topic> — index

- Index: `plans/<date>-<topic>/index.md` · created <date> · base: <git short hash> · skills: v1

## Problems
### P1. <one-line restatement>
**User's words:** <verbatim>
**Clarifications:** <answers / assumptions>
**Where:** `file:line`, … · **Reuse:** …
**Likely cause:** … (unverified)
**Difficulty:** high · **Size:** 4+ tasks, modules core/plan, viewer
**Depends on:** P4 (same code: `InFrame.descend`)

## Parts

| Part | Problems | Points | Plan slug | Plan when | Command |
|---|---|---|---|---|---|
| 1 | P1, P4, P7 | 9 | `<topic>-p1` | now | `/wave-plan plans/<date>-<topic>/index.md part 1`<br>`$wave-plan plans/<date>-<topic>/index.md part 1` |
| 2 | P2, P3 | 10 | `<topic>-p2` | now | `/wave-plan plans/<date>-<topic>/index.md part 2`<br>`$wave-plan plans/<date>-<topic>/index.md part 2` |
| 3 | P5, P6 | 6 | `<topic>-p3` | after part 1 merged | `/wave-plan plans/<date>-<topic>/index.md part 3`<br>`$wave-plan plans/<date>-<topic>/index.md part 3` |

Part status is not written here: a part is planned when its plan folder `plan-<K>/` exists; it is done when every
feature in that plan is `✅ merged`.

## Assumptions
- …

## Open questions
- … (empty when the user answered everything)
````

For more than 8 problems, the index has this layout. Each Summary cell is at most 80 characters; each problem
has exactly one overview row. Reuse the Parts table and the Assumptions and Open questions sections above.

````markdown
# <Topic> — index

- Index: `plans/<date>-<topic>/index.md` · created <date> · base: <git short hash> · skills: v1

## Problems

| P | Summary | Cluster | Difficulty | Size | Depends on | Part |
|---|---|---|---|---|---|---|
| P1 | <one-line restatement, ≤ 80 characters> | <cluster> | high | 4+ tasks | P4 | 1 |

## Clusters

| Cluster | Area | Problems |
|---|---|---|
| <cluster> | <module, screen or subsystem> | P1, P4, … |

## Parts

<Parts table and part-status explanation from the small-index template>

## Assumptions
- …

## Open questions
- … (empty when the user answered everything)
````

Each `triage/P<n>.md` uses the full problem-record format:

````markdown
# P<n>. <one-line restatement>

**User's words:** <verbatim>
**Clarifications:** <answers / assumptions>
**Where:** `file:line`, … · **Reuse:** …
**Likely cause:** … (unverified)
**Difficulty:** high · **Size:** 4+ tasks, modules core/plan, viewer
**Depends on:** P4 (same code: `InFrame.descend`)
````

### 7. Self-check
- Every problem is in exactly one part; every part is within budget.
- Every dependency between parts is either inside one part or marked "after part K is merged".
- Every problem has Where, Difficulty, Size, Depends on — enough for wave-plan to start without re-searching.
- More than 8 problems → every problem has a record file and one overview row; the index has no full records.
- Every confirmed dependency is in both records and the overview (in the small mode, both inline records).
- Parts are ordered hard → easy, respecting dependencies.

### 8. Commit, merge, stop
- Commit the index and any records on `triage/<topic>`: `Index <topic>: <n> problems in <k> parts`.
- Merge into the main branch: the main checkout must be ready for the merge of `triage/<topic>` (`layout.md`,
  "Main readiness"); then `git -C <main checkout> merge --no-ff triage/<topic> -m "Index <topic>"`. Otherwise
  do not touch it and give the user the merge command. Then remove the worktree and delete the branch. Never push.
- **Stop.** Do not start planning. Answer the user:
  - the parts table: problems, difficulty, points, why they are grouped this way;
  - assumptions and anything you were unsure about;
  - **the next commands**, one per line in both forms (`layout.md`, "Commands"), each to be run in a
    **fresh session**; say which can be run now (in parallel, in any order) and which only after a given part
    is merged;
  - "after a part's plan is written, run its waves with `/wave-run <plan folder> 1` · `$wave-run <plan folder> 1`".
