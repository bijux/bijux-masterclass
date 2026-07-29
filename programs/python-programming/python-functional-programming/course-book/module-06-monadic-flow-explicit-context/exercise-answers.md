# Module 06 Exercise Answers

Use these answers to review a completed attempt, not as starting code. Each
answer explains the decision, identifies common wrong turns, and limits the
claim supported by the focused evidence.

When an alternative implementation preserves the stated observable and the
earlier RAG contract, compare its trade-offs instead of treating syntax as the
grading criterion.

## and_then and bind: preserve the first failure

Make each prerequisite append its own stable name before checking the document.
Compose them in the required order:

```python
result = (
    source
    .and_then(require_title)
    .and_then(require_abstract)
    .and_then(clean_checked)
)
```

For a missing title, the expected trace is `["require_title"]`. Neither the
abstract check nor cleaning should run because `Err.and_then` preserves the
first error without invoking its function.

Common wrong turns:

- using `map(require_title)` creates a nested `Result`;
- checking all fields eagerly loses fail-fast order;
- asserting only the final error cannot prove later work was skipped;
- raising `ValueError` discards the Module 05 typed failure contract.

The proof establishes ordered short-circuiting for this chain. It does not prove
that fail-fast validation is always preferable; independent field validation
may still require accumulating `Validation`.

## Lifting plain functions: keep independent inputs independent

Validate `sample_size` separately, then lift a curried three-argument
constructor or combine two fields first and map the third. Keep the observable
failure order explicit in the test.

Common wrong turns:

- using `and_then` implies a dependency between fields that do not depend on
  one another;
- expecting `Result.liftA2` to accumulate both errors contradicts its fail-fast
  contract;
- placing validation inside the constructor can leak `ValueError`;
- comparing only successful output ignores error precedence.

The focused proof establishes independent combination and `Result` error order.
It does not establish cross-field validity for arbitrary values. If learners
must see every invalid field at once, use the Module 05 `Validation`
applicative and test the accumulated error tuple.
