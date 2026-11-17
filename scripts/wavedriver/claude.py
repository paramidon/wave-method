"""Run a wave skill in Claude Code print mode."""

from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


DEFAULT_MODELS = {
    "plan": "opus", "run": "sonnet", "status": "haiku",
    "low": "haiku", "medium": "sonnet", "high": "opus",
}
DEFAULT_CAPS = {
    "wave-plan": (50, 4.0), "wave-run": (110, 3.0),
    "task": (110, 5.0), "wave-status": (60, 0.5),
}


@dataclass
class Call:
    skill: str
    args: str
    model: str
    max_turns: int
    max_usd: float


@dataclass
class Settings:
    claude: list[str]
    skill_prefix: str = ""
    permission_mode: str = "auto"
    add_dirs: list[str] = field(default_factory=list)
    extra_args: list[str] = field(default_factory=list)
    timeout_s: int = 7200


@dataclass
class Result:
    outcome: str
    exit_code: Optional[int]
    data: dict
    text: str
    stderr: str
    minutes: float
    cost: float
    turns: int
    denials: int
    stop_code: str = ""
    stop_line: str = ""
    next: str = ""
    detail: str = ""
    warnings: list[str] = field(default_factory=list)


def both(command: str) -> str:
    return f"`/{command}` · `${command}`"


def prompt(call: Call, settings: Settings) -> str:
    return f"/{settings.skill_prefix}{call.skill} {call.args}".rstrip()


def command(call: Call, settings: Settings) -> list[str]:
    args = settings.claude + [
        "-p", prompt(call, settings),
        "--output-format", "json",
        "--permission-mode", settings.permission_mode,
        "--model", call.model,
        "--max-turns", str(call.max_turns),
        "--max-budget-usd", f"{call.max_usd:g}",
    ]
    for directory in settings.add_dirs:
        args.extend(["--add-dir", directory])
    return args + settings.extra_args


def _json_dict(value: str) -> dict:
    try:
        data = json.loads(value)
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def parse_output(stdout: str) -> dict:
    data = _json_dict(stdout.strip())
    if data:
        return data
    for line in reversed(stdout.splitlines()):
        data = _json_dict(line)
        if data.get("type") == "result":
            return data
    return {}


def _report_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_stop(text: str) -> Optional[tuple[str, str, str]]:
    lines = _report_lines(text)
    if lines and lines[0].startswith("Started:"):
        lines = lines[1:]
    if not lines:
        return None
    line = lines[0]
    match = re.match(r"^Stop ([a-z][a-z-]*): ", line)
    if match is None:
        return None
    return match.group(1), line, line.partition(" — next: ")[2]


def classify(exit_code: Optional[int], data: dict, stderr: str) -> tuple[str, str]:
    subtype = data.get("subtype")
    if exit_code == 0 and not data.get("is_error") and subtype == "success" and "result" in data:
        return "ok", ""

    errors = data.get("errors") or []
    if not isinstance(errors, list):
        errors = [errors]
    errors_text = "; ".join(map(str, errors))
    messages = "\n".join((str(data.get("result") or ""), errors_text, stderr))
    status = data.get("api_error_status")
    detail = f"exit {exit_code}, {subtype or 'no subtype'}"
    if errors_text:
        detail += f": {errors_text}"
    elif stderr.strip():
        detail += f": {stderr.strip()}"

    if status in (429, 529) or re.search(
        r"usage limit|rate[ -]?limit|limit reached|hit your limit|overloaded|too many requests|quota",
        messages, re.IGNORECASE,
    ):
        return "limit", detail
    if status == 401 or re.search(
        r"not logged in|/login|invalid api key|authentication|unauthorized",
        messages, re.IGNORECASE,
    ):
        return "auth", detail
    return "failed", detail


def _signal_group(pid: int, sig: int) -> None:
    try:
        # start_new_session makes the PID the group ID even after the leader exits.
        os.killpg(pid, sig)
    except ProcessLookupError:
        pass


def _terminate(proc: subprocess.Popen) -> tuple[str, str]:
    if os.name == "nt":
        killed = subprocess.run(
            ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
            stdin=subprocess.DEVNULL, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        if killed.returncode != 0:
            proc.kill()
    else:
        _signal_group(proc.pid, signal.SIGTERM)
        try:
            output = proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            pass
        else:
            _signal_group(proc.pid, signal.SIGKILL)
            return output
        _signal_group(proc.pid, signal.SIGKILL)
    return proc.communicate()


def run(call: Call, settings: Settings, cwd: Path, raw_path: Optional[Path] = None) -> Result:
    started = time.monotonic()
    process_group = (
        {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
        if os.name == "nt" else {"start_new_session": True}
    )
    timed_out = False
    exit_code = None
    try:
        proc = subprocess.Popen(
            command(call, settings), cwd=cwd, env={**os.environ, "MSYS_NO_PATHCONV": "1"},
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", **process_group,
        )
    except OSError as exc:
        stdout, stderr = "", str(exc)
    else:
        with proc:
            try:
                stdout, stderr = proc.communicate(timeout=settings.timeout_s)
            except subprocess.TimeoutExpired:
                timed_out = True
                stdout, stderr = _terminate(proc)
            except KeyboardInterrupt:
                _terminate(proc)
                raise
        exit_code = proc.returncode

    minutes = (time.monotonic() - started) / 60
    if raw_path is not None:
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        separator = "\n" if stdout and not stdout.endswith("\n") else ""
        raw_path.write_text(f"{stdout}{separator}--- stderr ---\n{stderr}", encoding="utf-8")

    data = parse_output(stdout)
    text = data.get("result") or ""
    if not isinstance(text, str):
        text = ""
    denials = len(data.get("permission_denials") or [])
    if timed_out:
        outcome, detail = "timeout", f"timeout after {settings.timeout_s / 60:g} min"
    else:
        outcome, detail = classify(exit_code, data, stderr)

    result = Result(
        outcome, exit_code, data, text, stderr, minutes,
        data.get("total_cost_usd") or 0.0, data.get("num_turns") or 0, denials,
        detail=detail,
    )
    if outcome == "ok":
        stop = parse_stop(text)
        if stop is not None:
            result.outcome = "stop"
            result.stop_code, result.stop_line, result.next = stop

    lines = _report_lines(text)
    if lines:
        if not lines[0].startswith("Started:"):
            result.warnings.append("no Started: line")
        if denials:
            result.warnings.append(f"{denials} permission denials")
        if lines[-1].endswith("?"):
            result.warnings.append("ends with a question")
    return result
