# Architecture Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph TD
  app["MonitoringApplication"] --> runtime["MonitoringRuntime"]
  runtime --> aggregate["MonitoringPolicy aggregate"]
  aggregate --> policies["Evaluation policies"]
  aggregate --> events["Domain events"]
  events --> projections["ActiveRuleIndex and IncidentLedger"]
  runtime --> sink["Incident sink"]
  runtime --> repo["Repository and unit of work"]
```

```mermaid
flowchart LR
  command["Learner command"] --> app["Application facade"]
  app --> domain["Domain model"]
  domain --> event["Events emitted"]
  event --> views["Read models updated"]
  views --> review["Snapshot, tests, and review surfaces"]
```
<!-- page-maps:end -->

This capstone is intentionally small, but its shape is strict. The domain is not buried
inside infrastructure, and the runtime does not quietly absorb domain rules. The goal is
to show an object-oriented design where ownership stays legible under change.

## Ownership boundaries

- `application.py` is the learner-facing use-case surface.
- `model.py` is the authoritative home of rule lifecycle and evaluation ownership.
- `policies.py` isolates replaceable evaluation behavior.
- `runtime.py` coordinates sources, sinks, projections, and units of work.
- `repository.py` expresses persistence intent and rollback semantics.
- `read_models.py` and `projections.py` remain downstream of events.

## Why this shape matters

The aggregate should stay authoritative for domain change. The runtime should stay thin
enough that replacing a source or sink does not change the rules of the domain. The
projections should stay derived so read concerns do not mutate authoritative state.

## Review routes for architecture questions

- Use `make inspect` when you want the derived state bundle before opening code.
- Use `make tour` when you want the learner-facing scenario route through the architecture.
- Use `make verify-report` when you need executable evidence alongside that review.
- Use `EXTENSION_GUIDE.md` when the architecture question is really a change-placement question.

## Architecture questions for review

- What would break if rule activation lived in the runtime instead of the aggregate?
- What would become harder to trust if the read models were updated directly?
- Which extension should modify `policies.py` without forcing a rewrite of `model.py`?

## Change placement

| If the change is... | Start in | Why |
| --- | --- | --- |
| a new rule lifecycle constraint | `model.py` | lifecycle authority belongs to the aggregate |
| a new evaluation mode | `policies.py` | variation should stay replaceable instead of widening the aggregate |
| a new sink or source integration | `runtime.py` | orchestration and adapters stay outside domain ownership |
| a new read model | `projections.py` or `read_models.py` | derived views should stay downstream of events |
| a persistence or rollback detail | `repository.py` | storage mechanics should adapt to the domain, not redefine it |

## Anti-patterns this architecture rejects

- runtime code deciding domain lifecycle transitions
- projections mutating authoritative state
- persistence concerns leaking into the aggregate's core rules
- evaluation variability implemented as condition ladders spread across multiple files
