# Module 05 Exercises

These exercises change or inspect the Module 05 FuncPipe RAG reference state.
Work in the declared core order because later prompts assume the earlier value
and construction distinctions are already explicit.

Before opening an answer:

1. write the legal and illegal states;
2. predict the complete value, error tuple, or transition;
3. run the named learning test;
4. state which Module 04 behavior must remain true; and
5. record what the evidence cannot establish.

Use this focused command shape from the course root:

```bash
cd capstone/module-reference-states/module-05
PYTHONPATH=src pytest -q tests/learning/test_module_05_data_modelling.py \
  -k NAME_FROM_THE_EXERCISE
```

## Product and sum types: account for the real chunk values

Run `test_rag_product_types_keep_chunk_fields_together` and
`test_result_sum_type_separates_embedding_success_from_failure`. Draw the
product shape of `ChunkWithoutEmbedding`, then write a function that accepts
`Result[Chunk, ErrInfo]` and reports either the chunk span or the failure stage.

Constraints: use the existing `Ok | Err` sum; do not add a success flag,
nullable error, or parallel chunk class; match both variants explicitly;
preserve Module 04 chunk identity and offsets. Evidence must include one
successful span, one failure stage, and an attempted metadata mutation.

## Domain states: prove the existing transition

Run `test_rag_stage_types_make_embedding_transition_explicit`. Starting with
one `RawDoc`, record the value and type after cleaning, chunking, and embedding.
Add assertions for every field that embedding must preserve.

Constraints: use `clean_doc`, `chunk_doc`, and `embed_chunk`; do not add
`Pending`, `Running`, or timestamp events; do not mutate the earlier values;
use an embedding dimension failure as the illegal final-state example.
Evidence must show the three stage types, preserved identity/text/offsets, the
unchanged raw abstract, and the rejected malformed `Chunk`.

## Functors: transform success without touching failure

Run `test_result_functor_transforms_success_without_running_failure_work`.
Map a pure word-count projection over a cleaned document result.

Constraints: preserve the exact `ErrInfo` object; record function calls; do not
inspect `.value` outside the functor operation. Evidence must show one mapped
success and a failure trace with no function call.

## Applicative validation: report independent problems together

Run `test_applicative_validation_accumulates_independent_chunk_errors`. Add an
independent source check to the text and embedding checks.

Constraints: evaluate every independent check; retain declared error order; do
not use `and_then`; keep `VFailure` non-empty. Evidence must show all three
errors for one input and one fully constructed value.

## Monoids: aggregate chunk evidence lawfully

Run `test_monoid_fold_aggregates_chunk_metrics_with_empty_identity`. Extend the
metric with a rejected count and aggregate two partitions.

Constraints: define an honest empty value; use an associative combine; compare
left and right regroupings; keep maximum latency distinct from summed latency.
Evidence must include the empty fold and both regroupings.

## Pydantic at the boundary: preserve a complete indexed chunk

Run `test_pydantic_adapter_rejects_invalid_embedding_before_core_conversion`.
Validate a complete `ChunkModel`, convert it to the domain `Chunk`, then
convert, serialize, and deserialize it back to the boundary model.

Constraints: keep Pydantic out of the core dataclass; include document ID,
text, offsets, metadata, and 16 finite values; reject extra fields; compare the
complete round-trip value. Evidence must also include one offset mismatch and
one wrong-dimension rejection before domain conversion.

## Pattern matching: consume every declared result variant

Reuse the `Result[Chunk, ErrInfo]` reporter from the first exercise. Replace
any wildcard branch with explicit `Ok` and `Err` patterns followed by
`assert_never`.

Constraints: destructure fields in each case; return stable public labels; do
not inspect a nonexistent success flag; do not add a catch-all string.
Evidence must cover both declared variants and include the type-check command
that would detect a forgotten future variant.

## Serialization: preserve typed failure provenance

Run `test_serialization_preserves_result_failure_provenance`. Round-trip a
failure with a non-empty stage and path, then corrupt the envelope version.

Constraints: use the shipped encoder and decoder; compare the complete
`ErrInfo`; reject the unknown version; do not serialize `repr`.
Evidence must include the JSON envelope and the rejection.

## Compositional domain models: own cross-field checks at assembly

Run `test_domain_assembly_reports_all_embedding_mismatches`. Add a metadata
normalization rule while retaining model and dimension checks.

Constraints: subsystem records stay independent; `assemble` owns cross-field
checks; duplicate tags normalize stably; invalid input returns both mismatch
errors in order. Evidence must include valid and invalid assembly.

## ADT performance: compare public observables

Run `test_hybrid_embedding_preserves_pure_rag_observables`. Add a second chunk
and compare the pure and hybrid batch routes.

Constraints: preserve chunk identity and order; compare text, metadata, model,
and vector values; declare numeric tolerance; do not benchmark inside the
correctness test. Evidence must show equivalence for the full batch.

## Refactoring guide: keep the accepted-input contract

Run `test_boundary_refactor_preserves_accepted_chunk_values`. Characterize a
small legacy dictionary adapter, then replace it with `ChunkModel` plus
`to_core_chunk`.

Constraints: compare complete values for accepted inputs before deleting the
legacy path; add one malformed input the new boundary rejects; do not change
normalization policy during the refactor. Evidence must separate equivalence
from the newly enforced rejection.
