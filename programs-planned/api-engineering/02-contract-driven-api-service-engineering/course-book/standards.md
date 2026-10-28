# Standards and Evidence — Contract-Driven API Service Engineering

## How standards are used

Standards settle the protocol and compatibility questions relevant to **Contract-Driven API Service Engineering**; they do not decide the architecture for you. Classify every cited rule as normative requirement, interoperability advice, course profile, observed tool behavior, or architecture decision.

## Standards profile

- HTTP idempotency and conditional request semantics;
- RFC 9457 Problem Details;
- PostgreSQL transaction, locking, and constraint behavior;
- OpenAPI 3.1.2 inherited contract;
- language-specific framework documentation only where runtime behavior matters;

## Reading discipline

Start from the module question, then read only the primary-source clauses needed for implement the promise durably. Restate the rule, build a counterexample in the Analysis Runs Platform, and name a falsifying oracle; citation alone never proves that the Python or TypeScript runtime conforms.

## Executable profile and frontier

Examples and proofs use the pinned Course 2 profile recorded in `course.json`: API 1.1 preserved; additive API 1.2 introduced; OpenAPI 3.1.2 preserved; migrations 001–005. A newer specification or tool does not silently change that profile; advance contracts, fixtures, compatibility rules, and the version ledger together.

## Evidence boundary

The strongest environment-backed claims in Course 2 require concurrent PostgreSQL transactions, process termination, and migration coexistence. Local parsers, fixtures, unit tests, or simulators remain useful but support narrower claims; [Evidence model](evidence-model.md) names those boundaries.

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
