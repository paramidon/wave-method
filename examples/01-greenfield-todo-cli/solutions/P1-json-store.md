# P1. JSON store
User problem: store tasks (id, text, done) in a JSON file in the current folder · feature F1

**Cause:** new project; nothing exists yet.

**Approach:** one small module with a dataclass and two functions. The CLI (P2) only calls these; it never touches
the file format. A plain JSON list keeps the file readable and easy to edit by hand.

**API** (`todo/store.py`):

```python
@dataclass
class Task:
    id: int
    text: str
    done: bool = False

def load(path: Path) -> list[Task]: ...
def save(path: Path, tasks: list[Task]) -> None: ...
def next_id(tasks: list[Task]) -> int: ...
```

**Algorithm:**
- `load`: missing file → `[]`; otherwise `json.loads` of a list of objects `{"id", "text", "done"}` → `Task` in
  file order.
- `save`: write to `path.with_suffix(".json.tmp")`, then `os.replace` onto `path` (no half-written file), UTF-8,
  `indent=2`, `ensure_ascii=False`.
- `next_id`: `max(id) + 1`, or `1` for an empty list (ids are never reused within one file).

**Limits:** a file that is not valid JSON, or not a list of such objects, raises `ValueError("todo.json: <reason>")`;
the CLI turns it into exit code 2.

**Acceptance tests** (`tests/test_store.py`):
1. missing file → `load` returns `[]`;
2. `save` then `load` round-trips three tasks, including non-ASCII text `"купить молоко"`;
3. `next_id([])` is 1; `next_id` of ids 1, 2, 5 is 6;
4. `save` leaves no `.json.tmp` file behind;
5. a file containing `{}` raises `ValueError` whose message starts with `todo.json:`.
