# Examples

Two small plans, exactly as `/wave-plan` writes them before any wave has run. They show what you review between
planning and execution. Both are fictional projects; the file paths and line numbers are illustrative.

| Example | Starts from | What it shows |
|---|---|---|
| [`01-greenfield-todo-cli/`](01-greenfield-todo-cli/) | an empty repository | design files for `medium` problems, a contract between two waves, a feature spread over two waves |
| [`02-bugfix-batch/`](02-bugfix-batch/) | an existing web app | the smallest useful plan: three `low` fixes, three features, one wave |

## 01 — a new tool from an empty repository

You type (Claude Code; in Codex start with `$`):

```
/wave-plan create a Python CLI "todo": add, list and done commands, tasks stored in todo.json; README with install
and usage; run the tests on every push
```

`wave-plan` writes `plans/2026-11-02-todo-cli/`:

- `README.md` — three features, two waves, four tasks;
- `solutions/P1-json-store.md`, `solutions/P2-cli-commands.md` — the API, behaviour table and acceptance tests that
  the executors implement;
- `solutions/lite.md` — the two `low` problems (README, CI workflow);
- `waves/w01.md`, `waves/w02.md` — the full task prompts.

Then, each in a fresh session:

```
/wave-run plans/2026-11-02-todo-cli 1
/wave-run plans/2026-11-02-todo-cli 2
```

Wave 1 runs A (store) and C (README) in parallel. After it, F2 (README) is merged into `main`; F1 waits, because its
task B is in wave 2. Wave 2 runs B (commands, built on A's API) and D (CI) in parallel; then F1 and F3 are merged.

## 02 — a batch of bug fixes

```
/wave-plan page 3 of the product list is missing with 41 products; order dates show UTC instead of the shop's
time zone; the sign-up form accepts "jane doe@example.com"
```

All three problems are `low`, so they get one-line solutions in `solutions/lite.md` and three tasks in one wave:

```
/wave-run plans/2026-11-03-shop-fixes 1
```

All three tasks run at once; each feature is merged as soon as its own check is green. A known failing test that
needs network access is listed in the README and does not block the merges.

## Checking an example

Both plans pass the status check:

```bash
python skills/wave-plan/scripts/status_check.py examples/01-greenfield-todo-cli
python skills/wave-plan/scripts/status_check.py examples/02-bugfix-batch
```
