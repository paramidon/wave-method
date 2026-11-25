# Rehearsal: wave-auto triage in clusters, and the installers' Codex links

2026-11-25 · Claude Code 2.1.326 · source checkout `ca9de6a` (the working folder before this record).

Rehearsal Q of feature F1 (in-session coordinator `wave-auto`): a list of ten problems, so that triage works in
clusters; a `steps` rail in the middle of triage and the resume in a new session; and the Codex links that
`install.sh` and `install.ps1` make with the fifth skill.

## Setup

- Made `<scratch>` with `mktemp -d`, outside every repository. Calls are saved as `<scratch>/calls/<run>.jsonl`
  (stream), `.err`, `.exit` and `<run>.evidence.txt` (branches, `refs/wave-method/`, `git log --oneline -3 main`,
  worktrees).
- Fixture repository `<scratch>/textkit` on `main`, local user `rehearsal` / `rehearsal@example.invalid`:
  `textkit/__init__.py` (empty), `tests/test_smoke.py` (`def test_import(): import textkit`), `README.md` (one line,
  "textkit — small text helpers. Check: python -m pytest -q"), `.gitignore` (`__pycache__/`, `.pytest_cache/`). Commit
  `Seed textkit`.
- Virtual environment `<scratch>/venv` (Python 3.14.6, `pip install pytest` gave pytest 9.2.0).
- `sh <working folder>/install.sh <scratch>/textkit --no-codex` installed the five skills, then commit
  `Seed textkit with wave skills` (`259fe7a`).
- Every call: `claude -p "<prompt>" --output-format stream-json --verbose --permission-mode auto
  --max-budget-usd <rest>`, run in `<scratch>/textkit` with `<scratch>/venv/Scripts` first on `PATH`,
  `MSYS_NO_PATHCONV=1` (Git Bash on Windows), stdin from `/dev/null`, no `--model`. The shell that started the calls
  belonged to a Claude Code desktop app session, so the calls inherited its environment variables.
- The coordinator ran on the CLI default, `claude-sonnet-5-5` in every `system/init` (the description of
  `wave-auto/SKILL.md` recommends a high-complexity model).
- Every `system/init` listed the project skills `wave-auto`, `wave-plan`, `wave-run`, `wave-status`, `wave-triage`
  and also the user-level plugin skills `wave-method:wave-plan` … `wave-method:wave-triage`; every step prompt carried
  `Skills folder: <scratch>\textkit\.claude\skills`.
- The list (one argument, verbatim):

  ```
  In every item a word is a run of ASCII letters and digits. 1. Add textkit/slug.py with slugify(text): the words in lower case joined by "-". 2. Add slug_parts(text) to textkit/slug.py returning the list of words slugify joins. 3. Add textkit/count.py with count_words(text) returning a dict word -> count, words in lower case. 4. Add count_chars(text) to textkit/count.py returning a dict character -> count, whitespace left out. 5. Add count_lines(text) to textkit/count.py returning the number of lines that are not blank. 6. Add textkit/case.py with snake_case(text): the words in lower case joined by "_". 7. Add camel_case(text) to textkit/case.py: the first word in lower case, the others capitalised, joined with nothing. 8. Add kebab_case(text) to textkit/case.py: the words in lower case joined by "-". 9. Add textkit/trim.py with squeeze(text) turning every run of whitespace into one space and stripping both ends. 10. Add truncate(text, n) to textkit/trim.py returning at most n characters, the last one "…" when it cuts.
  ```

- Clusters chosen by the triage (index `plans/2026-11-25-text-helpers/index.md`): `slug-case` (P1, P2, P6, P7, P8)
  and `count-trim` (P3, P4, P5, P9, P10).
- Cost: **2.52 USD** in total (cap 6 USD): the Q1 session 1.39 USD, the Q2 session 1.13 USD. The `total_cost_usd` of a
  `--continue` call includes the earlier call of its session (its `modelUsage` still holds that call's tokens), so the
  first Q1 call (0.84 USD) is not added again; adding the three printed figures would give 3.36 USD.
- Permission denials: none in any call (`permission_denials` empty).

### Models per step

| Run | Step | `model` of the agent call | Model in the subagent's messages |
|---|---|---|---|
| Q1 | `triage-ask` | opus | `claude-opus-5-5` |
| Q1 | `triage-answers` | opus | `claude-opus-5-5` |
| Q1 | `triage-cluster` (`slug-case`) | sonnet | `claude-sonnet-5-5` |
| Q1 | `status` | haiku | `claude-haiku-5-5` |
| Q2 | `navigate` | haiku | `claude-haiku-5-5` |
| Q2 | `triage-cluster` (`count-trim`) | sonnet | `claude-sonnet-5-5` |
| Q2 | `triage-finish` | opus | `claude-opus-5-5` |
| Q2 | `status` | haiku | `claude-haiku-5-5` |

## Runs

### Q1 · from the list, rail after the first cluster

Two calls, because `triage-ask` asked questions.

```bash
claude -p "/wave-auto steps 3 <list>" ...                          # call Q1
claude -p "Take reading (a) for every question." --continue ...    # call Q1b
```

- Call Q1: exit 0, 84 s, 0.8383 USD. The coordinator printed `Started: 2026-11-25 18:52` and `Capabilities: subagents ·
  parallel · model choice (low haiku, medium sonnet, high opus) · session start no`, ran `triage-ask`, then printed
  `18:53 · triage-ask · list → questions 6 · index plans/2026-11-25-text-helpers/index.md`, took the claim, printed the
  resume command and asked six questions (P4 twice, P5, P7, P9, P10).
- After call Q1 (`Q1.evidence.txt`): branches `main`, `triage/text-helpers`; ref
  `6fdb661… refs/wave-method/claims/auto/text-helpers`; `main` still `259fe7a`. The index on the triage branch had
  `- Triage: waiting for answers`, ten problems, two clusters and `- Q1` … `- Q6`; the list's `…` arrived intact.
- Call Q1b: exit 0, 93 s, 1.3913 USD (cumulative). Agent calls: `triage-answers` (prompt ends with `Answers:` and the
  answer verbatim), `triage-cluster` (`Run the skill wave-triage with the arguments: cluster slug-case
  plans/2026-11-25-text-helpers/index.md`), `status`. Returns: `answers recorded · clusters slug-case, count-trim`,
  `cluster slug-case: 5 records · high 0 · unsure 0`.
- **No progress line in call Q1b.** Between its agent calls the coordinator ran `date +%H:%M` (the second time in one
  command with `git update-ref -d` of its claim) and wrote no text; the only text of the call is the final report.
  Finding F-1.
- Final report: `Run: 3 steps · ended by rail: steps 3 · Capabilities: …`; Steps rows `18:53 triage-ask`,
  `18:54 triage-answers`, `18:55 triage-cluster`; `### Halts` `- none`; the `status` report copied verbatim;
  `### Next` with ``Continue: `/wave-auto plans/2026-11-25-text-helpers/index.md` · `$wave-auto …` ``;
  `Started: 2026-11-25 18:52 · Finished: 2026-11-25 18:55 (3 min)`.
- State after (`Q1b.evidence.txt`): no ref under `refs/wave-method/`; `main` `259fe7a`; the triage worktree at
  `78c3bea Index text-helpers: answers` with untracked `triage/P1.md`, `P2.md`, `P6.md`, `P7.md`, `P8.md` (the five
  problems of `slug-case`; the `cluster` form makes no commit).
- The `status` report of this run, made while the triage was half done, says `## No plans found`, `Index parts: none
  (no index under plans/)` and `Next: no plan exists yet. Start with a list of problems through /wave-triage …`, and
  suggests `git worktree remove` for the triage worktree that holds the uncommitted records (not run). Observation O-1.

### Q2 · resume in the middle of triage, new session

```bash
claude -p "/wave-auto steps 2 plans/2026-11-25-text-helpers/index.md" ...   # no --continue
```

`<m>` = 1 cluster without records + 1 = 2.

- Exit 0, 159 s, 1.1336 USD. The agent calls ran in the background this time; the coordinator ended its turn while each
  ran and the CLI re-invoked it (five `result` events, the last one with the final report).
- Steps and returns:
  - `navigate` → `next: triage-cluster plans/2026-11-25-text-helpers/index.md count-trim`;
  - `triage-cluster` → `cluster count-trim: 5 records · high 0 · unsure 0`;
  - `triage-finish` → `parts 1 · index plans/2026-11-25-text-helpers/index.md · merged 24d60f0`;
  - `status`.
- Progress lines: `18:56 · navigate · … → next: triage-cluster … count-trim` and `18:57 · triage-cluster · … → cluster
  count-trim: …`, each before the next agent call. **`triage-finish` got none**: after its return the coordinator ran
  `date +%H:%M; git update-ref -d <its claim>` and launched `status`. Finding F-1.
- Besides the lines the skill names, the coordinator wrote `Now the navigate step.`, `Rail check: steps 0 of 2 used.
  Dispatching the cluster step.` and ``Steps used: 1 of 2. Dispatching `triage-finish`.``, and ran the Bash command
  `sleep 1; echo waiting` while the navigator worked. Finding F-2.
- Final report: `Run: 2 steps · ended by rail: steps 2 · Capabilities: …`; Steps rows `18:57 triage-cluster`,
  `18:58 triage-finish`; `### Halts` `- none`; the `status` report copied verbatim (it shows part 1 unplanned,
  `Coordinator claims: none`); `### Next` with the `Continue:` line; `Started: 2026-11-25 18:56 · Finished:
  2026-11-25 18:58 (2 min)`.
- State after (`Q2.evidence.txt`): `git log --oneline -3 main`: `24d60f0 Index text-helpers`,
  `88d957e Index text-helpers: 10 problems in 1 parts`, `78c3bea Index text-helpers: answers`; only branch `main`; only
  the main worktree; no ref under `refs/wave-method/`. `git ls-tree -r --name-only main -- plans` lists `index.md` and
  `triage/P1.md` … `triage/P10.md`. The index has the overview filled (all `low`), one part (slug `text-helpers-p1`)
  and no `Triage: waiting for answers` line; the records of P4, P5, P7, P9 and P10 hold the answers.

### Q3 · installers with Codex links

Each target is a new folder on which `git init` ran; the script checked that the path was non-empty and new, and under
`<scratch>` for Q3.1 and Q3.2.

**Q3.1 · `install.sh` in Git Bash** — `sh <working folder>/install.sh <scratch>/q3-sh`

- Exit 0; five `installed …/.claude/skills/<name>` and five `linked …/.agents/skills/<name>` lines.
- `.agents/skills` holds `wave-auto`, `wave-plan`, `wave-run`, `wave-status`, `wave-triage`, each with a `SKILL.md`.
  They are **copies**, not links (`[ -L ]` false, PowerShell `LinkType` empty; `MSYS` unset); `diff -r` against
  `.claude/skills` shows no difference.

**Q3.2 · `install.ps1` in Windows PowerShell 5.1**
`powershell -NoProfile -ExecutionPolicy Bypass -File <working folder>\install.ps1 -Target <scratch>\q3-ps`

- Exit 0; five `installed` and five `linked` lines.
- Each of the five entries of `.agents\skills` has `LinkType` `Junction`, a `SKILL.md`, and the target
  `<scratch>\q3-ps\.claude\skills\<name>`.

**Q3.3 · Linux symlinks in WSL** (`wsl.exe -l -q` names `Ubuntu`) — `MSYS_NO_PATHCONV=1 wsl.exe sh <scratch>/q3.sh`

- The script makes `d=$(mktemp -d)` inside WSL, stops unless it is a non-empty folder, runs `git init` and
  `sh <working folder>/install.sh "$d"`.
- `install.sh exit 0`; five entries, each `symlink -> ../../.claude/skills/<name>; SKILL.md yes`.

## Results

| Expectation | Result | Evidence |
|---|---|---|
| Q1: steps `triage-ask`, `triage-answers`, one `triage-cluster` | Pass | three agent calls with those step lines in `Q1.jsonl` and `Q1b.jsonl` (plus `status`); the questions after `triage-ask` were answered as "Shared setup" says |
| Q1: `triage-answers` returns `clusters <names>` | Pass | `answers recorded · clusters slug-case, count-trim` |
| Q1: the `triage-cluster` call is on `sonnet` | Pass | agent call `model: sonnet`; subagent messages `claude-sonnet-5-5` |
| Q1: `ended by rail: steps 3` | Pass | `Run: 3 steps · ended by rail: steps 3` |
| Q1: the records of that cluster exist in the triage worktree | Pass | `triage/P1`, `P2`, `P6`, `P7`, `P8` in `Q1b.evidence.txt` |
| Q2: `navigate` returns `next: triage-cluster …` naming only the missing clusters | Pass | `next: triage-cluster plans/2026-11-25-text-helpers/index.md count-trim` |
| Q2: one `triage-cluster` step each | Pass | one agent call, `cluster count-trim …`, model `sonnet` |
| Q2: `triage-finish` returns `parts <k> …` | Pass | `parts 1 · index plans/2026-11-25-text-helpers/index.md · merged 24d60f0` |
| Q2: `ended by rail: steps <m>` (m = 2) | Pass | `Run: 2 steps · ended by rail: steps 2` |
| Q2: the index and the ten `triage/P<n>.md` records are on `main` | Pass | `git ls-tree -r --name-only main -- plans`: eleven files |
| Q3.1: exit 0, five entries in `.agents/skills`, each with a `SKILL.md` | Pass | `wave-auto` included; recorded: copies, not links |
| Q3.2: exit 0, five junctions, each with a `SKILL.md` | Pass | `LinkType` `Junction` for all five, `wave-auto` included |
| Q3.3: five symlinks | Pass | five `symlink -> ../../.claude/skills/<name>`, each with a `SKILL.md` |
| Report check 1 (progress lines), Q1 | Finding | line for `triage-ask` only; none for `triage-answers` and `triage-cluster` (F-1) |
| Report check 1 (progress lines), Q2 | Finding | lines for `navigate` and `triage-cluster`; none for `triage-finish` (F-1) |
| Report check 2 (claim), Q1 and Q2 | Pass | no `refs/wave-method/claims/auto/` ref and nothing about the run's claim in either Status part (they say only that there are none); the claim was released before `status` |
| Report check 3 (template), Q1 and Q2 | Pass | `Run:`, `### Steps`, `### Halts`, `### Status`, `### Next` with only their content; `### Next` holds the `Continue:` line; nothing after the last `Started: … · Finished: …`; the `status` text equals the subagent's return; no coordinator Bash call runs the project, its tests or `python` |
| Hard rules (not a report check): only the lines the skill names, only the commands it names | Finding | Q2: three extra remarks and `sleep 1; echo waiting` (F-2) |

### Findings

- **F-1 · progress lines missing.** Expected a line `HH:MM · <step> · <unit> → <return line>` for every counted step and
  every `navigate`, before the next step's agent call. Observed: none for `triage-answers` and `triage-cluster` in Q1
  and none for `triage-finish` in Q2. The coordinator read the clock each time but wrote no text; the times appear only
  in the Steps table. Decided by `skills/wave-auto/SKILL.md`, "Loop" and "Progress lines" (also "Hard rules"). The
  coordinator was `claude-sonnet-5-5`.
- **F-2 · output and commands beyond the skill.** Expected nothing but the named lines, and only commands that read git
  and skill files, take or release the claim, or read the clock. Observed in Q2: `Now the navigate step.`, two remarks
  about the rail count, and `sleep 1; echo waiting`. Decided by `skills/wave-auto/SKILL.md`, "Hard rules", last two
  bullets.

### Observation

- **O-1 · `wave-status` does not see a triage in progress** (not an expectation of the plan). With the index only on
  `triage/text-helpers`, the Status part of Q1 reports no plans and no index, advises starting from a list, and offers
  to remove the triage worktree with its uncommitted records, while the same report's `### Next` says to continue with
  the index. `skills/wave-status/SKILL.md`, "Input" and "What to read", look at `plans/` and `plan/*` branches only.
  The Status part of Q2 (an index, no plan yet) is also free text rather than the skill's "Template".

## Not verified

- Several `triage-cluster` steps launched together: the rail of Q1 stopped after the first cluster and Q2 had one left.
- The re-judging of `triage-finish`: no record was `high` or `(unsure)`.
- That Codex loads the skills from `.agents/skills`: Q3 checks the entries on disk only.

## Repeat

```bash
S=$(mktemp -d); [ -n "$S" ] || exit 1; mkdir -p "$S/calls" "$S/textkit/textkit" "$S/textkit/tests"
python -m venv "$S/venv" && "$S/venv/Scripts/python" -m pip install pytest      # venv/bin on Linux and macOS
cd "$S/textkit" && git init -q -b main
git config user.name rehearsal && git config user.email rehearsal@example.invalid
: > textkit/__init__.py
printf 'def test_import(): import textkit\n' > tests/test_smoke.py
printf 'textkit — small text helpers. Check: python -m pytest -q\n' > README.md
printf '__pycache__/\n.pytest_cache/\n' > .gitignore
git add -A && git commit -q -m "Seed textkit"
sh <working folder>/install.sh "$S/textkit" --no-codex
git add -A && git commit -q -m "Seed textkit with wave skills"

export PATH="$S/venv/Scripts:$PATH" MSYS_NO_PATHCONV=1
run() { n=$1; b=$2; p=$3; shift 3; claude -p "$p" "$@" --output-format stream-json --verbose \
  --permission-mode auto --max-budget-usd "$b" < /dev/null > "$S/calls/$n.jsonl"; }
run Q1 6 "/wave-auto steps 3 <the list above>"
run Q1b <rest> "Take reading (a) for every question." --continue     # only if Q1 asked
run Q2 <rest> "/wave-auto steps <clusters without records + 1> plans/<date>-<topic>/index.md"

# Q3: a new folder for each form
mkdir "$S/q3-sh" "$S/q3-ps" && git -C "$S/q3-sh" init -q && git -C "$S/q3-ps" init -q
sh <working folder>/install.sh "$S/q3-sh"
powershell -NoProfile -ExecutionPolicy Bypass -File "<working folder>\install.ps1" -Target "$(cygpath -w "$S/q3-ps")"
cat > "$S/q3.sh" <<'EOF'
d=$(mktemp -d)
[ -n "$d" ] && [ -d "$d" ] || exit 1
git init -q "$d" && sh <working folder as /mnt/...>/install.sh "$d" || exit 1
for e in "$d"/.agents/skills/*; do
  l=no; [ -L "$e" ] && l=yes; s=no; [ -f "$e/SKILL.md" ] && s=yes
  echo "$(basename "$e"): symlink $l, SKILL.md $s"
done
EOF
MSYS_NO_PATHCONV=1 wsl.exe sh "<scratch as /mnt/...>/q3.sh"
```

After each call: `git branch --list`, `git for-each-ref refs/wave-method/`, `git log --oneline -3 main` and
`git worktree list`; from the stream, the events without `parent_tool_use_id` (the coordinator's text and Bash calls),
every agent call's `model` and the `Coordinated run · step …` line of its prompt, the last `result` event's `result`
and `total_cost_usd`. The topic and the cluster names are chosen by the triage and can differ between repetitions.
Stop starting calls when the cost reaches 6 USD.
