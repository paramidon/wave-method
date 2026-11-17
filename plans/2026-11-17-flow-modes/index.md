# Flow modes — index

- Index: `plans/2026-11-17-flow-modes/index.md` · created 2026-11-17 · base: f5768a5 · triaged 2026-11-17 15:27 – (running)

## Problems

| P | Summary | Cluster | Difficulty | Size | Depends on | Part |
|---|---|---|---|---|---|---|
| P1 | Flow field (manual/autonomous), per-feature override, decision table in layout.md | skill-rules | | | | |
| P2 | Integration target so autonomous merges never reach the real main; refuse otherwise | skill-rules | | | | |
| P3 | wave-run autonomous behaviour (auto-approval, each interactive point) in autonomous.md | skill-rules | | | | |
| P4 | wave-plan / wave-triage proceed on recorded assumptions instead of questions | skill-rules | | | | |
| P5 | Final reports show the active flow and what was auto-merged and why | skill-rules | | | | |
| P6 | Cross-platform overnight driver in `scripts/` with rails, lock, log, morning report | driver-docs | | | | |
| P7 | Verify for real how `claude -p` runs skills; design the driver prompts around it | driver-docs | | | | |
| P8 | README, autonomous example, status_check.py new fields, CHANGELOG Unreleased | driver-docs | | | | |
| P9 | End-to-end test on a throwaway repo: manual run, autonomous run with red/blocked | driver-docs | | | | |
| P10 | "Plan after part K is merged" checks the integration target in autonomous flow | skill-rules | | | | |
| P11 | Morning report shows each feature's review block (essence, how to test) | driver-docs | | | | |

## Clusters

| Cluster | Area | Problems |
|---|---|---|
| skill-rules | skill texts: `wave-plan/layout.md`, `templates.md`, `wave-run/*`, `wave-plan/SKILL.md`, `wave-triage/SKILL.md` | P1, P2, P3, P4, P5, P10 |
| driver-docs | `scripts/` driver, `status_check.py`, README, `examples/`, CHANGELOG, end-to-end test | P6, P7, P8, P9, P11 |

## Source list (verbatim)

The user's task text, split into numbered problems. Shared context of the whole list:

> Add a second execution flow, "autonomous", next to the existing one, and let me choose:
> - `manual` (default, today's behavior, must stay byte-for-byte equivalent in behavior): wave-run makes each finished feature `👀 review` and waits for my approval; I start the next wave and the next plan part myself.
> - `autonomous`: a whole plan, or a chain of dependent plan parts, runs unattended (e.g. overnight, 100+ tasks) from the task list to merged features plus a morning report, without ever asking me a question.
>
> Today unattended runs stop at: the per-feature merge approval, the interactive questions of wave-run (open-problems, leftover-branches, design-conflict, red-before-wave, out-of-scope edits), the clarifying questions of triage/plan, `feature-unmerged` (a wave that `Depends on: F<k> merged`), and "plan after part K is merged" (a later part must be planned against code that already contains part K). Each of these is a dead stop at night. I want to keep all of them in manual flow and give autonomous flow a defined, safe answer for each.
>
> Hard constraints 1–2: Manual flow unchanged. A plan without the new field behaves exactly as today. Keep every existing hard rule: never push; nothing committed directly on the main branch; the tier gate is never waivable; a feature is never merged while any task is ⬜/🔄/⚠️/❌; coordinator never works in the main checkout. Autonomous flow only changes WHO gives the feature approval (the skill, under explicit conditions), never the merge mechanics of `wave-run/merge.md`.

- **P1.** "The flow is my choice per plan, switchable between waves, and overridable per feature (a risky feature can force manual review inside an autonomous plan; it then stays `👀 review` and its dependants stay blocked)." · "Single source of truth: put the flow field, its semantics and the decision table in `wave-plan/layout.md`; skills point to it, never repeat it." · "Decision table (starting proposal — challenge it). For every point where a skill asks me or waits for me, define the manual behavior (existing) and the autonomous behavior. […] Also decide: per-feature review override syntax, how flow is switched between waves, and what happens if flow changes while a wave is 🔄."
- **P2.** "Autonomous merges must never land on my real main unnoticed. Design an integration target (an integration branch the plan merges into instead of main, and/or a dedicated throwaway clone where the plan runs) so that in the morning I review one diff and merge it myself. Propose the mechanism with trade-offs (the main-readiness rules in layout.md assume the main checkout is on `<main>`; a `Main:` override in the plan README vs. a night clone). Autonomous flow must refuse to start (clear stop code) if it cannot guarantee this."
- **P3.** "Autonomous auto-approval of a feature requires ALL of: every task ✅ or ➖, full feature check green after merging main in, no open problem entry against it, tier gate clean, not marked manual-review. Anything else leaves it `👀 review` / ⚠️ with a problem entry; the run continues with whatever does not depend on it." · "Do not bloat the manual path: put wave-run's autonomous specifics in a new `wave-run/autonomous.md`, read only when the plan's flow is autonomous (same pattern as `merge.md`, `report.md`, `task-mode.md`)." · Starting proposal: "feature approval → auto-approve under constraint 3, merge into the integration target; open-problems → proceed, entries stay open; leftover-branches → never reuse silently; stop this wave with a machine-readable stop line, the driver moves to other independent work; red-before-wave, design-conflict → feature ⚠️ blocked + problem entry; do not guess; skip dependants; out-of-scope edit by a task → task ⚠️, do not merge that task, log it; red-after-merge → unchanged (2 attempts, then ⚠️); tier-missing / tier-mismatch → unchanged hard stops; feature-unmerged → resolved by auto-merge into the integration target; if the needed feature is blocked, the dependent wave waits"
- **P4.** "wave-plan / wave-triage clarifying questions → proceed on stated assumptions, recorded in README "assumptions" and the triage index"
- **P5.** "Everything in the repo stays English. The final reports still follow `report.md`; the report must show the active flow, and in autonomous flow list what was auto-merged and why."
- **P6.** "Add a cross-platform driver (Python 3.9+, stdlib only — status_check.py already needs Python, and I use Windows too) in `scripts/` plus a short doc. It must: read plan state (reuse the status check), pick the next action: triage-follow-up plan part, wave-run for the next wave, or stop; run each step as a fresh headless Claude Code session with the right model per tier (plan/triage = high/Opus, run = medium/Sonnet; model names configurable, never hardcoded beyond defaults); parse the first line `Stop <code>: … — next: …` of each report to decide: continue, skip to independent work, or halt; hard rails: max iterations, max consecutive failures, optional wall-clock deadline, stop on usage/rate-limit errors (do not spin), a lock so two drivers never run, a log file; at the end write a morning report file for me (what merged into the integration target, what is `👀 review`, blocked features and why, open problems, stops, cost-relevant counters) and print the exact commands to review and merge; never push; never touch the main branch directly" · "\"plan after part K is merged\" → the driver plans part K+1 only after part K is merged into the integration target"
- **P7.** "IMPORTANT: verify against current Claude Code docs whether skills / slash commands (`/wave-run ...`) work with `claude -p`; as far as I remember user-invoked skills may not, in which case the prompt must describe the task in words and name the skill (\"Use the wave-run skill to run wave N of plans/<folder>\"). Test it for real and design around the result."
- **P8.** "Update README, `examples/` (add an autonomous example), status_check.py (understand the new fields), and add an `Unreleased` line to wave-plan/CHANGELOG.md. Do not bump versions or create tags (the release workflow owns that)."
- **P9.** "Phase 3 — test on a throwaway repo (use examples/01-greenfield-todo-cli or a scratch clone), never on my real projects: one run in manual flow (must behave as before), one in autonomous flow including a forced failure (a red task) and a feature that must stay blocked. Report what actually happened, including anything you could not verify."
- **P10.** "учти что  Иногда планирование волн заблокировано нереализованными фичами, система так и говорит - запускай планирование волны после выполненного и реализованного плана N. Это уже учитано в новом плане который я тебе скинул ?" (agreed refinement: in autonomous flow "plan after part K is merged" checks the integration target, not `<main>`; part K+1's tracking branch is created from and merged into the integration target; if a feature of part K stays 👀 review or ⚠️, part K+1 is not planned, the driver moves on and the morning report names the waiting part and the feature it waits for)
- **P11.** "также при автоматической работе я хочу чтобы после завершения было записано в отчёте - конкретная реализованая фичи - как она выглядит, как её тестировать (без воды аля как запустить проект)." (agreed refinement: the morning report shows, for every feature merged into the integration target and every feature left 👀 review, its review block of `layout.md` "Feature review")

Process notes from the user: "Phase 1 — read everything first […] write me a short design […] and STOP for my approval." · "Phase 2 — implement on a new branch `feat/flow-modes`. Keep skill text tight; follow the existing style." · "Commit in logical steps. Never push."
