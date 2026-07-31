# Module 10 Exercise Answers

Use these answers after producing your own evidence. A passing assertion is only
the start of the review: each answer explains the decision, common wrong turns,
what the result proves, and what remains outside the proof.

## Retrieval composition: filter without corrupting rank

Put the threshold beside `text`, `embedding`, and `top_k` because it changes the
meaning of one retrieval request:

```python
@dataclass(frozen=True, slots=True)
class SearchQuery:
    text: str
    embedding: Embedding
    top_k: int
    min_score: float = -1.0

    def __post_init__(self) -> None:
        # existing text, top_k, and embedding checks remain
        if (
            not math.isfinite(self.min_score)
            or not -1.0 <= self.min_score <= 1.0
        ):
            raise ValueError(
                "SearchQuery.min_score must be finite and between -1 and 1"
            )
```

`-1.0` is the cosine lower bound, so the default does not remove any candidate
that the existing similarity contract can produce. A default of `0.0` would be
an unexplained behavior change for valid vectors with negative similarity.

Thread the value through `make_query`:

```python
def make_query(
    text: str,
    *,
    top_k: int = 3,
    min_score: float = -1.0,
) -> SearchQuery:
    return SearchQuery(
        text=text,
        embedding=Embedding(
            vector=embed_text(text),
            model=LOCAL_EMBEDDING_MODEL,
        ),
        top_k=top_k,
        min_score=min_score,
    )
```

Keep scoring, eligibility, ordering, and rank assignment visibly separate:

```python
scored = (
    (cosine_similarity(query.embedding.vector, chunk.embedding), chunk)
    for chunk in chunks
)
eligible = (
    (score, chunk)
    for score, chunk in scored
    if score >= query.min_score
)
ordered = sorted(
    eligible,
    key=lambda item: (
        -item[0],
        item[1].doc_id,
        item[1].start,
        item[1].end,
        item[1].text,
    ),
)

return tuple(
    RankedChunk(chunk=chunk, score=score, rank=rank)
    for rank, (score, chunk) in enumerate(
        ordered[: query.top_k],
        start=1,
    )
)
```

The comparison is inclusive: a candidate exactly on the declared minimum is
eligible. `enumerate` happens after filtering, so the first returned value always
has rank one and no gaps can appear.

Common wrong turns:

- storing the threshold in a CLI or adapter makes core behavior depend on an
  omitted boundary value;
- accepting `NaN` makes every comparison false without explaining why no results
  appeared;
- assigning ranks before filtering can return ranks such as one and three;
- using only `-score` as the sort key reintroduces encounter-order ties;
- calling the threshold a “relevance cutoff” overclaims the hash-vector fixture;
  and
- editing Module 05–09 snapshots rewrites the historical learning states instead
  of extending the live endpoint.

The focused proof establishes validation, inclusive filtering, stable ordering,
contiguous ranks, and backward-compatible default behavior for the supplied
vectors. It does not prove that any threshold separates relevant from irrelevant
language, that the threshold transfers to another embedding model, or that the
implementation is efficient for a large index.

## Systematic refactor: make the starting observation trustworthy

The two configured paths are useful reading routes, but they are not disjoint sets.
`Path.rglob` under `rag/` already discovers files under `rag/domain/`. Summing both
counts therefore treats one source file as two observations.

A defensible implementation gathers resolved Python paths into a set and takes its
length. The configuration stays descriptive while file identity controls counting.

Common wrong turns:

- removing `rag/domain/` hides a useful high-signal review route;
- subtracting the current number of domain files makes the rule depend on today's tree;
- deduplicating path strings before discovery does not help because the parent and
  child strings are distinct.

The test proves that nested configured paths do not inflate the source count. It
does not prove that file count measures quality, complexity, or ownership. It is
only a trustworthy inventory observation.

In FuncPipe, this changes the review shell and leaves the Module 09 RAG contracts
untouched. That is the narrowest safe first refactor: repair the evidence before
using it to justify larger work.

## Performance budgeting: reject a one-dimensional win

The correct decision evaluates all declared dimensions. An observation of
`(latency=60 ms, peak memory=48 MB, throughput=30/s)` fails a budget of
`(80 ms, 32 MB, 25/s)` because memory is over its maximum. The latency and
throughput wins do not compensate for an independent hard limit.

Common wrong turns:

- timing inside the decision function makes tests depend on scheduler noise;
- averaging unlike dimensions invents a meaningless unit;
- returning only `False` hides the evidence needed to choose the next change;
- benchmarking non-equivalent outputs rewards a semantic regression.

The test proves deterministic threshold evaluation and complete violation
reporting for supplied values. It does not prove measurement validity, workload
representativeness, or statistical significance.

In FuncPipe, performance is a selection pressure on already-correct RAG behavior.
The budget can reject an implementation, but it cannot redefine what a valid
`Chunk` or ranked result means.

## Observability: preserve facts without creating hidden policy

Append `StageObservation("rank", processed=3, failures=0, latency_ms=1.5)` to
the observation tuple. The resulting stage order ends in `rank`, processed
increases by three, and latency increases by 1.5 ms.

Common wrong turns:

- raising inside `summarize_observations` when failures are nonzero makes metrics
  an undocumented control-flow boundary;
- storing observations in a module-global list makes tests order-dependent;
- sorting stage names destroys the execution trace;
- accepting more failures than processed records admits an impossible fact.

The test proves deterministic aggregation, validation, and encounter order for
supplied observations. It does not prove that the runtime emitted every event or
that an external telemetry sink delivered it.

In FuncPipe, `Result` still controls application failure. Observations explain what
happened; an explicit policy may later decide whether the evidence blocks a
release.

## Property-based regression: state equivalence in domain terms

Change one successful result's `ChunkMetadata.source`. A batch containing only
that chunk is sufficient to disprove equivalence; Hypothesis does not need a
large corpus because metadata equality is part of the predicate.

Common wrong turns:

- comparing only vector values loses identity and provenance contracts;
- applying `allclose` to identifiers or counts weakens exact domain semantics;
- comparing concrete optimized container types forbids safe implementation changes;
- testing only a hand-picked ASCII sentence misses useful generated cases.

The property proves pure and hybrid embedding parity across the generated text
and batch-size domain. It does not prove the hybrid route is faster, nor does it
cover numeric behavior outside the declared tolerances.

In FuncPipe, the equivalence predicate is the gate before performance evidence.
Optimization may change representation and execution, not the meaning of a RAG
chunk.

## Async property testing: vary pressure without adding real I/O

Increasing the generated concurrency range changes how many plans may be in
flight. It must not change output because `async_gather` records each result by
input index before assembling the final list.

Common wrong turns:

- reusing one coroutine object violates `AsyncPlan` replayability;
- adding arbitrary sleeps makes the test slower without proving the bound;
- asserting only `set(output) == set(input)` loses ordering and duplicates;
- using real services turns a scheduling law into an availability test.

The property proves ordered success for generated immutable values and concurrency
limits. It does not prove cancellation safety, fairness between streams, or which
error wins when several plans fail.

In FuncPipe, async coordination is an effect-shell concern with a precise value
contract. Property generation varies pressure while the RAG semantics stay fixed.

## Advanced patterns and scaling: distinguish three readiness states

Use `BackendStatus(installed=True, compiler_shipped=True)` with verified proofs
that omit `backpressure`. `assess_scaling` reports `("backpressure",)` and both
readiness flags remain false.

Common wrong turns:

- treating import success as compiler implementation repeats the Module 09 error;
- treating compiler implementation as semantic proof skips the hardest review;
- requiring local installation for implementation review confuses code readiness
  with one workstation;
- silently ignoring a missing failure or ordering proof changes RAG semantics.

The test proves classification from supplied status and proof names. It does not
execute a distributed backend or validate an external scheduler.

In FuncPipe, scaling is optional and evidence-gated. The local pipeline remains
understandable and correct even when no distributed dependency is present.

## DDD and FP: assign review ownership without inventing services

`pipelines/configured.py` and `policies/retry.py` are both reviewed through
`orchestration-and-policy`, so `pipeline-runtime` is accountable. If the change
also alters a concrete adapter, `boundary-integrations` joins the review.

Common wrong turns:

- calling every directory a bounded context empties the DDD term of meaning;
- moving files only to match ownership labels destabilizes imports and history;
- assigning one repository-wide owner hides domain-specific judgment;
- encoding current people's names makes the map age quickly.

The test proves that every published package group has one stable ownership label.
It does not enforce approvals or prove organizational authority.

In FuncPipe, the RAG model retains its language and code shape. Ownership tells a
future maintainer who must understand a change, not how many services to deploy.

## Versioning and migration: separate shape from semantics

Adding required `language` yields `requires-migration` because an old value cannot
construct the new contract unaided. A defensible upcaster must receive a declared
default policy or a lookup capability at the shell; silently choosing `"en"`
corrupts documents whose language is unknown or different.

Common wrong turns:

- treating every added field as compatible ignores new constructor obligations;
- treating shape compatibility as semantic proof misses conversion rules;
- mutating the old tag list leaks ownership across versions;
- making the upcaster perform hidden I/O destroys deterministic replay.

The test proves the shipped metadata shape classification and the list-to-tuple
translation. It does not prove JSON, database, or cross-process compatibility.

In FuncPipe, the old contract remains a readable input value and the translator is
explicit. Versioning protects the RAG meaning across time rather than merely
renaming classes.

## Governance: require a claim-to-command route

A useful cleaning claim is:

```python
EvidenceClaim(
    name="cleaning-fixed-point",
    statement="Repeated document cleaning reaches the same value.",
    required_paths=(
        "src/funcpipe_rag/rag/stages.py",
        "tests/unit/rag/test_stages.py",
    ),
    command="pytest -q tests/unit/rag/test_stages.py "
    "-k clean_doc_is_idempotent",
)
```

With only `rag/stages.py` in the observed path set, `assess_evidence` reports
`tests/unit/rag/test_stages.py` missing. With both paths, the route is
discoverable but still not executed.

Common wrong turns:

- linking only to prose makes the claim unauditable;
- calling path presence “passed” confuses discovery with execution;
- using one broad command for every claim makes failures hard to locate;
- claiming semantic relevance from the deterministic ranking fixture exceeds the
  application contract; and
- letting the pure assessor walk the filesystem hides the observation boundary.

The test proves fail-closed completeness from a supplied path set. It does not run
the proof or judge whether the assertion is strong enough.

In FuncPipe, governance routes reviewers to an actual RAG law introduced in
Module 01 and preserved through the live endpoint. The test suite remains the
authority for behavior; the claim catalog makes that authority findable.

## Capstone delivery: compose an honest change dossier

A defensible dossier is:

1. **Claim:** pure and hybrid embedding preserve chunk text, metadata, failure
   position, model, expected dimension, and vector meaning.
2. **Source:** `src/funcpipe_rag/rag/domain/perf.py` owns both the routes and
   `embedding_batches_equivalent`.
3. **Proof:** run
   `pytest -q tests/unit/rag/domain/test_perf_equivalence.py` and the named
   Module 10 learning test.
4. **Applicable decisions:** semantic equivalence, claim completeness, and the
   performance budget apply. Migration and scaling do not.
5. **Result:** equivalence and discoverability pass, but the supplied observation
   exceeds peak memory, so the composed blocker is
   `("performance:peak_memory",)`.
6. **Limit:** the generated strategy and supplied observation do not establish
   representative workload performance or hardware-specific numeric behavior.

The key judgment is to preserve the memory blocker even though latency and
throughput pass. Independent hard constraints are not votes. It is equally
important not to add migration or scaling ceremony to a change that alters
neither contract shape nor execution backend.

Common wrong turns:

- treating a complete `EvidenceClaim` as proof that its command passed;
- accepting the change because two of three performance dimensions pass;
- running a benchmark inside `review_change`, which destroys deterministic replay;
- adding every available assessment to appear thorough;
- reporting only `acceptable=False` and losing the reason; and
- claiming that one generated property covers every input or environment.

`test_change_review_composes_only_applicable_application_evidence` proves that
already-classified application evidence composes into the expected blocker.
`test_change.py` proves independent blockers retain review order and irrelevant
checks may be absent. `make review-check` proves only that the published source
and test paths exist.

None of these commands proves that the 48 MB observation came from a representative
benchmark. A real optimization decision still needs a declared workload and an
effectful measurement route. The pure review model keeps that uncertainty visible
instead of pretending to resolve it.

In FuncPipe, capstone delivery is the learner's ability to connect one precise
application claim to source, executable proof, applicable decisions, an observed
result, and a stated limit. The local RAG application is the product being
reviewed; no invented production platform is required.
