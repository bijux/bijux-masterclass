# Laboratory 82 — Profile-Guided Query Engine

**Course 9 · Module 82: CPU Profiling, Cost Models, and Hot-Path Optimization**

[Chapter](../../course-book/module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md) · [Workbook](../../course-book/module-82-cpu-profiling-cost-models-and-hot-path-optimization/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **CPU Profiling, Cost Models, and Hot-Path Optimization**: Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase? The product must make **Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **profile and cost model** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a document query engine with two semantically equivalent paths: a linear reference search and an indexed search. The product’s purpose is to expose **why** work changes. Clock timings may be collected later, but the required evidence is a set of domain counters that remains meaningful even on a noisy machine.

A `Document` has a stable ID and body. A query matches complete whitespace-separated tokens and returns borrowed documents in original source order. `QueryEngine::build` owns the documents and constructs whatever index you choose. Every query returns results plus `QueryCounters` recording documents considered, candidates examined, and token comparisons.

## Invariants

Both paths must:

- implement exactly the same token definition;
- preserve document source order;
- return each matching document at most once;
- borrow results from the engine rather than clone documents;
- handle repeated query terms and repeated tokens correctly;
- keep index construction separate from query cost;
- expose enough counters to explain a win or loss.

The index may narrow candidates, but it may not silently change case sensitivity, punctuation rules, ordering, or duplicate behavior.

## Construction route

1. Write or preserve the linear search as the semantic oracle.
2. Define counters before choosing the index. They should correspond to terms in a cost model, not implementation trivia.
3. Build an index from token to source indices. Use deterministic structures or explicitly restore source order.
4. Query the index, deduplicate candidate indices where necessary, and verify candidate documents using the same token predicate as the oracle.
5. Return borrowed `&Document` values.
6. Compare oracle and indexed results across many corpora and terms.
7. Record build work/memory separately from per-query work.

## Workload family

Create corpora that vary independently:

- document count;
- tokens per document;
- query selectivity;
- repeated-token frequency;
- number of repeated queries;
- updates or rebuilds, if you extend the product.

Include a tiny corpus with one query, a large corpus with a selective term, a common term matching most documents, and a term absent from the corpus. The index should not be forced to win every case.

## Profiling questions

Before editing, predict whether cost is dominated by tokenization, hashing, candidate verification, result construction, or index build. After implementation, use counters to test the prediction. If available, profile a release build and map sampled stacks to the counter model. A wide `query` frame is not enough; inspect descendants and call count.

## Adversarial cases

Test empty documents, empty query terms according to the declared contract, duplicated IDs if they are legal/illegal, repeated tokens within one document, one term in every document, and source IDs deliberately out of numeric order. The result order follows source position, not ID or hash order.

## Transfer

Add a phrase query or case-normalized query without changing the existing token contract. First extend the semantic oracle, then the cost model, then the index. State whether the new requirement makes precomputation, memory, or update cost dominate.

## Completion

The laboratory is complete when both implementations are behaviorally equivalent, counters expose causal work, build cost is not hidden, and your report identifies a crossover rather than declaring one universal winner.

Inspect `solution/` only after completing the oracle, index, and counters. Compare the model terms, not the concrete map type. A different index is valid if it preserves the contract and provides equally causal evidence.

## Required causal report

Your report must include a cost equation for both query paths, not just counter dumps. Define every term and show at least four workload points where the dominant term changes. For one selective and one common query, present the candidate set, verification work, and final ordered result. If you use a sampling profiler, attach the shipped release profile and reconcile its stacks with the domain counters; explain any disagreement.

Finish with an optimization decision. State whether to keep the index, make it optional, rebuild it under a threshold, or reject it. The decision must account for build time, retained memory, update frequency, repeated-query rate, and semantic complexity. “The indexed path is faster” is not enough when the corpus is small or frequently rebuilt.

## Acceptance experiment

Run the same query sequence through the oracle and indexed implementation after every corpus mutation. Compare stable document IDs, source ordering, and result multiplicity before comparing counters. Include a workload where the index is predictably worse because construction dominates, and a repeated selective workload where it should reduce candidate verification. The final report must state the measured crossover and the assumptions that would move it; do not turn one corpus into a universal performance claim.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Profile-Guided Query Engine**.
2. Draw the smallest **profile and cost model** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked.
- Read call stacks and flame graphs without confusing inclusive cost with exclusive cost.
- Separate algorithmic work from parsing, allocation, hashing, formatting, synchronization, and system calls.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 82 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **profile and cost model**. Defend why your design is simpler than one plausible alternative under the new requirements.
