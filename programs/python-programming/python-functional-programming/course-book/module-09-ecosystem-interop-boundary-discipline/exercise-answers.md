# Module 09 Exercise Answers

Use these answers after producing your own evidence. The point is to compare
reasoning, not only final output.

## Standard library tools: prove laziness before preferring a helper

`merge_streams` returns `itertools.chain(*streams)`. Constructing the chain does not
ask any source for a value. A pull log owned by the source generator therefore
stays empty until the consumer calls `next`.

A defensible extension is:

```python
merged = merge_streams(source("left", (1,)), source("middle", (2,)), source("right", (3,)))

assert pulls == []
assert next(merged) == 1
assert pulls == [("left", 1)]
assert next(merged) == 2
assert pulls == [("left", 1), ("middle", 2)]
```

The important decision is to test an observable consumption contract. Testing
that the return value happens to be an `itertools.chain` would freeze an
implementation detail while proving nothing about future wrappers.

Common wrong turns:

- `list(merge_streams(...))` proves order but destroys the laziness evidence.
- counting generator construction as consumption confuses creating an iterator
  with advancing it.
- using `tee` for this exercise introduces a cache and a different memory
  question.

The result proves deferred, ordered consumption for the tested sources. It does
not prove constant memory for every stdlib iterator composition; `tee`, for
example, can buffer an unbounded skew between consumers.

In the application architecture, this keeps document ingestion on the lazy side
of the boundary. Later adapters may supply documents, but they do not gain
permission to materialize the whole corpus.

## Helper libraries: require semantic parity

The compatibility module is the public boundary. Calling `toolz` directly from
RAG stages would make installation state part of domain behavior. The exercise
therefore composes only the compatibility functions and asserts the same plain
Python result: `[5, 4]`.

The defensible dependency decision is conditional. Enable `toolz` when a team
already understands its left-to-right vocabulary and repeated pipelines become
easier to review. Keep the fallback when the helper only replaces a readable
generator expression with unfamiliar syntax.

Common wrong turns:

- testing `TOOLZ_AVAILABLE` instead of output tests installation state, not the
  contract
- returning a `toolz`-specific container leaks the library into the core
- materializing after every stage preserves values but abandons streaming

The result proves parity for the exercised compose, filter, map, and pipe route.
It does not prove every `toolz` operator has a compatible fallback. Each added
operator needs its own boundary contract.

In FuncPipe, the facade protects `RawDoc` and `Chunk` flows from optional-library
types. Removing the dependency should be a packaging decision, not a RAG rewrite.

## Data processing: separate record normalization from dataframe choice

The shipped `normalize_records` helper treats a missing abstract as `""`. That is
a normalization policy for permissive ingestion, not schema validation. A strict
HTTP or file adapter may reject the row before this helper runs.

A defensible test adds `{"doc_id": "paper-2"}` and expects
`clean_abstract == ""`, while also asserting the original dictionary still has no
new key. The copy `{**row, "clean_abstract": clean}` is the ownership boundary
that prevents caller mutation.

Common wrong turns:

- installing pandas to test a rule that is independent of dataframe semantics
- asserting only the cleaned text and missing the mutation contract
- silently dropping unrelated columns, which makes the adapter lossy

The result proves idempotent record normalization and non-mutation for ordinary
dictionary inputs. It does not prove pandas, Polars, and Dask have identical null,
string, or category semantics. Those need optional integration tests when a
specific backend is supported.

In FuncPipe, record normalization prepares boundary data. Construction of
`RawDoc` and rejection of invalid domain values remain explicit later decisions.

## Web and services: translate before invoking the framework

`parse_document_payloads` is deliberately framework-free. It translates mappings
into `RawDoc` values and returns `ErrInfo(code="INVALID_DOCUMENT", ...)` when a
required field or `categories` is not a string.

The shell may map that code to HTTP 422, but the translator must not know that
status code. The same translator can then serve FastAPI, a batch import endpoint,
or a direct unit test.

Common wrong turns:

- relying only on a Pydantic exception makes the framework own the failure model
- catching every exception and returning HTTP 500 hides a caller error
- running chunking or embedding in the payload translator mixes transport and
  application work

The result proves deterministic translation and typed validation for mapping
payloads. It does not prove routing, JSON decoding, authentication, or response
serialization; those remain framework integration concerns.

In FuncPipe, the HTTP shell translates, calls the established pipeline, and maps
the resulting value back out. It never becomes an alternative RAG core.

## Data and ML pipelines: validate topology before consuming data

`build_rag_pipeline` checks a small type-state sequence while walking the
configuration. `clean → embed` fails because embedding requires chunks.
`clean → chunk` passes the local adjacency checks but fails the final rule that a
pipeline must end at a `Result`-returning effect boundary.

The valid configuration is:

```python
PipelineConfig(
    steps=(
        StepConfig("clean"),
        StepConfig("chunk", {"chunk_size": 256, "overlap": 32}),
        StepConfig("embed"),
    )
)
```

Common wrong turns:

- using `size` instead of the shipped `chunk_size` key leaves the example
  disconnected from executable code
- discovering stage order only after processing documents wastes work and blurs
  configuration failures with data failures
- storing a live embedder in serializable config confuses data with resources

The result proves build-time topology validation and zero source consumption on
the tested invalid route. It does not prove an injected model is deterministic;
the boundary owner must pin and test that artifact.

In FuncPipe, config selects pure stages while the artifact mapping supplies
resources. That separation lets CLI and service shells reuse one builder.

## CLI and config: make misspelled overrides fail closed

`parse_override` is responsible only for turning dotted text into nested data.
`apply_step_params` owns the separate question of whether a step target exists.
Keeping those decisions separate makes each failure precise.

The correct update returns a new `PipelineConfig`; the frozen original remains at
512. A misspelled step raises `ValueError("unknown pipeline step: chnuk")` because
an unchanged successful result would mislead the operator into believing the run
used the requested configuration.

Common wrong turns:

- mutating `StepConfig.params` breaks value semantics and makes repeated CLI runs
  history-dependent
- accepting unmatched targets hides operational mistakes
- letting `argparse` or Typer perform deep merge logic makes the policy hard to
  reuse and test

The result proves precedence, non-mutation, and unknown-target rejection for the
shipped dotted override route. It does not prove shell quoting or environment
variable behavior; those belong in entrypoint integration tests.

In FuncPipe, the CLI is a translator from strings to `PipelineConfig`. The same
builder used by services and tests remains the application authority.

## Distributed dataflow: report capability without pretending to compile

`backend_statuses` separates two facts. `installed` describes the current Python
environment. `compiler_shipped` describes repository behavior and remains false
for both Dask and Beam. Neither fact by itself is verification.

A future compiler must run the same `PipelineSpec` through a local semantic
interpreter and the backend's local runner, then compare values, typed failures,
ordering rules, and materialization boundaries under an explicit equivalence
policy.

Common wrong turns:

- treating a successful import as a working adapter
- writing `NotImplementedError` tests that depend on which packages happen to be
  installed
- claiming distributed speed without a representative workload and cost model

The result proves honest capability reporting. It does not prove any distributed
execution behavior because the repository intentionally ships no compiler.

In FuncPipe, the seam is valuable precisely because it prevents backend concerns
from entering the core before a real scaling pressure and proof budget exist.
