# Worked Answers — Module 04: Synchronous Collaboration, API Composition, and Dependency Budgets

Use these solutions to audit your reasoning for **Synchronous Collaboration, API Composition, and Dependency Budgets**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why does a three-service serial path reduce availability?

The path requires all dependencies simultaneously. Approximate availability multiplies, so each additional required edge consumes the public objective.

**Decisive evidence:** dependency availability worksheet

The chapter’s decisive distinction is this: A remote call is not an implementation detail. It spends user latency and availability. If a public request calls Analysis Control and then Artifact Service serially, the request succeeds only when both services, both client libraries, name resolution, routing, and the network cooperate inside one deadline.

## 2. Why is a synchronous cycle more than a diagram smell?

It creates recursive failure, retry, deployment, and recovery coupling. Neither service can recover or release independently when each requires the other.

**Decisive evidence:** cycle detection proof

In the cumulative capstone, the rule becomes concrete: For reads, a bounded retry may be safe if the remaining deadline supports it. For mutations, retry requires durable request identity and an owner that can replay the original outcome. Course 2 established idempotency; Course 8 preserves it across services.

## 3. Who owns the deadline for a public request?

The edge that knows when the result loses user value. Downstream services receive remaining budget, not fresh timeouts.

**Decisive evidence:** deadline allocation trace

A useful way to reason about the boundary is: A caller knows the remaining objective for its operation. A callee knows only the budget it receives. Therefore the original caller establishes one absolute deadline and each layer derives a smaller child budget.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 4. What is wrong with retries in client, gateway, mesh, and callee simultaneously?

Attempts multiply, overload worsens, and ownership becomes invisible. One layer must own retries per edge with idempotency and remaining budget.

**Decisive evidence:** attempt-count fault test

The implementation consequence is: The capstone marks artifact enrichment as optional for the run view. Run authority remains available when artifact detail is temporarily unavailable. The response is partial, not silently successful as a complete representation.

**Evidence.** Run separate processes, remove one service, and measure dependency depth, fan-out, deadline propagation, partial response, routing ownership, and unaffected capabilities.

## 5. How should the gateway represent an unavailable artifact service for a completed run?

Return authoritative run state and explicit partial artifact status or warning, according to the public contract. Do not return an empty authoritative artifact list.

**Decisive evidence:** partial-response conformance

The important nuance is: If Control consumes 480 ms, the gateway cannot still grant Artifact a full 300 ms and keep the public promise. The caller either skips optional artifact enrichment, returns an explicit partial response, or fails according to policy.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 6. Why can parallel fan-out still be harmful when it lowers latency?

It increases instantaneous load, failure combinations, and downstream concurrency. Bound it and prefer batch interfaces.

**Decisive evidence:** fan-out resource profile

Under concurrency or failure, the distinction becomes: Parallel calls reduce elapsed time from the sum to approximately the maximum, but increase instantaneous demand and failure combinations. Bound concurrency. Prefer one batch call over hundreds of parallel calls. Propagate cancellation when the edge no longer needs the result.

**Evidence.** Run separate processes, remove one service, and measure dependency depth, fan-out, deadline propagation, partial response, routing ownership, and unaffected capabilities.

## 7. A run list triggers one artifact RPC per row. What should change?

Use summaries, a batch lookup, a local projection, or separate client-requested artifact connection. Remote N+1 is rejected.

**Decisive evidence:** call-count budget

The design remains honest only if: A fallback is correct only if it preserves the contract’s meaning. Returning an empty artifact list when Artifact Service is unavailable is misleading because “empty” means the authority has no artifacts. Returning stale authorization data may be unsafe. Returning a cached display label may be acceptable.

## 8. When can a read retry be safe?

When the operation is semantically safe, the status is retryable, remaining deadline covers another attempt, and one layer owns the retry.

**Decisive evidence:** retry policy vector

The consumer-facing consequence is: For reads, a bounded retry may be safe if the remaining deadline supports it. For mutations, retry requires durable request identity and an owner that can replay the original outcome. Course 2 established idempotency; Course 8 preserves it across services.

## 9. Why can service discovery not decide retry safety?

Discovery selects an address. It does not know whether a mutation committed or whether durable idempotency exists.

**Decisive evidence:** interaction ownership map

The operational consequence is: Kubernetes Services, DNS, client-side resolvers, proxies, and service meshes can locate healthy instances and balance traffic. They cannot decide whether a retry is safe, whether a partial response is truthful, or whether a deadline should be extended. Those remain application and contract decisions.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 10. What does maximum public synchronous depth protect?

It limits compounded latency, availability, and operational dependency on user-facing paths.

**Decisive evidence:** dependency graph fitness function

The strongest engineering interpretation is: Course 8 removes the reverse authorization call with a capability and forbids cycles in dependency-graph.yaml. A graph traversal can detect declared cycles, but runtime traces and code review are still needed to find undeclared calls.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 11. When should the gateway skip optional composition?

When remaining budget cannot satisfy the downstream call and the contract permits explicit partial data. It must not silently change semantics.

**Decisive evidence:** deadline degradation test

The defect-oriented view is: If Control uses 220 ms rather than 150 ms, Artifact receives at most the remaining budget; it does not start a fresh 550 ms timer. Timeout multiplication is one of the most common ways a service graph violates a public objective.

## 12. Why is a batch endpoint sometimes better than client-side concurrency?

It lets the owner optimize data access and enforce one bounded request, reducing network attempts and preserving authorization in one service.

**Decisive evidence:** batch contract and load evidence

Across the Python and TypeScript tracks, the invariant is: The reference DependencyGraph detects cycles and calculates public depth. Both tracks implement health-aware instance selection. The examples keep routing separate from business decisions: a registry returns an instance, not an authorization result.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.
