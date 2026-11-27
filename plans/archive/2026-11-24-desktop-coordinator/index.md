# Desktop coordinator — index

- Index: `plans/2026-11-24-desktop-coordinator/index.md` · created 2026-11-24 · base: fe1dbf2 · triaged 2026-11-24 21:11 – 2026-11-24 21:17; updated 2026-11-24 21:44 – 2026-11-24 21:45

## Source list (verbatim)

жалоба:
автономный режим работает в CLI интерфейсе только. 
Он не работает в десктопной версии клод кода и в десктопной версии чат ГПТ. надо чтобы работал также в десктопе.
например - я запускаю  новый скиk и он уже сам является координатором - делает в субагентах триажи, планирование, передаёт задачи между субагентах и так далее.
Возможно такое сделать?
Хочу чтобы была возможность запуска этого как из консоли так и из десктопных клод кода и чат ГПТ кодекс.

The one complaint is split into problems P1–P3 below; P4 came from the triage discussion.

## Problems

### P1. In-session coordinator skill: one command runs triage → plans → waves, delegating to subagents (Claude Code CLI and desktop)
**User's words:** "автономный режим работает в CLI интерфейсе только. Он не работает в десктопной версии клод кода … например - я запускаю новый скиk и он уже сам является координатором - делает в субагентах триажи, планирование, передаёт задачи между субагентах и так далее."
**Clarifications:**
- Today "autonomous mode" unattended = the Python driver `scripts/wave_driver.py`, which starts one headless
  `claude -p` per step; it needs a terminal and the Claude Code CLI. Autonomous *flow* itself (integration branch,
  auto-approval) already works in any session; what is missing is the in-session coordinator that chains the steps.
- Approval: autonomous flow, as the driver — features are auto-approved into `integration/<topic>`; the user
  reviews and merges the integration branch afterwards (user's answer).
- Questions: the coordinator asks the triage clarifying questions **once, at the start**, then runs without
  questions (user's answer). This is a new combination: triage today is either manual (asks) or `flow autonomous`
  (never asks, writes `- Flow: autonomous` into the index). The coordinator needs "ask once, then write the
  autonomous header".
- No subagents or no model choice per subagent: start the step in a fresh session where the environment can (for
  example the desktop app's session tool), otherwise stop with the task-mode commands; never run a task on a
  lower tier (user's answer; tier gate unchanged).
- Console = the same skill in an interactive `claude` session. No Python: the coordinator does the whole
  coordination itself; the driver is removed (P4).
- **Design direction agreed with the user (2026-11-24)**: the coordinator holds no state and reads no plan files;
  git and `plans/` are the only memory. Context per step stays at a few lines:
  1. **Navigator subagent** (low tier, read-only): reads the state from git and returns one line —
     `next: plan part <K>` / `next: wave <N> of <plan folder>` / `next: task-mode …` / `stop <code>: …`. It is the
     driver's `decide.py` logic expressed as skill rules.
  2. **A wave is cut into steps that need no nesting**: a *prepare* subagent (branches, worktrees; returns only
     `task ID · tier · worktree` per task); the coordinator launches one subagent per task with a short header that
     points to the prompt in the wave file (the task reads its own prompt; the full prompt never enters the
     coordinator's context); a *merge+check* subagent (merges, runs the check, records statuses and the wave report
     in files; returns one line such as `wave 3: ✅ 4/4, F2 auto-approved` or `stop …`).
  3. **Triage in two passes**: a subagent analyses the list and returns only the questions; the coordinator asks
     the user once; a second subagent records the answers and splits into parts. Cluster subagents of a large list
     are launched by the coordinator itself, not by the triage subagent.
  4. **Planning**: one high-tier subagent per part, returning one line.
  5. **Fixed return contract**: every subagent returns at most ~5 lines in a fixed form; all details go to files
     under `plans/`.
  6. **Resume**: since all state is in git, auto-compaction loses nothing, and a new session started with the same
     command continues where the last one stopped (closed window, usage limit).
  7. **Sub-coordinators as sessions**: where the environment can start a separate session that has its own
     subagents (for example the Claude Code desktop app), the coordinator may delegate a whole wave or part to it
     and receive its one-line result; this is an optional capability, the flat cut above is the base.
  Estimate: ~0.5–1k tokens of coordinator context per step.
**Where:** new skill folder `skills/wave-<name>/SKILL.md` (working name `wave-auto`, final name chosen by the
plan) · `skills/wave-plan/layout.md` ("Who reads what" line 5, "Environment capabilities" line 129, "Commands"
line 160, "Flow" line 354, "Planning in autonomous flow" line 540) · `skills/wave-triage/SKILL.md` (step 3
questions, step 4 cluster subagents) · `skills/wave-run/SKILL.md` (capability table line 73, final report and
"next command" ending — the coordinator continues instead of stopping) · `skills/wave-run/autonomous.md` (target
claim, stops) · `install.sh:32`, `install.ps1:18` (hard-coded skill list) · `.claude-plugin/plugin.json`
(description lists four skills) · `README.md` (skill list, Requirements line 330, Limitations line 397) ·
`skills/wave-plan/CHANGELOG.md`.
**Reuse:** the driver's next-action logic `scripts/wavedriver/decide.py` (`choose`, `after_call`) and state reader
`scripts/wavedriver/gitstate.py` (`read_snapshot`, `part_merged`) as the source of the navigator's rules (read
them before P4 deletes them; never call them); `wave-status` (read-only state reading); the stop codes and
"Results of an autonomous run" of `layout.md`; the morning report shape of `scripts/wavedriver/report.py`.
**Likely cause / gap:** no skill plays the driver's role inside a session; every skill ends by printing the next
command for the user. Constraint (unverified): in Claude Code a subagent cannot start subagents, so wave-run's
task dispatch and triage's cluster subagents cannot run inside a subagent — the coordinator must keep those
coordinator roles itself (or use fresh sessions) and delegate only leaf work (planning a part, tasks). Long runs
grow the coordinator's context; rails (deadline, max calls, cost) are only soft inside a session.
**Difficulty:** high (design of the coordinator's loop under the no-nesting constraint, context budget, rails,
resume after an interrupted session; touches core rules in `layout.md`) · **Size:** 4+ tasks, modules: new skill,
layout, wave-triage, wave-run, installers/docs, a rehearsal in Claude Code desktop and CLI.
**Depends on:** — (P2 and P3 depend on it)

### P2. The same coordinator works in Codex (CLI and desktop app)
**User's words:** "Он не работает … в десктопной версии чат ГПТ … Хочу чтобы была возможность запуска этого как из консоли так и из десктопных клод кода и чат ГПТ кодекс."
**Clarifications:** without subagents with model choice the coordinator starts fresh sessions where possible,
else stops with task-mode commands (user's answer, same as P1). The driver is not extended to `codex exec`
(see Assumptions).
**Where:** the new coordinator skill of P1 (capability detection, Codex command form `$wave-…`) ·
`skills/wave-plan/layout.md` "Environment capabilities", "Model tiers" (GPT tier names) · `install.sh` /
`install.ps1` (`.agents/skills/` links for Codex) · a new rehearsal under `docs/rehearsals/` for Codex CLI and the
Codex desktop app · `README.md` line 405 ("has no Codex counterpart").
**Reuse:** existing Codex install path (`.agents/skills/` links), the `$` command form, task mode as the fallback.
**Likely cause / gap:** unverified what Codex (CLI and desktop app) offers: subagents, parallel subagents, model
choice per subagent, starting another session. The coordinator's design from P1 must be checked against these
and the fallback chosen per capability; needs a probe first, like `docs/claude-print-mode.md` did for Claude.
**Difficulty:** high (capabilities unknown; outcome depends on a probe) · **Size:** 2–3 tasks (probe +
adaptation of the skill/layout + rehearsal doc).
**Depends on:** P1 (same new skill and the same `layout.md` sections).

### P3. Docs: how to launch an unattended run from the console and from the desktop apps
**User's words:** "Хочу чтобы была возможность запуска этого как из консоли так и из десктопных клод кода и чат ГПТ кодекс."
**Clarifications:** one place that says: coordinator skill in Claude Code CLI / desktop and Codex CLI / desktop;
the Python driver as an optional tool for long unattended Claude runs with hard rails.
**Where:** `README.md` (workflow, Requirements line 330, Limitations lines 397–405) · `docs/wave-driver.md`
("What it does", "Limits": when to use the driver instead of the skill) · `examples/03-autonomous-night-run/README.md`.
**Reuse:** existing README structure.
**Likely cause / gap:** the docs describe unattended runs only through the driver.
**Difficulty:** low · **Size:** 1 task.
**Depends on:** P1, P2 (describes both); P4 (same files: `README.md`, `docs/wave-driver.md`).

### P4. Remove the Python overnight driver
**User's words:** "питон драйвер удалить за ненадобностью." (answer in the triage discussion, 2026-11-24)
**Clarifications:** the coordinator skill (P1) replaces it fully; no Python remains for unattended runs.
`skills/wave-plan/scripts/status_check.py` is not part of the driver and stays.
**Where:** `scripts/wave_driver.py`, `scripts/wavedriver/*.py`, `scripts/tests/*.py` (delete) ·
`docs/wave-driver.md`, `docs/claude-print-mode.md`, `docs/rehearsals/print-mode-chain.md`,
`print-mode-fixture-chain.md`, `print-mode-multiwave.md` (delete or move to an archive note) ·
`docs/rehearsals/end-to-end-autonomous.md`, `end-to-end-manual.md`, `examples/README.md`,
`examples/03-autonomous-night-run/README.md`, `README.md` (driver sections, Requirements line 330, Limitations
line 405) · `skills/wave-plan/layout.md:505` ("a driver's summary") · `.github/workflows/release.yml:41`
(`unittest discover -s scripts/tests`) and `:48` (`scripts` in the release paths) · `skills/wave-plan/CHANGELOG.md`
(new entry; old entries stay).
**Likely cause / gap:** the driver was the only unattended path; once P1 exists it is redundant.
**Difficulty:** medium (many references, CI change; the removal must leave no dangling link) · **Size:** 2–3 tasks.
**Depends on:** P1 (removal only once the coordinator replaces it; P1 reads `decide.py` as its source) · P3 (same
files: `README.md`, `docs/wave-driver.md`).

## Parts

| Part | Problems | Points | Plan slug | Plan when | Command |
|---|---|---|---|---|---|
| 1 | P1 | 5 | `desktop-coordinator-p1` | now | `/wave-plan plans/2026-11-24-desktop-coordinator/index.md part 1`<br>`$wave-plan plans/2026-11-24-desktop-coordinator/index.md part 1` |
| 2 | P2, P3, P4 | 8 | `desktop-coordinator-p2` | after part 1 merged | `/wave-plan plans/2026-11-24-desktop-coordinator/index.md part 2`<br>`$wave-plan plans/2026-11-24-desktop-coordinator/index.md part 2` |

Part status is not written here: a part is planned when its plan folder `plan-<K>/` exists; it is done when every
feature in that plan is `✅ merged`.

P1 is `high` of size 4+ and goes alone. P2 changes the skill P1 creates, so part 2 is planned against code that
already contains part 1; P3 describes both and joins part 2; P4 removes the driver only after part 1 replaces it
and shares the docs with P3.

## Assumptions
- The Python driver is removed (P4, user's decision) and not extended to Codex. What it had that a session lacks
  is covered by the coordinator's design: fresh context per step through subagents, resume from git after a
  closed window or usage limit. Rails (deadline, max steps) become rules of the skill, soft but recorded.
- The skill's final name is chosen by wave-plan (working name `wave-auto`); it is the fifth skill in installers,
  plugin description and README.
- The coordinator is started on a high-tier model, because it runs triage itself and must be able to start
  high-tier subagents for planning.
- Feature approval, questions and the no-subagent fallback: as in P1 Clarifications (user's answers).

## Open questions
- (none)
