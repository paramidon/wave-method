# F2 · End-to-end runs of both flows on scratch repositories, and the fixes they found

- Branch: `feat/flow-modes-p4/F2-end-to-end-rehearsal` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p4-F2`

## How to test

- K: Commit an out-of-scope file in a scratch task and delete it in a second commit. Wave-run detects the path in the commit history, records a problem and blocks auto-approval.
- L: In a copy of example 03, put `abc123` in F4's `Merged` cell. The checker exits with code 1 and emits one `merged-fields` diagnostic.
- M: Compare task C's README requirements with P2 in example 01. The command table and the example session give the required output, including `added 2: call Bob`.

## Tasks

- K (wave 5) — Check every task commit for out-of-scope files and require clean scope for auto-approval.
- L (wave 5) — Reject merge hashes on unmerged features and limit merge records to the affected feature rows.
- M (wave 5) — Supply the full README session for example 01 and record the fixes in the changelog.
