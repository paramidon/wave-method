# Plan templates

### `README.md`

````markdown
# <Plan title>

- Plan: `plans/<…>/` · slug: `<slug>` · tracking branch: `plan/<slug>` · created <date> · base: <git short hash>
- Index: `plans/<date>-<topic>/index.md` part <K> (omit when planned from a raw list)
- Re-plans: none (later one sub-item each: `<date> at <hash>: <what>`; details in `history.md`)
- Models: (omit unless this plan names concrete models; tiers and rules: `layout.md`, "Model tiers")

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖ and the user approved it after review.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `cheap-interbody-omega` | … | P1, P2 | A (1), C (2), E (3) | tests … green | ⬜ | wave 1 | | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B | ⬜ |
| 2 | `waves/w02.md` | C, D, E (after C, D) | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `periapsis-argument-math` | F1 | 1 | medium | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/<slug>` and reach the
main branch with each feature merge.

## User problems

- P1 — <one-line statement> → F1 · `solutions/P1-<slug>.md`
- P2 — <one-line statement> → F1 · `solutions/lite.md` (low)

## How to try

- F1 — `<command that starts the project or the part it changes>`; <what the user does> → <what the user sees
  when it works>; before this feature: <what they saw instead>

## Known test failures before start

- <test> — <branch, until task <ID>>; <cause, if known>

## Assumptions

- …
````

### `solutions/P<n>-<slug>.md`

````markdown
# P<n>. <short>
User problem: <one line, as in README> · feature F<k>

**Cause:** … (`file:line`)
**Approach:** …
**API:** ```<signatures>```
**Algorithm:** …
**Limits:** …
**Acceptance tests:** …
````

### `solutions/lite.md`

````markdown
# Lite solutions (low problems)

## P2. <short>
User problem: <one line, as in README> · feature F<k>
**Edit:** <exact change, `file:line`> · **Check:** <one acceptance check>
````

### `waves/w<NN>.md`

````markdown
# Wave <N>
Status: see README "Waves"

## Tasks

| ID | Slug | Feature | Complexity | P | After | Needs | Files |
|---|---|---|---|---|---|---|---|
| A | `periapsis-argument-math` | F1 | medium | P1 | — | — | `src/…` |

Depends on: <`F<k> merged` for every other feature whose code this wave's tasks need; what this wave needs from
earlier waves; or "nothing">. Disjoint files: <why>.

## Task A · periapsis-argument-math · F1 · medium

```
<full prompt>
```

## Execution
Filled in by `wave-run`.

## Closed problems
Closed problem-log entries found in this wave (moved here from `problems.md`).
````

### `reviews/<feature>.md`

Written by `wave-run` (`wave-run/SKILL.md` steps 7 and 8), in English like every plan file. While the feature is in
progress the file holds only the header and "What was done"; the other sections are written when it becomes
`👀 review` and rewritten when it becomes `👀 review` again after a rejection.

````markdown
# F1 · <Title>

- Plan: `plans/<…>/` · branch: `feat/<plan>/<feature>` · worktree: `<absolute feature worktree path>`
- Status: 👀 review since <YYYY-MM-DD HH:MM> · <n> commits · <git diff --stat summary line>

## What and why

<The user problems of the feature (its P lines) in plain words, and what changes once it is merged: before →
after, one to three sentences.>

## What was done

- A (wave 1) — <what the task did, in plain words> · files: `<file>`, `<file>`
- C (wave 2) — ➖ dropped: <reason>

## How it was checked

- Done when: <the README cell> → <met / not met>
- `<full check command>` → <result, for example 48 passed, 1 known failure `<test>`>
- Tests added or changed: `<test file>` (<what they cover>)

## How to test

1. `cd <absolute feature worktree path>`
2. `<command>` → <what the user should see>
3. <action> → <what the user should see>; before this feature: <what they saw instead>

Not covered by tests: <what only a person can judge, or "nothing">.

## Worth a look

- <a decision the user may not expect: a closed problem entry, an assumption, a conflict resolution that changed
  the feature's code; or "nothing">
````

`problems.md` is created with the first entry (format: `layout.md`, "Problem log"); `history.md` at the first
re-plan, starting with `# History` and one section per re-plan.
