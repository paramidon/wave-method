"""Set "version" in a plugin.json: python set_plugin_version.py <plugin.json> <version>.

Used only by the release workflow; the version comes from the release tag.
"""
import json
import sys
from pathlib import Path

path, version = Path(sys.argv[1]), sys.argv[2]
data = json.loads(path.read_text(encoding="utf-8"))
ordered = {}
for key, value in data.items():
    if key != "version":
        ordered[key] = value
    if key == "name":
        ordered["version"] = version
path.write_bytes((json.dumps(ordered, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
