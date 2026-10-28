# Standards and Evidence — Event-Driven API Engineering

## How standards are used

Standards settle the protocol and compatibility questions relevant to **Event-Driven API Engineering**; they do not decide the architecture for you. Classify every cited rule as normative requirement, interoperability advice, course profile, observed tool behavior, or architecture decision.

## Standards profile

- AsyncAPI 3.1.0;
- CloudEvents 1.0-compatible event envelope;
- JSON Schema for message data where declared;
- inherited security, reliability, and performance profiles;
- course-defined replay, dead-letter, and consumer declaration profiles;

## Reading discipline

Start from the module question, then read only the primary-source clauses needed for extend the promise across asynchronous time. Restate the rule, build a counterexample in the Analysis Runs Platform, and name a falsifying oracle; citation alone never proves that the Python or TypeScript runtime conforms.

## Executable profile and frontier

Examples and proofs use the pinned Course 6 profile recorded in `course.json`: HTTP API 1.2 preserved; Analysis Events API 1.0 introduced; AsyncAPI 3.1.0; CloudEvents 1.0-compatible profile; migrations 001–012. A newer specification or tool does not silently change that profile; advance contracts, fixtures, compatibility rules, and the version ledger together.

## Evidence boundary

The strongest environment-backed claims in Course 6 require a live durable broker with retention, redelivery, consumer restart, and replay. Local parsers, fixtures, unit tests, or simulators remain useful but support narrower claims; [Evidence model](evidence-model.md) names those boundaries.

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
