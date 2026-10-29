# Lite solutions (low problems)

## P3. README with install and usage
User problem: a README that explains how to install and use the tool · feature F2
**Edit:** new `README.md`: one-line description; install `pip install -e .`; the three commands with the outputs of
`solutions/P2-cli-commands.md` "Behaviour"; an example session (add two tasks, list, done 1, list); "Data is stored
in `todo.json` in the current folder." · **Check:** every command and output in the README matches the P2 table.

## P4. Tests on every push
User problem: run the tests on every push · feature F3
**Edit:** new `.github/workflows/test.yml`: on `push` and `pull_request`; matrix Python `3.10` and `3.12`;
steps `actions/checkout@v4`, `actions/setup-python@v5`, `pip install -e . pytest`, `pytest -q` · **Check:**
`python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/test.yml` succeeds (or any YAML
linter), and the file names both Python versions.
