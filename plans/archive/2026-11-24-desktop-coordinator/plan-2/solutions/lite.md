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

Re-plan 2026-11-27: the desktop-app sentence that task P was to add never came (P was superseded), and the script lines
fail on Windows; "P5" below replaces the Codex desktop app row and the script paragraphs.

## P5. The unattended-run text of the README is right, and the cleanup leaves no long or split line

User problem: the README's "Unattended runs" text names guidance that does not exist and script lines that fail on
Windows (I24, I25 of wave 13) · feature F2

Facts, checked while planning on 2026-11-27 with a stand-in program that prints its arguments (no CLI was run):

- Git Bash on Windows turns an argument that starts with `/` into a Windows path: `"/wave-auto plans/…"` arrived as
  `C:/Program Files/Git/wave-auto plans/…`. With `MSYS_NO_PATHCONV=1` it arrived unchanged. `"\$wave-auto …"`
  arrived unchanged.
- Windows PowerShell 5.1: `"/wave-auto …"` and `'$wave-auto …'` arrive unchanged; `"$wave-auto …"` in double quotes
  arrives as `-auto …`; `< /dev/null` is a parse error; with `$null |` the program's input ends at once (in the
  session that checked it, after one byte-order mark).

The user chose on 2026-11-27 not to run the script lines against Claude Code or Codex; the README says so.

**Edit A** (`README.md`, section `### Unattended runs: wave-auto`, `#### Where to run it`):

1. In the table row that starts `| Codex desktop app |`, the second cell becomes exactly the text of this block:

   ```
   a new thread in the project, GPT-6.2-Astra; type `$wave-auto <list>`. Not rehearsed, the profile of [Codex permissions](#codex-permissions) included
   ```

2. Everything from the line that starts `To start a run from a script` up to, not including, `### In the morning`
   becomes exactly the text between the four-backtick fences, followed by one blank line:

````
To start a run from a script, with nobody at the keyboard, start from an index whose questions are answered (or answer
them in a second call). In bash or zsh:

```bash
claude -p "/wave-auto plans/<date>-<topic>/index.md"
codex exec -m gpt-6.2-astra "\$wave-auto plans/<date>-<topic>/index.md" < /dev/null
```

In PowerShell:

```powershell
claude -p "/wave-auto plans/<date>-<topic>/index.md"
$null | codex exec -m gpt-6.2-astra '$wave-auto plans/<date>-<topic>/index.md'
```

Git Bash on Windows rewrites an argument that starts with `/` into a Windows path: there, put
`MSYS_NO_PATHCONV=1` before the `claude` command, or use PowerShell.

A list start asks its questions first; answer with `claude -p --continue "<answers>"` or
`codex exec resume --last "<answers>"`, run in the project folder; give Codex the same `< /dev/null` (bash, zsh) or
`$null |` (PowerShell) as above. None of these script lines has been run as written yet.
````

**Edit B** (two places task Z left awkward; only line breaks and indentation change):

1. `examples/README.md`: the line that starts `In the morning, the final report` is longer than 120 characters. Rewrap
   that sentence and the lines of its paragraph to at most 120 characters each.
2. `skills/wave-plan/CHANGELOG.md`, the `- Unreleased` item: a code span is split between `-` and `Flow:`. The first
   line of the item ends with `A README line`; the second starts with two spaces and the whole code span
   `` `- Flow: autonomous · target: integration/<name> · manual review: <F-IDs>` ``. Rewrap the following lines only as
   far as needed to keep every line at most 120 characters, two-space continuation indent.

**Check:** the checks of tasks AC and AD in `waves/w15.md`.
