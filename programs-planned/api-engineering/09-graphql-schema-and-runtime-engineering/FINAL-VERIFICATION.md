# Final verification — Course 9

**Course:** GraphQL Schema and Runtime Engineering  
**Release:** 1.0.0  
**Graph contract:** Analysis Graph API 1.0  
**Verification date:** 2026-08-08

## Release conclusion

The dependency-light release proof passes from the source tree. It verifies the
exact Course 8 predecessor handoff, all 59 course-book pages, ten numbered
modules, 120 exercises and matching answers, ten laboratories, ten checkpoints,
the released schema and operation registry, both semantic implementation
tracks, the real loopback composition laboratory, release fixtures, planted
defects, and the exact Course 10 handoff.

The course is publication-ready within the evidence boundary below. It does not
claim that its bounded teaching parser is a complete GraphQL implementation or
that uninstalled external environments were executed.

## Executed evidence

### Course structure and pedagogy

```text
Course-book pages:              59
Numbered modules:               10 plus orientation
Exercises:                     120
Matching worked answers:       120
Laboratories:                   10
Evidence checkpoints:           10
Course-book words:          33,576
Total Markdown words:       36,978 before this report
```

The education guard checks page presence, chapter depth, answer identity,
required lab sections, checkpoint evidence, filler markers, and repeated long
paragraphs.

### Predecessor and successor boundaries

```text
Course 8 predecessor handoff:   8 exact files
Course 10 outgoing handoff:    12 exact files
```

The graph layer is prohibited from reading private service databases, owning
business facts, weakening tenant policy, hiding partial failures, or executing
unbounded service fan-out.

### Contract and runtime proof

```text
Analysis Graph API release:     1.0
Root operation types:             3
Active persisted operations:     10
Owned field coordinates:         15
GraphQL documents checked:       26
Shared vector files:             10
Shared vector cases:             36
Graph metadata migrations:    001–004
```

The proof covers:

- stable global identifiers;
- signed, tenant-, audience-, scope-, filter-, high-water-, and expiry-bound
  cursors;
- operation-name and SHA-256 document identity;
- fragment-aware depth, alias, page-size, cost, and service-fan-out analysis;
- request-scoped batching and cache isolation;
- authorization before protected source I/O;
- tenant resource concealment;
- source-owned mutation idempotency and expected-version handling;
- exact field-path partial failures and non-null propagation;
- subscription duplicate suppression, gap detection, and bounded buffering;
- directional schema compatibility and active-client release gates;
- one additive, one review-required, and eight rejected release candidates;
- ten planted defects mapped to falsifying proofs.

### Implementations

```text
Python semantic tests:          29 passed
TypeScript semantic tests:      15 passed
TypeScript strict compilation:  passed
Loopback network tests:          1 passed
Python syntax files:            28 passed
```

The loopback laboratory starts independent Analysis Control, Artifact Service,
Notification Service, and Graph Gateway HTTP servers. It verifies batched remote
composition, tenant propagation, exact partial-failure paths, and preservation
of valid data when Artifact Service fails.

### Data and repository integrity

```text
JSON documents parsed:          59
YAML documents parsed:          25
TOML documents parsed:           1
GraphQL documents inspected:    26
Local Markdown targets checked:  4
Repository hygiene:             passed
Capstone tour:                   passed
```

The final manifest and archive checks are recorded in the external release
record created during packaging.

## Environment-backed routes not executed

The build environment did not provide all optional tools. The following are
therefore recorded as **not executed**, not as successful:

- independent schema and operation validation through `graphql-core` or
  GraphQL.js;
- live Strawberry and GraphQL Yoga framework servers;
- registry-backed client generation and external schema checks;
- a production subscription transport and long-lived connection topology;
- Apollo Federation composition and router execution;
- strict MkDocs rendering.

The course includes setup instructions, adapters, commands, expected oracles,
and failure criteria for these routes. Their absence does not invalidate the
executed semantic proofs, but it limits the strength of claims about external
framework integration.

## Standards profile

The normative schema and execution chapters use the GraphQL September 2025
specification. The executable course schema includes OneOf input-object
semantics. HTTP transport guidance is explicitly identified as a Course 9
profile based on the current Stage 2 GraphQL-over-HTTP draft rather than a final
recommendation. Subscription delivery and incremental delivery are treated as
separate transport and execution concerns; the baseline does not silently claim
a standard production subscription protocol.

## Reproduction

From a clean extracted course directory:

```bash
make doctor
make predecessor-proof
make core-proof
make capstone-tour
make manifest-proof
```

In an environment with the optional dependencies:

```bash
make setup
make framework-proof
make docs-build
make full-proof
```
