# Flow switch target — index

- Index: `plans/2026-11-27-flow-switch-target/index.md` · created 2026-11-27 · base: f7e2065 · triaged 2026-11-27 23:34 – …

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
