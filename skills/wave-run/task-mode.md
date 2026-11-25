# wave-run — task mode

Read by the `wave-run` coordinator only when `SKILL.md` step 1 says so.

One task in one fresh session, whose model is of the task's tier or higher and which has the task's `Needs`.

- Coordinator: in step 4 prepare the task's worktree (task worktree or feature worktree, see `SKILL.md` step 4) but
  do not launch it. When the other tasks of the wave are merged and checked, end the wave file's Execution with
  `Waiting: task mode <ID>[ (fix <k>/2)], … — next: <commands>`, where `<commands>` is one pair
  `/wave-run <plan folder> <N> task <ID> · $wave-run <plan folder> <N> task <ID>` per ID, in the order of the IDs,
  the pairs separated by `; `, with the plan folder and the wave number written out, never one form alone, for
  example

  ```
  Waiting: task mode A, B (fix 1/2) — next: /wave-run plans/2026-11-02-hop-tuning 3 task A · $wave-run plans/2026-11-02-hop-tuning 3 task A; /wave-run plans/2026-11-02-hop-tuning 3 task B · $wave-run plans/2026-11-02-hop-tuning 3 task B
  ```

  commit `Plan <plan>: wave <N> waiting for task mode` (the wave stays 🔄), and report one command per task in
  launch-group order, in both forms (`layout.md`, "Commands"): `/wave-run <plan folder> <N> task <ID>` ·
  `$wave-run <plan folder> <N> task <ID>` — "fresh session, model: <models of the task's tier> (<tier>), needs
  <tool>".
- Task session (`/wave-run <plan folder> <N> task <ID>` · `$wave-run <plan folder> <N> task <ID>`):
  first apply the tier gate (`layout.md`, "Tier gate"): name the exact model this session runs on; below the
  task's tier, or unknown → stop `tier-mismatch` and do nothing else. Then check the wave is 🔄 with
  `Waiting: task mode` naming `<ID>`, and that the session has the task's `Needs`; otherwise stop
  `capability-missing`. Read only
  `README.md`, the wave file and the solution files the prompt names.
  - Already done: the task has its commits (task branch: `git log feat/<plan>/<feature>..<task branch>` is not
    empty; direct task: a commit after the head recorded in the waiting record whose subject starts
    `<plan> <feature-id> / <task-id>:`) and the waiting line has no `(fix <k>/2)` for it → change nothing; report
    `already committed <short hash>`.
  - Otherwise do the task from its prompt in the
    prepared worktree, commit there, adding the task's files by name and no generated files (as the header of `SKILL.md` step 4 says) (`<plan> <feature-id> / <task-id>: <short>`, with the trailer
    `Wave-Model: <exact model ID>` in one trailer block with any other trailer), run the check command,
    write nothing under `plans/`, and report the result in the language of the user's messages in this session
    and the next command `/wave-run <plan folder> <N>` · `$wave-run <plan folder> <N>`.
  - The last commit of the task carries the report's `Done:`, `Try:`, `Not checked:` and `Problems:` lines as one
    paragraph of its body, right before the trailer block, so the resume can read them (`SKILL.md` step 5).
  - Coordinated run: end with the `task` return line of `layout.md`, "Coordinated runs", instead of the report.
- Resume (`/wave-run <plan folder> <N>` · `$wave-run <plan folder> <N>` on a wave waiting for task mode):
  check each waiting task as in
  `SKILL.md` step 5 (including its tier gate), merge as in `SKILL.md` step 6, then continue with the remaining steps. A waiting task without commits is
  reported again with its command; the wave keeps waiting.

End your report with exactly this block (one item per line, "none" when empty):
Model: <the exact model ID this session runs on>
Done: <what changed for the user or the project, in one or two plain sentences, not file names>
Try: <the actions specific to this change that show it works → what one should see; not how to build, start or test the project; "none" when nothing is visible>
Changed: <files>
Checked: <command> → <result>
Not checked: <what, and why>
Problems: **[wave <N> / task <ID> / feature <F>] <essence>** — where: <file:line>; expected / got; proposal: <…>

## Fix requests

When the resume must change a task's work (`SKILL.md`, "Fix loop") and has no subagent to send it to, it writes
into the wave file's "Execution" a line `Fix <ID> <k>/2: <what to change; the error text, at most 20 lines>` and
ends the Execution again with the waiting line, the task marked `(fix <k>/2)`, committed as
`Plan <plan>: wave <N> waiting for task mode`. A task session whose ID carries that mark reads the last
`Fix <ID> <k>/2` line, makes that change on the task's branch in the prepared worktree, commits it with a new
report block, and runs the check. After the second attempt the task is ⚠️ as "Fix loop" says.
