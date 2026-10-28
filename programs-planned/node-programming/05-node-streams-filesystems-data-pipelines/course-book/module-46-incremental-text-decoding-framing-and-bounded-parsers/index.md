# Module 46 — Incremental Text Decoding, Framing, and Bounded Parsers

**Progress: 46/100**

## The governing question

> How do you turn arbitrary byte chunks into complete text records without corrupting split characters, accepting unbounded frames, or losing the physical location of malformed input?

## Why this module comes now

Module 45 gave the pipeline a durable file boundary. Most data products still need to interpret the file incrementally. Stream chunks are transport units, not records. Text characters and line delimiters can be split across chunks, so parsing must retain bounded incomplete state and commit positions only after validation.

Module 45 supplied a safe file boundary, but files and streams deliver arbitrary chunks rather than records. Module 46 introduces the state machine that turns those chunks into trusted units. It combines Course 1 runtime validation, Course 3 schema thinking, and Course 5 byte ownership without allowing any layer to disappear into `JSON.parse`.

The core separation is fourfold: decode bytes to text, frame text into records, parse syntax into JavaScript values, and validate values into domain records. Each boundary has its own error, limit, and source location.

## Observable outcomes

By the end of this module, you can:

- decode UTF-8 incrementally across arbitrary chunk boundaries

- distinguish byte limits, character counts, line limits, and record limits

- implement line and length framing with bounded unfinished state

- preserve physical byte and line context in structured parse errors

- separate framing, JSON syntax, runtime schema validation, and domain semantics

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| decoder state | Which incomplete UTF-8 bytes are retained across chunks? |
| frame state | Which incomplete line or length-prefixed payload is retained? |
| physical position | Which byte offset and line number identify the current evidence? |
| frame limit | What maximum applies before a delimiter arrives? |
| syntax trust | When does text become a JavaScript value? |
| domain trust | Which validator establishes the FlowEvent contract? |

## Chunk boundaries have no semantic meaning

A Readable may split a UTF-8 sequence, a newline delimiter, a JSON token, or a length-prefixed payload at any byte. It may also combine many logical records in one chunk. A parser that calls chunk.toString independently and splits the result is correct only by accident on friendly chunking. The decoder must preserve incomplete character bytes between writes, and the framer must preserve incomplete record bytes or text between decoded segments.

Tests must generate every split position around multibyte characters and delimiters. A single large test file read with the default highWaterMark does not exercise the parser contract.

## Decoding and framing are separate state machines

TextDecoder with stream true or StringDecoder can preserve incomplete multibyte sequences. Framing then consumes decoded text and searches for delimiters, or operates on bytes when the protocol is byte-defined. Keeping the two layers separate makes malformed UTF-8 distinguishable from a missing newline or malformed JSON record.

Fatal decoding is appropriate when invalid UTF-8 must reject the input. Replacement decoding is a product policy, not a harmless default. Once invalid bytes become the replacement character, the original evidence is gone.

## An unfinished frame needs its own bound

Backpressure limits queued chunks; it does not limit the size of one record. A peer or file can send an arbitrarily long line without a delimiter while the parser retains it. Define maxLineBytes or maxFrameBytes and enforce it before concatenating beyond the limit. For text frames, track encoded bytes rather than JavaScript string length when the external contract is in bytes.

Repeated Buffer.concat on every chunk can make a long incomplete frame quadratic. A parser can keep a list of bounded pieces and concatenate once, or maintain a capacity-managed buffer. The simpler design is acceptable when the maximum frame is small and explicitly enforced.

## Parsing has layered failure authority

Framing decides where one record ends. JSON.parse decides JSON grammar. Runtime validation decides whether the resulting unknown value has the expected shape. Domain validation decides whether values such as timestamps and identifiers are legal in this product. Each layer should report its own context without pretending to own later semantics.

A useful error records the physical line number, approximate byte offset, layer, stable code, and bounded excerpt. Do not include an unbounded source line or secret payload in the diagnostic.

## EOF is an input event, not implicit success

At EOF, the decoder must flush any incomplete character state. The framer must decide whether a final unterminated line is allowed. A length-framed parser must reject a partial prefix or payload. These decisions belong in the format contract and tests.

Normal stream end and syntactic completion are separate. A Readable can end successfully while the final record is truncated. The parser transform must convert that condition into pipeline failure before the output commits.

## Transport chunks are not characters or records

A stream can split a multibyte UTF-8 scalar between chunks and can split `
` across chunks. It can also deliver many lines together. Decoding each chunk independently can insert replacement characters; splitting each chunk independently can lose or invent frame boundaries. Correctness must hold for every possible chunk partition of the same byte sequence.

Incremental decoding retains incomplete character bytes. Framing retains incomplete record text or bytes. The parser should make both retained states visible and bounded rather than relying on accidental chunk sizes from one filesystem or test machine.

## One unfinished frame can defeat stream backpressure

A source can produce a line with no delimiter. Even if every stream queue remains near its high-water mark, the framer may append text indefinitely. `maxLineBytes` or `maxFrameBytes` is therefore independent of high-water marks. The check should occur as data is accumulated, not only after a delimiter finally appears.

Byte-defined protocols should measure encoded bytes. JavaScript string length counts UTF-16 code units and can understate or misstate the external byte budget. If decoded text is retained, the implementation may need both byte accounting and text state.

## Error context should survive every trust transition

A useful diagnostic distinguishes malformed UTF-8, an over-limit physical line, invalid JSON syntax, a non-object JSON value, and a domain-invalid event. Preserve physical line numbers and, when available, byte offsets. Wrap lower-level causes rather than flattening every failure into “bad input”.

Do not retain an entire huge line merely to improve the message. Error excerpts need their own bound. The diagnostic should provide enough local evidence to act without becoming another unbounded memory channel or leaking sensitive content.

## Worked case — Bounded ndjson line splitting

```ts
import { StringDecoder } from 'node:string_decoder';

export async function* lines(
  source: AsyncIterable<Uint8Array>,
  maxLineBytes: number,
): AsyncGenerator<{ readonly number: number; readonly text: string }> {
  const decoder = new StringDecoder('utf8');
  let pending = '';
  let pendingBytes = 0;
  let number = 1;
  for await (const chunk of source) {
    pendingBytes += chunk.byteLength;
    if (pendingBytes > maxLineBytes * 2) throw new Error('unfinished input exceeds safety bound');
    pending += decoder.write(Buffer.from(chunk.buffer, chunk.byteOffset, chunk.byteLength));
    let newline: number;
    while ((newline = pending.indexOf('
')) >= 0) {
      const text = pending.slice(0, newline).replace(/
$/, '');
      if (Buffer.byteLength(text, 'utf8') > maxLineBytes) throw new Error(`line ${number} exceeds limit`);
      yield { number, text };
      number += 1;
      pending = pending.slice(newline + 1);
      pendingBytes = Buffer.byteLength(pending, 'utf8');
    }
  }
  pending += decoder.end();
  if (pending.length > 0) {
    if (Buffer.byteLength(pending, 'utf8') > maxLineBytes) throw new Error(`line ${number} exceeds limit`);
    yield { number, text: pending.replace(/
$/, '') };
  }
}
```

The example demonstrates split-safe decoding and an explicit final-line policy. Its early pendingBytes bound is conservative because a chunk may contain many complete lines before they are processed; a production implementation should process decoded text before enforcing the unfinished-frame budget and should track exact buffered bytes. This deliberate imperfection is useful: the reader must distinguish a safety backstop from an accurate product limit.

## Extended case analysis

The UTF-8 bytes for `€` are `e2 82 ac`. If a file stream yields `e2` and then `82 ac 0a`, calling `chunk.toString('utf8')` on each part can emit replacement characters. `StringDecoder` or `TextDecoder` in streaming mode retains the incomplete scalar until the rest arrives. Framing then sees the actual character followed by the newline. This small case proves why chunk-boundary tests are semantic tests, not performance tests.

## What this mechanism establishes

A correct implementation establishes these local facts:

- Chunk partitioning does not change decoded records.

- Malformed UTF-8 is rejected rather than replaced when strict mode is selected.

- Pending line bytes never exceed the configured limit.

It does **not** establish the stronger claims hidden by these shortcuts:

- decoding each chunk independently;

- measuring `string.length` as external byte length;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. Specify whether framing is byte-defined or text-defined.

2. Choose strict or replacement decoding and state the consequence.

3. Bound one unfinished frame independently of stream queue thresholds.

4. Advance line and byte positions only after a frame is accepted.

5. Keep framing, syntax, schema, and domain errors distinct.

6. Test all boundary splits, empty records, final records, malformed encoding, and over-limit input.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Splitting each decoded chunk on newline

A line or a multibyte character can cross chunks; data is corrupted or misframed.

### Using highWaterMark as max line length

It is a queue threshold, not a semantic record bound.

### Reporting JSON.parse as a schema error

Grammar and trusted domain shape are different validation layers.

### Accepting partial final length frames at EOF

Transport completion does not make the declared record complete.

## Apply the mechanism in FlowLedger

Add FlowLedger’s bounded NDJSON decoder, event validator, structured diagnostic types, and canonical serializer. Malformed input must fail before the staged output becomes visible.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design a length-prefixed JSON protocol. State how prefix size, payload size, UTF-8 validity, JSON grammar, schema validation, and EOF truncation are reported separately.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 46 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Bounded NDJSON Decoder** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Decode UTF-8 incrementally across arbitrary chunk boundaries

- Distinguish byte limits, character counts, line limits, and record limits

- Implement line and length framing with bounded unfinished state

- Preserve physical byte and line context in structured parse errors

- Separate framing, JSON syntax, runtime schema validation, and domain semantics
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/string_decoder.html](https://nodejs.org/docs/latest-v24.x/api/string_decoder.html)
- [https://nodejs.org/docs/latest-v24.x/api/util.html#class-utiltextdecoder](https://nodejs.org/docs/latest-v24.x/api/util.html#class-utiltextdecoder)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-46-bounded-ndjson-decoder/README.md)
- [FlowLedger engineering guide](../capstone.md)
