# P1. Word counter

User problem: Count the words of a text, case-insensitive. · feature F1

**Cause:** New code.

**Approach:** Put the pure functions in `wordstat/core.py`. Create `wordstat/__init__.py` with the one-line docstring
`"""Word statistics."""`.

**API:** Use `from __future__ import annotations`, `import re` and `from collections import Counter`.

```python
WORD = re.compile(r"[^\W_]+(?:'[^\W_]+)*")

def count_words(text: str) -> Counter[str]: ...
def top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]: ...
```

**Algorithm:** `count_words` returns `Counter(WORD.findall(text.lower()))`. `top_words` raises
`ValueError("n must be at least 1")` when `n < 1`. Otherwise it returns
`sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]`.

**Limits:** Apostrophes inside a word stay (`don't`). Leading and trailing apostrophes are dropped. Underscores split
words.

**Acceptance tests:** Seven cases in `tests/test_core.py`.

1. `count_words("The cat and the hat.") == Counter({"the": 2, "cat": 1, "and": 1, "hat": 1})`
2. `count_words("Don't stop: don't!") == Counter({"don't": 2, "stop": 1})`
3. `count_words("") == Counter()`
4. `count_words("route 66, Route 66") == Counter({"route": 2, "66": 2})`
5. `top_words(count_words("b a b c a b"), 2) == [("b", 3), ("a", 2)]`
6. `top_words(Counter({"y": 1, "x": 1}), 5) == [("x", 1), ("y", 1)]`
7. `top_words(Counter(), 0)` raises `ValueError`.
