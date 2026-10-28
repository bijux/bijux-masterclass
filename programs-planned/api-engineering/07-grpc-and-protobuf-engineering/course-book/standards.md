# Standards and Evidence — gRPC and Protobuf Engineering

## How standards are used

Standards settle the protocol and compatibility questions relevant to **gRPC and Protobuf Engineering**; they do not decide the architecture for you. Classify every cited rule as normative requirement, interoperability advice, course profile, observed tool behavior, or architecture decision.

## Standards profile

- Protocol Buffers proto3 executable baseline;
- Protocol Buffers Edition 2024 standards frontier;
- gRPC status, deadline, cancellation, health, and reflection conventions;
- HTTP/2 flow-control concepts;
- inherited API, event, security, reliability, and performance profiles;

## Reading discipline

Start from the module question, then read only the primary-source clauses needed for engineer typed internal invocation and streaming. Restate the rule, build a counterexample in the Analysis Runs Platform, and name a falsifying oracle; citation alone never proves that the Python or TypeScript runtime conforms.

## Executable profile and frontier

Examples and proofs use the pinned Course 7 profile recorded in `course.json`: HTTP API 1.2 and Events API 1.0 preserved; RPC API 1.0 introduced; proto3 baseline; Edition 2024 frontier; migrations 001–015. A newer specification or tool does not silently change that profile; advance contracts, fixtures, compatibility rules, and the version ledger together.

## Evidence boundary

The strongest environment-backed claims in Course 7 require generated descriptors, a networked gRPC stack, TLS identity, and streaming peers. Local parsers, fixtures, unit tests, or simulators remain useful but support narrower claims; [Evidence model](evidence-model.md) names those boundaries.

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
