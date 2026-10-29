# A todo command-line tool in Python

- Plan: `plans/2026-11-02-todo-cli/` · slug: `todo-cli` · tracking branch: `plan/todo-cli` · created 2026-11-02 · base: 3f1c2a0
- Re-plans: none

## Features
A feature reaches the main branch only as a whole, when all its tasks are ✅ or ➖.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `todo-store-and-cli` | Tasks stored in `todo.json`, commands `add`, `list`, `done` | P1, P2 | A (1), B (2) | `pytest` green: `test_store.py` (5 cases), `test_cli.py` (6 cases) | ⬜ | wave 1 | | |
| F2 | `usage-readme` | README with install and usage | P3 | C (1) | README shows install, the three commands and an example session | ⬜ | wave 1 | | |
| F3 | `ci-tests` | Tests run on every push | P4 | D (2) | the workflow file is valid YAML and runs `pytest` on Python 3.10 and 3.12 | ⬜ | wave 2 | | |

Merged: short hash of the merge commit into the main branch.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, C | ⬜ |
| 2 | `waves/w02.md` | B, D | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `json-store` | F1 | 1 | medium | ⬜ |
| B | `cli-commands` | F1 | 2 | medium | ⬜ |
| C | `readme-usage` | F2 | 1 | low | ⬜ |
| D | `ci-workflow` | F3 | 2 | low | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/todo-cli` and reach the
main branch with each wave that merges a feature.

## User problems

- P1 — Store tasks (id, text, done) in a JSON file in the current folder. → F1 · `solutions/P1-json-store.md`
- P2 — Commands `todo add "<text>"`, `todo list`, `todo done <id>`. → F1 · `solutions/P2-cli-commands.md`
- P3 — A README that explains how to install and use the tool. → F2 · `solutions/lite.md` (low)
- P4 — Run the tests on every push. → F3 · `solutions/lite.md` (low)

## Known test failures before start

- None: the repository is empty except for `LICENSE`.

## Assumptions

- Python 3.10+, standard library only at run time; `pytest` for tests.
- The data file is `todo.json` in the current working folder; a missing file means an empty list.
- P1 and P2 are one feature: a store without commands, or commands without a store, is useless on `main`.
- B needs A's API, so it runs in wave 2; F2 can merge after wave 1, F1 and F3 after wave 2.
