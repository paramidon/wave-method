# F3 · Codex polish found by the CLI rehearsal

- Branch: `feat/desktop-coordinator-p2/F3-codex-coordinator-polish` · worktree:
  `D:\Documents\orbits\wave-method.worktrees\desktop-coordinator-p2-F3`
- 👀 review since 2026-11-27 22:51

## Essence

Before: a Codex coordinator could write text of its own and ask its questions through an input tool that only sleeps in
`codex exec`, and on Windows nothing said why your own git refuses the worktrees Codex made. After: the skill forbids
both, and README and the layout explain the refusal and how to review such a branch.

## How to test

1. In the feature worktree, `git grep -n request_user_input_async -- skills` -> one rule in
   `skills/wave-auto/SKILL.md`: questions are asked as the text of the answer, never through an input tool.
2. Open README "Codex permissions", the paragraph "On Windows the worktrees ..." -> it names `detected dubious
   ownership`, review from the main checkout, and both `safe.directory` commands with `'<worktree path>'`.

## Worth a look

The behaviour in Codex was not rehearsed in this plan: a later Codex run shows it, and its findings go to a new plan.
The `--global` form of the `safe.directory` command was only run against a scratch config file.

## Tasks

- AA (wave 14) — the coordinator skill says to read the clock before writing anything, never to restate questions,
  results or plans, and to ask its questions as the text of the answer, without an input tool.
- AB (wave 14) — README and the layout say that git outside the Codex sandbox on Windows refuses the worktrees Codex
  made, and name two ways to review such a branch.
- AE (wave 16) — the README command that allows a worktree for good now names the worktree path.

## Check

`python skills/wave-plan/scripts/test_status_check.py`, `status_check.py` on each of `examples/*/`,
`git diff --check main` -> 39 tests OK, three examples pass, no whitespace errors (141adb8); tests added or changed:
none
