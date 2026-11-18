# Lite solutions (low problems)

## P3. README with install and usage

User problem: Add a README with install and usage, which the user reads before it lands. · feature F3

**Edit:** Add `README.md` with a one-line description, the install command `pip install .`, and usage
`wordstat <file> [--top N]` (default 10) with the outputs from `solutions/P2-top-words-cli.md`, “Behaviour”.
Show an example session with `poem.txt` holding `the sun and the sea and the sky` and the command
`wordstat poem.txt --top 3` producing:

```text
the 3
and 2
sea 1
```

Include a “Library” section with `count_words` and `top_words` (`wordstat.core`) and `to_csv` (`wordstat.export`).

**Check:** `README.md` contains `pip install .`, `wordstat poem.txt --top 3`, `count_words` and `to_csv`. The example
output matches P1's ordering rule.

## P4. Counts as CSV

User problem: Export the counts as CSV. · feature F4

**Edit:** Add `wordstat/export.py` with `from __future__ import annotations` and
`def to_csv(pairs: list[tuple[str, int]]) -> str`. Use `csv.writer` on an `io.StringIO` with `lineterminator="\n"`.
Write the header row `word,count` and one row per pair in the given order. Return the buffer's string.

Add three cases to `tests/test_export.py`:

1. `to_csv([]) == "word,count\n"`
2. `to_csv([("the", 2), ("cat", 1)]) == "word,count\nthe,2\ncat,1\n"`
3. `to_csv([("a,b", 1)]) == 'word,count\n"a,b",1\n'`

**Check:** `python -m pytest -q tests/test_export.py` → 3 passed.
