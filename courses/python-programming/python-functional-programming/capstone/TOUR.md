# FuncPipe Capstone Tour

This tour is the learner-facing entrypoint for the FuncPipe capstone. It builds a proof
bundle that captures the code and evidence surfaces the course keeps referring to:
package layout, test proof, and the main areas where purity, effects, and async
coordination live.

## What the tour produces

- `pytest.txt`: the current test run for the capstone
- `package-tree.txt`: the package layout under `src/funcpipe_rag`
- `test-tree.txt`: the test layout under `tests`
- `focus-areas.txt`: the packages most relevant to course milestones
- `README.md`: the repository guide for the capstone
- `pyproject.toml`: the executable project contract

## How to run it

From the capstone directory:

```bash
make tour
```

From the repository root:

```bash
make COURSE=python-programming/python-functional-programming capstone-tour
```

## What to inspect first

1. `pytest.txt`
2. `focus-areas.txt`
3. `package-tree.txt`
4. `test-tree.txt`
5. `README.md`

That order mirrors the course: proof first, then architectural hotspots, then the wider
codebase shape.
