# Course 4 Study Plan — Functional Rust

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **How can Rust make capture, traversal, cardinality, ordering, failure, accumulation, structural sharing, effects, and cost visible in one dataflow?** answerable through construction and explanation.

## Daily rhythm

Use a **whole-pipeline architecture map** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 31: Closures, Capture, and Callable Contracts

**Question:** What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?

**Retrieval:** Without notes, restate the invariant carried from Module 30 — Architectural Synthesis. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 31](./module-31-closures-capture-and-callable-contracts/index.md) with a **closure capture map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-31-closures-capture-and-callable-contracts/workbook.md) before observation. The day’s minimum result is: **Distinguish function items, function pointers, and anonymous closure types.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Closure Policy Matrix](../labs/module-01-closure-policy-matrix/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 31 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish function items, function pointers, and anonymous closure types.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 32: The Iterator Model

**Question:** What state does an iterator own, when does work happen, and what is consumed by each call to next?

**Retrieval:** Without notes, restate the invariant carried from Module 31 — Closures, Capture, and Callable Contracts. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 32](./module-32-the-iterator-model/index.md) with a **iterator state trace** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-32-the-iterator-model/workbook.md) before observation. The day’s minimum result is: **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Lazy Log Query](../labs/module-02-lazy-log-query/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 32 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 33: Iterator Algebra and Pipeline Shape

**Question:** How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?

**Retrieval:** Without notes, restate the invariant carried from Module 32 — The Iterator Model. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 33](./module-33-iterator-algebra-and-pipeline-shape/index.md) with a **pipeline shape table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-33-iterator-algebra-and-pipeline-shape/workbook.md) before observation. The day’s minimum result is: **Derive the item type and cardinality effect of common iterator adapters.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Record-Shaping Pipeline](../labs/module-03-record-shaping-pipeline/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 33 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Derive the item type and cardinality effect of common iterator adapters.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 34: Folds, Scans, and Short-Circuiting

**Question:** What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?

**Retrieval:** Without notes, restate the invariant carried from Module 33 — Iterator Algebra and Pipeline Shape. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 34](./module-34-folds-scans-and-short-circuiting/index.md) with a **accumulator invariant** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-34-folds-scans-and-short-circuiting/workbook.md) before observation. The day’s minimum result is: **Design a fold accumulator with a precise prefix invariant.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Streaming Metrics](../labs/module-04-streaming-metrics/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 34 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Design a fold accumulator with a precise prefix invariant.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 35: Option, Result, and Fallible Traversal

**Question:** Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?

**Retrieval:** Without notes, restate the invariant carried from Module 34 — Folds, Scans, and Short-Circuiting. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 35](./module-35-option-result-and-fallible-traversal/index.md) with a **failure-policy matrix** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-35-option-result-and-fallible-traversal/workbook.md) before observation. The day’s minimum result is: **Compose optional and fallible transformations while preserving ownership and error meaning.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Resilient Import](../labs/module-05-resilient-import/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 35 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Compose optional and fallible transformations while preserving ownership and error meaning.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Closures, Capture, and Callable Contracts, The Iterator Model, Iterator Algebra and Pipeline Shape, Folds, Scans, and Short-Circuiting, Option, Result, and Fallible Traversal** as one dependency chain, rerun the two investigations that changed your model most, and describe the current LedgerFlow state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 36: Custom Iterators and Collection Protocols

**Question:** What laws must a custom traversal obey, and who owns the collection when iteration begins?

**Retrieval:** Without notes, restate the invariant carried from Module 35 — Option, Result, and Fallible Traversal. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 36](./module-36-custom-iterators-and-collection-protocols/index.md) with a **collection protocol map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-36-custom-iterators-and-collection-protocols/workbook.md) before observation. The day’s minimum result is: **Implement a correct custom `Iterator` by defining state and exhaustion behavior.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Custom Cursors](../labs/module-06-custom-cursors/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 36 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Implement a correct custom `Iterator` by defining state and exhaustion behavior.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 37: Recursive Data and Structural Sharing

**Question:** How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?

**Retrieval:** Without notes, restate the invariant carried from Module 36 — Custom Iterators and Collection Protocols. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 37](./module-37-recursive-data-and-structural-sharing/index.md) with a **structural-sharing graph** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-37-recursive-data-and-structural-sharing/workbook.md) before observation. The day’s minimum result is: **Define recursive algebraic data with the appropriate indirection.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Persistent History](../labs/module-07-persistent-history/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 37 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Define recursive algebraic data with the appropriate indirection.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 38: Functional Core and Effect Isolation

**Question:** Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?

**Retrieval:** Without notes, restate the invariant carried from Module 37 — Recursive Data and Structural Sharing. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 38](./module-38-functional-core-and-effect-isolation/index.md) with a **effect boundary map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-38-functional-core-and-effect-isolation/workbook.md) before observation. The day’s minimum result is: **Separate deterministic domain decisions from filesystem, time, environment, and terminal effects.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Deterministic Batch Runner](../labs/module-08-deterministic-batch-runner/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 38 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate deterministic domain decisions from filesystem, time, environment, and terminal effects.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 39: Combinator Laws and Cost Models

**Question:** What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?

**Retrieval:** Without notes, restate the invariant carried from Module 38 — Functional Core and Effect Isolation. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 39](./module-39-combinator-laws-and-cost-models/index.md) with a **law and counterexample table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-39-combinator-laws-and-cost-models/workbook.md) before observation. The day’s minimum result is: **Design domain combinators that preserve type and error meaning.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Combinator Contracts](../labs/module-09-combinator-contracts/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 39 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Design domain combinators that preserve type and error meaning.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 40: Functional Architecture Synthesis

**Question:** How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?

**Retrieval:** Without notes, restate the invariant carried from Module 39 — Combinator Laws and Cost Models. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 40](./module-40-functional-architecture-synthesis/index.md) with a **whole-pipeline architecture map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-40-functional-architecture-synthesis/workbook.md) before observation. The day’s minimum result is: **Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Route Analysis Engine](../labs/module-10-route-analysis-engine/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 40 in the [LedgerFlow guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add balance checkpoints to LedgerFlow without introducing a second source of truth for event order or reducer semantics.**

Seven days later, rebuild the ten-module sequence and the core **whole-pipeline architecture map** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
