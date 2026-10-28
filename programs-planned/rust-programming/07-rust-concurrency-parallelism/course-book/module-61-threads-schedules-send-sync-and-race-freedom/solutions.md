# Reasoned solutions — Module 61: Threads, Schedules, Send, Sync, and Race Freedom

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the BatchWeave guide](../capstone.md)

The module’s main correction is conceptual: thread safety is not one Boolean property. `Send` and `Sync` establish which ownership and reference movements safe Rust permits. Product correctness still requires a lifecycle protocol, a schedule-independent invariant, and an output policy.

The answers below are reasoning models, not scripts to imitate. A different implementation can be stronger when it proves the same contract more directly. Compare ownership, synchronization, progress, failure, and determinism—not only surface syntax.

## Part 1 — Prediction solutions

### Prediction 1

The closure takes ownership of the `String`, so parent use is rejected as use after move. Borrowing is not accepted by ordinary `spawn` because the worker may outlive the stack frame. Return the string through the join value, clone only when two semantic copies are required, or use `thread::scope` when temporary borrowing is the intended contract.

### Prediction 2

`Rc<T>` is not `Send`; synchronized lifetime management is absent. Cloning changes the count but not the auto-trait contract. Use unique ownership when one worker needs the value, or `Arc<T>` when cross-thread shared liveness is real.

### Prediction 3

`Arc` makes the reference count safe; `RefCell` remains non-`Sync` because its runtime borrow state is unsynchronized. Use partitioned ownership, `Arc<Mutex<T>>`, an atomic representation, or a message-passing owner according to the actual invariant.

### Prediction 4

There is no data race, but both threads can read one and both can store zero or both can perform downstream work. The logical reservation needs one compare-exchange or fetch-update transition whose success is the reservation linearization point.

### Prediction 5

Completion and channel-arrival order are schedule-dependent. Sorting by stable source index makes rendered output deterministic, assuming each job’s value is itself deterministic.

### Prediction 6

The code compiles and detaches workers. The function cannot claim work completion, panic observation, or cleanup before return. Finite operations should retain and join handles or document a separate service-lifetime protocol.

### Prediction 7

Returning early leaves later workers detached. Join every handle first, recording the first or all panic outcomes, and only then return the aggregate error.

### Prediction 8

`Mutex<Vec<u8>>` is `Send` and `Sync` when the inner vector is `Send`; the mutex serializes access exposed through shared references. `Arc` then supplies cross-thread shared ownership. The conclusion follows structurally from the components.

## Part 2 — Repair reasoning

The strongest repair removes unnecessary sharing. Move payloads to workers, keep immutable configuration in `Arc`, and return indexed results. If the input is borrowed and the parent operation encloses all work, use scoped threads and disjoint slices. A shared result vector is not needed; join values or a result channel create a clearer publication boundary.

The original whole-vector lock serializes removal, computation, and output insertion. Releasing the lock before computation improves exclusion scope but still leaves thread-per-item creation, detached lifecycle, and unstable output. A complete repair therefore addresses all six dimensions instead of treating mutex duration as the only defect.

## Part 3 — Focused construction guidance

### Construction 1

`String` is normally `Send` and `Sync`; `Rc<String>` is neither for cross-thread use; `Arc<String>` is both when `String` is; `Cell<u64>` is `Send` but not `Sync`; `Mutex<Vec<u8>>` supplies synchronized shared access; and `Arc<Mutex<Vec<u8>>>` adds shared liveness. The derivation must mention whether an owned value or `&T` crosses the boundary.

### Construction 2

Move `(index, payload)` into each closure, return `(index, sum)`, retain every handle, join all, and place values into an index-addressed output vector. Record panics rather than returning before later joins.

### Construction 3

The broken protocol separates observation from reservation. A successful compare-exchange from remaining to remaining-minus-one is the linearization point. Retry on interference and stop at zero.

### Construction 4

A complete ledger names the owner of each image, the `Arc` owners of the profile, the parent owner of handles, the worker owner of temporary buffers, and the coordinator owner of result ordering. Cleanup follows ownership, not an informal “thread pool” label.

### Construction 5

A thread-per-item design must reject or cap item count. Once accepted input greatly exceeds a reasonable thread bound, use a fixed worker group, a bounded queue, or data-parallel decomposition rather than changing only stack size.

## Part 4 — Laboratory comparison

Compare whether the solution transfers payload ownership once, joins every handle even after panic, and uses stable indices for assembly. A reference implementation that merely happens to return ordered output on one run is not equivalent. Inspect the thread ledger and the test strategy: schedule variation should be induced with barriers or controlled delays while assertions remain independent of exact timing.

## Part 5 — Capstone comparison

BatchWeave’s first increment should contain no queue and no mutex. Its purpose is to freeze identities and ownership. Jobs are immutable owned requests. Outcomes are owned facts carrying the same stable index. The coordinator owns ordering. This prevents later synchronization choices from silently redefining the product model.

## Part 6 — Reconstruction and defense

A complete defense says that `Send` permits ownership transfer and `Sync` permits shared-reference transfer. It distinguishes language-level data-race freedom from product-level race freedom, names every join obligation, and states that output order is a chosen stable projection over nondeterministic completion. It also admits that a thread-per-item demonstration is bounded pedagogy, not the final engine topology.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.
