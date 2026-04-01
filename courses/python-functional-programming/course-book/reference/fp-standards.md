# FP Python Standards (Module 09 – Team Adoption)

This repo’s defaults are **functional by default**:

- Pure core by default; effects only in `funcpipe_rag.boundaries` and `funcpipe_rag.infra`.
- Prefer **stdlib FP** (`itertools`, `functools`, `operator`, `pathlib`) before adding new abstractions.
- Keep configuration as immutable data; build pipelines from config (no global state).
- Keep error handling explicit via `funcpipe_rag.result.types.Result` and `ErrInfo`.
- Prefer small, composable functions; name intermediates when a pipeline becomes hard to scan.

## Patterns

- **Iterator pipelines**: use `itertools.chain`, `itertools.accumulate`, `itertools.islice`, `itertools.groupby` (sorted/consecutive precondition).
- **Higher-order**: use `functools.partial` for configurators; use `functools.lru_cache` only for pure functions.
- **Lambda avoidance**: prefer `operator.itemgetter`/`attrgetter` for simple projections.
- **Boundaries**: shells/adapters interpret `IOPlan`/`AsyncPlan`; ports return descriptions, never execute.

## Pragmatic escapes

- Loops are allowed where they improve clarity or performance.
- Eager materialization is allowed at explicit sinks/boundaries.
- Custom abstractions (monads/effects) exist from earlier modules; for Module 09 code, treat them as optional and prefer stdlib-first refactors unless there is a concrete benefit.

