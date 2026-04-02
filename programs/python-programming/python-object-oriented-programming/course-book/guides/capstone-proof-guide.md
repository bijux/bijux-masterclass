# Capstone Proof Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  chapter["Module chapter"] --> proof["Capstone Proof Guide"]
  proof --> capstone["capstone/PROOF_GUIDE.md"]
  capstone --> commands["inspect, verify-report, confirm, and proof commands"]
```

```mermaid
flowchart LR
  claim["Design claim"] --> route["Pick a proof route"]
  route --> command["Run the command"]
  command --> inspect["Inspect output and tests"]
  inspect --> refine["Refine the design understanding"]
```
<!-- page-maps:end -->

Use this page when a chapter makes a design claim and you want the most direct executable
evidence in the capstone.

## Proof route

1. Read `capstone/PROOF_GUIDE.md`.
2. Run `make inspect` when you want the saved learner-facing snapshot before reading tests.
3. Run `make verify-report` when you want test output and learner-facing state in one review bundle.
4. Run `make confirm` when you want the strongest local confirmation route.
5. Run `make proof` when you want the sanctioned end-to-end route.
6. Use [Capstone Review Checklist](capstone-review-checklist.md) to decide whether the evidence is strong enough.

## What you should be able to answer after proof review

- Which object owns the checked behavior?
- Which output or assertion confirmed it?
- Which bundle or command is the best durable proof route for that claim?
- Which change would require a new or updated proof route?

## Best proof route by module stage

- Modules 01-03: start with `make inspect` and lifecycle-oriented tests.
- Modules 04-07: prefer `make verify-report` when aggregate, repository, or runtime boundaries are the claim.
- Modules 08-10: use `make confirm` or `make proof` when the question is full-system trust rather than one narrow behavior.

## Claim to proof map

| If the claim is about... | Inspect first | Best proof route |
| --- | --- | --- |
| value semantics, lifecycle rules, or aggregate ownership | `tests/test_policy_lifecycle.py` | `make inspect` |
| replaceable evaluation behavior | `tests/test_policy_evaluation.py` | `make verify-report` |
| runtime orchestration versus domain ownership | `tests/test_runtime.py` and `application.py` | `make tour` or `make verify-report` |
| public learner-facing behavior | `tests/test_application.py` and `tests/test_demo.py` | `make inspect` or `make tour` |
| full-system trust and saved executable evidence | saved verification bundle plus `PROOF_GUIDE.md` | `make confirm` or `make proof` |

## Smallest honest proof by question

- If the question is architectural, start with guides and targeted tests before `confirm`.
- If the question is behavioral, start with the smallest saved bundle or test that exercises the claimed behavior.
- If the question is course-level trust, escalate to `make proof` only after the narrower claims are already clear.
