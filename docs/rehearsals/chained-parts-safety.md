# Rehearsal: chained-parts safety

2026-11-17 · `git version 2.52.0.windows.1` · skill texts at `16f9e13`

## Setup

The commands below ran in Git Bash with an empty temporary directory at `<scratch>`. I followed the checked-out skill documents as the coordinator, using Git and Python in the toy repository. The part 1 README is fixture data.

```bash
cd "<scratch>"
git init -b main repo
cd repo
git config user.name "Wave rehearsal"
git config user.email "wave-rehearsal@example.invalid"
git config core.autocrlf false

cat > todo.py <<'PY'
VERSION = "0.1.0"


def add(items, text):
    return items + [{"text": text, "done": False}]


def rm(items, n):
    return items[:n - 1] + items[n:]


def list_items(items):
    return [f"{n}. {item['text']}" for n, item in enumerate(items, 1)
            if not item["done"]]
PY

cat > test_todo.py <<'PY'
import unittest

from todo import add, list_items, rm


class TodoTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add([], "read"), [{"text": "read", "done": False}])

    def test_rm(self):
        self.assertEqual(rm(["first", "second"], 1), ["second"])

    def test_list_items(self):
        items = [{"text": "read", "done": True}, {"text": "write", "done": False}]
        self.assertEqual(list_items(items), ["2. write"])
PY

PYTHONDONTWRITEBYTECODE=1 python -m unittest
git add todo.py test_todo.py
git commit -m init
base=$(git rev-parse --short HEAD)

topic=plans/2026-11-17-todo
mkdir -p "$topic"
{
  printf '# Todo index\n\n- Index: `%s/index.md` · created 2026-11-17 · base: %s · triaged 2026-11-17 02:55 – 2026-11-17 02:56\n' "$topic" "$base"
  cat <<'MD'
- Flow: autonomous · target: integration/todo

## Problems

### P1. Print the version

- User's words: `--version` prints `VERSION`.
- Clarifications: none.
- Where: `todo.py:1`. Reuse: `VERSION`.
- Likely cause: there is no command-line entry point.
- Difficulty: low · Size: one task.
- Depends on: none.

### P2. Add a version header to list

- User's words: `list` prints a header line with the version.
- Clarifications: none.
- Where: `todo.py:12`. Reuse: `VERSION`, `list_items`.
- Likely cause: there is no list command.
- Difficulty: low · Size: one task.
- Depends on: P1 (command-line entry point).

### P3. List done items on request

- User's words: `list --all` also shows done items.
- Clarifications: none.
- Where: `todo.py:12`. Reuse: `list_items`.
- Likely cause: the formatter filters out done items.
- Difficulty: low · Size: one task.
- Depends on: none.

### P4. Mark an item done

- User's words: `done <n>` marks an item done.
- Clarifications: none.
- Where: `todo.py:5`. Reuse: the item records.
- Likely cause: there is no completion command.
- Difficulty: low · Size: one task.
- Depends on: none.

## Parts

| Part | Problems | Points | Plan slug | Plan when | Command |
|---|---|---|---|---|---|
| 1 | P1 | 1 | `todo-p1` | now | `/wave-plan plans/2026-11-17-todo/index.md part 1`<br>`$wave-plan plans/2026-11-17-todo/index.md part 1` |
| 2 | P2, P3 | 2 | `todo-p2` | after part 1 merged | `/wave-plan plans/2026-11-17-todo/index.md part 2`<br>`$wave-plan plans/2026-11-17-todo/index.md part 2` |
| 3 | P4 | 1 | `todo-p3` | now | `/wave-plan plans/2026-11-17-todo/index.md part 3` |

## Assumptions

- none

## Open questions

- none
MD
} > "$topic/index.md"
git add "$topic/index.md"
git commit -m "Index todo"

git switch -c feat/todo-p1/F1-version-option
cat >> todo.py <<'PY'


if __name__ == "__main__":
    import sys

    if sys.argv[1:] == ["--version"]:
        print(VERSION)
PY
git add todo.py
git commit -m "Print the version"
git switch main
git merge --no-ff feat/todo-p1/F1-version-option -m "Merge the version option"
h1=$(git rev-parse HEAD)

mkdir -p "$topic/plan-1"
{
  printf '# Version option\n\n- Plan: `%s/plan-1/` · slug: `todo-p1` · tracking branch: `plan/todo-p1` · created 2026-11-17 · base: %s\n' "$topic" "$base"
  cat <<'MD'
- Index: `plans/2026-11-17-todo/index.md` part 1
- Re-plans: none
- Flow: autonomous · target: integration/todo

## Features

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
MD
  printf '| F1 | `version-option` | Print the version | P1 | A (1) | `python todo.py --version` prints 0.1.0 | ✅ merged | | `feat/todo-p1/F1-version-option` | %s |\n' "$h1"
} > "$topic/plan-1/README.md"
git add "$topic/plan-1/README.md"
git commit -m "Record the merged version option"
```

## Scenario 4. Manual predecessor without a tracking branch

- Run: `/wave-plan plans/2026-11-17-todo/index.md part 2`. The index selected autonomous flow. After preflight, I planned P2 and P3 together as one list feature with two low-complexity tasks, one for `todo.py` and one for `test_todo.py`. The toy CLI starts with an empty list. The feature plan covered done items through the formatter API.
- Expected: Check 3 takes the completed predecessor from `main`. Check 4 creates the integration worktree from `main`. Part 2 lands on integration, with no change to `main` and no claim left.
- Seen: `git branch --list 'plan/*'` returned nothing before check 3. `git show main:plans/2026-11-17-todo/plan-1/README.md` returned F1 as ✅ merged with `b87941f`. `git merge-base --is-ancestor b87941f main` succeeded. Immediately after `git worktree add -b integration/todo ../repo.worktrees/integration-todo main`, `git rev-parse integration/todo` matched `main` at `e9c8ab8`. The three baseline tests passed in the integration worktree, and `python todo.py --version` printed `0.1.0`.
- Seen: The new tracking worktree's part 2 passed `status_check.py`. `git log -1 --format='%h %p %s' integration/todo` printed `87d9d43 e9c8ab8 7eff59d Plan todo-p2: list options`. `git cat-file -e integration/todo:plans/2026-11-17-todo/plan-2/README.md` succeeded, and the lookup on `main` failed. `git rev-parse main` still returned `e9c8ab8` (shortened). For release I compared the holder text, then read the current claim OID as the expected old value. `git for-each-ref refs/wave-method/claims/` returned nothing.
- Result: holds

## Scenario 5. Existing plan stops before writes

- Run: I added `note.txt` and committed it on `main` as `Advance main` (`b8bfa4f`). I ran `/wave-plan plans/2026-11-17-todo/index.md part 2` again.
- Expected: The first line after `Started:` is `Stop plan-exists:`. Integration, refs and worktrees remain unchanged, and there is no claim.
- Seen: Check 0 found `plan/todo-p2` with `git show-ref --verify --quiet refs/heads/plan/todo-p2`. The first line after `Started:` was `Stop plan-exists: plan/todo-p2 already exists — next: run /wave-run plans/2026-11-17-todo/plan-2 1 or $wave-run plans/2026-11-17-todo/plan-2 1`.
- Seen: `cmp` found identical before and after snapshots from `git for-each-ref --format="%(refname) %(objectname)"` and `git worktree list --porcelain`. `git rev-parse integration/todo` still returned `87d9d43` (shortened). `git merge-base --is-ancestor main integration/todo` returned 1. `git for-each-ref refs/wave-method/claims/` returned nothing.
- Result: holds

## Scenario 6. Target claim

I set `claim=refs/wave-method/claims/integration/todo`. I used `printf '%s\n' 'todo-p1 wave 2 2026-11-17 03:00' | git hash-object -w --stdin` and `git update-ref "$claim" "$held" "$zero"`, with the resulting OID in `held` and 40 zeros in `zero`. Git returned `f3a9419925274f6384515c7d0eef4efc3ef8c723`.

### Held claim during planning

- Run: `/wave-plan plans/2026-11-17-todo/index.md part 3`.
- Expected: `Stop wave-running` names the holder. The held claim, refs and worktrees remain unchanged, and `plan/todo-p3` is absent.
- Seen: `Stop wave-running: integration/todo is claimed by todo-p1 wave 2 2026-11-17 03:00 — next: wait`. `git rev-parse "$claim"` still returned the held OID. `git show-ref --verify --quiet refs/heads/plan/todo-p3` failed. `cmp` found identical before and after snapshots from `git for-each-ref --format="%(refname) %(objectname)"` and `git worktree list --porcelain`.
- Seen: I computed the contender OID with `git hash-object --stdin` and confirmed `git cat-file -e "$candidate"` failed before the attempt. After the rejected `git update-ref`, `git cat-file -t "$candidate"` returned `blob` and `git cat-file -p "$candidate"` printed `todo-p3 planning 2026-11-17 20:51`. The attempt had written the blob with `git hash-object -w --stdin` before trying to update the ref.
- Result: defect: the failed claim writes an unreferenced contender blob despite the instruction saying “nothing written” — `skills/wave-plan/layout.md:375`

### Held claim during wave execution

- Run: `/wave-run plans/2026-11-17-todo/plan-2 1`, through its readiness check.
- Expected: `Stop wave-running` names the same holder before a wave-start commit. Wave 1 stays ⬜, and there is no feature branch for `todo-p2`.
- Seen: Git located the README on `plan/todo-p2`. The integration worktree was on `integration/todo`, with no tracked changes or unfinished merge. The claim attempt returned `Stop wave-running: integration/todo is claimed by todo-p1 wave 2 2026-11-17 03:00 — next: wait`. `git show plan/todo-p2:plans/2026-11-17-todo/plan-2/README.md` still showed wave 1 as ⬜. `git branch --list 'feat/todo-p2/*'` and `git log --grep='wave 1 started' plan/todo-p2` returned nothing. Both snapshots and the held OID were unchanged.
- Seen: The same before and after object check with `git cat-file -e` and `git cat-file -t` found a newly written blob. `git cat-file -p "$candidate"` printed `todo-p2 wave 1 2026-11-17 20:51`.
- Result: defect: the failed claim writes an unreferenced contender blob despite the instruction saying “nothing written” — `skills/wave-run/autonomous.md:46–47`

### Guarded release

- Run: `git update-ref -d "$claim" "$wrong"`, then `git update-ref -d "$claim" "$held"`. The first OID came from hashing the line `unrelated` into a blob.
- Expected: The first deletion fails and leaves the claim holder intact. The second removes it.
- Seen: Git reported the held OID and the different expected OID on the first deletion. `git rev-parse "$claim"` still returned the held OID. The second deletion succeeded, and `git for-each-ref "$claim"` returned nothing.
- Result: holds

### Race

- Run: For each of ten rounds I started two background subshells with the claim commands and holder lines `race-a` and `race-b`. I used `wait` on both PIDs and counted successful exits.
- Expected: One success per round. The winner's OID deletes the claim before the next round.
- Seen: Exactly one process exited successfully each round. `git rev-parse "$claim"` matched its emitted OID. `git update-ref -d "$claim" "$winner"` succeeded, and `git for-each-ref "$claim"` returned nothing before the next round.
- Result: holds

Race: 1 1 1 1 1 1 1 1 1 1
