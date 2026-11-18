# P2. Top words command

User problem: Provide a command `wordstat <file> --top N` printing the most frequent words. · feature F2

**Cause:** New code.

**Approach:** Add `wordstat/cli.py` with `argparse`, `wordstat/__main__.py` for `python -m wordstat` and
`pyproject.toml` for the console script. The CLI reads the file and calls `wordstat.core` to count and rank words.

**API:** Use `from __future__ import annotations` in `wordstat/cli.py` and define
`def main(argv: list[str] | None = None) -> int`. Set `prog="wordstat"` for `argparse`, with positional `file` and
option `--top` (`type=int`, `default=10`).

In `wordstat/__main__.py`:

```python
import sys

from wordstat.cli import main

sys.exit(main())
```

In `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "wordstat"
version = "0.1.0"
requires-python = ">=3.10"

[project.scripts]
wordstat = "wordstat.cli:main"

[tool.setuptools]
packages = ["wordstat"]
```

## Behaviour

| Input | stdout | stderr | Exit |
|---|---|---|---|
| `wordstat notes.txt`, the file holds `the cat the` | `the 2` and `cat 1`, one per line | — | 0 |
| `wordstat notes.txt --top 1` | `the 2` | — | 0 |
| `wordstat empty.txt`, an empty file | nothing | — | 0 |
| `wordstat missing.txt` | nothing | `error: cannot read missing.txt` | 1 |
| `wordstat notes.txt --top 0` | nothing | `error: --top must be at least 1` | 2 |

**Algorithm:** Check `--top` first. When `args.top < 1`, print `error: --top must be at least 1` to stderr and
return 2. Read with `Path(args.file).read_text(encoding="utf-8")`. On `OSError` or `UnicodeDecodeError`, print
`error: cannot read <file>` to stderr with the path as given and return 1. Print `f"{word} {count}"` for each pair
of `top_words(count_words(text), args.top)` and return 0.

**Limits:** The repository also holds `plans/` and `.claude/`; setuptools' automatic flat-layout discovery would
count `plans` as a second top-level package and refuse to build, so `[tool.setuptools]` lists `wordstat` explicitly.

**Acceptance tests:** Add five cases to `tests/test_cli.py`, one per row of the Behaviour table. Use `tmp_path`,
`monkeypatch.chdir(tmp_path)` and `capsys`. Call `main([...])` directly.

- `python -m pip wheel --no-deps -w "$(mktemp -d)" .` in the repository root exits 0 (it needs network or a pip cache
  for setuptools). `python -m zipfile -l <that wheel>` lists `wordstat/cli.py` and no path starting with `plans/`.
- With a file `notes.txt` holding `the cat the` in a temporary folder `<tmp>`,
  `python -m wordstat <tmp>/notes.txt --top 1` in the repository root prints `the 2`.
