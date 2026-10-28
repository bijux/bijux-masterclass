# Glossary — API Reliability and Observability Engineering

Use this glossary alongside `program-book/glossary.md`. Program terms keep one meaning across all six courses; the entries below add course-specific distinctions.

Terms are defined as used in this program. When an Internet or OpenAPI specification gives a narrower normative meaning, the chapter and standards page name it.

## Critical journey

A user-meaningful sequence with explicit entry, eligible population, good and bad outcomes, and a durable oracle.

## Failure mode

A specific way a component or dependency can violate a journey, including detection and containment expectations.

## Deadline

An absolute monotonic time by which work must finish, propagated rather than reset at each layer.

## Timeout

A local waiting bound; several independent timeouts can exceed one caller deadline.

## Cancellation

A signal that work is no longer required; committed durable effects still need reconciliation.

## Retry budget

The bounded number and time of attempts permitted within one operation budget.

## Backoff

Delay between retry attempts, usually increasing and randomized with jitter.

## Circuit breaker

A dependency-local state machine that stops repeated calls after classified failures and permits bounded recovery probes.

## Bulkhead

A concurrency or resource partition that prevents one workload or dependency from consuming all capacity.

## Graceful degradation

A truthful reduced behavior that preserves accepted work and does not claim success for uncertain effects.

## Liveness

Whether the process should be restarted; it should not depend on every downstream dependency being healthy.

## Readiness

Whether the instance is currently safe to admit the class of work represented by the probe.

## Draining

A lifecycle state that rejects new ownership while completing, releasing, or persisting already-owned work.

## Telemetry

Operational events, metrics, and traces emitted for diagnosis; it is not the durable business record.

## Structured event

A versioned event name with bounded, typed, redacted attributes and explicit severity or outcome.

## Metric label

A bounded dimension used to partition a metric series; unbounded identifiers cause cardinality and privacy defects.

## Counter

A monotonically increasing measurement of accumulated events, interpreted with reset-aware queries.

## Gauge

A sampled current value such as queue depth or permits in use, with explicit ownership and collection semantics.

## Histogram

A distribution of observations across configured boundaries, used for latency and size analysis.

## SLI

A service-level indicator: a precise measurement of service behavior over an eligible event population.

## SLO

A service-level objective: a target for an SLI over a stated rolling window.

## Error budget

The amount of bad eligible behavior permitted by an SLO before its objective is exhausted.

## Burn rate

The rate at which an error budget is being consumed relative to the rate allowed by the objective.

## Trace context

Identifiers and flags propagated between components to correlate one distributed execution.

## Span link

A trace relationship used when asynchronous work is causally related but not a direct synchronous child.

## Cardinality

The number of distinct metric series or attribute values; unbounded cardinality can make telemetry unusable.

## Fault injection

A controlled, bounded introduction of a failure to test a stated hypothesis and oracle.

## Game day

A rehearsed operational exercise with roles, abort conditions, cleanup, and retained evidence.

## Reconciliation

Read-only comparison of durable facts to identify missing, duplicate, orphaned, or inconsistent effects.

## Repair key

A stable identifier making an approved repair action reviewable and idempotent.
