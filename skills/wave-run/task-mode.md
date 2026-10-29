# wave-run — task mode

Wave skill set version 1 (see `.claude/skills/wave-plan/layout.md`, "Version").
Read by the `wave-run` coordinator only when `SKILL.md` step 1 says so.

One task in one fresh session, whose model is of the task's tier or higher and which has the task's `Needs`.

- Coordinator: in step 4 prepare the task's worktree (task worktree or feature worktree, see `SKILL.md` step 4) but
  do not launch it. When the other tasks of the wave are merged and checked, end the wave file's Execution with
  `Waiting: task mode <IDs> — next: <commands>`, commit `Plan <plan>: wave <N> waiting for task mode` (the wave
  stays 🔄), and report one command per task in launch-group order, in both forms (`layout.md`, "Commands"):
  `/wave-run <plan folder> <N> task <ID>` · `$wave-run <plan folder> <N> task <ID>` —
  "fresh session, <tier> model, needs <tool>".
- Task session (`/wave-run <plan folder> <N> task <ID>` · `$wave-run <plan folder> <N> task <ID>`):
  check the wave is 🔄 with `Waiting: task mode`
  naming `<ID>`, and that the session's model and tools fit; otherwise stop `capability-missing`. Read only
  `README.md`, the wave file and the solution files the prompt names. Do the task from its prompt in the
  prepared worktree, commit there (`<plan> <feature-id> / <task-id>: <short>`), run the check command, write
  nothing under `plans/`, and report the result in the language of the user's messages in this session
  and the next command `/wave-run <plan folder> <N>` · `$wave-run <plan folder> <N>`.
- Resume (`/wave-run <plan folder> <N>` · `$wave-run <plan folder> <N>` on a wave waiting for task mode):
  check each waiting task as in
  `SKILL.md` step 5, merge as in `SKILL.md` step 6, then continue with the remaining steps. A waiting task without commits is
  reported again with its command; the wave keeps waiting.

End your report with exactly this block (one item per line, "none" when empty):
Changed: <files>
Checked: <command> → <result>
Not checked: <what, and why>
Problems: **[wave <N> / task <ID> / feature <F>] <essence>** — where: <file:line>; expected / got; proposal: <…>
