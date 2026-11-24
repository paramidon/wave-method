# Open problems
Next ID: I2

- **[I1 · wave 1 / task D / feature F1] The navigator's return grammar allows at most four `halt` lines, so with more than four halted units and no `next:` line the extra stops are dropped from the coordinator's final report** — where: `skills/wave-auto/navigator.md:112-125` ("Return grammar"), `solutions/P1-in-session-coordinator.md` "Return grammar"; expected / got: every halted unit listed in the final report / extra `halt` lines lost when the navigator answers `done`; proposal: raise the limit to the number of index parts, or let the coordinator navigate again with an extended `skip` before `done` (minor, not visible on typical indexes); status: → task J (wave 3)
