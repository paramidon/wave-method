# P4. Triage and planning never ask in autonomous flow: assumed readings and the flow of planning

User problem: in autonomous flow `wave-triage` and `wave-plan` proceed on stated assumptions, recorded in the index
and README "Assumptions", instead of asking clarifying questions · feature F1

## Cause

- The questions are unconditional: `skills/wave-triage/SKILL.md:65-69` (step 3, ask all questions once),
  `:128-129` (a problem over the budget: ask the user); `skills/wave-plan/SKILL.md:83-84` (step 1, ask all such
  questions once), `:217` (existing branch or folder of a new plan: ask the user).
- Both skills run before a plan README exists, so the README `Flow:` line of part 1 (`skills/wave-plan/layout.md`,
  "Flow") cannot tell them the flow. `layout.md:303` says outright: "`wave-plan` and `wave-triage` do not act on it."

## Approach

- **Flow of planning** — a flow for the two planning skills, taken from (1) the arguments (`flow autonomous` or
  `flow manual` as the first two words), (2) for an index part, the index header line `- Flow: autonomous · target:
  integration/<topic>` that `wave-triage` writes when its own flow is autonomous, (3) otherwise manual. A driver
  (part 3) states it in the command; a user who triaged by hand in autonomous flow does not repeat it per part.
  Why the first two words and not a suffix: `wave-triage` takes a free-text list, where a suffix is ambiguous; one
  position for both skills keeps the driver simple.
- Manual flow of planning = today's text, unchanged: every new sentence is conditioned on "autonomous flow".
- **Assumed readings**: where a question would be asked, a fixed tie-break picks the reading, and the choice is
  written down where the user reads it: the index and README Assumptions, and (through `wave-run` step 7) the
  "Worth a look" line of the feature's review block. Why it is safe to guess: in autonomous flow everything lands on
  the integration branch, which the user reviews before it reaches the main branch; a wrong guess costs one rejected
  feature, not a broken main branch.
- Why not "features built on a guess go under `manual review:`": that would stop every chained part behind the first
  guess, and the night would produce little. The guess is visible in the review block instead; the user can still
  add the feature to `manual review:` with the flow form.
- Cases that cannot be assumed get a stop code instead of a question (an existing branch or folder: `plan-exists`;
  a flow argument that contradicts a re-plan's README: `flow-mismatch`). A problem too big for a part is left out of
  every part with an "Open questions" line, so the other parts are still written.
- The rules live in one new subsection of `layout.md`, "Planning in autonomous flow" (text below; P10 adds its
  "Chained parts" part); the skills point to it.

## Exact text for `skills/wave-plan/layout.md` (task A)

### New subsection, appended at the end of "## Flow" (after the "### Decision table" table, before "## Archive")

`<…>` are the layout's own placeholders and stay as written. The block "Chained parts" at its end is given in
`solutions/P10-chained-parts.md`, section "Chained parts (text)"; insert it where this text says so.

````markdown
### Planning in autonomous flow

`wave-triage` and `wave-plan` run before a plan README exists, so they take their **flow of planning** from, in this
order:

1. the arguments: `flow autonomous` or `flow manual` as their first two words, for example
   `/wave-plan flow autonomous plans/<date>-<topic>/index.md part <K>` ·
   `$wave-plan flow autonomous plans/<date>-<topic>/index.md part <K>`, or
   `/wave-triage flow autonomous <list>` · `$wave-triage flow autonomous <list>`;
2. for `wave-plan` of an index part: the index header line `- Flow: autonomous · target: integration/<topic>`, which
   `wave-triage` writes when its flow of planning is autonomous;
3. otherwise manual: both skills behave exactly as if this subsection did not exist.

A re-plan's flow is its README `Flow:` line; a `flow` argument that differs from it stops `flow-mismatch` (the flow
form of `wave-run` changes the line).

In autonomous flow of planning:

- `wave-plan` writes `- Flow: autonomous · target: integration/<name>` into the README, where `<name>` is the index
  `<topic>` for an index part and the plan slug for a raw list.
- Neither skill asks the user a question. Each point where it would ask has the answer of the table below. A
  situation the table does not cover stops with the closest code; its `next:` says what the user must decide.
- A stop is the first line of the answer after `Started:`: `Stop <code>: <one line> — next: <command or action>`.

| Point | Where | Manual flow | Autonomous flow |
|---|---|---|---|
| a problem can be read two ways that lead to different work | `wave-triage` step 3; `wave-plan` step 1, also for an index's "Open questions" | ask all such questions once | "Assumed readings"; no question |
| one problem alone exceeds the part budget | `wave-triage` step 5 | tell the user and ask | the problem goes into no part; "Open questions" gets `P<n>: needs a research step first (not planned, autonomous flow)`; the other parts are written |
| the tracking branch or folder of a new plan already exists | `wave-plan` step 9 | ask the user | stop `plan-exists`; nothing written |
| a re-plan's `flow` argument differs from its README `Flow:` line | `wave-plan` re-planning | — | stop `flow-mismatch`; nothing written |

#### Assumed readings

Of two or more readings, take the first rule that decides:

1. the reading closer to the user's own words (the verbatim list and the clarifications already given);
2. the reading that changes less existing behaviour (it adds rather than replaces, and leaves defaults as they are);
3. the reading with less work.

Record every choice in the Assumptions list of the file being written: the index (with the problem) or the README
(with the feature built on it):

```
- Assumed (autonomous, not asked) · P3: <the question> → <the chosen reading>; not chosen: <the other reading>
```

`wave-plan` copies the assumed lines of its part's problems from the index into the README, with the feature ID in
place of the P. `wave-run` copies a feature's assumed lines into "Worth a look" of its review brief
(`wave-run/SKILL.md` step 7), so the user meets them in the review block.

<the "Chained parts" block of solutions/P10-chained-parts.md goes here>
````

### Flow bullets of "## Flow"

- "`wave-plan` writes the line only when the user asks for autonomous flow while planning." →
  "`wave-plan` writes the line only when its flow of planning is autonomous (\"Planning in autonomous flow\")."
  (the rest of that bullet stays).
- "`wave-run` reads the flow from the README on the tracking branch in its step 1 and keeps it for the whole run,
  including the resume of a task-mode wait. `wave-plan` and `wave-triage` do not act on it." → keep the first
  sentence; the second becomes "`wave-plan` and `wave-triage` follow their flow of planning instead (\"Planning in
  autonomous flow\")."

## Exact text for `skills/wave-plan/templates.md` (task A)

- README template, the `- Flow:` line → `- Flow: (omit for manual flow; `autonomous · target: integration/<name>`
  when the flow of planning is autonomous, `<name>` = the index topic or the plan slug; `manual review: <F-IDs>`
  only when the user asks: `layout.md`, "Flow", "Planning in autonomous flow")`.
- README template, "## Assumptions": after `- …` add the line
  `- Assumed (autonomous, not asked) · F<k>: <question> → <chosen reading>; not chosen: <other reading> (autonomous flow only: `layout.md`, "Assumed readings")`.

## Edits of `skills/wave-triage/SKILL.md` (task C)

Line numbers are of `main` at fc815cd; find each place by its text.

1. New section after "## Pipeline" (before "## What triage does and does not do"):

   ```markdown
   ## Flow of planning
   `flow autonomous` or `flow manual` as the first two words of the arguments sets the flow of planning
   (`layout.md`, "Planning in autonomous flow"); without them it is manual and every step below applies as written.
   In autonomous flow write `- Flow: autonomous · target: integration/<topic>` into the index header, right after the
   `- Index:` line, and never ask the user: each question of the steps below gets the answer of that subsection.
   ```

2. Step 3 (l.65-69), append to its paragraph: "Autonomous flow: ask nothing; choose by \"Assumed readings\" of
   `layout.md` and record each choice as an `Assumed (autonomous, not asked) · P<n>: …` line under "Assumptions";
   "Open questions" stays `none` unless step 5 adds a line."
3. Step 5, last paragraph (l.127-129), append: "Autonomous flow: put it into no part and add the \"Open questions\"
   line of `layout.md`, \"Planning in autonomous flow\"."
4. Step 6, both index templates: after the `- Index: …` header line add
   `- Flow: autonomous · target: integration/<topic> (autonomous flow of planning only; omit otherwise)`.
5. Step 7, first bullet: "Every problem is in exactly one part; …" → "Every problem is in exactly one part (in
   autonomous flow, except a problem left out by step 5 with its \"Open questions\" line); every part is within budget."
6. Step 8, the answer list: after "assumptions and anything you were unsure about;" add the item
   "- autonomous flow: every `Assumed (autonomous, not asked)` line first, then the stops, if any;". The merge of the
   index into `<main branch>` stays as it is in both flows.

## Edits of `skills/wave-plan/SKILL.md` for P4 (task B)

P10 adds more edits to the same file (`solutions/P10-chained-parts.md`, "Edits of `skills/wave-plan/SKILL.md`").

1. "## Input": new first bullet, before "- **A part of an index**":

   ```markdown
   - **Flow of planning** (`layout.md`, "Planning in autonomous flow"): `flow autonomous` or `flow manual` as the first
     two words of the arguments, else the index header's `Flow:` line for an index part, else manual. Read it first and
     keep it for the run. Manual: every step below as written. Autonomous: the answers of that subsection replace every
     question below; never ask the user. A stop is the first line after `Started:`:
     `Stop <code>: <one line> — next: <command or action>`.
   ```

2. Re-planning paragraph (l.60-70), after its first sentence add: "Its flow is the README `Flow:` line; a `flow`
   argument that differs stops `flow-mismatch` (`layout.md`, \"Planning in autonomous flow\")."
3. Step 1, second bullet (l.83-84), append: "Autonomous flow: no question; choose by \"Assumed readings\" (`layout.md`)
   and record each choice in README \"Assumptions\"; the index's \"Open questions\" of this part are handled the same
   way. Copy the index's `Assumed (autonomous, not asked)` lines of this part's problems into README \"Assumptions\",
   with the feature ID in place of the P."
4. Step 9, item 1 (l.217): "If the branch or the folder already exists for a new plan, ask the user." → "If the branch
   or the folder already exists for a new plan, ask the user (autonomous flow: stop `plan-exists`, nothing written)."
5. The answer paragraph (l.229-236), after "assumptions, remaining questions," add: "(autonomous flow: every
   `Assumed (autonomous, not asked)` line, and no remaining questions)".

## Edit of `skills/wave-run/SKILL.md` for P4 (task D)

Step 7, item 3 (l.297-302), append to its last sentence: "In \"Worth a look\" also copy every README \"Assumptions\"
line `Assumed (autonomous, not asked) · F<k>: …` of this feature (`layout.md`, \"Assumed readings\")." Manual plans
have no such lines, so manual flow is unchanged.

## Invariants and limits

- Manual flow of planning: no sentence of `wave-triage/SKILL.md` or `wave-plan/SKILL.md` that applies to it is
  deleted or reworded except the two Flow bullets of `layout.md` and the template lines above.
- Autonomous flow of planning never asks; every guess is a written `Assumed` line; every non-guessable case is a
  stop with a code from the table (or P10's).
- `wave-triage` in autonomous flow still merges the index into `<main branch>` (the main checkout, "Main readiness";
  not ready → it gives the merge command, as today). It writes no code and runs before any night.

## Acceptance tests

Walkthroughs, checked by reading the changed texts.

1. **Manual unchanged:** `/wave-triage <list>` with an ambiguous problem → the text still says to ask once, grouped by
   cluster; `/wave-plan <index> part 1` on an index without a `Flow:` line → step 1 asks, step 9 asks for an existing
   branch; the README gets no `Flow:` line.
2. **Triage assumes:** `/wave-triage flow autonomous <list>` where P3 can mean "rename the option" or "add a second
   option" → no question; the index header has `- Flow: autonomous · target: integration/<topic>`; "Assumptions" has
   `- Assumed (autonomous, not asked) · P3: rename or add? → add a second option; not chosen: rename` (rule 2);
   "Open questions" is `none`.
3. **Plan inherits:** `/wave-plan <that index> part 1` (no argument) → autonomous from the index line; README has the
   `Flow:` line with `target: integration/<topic>` and the line `Assumed … · F1: …`; no question.
4. **Brief shows it:** after the wave, `reviews/F1-….md` "Worth a look" holds the assumed line.
5. **Cannot assume:** the branch `plan/<slug>` exists → `Stop plan-exists: …`; a re-plan of a manual plan called with
   `flow autonomous` → `Stop flow-mismatch: …`; nothing written in either case.
6. **Too big:** a problem over the budget in autonomous triage → in no part; "Open questions" has its line; the
   other parts have commands.
