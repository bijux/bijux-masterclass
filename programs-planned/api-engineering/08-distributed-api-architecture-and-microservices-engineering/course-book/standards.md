# Standards and Evidence — Distributed API Architecture and Microservices Engineering

## How standards are used

Standards settle the protocol and compatibility questions relevant to **Distributed API Architecture and Microservices Engineering**; they do not decide the architecture for you. Classify every cited rule as normative requirement, interoperability advice, course profile, observed tool behavior, or architecture decision.

## Standards profile

- the inherited HTTP, AsyncAPI, CloudEvents, Protobuf, and gRPC contracts;
- service identity and trace-context standards inherited from earlier courses;
- course-defined architecture fitness functions and release profiles;
- container and orchestration examples as implementation environments rather than normative architecture;

## Reading discipline

Start from the module question, then read only the primary-source clauses needed for distribute ownership deliberately. Restate the rule, build a counterexample in the Analysis Runs Platform, and name a falsifying oracle; citation alone never proves that the Python or TypeScript runtime conforms.

## Executable profile and frontier

Examples and proofs use the pinned Course 8 profile recorded in `course.json`: HTTP API 1.2, Events API 1.0, and RPC API 1.0 preserved; distributed architecture profile 1.0 introduced; owner-local migration histories begin. A newer specification or tool does not silently change that profile; advance contracts, fixtures, compatibility rules, and the version ledger together.

## Evidence boundary

The strongest environment-backed claims in Course 8 require independent processes, owner-local databases, real routing, mixed versions, and network faults. Local parsers, fixtures, unit tests, or simulators remain useful but support narrower claims; [Evidence model](evidence-model.md) names those boundaries.

## Primary-source review worksheet

For a rule used in a module, record:

```text
claim:
source and version:
category:
course interpretation:
smallest counterexample:
cheapest falsifying proof:
tool limitation:
```
