# Case 5 — The canary average lied

The candidate served mostly low-cost internal traffic and a small number of requests from one large tenant. Aggregate error rate passed, but every request for the tenant's largest dataset failed.

The metric population did not represent the changed path. Low sample size and aggregation hid the failure.

The repair requires minimum samples, affected-segment coverage, absolute thresholds, and exact analysis queries. Progressive delivery becomes a designed experiment rather than a percentage animation.

## Extended reader notes

### Timeline

The canary’s overall success rate exceeded 99.8%, and promotion completed. One tenant using large artifact metadata experienced 100% failure, but that tenant represented less than 0.1% of traffic.

### Root cause

The analysis used an aggregate average and did not segment the population implicated by the code change. Stable and candidate traffic mixes also differed.

### Durable correction

The hypothesis names large-artifact processing and affected tenants. Analysis requires minimum samples in that segment, exact payload-class dimensions, and both absolute and relative thresholds. Missing segment traffic is inconclusive rather than success.
