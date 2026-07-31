# FuncPipe Capstone Glossary

These terms have precise meanings in the capstone. Use them when tracing code, writing an
exercise answer, or reviewing a change. The definitions do not replace the module
lessons; they prevent the same word from silently changing meaning across the cumulative
application.

## Application and course evolution

| Term | Meaning in FuncPipe |
| --- | --- |
| capstone delta | the explainable difference between consecutive application states: capability before, new pressure, changed source, new proof, and preserved behavior |
| reference state | tracked source and tests representing the completed endpoint of one module, available for Modules 01–09 |
| generated history worktree | a derived comparison checkout under `capstone/_history/worktrees`; it is regenerated and verified, not edited as source |
| live endpoint | `capstone/src` and `capstone/tests`, representing the cumulative Module 10 application |
| learning test | an executable, reader-oriented test that connects a module’s concept to an application behavior and earlier promises |
| cumulative proof | all learning tests present in one reference state, including preserved tests from earlier modules |
| preserved law | a behavior introduced earlier that later states must continue to satisfy, such as cleaning idempotence or bounded demand |

## RAG values and flow

| Term | Meaning in FuncPipe |
| --- | --- |
| `RawDoc` | document input before deterministic cleaning |
| `CleanDoc` | document value whose abstract has passed the configured normalization rules |
| `ChunkWithoutEmbedding` | bounded text span with document identity and offsets, before vector calculation |
| `Chunk` | chunk value carrying a deterministic local embedding and metadata |
| `RagConfig` | immutable policy data for environment, keep rules, cleaning, and debugging |
| `RagCoreDeps` | explicit cleaner, embedder, and optional observation taps used by RAG transformations |
| `RagBoundaryDeps` | core dependencies plus the reader capability needed by path-based APIs |
| streaming | values are requested incrementally from an iterator rather than collected before processing |
| bounded demand | a consumer requesting `n` outputs does not cause unexplained traversal of the entire upstream source |
| materialization | deliberate conversion of an iterable into a complete in-memory collection at a named boundary |
| structural deduplication | removing duplicates according to stable chunk structure and ordering, not object identity |
| deterministic embedding | local embedding whose value is reproducible from the same chunk text; it creates no network dependency |

## Functional control and failure

| Term | Meaning in FuncPipe |
| --- | --- |
| pure function | a function whose returned value depends only on explicit inputs and which performs no externally observable effect during evaluation |
| referential substitution | replacing a pure expression with its value without changing program behavior |
| `Result` | an explicit `Ok` or `Err` value used for expected application failure flow |
| `Option` | explicit presence or absence; absence is not automatically an error |
| `ErrInfo` | stable failure data such as code, stage, path, context, and preserved cause |
| fold | consumption of a structure into an accumulated value according to an explicit combining rule |
| fail-fast fold | a fold that stops demand at the first `Err` |
| accumulating validation | independent validation that retains multiple errors instead of short-circuiting on the first |
| fixed point | a value for which applying a transform again produces the same value; `clean_doc` is tested for this property |
| idempotent effect | an effect arranged so replay does not create an additional externally visible result |

## Effects and architecture

| Term | Meaning in FuncPipe |
| --- | --- |
| capability | a narrow protocol naming one external operation the application requires |
| effect plan | a value or delayed computation describing effectful work before a shell executes it |
| shell | the runtime edge that selects dependencies, invokes plans or adapters, and translates process input/output |
| adapter | implementation that translates a concrete runtime or library contract into a capability or domain value |
| boundary | the owned location where untyped, effectful, or foreign behavior becomes a stable application contract |
| policy | a decision expressed from explicit inputs, such as a retry classification, resource bound, or performance budget |
| backpressure | coordination that prevents producers from outrunning a bounded consumer or queue |
| fairness | a scheduling property that keeps one source or task from indefinitely excluding another |
| interoperability seam | named translation between FuncPipe values and stdlib, library, dataframe, CLI, or distributed representations |

## Evidence and sustainment

| Term | Meaning in FuncPipe |
| --- | --- |
| evidence claim | a named statement paired with required source paths, test paths, and a verification command |
| route available | every path declared by an evidence claim exists; this does not mean the command executed |
| executed proof | a command ran against the intended source and its observations satisfied the selected assertions |
| semantic equivalence | two implementations preserve the explicitly named domain behavior, not necessarily identity, speed, or internal structure |
| performance budget | acceptable limits for relevant dimensions such as latency, peak memory, and throughput |
| performance observation | already-measured values compared with a budget by a pure decision function |
| migration assessment | classification of public contract shape change, kept separate from semantic translation or upcasting evidence |
| applicable check | a proof category required by the actual proposal; an inapplicable check may be absent rather than fabricated |
| `ChangeEvidence` | immutable collection of already-classified semantic, claim, budget, and migration facts for one proposal |
| `ChangeDecision` | deterministic acceptance value containing `acceptable` and stable blocker names |
| blocker | a specific failed applicable check, such as `performance:peak_memory`; it is more actionable than a generic rejection |
| proof bundle | generated review material under `artifacts/` containing test output, inventories, guides, and a manifest |

## Distinctions worth preserving

| Do not collapse | Why |
| --- | --- |
| absence and failure | `Option` and `Result` answer different questions |
| lazy flow and async flow | laziness controls demand; async controls scheduling; either can exist without the other |
| capability and adapter | the domain owns the need; infrastructure owns one implementation |
| description and execution | an effect plan can be composed before a shell performs it |
| route availability and test success | file discovery cannot report an execution result |
| semantic equivalence and performance | equal values can still violate memory or latency budgets |
| compatibility and migration correctness | shape classification does not prove translated values preserve meaning |
| reference state and live endpoint | the live code contains concepts an earlier module has not taught |

When a review becomes vague, replace words such as “works,” “robust,” “advanced,” or
“production-ready” with one of the observable contracts above and name its proof.
