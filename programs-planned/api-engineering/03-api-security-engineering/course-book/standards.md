# Standards and Evidence — API Security Engineering

## How standards are used

Standards settle the protocol and compatibility questions relevant to **API Security Engineering**; they do not decide the architecture for you. Classify every cited rule as normative requirement, interoperability advice, course profile, observed tool behavior, or architecture decision.

## Standards profile

- OWASP ASVS 5.0.0 as a verification reference;
- OAuth and JWT RFCs for resource-server behavior;
- NIST digital identity and secure-development terminology where applicable;
- HTTP message and proxy semantics;
- course-specific webhook and audit profiles that are labeled as such;

## Reading discipline

Start from the module question, then read only the primary-source clauses needed for defend the promise. Restate the rule, build a counterexample in the Analysis Runs Platform, and name a falsifying oracle; citation alone never proves that the Python or TypeScript runtime conforms.

## Executable profile and frontier

Examples and proofs use the pinned Course 3 profile recorded in `course.json`: API 1.2 preserved; Security Profile 1.0 introduced; migrations 001–007. A newer specification or tool does not silently change that profile; advance contracts, fixtures, compatibility rules, and the version ledger together.

## Evidence boundary

The strongest environment-backed claims in Course 3 require an operated issuer, live network boundaries, and a real policy-enforcement path. Local parsers, fixtures, unit tests, or simulators remain useful but support narrower claims; [Evidence model](evidence-model.md) names those boundaries.

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
