# Workbook — Module 60: Integrated Systems Design, Testing, and Audit

[Chapter](index.md) · [Laboratory](../../labs/module-10-systems-boundary-audit/README.md) · [FrameVault guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Integrated Systems Design, Testing, and Audit** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?* Preserve your first prediction and record decisive facts in a **whole-system boundary dossier**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 59 — Foreign Resources, Callbacks, and Wrapper Architecture that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?**
3. Draw the smallest **whole-system boundary dossier** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

All end-to-end tests pass, but no truncation tests exist. Which parser property remains weakly evidenced?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

The archive output changes because directory iteration order changes. Which contract is missing?

For **Prediction 2**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

Miri passes one test. Is every safe public path sound?

For **Prediction 3**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

A Linux path test passes. Does it establish Windows prefix handling?

For **Prediction 4**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

One unsafe line is undocumented but appears obvious. Is line count a sufficient audit?

For **Prediction 5**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

A new format version silently accepts unknown flag bits. What evolution risk appears?

For **Prediction 6**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

The C ABI adds a field to a public struct without versioning. What can break?

For **Prediction 7**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A timeout feature is requested. Should a polling loop be presented as a portable sandbox?

For **Prediction 8**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

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

### Interleaved reasoning pass

1. For **Draw one boundary map from external bytes to final effects and back to foreign callers**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the whole-system boundary dossier.
2. For **Build a threat model that separates malformed input, hostile namespaces, untrusted processes, allocation pressure, and invalid foreign callers**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the whole-system boundary dossier.
3. For **Use layered tests, dynamic tools, cross-target checks, and failure injection as complementary evidence**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the whole-system boundary dossier.
4. For **Audit unsafe code through invariants and call graphs rather than counting blocks**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the whole-system boundary dossier.

5. Identify one guarantee from an earlier course that a careless implementation of **Integrated Systems Design, Testing, and Audit** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Systems Boundary Audit](../../labs/module-10-systems-boundary-audit/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a complete packet offset table and canonical golden byte sequence;
- exhaustive truncation and declared-length adversarial tests;
- a replacement state machine with an explicit commit point;
- a C/Rust ABI contract and null/overlap rules;
- an unsafe inventory mapping every block to safe entry points, assumptions, tests, and remaining target evidence.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

### Laboratory acceptance trace

Before opening the reference implementation for **Systems Boundary Audit**, record:

- the public behavior that demonstrates **Draw one boundary map from external bytes to final effects and back to foreign callers**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

### Capstone invariant trace

For the Module 60 FrameVault increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Which invariant crosses the largest number of layers?
2. Where is each commit point?
3. Which claims are types, checks, safety obligations, platform results, or foreign obligations?
4. What regression matrix proves that one new entry kind does not weaken old decoding or FFI behavior?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Build a compact packet inspector that combines a checked codec, transactional output, one narrow unsafe byte owner, and a stateless C validator. Create an audit table with one row per public operation and columns for input representation, checked facts, unsafe facts, owned resources, failure state, portability, and adversarial tests. The product is not complete until every row names both a positive guarantee and at least one property it does not claim.

### Closed-book defense

In five minutes, answer “How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?” using the **whole-system boundary dossier**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside FrameVault. A list of APIs without the deciding relationship is incomplete.
