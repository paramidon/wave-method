# Lite solutions (low problems)

## P3. Where to start an unattended run

User problem: one place in the docs that says how to start `wave-auto` from the console and from the desktop apps of
Claude Code and Codex · feature F2

**Edit:** in `README.md`, inside the new `### Unattended runs: wave-auto` (`solutions/P4-driver-removal.md`, "README
after the removal", item 2), in place of its placeholder line, insert:

````
#### Where to run it

| Where | Start | The questions | Continue after a closed window or a limit |
|---|---|---|---|
| Claude Code CLI | `claude` in the project, an Opus-class model, permission mode `auto`; type `/wave-auto <list>` | answer in the same session | `/wave-auto plans/<date>-<topic>/index.md` in a new session |
| Claude Code desktop app | a new session (Code tab) in the project folder, an Opus-class model, permission mode `auto`; type `/wave-auto <list>` | answer in the same session | the same, in a new session |
| Codex CLI | `codex -m gpt-6.2-astra` in the project, with the permission profile of [Codex permissions](#codex-permissions); type `$wave-auto <list>` | answer in the same session | `$wave-auto plans/<date>-<topic>/index.md` in a new session |
| Codex desktop app | a new thread in the project, GPT-6.2-Astra, permissions as [Codex permissions](#codex-permissions) says for the desktop app; type `$wave-auto <list>` | answer in the same thread | the same, in a new thread |

The worktrees live next to the project (`../<repo>.worktrees/`), so the agent needs write access there. Claude Code's
`auto` mode allows it. In Codex use the permission profile of [Codex permissions](#codex-permissions).

To start a run from a script, with nobody at the keyboard, start from an index whose questions are answered (or answer
them in a second call):

```
claude -p "/wave-auto plans/<date>-<topic>/index.md"
codex exec -m gpt-6.2-astra "\$wave-auto plans/<date>-<topic>/index.md" < /dev/null
```

A list start asks its questions first; answer with `claude -p --continue "<answers>"` or
`codex exec resume --last "<answers>" < /dev/null`, run in the project folder.
````

Re-plan 2026-11-26 (round 2 of F1): the Codex placeholders are gone. F1 adds the README section `### Codex
permissions` (`solutions/P2-codex-coordinator.md`, "Permissions and gate texts (task L)"), and task P adds its
desktop-app sentence; the table and the script lines point to it and need no options of their own, since the project's
`.codex/config.toml` applies the profile.

**Check:** the README has `#### Where to run it` with the 4-row table, both script lines and no `<sandbox>`,
`<permission>` or `<…as the Codex rehearsals recorded>` placeholder left (`grep -n -E "<sandbox|<permission" README.md`
prints nothing); `grep -c "(#codex-permissions)" README.md` prints at least 3 and `grep -n "^### Codex permissions"
README.md` prints one line.
