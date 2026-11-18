# Rehearsal: manual flow end to end

2026-11-18 · `claude --version` → `2.1.326 (Claude Code)` · source commit `6a8bc07`.

## Setup

```bash
scratch=$(mktemp -d)
working="<working folder>"
mkdir -p "$scratch/logs" "$scratch/v2120"
git -C "$working" archive v2.12.0 skills install.sh | tar -x -C "$scratch/v2120"

seed() {
    local repo="$1" source="$2"
    git init -b main "$scratch/$repo"
    git -C "$scratch/$repo" config user.name "wave e2e"
    git -C "$scratch/$repo" config user.email "e2e@example.invalid"
    printf 'MIT\n' > "$scratch/$repo/LICENSE"
    git -C "$scratch/$repo" add LICENSE
    git -C "$scratch/$repo" commit -qm init
    sh "$source/install.sh" "$scratch/$repo" --no-codex
    git -C "$scratch/$repo" add .claude
    git -C "$scratch/$repo" commit -qm "install wave skills"
    mkdir -p "$scratch/$repo/plans"
    cp -r "$working/examples/01-greenfield-todo-cli" "$scratch/$repo/plans/2026-11-02-todo-cli"
    git -C "$scratch/$repo" add plans
    git -C "$scratch/$repo" commit -qm "add plan"
    git -C "$scratch/$repo" branch plan/todo-cli
}

seed cur "$working"
seed base "$scratch/v2120"
python -m venv "$scratch/venv"
"$scratch/venv/Scripts/python" -m pip install pytest pyyaml
export PATH="$scratch/venv/Scripts:$PATH"
```

Both repositories were seeded from the unchanged fixture. Each commit uses the scratch identity `wave e2e`. The virtual environment installed pytest 9.2.0 and PyYAML 6.0.3.

Git Bash ran each step in its scratch repository’s main checkout with the virtual environment first on the launcher’s `PATH`. M3 and M5 were the user’s merge approvals. The cumulative cost of the last result events was USD 1.71601615500000026, below the USD 20 stop threshold. These `total_cost_usd` fields count toward subscription usage limits.

All evidence files named below are under `<scratch>/logs`. For each Claude call, the launcher captured `git for-each-ref --format='%(refname) %(objectname)'` and `git worktree list --porcelain` before and after. The M5 after-snapshot was captured separately after the launcher stopped. The real-project snapshots `working.before.refs` and `working.after.refs` are byte-for-byte identical before the report commit. Both have SHA-256 `b59f9984fc5af0fc6cece031ea21879fa85f0fbfe2e0a65f07947586e8b79141`.

## Runs

### cur M0

```bash
python "<working folder>/skills/wave-plan/scripts/status_check.py" plans/2026-11-02-todo-cli
```

- Pass. Exit `0` with empty stdout and stderr. Evidence: `cur-M0.exit`, `cur-M0.out`, `cur-M0.err`.

### cur M1

```bash
python "<working folder>/scripts/wave_driver.py" plans/2026-11-02-todo-cli --repo . --dry-run
```

- Pass. Exit `0` with one line, `next: nothing — plans/2026-11-02-todo-cli: manual flow: the driver runs autonomous plans only`. `<scratch>/cur.wave-driver` was absent. Evidence: `cur-M1.exit`, `cur-M1.out`, `cur-M1.driver-dir`.

### cur M2

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 1" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null \
  > "<scratch>/logs/cur-M2.jsonl" 2> "<scratch>/logs/cur-M2.err"
```

- Exit `0`. Model `claude-sonnet-5-5`. Wall time 2.03 min.
- Last result `cur-M2.jsonl:162`. `num_turns: 12` and `total_cost_usd: 0.58079327`.
- First line `Started: 2026-11-18 17:26`. Last line `Started: 2026-11-18 17:26 · Finished: 2026-11-18 17:29 (3 min)`.
- Stop line none.
- Refs and worktrees before and after: `cur-M2.before.refs`, `cur-M2.after.refs`, `cur-M2.before.worktrees`, `cur-M2.after.worktrees`.
- `main` `ad408c0696786a5c69943512ea4b26b7fb267417` → `ad408c0696786a5c69943512ea4b26b7fb267417`. First-parent merges: none. First-parent non-merges: none.
- Pass. The final result opens with `Started:` and shows `Flow: manual`. A is ✅ and F1 is 🔄, waiting for wave 2. `main` stayed at `ad408c0`. The after-snapshot has no integration branch or claim ref, and no `Flow:` line in the tracking README. Evidence: `cur-M2.jsonl:162` and the before/after snapshots.
- Finding. Expected wave 1 and C ✅, F2 👀 review with its review block and a merge question. The coordinator marked wave 1, C and F2 ⚠️ I1. Its final result says the README example outputs `added 2: call Bob`, which follows the described format but has no exact row in the P2 table. The result has no F2 review block or merge question. Evidence: `cur-M2.jsonl:162`, tracking commit `7b8cf02` and `plans/2026-11-02-todo-cli/problems.md` on that commit.
- Finding. Expected the nested checks to use the scratch Python environment. The coordinator ran `pip install -q pytest`. The install output reports success and a pytest directory appeared under `<home>/AppData/Roaming/Python/Python314/site-packages` during the call. Evidence: `cur-M2.jsonl:117,120` and the read-only host path check.

### cur M3

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null \
  > "<scratch>/logs/cur-M3.jsonl" 2> "<scratch>/logs/cur-M3.err"
```

- Exit `0`. Model `claude-sonnet-5-5`. Wall time 0.42 min.
- Last result `cur-M3.jsonl:27`. `num_turns: 8` and `total_cost_usd: 0.23244720000000002`.
- First line `Started: 2026-11-18 17:28`. Last line `Started: 2026-11-18 17:28 · Finished: 2026-11-18 17:28 (under 1 min)`.
- Stop line `` Stop not-ready: F2 is ⚠️ blocked, not `👀 review` — next: `/wave-plan plans/2026-11-02-todo-cli` · `$wave-plan plans/2026-11-02-todo-cli`, or accept I1 as is (see below) ``.
- Refs and worktrees before and after: `cur-M3.before.refs`, `cur-M3.after.refs`, `cur-M3.before.worktrees`, `cur-M3.after.worktrees`.
- `main` `ad408c0696786a5c69943512ea4b26b7fb267417` → `ad408c0696786a5c69943512ea4b26b7fb267417`. First-parent merges: none. First-parent non-merges: none.
- Pass. The first-parent range has no non-merge commits. Evidence: empty `cur-M3.nonmerges`.
- Finding. Expected the F2 branch to merge and its README row to record the merge hash. The command stopped at `not-ready` because F2 was still ⚠️ I1. `main` stayed at `ad408c0` and the row had no merge hash. Evidence: `cur-M3.jsonl:27`, empty `cur-M3.merges` and tracking commit `7b8cf02`.

### cur M4

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null \
  > "<scratch>/logs/cur-M4.jsonl" 2> "<scratch>/logs/cur-M4.err"
```

- Exit `0`. Model `claude-sonnet-5-5`. Wall time 2.10 min.
- Last result `cur-M4.jsonl:172`. `num_turns: 8` and `total_cost_usd: 0.5110468850000002`.
- First line `Wave 2 is finished. Both tasks are done, and I'm printing the report now.`. Last line `Started: 2026-11-18 17:29 · Finished: 2026-11-18 17:30 (1 min)`.
- Stop line none.
- Refs and worktrees before and after: `cur-M4.before.refs`, `cur-M4.after.refs`, `cur-M4.before.worktrees`, `cur-M4.after.worktrees`.
- `main` `ad408c0696786a5c69943512ea4b26b7fb267417` → `ad408c0696786a5c69943512ea4b26b7fb267417`. First-parent merges: none. First-parent non-merges: none.
- Pass. Wave 2, B and D are ✅. F1 and F3 are 👀 review with merge questions for both. `main` stayed at `ad408c0`. Evidence: `cur-M4.jsonl:172` and tracking commit `2724bb8`.
- Finding. Expected nested tools to use the prepared virtual environment and keep temporary setup under `<scratch>`. A nested Bash session resolved Python to `C:/Program Files/Python314/python.exe`. The calls attempted extra virtual environments and a PyYAML target install. A read-only path check found `C:/tmp/yamlchk`, `C:/tmp/yamlchk-f3`, `C:/tmp/yamldeps-f3` and two other `yamlchk-f3` directories outside `<scratch>` with creation times matching this step. Evidence: `cur-M4.jsonl:77,84,89,98,99,114,118,120`. The launcher was stopped when the out-of-scratch writes were confirmed.

### cur M5

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null \
  > "<scratch>/logs/cur-M5.jsonl" 2> "<scratch>/logs/cur-M5.err"
```

- Exit unavailable because the launcher stopped before writing the exit status. Model `claude-sonnet-5-5`. Wall time 1.15 min from the result duration (`duration_ms: 68787`).
- Last result `cur-M5.jsonl:77`. `num_turns: 18` and `total_cost_usd: 0.39172880000000004`.
- First line `Started: 2026-11-18 17:31`. Last line `Started: 2026-11-18 17:31 · Finished: 2026-11-18 17:32 (1 min)`.
- Stop line none.
- Refs and worktrees before and after: `cur-M5.before.refs`, `cur-M5.after.refs`, `cur-M5.before.worktrees`, `cur-M5.after.worktrees`.
- `main` `ad408c0696786a5c69943512ea4b26b7fb267417` → `fce160a85176e6c88a5ee87ccf0226054e363641`. First-parent merges: `fce160a`, `fad03b1`, `3ad0e1a`. First-parent non-merges: none.
- Pass. F1 and F3 reached `main` as `3ad0e1a` and `fad03b1`. The plan status merge is `fce160a`. The first-parent range has zero non-merge commits. The tracking README records both feature merge hashes. Evidence: `cur-M5.jsonl:77`, `cur-M5.merges`, empty `cur-M5.nonmerges` and tracking commit `bba5700`.
- Finding. Expected every feature ✅ merged and the plan in `plans/archive/2026-11-02-todo-cli/` on the tracking branch. F2 stayed ⚠️ I1, so the plan stayed in `plans/2026-11-02-todo-cli/`. Evidence: `cur-M5.after.tracking-tree` and tracking commit `bba5700`.

### cur M6

```bash
python -m pytest -q
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null \
  > "<scratch>/logs/cur-M6.jsonl" 2> "<scratch>/logs/cur-M6.err"
```

- Not run. The launcher was stopped before the main-checkout tests and status call because nested tools wrote outside `<scratch>`.

### base M0

```bash
python "<working folder>/skills/wave-plan/scripts/status_check.py" plans/2026-11-02-todo-cli
```

- Not run. Stopped the rehearsal on the current run’s confirmed scratch isolation failure.

### base M2

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 1" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null \
  > "<scratch>/logs/base-M2.jsonl" 2> "<scratch>/logs/base-M2.err"
```

- Not run. Stopped the rehearsal on the current run’s confirmed scratch isolation failure.

### base M3

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null \
  > "<scratch>/logs/base-M3.jsonl" 2> "<scratch>/logs/base-M3.err"
```

- Not run. Stopped the rehearsal on the current run’s confirmed scratch isolation failure.

### base M4

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli 2" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 400 --max-budget-usd 8 < /dev/null \
  > "<scratch>/logs/base-M4.jsonl" 2> "<scratch>/logs/base-M4.err"
```

- Not run. Stopped the rehearsal on the current run’s confirmed scratch isolation failure.

### base M5

```bash
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-run plans/2026-11-02-todo-cli merge F1 F3" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model sonnet \
  --max-turns 100 --max-budget-usd 3 < /dev/null \
  > "<scratch>/logs/base-M5.jsonl" 2> "<scratch>/logs/base-M5.err"
```

- Not run. Stopped the rehearsal on the current run’s confirmed scratch isolation failure.

### base M6

```bash
python -m pytest -q
MSYS_NO_PATHCONV=1 timeout 3600 claude -p "/wave-status" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 60 --max-budget-usd 0.5 < /dev/null \
  > "<scratch>/logs/base-M6.jsonl" 2> "<scratch>/logs/base-M6.err"
```

- Not run. Stopped the rehearsal on the current run’s confirmed scratch isolation failure.

## Results

| Step | Expectation | Current | Current evidence | v2.12.0 |
| --- | --- | --- | --- | --- |
| M0 | Status check exits 0 and emits no output | Pass | `cur-M0.exit`, empty `cur-M0.out` and `cur-M0.err` | Not run |
| M1 | Driver exits 0, prints only the manual-flow refusal and leaves no driver directory | Pass | `cur-M1.out`, `cur-M1.exit`, `cur-M1.driver-dir` | — |
| M2 | Final result opens with `Started:` | Pass | `cur-M2.jsonl:162` | Not run |
| M2 | Wave 1, A and C ✅ | Finding | A ✅. Wave 1 and C ⚠️ I1 at `7b8cf02`. | Not run |
| M2 | F2 👀 review with its review block | Finding | F2 ⚠️ I1 and no review block in `cur-M2.jsonl:162`. | Not run |
| M2 | F1 🔄, waiting for wave 2 | Pass | `cur-M2.jsonl:162`, tracking commit `7b8cf02` | Not run |
| M2 | Final result ends with a question about merging F2 | Finding | `cur-M2.jsonl:162` says there is no merge question. | Not run |
| M2 | `main` unchanged, no `integration/*` branch or `refs/wave-method/claims/*` ref | Pass | `ad408c0` before and after, `cur-M2.after.refs` | Not run |
| M2 | Tracking README has no `Flow:` line | Pass | `cur-M2.after.readme` at `7b8cf02` | Not run |
| M2 | Current result shows `Flow: manual` | Pass | `cur-M2.jsonl:162` | — |
| M3 | No first-parent non-merge commits on `main` | Pass | Empty `cur-M3.nonmerges` | Not run |
| M3 | A merge commit brings in F2 and its tracking row records that hash | Finding | `Stop not-ready` in `cur-M3.jsonl:27`. No new merge and F2 remains ⚠️ I1 at `7b8cf02`. | Not run |
| M4 | Wave 2, B and D ✅ | Pass | `cur-M4.jsonl:172`, tracking commit `2724bb8` | Not run |
| M4 | F1 and F3 👀 review and the result asks whether to merge them | Pass | Questions beginning `Merge F1` and `Merge F3` in `cur-M4.jsonl:172`. | Not run |
| M4 | `main` unchanged | Pass | `ad408c0` before and after | Not run |
| M5 | Only merge commits on `main`, including F1 and F3, with both hashes in the tracking README | Pass | `3ad0e1a`, `fad03b1`, `fce160a`, empty `cur-M5.nonmerges`, tracking commit `bba5700` | Not run |
| M5 | Every feature ✅ merged | Finding | F1 and F3 ✅ merged, F2 ⚠️ I1 at `bba5700`. | Not run |
| M5 | Plan archived as specified by `wave-plan/layout.md` | Finding | The plan remained at its active path, `cur-M5.after.tracking-tree`. | Not run |
| M6 | 11 pytest cases pass in the main checkout after M5 | Not run | Stopped at scratch isolation failure. `cur-M5.jsonl:77` reports 11 passed in feature worktrees. | Not run |
| M6 | `/wave-status` names no plan in progress or shows the archived plan as finished | Not run | No `cur-M6.jsonl`. | Not run |
| Common rules | Nested checks use the scratch environment and temporary dependency writes stay under `<scratch>` | Finding | `cur-M2.jsonl:117,120`, `cur-M4.jsonl:99,114,118,120` and the host path check. | Not run |
| Comparison | Observable current and v2.12.0 results agree apart from the `Flow: manual` line and wording | Not run | Only the current side of the comparison was recorded. | Not run |

Branch creation is measured by refs added between snapshots. Worktrees are shown by their checked-out branches. All README statuses below come from `plan/todo-cli` after each step.

| Step | Repository | Branches created | Worktrees left | Commits on `main` (merge / non-merge) | README statuses on tracking branch | Report asked a merge question | Stop line |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M2 | cur | `feat/todo-cli/F1-todo-store-and-cli`, `feat/todo-cli/F2-usage-readme` | `main`, `feat/todo-cli/F1-todo-store-and-cli`, `feat/todo-cli/F2-usage-readme`, `plan/todo-cli` | 0 / 0 | Waves 1 ⚠️ I1, 2 ⬜. Tasks A ✅, B ⬜, C ⚠️ I1, D ⬜. Features F1 🔄, F2 ⚠️ I1, F3 ⬜ | No | None |
| M2 | base | Not run | Not run | Not run | Not run | Not run | Not run |
| M3 | cur | None | `main`, `feat/todo-cli/F1-todo-store-and-cli`, `feat/todo-cli/F2-usage-readme`, `plan/todo-cli` | 0 / 0 | Waves 1 ⚠️ I1, 2 ⬜. Tasks A ✅, B ⬜, C ⚠️ I1, D ⬜. Features F1 🔄, F2 ⚠️ I1, F3 ⬜ | No | Stop not-ready: F2 is ⚠️ blocked, not `👀 review` — next: `/wave-plan plans/2026-11-02-todo-cli` · `$wave-plan plans/2026-11-02-todo-cli`, or accept I1 as is (see below) |
| M3 | base | Not run | Not run | Not run | Not run | Not run | Not run |
| M4 | cur | `feat/todo-cli/F3-ci-tests` | `main`, `feat/todo-cli/F1-todo-store-and-cli`, `feat/todo-cli/F2-usage-readme`, `feat/todo-cli/F3-ci-tests`, `plan/todo-cli` | 0 / 0 | Waves 1 ⚠️ I1, 2 ✅. Tasks A ✅, B ✅, C ⚠️ I1, D ✅. Features F1 👀 review, F2 ⚠️ I1, F3 👀 review | Yes | None |
| M4 | base | Not run | Not run | Not run | Not run | Not run | Not run |
| M5 | cur | None | `main`, `feat/todo-cli/F2-usage-readme`, `plan/todo-cli` | 3 / 0 | Waves 1 ⚠️ I1, 2 ✅. Tasks A ✅, B ✅, C ⚠️ I1, D ✅. Features F1 ✅ merged, F2 ⚠️ I1, F3 ✅ merged | No | None |
| M5 | base | Not run | Not run | Not run | Not run | Not run | Not run |

## Not verified

- The main-checkout pytest run and `/wave-status` after current M5. The launcher stopped after M5’s last result was written and before it started M6.
- Baseline M0 and M2–M6, and agreement between the current and v2.12.0 flows. Baseline seeding completed. The scratch isolation failure stopped the chain before any baseline step.
- The operating-system exit code for current M5. The terminal result was successful, but the stopped launcher left no exit record.

## Repeat

Use Git Bash and the setup block to create a fresh scratch directory. The nested environment must honor the scratch boundary for the full sequence to run.

1. Save the working-folder refs with `git -C "$working" for-each-ref --format='%(refname) %(objectname)'`.
2. Run the current M0–M6 commands above from `"$scratch/cur"`, then baseline M0 and M2–M6 from `"$scratch/base"`. Substitute the new scratch and working-folder paths. Use the last `result` event per call and stop starting new calls when their cumulative cost reaches USD 20.
3. For each call, save `git for-each-ref --format='%(refname) %(objectname)'` and `git worktree list --porcelain` before and after. Use `git rev-parse main` and `git rev-list --no-merges --first-parent <before>..main` to check main at the approval steps.
4. Repeat the working-folder ref snapshot and compare it with the first.
