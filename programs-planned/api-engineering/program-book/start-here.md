# Start Here

## Who this program is for

You should be comfortable reading small programs, running command-line tools, and following tests. You do not need prior OpenAPI, PostgreSQL, OAuth, observability, performance, or messaging expertise. Course 1 begins at the HTTP and contract boundary; later courses assume the earlier outcomes or require an equivalent predecessor proof.

## Do not begin by browsing the repository

Begin with the course book. Repository exploration before a mental model often turns learning into filename archaeology. For each course:

1. read its `course-book/index.md`;
2. complete orientation and verify the predecessor boundary;
3. read the module chapter without opening the answer file;
4. answer the twelve exercises in your own words;
5. inspect the focused implementation paths named by the chapter;
6. perform the lab in one primary language track;
7. compare the shared invariant in the second track;
8. complete the checkpoint and preserve the evidence.

## Choose a language strategy

Course 1 uses Python and TypeScript symmetrically because its purpose is to prove contract independence. From Course 2 onward, choose one primary implementation track. Complete the deep build there. Use the comparison track to answer a narrower question: does the same public or engineering invariant survive an idiomatic implementation in another ecosystem?

Do not force identical folder structures, exception classes, asynchronous primitives, database libraries, or framework hooks. Parity applies to externally observable behavior and named guarantees.

## Use the evidence ladder

Ask what kind of claim you are making before choosing a test:

- document parsing and schema fixtures establish description properties;
- black-box HTTP observations establish provider conformance;
- pure domain tests establish deterministic rules;
- database and storage evidence establish committed outcomes;
- adversarial policy decisions establish security controls;
- telemetry supports diagnosis but does not replace durable truth;
- live process and network experiments establish lifecycle and failure behavior;
- comparable workload runs support performance decisions;
- broker delivery and consumer-state evidence establish asynchronous effects.

The cheapest valid oracle should fail first. Escalate only when the lower layer passes.

## Work without blind copying

Before executing a command, predict its outcome. Before planting a defect, predict the first proof gate that should fail. Before accepting a repair, name the permanent regression. When a result surprises you, classify the disagreement before editing:

- the mental model may be wrong;
- the contract may be wrong;
- the implementation may drift;
- the fixture or test may encode the wrong claim;
- the environment may be incomparable;
- the proof may be too weak for the claim.

## A practical study rhythm

Each course is designed as ten dense weekdays over two calendar weeks. A typical day contains four cycles rather than one uninterrupted session:

- concept and protocol reading;
- worked design and implementation reading;
- exercise attempt and answer review;
- lab, evidence capture, and checkpoint defense.

Take breaks before reasoning quality collapses. The middle weekend is for repair and synthesis, not hidden new curriculum. If one checkpoint fails, do not stack later material on top of it. Use the recovery route in [Study and assessment](study-and-assessment.md).

## First commands

From `programs/api-engineering`:

```bash
make doctor
make release-proof
```

Then enter Course 1 and follow its orientation. A green program proof confirms repository structure and dependency-light claims; it does not substitute for the live laboratories described in later courses.
