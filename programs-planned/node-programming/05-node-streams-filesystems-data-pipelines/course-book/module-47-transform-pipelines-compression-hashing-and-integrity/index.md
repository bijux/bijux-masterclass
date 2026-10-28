# Module 47 — Transform Pipelines: Compression, Hashing, and Integrity

**Progress: 47/100**

## The governing question

> How do compression, decompression, hashing, and format transforms compose without confusing data representation, integrity evidence, security, and resource amplification?

## Why this module comes now

Module 46 turned bytes into bounded records and back into canonical bytes. Course 5 now adds transforms whose output size and representation differ substantially from input. Compression and hashing are common stream stages, but their correctness claims depend on where they sit in the pipeline and which byte representation they observe.

Module 46 turned bytes into validated records. Module 47 adds transforms whose input and output are both byte sequences but represent different things. Compression, canonical serialization, and hashing are easy to compose mechanically and easy to report incorrectly. Course 3’s public-contract discipline now applies to every digest label and every claimed integrity domain.

The rule for this module is simple to state and demanding to maintain: name the representation at every edge before measuring or hashing it.

## Observable outcomes

By the end of this module, you can:

- place compression, decompression, hashing, and serialization stages according to the claimed byte representation

- distinguish a digest of source bytes, canonical bytes, compressed bytes, and domain values

- bound decompression expansion and retained transform state

- use crypto hashes as integrity identifiers without presenting them as authentication

- design transform errors and metadata so a reader can reproduce the claim

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| edge representation | Are these source, decoded, canonical, compressed, encrypted, or output bytes? |
| transform state | What window or native state does the transform retain? |
| expansion bound | What limits decompressed or transformed output independently of input size? |
| digest domain | Which exact bytes feed each hash? |
| metadata authority | When may counts and digests be reported as final? |
| integrity claim | Does the mechanism detect accidents, authenticate an origin, or neither? |

## A digest names a specific byte sequence

The phrase “hash of the file” is ambiguous when the system decodes, normalizes, reorders, or compresses data. A digest before decompression identifies the compressed transport bytes. A digest after decompression identifies the uncompressed representation. A digest after canonical serialization identifies the normalized product. These can all be useful, but they answer different questions.

Record the algorithm, byte domain, version, and encoding of the digest. SHA-256 produces bytes; a hexadecimal string is one textual representation. Comparing user-supplied digests requires canonical validation before conversion.

## Compression changes both representation and risk

Gzip and Brotli transforms can make storage smaller, but decompression can expand a small input into a very large output. Backpressure controls the rate at which downstream consumes expanded bytes; it does not impose a total expansion limit. A decompression boundary must enforce maximum uncompressed bytes, record counts, and frame sizes.

Compression streams also retain algorithmic windows and metadata. Their highWaterMark values do not describe the whole memory cost. For security-sensitive input, choose formats and limits with adversarial expansion in mind.

## Transform order defines the product

Serialize then compress is not equivalent to compress then serialize. Hashing before normalization preserves source identity; hashing after canonicalization preserves semantic representation under allowed source variation. Encrypting, authenticating, compressing, and signing have additional ordering rules that are beyond this course, but the habit is the same: draw the exact byte stages.

A pipeline diagram should label each edge with chunk type and representation. “records” is insufficient when one edge contains untrusted unknown objects and another contains validated FlowEvent values.

## Hash transforms need finalization ownership

A crypto Hash is a Transform-like object, but using it as a transparent pipeline stage and reading its digest requires care: digest finalizes the hash and cannot be called repeatedly. A simple custom Transform that calls hash.update and passes chunks through can make the ownership explicit; the pipeline owner reads the digest only after successful completion.

If the destination fails after the hash observed bytes, the digest describes an attempted candidate, not a committed output. Report it only with the correct status. A post-commit manifest should be generated from the bytes that actually became the candidate file.

## Integrity is not authenticity

An unkeyed digest detects accidental change when the expected digest is trusted through another channel. An attacker who can replace both content and digest can recompute it. Course 5 uses SHA-256 for deterministic identity and corruption checks, not as proof of origin. HMACs and signatures belong to later security work.

The course also rejects MD5 and SHA-1 for new integrity identifiers because collision resistance matters for content identity. Even with SHA-256, compare the exact byte representation and validate the expected digest syntax.

## A digest without a representation name is ambiguous

The SHA-256 of compressed bytes differs from the SHA-256 of the original bytes and from the SHA-256 of a canonical reserialization. All may be useful. A download cache may identify compressed transfer bytes; a data model may identify canonical records; an ingestion audit may record the source file. A report field called `sha256` forces readers to guess.

Place hash taps on explicit edges and name their outputs accordingly. The stage order is part of the product contract. Moving a tap across gzip may preserve pipeline success while silently changing the identifier used by caches, verification, or users.

## Small compressed input can produce large output

Backpressure controls the rate at which expanded bytes move downstream; it does not impose a total expanded-byte limit. A compression bomb can keep producing bytes until disk or time is exhausted. The product needs a cumulative expanded-byte counter and a terminal policy when the limit is crossed.

Synchronous decompression helpers can use a maximum output option for bounded in-memory values. Streaming decompression needs an explicit counting stage or transform policy. The limit should be checked before retaining or publishing more expanded data.

## Hashing supplies integrity evidence, not authenticity

A cryptographic hash can detect that bytes differ from an expected digest. If an attacker can replace both data and the expected digest, the hash does not establish origin. Authentication needs a trusted signature, MAC, or authenticated channel and a key-management story.

Course 5 uses SHA-256 as deterministic representation evidence. The docs deliberately avoid calling it tamper-proof. This precision matters because production code often turns a correct primitive into a false security claim.

## Worked case — A transparent sha-256 tap

```ts
import { createHash } from 'node:crypto';
import { Transform, type TransformCallback } from 'node:stream';

export class Sha256Tap extends Transform {
  #hash = createHash('sha256');
  #done = false;

  digestHex(): string {
    if (!this.#done) throw new Error('digest is available only after successful stream finalization');
    return this.#hash.digest('hex');
  }

  override _transform(chunk: Buffer, _encoding: BufferEncoding, callback: TransformCallback): void {
    this.#hash.update(chunk);
    callback(null, chunk);
  }

  override _flush(callback: TransformCallback): void {
    this.#done = true;
    callback();
  }
}
```

The tap hashes exactly the bytes passing through its writable side and emits the same chunk objects. digestHex is intentionally unavailable before _flush. A stronger implementation would also make repeated digest calls explicit, because crypto.Hash.digest can be consumed once. The caller must document whether the tap sits before or after compression and must not call the digest a committed-output digest until file replacement succeeds.

## Extended case analysis

A pipeline reads gzip input, parses events, canonicalizes object key order, and writes gzip output. It can legitimately report four byte domains: compressed source, expanded source, canonical NDJSON, and compressed output. A verification command must say which domain its expected digest describes. Without that label, two correct implementations can disagree while both compute SHA-256 correctly.

## What this mechanism establishes

A correct implementation establishes these local facts:

- Hash taps pass bytes through unchanged.

- Source and compressed digests are computed over explicitly different edges.

- Digests are unavailable before the associated stream completes.

It does **not** establish the stronger claims hidden by these shortcuts:

- naming every digest `sha256` without a representation;

- calling a hash authentication;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. Draw every representation edge from source bytes to final bytes.

2. Place each digest at the edge whose identity the product needs.

3. Define compressed-input, expanded-byte, frame, and record limits separately.

4. Keep transform finalization owned by the pipeline scope.

5. Publish digests only with status that distinguishes attempted, staged, and committed data.

6. Test empty input, tiny chunks, corrupt compressed data, expansion limits, destination failure, and abort.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Calling one digest “the data hash”

Normalization and compression create several distinct byte sequences.

### Trusting backpressure to stop decompression bombs

Backpressure limits flow rate, not cumulative expanded bytes.

### Reading digest before completion

The hash does not yet include all bytes and may describe a failed candidate.

### Calling SHA-256 authentication

An unkeyed digest does not establish who produced the data.

## Apply the mechanism in FlowLedger

Add optional gzip input and output to FlowLedger, separate raw-input and canonical-output digests, and ensure digest metadata is committed only with the staged output.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design a backup verifier for compressed archives. Decide which digests are stored, which representation each covers, and how an expansion limit is enforced during verification.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 47 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Compressed Digest Pipeline** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Place compression, decompression, hashing, and serialization stages according to the claimed byte representation

- Distinguish a digest of source bytes, canonical bytes, compressed bytes, and domain values

- Bound decompression expansion and retained transform state

- Use crypto hashes as integrity identifiers without presenting them as authentication

- Design transform errors and metadata so a reader can reproduce the claim
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/zlib.html](https://nodejs.org/docs/latest-v24.x/api/zlib.html)
- [https://nodejs.org/docs/latest-v24.x/api/crypto.html](https://nodejs.org/docs/latest-v24.x/api/crypto.html)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-47-compressed-digest-pipeline/README.md)
- [FlowLedger engineering guide](../capstone.md)
