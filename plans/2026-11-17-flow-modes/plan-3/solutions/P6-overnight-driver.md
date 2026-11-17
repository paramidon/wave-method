# P6. Overnight driver
User problem: a cross-platform driver (Python 3.9+, stdlib only) runs plan parts and waves as fresh headless Claude
Code sessions, with rails, a lock and a log, and writes a morning report · feature F1

## Cause

No automation exists: every step is a session the user launches. The skills already have everything a driver needs:
autonomous flow never asks (`skills/wave-plan/layout.md`, "Flow", "Decision table"), every stop is one parsable line
(`skills/wave-run/SKILL.md:89-116`, `skills/wave-plan/layout.md:500`), plan state lives in git
(`docs/claude-print-mode.md:391-409`, "Reading the result", rule 4), and the print-mode call form and caps are
measured (`docs/claude-print-mode.md:347-374`). What is missing is the program that reads the state, picks the next
call, runs it, checks it and reports.

## Approach

- One feature. The driver lives in the repository root `scripts/` (the user's words), as an entry script
  `scripts/wave_driver.py` plus a package `scripts/wavedriver/` of small modules, so the work can run in parallel
  tasks. The plugin ships the whole repository, so `scripts/` reaches plugin installs too; the installers stay
  unchanged (part 4 documents installation).
- The driver runs **against** a project repository (`--repo`, default the current folder), from wherever the
  wave-method files are. It imports `skills/wave-plan/scripts/status_check.py` from the same wave-method folder
  (`Path(__file__).resolve().parents[2] / "skills" / "wave-plan" / "scripts"` for modules in `scripts/wavedriver/`).
- **State is read from git only, never from reports** (`docs/claude-print-mode.md`, rule 4): the index from
  `<main branch>`, each plan README, wave files, `problems.md` and briefs from the plan's tracking branch. Reports are
  used only for the stop line and for the final `wave-status` text shown as it is.
- **Stateless loop.** Each iteration reads a fresh snapshot, picks the first runnable action, runs one `claude -p`
  call, checks it, and records halts. The only memory between iterations: halted units, attempt counters, task-mode
  tasks already run, counters.
- **Units.** A unit is one plan folder: for an index, `<index folder>/plan-<K>` of every part (planned or not); for a
  plan-folder start, that folder. A halt stops one unit; the driver goes on with the others ("skip to independent
  work"). Parts that wait for an earlier part become runnable only when the git check says that part is merged
  (layout.md, "Chained parts and the integration branch", check 3), so a halted part never lets a dependant start.
- **Actions** (only these; no triage, no re-plan, no merge form, no flow form — those are the user's): plan an
  unplanned part (`/wave-plan flow autonomous <index> part <K>`, plan model), run the first ⬜ wave
  (`/wave-run <plan folder> <N>`, run model), run a task waiting for task mode (`/wave-run <plan folder> <N> task
  <ID>`, model of the task's tier) and resume that wave (`/wave-run <plan folder> <N>`). At the end one
  `/wave-status` call (status model) whose text goes into the report.
- **Manual-flow plans are not driven**: they are halted with the flow-form command as `next`. The driver plans index
  parts with `flow autonomous` explicitly, so the parts it plans are always autonomous.
- **Guards instead of trust.** Before and after every call the driver snapshots `refs/heads/<main branch>`, every
  `refs/remotes/*`, the main checkout's branch and its tracked status. Any change ends the run at once ("never push,
  never touch the main branch" is then checked, not hoped for).
- **Permission mode** default `auto` (`docs/claude-print-mode.md`, Q-a passed every step), not `bypassPermissions`:
  the driver runs in the user's own repository, not an isolated one. `--permission-mode bypassPermissions` is for
  isolated clones. Denials are recorded as warnings; progress is judged by git.
- Why not one Python file: six parallel tasks would edit the same file. Why not a re-plan or merge action: those are
  the user's decisions (open problems, manual review); the report gives the commands.

## Files

| File | Task | Holds |
|---|---|---|
| `scripts/wavedriver/__init__.py` | A | one docstring line |
| `scripts/wavedriver/gitstate.py` | A | git access, parsers, snapshot |
| `scripts/tests/test_gitstate.py` | A | its tests |
| `scripts/wavedriver/claude.py` | B | call, command line, subprocess run, result classification |
| `scripts/tests/test_claude.py` | B | its tests |
| `scripts/wavedriver/rails.py` | C | lock, log, deadline, counters, rails, guard |
| `scripts/tests/test_rails.py` | C | its tests |
| `scripts/tests/fake_claude.py`, `scripts/tests/test_fake_claude.py` | D | scripted stand-in for `claude` |
| `scripts/wavedriver/decide.py`, `scripts/tests/test_decide.py` | E | next action, halts after a call |
| `scripts/wavedriver/report.py`, `scripts/tests/test_report.py` | F | morning report |
| `scripts/wave_driver.py`, `scripts/tests/test_driver.py` | G | CLI and loop; end-to-end tests with the fake |
| `docs/wave-driver.md`, `.github/workflows/release.yml` | H | the short doc; CI runs the driver tests |

Common rules for every module:

- Python 3.9+, standard library only. `from __future__ import annotations` at the top; no `match`, no `X | Y` outside
  annotations, no `str.removeprefix` (3.9 has it, but keep to `startswith` + slicing for clarity).
- Every subprocess call: argument list (never `shell=True`), `text=True, encoding="utf-8", errors="replace"`.
- Every test file starts with
  `sys.path.insert(0, str(Path(__file__).resolve().parents[1]))` and imports `from wavedriver import <module>`;
  tests use `unittest` and temporary folders (`tempfile.TemporaryDirectory`); git repositories in tests are created
  with `git init -b main` and `user.name`/`user.email` set locally. The suite runs with
  `python -m unittest discover -s scripts/tests -v` from the repository root.
- Paths of plan folders and index files are repository-relative POSIX strings (`plans/2026-11-17-x/plan-1`), never
  with a trailing slash.

## API

### `gitstate.py` (task A)

```python
SKILL_SCRIPTS = Path(__file__).resolve().parents[2] / "skills" / "wave-plan" / "scripts"
# sys.path.insert(0, str(SKILL_SCRIPTS)); import status_check  -> reuse status_check.tables, .mark, .cells, .check

class GitError(RuntimeError): ...

class Git:
    def __init__(self, repo: Path) -> None
    def run(self, *args: str, check: bool = True) -> str     # git -C <repo> <args>; stdout with the trailing newline stripped; GitError(f"git {' '.join(args)}: {stderr}") when check and exit != 0
    def ok(self, *args: str) -> bool                         # exit code == 0
    def show(self, ref: str, path: str) -> Optional[str]     # git show <ref>:<path>, None when missing
    def exists(self, ref: str) -> bool                       # git rev-parse -q --verify <ref>^{commit}
    def is_ancestor(self, a: str, b: str) -> bool            # git merge-base --is-ancestor a b
    def branches(self, pattern: str) -> list[str]            # git for-each-ref --format=%(refname:short) refs/heads/<pattern>  e.g. "plan/*"
    def ls(self, ref: str, folder: str) -> list[str]         # git ls-tree --name-only <ref> <folder>/ -> repository-relative paths; [] when missing
    def toplevel(self) -> Path                               # git rev-parse --show-toplevel
    def common_dir(self) -> Path                             # absolute git rev-parse --git-common-dir

def resolve_main(git: Git, explicit: Optional[str] = None) -> str
    # explicit when given and refs/heads/<explicit> exists; else "main" if it exists; else "master"; else GitError

@dataclass
class Feature:
    id: str; slug: str; title: str; done_when: str
    status: str          # the mark: ⬜ 🔄 👀 ✅ ⚠️ ❌ ➖ ("" when none)
    cell: str            # the whole Status cell, e.g. "⚠️ I4" or "✅ merged"
    waiting: str         # "Waiting for" cell
    branch: str          # "Branch" cell without backticks
    merged: str          # "Merged" cell without backticks ("" when empty)
    @property
    def is_merged(self) -> bool   # re.search(r"✅\s+merged\b", cell)

@dataclass
class Wave:
    number: int; file: str; status: str; cell: str     # file without backticks, e.g. "waves/w01.md"

@dataclass
class Task:
    id: str; slug: str; feature: str; wave: int; complexity: str; status: str; cell: str

@dataclass
class Readme:
    slug: str
    flow: str                    # "manual" | "autonomous"
    target: Optional[str]        # "integration/<name>" in autonomous flow, else None
    manual_review: list[str]
    features: list[Feature]; waves: list[Wave]; tasks: list[Task]

def parse_readme(text: str) -> Readme       # ValueError when slug or a table is missing

@dataclass
class WaveFile:
    depends_merged: list[str]    # F-IDs written "F<k> merged" in the "Depends on:" paragraph
    needs: dict[str, str]        # task ID -> Needs cell, "" for "—", "-" or empty
    waiting_ids: list[str]       # IDs of a "Waiting: task mode …" line that is the last non-empty line of "## Execution"
    last_stop: str               # the last line of "## Execution" that starts with "Stop ", else ""

def parse_wave_file(text: str) -> WaveFile

@dataclass
class Entry:
    id: str; scope: str; essence: str; status: str; open: bool; features: list[str]

def parse_problems(text: str) -> list[Entry]

@dataclass
class Part:
    number: int; slug: str; plan_when: str; after: list[int]

@dataclass
class Index:
    path: str; folder: str; topic: str; target: str; parts: list[Part]

def parse_index(text: str, path: str) -> Index

@dataclass
class PlanState:
    folder: str; source: str; tracking: bool
    readme: Readme
    problems: list[Entry]
    wave_files: dict[int, WaveFile]      # every wave whose status is ⬜, 🔄 or ❌
    merged_not_in_main: list[str]        # feature IDs: ✅ merged and the Merged hash is not an ancestor of <main branch>
    briefs: dict[str, str]               # feature ID -> brief text, for merged_not_in_main and 👀 review features that have one
    check_lines: list[str]               # output of status_check.check on the tracking worktree's plan folder; [] when that folder is missing

@dataclass
class PartState:
    part: Part; folder: str; plan: Optional[PlanState]; ready: bool; ready_reason: str

@dataclass
class TargetState:
    name: str; exists: bool; ahead: int; worktree: str     # name "integration/<n>"; ahead = commits <main branch> lacks

@dataclass
class Snapshot:
    repo: Path; main: str
    index: Optional[Index]
    parts: list[PartState]          # index start: one per Parts row, in order; plan start: []
    plans: list[PlanState]          # every planned unit, in unit order
    targets: dict[str, TargetState] # every target named by a plan in scope or by the index
    heads: dict[str, str]

def heads(git: Git, main: str) -> dict[str, str]
def read_plan(git: Git, folder: str, main: str, slug: Optional[str] = None) -> Optional[PlanState]
def part_merged(git: Git, index: Index, number: int, main: str) -> tuple[bool, str]
def read_snapshot(git: Git, start: str, main: str) -> Snapshot
```

### `claude.py` (task B)

```python
DEFAULT_MODELS = {"plan": "opus", "run": "sonnet", "status": "haiku",
                  "low": "haiku", "medium": "sonnet", "high": "opus"}
DEFAULT_CAPS = {"wave-plan": (50, 4.0), "wave-run": (110, 3.0),
                "task": (110, 5.0), "wave-status": (60, 0.5)}      # (max turns, max USD)

@dataclass
class Call:
    skill: str          # "wave-plan" | "wave-run" | "wave-status"
    args: str           # text after the slash command, may be ""
    model: str
    max_turns: int
    max_usd: float

@dataclass
class Settings:
    claude: list[str]                         # command prefix, e.g. ["C:/Users/x/.local/bin/claude.exe"]
    skill_prefix: str = ""                    # "wave-method:" for a plugin install
    permission_mode: str = "auto"
    add_dirs: list[str] = field(default_factory=list)
    extra_args: list[str] = field(default_factory=list)
    timeout_s: int = 7200

@dataclass
class Result:
    outcome: str            # "ok" | "stop" | "failed" | "timeout" | "limit" | "auth"
    exit_code: Optional[int]
    data: dict
    text: str               # data["result"] or ""
    stderr: str
    minutes: float          # wall time
    cost: float             # data["total_cost_usd"] or 0.0
    turns: int              # data["num_turns"] or 0
    denials: int            # len(data["permission_denials"]) or 0
    stop_code: str = ""
    stop_line: str = ""
    next: str = ""
    detail: str = ""        # why it failed: subtype, errors, timeout
    warnings: list[str] = field(default_factory=list)

def both(command: str) -> str
    # both("wave-run plans/x 2") -> "`/wave-run plans/x 2` · `$wave-run plans/x 2`"
def prompt(call: Call, settings: Settings) -> str
    # f"/{settings.skill_prefix}{call.skill} {call.args}".rstrip()
def command(call: Call, settings: Settings) -> list[str]
def parse_output(stdout: str) -> dict
def parse_stop(text: str) -> Optional[tuple[str, str, str]]    # (code, whole stop line, next)
def classify(exit_code: Optional[int], data: dict, stderr: str) -> tuple[str, str]   # (outcome, detail) for the non-stop cases
def run(call: Call, settings: Settings, cwd: Path, raw_path: Optional[Path] = None) -> Result
```

### `rails.py` (task C)

```python
class LockHeld(Exception):
    holder: str                               # the lock file's text

class Lock:
    def __init__(self, path: Path) -> None
    def acquire(self) -> str                  # returns the holder line it wrote; LockHeld when the file exists
    def release(self) -> None                 # deletes the file only if it still holds this lock's token

class Log:
    def __init__(self, path: Path, echo: bool = True) -> None
    def write(self, message: str) -> None

def parse_deadline(text: str, now: datetime) -> datetime

@dataclass
class Limits:
    max_calls: int = 60
    max_failures: int = 3
    deadline: Optional[datetime] = None
    max_usd: Optional[float] = None

@dataclass
class Counters:
    calls: int = 0; failures: int = 0; failures_in_row: int = 0
    cost: float = 0.0; turns: int = 0; minutes: float = 0.0
    def record(self, outcome: str, cost: float, turns: int, minutes: float) -> None

def rail_reason(limits: Limits, counters: Counters, now: datetime) -> Optional[str]

def guard_snapshot(repo: Path, main: str) -> dict[str, str]
def guard_violations(before: dict[str, str], after: dict[str, str]) -> list[str]
```

### `fake_claude.py` (task D)

A script that stands in for `claude` in tests, driven by a scenario file. Interface in "Algorithm", "Fake claude".

### `decide.py` (task E)

```python
TARGET_CODES = {"target-unsafe", "target-conflict", "target-unmerged"}

@dataclass
class Halt:
    unit: str; reason: str; next: str = ""

@dataclass
class Action:
    kind: str               # "plan" | "wave" | "task" | "resume"
    unit: str
    call: claude.Call
    why: str
    wave: int = 0           # wave number for wave, task, resume
    task: str = ""          # task ID for task

@dataclass
class Choice:
    action: Optional[Action]
    halts: list[Halt]       # units found blocked by their state in this scan (new halts)
    waits: list[Halt]       # units that are not runnable now but not blocked: waiting parts, finished plans

@dataclass
class DecideConfig:
    models: dict = field(default_factory=lambda: dict(claude.DEFAULT_MODELS))
    caps: dict = field(default_factory=lambda: dict(claude.DEFAULT_CAPS))

def units(snapshot: gitstate.Snapshot) -> list[str]
def target_of(snapshot: gitstate.Snapshot, unit: str) -> str
def choose(snapshot, halted: dict[str, Halt], task_runs: set, cfg: DecideConfig) -> Choice
def after_call(action: Action, result: claude.Result, snapshot, progressed: bool,
               attempts: dict) -> list[Halt]
def status_call(snapshot, cfg: DecideConfig) -> claude.Call
```

### `report.py` (task F)

```python
@dataclass
class CallRecord:
    number: int; started: str; kind: str; unit: str; prompt: str; model: str
    outcome: str; exit_code: Optional[int]; subtype: str
    turns: int; cost: float; minutes: float; denials: int
    stop_line: str = ""; detail: str = ""; warnings: list[str] = field(default_factory=list)

@dataclass
class RunInfo:
    started: datetime; finished: datetime
    repo: str; start: str; main: str
    end_reason: str
    options: list[str]          # "name: value" lines
    out_dir: str; log_path: str

def brief_sections(text: str) -> dict[str, str]
def merged_block(snapshot, plan, feature, brief: Optional[str]) -> str
def review_block(snapshot, plan, feature, brief: Optional[str]) -> str
def next_commands(snapshot, halts: list) -> list[str]
def render(run: RunInfo, snapshot, calls: list[CallRecord], halts: list, waits: list,
           status_text: Optional[str]) -> str
```

### `wave_driver.py` (task G)

```python
def main(argv: Optional[list[str]] = None, claude_prefix: Optional[list[str]] = None) -> int
if __name__ == "__main__": sys.exit(main())
```

`claude_prefix` replaces the `claude` command (tests pass `[sys.executable, <fake_claude.py>]`).

## Algorithm

### Reading state (task A)

- `parse_readme`: slug from the header, regex ``slug: `([^`]+)` ``. Tables with `status_check.tables(lines, report)`
  (a no-op `report`), columns by header name; `mark()` for the status; strip backticks from File, Branch, Merged, Slug.
  `Wave` and task `Wave` cells to `int` (a cell that is not a number → skip the row). Flow: the line
  `^- Flow: (.+)$` (multiline). Absent, or its value starts with `manual` → `flow="manual"`, `target=None`. Else
  split the value at `·`, strip each part and backticks: first part `autonomous`; a part `target: <t>` → target `<t>`;
  a part `manual review: …` → `re.findall(r"F\d+", part)`; no target part → `integration/<slug>`.
- `parse_wave_file`: the "Depends on:" paragraph is the line starting `Depends on:` and the following lines up to the
  first blank line; remove backticks; `re.findall(r"\b(F\d+) merged\b", paragraph)`. Needs: the table under
  `## Tasks` (columns ID and Needs). Execution: the lines after `## Execution` up to the next `## ` heading; the last
  non-empty line starting `Waiting: task mode ` → IDs are `re.findall(r"\b[A-Z]{1,2}\b", line.split(" — ", 1)[0][len("Waiting: task mode "):])`.
  `last_stop`: the last line there starting with `Stop `.
- `parse_problems`: entries start with `^- \*\*\[(I\d+) · ([^\]]*)\]\s*(.*?)\*\*`; an entry's block runs to the next
  entry; status = text after the last `status:` of the block, stripped; `open` = status starts with `open` or `→`;
  features = `re.findall(r"feature (F\d+)", scope)`.
- `parse_index`: `folder` = the parent of `path`; `topic` = the folder's last name without `^\d{4}-\d{2}-\d{2}-`;
  `target` = `target: <t>` of a `^- Flow: autonomous` header line, else `integration/<topic>`. Parts: the table under
  `## Parts`, columns Part, Plan slug (backticks stripped), Plan when; `after` = every number in Plan when that is
  not `now` (`re.findall(r"\d+", cell)`).
- `read_plan(git, folder, main, slug)`: sources in order: `plan/<slug>` when slug is given and the branch exists;
  without a slug every branch of `branches("plan/*")` whose `<branch>:<folder>/README.md` exists and whose README slug
  equals the branch name after `plan/`; then `main`; then every branch of `branches("integration/*")`. The first
  source that has the README is used for the README, `problems.md`, wave files (`<folder>/<wave.file>`) and briefs.
  None found → `None`. `tracking` = source is `plan/<readme.slug>`. Briefs: in `ls(source, folder + "/reviews")` the
  file whose name matches `^F<k>(-.*)?\.md$`. `check_lines`: when
  `<repo.parent>/<repo.name>.worktrees/<slug>-plan/<folder>` is a folder, run `status_check.check(Path(...))` with
  stdout and stderr redirected into a buffer (`contextlib.redirect_stdout/redirect_stderr`), its lines.
- `part_merged(git, index, J, main)`: P10's check 3 (`skills/wave-plan/layout.md:544-558`). README of part J from the
  first of `plan/<slug of J>`, `main`, `index.target` (when that branch exists) at
  `<index.folder>/plan-<J>/README.md`. None → `(False, f"part {J} is not planned")`. Else merged when every feature
  is `is_merged` or ➖ and each merged hash is an ancestor of `index.target` (when the branch exists) or of `main`.
  Not merged → `(False, "part J — F2 👀 review (review), F3 ⚠️ I4 (I4)")`: each feature that is neither ➖ nor merged
  into those branches, as `<id> <cell> (<waiting>)`, joined with `, `.
- `read_snapshot(git, start, main)`: `start` ending in `index.md` → index start: read it with
  `git.show(main, start)` (missing → `GitError`), one `PartState` per part, folder `<index folder>/plan-<K>`, plan =
  `read_plan(git, folder, main, part.slug)`; `ready` = `True, ""` when `after` is empty, else every J of `after` must
  pass `part_merged` (the first failing reason is `ready_reason`). Otherwise a plan start: `read_plan(git, start,
  main)`; `None` → `GitError(f"plan folder {start} not found on any branch")`. Targets: every `readme.target` of the
  plans in scope plus `index.target`; `exists` = branch exists; `ahead` =
  `int(git rev-list --count <main>..<target>)` when it exists else 0; worktree =
  `<repo.parent>/<repo.name>.worktrees/integration-<name after "integration/">`.
- `heads(git, main)`: `git for-each-ref --format=%(refname) %(objectname) refs/heads/plan refs/heads/integration
  refs/heads/feat refs/heads/task refs/wave-method/claims refs/heads/<main>` as a dict.

### Calling Claude (task B)

- `command`: `settings.claude + ["-p", prompt(call, settings), "--output-format", "json", "--permission-mode",
  settings.permission_mode, "--model", call.model, "--max-turns", str(call.max_turns), "--max-budget-usd",
  f"{call.max_usd:g}"]`, then `["--add-dir", d]` per add dir, then `settings.extra_args`.
- `run`: environment = `os.environ` plus `MSYS_NO_PATHCONV=1`; `stdin=subprocess.DEVNULL`; stdout and stderr piped;
  POSIX `start_new_session=True`, Windows `creationflags=subprocess.CREATE_NEW_PROCESS_GROUP`;
  `proc.communicate(timeout=settings.timeout_s)`. On `TimeoutExpired` or `KeyboardInterrupt`: kill the tree
  (Windows `taskkill /PID <pid> /T /F`; POSIX `os.killpg(os.getpgid(pid), signal.SIGTERM)`, wait 10 s, then
  `SIGKILL`), collect the output with `communicate()`; a timeout gives outcome `timeout`, detail
  `timeout after <n> min`; `KeyboardInterrupt` is re-raised after the kill. `raw_path`: write stdout, then a line
  `--- stderr ---`, then stderr (parents created). Minutes = wall time / 60.
- `parse_output`: `json.loads(stdout.strip())` when it is a dict; else the last line of stdout that parses as a dict
  with `type == "result"`; else `{}`.
- `parse_stop`: the non-empty lines of `text`, stripped; the candidate is the line after a first line that starts with
  `Started:`, else the first line; it must match `^Stop ([a-z][a-z-]*): ` → code; next = the part after the first
  ` — next: ` (`""` when absent).
- Classification in `run`, first rule that holds:
  1. timeout → `timeout`.
  2. The run failed (exit code not 0, or `is_error` true, or `subtype` not `success`, or no `result` key) and
     `api_error_status` is 429 or 529, or the joined text of `result`, `errors` and stderr matches
     `(?i)usage limit|rate[ -]?limit|limit reached|hit your limit|overloaded|too many requests|quota` → `limit`.
  3. The run failed and `api_error_status` is 401 or the text matches
     `(?i)not logged in|/login|invalid api key|authentication|unauthorized` → `auth`.
  4. The run failed → `failed`, detail `exit <code>, <subtype>: <errors joined with "; ">`.
  5. `parse_stop(text)` → `stop` with code, line and next.
  6. Otherwise `ok`.
  Warnings (any outcome with a text): first non-empty line does not start with `Started:` → `no Started: line`;
  `denials > 0` → `<n> permission denials`; the last non-empty line ends with `?` → `ends with a question`.

### Rails (task C)

- `Lock.acquire`: `os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)`; write
  `pid <pid> host <socket.gethostname()> started <YYYY-MM-DD HH:MM> token <8 hex>` and a newline (token
  `secrets.token_hex(4)`). `FileExistsError` → `LockHeld` with the file's text. `release`: when the file still
  contains this token, delete it; otherwise leave it. The driver puts it at `<git common dir>/wave-driver.lock`.
- `Log.write`: append `YYYY-MM-DD HH:MM:SS <message>` + newline (utf-8, flushed); with `echo`, print the same line; a
  `UnicodeEncodeError` on print → print `line.encode("ascii", "replace").decode("ascii")`.
- `parse_deadline`: `HH:MM` → today at that time when later than `now`, else tomorrow; `YYYY-MM-DD HH:MM` → that
  time; anything else → `ValueError`.
- `Counters.record`: calls +1, cost/turns/minutes added; outcome `ok` or `stop` → `failures_in_row = 0`; `failed` or
  `timeout` → `failures` and `failures_in_row` +1; `limit` and `auth` count as failures too.
- `rail_reason`, first that holds: `counters.calls >= max_calls` → `max-calls: <n> calls made`;
  `failures_in_row >= max_failures` → `max-failures: <n> failed calls in a row`; deadline set and `now >= deadline` →
  `deadline: <YYYY-MM-DD HH:MM> reached`; `max_usd` set and `cost >= max_usd` → `max-usd: <cost:.2f> USD spent`.
  Else `None`.
- `guard_snapshot(repo, main)`: `git -C repo for-each-ref --format=%(refname) %(objectname) refs/heads/<main>
  refs/remotes` as entries, plus `"checkout:HEAD"` = `git symbolic-ref -q HEAD` (or `detached <sha>`) and
  `"checkout:status"` = `git status --porcelain --untracked-files=no`.
- `guard_violations`: one message per key that differs: `<key> changed: <before> -> <after>`, `<key> added`,
  `<key> removed` (sorted by key).

### Fake claude (task D)

`python scripts/tests/fake_claude.py <args>`:

- `--version` alone → prints `0.0.0 (fake claude)`, exit 0.
- Otherwise the prompt is the value after `-p`. Environment `FAKE_CLAUDE_SCENARIO` names a JSON file
  `{"steps": [step, …]}`. The stub appends one JSON line `{"argv": [...], "cwd": "<cwd>"}` to `<scenario>.calls`,
  reads the number of used steps from `<scenario>.state` (missing → 0), takes the next step, writes the new number.
- A step (every key optional except `expect`):

  ```json
  {"expect": "^/wave-run plans/x/plan-1 1$", "args": {"--model": "sonnet"},
   "commits": [{"branch": "plan/x-p1", "base": "main", "message": "Plan x-p1: wave 1 done",
                "files": {"plans/x/plan-1/README.md": "…{{rev:integration/x}}…"}}],
   "refs": {"refs/heads/integration/x": "feat/x-p1/F1-a"},
   "result": "Started: 2026-11-17 01:00\n…", "exit": 0, "subtype": "success", "is_error": false,
   "cost": 0.25, "turns": 12, "api_error_status": null, "denials": 0, "sleep": 0}
  ```

- No step left, `re.search(expect, prompt)` fails, or an `args` flag is missing or has another value → print
  `{"type": "result", "subtype": "error_during_execution", "is_error": true, "errors": ["fake: <why>"]}`, exit 1,
  nothing else done.
- Else in order: `sleep` seconds; each commit with git plumbing in the current folder (the repository):
  `parent = rev-parse -q --verify <branch>` else `<base>` (absent → no parent); a temporary index file
  (`GIT_INDEX_FILE`), `read-tree <parent>` when there is one, per file `hash-object -w --stdin` and
  `update-index --add --cacheinfo 100644,<blob>,<path>`, `write-tree`, `commit-tree <tree> [-p <parent>] -m <message>`
  with fixed author and committer (`fake <fake@example.com>`), `update-ref refs/heads/<branch> <commit>`; then each
  `refs` entry `update-ref <name> <rev-parse of value>`. In file contents and in `result`, `{{rev:<ref>}}` becomes
  `git rev-parse --short <ref>` at that moment.
- Output: one JSON line `{"type": "result", "subtype": …, "is_error": …, "result": <result>, "num_turns": <turns>,
  "total_cost_usd": <cost>, "permission_denials": [{} × denials], "api_error_status": …}`; the `result` key is left
  out when `subtype` starts with `error`. Exit with `exit`.

### Choosing the next action (task E)

`units(snapshot)`: `[ps.folder for ps in snapshot.parts]` for an index start, else `[snapshot.plans[0].folder]`.
`target_of`: the unit's `plan.readme.target` when planned, else `snapshot.index.target`.

`choose` scans every unit in order, skips units in `halted`, collects new halts and waits, and takes the first action
it finds (it still finishes the scan, so halts and waits are complete). Per unit, the first rule that holds:

Unplanned part (`ps.plan is None`):

1. not `ps.ready` → wait `part <K> waits: <ready_reason>`.
2. → action `plan`: `Call("wave-plan", f"flow autonomous {index.path} part {K}", models["plan"], *caps["wave-plan"])`.

Planned plan `p` (unit `u`):

1. not `p.tracking`: every feature merged or ➖ → wait `finished`; else halt `tracking branch plan/<slug> is missing`,
   next `both("wave-status " + u)`.
2. `p.readme.flow != "autonomous"` → halt `manual flow: the driver runs autonomous plans only`, next
   `both(f"wave-run {u} flow autonomous")`.
3. A wave is 🔄 (the first one, N): its wave file has `waiting_ids` →
   - the first waiting ID whose `needs` is not empty → halt `wave N waits for task mode <ID>, which needs <needs>`,
     next `both(f"wave-run {u} N task <ID>")` + ` in a session that has it, then ` + `both(f"wave-run {u} N")`;
   - else the first waiting ID with `(u, N, ID)` not in `task_runs` → action `task`:
     `Call("wave-run", f"{u} {N} task {ID}", models[<task complexity, default "medium">], *caps["task"])`;
   - else action `resume`: `Call("wave-run", f"{u} {N}", models["run"], *caps["wave-run"])`.
   Not waiting → halt `wave N is 🔄 (<cell>): another run holds it, or a run was interrupted`, next
   `wait for it, or release the lock (wave-plan/layout.md, "Running waves")`.
4. A wave is ❌ (the first, N) → halt with reason = its `last_stop` or `wave N ❌`; next = the part of `last_stop`
   after ` — next: `, else `both("wave-plan " + u)`.
5. The first ⬜ wave N: every `F<k>` of its `depends_merged` that is not `is_merged` → halt
   `wave N depends on F<k> merged; F<k> is <cell>, waiting for <waiting>`, next: for a 👀 feature
   `review F<k>, then ` + `both(f"wave-run {u} merge F<k>")`, else `both("wave-status " + u)`. None → action `wave`:
   `Call("wave-run", f"{u} {N}", models["run"], *caps["wave-run"])`.
6. No ⬜, 🔄 or ❌ wave → wait `finished`.

`after_call(action, result, snapshot, progressed, attempts)`, key `(action.unit, action.call.args)`:

- `stop` → halts with `reason = result.stop_line`, `next = result.next`: for a code in `TARGET_CODES`, one per unit
  whose `target_of` equals that of `action.unit`; otherwise one for `action.unit`.
- `limit`, `auth` → `[]` (the loop ends the run).
- `ok` and `progressed` → remove the key from `attempts`; `[]`.
- Otherwise `attempts[key] += 1`; at 2 → halt `no progress after 2 successful calls of <prompt>` (for `ok`) or
  `failed twice: <detail>` (for `failed`, `timeout`), next `both("wave-status " + unit)`; below 2 → `[]`.

`status_call`: `Call("wave-status", "" for an index start else the plan folder, models["status"],
*caps["wave-status"])`.

### Morning report (task F)

`render` returns Markdown, sections in this order, each always present (`none` when empty):

```
# Wave driver report · <finished YYYY-MM-DD HH:MM>

- Repository: `<repo>` · main branch: `<main>` · start: `<start>`
- Run: <started> – <finished> (<duration>) · ended: <end_reason>
- Calls: <n> (plan <a>, wave <b>, task <c>, resume <d>, status <e>) · failed: <f> · turns: <t> · cost: <x.xx> USD (total_cost_usd) · Claude minutes: <m.m>
- Options: <options joined with " · ">
- Log: `<log_path>`

## Integration targets
## Merged, not in <main>
## Ready for review
## Blocked and waiting
## Halts
## Open problems
## Status check
## Calls
## Next
## wave-status
```

- Duration: `<h> h <m> min`, or `<m> min` under an hour.
- Integration targets: per target with `exists`: ``- `integration/<n>` · worktree `<path>` · <ahead> commits not in
  `<main>` ``; a missing one: ``- `integration/<n>` · not created``.
- Merged: per plan, per feature of `merged_not_in_main`, `merged_block`, blocks separated by a blank line.
- Ready for review: per plan, per `👀 review` feature, `review_block`.
- Blocked and waiting: per plan, a feature ⚠️ → ``- `<folder>` F<k> <title> — ⚠️ I<n>: <essence>`` (the first
  `I\d+` of its cell, essence from `problems`; unknown → the cell); ⬜ or 🔄 → ``- `<folder>` F<k> <title> — <cell>,
  waiting for <waiting>``; then every wait as ``- `<unit>` — <reason>``.
- Halts: ``- `<unit>` — <reason>`` plus ` — next: <next>` when next is not empty.
- Open problems: per plan, every `open` entry: ``- `<folder>` <id> · <scope>: <essence> — <status>``.
- Status check: per plan with `check_lines`: ``- `<folder>`: <line>``.
- Calls: a table `| # | Time | Kind | Unit | Prompt | Model | Outcome | Exit | Turns | USD | Min | Denials | Stop or detail |`,
  one row per record (USD `0.00`, Min `0.0`; a `|` in a cell written `\|`; the last cell is the stop line, else the
  detail, else the warnings joined with `; `).
- Next: the numbered `next_commands`.
- wave-status: the status text as it is inside a four-backtick fence, or `not run`.

`brief_sections`: `header` = the lines before the first `## ` heading; each `## <name>` section's text, stripped,
under its name (`Essence`, `How to test`, `Worth a look`, …).

`merged_block` (layout.md, "Feature review", merged block); `<n>` and the worktree come from the plan's target in
`snapshot.targets`:

```
**F1 · <title>** · merged into `integration/<n>` `<merged hash>` · `<integration worktree>`
<Essence, else the title>
How to test:
<the "How to test" section as written>
Worth a look: <the section joined into one line>
Approved: auto — every task ✅ or ➖, check green, no open entry, tier gate clean, not under manual review
```

- No brief or no "How to test" → the two "How to test" lines become `How to test: not recorded — <done_when>`.
- "Worth a look" missing, empty or `nothing` → no such line.
- The brief header contains `approved by the user` → `Approved: by the user`.

`review_block`: first line ``**F1 · <title>** · `<branch>` · `<worktree>` `` from the brief header line
`Branch: <branch> · worktree: <path>` (backticks optional); without it the branch is the Features `Branch` cell, else
`feat/<slug>/<id>-<feature slug>`, and the worktree `<repo.parent>/<repo.name>.worktrees/<slug>-<id>`. Then the same
Essence, How to test and Worth a look lines, and last ``Merge: `/wave-run <folder> merge F1` · `$wave-run <folder>
merge F1` ``.

`next_commands` (in this order):

1. per target with `ahead > 0`: ``review `git diff <main>...integration/<n>`, then merge it in the main checkout:
   `git merge --no-ff integration/<n>` ``;
2. per `👀 review` feature: ``review `<branch>`, then `/wave-run <folder> merge F<k>` · `$wave-run <folder> merge F<k>` ``;
3. per halt with a next: ``<unit>: <next>``;
4. per plan with open entries: `` re-plan the open problems I<n>, …: `/wave-plan <folder>` · `$wave-plan <folder>` ``.

### Loop and CLI (task G)

```
python scripts/wave_driver.py <start> [options]
```

| Option | Default | Meaning |
|---|---|---|
| `<start>` | — | `plans/<date>-<topic>/index.md`, or a plan folder; relative to the repository root (an absolute path inside it is made relative; `\` becomes `/`; a trailing `/` is removed) |
| `--repo PATH` | current folder | the project repository (its top level is used) |
| `--main BRANCH` | `main`, else `master` | the main branch |
| `--plan-model`, `--run-model`, `--status-model`, `--low-model`, `--medium-model`, `--high-model` | `DEFAULT_MODELS` | models per role and per task tier |
| `--cap SKILL=TURNS:USD` (repeatable) | `DEFAULT_CAPS` | SKILL is `wave-plan`, `wave-run`, `task` or `wave-status` |
| `--max-calls N` | 60 | rail |
| `--max-failures N` | 3 | rail: failed calls in a row |
| `--deadline TIME` | none | `HH:MM` or `YYYY-MM-DD HH:MM`: no call starts after it |
| `--max-usd X` | none | rail on the sum of `total_cost_usd` |
| `--call-timeout-min N` | 120 | per call |
| `--permission-mode MODE` | `auto` | passed to `claude` |
| `--claude PATH` | `shutil.which("claude")` | the CLI |
| `--skill-prefix TEXT` | `""` | `wave-method:` for a plugin install |
| `--add-dir PATH` (repeatable) | none | passed as `--add-dir` (the plugin folder for a plugin install) |
| `--claude-arg ARG` (repeatable, write `--claude-arg=--setting-sources`) | none | extra arguments |
| `--out DIR` | `<repo.parent>/<repo.name>.wave-driver/<YYYY-MM-DD-HHMM>` | report, log and raw call output |
| `--no-status` | off | skip the final `wave-status` call |
| `--dry-run` | off | print the snapshot's next action and its command line; no lock, no call, no files |

Exit codes: 0 — ended because nothing is left to run; 1 — ended by a rail, a usage limit, an authentication error, a
guard violation, an interrupt or a driver error; 2 — bad arguments or setup (not a git repository, start not found,
`claude` not found or `claude --version` failing); 3 — another driver holds the lock.

`main`:

1. Parse arguments (`argparse`); errors → exit 2. `git = Git(Path(args.repo))`, `repo = git.toplevel()`, `main =
   resolve_main(git, args.main)`, start normalised; `read_snapshot` once (errors → message, exit 2). The claude prefix
   is `claude_prefix`, else `[args.claude or shutil.which("claude")]`; unless `--dry-run`, run `<prefix> --version`
   (exit not 0 or missing → exit 2).
2. `--dry-run`: `choose` on the snapshot with empty state; print `next: <kind> <unit> — <why>` and the command line
   (`subprocess.list2cmdline` on Windows, `shlex.join` elsewhere) or `next: nothing — <waits and halts>`; exit 0.
3. Out folder (created), `Log(out/"driver.log")`, `Lock(git.common_dir()/"wave-driver.lock").acquire()`;
   `LockHeld` → print `another driver runs: <holder> (lock file <path>; delete it only if no driver runs)`, exit 3.
4. Loop, with `halted = {}`, `attempts = {}`, `task_runs = set()`, `calls = []`, `counters`, `limits`:
   1. `reason = rail_reason(limits, counters, now)` → end with it (exit 1).
   2. `snap = read_snapshot(...)`; `choice = choose(snap, halted, task_runs, cfg)`; add `choice.halts` to `halted`
      (logged); keep `choice.waits` as the last waits. No action → end `nothing left to run` (exit 0).
   3. `before = guard_snapshot(repo, main)`; `heads_before = snap.heads`; log the call; `result = claude.run(call,
      settings, repo, out/"calls"/f"{n:02d}-{kind}.json")`; `counters.record(...)`; append a `CallRecord`.
   4. `guard_violations(before, guard_snapshot(...))` not empty → end `guard: <violations joined with "; ">` (exit 1).
   5. Outcome `limit` → end `usage limit: <detail or first 200 characters of the text>`; `auth` → end
      `authentication: …` (exit 1).
   6. `progressed = heads(git, main) != heads_before`; a `task` action with outcome `ok` adds `(unit, wave, task)` to
      `task_runs`; `after_call(...)` halts go into `halted` (logged).
   `KeyboardInterrupt` → end `interrupted` (exit 1); any other exception → end `driver error: <type>: <message>`
   (exit 1), with the traceback in the log.
5. Unless `--no-status` or the end was `usage limit`, `authentication` or `guard`: one `status_call`; its text (or
   `failed: <detail>`) is the status text; it is recorded as a call (not counted against the rails).
6. Always (`finally`): a fresh snapshot (on error: the last good one), `render`, write `out/report.md`, print
   `Report: <path>` and the "Next" lines, release the lock.

## Limits

- The driver never runs `wave-triage`, a re-plan, the merge form or the flow form, never runs git commands that
  write, and never deletes branches, worktrees or claims. It writes only its out folder and its lock file.
- A deadline stops new calls; it never cuts a running call (the call timeout does, and a cut wave stays 🔄 with its
  claim: the next driver halts that unit and the report names it).
- A guard violation ends the run after the call that caused it; the driver cannot undo it. The report names the refs.
- Units of one integration target run one after another anyway (the driver is sequential); the target claim of the
  skills stays the real lock.
- A task waiting for task mode with `Needs` is never run by the driver (headless sessions may lack the tool).
- Plans of other indexes and plans outside the start are not read.

## Acceptance tests

- A: `test_gitstate.py` — parsers on literal texts (README with `- Flow: autonomous · target: integration/t ·
  manual review: F2`, without Flow, with `- Flow: manual`; wave file with ``Depends on: `F1 merged` …`` over two lines,
  a Needs cell, `Waiting: task mode B, C — next: …` as the last Execution line, and one with a later line; problems
  with an open and a `fixed in …` entry; index Parts with `now` and `after part 1 merged`); a temp repository with
  `plan/t-p1` holding a README (two features: F1 `✅ merged` with a hash in `integration/t`, F2 `👀 review`), a brief
  `reviews/F2.md`, an index on `main` with two parts → `read_snapshot` gives part 1 planned with `tracking` true,
  part 2 `ready` true when F2 is ➖ and false with reason naming `F2` when it is `👀 review`; `merged_not_in_main ==
  ["F1"]`; `briefs` has F2; `targets["integration/t"].ahead` equals the commits made there; a plan-folder start of a
  folder that is on no branch raises `GitError`.
- B: `test_claude.py` — `command` exact list for a call with an add dir and an extra arg; `prompt` with prefix
  `wave-method:`; `parse_stop` on `Started: …\nStop wave-running: x — next: y` → (`wave-running`, line, `y`), on a
  stop line without `next`, and on a report without stop → `None`; `parse_output` on one JSON object and on two
  `result` lines (the last wins); `run` with `Settings(claude=[sys.executable, "-c", <code>])` covering `ok`, `stop`,
  `failed` (exit 1, `error_max_turns`), `limit` (429), `limit` by text `usage limit reached`, `auth`, warnings
  (no `Started:`, 2 denials, a closing question), `timeout` (a sleeping child, `timeout_s=1`, returns in under 15 s)
  and `raw_path` written.
- C: `test_rails.py` — a second `acquire` on the same path raises `LockHeld` naming the first pid; `release` of a lock
  whose file was replaced leaves the file; `parse_deadline("06:30", 05:00)` → same day, `("06:30", 07:00)` → next
  day, a full date, and `"tomorrow"` → `ValueError`; `rail_reason` for each of the four rails and `None`;
  `Counters.record` resets `failures_in_row` on `ok`; guard on a temp repository: a commit on `main`, a new
  `refs/remotes/origin/x`, a tracked edit in the checkout each give a violation; a commit on another branch gives
  none; `Log` writes a line with `✅` while echo goes to a cp1252-like stream without raising.
- D: `test_fake_claude.py` — `--version`; two steps consumed in order with the state file; a commit on a new branch
  from `main` with a `{{rev:main}}` placeholder resolved; a `refs` entry; a prompt that does not match → exit 1 with
  `error_during_execution`; an `args` mismatch → exit 1; the calls log has one line per call; `result` key absent for
  an `error_max_turns` step.
- E: `test_decide.py` — on hand-built `Snapshot` objects: each rule of `choose` (unplanned part ready / waiting; plan
  without tracking branch finished / missing; manual flow; 🔄 waiting with a task of `high` complexity → `task` call
  with model `opus` and caps `task`; the same after the task is in `task_runs` → `resume`; waiting task with Needs →
  halt; 🔄 not waiting → halt; ❌ with a stop line → halt with its next; ⬜ with an unmerged dependency 👀 → halt with
  the merge command; ⬜ → `wave` call `/wave-run <folder> <N>` args); halted units are skipped and a later unit's
  action is chosen; `after_call` for a target code halts both units of that target and not a unit of another
  target; no progress twice → halt; a failure then a success with progress → no halt and the key removed.
- F: `test_report.py` — `render` on a snapshot with one merged-not-in-main feature (brief with "Worth a look:
  nothing"), one `👀 review` feature (brief with `- Branch: feat/x/F2-b · worktree: /w/x-F2`), one ⚠️ feature with
  an open entry, one wait, one halt, two call records (one with a `|` in the detail) and a status text: every section
  heading present in order; the merged block's first line exact; no `Worth a look` line for `nothing`; the review
  block ends with the exact `Merge:` line; `next_commands` order; the calls table rows have 13 cells; a feature
  without a brief gets `How to test: not recorded — <done when>`; the duration `1 h 5 min`.
- G: `test_driver.py` with the fake claude, each scenario in a temp repository (`main` with an index of two parts,
  part 2 `after part 1 merged`; part 1 planned on `plan/t-p1`, autonomous, waves 1 and 2 ⬜, F1):
  1. chain: wave 1 → wave 2 (a first commit creates `integration/t` from `main`, a second one writes the README with
     F1 `✅ merged` and Merged = `{{rev:integration/t}}`) → plan part 2 →
     part 2 wave 1 answers `Stop red-after-merge: … — next: …` and marks it ❌ → status call; exit 0, five calls in
     that order with the models `sonnet, sonnet, opus, sonnet, haiku`, `report.md` has F1's merged block, the stop
     line under "Halts", `git diff main...integration/t` under "Next", and `main` unchanged;
  2. usage limit (exit 1, `api_error_status` 429) on the first call → exit 1, one call, no status call, ended
     `usage limit`;
  3. lock file present → exit 3, no call;
  4. the first call commits on `main` → exit 1, ended `guard`, the report names `refs/heads/main`;
  5. two successful calls without changes → unit halted `no progress`, then the status call; exit 0;
  6. `--dry-run` → prints `/wave-run plans/<…>/plan-1 1`, exit 0, the fake's calls log is empty, no out folder;
  7. `--deadline` one minute in the past (full date) → exit 1, ended `deadline`; no wave or plan call, only the
     status call (rails do not stop it), so the report's Calls table has one row;
  8. `--max-failures 2` with two `error_max_turns` answers → exit 1, ended `max-failures`;
  9. wave 1 🔄 with `Waiting: task mode B` and task B `high` → calls `/wave-run <folder> 1 task B` with
     `--model opus`, then `/wave-run <folder> 1`;
  and a test that `ast.parse(source, feature_version=(3, 9))` accepts every file of `scripts/wavedriver/` and
  `scripts/wave_driver.py`.
- H: `docs/wave-driver.md` has the sections of task H's prompt and every option of the CLI table; the release workflow
  runs `python -m unittest discover -s scripts/tests -v`.
