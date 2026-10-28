# Module 46 Reasoned Solutions — Incremental Text Decoding, Framing, and Bounded Parsers

These are reasoning standards, not a mandate to copy one implementation. A different design is correct when it proves the same public behavior, ownership, bound, failure, and completion contracts.

## 1. Prediction reasoning

### Split scalar

The decisive relationship is **chunk boundaries have no semantic meaning**. A Readable may split a UTF-8 sequence, a newline delimiter, a JSON token, or a length-prefixed payload at any byte. It may also combine many logical records in one chunk. A parser that calls chunk.toString independently and splits the result is correct only by accident on friendly chunking. The decoder must preserve incomplete character bytes between writes, and the framer must preserve incomplete record bytes or text between decoded segments.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. A line or a multibyte character can cross chunks; data is corrupted or misframed. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Unterminated line

The decisive relationship is **decoding and framing are separate state machines**. TextDecoder with stream true or StringDecoder can preserve incomplete multibyte sequences. Framing then consumes decoded text and searches for delimiters, or operates on bytes when the protocol is byte-defined. Keeping the two layers separate makes malformed UTF-8 distinguishable from a missing newline or malformed JSON record.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. It is a queue threshold, not a semantic record bound. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### CRLF split

The decisive relationship is **an unfinished frame needs its own bound**. Backpressure limits queued chunks; it does not limit the size of one record. A peer or file can send an arbitrarily long line without a delimiter while the parser retains it. Define maxLineBytes or maxFrameBytes and enforce it before concatenating beyond the limit. For text frames, track encoded bytes rather than JavaScript string length when the external contract is in bytes.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Grammar and trusted domain shape are different validation layers. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Final line policy

The decisive relationship is **parsing has layered failure authority**. Framing decides where one record ends. JSON.parse decides JSON grammar. Runtime validation decides whether the resulting unknown value has the expected shape. Domain validation decides whether values such as timestamps and identifiers are legal in this product. Each layer should report its own context without pretending to own later semantics.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Transport completion does not make the declared record complete. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.

## 2. Repair reasoning

### Chunk-local split

A principled repair begins with: **Specify whether framing is byte-defined or text-defined.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Late limit check

A principled repair begins with: **Choose strict or replacement decoding and state the consequence.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Flattened error

A principled repair begins with: **Bound one unfinished frame independently of stream queue thresholds.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.

## 3. Focused construction review

A strong submission makes the module’s difficult relationship visible in function boundaries and tests. For this module, review the construction in this order:

1. Specify whether framing is byte-defined or text-defined.

2. Choose strict or replacement decoding and state the consequence.

3. Bound one unfinished frame independently of stream queue thresholds.

4. Advance line and byte positions only after a frame is accepted.

5. Keep framing, syntax, schema, and domain errors distinct.

6. Test all boundary splits, empty records, final records, malformed encoding, and over-limit input.

Use deterministic fault injection. Exact byte, item, write, line, or lifecycle counts identify the causal boundary more clearly than timers.

Treat counters as evidence only when categories are disjoint and satisfy a stated conservation relationship.

## 4. Laboratory acceptance — Bounded NDJSON Decoder

The laboratory is complete only when all of these invariants are supported by executable evidence:

- Chunk partitioning does not change decoded records.
- Malformed UTF-8 is rejected rather than replaced when strict mode is selected.
- Pending line bytes never exceed the configured limit.
- CRLF is normalized without leaving a trailing carriage return.
- JSON arrays, primitives, and null do not pass an object-record validator.

The reference is one possible proof. Compare the first meaningful difference and keep your simpler design when it establishes the same invariants. Do not import abstraction without a requirement.

## 5. FlowLedger transfer

Add FlowLedger’s bounded NDJSON decoder, event validator, structured diagnostic types, and canonical serializer. Malformed input must fail before the staged output becomes visible.

Confirm that representation names, limits, causal errors, cancellation, accounting, CLI text, and process tests describe one feature. A passing unit test does not repair a stale public contract.

## 6. Independent transfer standard

Design a length-prefixed JSON protocol. State how prefix size, payload size, UTF-8 validity, JSON grammar, schema validation, and EOF truncation are reported separately.

A strong answer identifies the external authority, validates before retention or allocation, states the owner of every live resource, and names the exact event that changes visible product state. It also states at least one intentionally unsupported guarantee.

## 7. Defense standard

Defend the design in both directions: map each product claim to its mechanism and evidence, then map each Node event or return value to the narrower fact it proves.

Replace “the stream handled it” with representation, owner, bound, and terminal state.
