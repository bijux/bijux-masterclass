# One reasoning model for all six courses

Rust becomes easier when every mechanism is analyzed with the same questions. The vocabulary becomes richer across the program, but the investigation does not restart.

## 1. What exists?

Name the values, types, resources, syntax, bytes, handles, and external actors. Distinguish a Rust value from its representation, a declaration from generated code, and a path string from the filesystem object a later lookup may resolve.

## 2. Who owns it, and who may act on it?

Record the unique owner or liveness roots. Then record temporary permissions: shared inspection, exclusive mutation, consumption, callback access, or foreign borrowing. In early modules this is an ownership ledger; later it becomes a graph, capability map, or safety contract.

## 3. What contract is promised?

Write the invariant before the implementation. A function promises inputs, outputs, failure, and visible state. A trait adds laws across implementations. A macro adds an accepted language and generated surface. An unsafe wrapper or FFI function adds obligations that Rust cannot verify automatically.

## 4. How does information flow?

Trace type, cardinality, order, state, failure, and effects from input to output. Iterator pipelines, parsers, state machines, build scripts, and binary decoders all become more understandable when every stage has an explicit input and output.

## 5. When is the fact established?

Identify the decisive phase:

- source parsing;
- macro matching or procedural parsing;
- name resolution;
- type and borrow checking;
- build execution;
- runtime validation;
- operating-system action;
- foreign-code behavior.

A later phase cannot retroactively prove an earlier assumption. A successful compile does not validate a file format; a successful checksum does not authenticate a sender; a non-null pointer does not prove valid storage.

## 6. What evidence supports the claim?

Choose evidence that matches the contract:

- compiler prediction for type-system behavior;
- unit and integration tests for observable behavior;
- compile-fail cases for rejected APIs;
- law tests for substitutability;
- golden and adversarial data for formats;
- state-transition tests for failure atomicity;
- target-conditioned measurements for layout or platform claims;
- a safety ledger for unsafe operations;
- a matching header and consumer for FFI.

## The maturity path

| Course | The same question becomes… |
|---:|---|
| 1 | What type and owner does this ordinary program give each value? |
| 2 | Which place, lifetime, cleanup obligation, and liveness edge makes the memory design valid? |
| 3 | Which contract and variation mechanism lets several implementations remain lawful and evolvable? |
| 4 | How do data, failure, state, and effects compose without hidden work? |
| 5 | Which declaration owns generated syntax, and in which phase can misuse be rejected? |
| 6 | Which external assumptions remain, and how does one safe boundary contain them? |

Use this model in every workbook and design review. The goal is not to memorize sixty isolated features. The goal is to reason through unfamiliar Rust code with one increasingly powerful method.
