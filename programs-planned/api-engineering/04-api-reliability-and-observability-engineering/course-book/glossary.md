# Glossary — API Reliability and Observability Engineering

These terms have precise meanings in Course 4. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## critical journey

An end-to-end user or operator outcome whose correctness and availability are important enough to govern reliability decisions.

## failure mode

A specific way a component or interaction can fail, including its cause, observable symptoms, affected journey, and recovery path.

## deadline

An absolute time after which the caller no longer requires a result; child operations must derive budgets from it.

## timeout

A local waiting limit for one operation or phase; it must not be confused with the caller’s end-to-end deadline.

## cancellation

A signal that work is no longer needed and should stop or reach a safe boundary without corrupting durable state.

## retry budget

A bound on additional attempts, time, and load permitted after failure so retries cannot amplify an outage indefinitely.

## circuit breaker

A dependency-local state machine that temporarily rejects calls after qualifying failures and uses bounded probes to test recovery.

## bulkhead

An isolation limit preventing one dependency, tenant, operation, or workload from consuming all shared concurrency or capacity.

## liveness

Evidence that a process is running sufficiently to be restarted only when it is genuinely stuck, not merely unable to serve traffic.

## readiness

Evidence that an instance is currently safe to receive the traffic assigned to it.

## draining

A lifecycle state in which new work is refused while admitted work is allowed a bounded opportunity to finish or transfer safely.

## telemetry

Structured events, metrics, traces, and logs emitted to support diagnosis and operational decisions; telemetry is evidence, not business truth.

## metric cardinality

The number of distinct label combinations a metric can produce; unbounded dimensions can make the monitoring system itself fail.

## trace link

A causal association between spans when asynchronous work cannot be represented accurately as one direct parent-child chain.

## SLI

A precisely defined measurement of service behavior over an eligible population, such as successful completion within a latency threshold.

## SLO

A target for an SLI over a stated window, population, and measurement source.

## error budget

The amount of allowed bad SLI outcome implied by an SLO before the objective is exhausted.

## burn rate

The speed at which an error budget is being consumed relative to the rate that would exactly exhaust it over the objective window.

## game day

A controlled operational exercise with a bounded fault, explicit abort conditions, expected observations, cleanup, and retained evidence.

## reconciliation

A process that compares durable intent with observable effects and proposes stable, reviewable repair actions rather than guessing from telemetry.
