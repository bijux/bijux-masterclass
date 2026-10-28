# Worked Answers — Module 08: Traffic Shaping, Quotas, and Load Shedding

Use these solutions to audit your reasoning for **Traffic Shaping, Quotas, and Load Shedding**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. A bucket capacity is 100 tokens, refill 20/s, current 10, cost 50. How long until admission?

Forty tokens are missing. At 20 tokens/s, the minimum wait is 2 seconds, assuming no other consumption. Report a conservative value and let clients jitter.

The chapter’s decisive distinction is this: A rate limit controls how quickly work may arrive over a short horizon. A quota controls total consumption over a longer horizon. A concurrency limit bounds simultaneous active work. Capacity admission rejects when current downstream conditions cannot safely accept more work.

## 2. Why use integer microtokens?

They avoid cumulative floating-point boundary differences between languages and permit fractional conceptual costs through scaling. Units and scale must be recorded.

In the cumulative capstone, the rule becomes concrete: Cost weights are policy approximations and must be versioned. Do not set them solely from intuition; use Modules 3–7 evidence. A large request cannot lie about its cost: size-dependent costs are charged incrementally or reserved from validated content length and adjusted safely.

## 3. How do rate and concurrency limits differ for long downloads?

Rate controls starts or cost over time; concurrency controls simultaneously active streams. A low start rate can still accumulate many long streams, so both may be needed.

A useful way to reason about the boundary is: Rule Required behavior Failure if omitted Decisive evidence --- --- --- --- Control type explicit Rate, quota, concurrency, and capacity decisions are separate. One RPS number hides resource use. Traffic policy schema Cost versioned Operation/size weights derive from evidence and carry profile version. Policy changes silently alter capacity. Cost catalogue Atomic multi-budget decision Global/tenant/principal reservations cannot partially leak. Rejected request consumes some budgets.

## 4. Design a cost for uploads.

Reserve a base operation cost plus size-based units from validated length or charge incrementally per chunk. Also require an active stream permit and storage quota. Handle unknown length with a conservative cap or reject unsupported transfer mode.

The implementation consequence is: Requests per second alone can improve while cost or bytes explode. Compare admitted work with completed work and service objectives. Rejection is acceptable only when policy selects it and the response is correct.

## 5. What is an atomic multi-budget decision?

Global, tenant, principal, and operation budgets either all reserve successfully or none remains charged. Implement under one authority or with a reservation that rolls back pre-admission failure exactly.

The important nuance is: Global, tenant, and principal buckets can all apply. Admission succeeds only when all required budgets can be consumed atomically. A rollback mechanism returns reservations when a later policy layer rejects before work begins.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 6. When is 429 appropriate?

When the caller or policy partition exceeded a defined rate/quota/cost limit. It should return the documented problem response and truthful retry guidance. Service-wide incapacity may use 503 according to contract.

Under concurrency or failure, the distinction becomes: Equal per-tenant limits are simple but may waste capacity. Weighted fairness may reflect purchased service tiers or workload value. Borrowing unused capacity can improve utilization but must not eliminate a minimum share for others.

## 7. Why reserve capacity for cancellation/status?

These operations help stop work and let clients observe already admitted state. If overload blocks them, the system can consume more resources and violate reliability. Reservation must remain bounded.

The design remains honest only if: Reservation must be modest and measured; excessive reserved idle capacity lowers utilization. Ensure high-priority work does not depend on a lower-priority queue holding a lock or connection, a form of priority inversion.

**Evidence.** Calculate demand, utilization, queue growth, storage, egress, headroom, and uncertainty for several workload scenarios, then identify the first bottleneck.

## 8. Three instances each enforce 100 requests/s locally. What is the possible aggregate?

Approximately 300 requests/s, with distribution-dependent variation. It is not a 100 requests/s global limit. State the scope or use shared/global enforcement.

The consumer-facing consequence is: Requests per second alone can improve while cost or bytes explode. Compare admitted work with completed work and service objectives. Rejection is acceptable only when policy selects it and the response is correct.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 9. How can borrowing improve fairness and utilization?

Tenants may use unused global capacity while a minimum share remains protected for others. Define weights, borrowing ceiling, and behavior when protected demand appears; test skew and starvation.

The operational consequence is: Equal per-tenant limits are simple but may waste capacity. Weighted fairness may reflect purchased service tiers or workload value. Borrowing unused capacity can improve utilization but must not eliminate a minimum share for others.

**Evidence.** Drive overload across tenants and operation costs, then inspect admission, queue delay, bounded memory, fairness, 429/503 outcomes, and recovery.

## 10. What must a shedding ladder never do?

It must not silently weaken authorization, durability, response schemas, pagination, correctness or SLI populations. It may reject new work or use documented degradation options.

The strongest engineering interpretation is: Rule Required behavior Failure if omitted Decisive evidence --- --- --- --- Control type explicit Rate, quota, concurrency, and capacity decisions are separate. One RPS number hides resource use. Traffic policy schema Cost versioned Operation/size weights derive from evidence and carry profile version. Policy changes silently alter capacity. Cost catalogue Atomic multi-budget decision Global/tenant/principal reservations cannot partially leak. Rejected request consumes some budgets.

## 11. How should limiter keys be bounded?

Authenticate/normalize identities, expire inactive entries, cap total state, prevent attacker-controlled high cardinality, and retain durable quotas separately when exact long-horizon accounting is required.

The defect-oriented view is: Global, tenant, and principal buckets can all apply. Admission succeeds only when all required budgets can be consumed atomically. A rollback mechanism returns reservations when a later policy layer rejects before work begins.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 12. Design a mixed-tenant traffic experiment.

Offer skewed reads, submissions, uploads, and downloads from at least two tenants. Record offered/admitted/completed cost, rejections by reason, waits, resource use, and journey objectives. Verify minimum share and critical controls under overload.

Across the Python and TypeScript tracks, the invariant is: Reservation must be modest and measured; excessive reserved idle capacity lowers utilization. Ensure high-priority work does not depend on a lower-priority queue holding a lock or connection, a form of priority inversion.
