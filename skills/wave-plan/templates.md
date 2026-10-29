# Plan templates

### `README.md`

````markdown
# <Plan title>

- Plan: `plans/<…>/` · slug: `<slug>` · tracking branch: `plan/<slug>` · created <date> · base: <git short hash>
- Index: `plans/<date>-<topic>/index.md` part <K> (omit when planned from a raw list)
- Re-plans: none (later one sub-item each: `<date> at <hash>: <what>`; details in `history.md`)
- Models: (omit unless this plan names concrete models; tiers and rules: `layout.md`, "Model tiers")

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖.

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
main branch with each wave that merges a feature.

## User problems

- P1 — <one-line statement> → F1 · `solutions/P1-<slug>.md`
- P2 — <one-line statement> → F1 · `solutions/lite.md` (low)

## Known test failures before start

- <test> — <cause, if known>

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

Depends on: <what this wave needs from earlier waves, or "nothing">. Disjoint files: <why>.

## Task A · periapsis-argument-math · F1 · medium

```
<full prompt>
```

## Execution
Filled in by `wave-run`.

## Closed problems
Closed problem-log entries found in this wave (moved here from `problems.md`).
````

`problems.md` is created with the first entry (format: `layout.md`, "Problem log"); `history.md` at the first
re-plan, starting with `# History` and one section per re-plan.
