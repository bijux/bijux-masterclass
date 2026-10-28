# Worked answers — Runtime Control Plane, Usage Intelligence, and Support Operations

## 1. Why must gateway state derive from approved releases?

Otherwise runtime routes can expose versions or paths the catalog and registry do not recognize. Desired-state synchronization makes drift visible and ties deployment to governance.

## 2. Which policies belong at the edge?

Transport security, authentication, coarse request size and rate limits, routing, and bounded metadata. Domain ownership, resource authorization, workflow state, and business retries belong to owning services.

## 3. Why is route drift dangerous?

Consumers may reach a retired version, an undocumented endpoint, or a route with stale security policy. Drift also makes incidents hard to assign to a release.

## 4. What is the difference between usage and value?

Usage counts interactions. Value measures successful consumer outcomes, reduced effort, safety, or business results. High usage can reflect retries, errors, or confusing documentation.

## 5. Why measure deprecated-version traffic?

It identifies migration impact and verifies whether deprecation communication is working. It must be combined with registered consumers because telemetry can miss dormant use.

## 6. What is support routing from catalog metadata?

The platform uses the API or component owner relation to choose the accountable domain team, while platform-specific categories route to the platform team.

## 7. Why avoid per-consumer high-cardinality metrics in the runtime data plane?

They can create cost, privacy, and performance risk. Product analytics can use bounded event pipelines or sampled records with retention and access controls.

## 8. How can a metric become surveillance?

Collecting individual developer behavior beyond a declared product purpose, retaining it unnecessarily, or using it for performance ranking changes an improvement signal into surveillance.

## 9. What is a platform SLO?

An objective for the platform service itself, such as catalog freshness, registry publication latency, sandbox creation success, or portal availability. It is distinct from the APIs’ own SLOs.

## 10. Why track support handoff failures?

They reveal unclear ownership or broken catalog relations. A ticket bouncing between teams is a platform defect even if the underlying API eventually works.

## 11. How should cost allocation be used?

To reveal platform operating trade-offs and high-cost workflows, not to incentivize teams to bypass safety controls. Allocation needs context and transparent methodology.

## 12. What does the capstone time-to-first-success metric show?

The reference consumer reaches success 240 seconds after credential issue. This is useful as a baseline; it is not representative production evidence until measured across real users and environments.
