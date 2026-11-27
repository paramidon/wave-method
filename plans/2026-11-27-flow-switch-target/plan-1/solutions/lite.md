# Lite solutions (low problems)

## P1. The flow form names an index part's integration branch after the index topic

User problem: switching a plan of an index part to autonomous flow names `integration/<plan>`, not the index's shared
`integration/<topic>` · feature F1

**Cause:** the flow form takes `<name>` from the current `target:`, else `<plan>` (`skills/wave-run/autonomous.md:17`);
"Names" (`skills/wave-plan/layout.md:229`) and "Flow" (`skills/wave-plan/layout.md:458`) give the same default. Only
`wave-plan` in autonomous flow of planning writes `integration/<topic>` for an index part.

**Rule (new):** `<name>` = the `<name>` of `target:`; else, for a plan of an index part (README header line
`` - Index: `plans/<date>-<topic>/index.md` part <K> ``, backticks optional), the index `<topic>` (the index folder name
without its `YYYY-MM-DD-` prefix); else `<plan>`.

### Edit 1 · `skills/wave-plan/layout.md`, "Names" (lines 229–230)

Replace

```
- `<name>` — the name of the plan's integration branch after `integration/`: from `target:` of the README `Flow:`
  line, else `<plan>` ("Flow"). Used in autonomous flow only.
```

with

```
- `<name>` — the name of the plan's integration branch after `integration/`: from `target:` of the README `Flow:`
  line; else, for a plan of an index part (README header line `- Index: plans/<date>-<topic>/index.md part <K>`,
  the path in backticks or not), the index `<topic>`, the index folder name without its `YYYY-MM-DD-` prefix; else
  `<plan>` ("Flow"). Used in autonomous flow only.
```

### Edit 2 · `skills/wave-plan/layout.md`, "Flow" (lines 458–460)

Replace

```
- `target:` names the integration branch; without it the target is `integration/<plan>`. A plan of an index part in
  autonomous flow names `integration/<topic>`: all parts of an index share one integration branch
  ("Planning in autonomous flow").
```

with

```
- `target:` names the integration branch; without it the target is `integration/<name>`, `<name>` as "Names" defines
  it. A plan of an index part in autonomous flow names `integration/<topic>`, whether it was planned in autonomous
  flow or switched later by the flow form: all parts of an index share one integration branch ("Planning in
  autonomous flow"). The status check reports `flow-target` for an index part with another `target:`.
```

### Edit 3 · `skills/wave-plan/layout.md`, "Statuses", status check (lines 273–275)

In the sentence that starts `It also checks the` replace

```
`flow-review-unknown` for a `manual review:`
  ID that is not a feature.
```

with

```
`flow-review-unknown` for a `manual review:`
  ID that is not a feature, `flow-target` for a plan of an index part whose `target:` is not `integration/<topic>`.
```

Re-wrap the paragraph so that no line exceeds 120 characters; change no other word.

### Edit 4 · `skills/wave-run/autonomous.md`, "Flow form", step 2 (lines 17–18)

Replace

```
2. `autonomous`: `<name>` is the `<name>` of the current `target:`, else `<plan>`; run the checks of "Integration
   target", step 1.
```

with

```
2. `autonomous`: `<name>` is the `<name>` of the current `target:`; else, for a plan of an index part (README header
   line `- Index: plans/<date>-<topic>/index.md part <K>`), the index `<topic>`, so that the part shares
   `integration/<topic>` with the other parts of its index; else `<plan>` (`layout.md`, "Names"). Run the checks of
   "Integration target", step 1.
```

(the rest of step 2, from `` `manual`: ``, stays as it is).

### Edit 5 · `skills/wave-run/autonomous.md`, "Integration target" (line 34)

Replace `` `<name>` comes from `target:`, else it is `<plan>`. `` with
`` `<name>` comes from `target:`, else from `layout.md`, "Names" (the index topic for a plan of an index part, else `<plan>`). ``
and re-wrap that paragraph to at most 120 characters per line.

### Edit 6 · `README.md`, "Choosing the flow" (third bullet) and "The integration branch"

- After the sentence `` Between waves, `/wave-run <plan folder> flow autonomous review F2` switches an existing plan and keeps F2
  under manual review. `` insert the sentence
  `` A plan of an index part then merges into the index's `integration/<topic>`, as the parts planned in autonomous flow do. ``
- In "The integration branch", replace `` All parts of an index share `integration/<name>`, where `<name>` is the index topic. ``
  with `` All parts of an index share `integration/<name>`, where `<name>` is the index topic, also a part switched later with the flow form. ``

Re-wrap both paragraphs to at most 120 characters per line.

### Edit 7 · `skills/wave-plan/CHANGELOG.md`

Insert, after the introduction paragraph and its blank line, before the `- v2.13.0 (2026-11-27) — …` item, this item
followed by a blank line (lines at most 120 characters, continuation lines indented by two spaces):

```
- Unreleased — the flow form `/wave-run <plan folder> flow autonomous` switches a plan of an index part to the
  index's shared `integration/<topic>` instead of `integration/<plan>` (`layout.md`, "Names"); `status_check.py`
  reports `flow-target` for an index part whose `target:` names another branch.
```

### Edit 8 · checker guard, `skills/wave-plan/scripts/status_check.py`

Add after the `FLOW = …` definition (line 8–9):

```python
INDEX = re.compile(r"- Index: `?plans/\d{4}-\d{2}-\d{2}-([A-Za-z0-9][A-Za-z0-9._-]*)/index\.md`? part \d+")
```

Add after the function `flow` (after line 86):

```python
def index_topic(lines):
    """Return the topic of the README header's Index line, or None for a plan without an index."""
    for text in lines:
        if text.startswith("## "):
            break
        match = INDEX.match(text.rstrip())
        if match:
            return match[1]
    return None
```

In `check`, replace `flow_name, _, manual_review, flow_line = flow(readme_lines, report_readme)` with
`flow_name, target, manual_review, flow_line = flow(readme_lines, report_readme)`, and right after the loop that reports
`flow-review-unknown` add:

```python
    topic = index_topic(readme_lines)
    if flow_name == "autonomous" and topic and target and target != "integration/" + topic:
        report(readme, flow_line, "flow-target",
               f"a plan of index part targets integration/{topic}, found {target}")
```

A missing `target:` is not reported: its default is now `integration/<topic>`.

Tests in `skills/wave-plan/scripts/test_status_check.py`, after `test_flow_autonomous_default_target`, each built with
`README.replace("# Test plan\n", "# Test plan\n\n" + <header lines>)`:

| Test | Header lines | Expected |
|---|---|---|
| `test_flow_target_index_part` | ``- Index: `plans/2026-11-27-test-plan/index.md` part 3\n- Flow: autonomous · target: integration/test-plan-p3\n`` | `self.assert_rule("flow-target", readme)` |
| `test_flow_target_index_topic` | ``- Index: `plans/2026-11-27-test-plan/index.md` part 3\n- Flow: autonomous · target: integration/test-plan\n`` | exit 0, no output |
| `test_flow_target_index_default` | ``- Index: `plans/2026-11-27-test-plan/index.md` part 3\n- Flow: autonomous\n`` | exit 0, no output |
| `test_flow_target_raw_plan` | `- Flow: autonomous · target: integration/other-name\n` (no Index line) | exit 0, no output |

**Check:** `python skills/wave-plan/scripts/test_status_check.py` → 43 tests OK;
`for plan in examples/*/; do python skills/wave-plan/scripts/status_check.py "${plan%/}"; done` → no output;
`` git grep -n -e "else \`<plan>\`; run the checks" -e "without it the target is \`integration/<plan>\`" -e "else it is \`<plan>\`" -- skills README.md ``
→ no output (the three old sentences are gone); `git diff --check` → no output.
