# Wave skill set changelog

Releases are git tags `vMAJOR.MINOR.PATCH`; the release workflow copies the tag into `.claude-plugin/plugin.json`,
and no other file carries a version. Changes since the last tag go into a line
`- Unreleased — …` at the top; a release renames it to the tag and date.

- Unreleased — the release workflow writes the tag's version into `version` of `.claude-plugin/plugin.json` on `main`
  and into the archives, so Claude Code shows the release version and offers the update; `wave-status` leads with
  feature status (a count per status, a table with task progress and merge hash) before the wave line.
- v2.0.3 (2026-10-29) — the changelog no longer lists the deleted tag v2.0.1.
- v2.0.2 (2026-10-29) — the version lives only in the release tag: version lines, `skills: vN` in plan and index
  headers, `SKILL_SET_VERSION` and the plugin `version` field are removed.
- v2.0.0 (2026-10-29) — skill file paths are relative to the wave skills folder instead of `.claude/skills/`, so the
  set also works as a Claude Code plugin.
- v1 (2026-10-29) — first public version (untagged).
