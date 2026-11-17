# Claude Code print mode and the wave skills

This file records how `claude -p` (print mode) runs the wave skills. It is based on the current Claude Code docs and
real runs. It is the input for the part 3 driver, which runs the skills unattended.

## Environment

- Date: 2026-11-17.
- OS: Windows 11 Pro 10.0.26200. The probes ran from Git Bash (MSYS2), with git 2.52.0.windows.1.
- `claude --version`: `2.1.326 (Claude Code)`, the native binary at `~/.local/bin/claude.exe`. It was signed in with
  a claude.ai account (`claude auth status`: `"authMethod": "claude.ai"`). The Claude desktop app also ships a Claude
  Code binary (2.1.325), but that binary was not on `PATH` and was not signed in.
- Scratch repository: a new git repository in a temporary folder outside this repository (`git init -b main`, one
  commit), referred to as `<scratch>/repo` below. The skills were installed with `sh install.sh <scratch>/repo --no-codex`,
  which is a project install into `.claude/skills/wave-*`. The plan `examples/02-bugfix-batch` was copied to
  `plans/2026-11-03-shop-fixes/`, and both were committed.
- Plugin install (P-c): a second scratch repository, `<scratch>/repo2`, had the same plan and no project skills. A
  copy of this repository's `.claude-plugin/` and `skills/` was placed in `<scratch>/plugin` and loaded with
  `--plugin-dir`.
- The user account also has the `wave-method` plugin 2.11.0 enabled. Without `--setting-sources`, the `system/init`
  event listed both the project skills (`wave-status`, …) and the plugin skills (`wave-method:wave-status`, …).
- Probe model: `--model haiku`, which resolved to `claude-haiku-5-5` and loaded and followed the skills. Every
  probe also set `--max-budget-usd 0.5`. There were 13 runs (P-a ran twice, see below), which cost $0.08 in total
  according to `total_cost_usd`.
- Commands are shown as they were run, except that `claude` stands for the binary path and `<scratch>` for the
  temporary folder. From the second P-a run on, every command was run with `MSYS_NO_PATHCONV=1` set and
  `< /dev/null` as stdin (see P-a).

## What the docs say

All pages were read on 2026-11-17.

- <https://code.claude.com/docs/en/headless> ("Run Claude Code programmatically"):
  - A note in "Create a commit" says "User-invoked skills and custom commands work."
  - The same note says `/skill-name` in the prompt is expanded before the run starts.
  - Built-in commands that need the terminal UI, such as `/login`, are not available.
  - Exit code: 0 on success, non-zero when the run fails. A failure inside the run, such as missing authentication,
    is printed as the result on stdout.
  - `--output-format json` returns one result object, with the text in `result`.
  - `--bare` skips skill auto-discovery (only `--add-dir` skills load) and never reads OAuth. The page says it will
    become the default for `-p`.
  - Since v2.1.302 a `-p` run starts in Manual mode when nothing sets a permission mode. A call that needs approval
    is then denied.
  - `--permission-prompts none` removes `AskUserQuestion` and denies anything that would prompt.
- <https://code.claude.com/docs/en/skills> ("Extend Claude with skills"):
  - "Claude uses skills when relevant, or you can invoke one directly with `/skill-name`."
  - The name must start the message. Otherwise it only permits Claude to use the skill.
  - In `-p` only the first skill of a message loads, and the rest of the line becomes its arguments.
  - `disable-model-invocation: true` stops Claude from loading the skill on its own. The wave skills do not set it.
- <https://code.claude.com/docs/en/cli-reference> ("CLI reference"):
  - `--max-turns`: "Limit the number of agentic turns (print mode only)." The flag is documented there but missing
    from `claude --help` in 2.1.326.
  - The page also documents `--permission-mode` (`acceptEdits`, `auto`, `bypassPermissions`, `manual`, `dontAsk`,
    `plan`), `--allowedTools`, `--dangerously-skip-permissions` (the same as `bypassPermissions`),
    `--disable-slash-commands`, `--plugin-dir`, `--add-dir`, `--setting-sources` and `--max-budget-usd`.

## Probes

### P-a: slash command `/wave-status`

First run, from Git Bash:

```
cd <scratch>/repo
claude -p "/wave-status" --model haiku --max-turns 10 --max-budget-usd 0.5 --output-format stream-json --verbose
```

- Exit code 0.
- Git Bash (MSYS) rewrote the argument `/wave-status` to `C:/Program Files/Git/wave-status` before `claude` saw it.
  The model tried to list that path, which was denied.
- Its final answer began "I couldn't read `C:/Program Files/Git/wave-status`", followed by a status table it made
  up without the skill.
- stderr: `Warning: no stdin data received in 3s, proceeding without it.`

Second run, with path conversion and stdin fixed:

```
MSYS_NO_PATHCONV=1 claude -p "/wave-status" --model haiku --max-turns 10 --max-budget-usd 0.5 --output-format stream-json --verbose < /dev/null
```

- Exit code 0. Result: `subtype` `success`, `is_error` false, `num_turns` 10.
- The skill was expanded before the run: the stream has no `Skill` tool call. The model's first action read
  `.claude/skills/wave-plan/layout.md`, which only the skill text names.
- The final answer had the skill's form: the first line was `Started: 2026-11-17 20:10`, followed by the feature
  table, `Waves:`, `Ready for review:`, `Next:` with both command forms, and a `Finished:` line.
- One compound Bash command (`git -C … ; echo ---; …`) was denied in the default Manual mode. The model retried
  with single commands, which ran.

### P-b: skill named in words

```
MSYS_NO_PATHCONV=1 claude -p "Use the wave-status skill to report the status of every plan in plans/." --model haiku --max-turns 10 --max-budget-usd 0.5 --output-format stream-json --verbose < /dev/null
```

- Exit code 0. `success`, `num_turns` 7, no permission denials.
- The model's first call was the `Skill` tool with `{"skill": "wave-status"}`. The next user message began
  "Base directory for this skill: …\.claude\skills\wave-status".
- The final answer started with `Started: 2026-11-17 20:10` and had the same report form as P-a.

### P-c: plugin install

The installer has no plugin option. Instead, the repository's own plugin manifest was loaded with `--plugin-dir`.
`--setting-sources project,local` kept the user's installed 2.11.0 plugin out, and `system/init` listed only
`wave-method` 2.12.0 from `<scratch>/plugin`, with skills `wave-method:wave-*`.

Slash form:

```
cd <scratch>/repo2
MSYS_NO_PATHCONV=1 claude -p "/wave-method:wave-status" --plugin-dir <scratch>\plugin --setting-sources project,local --model haiku --max-turns 10 --max-budget-usd 0.5 --output-format stream-json --verbose < /dev/null
```

- Exit code 0. `success`, `num_turns` 12, even though `--max-turns` was 10.
- The skill was expanded, and the report had the skill's form.
- Reading `<scratch>/plugin/skills/wave-plan/layout.md` was denied with "Path is outside" the working directories.
  The model went on without `layout.md`, so the report did not follow it fully: it had no `Started:` line.

Words form, with the plugin folder added as a working directory:

```
MSYS_NO_PATHCONV=1 claude -p "Use the wave-status skill to report the status of every plan in plans/." --plugin-dir <scratch>\plugin --add-dir <scratch>\plugin --setting-sources project,local --model haiku --max-turns 10 --max-budget-usd 0.5 --output-format stream-json --verbose < /dev/null
```

- Exit code 0. `success`, `num_turns` 8, no permission denials.
- The model called `Skill` with `{"skill": "wave-method:wave-status"}`, then read `layout.md` from the plugin folder.
- The report started with `Started: 2026-11-17 20:12` and ended with `Started: … · Finished: …`.

### P-d: JSON output

```
MSYS_NO_PATHCONV=1 claude -p "Use the wave-status skill to report the status of every plan in plans/." --model haiku --max-turns 10 --max-budget-usd 0.5 --output-format json < /dev/null
```

- Exit code 0. stdout is one JSON object on one line.
- Fields of the object: `type` (`result`), `subtype` (`success`), `is_error` (false), `result`, `num_turns` (7),
  `terminal_reason` (`completed`), `stop_reason` (`end_turn`), `session_id`, `total_cost_usd`, `usage`,
  `modelUsage`, `permission_denials`, `api_error_status`, `duration_ms`, `duration_api_ms`, and several timing
  fields.
- `result` carries the final answer: the skill's report as Markdown.
- One Bash command was denied (`…; date …`). The model then wrote `Started: 2026-11-17 ~20:11`, a guessed time,
  where the skill requires the clock. A permission denial can make a run break a skill rule while still reporting
  `success`.

### P-e: turn limit and a question to the user

Turn limit:

```
MSYS_NO_PATHCONV=1 claude -p "/wave-status" --model haiku --max-turns 1 --max-budget-usd 0.5 --output-format json < /dev/null
```

- Exit code 1.
- The JSON had `subtype` `error_max_turns`, `is_error` true, `terminal_reason` `max_turns`, `stop_reason`
  `tool_use`, `num_turns` 2, `errors` `["Reached maximum number of turns (1)"]` and no `result` field.

Question to the user:

```
MSYS_NO_PATHCONV=1 claude -p "Ask me which plan to show, then show it." --model haiku --max-turns 5 --max-budget-usd 0.5 --output-format stream-json --verbose < /dev/null
```

- Exit code 0 after 6 seconds. `success`, `is_error` false, `num_turns` 2. The run did not hang.
- `AskUserQuestion` was not in the session's tool list.
- The model listed the plan's files and ended with the question as its result: "Which should I show?" and three
  numbered options.

### P-f: permission flags

All four runs used the same prompt in `<scratch>/repo`, which was reset to its base commit before each run:

```
MSYS_NO_PATHCONV=1 claude -p "Create a file probe.txt containing the word x, then run git add probe.txt and then git commit -m probe as two separate commands. Reply with the new commit hash, or with what was refused." --model haiku --max-turns 6 --max-budget-usd 0.5 --output-format json <flags> < /dev/null
```

Every run exited with code 0, `success` and `is_error` false, even when the work was refused.

| `<flags>` | File written | Commit made | `permission_denials` |
|---|---|---|---|
| none (Manual mode) | no | no | `Write` of `probe.txt` |
| `--permission-mode acceptEdits` | yes | no | `Bash` `git add probe.txt` |
| `--permission-mode acceptEdits --allowedTools "Bash(git add *),Bash(git commit *)"` | yes | yes | none |
| `--dangerously-skip-permissions` | yes | yes | none |

`--permission-mode auto` and `dontAsk` were not run: they are documented, but the four runs above were enough to
choose the driver's flags.

## Result

A user-invoked skill runs from a slash command in `claude -p`. The prompt `/wave-status`, or `/wave-method:wave-status`
for the plugin install, is expanded before the run, exactly as the headless docs say. Naming the skill in words also
works, because the model calls the `Skill` tool, but that relies on the model choosing to do so. The slash form is
the reliable one: it needs no model decision, it is what the docs describe, and it passes arguments the same way as
an interactive session (the rest of the line).

Three conditions apply:

- On Windows, a shell must not rewrite the leading `/`. Git Bash does unless `MSYS_NO_PATHCONV=1` is set.
  PowerShell and `cmd` do not rewrite it.
- With the plugin install, the plugin folder must be readable: add it with `--add-dir`.
- The default Manual permission mode denies the writes and git commands that the skills need, so the driver must
  set a permission mode.

## Prompt form for the driver

Flags for every call:

```
claude -p "<prompt>" --output-format json --permission-mode bypassPermissions --model <model of the skill's tier> --max-turns <cap> --max-budget-usd <cap> < /dev/null
```

- `--output-format json` gives one object to parse.
- `--permission-mode bypassPermissions` (the same as `--dangerously-skip-permissions`) is the only tested mode in
  which a skill can write, run git, create worktrees and run the check commands without a list of every command.
  The driver must run only in a repository it owns, and preferably in a container or VM. The narrower alternative
  is `--permission-mode acceptEdits` plus `--allowedTools` for each command the skill runs (`Bash(git *)`,
  `Bash(python *)`, …). A command missing from that list is denied without any error, as P-f shows.
- `--model`: `opus` for `wave-triage` and `wave-plan`. The coordinator of `wave-run` must be medium or higher
  (`sonnet`), but a wave with `high` tasks needs subagents of the high tier. `wave-status` can use `haiku`.
- `--max-turns`: a safety cap, not a target. A run that reaches it fails (P-e). Set it well above a normal run, for
  example 400 for `wave-run` and 60 for `wave-status`.
- `--max-budget-usd`: a per-call spend cap.
- Do not use `--bare`: it skips skill discovery and never reads the subscription login.
- With the plugin install, add `--add-dir <plugin folder>` and use the `wave-method:` prefix. Pass
  `--setting-sources project,local` when the user's own plugin version must not load.
- On Windows from Git Bash, set `MSYS_NO_PATHCONV=1`. Always give stdin explicitly (`< /dev/null`).

Prompts. The skill command must be the first word of the prompt, and only one skill can be used per call:

| Skill | Prompt |
|---|---|
| `wave-triage` | `/wave-triage flow autonomous <the list of problems, one per line>` |
| `wave-plan` | `/wave-plan flow autonomous <index path> part <K>` |
| `wave-run` | Once per plan: `/wave-run <plan folder> flow autonomous`. Then, per wave: `/wave-run <plan folder> <N>` (or `/wave-run <plan folder>` for the next open wave) |
| `wave-status` | `/wave-status` or `/wave-status <plan folder>` |

Plugin install: `/wave-method:wave-triage …`, and the same for the other skills.

Reading the result:

1. A non-zero exit code means the run failed: for example `error_max_turns`, a budget cap, an API or auth failure,
   or SIGTERM (exit 143). Read `subtype` and `errors` from the JSON. In this case there may be no `result`.
2. If the exit code is 0, `is_error` false and `subtype` `success`, the report is in `result`. Its first line is
   `Started: <time>`. If the next line starts with `Stop <code>:`, it is the stop line. Parse it as
   `Stop <code>: <one line> — next: <command or action>`, split on the first ` — next: `. A run without a stop line
   finished its step normally. Its next command follows the skill's report, for example `Next:` in `wave-status` and
   the next command in `wave-run`.
3. Treat the run as failed, even with exit code 0, when:
   - `permission_denials` is not empty: the skill may have skipped or guessed a step (P-d, P-f);
   - `result` has no `Started:` line: the skill most likely did not load (the first P-a run);
   - `result` ends with a question to the user: autonomous flow never asks, so a question means the skill was not
     followed (P-e).
4. Do not trust the report alone. Read the repository state that the skill writes (README statuses, the wave
   file's "Execution", branches) before starting the next call.

## Open points

- `num_turns` does not equal the turn limit. P-c reported 12 turns under `--max-turns 10` and completed, while P-e
  reported 2 turns and failed under `--max-turns 1`. Caps must therefore be generous, and real runs should measure
  them.
- No full `wave-run`, `wave-triage` or `wave-plan` run was probed, only `wave-status`. Subagents launched by
  `wave-run` in `-p` (their models, permissions, and the 10-minute wait for background work at exit) and the length
  of a real wave are unmeasured.
- `--permission-mode auto`, `dontAsk` and `--permission-prompts none` were not tested. `auto` may be a safer choice
  than `bypassPermissions` for a night run if its classifier allows git worktrees and merges.
- The `flow autonomous` arguments of `wave-triage` and `wave-plan` come from part 2's feature F1, which is not
  merged into `main` yet. Check the final argument form once it is merged.
- PowerShell was not probed. It does not rewrite a leading `/`, but the driver's quoting there is untested.
