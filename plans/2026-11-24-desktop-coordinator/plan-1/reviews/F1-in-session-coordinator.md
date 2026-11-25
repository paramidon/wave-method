# F1 · In-session coordinator

- Branch: `feat/desktop-coordinator-p1/F1-in-session-coordinator` · worktree: `D:/Documents/orbits/wave-method.worktrees/desktop-coordinator-p1-F1`

## Tasks

- A (wave 1) — the contract between the coordinator and the skills it starts is now in `layout.md` ("Coordinated runs": eleven steps with their return lines, the coordinator claim), and six places of `layout.md` name `wave-auto`.
- B (wave 1) — `wave-run` can run as a coordinated step (every task in task mode, a one-line return, the new stop `manual-flow`), and task mode keeps the report block in the last commit, skips an already committed task and takes fix requests through the wave file.
- C (wave 1) — `wave-triage` is split into four coordinated phases (ask, answers, cluster, finish) so the coordinator asks the user once and launches the cluster subagents itself.
- D (wave 1) — the rules of the navigator, a read-only low-tier subagent that reads the pipeline state from git and returns the next action in one line, are written (`skills/wave-auto/navigator.md`).
- E (wave 1) — the skill `wave-auto`, the coordinator that runs triage, plans and waves from one command in one session through subagents, is written (`skills/wave-auto/SKILL.md`).
- J (wave 3) — the navigator now reports every halted unit instead of at most four, `wave-plan` knows that a coordinated run ends with a return line, and `wave-status` shows coordinator claims and offers `/wave-auto` for an index.
- K (wave 3) — the installers and the plugin files install the fifth skill `wave-auto`, and the README and the changelog describe `/wave-auto`.
- L (wave 3) — the rehearsal of `/wave-auto` in the Claude Code CLI on a small fixture project is recorded in `docs/rehearsals/coordinator-cli.md`: questions asked once, a rail, a resume in a new session, a claim takeover, two merged features and green tests; it found three issues (I2–I4).
- M (wave 3) — the desktop-app rehearsal of `/wave-auto` is recorded in `docs/rehearsals/coordinator-desktop.md`: from a list to both features merged into the integration branch in a separate session, and a second session that found nothing left to run; it found two new issues (I7, I8) and repeated I4.

## How to test

- B: open `skills/wave-run/SKILL.md` and `skills/wave-run/task-mode.md` → the stops table has the row `manual-flow`, the paragraph "Coordinated run" follows "Flow form", task mode has the rule "already committed", the waiting line with `(fix <k>/2)` and the section "Fix requests".
- C: open `skills/wave-triage/SKILL.md` → after "Flow of planning" stands "Coordinated phases" with the table of four forms; steps 4 and 8 mention the coordinated run.
- D: read `skills/wave-auto/navigator.md` → an index on `triage/<topic>` with `- Triage: waiting for answers` gives `next: ask <index>`; part 2 after a merged part 1 gives `next: plan <index> part 2`; a wave 🔄 with `Waiting: task mode B (fix 1/2), C` gives `next: tasks <plan folder> 2 B:<tier>; C:<tier>`; all waves ✅ or ⚠️ with an open entry for F2 gives `next: re-plan <plan folder>`.
- E: `head -4 skills/wave-auto/SKILL.md` → frontmatter with `name: wave-auto`; `grep -n "^## " skills/wave-auto/SKILL.md` → Layout, Input, Hard rules, Capabilities, Step prompt, Start phase, Loop, Wave, Results of steps, Session fallback, Rails, End of the run, Stops, Resume.
- J: `grep -n "one per halted unit" skills/wave-auto/navigator.md skills/wave-plan/layout.md` → one line in each file; `grep -n "claims/auto/" skills/wave-status/SKILL.md` → the read bullet and the Leftovers suggestion.
- K: `grep -n "wave-auto" install.sh install.ps1 .claude-plugin/plugin.json` → one line each; README has the subsection "One command in one session: wave-auto"; after the installer runs in a fresh project, `.claude/skills` holds five folders including `wave-auto`.
- L: open `docs/rehearsals/coordinator-cli.md` → sections Setup, Runs, Results, Not verified, Repeat; Results show every expectation as Pass or Finding with commit hashes and quoted lines.
- M: open `docs/rehearsals/coordinator-desktop.md` → Results shows every Rehearsal I expectation as Pass, Finding or Not run, with evidence.
