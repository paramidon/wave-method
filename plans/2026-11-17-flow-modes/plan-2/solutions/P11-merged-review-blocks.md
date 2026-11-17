# P11. Every feature of an autonomous run is shown with its review block

User problem: after an unattended run the report shows, for every feature merged into the integration branch and
every feature left `👀 review`, what it changes and how to test it (no how-to-build) · feature F2

## Cause

- `skills/wave-run/report.md:63-66` and `:95`: the "Auto-merged" section prints only the "Essence" of a merged
  feature; "How to test" and "Worth a look" are printed only for `👀 review` features (`report.md:97`).
- `skills/wave-plan/layout.md`, "Feature review": the review block is defined for a `👀 review` feature only; nothing
  says the brief `reviews/<feature>.md` is kept and readable after the merge, or how a merged feature is shown.
- `skills/wave-status/SKILL.md:39-42`: briefs are read only for `👀 review` features, so in the morning `/wave-status`
  shows nothing about what the night merged.
- The driver of part 3 (P6) needs one defined source for its morning report.

## Approach

- Define a **merged block** next to the review block in `layout.md`, "Feature review": the same lines built from the
  same brief, with the header naming the integration branch and the merge hash, and an `Approved:` line instead of
  `Merge:`. "How to test" keeps all its rules (at most five feature-specific steps, never how to build or start).
- State that a brief is kept after the merge (it already is: nothing deletes it; archiving moves it with the plan).
  In autonomous flow every merge adds one header line to the brief, so any reader can tell a merged feature and how
  it was approved without reading wave files.
- Define **what is shown after an autonomous run** once, in `layout.md` ("Results of an autonomous run"), and let
  every reader use it: the `wave-run` report (this run's merges), `wave-status` (the morning view: everything merged
  into the integration branch that is not yet in the main branch) and the part 3 driver.
- Why not a separate morning-report file written by `wave-run`: it would duplicate the briefs and go stale when a
  later wave or the user changes a status; the briefs and README on the tracking branch are already the record.

## Exact text for `skills/wave-plan/layout.md` (task F)

### "Feature review": new paragraph and block after the bullet "`wave-run` leaves out the `Merge:` line: …"

````markdown
A feature merged into an integration branch (autonomous flow, "Flow") is shown with its **merged block**: the review
block with two lines changed, built from the same brief, so the user can test it in the integration worktree, where
it sits together with the other features merged since the user's last merge:

```
**F1 · <title>** · merged into `integration/<name>` `<hash>` · `<integration worktree path>`
<Essence>
How to test:
1. <an action specific to this feature> → <what the user should see>
Worth a look: <as in the review block>
Approved: <auto — every task ✅ or ➖, check green, no open entry, tier gate clean, not under manual review · by the user>
```

The brief stays on the tracking branch after the merge, in every flow; nothing deletes it, and archiving moves it
with the plan.
````

### "Flow": new subsection after "### Auto-approval" (before "### Decision table")

````markdown
### Results of an autonomous run

What the user is shown after an unattended run, by every reader (the `wave-run` report, `wave-status`, a driver's
summary): per plan in autonomous flow, from its README and briefs on the tracking branch:

| Feature | Shown as |
|---|---|
| `✅ merged`, and its `Merged` hash is not in `<main branch>` yet (`git merge-base --is-ancestor <hash> <main branch>` fails) | its merged block ("Feature review") |
| `👀 review` | its review block, with the `Merge:` line |
| ⚠️ blocked | one line: `F<k> <title> — ⚠️ I<n>: <essence of the entry>` |
| 🔄 or ⬜ | one line: `F<k> <title> — <status>, waiting for <Waiting for>` |

Merged features drop out of this view once the user has merged the integration branch into `<main branch>`. A feature
without a brief (a plan run by an older `wave-run`) is shown as `wave-status` builds a missing brief.
````

### "Who reads what", row `wave-status`

"see its skill (READMEs, problem headers, Execution of 🔄/❌/⚠️ waves, review briefs of `👀 review` features, index
"Parts")" → "… review briefs of `👀 review` features and, in autonomous flow, of features merged into the integration
branch but not yet into `<main branch>`, index "Parts")".

## Exact text for `skills/wave-plan/templates.md` (task F)

In the `reviews/<feature>.md` template, after the line `- 👀 review since <YYYY-MM-DD HH:MM>` add:

```
- Merged <YYYY-MM-DD HH:MM> into `integration/<name>` `<hash>`, <auto-approved | approved by the user> (autonomous flow only)
```

In the paragraph above the template, after "…\"Worth a look\"." add: "A feature merged into an integration branch is
shown with the merged block instead (`layout.md`, \"Feature review\")."

## Edits of `skills/wave-run/autonomous.md` (task G)

"Auto-approval", the list after "Then `merge.md`, \"Record\", with these differences:" — add the item:

```markdown
- the brief `reviews/<feature>.md` of every merged feature gets the header line
  `- Merged <YYYY-MM-DD HH:MM> into `integration/<name>` `<hash>`, auto-approved` after its `👀 review since` line;
```

and after that list one paragraph:

```markdown
A feature under manual review that the user approves with the merge form is merged into the integration branch by
`merge.md` as in manual flow; its brief gets the same header line ending `approved by the user`.
```

(In the file the inline code is written as in the rest of the file; nested backticks are not needed:
``- Merged <YYYY-MM-DD HH:MM> into `integration/<name>` `<hash>`, auto-approved``.)

## Edits of `skills/wave-run/report.md` (task G)

1. Wave report template, "### Auto-merged": the first line
   `- **F<k> <title>** → \`integration/<name>\` \`<hash>\`: <"Essence" of its brief> — why: <…>` becomes
   `<merged block of every feature merged in this run ("Feature review"), each followed by a blank line>`; the
   "not merged" line stays.
2. Table row "Auto-merged": "one line per `👀 review` feature that \"Auto-approval\" … looked at in this run: merged
   (target, hash, \"Essence\", and why: …)" → "for every `👀 review` feature that \"Auto-approval\" of
   `wave-run/autonomous.md` looked at in this run: merged → its merged block of `layout.md`, \"Feature review\", in full
   (its `Approved:` line says why); not merged → one line (manual review, the failed condition with its entry, or
   `main-dirty` with the reason); `none` when no feature was `👀 review`". The rules for "How to test" of the review
   block apply.
3. Merge report, after the paragraph that ends "The `Flow:` line is always printed.", add: "Autonomous flow: each
   \"Merged\" line is the feature's merged block instead (`layout.md`, \"Feature review\")."
4. "## Before sending": append "In autonomous flow every merged feature is a full merged block, never a one-line
   summary."

## Edits of `skills/wave-status/SKILL.md` (task G)

1. "## What to read", the bullet "For each `👀 review` feature: its review brief …": add a new bullet after it:
   "- Autonomous flow: for each `✅ merged` feature whose `Merged` hash is not in `<main branch>`
   (`git merge-base --is-ancestor <hash> <main branch>` fails): its brief, from the tracking branch."
2. "## Report", the per-plan item list: add a new item right before `- \`Ready for review:\` …`:

   ```markdown
   - `Merged, not in <main branch>:` autonomous flow only ("Results of an autonomous run" of `layout.md`): the merged
     block of `layout.md`, "Feature review", for every `✅ merged` feature whose `Merged` hash is not in `<main branch>`
     yet, from its brief, in full. These are what the user tests before merging `integration/<name>`. A feature without
     a brief gets the block built as `Ready for review:` builds one, with the merged block's header and `Approved:` line.
   ```

   The ⚠️, 🔄 and ⬜ features of that view are already rows of the feature table and need no extra line; the
   `👀 review` features are already in `Ready for review:` with their `Merge:` line.

## Invariants and limits

- Manual flow: no change in what any report prints (every new rule is conditioned on autonomous flow or an
  integration branch).
- The merged block follows every rule of the review block ("How to test" at most five feature-specific steps, never
  how to build, start or test the project; nothing recorded → `How to test: not recorded — <Done when>`).
- No new files are written: the brief and README are the only source.

## Acceptance tests

Walkthroughs, checked by reading the changed texts.

1. **Night report:** autonomous wave merges F1, leaves F2 under manual review `👀 review`, F3 ⚠️ I4 → the wave report's
   "Auto-merged" has F1's full merged block (header with `integration/<name>` and hash, Essence, How to test, Worth a
   look, `Approved: auto — …`) and one line for F2 and F3; "Ready for review" has F2's review block with `Merge:`.
2. **Morning view:** `/wave-status <plan>` → `Merged, not in main:` with F1's merged block (its brief has the
   `- Merged … auto-approved` line), `Ready for review:` with F2's review block, F3 ⚠️ in the feature table.
3. **After the user's merge:** `main` now contains F1's hash → `/wave-status` no longer shows F1's block.
4. **Manual unchanged:** a manual plan → the wave report has no "Auto-merged" section and its "Ready for review" is as
   before; `wave-status` prints no merged blocks.
