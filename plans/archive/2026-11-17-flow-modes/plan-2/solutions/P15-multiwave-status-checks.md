# P15. Exact wave-status labels, git-based reading, and a multi-wave print-mode chain
User problem: re-plan of I9–I10: `wave-status` prints its merged-feature label exactly, the driver reads merged
features from git and not from report headings, and a multi-wave chain with parallel subagents is measured under
`claude -p` through process exit, validating the caps · feature F4

## Cause

- I9: `skills/wave-status/SKILL.md:62-113` describes the report as prose bullets with placeholder labels. The label
  `Merged, not in <main branch>:` (`skills/wave-status/SKILL.md:79`) is the only label with a placeholder, and the
  same file also uses `<main>`, which in autonomous flow is the integration branch (`skills/wave-status/SKILL.md:39-41`,
  `skills/wave-plan/layout.md:137-140`). In R6 of `docs/rehearsals/print-mode-chain.md:71` the model rendered the
  placeholder twice and mixed in the plan slug. `wave-run` has no such problem: its report has a fenced template and
  a "Before sending" check (`skills/wave-run/report.md:8-21`, `:184-190`); `wave-status` has neither.
- I9, driver side: reading rule 4 of `docs/claude-print-mode.md` ("Prompt form for the driver") only says to read the
  merged-feature details "even if the section heading varies". The state it needs is in git: the README Features row
  (`✅ merged`, `Merged` hash) on the tracking branch, and `git merge-base --is-ancestor`, exactly as
  `skills/wave-status/SKILL.md:50-52` and `skills/wave-plan/layout.md`, "Results of an autonomous run", define it.
- I10: the only chain (`docs/rehearsals/print-mode-chain.md`, R1–R3, R6) had a one-wave plan with two `Agent` calls,
  both returned before the final event. Not measured: a plan with several waves (one `wave-run` call per wave), a
  launch group of two or more tasks at once, subagents run in the background, whether the `result` event comes before
  they end, whether anything changes in the repository after the process exits, and whether the caps of the prompt
  table (`wave-triage` 30 turns / 2 USD, `wave-plan` 50 / 3, `wave-run` 60 / 2, `wave-status` 60 / 0.5), which are
  three times one small measurement, hold for a larger plan.

## Approach

One new feature F4 (F3 is merged; fixes of a merged feature go into a new feature), three tasks in one wave, run one
after another on F4's branch:

- **U** gives `wave-status` a fenced report template with literal labels and a "Before sending" check, as
  `wave-run/report.md` has. The label becomes `Merged, not in main:` with an explicit rule for the branch name. The
  content rules (the bullets) stay; only the form is fixed.
- **V** (after U) runs a second, larger autonomous chain under `claude -p` in a scratch toy repository, with skills
  installed from F4's branch (so with U's template): a six-item list that needs several waves; one `wave-run` call per
  wave; two `wave-status` calls at the end. It records each call, every subagent call and a post-exit check in a new
  record `docs/rehearsals/print-mode-multiwave.md`.
- **W** (after V) updates `docs/claude-print-mode.md`: a table of V's runs, caps recomputed over both chains, reading
  rule 4 replaced by the git recipe below, and "Open points" cleaned.

Why not make the driver parse the headings more leniently: the report's labels follow the user's language
(`wave-run/report.md:18`) and a model can still vary them; git state cannot vary. The template fixes the report for
people; the git recipe makes the driver independent of it. Why a new record and not appending to
`print-mode-chain.md`: it is a different toy list and plan, and R-numbers would clash; the run IDs are M1, M2, ….

Nothing under `skills/` changes except `skills/wave-status/SKILL.md` (task U). A skill defect V finds is a finding
of its record and report, never an edit.

## Model/API changes

### `skills/wave-status/SKILL.md` (task U)

1. Replace the paragraph right under `## Report` (lines 64-65, "For each plan, report the following in order. …
   before anything about waves.") with:

   ```
   The user asked for this report by running the command, and its format is part of that request. Print it as the
   template in "Template" shows; the bullets below say what each line holds. The environment's default answer style
   (short prose, no tables) does not shorten it. Keep a blank line before and after every table and every block.
   Feature status comes first: the user reads it before anything about waves.
   ```

2. Replace the bullet of line 79-83 (`Merged, not in <main branch>:` …) with:

   ```
   - `Merged, not in <main branch>:` autonomous flow only ("Results of an autonomous run" of `layout.md`): the
     merged block of `layout.md`, "Feature review", for every `✅ merged` feature whose `Merged` hash is not in
     `<main branch>` yet, from its brief, in full; `none` when there is no such feature. These are what the user tests
     before merging `integration/<name>`. A feature without a brief gets the block built as `Ready for review:`
     builds one, with the merged block's header and `Approved:` line. In the label, `<main branch>` is replaced by
     the branch name alone, as `git branch` prints it: `Merged, not in main:` or `Merged, not in master:`. Never the
     plan slug, the integration branch, `<main>`, quotes, a possessive or a second rendering of the name; the label
     appears once per plan.
   ```

3. Insert, right before `### Suggested commands`, this subsection (the outer fence below is four backticks in the
   file, as in `wave-run/report.md`):

   ````
   ### Template

   ```
   ## <plan folder> · `<plan>` · <flow>

   - Tracking branch: `plan/<plan>` <present · absent>
   - Features: <count per status>

   | Feature | Status | Tasks | Waiting for | Branch | Merged |
   |---|---|---|---|---|---|
   | F1 <Title> | <README status> | <done>/<total> | <README Waiting for> | <feature branch> | <README Merged> |

   - Waves: <1 ✅ · 2 🔄 since <date time> · 3 ⬜ · or: none running>

   Merged, not in <main branch>:

   <merged block of every such feature, each followed by a blank line · or: none>

   Ready for review:

   <review block of every 👀 review feature, each followed by a blank line>

   - Integration: <as the bullet says>
   - Merged, not recorded: <F-IDs and branches>
   - Last stop: <the line>
   - Inconsistencies: <one item per line>
   - Leftovers: <one item and its suggested command per line>
   - Next: <one command, both forms>

   ## Index parts

   | Index | Part | Plan when | Met | Command |
   |---|---|---|---|---|
   | `<index path>` | <K> | <Plan when> | <yes · no: why> | `/wave-plan <index> part <K>`<br>`$wave-plan <index> part <K>` |

   Started: <YYYY-MM-DD HH:MM> · Finished: <YYYY-MM-DD HH:MM> (<duration>)
   ```

   - One `## ` block per plan: plan folders under `plans/` first, then plans found only on their tracking branch.
     `<flow>` is `manual`, or `autonomous · target: integration/<name>` followed by ` · manual review: <F-IDs>` when
     that list is not empty.
   - Always printed: the plan header, `Tracking branch`, `Features`, the table, `Waves`, `Next`, the times line.
     `Merged, not in <main branch>:` and `Integration:`: autonomous flow only, always there (`none`, `not created
     yet`). `Ready for review:`: when a feature is `👀 review`. `Merged, not recorded`, `Last stop`,
     `Inconsistencies`, `Leftovers`: only when they have content. `## Index parts`: when an index has a part
     without a plan folder.
   - Labels and column names are written exactly as the template writes them; when the user's language is not
     English, they are translated, and statuses, IDs, branch names, paths and commands stay as written.
   - A merged block and a review block are printed in full, never retold as one line.
   ````

4. Insert, right before `## Next-command rules`, this subsection:

   ```
   ### Before sending

   Compare the report with "Template": every plan has its header, `Tracking branch`, `Features`, the table, `Waves`
   and `Next` lines, in this order. In autonomous flow the `Merged, not in <main branch>:` label appears exactly once
   per plan, with the branch name alone (`Merged, not in main:`), followed by one full merged block per feature or
   `none`. If something is missing, merged into prose, or the label differs, rewrite the report before sending it.
   ```

No other line of the file changes.

### Reading rule 4 of `docs/claude-print-mode.md` (task W)

Replace rule 4 of "Reading the result" in "## Prompt form for the driver" with:

```
4. Before continuing, read the state from git, never from report headings: the labels of a report follow the
   user's language and can vary. For each plan of the run, read its README from the tracking branch
   (`git show plan/<plan>:<plan folder>/README.md`) and its `Flow:` line. A Features row `✅ merged` with hash `<h>`
   is merged but not yet in the main branch when `git merge-base --is-ancestor <h> <main branch>` exits non-zero;
   its text for a summary is `git show plan/<plan>:<plan folder>/reviews/<feature>.md`. A row `👀 review` waits for
   the user. Wave statuses are the README "Waves" table; a held integration branch is
   `git for-each-ref refs/wave-method/claims/`. Show the `wave-status` report to the user as it is; do not extract
   data from it.
```

## Algorithm

### Scratch, toy project and call form (task V)

As `solutions/P13-print-mode-runs.md`, "Scratch and toy project (both tasks)" and "Call form (N, and O where it says
so)": the same `todo.py` and `test_todo.py`, the install from the task's worktree with
`sh install.sh <scratch>/repo --no-codex`, the same Git Bash call with `--output-format stream-json --verbose
--permission-mode bypassPermissions --setting-sources project,local`, `timeout 3600`, stdin from `/dev/null`, the
`system/init` check (four project `wave-*` skills, no `wave-method:` skill), and `claude`, `<scratch>`, `~` in every
written path.

Around every call, in Git Bash, from `<scratch>/repo`:

1. `MSYS_NO_PATHCONV=1 tasklist /FI "IMAGENAME eq claude.exe" /NH | grep -c claude.exe` → `procs_before`.
2. `start=$(date +%s)`; start the call in the background (`… &`), `wait $!`; `end=$(date +%s)`; wall minutes =
   `(end - start) / 60`.
3. At once: `git for-each-ref --format='%(refname) %(objectname)'` and `git worktree list --porcelain` into
   `<scratch>/logs/<run>.refs-exit` and `<run>.wt-exit`.
4. Wait 120 seconds (any means the environment allows), then the same two commands into `<run>.refs-120` and
   `<run>.wt-120`, and the process count again → `procs_after`.
5. Post-exit check passes when both pairs of files are identical and `procs_after` ≤ `procs_before`.
6. From the stream: the number of lines after the line whose `type` is `result` (expected 0), and the `result`
   event's `duration_ms` against the wall minutes.

### Runs of task V

| Run | Prompt | `--model` | `--max-turns` | `--max-budget-usd` |
|---|---|---|---|---|
| M1 | `/wave-triage flow autonomous 1. add a storage module store.py with load(path) and save(path, items) that keep the items as JSON 2. add a command line to todo.py (python todo.py add TEXT, rm N, list) that loads and saves todo.json through store.py 3. add a --version option that prints VERSION 4. add a done N command that marks item N done 5. show done items in list with an [x] marker instead of hiding them 6. rename rm to delete and keep rm as an alias` | `opus` | 150 | 6 |
| M2 | `/wave-plan flow autonomous <index path from M1> part 1` | `opus` | 200 | 10 |
| M3 … M8 | `/wave-run <plan folder from M2>` | `sonnet` | 400 | 8 |
| M9 | `/wave-status` | `haiku` | 60 | 0.5 |
| M10 | `/wave-status <plan folder from M2>` | `haiku` | 60 | 0.5 |

- Items 2, 4, 5 and 6 change `todo.py` and item 2 needs item 1: a plan cannot put them in one wave, so it needs
  several. If M1's index has more than one part, plan part 1 only and record the others.
- M3 to M8: one call per wave, the next only when the README on the tracking branch shows a wave still ⬜ or ❌ and
  the call ended without a stop line. A stop line ends the chain: record it (code and `next:`), then run M9 and M10.
  At most six `wave-run` calls.
- Spend cap of the whole task: 30 USD by the sum of `total_cost_usd`; when passed, run M9 and M10 and stop.
- No flow form: the plan from M2 is in autonomous flow already.

Record after every run what `docs/rehearsals/print-mode-chain.md` records (command; exit code; `subtype`,
`is_error`, `num_turns`, `total_cost_usd`, minutes from `duration_ms`; `permission_denials`; first `result` line;
stop line or none; the checks of `solutions/P13-print-mode-runs.md`, "Runs of task N", for the matching skill), plus
the wall minutes and the post-exit check. For M2 also: the number of waves, features and tasks of the plan, and the
largest number of tasks in one wave with `After` `—`.

For every `wave-run` call, one row per `Agent` (subagent) tool call in the stream, in the section "## Subagents":
run; wave; task ID (from its prompt); `model` requested (or `—`); `run_in_background` (true, false or absent);
launched in the same assistant message as another `Agent` call (yes/no); its result arrived before the `result`
event (yes/no; for a background call, the event that carries its final output, not the launch acknowledgement);
the task's commit is in the feature branch at process exit (yes/no).

Checks of M9 and M10 (each pass or a finding): the label `Merged, not in main:` appears exactly once per plan in
autonomous flow, exactly in this form; each feature merged into `integration/<topic>` and not in `main` follows it
with a full merged block (header with `merged into`, essence, how to test, `Approved:`); every plan has the header,
`Tracking branch`, `Features`, table, `Waves` and `Next` lines.

### Record `docs/rehearsals/print-mode-multiwave.md` (task V)

- Title `# Rehearsal: multi-wave print-mode chain`; one line with the date, `claude --version` and the commit of the
  source branch.
- `## Setup` (scratch, toy project, install, call form, the post-exit procedure); `## Runs` with one
  `### M<n> · <skill>` per run; `## Subagents` (the table above); `## Findings` (each: run, expected / got, CLI effect
  or skill defect); `## Caps` (per skill: the largest turns and cost over R1–R6 of `print-mode-chain.md` and M1–M10,
  and three times each, turns rounded up to a multiple of 10 and dollars up to a whole number; `wave-run` per call).

### Edits of `docs/claude-print-mode.md` (task W)

The six `## ` sections keep their names and order.

- "## Environment": one bullet for this re-run: date, `claude --version`, skills installed from F4's branch, link to
  `rehearsals/print-mode-multiwave.md`.
- "## Probes": after "### Chain runs (R1–R3 and R6)", a subsection "### Multi-wave chain runs (M1–M<n>)" with the same
  table columns, plus one sentence each on the subagents (how many, background or not, all done before `result` or
  not) and the post-exit checks.
- "## Result": one paragraph on the multi-wave chain: the number of waves run, whether `wave-run` ends only after its
  subagents end, and whether the repository changed after exit.
- "## Prompt form for the driver": the caps of the prompt table from V's "## Caps" (`wave-status` keeps 60 and 0.5
  unless V measured more than a third of them); the sentence about how the caps were derived names both chains;
  reading rule 4 replaced by the text in "Model/API changes"; if V found that a call can end while a background
  subagent still runs, a rule 5 that says what the driver checks before the next call (the task branches and README
  statuses of that wave), from V's record.
- "## Open points": remove the point on the multi-wave plan and background subagents when V measured them, and the
  point on the R6 heading when M9 and M10 passed their checks; keep the turn-cap enforcement point; add only what V
  left unsettled, each with what would settle it.

## Limits

- Only `skills/wave-status/SKILL.md` changes under `skills/` (task U).
- The chain runs only in `<scratch>`; nothing is pushed; `<scratch>` is deleted at the end; nothing else is deleted.
- No user path or user name in the docs:
  `git grep -n -e "C:/Users" -e "C:\\\\Users" -e "/home/" -e "/Users/" -- docs` prints nothing.
- Quote at most one sentence (under 15 words) per docs page.
- If M2's plan has a single wave, or no `wave-run` call launches two `Agent` calls in one launch group, the chain
  still runs to the end; record a finding `multi-wave not reached` (or `no parallel launch`) and say in the report
  that I10 stays open. Do not change the list and run again.
- If the chain cannot start (`claude` missing or not signed in, M1 fails before triage starts), stop and report; do
  not write a record of runs that did not happen.

## Acceptance tests

- U: `git grep -n -e "^### Template" -e "^### Before sending" -e "Merged, not in" -- skills/wave-status/SKILL.md` →
  both headings, the template's label line, the bullet and the "Before sending" sentence; `git diff --stat
  main...HEAD` lists only `skills/wave-status/SKILL.md`. Three walkthroughs in the report, following the new text by
  hand: (a) a plan in manual flow with one `👀 review` feature → no `Merged, not in` label, no `Integration:` line,
  one review block; (b) a plan in autonomous flow with F1 and F2 `✅ merged` into `integration/demo`, hashes not in
  `main`, and F3 `👀 review` → `Merged, not in main:` once, then two merged blocks, then `Ready for review:` with F3's
  block; (c) the same plan after the user merged `integration/demo` into `main` → `Merged, not in main:` followed by
  `none`.
- V: `docs/rehearsals/print-mode-multiwave.md` has `## Setup`, `## Runs` (M1, M2, at least two `wave-run` runs, M9,
  M10), `## Subagents`, `## Findings`, `## Caps`; every run has its command, exit code, result fields, wall minutes,
  post-exit check and checks; every failed check is a finding.
- W: `git grep -n "^## " -- docs/claude-print-mode.md` → the six sections in order;
  `git grep -n "^### Multi-wave chain runs" -- docs/claude-print-mode.md` → one line;
  `git grep -n "heading varies" -- docs/claude-print-mode.md` → nothing; `git grep -n "merge-base --is-ancestor" --
  docs/claude-print-mode.md` → rule 4; the caps in the prompt table equal V's "## Caps".
- All: `git diff --stat main...HEAD` lists only `skills/wave-status/SKILL.md`,
  `docs/rehearsals/print-mode-multiwave.md` and `docs/claude-print-mode.md`; the check command is green.
