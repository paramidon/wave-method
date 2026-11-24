# Desktop coordinator — index

- Index: `plans/2026-11-24-desktop-coordinator/index.md` · created 2026-11-24 · base: fe1dbf2 · triaged 2026-11-24 21:11 – …

## Source list (verbatim)

жалоба:
автономный режим работает в CLI интерфейсе только. 
Он не работает в десктопной версии клод кода и в десктопной версии чат ГПТ. надо чтобы работал также в десктопе.
например - я запускаю  новый скиk и он уже сам является координатором - делает в субагентах триажи, планирование, передаёт задачи между субагентах и так далее.
Возможно такое сделать?
Хочу чтобы была возможность запуска этого как из консоли так и из десктопных клод кода и чат ГПТ кодекс.

The one complaint is split into three problems (pass 1):

| P | Summary | Cluster |
|---|---|---|
| P1 | In-session coordinator skill: one command runs triage → plan → waves via subagents (Claude Code) | coordinator |
| P2 | The same coordinator works in Codex (CLI and desktop app) | coordinator |
| P3 | Docs: how to launch unattended runs from the console and from the desktop apps | coordinator |

| Cluster | Area | Problems |
|---|---|---|
| coordinator | unattended run outside the Python driver (`scripts/wave_driver.py`) | P1, P2, P3 |
