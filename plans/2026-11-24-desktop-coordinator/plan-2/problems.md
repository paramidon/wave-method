# Open problems
Next ID: I8

- **[I1 · wave 1 / task A / feature F1] The `wave-run` skill description still names the medium model "GPT-6.1 SOL"** —
  where: `skills/wave-run/SKILL.md:3`; expected / got: the names of the new tier table (GPT-6.2-Sol) / "Sonnet 5.5 /
  GPT-6.1 SOL"; neither task A nor task B listed this edit; proposal: replace it with "GPT-6.2-Sol"; status: open
- **[I2 · wave 1 / task A / feature F1] README and layout already claim Codex rehearsals that are not recorded yet** —
  where: `README.md:434`, `skills/wave-plan/layout.md:160`; expected / got: claims backed by records in
  `docs/rehearsals/` / the texts of the solution, taken verbatim, while tasks D and E have not run; proposal: run D and E
  before F1 is merged, and correct both sentences if a rehearsal is recorded as Not run; status: open
- **[I3 · wave 1 / task A / feature F1] The two `codex plugin` commands of the README were not run and the Markdown was not
  viewed rendered** — where: `README.md`, "Codex plugin (recommended for Codex)"; expected / got: commands tried before
  they are documented / not run, because they change the user's Codex settings; proposal: run them in the rehearsal of
  task D or by hand; status: open
- **[I5 · wave 1 / task B / feature F1] The Codex example line of `wave-auto` is longer than 120 characters** — where:
  `skills/wave-auto/SKILL.md:70`; expected / got: at most 120 characters / 133 (one inline code span the solution puts on
  one line); proposal: keep it as an exception or wrap the span; status: open
- **[I6 · wave 1 / task B / feature F1] The "Launch groups" row of `wave-run` reads badly after the verbatim edit** —
  where: `skills/wave-run/SKILL.md:217`; expected / got: one clear sentence / "A group launches at once; up to the
  parallel limit, the rest as earlier tasks return; …", which splits "at once" from the limit; proposal: "A group
  launches at once, up to the parallel limit, the rest as earlier tasks return; without parallel subagents, …";
  status: open
