# Open problems
Next ID: I22

- **[I2 · wave 1 / task A / feature F1] README and layout already claim Codex rehearsals that are not recorded yet** —
  where: `README.md:434`, `skills/wave-plan/layout.md:160`; expected / got: claims backed by records in
  `docs/rehearsals/` / the texts of the solution, taken verbatim, while tasks D and E have not run; since wave 7 both
  records exist and show runs X2–X5 and E1–E4 as Not run, and task P changed nothing (I21), so the claims are still
  unbacked; proposal: run the rehearsals before F1 is merged, and correct both sentences if a rehearsal is recorded as
  Not run; status: open
- **[I8 · wave 2 / task D / feature F1] Under the Codex `workspace-write` sandbox `.git` is read-only, so `$wave-auto` stops at its first step** — where: `skills/wave-plan/layout.md:148-162` ("Vendors" and `README.md` say nothing about Codex permissions); runs X1, X2 in `docs/rehearsals/coordinator-codex-cli.md`;
  expected / got: a worktree and a commit / `cannot lock ref ... Permission denied`, then `Stop repository-read-only` (a code no skill defines), no question, branch or claim;
  proposal: decide and document which permissions the wave skills need in Codex and how to grant them (an extra writable root for `.git` was not tried), then repeat the rehearsal;
  wave 7: the permissions are documented (tasks L, M) but not verified, because the project's profile was not applied
  (I21);
  status: open
- **[I9 · wave 2 / task D / feature F1] In the Windows sandbox of Codex, commands do not start in the project folder** — where: `skills/wave-plan/layout.md:148-162`; runs X1, X2;
  expected / got: commands run in the project / root and subagent shells ran in `C:\`, and `Set-Location` into the project was denied once;
  proposal: check with a project outside the user profile; if it repeats, require full paths and `git -C` for Codex in "Vendors";
  wave 7, run X1: the root shell started in the project; no subagent ran;
  status: open
- **[I10 · wave 2 / task D / feature F1] `gpt-6-luna` is not chosen for `low` steps** — where: `skills/wave-plan/layout.md:156`, `skills/wave-auto/SKILL.md:61-63`; run X2, check 1;
  expected / got: three model IDs and `status` on `gpt-6-luna` / `low` and `medium` both `gpt-6.2-sol`; the `spawn_agent` description does not list `gpt-6-luna`;
  proposal: say in "Vendors" that the ID of "Model tiers" is passed even when the tool does not list it, and what to do when it is refused;
  wave 7: not verified, no coordinator ran (I21);
  status: open
- **[I11 · wave 2 / task D / feature F1] A `high` step subagent in Codex did not check its own model** — where: `skills/wave-plan/layout.md:122-125`, `:693-694`, `skills/wave-auto/SKILL.md:79`; run X2;
  expected / got: the model lookup before any read or change / `triage_ask` ran no lookup and named no model; whether its prompt had the gate line cannot be read (encrypted);
  proposal: make the lookup an explicit part of the step prompt for Codex and check it in the next rehearsal;
  wave 7: not verified, no subagent ran (I21);
  status: open
- **[I12 · wave 2 / task D / feature F1] The Codex coordinator leaves the fixed output texts** — where: `skills/wave-auto/SKILL.md:41`, `:51-53`, `:225`, `:232`, `:236`, `:244`; run X2;
  expected / got: `Started:` first, the given title, return lines, `next:` in Halts, the real start in `Continue:` / a preamble, an invented title, a retold result, no `next:`, a placeholder `<original list>`;
  proposal: tighten these rules at the next `wave-auto` edit and check them again in Codex;
  wave 7: not verified, no coordinator ran (I21);
  status: open
- **[I14 · wave 2 / task D / feature F1] Not checked: the whole Codex CLI pipeline after its first step (questions, resume, plans, waves, parallel limit, trailers, claims, merge, tests)** — where: `docs/rehearsals/coordinator-codex-cli.md`, runs X3-X5 and checks 2, 3;
  expected / got: a recorded run / Not run because of I8; not run again in wave 7 (task N), because of I21;
  proposal: repeat the rehearsal once I8 and I21 are solved;
  status: open
- **[I15 · wave 2 / task D / feature F1] Not checked: whether the pipeline works with other Codex permissions** — where: `docs/rehearsals/coordinator-codex-cli.md`, "Not verified";
  expected / got: the permissions it needs are known / neither the bypass option (forbidden by the user for this run) nor an extra writable root for `.git` was tried;
  proposal: an extra writable root for `.git` was tried by the coordinator on 2026-11-26 and does not help (wave 2,
  Execution: Codex lists `.git` as both `write` and `read`, and the write is refused); not tried: a custom permission
  profile or a git directory elsewhere;
  wave 7: the project profile was tried and not applied in an untrusted folder (I21);
  status: open
- **[I16 · wave 2 / task D / feature F1] Not checked: the model lookup of "Vendors" inside the Codex sandbox** — where: `skills/wave-plan/layout.md`, "Vendors"; `docs/rehearsals/coordinator-codex-cli.md`;
  expected / got: the lookup prints a model ID in a sandboxed thread / no thread ran it;
  proposal: run it in the next rehearsal;
  wave 7: no thread ran it (I21);
  status: open
- **[I17 · wave 2 / task D / feature F1] Not checked: the texts of the step prompts in Codex** — where: `docs/rehearsals/coordinator-codex-cli.md`, "Not verified";
  expected / got: the prompts can be inspected / encrypted in the rollout files and absent from the stream;
  proposal: judge the prompts by what the step subagents do, or accept the limit;
  wave 7: no step subagent ran (I21, I19);
  status: open
- **[I18 · wave 2 / task D / feature F1] Not checked: whether I9 happens outside the user profile, or on macOS or Linux** — where: `docs/rehearsals/coordinator-codex-cli.md`, "Not verified";
  expected / got: known / only one Windows project below the user profile was run;
  proposal: check it with I9;
  wave 7: still only a Windows project below the user profile;
  status: open
- **[I19 · wave 2 / task E / feature F1] The Codex desktop app rehearsal was not run** — where:
  `docs/rehearsals/coordinator-codex-desktop.md`, `solutions/P2-codex-coordinator.md`, "Rehearsal E";
  expected / got: a recorded run in the app / the user closed wave 2 without it on 2026-11-26, since it likely meets I8;
  wave 7 (task O): not run again, desktop control of the app (listed as `ChatGPT`) was denied (`user_denied`); the
  record exists with every step Not run, so it is still unknown whether the app applies the profile;
  proposal: decide I21 first, then plan the desktop rehearsal again or record the app as not rehearsed (see I2); a
  full-access mode of the app needs the user's explicit permission;
  status: open
- **[I21 · wave 7 / task N / feature F1] Codex CLI does not apply the permission profile of `<project>/.codex/config.toml` in a project it was never told to trust: the thread runs read-only** —
  where: `README.md:62-78`, `skills/wave-plan/layout.md:183-202` ("for a trusted project"); run X1 and finding N1 in
  `docs/rehearsals/coordinator-codex-cli.md`;
  expected / got: a worktree and a commit / `sandbox_policy` `read-only`, active profile `:read-only`, nothing created,
  X2–X5 not run. Probable cause, not verified: the new folder is not trusted; `codex exec` with `-C` and
  `approval_policy` added no trust entry, against the planning evidence "Codex writes a trust entry for every new
  project folder", and neither the README nor the layout says how a project becomes trusted. Task P changed nothing for
  this reason ("CLI profile works" is false); its edits run after the fix;
  proposal: the user decides how a project becomes trusted (a `[projects.…]` entry, or the profile in
  `~/.codex/config.toml`; both change the user's Codex settings), then document it and repeat the CLI rehearsal;
  status: open
