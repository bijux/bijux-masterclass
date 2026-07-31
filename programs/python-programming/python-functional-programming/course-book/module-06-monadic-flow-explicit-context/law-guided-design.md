# Law-Guided Design: Know What a Refactor Preserves

Container laws are useful because they answer a narrow engineering question:
which structural rewrites should preserve the meaning of this flow?

They do not prove that `clean_doc` implements the right normalization policy,
that retrieval ranks relevant documents, or that a production boundary is
reliable. Those are application claims and need application evidence.

Module 06 keeps the two kinds of proof separate.

## Start with one legal regrouping

The learning proof compares two ways to transform a successful `RawDoc`:

```python
separate = (
    source
    .map(clean_doc)
    .map(lambda cleaned: cleaned.abstract)
)

composed = source.map(
    lambda raw: clean_doc(raw).abstract
)

assert separate == composed
```

Run the property:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k result_map_composition_preserves_rag_cleaning
```

Hypothesis generates mixed-case and whitespace-heavy abstract strings. Both
groupings must return the same complete `Result`, not merely the same inner
string.

This is the functor composition law applied to real FuncPipe behavior:

```text
m.map(f).map(g) == m.map(lambda x: g(f(x)))
```

The law permits composition or extraction of pure transformations. It does not
permit reversing `f` and `g`, because order is part of the program.

## Three Result laws and the refactors they support

For dependent operations using `and_then`, Module 06 checks:

### Left identity

```text
Ok(x).and_then(f) == f(x)
```

Wrapping an available value in the success constructor before the next
dependent operation adds no new meaning.

Practical use: a helper can start from a plain fixture value or from
`Ok(value)` without changing the next Result-producing stage.

### Right identity

```text
m.and_then(Ok) == m
```

Lifting the current success back into the same context adds no new meaning.

Practical use: an extracted sub-pipeline may return with `Ok` without changing
the surrounding failure behavior.

### Associativity

```text
m.and_then(f).and_then(g)
==
m.and_then(lambda x: f(x).and_then(g))
```

The two groupings preserve the same success or first failure.

Practical use: you can extract `f` followed by `g` into a named dependent
sub-pipeline, or inline that sub-pipeline, without changing the Result
structure.

Associativity does not say that `f` and `g` commute. A requirement check
followed by cleaning is not equivalent to cleaning followed by the requirement
check.

## Why property-based tests help here

A law quantifies over many values. Three hand-selected examples can be useful,
but they do not match the shape of the claim.

The Module 06 law suite uses bounded Hypothesis strategies for:

- successful and failed Results;
- present and absent Options;
- small deterministic families of functions returning Result or Option; and
- transformations that exercise both success and stopping branches.

For example, a generated Result strategy includes both constructors:

```python
st.one_of(
    st.builds(Ok, st.integers()),
    st.builds(Err, st.text()),
)
```

A function strategy must also be rich enough to reveal broken behavior. If
every generated function returns `Ok(1)`, some properties can pass without
testing meaningful propagation.

Run the Result and Option laws in the Module 06 state:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q \
  tests/test_monad_laws.py
```

When a property fails, read the smallest counterexample as an explanation. Ask
which constructor, value, or function family exposes the mismatch.

## Laws are conditional on observable purity

Consider:

```python
events: list[str] = []

def observe(doc: CleanDoc) -> str:
    events.append(doc.doc_id)
    return doc.abstract
```

The returned string may satisfy the map composition equality while the event
trace differs under a test that evaluates one side more than once. The law of
the container has not made `observe` pure.

For law-guided substitution, decide which observations matter:

- returned values;
- exceptions;
- mutation;
- I/O;
- time or randomness;
- resource consumption; and
- evaluation count.

The Module 06 laws are most useful for pure value transformations and explicit
context values. Module 07 addresses actual effect execution boundaries.

## Algebraic proof versus product proof

Use this distinction in reviews:

| Claim | Appropriate evidence |
| --- | --- |
| Result `map` preserves identity and composition | Result law properties |
| Result `and_then` preserves identity and associativity | Result law properties |
| Failed prerequisites skip cleaning | Module 06 learning test with call trace |
| `clean_doc` implements the desired normalization policy | normalization examples and domain tests |
| Chunk boundaries remain unchanged after a refactor | complete chunk equality over relevant inputs |
| A flow is faster | a benchmark with an explicit workload and environment |

A passing monad law cannot stand in for the last four rows. Conversely, many
application examples cannot prove a generic container law.

## Deliberately break one rule

To understand the diagnostic value, imagine this incorrect implementation:

```python
class Err:
    def and_then(self, _):
        return Ok(0)
```

Right identity fails immediately:

```text
Err(error).and_then(Ok) != Err(error)
```

The failure identifies the structural defect: the error branch has stopped
preserving its error. It does not tell you whether `ErrInfo` contains a useful
code or whether the application should recover from that error.

Do this experiment only in a disposable learner copy or by reasoning through
the counterexample. Do not damage the tracked reference state.

## Reader, State, and Writer laws are observed by running them

`Reader`, `State`, and `Writer` contain callables, so comparing wrapper objects
directly is usually not meaningful. Their law tests compare observable runs:

```text
Reader: run both sides with the same environment
State:  run both sides with the same initial state
Writer: compare the returned value and ordered entries
```

This is an important testing principle: equality evidence must match the public
observation for the abstraction.

The focused law files are:

```text
tests/test_reader_laws.py
tests/test_state_laws.py
tests/test_writer_laws.py
```

## A review checklist for lawful refactors

Before citing a law:

1. Write the exact before and after expressions.
2. Name the law that relates those expressions.
3. Confirm function order is unchanged.
4. Confirm the functions are pure for the observations that matter.
5. Compare the complete contextual result.
6. Add application evidence for any domain claim outside the law.
7. State the input domain exercised by the property strategy.

## What the learning property proves

The RAG property establishes that separate and composed `map` groupings
preserve the normalized abstract inside `Result` for the generated strings.

It does not prove:

- all Unicode normalization behavior;
- that the normalization policy is desirable;
- exception safety for impure functions;
- Result performance; or
- correctness of the whole RAG pipeline.

Continue with [Reader Pattern](reader-pattern.md), where a shared read-only
environment becomes part of the observable run.
