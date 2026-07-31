# Run the Smallest Honest FuncPipe Command

Choose commands by the claim you need to settle. The tables distinguish working
directory, execution cost, output location, and interpretation so a passing command does
not become a larger claim than it supports.

## Establish the course environment

From the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming install
```

The managed environment is written under:

```text
artifacts/venv/python-programming/python-functional-programming/capstone
```

Generated reports, sites, caches, and bundles also remain under `artifacts/`; they should
not appear inside course source directories.

Run installation once before focused commands, and again when dependency metadata or the
Python environment changes. Make-based capstone routes declare installation as a
prerequisite, so they can prepare it automatically.

## Study a tracked module

From the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-module-state-proof MODULE=06
```

Valid values are `01` through `09`. The leading zero is required.

This command:

1. places the selected reference state’s `src` on `PYTHONPATH`;
2. collects the learning tests stored in that same state; and
3. runs current and preserved earlier-module learning proofs together.

It does not test the live Module 10 source.

| Need | Command |
| --- | --- |
| all cumulative learning tests through a tracked module | `capstone-module-state-proof MODULE=XX` |
| only Module 01 foundation laws | `capstone-foundation-proof` |
| strict Module 01 source typing | `capstone-foundation-types` |
| Module 01 filesystem shell behavior | `capstone-shell-proof` |
| Module 02 data-first API laws | `capstone-data-api-proof` |
| Module 02 filesystem boundary | `capstone-data-shell-proof` |
| Module 03 complete streaming laws | `capstone-streaming-rag-proof` |
| Module 03 multi-source scheduling laws | `capstone-source-scheduling-proof` |

The focused historical commands remain useful when their narrower claim is exactly your
question. The cumulative state route is the default end-of-module check.

## Inspect one live evidence route

From the capstone directory:

```bash
funcpipe-rag-review summary --claim migration-review --project-root .
```

Use `--format json` when another program or saved review needs structured output:

```bash
funcpipe-rag-review summary \
  --claim migration-review \
  --format json \
  --project-root .
```

`summary` always exits successfully when it can render. `check` exits nonzero if the
selected route’s required paths are missing:

```bash
funcpipe-rag-review check --claim migration-review --project-root .
```

Neither command executes the printed pytest command. Run that command separately when
you need behavioral evidence.

## Verify the live endpoint

From the repository root:

| Question | Command | Pytest runs | Additional result |
| --- | --- | ---: | --- |
| Do all live capstone tests pass? | `make PROGRAM=python-programming/python-functional-programming capstone-test` | 1 | saved pytest report |
| What packages, tests, and routes exist? | `make PROGRAM=python-programming/python-functional-programming inspect` | 0 | inspection bundle |
| Can I review a guided source/test bundle? | `make PROGRAM=python-programming/python-functional-programming capstone-tour` | 1 | tour bundle |
| Do I need a durable review record? | `make PROGRAM=python-programming/python-functional-programming capstone-verify-report` | 1 | verification bundle |
| Do I need inspection and tour together? | `make PROGRAM=python-programming/python-functional-programming proof` | 1 | both bundles reuse one report |
| Do tests, lint, types, build, inventory, and bundles all pass? | `make PROGRAM=python-programming/python-functional-programming test` | 1 | strongest published course gate |

These are alternatives at increasing scope. Running each row separately reruns pytest.
Within one composite `proof` or `test` invocation, dependent bundles reuse the saved
test report.

From the capstone directory, the corresponding short names are:

```text
make test
make inspect
make tour
make verify-report
make proof
make confirm
```

`make confirm` is the capstone-local form of the strongest published gate.

## Build and inspect the website

From the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming docs-build
```

The generated site belongs under:

```text
artifacts/site/python-programming/python-functional-programming
```

Use `docs-serve` for local browser reading:

```bash
make PROGRAM=python-programming/python-functional-programming docs-serve
```

A successful strict build proves navigation, Markdown links understood by MkDocs,
plugins, hooks, and theme generation completed. It does not prove every diagram is
legible at every viewport. Inspect the rendered capstone pages when diagram or layout
code changes.

## Verify cumulative history

From the repository root:

| Intent | Command |
| --- | --- |
| regenerate module tags, manifests, and comparison worktrees | `make PROGRAM=python-programming/python-functional-programming history-refresh` |
| compare generated history with tracked reference states | `make PROGRAM=python-programming/python-functional-programming history-verify` |
| remove generated history worktrees and local history refs | `make PROGRAM=python-programming/python-functional-programming history-clean` |

Use `history-verify` after course-only prose changes to confirm existing state integrity.
Use `history-refresh` when a reference state or live endpoint history contract changes.
Do not hand-edit `_history/worktrees`; they are generated comparison surfaces.

## Run a single pytest node

From the capstone directory, use the managed executable:

```bash
../../../../artifacts/venv/python-programming/python-functional-programming/capstone/bin/pytest \
  -q tests/unit/review/test_change.py \
  -k reports_independent_blockers
```

For a tracked state, also select that state’s source:

```bash
PYTHONPATH=module-reference-states/module-04/src \
  ../../../../artifacts/venv/python-programming/python-functional-programming/capstone/bin/pytest \
  -q module-reference-states/module-04/tests/learning/test_module_04_resilient_streaming.py \
  -k bounds_demand
```

If pytest reports many deselected tests and one pass, the focused claim executed. If it
collects live source while you intended a historical state, stop and correct
`PYTHONPATH`; a green result against the wrong source is not useful evidence.

## Interpret common failures

### `MODULE must be one of 01 through 09`

Use a two-digit tracked state. Module 10 is the live endpoint; run `capstone-test`.

### `funcpipe-rag-review: command not found`

Run the course installation or call the executable from the managed environment. Do not
install another global copy and accidentally inspect different source.

### A route is `missing`

Read `missing_paths` in text or JSON output. Determine whether a published path is stale
or the implementation/test was accidentally removed. Do not mark the route available
without restoring or deliberately revising the claim.

### Strict docs build reports a page outside navigation

Either add a genuine learner-facing page to `mkdocs.yml` or remove an unintended file.
Do not silence the warning while leaving hidden course material.

### A broad command fails after focused checks pass

Treat the broad failure as new evidence. Record the failing surface, run only its
focused reproduction, and repair the contract. Do not rerun an unchanged multi-minute
gate hoping for a different result.

## Record every meaningful run

For independent study or review, note:

```text
working directory:
command:
selected module or claim:
result:
what it proves:
what it does not prove:
```

This is enough to distinguish a historical state proof, live test run, route inspection,
site build, and full confirmation without saving raw terminal output in course source.
