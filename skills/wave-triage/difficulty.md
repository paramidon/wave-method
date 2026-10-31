# Problem difficulty and part budget

Single source of truth for the `wave-triage` and `wave-plan` skills. Change the numbers here only.
This is the difficulty of a **problem** (how unclear the way to solve it is), judged before any design.
It is not the complexity of a **task** (which model executes it): tasks exist only after wave-plan has done
the architecture, whose job is to turn hard problems into medium tasks.

## Difficulty
- `low` — the change is obvious and local.
- `medium` — the approach is clear, the work spans several files or needs its own tests.
- `high` — the approach itself is unclear: needs design, research, numeric experiments, or touches core
  invariants (see the project's AGENTS.md / CLAUDE.md / GEMINI.md for which invariants are core).

Judge it from a quick look at the code: find where the problem lives (search, open the relevant
class/function), not from the statement alone. Do not design a solution while judging.

## Size
Rough number of tasks the problem will become: 1, 2–3, 4+.

## Part budget
One part = one wave-plan run in a fresh session = one plan folder.
- Points: `low` = 1, `medium` = 2, `high` = 5. At most **10 points** per part.
- At most **2 `high`** problems per part.
- A `high` problem of size 4+ goes alone (it may take `low` problems as companions).
- At most ~4 expected features and ~12 expected tasks per part.
- One problem that alone exceeds the budget (8+ tasks, or design that cannot be judged at all) needs a
  dedicated research step first: tell the user, do not hide it inside a part.
