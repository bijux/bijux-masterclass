# Laboratory 2 — Profile-Guided Query Engine

[Common laboratory method](../../../START_HERE.md#laboratory-method) · [Module 82 chapter](../../course-book/module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md)

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

