"""Render the overnight driver's morning report."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from . import gitstate


@dataclass
class CallRecord:
    number: int
    started: str
    kind: str
    unit: str
    prompt: str
    model: str
    outcome: str
    exit_code: Optional[int]
    subtype: str
    turns: int
    cost: float
    minutes: float
    denials: int
    stop_line: str = ""
    detail: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class RunInfo:
    started: datetime
    finished: datetime
    repo: str
    start: str
    main: str
    end_reason: str
    options: list[str]
    out_dir: str
    log_path: str


def brief_sections(text: str) -> dict[str, str]:
    parts = re.split(r"^## ([^\n]+)$", text, flags=re.MULTILINE)
    sections = {"header": parts[0].strip()}
    sections.update(
        (name.strip(), body.strip()) for name, body in zip(parts[1::2], parts[2::2])
    )
    return sections


def _feature_summary(feature: gitstate.Feature, sections: dict[str, str]) -> list[str]:
    lines = [sections.get("Essence") or feature.title]
    how = sections.get("How to test")
    if how:
        lines.extend(("How to test:", how))
    else:
        lines.append(f"How to test: not recorded — {feature.done_when}")
    worth = " ".join(sections.get("Worth a look", "").splitlines())
    if worth and worth.casefold() != "nothing":
        lines.append(f"Worth a look: {worth}")
    return lines


def merged_block(
    snapshot: gitstate.Snapshot, plan: gitstate.PlanState, feature: gitstate.Feature,
    brief: Optional[str],
) -> str:
    sections = brief_sections(brief or "")
    target = snapshot.targets.get(plan.readme.target)
    destination = target.name if target else (plan.readme.target or snapshot.main)
    heading = f"**{feature.id} · {feature.title}** · merged into `{destination}` `{feature.merged}`"
    if target:
        heading += f" · `{target.worktree}`"
    approval = (
        "by the user" if "approved by the user" in sections["header"].casefold()
        else "auto — every task ✅ or ➖, check green, no open entry, tier gate clean, scope clean, not under manual review"
    )
    return "\n".join([heading, *_feature_summary(feature, sections), f"Approved: {approval}"])


def _review_location(
    snapshot: gitstate.Snapshot, plan: gitstate.PlanState, feature: gitstate.Feature,
    header: str,
) -> tuple[str, str]:
    match = re.search(r"^(?:- )?Branch:\s*(.+?)\s+·\s+worktree:\s*(.+)$", header, re.MULTILINE)
    if match:
        return match[1].strip().strip("`"), match[2].strip().strip("`")
    slug = plan.readme.slug
    branch = feature.branch if feature.branch not in ("", "—", "-") else (
        f"feat/{slug}/{feature.id}-{feature.slug}"
    )
    worktree = snapshot.repo.parent / f"{snapshot.repo.name}.worktrees" / f"{slug}-{feature.id}"
    return branch, worktree.as_posix()


def _both(command: str) -> str:
    return f"`/{command}` · `${command}`"


def review_block(
    snapshot: gitstate.Snapshot, plan: gitstate.PlanState, feature: gitstate.Feature,
    brief: Optional[str],
) -> str:
    sections = brief_sections(brief or "")
    branch, worktree = _review_location(snapshot, plan, feature, sections["header"])
    heading = f"**{feature.id} · {feature.title}** · `{branch}` · `{worktree}`"
    command = _both(f"wave-run {plan.folder} merge {feature.id}")
    return "\n".join([heading, *_feature_summary(feature, sections), f"Merge: {command}"])


def next_commands(snapshot: gitstate.Snapshot, halts: list) -> list[str]:
    commands = [
        f"review `git diff {snapshot.main}...{target.name}`, then merge it in the main checkout: "
        f"`git merge --no-ff {target.name}`"
        for target in snapshot.targets.values() if target.ahead > 0
    ]
    for plan in snapshot.plans:
        for feature in plan.readme.features:
            if feature.status == "👀":
                header = brief_sections(plan.briefs.get(feature.id, ""))["header"]
                branch, _ = _review_location(snapshot, plan, feature, header)
                command = _both(f"wave-run {plan.folder} merge {feature.id}")
                commands.append(f"review `{branch}`, then {command}")
    commands.extend(f"{halt.unit}: {halt.next}" for halt in halts if halt.next)
    for plan in snapshot.plans:
        entries = ", ".join(entry.id for entry in plan.problems if entry.open)
        if entries:
            commands.append(f"re-plan the open problems {entries}: {_both(f'wave-plan {plan.folder}')}")
    return commands


def _blocked_and_waiting(snapshot: gitstate.Snapshot, waits: list) -> list[str]:
    lines = []
    for plan in snapshot.plans:
        problems = {entry.id: entry.essence for entry in plan.problems}
        for feature in plan.readme.features:
            prefix = f"- `{plan.folder}` {feature.id} {feature.title} — "
            if feature.status in ("⬜", "🔄"):
                lines.append(f"{prefix}{feature.cell}, waiting for {feature.waiting}")
            elif feature.status == "⚠️":
                issue = re.search(r"I\d+", feature.cell)
                if issue and issue[0] in problems:
                    lines.append(f"{prefix}⚠️ {issue[0]}: {problems[issue[0]]}")
                else:
                    lines.append(prefix + feature.cell)
    lines.extend(f"- `{wait.unit}` — {wait.reason}" for wait in waits)
    return lines


def _call_table(calls: list[CallRecord]) -> list[str]:
    if not calls:
        return []
    headings = [
        "#", "Time", "Kind", "Unit", "Prompt", "Model", "Outcome", "Exit",
        "Turns", "USD", "Min", "Denials", "Stop or detail",
    ]
    rows = [headings, ["---"] * len(headings)]
    for call in calls:
        rows.append([
            call.number, call.started, call.kind, call.unit, call.prompt, call.model,
            call.outcome, "" if call.exit_code is None else call.exit_code,
            call.turns, f"{call.cost:.2f}", f"{call.minutes:.1f}", call.denials,
            call.stop_line or call.detail or "; ".join(call.warnings),
        ])
    return [
        "| " + " | ".join(" ".join(str(cell).splitlines()).replace("|", r"\|") for cell in row) + " |"
        for row in rows
    ]


def _run_header(run: RunInfo, calls: list[CallRecord]) -> str:
    started = run.started.strftime("%Y-%m-%d %H:%M")
    finished = run.finished.strftime("%Y-%m-%d %H:%M")
    hours, minutes = divmod(int((run.finished - run.started).total_seconds() // 60), 60)
    duration = f"{hours} h {minutes} min" if hours else f"{minutes} min"
    counts = Counter(call.kind for call in calls)
    kinds = ", ".join(f"{kind} {counts[kind]}" for kind in ("plan", "wave", "task", "resume", "status"))
    failed = sum(call.outcome in ("failed", "timeout", "limit", "auth") for call in calls)
    return "\n".join([
        f"# Wave driver report · {finished}",
        "",
        f"- Repository: `{run.repo}` · main branch: `{run.main}` · start: `{run.start}`",
        f"- Run: {started} – {finished} ({duration}) · ended: {run.end_reason}",
        f"- Calls: {len(calls)} ({kinds}) · failed: {failed} · turns: {sum(c.turns for c in calls)}"
        f" · cost: {sum(c.cost for c in calls):.2f} USD (total_cost_usd)"
        f" · Claude minutes: {sum(c.minutes for c in calls):.1f}",
        f"- Options: {' · '.join(run.options)}",
        f"- Log: `{run.log_path}`",
    ])


def render(
    run: RunInfo, snapshot: gitstate.Snapshot, calls: list[CallRecord], halts: list,
    waits: list, status_text: Optional[str],
) -> str:
    targets = [
        f"- `{target.name}` · worktree `{target.worktree}` · {target.ahead} commits not in `{snapshot.main}`"
        if target.exists else f"- `{target.name}` · not created"
        for target in snapshot.targets.values()
    ]
    merged = []
    review = []
    for plan in snapshot.plans:
        for feature in plan.readme.features:
            brief = plan.briefs.get(feature.id)
            if feature.id in plan.merged_not_in_main:
                merged.append(merged_block(snapshot, plan, feature, brief))
            if feature.status == "👀":
                review.append(review_block(snapshot, plan, feature, brief))
    halt_lines = [
        f"- `{halt.unit}` — {halt.reason}" + (f" — next: {halt.next}" if halt.next else "")
        for halt in halts
    ]
    problems = [
        f"- `{plan.folder}` {entry.id} · {entry.scope}: {entry.essence} — {entry.status}"
        for plan in snapshot.plans for entry in plan.problems if entry.open
    ]
    checks = [
        f"- `{plan.folder}`: {line}" for plan in snapshot.plans for line in plan.check_lines
    ]
    commands = [
        f"{number}. {command}" for number, command in enumerate(next_commands(snapshot, halts), 1)
    ]
    status = "not run"
    if status_text is not None:
        separator = "" if status_text.endswith("\n") else "\n"
        status = "````\n" + status_text + separator + "````"
    sections = [
        ("Integration targets", "\n".join(targets)),
        (f"Merged, not in {snapshot.main}", "\n\n".join(merged)),
        ("Ready for review", "\n\n".join(review)),
        ("Blocked and waiting", "\n".join(_blocked_and_waiting(snapshot, waits))),
        ("Halts", "\n".join(halt_lines)),
        ("Open problems", "\n".join(problems)),
        ("Status check", "\n".join(checks)),
        ("Calls", "\n".join(_call_table(calls))),
        ("Next", "\n".join(commands)),
        ("wave-status", status),
    ]
    return "\n\n".join([
        _run_header(run, calls),
        *(f"## {heading}\n\n{body or 'none'}" for heading, body in sections),
    ]) + "\n"
