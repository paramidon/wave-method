# P2. Commands `add`, `list`, `done`
User problem: commands `todo add "<text>"`, `todo list`, `todo done <id>` · feature F1

**Cause:** new project; nothing exists yet.

**Approach:** `argparse` with three sub-commands in `todo/cli.py`, a `main(argv=None) -> int` that returns the exit
code (testable without a subprocess), and a console script `todo = "todo.cli:main"` in `pyproject.toml`. All file
access goes through `todo.store` (P1).

**API:**

```python
def main(argv: list[str] | None = None) -> int: ...
```

**Behaviour** (data file `Path.cwd() / "todo.json"`):

| Command | Output (stdout) | Exit code |
|---|---|---|
| `todo add "buy milk"` | `added 1: buy milk` | 0 |
| `todo list` | one line per task: `[ ] 1 buy milk` or `[x] 2 call Bob`; nothing when empty | 0 |
| `todo done 1` | `done 1: buy milk` | 0 |
| `todo done 9` (no such id) | `no task 9` on stderr | 1 |
| empty text, or no sub-command | `argparse` usage on stderr | 2 |
| corrupt `todo.json` | the `ValueError` message on stderr | 2 |

**Limits:** `done` on a task that is already done prints the same line and exits 0.

**Acceptance tests** (`tests/test_cli.py`, each test in a `tmp_path` with `monkeypatch.chdir`):
1. `add` prints `added 1: buy milk` and creates `todo.json`;
2. a second `add` gets id 2;
3. `list` prints `[ ] 1 buy milk` and `[ ] 2 call Bob` in that order;
4. `done 1` then `list` shows `[x] 1 buy milk`;
5. `done 9` returns 1 and writes `no task 9` to stderr;
6. `main([])` returns 2.
