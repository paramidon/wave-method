"""Run limits, repository guards, and ownership of the driver lock."""

from __future__ import annotations

import os
import re
import secrets
import socket
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class LockHeld(Exception):
    def __init__(self, holder: str) -> None:
        super().__init__(holder)
        self.holder = holder


class Lock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._token: Optional[str] = None

    def acquire(self) -> str:
        token = secrets.token_hex(4)
        started = datetime.now().strftime("%Y-%m-%d %H:%M")
        holder = f"pid {os.getpid()} host {socket.gethostname()} started {started} token {token}"
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                existing = self.path.read_text(encoding="utf-8", errors="replace").rstrip("\n")
            except FileNotFoundError:
                existing = ""
            raise LockHeld(existing) from None

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(holder + "\n")
        except OSError:
            self.path.unlink(missing_ok=True)
            raise
        self._token = token
        return holder

    def release(self) -> None:
        if self._token is None:
            return
        try:
            holder = self.path.read_text(encoding="utf-8", errors="replace").rstrip("\n")
            if holder.endswith(f" token {self._token}"):
                self.path.unlink()
        except FileNotFoundError:
            pass
        self._token = None


class Log:
    def __init__(self, path: Path, echo: bool = True) -> None:
        self.path = path
        self.echo = echo

    def write(self, message: str) -> None:
        line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {message}"
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")
        if self.echo:
            try:
                print(line)
            except UnicodeEncodeError:
                print(line.encode("ascii", "replace").decode("ascii"))


def parse_deadline(text: str, now: datetime) -> datetime:
    if re.fullmatch(r"[0-9]{2}:[0-9]{2}", text):
        clock = datetime.strptime(text, "%H:%M").time()
        deadline = datetime.combine(now.date(), clock, tzinfo=now.tzinfo)
        if deadline <= now:
            deadline += timedelta(days=1)
        return deadline
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", text):
        return datetime.strptime(text, "%Y-%m-%d %H:%M").replace(tzinfo=now.tzinfo)
    raise ValueError(f"invalid deadline {text!r}; use HH:MM or YYYY-MM-DD HH:MM")


@dataclass
class Limits:
    max_calls: int = 60
    max_failures: int = 3
    deadline: Optional[datetime] = None
    max_usd: Optional[float] = None


@dataclass
class Counters:
    calls: int = 0
    failures: int = 0
    failures_in_row: int = 0
    cost: float = 0.0
    turns: int = 0
    minutes: float = 0.0

    def record(self, outcome: str, cost: float, turns: int, minutes: float) -> None:
        self.calls += 1
        self.cost += cost
        self.turns += turns
        self.minutes += minutes
        if outcome in ("ok", "stop"):
            self.failures_in_row = 0
        elif outcome in ("failed", "timeout", "limit", "auth"):
            self.failures += 1
            self.failures_in_row += 1


def rail_reason(limits: Limits, counters: Counters, now: datetime) -> Optional[str]:
    if counters.calls >= limits.max_calls:
        return f"max-calls: {counters.calls} calls made"
    if counters.failures_in_row >= limits.max_failures:
        return f"max-failures: {counters.failures_in_row} failed calls in a row"
    if limits.deadline is not None and now >= limits.deadline:
        return f"deadline: {limits.deadline:%Y-%m-%d %H:%M} reached"
    if limits.max_usd is not None and counters.cost >= limits.max_usd:
        return f"max-usd: {counters.cost:.2f} USD spent"
    return None


def _git(repo: Path, *args: str, allowed_statuses: tuple[int, ...] = (0,)) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "--no-optional-locks", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode not in allowed_statuses:
        raise RuntimeError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout.rstrip("\n")


def guard_snapshot(repo: Path, main: str) -> dict[str, str]:
    main_ref = f"refs/heads/{main}"
    refs = _git(repo, "for-each-ref", "--format=%(refname) %(objectname)", main_ref, "refs/remotes")
    snapshot = {}
    for line in refs.splitlines():
        ref, sha = line.split()
        if ref == main_ref or ref.startswith("refs/remotes/"):
            snapshot[ref] = sha

    head = _git(repo, "symbolic-ref", "-q", "HEAD", allowed_statuses=(0, 1))
    if not head:
        head = "detached " + _git(repo, "rev-parse", "--verify", "HEAD")
    snapshot["checkout:HEAD"] = head
    snapshot["checkout:status"] = _git(repo, "status", "--porcelain", "--untracked-files=no")
    return snapshot


def guard_violations(before: dict[str, str], after: dict[str, str]) -> list[str]:
    violations = []
    for key in sorted(before.keys() | after.keys()):
        if key not in before:
            violations.append(f"{key} added")
        elif key not in after:
            violations.append(f"{key} removed")
        elif before[key] != after[key]:
            violations.append(f"{key} changed: {before[key]} -> {after[key]}")
    return violations
