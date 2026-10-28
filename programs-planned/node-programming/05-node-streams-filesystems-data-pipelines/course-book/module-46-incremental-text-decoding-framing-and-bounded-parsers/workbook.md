# Module 46 Workbook — Incremental Text Decoding, Framing, and Bounded Parsers

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Split scalar

Predict the result of independently decoding each byte of a multibyte UTF-8 character.

### Unterminated line

A source sends 100 MB without a newline. Identify the state that grows even though stream pressure works.

### CRLF split

Predict the correct framing behavior when `
` ends one chunk and `
` begins the next.

### Final line policy

A file ends with valid JSON but no newline. State two defensible policies and the compatibility consequence of each.

## 2. Diagnose and repair

### Chunk-local split

Repair a parser that runs `chunk.toString().split("\n")` independently for every chunk.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Late limit check

Move a maximum-line check so it rejects before the pending frame exceeds the bound.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Flattened error

Replace “invalid record” with layered errors preserving line, phase, and cause without retaining the full source.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Implement fatal incremental UTF-8 decoding.

2. Retain a bounded pending line across chunks.

3. Handle LF, CRLF, empty lines, and the final unterminated line according to a stated policy.

4. Parse JSON with physical line context.

5. Validate that each value is a non-array object before yielding.

6. Generate tests for every split position around a multibyte scalar and delimiter.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- every split position of a multibyte character;

- delimiter split across chunks;

- empty lines and whitespace-only lines;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Bounded NDJSON Decoder

Implement a byte-to-object Transform with fatal UTF-8 decoding, CRLF handling, exact physical line numbers, maximum line bytes, structured syntax errors, runtime object validation, and explicit final-line behavior.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Add FlowLedger’s bounded NDJSON decoder, event validator, structured diagnostic types, and canonical serializer. Malformed input must fail before the staged output becomes visible.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design a length-prefixed JSON protocol. State how prefix size, payload size, UTF-8 validity, JSON grammar, schema validation, and EOF truncation are reported separately.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **decoder state:** Which incomplete UTF-8 bytes are retained across chunks?

- **frame state:** Which incomplete line or length-prefixed payload is retained?

- **physical position:** Which byte offset and line number identify the current evidence?

- **frame limit:** What maximum applies before a delimiter arrives?

- **syntax trust:** When does text become a JavaScript value?

- **domain trust:** Which validator establishes the FlowEvent contract?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. Why are decoding and framing different state machines?

2. Which limit applies before a delimiter arrives?

3. When does an `unknown` value become a domain event?

4. How do you preserve useful diagnostics without retaining hostile input?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
