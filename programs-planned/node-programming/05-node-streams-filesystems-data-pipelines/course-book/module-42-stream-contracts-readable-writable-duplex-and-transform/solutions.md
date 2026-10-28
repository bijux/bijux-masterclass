# Module 42 Reasoned Solutions — Stream Contracts: Readable, Writable, Duplex, and Transform

These are reasoning standards, not a mandate to copy one implementation. A different design is correct when it proves the same public behavior, ownership, bound, failure, and completion contracts.

## 1. Prediction reasoning

### Duplex half-close

The decisive relationship is **a stream is a protocol plus buffered state**. Readable and Writable name directions relative to the JavaScript consumer. A Readable produces chunks that the consumer reads. A Writable accepts chunks that the consumer writes. Duplex owns both directions, which are independent unless the product links them. Transform is a Duplex whose readable output is derived from writable input. These names describe capabilities, not files or sockets specifically.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. A stream can close after error or destruction. Success must be established by the operation that owns the full protocol. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Mixed consumption

The decisive relationship is **readable consumption style is a design choice**. Readable streams can be consumed through data events, readable/read calls, pipe, pipeline, or async iteration. Mixing styles can move the stream between paused and flowing states in ways that obscure ownership and loss. A module should select one primary consumption style and encapsulate it. Application code in this course prefers pipeline for linear byte flows and async iteration for explicit control-flow transforms.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Two consumption models compete for the same chunks and make flow state difficult to reason about. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Transform callback timing

The decisive relationship is **terminal events answer different questions**. end means a readable has no more data. finish means a writable has accepted end and flushed its implementation callbacks. close means the underlying resource has closed. error reports failure but does not, by itself, prove every side is closed. destroyed is local state, not a promise that operating-system cleanup is complete. The correct terminal observation depends on what the caller owns.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. It changes buffering units; it does not validate objects or bound their retained size. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Event trace

The decisive relationship is **custom stream implementations obey callback discipline**. A custom Writable calls its _write callback exactly once after the chunk has been accepted or rejected. A custom Readable calls push when data is available and pushes null exactly once to signal end. A Transform never runs _transform concurrently for one instance; this serial property can simplify incremental parser state. Throwing asynchronously instead of passing an error to the callback can escape the stream lifecycle.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Internal hooks rely on public stream machinery for buffering and lifecycle. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.

## 2. Repair reasoning

### One completion authority

A principled repair begins with: **Name the stream direction from the caller’s perspective.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### One consumer

A principled repair begins with: **State whether the unit is bytes, strings, or objects.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Callback exactly once

A principled repair begins with: **Choose one consumption style and one completion primitive.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.

## 3. Focused construction review

A strong submission makes the module’s difficult relationship visible in function boundaries and tests. For this module, review the construction in this order:

1. Name the stream direction from the caller’s perspective.

2. State whether the unit is bytes, strings, or objects.

3. Choose one consumption style and one completion primitive.

4. Identify every internal or external queue and its measurement unit.

5. State who destroys the stream after error, cancellation, or early return.

6. Keep custom hook callbacks single, causal, and terminally complete.

Use deterministic fault injection. Exact byte, item, write, line, or lifecycle counts identify the causal boundary more clearly than timers.

Treat counters as evidence only when categories are disjoint and satisfy a stated conservation relationship.

## 4. Laboratory acceptance — Stream State Observatory

The laboratory is complete only when all of these invariants are supported by executable evidence:

- The transform callback is invoked exactly once per accepted chunk.
- The byte counter describes bytes that actually passed through the transform.
- The collector does not retain aliases to producer-owned mutable chunks.
- The laboratory distinguishes readable end, transform finish/end, writable finish, and close.
- Pipeline settlement, not event ordering alone, decides operation success.

The reference is one possible proof. Compare the first meaningful difference and keep your simpler design when it establishes the same invariants. Do not import abstraction without a requirement.

## 5. FlowLedger transfer

Define FlowLedger’s byte-mode and object-mode boundaries. Add transparent counting transforms and a single completion authority for each linear pipeline.

Confirm that representation names, limits, causal errors, cancellation, accounting, CLI text, and process tests describe one feature. A passing unit test does not repair a stale public contract.

## 6. Independent transfer standard

Design a Duplex that accepts commands as objects and emits encoded response bytes. Specify separate modes, high-water-mark units, and terminal ownership.

A strong answer identifies the external authority, validates before retention or allocation, states the owner of every live resource, and names the exact event that changes visible product state. It also states at least one intentionally unsupported guarantee.

## 7. Defense standard

Defend the design in both directions: map each product claim to its mechanism and evidence, then map each Node event or return value to the narrower fact it proves.

Replace “the stream handled it” with representation, owner, bound, and terminal state.
