# Test Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  lifecycle["test_policy_lifecycle.py"] --> aggregate["MonitoringPolicy aggregate"]
  evaluation["test_policy_evaluation.py"] --> policies["Evaluation policies"]
  app["test_application.py"] --> facade["MonitoringApplication facade"]
  runtime["test_runtime.py"] --> orchestration["MonitoringRuntime"]
  cli["test_cli.py"] --> review["Learner-facing inspection routes"]
  uow["test_unit_of_work.py"] --> persistence["Repository and unit of work"]
```

```mermaid
flowchart LR
  claim["Design claim"] --> suite["Choose the closest test suite"]
  suite --> behavior["Read the asserted behavior"]
  behavior --> owner["Name the responsible object"]
  owner --> decision["Decide whether the claim is actually proven"]
```
<!-- page-maps:end -->

Use this guide when you trust the test count less than the test shape. The goal is to map
each suite to the boundary it is defending instead of reading `tests/` alphabetically.

## Test route

1. `tests/test_policy_lifecycle.py`
2. `tests/test_policy_evaluation.py`
3. `tests/test_application.py`
4. `tests/test_runtime.py`
5. `tests/test_unit_of_work.py`
6. `tests/test_cli.py`

That route moves from aggregate authority into orchestration, persistence, and finally
the learner-facing review surface.

## What each suite proves

| Test file | Main proof question |
| --- | --- |
| `test_policy_lifecycle.py` | does the aggregate own lifecycle change directly and reject invalid transitions |
| `test_policy_evaluation.py` | do policy objects express evaluation behavior without leaking it into the aggregate |
| `test_application.py` | does the learner-facing facade preserve readable use cases without hiding domain ownership |
| `test_runtime.py` | does runtime coordination stay outside the aggregate while still publishing incidents correctly |
| `test_unit_of_work.py` | do repository and rollback boundaries behave as explicit persistence intent |
| `test_cli.py` | do the learner-facing inspection commands reflect the scenario honestly |

## Failure-first routing

| If this design drift happened... | Read first | Most likely first failing suite |
| --- | --- | --- |
| lifecycle rules moved out of the aggregate | `model.py` | `test_policy_lifecycle.py` |
| a new rule mode became a condition ladder instead of a policy seam | `policies.py` | `test_policy_evaluation.py` |
| orchestration started deciding domain truth | `runtime.py` and `application.py` | `test_runtime.py` |
| the learner-facing scenario stopped matching the intended use case | `application.py` and demo output | `test_application.py` or `test_demo.py` |
| persistence or rollback semantics became blurry | `repository.py` | `test_unit_of_work.py` |
| inspection output stopped telling the truth about the state | saved bundles and CLI output | `test_cli.py` |

## Best review questions

- Which test would fail first if rule activation moved out of the aggregate?
- Which test would fail first if a new rule mode were implemented with condition ladders?
- Which test would fail first if projections started mutating authoritative state?
- Which test would fail first if the learner-facing inspection route stopped matching the scenario?

Keep [DOMAIN_GUIDE.md](domain-guide.md) nearby when the test names are
clearer than the state transitions but you still need the lifecycle model in one place.

## When one suite is not enough

- pair lifecycle and evaluation suites when a change touches both aggregate ownership and replaceable policy behavior
- pair application and runtime suites when a scenario route crosses the public facade and orchestration boundary
- pair runtime and unit-of-work suites when infrastructure flow changes could blur persistence intent
- pair CLI and application suites when learner-facing output must still reflect the same story and ownership claims

## What this guide prevents

- counting green tests without knowing what they prove
- using runtime tests to justify domain ownership claims
- treating CLI output as if it were stronger proof than domain or runtime tests
- missing the difference between application-surface readability and aggregate authority
