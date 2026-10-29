# Three small fixes in the shop web app

- Plan: `plans/2026-11-03-shop-fixes/` · slug: `shop-fixes` · tracking branch: `plan/shop-fixes` · created 2026-11-03 · base: 9b4e7d1 · skills: v1
- Re-plans: none

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `last-page-items` | The last page of a list shows its items | P1 | A (1) | `test_pagination.py` green, full `pytest` green | ⬜ | wave 1 | | |
| F2 | `local-order-dates` | Order dates in the shop's time zone | P2 | B (1) | `test_filters.py` green, full `pytest` green | ⬜ | wave 1 | | |
| F3 | `strict-email-check` | E-mail addresses with spaces are rejected | P3 | C (1) | `test_validators.py` green, full `pytest` green | ⬜ | wave 1 | | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, B, C | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `page-count-fix` | F1 | 1 | low | ⬜ |
| B | `order-date-timezone` | F2 | 1 | low | ⬜ |
| C | `email-no-spaces` | F3 | 1 | low | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`.claude/skills/wave-plan/layout.md`. Marks are committed on the tracking branch `plan/shop-fixes` and reach the
main branch with each wave that merges a feature.

## User problems

- P1 — With 41 products and 20 per page, page 3 is missing. → F1 · `solutions/lite.md` (low)
- P2 — Order dates are shown in UTC; customers expect the shop's time zone. → F2 · `solutions/lite.md` (low)
- P3 — The sign-up form accepts `jane doe@example.com`. → F3 · `solutions/lite.md` (low)

## Known test failures before start

- `tests/test_payment.py::test_sandbox_refund` — needs network access to the payment sandbox; fails offline.

## Assumptions

- Three independent fixes in different files: three features, so each can reach `main` on its own.
- The shop's time zone is the existing setting `SHOP_TIMEZONE` (`config.py:14`).
