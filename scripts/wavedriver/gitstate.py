"""Read the overnight driver's plan state from Git."""

from __future__ import annotations

import re
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from io import StringIO
from pathlib import Path, PurePosixPath
from typing import Optional

SKILL_SCRIPTS = Path(__file__).resolve().parents[2] / "skills" / "wave-plan" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
import status_check


class GitError(RuntimeError):
    pass


class Git:
    def __init__(self, repo: Path) -> None:
        self.repo = repo

    def _execute(self, args: tuple[str, ...]) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(
                ["git", "-C", str(self.repo), *args],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
        except OSError as error:
            raise GitError(f"git {' '.join(args)}: {error}") from error

    def run(self, *args: str, check: bool = True) -> str:
        result = self._execute(args)
        if check and result.returncode != 0:
            raise GitError(f"git {' '.join(args)}: {result.stderr.rstrip()}")
        return result.stdout.rstrip("\n")

    def ok(self, *args: str) -> bool:
        return self._execute(args).returncode == 0

    def show(self, ref: str, path: str) -> Optional[str]:
        try:
            return self.run("show", f"{ref}:{path}")
        except GitError:
            return None

    def exists(self, ref: str) -> bool:
        return self.ok("rev-parse", "-q", "--verify", f"{ref}^{{commit}}")

    def is_ancestor(self, a: str, b: str) -> bool:
        return self.ok("merge-base", "--is-ancestor", a, b)

    def branches(self, pattern: str) -> list[str]:
        return self.run(
            "for-each-ref", "--format=%(refname:short)", f"refs/heads/{pattern}",
        ).splitlines()

    def ls(self, ref: str, folder: str) -> list[str]:
        tree = self.run("ls-tree", "--full-tree", "--name-only", "-z", ref, "--", f"{folder}/")
        return tree.rstrip("\0").split("\0") if tree else []

    def toplevel(self) -> Path:
        return Path(self.run("rev-parse", "--show-toplevel"))

    def common_dir(self) -> Path:
        return Path(self.run("rev-parse", "--path-format=absolute", "--git-common-dir"))


def resolve_main(git: Git, explicit: Optional[str] = None) -> str:
    for branch in (explicit, "main", "master"):
        if branch and git.exists(f"refs/heads/{branch}"):
            return branch
    raise GitError("main branch not found")


@dataclass
class Feature:
    id: str
    slug: str
    title: str
    done_when: str
    status: str
    cell: str
    waiting: str
    branch: str
    merged: str

    @property
    def is_merged(self) -> bool:
        return bool(re.search(r"✅\s+merged\b", self.cell))


@dataclass
class Wave:
    number: int
    file: str
    status: str
    cell: str


@dataclass
class Task:
    id: str
    slug: str
    feature: str
    wave: int
    complexity: str
    status: str
    cell: str


@dataclass
class Readme:
    slug: str
    flow: str
    target: Optional[str]
    manual_review: list[str]
    features: list[Feature]
    waves: list[Wave]
    tasks: list[Task]


def _flow_header(header: str) -> tuple[str, Optional[str], list[str]]:
    match = re.search(r"^- Flow: (.+)$", header, re.MULTILINE)
    if not match or match[1].startswith("manual"):
        return "manual", None, []
    flow, *fields = (field.strip().strip("`") for field in match[1].split("·"))
    target = None
    manual_review = []
    for field in fields:
        name, _, value = field.partition(":")
        if name == "target":
            target = value.strip().strip("`")
        if name == "manual review":
            manual_review = re.findall(r"F\d+", value)
    return flow, target, manual_review


def parse_readme(text: str) -> Readme:
    header = text.split("\n## ", 1)[0]
    slug_match = re.search(r"slug: `([^`]+)`", header)
    if not slug_match:
        raise ValueError("plan slug missing")
    slug = slug_match[1]
    parsed = status_check.tables(text.splitlines(), lambda *_: None)
    flow, target, manual_review = _flow_header(header)
    if flow == "autonomous":
        target = target or f"integration/{slug}"

    features = [
        Feature(row["ID"], row.get("Slug", "").strip("`"), row.get("Title", ""),
                row.get("Done when", ""), status_check.mark(row["Status"]), row["Status"],
                row.get("Waiting for", ""), row.get("Branch", "").strip("`"),
                row["Merged"].strip("`"))
        for _, row in parsed["Features"]
    ]
    waves = [
        Wave(int(row["Wave"]), row.get("File", "").strip("`"),
             status_check.mark(row["Status"]), row["Status"])
        for _, row in parsed["Waves"] if re.fullmatch(r"[0-9]+", row["Wave"])
    ]
    tasks = [
        Task(row["ID"], row.get("Slug", "").strip("`"), row.get("Feature", ""),
             int(row["Wave"]), row.get("Complexity", ""), status_check.mark(row["Status"]),
             row["Status"])
        for _, row in parsed["Tasks"]
        if re.fullmatch(r"[0-9]+", row.get("Wave", ""))
    ]
    return Readme(slug, flow, target, manual_review, features, waves, tasks)


@dataclass
class WaveFile:
    depends_merged: list[str]
    needs: dict[str, str]
    waiting_ids: list[str]
    last_stop: str


def _section(text: str, name: str) -> list[str]:
    lines = text.splitlines()
    try:
        start = lines.index(f"## {name}") + 1
    except ValueError:
        return []
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def _table(lines: list[str]) -> list[dict[str, str]]:
    start = next((i for i, line in enumerate(lines) if line.startswith("|")), len(lines))
    if start + 1 >= len(lines):
        return []
    header = status_check.cells(lines[start])
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        cells = status_check.cells(line)
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def parse_wave_file(text: str) -> WaveFile:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("Depends on:")), len(lines))
    paragraph = []
    for line in lines[start:]:
        if not line.strip():
            break
        paragraph.append(line)
    depends = re.findall(r"\b(F\d+) merged\b", "\n".join(paragraph).replace("`", ""))
    needs = {}
    for row in _table(_section(text, "Tasks")):
        cell = row.get("Needs", "")
        needs[row["ID"]] = "" if cell in ("—", "-") else cell

    execution = [line for line in _section(text, "Execution") if line.strip()]
    waiting_ids = []
    prefix = "Waiting: task mode "
    if execution and execution[-1].startswith(prefix):
        waiting = execution[-1].split(" — ", 1)[0][len(prefix):]
        waiting_ids = re.findall(r"\b[A-Z]{1,2}\b", waiting)
    last_stop = next((line for line in reversed(execution) if line.startswith("Stop ")), "")
    return WaveFile(depends, needs, waiting_ids, last_stop)


@dataclass
class Entry:
    id: str
    scope: str
    essence: str
    status: str
    open: bool
    features: list[str]


def parse_problems(text: str) -> list[Entry]:
    starts = list(re.finditer(r"^- \*\*\[(I\d+) · ([^\]]*)\]\s*(.*?)\*\*", text, re.MULTILINE))
    entries = []
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block = text[match.start():end]
        status = block.rpartition("status:")[2].strip() if "status:" in block else ""
        entry_id, scope, essence = match.groups()
        entries.append(Entry(entry_id, scope, essence, status, status.startswith(("open", "→")),
                             re.findall(r"feature (F\d+)", scope)))
    return entries


@dataclass
class Part:
    number: int
    slug: str
    plan_when: str
    after: list[int]


@dataclass
class Index:
    path: str
    folder: str
    topic: str
    target: str
    parts: list[Part]


def parse_index(text: str, path: str) -> Index:
    folder = PurePosixPath(path).parent
    topic = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", folder.name)
    flow, target, _ = _flow_header(text.split("\n## ", 1)[0])
    parts = []
    for row in _table(_section(text, "Parts")):
        plan_when = row["Plan when"]
        after = [] if plan_when == "now" else [int(n) for n in re.findall(r"\d+", plan_when)]
        parts.append(Part(int(row["Part"]), row["Plan slug"].strip("`"), plan_when, after))
    return Index(path, folder.as_posix(), topic, (target if flow == "autonomous" else None)
                 or f"integration/{topic}", parts)


@dataclass
class PlanState:
    folder: str
    source: str
    tracking: bool
    readme: Readme
    problems: list[Entry]
    wave_files: dict[int, WaveFile]
    merged_not_in_main: list[str]
    briefs: dict[str, str]
    check_lines: list[str]


@dataclass
class PartState:
    part: Part
    folder: str
    plan: Optional[PlanState]
    ready: bool
    ready_reason: str


@dataclass
class TargetState:
    name: str
    exists: bool
    ahead: int
    worktree: str


@dataclass
class Snapshot:
    repo: Path
    main: str
    index: Optional[Index]
    parts: list[PartState]
    plans: list[PlanState]
    targets: dict[str, TargetState]
    heads: dict[str, str]


def heads(git: Git, main: str) -> dict[str, str]:
    refs = git.run(
        "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads/plan",
        "refs/heads/integration", "refs/heads/feat", "refs/heads/task",
        "refs/wave-method/claims", f"refs/heads/{main}",
    )
    return dict(line.split(maxsplit=1) for line in refs.splitlines())


def _worktrees(git: Git) -> Path:
    repo = git.toplevel()
    return repo.parent / f"{repo.name}.worktrees"


def _plan_sources(git: Git, main: str, slug: Optional[str]):
    if slug is None:
        yield from git.branches("plan/*")
    elif git.exists(f"refs/heads/plan/{slug}"):
        yield f"plan/{slug}"
    yield main
    yield from git.branches("integration/*")


def read_plan(git: Git, folder: str, main: str, slug: Optional[str] = None) -> Optional[PlanState]:
    for source in _plan_sources(git, main, slug):
        text = git.show(source, f"{folder}/README.md")
        if text is None:
            continue
        readme = parse_readme(text)
        tracking = source == f"plan/{readme.slug}"
        if slug is None and source.startswith("plan/") and not tracking:
            continue
        break
    else:
        return None

    problems = parse_problems(git.show(source, f"{folder}/problems.md") or "")
    wave_files = {}
    for wave in readme.waves:
        if wave.status in ("⬜", "🔄", "❌"):
            wave_files[wave.number] = parse_wave_file(git.show(source, f"{folder}/{wave.file}") or "")

    merged_not_in_main = [
        feature.id for feature in readme.features
        if feature.is_merged and not (feature.merged and git.is_ancestor(feature.merged, main))
    ]
    wanted = set(merged_not_in_main)
    wanted.update(feature.id for feature in readme.features if feature.status == "👀")
    briefs = {}
    if wanted:
        for path in git.ls(source, f"{folder}/reviews"):
            match = re.fullmatch(r"(F\d+)(?:-.*)?\.md", PurePosixPath(path).name)
            if match and match[1] in wanted and match[1] not in briefs:
                brief = git.show(source, path)
                if brief is not None:
                    briefs[match[1]] = brief

    check_lines = []
    check_folder = _worktrees(git) / f"{readme.slug}-plan" / folder
    if check_folder.is_dir():
        buffer = StringIO()
        with redirect_stdout(buffer), redirect_stderr(buffer):
            status_check.check(check_folder)
        check_lines = buffer.getvalue().splitlines()

    return PlanState(folder, source, tracking, readme, problems, wave_files,
                     merged_not_in_main, briefs, check_lines)


def part_merged(git: Git, index: Index, number: int, main: str) -> tuple[bool, str]:
    part = next((part for part in index.parts if part.number == number), None)
    if part is None:
        return False, f"part {number} is not planned"
    target_exists = git.exists(f"refs/heads/{index.target}")
    tracking = f"plan/{part.slug}"
    sources = [tracking] if git.exists(f"refs/heads/{tracking}") else []
    sources.append(main)
    if target_exists:
        sources.append(index.target)
    path = f"{index.folder}/plan-{number}/README.md"
    for source in sources:
        text = git.show(source, path)
        if text is not None:
            break
    else:
        return False, f"part {number} is not planned"

    waiting = []
    for feature in parse_readme(text).features:
        if feature.status == "➖":
            continue
        if feature.is_merged and feature.merged:
            if git.is_ancestor(feature.merged, main):
                continue
            if target_exists and git.is_ancestor(feature.merged, index.target):
                continue
        waiting.append(f"{feature.id} {feature.cell} ({feature.waiting})")
    if waiting:
        return False, f"part {number} — {', '.join(waiting)}"
    return True, ""


def read_snapshot(git: Git, start: str, main: str) -> Snapshot:
    index = None
    parts = []
    plans = []
    if start.endswith("index.md"):
        text = git.show(main, start)
        if text is None:
            raise GitError(f"index {start} not found on {main}")
        index = parse_index(text, start)
        for part in index.parts:
            folder = f"{index.folder}/plan-{part.number}"
            plan = read_plan(git, folder, main, part.slug)
            ready, reason = True, ""
            for dependency in part.after:
                ready, reason = part_merged(git, index, dependency, main)
                if not ready:
                    break
            parts.append(PartState(part, folder, plan, ready, reason))
            if plan is not None:
                plans.append(plan)
    else:
        plan = read_plan(git, start, main)
        if plan is None:
            raise GitError(f"plan folder {start} not found on any branch")
        plans.append(plan)

    names = [plan.readme.target for plan in plans if plan.readme.target is not None]
    if index is not None:
        names.append(index.target)
    repo = git.toplevel()
    worktrees = repo.parent / f"{repo.name}.worktrees"
    targets = {}
    for name in dict.fromkeys(names):
        exists = git.exists(f"refs/heads/{name}")
        ahead = int(git.run("rev-list", "--count", f"{main}..{name}")) if exists else 0
        worktree = worktrees / ("integration-" + name[len("integration/"):])
        targets[name] = TargetState(name, exists, ahead, str(worktree))
    return Snapshot(repo, main, index, parts, plans, targets, heads(git, main))
