# History

## Re-plan 2026-11-17 (at ff668d6): I1–I4

Wave 1 left F1 ⚠️ blocked with four open entries from task E's audit. All four concern the checks of
"Chained parts and the integration branch" (`skills/wave-plan/layout.md` on the F1 branch), so they are one new
solution, `solutions/P12-chain-safety.md`, and one new wave of F1 fix tasks.

- I1 (manual predecessor without a tracking branch) → a fixed source order for part J's README: tracking branch,
  `<main branch>`, integration branch (tasks I, J).
- I2 (`plan-exists` after the first write) → a read-only check 0 before any write; step 9 points to it (tasks I, J).
- I3 (two runs pass the 🔄 check together) → the target claim, an atomic git ref taken by every run that writes the
  integration worktree; the 🔄 read stays as a second guard (tasks I, J, K). Alternatives not taken: a lock file in
  `.git/` (per-worktree git dirs, no portable atomic create across bash and PowerShell) and a commit on a tracking
  branch (two plans, two branches).
- I4 (no live run) → two rehearsals that run the skill texts in scratch repositories and keep their records in
  `docs/rehearsals/` (tasks L, M). They run after I, J and K, so they rehearse the fixed texts.

Nothing of waves 1 and 2 changes: wave 2 (F2, F3) does not touch F1's branch and runs first. Task A and task E stay
⚠️ until wave 3 closes their entries.

## Re-plan 2026-11-17 (at 855d09b): I5–I6

Wave 2 left F3 ⚠️ blocked with two open entries from task H: its probes covered `wave-status` only (I5), and its
prompt table used F1's argument forms before F1 was merged (I6). Both concern `docs/claude-print-mode.md` and the
driver form, so they are one new solution, `solutions/P13-print-mode-runs.md`, and one new wave of F3 tasks.

- I6 was checked against F1's branch at 1c65676 during the re-plan: the `flow autonomous` forms of `wave-triage` and
  `wave-plan` match; the table's "Once per plan: `/wave-run <plan folder> flow autonomous`" does not, because a plan
  of an autonomous index already carries its `Flow:` line. Task O corrects the table; task N runs the forms on the
  merged texts, since wave 3 may still change them.
- I5 → task N runs one real chain (triage, plan, `wave-run`, status) under `claude -p` in a scratch toy repository
  and records it in `docs/rehearsals/print-mode-chain.md`; task O probes `auto`, `dontAsk`,
  `--permission-prompts none` and PowerShell, then rewrites the doc's result, prompt form and open points.
- Wave 4 waits for `F1 merged`: the installer must install skill texts that contain F1. F2 was merged into `main`
  (47d69de) before this re-plan; nothing of F2 changes.

Task H and wave 2 stay ⚠️ until wave 4 closes I5 and I6.
