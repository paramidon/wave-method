# Lite solutions (low problems)

## P2. Every evidence rule admits the "not verifiable by running" fallback

User problem: the planner's self-check demands an `Evidence` section with a command run in the session, while
`layout.md`, "Re-plan escalation", step 3 allows `not verifiable by running: <why>` and the alternative check when
nothing can be run; align every evidence rule with that fallback (I2, found by task B in wave 1) · feature F1

Cause: three texts on the feature branch name only the "run it" path; `skills/wave-plan/layout.md:243-245` (the
source of truth) names both. Disagreeing: `skills/wave-plan/SKILL.md:126-128` (step 2 bullet),
`skills/wave-plan/SKILL.md:252-255` (step 8 "Re-plan rounds" bullet, the one I2 names) and
`skills/wave-plan/templates.md:72` (the solution template's `Evidence` line). `layout.md` stays unchanged.

**Edit 1 (task F):** `skills/wave-plan/SKILL.md`, step 2, replace the bullet

```markdown
- Escalated re-plan (`layout.md`, "Re-plan escalation"): for every open entry of the feature, name the disputed
  assumption and verify it by running code, tests or commands in a throwaway worktree or a scratch folder, never by
  reading alone; record the evidence in the solution file the new tasks name.
```

with

```markdown
- Escalated re-plan (`layout.md`, "Re-plan escalation"): for every open entry of the feature, name the disputed
  assumption and verify it by running code, tests or commands in a throwaway worktree or a scratch folder, never by
  reading alone; record the evidence in the solution file the new tasks name. When it cannot be run (a tool this
  session lacks, a GUI), record `not verifiable by running: <why>` and what was checked instead.
```

**Edit 2 (task F):** `skills/wave-plan/SKILL.md`, step 8, replace the bullet

```markdown
- Re-plan rounds: the new `Re-plans:` sub-item names every feature planned from wave entries under `fixes:`, from
  round 2 under `escalated:` and past the limit under `override:`; every escalated feature has an `Evidence` section
  with a command run in this session, only `high` new tasks and, in autonomous flow, a place in `manual review:`; a
  held feature got no task.
```

with

```markdown
- Re-plan rounds: the new `Re-plans:` sub-item names every feature planned from wave entries under `fixes:`, from
  round 2 under `escalated:` and past the limit under `override:`; every escalated feature has an `Evidence` section
  (with a command run in this session, or `not verifiable by running: <why>` and what was checked instead), only
  `high` new tasks and, in autonomous flow, a place in `manual review:`; a held feature got no task.
```

**Edit 3 (task G):** `skills/wave-plan/templates.md:72`, replace the line

```markdown
**Evidence (re-plan <YYYY-MM-DD>, round <r>):** assumption, commands, deciding output lines, conclusion (escalated re-plans only: `layout.md`, "Re-plan escalation")
```

with

```markdown
**Evidence (re-plan <YYYY-MM-DD>, round <r>):** assumption, commands, deciding output lines, conclusion — or `not verifiable by running: <why>` and what was checked instead (escalated re-plans only: `layout.md`, "Re-plan escalation")
```

**Check:** `git grep -n "not verifiable by running" skills/wave-plan` → exactly four lines: `layout.md` (step 3 of
"Re-plan escalation"), `SKILL.md` (step 2 bullet and step 8 bullet) and `templates.md` (the `Evidence` line);
`git grep -n "with a command run in this session, only" skills/wave-plan/SKILL.md` → no match; the plan's check
command stays green.
