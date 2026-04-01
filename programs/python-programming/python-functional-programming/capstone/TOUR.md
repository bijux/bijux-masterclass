# FuncPipe Capstone Tour

This tour is the learner-facing entrypoint for the FuncPipe capstone. It builds a proof
bundle that captures the code and evidence surfaces the course keeps referring to:
package layout, test proof, and the main areas where purity, effects, and async
coordination live.

## What the tour produces

- `pytest.txt`: the current test run for the capstone
- `ARCHITECTURE.md`: the package map for the capstone
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
make PROGRAM=python-programming/python-functional-programming capstone-tour
```

## What to inspect first

1. `ARCHITECTURE.md`
2. `pytest.txt`
3. `focus-areas.txt`
4. `package-tree.txt`
5. `test-tree.txt`
6. `README.md`

That order mirrors the course: map first, proof second, then architectural hotspots, and
finally the wider codebase shape.
