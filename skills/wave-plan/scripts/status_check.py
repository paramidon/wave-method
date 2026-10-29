"""Check the status tables and problem entries of one wave plan."""
import re
import sys
from pathlib import Path

MARK = re.compile(r"⬜|🔄|✅|⚠️|❌|➖")
ENTRY = re.compile(r"^- \*\*\[(I\d+) · ([^\]]*)\]")
COLUMNS = {
    "Features": ("ID", "Status", "Merged"),
    "Waves": ("Wave", "Status"),
    "Tasks": ("ID", "Status"),
}


def cells(line):
    values = re.split(r"(?<!\\)\|", line)[1:]
    if values and not values[-1].strip():
        values.pop()
    return [cell.strip() for cell in values]


def mark(cell):
    match = MARK.search(cell)
    return match.group() if match else ""


def tables(lines, report):
    result = {}
    for name, required in COLUMNS.items():
        heading = next((i for i, line in enumerate(lines)
                        if line.strip() == "## " + name), None)
        if heading is None:
            raise ValueError("required table missing: " + name)
        start = heading + 1
        while start < len(lines) and not lines[start].startswith("|"):
            if lines[start].startswith("#"):
                raise ValueError("required table missing: " + name)
            start += 1
        if start + 1 >= len(lines):
            raise ValueError("required table missing: " + name)
        header = cells(lines[start])
        separator = cells(lines[start + 1])
        if (not all(column in header for column in required)
                or len(separator) != len(header)
                or not all(re.fullmatch(r":?-+:?", cell) for cell in separator)):
            raise ValueError("invalid table header or separator: " + name)
        rows = []
        for index in range(start + 2, len(lines)):
            if not lines[index].startswith("|"):
                break
            values = cells(lines[index])
            if len(values) != len(header):
                report(index + 1, "row-cells",
                       f"{name}: expected {len(header)} cells, found {len(values)}")
                continue
            rows.append((index + 1, dict(zip(header, values))))
        result[name] = rows
    return result


def problems(lines):
    entries = {}
    starts = [(i, ENTRY.match(line)) for i, line in enumerate(lines) if ENTRY.match(line)]
    for position, (index, match) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[index:end])
        status = text.rsplit("status:", 1)[1].strip() if "status:" in text else ""
        items = set(re.findall(r"\b(wave|task|feature)\s+([\w-]+)", match[2]))
        for tasks in re.findall(r"→\s+tasks?\s+([\w-]+(?:\s*,\s*[\w-]+)*)", status):
            items.update(("task", task.strip()) for task in tasks.split(","))
        entries[match[1]] = (index + 1, status.startswith(("open", "→")), items)
    return entries


def check(folder):
    readme = folder / "README.md"
    problem_file = folder / "problems.md"
    if not folder.is_dir() or not readme.is_file():
        print(f"{readme}:1: plan folder or README is missing", file=sys.stderr)
        return 2
    violations = []

    def report(file, line, rule, detail):
        violations.append(f"{file}:{line}: {rule}: {detail}")

    try:
        parsed = tables(readme.read_text(encoding="utf-8").splitlines(),
                        lambda line, rule, detail: report(readme, line, rule, detail))
        lines = problem_file.read_text(encoding="utf-8").splitlines() if problem_file.exists() else []
    except (OSError, UnicodeError, ValueError) as error:
        print(f"{readme}:1: {error}", file=sys.stderr)
        return 2
    entries = problems(lines)
    items = {}
    for name, kind, key in (("Features", "feature", "ID"),
                            ("Waves", "wave", "Wave"), ("Tasks", "task", "ID")):
        for line, row in parsed[name]:
            cell = row["Status"]
            status = mark(cell)
            item = f"{kind} {row[key]}"
            items[kind, row[key]] = status
            if status in ("⚠️", "❌"):
                ids = re.findall(r"I\d+", cell)
                if (not any(entries.get(entry, (0, False, ()))[1] for entry in ids)
                        and not (kind == "wave" and status == "❌" and "re-run" in cell)):
                    report(readme, line, "red-without-entry", item + " names no open entry")
                closed = [entry for entry in ids if not entries.get(entry, (0, False, ()))[1]]
                if closed:
                    report(readme, line, "entry-names-closed",
                           item + " names closed or missing " + ", ".join(closed))
            if kind == "feature":
                merged = status == "✅" and re.search(r"✅\s+merged\b", cell)
                waiting = row.get("Waiting for", "")
                if merged and (waiting or not row["Merged"]):
                    report(readme, line, "merged-fields",
                           item + " needs empty Waiting for and non-empty Merged")
                if not merged and status != "➖" and "Waiting for" in row and not waiting:
                    report(readme, line, "waiting-missing", item + " has empty Waiting for")
    for entry, (line, opened, concerned) in entries.items():
        if opened and concerned and all(items.get(item) in ("✅", "➖") for item in concerned):
            report(problem_file, line, "entry-all-done", entry + " concerns only completed items")
    next_ids = [(i + 1, int(match[1])) for i, line in enumerate(lines)
                if (match := re.search(r"Next ID:\s*I(\d+)", line))]
    if entries and (not next_ids or next_ids[-1][1] <= max(int(entry[1:]) for entry in entries)):
        report(problem_file, next_ids[-1][0] if next_ids else 1, "next-id",
               "Next ID must exceed every entry ID")
    for violation in violations:
        print(violation)
    return 1 if violations else 0


def main():
    if len(sys.argv) != 2:
        print("usage: status_check.py <plan folder>", file=sys.stderr)
        return 2
    return check(Path(sys.argv[1]))


if __name__ == "__main__":
    sys.exit(main())
