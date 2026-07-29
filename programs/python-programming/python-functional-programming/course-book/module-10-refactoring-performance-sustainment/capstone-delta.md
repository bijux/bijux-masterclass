# Module 10 Capstone Delta

Module 09 left FuncPipe with disciplined ecosystem boundaries and a review command
that inventories packages, test groups, and proof routes. Module 10 does not add
another RAG feature. It makes the existing system safer to change.

## The application delta

| Delta question | Module 10 answer |
| --- | --- |
| Previous capability | A deterministic local RAG pipeline with typed failures, streaming and async policies, adapters, interop boundaries, and learner-facing proof routes |
| New pressure | A maintainer must decide whether a refactor, optimization, migration, or scaling proposal is safe without trusting a persuasive description |
| Concept introduced | Sustainment as explicit observations, pure review decisions, and executable evidence |
| Source surfaces | `capstone/src/funcpipe_rag/review/` and `capstone/src/funcpipe_rag/boundaries/shells/review_cli.py` |
| Proof surfaces | `capstone/tests/learning/test_module_10_sustainment.py` plus focused unit tests beside each review boundary |
| Preserved behavior | Module 09 CLI, web, interop, local-pipeline, error, streaming, and async contracts |
| Completed state | The live capstone and generated `capstone/_history/worktrees/module-10/` endpoint |
| Learner route | Run focused learning tests first, then `make inspect`; use `make confirm` only for final confirmation |
| Later states affected | None: Module 10 is the cumulative endpoint |

The important boundary is the one between an observation and a decision. Timing a
stage, listing a required proof, or discovering an optional backend is effectful.
Deciding whether the observation meets a declared budget or evidence rule can remain
pure. That separation makes the decision cheap to test and keeps noisy measurements
out of the functional core.

## Why the Module 09 state stays unchanged

The Module 09 reference state represents the course immediately after ecosystem
integration. Backporting sustainment types or review rules into that state would erase
the pressure that Module 10 is meant to solve. All implementation changes in this
module therefore belong only to the live capstone. History refresh copies that endpoint
to the generated Module 10 worktree; it must not rewrite Modules 01 through 09.

## Working route

1. Compare `capstone/module-reference-states/module-09/` with `capstone/`.
2. Read the current core lesson and identify its review decision.
3. Run the named test in `capstone/tests/learning/test_module_10_sustainment.py`.
4. Change either the supplied observation or the pure decision rule and predict the result.
5. Run `make inspect` from `capstone/` and review the saved text and JSON reports.
6. Finish with the module exercises and explain what each proof does **not** establish.

## Preservation checklist

Before accepting a Module 10 change, confirm that:

- the RAG result and typed failure contracts did not change accidentally;
- performance evidence compares equivalent behavior;
- observations are values and do not become hidden control flow;
- async proofs cover ordering, boundedness, or cancellation rather than merely completing;
- optional scaling remains an explicit capability decision;
- migrations state which callers remain compatible;
- governance checks point to executable evidence; and
- the strongest confirmation route is reserved for the final review.

Continue with [Systematic Refactor](systematic-refactor.md).
