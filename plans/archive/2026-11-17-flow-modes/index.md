# Flow modes — index

- Index: `plans/2026-11-17-flow-modes/index.md` · created 2026-11-17 · base: f5768a5 · triaged 2026-11-17 15:27 – 2026-11-17 15:33

## Problems

| P | Summary | Cluster | Difficulty | Size | Depends on | Part |
|---|---|---|---|---|---|---|
| P1 | Flow field (manual/autonomous), per-feature override, decision table in layout.md | skill-rules | medium | 2–3 tasks | — | 1 |
| P2 | Integration target so autonomous merges never reach the real main; refuse otherwise | skill-rules | high | 2–3 tasks | P1 | 1 |
| P3 | wave-run autonomous behaviour (auto-approval, each interactive point) in autonomous.md | skill-rules | medium | 2–3 tasks | P1, P2 | 1 |
| P4 | wave-plan / wave-triage proceed on recorded assumptions instead of questions | skill-rules | medium | 2–3 tasks | P1 | 2 |
| P5 | Final reports show the active flow and what was auto-merged and why | skill-rules | low | 1 task | P1, P3 | 1 |
| P6 | Cross-platform overnight driver in `scripts/` with rails, lock, log, morning report | driver-docs | high | 4+ tasks | P1, P2, P3, P5, P7, P10, P11 | 3 |
| P7 | Verify for real how `claude -p` runs skills; design the driver prompts around it | driver-docs | low | 1 task | — | 2 |
| P8 | README, autonomous example, status_check.py new fields, CHANGELOG Unreleased | driver-docs | medium | 4+ tasks | P1, P2, P3, P5, P6 | 4 |
| P9 | End-to-end test on a throwaway repo: manual run, autonomous run with red/blocked | driver-docs | high | 2–3 tasks | P6, P7, P8 (and all it exercises) | 4 |
| P10 | "Plan after part K is merged" checks the integration target in autonomous flow | skill-rules | medium | 2–3 tasks | P1, P2 | 2 |
| P11 | Morning report shows each feature's review block (essence, how to test) | driver-docs | medium | 2–3 tasks | P2, P3, P5 | 2 |

## Clusters

| Cluster | Area | Problems |
|---|---|---|
| skill-rules | skill texts: `wave-plan/layout.md`, `templates.md`, `wave-run/*`, `wave-plan/SKILL.md`, `wave-triage/SKILL.md` | P1, P2, P3, P4, P5, P10 |
| driver-docs | `scripts/` driver, `status_check.py`, README, `examples/`, CHANGELOG, end-to-end test | P6, P7, P8, P9, P11 |

## Parts

| Part | Problems | Points | Plan slug | Plan when | Command |
|---|---|---|---|---|---|
| 1 | P1, P2, P3, P5 | 10 | `flow-modes-p1` | now | `/wave-plan plans/2026-11-17-flow-modes/index.md part 1`<br>`$wave-plan plans/2026-11-17-flow-modes/index.md part 1` |
| 2 | P4, P7, P10, P11 | 7 | `flow-modes-p2` | after part 1 merged | `/wave-plan plans/2026-11-17-flow-modes/index.md part 2`<br>`$wave-plan plans/2026-11-17-flow-modes/index.md part 2` |
| 3 | P6 | 5 | `flow-modes-p3` | after part 2 merged | `/wave-plan plans/2026-11-17-flow-modes/index.md part 3`<br>`$wave-plan plans/2026-11-17-flow-modes/index.md part 3` |
| 4 | P8, P9 | 7 | `flow-modes-p4` | after part 3 merged | `/wave-plan plans/2026-11-17-flow-modes/index.md part 4`<br>`$wave-plan plans/2026-11-17-flow-modes/index.md part 4` |

Part status is not written here: a part is planned when its plan folder `plan-<K>/` exists; it is done when every
feature in that plan is `✅ merged`.

Why this split: all eleven problems form one dependency group (29 points, three `high`), so it is cut along the
dependency chain. Part 1 holds the rules every other problem builds on: the flow field and decision table (P1), the
integration target (P2, `high`), wave-run's autonomous behaviour (P3) and the report's flow line (P5, same file as
P3's report changes). Part 2 holds the rules that need part 1's target and table: triage/plan assumptions (P4),
chained parts against the target (P10), review blocks of auto-merged features (P11), and the `claude -p` check (P7,
no dependencies) so its result exists before the driver is designed. Part 3 is the driver alone (P6, `high`, 4+
tasks). Part 4 documents and tests the whole: README, example, status_check.py, CHANGELOG (P8) and the end-to-end
run (P9, `high`), which needs the driver.

## Assumptions

- The driver starts from an existing index or plan folder; the user runs `wave-triage` (answer, 2026-11-17).
- The end-to-end test (P9) is a task of the plan, run by an agent with real `claude -p` sessions in a scratch repo
  (answer, 2026-11-17).
- The user's "Phase 1 design, stop for approval" is served by the pipeline itself: each part's plan is the design,
  reviewed before `/wave-run`. Branches follow `wave-plan/layout.md` ("Names"), not one `feat/flow-modes` branch;
  commits are made by the skills, one per task and merge.
- P7 and P9 need the Claude Code CLI: on 2026-11-17 the user's machine has no `claude` in PATH (only the desktop
  app). It must be installed and signed in before part 2's P7 task runs.
- P2 is sized 2–3 tasks on the expectation that the chosen mechanism keeps `<main>` meaning "the merge target"
  (for example a night clone). If part 1's design needs every `<main>` reinterpreted (4+ tasks), part 1 exceeds the
  budget: `wave-plan` moves P5 to part 2 and says so.
- How `wave-triage` and `wave-plan` learn the flow before a plan exists (P4) is decided by part 2's design (for
  example the driver states it in the prompt).

## Open questions

- none

## Shared constraints (verbatim)

Shared context of the whole list, verbatim; each problem's own words are in its record `triage/P<n>.md`:

> Add a second execution flow, "autonomous", next to the existing one, and let me choose:
> - `manual` (default, today's behavior, must stay byte-for-byte equivalent in behavior): wave-run makes each finished feature `👀 review` and waits for my approval; I start the next wave and the next plan part myself.
> - `autonomous`: a whole plan, or a chain of dependent plan parts, runs unattended (e.g. overnight, 100+ tasks) from the task list to merged features plus a morning report, without ever asking me a question.
>
> Today unattended runs stop at: the per-feature merge approval, the interactive questions of wave-run (open-problems, leftover-branches, design-conflict, red-before-wave, out-of-scope edits), the clarifying questions of triage/plan, `feature-unmerged` (a wave that `Depends on: F<k> merged`), and "plan after part K is merged" (a later part must be planned against code that already contains part K). Each of these is a dead stop at night. I want to keep all of them in manual flow and give autonomous flow a defined, safe answer for each.
>
> Hard constraints 1–2: Manual flow unchanged. A plan without the new field behaves exactly as today. Keep every existing hard rule: never push; nothing committed directly on the main branch; the tier gate is never waivable; a feature is never merged while any task is ⬜/🔄/⚠️/❌; coordinator never works in the main checkout. Autonomous flow only changes WHO gives the feature approval (the skill, under explicit conditions), never the merge mechanics of `wave-run/merge.md`.

Process notes from the user: "Phase 1 — read everything first […] write me a short design […] and STOP for my approval." · "Phase 2 — implement on a new branch `feat/flow-modes`. Keep skill text tight; follow the existing style." · "Commit in logical steps. Never push."
