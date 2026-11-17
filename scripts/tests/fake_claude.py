"""Play scripted Claude CLI responses against a test repository."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time


def git(*args, check=True, env=None, stdin=None):
    completed = subprocess.run(
        ["git", *args], check=check, capture_output=True, env=env, stdin=stdin,
        text=True, encoding="utf-8", errors="replace",
    )
    return completed.stdout.strip()


def expand_revisions(text):
    return re.sub(r"\{\{rev:([^{}]+)\}\}", lambda match: git("rev-parse", "--short", match[1]), text)


def commit(spec):
    branch = spec["branch"]
    parent = git("rev-parse", "-q", "--verify", branch, check=False)
    if not parent and "base" in spec:
        parent = git("rev-parse", "--verify", spec["base"])

    with tempfile.TemporaryDirectory() as directory:
        index_env = {**os.environ, "GIT_INDEX_FILE": str(Path(directory) / "index")}
        if parent:
            git("read-tree", parent, env=index_env)
        for path, contents in spec["files"].items():
            with tempfile.TemporaryFile() as source:
                source.write(expand_revisions(contents).encode("utf-8"))
                source.seek(0)
                blob = git("hash-object", "-w", "--stdin", stdin=source)
            git("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=index_env)
        tree = git("write-tree", env=index_env)

    identity = {
        **os.environ,
        "GIT_AUTHOR_NAME": "fake",
        "GIT_AUTHOR_EMAIL": "fake@example.com",
        "GIT_COMMITTER_NAME": "fake",
        "GIT_COMMITTER_EMAIL": "fake@example.com",
    }
    parents = ["-p", parent] if parent else []
    revision = git("commit-tree", tree, *parents, "-m", spec["message"], env=identity)
    git("update-ref", f"refs/heads/{branch}", revision)


def argument(argv, flag):
    for index, value in enumerate(argv[:-1]):
        if value == flag:
            return argv[index + 1]
    return None


def fail(reason):
    print(json.dumps({
        "type": "result",
        "subtype": "error_during_execution",
        "is_error": True,
        "errors": [f"fake: {reason}"],
    }))
    return 1


def main(argv):
    if argv == ["--version"]:
        print("0.0.0 (fake claude)")
        return 0

    scenario = Path(os.environ["FAKE_CLAUDE_SCENARIO"])
    with Path(str(scenario) + ".calls").open("a", encoding="utf-8") as calls:
        calls.write(json.dumps({"argv": argv, "cwd": os.getcwd()}) + "\n")

    state = Path(str(scenario) + ".state")
    used = int(state.read_text(encoding="utf-8")) if state.exists() else 0
    steps = json.loads(scenario.read_text(encoding="utf-8"))["steps"]
    if used >= len(steps):
        return fail("no scenario step left")

    step = steps[used]
    state.write_text(str(used + 1), encoding="utf-8")
    prompt = argument(argv, "-p")
    if prompt is None or not re.search(step["expect"], prompt):
        return fail(f"expected prompt matching {step['expect']!r}, got {prompt!r}")

    prompt_index = argv.index("-p")
    flags = argv[:prompt_index] + argv[prompt_index + 2:]
    for flag, expected in step.get("args", {}).items():
        actual = argument(flags, flag)
        if actual != expected:
            return fail(f"expected {flag} {expected!r}, got {actual!r}")

    time.sleep(step.get("sleep", 0))
    for spec in step.get("commits", []):
        commit(spec)
    for name, value in step.get("refs", {}).items():
        git("update-ref", name, git("rev-parse", "--verify", value))

    subtype = step.get("subtype", "success")
    output = {
        "type": "result",
        "subtype": subtype,
        "is_error": step.get("is_error", False),
        "num_turns": step.get("turns", 0),
        "total_cost_usd": step.get("cost", 0.0),
        "permission_denials": [{}] * step.get("denials", 0),
        "api_error_status": step.get("api_error_status"),
    }
    if not subtype.startswith("error"):
        output["result"] = expand_revisions(step.get("result", ""))
    print(json.dumps(output))
    return step.get("exit", 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
