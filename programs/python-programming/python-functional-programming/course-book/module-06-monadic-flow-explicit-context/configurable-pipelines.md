# Configurable Pipelines: Choose Policy at Assembly

A pipeline often needs strict and permissive modes. The fragile approach is to
thread a Boolean through every domain function:

```python
def normalize(
    doc: RawDoc,
    strict: bool,
) -> Result[CleanDoc, ErrInfo]:
    if strict:
        ...
```

Now normalization owns both its domain transformation and deployment policy.
Every caller can select a different branch, and adding another toggle expands
the function’s responsibility.

Module 06 keeps the base function stable and chooses wrappers when constructing
the callable.

## Run strict and permissive normalization

The learning proof defines one normalization function:

```python
calls: list[str] = []

def normalize(
    doc: RawDoc,
) -> Result[CleanDoc, ErrInfo]:
    calls.append(doc.doc_id)
    return Ok(clean_doc(doc))
```

It also defines a prerequisite:

```python
def require_abstract(
    doc: RawDoc,
) -> Result[RawDoc, ErrInfo]:
    if not doc.abstract.strip():
        return Err(
            ErrInfo(
                code="EMPTY_ABSTRACT",
                msg="abstract is required",
            )
        )
    return Ok(doc)
```

Assembly chooses the policy:

```python
strict = toggle_validation(
    True,
    require_abstract,
    normalize,
)

permissive = toggle_validation(
    False,
    require_abstract,
    normalize,
)
```

For invalid input:

- `strict` returns `Err(EMPTY_ABSTRACT)` and does not call `normalize`;
- `permissive` returns the same value as `normalize` and calls it exactly once.

Run the proof:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k validation_toggle_changes_policy_without_duplicating_rag_pipeline
```

The call trace proves skipped and exactly-once evaluation. Result equality
alone cannot establish either claim.

## Read the higher-order function

`toggle_validation` returns a callable:

```python
def toggle_validation(
    enabled: bool,
    validate: Callable[[T], Result[T, E]],
    pipeline: Callable[[T], Result[U, E]],
) -> Callable[[T], Result[U, E]]:
    if not enabled:
        return pipeline

    return lambda value: validate(value).and_then(
        pipeline
    )
```

The branch has not disappeared. It has moved to a place that owns assembly.
After construction, the selected callable has one coherent flow.

Disabled mode returns the original callable object. Enabled mode returns a
wrapper that validates before running the base pipeline.

This design is especially useful when policy changes less often than the
pipeline runs—for example, once per command invocation or application
configuration load.

## Endomorphic validation earns simple composition

The validator has this shape:

```text
T -> Result[T, E]
```

It either rejects the input or returns the same input type. That endomorphic
shape lets the existing `T -> Result[U, E]` pipeline follow under `and_then`.

If validation converts `RawDoc` into a different type, name that stage
according to the conversion rather than forcing it into a generic toggle.

## Logging and metrics change the output shape

The reference state also contains:

```text
toggle_logging:
  (T -> A) -> (T -> Writer[A])

toggle_metrics:
  (T -> A) -> (T -> (A, M))
```

Unlike validation, these wrappers change the public return type. That is a
real API cost. A caller now needs to consume Writer entries or a metrics tuple.

The combinators preserve the base payload:

```text
run(toggle_logging(...)(x)).value == pipeline(x)
first(toggle_metrics(...)(x)) == pipeline(x)
```

Their tests also protect evaluation count by computing the base value once
inside the wrapper.

Run the focused properties:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/test_configurable.py
```

Do not add shape-changing toggles casually. If most callers immediately discard
the extra context, the wrapper may belong at a narrower boundary.

## Wrapper order is behavior

Suppose validation and tracing are both enabled. These orders mean different
things:

```text
trace(validate(pipeline))
validate(trace(pipeline))
```

Questions to decide:

- Should invalid input create a trace entry?
- Should metrics count rejected values?
- Does logging describe attempts or only successful work?
- Which wrapper owns a failure before the base pipeline starts?

Assembly code must make the order explicit and tests must observe it. “All
wrappers are pure” does not make them commutative.

## Use a configuration value without hiding the branch

A small builder can translate configuration into a callable:

```python
@dataclass(frozen=True)
class PipelinePolicy:
    require_nonempty_abstract: bool


def build_normalizer(
    policy: PipelinePolicy,
) -> Callable[
    [RawDoc],
    Result[CleanDoc, ErrInfo],
]:
    return toggle_validation(
        policy.require_nonempty_abstract,
        require_abstract,
        normalize,
    )
```

The domain function does not inspect the configuration. The builder does.

Reader is optional here. If several builders share the same policy environment
and compose as descriptions, Reader may help. For one builder call, an
ordinary parameter is clearer.

## Feature toggles are not always the right product model

Separate deployment configuration may be better when:

- strictness should never change during a process;
- permissive mode is unsafe outside tests or migration;
- different modes have distinct public contracts; or
- a Boolean name does not explain the policy.

A sum type can be clearer than several flags:

```python
type ValidationPolicy = Strict | Permissive
```

The course’s Boolean helper isolates the composition principle. It is not a
recommendation to build an application around many independent feature flags.

## Common wrong turns

- **Passing flags into every domain function.** Policy ownership spreads
  through the core.
- **Duplicating strict and permissive pipelines.** The two copies drift.
- **Claiming there is no branch.** Assembly still makes a policy decision.
- **Changing return shape without updating callers.** Logging and metrics
  wrappers require explicit consumption.
- **Ignoring wrapper order.** Attempts, rejections, and successes may be
  counted differently.
- **Evaluating the base pipeline twice.** Observation changes behavior and
  cost.
- **Using Reader for one configuration argument.** A builder parameter may be
  sufficient.

## What the focused evidence establishes

The learning test proves that one normalization function supports strict and
permissive assembly, strict failure skips normalization, and permissive mode
executes the original behavior exactly once.

The configurable property tests separately establish payload preservation for
the shipped logging and metrics wrappers over their generated inputs.

They do not prove that runtime toggles are the best deployment design, that
wrapper order is irrelevant, or that Writer strings are production logging.

Continue with the [Module 06 Refactoring Guide](refactoring-guide.md) to review
the complete module delta and decide where an explicit context is actually
earned.
