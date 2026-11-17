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

- Re-run (2026-11-17): Claude Code 2.1.326. Q-d and the chain rehearsal used project skills installed from
  the branch containing the merged autonomous-flow skills. Q-a to Q-c used repositories without wave skills.

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

- <https://code.claude.com/docs/en/permissions> ("Configure permissions"): a classifier reviews actions in
  `auto`. `dontAsk` denies calls that would prompt and permits preapproved calls. `bypassPermissions`
  skips most approval prompts and is intended for isolated environments. The CLI reference also lists
  `--permission-prompts none` for denying calls that would prompt.

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

P-f tested four flag combinations. Q-a and Q-b record the later runs of the two additional permission modes.

### Q-a: auto mode

Q-a through Q-c used the same Git Bash prompt, each in a fresh repository with one README commit:

```bash
prompt='Do these steps as separate commands and report each as done or refused: 1. create probe.txt containing x; 2. git add probe.txt; 3. git commit -m probe; 4. git worktree add -b feat/probe ../wt-probe; 5. in ../wt-probe create b.txt and commit it; 6. back in this folder run git merge --no-ff feat/probe -m merge-probe; 7. python -c "print(1)".'
MSYS_NO_PATHCONV=1 claude -p "$prompt" --model haiku --max-turns 15 --max-budget-usd 0.5 --output-format json --permission-mode auto < /dev/null
```

Exit 0, subtype `success`, no permission denials. All seven steps completed. The Git log and worktree list
confirmed both commits, the sibling worktree and the merge. Claude reported Python output `1`.

### Q-b: dontAsk with and without an allowlist

```bash
MSYS_NO_PATHCONV=1 claude -p "$prompt" --model haiku --max-turns 15 --max-budget-usd 0.5 --output-format json --permission-mode dontAsk < /dev/null
MSYS_NO_PATHCONV=1 claude -p "$prompt" --model haiku --max-turns 15 --max-budget-usd 0.5 --output-format json --permission-mode dontAsk --allowedTools "Write,Edit,Bash(git *),Bash(python *)" < /dev/null
```

Both exited 0 with subtype `success`.

| Step | Without allowlist | With allowlist |
|---|---|---|
| 1. Write probe.txt | Refused | Done |
| 2. Stage probe.txt | Skipped | Done |
| 3. Commit probe.txt | Skipped | Done |
| 4. Add sibling worktree | Refused | Done |
| 5. Write and commit b.txt | Skipped | File written, commit refused |
| 6. Merge | Skipped | Skipped |
| 7. Run Python | Refused | Refused |

Without the list, `permission_denials` contained the Write call and the Bash worktree and Python calls. With the
list, it contained a compound Bash call starting with `cd ../wt-probe` and a PowerShell Python call. The model
combined commands at step 5 despite the instruction to run separately, and the Python rule covered Bash.

### Q-c: turn off permission prompts

```bash
MSYS_NO_PATHCONV=1 claude -p "$prompt" --model haiku --max-turns 15 --max-budget-usd 0.5 --output-format stream-json --verbose --permission-prompts none < /dev/null
```

Exit 0, subtype `success`. `AskUserQuestion` was absent from `system/init`. `permission_denials` covered step 1
(Write), step 4 (Bash worktree) and step 7 (Bash Python). Steps 2, 3, 5 and 6 were skipped, and the repository
stayed at its initial commit.

### Q-d: Windows PowerShell and PowerShell 7

The toy repository had the skills installed and three passing unit tests. The commands below ran in
`powershell -NoProfile -File <scratch>/q-d.ps1` (5.1.26100.9818) and
`pwsh -NoProfile -File <scratch>/q-d.ps1` (7.6.9).

```powershell
$common = @('--model', 'haiku', '--max-budget-usd', '0.5', '--setting-sources', 'project,local', '--output-format', 'json')
$prompt = @'
Repeat the text after the colon exactly, nothing else:
"quoted"
$HOME
one ` | two
'@
$out = $null | claude -p "/wave-status" @common --max-turns 15
$exitCode = $LASTEXITCODE
($out | ConvertFrom-Json).subtype
$out = $null | claude -p $prompt @common --max-turns 15
$exitCode = $LASTEXITCODE
($out | ConvertFrom-Json).result
$out = $null | claude -p "/wave-status" @common --max-turns 1
$exitCode = $LASTEXITCODE
($out | ConvertFrom-Json).subtype
```

| Call | Windows PowerShell 5.1 | PowerShell 7 |
|---|---|---|
| Status | Exit 0, `success`. `Started:` appeared only in the footer after a compound Bash permission denial. | Exit 0, `success`. `Started:` appeared first. No denials. |
| Here-string | Exit 0, `success`. Both double quotes were lost. The dollar sign, backtick and pipe survived. No denials. | Exit 0, `success`. All three lines matched after normalizing line endings. No denials. |
| One-turn status | Exit 1, `error_max_turns`. No denials. | Exit 1, `error_max_turns`. No denials. |

No call emitted the stdin timeout warning. A 5.1 retry passed `$prompt.Replace('"', '\"')` as the prompt.
It exited 0 with subtype `success`, no permission denials and an exact match after line-ending normalization.

### Chain runs (R1–R3 and R6)

See the [chain rehearsal](rehearsals/print-mode-chain.md) for the commands and repository checks. The plan had
one wave, so R4 and R5 were unnecessary.

| Run | Skill | Exit | Subtype | Turns | Cost (USD) | Minutes | Denials | Stop line |
|---|---|---:|---|---:|---:|---:|---:|---|
| R1 | wave-triage | 0 | success | 8 | 0.3803526 | 0.860 | 0 | none |
| R2 | wave-plan | 0 | success | 16 | 0.8076864 | 1.822 | 0 | none |
| R3 | wave-run | 0 | success | 20 | 0.562945385 | 2.111 | 0 | none |
| R6 | wave-status | 0 | success | 6 | 0.01326129 | 0.502 | 0 | none |

## Result

All four wave skills ran via leading slash commands in print mode. The rehearsal created an autonomous index,
planned its single part, executed the single wave and reported the merged feature. Both `Agent` calls returned
before the final stream event. The merged feature and passing tests were verified in the integration worktree.

Use `MSYS_NO_PATHCONV=1` in Git Bash to preserve the leading slash. PowerShell passed the slash intact and
`$null | claude` closed stdin without a timeout warning in both versions. For a plugin install, grant access
to its folder with `--add-dir`.

The rehearsal used `bypassPermissions`. The seven-step write, worktree, merge and Python probe also completed under
`auto`. The `dontAsk` allowlist covered the initial commit and worktree creation. The remaining operations failed
or were skipped. A `success` result can accompany tool denials or an incomplete report.

## Prompt form for the driver

```bash
MSYS_NO_PATHCONV=1 claude -p "$prompt" --output-format json --permission-mode bypassPermissions --model "$model" --max-turns "$turnCap" --max-budget-usd "$budgetCap" < /dev/null
```

Use `bypassPermissions` in a repository owned by the driver in an isolated environment. `auto` is an alternative
that passed Q-a on this account. Check tool denials and repository state after each call. Use
`--setting-sources project,local` to exclude the user's installed plugin if needed. For a plugin install, use
`--add-dir <plugin folder>` and the `wave-method:` prefix. Avoid `--bare` because it skips skill auto-discovery and
does not read the subscription login.

Start the prompt with the slash command and invoke one skill per call. Caps for the first three skills are three
times the largest measurements, rounded up to tens of turns and whole dollars. `wave-status` retains its prior
60-turn and $0.50 caps.

| Skill | Prompt | Model | Turns | USD | Rehearsal |
|---|---|---|---:|---:|---|
| `wave-triage` | `/wave-triage flow autonomous <list>` | `opus` | 30 | 2 | R1 used an inline numbered list. |
| `wave-plan` | `/wave-plan flow autonomous <index path> part <K>` | `opus` | 50 | 3 | R2. |
| `wave-run` | `/wave-run <plan folder> <N>` or `/wave-run <plan folder>` for the next ⬜ or ❌ wave | `sonnet` or higher | 60 | 2 | R3 used next-wave selection. Explicit numbering was unnecessary for the single-wave plan. |
| `wave-status` | `/wave-status` or `/wave-status <plan folder>` | `haiku` | 60 | 0.50 | R6 reported all plans to check the complete pipeline. A folder-scoped call was unnecessary for the single plan. |

Use `/wave-run <plan folder> flow autonomous [review <F-IDs>]` only to switch a manual plan into autonomous flow
or change the manual-review list. The rehearsal plan already used autonomous flow and the default review list.
The plugin namespace was outside the project-install rehearsal. A wave with high-tier tasks needs high-tier subagents.

Put a multiline PowerShell prompt in a single-quoted here-string. For the embedded double quotes tested in Q-d,
Windows PowerShell 5.1 needed a backslash before each quote. PowerShell 7.6 used the literal value.

```powershell
$nativePrompt = $prompt
if ($PSVersionTable.PSVersion.Major -eq 5) {
    $nativePrompt = $prompt.Replace('"', '\"')
}
$out = $null | claude -p $nativePrompt --output-format json --permission-mode bypassPermissions --model $model --max-turns $turnCap --max-budget-usd $budgetCap
$exitCode = $LASTEXITCODE
if ($out) {
    $result = $out | ConvertFrom-Json
}
```

Reading the result:

1. A non-zero exit code means the run failed. Read `subtype` and `errors` where JSON is available. A turn or budget
   cap, API or authentication error, or termination can leave no `result` field.
2. If the exit code is 0, `is_error` is false and `subtype` is `success`, the report is in `result`. Expect
   `Started: <time>` on its first line. Parse an immediately following `Stop <code>:` line by splitting it at
   the first ` — next: `. In the absence of a stop line, read the next command from the report, for example
   `Next:` in `wave-status`.
3. Treat unexpected output as a failed check even on exit 0. A nonempty `permission_denials` array can mean skipped
   checks or guessed output. A missing first-line `Started:` means skill loading or report formatting needs
   inspection. A closing question requires attention because autonomous flow does not ask.
4. Before continuing, verify the README statuses, wave execution record and Git refs. Read the merged-feature
   details even if the section heading varies, as it did in R6.

## Open points

- P-c completed with 12 reported turns under a cap of 10, while P-e and Q-d failed at the one-turn cap. Repeated
  runs near the cap would help relate CLI turn enforcement to `num_turns`.
- The chain measured one small wave with two completed `Agent` calls. Rehearse a larger multi-wave plan with
  background subagents and inspect the stream through process exit to measure wait behavior and validate the caps.
- R6 reported the full F1 block under a repeated, unexpected heading. Re-run `wave-status` on plans with several
  merged features and compare the report against the tracking and integration refs before depending on heading-based
  extraction.
