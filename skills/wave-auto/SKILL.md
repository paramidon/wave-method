---
name: wave-auto
description: Runs the whole wave pipeline from one command inside one session — triage of a list (its clarifying questions asked once, at the start), the plan of every part and every wave, in autonomous flow — as a coordinator that delegates each step to a subagent and keeps one line per step. Git and plans/ are its only memory, so the same command in a new session continues where the last one stopped. Use when the user runs "/wave-auto <list | index | plan folder>" or "$wave-auto …", or asks to run the pipeline unattended in one session ("запусти всё сам", "прогони от списка до мержа"). Recommended model: high complexity (Opus-class) — a subagent without a model choice inherits it.
---

# wave-auto — run triage, plans and waves from one session

Language: talk to the user in the language of their messages; write everything into the repository in English,
always (`wave-plan/layout.md`, "Language"). Start and end time of the run: `wave-plan/layout.md`, "Run times".

Skill paths such as `wave-plan/layout.md` are relative to the wave skills folder, the parent of this skill's
folder (`wave-plan/layout.md`, "Skill paths").

## Layout

Read `wave-plan/layout.md` first, above all "Flow", "Coordinated runs", "Model tiers", "Tier gate", "Environment
capabilities", "Target claim" and "Results of an autonomous run". This skill does not repeat it. The navigator
subagent reads `wave-auto/navigator.md`; the coordinator does not need it, except to know what it returns.

## Input

`/wave-auto [until <HH:MM | YYYY-MM-DD HH:MM>] [steps <N>] <start>` ·
`$wave-auto [until <HH:MM | YYYY-MM-DD HH:MM>] [steps <N>] <start>`

Options come first. A bare `HH:MM` is the next such time after the start of the run. `<start>` is one of:

- `plans/<date>-<topic>/index.md` → an index start (its topic names the claim);
- a plan folder (`git cat-file -e <source>:<folder>/README.md` succeeds for `<main branch>`, a `plan/*` branch or an
  `integration/*` branch) → a plan start (its slug names the claim);
- anything else, verbatim → a list start;
- nothing → stop `no-start` with the three forms.

## Hard rules

- The coordinator changes no file, makes no commit or merge, and never pushes; the only ref it writes is its claim.
  Every change is made by a step's subagent through its skill. The token and oid of its claim live in the
  conversation only: never in a file, not even in a temp folder, and never in a shell variable that a later command
  needs. The command that takes the claim prints the oid, and the release or takeover command has it
  written out literally (`wave-plan/layout.md`, "Target claim").
- It reads nothing of `plans/` but the "Open questions" of an index on its triage branch, when it asks them. It never
  reads plan READMEs, wave files, solutions or task prompts, and never retells a subagent's output beyond its return
  line.
- It asks the user only in the start phase. It never answers a question for the user and never lowers a tier.
- Every step is in autonomous flow: features are auto-approved into `integration/<topic>` (or `integration/<slug>`);
  `<main branch>` receives only the triage index (step `triage-finish`).
- One progress line per step to the user, `navigate` included: `<HH:MM> · <step> · <unit> → <return line>`
  ("Loop", "Progress lines").
- It never runs, builds, tests or tries the project, in any worktree, at any point of the run, not even to confirm a
  result. The commands it runs itself only read git and the skill files this skill names, take or release its claim,
  and read the clock.
- It writes the user only what this skill names: the `Started:` and `Capabilities:` lines, the progress lines, the
  `Resume:` line, its questions, a line that it waits for running steps, a stop line and the final report. It adds no
  summary, comment or explanation of its own.

## Capabilities

At the start, from the tools this session has (`wave-plan/layout.md`, "Environment capabilities"), find out:

- subagents;
- parallel subagents;
- model choice per subagent: which choice names a model of each tier. In Claude Code the agent tool's `haiku` = low,
  `sonnet` = medium, `opus` = high; a README `Models:` line may only name a tier or higher;
- starting a session;
- the tools a task's `Needs` names (checked when a task needs one).

Print one line `Capabilities: …`, for example
`Capabilities: subagents · parallel · model choice (low haiku, medium sonnet, high opus) · session start no`.
Neither subagents nor starting a session → stop `no-subagents`, `next:` the manual commands (`/wave-triage`,
`/wave-plan`, `/wave-run`, in both forms).

## Step prompt

Every step's subagent gets exactly this prompt (the first line only for a medium or high step):

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

`<skill>` and `<arguments>` are those of the step's row in the steps table of `wave-plan/layout.md`, "Coordinated
runs"; `<tier>` is its Tier column, and `<models of that tier or higher>` come from "Model tiers" (or the README
`Models:` line). The `navigate` step takes `wave-auto/navigator.md` and `start <start> · skip <units, or none>` for
`<skill>` and `<arguments>` and replaces the last three lines with
`Read <skills folder>/wave-auto/navigator.md and follow it with: start <start> · skip <units, or none>`.
The `triage-answers` step appends `Answers:` and the user's answer verbatim. Model: the tier's model choice.

`<unit>`: a plan folder; for an index part not planned yet, the folder its plan will have
(`plans/<date>-<topic>/plan-<K>`); before the index has parts, the index path; for `triage-ask` of a list start, which
has no index yet, `list`; for `navigate`, the start.

## Start phase

The only questions of a run. Each kind is asked at most once, all questions of one kind in one message, in the user's
language.

1. Read the clock (`Started:` line, `wave-plan/layout.md`, "Run times"); resolve the skills folder, the main checkout
   (`git rev-parse --show-toplevel`) and `<main branch>`; check the capabilities.
2. List start: run `triage-ask`; its index path gives `<topic>`. Right after its progress line, in the same text and
   before anything else, write the line `Resume: /wave-auto <index path> · $wave-auto <index path>`, whether or not
   questions follow (`questions 0` too).
3. Take the coordinator claim, the ref `refs/wave-method/claims/auto/<name>` (`wave-plan/layout.md`, "Coordinated
   runs", "Coordinator claim"): `<name>` is the index topic, or the plan slug for a plan start (the folder
   `plans/<date>-<topic>/plan-<K>` has slug `<topic>-p<K>`, the folder `plans/<date>-<slug>` has slug `<slug>`; no file
   is read for it); `<start>` in the holder line is the index path for a list start. Refused → ask whether the holder
   is gone (quote its holder line); yes → take it over; no → stop `wave-running`, naming the holder.
4. Questions: after `triage-ask` with `questions <n>` > 0, or when the navigator returns `next: ask <index>`, read the
   `- Q<n> · …` lines of "Open questions" with `git show triage/<topic>:<index path>`, ask them all in one message and
   wait. With `questions 0`, or when the index has no `- Q<n>` line, ask nothing and do not wait. Then run
   `triage-answers` with the answer verbatim (`Answers: none` for 0 questions; the user may answer only some). When
   the navigator returns `next: ask-flow <plan folder>`: ask whether to switch that plan to autonomous flow; yes →
   step `flow`; no → halt the unit.
5. The start phase ends with the first step that is not `triage-ask` or `navigate`. From then on a navigator line
   `next: ask …` or `next: ask-flow …` halts its unit instead (`questions-late`, `next:` the manual command).

## Loop

```
repeat:
  rails (below) → end the run when one is reached
  navigate (start, skip = halted units), then its progress line
  add every `halt` line's unit to the halted units, keep its line for the report
  `done` → final report
  the same `next:` line as the previous navigate → halt that unit `no-progress`
  dispatch the `next:` line (table below), each step with its progress line as it returns
```

| Navigator line | Dispatch |
|---|---|
| `next: ask <index path>` | start phase only: the questions of 4 of the start phase, then `triage-answers` |
| `next: triage-cluster <index path> <cluster> …` | one `triage-cluster` step per cluster, in parallel where possible, then `triage-finish` |
| `next: triage-finish <index path>` | `triage-finish` |
| `next: plan <index path> part <K>` | `plan` |
| `next: ask-flow <plan folder>` | start phase only: 4 of the start phase |
| `next: wave <plan folder> <N>` | "Wave" below |
| `next: tasks <plan folder> <N> <ID>:<tier>[ needs <Needs>]; …` | "Wave" below, from its task steps |
| `next: re-plan <plan folder>` | `re-plan` |

After `triage-answers`, run the cluster steps its return names (none → `triage-finish`) without navigating first.

### Progress lines

Every step except `status`, whose report is the final one, gets its own line: `triage-ask`, `triage-answers`,
`triage-cluster`, `triage-finish`, `plan`, `re-plan`, `flow`, `wave`, `task` and `navigate` alike. For `navigate` the
result is its `next:` or `done` line.

- When a step returns, read the clock with a shell command (`date +%H:%M`; PowerShell `Get-Date -Format HH:mm`), then
  write its line to the user as text, before the next step starts. Never collect lines to write later: the "Steps"
  table of the final report does not replace them.
- Never estimate a time and never write a placeholder such as `17:3x`. The "Steps" table repeats the times of these
  lines.
- Steps launched together (tasks, clusters) get one line each, as each one returns.

## Wave

`wave` step → while it returns `waiting …`, for the tasks it lists:

1. Launch one `task` step for every listed task that can run here as a subagent of its tier (its `Needs` tools are in
   this session), in parallel where the environment allows: all in one message, each on its tier's model. Wait until
   every one of them has returned.
2. Only then: each listed task that cannot run here goes to "Session fallback".
3. No task of 1 returned a stop (`tier-mismatch`, `capability-missing`, …) and no task of 2 was halted → the `wave`
   step again (the resume). Otherwise halt the unit with the first such stop or halt, and do not resume: the commits
   of the other tasks stay on their branches, and the next `/wave-auto <start>` · `$wave-auto <start>` resumes the
   wave, where they return `already committed`.

A task ID run 3 times in one dispatch (once and two fix requests) and listed again → halt the unit `step-failed`.

A halt never ends the run and prints no `Stop` line: the unit goes to "Halts", and the loop navigates again with that
unit skipped ("Loop").

When the navigator line is `next: tasks …`, the wave is already waiting: start from the `task` steps of that line.

## Results of steps

A return line that does not match its step's form (or no return) → run the step once more; again wrong → halt the
unit `step-failed: <step>`. A `Stop <code>` return halts its unit with that line, except `target-unsafe`,
`target-conflict` and `target-unmerged`, which halt every unit of the run (one index shares one target) and end it.
A `triage-*` stop ends the run (nothing else can run before the index exists).

## Session fallback

A step that cannot run as a subagent of its tier (no subagents, no model choice for its tier, or a `Needs` tool
missing): when the environment can start a session with a model of that tier whose result comes back here, start it
there with the skill's command in its normal form, `flow autonomous` included
(`/wave-plan flow autonomous <index path> part <K>`, `/wave-run <plan folder> <N>`,
`/wave-run <plan folder> <N> task <ID>`), in the repository, and wait for its result. The session runs the skill
normally, so a whole wave in a session uses its own subagents. Then go on: for a task, with item 3 of "Wave"; for any
other step, navigate again. The session's text is not kept.

Otherwise halt the unit `tier-missing` or `capability-missing`, `next:` that command in both forms, "in a fresh
session with <models>", then `/wave-auto <start>` · `$wave-auto <start>` again.

## Rails

Checked before every step except `navigate` and `status`:

- `until`: no step starts at or after that time, read from the clock;
- `steps`: at most N steps; default 60. The count is the number of step subagents this run has launched for steps
  other than `navigate` and `status`: each agent call whose prompt has the line `Coordinated run · step <step> · …`.
  Count them again in this conversation before each step; never carry the count in mind.

Reaching one ends the run with its final report, `ended by rail: …`. A step already running is not cut short. A wave
left waiting by a rail stays 🔄 with its claim marked waiting: the next `/wave-auto <start>` · `$wave-auto <start>`
resumes it.

## End of the run

Release the claim, then run the `status` step (the start's plan folder for a plan start, no argument otherwise), so
that its report does not list this run's own claim. Read the clock and print:

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

The Steps table has one row per step this run launched other than `navigate` and `status`, in the order launched;
`<n>` in `Run:` is the number of its rows, counted after the table is written, never from memory. Halts lists the
`halt` lines the navigator returned and the units halted by "Results of steps".

The final report is this template and nothing else: no paragraph, section or note is added between or inside its
parts, the `status` report is copied verbatim, and nothing follows the `Started: … · Finished: …` line. `### Next`
holds only the `Continue:` line, or `- none` when nothing is halted, waiting or cut by a rail. After the `status` step
returns, the only command the coordinator runs reads the clock.

## Stops

Every stop prints `Stop <code>: <one line> — next: <command or action>` as the first line of the report after the
`Started:` line. A stop that ends the run releases the claim, then prints the report of "End of the run", without the
`status` step when no step ran.

Stops that end the run:

| Code | When | Next |
|---|---|---|
| `no-start` | the command has no `<start>` | `/wave-auto <list>`<br>`$wave-auto <list>`<br>`/wave-auto plans/<date>-<topic>/index.md`<br>`$wave-auto plans/<date>-<topic>/index.md`<br>`/wave-auto <plan folder>`<br>`$wave-auto <plan folder>` |
| `no-subagents` | the session has neither subagents nor a way to start a session | `/wave-triage <list>`<br>`$wave-triage <list>`<br>`/wave-plan <index path> part <K>`<br>`$wave-plan <index path> part <K>`<br>`/wave-run <plan folder> <N>`<br>`$wave-run <plan folder> <N>` |
| `wave-running` | the coordinator claim is refused and the user said the holder is not gone | wait for the holder, or release `refs/wave-method/claims/auto/<name>` once sure no `wave-auto` session runs, then `/wave-auto <start>`<br>`$wave-auto <start>` |
| `target-unsafe`, `target-conflict`, `target-unmerged`, any `triage-*` stop | passed through from a step ("Results of steps") | the `next:` of the step's own stop line |

Halts of one unit. A halt is not a stop: it prints no `Stop` line and does not end the run, whatever its code; the
run goes on with the other units and ends with them in "Halts":

| Code | When | Next |
|---|---|---|
| `questions-late` | the navigator returns `next: ask …` or `next: ask-flow …` after the start phase | the manual command of the unit, for example `/wave-triage flow autonomous answers <index path>`<br>`$wave-triage flow autonomous answers <index path>` |
| `no-progress` | the navigator returns the same `next:` line twice in a row | `/wave-status <unit>`<br>`$wave-status <unit>` |
| `step-failed` | a step's return does not match its form twice, or a task ID is listed again after three runs in one dispatch | `/wave-status <unit>`<br>`$wave-status <unit>` |
| `tier-missing` | a step needs a model of a tier this session cannot choose and no session can be started for it | its command in both forms ("Session fallback"), in a fresh session with the models of that tier, then `/wave-auto <start>`<br>`$wave-auto <start>` |
| `capability-missing` | a task's `Needs` names a tool this session lacks and no session can be started | the task's command in both forms ("Session fallback"), then `/wave-auto <start>`<br>`$wave-auto <start>` |
| any other `Stop <code>` of a step (`tier-mismatch`, …) | returned by a step ("Results of steps") | the `next:` of the step's own stop line |

## Resume

The same command in a new session: the start phase takes the claim (the old session released it, or the user confirms
the takeover), and the navigator finds where the state is. A list start resumes with
`/wave-auto plans/<date>-<topic>/index.md` · `$wave-auto plans/<date>-<topic>/index.md`; the coordinator writes it as
the `Resume:` line right after the progress line of `triage-ask` ("Start phase", 2).
