# P1. In-session coordinator skill `wave-auto`

User problem: one command, in an interactive Claude Code session (CLI or desktop app), runs triage → plans → waves
as a coordinator that delegates every step to subagents, asking the triage questions once at the start · feature F1

## Cause

Every skill ends by printing the next command for the user (`skills/wave-triage/SKILL.md` step 8 "Stop",
`skills/wave-plan/SKILL.md` step 9, `skills/wave-run/SKILL.md` step 9). The only thing that chains the steps is the
Python driver `scripts/wave_driver.py`, which starts one headless `claude -p` per step (`scripts/wavedriver/decide.py`
`choose()`, `after_call()`), so it needs a terminal, Python and the CLI, and never triages.

Two facts of the environment shape the design:

- A subagent cannot start subagents (Claude Code gives a subagent no agent tool; to be confirmed by rehearsal H,
  probe P0). So `wave-run`, which launches one subagent per task, and `wave-triage` step 4, which launches one per
  cluster, cannot run *inside* a subagent with their launching role. The coordinator, a main session, keeps those
  roles and delegates only leaf work.
- A long chain in one session grows its context. Every step therefore returns one line, and the coordinator reads
  no plan file: git and `plans/` are its only memory, which also makes a closed window or a usage limit harmless —
  the same command in a new session continues.

## Approach

A fifth skill, `skills/wave-auto/`, with two files:

- `SKILL.md` — the coordinator: start forms, the start phase (the only place where it asks the user), the loop
  "navigate → dispatch one step → print one line", capability fallbacks, rails, its claim and the final report.
- `navigator.md` — rules for a low-tier, read-only navigator subagent that reads the state from git and returns
  the next action in one line. It is the driver's `decide.py` (`choose`, `_planned`, `_running`) and the readiness
  part of `gitstate.py` (`read_snapshot`, `part_merged`, `read_plan`) written as skill rules.

The existing skills get a **coordinated run** mode, defined once in `layout.md`, "Coordinated runs": the subagent
follows the skill as written, in autonomous flow, asks nothing, launches nothing, and ends with one fixed return
line instead of the user report. Wherever a skill would launch subagents, the coordinated run ends at that point and
returns what to launch:

- **A wave** reuses task mode, which already splits a wave into "prepare → one fresh session per task → resume"
  (`skills/wave-run/task-mode.md`). In a coordinated run every task goes to task mode; the coordinator runs each
  task as a subagent of its tier (`wave-run <plan folder> <N> task <ID>`) and then the resume. Task mode gains three
  things it lacked: the task's report block travels in its last commit's body (today a task-mode report reaches only
  the user, so the resume cannot fill the review brief), a task that already has its commits is not redone (resume
  after an interruption), and a fix request goes through the wave file (the resume cannot continue a subagent).
- **Triage** gets four phases (`ask`, `answers`, `cluster`, `finish`), so the coordinator asks the user once between
  `ask` and `answers` and launches the cluster subagents itself.
- **Planning** (`wave-plan flow autonomous <index> part <K>`) and **re-planning** (`wave-plan <plan folder>`) already
  run without nesting; they only get the return line.

Why not the alternatives:

- The coordinator runs `wave-run` itself in its own context: every wave file (all prompts), merges and checks would
  enter the coordinator's context; a few waves exhaust it. Rejected (agreed with the user).
- A `wave-run` subagent that launches task subagents: impossible without nesting.
- Keep or port the Python driver: needs a terminal and Python; the user wants the same skill in the desktop apps,
  and P4 (part 2) removes the driver.
- Sub-coordinator sessions for every wave: depends on an app feature (a session tool); kept as the fallback for a
  step that cannot run as a subagent, not as the base.

The coordinator always runs in autonomous flow (features auto-approved into `integration/<topic>`, user's answer);
triage questions are asked once, at the start (user's answer); a step that cannot run on a subagent of its tier runs
in a separate session where the environment can start one, else the run halts with the commands for the user
(user's answer; the tier gate is unchanged).

## Names and files

- Skill `wave-auto`; commands `/wave-auto <args>` · `$wave-auto <args>`.
- New: `skills/wave-auto/SKILL.md` (task E), `skills/wave-auto/navigator.md` (task D).
- Changed: `skills/wave-plan/layout.md` (task A), `skills/wave-run/SKILL.md` and `skills/wave-run/task-mode.md`
  (task B), `skills/wave-triage/SKILL.md` (task C), `skills/wave-plan/SKILL.md` and `skills/wave-status/SKILL.md`
  (task F), installers, plugin files, `README.md`, `skills/wave-plan/CHANGELOG.md` (task G).
- Records: `docs/rehearsals/coordinator-cli.md` (task H), `docs/rehearsals/coordinator-desktop.md` (task I).

Step names, return lines and the waiting-line grammar below are a contract shared by A, B, C, D, E and F: every task
copies them character for character.

## Layout: "Coordinated runs" (task A)

### Text of the new section

Insert as a new `## Coordinated runs` section of `skills/wave-plan/layout.md` right before `## Archive`, with this
content (keep the wording; reflow lines to ≤ 120 characters):

````markdown
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
- A role that launches subagents stays with the coordinator: the cluster subagents of `wave-triage` step 4 and the
  task subagents of `wave-run`. In a coordinated run such a skill ends where it would launch them and returns what the
  coordinator must launch (`wave-triage`, "Coordinated phases"; `wave-run/task-mode.md`).
- A return line has no Markdown and nothing before it. Any step may return a stop instead, as its first line:
  `Stop <code>: <one line> — next: <command or action>`. The coordinator reads nothing after the return line.

### Steps

| Step | Skill and arguments | Tier | Return line |
|---|---|---|---|
| `navigate` | `wave-auto/navigator.md` with `start <start> · skip <units, or none>` | low | 0–4 lines `halt <unit>: <reason> — next: <command or action>`, then one line `next: <action>` or `done` |
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

Two coordinators of one start would launch the same tasks into the same worktrees. A coordinator therefore holds the
ref `refs/wave-method/claims/auto/<name>` for its whole run, where `<name>` is the index topic, or the plan slug when
it starts from a plan folder. Holder line, in ASCII only: `wave-auto <start> <YYYY-MM-DD HH:MM> run <token>`. Take,
refusal and release work as in "Target claim". A refused claim is the one point of a run where the coordinator offers
a takeover: at the start it asks the user once whether the holder is gone; yes → it moves the ref from the held oid to
its own (`git update-ref <ref> <new oid> <held oid>`); no → stop `wave-running`, naming the holder. It releases the claim
after its final report's last step, and before the report of a stop that ends the run. A coordinator claim and a
target claim are independent: each step takes the target claim its skill takes.
````

### Other edits of `layout.md` (task A)

1. "Who reads what": add three rows after the `wave-status` row:
   - `` `wave-auto` coordinator `` | `wave-auto/SKILL.md`; of `plans/` only the "Open questions" section of an index on
     its triage branch, when it asks them; everything else reaches it as return lines ("Coordinated runs")
   - `navigator subagent` | `wave-auto/navigator.md` and the git state it names; it changes nothing
   - `coordinated step subagent` | what the row of its skill says; its prompt names the skill and arguments
     ("Coordinated runs")
2. "Run times": in the first sentence's list of skills add `wave-auto`; in the last bullet add
   "`wave-auto` writes nothing of its own; its steps record their times".
3. "Skill paths": "the folder that holds `wave-triage/`, `wave-plan/`, `wave-run/` and `wave-status/`" →
   "the folder that holds `wave-triage/`, `wave-plan/`, `wave-run/`, `wave-status/` and `wave-auto/`".
4. "Environment capabilities": add after **built-in worktree isolation**:
   `**starting a session** (a separate session with a chosen model, whose result comes back to this session)`.
5. "Running waves", last bullet: "So is a target claim of autonomous flow ("Target claim")." →
   "So is a target claim of autonomous flow ("Target claim") and a coordinator claim ("Coordinated runs")."
6. "Results of an autonomous run", first sentence: "(the `wave-run` report, `wave-status`, a driver's summary)" →
   "(the `wave-run` report, `wave-status`, the `wave-auto` final report, a driver's summary)". The driver mention
   stays; part 2 (P4) removes it.

## Coordinator `wave-auto/SKILL.md` (task E)

### Frontmatter

```yaml
---
name: wave-auto
description: Runs the whole wave pipeline from one command inside one session — triage of a list (its clarifying questions asked once, at the start), the plan of every part and every wave, in autonomous flow — as a coordinator that delegates each step to a subagent and keeps one line per step. Git and plans/ are its only memory, so the same command in a new session continues where the last one stopped. Use when the user runs "/wave-auto <list | index | plan folder>" or "$wave-auto …", or asks to run the pipeline unattended in one session ("запусти всё сам", "прогони от списка до мержа"). Recommended model: high complexity (Opus-class) — a subagent without a model choice inherits it.
---
```

### Sections, in this order

1. **Title and language** — `# wave-auto — run triage, plans and waves from one session`; the language line and the
   skill-paths line exactly as the other skills have them (copy from `skills/wave-run/SKILL.md` lines 8–12).
2. **Layout** — read `wave-plan/layout.md` first, above all "Flow", "Coordinated runs", "Model tiers", "Tier gate",
   "Environment capabilities", "Target claim", "Results of an autonomous run". This skill does not repeat it.
3. **Input** — `/wave-auto [until <HH:MM | YYYY-MM-DD HH:MM>] [steps <N>] <start>` ·
   `$wave-auto [until …] [steps <N>] <start>`. Options come first. `<start>`:
   - `plans/<date>-<topic>/index.md` → an index start (its topic names the claim);
   - a plan folder (`git cat-file -e <source>:<folder>/README.md` succeeds for `<main branch>`, a `plan/*` branch or
     an `integration/*` branch) → a plan start (its slug names the claim);
   - anything else, verbatim → a list start;
   - nothing → stop `no-start` with the three forms.
4. **Hard rules**
   - The coordinator changes no file, makes no commit or merge, and never pushes; the only ref it writes is its
     claim. Every change is made by a step's subagent through its skill.
   - It reads nothing of `plans/` but the "Open questions" of an index on its triage branch, when it asks them.
     It never reads plan READMEs, wave files, solutions or task prompts, and never retells a subagent's output beyond
     its return line.
   - It asks the user only in the start phase. It never answers a question for the user and never lowers a tier.
   - Every step is in autonomous flow: features are auto-approved into `integration/<topic>` (or
     `integration/<slug>`); `<main branch>` receives only the triage index (step `triage-finish`).
   - One progress line per step to the user: `<HH:MM> · <step> · <unit> → <return line>`.
5. **Capabilities** — at the start, from the tools this session has (`layout.md`, "Environment capabilities"):
   subagents; parallel subagents; model choice per subagent (which choice names a model of each tier: in Claude Code
   the agent tool's `haiku` = low, `sonnet` = medium, `opus` = high; a README `Models:` line may only name a tier or
   higher); starting a session; the tools a task's `Needs` names (checked when a task needs one). Print one line
   `Capabilities: …`. Neither subagents nor starting a session → stop `capability-missing`, `next:` the manual
   commands (`/wave-triage`, `/wave-plan`, `/wave-run`, in both forms).
6. **Step prompt** — every step's subagent gets exactly this prompt (the first line only for a medium or high step):

   ```
   Required tier: <tier> — <models of that tier or higher>. Stop if this session runs a weaker model.
   Coordinated run · step <step> · unit <unit> · return: wave-plan/layout.md, "Coordinated runs"
   Skills folder: <absolute wave skills folder>
   Repository: <absolute path of the main checkout>
   Report language: English
   Run the skill <skill> with the arguments: <arguments>
   Read <skills folder>/<skill>/SKILL.md and follow it as if the user had typed that command in a fresh session.
   You are a subagent of a coordinator: ask nothing, start no subagent, and end with only the return line of that
   section.
   ```

   The `navigate` step replaces the last three lines with
   `Read <skills folder>/wave-auto/navigator.md and follow it with: start <start> · skip <units, or none>`.
   The `triage-answers` step appends `Answers:` and the user's answer verbatim. Model: the tier's model choice.
7. **Start phase** — the only questions of a run, each kind asked at most once, all questions of one kind in one
   message, in the user's language:
   1. Read the clock (`Started:` line, `layout.md`, "Run times"); resolve the skills folder, the main checkout
      (`git rev-parse --show-toplevel`) and `<main branch>`; check capabilities.
   2. List start: run `triage-ask`; its index path gives `<topic>`.
   3. Take the coordinator claim (`layout.md`, "Coordinated runs"). Refused → ask whether the holder is gone (quote its
      holder line); yes → take it over; no → stop `wave-running`.
   4. Questions: after `triage-ask` with `questions <n>` > 0, or when the navigator returns `next: ask <index>`, read
      the `- Q<n> · …` lines of "Open questions" with `git show triage/<topic>:<index path>`, ask them all in one
      message and wait. Then run `triage-answers` with the answer verbatim (`Answers: none` for 0 questions; the user
      may answer only some). When the navigator returns `next: ask-flow <plan folder>`: ask whether to switch that
      plan to autonomous flow; yes → step `flow`; no → halt the unit.
   5. The start phase ends with the first step that is not `triage-ask` or `navigate`. From then on a navigator line
      `next: ask …` or `next: ask-flow …` halts its unit instead (`questions-late`, `next:` the manual command).
8. **Loop**

   ```
   repeat:
     rails (below) → end the run when one is reached
     navigate (start, skip = halted units)
     add every `halt` line's unit to the halted units, keep its line for the report
     `done` → final report
     the same `next:` line as the previous navigate → halt that unit `no-progress`
     dispatch the `next:` line (table below)
   ```

   | Navigator line | Dispatch |
   |---|---|
   | `next: ask <index path>` | start phase only: the questions of 7.4, then `triage-answers` |
   | `next: triage-cluster <index path> <cluster> …` | one `triage-cluster` step per cluster, in parallel where possible, then `triage-finish` |
   | `next: triage-finish <index path>` | `triage-finish` |
   | `next: plan <index path> part <K>` | `plan` |
   | `next: ask-flow <plan folder>` | start phase only: 7.4 |
   | `next: wave <plan folder> <N>` | "Wave" below |
   | `next: tasks <plan folder> <N> <ID>:<tier>[ needs <Needs>]; …` | "Wave" below, from its task steps |
   | `next: re-plan <plan folder>` | `re-plan` |

   After `triage-answers`, run the cluster steps its return names (none → `triage-finish`) without navigating first.
9. **Wave** — `wave` step → while it returns `waiting …`: one `task` step per listed task, in parallel where the
   environment allows (all in one message, each on its tier's model; a task whose `Needs` names a tool this session
   lacks goes to the session fallback), wait for all, then the `wave` step again (the resume). A task step that
   returns a stop (`tier-mismatch`, `capability-missing`) halts the unit; do not resume. A task ID run 3 times in one
   dispatch (once and two fix requests) and listed again → halt the unit `step-failed`.
10. **Results of steps** — a return line that does not match its step's form (or no return) → run the step once
    more; again wrong → halt the unit `step-failed: <step>`. A `Stop <code>` return halts its unit with that line,
    except `target-unsafe`, `target-conflict` and `target-unmerged`, which halt every unit of the run (one index shares
    one target) and end it. A `triage-*` stop ends the run (nothing else can run before the index exists).
11. **Session fallback** — a step that cannot run as a subagent of its tier (no subagents, no model choice for its
    tier, or a `Needs` tool missing): when the environment can start a session with a model of that tier whose
    result comes back here, start it there with the skill's command in its normal form, `flow autonomous` included
    (`/wave-plan flow autonomous <index path> part <K>`, `/wave-run <plan folder> <N>`, `/wave-run <plan folder> <N>
    task <ID>`), in the repository, and wait for its result. The session runs the skill normally, so a whole wave
    in a session uses its own subagents. Then navigate again; the session's text is not kept. Otherwise halt the
    unit `tier-missing` or `capability-missing`, `next:` that command in both forms, "in a fresh session with
    <models>", then `/wave-auto <start>` again.
12. **Rails** — checked before every step except `navigate` and `status`: `until` (no step starts at or after that
    time, read from the clock) and `steps` (at most N steps; default 60; `navigate` and `status` do not count).
    Reaching one ends the run with its final report, `ended by rail: …`. A step already running is not cut short. A
    wave left waiting by a rail stays 🔄 with its claim marked waiting: the next `/wave-auto <start>` resumes it.
13. **End of the run** — run the `status` step (the start's plan folder for a plan start, no argument otherwise),
    release the claim, read the clock and print:

    ```
    ## wave-auto · <start>
    Run: <n> steps · ended by <done | rail: until <time> | rail: steps <N> | stop <code>> · <capabilities line>

    ### Steps

    | Time | Step | Unit | Result |
    |---|---|---|---|
    | <HH:MM> | <step> | <unit> | <return line> |

    ### Halts

    - <unit> — <reason> — next: <command or action>   (or "none")

    ### Status

    <the status step's report, verbatim>

    ### Next

    - Continue: `/wave-auto <start>` · `$wave-auto <start>` (only when a unit is halted, waiting or a rail ended the run)

    Started: <…> · Finished: <…> (<duration>)
    ```
14. **Stops of the coordinator** — table: `no-start`, `capability-missing`, `wave-running` (claim refused, user said
    no), and the codes it passes through from steps. Every stop ends the run: release the claim, then the report of
    13 without the `status` step when no step ran.
15. **Resume** — the same command in a new session: the start phase takes the claim (the old session released it, or
    the user confirms the takeover), and the navigator finds where the state is. A list start resumes with
    `/wave-auto plans/<date>-<topic>/index.md`; the coordinator prints that command right after `triage-ask`.

## Navigator `wave-auto/navigator.md` (task D)

Read only by the navigator subagent. Read-only: git commands that read (`git show`, `git cat-file -e`,
`git branch --list`, `git rev-parse`, `git merge-base --is-ancestor`, `git worktree list`), and files of the triage
worktree; no build, test, edit, commit or checkout. Input: `start <start> · skip <units>`. Output: the return of the
`navigate` step (`layout.md`, "Coordinated runs"), nothing else.

### Sources

- `<main branch>`: `main` when `git rev-parse --verify --quiet refs/heads/main` succeeds, else `master`.
- A plan's README: from the first of `plan/<slug>`, `<main branch>`, `integration/<topic>` (index part) or every
  `integration/*` branch (plan start) where `git cat-file -e <branch>:<plan folder>/README.md` succeeds; for a plan
  start without a known slug, a `plan/*` branch counts only when the README's slug is that branch's name after
  `plan/` (as `gitstate.read_plan`). The plan's other files (`problems.md`, wave files) are read from the same branch.
- "Tracking branch exists": `refs/heads/plan/<slug>` exists, slug from the README header (`slug: `...``).

### Index start

1. `git show <main branch>:<index path>` fails → try `triage/<topic>` (`<topic>`: the index folder name without its
   `YYYY-MM-DD-` prefix). Found there → triage rules below. Not found → `halt <index path>: index not found — next:
   /wave-auto <list> · $wave-auto <list>` and `done`.
2. Triage rules (index only on `triage/<topic>`):
   - the header has `- Triage: waiting for answers` → `next: ask <index path>`;
   - the index has more than 8 problems (an overview table `| P | Summary | …`) and the triage worktree
     (`../<repo-folder>.worktrees/<topic>-triage`) lacks `plans/<date>-<topic>/triage/P<n>.md` of a problem of the
     overview → `next: triage-cluster <index path> <the clusters of those problems, from the overview's Cluster
     column, in order>`;
   - otherwise → `next: triage-finish <index path>`.
3. Index on `<main branch>`: for each row of "Parts", in order, unit `plans/<date>-<topic>/plan-<K>`, skipping the
   units of `skip`:
   - its README is found (Sources) → the plan rules below for that unit;
   - not found, "Plan when" is `now` → `next: plan <index path> part <K>`;
   - not found, `after part <J> merged`: part J is merged when its README is found and every feature is `✅ merged`
     or ➖ with its `Merged` hash in `<main branch>` or, when it exists, `integration/<topic>`
     (`git merge-base --is-ancestor <hash> <branch>`) — the rule of `layout.md`, "Chained parts and the integration
     branch", check 3 → `next: plan <index path> part <K>`; otherwise the part waits (no line).
   The first unit that yields a `next:` line ends the reading: print the `halt` lines found before it, then that line.
   No unit yields one → the `halt` lines, then `done`.

### Plan rules (one unit)

In this order; the first rule that applies decides the unit:

1. No tracking branch: every feature `✅ merged` or ➖ → finished (no line); else `halt <unit>: tracking branch
   plan/<slug> is missing — next: /wave-status <unit> · $wave-status <unit>`.
2. No `- Flow: autonomous` line in the README header → `next: ask-flow <unit>`.
3. A wave is `🔄`: the last non-empty line of its wave file's "Execution" starts with `Waiting: task mode ` →
   `next: tasks <unit> <N> <ID>:<tier>[ needs <Needs>]; …` for each ID of that line (strip a `(fix <k>/2)` mark),
   `<tier>` from the README "Tasks" Complexity column, `<Needs>` from the wave file's task table when it is not `—`.
   Otherwise `halt <unit>: wave <N> is 🔄 since <time> with no task-mode wait — next: wait for the run that holds it,
   or release the lock (wave-plan/layout.md, "Running waves")`.
4. A wave is `❌` → `halt <unit>: <the last "Stop <code>: …" line of its Execution>` (its own `— next:` part), or
   `wave <N> ❌ — next: /wave-plan <unit> · $wave-plan <unit>` when it has none.
5. The first `⬜` wave N: every `F<k> merged` of its `Depends on:` line must be `✅ merged`. For the first that is not:
   rule 6 applies → follow it; F<k> is `👀 review` → `halt <unit>: wave <N> needs F<k> merged; F<k> waits for review —
   next: review F<k>, then /wave-run <unit> merge F<k> · $wave-run <unit> merge F<k>`; otherwise `halt <unit>: wave
   <N> needs F<k> merged; F<k> is <status>, waiting for <Waiting for> — next: /wave-status <unit> · $wave-status
   <unit>`. All merged → `next: wave <unit> <N>`.
6. Re-plan: `problems.md` has an entry with `status: open` (not `→ task …`) whose feature's `Waiting for` is not
   `user: re-plan limit`, and no `⬜` wave can run (rule 5 found an unmerged `F<k> merged`, or no wave is `⬜`) →
   `next: re-plan <unit>`.
7. No `⬜` wave and rule 6 does not apply → finished (no line).

### Return grammar

```
halt <unit>: <reason> — next: <command or action>      (0–4 lines)
next: <action>                                          (or: done)
```

`<action>` is one of `ask <index path>`, `triage-cluster <index path> <cluster> …`, `triage-finish <index path>`,
`plan <index path> part <K>`, `ask-flow <plan folder>`, `wave <plan folder> <N>`,
`tasks <plan folder> <N> <ID>:<tier>[ needs <Needs>]; …`, `re-plan <plan folder>`. Commands in a `next:` part are
given in both forms.

## Triage phases (task C)

Add a section `## Coordinated phases` to `skills/wave-triage/SKILL.md` right after "Flow of planning":

````markdown
## Coordinated phases

`wave-auto` runs triage as four steps (`layout.md`, "Coordinated runs"), so that the coordinator asks the user once,
between `ask` and `answers`, and launches the cluster subagents itself. The phases of one index share its branch
`triage/<topic>` and worktree, which stay until `finish` merges them. A user may type these forms too.

| Form | Does | Returns |
|---|---|---|
| `flow autonomous ask <list>` | steps 1 and 2; then step 3 without asking and without choosing readings: every question goes into "Open questions" as `- Q<n> · P<k>: <question> — readings: (a) <…>; (b) <…>`, and the header gets `- Triage: waiting for answers` right after its `- Flow:` line; commit `Index <topic>: questions` | `questions <n> · index <index path>` |
| `flow autonomous answers <index path>` | the `Answers:` block of the prompt holds the user's answer verbatim; write each answer into the **Clarifications** of its problems (`<answer> (user's answer, <YYYY-MM-DD>)`; for more than 8 problems the records do not exist yet: write them into a section `## Answers` of the index, right before "Assumptions", one line `- P<k>: <answer> (user's answer, <YYYY-MM-DD>)` each, and `cluster` copies them into the records' **Clarifications**); each unanswered question gets an assumed reading ("Assumed readings" of `layout.md`); remove the `Q` lines and the `- Triage: waiting for answers` line; commit `Index <topic>: answers` | `answers recorded · clusters <cluster names>` for more than 8 problems, else `answers recorded · clusters none` |
| `cluster <cluster> <index path>` | the work of one cluster subagent of step 4, with its prompt's content read from the index (the cluster's problems, the user's words, the answers); write its `triage/P<n>.md` records in the triage worktree; a problem it cannot judge gets `**Difficulty:** <best guess> (unsure)`; no commit | `cluster <cluster>: <n> records · high <h> · unsure <u>` |
| `flow autonomous finish <index path>` | step 4 for at most 8 problems (inline records); for more, only the re-judging (records whose Difficulty is `high` or ends `(unsure)`) and the dependencies (shared paths of the records' **Where**); then steps 5 to 8. When "Parts" is already committed: only the merge of step 8 | `parts <k> · index <index path> · merged <short hash>` |

- `ask` and `answers` are in autonomous flow of planning, so `ask` writes the `- Flow:` line; `ask` collects the
  questions instead of choosing readings, `answers` chooses readings only for unanswered questions.
- A form that finds the index in another phase (`answers` without the `- Triage: waiting for answers` line, `finish`
  with a record of the overview missing) stops `phase-mismatch`, naming what it found; nothing written.
- `finish`, step 8: `<main checkout>` not ready (`layout.md`, "Main readiness") → stop `main-dirty: <reason> — next:
  git -C <main checkout> merge --no-ff triage/<topic> -m "Index <topic>"`; branch and worktree stay.
````

Also, in step 4, after "For more than 8 problems, when the environment has subagents …" add one sentence: "In a
coordinated run the coordinator launches them (`cluster` form of "Coordinated phases")." In step 8 "Stop", add: "In
a coordinated run return the line of "Coordinated phases" instead of this answer."

## `wave-run` in a coordinated run (task B)

### `skills/wave-run/SKILL.md`

1. After the "Flow form" paragraph of the arguments, add:

   > **Coordinated run** (`layout.md`, "Coordinated runs"; steps `wave`, `task`, `flow`): the plan must be in
   > autonomous flow, else stop `manual-flow` before anything is written. Every task runs in task mode
   > (`task-mode.md`): no task subagent is launched and `tier-missing` is not checked, because the coordinator
   > launches each task on a model of its tier. Nothing is asked, `report.md` is not read, and the run ends with the
   > return line of that section instead of the final report. Step 1 writes `Capabilities: coordinated run (every task
   > in task mode)`.
2. Hard rules, "Every final report follows the template …": append "A coordinated run returns its return line
   instead (`layout.md`, "Coordinated runs")."
3. Stops table: new row after `capability-missing`: `` `manual-flow` `` | a coordinated run of a plan in manual flow |
   `/wave-run <plan folder> flow autonomous`<br>`$wave-run <plan folder> flow autonomous`.
4. "Fix loop": append "Without a subagent to send it to (a coordinated run, or a resume in a session without
   subagents), the request becomes a fix request for a task-mode session (`task-mode.md`, "Fix requests"); each
   counts as an attempt."
5. Step 5, the bullet "Read the report's final block": insert at its start "For a task run in task mode, the block is
   the paragraph of `Done:`/`Try:`/`Not checked:`/`Problems:` lines in the body of its last commit
   (`git log -1 --format=%B <last commit of the task>`, `task-mode.md`)."

### `skills/wave-run/task-mode.md`

1. Waiting line grammar (coordinator bullet): `Waiting: task mode <ID>[ (fix <k>/2)], … — next: <commands>`.
2. Task session, after "Do the task from its prompt in the prepared worktree": add
   - "Already done: the task has its commits (task branch: `git log feat/<plan>/<feature>..<task branch>` is not
     empty; direct task: a commit after the head recorded in the waiting record whose subject starts
     `<plan> <feature-id> / <task-id>:`) and the waiting line has no `(fix <k>/2)` for it → change nothing; report
     `already committed <short hash>`."
   - "The last commit of the task carries the report's `Done:`, `Try:`, `Not checked:` and `Problems:` lines as one
     paragraph of its body, right before the trailer block, so the resume can read them (`SKILL.md` step 5)."
   - "Coordinated run: end with the `task` return line of `layout.md`, "Coordinated runs", instead of the report."
3. New section `## Fix requests`:

   > When the resume must change a task's work (`SKILL.md`, "Fix loop") and has no subagent to send it to, it writes
   > into the wave file's "Execution" a line `Fix <ID> <k>/2: <what to change; the error text, at most 20 lines>` and
   > ends the Execution again with the waiting line, the task marked `(fix <k>/2)`, committed as
   > `Plan <plan>: wave <N> waiting for task mode`. A task session whose ID carries that mark reads the last
   > `Fix <ID> <k>/2` line, makes that change on the task's branch in the prepared worktree, commits it with a new
   > report block, and runs the check. After the second attempt the task is ⚠️ as "Fix loop" says.

## `wave-plan` and `wave-status` (task F)

- `skills/wave-plan/SKILL.md`, Input, after the "Flow of planning" bullet: add a bullet "**Coordinated run**
  (`layout.md`, "Coordinated runs"; steps `plan` and `re-plan`): autonomous flow of planning; ask nothing; end with
  the return line of that section instead of the answer of step 9." In step 9's answer paragraph, append the same
  exception in one sentence.
- `skills/wave-status/SKILL.md`:
  - "What to read": add `git for-each-ref --format="%(refname)" refs/wave-method/claims/auto/` and, for each ref,
    `git cat-file -p <ref>`.
  - "Index parts" section: after the parts table rules add a line rule: `Coordinator claims:` one line per ref,
    `<name>: <holder line>`; `none` when there is no ref. In the commands of that section, every index with an
    unplanned part or an unfinished plan also gets `/wave-auto <index path>` · `$wave-auto <index path>` as the
    alternative that runs everything from one session.
  - "Leftovers": a coordinator claim: suggest `git update-ref -d refs/wave-method/claims/auto/<name>`, once the user
    is sure no `wave-auto` session runs.

## Installers and docs (task G)

- `install.sh` line 32: `skills="wave-triage wave-plan wave-run wave-status wave-auto"`. `install.ps1` line 18: add
  `'wave-auto'` to `$skills`. Header comments unchanged (`wave-*` already covers it).
- `.claude-plugin/plugin.json` description: "… merge only what is finished: wave-triage, wave-plan, wave-run,
  wave-status and wave-auto skills." `.claude-plugin/marketplace.json` description: "… run them in git worktrees and merge
  finished features, or run it all from one command in one session." (one sentence).
- `README.md`:
  - line 5: "a set of four agent skills" → "a set of five agent skills"; "Manual install: copy the four folders" →
    "the five folders".
  - New subsection `### One command in one session: wave-auto` in "Overnight runs (autonomous flow)", right before
    "### Running overnight with the driver", text:

    ```markdown
    `/wave-auto <list>` (Codex: `$wave-auto <list>`) runs the whole pipeline in the session you type it in — the
    Claude Code CLI (`claude`) or the Claude Code desktop app. It asks the triage questions once, at the start, then
    triages, plans every part and runs every wave in autonomous flow, each step as a subagent on a model of the
    step's tier, printing one line per step. It ends with the `wave-status` report: features merged into
    `integration/<topic>`, features waiting for your review, blocked features and what each waits for.

    - Start from a list, an index (`/wave-auto plans/<date>-<topic>/index.md`) or a plan folder.
    - Bound it with `until 07:00` or `steps 40` before the start: `/wave-auto until 07:00 plans/<…>/index.md`.
    - Nothing is kept in the chat: if the window closes or a usage limit stops the session, run
      `/wave-auto plans/<date>-<topic>/index.md` in a new session and it continues where it stopped.
    - A step that cannot run as a subagent of its tier runs in a separate session where the app can start one;
      otherwise the run stops with the command to run by hand.
    ```
  - "Requirements", the Claude Code bullet: append "`wave-auto` needs subagents with a choice of model (Claude Code
    CLI or desktop app)."
  - "Limitations": add a bullet "**wave-auto** was rehearsed in the Claude Code CLI and desktop app
    ([rehearsals](docs/rehearsals/)); its rails (`until`, `steps`) are rules of the skill, not enforced limits."
  - "Customising": add a row `Rails of an in-session run` | `until` and `steps` of `/wave-auto`
    (`wave-auto/SKILL.md`).
- `skills/wave-plan/CHANGELOG.md`: append to the `- Unreleased — …` item a new paragraph line:
  "New skill `wave-auto`: one command runs triage (its questions asked once, at the start), the plan of every part and
  every wave in autonomous flow inside one session, each step as a subagent that returns one line
  (`layout.md`, "Coordinated runs"; navigator rules in `wave-auto/navigator.md`); git is its only memory, so the same
  command in a new session continues; a claim ref `refs/wave-method/claims/auto/<name>` keeps one coordinator per
  start. `wave-triage` gains the phases `ask`, `answers`, `cluster` and `finish`; a task-mode session puts its report
  block into its last commit's body, does not redo a committed task and takes fix requests from the wave file;
  `wave-run` stops `manual-flow` in a coordinated run of a manual plan. Installers and the plugin list the fifth skill."

## Rehearsals (tasks H and I)

### Fixture (both)

A scratch folder made with `mktemp -d` outside every repository. Repository `textkit`:

- `git init -b main`, user name/email set locally to `rehearsal` / `rehearsal@example.invalid`.
- `textkit/__init__.py` (empty), `tests/test_smoke.py` with `def test_import(): import textkit`, `README.md` one line
  "textkit — small text helpers. Check: python -m pytest -q", `.gitignore` with `__pycache__/`, `.pytest_cache/`.
- A virtual environment `<scratch>/venv` with pytest (`python -m venv`, `pip install pytest`); every command runs
  with that venv first on `PATH`.
- Skills: `<working folder>/install.sh <scratch>/textkit --no-codex`, then commit everything:
  `Seed textkit with wave skills`.

The list (verbatim, one start argument):

```
1. Add textkit/slug.py with slugify(text): lowercase, words joined by "-", only letters and digits kept. 2. Add textkit/count.py with count_words(text) returning a dict word -> count, words compared without case. 3. Add a command "python -m textkit top <file>" that prints the top words of the file with their counts.
```

Item 3 is deliberately open ("top" = how many?), so triage has at least one question.

### Rehearsal H — Claude Code CLI (`docs/rehearsals/coordinator-cli.md`)

Every call in `<scratch>/textkit`, with `--output-format stream-json --verbose` saved to `<scratch>/calls/<run>.jsonl`,
`--permission-mode auto` (if denials keep a step from finishing, repeat the whole rehearsal in a fresh scratch with
`--permission-mode bypassPermissions` and record why), and `MSYS_NO_PATHCONV=1` on Windows Git Bash.

| Run | Command | Expected |
|---|---|---|
| P0 | `claude -p "Launch one subagent. Ask it to list the names of all its tools that can start another agent, subagent or session, or to answer 'none'. Reply with its answer verbatim."` | the answer is `none` or names no agent tool (records the no-nesting fact) |
| C1 | `claude -p "/wave-auto steps 4 <list>"` | one `triage-ask` step; the result asks ≥ 1 question about item 3; branch `triage/<topic>` exists with `- Triage: waiting for answers`; claim `refs/wave-method/claims/auto/<topic>` exists |
| C2 | `claude -p --continue "Top 10 words, most frequent first."` | steps `triage-answers`, `triage-finish`, `plan` (rail ends after 4 steps: `ended by rail: steps 4`); index merged into `main`; plan folder on `plan/<slug>` and `integration/<topic>`; claim released; the final report has the Steps, Halts, Status and Next sections and the resume command |
| C3 | write a stale claim: `printf 'wave-auto stale 2026-01-01 00:00 run deadbeef\n' \| git hash-object -w --stdin` and `git update-ref refs/wave-method/claims/auto/<topic> <oid>`; then `claude -p "/wave-auto plans/<date>-<topic>/index.md"` | the coordinator asks whether the holder is gone, quoting the holder line; nothing else happens |
| C4 | `claude -p --continue "Yes, it is gone."` | waves run to the end: per wave a `wave` step, `task` steps, a resume; every feature `✅ merged` into `integration/<topic>` (auto-approved) or a finding; `main` unchanged since C2; no 🔄 wave; claim released; final report |
| C5 | in the scratch main checkout: `git merge --no-ff integration/<topic>` then `python -m pytest -q`; and `python -m textkit top README.md` | tests green; the command prints at most 10 lines `word count` |

Also check from the stream of C2 and C4: every agent-tool call's model matches its step's tier (`navigate` haiku;
`triage-*` and `plan` opus, `triage-cluster` sonnet; `wave` sonnet; `task` by the task's complexity); the coordinator's
own context stays small (record the `usage` of the last `result` event: input and output tokens); no step's subagent
asked a question. Cost cap: stop starting calls when the summed `total_cost_usd` reaches 30 USD; record the rest as
Not run.

### Rehearsal I — Claude Code desktop app (`docs/rehearsals/coordinator-desktop.md`)

Needs a session of the Claude Code desktop app (Code tab) that can start another session in a given folder with a
chosen model and send it a message (the app's session tools). Same fixture, in its own scratch folder.

| Run | Action | Expected |
|---|---|---|
| D1 | start a new desktop session, folder `<scratch>/textkit`, model Opus, first message `/wave-auto <list>` | it asks ≥ 1 question about item 3 and waits |
| D2 | send it `Top 10 words, most frequent first.` | it runs to the end without another question: one progress line per step; final report with every feature merged into `integration/<topic>` or listed under Halts with a next command |
| D3 | start a second new session there with `/wave-auto plans/<date>-<topic>/index.md` | no question; the navigator finds nothing to run; the report says `ended by done` with the same Status |
| D4 | merge and test as C5 | green |

If this session cannot start or message another session, do D1–D2 by following `skills/wave-auto/SKILL.md` yourself in
this session with `<scratch>/textkit` as the repository (answer the question in your own next message) and record
that the separate-session form was not run.

### Record format (both)

Sections `## Setup`, `## Runs` (one subsection per run: command, exit, the deciding lines quoted, the files that
show it), `## Results` (table: expectation | Pass / Finding / Not run | evidence), `## Not verified`, `## Repeat`
(the commands to repeat it). Replace real paths with `<scratch>` and `<working folder>`; no user name or home path.
A step that differs from its expectation is a finding, never fixed in the rehearsal; each finding also goes into the
report's `Problems:`.

## Limits

- The rails are soft: they act between steps; a long step is not cut short. No guard on `<main branch>` as the
  driver had: in an interactive session the user may work on `main` meanwhile; the skills' own rules keep it
  untouched (autonomous flow writes only the integration branch; triage merges only its index).
- A wave interrupted between its "started" and "waiting" commits stays 🔄 without a waiting line; the navigator
  halts it (`wave-running`); the user releases it as "Running waves" says.
- Re-plans are bounded by "Re-plan escalation": a feature is re-planned automatically at most twice (round 2
  escalated, under manual review); round 3 is held for the user.
- Permission prompts of the environment still appear; an unattended run needs a permission mode that lets subagents
  run git, the check command and file edits in the worktrees.
- Codex (CLI and desktop) is part 2 (P2): this part writes the skill vendor-neutrally where it costs nothing
  (subagent, session, both command forms) but verifies Claude Code only.

## Acceptance tests

1. `layout.md` has `## Coordinated runs` with the steps table (11 steps, exactly the names `navigate`,
   `triage-ask`, `triage-answers`, `triage-cluster`, `triage-finish`, `plan`, `re-plan`, `flow`, `wave`, `task`,
   `status`) and `### Coordinator claim`; the six other edits are in place (task A).
2. `skills/wave-auto/SKILL.md` has the frontmatter above and sections 1–15; its dispatch table names every `next:`
   action of the navigator grammar; its step prompt template matches "Coordinated runs" (task E).
3. `skills/wave-auto/navigator.md` has Sources, Index start, Plan rules 1–7 and Return grammar; every action of the
   grammar is one of the dispatch table's (task D).
4. `wave-run`: `manual-flow` stop, coordinated paragraph, fix-loop fallback, commit-body block, `Fix requests`
   section, already-done rule (task B). `wave-triage`: "Coordinated phases" with four forms (task C).
5. Status-check tests, driver tests and the three examples pass unchanged; `git diff --check` is clean.
6. Rehearsal H: P0 and C1–C5 recorded; every expectation Pass, or a Finding with an open problem entry.
7. Rehearsal I: D1–D4 recorded likewise.
