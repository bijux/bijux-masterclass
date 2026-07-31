# Module 06 Refactoring Guide: Earn Each Context

Module 06 should not end with every FuncPipe function wrapped in Reader, State,
Writer, or Result. It should end with clearer ownership:

- domain functions own domain transformations;
- containers own explicit propagation rules;
- adapters classify expected throwing behavior;
- builders choose optional policy; and
- tests compare the observations that matter.

Use this guide to review one flow from the Module 06 reference state before
moving to effect boundaries in Module 07.

## Begin with the direct route

For valid inputs, the direct RAG path is already clear:

```python
cleaned = clean_doc(raw)
chunks = [
    embed_chunk(chunk)
    for chunk in iter_chunk_doc(cleaned, env)
]
```

Do not replace it to demonstrate vocabulary.

A Result-preserving path becomes relevant when `raw` already arrived inside a
typed outcome:

```python
refactored = (
    source
    .map(clean_doc)
    .map(
        lambda doc: list(
            iter_chunk_doc(doc, env)
        )
    )
    .map(
        lambda chunks: [
            embed_chunk(chunk)
            for chunk in chunks
        ]
    )
)
```

Every function under `map` is plain and infallible for the modeled input. If a
new dependent prerequisite returns `Result`, only that operation moves under
`and_then`.

## Prove the complete output

The final Module 06 learning property generates abstract text and valid chunk
sizes. It compares:

```text
direct list[EmbeddedChunk]
Ok(direct list[EmbeddedChunk])
```

with the mapped Result route.

Run it:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k explicit_flow_refactor_preserves_rag_chunk_output
```

Complete chunk equality protects:

- document identity;
- normalized text;
- chunk boundaries and offsets;
- output order; and
- deterministic embeddings.

Comparing only list length would allow incorrect text, offsets, order, or
embedding values to pass.

The exercise extends the generator with valid overlap values. Generate
`chunk_size` first, then constrain overlap to
`0 <= overlap < chunk_size`. Otherwise the property tests constructor
rejection rather than equivalence of two valid routes.

## Use a context ledger

Before introducing an abstraction, complete one row:

| Pressure | Smallest honest option | When the Module 06 type earns its place | Evidence |
| --- | --- | --- | --- |
| one plain success transformation | direct call or `map` | the value already lives inside a context | complete contextual equality |
| dependent fallible step | explicit branch | repeated propagation obscures the domain flow | first error and skipped-work trace |
| independent contextual inputs | explicit pattern match | the same combination structure repeats | success and declared error order |
| shared read-only context | ordinary argument or configured closure | several descriptions share and compose over one environment | same program, controlled environments |
| local changing value | tuple or fold | reusable dependent operations thread the same state | value, final state, unchanged initial state |
| ordered side data | tuple or domain record | several operations append while preserving one payload | payload equality and exact entry order |
| throwing adapter | local `try` | callers need a typed recoverable outcome | expected mapping and unexpected propagation |
| optional policy | direct builder branch | one base callable needs reusable wrappers | enabled, disabled, and evaluation-count proofs |

If the “smallest honest option” is clearer, keep it.

## Review layer order separately

When a flow contains more than one context, write the complete type:

```text
Result[Option[CleanDoc], ErrInfo]
Writer[Result[EmbeddedChunk, ErrInfo]]
State[Progress, Result[Chunk, ErrInfo]]
```

Then answer:

- Which decision happens first?
- Does an error retain earlier state or trace entries?
- Is absence successful?
- What must the caller pattern-match?
- Can every represented combination occur?

Do not hide these choices behind a generic “effect stack” description.

## Characterize boundaries before changing them

For a `try`/`except` refactor:

1. record the old success and error values;
2. name the exact expected exception class;
3. wrap the smallest throwing expression;
4. compare complete results;
5. prove a different exception still raises; and
6. make domain validation a separate pure step.

This keeps parser behavior, validation policy, and control-flow structure in
reviewable changes.

## Read the Module 05 to 06 delta in ownership order

After running `make history-refresh` from the course directory:

1. inspect new files under
   `capstone/_history/worktrees/module-06/src/funcpipe_rag/fp/effects/`;
2. inspect
   `boundaries/adapters/exception_bridge.py`;
3. inspect changed exports only to see what became public;
4. run
   `tests/learning/test_module_06_explicit_context.py`;
5. inspect the matching law files; and
6. confirm the same learning test remains in Modules 07–09.

This route avoids treating widespread `__init__.py` or formatting differences
as new application behavior.

## Separate three kinds of evidence

| Evidence | Supports | Does not support |
| --- | --- | --- |
| container law property | legal structural regrouping | RAG policy correctness |
| focused learning test | one named application behavior | every possible input or deployment |
| before/after equivalence property | preservation over a generated domain | superiority of the new design |

A refactor needs both preservation evidence and a readability or ownership
reason. Equality alone proves the rewrite did not change the tested behavior;
it does not prove the additional abstraction is worthwhile.

## Module exit review

Take one changed flow and explain it without using the word *monad*:

- what value enters;
- what can stop the flow;
- what context the caller supplies;
- what local value changes;
- what side information is returned;
- which exception is expected;
- what exact RAG output remains unchanged; and
- which test supports each statement.

Then explain where an ordinary function, argument, fold, or tuple would be
clearer.

You are ready for Module 07 when you can distinguish describing context from
executing effects. Reader can describe a computation that depends on a value;
Writer can return trace data; neither one opens, closes, retries, or emits an
external resource. Module 07 assigns those responsibilities to capabilities,
ports, adapters, and resource-safe shells.
