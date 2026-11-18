# P21. Isolated reruns of both end-to-end rehearsals

User problem: (re-plan, I6, I7, and the checks of I8 and I9) the first manual run wrote dependencies outside the
scratch folder and was stopped before M6 and before the whole `v2.12.0` chain; the fixes of P18–P20 need a run
that shows them working · feature F2

This file amends `solutions/P9-end-to-end-runs.md`. Everything there holds unless a section below replaces it. Tasks N
and O read P9 first, then this file.

## Cause

- **I6.** The launcher prepended the scratch venv to `PATH`, but the Bash tool of the headless sessions resolved
  `C:/Program Files/Python314/python.exe` (its shell is set up from the user's profile, not only from the inherited
  environment). Without pytest and PyYAML there, the coordinator ran `pip install` into the user site and made extra
  venvs. `MSYS_NO_PATHCONV=1`, set for the `claude` call so Git Bash keeps `/wave-run` intact, is inherited by every
  nested shell, so a native program given `/tmp/yamlchk` wrote `C:/tmp/yamlchk`.
- **I7.** The launcher ran the chain as one long script; stopped after M5's result, it never wrote M5's exit code, and
  M6 and every `base` step stayed unrun.
- **I8, I9.** Fixed in P18 and P19; no run has shown the fixed behaviour yet.

## Approach

1. **Isolation.** Claude Code sources the file named by `CLAUDE_ENV_FILE` before every Bash command of the session
   and its subagents. The env file activates the scratch venv, unsets `MSYS_NO_PATHCONV` and points every
   Python, pip and temp-file location into scratch. A **preflight** call (P0) proves it before any skill runs; a
   **watch** after every call proves nothing was written to the two places I6 found.
2. **One call per shell command.** Each call is its own foreground shell command that writes its exit code in the
   same command line, so a stop between calls loses nothing.
3. **Manual rerun (task N):** P9 "Manual run", all of it, on the fixed example 01 (P20); the expectations of P9 hold as
   written.
4. **Autonomous rerun (task O):** P9 "Autonomous run" plus a forced out-of-scope edit in task B's commit, made by a git
   hook, so the P18 path (entry, revert, blocked feature) runs deterministically; the expectations change as below.

## Isolation (replaces P9 "Python for the projects")

Run once, first, in Git Bash (POSIX `sh` elsewhere), before seeding:

```bash
scratch=$(mktemp -d)
ws=$(cygpath -m "$scratch" 2>/dev/null || printf '%s' "$scratch")
mkdir -p "$scratch/logs" "$scratch/tmp" "$scratch/userbase" "$scratch/pip-cache"
gpy=$(command -v python); usersite=$("$gpy" -m site --user-site)
python -m venv "$scratch/venv"
bin="$scratch/venv/Scripts"; [ -d "$bin" ] || bin="$scratch/venv/bin"
cat > "$scratch/env.sh" <<EOF
unset MSYS_NO_PATHCONV
export VIRTUAL_ENV="$ws/venv"
export PATH="$bin:\$PATH"
export PIP_REQUIRE_VIRTUALENV=true
export PYTHONUSERBASE="$ws/userbase" PIP_CACHE_DIR="$ws/pip-cache"
export TMPDIR="$ws/tmp" TMP="$ws/tmp" TEMP="$ws/tmp"
EOF
. "$scratch/env.sh"
export CLAUDE_ENV_FILE="$ws/env.sh"
"$bin/python" -m pip install pytest pyyaml
touch "$scratch/logs/start.stamp"
```

`CLAUDE_ENV_FILE` and the variables stay exported in the launcher shell, so every `claude` call and the driver
(task O) inherit them. Record `$gpy` and `$usersite` (as `<global python>`, `<user site>`) in the report, not in the
record.

**Watch.** After every call (P0, each M or A step, the driver run as one call):

```bash
{ find "$usersite" -maxdepth 1 -newer "$scratch/logs/start.stamp" 2>/dev/null
  [ -d /c/tmp ] && find /c/tmp -maxdepth 1 -newer "$scratch/logs/start.stamp"; } > "$scratch/logs/<step>.outside"
```

An empty file is a Pass. A non-empty one is a finding `wrote outside scratch: <paths>`: record it, delete nothing
outside scratch (the user decides), and start no further call; the remaining steps are Not run.

**Preflight P0.** After seeding, before the first step (task N: in `$scratch/cur`, once for both repositories, which
share the venv and env file; task O: in `$scratch/night`):

```bash
probe='Run this one command with the Bash tool: command -v python; python -c "import sys, tempfile; print(sys.prefix); print(tempfile.gettempdir())"; echo "pathconv=${MSYS_NO_PATHCONV-unset}". Then launch one subagent and have it run the same command with its Bash tool. Reply with both outputs verbatim.'
MSYS_NO_PATHCONV=1 timeout 600 claude -p "$probe" --output-format stream-json --verbose \
  --permission-mode bypassPermissions --setting-sources project,local --model haiku \
  --max-turns 8 --max-budget-usd 0.3 < /dev/null > "$scratch/logs/P0.jsonl" 2> "$scratch/logs/P0.err"; \
  echo $? > "$scratch/logs/P0.exit"
```

Judge P0 from the `tool_result` events of the stream (not from the reply's wording). Pass when both results show:
the python path under `<scratch>/venv`, `sys.prefix` equal to `$ws/venv` and the temp dir equal to `$ws/tmp`
(compared case-insensitively with `\` read as `/`), and `pathconv=unset`. A subagent result missing (no subagent
tool in print mode) is recorded and does not fail P0 when the session's own result passes. **P0 fails → the
procedure does not work on this machine: stop before any skill call**, record Setup and P0, mark every other step Not
run, and describe in the report what each result showed.

## Call form (amends P9 "Common rules")

Every call of P9 keeps its form and caps, written as one shell command that ends with
`; echo $? > "$scratch/logs/<repo>-<step>.exit"`, followed by its snapshots and the watch. Never run the chain, or
several calls, as one script or a background job. Per call the record also names the `.exit` value and the watch
result.

## Manual rerun (task N)

P9 "Manual run (task I)" unchanged: `cur` then `base`, M0–M6 each (M1 `cur` only), every expectation, the comparison
table. The `base` repository is seeded from `$scratch/v2120` but its plan comes from the working folder's
`examples/01-greenfield-todo-cli`, now with the P20 fix, the same for both. So M2 must give F2 `👀 review` with a merge
question on both sides, M3 must merge F2, and M5 must archive the plan. A remaining difference between `cur` and
`base` in a comparison cell is a finding "manual flow differs from v2.12.0", as P9 says.

## Autonomous rerun (task O)

P9 "Autonomous run (task J)" with these changes.

**Forced out-of-scope edit.** After the forced-red commit and before the remote, install this hook in
`$scratch/night/.git/hooks/post-commit` (not committed; worktrees share it):

```sh
#!/bin/sh
# End-to-end run: task B's first commit also adds stray.txt, outside its file list.
marker="$(git rev-parse --git-common-dir)/stray-done"
[ -e "$marker" ] && exit 0
case "$(git log -1 --format=%s)" in
  "wordstat-cli F2 / B:"*) ;;
  *) exit 0 ;;
esac
touch "$marker"
printf 'forced out-of-scope file of the end-to-end run\n' > stray.txt
git add stray.txt
git commit -q --amend --no-edit --no-verify
```

`chmod +x` it. Prove it in a throwaway repository `$scratch/hookprobe` (init, same identity, copy the hook):
`git commit -q --allow-empty -m "wordstat-cli F2 / B: probe"` → `git show --name-only --format= HEAD` prints
`stray.txt`; a second `git commit -q --allow-empty -m "wordstat-cli F2 / B: again"` adds nothing; the message of the
first commit is unchanged. A failing probe is a procedure failure: stop as for P0. Then delete the marker of the probe
only (it lives in `hookprobe/.git`, not in `night`).

**Expectations that replace P9's for A2–A6** (A1 and the setup checks are unchanged):

- A2: F1 `✅ merged`, auto-approved; its block in `report.md` ends `Approved: auto — every task ✅ or ➖, check green,
  no open entry, tier gate clean, scope clean, not under manual review`. No `__pycache__` or other generated path in
  `git log --no-merges --name-only --format= main..integration/wordstat-cli`.
- A2: task B ⚠️ and F2 `⚠️ blocked I<a>`, `Waiting for: I<a>`, where I<a> is open in `problems.md` on
  `plan/wordstat-cli` and names `stray.txt`; `git log --format=%s integration/wordstat-cli..feat/wordstat-cli/F2-top-words-cli`
  shows B's commit(s) and a `Revert "wordstat-cli F2 / B: …"` commit and no other commit that deletes `stray.txt`;
  `git diff --quiet integration/wordstat-cli...feat/wordstat-cli/F2-top-words-cli` exits 0 (the revert leaves no net
  change); `git merge-base --is-ancestor feat/wordstat-cli/F2-top-words-cli integration/wordstat-cli` fails.
- A2: F4 ⚠️ blocked by the forced red, F3 `👀 review`, `main`, the remote, claims and lock as P9 says.
  `report.md` lists F2 and F4 under "Blocked and waiting" and only F1 under "Merged, not in main".
- A3: F3 `✅ merged` into `integration/wordstat-cli`; the `Merged` cells of F2 and F4 stay empty;
  `python <working folder>/skills/wave-plan/scripts/status_check.py plans/2026-11-04-wordstat-cli` in the tracking
  worktree (`git -C "$scratch/night" worktree list` names it) exits 0.
- A4: the merge succeeds; `python -m pytest -q` → `7 passed, 1 skipped` (F1's 7 cases; F2 and F4 never reached
  `main`).
- A5: `next: nothing — …`, no call for F2 or F4.
- A6: F2 and F4 ⚠️ with their entries; `Merged, not in main:` shows none.

Which gate caught `stray.txt` (step 5 of the wave, or auto-approval condition 6) is recorded, not judged. If B's
executor notices `stray.txt` and removes it in a later commit, the expectations above still hold: the scope command
lists the file anyway.

## Record (amends P9 "Record format")

Same file names and six sections as P9; task N rewrites `docs/rehearsals/end-to-end-manual.md`, task O
`docs/rehearsals/end-to-end-autonomous.md`, as new records of the new runs (the old text goes; git history keeps it).
"Setup" shows the isolation block and, for O, the hook and its probe; "Runs" starts with `### P0`; "Results" has one
row for P0, one for the watch (all calls), and for O one per expectation above. Paths: `<scratch>`, `<working folder>`,
`<home>`; never `$gpy` or `$usersite` as real paths.

## Limits

- The watch covers the two places I6 found, not the whole disk; the record says so under "Not verified".
- `CLAUDE_ENV_FILE` is the only isolation mechanism; if P0 fails, do not try another one (`PATH` tricks, a
  `CLAUDE.md`, settings files): stop and report.
- Costs and caps as P9: N stops starting calls at 20 USD, O at 25 USD.

## Acceptance tests

1. Each record has the six sections; P0 and the watch have a result; every expectation of P9 (task N) or of this file
   (task O) is Pass, Finding or Not run with evidence.
2. Task N: the comparison table covers M2–M5 for `cur` and `base`, and every call has an exit code.
3. Task O: F2 blocked by an entry naming `stray.txt`, its revert, the empty `Merged` cells of F2 and F4 after A3, and
   `status_check.py` exit 0 at A3 are each shown with evidence.
4. Every `.outside` file is empty, or the run stopped right after the first non-empty one and the record names its
   paths.
5. The check command of the wave file is green; the working folder's refs are unchanged except the task's own
   branch.
