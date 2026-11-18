# F1 · Overnight driver with rails and a morning report

## How to test

- A: Read the snapshot for an index with a dependency on part 1 → a feature under review in part 1 holds part 2 back; part 2 becomes ready once the required features are merged or dropped.
- B: Pass a result with a `Stop wave-running: x — next: y` line immediately after `Started:` → the runner reports a stop with code `wave-running` and next action `y`.
- C: Acquire an already-held lock → `LockHeld` includes the holder's PID. Create a remote-tracking ref between snapshots → the guard reports the ref by name.
- D: Set `FAKE_CLAUDE_SCENARIO` to a two-step scenario and invoke the stub twice with `-p` → it returns both steps in order, logs both calls, and records step count `2`.

## Tasks

- A (wave 1) — The driver reads plan state from Git and checks whether dependent parts can proceed based on feature statuses and merge history.
- B (wave 1) — The Claude Code runner launches headless calls, terminates the process tree on timeout, classifies JSON results, and saves raw output when requested.
- C (wave 1) — Added the run lock, UTF-8 log, deadline, limits, and Git guard. The guard compares refs, HEAD, and the porcelain status of tracked files.
- D (wave 1) — The Claude CLI stub plays back scenarios, checks arguments, updates Git refs using a temporary index, and emits JSON for driver integration tests.
