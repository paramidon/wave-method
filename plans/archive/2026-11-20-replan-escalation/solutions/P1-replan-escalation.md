# P1. Escalate repeated re-plans of one feature
User problem: an executor that meets a plan error logs it and asks for `/wave-plan`; the planner re-plans, the next
executor meets another error of the same feature, and the cycle repeats with nothing that counts it · feature F1

**Cause:** nothing in the plan records which features a re-plan fixed. `wave-plan` writes a free-text line per
re-plan (`skills/wave-plan/SKILL.md:81-83`, `skills/wave-plan/templates.md:10`); the fix loop of `wave-run` caps
attempts per task (`skills/wave-run/SKILL.md:122-129`), but nothing caps re-plans per feature. The archived plan
`plans/archive/2026-11-17-flow-modes/plan-4/README.md` shows the effect: feature F2 was re-planned six times, each
time with new medium tasks planned by reading alone.

**Approach:** count re-plans per feature in the README header, which every skill already reads. Each re-plan
sub-item of `Re-plans:` ends with machine-readable parts: `· fixes:` names the features it planned new tasks for
from entries found in a wave, `· escalated:` and `· override:` record what the rules below demanded. The second
re-plan of a feature is escalated (assumption verified by running code, evidence recorded, every new task `high`,
manual review in autonomous flow); the third is held until the user gives a direction with
`/wave-plan <plan folder> override F<k>: <direction>`. `status_check.py` verifies the record, so a planner that skips
the escalation fails the status check it must pass before committing. `wave-run` and `wave-status` show the count.

Why not count per problem entry (lineage of `→ task Y`): an error often shifts inside a feature (the fix works, a
later task of the same feature breaks), and lineage misses that. Why entries from the user's review do not count:
the user is already in the loop there (decided with the user on 2026-11-20). Why not a column in "Features": it
would change every README, the status-check table parser, `wave-status` and the examples; the header item is
already free-form and read by all skills.

**Limits:** a sub-item written before this rule has no parts and names no feature, so old plans count from zero.
Nothing overrides the limit except the user's command; autonomous flow and the driver never re-plan past it. The
driver (`scripts/wave_driver.py`) never re-plans, so it needs no change.

## Edits

Apply each edit exactly as written; quoted or fenced text is the new text, verbatim. Markdown rules of
`skills/wave-plan/layout.md` apply (blank lines around tables, lists and fenced blocks; one physical line per table
row with as many cells as its header).

### Edit A — `skills/wave-plan/layout.md`

A1. Insert this section between the end of "## Problem log" and "## Markdown rules":

````markdown
## Re-plan escalation

A feature whose fixes keep failing must not cycle between `wave-run` and `wave-plan` without limit. The count lives in
the README header, which every skill reads.

- **Record.** Every re-plan adds one sub-item to the README `Re-plans:` item (`wave-plan/templates.md`). Its text ends
  with these parts, in this order, each only when it has content:
  - `· fixes: F<k> (I<n>, …), …` — every feature for which this re-plan planned new tasks from open entries found in a
    wave (an entry whose header starts `[I<n> · wave`), each with those entries. Entries from the user's review
    (`[I<n> · review / …]`) do not count; a feature with only such entries is not listed;
  - `· escalated: F<k>, …` — the features of `fixes:` at round 2 or later;
  - `· override: F<k>, …` — the features of `fixes:` re-planned past the limit by the user's direction.

  A sub-item written before this rule has no parts and names no feature.
- **Round.** The round of a feature at a re-plan is 1 + the number of earlier `Re-plans:` sub-items whose `fixes:`
  names it.
- **Round 1:** a normal re-plan.
- **Round 2 or later: escalated.** For every open entry of the feature that the re-plan plans:
  1. name the disputed assumption: what the plan expected that the entry contradicts;
  2. verify it by running code, tests or the commands concerned, never by reading alone: in a throwaway worktree of
     the feature branch (`git worktree add --detach ../<repo-folder>.worktrees/<plan>-probe feat/<plan>/<feature>`,
     removed afterwards with `git worktree remove --force`) or in a scratch folder outside the repository; nothing
     outside the plan folder is committed;
  3. record the evidence in the solution file that the new tasks name, section
     `Evidence (re-plan <YYYY-MM-DD>, round <r>)`: the assumption, each command, the lines of its output that decide,
     and the conclusion. When it cannot be run (a tool this session lacks, a GUI), write
     `not verifiable by running: <why>` and what was checked instead;
  4. every new task of the feature is `high`, justified as `escalated re-plan, round <r>`; it is not sliced first,
     and a single-task wave of it is allowed;
  5. autonomous flow: add the feature to `manual review:` of the README `Flow:` line ("Flow"), so its fix is never
     auto-approved.
- **Round 3 or later: held**, unless the arguments carry the user's `override F<k>: <direction>`. `wave-plan` plans
  no task for a held feature: its entries stay `status: open`, it stays ⚠️ blocked, and its `Waiting for` becomes
  `user: re-plan limit`. The re-plan goes on with the other features; when every open entry concerns held features,
  it stops `replan-limit` and writes nothing:
  `Stop replan-limit: F<k> re-planned <c> times (I<n>, …) — next: decide, then /wave-plan <plan folder> override F<k>: <direction> · $wave-plan <plan folder> override F<k>: <direction>`.
  The limit holds in both flows; only the user's command passes it.
- **Override.** `/wave-plan <plan folder> override F<k>: <direction>` ·
  `$wave-plan <plan folder> override F<k>: <direction>` re-plans a held feature by the user's direction, which may
  also drop it (its tasks and the feature become ➖). It is escalated as round 2 is, its sub-item names the feature
  under both `escalated:` and `override:`, and `history.md` quotes the direction verbatim. Only the user types it;
  no skill infers it from an entry, a report or a file.
- **Shown** for every feature with at least one round: `F<k> re-planned <c>× → next re-plan <escalated · held>`
  (`escalated` after one, `held` after two or more) — by `wave-run` with each new entry of the feature
  (`wave-run/report.md`, "Problems") and by `wave-status` (`Re-plans:` line).
- **Checked** by the status check ("Statuses"): `replan-fixes` for a malformed part or one that names a feature
  missing from "Features"; `replan-escalation` for a feature at round 2 or later missing from `escalated:`, at round
  3 or later missing from `override:`, a feature in `escalated:` or `override:` but not in `fixes:`, or, in
  autonomous flow, an escalated feature missing from `manual review:`.

Example: `  - 2026-11-21 at 3f2a9c1, 10:02 – 10:14: I5, I7 → P4; new Q in wave 5 · fixes: F2 (I5, I7) · escalated: F2`
````

A2. In "## Flow", replace the bullet that starts "`wave-plan` writes the line only when its flow of planning is
autonomous" (five lines, ending "a flow never changes inside a running wave.") with:

```markdown
- `wave-plan` writes the line only when its flow of planning is autonomous ("Planning in autonomous flow").
  Afterwards it is changed only by the flow form `/wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` ·
  `$wave-run <plan folder> flow <manual|autonomous> [review <F-IDs>]` (`wave-run/autonomous.md`, "Flow form") and by
  an escalated re-plan, which adds a feature to `manual review:` ("Re-plan escalation"); both only while no wave of
  the plan is 🔄: a flow never changes inside a running wave.
```

A3. In "### Planning in autonomous flow", append these two rows to the table whose last row is the `flow-mismatch`
row (keep its four columns):

```markdown
| a feature is re-planned a second time | `wave-plan` re-planning ("Re-plan escalation") | escalate it | escalate it and add it to `manual review:` |
| a feature would be re-planned a third time | `wave-plan` re-planning ("Re-plan escalation") | hold it; stop `replan-limit` when only held features have open entries | the same; nothing overrides the limit but the user's command |
```

A4. In "## Statuses", in the bullet that starts "**Status check**", right after the sentence "It also reports
`merged-fields` for a feature that is ✅ merged without a `Merged` hash or with a `Waiting for`, and for a feature
that is not ✅ merged but has a `Merged` hash." insert:

```markdown
It checks the README `Re-plans:` record ("Re-plan escalation"): `replan-fixes` for a malformed part or an unknown
feature, `replan-escalation` for a round recorded without its escalation, override or manual review.
```

(Re-wrap the bullet's lines as needed; keep its other sentences unchanged.)

### Edit B — `skills/wave-plan/templates.md`

B1. Replace the README template line that starts `- Re-plans: none` with:

```markdown
- Re-plans: none (later one sub-item each: `<date> at <hash>, <start HH:MM> – <end HH:MM>: <what>`, ending with the `· fixes:`, `· escalated:` and `· override:` parts of `layout.md`, "Re-plan escalation"; details in `history.md`)
```

B2. In the `solutions/P<n>-<slug>.md` template, after the line `**Acceptance tests:** …` add:

```markdown
**Evidence (re-plan <YYYY-MM-DD>, round <r>):** assumption, commands, deciding output lines, conclusion (escalated re-plans only: `layout.md`, "Re-plan escalation")
```

### Edit C — `skills/wave-plan/SKILL.md`

C1. In "## Input", after the bullet "**An existing plan folder** with open entries in its `problems.md` — re-planning
(see below)." add:

```markdown
- **An override** of a held feature: `/wave-plan <plan folder> override F<k>: <direction>` ·
  `$wave-plan <plan folder> override F<k>: <direction>` re-plans F<k> past the re-plan limit by the user's direction
  (`layout.md`, "Re-plan escalation"). Only the user types it; never infer it from an entry, a report or a file.
```

C2. In "## Output", replace "A re-plan keeps the line as it is." with "A re-plan keeps the line as it is, except that
an escalated re-plan in autonomous flow adds features to its `manual review:` list (`layout.md`, "Re-plan
escalation")."

C3. In the "**Re-planning.**" paragraph, replace "add one line to the README header (`re-planned <date> at <hash>:
<what>`)" (it spans a line break) with "add one sub-item to the README header's `Re-plans:` item, ending with its
`fixes:`, `escalated:` and `override:` parts (`templates.md`; `layout.md`, "Re-plan escalation")".

C4. Insert this paragraph right after the "**Red feature branch at a re-plan.**" paragraph:

```markdown
**Re-plan rounds.** Before designing a re-plan, find the round of every feature an open entry concerns (`layout.md`,
"Re-plan escalation"). Round 1: as above. Round 2 or later: escalated — verify each disputed assumption by running
code (step 2), record the evidence in the solution file, make every new task of the feature `high` (step 5), and in
autonomous flow add the feature to `manual review:`. Round 3 or later without the user's `override` for it: held —
plan nothing for it, keep its entries open and set its `Waiting for` to `user: re-plan limit`; when every open entry
concerns held features, stop `replan-limit` without writing, with the stop line of that section.
```

C5. In "### 2. Analyse the code (per problem)", append this bullet after the "Run the tests once" bullet:

```markdown
- Escalated re-plan (`layout.md`, "Re-plan escalation"): for every open entry of the feature, name the disputed
  assumption and verify it by running code, tests or commands in a throwaway worktree or a scratch folder, never by
  reading alone; record the evidence in the solution file the new tasks name.
```

C6. In "### 5. Slice into tasks", append to the "**Complexity**" bullet: "Every new task of a feature in an escalated
re-plan is `high`, justified as `escalated re-plan, round <r>`, without slicing it first (`layout.md`, \"Re-plan
escalation\")." (write the quotes as plain `"`). In "### 6. Waves", replace "A wave with one task is allowed only for
a `high` task that cannot be paired or sliced." with "A wave with one task is allowed only for a `high` task that
cannot be paired or sliced, or a task of an escalated re-plan."

C7. In "### 8. Self-check", replace "No single-task waves except an unpairable `high` task; no solo `low`/`medium`
task anywhere." with "No single-task waves except an unpairable `high` task or a task of an escalated re-plan; no solo
`low`/`medium` task anywhere." and add as the last bullet:

```markdown
- Re-plan rounds: the new `Re-plans:` sub-item names every feature planned from wave entries under `fixes:`, from
  round 2 under `escalated:` and past the limit under `override:`; every escalated feature has an `Evidence` section
  with a command run in this session, only `high` new tasks and, in autonomous flow, a place in `manual review:`; a
  held feature got no task.
```

C8. In "### 9.", in the paragraph that starts "Answer the user briefly:", after "assumptions, remaining questions,"
insert "for a re-plan each feature's round (escalated, or held with its override command in both forms),".

### Edit D — `skills/wave-plan/scripts/status_check.py` and `test_status_check.py`

D1. Add a function `replans(lines, report, feature_ids, flow_name, manual_review)` and call it from `check()` right
after the `flow-review-unknown` loop, with the README lines, `report_readme`, `feature_ids`, the flow name and the
manual-review list that `flow()` returns (keep `flow()` unchanged; use its first return value instead of `_`).

Parsing:

- Header only: stop at the first line that starts with `## `. Find the first line that starts with `- Re-plans:`.
  None → return.
- Sub-items: the lines after it that start with `  - `; a line that starts with four spaces and not `  - ` continues
  the current sub-item (join with one space, after stripping). The first line that matches neither ends the list.
  Keep the 1-based line number of each sub-item's first line.
- Parts: in the joined text, every match of `· (fixes|escalated|override): ([^·]*)`; the value is stripped.
  - `fixes` must fully match `F\d+ \(I\d+(?:, I\d+)*\)(?:, F\d+ \(I\d+(?:, I\d+)*\))*`; its features are
    `re.findall(r"(F\d+) \(", value)`.
  - `escalated` and `override` must fully match `F\d+(?:, F\d+)*`.
  - A value that does not match → `replan-fixes`, detail `<part>: malformed '<value>'`; skip that part.
  - A feature not in `feature_ids` → `replan-fixes`, detail `<part> names missing feature F<k>`.

Rules, over the sub-items in order, with `count[F]` = earlier sub-items whose `fixes:` named F (start 0):

- F in `fixes:` with `count[F] >= 1` and F not in `escalated:` → `replan-escalation`,
  `F<k> re-planned again without escalated`;
- F in `fixes:` with `count[F] >= 2` and F not in `override:` → `replan-escalation`,
  `F<k> re-planned past the limit without override`;
- F in `escalated:` or `override:` but not in `fixes:` → `replan-escalation`, `<part> names F<k> outside fixes`;
- flow autonomous and F in `escalated:` and F not in `manual_review` → `replan-escalation`,
  `escalated F<k> is not under manual review`;
- then add 1 to `count[F]` for every F of this sub-item's `fixes:`.

Every violation is reported on the README at the sub-item's first line, through `report`. Add the rule names to the
module docstring only if the docstring lists rules (it does not today; then leave it).

D2. Add exactly six tests to `StatusCheckTest`, using `run_check` / `assert_rule` and `README.replace("# Test
plan\n", …)` as the flow tests do. The header lines below go right after `# Test plan` and a blank line:

1. `test_replans_escalated` — `- Re-plans:` then `  - 2026-11-01 at abc1234, 10:00 – 10:10: old free text`,
   `  - 2026-11-02 at abc1235, 10:00 – 10:10: I1 → P2 · fixes: F1 (I1)`,
   `  - 2026-11-03 at abc1236, 10:00 – 10:10: I2 → P3 · fixes: F1 (I2) · escalated: F1` → exit 0, empty output.
2. `test_replans_malformed` — one sub-item `… · fixes: F1 I1` → `replan-fixes`.
3. `test_replans_unknown_feature` — one sub-item `… · fixes: F9 (I1)` → `replan-fixes`.
4. `test_replans_not_escalated` — two sub-items, both `· fixes: F1 (I1)` and `· fixes: F1 (I2)`, no `escalated:` →
   `replan-escalation`.
5. `test_replans_no_override` — three sub-items `· fixes: F1 (I1)`, `· fixes: F1 (I2) · escalated: F1`,
   `· fixes: F1 (I3) · escalated: F1` → `replan-escalation` (only the missing override).
6. `test_replans_autonomous_review` — `- Flow: autonomous` and two sub-items `· fixes: F1 (I1)`,
   `· fixes: F1 (I2) · escalated: F1` → `replan-escalation`; with `- Flow: autonomous · manual review: F1` the same
   README is clean (assert both in this test).

After D the status-check suite has 39 tests.

### Edit E — `skills/wave-run/SKILL.md`, `skills/wave-run/report.md`, `skills/wave-run/autonomous.md`

E1. `SKILL.md`, step 8, the bullet that starts "New problems:": append "For every feature a new entry concerns, count
its earlier re-plans: the README `Re-plans:` sub-items whose `fixes:` part names it (`layout.md`, \"Re-plan
escalation\"); the report shows the count." (plain `"` quotes).

E2. `report.md`, wave report template: replace the line `- New: **I<n>** <essence> (<task, feature>)` with
`- New: **I<n>** <essence> (<task, feature>; F<k> re-planned <c>× → next re-plan <escalated · held>)`.
In the section table, the `Problems` row's content cell: append "; a feature re-planned at least once
(`layout.md`, \"Re-plan escalation\") adds its count and what the next re-plan does to each new entry's line, which
otherwise ends after `<task, feature>`". In the next-command table, replace the `open problems` row with:

```markdown
| open problems | `/wave-plan <plan folder>`<br>`$wave-plan <plan folder>`, listing them; a feature held at the re-plan limit: decide, then `/wave-plan <plan folder> override F<k>: <direction>`<br>`$wave-plan <plan folder> override F<k>: <direction>` |
```

E3. `autonomous.md`, "Flow form", step 3: replace "(`review <F-IDs>` replaces the list; `review none` empties it;
without `review` the list stays)" with "(`review <F-IDs>` replaces the list; `review none` empties it; without
`review` the list stays; a feature that the README `Re-plans:` record names under `escalated:` always stays in it,
`layout.md`, \"Re-plan escalation\")".

### Edit F — `skills/wave-status/SKILL.md`

F1. "## What to read", first bullet: after "Also its `Flow:` header line (`layout.md`, \"Flow\")." insert " and its
`Re-plans:` header item (`layout.md`, \"Re-plan escalation\")." — adjust so the sentence reads: "Also its `Flow:`
header line (`layout.md`, "Flow") and its `Re-plans:` header item (`layout.md`, "Re-plan escalation")."

F2. "## Report", bullet list: after the `Last stop:` bullet add:

```markdown
- `Re-plans:` every feature re-planned at least once, counted from the `Re-plans:` sub-items whose `fixes:` names it
  (`layout.md`, "Re-plan escalation"): `F<k> re-planned <c>× → next re-plan <escalated · held>`, separated by `;`.
```

F3. Template: after the line `- Last stop: <the line>` add `- Re-plans: <F<k> re-planned <c>× → next re-plan <escalated · held>; …>`.
In the "Always printed" bullet, replace "`Merged, not recorded`, `Last stop`, `Inconsistencies`, `Leftovers`: only
when they have content." with "`Merged, not recorded`, `Last stop`, `Re-plans`, `Inconsistencies`, `Leftovers`: only
when they have content."

F4. "## Next-command rules", rule 3: append "; when such an entry concerns a feature held at the re-plan limit
(`layout.md`, \"Re-plan escalation\"): decide, then `/wave-plan <plan folder> override F<k>: <direction>` ·
`$wave-plan <plan folder> override F<k>: <direction>`" before the final period (plain `"` quotes).

### Edit G — `README.md` and `skills/wave-plan/CHANGELOG.md`

G1. `README.md`, "### 4. Check progress, fix problems": after the sentence that ends "re-plan
them with `/wave-plan plans/2026-11-02-csv-export`." add: "A feature whose fixes keep failing is escalated at its
second re-plan and held at its third until you give a direction
(`/wave-plan plans/2026-11-02-csv-export override F2: <what to do>`); see
[Re-plan escalation](skills/wave-plan/layout.md#re-plan-escalation)."

G2. `README.md`, "Is this another SDLC?", the bullet that starts "**A closed problem loop.**": append " A feature
re-planned a second time is escalated: the planner verifies its assumption by running code, its fix tasks need a
high-tier model and, in autonomous flow, it waits for your review; a third re-plan waits for your direction."

G3. `README.md`, "## Safety rules": add after the bullet "A task never runs on a model below its tier.":

```markdown
- A feature is re-planned at most twice on its own; a third re-plan needs your `override` direction.
```

G4. `skills/wave-plan/CHANGELOG.md`: at the end of the `- Unreleased — …` item (the last line before the `- v2.12.0`
item), append as new sentences, wrapped like the rest of the item:

```markdown
Re-plan escalation (`layout.md`, "Re-plan escalation"): each README `Re-plans:` sub-item names the features it
fixed from wave entries (`fixes:`); a feature's second re-plan is escalated — its assumption verified by running
code and recorded as evidence, its new tasks `high`, and in autonomous flow its review manual — and a third is held
until the user's `/wave-plan <plan folder> override F<k>: <direction>` (stop `replan-limit`); `wave-run` and
`wave-status` show each feature's count, and `status_check.py` checks the record (`replan-fixes`,
`replan-escalation`).
```

## Acceptance tests

1. `git grep -n "## Re-plan escalation" skills/wave-plan/layout.md` → one line; `git grep -c "Re-plan escalation"
   skills` → at least one match in each of `wave-plan/layout.md`, `wave-plan/SKILL.md`, `wave-plan/templates.md`,
   `wave-run/SKILL.md`, `wave-run/report.md`, `wave-run/autonomous.md`, `wave-status/SKILL.md`.
2. `git grep -n "replan-limit" skills` → lines in `layout.md` (section and table) and `wave-plan/SKILL.md`.
3. `git grep -n "override F<k>: <direction>" skills` → lines in `layout.md`, `wave-plan/SKILL.md`,
   `wave-run/report.md`, `wave-status/SKILL.md`.
4. `python skills/wave-plan/scripts/test_status_check.py` → 39 tests OK; the six `test_replans_*` tests pass.
5. On a copy of `examples/02-bugfix-batch` whose `- Re-plans: none` is replaced by `- Re-plans:` and two sub-items
   `  - 2026-11-21 at abc1234, 10:00 – 10:10: t · fixes: F1 (I1)` and
   `  - 2026-11-22 at abc1235, 10:00 – 10:10: t · fixes: F1 (I2)`, `status_check.py` prints one `replan-escalation`
   line; with `· escalated: F1` added to the second sub-item it prints nothing.
6. `git grep -n "re-plan-escalation\|Re-plan escalation\|override" README.md` → the three README edits;
   `git grep -n "replan-escalation" skills/wave-plan/CHANGELOG.md` → one line.
7. The check command of `waves/w01.md` is green; all three examples pass `status_check.py` unchanged.
