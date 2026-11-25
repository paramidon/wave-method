# P2. The coordinator and the wave skills in Codex (CLI and desktop app)

User problem: `/wave-auto` works only in Claude Code; the same coordinator should run from the Codex CLI and the
Codex desktop app (`$wave-auto …`) · feature F1

## Cause

The skills are written vendor-neutrally, but three things are Claude-only or unknown for Codex:

- **Model tiers** name no GPT model for `low` and `high` (`skills/wave-plan/layout.md:103-107`): a Codex coordinator
  cannot choose a model for a `low` or `high` step, and the tier gate cannot place a GPT model ID in a tier.
- **The tier gate's executor check** (`skills/wave-plan/layout.md:120-123`) needs the executor to name its exact model
  "from its own environment (system prompt, model ID)". A Codex model cannot: probed below, every Codex agent answers
  `Unknown` → every `medium` and `high` task and step stops `tier-mismatch`.
- **Model choice** in `wave-auto` is spelled for Claude Code only (`skills/wave-auto/SKILL.md:61-67`: `haiku`, `sonnet`,
  `opus`); "all in one message" (`skills/wave-auto/SKILL.md:164-166`, `:137`) assumes no limit on parallel agents;
  `wave-run` (`skills/wave-run/SKILL.md:78-83`, `:217`) and `wave-triage` (`skills/wave-triage/SKILL.md:113-115`)
  likewise.

## Evidence (planning, 2026-11-25)

Run in this planning session with the Codex CLI that ships with the Codex desktop app on this machine
(`~/.codex/plugins/.plugin-appserver/codex.exe`, not on `PATH`), `codex-cli 0.167.0-alpha.3.2`, default model
`gpt-6.2-astra` (`~/.codex/config.toml`), in a scratch folder outside every repository.

1. `codex features list` → `multi_agent  stable  true` (`multi_agent_v2  stable  false`).
2. `codex exec --skip-git-repo-check --ephemeral -s read-only "<list your agent tools with their schemas>"` → tools
   `collaboration.spawn_agent`, `wait_agent`, `followup_task`, `send_message`, `interrupt_agent`, `list_agents`.
   `spawn_agent` parameters, verbatim: `fork_turns?: string` ("Parent history to inherit. Defaults to `all`; use `none`
   to start without parent history"), `message: string`, `model?: string` ("Model override for the new agent"),
   `reasoning_effort?: string`, `task_name: string` (lowercase letters, digits, underscores). `wait_agent`:
   `timeout_ms?: number` (default 30000, min 10000, max 3600000). "A spawned agent can itself spawn agents. This session
   permits four concurrently active agents in total, including the root." "No exposed tool creates an independent
   top-level Codex session or thread."
3. Root and two children spawned with `model: gpt-6-luna` and `model: gpt-6.2-astra`, each asked for its exact model ID
   → all three: `Unknown.` Both spawns succeeded without error.
4. `env` in the root and in a child (`model: gpt-6-luna`): both have `CODEX_SESSION_ID` (the root's) and
   `CODEX_THREAD_ID` (their own: root `01a21428-8baf-…`, child `01a21428-e2c6-…`). The rollout files
   `~/.codex/sessions/2026/11/25/rollout-<time>-<thread id>.jsonl` exist for both; their `turn_context` record has
   `"model"`: root `gpt-6.2-astra`, child `gpt-6-luna` (effort `medium` and `low`).
5. The lookup command of "Model lookup in Codex" run **during the agent's own turn** in a read-only sandbox: root →
   `"model":"gpt-6.2-astra"`, child spawned with `model: gpt-6.2-sol` → `"model":"gpt-6.2-sol"`. Both PowerShell and
   bash forms below were then tested against the child's rollout (→ `gpt-6-luna`) and a missing thread ID
   (→ `unknown model`).
6. Five children spawned one after another (each waited for) all succeeded; `list_agents` then listed the root and
   only the last three children as `completed`: finished agents do not block new spawns, older ones drop off the list.
7. `codex exec` without stdin closed waited forever on `Reading additional input from stdin...` (timeout 124); with
   `< /dev/null` it ran. `codex exec resume [SESSION_ID|--last] [PROMPT]` has no `-s`; it takes `-c` overrides and
   `--dangerously-bypass-approvals-and-sandbox`.
8. `codex plugin list` → `wave-method@wave-method  installed, enabled  2.12.0`, from the Git marketplace
   `paramidon/wave-method` (its `.claude-plugin/marketplace.json`); `~/.codex/config.toml` has
   `[marketplaces.wave-method]` and `[plugins."wave-method@wave-method"]`, and its `[desktop]` table shows the desktop
   app uses the same config. Commands: `codex plugin marketplace add <owner/repo>`, `codex plugin add <plugin>@<marketplace>`.
9. Model list (`~/.codex/models_cache.json`): `gpt-6.2-astra` "Our most capable model for complex coding and
   professional work"; `gpt-6.2-sol` "Fast, go-to model for coding and everyday work"; `gpt-6.1-sol` "Previous
   generation model for coding"; `gpt-6-luna` "Fast and affordable model for easier tasks".

Not verified by running: the Codex desktop app's own tools (whether it offers starting a session, and the same
`spawn_agent`), a write to a worktree outside the project under `workspace-write`, and a whole `$wave-auto` run. Tasks D
and E rehearse them.

## Approach

Make Codex a documented vendor next to Claude Code, in the single source of truth, and point the skills to it:

1. `layout.md` "Model tiers" names a GPT model per tier, with exact model IDs, so any coordinator can choose a model of
   a tier and the tier gate can place a trailer's model ID.
2. `layout.md` "Tier gate": where the system prompt names no model, the executor uses its vendor's **model lookup** —
   a command that reads the model of its own thread from the environment. This keeps the rule "from its own
   environment, never from the prompt": the rollout file is written by Codex, not by the coordinator. No file → unknown
   model → stop, as today.
3. `layout.md` "Environment capabilities" gets `### Vendors`: how each capability is reached in Claude Code and in
   Codex (tool, fresh context, model choice, parallel limit, waiting, continuing, starting a session, model lookup,
   non-interactive form). Skills refer to it instead of naming tools.
4. `wave-auto`, `wave-run`, `wave-triage` launch at most the environment's parallel limit at once and launch the rest
   as earlier agents return; `wave-auto` takes model choice from "Vendors".
5. Rehearse in the Codex CLI (task D) and the Codex desktop app (task E) with the fixture of part 1, as part 1 did for
   Claude Code.

Not chosen: telling the executor its model in the prompt (the gate exists because a prompt can reach the wrong model);
a Codex-only skill copy (two copies drift); `codex exec` sessions per step as in the old driver (P4 removes that path;
Codex has subagents with model choice, evidence 2–5).

## Edits of `skills/wave-plan/layout.md` (task A)

### "Model tiers" table, lines 103-107

Replace the table body and the paragraph after it with:

```
| Complexity | Meaning | Model tier |
|---|---|---|
| `low` | mechanical edit from an exact description | Haiku 5.5 (`claude-haiku-5-5`) / GPT-6-Luna (`gpt-6-luna`) (or any stronger model) |
| `medium` | implementation of a given solution, several files, its own tests | Sonnet 5.5 (`claude-sonnet-5-5`) / GPT-6.2-Sol (`gpt-6.2-sol`), GPT-6.1-Sol (`gpt-6.1-sol`) (or stronger) |
| `high` | design uncertainty remains that cannot be removed upfront | Opus 5.5 (`claude-opus-5-5`) / GPT-6.2-Astra (`gpt-6.2-astra`) |

A task never runs below its tier; a `high` task never runs on a medium model. A plan README may add a line `Models: <complexity> = <model>, …` naming concrete models of the same or a higher tier; it never lowers one.
A model ID (a `Wave-Model` trailer, a lookup's result) is placed in a tier by the IDs in this table or the README
`Models:` line; an ID neither names is an unknown model ("Tier gate").
```

### "Tier gate", executor check, line 120-121

Replace `The executor names the exact model it runs on, from its own environment (system prompt, model ID), never from the prompt.`
with:

```
The executor names the exact model it runs on, from its own environment, never from the prompt: the model ID its
system prompt or environment states, or, where they state none, the result of its vendor's model lookup
("Vendors"; Codex states none).
```

The rest of the bullet stays.

### "Environment capabilities", after line 139 (`What each skill does when one is missing is in that skill.`)

Append, with a blank line before:

````
- **Parallel limit**: an environment may cap how many subagents run at once (Codex: 4 agents with the root, so 3
  subagents, unless its tool or config says otherwise). Launch at most that many at once and launch the next as one
  returns; each still gets its own result.

### Vendors

How each capability is reached; a skill that launches subagents uses the row of the vendor it runs in.

| Capability | Claude Code (CLI, desktop app) | Codex (CLI, desktop app) |
|---|---|---|
| subagent | the agent tool | `spawn_agent`, feature `multi_agent` |
| fresh context | the default | always `fork_turns: "none"`; the default `all` copies the whole conversation into the subagent |
| model of a tier | the agent tool's `model`: `haiku` low, `sonnet` medium, `opus` high | `spawn_agent`'s `model`: the model ID of "Model tiers" (`gpt-6-luna`, `gpt-6.2-sol`, `gpt-6.2-astra`) |
| parallel | several agent calls in one message | several `spawn_agent` calls, at most the parallel limit (3); then `wait_agent` |
| waiting | the agent call returns its result | call `wait_agent` (`timeout_ms` up to 3600000) again until `list_agents` shows every launched subagent completed; its result is its final message |
| continuing a subagent | the environment's message tool, where it has one | `followup_task` with the subagent's `task_name` |
| starting a session | the desktop app's session tools; none in the CLI | none in the CLI; the desktop app as its rehearsal recorded (`docs/rehearsals/coordinator-codex-desktop.md`) |
| own model ID | stated in the system prompt | not stated: the model lookup below |
| non-interactive run | `claude -p "<prompt>"`, then `claude -p --continue "<answer>"` | `codex exec "<prompt>" < /dev/null`, then `codex exec resume --last "<answer>" < /dev/null` |

**Model lookup in Codex.** Codex records every thread in `<CODEX_HOME>/sessions/YYYY/MM/DD/rollout-<time>-<thread id>.jsonl`
(`CODEX_HOME` defaults to `~/.codex`); every shell of a thread has its ID in `CODEX_THREAD_ID`, and the thread's last
`turn_context` record names its model. Run one of these; its one output line is the model ID, or `unknown model` (no
thread ID, no rollout file: an `--ephemeral` run):

```bash
m=$(f=$(find "${CODEX_HOME:-$HOME/.codex}/sessions" -name "rollout-*-${CODEX_THREAD_ID:-none}.jsonl" 2>/dev/null | head -1); [ -n "$f" ] && grep '"type":"turn_context"' "$f" | tail -1 | grep -o '"model":"[^"]*"' | head -1 | cut -d'"' -f4); echo "${m:-unknown model}"
```

```powershell
$h = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }; $f = Get-ChildItem (Join-Path $h 'sessions') -Recurse -Filter "rollout-*-$env:CODEX_THREAD_ID.jsonl" -ErrorAction SilentlyContinue | Select-Object -First 1; $l = if ($f) { Select-String -LiteralPath $f.FullName -Pattern '"type":"turn_context"' | Select-Object -Last 1 }; if ($l -and $l.Line -match '"model":"([^"]+)"') { $Matches[1] } else { 'unknown model' }
```
````

Notes for the editor: the bash block is one line; the PowerShell block is one line. Keep both verbatim.

### Other edits

- `skills/wave-plan/SKILL.md:72`: `(Sonnet 5.5, GPT-6.1 SOL)` → `(Sonnet 5.5, GPT-6.2-Sol)`.

## Edits of `README.md` (task A)

Only these; the unattended-run docs are rewritten by F2 after F1 is merged.

1. After the section `### Claude Code plugin (recommended for Claude Code)` (it ends at line 48), insert:

   ````
   ### Codex plugin (recommended for Codex)

   In a terminal, add this repository as a Codex plugin marketplace and install the plugin; the Codex CLI and the
   Codex desktop app share it:

   ```
   codex plugin marketplace add paramidon/wave-method
   codex plugin add wave-method@wave-method
   ```

   Type the commands with `$` in Codex (`$wave-plan …`).
   ````

2. Line 50: `### Installer (Codex, or a copy inside the project)` → `### Installer (a copy inside the project)`.
3. Lines 212-213: `runs the whole pipeline in the session you type it in — the
   Claude Code CLI (`claude`) or the Claude Code desktop app.` → `runs the whole pipeline in the session you type it
   in — the CLI or the desktop app of Claude Code or Codex.`
4. Line 324, row `tiers`: `` `low` (Haiku-class), `medium` (Sonnet-class / GPT), `high` (Opus-class) `` →
   `` `low` (Haiku-class / GPT-6-Luna), `medium` (Sonnet-class / GPT-6.2-Sol), `high` (Opus-class / GPT-6.2-Astra) ``.
5. Line 347: `` `wave-auto` needs subagents with a choice of model (Claude Code CLI or desktop app). `` →
   `` `wave-auto` needs subagents with a choice of model: Claude Code or Codex, CLI or desktop app. ``
6. Lines 422-423: `` **wave-auto** was rehearsed in the Claude Code CLI and desktop app ([rehearsals](docs/rehearsals/)); its rails `` →
   `` **wave-auto** was rehearsed in the Claude Code CLI and desktop app and in the Codex CLI and desktop app ([rehearsals](docs/rehearsals/)); its rails ``
   (keep the rest of the bullet; rewrap to at most 120 characters per line).

## Edits of the coordinator and the launching skills (task B)

### `skills/wave-auto/SKILL.md`

1. Frontmatter `description`, last sentence: `Recommended model: high complexity (Opus-class) — a subagent without a model choice
   inherits it.` → `Recommended model: high complexity (Opus-class or GPT-6.2-Astra) — a subagent without a model choice inherits
   it.`
2. "Capabilities", the bullets `parallel subagents;` and `model choice per subagent: …` (lines 60-62) become:

   ```
   - parallel subagents, and their limit (`wave-plan/layout.md`, "Environment capabilities", "Parallel limit");
   - model choice per subagent: which choice names a model of each tier, from the row of this vendor in
     `wave-plan/layout.md`, "Vendors" (Claude Code `haiku`, `sonnet`, `opus`; Codex the model IDs of "Model tiers"); a
     README `Models:` line may only name a tier or higher;
   ```

   After the example line `Capabilities: subagents · parallel · model choice (low haiku, medium sonnet, high opus) · session start no`
   add a second example on its own line, introduced by `or, in Codex,`:
   `Capabilities: subagents · parallel 3 · model choice (low gpt-6-luna, medium gpt-6.2-sol, high gpt-6.2-astra) · session start no`.
3. "Step prompt", after `The `triage-answers` step appends … Model: the tier's model choice.` add:
   `Launch every step with a fresh context and its tier's model, as the row of this vendor in `wave-plan/layout.md`,
   "Vendors", says (Codex: `fork_turns: "none"`, `model: <model ID>`), and wait for its result as that row says.`
4. Dispatch table row `next: triage-cluster …` (line 137): `in parallel where possible` → `in parallel up to the
   parallel limit`.
5. "Wave", item 1 (lines 164-166): `in parallel where the environment allows: all in one message, each on its tier's
   model.` → `in parallel up to the parallel limit, each on its tier's model: all of them at once when the limit
   allows (in Claude Code in one message), otherwise the next as one returns.`

### `skills/wave-run/SKILL.md`

1. "Environment capabilities" table, row `parallel subagents`: the "Used for" cell `one launch group at once` → `one
   launch group at once, up to the parallel limit (`layout.md`, "Environment capabilities")`.
2. Same table, row `model choice per subagent`, "Used for" cell `tiers` → `tiers; the model of a tier per vendor:
   `layout.md`, "Vendors"`.
3. Step 4, row "Launch groups": after `A group launches at once;` insert ` up to the parallel limit, the rest as earlier tasks return;`.

### `skills/wave-triage/SKILL.md`

Line 114: `all at once where the environment allows parallel subagents, otherwise one after another` → `all at once up to
the parallel limit (`layout.md`, "Environment capabilities"), otherwise one after another`.

### `skills/wave-plan/CHANGELOG.md`

Append to the `- Unreleased` item, after its last line (`… Installers and the plugin list the fifth skill.`, line 41),
as continuation lines indented by two spaces:

```
  Codex: the model tiers name GPT models with exact IDs (`gpt-6-luna`, `gpt-6.2-sol`, `gpt-6.2-astra`); a Codex agent,
  which cannot name its model, takes it from the rollout of its thread for the tier gate (`layout.md`, "Vendors",
  model lookup); `layout.md` "Vendors" says how each capability is reached in Claude Code and Codex, and every skill
  launches at most the environment's parallel limit of subagents at once; README shows the Codex plugin install;
  rehearsals of `$wave-auto` in the Codex CLI and desktop app.
```

## Rehearsals (tasks D and E)

### Fixture (both)

A scratch folder made with `mktemp -d` outside every repository (`<scratch>`). Repository `<scratch>/textkit`:

- `git init -b main`, user name/email set locally to `rehearsal` / `rehearsal@example.invalid`.
- `textkit/__init__.py` (empty), `tests/test_smoke.py` with `def test_import(): import textkit`, `README.md` one line
  `textkit — small text helpers. Check: python -m pytest -q`, `.gitignore` with `__pycache__/`, `.pytest_cache/`.
- A virtual environment `<scratch>/venv` with pytest (`python -m venv`, `pip install pytest`); every command runs with
  it first on `PATH` where the environment can be given one.
- Skills, **with the Codex links** (no `--no-codex`): Windows `<working folder>\install.ps1 -Target <scratch>\textkit`,
  else `<working folder>/install.sh <scratch>/textkit`; check that `.agents/skills/` has the five `wave-*` entries; add the line
  `.agents/` to `.gitignore` (git does not keep the links); then commit everything: `Seed textkit with wave skills`.

The list (verbatim, one start argument):

```
1. Add textkit/slug.py with slugify(text): lowercase, words joined by "-", only letters and digits kept. 2. Add textkit/count.py with count_words(text) returning a dict word -> count, words compared without case. 3. Add a command "python -m textkit top <file>" that prints the top words of the file with their counts.
```

Item 3 is open ("top" = how many?), so triage asks at least one question. Answer for every question:
`Top 10 words, most frequent first.`

### Rehearsal D — Codex CLI (`docs/rehearsals/coordinator-codex-cli.md`)

`<codex>`: `codex` when `command -v codex` finds it, else the Codex desktop app's copy
`~/.codex/plugins/.plugin-appserver/codex.exe` (Windows); none → the whole rehearsal is Not run, `Needs` missing.
Every call in `<scratch>/textkit`, with `--json` saved to `<scratch>/calls/<run>.jsonl`, `-o <scratch>/calls/<run>.txt`
and stdin closed (`< /dev/null`), model `-m gpt-6.2-astra` on the first call of a session. Never `--ephemeral` (the
model lookup needs the rollout). `<mode>`: the sandbox chosen in X1.

| Run | Command | Expected |
|---|---|---|
| X0 | `<codex> --version`; `<codex> features list` | the version; `multi_agent` … `true` |
| X1 | `<codex> exec -m gpt-6.2-astra -c sandbox_mode="workspace-write" -c 'sandbox_workspace_write.writable_roots=["<scratch>"]' "Run: git worktree add -b probe ../textkit.worktrees/probe main; then create probe.txt in that worktree and commit it there with message probe. Report each command and its output."` | the worktree and commit exist → `<mode>` = those two `-c` options; otherwise `<mode>` = `--dangerously-bypass-approvals-and-sandbox` (the scratch is isolated) and the record quotes the error. Afterwards remove the probe: `git worktree remove --force ../textkit.worktrees/probe`, `git branch -D probe` |
| X2 | `<codex> exec -m gpt-6.2-astra <mode> "\$wave-auto steps 4 <list>"` | first lines `Started:` and `Capabilities:` naming `parallel` and the three model IDs; one `triage-ask` step; the `Resume:` line in both forms; ≥ 1 question about item 3; branch `triage/<topic>` exists; claim `refs/wave-method/claims/auto/<topic>` exists |
| X3 | `<codex> exec resume --last <mode> "Top 10 words, most frequent first."` | steps `triage-answers`, `triage-finish`, `plan`, and `ended by rail: steps 4` (or the steps up to the rail); index merged into `main`; plan folder on `plan/<slug>` and `integration/<topic>`; claim released; final report with Steps, Halts, Status, Next |
| X4 | `<codex> exec -m gpt-6.2-astra <mode> "\$wave-auto plans/<date>-<topic>/index.md"` | no question; waves run to the end: `wave`, `task` steps, resume; every feature `✅ merged` into `integration/<topic>` or listed under Halts; no `tier-mismatch`; `main` unchanged since X3; claim released; `ended by done` |
| X5 | in `<scratch>/textkit` on `main`: `git merge --no-ff integration/<topic>`, `python -m pytest -q`, `python -m textkit top README.md` | tests green; at most 10 lines `word count` |

`<mode>` in `exec resume`: the `-c` options work there too; `--dangerously-bypass-approvals-and-sandbox` likewise.

Checks from the saved streams and the repository, one Results row each:

1. Every `spawn_agent` call of the coordinator has `fork_turns` `none` and a `model` of its step's tier ("Vendors":
   `navigate` `gpt-6-luna`; `triage-ask`, `triage-answers`, `triage-finish`, `plan`, `re-plan` `gpt-6.2-astra`;
   `triage-cluster`, `flow`, `wave` `gpt-6.2-sol`; `task` by the task's complexity). If the `--json` stream does not
   show tool arguments, read them from the thread's rollout file (`~/.codex/sessions/…/rollout-*-<thread id>.jsonl`,
   records of type `response_item`) and say so.
2. No more than 3 subagents ran at once (from `list_agents` results or spawn/complete order in the stream).
3. Every task commit of the run has a `Wave-Model` trailer naming a GPT model ID of its tier or higher:
   `git log --no-merges --format="%h %s | %(trailers:key=Wave-Model,valueonly)" integration/<topic>`.
4. The coordinator wrote no file and ran no test (its own shell calls only read git, the skill files and the clock, and
   take or release its claim); after X4 `git for-each-ref refs/wave-method/claims/` prints nothing.
5. Usage: the `usage` of the last `turn.completed` event of X2–X4 (input, cached input, output tokens).

Caps: stop starting calls after 3 hours; record the rest as Not run. When a run asks a question its row does not
expect, answer with the line of "Fixture (both)" in the next `exec resume` and record it as a finding.

### Rehearsal E — Codex desktop app (`docs/rehearsals/coordinator-codex-desktop.md`)

Needs desktop control of the Codex desktop app (screenshots, clicks, typing). Same fixture in its own scratch folder.

| Run | Action | Expected |
|---|---|---|
| E0 | open the Codex desktop app; note its version (About or settings) and the tools a new thread lists if it shows them | recorded |
| E1 | open the folder `<scratch>/textkit` as a project; new thread, model GPT-6.2-Astra, the most permissive permission mode the app offers for a local folder (record its name); message `$wave-auto <list>` | `Capabilities:` line (record whether `session start` is yes); ≥ 1 question about item 3; it waits |
| E2 | reply `Top 10 words, most frequent first.` | runs to the end without another question: one progress line per step; final report; every feature merged into `integration/<topic>` or under Halts with a next command. If the app asks for a permission, allow it for this folder and record each prompt as a finding |
| E3 | a second new thread in the same project: `$wave-auto plans/<date>-<topic>/index.md` | no question; `ended by done` with the same Status |
| E4 | merge and test as X5 | green |

Checks 1, 3 and 4 of Rehearsal D, from the threads' rollout files (`~/.codex/sessions/…`, newest files after E1) and
the repository. Cap: 3 hours.

### Record format (both)

Sections `## Setup`, `## Runs` (one subsection per run: command or action, exit, the deciding lines quoted, the files
that show it), `## Results` (table: expectation | Pass / Finding / Not run | evidence), `## Not verified`, `## Repeat`
(the commands to repeat it). Replace real paths with `<scratch>`, `<working folder>` and `~`; no user name, e-mail or
home path. A step that differs from its expectation is a finding, never fixed in the rehearsal; each finding also goes
into the report's `Problems:`.

## Limits

- The GPT model names are those this machine's Codex lists on 2026-11-25; like the Claude names they are examples, and
  a README `Models:` line can name others.
- The model lookup depends on Codex's rollout format (`turn_context` with `model`) and on `CODEX_THREAD_ID`; if a later
  Codex changes either, the lookup prints `unknown model` and tasks stop `tier-mismatch` — safe, never a wrong tier.
- The parallel limit 3 is Codex 0.167's default; the tool or config may state another.
- Starting a session from Codex: none in the CLI (evidence 2); the desktop app is recorded by task E. Without it a
  step that cannot run as a subagent halts with its manual command, as `wave-auto` already does.

## Acceptance tests

1. `layout.md`: the tier table has the three GPT IDs and the paragraph on placing a model ID; the executor check names
   the model lookup; "Environment capabilities" has the "Parallel limit" bullet and `### Vendors` with the table (9
   rows) and both lookup commands verbatim (task A).
2. Run in bash with `CODEX_THREAD_ID=nope` and in PowerShell with `$env:CODEX_THREAD_ID='nope'`, the two lookup
   commands copied from `layout.md` each print `unknown model` (task A).
3. README has `### Codex plugin (recommended for Codex)` with both commands and edits 2–6 (task A).
4. `wave-auto/SKILL.md`, `wave-run/SKILL.md`, `wave-triage/SKILL.md` and `CHANGELOG.md` carry the texts of "Edits of the
   coordinator and the launching skills" (task B).
5. Status-check tests, driver tests and the three examples pass; `git diff --check main` is clean.
6. Rehearsal D: X0–X5 and checks 1–5 recorded; every expectation Pass, a Finding with an open problem entry, or Not
   run with its reason (task D).
7. Rehearsal E: E0–E4 and its checks recorded likewise (task E).
