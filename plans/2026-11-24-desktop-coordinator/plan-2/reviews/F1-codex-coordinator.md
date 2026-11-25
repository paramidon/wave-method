# F1 · The coordinator and the wave skills in Codex

- Branch: `feat/desktop-coordinator-p2/F1-codex-coordinator` · worktree: `D:\Documents\orbits\wave-method.worktrees\desktop-coordinator-p2-F1`

## How to test

- B: `$wave-auto <list>` in Codex → `Capabilities:` names `parallel 3` and the GPT models, and no more than three
  subagents run at once.
- L: open `README.md` → a section "Codex permissions" with a TOML profile follows "Codex plugin"; `layout.md`,
  "Vendors" has the row "git writes" and the paragraph "Permissions in Codex".
- M: `$wave-auto <list>` in Codex with a profile that cannot write `.git` → `Started:` first, then
  `Stop git-read-only: …`; with the right permissions low steps run on `gpt-6-luna`, and a medium or high step runs
  the model lookup first.

## Tasks

- B (wave 1) — the launching skills take the tier's model and the way to launch and wait from "Vendors" and launch at
  most the parallel limit of subagents (Codex: 3).
- E — ➖ superseded by O
- H — ➖ superseded by L, M
- I — ➖ superseded by N, P
- L (wave 6) — the skills describe a Codex permission profile that allows git writes and the stop `git-read-only`;
  prompts to Codex subagents carry the model lookup line; the GPT model names in the skill descriptions are fixed.
- M (wave 6) — `wave-auto` takes each tier's own model, checks before the first step that it can write git, passes the
  model lookup to its steps and keeps its fixed output texts.
