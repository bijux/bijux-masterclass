# Module 02 Exercise Answers

These answers show defensible review routes. Keep your own names when they express
the same ownership and behavior more clearly.

## Answer 1: Classify the API inputs

| Value | Classification | Owner | Why |
| --- | --- | --- | --- |
| `docs` | run input | caller | changes every invocation |
| `RagEnv` | policy data | configuration | chunk and sample sizes |
| `RulesConfig` | policy data | configuration | inspectable keep predicate |
| `CleanConfig` | policy data | configuration | ordered cleaning rule names |
| cleaner | pure capability | composition root | behavior constructed from cleaning policy |
| embedder | pure capability | composition root | replaceable deterministic behavior |
| taps | observation effects | composition root | callbacks mutate external observation state |

Putting a reader in `RagConfig` would mix a live effect capability with comparable
policy. Putting chunk size in dependencies would hide a domain policy among
functions. A useful grouping explains ownership; it does not merely reduce the
parameter count.

The common wrong turn is classifying frozen dataclasses as “pure” and callables as
“impure.” A callable embedder may be pure, while a frozen object can reference
mutable state. Review behavior and ownership.

This table proves a coherent API model on paper. It does not prove the implementations
obey their contracts. The Module 01 compatibility and tap-neutrality tests supply
behavioral evidence.

## Answer 2: Add a cleaning policy

Add one pure function and registry entry:

```python
def casefold_text(text: str) -> str:
    return text.casefold()


RULES: dict[str, TextRule] = {
    # existing rules
    "casefold": casefold_text,
}
```

Keep `DEFAULT_CLEAN_CONFIG` unchanged. Then test direct behavior and composition:

```python
assert casefold_text("Straße") == "strasse"

cfg = CleanConfig(("strip", "casefold"))
assert clean_abstract(" Straße ", cfg) == "strasse"
```

The existing `boundary_rag_config` registry check will accept the new name and still
reject unknown names. If another adapter keeps a separate allowlist, update it or
centralize validation around the same registry.

Common wrong turns:

- replacing `"lower"` in the default changes Module 01 behavior;
- storing `str.casefold` directly in serialized config loses a durable external name;
- converting rule names to a set destroys order;
- catching `KeyError` during cleaning delays boundary validation.

The tests prove deterministic rule behavior, order, and boundary selection. They do
not prove casefolding is the correct retrieval policy for every language. The
architecture keeps that choice in data so application owners can decide.

## Answer 3: Compare rule representations

```python
function_rule = rule_and(
    category_startswith("cs."),
    abstract_min_len(4),
)

predicate_data = All(
    (
        StartsWith("categories", "cs."),
        LenGt("abstract", 3),
    )
)

parsed_rule = parse_rule(
    'd.categories.startswith("cs.") and len(d.abstract) >= 4'
)
```

`LenGt(..., 3)` matches “at least four”; using `LenGt(..., 4)` would require five.
Test all three against the same accepted, wrong-category, and short-abstract
documents.

| Property | Function | Predicate data | Guarded text |
| --- | --- | --- | --- |
| execute directly | yes | through interpreter | after parsing |
| structural equality | no useful value equality | yes | source strings only |
| inspect policy fields | closure introspection only | yes | AST after parsing |
| easy serialization | no | yes with a codec | yes |
| untrusted-input surface | avoid | codec validation | strict parser and whitelist |

The common wrong turn is calling the guarded string “safe Python.” It is a tiny
interpreted language, not arbitrary Python. Another is assuming all three
representations must exist in every application.

Agreement on fixtures proves equivalent behavior for those cases. It does not prove
the languages remain equivalent after adding features. The simplest representation
that satisfies inspection and boundary needs is usually best.

## Answer 4: Prove boundary short-circuiting

Use a reader plus recording core capabilities:

```python
events: list[str] = []


class FailingReader:
    def read_docs(self, path: str):
        events.append("read")
        return Err("source unavailable")


def forbidden_cleaner(doc):
    events.append("clean")
    raise AssertionError("core must not run")


def forbidden_embedder(chunk):
    events.append("embed")
    raise AssertionError("core must not run")
```

Build `RagCoreDeps` with those functions and call `full_rag_api_path`. Assert the
result equals the original `Err` and `events == ["read"]`. A successful reader test
should assert `read` precedes cleaning and embedding.

Also record whether functions passed to `result_map` and `result_and_then` execute.
For `Err`, they must not.

The common wrong turn is wrapping the entire route in `try/except Exception` and
returning one generic error. That hides programmer failures from the test and erases
the expected boundary distinction.

This proves synchronous short-circuiting and preservation of the failure value. It
does not prove retry, resource closure, logging, or asynchronous cancellation.
Those are later policy layers around the same boundary.

## Answer 5: Add neutral stage observation

Store bounded identifiers and counts:

```python
events: list[tuple[str, int]] = []
sample_ids: list[str] = []


def observe_docs(values: tuple[RawDoc, ...]) -> None:
    events.append(("docs", len(values)))
    remaining = max(0, 5 - len(sample_ids))
    sample_ids.extend(doc.doc_id for doc in values[:remaining])


taps = RagTaps(
    docs=observe_docs,
    cleaned=lambda values: events.append(("cleaned", len(values))),
    chunks=lambda values: events.append(("chunks", len(values))),
)
```

Run the same replayable documents with and without taps. Assert complete tuple
equality of `(chunks, observations)`, exact event order, and `len(sample_ids) <= 5`.
The chunk tap count is pre-deduplication; compare it with final
`observations.total_chunks` rather than assuming equality.

Common wrong turns:

- retaining whole `RawDoc` values when IDs answer the question;
- filtering inside a tap;
- appending every observed value to an unbounded list;
- describing a callback that may raise as “non-intrusive.”

The test proves neutrality for the fixture and bounds the local ID sample. It does
not prove identifiers are non-sensitive, callbacks are thread-safe, or external
metrics storage is bounded. Taps remain explicit effect dependencies outside the
pure RAG transformations.

## Final self-review

If a solution proves only final chunk counts, inspect text, metadata, embeddings,
and order. If it proves only pure values, add boundary failure and observation
evidence. Module 02 is complete only when policy values and capabilities make the
same Module 01 application easier to configure and review without changing its
default meaning.
