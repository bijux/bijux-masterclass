# Workbook — Module 60: Integrated Systems Design, Testing, and Audit

[Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze answers before compiling or reading the reference implementation. A correct result without the governing reason is incomplete.

## Part 1 — Predict

### Prediction 1

All end-to-end tests pass, but no truncation tests exist. Which parser property remains weakly evidenced?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

The archive output changes because directory iteration order changes. Which contract is missing?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

Miri passes one test. Is every safe public path sound?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

A Linux path test passes. Does it establish Windows prefix handling?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

One unsafe line is undocumented but appears obvious. Is line count a sufficient audit?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

A new format version silently accepts unknown flag bits. What evolution risk appears?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

The C ABI adds a field to a public struct without versioning. What can break?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A timeout feature is requested. Should a polling loop be presented as a portable sandbox?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Build one end-to-end ledger crossing bytes, domain values, staged files, native paths, child-process data, manual storage, ABI reports, and opaque sessions. For every transition, name the owner, validation, failure state, cleanup, compatibility effect, and strongest honest success claim.

For **Integrated Systems Design, Testing, and Audit**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- auditing each module in isolation while ignoring cross-layer assumptions;
- letting the CLI reinterpret a format rule;
- claiming portability from one target test;
- treating all failures as one string;
- expanding the unsafe core during integration;
- adding features without updating the compatibility and threat model;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Create a full boundary and ownership map for FrameVault.

Required evidence: Include bytes, files, paths, child process, allocation, ABI, handles, and callbacks.

### Construction 2

Write a threat table with prevent/detect/bound/out-of-scope outcomes.

Required evidence: Avoid one generic security statement.

### Construction 3

Design the cross-platform test matrix and identify unavailable evidence.

Required evidence: Separate source checks from executed target checks.

### Construction 4

Audit one unsafe abstraction from public constructor through drop.

Required evidence: Include panic and zero-length states.

### Construction 5

Build an independent packet inspector using the same method.

Required evidence: Require a versioned format, checked parser, one file effect, and an optional FFI validator.

## Part 4 — Independent laboratory

Build [Systems Boundary Audit](../../labs/module-10-systems-boundary-audit/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a complete packet offset table and canonical golden byte sequence;
- exhaustive truncation and declared-length adversarial tests;
- a replacement state machine with an explicit commit point;
- a C/Rust ABI contract and null/overlap rules;
- an unsafe inventory mapping every block to safe entry points, assumptions, tests, and remaining target evidence.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Which invariant crosses the largest number of layers?
2. Where is each commit point?
3. Which claims are types, checks, safety obligations, platform results, or foreign obligations?
4. What regression matrix proves that one new entry kind does not weaken old decoding or FFI behavior?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Build a compact packet inspector that combines a checked codec, transactional output, one narrow unsafe byte owner, and a stateless C validator. Create an audit table with one row per public operation and columns for input representation, checked facts, unsafe facts, owned resources, failure state, portability, and adversarial tests. The product is not complete until every row names both a positive guarantee and at least one property it does not claim.
