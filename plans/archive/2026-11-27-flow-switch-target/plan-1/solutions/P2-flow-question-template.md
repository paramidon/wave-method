# P2. A fixed, plain flow question in wave-auto

User problem: the `ask-flow` question of `wave-auto` has no template; the model wrote it in its own words, with step
names, `integration/…` instead of the branch and no word on why the plan is manual or what the user does afterwards ·
feature F2

## Cause

- `skills/wave-auto/SKILL.md:137` (start phase 4) says only "ask whether to switch that plan to autonomous flow": no
  wording, unlike every other message of the skill (progress lines, `Resume:`, stops, final report).
- `skills/wave-auto/SKILL.md:40` forbids the coordinator to read plan files, so it cannot read a README to name the
  integration branch; `skills/wave-auto/navigator.md:84` and `:129` give the `ask-flow` line only the plan folder.
- With the hard rule "no explanation of its own" (`skills/wave-auto/SKILL.md:51`) the model wrote a terse question.

## Approach

1. The navigator, which reads READMEs, supplies the branch: every entry of the `ask-flow` line carries the integration
   branch the plan will merge into once the flow form switches it. The rule is the one of `wave-plan/layout.md`,
   "Names", after feature F1: `integration/<topic>` for a plan of an index part, else `integration/<slug>`. The
   coordinator keeps reading no plan file.
2. The coordinator asks a fixed template, written in English in the skill and translated into the user's language,
   like the other fixed messages. It names the plans and the branch, says why the plans are manual, what changes when
   they are switched, and what the user does with the integration branch afterwards. Step names are forbidden.

Not chosen: letting the coordinator read the README `Flow:` / `Index:` lines. It would break the hard rule that keeps
the coordinator's context small and its behaviour independent of plan contents.

## Navigator return line

The `ask-flow` action (feature F2 also lists several plans in it, `solutions/P3-ask-all-manual-plans.md`):

```
next: ask-flow <plan folder> <branch>; <plan folder> <branch>; …
```

Example: `next: ask-flow plans/2026-11-22-cozy-cooking-slice/plan-3 integration/cozy-cooking-slice`.

`<branch>` (navigator, "Plan rules", rule 2): `integration/<topic>` when the README header has a line
`- Index: plans/<date>-<topic>/index.md part <K>` (the path in backticks or not; `<topic>` is the index folder name
without its `YYYY-MM-DD-` prefix), else `integration/<slug>` with `<slug>` from the README's `slug: ` field. A manual
README has no `target:` (`- Flow: manual` carries no field), so no other source exists.

## Flow question (coordinator)

A new subsection `### Flow question` of `skills/wave-auto/SKILL.md`, right after "Start phase" and before "Loop",
with exactly this text:

````
### Flow question

Asked in start phase 4, once, in the user's language: translate the template below, keep plan folders, branch names
and commands verbatim, and add or leave out nothing. One `- <plan folder> → <branch>` line per entry of the navigator
line, in its order. `<main branch>` is the one resolved in start phase 1. Every entry of an index start names the same
branch; if entries name different branches, write the paragraph once per branch, with its plans, in the same message.

```
These plans are in manual flow:
- <plan folder> → <branch>
They were planned without `flow autonomous`, so every ready feature waits for your review and is merged into
<main branch> only after you approve it. Switched to autonomous flow, this run approves a ready feature itself when
its tasks are done, its check is green and no problem concerns it, and merges it into <branch>, never into
<main branch>. Afterwards you review <branch> as one diff (`git diff <main branch>...<branch>`) and merge it into
<main branch> yourself (`git merge --no-ff <branch>` in the main checkout).
Switch all of them to autonomous flow? yes — switch them all · no — keep them manual: this run skips them and goes on
with the rest; one plan can be switched later with `/wave-run <plan folder> flow autonomous` · `$wave-run <plan folder> flow autonomous`.
```

Never write a step name (`flow`, `ask-flow`, `navigate`), a placeholder such as `integration/…` or a reason of your
own, and write no sentence before or after the question.
````

In the hard rule of `skills/wave-auto/SKILL.md:51`–`52`, replace `its questions,` with
`its questions (the flow question in the words of "Flow question"),`.

## Limits

- The template is the only text of that message; the coordinator still writes its progress lines before it.
- The coordinator never reads the README to check `<branch>`: the navigator's value is used as given.
- A plan of an index part switched before feature F1 (target `integration/<topic>-p<K>`) is not in manual flow, so it
  is never asked about (index assumption: none exists).

## Acceptance tests

1. Navigator, plan start `plans/2026-11-20-foo` (raw plan, slug `foo`, README with no `Flow:` line, tracking branch
   `plan/foo` exists) → output is exactly `next: ask-flow plans/2026-11-20-foo integration/foo`.
2. Navigator, index start `plans/2026-11-22-cozy-cooking-slice/index.md`, part 3 planned in manual flow (README header
   `` - Index: `plans/2026-11-22-cozy-cooking-slice/index.md` part 3 ``, slug `cozy-cooking-slice-p3`) → its entry is
   `plans/2026-11-22-cozy-cooking-slice/plan-3 integration/cozy-cooking-slice`, never `…-p3`.
3. Coordinator, given entry 2 and `<main branch>` = `main`, user writing Russian → one message in Russian: the plan
   line with `integration/cozy-cooking-slice`, the reason (planned without `flow autonomous`), the auto-approval
   sentence, `git diff main...integration/cozy-cooking-slice` and `git merge --no-ff integration/cozy-cooking-slice`,
   the yes/no line with the `/wave-run … flow autonomous` command in both forms; no `ask-flow`, no "step", no
   `integration/…`.
4. Checks: `git grep -n "ask-flow <plan folder> <branch>" -- skills` lists `skills/wave-auto/navigator.md` and
   `skills/wave-auto/SKILL.md`; `git grep -n "### Flow question" -- skills/wave-auto/SKILL.md` → one line;
   `git diff --check` → no output.
