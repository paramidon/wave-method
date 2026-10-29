# wave-run — deferred merges

Wave skill set version 1 (see `.claude/skills/wave-plan/layout.md`, "Version").
Read by the `wave-run` coordinator only when `SKILL.md` step 1 says so.

A feature stays `✅ ready` with `Waiting for: main-dirty` when the main checkout was not ready for its merge
(`layout.md`, "Main readiness"). Every later `/wave-run <plan folder>` merges such features first:

- In a wave run: right after `SKILL.md` step 2, run "merge one feature" (`SKILL.md` step 7) for each of them, in "Features" order, and
  record them in the "wave N started" commit (rows `✅ merged` with hash and empty `Waiting for`; a line
  `Merged <YYYY-MM-DD HH:MM>: <feature-id> <hash>` in the Execution of the wave file whose wave made it ready). A
  feature still blocked by the main checkout keeps its row; the wave runs anyway.
- Without a wave (no wave ⬜ or ❌): `SKILL.md` steps 1 (lock and repair checks only) and 2 (tracking worktree, no "started"
  commit), then the same merges, then `SKILL.md` step 8 for these features only, with **one** commit
  `Plan <plan>: merge — <parts>`, where `<parts>` joins with `; ` only the parts that apply, in this order:
  `<IDs> merged`, `<IDs> blocked`, `archived` (for example `merge — F1 merged; archived`, `merge — F1 blocked`).
  If nothing changed, write nothing and report the reason. No feature `✅ ready` either → stop `nothing-to-run`.
