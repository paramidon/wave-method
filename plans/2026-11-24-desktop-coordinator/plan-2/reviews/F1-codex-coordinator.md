# F1 · The coordinator and the wave skills in Codex

- Branch: `feat/desktop-coordinator-p2/F1-codex-coordinator` · worktree: `D:\Documents\orbits\wave-method.worktrees\desktop-coordinator-p2-F1`
- 👀 review since 2026-11-26 20:55

## Essence

`$wave-auto` and the wave skills can be run in the Codex CLI. Before, a Codex agent could not name its model, so the
tier gate stopped every medium and high step; now the skills name GPT models per tier, look the model up, limit
parallel subagents and document the permissions Codex needs. Rehearsed in the Codex CLI up to the start of a wave only.

## How to test

1. In a scratch project with the skills installed, the "Codex permissions" profile and its trust entry set up, start
   `codex -m gpt-6.2-astra` and type `$wave-auto` with two small changes → `Capabilities:` names `parallel 3` and a GPT
   model per tier, the questions come once, triage and planning print one line per step and the first wave starts
   (remove the trust entry afterwards).
2. The same in a project where Codex cannot write `.git` → `Started:` first, then `Stop git-read-only: …`.
3. Open `README.md`, "Codex permissions" → a TOML permission profile, the `[projects.'<project>']` trust entry, and
   the sentence "The Codex desktop app is not rehearsed with it yet."
4. Open `README.md`, Limitations → the `wave-auto` item says the Codex CLI was rehearsed up to the start of a wave,
   the end of a wave is not verified and the Codex desktop app is not rehearsed.

## Worth a look

- Never run in Codex: the end of a wave (task commits, the merge, auto-approval); the Codex account hit its usage
  limit and the user accepted the gap on 2026-11-26. The Codex desktop app was not rehearsed, by the user's decision.
- Seen in the CLI rehearsal and not fixed here, but in the next small feature (F3): the coordinator adds lines of its
  own, `codex exec` first tries an input tool for its questions, and on Windows the user's own shell refuses the
  worktrees Codex made (`detected dubious ownership`).
- `README.md`, Limitations: "Its rails (`until`, `steps`)" now follows the sentence about the Codex desktop app, so
  "Its" can be read as the app, though it means `wave-auto` (the text is the plan's, copied verbatim).

## Tasks

- A (wave 1) — documented Codex as a vendor: GPT model tiers, the model lookup, the plugin install in the README.
- B (wave 1) — the launching skills take the tier's model and the way to launch and wait from "Vendors" and launch at
  most the parallel limit of subagents (Codex: 3).
- D — ➖ superseded by T
- E — ➖ superseded by O
- H — ➖ superseded by L, M
- I — ➖ superseded by N, P
- L (wave 6) — the skills describe a Codex permission profile that allows git writes and the stop `git-read-only`;
  prompts to Codex subagents carry the model lookup line; the GPT model names in the skill descriptions are fixed.
- M (wave 6) — `wave-auto` takes each tier's own model, checks before the first step that it can write git, passes the
  model lookup to its steps and keeps its fixed output texts.
- N — ➖ superseded by T
- O — ➖ dropped: the user decided not to rehearse the Codex desktop app
- P — ➖ superseded by U
- S (wave 9) — the docs say that Codex applies a project's permission profile only in a trusted project, and show
  how to trust it (the `~/.codex/config.toml` entry, or `-c` for one `codex exec` run).
- T (wave 9) — rehearsed `$wave-auto` in the Codex CLI in a trusted project: it ran through triage, planning and the
  start of a wave, then the account's usage limit ended the run; recorded as it ran.
- U — ➖ superseded by X
- X (wave 12) — README, layout and changelog claim only what was rehearsed in Codex; both rehearsal records note the
  user's decisions.

## Check

`python skills/wave-plan/scripts/test_status_check.py`, `python -m unittest discover -s scripts/tests`,
`status_check.py` over `examples/*/`, `git diff --check main` → on 788547a: 39 and 59 tests OK, three examples pass,
diff check clean; tests added or changed: none (the feature changes skill texts and docs).
