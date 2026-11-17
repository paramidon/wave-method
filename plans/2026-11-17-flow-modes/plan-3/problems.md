# Open problems
Next ID: I2

- **[I1 · wave 1 / feature F1] Driver test discovery fails before the driver test directory exists** — where: `waves/w01.md:26`; the feature baseline check expects successful discovery, but `scripts/tests` is first created by tasks A–D and discovery exits 1; proposal: define the baseline check to run the status tests and diff check, and require driver test discovery after task files are present; status: open
