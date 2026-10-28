# Module 47 Reasoned Solutions — Transform Pipelines: Compression, Hashing, and Integrity

These are reasoning standards, not a mandate to copy one implementation. A different design is correct when it proves the same public behavior, ownership, bound, failure, and completion contracts.

## 1. Prediction reasoning

### Tap placement

The decisive relationship is **a digest names a specific byte sequence**. The phrase “hash of the file” is ambiguous when the system decodes, normalizes, reorders, or compresses data. A digest before decompression identifies the compressed transport bytes. A digest after decompression identifies the uncompressed representation. A digest after canonical serialization identifies the normalized product. These can all be useful, but they answer different questions.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Normalization and compression create several distinct byte sequences. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Compression bomb

The decisive relationship is **compression changes both representation and risk**. Gzip and Brotli transforms can make storage smaller, but decompression can expand a small input into a very large output. Backpressure controls the rate at which downstream consumes expanded bytes; it does not impose a total expansion limit. A decompression boundary must enforce maximum uncompressed bytes, record counts, and frame sizes.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Backpressure limits flow rate, not cumulative expanded bytes. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Flush timing

The decisive relationship is **transform order defines the product**. Serialize then compress is not equivalent to compress then serialize. Hashing before normalization preserves source identity; hashing after canonicalization preserves semantic representation under allowed source variation. Encrypting, authenticating, compressing, and signing have additional ordering rules that are beyond this course, but the habit is the same: draw the exact byte stages.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. The hash does not yet include all bytes and may describe a failed candidate. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Canonicalization

The decisive relationship is **hash transforms need finalization ownership**. A crypto Hash is a Transform-like object, but using it as a transparent pipeline stage and reading its digest requires care: digest finalizes the hash and cannot be called repeatedly. A simple custom Transform that calls hash.update and passes chunks through can make the ownership explicit; the pipeline owner reads the digest only after successful completion.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. An unkeyed digest does not establish who produced the data. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.

## 2. Repair reasoning

### Unnamed digest

A principled repair begins with: **Draw every representation edge from source bytes to final bytes.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Input-only limit

A principled repair begins with: **Place each digest at the edge whose identity the product needs.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Premature metadata

A principled repair begins with: **Define compressed-input, expanded-byte, frame, and record limits separately.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.

## 3. Focused construction review

A strong submission makes the module’s difficult relationship visible in function boundaries and tests. For this module, review the construction in this order:

1. Draw every representation edge from source bytes to final bytes.

2. Place each digest at the edge whose identity the product needs.

3. Define compressed-input, expanded-byte, frame, and record limits separately.

4. Keep transform finalization owned by the pipeline scope.

5. Publish digests only with status that distinguishes attempted, staged, and committed data.

6. Test empty input, tiny chunks, corrupt compressed data, expansion limits, destination failure, and abort.

Use deterministic fault injection. Exact byte, item, write, line, or lifecycle counts identify the causal boundary more clearly than timers.

Treat counters as evidence only when categories are disjoint and satisfy a stated conservation relationship.

## 4. Laboratory acceptance — Compressed Digest Pipeline

The laboratory is complete only when all of these invariants are supported by executable evidence:

- Hash taps pass bytes through unchanged.
- Source and compressed digests are computed over explicitly different edges.
- Digests are unavailable before the associated stream completes.
- Corrupt compressed input fails with its causal zlib error.
- Expanded output is bounded independently of compressed input.

The reference is one possible proof. Compare the first meaningful difference and keep your simpler design when it establishes the same invariants. Do not import abstraction without a requirement.

## 5. FlowLedger transfer

Add optional gzip input and output to FlowLedger, separate raw-input and canonical-output digests, and ensure digest metadata is committed only with the staged output.

Confirm that representation names, limits, causal errors, cancellation, accounting, CLI text, and process tests describe one feature. A passing unit test does not repair a stale public contract.

## 6. Independent transfer standard

Design a backup verifier for compressed archives. Decide which digests are stored, which representation each covers, and how an expansion limit is enforced during verification.

A strong answer identifies the external authority, validates before retention or allocation, states the owner of every live resource, and names the exact event that changes visible product state. It also states at least one intentionally unsupported guarantee.

## 7. Defense standard

Defend the design in both directions: map each product claim to its mechanism and evidence, then map each Node event or return value to the narrower fact it proves.

Replace “the stream handled it” with representation, owner, bound, and terminal state.
