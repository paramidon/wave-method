# F2 · End-to-end runs of both flows on scratch repositories, and the fixes they found

- Branch: `feat/flow-modes-p4/F2-end-to-end-rehearsal` · worktree: `D:/Documents/orbits/wave-method.worktrees/flow-modes-p4-F2`

## How to test

- K: Commit an out-of-scope file in a scratch task and delete it in a second commit. Wave-run detects the path in the commit history, records a problem and blocks auto-approval.
- L: In a copy of example 03, put `abc123` in F4's `Merged` cell. The checker exits with code 1 and emits one `merged-fields` diagnostic.
- M: Compare task C's README requirements with P2 in example 01. The command table and the example session give the required output, including `added 2: call Bob`.

- P: Use Git to read the model from a task commit with a contiguous trailer block.
- R: In the autonomous rehearsal record, follow the scope finding for stray.txt to the revert and the empty merge cells of the blocked features.

- S: Run example 01's CI command from F3 before F1 merges. CI passes when pytest collects no tests.
- T: Compare the time in a Merged entry with the merge commit's committer time in Git. The two values match.

## Tasks

- K (wave 5) — Check every task commit for out-of-scope files and require clean scope for auto-approval.
- L (wave 5) — Reject merge hashes on unmerged features and limit merge records to the affected feature rows.
- M (wave 5) — Supply the full README session for example 01 and record the fixes in the changelog.
- P (wave 7) — Require a single trailer block and verify the model with Git.
- R (wave 7) — Complete the isolated autonomous rehearsal and verify that the scope gate reverts out-of-scope work and holds the feature back.
- S (wave 8) — Make example 01's CI independent of the application package so F3 can pass in isolation.
- T (wave 8) — Take Merged entry times from their merge commits in manual and autonomous flow.
