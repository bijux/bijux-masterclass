# Module 05 Glossary

Use this page when two related terms begin to blur together. The definitions
refer to the FuncPipe code in Module 5; they are not intended as universal
one-line definitions for every functional language.

## Value shapes

| Term | Meaning in this module | FuncPipe example |
| --- | --- | --- |
| algebraic data type (ADT) | a type assembled from product and/or sum shapes | `Result[T, E]`, `ChunkWithoutEmbedding` |
| product type | all named components exist together—an “and” shape | a chunk has document ID **and** text **and** offsets |
| sum type | exactly one of a known set of alternatives—an “or” shape | `Ok[T] | Err[E]` |
| variant | one member of a sum | `Ok` is a `Result` variant |
| invariant | a condition that every valid value or operation must preserve | an indexed pipeline chunk has 16 embedding values |
| impossible state | a contradictory combination excluded by the type design | a value cannot be both `Ok` and `Err` |

## Pipeline states and focused models

| Term | Meaning in this module |
| --- | --- |
| stage product | a product whose fields express what is known at one application stage; `ChunkWithoutEmbedding` and `Chunk` distinguish before and after embedding |
| stage transition | a function whose input/output types expose the guarantee added; `embed_chunk: ChunkWithoutEmbedding -> Chunk` |
| pipeline `Chunk` | `core.rag_types.Chunk`, the cumulative RAG application's indexed text span |
| `AssembledChunk` | the separate focused `rag.domain` product used to teach cross-field assembly and representation equivalence |
| assembler | the integration function that sees several subsystem values and owns their cross-field rules |
| local invariant | a rule one product can enforce using only its own data; `Embedding` can reject non-finite vector entries |
| cross-field invariant | a rule requiring more than one product; `assemble` checks metadata expectations against an embedding |

`AssembledChunk` does not mean “a newer pipeline chunk.” The distinct name is
intentional: it marks a focused lab with different fields and ownership.

## Contexts and operations

| Term | Meaning in this module |
| --- | --- |
| `Option[T]` | explicit presence (`Some[T]`) or absence (`NONE`) |
| `Result[T, E]` | a successful value (`Ok[T]`) or one fail-fast error (`Err[E]`) |
| `Validation[T, E]` | a successful value or a non-empty tuple of accumulated independent errors |
| functor | a context with lawful mapping: transform its inner value while preserving the context |
| `map` | apply `T -> U` inside a context; `result_map` changes `Ok[T]` and passes `Err` through |
| applicative validation | combination of independently validated inputs so a constructor runs on success and all failures accumulate |
| sequencing | dependent composition where the next operation requires the previous successful value |

The important distinction is dependency. Use `Result` sequencing when work
cannot continue after a failure. Use applicative `Validation` when checks can
run independently and complete feedback is valuable.

## Aggregation

| Term | Meaning in this module |
| --- | --- |
| semigroup | an associative combine operation for one or more values |
| monoid | a semigroup plus an identity, allowing zero or more values |
| associativity | regrouping preserves the intended answer: `(a <> b) <> c == a <> (b <> c)` |
| identity | a value that leaves any valid value unchanged on both sides |
| commutativity | reordering preserves the answer; not required for a monoid |
| fold | traverse values while combining them from an identity |

Floating-point addition is not exactly associative under IEEE-754 rounding.
`METRICS` is a useful domain aggregate, but its name does not make arbitrary
parallel regrouping bit-identical.

## Boundaries and persistence

| Term | Meaning in this module |
| --- | --- |
| boundary model | a representation that validates untrusted external input before conversion; `ChunkModel` is a Pydantic boundary model |
| core value | an ordinary domain value used after boundary conversion |
| codec | paired functions that deliberately encode and decode a supported value domain |
| envelope | serialized `tag`, `ver`, and `payload` fields around a value |
| discriminator | a field identifying a sum variant; `payload.kind` distinguishes `ok` from `err` |
| migration | a deterministic conversion from one known envelope version to another |
| round trip | decode after encode returns an equal supported value |
| provenance | operational failure context such as code, stage, and path |

A round-trip claim is always scoped to the codec's supported values. The
default `ErrInfo` codec preserves code, message, stage, and path; it does not
preserve arbitrary exception causes or context objects.

## Representation and evidence

| Term | Meaning in this module |
| --- | --- |
| reference representation | the clearest implementation against which another path is compared |
| optimized representation | an internal shape chosen for a measured performance reason |
| equivalence ledger | the explicit list of observables two representations must preserve |
| semantic equivalence | equality of the declared public observables, not necessarily identical internal layout |
| numeric tolerance | documented allowed floating-point difference, such as `rtol` and `atol` |
| correctness evidence | tests that compare outputs, variants, order, identity, metadata, or laws |
| performance evidence | benchmarks or profiles that measure time, allocation, or memory on representative data |

Property tests can strengthen equivalence evidence. They do not prove a path is
faster. Benchmarks can show a speed difference. They do not prove domain
meaning was preserved.

Return to the [Module 05 index](index.md) for the reading route or
[Exercises](exercises.md) to apply these distinctions.
