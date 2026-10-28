# Standards and Evidence — OpenAPI Contract Engineering

## How standards are used

Standards settle the protocol and compatibility questions relevant to **OpenAPI Contract Engineering**; they do not decide the architecture for you. Classify every cited rule as normative requirement, interoperability advice, course profile, observed tool behavior, or architecture decision.

## Standards profile

- HTTP semantics and conditional request rules;
- OpenAPI 3.1.2 as the executable baseline;
- OpenAPI 3.2.0 as a standards-frontier profile;
- JSON Schema 2020-12;
- Overlay 1.1 and Arazzo 1.1;

## Reading discipline

Start from the module question, then read only the primary-source clauses needed for specify the public promise. Restate the rule, build a counterexample in the Analysis Runs Platform, and name a falsifying oracle; citation alone never proves that the Python or TypeScript runtime conforms.

## Executable profile and frontier

Examples and proofs use the pinned Course 1 profile recorded in `course.json`: Public API 1.1; OpenAPI 3.1.2 executable baseline; OpenAPI 3.2.0 standards frontier; no durable database yet. A newer specification or tool does not silently change that profile; advance contracts, fixtures, compatibility rules, and the version ledger together.

## Evidence boundary

The strongest environment-backed claims in Course 1 require a real provider conformance run and an independent OpenAPI validator. Local parsers, fixtures, unit tests, or simulators remain useful but support narrower claims; [Evidence model](evidence-model.md) names those boundaries.

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
