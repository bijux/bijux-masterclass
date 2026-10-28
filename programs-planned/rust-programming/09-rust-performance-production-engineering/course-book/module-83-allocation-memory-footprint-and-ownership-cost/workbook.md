# Workbook — Module 83: Allocation, Memory Footprint, and Ownership Cost

[Chapter](index.md) · [Laboratory](../../labs/module-03-allocation-budgeted-batch-parser/README.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Allocation, Memory Footprint, and Ownership Cost** has become a usable model rather than remembered vocabulary. Its governing question is: *Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?* Preserve your first prediction and record decisive facts in a **allocation ledger**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 82 — CPU Profiling, Cost Models, and Hot-Path Optimization that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?**
3. Draw the smallest **allocation ledger** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### 1. `Vec` representation versus footprint

A `Vec<Record>` is 24 bytes on a 64-bit target. It contains 100,000 records, and each record owns two `String`s. Explain why 24 bytes is almost irrelevant to capacity planning. List the allocations and capacities that must be counted.

### 2. Clone taxonomy

Classify the likely cost and lifetime consequence of:

- `String::clone`;
- `Arc::clone`;
- `Bytes::clone`;
- cloning a `Vec<u64>`;
- moving each of those values.

Do not reduce the answer to “cheap” or “expensive.”

### 3. Borrowed parsing

A parser can return `BorrowedRecord<'a>` or owned `Record`. Predict which is better for immediate aggregation, queued cross-task work, long-term storage, and detailed error reporting. State which owner must remain alive in every borrowed design.

### 4. Capacity retention

A connection buffer grows once to 8 MiB for an allowed boundary request, then handles 2 KiB requests forever. Predict steady-state memory for 2,000 idle connections if the buffer retains peak capacity. Design a shrink/reuse policy without introducing an allocation on every request.

### 5. Preallocation

A service knows only a configured maximum of one million records. Explain why `Vec::with_capacity(1_000_000)` for every request is not “efficient.” Give two evidence-based ways to choose an initial capacity.

### 6. Interning

Tenant and metric names repeat heavily. Identify when interning can reduce memory and when it can create unbounded retention, synchronization, or identity problems.

## Part 2 — Diagnose and repair

### Case A — Clone removal that extends a lifetime

A patch replaces owned keys with `&str` references into each request buffer. Allocations fall, but all request buffers must now live until the final snapshot. Diagnose the capacity consequence and propose a boundary that borrows transiently but promotes durable identifiers selectively.

### Case B — Reusable buffer pool

A global pool keeps every returned buffer at its largest capacity. Under a burst, 128 workers each grow a 4 MiB buffer. After traffic returns to normal, resident memory remains high. Repair the policy.

### Case C — `Arc` everywhere

A team wraps every configuration, record, and result in `Arc` to avoid clones. Identify semantic, atomic, allocation, and retention costs. Which data actually needs shared ownership?

### Case D — Allocation-count victory

An implementation reduces allocations by 70% but increases peak live bytes and p99 latency. Explain how this can happen and why allocation count alone cannot choose the design.

## Part 3 — Focused exercises

### Exercise 1 — Memory budget

For a service with `C` connections, `Q` queued records, `S` retained series, and snapshot size `O`, write a checked upper-bound formula using:

- per-connection buffer bound;
- per-queued-record owned bytes;
- per-series key and aggregate bytes;
- snapshot temporary bytes;
- fixed runtime allowance.

Identify which terms are strict configuration bounds and which require measurement.

### Exercise 2 — Allocation ledger

Trace one MetricRail line from network buffer to parser, queue, aggregate map, and snapshot. For every field, mark borrow, move, clone, new allocation, retained capacity, and drop point.

### Exercise 3 — Promotion policy

Design an API that parses borrowed fields, validates them, and copies only identifiers that must become map keys. Explain how duplicate hot identifiers can be reused without retaining entire input frames.

### Exercise 4 — Peak experiment

Design an experiment that distinguishes allocation churn, retained memory, and temporary peak. Include warm-up, steady state, boundary bursts, recovery, and what must be sampled.

### Exercise 5 — Retention decision

Choose one large reusable buffer or shared backing allocation from a real program. Write its normal size, legal maximum, owner, borrowers, reuse frequency, high-water behavior, and release trigger. Then define a retention policy with a steady-state budget and an exceptional-burst policy. Include the observation that would prove the policy too aggressive—such as renewed allocation churn—and the observation that would prove it too permissive—such as peak capacity remaining live after recovery.

### Interleaved reasoning pass

1. For **Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the allocation ledger.
2. For **Trace ownership operations that allocate, clone, reallocate, promote, or retain data**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the allocation ledger.
3. For **Explain when borrowing reduces work and when it only complicates lifetimes without changing allocation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the allocation ledger.
4. For **Design capacity policies from observed size distributions instead of guessing large defaults**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the allocation ledger.

5. Identify one guarantee from an earlier course that a careless implementation of **Allocation, Memory Footprint, and Ownership Cost** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build the [Allocation-Budgeted Batch Parser](../../labs/module-03-allocation-budgeted-batch-parser/README.md). Validate total input bytes and record count before allocating the output vector. Parse each line into a borrowed form, then promote only the key. Preserve physical line numbers and exact error categories. Explain why pre-counting lines is acceptable here and where it could become duplicated work worth measuring.

### Laboratory acceptance trace

Before opening the reference implementation for **Allocation-Budgeted Batch Parser**, record:

- the public behavior that demonstrates **Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add a memory ledger and enforce configuration relationships before startup. Bound:

- line bytes;
- identifier bytes;
- queued messages;
- active ingestion;
- retained series;
- snapshot output;
- offline input;
- per-connection buffer capacity.

Measure retained memory after a boundary burst and decide when buffers shrink or are dropped. Document which counters are exact product state and which memory values are target observations.

### Capstone invariant trace

For the Module 83 MetricRail increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. Why is `size_of::<Vec<T>>()` not collection footprint?
2. What is the difference between allocation count, allocated bytes, live bytes, and retained capacity?
3. Why can eliminating a clone increase memory?
4. When is `Arc::clone` cheap but still architecturally costly?
5. What owner keeps a borrowed field valid?
6. How do you prevent shared byte slices from retaining oversized frames?
7. What belongs in a memory budget formula?
8. Defend one deliberate allocation as the correct design.

### Exercise 6 — Build a lifetime-and-retention census

For one MetricRail ingest followed by one snapshot, classify every significant allocation as request-local, batch-local, series-retained, snapshot-temporary, or process-lifetime. Record who creates it, the event that makes it unreachable, whether capacity can exceed logical length, and which workload variable controls its size. Then choose one allocation to remove and one retained structure to bound. Explain why removing the temporary allocation may have less production value than reducing retained capacity, even when the allocator profile makes the temporary allocation more visible.

### Memory acceptance gate

A memory change is acceptable only when peak resident behavior, retained state after quiescence, allocation count, and semantic output have all been reconsidered. Report both logical bytes and container capacity where they differ. A lower allocation count does not justify a cache that grows without a workload-derived limit, and a smaller object does not prove a smaller process if it increases fragmentation or duplicates data elsewhere.

### Closed-book defense

In five minutes, answer “Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?” using the **allocation ledger**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside MetricRail. A list of APIs without the deciding relationship is incomplete.
