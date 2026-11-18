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

## Re-plan 2026-11-17 (at 06e0731): I7–I8

Wave 3 closed I1–I4 but left F1 ⚠️ blocked with two open entries about the target claim. Both concern the
"Target claim" subsection of `skills/wave-plan/layout.md` on the F1 branch, so they are one new solution,
`solutions/P14-claim-handoff.md`, and one new wave of F1 fix tasks.

- I7 (two resumes adopt one claim) → a waiting form of the claim, written by compare-and-swap when a wave ends with
  `Waiting: task mode …`, and a takeover by compare-and-swap from that waiting oid; a run token in every holder line,
  because two runs of one plan and wave in the same minute stored the same blob and so shared one oid (task P).
  Measured on git 2.52.0.windows.1: 10 rounds of two concurrent takeovers → one success each round.
- I8 (a refused claim writes a blob) → the guarantee is stated for refs, worktrees and commits; the unreachable blob
  is documented (git refuses a ref to a missing object, so the blob cannot be avoided) (task P).
- Task Q rehearses both and appends scenarios 7 and 8 to `docs/rehearsals/chained-parts-safety.md`.

Wave order: wave 4 (F3) depends on `F1 merged`, and `wave-run` refuses a wave while an earlier one is ⬜
(`earlier-wave-open`), so a wave 5 of F1 fixes could never start. Wave 4 is ➖ dropped; its tasks N and O run
unchanged as S and T in wave 6, after wave 5 and F1's merge. I5 and I6 now point to S and T.

Tasks I and M and wave 3 stay ⚠️ until wave 5 closes I7 and I8.

## Re-plan 2026-11-17 (at 16d9953): I9–I10

Wave 6 finished F3, and the user merged it (5db5e02) with two open entries from task S's chain, both about what the
part 3 driver can rely on. F3 is merged, so the fixes form a new feature F4 with one solution,
`solutions/P15-multiwave-status-checks.md`, and one wave of three chained tasks.

- I9 (the merged-feature label varied in R6) → `wave-status` gets a fenced report template with literal labels and a
  "Before sending" check, modelled on `wave-run/report.md`; the label is pinned to the branch name alone
  (`Merged, not in main:`) (task U). Separately, the driver stops reading report headings: reading rule 4 of
  `docs/claude-print-mode.md` takes merged features from the README on the tracking branch and
  `git merge-base --is-ancestor` (task W). Alternative not taken: lenient heading matching in the driver, since labels
  follow the user's language.
- I10 (one small wave only) → a second chain with a six-item list that needs several waves, one `wave-run` call per
  wave, a subagent table and a post-exit check (refs, worktrees and `claude.exe` processes 120 s after exit), recorded
  in `docs/rehearsals/print-mode-multiwave.md` (task V); its two `wave-status` calls also check task U's template on a
  plan with several merged features. Task W recomputes the caps over both chains.

Wave 6 stays ⚠️ until wave 7 closes I9 and I10; F3 stays ✅ merged.

## Re-plan 2026-11-17 (at 6ad9095): I9–I11

Wave 7 left F4 ⚠️ blocked: task V's chain planned a single wave with no parallel launch group (I10 open), M10 wrote
the wrong main branch name and appended a correction (I9 open), and M9 and M10 opened with the plan header instead of
`Started:` (I11). F4 is not merged, so the fixes stay in F4: one solution,
`solutions/P16-status-format-fixture-chain.md`, and one wave of three chained tasks.

- I11 → the `wave-status` template opens with `Started:`; "Before sending" checks the first and the last line
  (task X). The shared run-times rule stays: `wave-run` already follows it.
- I9 → `wave-status` resolves the main branch name with `git rev-parse --verify --quiet refs/heads/main`, else
  `master`, and no longer lists both spellings as examples; a report is one message with nothing after the times
  line (task X). Task Y checks the label on `master` (C5, C6), on `main` after a rename (C7) and with nothing left to
  merge (C8).
- I10 → task Y no longer lets `wave-plan` decide the plan's shape: it runs the ready two-wave plan of
  `examples/01-greenfield-todo-cli/` (each wave one launch group of two tasks of different features), switched to
  autonomous flow by the flow form; a direct probe call (C4) measures what `claude -p` does with background
  subagents when the main agent ends. Alternatives not taken: another toy list (the planner may still merge tasks),
  and forcing background launches in `wave-run` (not what the driver needs to know).
- Task Z rewrites the reading rules 2 and 3 of `docs/claude-print-mode.md` for the new first line, adds rule 5 only
  if background subagents outlive the process, and recomputes the caps over the three chains.

Waves 6 and 7 and task V stay ⚠️ until wave 8 closes I9–I11; F4 stays ⚠️ blocked, waiting for wave 8.
