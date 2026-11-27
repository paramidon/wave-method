# Examples

Three small plans, exactly as `/wave-plan` writes them before any wave has run. They show what you review between
planning and execution. All three are fictional projects; the file paths and line numbers are illustrative.

| Example | Starts from | What it shows |
|---|---|---|
| [`01-greenfield-todo-cli/`](01-greenfield-todo-cli/) | an empty repository | design files for `medium` problems, a contract between two waves, a feature spread over two waves |
| [`02-bugfix-batch/`](02-bugfix-batch/) | an existing web app | the smallest useful plan: three `low` fixes, three features, one wave |
| [`03-autonomous-night-run/`](03-autonomous-night-run/) | an empty repository, autonomous flow | the `Flow:` line, assumed readings, a feature under manual review, a wave that waits for an auto-merged feature |

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

Wave 1 runs A (store) and C (README) in parallel. After it, F2 (README) is ready: `wave-run` names its branch
`feat/todo-cli/F2-usage-readme` and asks whether to merge it; F1 waits, because its task B is in wave 2. Wave 2 runs
B (commands, built on A's API) and D (CI) in parallel; then F1 and F3 are offered for review, each on its own branch,
and merged when you approve them.

## 02 — a batch of bug fixes

```
/wave-plan page 3 of the product list is missing with 41 products; order dates show UTC instead of the shop's
time zone; the sign-up form accepts "jane doe@example.com"
```

All three problems are `low`, so they get one-line solutions in `solutions/lite.md` and three tasks in one wave:

```
/wave-run plans/2026-11-03-shop-fixes 1
```

All three tasks run at once; each feature is offered for review on its own branch as soon as its own check is
green, and merged when you approve it. A known failing test that needs network access is listed in the README and
does not block the features.

## 03 — a night run in autonomous flow

```
/wave-plan flow autonomous a Python package "wordstat" that counts the words of a text file, case-insensitive; a
command "wordstat <file> --top N" that prints the most frequent words; a README with install and usage, which I want
to read myself before it lands; export the counts as CSV for spreadsheets
```

`wave-plan` writes `plans/2026-11-04-wordstat-cli/` with four features and two waves:

- `Flow: autonomous · target: integration/wordstat-cli · manual review: F3`
- `Assumed (autonomous, not asked) · F1: do digits count as words? → yes: a word is a run of Unicode letters and digits with inner apostrophes; not chosen: letters only`
- `Assumed (autonomous, not asked) · F2: what does --top default to? → 10; not chosen: every word`

For the night run, start the coordinator in a Claude Code or Codex session (Codex: `$wave-auto …`) and bound it by time:

```
/wave-auto until 07:00 plans/2026-11-04-wordstat-cli
```

Wave 1 runs A and C. `wave-run` auto-approves F1 and merges it into `integration/wordstat-cli`. F3 waits for your
review. The F1 merge unlocks wave 2, which runs B and D and then auto-merges F2 and F4. `main` stays at its
starting commit.

In the morning, the final report of `/wave-auto` (or `/wave-status`) shows review blocks for the merged F1, F2, and F4
and a merge command for F3. After reviewing F3, run its merge command, inspect the integration diff, and merge the
branch from `main`:

```
/wave-run plans/2026-11-04-wordstat-cli merge F3
git diff main...integration/wordstat-cli
git merge --no-ff integration/wordstat-cli
```

To run without `wave-auto`, enter each command in a fresh session. The waves run without prompting for approval.

```
/wave-run plans/2026-11-04-wordstat-cli 1
/wave-run plans/2026-11-04-wordstat-cli 2
```

## Checking an example

All three plans pass the status check:

```bash
python skills/wave-plan/scripts/status_check.py examples/01-greenfield-todo-cli
python skills/wave-plan/scripts/status_check.py examples/02-bugfix-batch
python skills/wave-plan/scripts/status_check.py examples/03-autonomous-night-run
```
