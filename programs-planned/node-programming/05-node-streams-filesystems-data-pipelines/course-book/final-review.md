# Course 5 Final Review

Complete this review without the course book, then use the solutions to locate weak models. The review is passed only when the implementation and explanation agree.

## Whole-course construction

Design a bounded data converter that reads optional gzip NDJSON, validates records, invokes an optional child filter, writes canonical output transactionally, and returns deterministic accounting. Produce the representation graph, queue budget, cancellation tree, failure matrix, publication protocol, and ten adversarial tests before writing code.

## Module 41

1. When a Node.js API gives you bytes, which allocation owns them, which views alias them, and at what exact boundary do bytes become text or typed values?
2. Apply the decision procedure to this scenario: Design a binary thumbnail record containing a media type, width, height, and payload. State which fields are validated before allocation and whether the decoded record owns its payload.
3. Explain why **Assuming Buffer.slice copies** is wrong and give a falsifying test.
4. State FlowLedger’s Module 41 increment and the prior-course invariant it must preserve.


## Module 42

1. What state does a Node.js stream own, which side is readable or writable, and which observation proves that the resource has actually completed?
2. Apply the decision procedure to this scenario: Design a Duplex that accepts commands as objects and emits encoded response bytes. Specify separate modes, high-water-mark units, and terminal ownership.
3. Explain why **Treating close as successful completion** is wrong and give a falsifying test.
4. State FlowLedger’s Module 42 increment and the prior-course invariant it must preserve.


## Module 43

1. How does a producer learn that downstream capacity is temporarily exhausted, and which component owns failure propagation and teardown across the complete chain?
2. Apply the decision procedure to this scenario: Design a network uploader whose request body is a Readable and whose response acknowledgment is the semantic commit. Separate write pressure, pipeline completion, HTTP response, and final product success.
3. Explain why **Awaiting write()** is wrong and give a falsifying test.
4. State FlowLedger’s Module 43 increment and the prior-course invariant it must preserve.


## Module 44

1. When should a streaming computation be expressed as a Node stream, an async iterable, or a Web Stream, and what lifecycle semantics are changed by crossing between them?
2. Apply the decision procedure to this scenario: Design an API that tails a log file as an AsyncIterable of validated records. Explain who owns the FileHandle, what early return does, and whether a second iteration reopens the file.
3. Explain why **Assuming async iteration makes every source bounded** is wrong and give a falsifying test.
4. State FlowLedger’s Module 44 increment and the prior-course invariant it must preserve.


## Module 45

1. What does it mean for a file operation to be complete, visible, replaced, durable, and safely owned in a Node.js process?
2. Apply the decision procedure to this scenario: Design a checkpoint writer for a long-running import. Decide whether checkpoints replace one file, append immutable versions, or update a directory manifest, and state the crash-recovery evidence for the choice.
3. Explain why **Writing directly to the destination** is wrong and give a falsifying test.
4. State FlowLedger’s Module 45 increment and the prior-course invariant it must preserve.


## Module 46

1. How do you turn arbitrary byte chunks into complete text records without corrupting split characters, accepting unbounded frames, or losing the physical location of malformed input?
2. Apply the decision procedure to this scenario: Design a length-prefixed JSON protocol. State how prefix size, payload size, UTF-8 validity, JSON grammar, schema validation, and EOF truncation are reported separately.
3. Explain why **Splitting each decoded chunk on newline** is wrong and give a falsifying test.
4. State FlowLedger’s Module 46 increment and the prior-course invariant it must preserve.


## Module 47

1. How do compression, decompression, hashing, and format transforms compose without confusing data representation, integrity evidence, security, and resource amplification?
2. Apply the decision procedure to this scenario: Design a backup verifier for compressed archives. Decide which digests are stored, which representation each covers, and how an expansion limit is enforced during verification.
3. Explain why **Calling one digest “the data hash”** is wrong and give a falsifying test.
4. State FlowLedger’s Module 47 increment and the prior-course invariant it must preserve.


## Module 48

1. How do you integrate another executable into a Node.js data pipeline without introducing shell ambiguity, unbounded output capture, orphan processes, or incomplete terminal accounting?
2. Apply the decision procedure to this scenario: Design an image-conversion wrapper around a native tool. State argument validation, executable policy, output-size limits, stderr retention, timeout, exit handling, and stage replacement.
3. Explain why **Interpolating user input into exec** is wrong and give a falsifying test.
4. State FlowLedger’s Module 48 increment and the prior-course invariant it must preserve.


## Module 49

1. How do you coordinate branches, side outputs, metadata, and multiple candidate files when a linear pipeline is no longer enough?
2. Apply the decision procedure to this scenario: Design an export that produces data.ndjson, rejects.ndjson, and manifest.json. Choose a publication protocol and give the visible-artifact state after each possible failure.
3. Explain why **Using EventEmitter for required side outputs** is wrong and give a falsifying test.
4. State FlowLedger’s Module 49 increment and the prior-course invariant it must preserve.


## Module 50

1. Can you review and evolve a complete Node.js dataflow system without losing byte semantics, pressure, parser bounds, resource ownership, commit rules, or deterministic evidence?
2. Apply the decision procedure to this scenario: Add a resumable import checkpoint to a streaming system. Define what state can be replayed safely, what byte position means after decoding and filtering, and how the checkpoint is committed with the data.
3. Explain why **Testing only happy-path files** is wrong and give a falsifying test.
4. State FlowLedger’s Module 50 increment and the prior-course invariant it must preserve.


## Oral defense

Explain one end-to-end input byte from source read through decoding, record validation, transformation, serialization, optional compression, staged write, synchronization, and publication. At every step state who owns the current representation and what failure can still invalidate the candidate.
