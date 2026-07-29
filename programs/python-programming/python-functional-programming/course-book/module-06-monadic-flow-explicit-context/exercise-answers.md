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

## Law-guided design: justify a regrouping

Define `word_count` as an ordinary pure function. Compare:

```python
source.map(clean_doc).map(lambda doc: doc.abstract).map(word_count)
```

with one `map` containing the same composed function order. The equality should
hold for the generated source documents.

Common wrong turns:

- reversing functions tests a different program, not a regrouping;
- adding logging inside a mapped function invalidates the pure substitution
  argument;
- testing only one tidy string misses the useful generated input space;
- claiming the property proves the normalization policy confuses algebraic and
  product correctness.

The property proves the chosen map composition law for the modeled documents.
It does not prove every possible `Result` implementation or every RAG business
rule.

## Reader pattern: vary overlap at the call site

Keep the `asks` expression unchanged and run it with two valid `RagEnv`
instances. For chunk size `4`, overlap `2` advances by two characters instead
of four, so the expected text sequence must include the overlapping windows.

Common wrong turns:

- reconstructing the Reader for each environment hides whether the program
  itself changed;
- mutating a shared configuration object contradicts frozen value semantics;
- asserting only chunk counts can miss wrong boundaries or ordering;
- wrapping a single ordinary argument in Reader without shared context adds
  ceremony without visibility.

The proof establishes explicit environment injection and deterministic chunk
output for these runs. It does not prove Reader is necessary for every
configuration-dependent function.

## Explicit state threading: add skipped-chunk progress

Add `skipped` to the frozen dataclass and make the accounting operation choose
one new `Progress` value from the current state. Chain it in the same location
where the chunk is observed.

Common wrong turns:

- mutating fields in place hides the state transition;
- reading a module-global counter removes the caller-supplied initial state;
- counting skipped text as processed changes the declared metric;
- asserting only the final integer loses the result value and other state
  fields.

The proof establishes deterministic local state transitions for the tested
sequence. It does not establish concurrency safety or justify using State when
a direct fold would be simpler.

## Error-typed flows: narrow the expected exception set

Keep `try_result` around `int(raw)` only. Then compose a pure
`require_positive` function with `and_then` so parse and range failures have
separate owners.

Common wrong turns:

- catching `Exception` converts bugs into misleading input failures;
- raising for a routine negative configuration value bypasses the typed
  contract;
- using one generic error code destroys provenance;
- placing `try_result` throughout the domain confuses boundary conversion with
  business validation.

The proof establishes the declared exception classification for this adapter
and domain check. It does not prove that every `ValueError` in the application
is expected or recoverable.
