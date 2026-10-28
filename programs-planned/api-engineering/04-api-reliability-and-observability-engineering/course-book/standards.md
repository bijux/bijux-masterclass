# Standards and Evidence — API Reliability and Observability Engineering

## How standards are used

Standards settle the protocol and compatibility questions relevant to **API Reliability and Observability Engineering**; they do not decide the architecture for you. Classify every cited rule as normative requirement, interoperability advice, course profile, observed tool behavior, or architecture decision.

## Standards profile

- W3C Trace Context Recommendation;
- OpenTelemetry specification and semantic conventions;
- Prometheus rule and metric semantics where used;
- HTTP deadline and retry-related semantics;
- course-defined reliability and SLO profiles;

## Reading discipline

Start from the module question, then read only the primary-source clauses needed for observe, diagnose, contain, and recover the promise. Restate the rule, build a counterexample in the Analysis Runs Platform, and name a falsifying oracle; citation alone never proves that the Python or TypeScript runtime conforms.

## Executable profile and frontier

Examples and proofs use the pinned Course 4 profile recorded in `course.json`: API 1.2 and Security Profile 1.0 preserved; Reliability Profile 1.0 introduced; migrations 001–008. A newer specification or tool does not silently change that profile; advance contracts, fixtures, compatibility rules, and the version ledger together.

## Evidence boundary

The strongest environment-backed claims in Course 4 require a multiprocess topology with telemetry export, injected dependency failure, and recovery. Local parsers, fixtures, unit tests, or simulators remain useful but support narrower claims; [Evidence model](evidence-model.md) names those boundaries.

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
