# Lite solutions (low problems)

## P7. Verify how `claude -p` runs skills, and record the prompt form for the driver
User problem: check the current Claude Code docs and real `claude -p` runs: do skills and slash commands such as
`/wave-run …` work in print mode, or must the prompt name the skill in words; record the result for the driver
(part 3) · feature F3

**Edit:** create `docs/claude-print-mode.md` (new; no other file changes). Sections, in this order:

1. `## Environment` — date, OS, `claude --version`, how the skills were installed in the scratch repository
   (`install.sh` / `install.ps1 <scratch repo>`, project install), the model used for the probes.
2. `## What the docs say` — the URLs read (Claude Code docs pages on headless / print mode, skills, slash commands,
   CLI reference), with the date read, and what each says about skills and slash commands in `-p`; one short quote at
   most per page, under 15 words.
3. `## Probes` — one subsection per probe, each with the exact command, the exit code, and the observed result in 2–5
   lines (trimmed output). Probes, all in a throwaway git repository outside this repository, with the wave skills
   installed into it and a tiny plan copied from `examples/02-bugfix-batch`:
   - P-a `claude -p "/wave-status"` — does the skill expand (its "Started:" line and plan table appear)?
   - P-b `claude -p "Use the wave-status skill to report the status of every plan in plans/."`
   - P-c the same two with the plugin-style install, if the installer offers one; else write "not available".
   - P-d `--output-format json` on P-b: the top-level fields seen (for example `result`, `is_error`, `num_turns`,
     `session_id`, `total_cost_usd`); which one carries the final answer.
   - P-e the exit code and JSON when the run hits `--max-turns 1`, and when the prompt makes the model want to ask
     the user a question (for example "Ask me which plan to show, then show it"): does the run end, hang, or answer?
   - P-f which permission flags let a run write files and run git without prompts (`--permission-mode`,
     `--allowedTools`, `--dangerously-skip-permissions` — only test what the docs list; record what each did).
4. `## Result` — one paragraph: does a slash command run a user-invoked skill in `-p`; does naming the skill in words
   work; which form is reliable.
5. `## Prompt form for the driver` — the exact prompt templates the part 3 driver should use for `wave-triage`,
   `wave-plan`, `wave-run` (with `flow autonomous`) and `wave-status`, the flags of every call, how to read the final
   report and stop line (`Stop <code>: …`) from the output, and how to detect a failed run (exit code, `is_error`).
6. `## Open points` — anything the probes could not settle.

Keep every probe cheap: the smallest model that runs skills, `--max-turns` as low as the probe allows. Never use the
user's real projects or this repository's branches; delete nothing outside the scratch folder.

**Check:** `docs/claude-print-mode.md` exists with the six `## ` sections in that order; every probe P-a…P-f has a
command, an exit code and an observed result (or "not available" with the reason); "Prompt form for the driver"
names one prompt per skill. `git diff --stat main` lists only `docs/claude-print-mode.md`.
