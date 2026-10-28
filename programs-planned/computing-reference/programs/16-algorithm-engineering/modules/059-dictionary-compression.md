---
module_id: ALGE-059
program: Algorithm Engineering
level: 2
module_number: 59
title: Dictionary Compression
status: complete
last_verified: 2026-09-05
---

# Dictionary Compression

## One-Page Review

### Governing question

How can a compressor replace repeated byte strings with dictionary references while preserving exact reconstruction, bounding resources, selecting parses by encoded cost, and treating every compressed stream as hostile input?

### Essential definitions

- **Lossless compression** maps an input to a representation from which a decoder recovers the input exactly.
- A **phrase** is a repeated or newly learned sequence represented as one coding unit.
- An **LZ77 reference** is a backward distance and length into already reconstructed output.
- A **sliding window** bounds how far backward a reference may reach.
- **LZ78** emits a prior phrase index plus a new symbol and grows an explicit phrase dictionary.
- **LZW** initializes a symbol dictionary, emits phrase codes, and lets encoder and decoder grow matching dictionaries implicitly.
- A **preset dictionary** is shared out of band and must be identified and versioned.
- A **parse** partitions the input into literals and phrases; its token count need not equal its bit cost.

### Central model, mechanism, or theorem

An LZ77 decoder maintains reconstructed output $O$. A literal appends one symbol. A reference $(d,\ell)$ repeatedly appends $O[|O|-d]$ for $\ell$ steps, requiring $1\le d\le |O|$. Reading the source position again after every append gives deliberate overlap: distance one can expand one seed byte into an arbitrarily long run, subject to the format's length limit. The round-trip invariant is that after every token, $O$ equals the source prefix consumed by the encoder.

No injective lossless compressor can shorten every input. Among all $2^n$ bit strings of length $n$, fewer than $2^n$ binary strings have length below $n$. Some inputs must therefore remain the same size or expand once framing and metadata are counted.

### Critical invariants

- Decoding is deterministic from the bitstream, format version, parameters, and any identified external dictionary.
- Every reference points into permitted history; overlap follows the specified byte-by-byte semantics.
- Encoder and decoder dictionary updates occur in exactly the same order.
- Phrase selection is evaluated in encoded bits, including tags, lengths, distances, tables, and framing.
- Arithmetic is checked before allocation, copying, or output growth.
- Decoded bytes, memory, nesting, work, and compression ratio are capped by policy.
- Integrity checks detect some corruption; they do not make parsing or allocation safe.

### Common failures

Common failures include copying an overlapping match as one fixed slice; accepting a zero or too-large distance; confusing LZ77, LZ78, and LZW update rules; assuming longest match is always cheapest; measuring only payload bytes; failing to identify a preset dictionary; resetting code width on only one side; treating checksums as authenticity; decompressing secrets with attacker-controlled text in one context; and allocating from untrusted declared sizes before applying limits.

### Compact example

After literals `a`, `b`, and `c`, a reference $(d=3,\ell=6)$ appends `abcabc`: the second `abc` is copied from bytes produced during the same reference. A snapshot copy of the original three-byte source would produce only half the required output. The decoder must validate the distance, then append one symbol at a time or implement an equivalent overlap-safe copy.

### Connections

[ALGE-058](./058-global-and-local-sequence-alignment.md) optimizes sequence correspondence; dictionary compression exploits exact repeated factors. [ALGE-060](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) engineers searchable collections where compression, indexing, and access granularity interact. Data Engineering owns dataset representation and lifecycle; Security Engineering owns threat models for secret-dependent and adversarial decompression.

## Governing Question

Given a byte sequence, a dictionary model, and a concrete wire format, how should an engineer construct and cost phrases, prove exact decoding, select memory and random-access boundaries, and defend the decoder against malformed or adversarial streams?

Dictionary compression is not merely “find repeated strings.” It is a synchronized state machine whose correctness depends on reference semantics, dictionary evolution, token coding, framing, and resource policy. A parser can be optimal for token count yet poor in bytes; a valid compressed stream can still demand unacceptable memory or output.

## Why This Matters

Dictionary methods underlie archival formats, transport encodings, database pages, executable packaging, telemetry, and modern compressors. They turn repetition into references and often combine those references with entropy coding. This separation matters: phrase discovery explains *what* is repeated; the entropy coder explains *how expensively* token symbols are represented.

Production requirements pull in opposing directions. Larger histories discover longer matches but consume memory and weaken random access. Greedy matching is fast but can miss a cheaper parse. Preset dictionaries improve small-message ratios but introduce compatibility and lifecycle state. Streaming lowers latency but creates reset and corruption-propagation boundaries.

The decompressor is usually the sharper security boundary. A tiny input may expand enormously, request an unsupported window, contain invalid offsets, or exploit shared compression state. Correctness therefore includes explicit budgets and failure semantics, not only successful round trips on friendly data.

## Prerequisites and Retrieval

Retrieve [ALGE-053](./053-boyer-moore-family.md) through [ALGE-056](./056-suffix-trees-and-automata.md) for exact-match search structures, plus prefix codes, amortized analysis, injective mappings, integer bounds, and finite-state parsing. Recall that a byte string and a character string are not interchangeable unless an encoding is fixed.

This chapter owns LZ77-style references, LZ78/LZW dictionary growth, parse costing, framing implications, and decoder safety. It does not derive Huffman or arithmetic coding, specialize image/audio/video codecs, or define one product's API.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish LZ77, LZ78, LZW, and preset-dictionary mechanisms;
2. trace overlapping backward references exactly;
3. prove round-trip correctness with a prefix invariant;
4. explain why universal lossless shrinking is impossible;
5. compare greedy, lazy, and cost-aware parsing;
6. separate phrase parsing, token coding, and container framing;
7. reason about windows, resets, checkpoints, and random access;
8. design synchronized dictionary growth and width transitions;
9. validate hostile streams before arithmetic, allocation, and copying; and
10. benchmark ratio, speed, memory, latency, and failures without hiding metadata.

## Core Exposition

### Begin with an exact interface

Let the source be $S\in\Sigma^*$, usually a byte sequence. A lossless encoder $E$ and decoder $D$ satisfy

$$
D(E(S;\theta);\theta)=S,
$$

where $\theta$ includes the format version, parameters, and any external dictionary. If a required part of $\theta$ is absent or different, silent output is worse than an explicit incompatibility error.

Losslessness implies injectivity for fixed $\theta$: if $E(x)=E(y)$ then applying $D$ gives $x=y$. There are $2^n-1$ binary strings shorter than $n$ bits but $2^n$ inputs of length $n$. Consequently, at least one length-$n$ input cannot map to a shorter bit string. Headers and checksums strengthen the operational reason to retain an uncompressed mode.

Two ratio conventions occur. This chapter reports **compressed fraction** $C/U$ and **space saving** $1-C/U$, where $U>0$ and $C$ includes format metadata. Some tools call $U/C$ the compression ratio. Always name the formula; empty input needs a separate convention.

### Decode LZ77 references from reconstructed history

An LZ77-family parser emits literal symbols or matches $(d,\ell)$, where $d$ is backward distance and $\ell$ is length. At output length $p$, a match is legal only if $1\le d\le p$ and its length is supported by the format. For each copied symbol, append the symbol currently $d$ positions behind the end.

This rule permits overlap. With output `A` and $(1,5)$, appends observe `A` each time and produce `AAAAAA`. Implementations may vectorize or repeat chunks, but observable behavior must equal sequential copying. A one-time source slice is not generally equivalent.

A sliding-window encoder limits $d\le W$. It searches history for a prefix of the remaining input, selects a match or literal, and advances by the phrase length. Search structures include hash chains, binary trees, suffix structures, and specialized match finders. They change time and candidate quality, not the decoder's wire semantics.

The following instructional codec exposes the invariant. Its tokens are Python values, not a serialized standard. Exhaustive small-input tests are needed in addition to these examples.

<!-- bijux-verify: {"id":"lz77-overlap-round-trip","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"tokens=(('L', 'a'), ('L', 'b'), ('L', 'r'), ('L', 'a'), ('L', 'c'), ('L', 'a'), ('L', 'd'), ('R', 7, 4))\nround_trip=True\noverlap=(('L', 'a'), ('R', 1, 5))\ninvalid_distance=rejected\n","stderr":""}} -->
```python
def encode(text, window=8, minimum=3):
    tokens = []
    position = 0
    while position < len(text):
        best_distance = best_length = 0
        for distance in range(1, min(window, position) + 1):
            length = 0
            while (
                position + length < len(text)
                and text[position + length] == text[position + length - distance]
            ):
                length += 1
            if length > best_length:
                best_distance, best_length = distance, length
        if best_length >= minimum:
            tokens.append(("R", best_distance, best_length))
            position += best_length
        else:
            tokens.append(("L", text[position]))
            position += 1
    return tuple(tokens)


def decode(tokens, output_limit=1_000):
    output = []
    for token in tokens:
        if token[0] == "L" and len(token) == 2:
            if len(output) >= output_limit:
                raise ValueError("output limit")
            output.append(token[1])
        elif token[0] == "R" and len(token) == 3:
            distance, length = token[1:]
            if not (isinstance(distance, int) and 1 <= distance <= len(output)):
                raise ValueError("invalid distance")
            if not (isinstance(length, int) and length > 0):
                raise ValueError("invalid length")
            if length > output_limit - len(output):
                raise ValueError("output limit")
            for _ in range(length):
                output.append(output[-distance])
        else:
            raise ValueError("invalid token")
    return "".join(output)


tokens = encode("abracadabra")
print(f"tokens={tokens}")
print(f"round_trip={decode(tokens) == 'abracadabra'}")
print(f"overlap={encode('aaaaaa')}")
try:
    decode((("R", 1, 3),))
except ValueError:
    print("invalid_distance=rejected")
```

### Grow phrases explicitly with LZ78

LZ78 starts with an empty phrase at index zero. At the current input position, find the longest dictionary phrase $P_i$ matching the input prefix, read the next symbol $a$, emit $(i,a)$, and insert $P_i a$. The decoder reconstructs the same phrase from its existing index, appends $a$, emits it, and inserts it at the same next index.

Unlike an LZ77 offset, an LZ78 index names a phrase object rather than an output position. Unbounded dictionaries are theoretical conveniences; real formats need limits, eviction or reset rules, width transitions, and a defined terminal representation when the input ends exactly on an existing phrase.

### Remove transmitted suffixes with LZW

LZW initializes both sides with every alphabet symbol. The encoder emits the code for the longest known phrase $w$, observes next symbol $k$, and inserts $wk$. The decoder normally receives code $c$, emits its phrase, and inserts `previous_phrase + first(current_phrase)`.

There is one famous forward-reference case: the received code can equal the next dictionary index before that entry has been inserted. Then the current phrase is `previous_phrase + first(previous_phrase)`. Any other unknown code is invalid. This “KwKwK” case follows from synchronized update timing; treating every missing code as that case accepts corruption.

Code width growth and dictionary reset are wire rules. If one side moves from 9 to 10 bits one token earlier, every following boundary is misparsed. Tests must cross each width threshold, fill the dictionary, reset it, and immediately exercise the special case.

### Optimize encoded cost, not a proxy

Greedy LZ77 chooses the longest current match. It often works well and is easy to stream, but longest phrase is not necessarily minimum bits. A shorter first match can place the next position at a cheap long match; distance and length codes can have different widths; a literal may be inexpensive under the current entropy table.

Model candidate phrases as edges in a DAG over positions. An edge $(i,j)$ represents encoding $S[i:j]$ with cost $c(i,j)$. Then

$$
best[j]=\min_{0\le i<j}\{best[i]+c(i,j)\},\qquad best[0]=0.
$$

This shortest-path formulation yields an optimal parse only for the declared cost model. When symbol frequencies and code lengths depend on the chosen parse, the costs are coupled; implementations iterate estimates, use block models, or accept a heuristic.

### Separate parser, token code, and container

A dictionary parser produces literals, lengths, distances, or phrase codes. An entropy coder assigns bit representations to these symbols. A container supplies boundaries, parameters, checks, dictionaries, and metadata. Conflating the layers creates false claims about both ratio and compatibility.

DEFLATE is a durable example: RFC 1951 defines blocks containing literals and length/distance pairs represented with Huffman codes. Its distances are bounded by 32 KiB and match lengths by 258 bytes. Raw DEFLATE does not itself supply the zlib or gzip wrapper's uncompressed-data checksum. The format permits references across DEFLATE block boundaries, so a block is not automatically a random-access reset point.

Modern formats preserve the layered idea with different details. RFC 8878 describes Zstandard frames, blocks, sequence execution, entropy coding, and optional dictionaries. RFC 9659 updates HTTP use by requiring encoders not to exceed an 8 MiB window and decoders to support up to that size; that HTTP rule must not be generalized to every Zstandard context.

### Design window and access boundaries

A larger window can expose more repeated substrings and longer distances, but it increases match-search work, decoder history, and worst-case memory. A frame or reset point bounds dependencies and corruption propagation but prevents references across the boundary. A checkpoint can store enough state to resume, trading index size for seek latency.

Random access therefore needs designed granularity: independent chunks, periodic resets, external seek tables, or checkpoints. Merely splitting a compressed stream into transport pieces does not remove dictionary dependencies. Benchmark at intended object sizes because small records may be dominated by headers and dictionary identifiers.

Preset dictionaries seed the history or coding tables with domain-specific bytes. They can make small, similar messages much cheaper, but the identifier is part of the decode contract. Deployment needs immutable dictionary bytes, collision-resistant identity where adversaries matter, negotiated support, retention, rollback, and an explicit missing-dictionary error.

### Treat decompression as resource-sensitive parsing

Parse lengths and offsets with checked arithmetic before computing allocation sizes. Reject reserved symbols, impossible codes, references before available history, unsupported windows, truncated inputs, trailing-data violations, and checksum failures according to the format contract. Apply limits to total output, per-object output, memory, nesting, wall or CPU work, and expansion ratio.

A ratio limit alone is insufficient: a large legitimate input can still exhaust memory, and a small denominator makes ratios unstable. Stream output when possible, yet enforce a cumulative cap before each write. Return distinct outcomes such as malformed, unsupported parameter, missing dictionary, checksum mismatch, resource limit, and success.

Checksums are evidence of accidental-integrity consistency, not memory safety or authenticity. Validate structure and budgets even if a checksum will later fail. Cryptographic authentication, when required, belongs to a specified composition with carefully ordered verification and resource limits.

Compression can also leak. If attacker-controlled bytes and secrets share adaptive compression state and an observer sees compressed lengths, guesses correlated with the secret may change length. Mitigations include separating contexts, disabling compression for secrets, masking lengths, and avoiding attacker-controlled reflection near secrets. A generic “encrypted afterward” claim does not remove this length channel.

## Definitions and Notation

Let $S=S[0:n]$ be an $n$-symbol source, $p$ the consumed prefix length, $O$ decoded output, $W$ the history-window bound, $d$ backward distance, and $\ell$ match length. Let $U$ and $C$ be uncompressed and complete compressed sizes measured in the same unit.

- A **literal** represents a source symbol directly.
- A **match** represents a source substring using prior state.
- A **dictionary** maps phrases to identifiers or provides addressable history.
- A **dynamic dictionary** changes as tokens are processed.
- A **reset** returns dictionary state to a format-defined initial state.
- A **frame** is a self-described decoding unit; a **block** may still depend on earlier blocks.
- A **compression bomb** is a stream whose decoding consumes disproportionate resources.
- **Round-trip correctness** is $D(E(S;\theta);\theta)=S$, not merely successful parsing.
- **Compressed fraction** is $C/U$; **space saving** is $1-C/U$ for $U>0$.

## Mechanisms, Invariants, or Proof Structure

### Prefix proof for LZ77 round trips

Assume the encoder emits a token only when it represents the next source phrase and the decoder begins empty. Induct on tokens. The base case reconstructs the empty prefix. A literal appends exactly the next source symbol. For a reference, the encoder found equality between the next source symbols and history under the same overlap semantics. Each decoder append therefore equals the next source symbol; newly appended symbols become legal history for the remaining copy. The invariant holds after the phrase and, by induction, after all tokens.

The proof depends on range checks, identical overlap semantics, and identical token interpretation. It does not prove the parser terminates efficiently, the representation is small, or malformed inputs are safe.

### Impossibility of shrinking every input

For fixed $n$, losslessness makes encodings of the $2^n$ length-$n$ inputs distinct. Exactly $\sum_{k=0}^{n-1}2^k=2^n-1$ binary strings are shorter than $n$. There are not enough shorter outputs for all inputs, so at least one encoding has length at least $n$. This is a theorem about injective coding, not a prediction that every incompressible file expands under every container.

### Decoder state invariants

Before every token:

1. output length is within the configured cap;
2. dictionary indices name initialized phrases only, except the single specified LZW next-code case;
3. a backward distance is positive and no greater than available permitted history;
4. `output_length + match_length` is checked without overflow and fits the cap;
5. encoder-relevant resets, alphabet, width, and preset identity match the bitstream;
6. no result is released as authenticated merely because decompression and checksum verification succeeded.

### Evidence ladder

Unit examples establish selected traces. Exhaustive bounded testing can enumerate all small strings and parameter combinations. Differential testing compares independent implementations. Fuzzing explores malformed parsers. Property tests assert round trips and caps. Standards vectors establish conformance cases. None alone proves universal correctness; report the population, oracle, toolchain, and residual risk.

## Alternatives and Trade-Offs

| Choice | Benefit | Cost or risk | Suitable evidence |
|---|---|---|---|
| LZ77 sliding history | Bounded decoder memory; good local repetition | Match search and weak native random access | Round trips, overlap vectors, offset bounds |
| LZ78 phrase table | Clear explicit phrase growth | Dictionary memory and index-width policy | Update traces and reset thresholds |
| LZW implicit phrases | No new symbol transmitted per learned phrase | Delicate special case and width synchronization | Boundary vectors and decoder differential tests |
| Greedy parse | Low latency and simple implementation | May miss minimum-bit parse | Compare with exact small-instance oracle |
| Cost-aware parse | Better modeled bit cost | More search and model coupling | Re-encode cost and optimality oracle |
| Large window | More distant matches | Memory, latency, interoperability | Corpus benchmarks and adversarial allocation tests |
| Independent frames | Parallelism and bounded corruption | Lost cross-frame matches and headers | Seek/recovery tests at target granularity |
| Preset dictionary | Strong small-message compression | Distribution, identity, privacy, retention | Version-mismatch and missing-dictionary tests |
| Store uncompressed | Predictable cost on incompressible data | No size reduction | Expansion threshold and framing tests |

## Failure Modes and Misconceptions

- **“Longest match means best compression.”** Token prices and future positions determine total bits.
- **“A block boundary is a reset.”** Some formats allow references across blocks; consult the format.
- **“Overlap is an implementation detail.”** It changes decoded bytes unless implemented equivalently.
- **“A checksum makes decoding safe.”** It neither validates allocation arithmetic nor authenticates data.
- **“Dictionary IDs are optional metadata.”** A wrong dictionary can make exact reconstruction impossible or incorrect.
- **“All unknown LZW codes are the special case.”** Only the exactly-next code has the defined reconstruction.
- **“Compression ratio has one definition.”** $C/U$ and $U/C$ are reciprocals and must be named.
- **“Streaming means constant memory.”** The window, tables, buffers, metadata, and caller retention still matter.
- **“Encryption hides compression behavior.”** Ciphertext length can preserve a secret-dependent length signal.
- **“Round-trip tests prove decoder safety.”** Friendly encoder output omits most malformed-state transitions.
- **“Text is the natural input.”** Formats operate on bytes; normalization or encoding changes the byte sequence.
- **“A newer codec is always better.”** Ratio, CPU, memory, latency, compatibility, and access requirements differ.

## Worked Examples

### Example 1

**Situation.** Output is `ABCXYZ`, and the next token is $(d=6,\ell=3)$.

At output length six, source index is $6-6=0$. Sequentially copying three symbols appends `A`, `B`, `C`. The new output is `ABCXYZABC`. The distance was legal because $1\le6\le6$.

**Conclusion.** A backward reference addresses already reconstructed history and can replace a repeated factor exactly.

### Example 2

**Situation.** Output is `AB`, followed by $(d=2,\ell=7)$.

The source positions evolve as output grows: append `A`, `B`, `A`, `B`, `A`, `B`, `A`. The result is `ABABABABA`. A fixed two-byte snapshot copied once is incomplete; repeated snapshot doubling is valid only if it preserves the same sequence.

**Conclusion.** Overlap-safe copying is part of decoding semantics, not merely an optimization choice.

### Example 3

**Situation.** Three bytes have been produced and the stream requests $(d=4,\ell=10)$.

The legal-distance predicate fails because $4>|O|=3$. The decoder rejects before subtracting an unchecked unsigned value, allocating output, or reading memory. It does not clamp the distance or substitute zeros.

**Conclusion.** Structural validity precedes copying and prevents ambiguous output and out-of-bounds access.

### Example 4

**Situation.** Encode `ABAABABA` with root index 0.

The phrases are: emit $(0,A)$ and add `A` as 1; emit $(0,B)$ and add `B` as 2; match `A`, emit $(1,A)$ and add `AA` as 3; match `B`, emit $(2,A)$ and add `BA` as 4. The remaining `BA` is an already known phrase, so a real format needs an explicit end rule rather than pretending there is a following symbol.

**Conclusion.** LZ78 mechanics are simple only after dictionary initialization and terminal encoding are specified.

### Example 5

**Situation.** The decoder has emitted previous phrase `AB`; its next free code is 260, and it now reads code 260.

Because the code equals—not exceeds—the next free index, construct current phrase as `AB` plus its first symbol: `ABA`. Emit `ABA`, then insert the phrase prescribed by the normal update timing. Code 261 at this moment would be malformed.

**Conclusion.** The LZW special case is one precisely bounded forward reference, not permission to accept arbitrary missing codes.

### Example 6

**Situation.** From position 0, a length-four match costs 7 bits and leaves a 10-bit literal; a length-three match costs 4 bits and enables a following length-two match costing 4 bits.

Greedy longest match costs $7+10=17$ bits. The shorter-first parse costs $4+4=8$ bits. These stipulated costs can arise from distance/length code classes and the next position's candidates.

**Conclusion.** Match length is a proxy; optimal parsing minimizes complete encoded cost.

### Example 7

**Situation.** A 40-byte record becomes 24 payload bytes, plus a 6-byte frame header and 4-byte checksum.

Complete compressed size is $C=24+6+4=34$ bytes, not 24. Compressed fraction is $34/40=0.85$ and space saving is $1-0.85=0.15$, or 15%. Reporting payload alone would claim 40% saving.

**Conclusion.** Include all stored or transmitted metadata and name the ratio formula.

### Example 8

**Situation.** A 1 GiB log is one dependent stream, but queries need a record near byte 800 MiB within 100 ms.

Without checkpoints, decoding may require all preceding history. Independent 4 MiB frames bound restart work to one frame but lose matches across boundaries and add headers. A seek table plus periodic dictionary checkpoints offers another point on the size/latency curve and must include checkpoint storage in $C$.

**Conclusion.** Random access is an explicit format-and-index design, not a free property of block compression.

### Example 9

**Situation.** A service accepts at most 2 MiB compressed input and 64 MiB output. A 20 KiB stream declares operations that would produce 2 GiB.

Before each append, check `length <= output_limit - produced`; stop once the cumulative result would exceed 64 MiB. Also cap window allocation independently and charge CPU work, because a stream can consume excessive work without reaching the output cap.

**Conclusion.** Enforce cumulative output, memory, and work limits during decoding, not after materialization.

### Example 10

**Situation.** A response contains secret `token=ALPHA` and reflects an attacker-controlled guess. Compressed lengths are observable across many requests.

Guesses sharing a prefix with the secret can create longer matches and smaller responses. Encryption preserves ciphertext length closely enough for the signal to remain. Put secrets and reflection in separate compression contexts or disable compression for this response; add padding only as a defense whose leakage distribution has been measured.

**Conclusion.** Shared adaptive state can turn compression ratio into a confidentiality side channel.

## Cross-Program Connections

- **Algorithms:** [ALGE-055](./055-suffix-arrays-and-lcp.md) and [ALGE-056](./056-suffix-trees-and-automata.md) supply exact-factor machinery; [ALGE-060](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) combines compact storage with collection search.
- **Data Structures:** owns hash tables, tries, trees, and cache-aware layouts used by match finders.
- **Data Engineering:** owns byte representation, corpus sampling, dictionaries as governed data, retention, and end-to-end pipeline measurements.
- **Operating Systems:** owns mapped files, buffering, page behavior, memory pressure, and safe streaming I/O.
- **Security Engineering:** owns authentication composition, secret-dependent length threat models, sandboxing, and hostile-input policy.
- **API Engineering:** owns negotiation, content-coding semantics, error representation, quotas, and compatibility promises.
- **Platform Engineering:** owns dictionary distribution, version rollout, observability, and fleet-wide resource controls.

## References

1. Jacob Ziv and Abraham Lempel, “A Universal Algorithm for Sequential Data Compression,” *IEEE Transactions on Information Theory* 23(3), 337–343, May 1977, [doi:10.1109/TIT.1977.1055714](https://doi.org/10.1109/TIT.1977.1055714). Primary LZ77 source; bibliographic record verified 2026-09-05.
2. Jacob Ziv and Abraham Lempel, “Compression of Individual Sequences via Variable-Rate Coding,” *IEEE Transactions on Information Theory* 24(5), 530–536, September 1978, [doi:10.1109/TIT.1978.1055934](https://doi.org/10.1109/TIT.1978.1055934). Primary LZ78 source; bibliographic record verified 2026-09-05.
3. Terry A. Welch, “A Technique for High-Performance Data Compression,” *Computer* 17(6), 8–19, June 1984, [doi:10.1109/MC.1984.1659158](https://doi.org/10.1109/MC.1984.1659158). Primary LZW source; bibliographic record verified 2026-09-05.
4. L. Peter Deutsch, [*DEFLATE Compressed Data Format Specification version 1.3*](https://www.rfc-editor.org/rfc/rfc1951), RFC 1951, May 1996, doi:10.17487/RFC1951. Official format specification; limits, overlap, block dependencies, and security notes checked 2026-09-05.
5. L. Peter Deutsch and Jean-Loup Gailly, [*ZLIB Compressed Data Format Specification version 3.3*](https://www.rfc-editor.org/rfc/rfc1950), RFC 1950, May 1996, doi:10.17487/RFC1950. Official wrapper and preset-dictionary specification; checked 2026-09-05.
6. Yann Collet and Murray S. Kucherawy, [*Zstandard Compression and the 'application/zstd' Media Type*](https://www.rfc-editor.org/rfc/rfc8878), RFC 8878, February 2021, doi:10.17487/RFC8878. Official informational format document with verified errata and RFC 9659 update status checked 2026-09-05.
7. Nidhi Jaju and W. Felix P. Handte, [*Window Sizing for Zstandard Content Encoding*](https://www.rfc-editor.org/rfc/rfc9659), RFC 9659, September 2024, doi:10.17487/RFC9659. Official update for the HTTP content-coding window requirement; checked 2026-09-05.
8. David Salomon and Giovanni Motta, *Handbook of Data Compression*, 5th ed., Springer, 2010, [doi:10.1007/978-1-84882-903-9](https://doi.org/10.1007/978-1-84882-903-9). Broad treatment of dictionary and entropy methods.

## Exercises

### Exercise 1

Explain the different meanings of “dictionary” in LZ77, LZ78, LZW, and a preset-dictionary format. State what information the decoder must possess in each case.

### Exercise 2

Starting from output `XYZ`, decode $(d=3,\ell=8)$. List each appended symbol and explain why the round-trip prefix invariant permits reading bytes created during this token.

### Exercise 3

A decoder allocates `declared_output_length`, copies every reference with a one-time slice, verifies the checksum, and only then enforces a 100 MiB quota. Identify at least four independent defects and give a correction for each.

### Exercise 4

A 400 GiB event collection is read sequentially for training but also serves point queries with a 200 ms target. Compare one continuous large-window stream with independent 8 MiB frames plus a seek index. Give a reasoned recommendation and the evidence needed before deployment.

### Exercise 5

Two services exchange LZW-like phrase codes while deploying dictionary resets independently. Design a protocol rule that restores deterministic decoding across retries, reordering, and rolling upgrades. Include identity, ordering, resource, and failure requirements.

## Answers to the Exercises

### Answer 1

LZ77's dictionary is addressable reconstructed history; the stream supplies a distance and length, so the decoder needs prior output and the window rules. LZ78's dictionary is an explicit table of phrases grown from emitted `(prior index, next symbol)` pairs; the decoder needs initialization, insertion, terminal, limit, and reset rules. LZW begins with the complete alphabet and transmits phrase codes while both sides infer new phrases; it additionally needs code-width and special-case timing. A preset dictionary consists of external immutable bytes or tables supplied before decoding; its exact identity and acquisition contract are required. Acceptable answers must distinguish position references from phrase indices and identify synchronized state.

### Answer 2

The appends are `X`, `Y`, `Z`, `X`, `Y`, `Z`, `X`, `Y`, producing `XYZXYZXYZXY`. Initially the referenced `XYZ` is in prior output. After those three copies, the newly appended `XYZ` is itself three positions behind and supplies the next symbols. The prefix proof reasons one append at a time: if output equals the consumed source prefix before an append and encoder match semantics assert the next source symbol equals `output[-3]`, appending it preserves the invariant. A complete answer must show all eight symbols and explicitly use evolving output.

### Answer 3

First, allocating from an untrusted size can exhaust memory or overflow; validate representation and compare with configured bounds before allocation. Second, one-time slice copying breaks overlapping-reference semantics; use sequential or provably equivalent overlap-safe copying. Third, a checksum after decoding is too late to prevent unsafe arithmetic, reads, writes, or resource exhaustion; validate each token and budget incrementally. Fourth, the quota is enforced after the damage; test `length <= limit - produced` before every append. Also validate positive in-range distances, legal lengths and codes, window limits, work budgets, and truncated input. Any four independent findings with preventive corrections earn full credit.

### Answer 4

The continuous stream can exploit cross-collection repetition and reduce header overhead, but a point query may require decoding a huge prefix and retaining a large history. Independent 8 MiB frames plus a seek index bound restart work and enable parallel recovery, at the cost of lost cross-frame matches, headers, and index space. Given a hard point-query target, begin with framed storage unless measurements show 8 MiB decoding cannot meet 200 ms; then tune frame size or add checkpoints. Measure complete bytes, cold/warm seek latency percentiles, throughput, peak memory, corruption scope, object-size distribution, and representative corpus ratio. A different recommendation is acceptable if it satisfies both workloads with stated evidence.

### Answer 5

Put a monotonically ordered frame or epoch identifier, codec/version identifier, initial alphabet or preset-dictionary digest, reset flag, and declared resource parameters in authenticated framing. A phrase-code frame may depend only on a named prior epoch or must carry a reset; retries are idempotent by frame identity, and out-of-order dependent frames wait or fail explicitly. Rolling upgrades retain decoders and dictionaries for advertised versions until dependencies expire. Receivers cap window, table, output, and work before processing and distinguish missing state, unsupported version, malformed code, resource limit, and authentication failure. Full credit requires deterministic state identity and order, bounded resources, and explicit failure—not merely “synchronize the deployments.”
