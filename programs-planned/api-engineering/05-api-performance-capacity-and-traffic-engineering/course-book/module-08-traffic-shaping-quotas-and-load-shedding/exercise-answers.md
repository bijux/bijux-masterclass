# Reference Answers — Module 08: Module 08 exercise answers — Traffic Shaping, Quotas, and Load Shedding

Read after attempting all twelve Traffic Shaping, Quotas, and Load Shedding exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. A bucket capacity is 100 tokens, refill 20/s, current 10, cost 50. How long until admission?

Forty tokens are missing. At 20 tokens/s, the minimum wait is 2 seconds, assuming no other consumption. Report a conservative value and let clients jitter.

## 2. Why use integer microtokens?

They avoid cumulative floating-point boundary differences between languages and permit fractional conceptual costs through scaling. Units and scale must be recorded.

## 3. How do rate and concurrency limits differ for long downloads?

Rate controls starts or cost over time; concurrency controls simultaneously active streams. A low start rate can still accumulate many long streams, so both may be needed.

## 4. Design a cost for uploads.

Reserve a base operation cost plus size-based units from validated length or charge incrementally per chunk. Also require an active stream permit and storage quota. Handle unknown length with a conservative cap or reject unsupported transfer mode.

## 5. What is an atomic multi-budget decision?

Global, tenant, principal, and operation budgets either all reserve successfully or none remains charged. Implement under one authority or with a reservation that rolls back pre-admission failure exactly.

## 6. When is 429 appropriate?

When the caller or policy partition exceeded a defined rate/quota/cost limit. It should return the documented problem response and truthful retry guidance. Service-wide incapacity may use 503 according to contract.

## 7. Why reserve capacity for cancellation/status?

These operations help stop work and let clients observe already admitted state. If overload blocks them, the system can consume more resources and violate reliability. Reservation must remain bounded.

## 8. Three instances each enforce 100 requests/s locally. What is the possible aggregate?

Approximately 300 requests/s, with distribution-dependent variation. It is not a 100 requests/s global limit. State the scope or use shared/global enforcement.

## 9. How can borrowing improve fairness and utilization?

Tenants may use unused global capacity while a minimum share remains protected for others. Define weights, borrowing ceiling, and behavior when protected demand appears; test skew and starvation.

## 10. What must a shedding ladder never do?

It must not silently weaken authorization, durability, response schemas, pagination, correctness or SLI populations. It may reject new work or use documented degradation options.

## 11. How should limiter keys be bounded?

Authenticate/normalize identities, expire inactive entries, cap total state, prevent attacker-controlled high cardinality, and retain durable quotas separately when exact long-horizon accounting is required.

## 12. Design a mixed-tenant traffic experiment.

Offer skewed reads, submissions, uploads, and downloads from at least two tenants. Record offered/admitted/completed cost, rejections by reason, waits, resource use, and journey objectives. Verify minimum share and critical controls under overload.
