# Rehearsal: autonomous triage and chained planning

2026-11-17 · `git version 2.52.0.windows.1` · skill texts at start commit `16f9e13`

## Setup

In Git Bash, replace `<scratch>` with a new system temporary directory. The first block creates both toy repositories.
The second block builds the chain fixture used in scenario 2. Run the last block after scenario 2 to prepare scenario 3.

```bash
scratch='<scratch>'
cd "$scratch"
export PYTHONDONTWRITEBYTECODE=1
git init -b main repo
cd repo
git config user.name "Wave rehearsal"
git config user.email "wave-rehearsal@example.invalid"
git config core.autocrlf false
cat >todo.py <<'PY'
VERSION = "0.1.0"


def add(items, text):
    return items + [{"text": text, "done": False}]


def rm(items, n):
    return items[:n - 1] + items[n:]


def list_items(items):
    return [
        f"{n}. {item['text']}"
        for n, item in enumerate(items, 1)
        if not item["done"]
    ]
PY
cat >test_todo.py <<'PY'
import unittest

from todo import add, list_items, rm


class TodoTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add([], "buy milk"), [{"text": "buy milk", "done": False}])

    def test_rm(self):
        items = add(add([], "buy milk"), "post letter")
        self.assertEqual(rm(items, 1), [items[1]])

    def test_list_items(self):
        items = [{"text": "buy milk", "done": True}, {"text": "post letter", "done": False}]
        self.assertEqual(list_items(items), ["2. post letter"])
PY
python -m unittest
git add todo.py test_todo.py
git commit -m init
git init -b main ../triage-repo
git -C ../triage-repo config user.name "Wave rehearsal"
git -C ../triage-repo config user.email "wave-rehearsal@example.invalid"
git -C ../triage-repo config core.autocrlf false
cp todo.py test_todo.py ../triage-repo/
git -C ../triage-repo add todo.py test_todo.py
git -C ../triage-repo commit -m init
```

```bash
cd "$scratch/repo"
index=plans/2026-11-17-todo/index.md
base=$(git rev-parse --short main)
mkdir -p "$(dirname "$index")"
cat >"$index" <<EOF
# Todo — index

- Index: \`$index\` · created 2026-11-17 · base: $base
- Flow: autonomous · target: integration/todo
EOF
cat >>"$index" <<'EOF'

## Problems

### P1. Print VERSION with --version

**User's words:** `--version` prints `VERSION`
**Clarifications:** none
**Where:** `todo.py:1` · **Reuse:** `VERSION`
**Likely cause:** There is no version command.
**Difficulty:** low · **Size:** 1 task
**Depends on:** none

### P2. Print a version header in list

**User's words:** `list` prints a header line with the version
**Clarifications:** none
**Where:** `todo.py:12` · **Reuse:** `list_items`, `VERSION`
**Likely cause:** The formatter returns item lines only.
**Difficulty:** low · **Size:** 1 task
**Depends on:** P1 (CLI entry point)

### P3. Include done items with list --all

**User's words:** `list --all` also shows done items
**Clarifications:** none
**Where:** `todo.py:12` · **Reuse:** `list_items`
**Likely cause:** The formatter filters out all done items.
**Difficulty:** low · **Size:** 1 task
**Depends on:** none

### P4. Mark an item done

**User's words:** `done <n>` marks an item done
**Clarifications:** none
**Where:** `todo.py:4` · **Reuse:** item done flag
**Likely cause:** There is no command to mark an item done.
**Difficulty:** low · **Size:** 1 task
**Depends on:** none

## Parts

| Part | Problems | Points | Plan slug | Plan when | Command |
|---|---|---|---|---|---|
| 1 | P1 | 1 | `todo-p1` | now | `/wave-plan plans/2026-11-17-todo/index.md part 1`<br>`$wave-plan plans/2026-11-17-todo/index.md part 1` |
| 2 | P2, P3 | 2 | `todo-p2` | after part 1 merged | `/wave-plan plans/2026-11-17-todo/index.md part 2`<br>`$wave-plan plans/2026-11-17-todo/index.md part 2` |
| 3 | P4 | 1 | `todo-p3` | now | `/wave-plan plans/2026-11-17-todo/index.md part 3`<br>`$wave-plan plans/2026-11-17-todo/index.md part 3` |

A part is planned when its plan folder exists and done when every feature is merged.

## Assumptions

- none

## Open questions

- none
EOF
git add "$index"
git commit -m 'Index todo'
git worktree add -b feat/todo-p1/F1-version-option ../repo.worktrees/todo-p1-F1 main
cat >>../repo.worktrees/todo-p1-F1/todo.py <<'PY'


if __name__ == "__main__":
    import sys

    if sys.argv[1:] == ["--version"]:
        print(VERSION)
PY
git -C ../repo.worktrees/todo-p1-F1 add todo.py
git -C ../repo.worktrees/todo-p1-F1 commit -m 'Add version option'
git worktree remove ../repo.worktrees/todo-p1-F1
git worktree add -b plan/todo-p1 ../repo.worktrees/todo-p1-plan main
cd ../repo.worktrees/todo-p1-plan
readme=plans/2026-11-17-todo/plan-1/README.md
mkdir -p "$(dirname "$readme")"
cat >"$readme" <<'EOF'
# Todo version option

- Plan: `plans/2026-11-17-todo/plan-1/` · slug: `todo-p1` · tracking branch: `plan/todo-p1` · created 2026-11-17
- Index: `plans/2026-11-17-todo/index.md` part 1
- Re-plans: none
- Flow: autonomous · target: integration/todo

## Features

| ID | Slug | Title | P | Tasks (wave) | Done when | Status | Waiting for | Branch | Merged |
|---|---|---|---|---|---|---|---|---|---|
| F1 | `version-option` | Version option | P1 | A (1) | --version prints 0.1.0 | 👀 review | review | `feat/todo-p1/F1-version-option` | |

## Waves

| Wave | File | Tasks | Status |
|---|---|---|---|
| 1 | `waves/w01.md` | A | ✅ |
EOF
git add "$readme"
git commit -m 'Fixture todo-p1: record version option for review'
```

```bash
cd "$scratch/repo"
git worktree add -b integration/todo ../repo.worktrees/integration-todo main
git -C ../repo.worktrees/integration-todo merge --no-ff feat/todo-p1/F1-version-option -m 'Merge the version option'
h1=$(git rev-parse --short integration/todo)
readme=plans/2026-11-17-todo/plan-1/README.md
(
    cd ../repo.worktrees/todo-p1-plan
    python - "$readme" "$h1" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
old = "👀 review | review | `feat/todo-p1/F1-version-option` | |"
new = f"✅ merged | | `feat/todo-p1/F1-version-option` | {sys.argv[2]} |"
content = path.read_text(encoding="utf-8")
assert old in content
path.write_text(content.replace(old, new), encoding="utf-8", newline="\n")
PY
    git add "$readme"
    git commit -m 'Fixture todo-p1: record merged version option'
)
git rev-parse main >"$scratch/main.before"
printf '%s\n' "$h1" >"$scratch/h1"
```

## Scenario 1. Triage assumes

- **Run** — `/wave-triage flow autonomous 1. add a --version option 2. show done items differently in list 3. rename rm to delete` · `$wave-triage flow autonomous 1. add a --version option 2. show done items differently in list 3. rename rm to delete`, in the toy `triage-repo`.
- **Expected** — No question. The flow line immediately follows the index header, P2 has a recorded assumption, and Open questions is `none`. The index is committed and merged into `main`.
- **Seen** — The coordinator interpreted “show” as including done items with strike-through, recorded that choice without asking, and put all three low problems in one part. The two-parent merge `858becc` brought the index commit `f297b5f` into `main`.
- **Result** — holds.

```bash
cd "$scratch/triage-repo"
git show main:plans/2026-11-17-todo-list/index.md | sed -n '1,4p;/^## Assumptions/,$p'
git log -1 --format='%h %P %s' main
```

```text
- Index: `plans/2026-11-17-todo-list/index.md` · created 2026-11-17 · base: 87cbf4f · triaged 2026-11-17 20:47 – 2026-11-17 20:48
- Flow: autonomous · target: integration/todo-list
## Assumptions

- Assumed (autonomous, not asked) · P2: How should done items appear? → show them with strike-through; not chosen: hide them.

## Open questions

- none
858becc 87cbf4ff618805f7d117f52a9c27324b0bdf7bc5 f297b5f4b3074ab93372f3ad38e3aefe5264d0f6 Index todo-list
```

## Scenario 2. Part 1 waits for review

- **Run** — `/wave-plan plans/2026-11-17-todo/index.md part 2` · `$wave-plan plans/2026-11-17-todo/index.md part 2`, in the toy `repo`.
- **Expected** — The first line after `Started:` is a `part-unmerged` stop for F1, with the review action and both merge commands. The ref and worktree snapshots match.
- **Seen** — The flow was inherited from the index. Check 3 read F1 as `👀 review` on `plan/todo-p1`; the run released the claim before reporting the stop. Both `cmp` commands exited 0, and the final ref query printed nothing.
- **Result** — holds.

```text
Started: 2026-11-17 20:49
Stop part-unmerged: part 1 — F1 👀 review (review) — next: review F1, then /wave-run plans/2026-11-17-todo/plan-1 merge F1 · $wave-run plans/2026-11-17-todo/plan-1 merge F1
```

```bash
cd "$scratch/repo"
snap() {
    git for-each-ref --format="%(refname) %(objectname)" >"$scratch/refs.$1"
    git worktree list --porcelain >"$scratch/worktrees.$1"
}
snap before
# Run the coordinator here. Check 3 reads the predecessor with:
git show plan/todo-p1:plans/2026-11-17-todo/plan-1/README.md | grep '^| F1 |'
snap after
cmp "$scratch/refs.before" "$scratch/refs.after"
cmp "$scratch/worktrees.before" "$scratch/worktrees.after"
git for-each-ref refs/heads/integration/todo refs/heads/plan/todo-p2 refs/wave-method/claims/
```

## Scenario 3. Part 2 on the integration branch

- **Run** — `/wave-plan plans/2026-11-17-todo/index.md part 2` · `$wave-plan plans/2026-11-17-todo/index.md part 2`, in the toy `repo` after the scenario 3 fixture update.
- **Expected** — No question. The autonomous plan for P2 and P3 starts from H1, merges into `integration/todo` only, leaves `main` at its original hash, releases the claim, and passes the status checker in its tracking worktree.
- **Seen** — Check 3 accepted `80f3c7b` (H1) from the predecessor's README. All three baseline unit tests passed in the integration worktree. The new plan has a README, two lite solutions, and a wave pairing the CLI edits with tests. Commit `64b49ae` started from H1 and merge `59c5ef2` put it into `integration/todo`. No question was asked. The flow line matched, the ancestor and integration README checks exited 0, and the main README lookup failed as expected. The main snapshot matched (`e55784b`), the claim query printed nothing, and the tracking status check exited 0.
- **Result** — holds.

```bash
cd "$scratch/repo"
plan=plans/2026-11-17-todo/plan-2
h1=$(cat "$scratch/h1")
# Set wave_skills to the absolute path of the skills directory at the start commit.
git show "plan/todo-p2:$plan/README.md" | grep -Fx -- '- Flow: autonomous · target: integration/todo'
git merge-base --is-ancestor "$h1" plan/todo-p2
git cat-file -e "integration/todo:$plan/README.md"
! git cat-file -e "main:$plan/README.md" 2>/dev/null
git rev-parse main >"$scratch/main.after"
cmp "$scratch/main.before" "$scratch/main.after"
git rev-parse --short main
git for-each-ref refs/wave-method/claims/
git log -1 --format='%h %P %s' integration/todo
(cd ../repo.worktrees/todo-p2-plan && python "$wave_skills/wave-plan/scripts/status_check.py" "$plan")
```
