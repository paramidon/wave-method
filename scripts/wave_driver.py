"""Run autonomous wave plans as fresh headless Claude sessions."""

from __future__ import annotations

import argparse
from datetime import datetime
import math
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import traceback
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wavedriver import gitstate, claude, rails, decide, report


def display(message):
    try:
        print(message)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "ascii"
        print(message.encode(encoding, "replace").decode(encoding))


def cap(value):
    try:
        skill, pair = value.split("=")
        turns, dollars = pair.split(":")
        turns, dollars = int(turns), float(dollars)
        if skill not in claude.DEFAULT_CAPS or turns <= 0 or not (0 < dollars < math.inf):
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError("expected a known SKILL=TURNS:USD with positive caps")
    return skill, (turns, dollars)


def arguments(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("start", help="repository-relative index or plan folder")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--main")
    for role, model in claude.DEFAULT_MODELS.items():
        parser.add_argument(f"--{role}-model", default=model)
    parser.add_argument("--cap", action="append", default=[], type=cap, metavar="SKILL=TURNS:USD")
    parser.add_argument("--max-calls", type=int, default=60)
    parser.add_argument("--max-failures", type=int, default=3)
    parser.add_argument("--deadline")
    parser.add_argument("--max-usd", type=float)
    parser.add_argument("--call-timeout-min", type=int, default=120)
    parser.add_argument("--permission-mode", default="auto")
    parser.add_argument("--claude")
    parser.add_argument("--skill-prefix", default="")
    parser.add_argument("--add-dir", action="append", default=[])
    parser.add_argument("--claude-arg", action="append", default=[])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--no-status", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def execute(call, kind, unit, settings, repo, main, out, log, calls):
    number = len(calls) + 1
    prompt = claude.prompt(call, settings)
    log.write(f"Call {number}: {prompt} (model {call.model})")
    before = rails.guard_snapshot(repo, main)
    started = datetime.now().strftime("%H:%M:%S")
    result = claude.run(call, settings, repo, out / "calls" / f"{number:02d}-{kind}.json")
    calls.append(report.CallRecord(
        number, started, kind, unit, prompt, call.model, result.outcome, result.exit_code,
        result.data.get("subtype", ""), result.turns, result.cost, result.minutes,
        result.denials, result.stop_line, result.detail, result.warnings,
    ))
    violations = rails.guard_violations(before, rails.guard_snapshot(repo, main))
    reason = ""
    if violations:
        reason = "guard: " + "; ".join(violations)
    elif result.outcome in ("limit", "auth"):
        label = "usage limit" if result.outcome == "limit" else "authentication"
        reason = f"{label}: {result.detail or result.text[:200]}"
    return result, reason


def run_locked(args, git, snap, start, cfg, settings, limits, out, started):
    repo, main = snap.repo, snap.main
    log = rails.Log(out / "driver.log")
    counters = rails.Counters()
    halted, attempts, task_runs = {}, {}, set()
    calls, waits = [], []
    reason, status_text = "", None

    def halt(items):
        for item in items:
            halted[item.unit] = item
            log.write(f"Halt {item.unit}: {item.reason}")

    try:
        try:
            while True:
                reason = rails.rail_reason(limits, counters, datetime.now())
                if reason:
                    break
                snap = gitstate.read_snapshot(git, start, main)
                choice = decide.choose(snap, halted, task_runs, cfg)
                halt(choice.halts)
                waits = choice.waits
                action = choice.action
                if action is None:
                    reason = "nothing left to run"
                    break
                result, reason = execute(action.call, action.kind, action.unit, settings,
                                         repo, main, out, log, calls)
                counters.record(result.outcome, result.cost, result.turns, result.minutes)
                if reason:
                    break
                progressed = gitstate.heads(git, main) != snap.heads
                if action.kind == "task" and result.outcome == "ok":
                    task_runs.add((action.unit, action.wave, action.task))
                halt(decide.after_call(action, result, snap, progressed, attempts))
        except KeyboardInterrupt:
            reason = "interrupted"
        except Exception as exc:
            reason = f"driver error: {type(exc).__name__}: {exc}"
            log.write(traceback.format_exc())

        if not args.no_status and not reason.startswith(("guard:", "usage limit:", "authentication:")):
            result, status_reason = execute(decide.status_call(snap, cfg), "status", start,
                                            settings, repo, main, out, log, calls)
            status_text = result.text if result.outcome in ("ok", "stop") else f"failed: {result.detail}"
            reason = status_reason or reason
    except KeyboardInterrupt:
        reason = "interrupted"
    except Exception as exc:
        reason = f"driver error: {type(exc).__name__}: {exc}"
        log.write(traceback.format_exc())
    finally:
        try:
            snap = gitstate.read_snapshot(git, start, main)
        except Exception:
            log.write(traceback.format_exc())
        options = [f"{key.replace('_', '-')}: {value}" for key, value in vars(args).items()
                   if value is not None and key not in ("start", "repo", "out")]
        info = report.RunInfo(started, datetime.now(), str(repo), start, main, reason, options,
                              str(out), str(log.path))
        halts = list(halted.values())
        (out / "report.md").write_text(report.render(info, snap, calls, halts, waits, status_text),
                                       encoding="utf-8")
        log.write(f"Ended: {reason}")
        display(f"Report: {out / 'report.md'}")
        for number, command in enumerate(report.next_commands(snap, halts), 1):
            display(f"{number}. {command}")
    return 0 if reason == "nothing left to run" else 1


def main(argv: Optional[list[str]] = None, claude_prefix: Optional[list[str]] = None) -> int:
    args = arguments(argv)
    started = datetime.now()
    try:
        if (args.max_calls < 0 or args.max_failures < 0 or args.call_timeout_min <= 0
                or (args.max_usd is not None and not (0 <= args.max_usd < math.inf))):
            raise ValueError("invalid rail or timeout value")
        deadline = rails.parse_deadline(args.deadline, started) if args.deadline else None
        limits = rails.Limits(args.max_calls, args.max_failures, deadline, args.max_usd)
        git = gitstate.Git(Path(args.repo))
        repo = git.toplevel()
        git = gitstate.Git(repo)
        main_branch = gitstate.resolve_main(git, args.main)
        path = Path(args.start.replace("\\", "/"))
        start = (repo / path).resolve().relative_to(repo.resolve()).as_posix()
        snap = gitstate.read_snapshot(git, start, main_branch)
        prefix = claude_prefix or [args.claude or shutil.which("claude") or "claude"]
        settings = claude.Settings(prefix, args.skill_prefix, args.permission_mode, args.add_dir,
                                   args.claude_arg, args.call_timeout_min * 60)
        cfg = decide.DecideConfig()
        cfg.models.update({role: getattr(args, f"{role}_model") for role in cfg.models})
        cfg.caps.update(args.cap)
        if args.dry_run:
            choice = decide.choose(snap, {}, set(), cfg)
            if choice.action:
                action = choice.action
                display(f"next: {action.kind} {action.unit} — {action.why}")
                join = subprocess.list2cmdline if os.name == "nt" else shlex.join
                display(join(claude.command(action.call, settings)))
            else:
                display("next: nothing — " + "; ".join(
                    f"{item.unit}: {item.reason}" for item in choice.waits + choice.halts))
            return 0
        subprocess.run([*prefix, "--version"], cwd=repo, capture_output=True, check=True,
                       text=True, encoding="utf-8", errors="replace")
        out = args.out or repo.parent / f"{repo.name}.wave-driver" / started.strftime("%Y-%m-%d-%H%M")
        out.mkdir(parents=True, exist_ok=True)
        lock = rails.Lock(git.common_dir() / "wave-driver.lock")
        lock.acquire()
    except rails.LockHeld as exc:
        display(f"another driver runs: {exc.holder} (lock file {lock.path}; delete it only if no driver runs)")
        return 3
    except (OSError, ValueError, gitstate.GitError, subprocess.CalledProcessError) as exc:
        print(f"Setup error: {exc}", file=sys.stderr)
        return 2

    try:
        return run_locked(args, git, snap, start, cfg, settings, limits, out, started)
    except (KeyboardInterrupt, Exception) as exc:
        print(f"Driver error: {exc}", file=sys.stderr)
        return 1
    finally:
        lock.release()


if __name__ == "__main__":
    sys.exit(main())
