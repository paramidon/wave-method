#!/usr/bin/env sh
# Installs the wave skill set into a project:
#   <target>/.claude/skills/wave-*   copies of skills/wave-*
#   <target>/.agents/skills/wave-*   symlinks to them, for Codex (skip with --no-codex)
#
# Usage:
#   ./install.sh /path/to/project
#   ./install.sh /path/to/project --force      # replace existing wave-* skill folders
#   ./install.sh /path/to/project --no-codex
set -eu

if [ $# -lt 1 ]; then
    echo "usage: $0 <target project> [--force] [--no-codex]" >&2
    exit 2
fi

target=$(cd "$1" && pwd)
shift
force=0
codex=1
for arg in "$@"; do
    case "$arg" in
        --force) force=1 ;;
        --no-codex) codex=0 ;;
        *) echo "unknown option: $arg" >&2; exit 2 ;;
    esac
done

source_dir=$(cd "$(dirname "$0")/skills" && pwd)
claude_skills="$target/.claude/skills"
agent_skills="$target/.agents/skills"
skills="wave-triage wave-plan wave-run wave-status"

mkdir -p "$claude_skills"
for name in $skills; do
    to="$claude_skills/$name"
    if [ -e "$to" ]; then
        if [ "$force" -ne 1 ]; then
            echo "$to already exists; re-run with --force to replace it" >&2
            exit 1
        fi
        rm -rf "$to"
    fi
    cp -R "$source_dir/$name" "$to"
    find "$to" -type d -name __pycache__ -prune -exec rm -rf {} +
    echo "installed $to"
done

if [ "$codex" -eq 1 ]; then
    mkdir -p "$agent_skills"
    for name in $skills; do
        link="$agent_skills/$name"
        if [ -L "$link" ]; then
            continue
        fi
        if [ -e "$link" ]; then
            echo "$link exists and is not a symlink" >&2
            exit 1
        fi
        ln -s "../../.claude/skills/$name" "$link"
        echo "linked  $link"
    done
    echo "Consider adding '.agents/' to the project's .gitignore."
fi
