# Flow switch target — index

- Index: `plans/2026-11-27-flow-switch-target/index.md` · created 2026-11-27 · base: f7e2065 · triaged 2026-11-27 23:34 – 2026-11-27 23:37

## Source

The user ran `/wave-auto` on `plans/2026-11-22-cozy-cooking-slice/index.md` in another repository; the coordinator
asked whether to switch `plan-3` (planned earlier in manual flow) to autonomous flow. The user's words, verbatim:

> почему система выдала именно такой ответ? гдето недочёт? почему автоматический режим не включился? я думал этот
> скил спецмиально предназначен для автоматического режима? почему слив происходит в integration? как конкретно
> происходит мерж? Всех реализованных фичей в одну integration ветку или как ?

The analysis in the same session found the problems below; the user then asked: "составляй план".

1. Switching a plan of an index part to autonomous flow (`/wave-run <plan folder> flow autonomous`) names the
   integration branch after the plan slug (`integration/cozy-cooking-slice-p3`), not after the index topic
   (`integration/cozy-cooking-slice`), so the part no longer shares the index's one integration branch.
2. The `ask-flow` question of `wave-auto` has no template: the model wrote it in its own words, with internal step
   names ("шаг `flow`"), `integration/…` instead of the branch name, and no word on why the plan is manual or what
   the user does with the integration branch afterwards.
3. Only the first manual plan of an index is asked about at the start; every later manual plan halts
   `questions-late` and has to be run by hand.

## Problems

One cluster, `wave-auto-flow` (switching an existing manual plan to autonomous flow from `wave-auto`): P1, P2, P3.

### P1. The flow form names an index part's integration branch after the plan slug, not the index topic
**User's words:** item 1 of "Source" (found in the analysis; the user asked to plan it: "составляй план")
**Clarifications:** none asked.
**Where:** `skills/wave-run/autonomous.md:17` (Flow form, step 2: `<name>` is the current `target:`, else `<plan>`)
· `skills/wave-plan/layout.md:229` ("Names", `<name>`) · `skills/wave-plan/layout.md:458` ("Flow": "without it the
target is `integration/<plan>`"; "a plan of an index part … names `integration/<topic>`") · `README.md:227`
("Choosing the flow") · `skills/wave-plan/CHANGELOG.md` (Unreleased line). · **Reuse:** the README header line
`- Index: plans/<date>-<topic>/index.md part <K>` (`skills/wave-plan/templates.md:9`) gives `<topic>`; the navigator
already reads `integration/<topic>` for chained parts (`skills/wave-auto/navigator.md:61`) and `wave-plan` check 3
(`skills/wave-plan/layout.md:701`), so both work once the switched part targets it. Optional guard:
`skills/wave-plan/scripts/status_check.py:63` (`flow()`) could flag an index part whose target is not
`integration/<topic>`.
**Likely cause:** the flow form was written for raw-list plans; the index-part rule of "Planning in autonomous flow"
covers only `wave-plan`, not a later switch.
**Difficulty:** low · **Size:** 1 task (2 with the checker guard), skill text only
**Depends on:** none (P2 depends on it)

### P2. The `ask-flow` question of `wave-auto` needs a fixed, plain template
**User's words:** "почему система выдала именно такой ответ? гдето недочёт? почему автоматический режим не
включился? … почему слив происходит в integration?"; item 2 of "Source"
**Clarifications:** the question is asked in the user's language; the template is written in English in the skill.
**Where:** `skills/wave-auto/SKILL.md:137` (start phase 4: "ask whether to switch that plan to autonomous flow", no
wording) · `skills/wave-auto/SKILL.md:40` (hard rule: the coordinator reads no plan file, so it cannot read the
target) · `skills/wave-auto/SKILL.md:51` (it writes only what the skill names) · `skills/wave-auto/navigator.md:84`
and `:129` (the `ask-flow` line carries only the plan folder) · `skills/wave-plan/layout.md:751` (`navigate` return
line). · **Reuse:** the integration-branch explanation of `README.md` ("The integration branch") and
`skills/wave-plan/layout.md:495` (the user reviews `git diff <main branch>...integration/<name>` and merges it
themselves).
**Likely cause:** the skill fixes the wording of every other message (progress lines, `Resume:`, stops, final report)
but leaves this one free; with the "no explanation of its own" rule the model wrote a terse question with step names.
The coordinator cannot name the branch because it reads no README: the navigator (or the folder-name rule of P1) has
to supply it.
**Difficulty:** medium · **Size:** 1–2 tasks, `wave-auto` skill and the `navigate` contract
**Depends on:** P1 (the branch name the question shows follows P1's rule); P3 (same lines,
`skills/wave-auto/SKILL.md:132`–`141`, and the same `ask-flow` navigator line)

### P3. Every manual plan of an index should be asked about at the start, not only the first
**User's words:** item 3 of "Source" (found in the analysis; the user asked to plan it: "составляй план")
**Clarifications:** one answer covers every listed plan: "yes" switches all of them, "no" switches none (user's
answer, 2026-11-27). A single plan can still be switched later with `/wave-run <plan folder> flow autonomous`.
**Where:** `skills/wave-auto/navigator.md:55`–`69` (Index start, step 3: the first row that yields a `next:` line
ends the reading, so only the first manual plan is reported) · `skills/wave-auto/navigator.md:83` (Plan rules,
rule 2) · `skills/wave-auto/navigator.md:112`–`133` (return grammar) · `skills/wave-auto/SKILL.md:137`–`141` (start
phase 4 and 5), `:160` (dispatch table), `:299` (`questions-late`) · `skills/wave-plan/layout.md:751` and `:758`
(`navigate` and `flow` steps) · `docs/rehearsals/coordinator-cli-flow.md` (rehearsal of the flow question; may need a
case with two manual plans). · **Reuse:** the `flow` step already switches one plan; it runs once per listed plan.
**Likely cause:** the navigator returns one `next:` line by design; `ask-flow` is legal only in the start phase,
which ends with the first `flow` step, so a second manual plan found later can only halt `questions-late`.
**Difficulty:** medium · **Size:** 2–3 tasks, navigator, coordinator, `layout.md` contract
**Depends on:** P2 (same code: `skills/wave-auto/SKILL.md:137`, the `ask-flow` navigator line)

## Parts

| Part | Problems | Points | Plan slug | Plan when | Command |
|---|---|---|---|---|---|
| 1 | P1, P2, P3 | 5 | `flow-switch-target-p1` | now | `/wave-plan plans/2026-11-27-flow-switch-target/index.md part 1`<br>`$wave-plan plans/2026-11-27-flow-switch-target/index.md part 1` |

Part status is not written here: a part is planned when its plan folder `plan-1/` exists; it is done when every
feature in that plan is `✅ merged`.

## Assumptions

- The canonical skill text is under `skills/`; `.claude/skills/` is a local installed copy and is not edited
  (`CONTRIBUTING.md`, item 3).
- A plan of an index part that was already switched to `integration/<slug>` before the fix is not migrated: none is
  known to exist; the user's `plan-3` was not switched yet.
- The `ask-flow` question explains, in two or three plain sentences, why the plan is manual (it was planned without
  `flow autonomous`), the exact integration branch, and that the user reviews and merges that branch into
  `<main branch>` themselves; "no" leaves the plan manual and the run goes on with the other units.
- `README.md` says "all five auto-approval conditions" while `skills/wave-plan/layout.md` "Auto-approval" lists six;
  this drift is out of scope here and is noted for the plan as a possible one-line fix.

## Open questions

- none
