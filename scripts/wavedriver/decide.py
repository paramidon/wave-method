"""Choose driver actions and translate call outcomes into unit halts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from wavedriver import claude, gitstate

TARGET_CODES = {"target-unsafe", "target-conflict", "target-unmerged"}


@dataclass
class Halt:
    unit: str
    reason: str
    next: str = ""


@dataclass
class Action:
    kind: str
    unit: str
    call: claude.Call
    why: str
    wave: int = 0
    task: str = ""


@dataclass
class Choice:
    action: Optional[Action]
    halts: list[Halt]
    waits: list[Halt]


@dataclass
class DecideConfig:
    models: dict = field(default_factory=lambda: dict(claude.DEFAULT_MODELS))
    caps: dict = field(default_factory=lambda: dict(claude.DEFAULT_CAPS))


def units(snapshot: gitstate.Snapshot) -> list[str]:
    if snapshot.index is not None:
        return [part.folder for part in snapshot.parts]
    return [snapshot.plans[0].folder]


def target_of(snapshot: gitstate.Snapshot, unit: str) -> str:
    for plan in snapshot.plans:
        if plan.folder == unit:
            return plan.readme.target or ""
    return snapshot.index.target if snapshot.index is not None else ""


def _running(plan: gitstate.PlanState, wave: gitstate.Wave, task_runs: set,
             cfg: DecideConfig, choice: Choice) -> Optional[Action]:
    unit = plan.folder
    number = wave.number
    args = f"{unit} {number}"
    wave_file = plan.wave_files.get(number)
    if wave_file is None or not wave_file.waiting_ids:
        choice.halts.append(Halt(
            unit, f"wave {number} is 🔄 ({wave.cell}): another run holds it, or a run was interrupted",
            'wait for it, or release the lock (wave-plan/layout.md, "Running waves")',
        ))
        return None

    for task_id in wave_file.waiting_ids:
        needs = wave_file.needs.get(task_id, "")
        if needs:
            choice.halts.append(Halt(
                unit, f"wave {number} waits for task mode {task_id}, which needs {needs}",
                claude.both(f"wave-run {args} task {task_id}") + " in a session that has it, then "
                + claude.both(f"wave-run {args}"),
            ))
            return None

    for task_id in wave_file.waiting_ids:
        if (unit, number, task_id) not in task_runs:
            tier = next((task.complexity for task in plan.readme.tasks if task.id == task_id), "medium")
            call = claude.Call("wave-run", f"{args} task {task_id}",
                               cfg.models.get(tier, cfg.models["medium"]), *cfg.caps["task"])
            return Action("task", unit, call, f"wave {number} waits for task mode {task_id}", number, task_id)

    call = claude.Call("wave-run", args, cfg.models["run"], *cfg.caps["wave-run"])
    return Action("resume", unit, call, f"wave {number} is ready to resume", number)


def _planned(plan: gitstate.PlanState, task_runs: set, cfg: DecideConfig,
             choice: Choice) -> Optional[Action]:
    unit = plan.folder
    readme = plan.readme
    status_next = claude.both(f"wave-status {unit}")
    if not plan.tracking:
        if all(feature.is_merged or feature.status == "➖" for feature in readme.features):
            choice.waits.append(Halt(unit, "finished"))
        else:
            choice.halts.append(Halt(unit, f"tracking branch plan/{readme.slug} is missing", status_next))
        return None
    if readme.flow != "autonomous":
        choice.halts.append(Halt(unit, "manual flow: the driver runs autonomous plans only",
                                 claude.both(f"wave-run {unit} flow autonomous")))
        return None

    for wave in readme.waves:
        if wave.status == "🔄":
            return _running(plan, wave, task_runs, cfg, choice)

    for wave in readme.waves:
        if wave.status == "❌":
            wave_file = plan.wave_files.get(wave.number)
            stop = wave_file.last_stop if wave_file else ""
            next_command = stop.partition(" — next: ")[2] or claude.both(f"wave-plan {unit}")
            choice.halts.append(Halt(unit, stop or f"wave {wave.number} ❌", next_command))
            return None

    wave = next((wave for wave in readme.waves if wave.status == "⬜"), None)
    if wave is None:
        choice.waits.append(Halt(unit, "finished"))
        return None

    wave_file = plan.wave_files.get(wave.number)
    features = {feature.id: feature for feature in readme.features}
    for feature_id in wave_file.depends_merged if wave_file else []:
        feature = features.get(feature_id)
        if feature is not None and feature.is_merged:
            continue
        cell = feature.cell if feature is not None else "missing"
        waiting = feature.waiting if feature is not None else ""
        next_command = status_next
        if feature is not None and feature.status == "👀":
            next_command = f"review {feature_id}, then " + claude.both(f"wave-run {unit} merge {feature_id}")
        choice.halts.append(Halt(
            unit, f"wave {wave.number} depends on {feature_id} merged; {feature_id} is {cell}, waiting for {waiting}",
            next_command,
        ))

    if any(halt.unit == unit for halt in choice.halts):
        return None
    call = claude.Call("wave-run", f"{unit} {wave.number}", cfg.models["run"], *cfg.caps["wave-run"])
    return Action("wave", unit, call, f"wave {wave.number} is ready", wave.number)


def choose(snapshot: gitstate.Snapshot, halted: dict[str, Halt], task_runs: set,
           cfg: DecideConfig) -> Choice:
    choice = Choice(None, [], [])
    if snapshot.index is None:
        plan = snapshot.plans[0]
        if plan.folder not in halted:
            choice.action = _planned(plan, task_runs, cfg, choice)
        return choice

    for part in snapshot.parts:
        if part.folder in halted:
            continue
        number = part.part.number
        if part.plan is not None:
            action = _planned(part.plan, task_runs, cfg, choice)
        elif part.ready:
            args = f"flow autonomous {snapshot.index.path} part {number}"
            call = claude.Call("wave-plan", args, cfg.models["plan"], *cfg.caps["wave-plan"])
            action = Action("plan", part.folder, call, f"part {number} is ready to plan")
        else:
            choice.waits.append(Halt(part.folder, f"part {number} waits: {part.ready_reason}"))
            continue
        if choice.action is None:
            choice.action = action
    return choice


def after_call(action: Action, result: claude.Result, snapshot: gitstate.Snapshot,
               progressed: bool, attempts: dict) -> list[Halt]:
    unit = action.unit
    if result.outcome == "stop":
        affected = [unit]
        if result.stop_code in TARGET_CODES:
            target = target_of(snapshot, unit)
            affected = [candidate for candidate in units(snapshot) if target_of(snapshot, candidate) == target]
        return [Halt(candidate, result.stop_line, result.next) for candidate in affected]
    if result.outcome in {"limit", "auth"}:
        return []

    key = (unit, action.call.args)
    if result.outcome == "ok" and progressed:
        attempts.pop(key, None)
        return []
    attempts[key] = attempts.get(key, 0) + 1
    if attempts[key] < 2:
        return []
    if result.outcome == "ok":
        command = claude.both(f"{action.call.skill} {action.call.args}".rstrip())
        reason = f"no progress after 2 successful calls of {command}"
    else:
        reason = f"failed twice: {result.detail}"
    return [Halt(unit, reason, claude.both(f"wave-status {unit}"))]


def status_call(snapshot: gitstate.Snapshot, cfg: DecideConfig) -> claude.Call:
    args = "" if snapshot.index is not None else snapshot.plans[0].folder
    return claude.Call("wave-status", args, cfg.models["status"], *cfg.caps["wave-status"])
