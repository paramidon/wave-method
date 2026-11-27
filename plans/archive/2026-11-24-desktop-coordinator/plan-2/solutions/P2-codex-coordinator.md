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
8. Re-plan 2026-11-26 (tasks H and I): the five edits of "Text fixes (task H)" are in place; README, layout and
   changelog claim exactly the Codex rehearsals the records show; `## Plugin install` of the CLI record is Pass, a
   Finding with an open entry, or Not run with its reason.

## Fixes after wave 1 (re-plan 2026-11-26)

Open entries of wave 1, all of feature F1, round 1. Line numbers are those of
`feat/desktop-coordinator-p2/F1-codex-coordinator` at bbfbe18; tasks D and E (wave 2) add only their two records, so
the numbers stay valid for wave 4.

| Entry | Essence | Fixed by |
|---|---|---|
| I1 | the `wave-run` description names "GPT-6.1 SOL" | task H, "Text fixes (task H)", item 1 |
| I5 | the Codex `Capabilities:` example of `wave-auto` is a 133-character prose line | task H, item 4 |
| I6 | the "Launch groups" row of `wave-run` splits "at once" from the limit | task H, item 5 |
| I2 | README and layout claim Codex rehearsals before D and E recorded them | task I, "Claims after the rehearsals (task I)" |
| I3 | the README's two `codex plugin` commands were never run | task I, "Plugin install check (task I)" |

### Text fixes (task H)

1. `skills/wave-run/SKILL.md:3` (frontmatter `description`): `(Sonnet 5.5 / GPT-6.1 SOL)` → `(Sonnet 5.5 / GPT-6.2-Sol)`.
2. `skills/wave-plan/SKILL.md:3`: `Recommended model: high complexity (Opus-class), because` →
   `Recommended model: high complexity (Opus-class or GPT-6.2-Astra), because`.
3. `skills/wave-triage/SKILL.md:3`: `Recommended model: high complexity (Opus-class) — misjudged` →
   `Recommended model: high complexity (Opus-class or GPT-6.2-Astra) — misjudged`.
   Items 2 and 3 are not in I1; they make every high-tier description name the GPT model as `wave-auto`'s already
   does (task B), since Codex shows these descriptions when it lists skills.
4. `skills/wave-auto/SKILL.md:67-70`, the four lines from `Print one line` through the Codex example and its period,
   become the text below: the two example lines inside a fenced block, without backticks or a final period. A fenced
   block may hold lines over 120 characters, as the lookup commands of `layout.md` do.

   ````
   Print one line `Capabilities: …`, for example in Claude Code and in Codex:

   ```
   Capabilities: subagents · parallel · model choice (low haiku, medium sonnet, high opus) · session start no
   Capabilities: subagents · parallel 3 · model choice (low gpt-6-luna, medium gpt-6.2-sol, high gpt-6.2-astra) · session start no
   ```

   ````

   A blank line follows the block; then the line `Neither subagents nor starting a session → stop …`, unchanged.
5. `skills/wave-run/SKILL.md:217`, row "Launch groups": `A group launches at once; up to the parallel limit, the rest
   as earlier tasks return; without parallel subagents, its tasks run one after another with the same worktrees and
   checks.` → `A group launches at once, up to the parallel limit; the rest start as earlier tasks return. Without
   parallel subagents, its tasks run one after another with the same worktrees and checks.` (the row stays one line).

### Claims after the rehearsals (task I)

Read the `## Results` tables of `docs/rehearsals/coordinator-codex-cli.md` (task D) and
`docs/rehearsals/coordinator-codex-desktop.md` (task E). Definitions:

- **CLI rehearsed**: the CLI record exists and its rows for X2, X3 and X4 are each Pass or Finding (none Not run).
- **Desktop rehearsed**: the desktop record exists and its rows for E1 and E2 are each Pass or Finding.
- **Desktop session start**: the `session start` value of the `Capabilities:` line that run E1 quotes: `yes` (with the
  tool the record names for it, if any), `no`, or not recorded (E1 Not run, or no such line quoted).

Edits, each exactly one of its variants:

1. `README.md:434-435`, Limitations bullet `- **wave-auto** was rehearsed …` (rewrap to at most 120 characters, two-space
   continuation indent):

   | Case | Bullet |
   |---|---|
   | CLI and desktop rehearsed | unchanged |
   | only CLI | `- **wave-auto** was rehearsed in the Claude Code CLI and desktop app and in the Codex CLI ([rehearsals](docs/rehearsals/)); the Codex desktop app is not rehearsed yet. Its rails (`until`, `steps`) are rules of the skill, not enforced limits.` |
   | only desktop | `- **wave-auto** was rehearsed in the Claude Code CLI and desktop app and in the Codex desktop app ([rehearsals](docs/rehearsals/)); the Codex CLI is not rehearsed yet. Its rails (`until`, `steps`) are rules of the skill, not enforced limits.` |
   | neither | `- **wave-auto** was rehearsed in the Claude Code CLI and desktop app ([rehearsals](docs/rehearsals/)); in Codex it is not rehearsed yet. Its rails (`until`, `steps`) are rules of the skill, not enforced limits.` |

2. `skills/wave-plan/layout.md:160`, "Vendors" row `starting a session`, Codex cell
   `none in the CLI; the desktop app as its rehearsal recorded (`docs/rehearsals/coordinator-codex-desktop.md`)`:

   | Desktop session start | Codex cell |
   |---|---|
   | `yes`, tool named | `none in the CLI; the desktop app: `<tool>` (`docs/rehearsals/coordinator-codex-desktop.md`)` |
   | `yes`, no tool named | `none in the CLI; the desktop app: yes (`docs/rehearsals/coordinator-codex-desktop.md`)` |
   | `no` | `none in the CLI or the desktop app (`docs/rehearsals/coordinator-codex-desktop.md`)` |
   | not recorded | `none in the CLI; the desktop app not verified, so treat it as missing` |

3. `skills/wave-plan/CHANGELOG.md:45-46`, the end of the Codex sentence of the `- Unreleased` item,
   `README shows the Codex plugin install;` and `rehearsals of `$wave-auto` in the Codex CLI and desktop app.`:

   | Case | End of the sentence |
   |---|---|
   | CLI and desktop rehearsed | unchanged |
   | only CLI | `…; README shows the Codex plugin install; a rehearsal of `$wave-auto` in the Codex CLI.` |
   | only desktop | `…; README shows the Codex plugin install; a rehearsal of `$wave-auto` in the Codex desktop app.` |
   | neither | `…; README shows the Codex plugin install.` |

   Rewrap only the last lines of that item, at most 120 characters, two-space indent.

Nothing else of the README, layout or changelog changes: the other Codex sentences describe what the skills support,
not what was rehearsed.

### Plugin install check (task I)

Proves the two commands of README "Codex plugin (recommended for Codex)" without touching the user's Codex settings:
Codex reads its home from `CODEX_HOME` (default `~/.codex`, "Vendors"), so the check runs with a fresh one in a scratch
folder.

1. `<codex>` as in Rehearsal D. None → result `Not run (Codex CLI missing)`.
2. Hash `~/.codex/config.toml` (`sha256sum`, PowerShell `Get-FileHash`) before; keep it.
3. `export CODEX_HOME=<scratch>/codex-home` (create the folder first); every call with stdin closed (`< /dev/null`):
   `<codex> plugin marketplace add paramidon/wave-method`, then `<codex> plugin add wave-method@wave-method`, then
   `<codex> plugin list`.
4. Expected: both commands exit 0; `plugin list` prints a line with `wave-method@wave-method` and `installed`; the hash
   of `~/.codex/config.toml` after is the one before.
5. A command that Codex rejects as unknown or malformed is a Finding (the README commands are wrong); do not try other
   commands. A failure for another reason (network, sign-in) is Not run, with the error quoted.
6. Markdown of that README section, by `layout.md` "Markdown rules": a blank line before and after the fenced block and
   the paragraphs; its heading level `###`, like `### Claude Code plugin (recommended for Claude Code)`. Its rendered
   view is left to the user's review of F1.

Recorded as a new last section `## Plugin install` of `docs/rehearsals/coordinator-codex-cli.md`: the Codex version,
each command with its exit and deciding output lines, whether the two hashes are equal (not the hash values), the
Markdown check, and one result line: Pass, Finding or Not run. Paths as `<scratch>` and `~`.

## Evidence (re-plan 2026-11-26, round 2)

Run in the re-planning session on Windows with `codex-cli 0.167.0-alpha.3.2` (`<codex>`, the copy of the desktop app),
`[windows] sandbox = "elevated"` in the user's config, the user's account signed in. Scratch repositories: `<scratch>`
below the temp folder, and `<data>` = a new folder on a data drive outside the user profile and the temp folder. Every
`codex sandbox` call runs one command under a permission profile without a model; `codex exec` calls ran the model.
Profiles are passed as `-c 'permissions.<name>.filesystem={…}' -P <name>` (sandbox) or
`-c 'default_permissions="<name>"'` (exec), or come from `<repo>/.codex/config.toml`.

| Entry | Disputed assumption | Command (shortened) | Deciding output | Conclusion |
|---|---|---|---|---|
| I8, I15 | `workspace-write` with a writable root can write `.git` | `<codex> sandbox -P :workspace -C <scratch>/repo -- git branch probe1` | `fatal: cannot lock ref 'refs/heads/probe1' … Permission denied` | the built-in workspace profile never writes `.git` |
| I8, I15 | only full access writes `.git` | `<codex> sandbox -P :danger-full-access -C <scratch>/repo -- git branch probe2` | exit 0, branch `probe2` exists | full access works |
| I8, I15 | (same) | profile `{":root"="read", "<repo>"="write", "<repo>/.git"="write"}` | `cannot lock ref … Permission denied` | a writable folder protects its own `.git`, even when `.git` is listed |
| I8, I15 | (same) | profile `{":root"="read", "<data>"="write", ":tmpdir"="write"}`, `-C <data>/textkit`: `git worktree add -b wt1 ../textkit.worktrees/wt1 main`; `git -C ../textkit.worktrees/wt1 commit --allow-empty -m wt1commit`; `git update-ref refs/wave-method/claims/test HEAD` | `HEAD is now at …`; `[wt1 310494a] wt1commit`; exit 0 | a profile whose writable folder is the **parent** of the repository writes branches, worktrees next to it, commits and claim refs |
| I8, I15 | (same) | the same profile: `git -C <this repository> update-ref refs/wave-method/probe-should-fail HEAD` | `cannot lock ref …`; no such ref in this repository | writes outside the parent folder stay refused |
| I8, I15 | (same) | `<codex> exec -C <data>/textkit -c 'default_permissions="wave"' -c 'permissions.wave.filesystem={…as above…}' -c 'approval_policy="never"'`: the model ran `git worktree add` and a commit | `Preparing worktree (new branch 'x1')`, `[x1 caf610d] x1`; `turn_context`: `writable_roots` `["<data>"]` | the model's own shell works under the profile; its subagents inherit it (their `turn_context` has the same roots) |
| I8 | a project can carry the profile | `<data>/textkit/.codex/config.toml` with `default_permissions = "wave"` and `[permissions.wave]`; `<codex> exec -C <data>/textkit` without sandbox options: `git branch probeP`, `git branch -D probeP` | `Deleted branch probeP` | the project config of a trusted project applies the profile in the CLI; the desktop app: not verifiable by running here (needs desktop control), task O |
| I8 | relative paths in the profile | `filesystem = { …, ".." = "write" }` | ``filesystem path `..` must be absolute, use `~/...`, or start with `:` `` | the parent folder is written as an absolute path |
| I8 | the agent cannot widen its own profile | profile plus `"<data>/proj/.codex" = "read"`: python writes `.codex/config.toml`; `git branch`; python writes `ok.txt` | `PermissionError: [Errno 13] Permission denied: '.codex/config.toml'`; exit 0; `repo write ok` | a more specific read entry protects `.codex` |
| I8 | temp files work | the profile without `:tmpdir`: `python -c "tempfile.mkdtemp()"` | `tempdir ok <data>\p2\proj\tmp…` (inside the project) | keep `:tmpdir`, or temp files land in the project |
| I8 (Windows) | the ACL of `.git` does not persist | `icacls <scratch>/…/.git` after a `:workspace` session; then the parent profile on that repository in the temp folder, and on D's old scratch | `(DENY)(W,D,Rc,GW,DC)` entries for sandbox SIDs; `cannot lock ref` for the profile with `:tmpdir` (repository inside the temp folder) and for D's scratch (its parent was a writable root of D's `workspace-write` run) | the elevated Windows sandbox leaves deny entries on `.git` for every writable folder of an earlier `workspace-write` session that held the repository; a project outside the temp folder keeps working after such a session (`<data>` test: `:workspace` once, then the parent profile with `:tmpdir`: exit 0) |
| I9, I18 | shells start outside the project | the exec runs above: `Get-Location` in `<data>/textkit` (outside the user profile) and in D's scratch (below it) | `D:\…\textkit`; `C:\Users\…\d.Ssk0\textkit` | with the profile the shell starts in the project in both places; I9 came with D's failing `workspace-write` thread; macOS and Linux: not verifiable by running here (one Windows machine) |
| I10 | `spawn_agent` refuses `gpt-6-luna`, which its description does not list | exec: two `spawn_agent` calls with `model: "gpt-6-luna"`, `fork_turns: "none"` | `{"task_name":"/root/gate_plain"}`, `{"task_name":"/root/gate_lookup"}`; both children's `turn_context` `"model":"gpt-6-luna"` | the ID is accepted; D3 was the coordinator's choice, so the rule must say to pass the ID of "Model tiers" anyway |
| I11, I17 | the gate line alone makes a Codex subagent check its model | child `gate_plain` (`gpt-6-luna`) got the medium gate line and a one-line task | its final message: `ref: refs/heads/main` (it did the task) | a gate line alone is not enough |
| I11, I17 | a lookup line makes it check | child `gate_lookup` (`gpt-6-luna`) got the gate line, then `Model lookup: … run this PowerShell command …: <lookup command>` | `gpt-6-luna; stopping because it is below the required tier.` | the prompt must carry the lookup command; the behaviour shows it although the prompt text is encrypted in the rollout |
| I16 | the lookup works inside the sandbox | exec root: `powershell -NoProfile -File lookup.ps1` (the PowerShell command of "Vendors") | `gpt-6.2-astra` | verified |
| I13 | `--ignore-user-config` keeps `~/.codex/config.toml` unchanged | exec in a new folder with `--ignore-user-config` | the file got `[projects.'d:\…\textkit']` `trust_level = "trusted"` | Codex writes a trust entry for every new project folder; the user accepted this on 2026-11-26; the entries of the probes and of D were removed with the user's consent |

Side notes: a sandboxed git prints `warning: unable to access '<home>/.config/git/ignore': Permission denied`
(harmless); `codex sandbox` needs `-P`; `sandbox_mode` and `default_permissions` cannot both be set.

## Fixes after wave 2 (re-plan 2026-11-26, round 2)

F1 is escalated (round 2): every new task is `high`. Wave 4 (H, I) and wave 5 (J, K) never ran and are dropped: I needs
the desktop record that E never wrote, and both waves would block the new waves. H's five edits move to L and M; I's
two parts to N (plugin check) and P (claims). Line numbers are those of
`feat/desktop-coordinator-p2/F1-codex-coordinator` at 4d0d1f7.

| Entry | Essence | Fixed by |
|---|---|---|
| I1, I6 | stale model name; "Launch groups" row | task L, "Permissions and gate texts (task L)", items 6, 8 |
| I5 | the Codex `Capabilities:` example line | task M, "wave-auto rules (task M)", item 1 |
| I8, I15 | `.git` is read-only under `workspace-write` | L (profile, `git-read-only`), M (capability check); verified by N and O |
| I9, I18 | shells did not start in the project | verified above; N and O check it again (check 7) |
| I10 | `gpt-6-luna` not chosen for `low` | L (Vendors cell), M (Capabilities rule); N check 1 |
| I11, I16, I17 | no model check in a Codex step; the lookup in the sandbox; prompts unreadable | L and M (lookup line); N and O check 6 judge prompts by behaviour |
| I12 | the coordinator leaves its fixed texts | M, item 5; N and O check 8 |
| I14 | the rest of the CLI pipeline | task N |
| I19 | the desktop rehearsal | task O |
| I2 | claims match the records | task P |
| I3 | the README plugin commands | task N, "Plugin install" |

I13 is closed: accepted by the user on 2026-11-26 (rehearsals list the trust entries they add).

### Shared texts (tasks L and M)

The **lookup line**, one line, `<command>` being the model lookup of "Vendors" for the subagent's shell, verbatim:

```
Model lookup: this environment states no model ID; before reading or changing anything, run this command and take its one output line as the exact model you run on: <command>
```

The stop code **`git-read-only`**: a git write refused by the environment (`Permission denied` on `.git`, a ref or the
worktrees folder). Stop line:
`Stop git-read-only: <the refused path> — next: grant the permissions of wave-plan/layout.md, "Vendors", "Permissions in Codex", then run the same command again`.

### Permissions and gate texts (task L)

Files: `skills/wave-plan/layout.md`, `skills/wave-run/SKILL.md`, `skills/wave-plan/SKILL.md`,
`skills/wave-triage/SKILL.md`, `README.md`, `skills/wave-plan/CHANGELOG.md`.

1. `layout.md` "Tier gate": after the bullet `- **Gate line.** …` (lines 118-121) insert the bullet:

   ```
   - **Lookup line.** Where the vendor states no model ID in an agent's environment (Codex, "Vendors"), every prompt
     that starts with a gate line and goes to a subagent (`wave-run`'s launch header, `wave-auto`'s step prompt) has
     this second line, `<command>` being the model lookup of "Vendors" for the subagent's shell, verbatim:
     `Model lookup: this environment states no model ID; before reading or changing anything, run this command and take its one output line as the exact model you run on: <command>`
     A Codex subagent given the gate line alone does not run the lookup.
   ```

2. `layout.md` "Vendors", row `model of a tier` (line 156), Codex cell → `` `spawn_agent`'s `model`: the model ID of
   "Model tiers" (`gpt-6-luna`, `gpt-6.2-sol`, `gpt-6.2-astra`), also when the tool's description does not list it; a
   model the tool refuses is a missing tier ``.
3. Same table, after the row `own model ID` (line 161), a new row:
   `` | git writes | a permission mode that allows git and file writes in the repository and in `../<repo-folder>.worktrees/` (`auto` does) | the permission profile of "Permissions in Codex"; the default `workspace-write` keeps `.git` read-only | ``
4. `layout.md`, after the PowerShell block of "Model lookup in Codex" (it ends before `## Names`, line 177), with a
   blank line before and after:

   ````
   **Permissions in Codex.** The wave skills write branches, refs and commits in `.git` and create worktrees next to
   the repository (`../<repo-folder>.worktrees/`). Codex's `workspace-write` sandbox keeps the `.git` of every writable
   folder read-only, so they need this permission profile, in `<repository>/.codex/config.toml` (Codex reads it for a
   trusted project) or in `~/.codex/config.toml`. Paths are absolute (`~/…` allowed); `<parent>` is the folder that
   holds the repository:

   ```toml
   default_permissions = "wave"

   [permissions.wave]
   filesystem = { ":root" = "read", "<parent>" = "write", ":tmpdir" = "write", "<repository>/.codex" = "read" }
   ```

   The sandbox stays on: the agent reads everything, writes only below `<parent>` and in the temp folder, and cannot
   change its own profile. Subagents inherit it. Keep the file out of git (`.git/info/exclude`): its paths belong to
   one machine. On Windows the sandbox keeps denying `.git` to a folder that was a writable folder of an earlier
   `workspace-write` session holding that repository, the temp folder included: keep the repository out of the temp
   folder and do not use such a folder as `<parent>`. Where the profile cannot be used, full access works
   (`codex -s danger-full-access`). Every wave skill whose git write is refused stops `git-read-only`:
   `Stop git-read-only: <the refused path> — next: grant the permissions of wave-plan/layout.md, "Vendors", "Permissions in Codex", then run the same command again`.
   ````

5. `wave-run/SKILL.md` step 4: the text before the header block (lines 231-232) `(the first line only for a `medium` or
   `high` task, `layout.md`, "Tier gate"):` → `(the first line only for a `medium` or `high` task, the second only for
   such a task where the vendor states no model ID: `layout.md`, "Tier gate"):`; in the block, after the line
   `Required tier: …` (line 235), insert the lookup line of "Shared texts" with `<command>` kept as a placeholder.
6. `wave-run/SKILL.md` line 217, row "Launch groups": `A group launches at once; up to the parallel limit, the rest as
   earlier tasks return; without parallel subagents, its tasks run one after another with the same worktrees and
   checks.` → `A group launches at once, up to the parallel limit; the rest start as earlier tasks return. Without
   parallel subagents, its tasks run one after another with the same worktrees and checks.` (one physical line).
7. `wave-run/SKILL.md` "Stops" table, after the row `capability-missing` (line 115), a new row:
   `` | `git-read-only` | a git write is refused by the environment (`Permission denied` on `.git`, a ref or the worktrees folder) | grant the permissions of `layout.md`, "Vendors", "Permissions in Codex", then run the same command again | ``
8. `wave-run/SKILL.md:3` (description): `(Sonnet 5.5 / GPT-6.1 SOL)` → `(Sonnet 5.5 / GPT-6.2-Sol)`.
9. `wave-plan/SKILL.md:3`: `Recommended model: high complexity (Opus-class), because` → `Recommended model: high
   complexity (Opus-class or GPT-6.2-Astra), because`; `wave-triage/SKILL.md:3`: `Recommended model: high complexity
   (Opus-class) — misjudged` → `Recommended model: high complexity (Opus-class or GPT-6.2-Astra) — misjudged`.
10. `README.md`: after the section `### Codex plugin (recommended for Codex)` (it ends with line 60, `Type the commands
    with `$` in Codex (`$wave-plan …`).`), before `### Installer (a copy inside the project)`, insert:

    ````
    ### Codex permissions

    The skills write branches and commits in `.git` and create worktrees next to the project
    (`../<project>.worktrees/`). Codex's default `workspace-write` sandbox keeps `.git` read-only, so give Codex this
    permission profile in `<project>/.codex/config.toml` (absolute paths; `<parent>` is the folder that holds the
    project):

    ```toml
    default_permissions = "wave"

    [permissions.wave]
    filesystem = { ":root" = "read", "<parent>" = "write", ":tmpdir" = "write", "<project>/.codex" = "read" }
    ```

    The sandbox stays on: Codex reads everything and writes only below `<parent>` and in the temp folder. Keep the file
    out of git (add `.codex/config.toml` to `.git/info/exclude`). Where the profile cannot be used, full access works
    too (`codex -s danger-full-access`). Details: `skills/wave-plan/layout.md`, "Vendors".
    ````

11. `CHANGELOG.md`, the `- Unreleased` item: after its last line, as continuation lines with a two-space indent, at
    most 120 characters:

    ```
      Codex permissions: a permission profile that writes only the folder holding the repository (`layout.md`,
      "Vendors"; README "Codex permissions"); a git write the sandbox refuses stops `git-read-only`; prompts to Codex
      subagents carry the model lookup right after the gate line.
    ```

### wave-auto rules (task M)

File: `skills/wave-auto/SKILL.md` only.

1. Lines 67-70 (from `Print one line `Capabilities: …`, for example` through the Codex example line and its period):
   the text of "Text fixes (task H)", item 4 — the line `Print one line `Capabilities: …`, for example in Claude Code
   and in Codex:`, a blank line, a fenced block (no language) with the two example lines without backticks or final
   period, a blank line.
2. "Capabilities", the bullet `- model choice per subagent: …` (lines 61-63): append the sentence `Name each tier's
   model as that row says, also when the tool does not list it; never launch a step on another tier's model.`
3. "Capabilities", after the bullet `- starting a session;` (line 64), a new bullet:
   `- git writes: whether this session may write the main checkout's `.git` and the folder that holds it — in Codex,
   from the sandbox and writable folders its environment states (`wave-plan/layout.md`, "Vendors", "Permissions in
   Codex"); no → stop `git-read-only` before any step;`
4. "Step prompt": line 76 `Every step's subagent gets exactly this prompt (the first line only for a medium or high
   step):` → `Every step's subagent gets exactly this prompt (the first line only for a medium or high step; the second
   only for such a step where the vendor states no model ID: `wave-plan/layout.md`, "Tier gate", "Lookup line"):`; in
   the block, after the line `Required tier: …` (line 79), insert the lookup line of "Shared texts" with `<command>`
   kept as a placeholder.
5. Output texts:
   - "Hard rules", the bullet `- It writes the user only what this skill names: …` (lines 51-53): append `Its first
     message starts with the `Started:` line: no sentence comes before it.`
   - "End of the run", after the paragraph `The Steps table has one row per step …` (lines 249-251), a new paragraph:
     `` `<start>` in the title and in `Continue:` is the start as typed: for a list start the index path once
     `triage-ask` returned one, else the list verbatim; never a summary, a title of its own or a placeholder such as
     `<original list>`. The Result cell is the step's return line, verbatim. Every Halts line ends with
     `— next: <command or action>`. ``
   - "Stops", table "Stops that end the run", after the row `no-subagents` (line 269), a new row:
     `` | `git-read-only` | the session cannot write the main checkout's `.git` ("Capabilities"), or a step returns it | grant the permissions of `wave-plan/layout.md`, "Vendors", "Permissions in Codex", then `/wave-auto <start>`<br>`$wave-auto <start>` | ``

### Rehearsal D2 — Codex CLI with the permission profile (task N)

Rehearsal D of "Rehearsals (tasks D and E)" again, with these changes; the record replaces
`docs/rehearsals/coordinator-codex-cli.md`.

- `<scratch>`: a new empty folder outside every repository and outside the temp folder, never used by Codex before
  (`~/wave-rehearsal-<YYYYMMDD-HHMM>`). Fixture as "Fixture (both)"; then write `<scratch>/textkit/.codex/config.toml`
  with the profile of README "Codex permissions" (`<parent>` = `<scratch>`, `<project>` = `<scratch>/textkit`, absolute
  paths) and add `.codex/` to `<scratch>/textkit/.git/info/exclude`.
- Before X0: hash `~/.codex/config.toml` and keep the list of its `[projects.` lines.
- `<mode>` is `-C <scratch>/textkit -c 'approval_policy="never"'` for every call; no `-s`, no `sandbox_mode`, no
  bypass, no `danger-full-access` (the user's decision: rehearsals use the profile only). `exec resume --last` runs
  from `<scratch>/textkit` with `-c 'approval_policy="never"'`.
- X1: first `Get-Location` (bash: `pwd`), then the worktree and commit probe of X1; expected Pass; remove the probe as
  before. A failure is a finding; then X2–X5 are Not run.
- X2–X5 and checks 1–5 as written, plus:
  6. Every `medium` and `high` step subagent runs the model lookup before any other command and gets its model
     (`turn_context` of its rollout; its first `function_call` is the lookup); its prompt is judged by this behaviour,
     since the text is encrypted (I11, I16, I17).
  7. The first shell of the root and of every subagent starts in the project or its worktree (I9, I18).
  8. The coordinator's texts: the first output line is `Started:`; the title is `## wave-auto · <start>` as "End of the
     run" says; each Result cell is a return line; every Halts line has `— next:`; `Continue:` holds the real start
     (I12).
  9. Trust entries: the `[projects.` lines added to `~/.codex/config.toml` during the run, paths as `<scratch>`;
     nothing else of the file changed.
- Then the plugin check of "Plugin install check (task I)", recorded as `## Plugin install`.
- Record: the format of "Record format (both)"; right after the header paragraph a section
  `## First attempt (2026-11-26)` of at most six lines: under `workspace-write` the pipeline stopped at its first step
  (findings D1–D6); the full record is commit 7bcdaf1.
- Caps: 3 hours of Codex calls. Leave `<scratch>` in place and name it in the report.

### Rehearsal E2 — Codex desktop app with the permission profile (task O)

Rehearsal E of "Rehearsals (tasks D and E)" again (record `docs/rehearsals/coordinator-codex-desktop.md`), with these
changes:

- `<scratch>` and the fixture as in Rehearsal D2, in its own new folder; the same `.codex/config.toml`; the config hash
  and `[projects.` list before E0.
- E1: open `<scratch>/textkit` as a project; new thread with GPT-6.2-Astra; leave the permission setting the app shows
  for this project and record its exact name; if the app offers a setting that names the profile `wave` or the
  project's config, choose it and record it. Never choose a full-access mode: that needs the user's separate
  permission. Record the thread's `sandbox_policy` from its rollout `turn_context` (writable roots as `<scratch>`).
- If git writes are refused (a `git-read-only` stop or `Permission denied`), that is a finding; record it and stop the
  rehearsal there: the rest is Not run.
- Checks 1, 3, 4, 6, 7, 8 and 9 of Rehearsal D2; the value of `session start` in the `Capabilities:` line.
- Cap: 3 hours. Leave `<scratch>` in place and name it in the report.

### Claims after the rehearsals (task P)

The definitions and edits 1–3 of "Claims after the rehearsals (task I)", unchanged, read from the records of tasks N
and O, plus edit 4. Definitions added:

- **CLI profile works**: run X1 of the CLI record is Pass.
- **Desktop profile works**: the desktop record's E1 shows writable roots `<scratch>` and no git write was refused in
  E1–E3.

4. README "### Codex permissions", after its sentence `Where the profile cannot be used, full access works too
   (`codex -s danger-full-access`).`, add exactly one sentence:

   | Case | Sentence |
   |---|---|
   | desktop profile works | `The Codex desktop app applies the same file.` |
   | desktop record exists, profile does not work | `The Codex desktop app did not apply it in its rehearsal: use its full access mode there.` |
   | desktop E1 Not run, or no record | `The Codex desktop app is not rehearsed with it yet.` |

   If "CLI profile works" is false, change nothing and stop: the plan's solution failed (report it).

## Acceptance tests (re-plan 2026-11-26, round 2)

9. `layout.md` has the "Lookup line" bullet, the `git writes` row, the changed `model of a tier` cell and "Permissions
   in Codex" with the profile; `wave-run/SKILL.md` has the lookup line in its header block, the `git-read-only` row and
   the fixed "Launch groups" row; README has `### Codex permissions`; `git grep -n "GPT-6.1 SOL" -- skills README.md`
   prints nothing (task L).
10. `wave-auto/SKILL.md` has the fenced capabilities examples, the `git writes` bullet, the model rule, the lookup line
    in its step prompt, the three output rules and the `git-read-only` row (task M).
11. The CLI record (task N) shows X1 Pass under the profile, X2–X5 and checks 1–9 each Pass, a Finding with an entry,
    or Not run with its reason, and `## Plugin install`; the desktop record (task O) likewise for E0–E4.
12. README, layout and changelog claim exactly what the two records show (task P).

## Evidence (re-plan 2026-11-26, round 3)

Override of F1 by the user (direction quoted in `history.md`): trust only the test project, adding its entry to
`~/.codex/config.toml` and removing it afterwards. Run in the re-planning session with `<codex>` =
`codex-cli 0.167.0-alpha.3.2` on task N's fixture `<scratch>/textkit` (`<scratch>` = `~/wave-rehearsal-20261126-0319`,
the profile of README "Codex permissions" in `<scratch>/textkit/.codex/config.toml`). Every run: `<codex> exec -m
gpt-6.2-astra -C <scratch>/textkit -c 'approval_policy="never"' --json`, stdin closed, the X1 prompt of Rehearsal D2
(`Get-Location`, `git worktree add -b probe ../textkit.worktrees/probe main`, a file and a commit there). The hash of
`~/.codex/config.toml` was taken before T0 and compared after every run; each probe worktree and branch was removed.

| Entry | Disputed assumption | Run | Deciding output | Conclusion |
|---|---|---|---|---|
| I21 | (baseline) an untrusted project's profile is ignored | T0: no trust entry | `sandbox_policy` `{"type":"read-only"}`, `active_permission_profile` `:read-only`; `fatal: cannot lock ref 'refs/heads/probe' … Permission denied`; hash unchanged | N1 reproduces |
| I21 | the missing trust is the cause | T1: `[projects.'<scratch>\textkit']` with `trust_level = "trusted"` appended to `~/.codex/config.toml` (Windows path, upper-case drive and folder names) | `sandbox_policy` `workspace-write`, `writable_roots` `["<scratch>"]`, `active_permission_profile` `wave`; `[probe f66842b] probe`; worktree `<scratch>/textkit.worktrees/probe` | confirmed: a trusted project gets its profile; the entry was removed and the hash equals the one before |
| I21 | trust can be given for one run without changing the file | T2: no entry; `-c "projects={'<scratch>\textkit'={trust_level=\"trusted\"}}"` | `active_permission_profile` `wave`; `[probe aedba23] probe`; hash unchanged | a one-run alternative for `codex exec` |
| I21 | a profile given at user level also needs trust | T3: no entry; `-c 'default_permissions="wave"' -c "permissions.wave.filesystem={\":root\"=\"read\", '<scratch>'=\"write\", \":tmpdir\"=\"write\"}"` | `active_permission_profile` `wave`; `[probe 93da6ed] probe`; `~/.codex/config.toml` got `[projects.'c:\users\…\textkit']` `trust_level = "trusted"` (lower case), written by Codex | a user-level profile applies without trust, and Codex then trusts the folder itself (as in I13); the entry was removed with `trust_entry.py` below and the hash equals the one before. The `[permissions]` form in `~/.codex/config.toml` itself was not tried: the user permitted only the test project's entry |

Side notes: a first T1 attempt wrote a malformed key (the shell expanded `\t` and `\U` in the path); its run was
discarded and the file restored from the copy taken before T0 (hash equal). Every run with the profile also listed
`<scratch>\textkit\.codex` as `read`, T3 included, whose `-c` profile did not name it. Codex compares the trust path
without letter case: T1's upper-case entry and T3's lower-case one both name the same folder. The desktop app: not
verifiable by running here, and by the user's direction not rehearsed.

## Fixes after wave 7 (re-plan 2026-11-26, round 3, override)

F1 is past the re-plan limit and re-planned by the user's override: escalated, every new task `high`. Wave 7 ran N, O
and P: N's rehearsal stopped at X1 because the untrusted project ran read-only (I21), O was not run (desktop control
denied, I19), P changed nothing ("CLI profile works" false). Line numbers are those of
`feat/desktop-coordinator-p2/F1-codex-coordinator` at 89a4ecb.

| Entry | Essence | Fixed by |
|---|---|---|
| I21, I8 | the project's profile needs a trusted project; the docs do not say how | task S, "Trust docs (task S)"; verified by task T, run X1 |
| I15 | permissions the pipeline works with | evidence above (trust entry, `-c` trust, user-level profile); task T, X1–X4 |
| I14 | the rest of the CLI pipeline | task T, X2–X5 |
| I9, I18 | shells start in the project | task T, check 7; outside the user profile verified in round 2; macOS and Linux go to the record's "Not verified" |
| I10, I11, I12, I16, I17 | model of `low` steps, the model lookup, the coordinator's texts, prompts judged by behaviour | task T, checks 1, 6 and 8 |
| I2 | claims match the records | task U, "Claims after the rehearsal (task U)" |
| I19 | the desktop app rehearsal | not rehearsed by the user's decision; task U records it |

`trust_entry.py`, the helper task T writes into `<scratch>` (never into the repository), tested in planning on a copy
of `~/.codex/config.toml`: `add` then `remove` gives back the same hash; a `remove` with nothing to remove changes
nothing:

```python
"""usage: python trust_entry.py add <config.toml> <project path>
       python trust_entry.py remove <config.toml> <scratch folder>"""
import re
import sys

action, config, path = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("\\/")
text = open(config, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in text else "\n"
if action == "add":
    if text and not text.endswith(nl):
        text += nl
    text += f"[projects.'{path}']{nl}trust_level = \"trusted\"{nl}{nl}"
elif action == "remove":
    key = path.lower().replace("/", "\\")
    header = re.compile(r"^\[projects\.'([^']*)'\]\s*$")
    lines, out, i = text.split(nl), [], 0
    while i < len(lines):
        m = header.match(lines[i])
        p = m.group(1).lower().replace("/", "\\") if m else ""
        if m and (p == key or p.startswith(key + "\\")):
            print("removed", lines[i])
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("["):
                i += 1
            if i < len(lines) and not lines[i].strip():
                i += 1
            continue
        out.append(lines[i])
        i += 1
    text = nl.join(out)
else:
    sys.exit("usage: trust_entry.py add|remove <config.toml> <path>")
open(config, "w", encoding="utf-8", newline="").write(text)
```

### Trust docs (task S)

Files: `README.md`, `skills/wave-plan/layout.md`, `skills/wave-plan/CHANGELOG.md`. Lines at most 120 characters,
except table rows and lines inside fenced blocks.

1. `README.md`, section `### Codex permissions` (lines 62-78): after the closing fence of its `toml` block and the
   blank line after it, before `The sandbox stays on: Codex reads everything …`, insert (a blank line after it):

   ````
   Codex reads this file only in a project it trusts; in any other folder it runs read-only and the skills stop
   `git-read-only`. To trust the project, add its entry to `~/.codex/config.toml`, with the absolute path of the
   project folder in single quotes (on Windows with backslashes, as `'C:\Users\me\textkit'`):

   ```toml
   [projects.'<project>']
   trust_level = "trusted"
   ```
   ````

   In the paragraph that follows, `Keep the file out of git (add `.codex/config.toml` to `.git/info/exclude`).` →
   `Keep `.codex/config.toml` out of git (add it to `.git/info/exclude`).`; rewrap that paragraph only.
2. `skills/wave-plan/layout.md`, "Permissions in Codex" (lines 183-202): `in `<repository>/.codex/config.toml` (Codex
   reads it for a trusted project) or in `~/.codex/config.toml`.` → `in `<repository>/.codex/config.toml` of a trusted
   project ("Trust" below) or in `~/.codex/config.toml`.`; after the closing fence of its `toml` block, before `The
   sandbox stays on: the agent reads everything …`, insert (blank lines before and after each part):

   ````
   **Trust.** Codex applies a project's `.codex/config.toml` only when `~/.codex/config.toml` trusts the project: an
   entry under the absolute path of the repository root, in single quotes (Windows paths with backslashes, any letter
   case):

   ```toml
   [projects.'<repository>']
   trust_level = "trusted"
   ```

   In a project without it Codex runs the thread with its built-in `:read-only` profile, and every git write stops
   `git-read-only`. For one `codex exec` run, `-c "projects={'<repository>'={trust_level=\"trusted\"}}"` (bash quoting)
   trusts it without changing the file. A profile given on the command line (`-c 'default_permissions="wave"'` with
   `-c 'permissions.wave.filesystem={…}'`) applies without trust; Codex then adds the entry itself, as it does when a
   run in a new folder gets write access.
   ````

   Rewrap only the sentence of the first change.
3. `layout.md`, "Vendors", row `git writes` (line 167), Codex cell: `the permission profile of "Permissions in Codex";
   the default `workspace-write` keeps `.git` read-only` → `the permission profile of "Permissions in Codex", in a
   trusted project; the default `workspace-write` keeps `.git` read-only` (one physical line).
4. `skills/wave-plan/CHANGELOG.md`, the `- Unreleased` item: after its last line (`subagents carry the model lookup
   right after the gate line.`), two continuation lines with a two-space indent:

   ```
     Codex applies a project's profile only in a trusted project: README "Codex permissions" and `layout.md`
     ("Permissions in Codex", "Trust") show the entry of `~/.codex/config.toml` that trusts it.
   ```

Nothing else changes; the rehearsal claims are task U's.

### Rehearsal D3 — Codex CLI in a trusted test project (task T)

Rehearsal D2 again ("Rehearsal D2 — Codex CLI with the permission profile", which changes Rehearsal D), with these
changes; the record replaces `docs/rehearsals/coordinator-codex-cli.md`.

- `<scratch>`: a new empty folder `~/wave-rehearsal-<YYYYMMDD-HHMM>`, outside every repository and the temp folder,
  never used by Codex. Fixture, skills with the Codex links and `<scratch>/textkit/.codex/config.toml` as in D2,
  following README "Codex permissions" of the working folder (which task S extended with the trust entry).
- `<trusted>`: the Windows form of `<scratch>/textkit` (`cygpath -w`), e.g. `C:\Users\<name>\wave-rehearsal-…\textkit`.
- Before X0: copy `~/.codex/config.toml` to `<scratch>/calls/config.before.toml` (a safety copy, never committed), keep
  its SHA-256 and its `[projects.` lines; write `trust_entry.py` (above) to `<scratch>/trust_entry.py`; then
  `python <scratch>/trust_entry.py add ~/.codex/config.toml '<trusted>'`. This is the only change to that file that the
  user permitted: one entry for the test project, removed afterwards. Never add or change any other entry or key.
- Removal, right after the last Codex call, and also before any early stop of the task (a failed X1, the cap, an error):
  `python <scratch>/trust_entry.py remove ~/.codex/config.toml '<Windows form of <scratch>>'`. It also removes the
  entries Codex adds itself for folders below `<scratch>` (worktrees, I13). Then the SHA-256 must equal the one before.
  Equal → check 9 Pass. Not equal → a finding: quote `diff <scratch>/calls/config.before.toml ~/.codex/config.toml`
  with paths replaced; never restore the safety copy over the file (other changes may be the user's or an app's); name
  the copy in the report.
- `<mode>` as in D2 (`-C <scratch>/textkit -c 'approval_policy="never"'`, no `-s`, no `sandbox_mode`, no bypass, no
  `danger-full-access`); never the `-c "projects=…"` option: the rehearsal tests the documented entry.
- X1 expected: `Get-Location` is the project; `sandbox_policy` `workspace-write` with `writable_roots` `["<scratch>"]`
  and `active_permission_profile` `wave` in the `turn_context`; the worktree and commit exist. A failure is a finding;
  then remove the entry, and X2–X5 are Not run.
- X2–X5 and checks 1–9 as in D2; check 9 is the removal above plus the list of `[projects.` lines the run added (paths
  as `<scratch>`), which must all lie below `<scratch>`.
- `## Plugin install`: keep the section of the record on the branch (task N, 2026-11-26) unchanged as the last section;
  do not run the plugin commands again (I3 is closed).
- Record, after the header paragraph: `## Earlier attempts (2026-11-26)`, at most eight lines: under `workspace-write`
  the pipeline stopped at its first step (findings D1–D6, commit 7bcdaf1); with the project's profile in a project
  Codex did not trust, the thread ran read-only and X1 failed (finding N1, commit d794ad8). Then `## Setup` (with the
  trust entry, written as `[projects.'<scratch>\textkit']`), `## Runs` (X0–X5), `## Results`, `## Not verified` (the
  Codex desktop app: not rehearsed by the user's decision of 2026-11-26; macOS and Linux), `## Repeat` (with the
  `trust_entry.py` add and remove commands), `## Plugin install`.
- Caps: 3 hours of Codex calls. Leave `<scratch>` in place and name it in the report.

### Claims after the rehearsal (task U)

The definitions and edits 1–4 of "Claims after the rehearsals (task P)" (which take edits 1–3 and the first three
definitions from "Claims after the rehearsals (task I)"), unchanged, read from the CLI record of task T and the
desktop record of task O. The desktop record is not rehearsed again (the user's decision of 2026-11-26), so
"Desktop rehearsed" is false, "Desktop session start" is not recorded and edit 4 takes its last row, unless the
record says otherwise. If "CLI profile works" is false, change nothing and stop, as for P.

5. `docs/rehearsals/coordinator-codex-desktop.md`: after its header paragraphs, before `## Setup`, insert:

   ```
   ## Not rehearsed by decision

   On 2026-11-26 the user decided not to rehearse the Codex desktop app in this feature: this record stays as it is,
   and README and `skills/wave-plan/layout.md` call the app not rehearsed. Whether the app applies a project's
   permission profile and trust entry (README "Codex permissions") is not known.
   ```

## Acceptance tests (re-plan 2026-11-26, round 3)

Tests 11 and 12 are superseded by 14 and 15.

13. README "Codex permissions" has the trust paragraph and the `[projects.'<project>']` block; `layout.md` "Permissions
    in Codex" has "Trust" with its block and the `-c` sentence; the `git writes` cell names a trusted project; the
    changelog has the two trust lines (task S).
14. The CLI record (task T) shows X1 Pass under the profile in the trusted test project, X2–X5 and checks 1–9 each
    Pass, a Finding with an entry, or Not run with its reason, the earlier attempts and `## Plugin install`; check 9
    shows the hash of `~/.codex/config.toml` equal before and after (task T).
15. README, layout and changelog claim exactly what the CLI record shows and call the Codex desktop app not
    rehearsed; the desktop record has "Not rehearsed by decision" (task U).

## Evidence (re-plan 2026-11-26, round 4)

Override of F1 by the user's direction (quoted in `history.md`): split F1 — merge it with the rehearsal as recorded,
accept the unverified end of a wave, move the remaining findings to a new feature F3. Run in the re-planning session in
a throwaway worktree of `feat/desktop-coordinator-p2/F1-codex-coordinator` at bcd3b0d (removed afterwards).

| Entry | Disputed assumption | Run | Deciding output | Conclusion |
|---|---|---|---|---|
| I2 | the definitions of "Claims after the rehearsals (task I)" and "(task P)", applied to task T's record, give claims that match what was rehearsed (task U) | a Python script that reads the `## Results` tables of both records and applies the definitions verbatim | `X1 ['Pass', 'Pass', 'Pass', 'Pass']`; `X4 ['Pass', 'Finding (T1)', 'Not run', 'Pass (up to the cut)', 'Pass', 'Not run']`; `CLI rehearsed: False · CLI profile works: True`; `E1`, `E2` all `Not run`; `Desktop rehearsed: False` | refuted: U would take the case "neither" and write "in Codex it is not rehearsed yet", although X0–X3 passed and X4 started its wave; and no variant names the end of a wave as an accepted gap. Task X replaces U with fixed texts |
| I2 | the places U edits are where the solution says | `grep -n` on the branch | README `:461` `- **wave-auto** was rehearsed in the Claude Code CLI and desktop app and in the Codex CLI and desktop app`; layout `:165` row `starting a session`; CHANGELOG `:46` ``rehearsals of `$wave-auto` in the Codex CLI and desktop app.``; README `:86-87` `Where the profile cannot be used, full access works` / ``too (`codex -s danger-full-access`).`` (wrapped); desktop record `## Setup` at `:13`; CLI record `:331` `- The end of a wave in Codex: …` | confirmed; X finds each place by its quoted text |
| I14 | (accepted by the user) | the F1 check on bcd3b0d | 39 and 59 tests `OK`; three examples exit 0; `git diff --check main` exit 0 | F1 is green as it stands; only texts change |
| I23 | the user can review a branch of a sandbox-made worktree without changing ownership | in `~/wave-rehearsal-20261126-1955`: `git -C <worktree> status`; the same with `git -c safe.directory=<worktree>`; `git -C textkit log -2 integration/text-utilities` from the main checkout | `fatal: detected dubious ownership … owned by: …/CodexSandboxOffline`; with `-c safe.directory=…` exit 0; from the main checkout the log prints `5bb99bc`, `a4c08ac` | both ways work: review from the main checkout, or name the worktree in `safe.directory` (texts of task AB) |

I12 and I22 are behaviour of a GPT model in Codex: not verifiable by running here (the Codex account hit its usage
limit at 20:12, reset 23:09, and by the direction F3 has no rehearsal); checked instead: the rules they break are
already explicit (`skills/wave-auto/SKILL.md:51-54`, step 4 at `:129-130`), so F3 states the Codex case in the place
where the model acts, and its acceptance is the text only.

## Split of F1 (re-plan 2026-11-26, round 4, override)

F1 stops depending on a new live run: its done-when takes task T's record as it is. Findings of a later Codex run go to
a new plan, never back into F1 or F3.

| Entry | Essence | Fixed by |
|---|---|---|
| I14 | the end of a wave in Codex is not verified (usage limit) | accepted by the user on 2026-11-26; task X names it in README Limitations and the CLI record |
| I2 | claims match the records | task X, "Claims after the split (task X)" |
| I19 | the desktop app is not rehearsed | the user's decision of round 3; task X records it |
| I12 | the coordinator's first line and its own sentences | feature F3, task AA |
| I22 | questions go to `request_user_input_async` in `codex exec` | feature F3, task AA |
| I23 | git refuses sandbox-made worktrees in the user's shell | feature F3, task AB |

### Claims after the split (task X)

Files: `README.md`, `skills/wave-plan/layout.md`, `skills/wave-plan/CHANGELOG.md`,
`docs/rehearsals/coordinator-codex-desktop.md`, `docs/rehearsals/coordinator-codex-cli.md`. Find every place by its
quoted text; lines at most 120 characters except table rows; rewrap only what is edited.

1. `README.md`, Limitations, the bullet `- **wave-auto** was rehearsed in the Claude Code CLI and desktop app and in the
   Codex CLI and desktop app` with its continuation line → (two-space continuation indent):

   ```
   - **wave-auto** was rehearsed in the Claude Code CLI and desktop app ([rehearsals](docs/rehearsals/)), and in the
     Codex CLI up to the start of a wave: triage, the questions, the plan and the launch of a wave's tasks passed,
     while the end of a wave in Codex (task commits, the merge into `integration/<topic>`, auto-approval) is not
     verified yet. The Codex desktop app is not rehearsed. Its rails (`until`, `steps`) are rules of the skill, not
     enforced limits.
   ```

2. `skills/wave-plan/layout.md`, "Vendors", row `starting a session`, Codex cell ``none in the CLI; the desktop app as
   its rehearsal recorded (`docs/rehearsals/coordinator-codex-desktop.md`)`` → `none in the CLI; the desktop app not
   verified, so treat it as missing` (one physical line).
3. `skills/wave-plan/CHANGELOG.md`, the `- Unreleased` item: `README shows the Codex plugin install;` followed by
   ``rehearsals of `$wave-auto` in the Codex CLI and desktop app.`` → ``README shows the Codex plugin install; a
   rehearsal of `$wave-auto` in the Codex CLI up to the start of a wave.``; rewrap only these lines, two-space indent.
4. `README.md`, "### Codex permissions": after the sentence ``Where the profile cannot be used, full access works too
   (`codex -s danger-full-access`).`` add `The Codex desktop app is not rehearsed with it yet.`; rewrap that paragraph
   only.
5. `docs/rehearsals/coordinator-codex-desktop.md`: after its header paragraphs, before `## Setup`, insert (blank lines
   around it):

   ```
   ## Not rehearsed by decision

   On 2026-11-26 the user decided not to rehearse the Codex desktop app in this feature: this record stays as it is,
   and README and `skills/wave-plan/layout.md` call the app not rehearsed. Whether the app applies a project's
   permission profile and trust entry (README "Codex permissions") is not known.
   ```

6. `docs/rehearsals/coordinator-codex-cli.md`, "## Not verified", the bullet `- The end of a wave in Codex: …` ending
   `cut by the usage limit (T1).` → append ` The user accepted this gap on 2026-11-26: the feature is merged without
   it.` and rewrap that bullet only. Nothing else of the record changes.

Nothing else changes. `git grep -n "as its rehearsal recorded" -- skills README.md` prints nothing afterwards.

### Polish (feature F3, tasks AA and AB)

F3 starts from `main` after F1 is merged, so it sees task X's texts. Text edits only; no Codex run.

Task AA, `skills/wave-auto/SKILL.md`:

1. "Hard rules", the bullet that starts `- It writes the user only what this skill names:` and ends ``Its first message
   starts with the `Started:` line: no sentence comes before it.`` → append (rewrap that bullet only):

   ```
   It reads the clock before it writes any text, so that line always carries the time (`Started: 2026-11-26 19:57`):
   never a `Started:` line without a time, never a second one. It never restates its questions, results or plans in
   its own words (no table of the questions, no sentence that opens or closes a message); this holds for every model,
   also one that tends to announce what it will do.
   ```

2. "Start phase", step 1: ``1. Read the clock (`Started:` line, `wave-plan/layout.md`, "Run times");`` →
   ``1. Read the clock with a shell command before writing anything, then write the `Started:` line with that time
   (`wave-plan/layout.md`, "Run times");`` — the rest of the step unchanged; rewrap the step only.
3. "Start phase", step 4: `ask them all in one message and` / `wait.` → the text below; the next sentence
   (``With `questions 0`, …``) unchanged; rewrap step 4 only:

   ```
   ask them all in one message, as the text of your answer, and wait (end the turn). In Codex never use
   `request_user_input_async` or another input tool for them: in `codex exec` it only sleeps.
   ```

Task AB, `README.md` and `skills/wave-plan/layout.md`:

1. `README.md`, "### Codex permissions": after the paragraph that ends ``Details: `skills/wave-plan/layout.md`,
   "Vendors".``, before `### Installer (a copy inside the project)`, insert one paragraph (blank lines around it):

   ```
   On Windows the worktrees that Codex creates in its sandbox belong to the sandbox account (`CodexSandboxOffline`),
   and git in your own shell refuses them with `detected dubious ownership`. Review the branches from the main
   checkout (`git log <branch>`, `git diff main...<branch>`), or allow one worktree for a command with
   `git -c safe.directory='<worktree path>' …` (or for good with `git config --global --add safe.directory`).
   ```

2. `skills/wave-plan/layout.md`, "Permissions in Codex": after the sentence `Subagents inherit it.` insert, in the same
   paragraph, the text below; rewrap that paragraph only:

   ```
   On Windows the worktrees it creates belong to the sandbox account, and git outside the sandbox refuses them
   (`detected dubious ownership`): the user reviews a feature branch from the main checkout or names the worktree in
   `safe.directory`.
   ```

## Acceptance tests (re-plan 2026-11-26, round 4)

Test 15 is superseded by 16.

16. README Limitations says the Codex CLI was rehearsed up to the start of a wave, that the end of a wave in Codex is
    not verified and that the desktop app is not rehearsed; the `starting a session` Codex cell is `none in the CLI; the
    desktop app not verified, so treat it as missing`; the changelog says ``a rehearsal of `$wave-auto` in the Codex CLI
    up to the start of a wave``; README "Codex permissions" says the desktop app is not rehearsed with it; the desktop
    record has "Not rehearsed by decision"; the CLI record's "Not verified" says the user accepted the gap; the F1 check
    is green (task X).
17. `skills/wave-auto/SKILL.md` has the time rule and the no-restating rule in "Hard rules", step 1 reads the clock
    before writing, step 4 forbids `request_user_input_async`; README "Codex permissions" and layout "Permissions in
    Codex" name `detected dubious ownership` and `safe.directory`; the check is green (tasks AA, AB). The behaviour in
    Codex is not rehearsed in this plan.

## Evidence (re-plan 2026-11-27, round 2)

Round 2 of F3 (its first round was the split of F1, re-plan of 2026-11-26, round 4 of F1). Open entry I33.

Assumption disputed by I33: the README command `git config --global --add safe.directory` (task AB, edit 1 of
"Polish") works as written. Run on 2026-11-27 with git 2.52.0.windows.1 in a scratch folder outside the repository
(`<s>` = the scratch folder, `repo` a fresh repository with one commit, `cfg` an empty config file):

| Command | Deciding output | Exit |
|---|---|---|
| `git config --file cfg --add safe.directory` | `error: wrong number of arguments, should be 2` | 129 |
| `git config --file cfg --add safe.directory "<s>/repo"` | `cfg` gets `[safe]` / `directory = C:/…/repo` | 0 |
| `GIT_TEST_ASSUME_DIFFERENT_OWNER=1 git -C repo log --oneline` | `fatal: detected dubious ownership in repository at '…/repo'`, then git's hint `git config --global --add safe.directory C:/…/repo` | 128 |
| `GIT_TEST_ASSUME_DIFFERENT_OWNER=1 git -c safe.directory="<s>/repo" -C repo log --oneline` | `c23e97e init` | 0 |
| the same with a global config (`GIT_CONFIG_GLOBAL`) holding `safe.directory` = the path | `c23e97e init` | 0 |
| the same `-c` form with the backslash path `C:\…\repo` | `c23e97e init` | 0 |

Conclusion: the command without a path fails, as I33 says; with the worktree path it works, both for good (global
config) and for one command (`-c`), with forward or back slashes. The `-c` form of the README is right as written.

Not verifiable by running: a worktree really owned by the Codex sandbox account (`CodexSandboxOffline`); this session
has no Codex sandbox. Checked instead with git's own test switch `GIT_TEST_ASSUME_DIFFERENT_OWNER=1`, which makes git
treat the repository as owned by another account and prints the same `detected dubious ownership` error.

## Fix after wave 14 (re-plan 2026-11-27, round 2 of F3)

### Safe-directory command (task AE)

`README.md` on the F3 branch, section "### Codex permissions", the paragraph that starts "On Windows the worktrees
that Codex creates in its sandbox": its last line

```
`git -c safe.directory='<worktree path>' …` (or for good with `git config --global --add safe.directory`).
```

becomes these two lines (the three lines before it stay as they are):

```
`git -c safe.directory='<worktree path>' …` (or for good with
`git config --global --add safe.directory '<worktree path>'`).
```

Nothing else changes: the layout's sentence ("names the worktree in `safe.directory`") gives no command and is right.

## Acceptance tests (re-plan 2026-11-27, round 2)

18. `README.md` has `` `git config --global --add safe.directory '<worktree path>'` `` and no
    `` --add safe.directory` `` without a path; the paragraph's lines are at most 120 characters; the F3 check is
    green (task AE).
