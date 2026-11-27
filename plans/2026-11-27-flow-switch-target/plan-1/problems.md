# Open problems
Next ID: I5

- **[I4 · wave 1 / task C / feature F2] P3 acceptance test 4 and the navigator's "(the next reading prints it)" promise
  a `halt` line that the rules do not give while an earlier part has a step to run** — where:
  `skills/wave-auto/navigator.md:61`, `solutions/P3-ask-all-manual-plans.md` "Acceptance tests" 4; expected: after
  plan-3 is switched, `halt …/plan-2: tracking branch … is missing` before the `next:` line / got: only
  `next: wave …/plan-1 1`, because step 3.2 ends the reading at the first row that yields a `next:` line, so the halt
  appears only once part 1 has nothing to run (confirmed by the coordinator against the rule text); proposal: keep the
  behaviour and correct both texts: "(a later reading that reaches its row prints it)", and scenario 4 with plan-1 in
  `skip`; status: open
