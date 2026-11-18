# P17. Example 03 fixes: plan slug, a check that passes on an empty baseline, explicit packaging
User problem: (re-plan, from I1–I3 of wave 1 / task B) example 03 as specified in `solutions/P8-flow-docs.md`, "B.
Example 03", cannot run: a README-only feature never passes `pytest`, `pip install .` refuses the repository, and
the plan slug breaks the layout · feature F1

**Cause:**

- I1. Every check of example 03 is bare `python -m pytest -q` (P8 "B. Example 03", "Waves", line 243). pytest exits
  5 ("no tests ran") when it collects nothing. That happens on the seed (`LICENSE`, `plans/`, `.claude/`), where
  `wave-run` step 3 runs the check on the new branches of F1 and F3 before wave 1, and on F3's branch for its whole
  life: task C adds only `README.md`, and F3 is under manual review, so nothing else reaches its branch. F3 could
  never become `👀 review`.
- I2. The `pyproject.toml` of P8 ("`solutions/P2-top-words-cli.md`", line 199) leaves package discovery to setuptools.
  The repository holds `plans/` (and `.claude/`) next to `wordstat/`. setuptools' automatic flat-layout discovery
  (`setuptools/discovery.py`, `FlatLayoutPackageFinder`, PEP 420 namespaces included) counts every top-level folder
  whose name is an identifier and is not on its exclude list (`tests`, `docs`, `scripts`, dot-folders, …): it finds
  `plans` and `wordstat` and stops with `Multiple top-level packages discovered in a flat-layout`. Not run at the
  re-plan (no setuptools offline); task H proves it.
- I3. The example's slug `wordstat` (P8 line 129) is one word; `layout.md` "Folders" requires 2–4 kebab-case words.
  The driver does not check it, so the example would teach a slug `wave-plan` never writes.

**Approach:** three literal corrections to P8 "B. Example 03"; everything else of that section stays exactly as
written (features, tasks, API, algorithm, acceptance values, prompts' structure). The example task (G) reads P8
section B **and** this file; where they differ, this file wins.

- I3: the slug becomes `wordstat-cli`. The target becomes `integration/wordstat-cli`, not the `integration/wordstat`
  that I3's proposal kept: for a plan made from a raw list `wave-plan` writes `target: integration/<slug>`
  (`layout.md`, "Planning in autonomous flow"), and the example must look exactly as `wave-plan` writes it. The
  package, its modules, the command and the project name stay `wordstat`.
- I1: one check command for every task and both waves, green on a branch without tests and plain pytest once
  `tests/` exists. Not `python -m pytest -q || [ $? -eq 5 ]`: harder to read in a first example, and it would also
  accept a `tests/` folder whose tests a task deleted. Not a placeholder test: a file no task owns. Task C's own
  acceptance is the README content check of `solutions/lite.md` "P3".
- I2: the package list is explicit in `pyproject.toml`; task B proves the build with `pip wheel`, which builds the
  package without installing anything into the user's Python.

## Replacements (I3)

In every text of example 03 and of the `examples/README.md` section that P8 section B specifies:

| P8 section B writes | Example 03 writes |
|---|---|
| `plans/2026-11-04-wordstat/`, `plans/2026-11-04-wordstat` | `plans/2026-11-04-wordstat-cli/`, `plans/2026-11-04-wordstat-cli` |
| `slug: \`wordstat\`` | `slug: \`wordstat-cli\`` |
| `plan/wordstat` | `plan/wordstat-cli` |
| `integration/wordstat` | `integration/wordstat-cli` |

Unchanged: `wordstat/`, `wordstat.core`, `wordstat.export`, `wordstat.cli:main`, the command `wordstat <file>`, the
project name `"wordstat"`, the title. The README header becomes:

```
# Word statistics in Python, planned for a night run

- Plan: `plans/2026-11-04-wordstat-cli/` · slug: `wordstat-cli` · tracking branch: `plan/wordstat-cli` · created 2026-11-04 · base: 7d2e9b1 · planned 2026-11-04 18:02 – 2026-11-04 18:14
- Re-plans: none
- Flow: autonomous · target: integration/wordstat-cli · manual review: F3
```

## Check command (I1)

The example's check command, verbatim, the same for every task of both waves:

```bash
if [ -d tests ]; then python -m pytest -q; else echo "no tests yet"; fi
```

| Branch state | Output | Exit |
|---|---|---|
| no `tests/` folder: the seed, F1's and F3's branches before wave 1, F3's branch after task C | `no tests yet` | 0 |
| `tests/` with test files | pytest's summary | pytest's exit code: 0 green, 1 a failing test |

Where it is written in example 03:

1. README "Known test failures before start": the single item
   `- None: the repository is empty except for LICENSE; until task A adds tests/, the check command prints "no tests yet" and exits 0.`
2. Each wave file, right after the "Depends on: … Disjoint files: …" paragraph:
   `Check command of every task (the feature's full check):`, a blank line, the fenced `bash` block above, a blank
   line, then `Known failures: none.`
3. Each task prompt has a line `Check command: if [ -d tests ]; then python -m pytest -q; else echo "no tests yet"; fi (no known failures).`
   and, before it, its acceptance:
   - A: `python -m pytest -q` → `7 passed` (the seven cases of `tests/test_core.py`).
   - B: `python -m pytest -q` → `12 passed` (7 of `test_core.py`, 5 of `test_cli.py`), plus the packaging check below.
   - C: each of `pip install .`, `wordstat poem.txt --top 3`, `count_words` and `to_csv` appears in `README.md`
     (`grep -c -F -- "<text>" README.md` prints at least 1 for each); the example output `the 3`, `and 2`, `sea 1`
     follows P1's ordering rule; the check command prints `no tests yet` (C adds no test).
   - D: `python -m pytest -q tests/test_export.py` → `3 passed`; the check command → `10 passed` (7 + 3) on F4's
     branch, which has F1 but not F2.
4. P8's sentence "the check command `python -m pytest -q` with 'no known failures'" (P8 "Waves", third bullet) is
   replaced by item 3.

## Packaging (I2)

`solutions/P2-top-words-cli.md` of the example gives `pyproject.toml` as a fenced `toml` block, verbatim:

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

and adds to its "Limits": "The repository also holds `plans/` and `.claude/`; setuptools' automatic flat-layout
discovery would count `plans` as a second top-level package and refuse to build, so `[tool.setuptools]` lists
`wordstat` explicitly." Task B's prompt in `waves/w02.md` quotes the same block and adds to its acceptance:

- `python -m pip wheel --no-deps -w "$(mktemp -d)" .` in the repository root exits 0 (it needs network or a pip cache
  for setuptools); `python -m zipfile -l <that wheel>` lists `wordstat/cli.py` and no path starting with `plans/`.
- With a file `notes.txt` holding `the cat the` in a temporary folder `<tmp>`,
  `python -m wordstat <tmp>/notes.txt --top 1` run in the repository root prints `the 2`.

## Limits

- No other change to example 03: the four features, tasks A–D, waves (A, C; B, D), the two `Assumed` lines, every
  acceptance value of P8 section B ("Key values" of the task) stay.
- `status_check.py` must accept the README unchanged (exit 0, no output).
- Plan paths in this plan's own `solutions/P9-end-to-end-runs.md` already use the new slug (re-plan of 2026-11-18).

## Acceptance tests

1. `python skills/wave-plan/scripts/status_check.py examples/03-autonomous-night-run` → exit 0, no output; the
   header has `slug: \`wordstat-cli\`` and `- Flow: autonomous · target: integration/wordstat-cli · manual review: F3`.
2. `git grep -n -E "(plan/|integration/|feat/|2026-11-04-)wordstat($|[^-])" -- examples` → no output.
3. `git grep -c -F 'if [ -d tests ]; then python -m pytest -q; else echo "no tests yet"; fi' -- examples/03-autonomous-night-run/waves`
   → `w01.md` 3 or more (wave check, A, C), `w02.md` 3 or more (wave check, B, D).
4. Empty baseline, in a scratch repository seeded with `LICENSE`, an empty `.claude/` folder with one file, and the
   example copied to `plans/2026-11-04-wordstat-cli`: the check command prints `no tests yet` and exits 0; after
   adding `tests/test_ok.py` with `def test_ok(): pass` it prints `1 passed` and exits 0 (with pytest installed).
5. Packaging, in the same scratch repository plus `wordstat/__init__.py` (`"""Word statistics."""`),
   `wordstat/cli.py` (`def main(argv=None):` / `    return 0`) and the `pyproject.toml` block above:
   `python -m pip wheel --no-deps -w <tmp> .` exits 0 and the wheel has no `plans/` path. Then the same with the
   `[tool.setuptools]` table removed: expected to fail with `Multiple top-level packages` in its output. This second
   build only confirms the cause; if it succeeds, report its output and go on (the explicit list stays).
6. `examples/03-autonomous-night-run/solutions/P2-top-words-cli.md` contains the `pyproject.toml` block verbatim.
