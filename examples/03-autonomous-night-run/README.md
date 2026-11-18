# Word statistics in Python, planned for a night run

- Plan: `plans/2026-11-04-wordstat-cli/` · slug: `wordstat-cli` · tracking branch: `plan/wordstat-cli` · created 2026-11-04 · base: 7d2e9b1 · planned 2026-11-04 18:02 – 2026-11-04 18:14
- Re-plans: none
- Flow: autonomous · target: integration/wordstat-cli · manual review: F3

## Features

A feature reaches `integration/wordstat-cli` as a whole when all its tasks are ✅ or ➖. F3 requires the user's approval.

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `word-counter` | Count the words of a text | P1 | A (1) | `python -m pytest -q` green: `tests/test_core.py` (7 cases) | ⬜ | wave 1 | | |
| F2 | `top-words-cli` | Command `wordstat <file> --top N` | P2 | B (2) | `tests/test_cli.py` (5 cases) green | ⬜ | wave 2 | | |
| F3 | `usage-readme` | README with install and usage | P3 | C (1) | README shows install, the command, an example session and the library calls | ⬜ | wave 1 | | |
| F4 | `csv-export` | Word counts as CSV | P4 | D (2) | `tests/test_export.py` (3 cases) green | ⬜ | wave 2 | | |

Merged: short hash of the merge commit into `integration/wordstat-cli`.

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A, C | ⬜ |
| 2 | `waves/w02.md` | B, D | ⬜ |

## Tasks

| ID | Slug | Feature | Wave | Complexity | Status |
|---|---|---|---|---|---|
| A | `word-counter-core` | F1 | 1 | medium | ⬜ |
| B | `top-words-command` | F2 | 2 | medium | ⬜ |
| C | `usage-readme` | F3 | 1 | low | ⬜ |
| D | `csv-export` | F4 | 2 | low | ⬜ |

Files, prompts and dependencies are in the wave files. Branch names, statuses and their rules:
`wave-plan/layout.md` of the wave skills. Marks are committed on the tracking branch `plan/wordstat-cli` and reach
`integration/wordstat-cli` with each feature merge.

## User problems

- P1 — Count the words of a text, case-insensitive. → F1 · `solutions/P1-word-counter.md`
- P2 — Provide a command `wordstat <file> --top N` printing the most frequent words. → F2 · `solutions/P2-top-words-cli.md`
- P3 — Add a README with install and usage, which the user reads before it lands. → F3 · `solutions/lite.md` (low)
- P4 — Export the counts as CSV. → F4 · `solutions/lite.md` (low)

## How to try

- F1 — `python -c "from wordstat.core import count_words, top_words; print(top_words(count_words('b a b c a b'), 2))"`
  → `[('b', 3), ('a', 2)]`; before: no package
- F2 — `wordstat poem.txt --top 3` → three lines `<word> <count>`; before: no command
- F3 — open `README.md` → install, the command with its output, an example session and the library calls; before: only `LICENSE`
- F4 — `python -c "from wordstat.export import to_csv; print(to_csv([('the', 2)]), end='')"`
  → `word,count` and `the,2`; before: no export

## Known test failures before start

- None: the repository is empty except for LICENSE; until task A adds tests/, the check command prints "no tests yet" and exits 0.

## Assumptions

- Python 3.10+, standard library only at run time; `pytest` for tests.
- Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only
- Assumed (autonomous, not asked) · F2: what does --top default to? → 10; not chosen: every word
- F3 is under manual review because the user asked to read it first. After the night it waits as `👀 review`.
- Wave 2 depends on `F1 merged`. B uses `wordstat.core` and D adds a module to the `wordstat` package. In autonomous
  flow `wave-run` merges F1 into `integration/wordstat-cli` after wave 1 without asking, so wave 2 runs the same night.
  In manual flow, wave 2 would stop with `feature-unmerged` until the user merged F1.
