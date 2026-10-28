# Standards and Evidence — API Performance, Capacity, and Traffic Engineering

## How standards are used

Standards settle the protocol and compatibility questions relevant to **API Performance, Capacity, and Traffic Engineering**; they do not decide the architecture for you. Classify every cited rule as normative requirement, interoperability advice, course profile, observed tool behavior, or architecture decision.

## Standards profile

- HTTP caching, ranges, compression, and conditional semantics;
- PostgreSQL plan and statistics documentation;
- reproducible benchmark and statistical methods declared by the course;
- inherited SLO and telemetry profiles;
- course-defined workload and performance evidence envelopes;

## Reading discipline

Start from the module question, then read only the primary-source clauses needed for sustain the promise under pressure. Restate the rule, build a counterexample in the Analysis Runs Platform, and name a falsifying oracle; citation alone never proves that the Python or TypeScript runtime conforms.

## Executable profile and frontier

Examples and proofs use the pinned Course 5 profile recorded in `course.json`: API 1.2, Security Profile 1.0, and Reliability Profile 1.0 preserved; Performance Profile 1.0 introduced; migrations 001–009. A newer specification or tool does not silently change that profile; advance contracts, fixtures, compatibility rules, and the version ledger together.

## Evidence boundary

The strongest environment-backed claims in Course 5 require representative load against a provisioned database and measured resource limits. Local parsers, fixtures, unit tests, or simulators remain useful but support narrower claims; [Evidence model](evidence-model.md) names those boundaries.

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
