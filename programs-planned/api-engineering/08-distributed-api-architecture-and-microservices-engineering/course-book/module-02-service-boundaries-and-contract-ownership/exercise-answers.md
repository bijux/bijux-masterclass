# Worked Answers — Module 02: Service Boundaries, Bounded Contexts, and Contract Ownership

Use these solutions to audit your reasoning for **Service Boundaries, Bounded Contexts, and Contract Ownership**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is RunService plus ProjectService plus DatasetService likely worse than Analysis Control?

Run creation needs project ownership, dataset readiness, policy, idempotency, and run initialization in one decision. Splitting nouns creates remote validation and transaction choreography without independent capability ownership.

**Decisive evidence:** use-case invariant map

The chapter’s decisive distinction is this: Nouns are easy to extract: Project, Dataset, Run, Artifact. Cohesive decisions are harder. CreateRun depends on project ownership, dataset readiness, algorithm policy, idempotency, capacity admission, and run-state initialization. Those rules form one capability even though they touch several nouns. A Run Service separated from Project and Dataset table services would call across the network to reconstruct a decision that was previously local.

## 2. What makes Worker Plane a compute plane rather than a business service?

It executes work and reports attempt outcomes, but durable lease generation and run state remain owned by Analysis Control. Its local session state is disposable.

**Decisive evidence:** state authority table

In the cumulative capstone, the rule becomes concrete: The catalogue must classify every component, assign one accountable owner, declare canonical data, and reject table-shaped services. You must be able to explain why Worker Plane is a deployment boundary but not a business-state boundary.

## 3. Can a gateway be called a microservice? Why is that label insufficient?

It may be independently deployed, but its architectural role is edge component. The important facts are that it owns routing and normalization, owns no business state, and cannot be the sole policy enforcement point.

**Decisive evidence:** service catalogue

A useful way to reason about the boundary is: A service boundary should contain a language and a set of invariants that can be understood together. In Analysis Control, “attempt,” “lease generation,” “run completion,” and “idempotency record” have precise meanings. Artifact Service has a different language: “staged object,” “published content,” “checksum,” “retention,” and “orphan.” Notification Service speaks about “subscription,” “delivery attempt,” “destination,” “retry schedule,” and “receipt.”

## 4. Why should Artifact Service not import Analysis Control domain classes?

Shared domain classes couple private models and release timing. Artifact Service needs a contract-specific mapping that preserves only the facts it requires.

**Decisive evidence:** anti-corruption mapping test

The implementation consequence is: Interface Contract owner State authority --- --- --- Public HTTP API 1.2 API product owner Analysis Control / Artifact Service by resource Analysis Events API 1.0 Analysis Control committed source service Analysis RPC API 1.0 Analysis Control method-specific owner Artifact RPC/HTTP 1.0 Artifact Platform Artifact Service Notification administration Notification Platform Notification Service

## 5. Who owns the `AnalysisRunCompleted` event contract?

Analysis Control owns the fact because it commits authoritative run completion. Consumers own their reaction, not the source event meaning.

**Decisive evidence:** event catalogue ownership

The important nuance is: For an event interface, ownership is more nuanced. The event producer owns the fact and schema meaning. Each consumer owns its projection, acknowledgement, and side effects. A consumer must not reinterpret AnalysisRunCompleted as “a notification was delivered.” The event means only that Analysis Control committed completion.

## 6. What is the difference between contract owner and state owner?

The contract owner governs interface semantics and compatibility. The state owner decides canonical business truth. They often align but must be recorded separately.

**Decisive evidence:** contract and state ownership matrix

Under concurrency or failure, the distinction becomes: Interface Contract owner State authority --- --- --- Public HTTP API 1.2 API product owner Analysis Control / Artifact Service by resource Analysis Events API 1.0 Analysis Control committed source service Analysis RPC API 1.0 Analysis Control method-specific owner Artifact RPC/HTTP 1.0 Artifact Platform Artifact Service Notification administration Notification Platform Notification Service

## 7. Why are generated Protobuf messages acceptable to share while a `canCompleteRun` library is risky?

Generated messages are contract artifacts. `canCompleteRun` contains mutable business policy and would make several services co-own a decision outside a service contract.

**Decisive evidence:** shared-library classification

The design remains honest only if: A package that contains canCompleteRun, calculateArtifactRetention, or authorizeProject can silently make multiple services co-own decisions. If two services need the same fact, expose a contract or replicate a view; do not distribute mutable policy as a package without an explicit governance model.

## 8. A service owns no data but has a distinct deployment and protocol. Is it invalid?

Not necessarily. Edge gateways and compute planes can be legitimate non-data components if their non-authoritative role and operational owner are explicit.

**Decisive evidence:** component-kind validation

The consumer-facing consequence is: Both tracks implement ServiceCatalog and require one writer per fact. The TypeScript track uses ReadonlySet to make ownership declarations non-accidental. The Python track returns the exact owner or fails. This is intentionally stricter than a runtime that “usually” routes to the right service.

## 9. How does ubiquitous language help detect a boundary?

Different precise meanings reveal separate contexts. Artifact `state` describes publication and retention; run `state` describes analysis lifecycle. Treating them as one enum couples unrelated rules.

**Decisive evidence:** language collision review

The operational consequence is: The same word may mean different things across contexts. In Analysis Control, an artifact reference means “the artifact attached to this completed run.” In Artifact Management, an artifact is a stored object with checksum, retention state, publication version, and access policy. The contexts exchange a stable artifact identifier rather than sharing one object model.

## 10. What indicates a distributed monolith even if services have separate repositories?

Shared database access, coordinated releases, chatty synchronous calls, shared domain libraries, and collective ownership show that autonomy is absent.

**Decisive evidence:** distributed-monolith rejection checklist

The strongest engineering interpretation is: A bounded context is a boundary within which terms, rules, and models have one coherent meaning. It is not automatically a process boundary. Course 8 uses contexts to clarify ownership before deciding deployment.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 11. Who owns an artifact reference stored in Analysis Control?

Analysis Control owns the reference as part of the run representation; Artifact Service owns the artifact object. The reference is not authority over content.

**Decisive evidence:** data ownership map

The defect-oriented view is: The same word may mean different things across contexts. In Analysis Control, an artifact reference means “the artifact attached to this completed run.” In Artifact Management, an artifact is a stored object with checksum, retention state, publication version, and access policy. The contexts exchange a stable artifact identifier rather than sharing one object model.

## 12. Why is one accountable operational owner a completion gate?

When failure occurs, someone must decide rollback, repair, and communication. Shared or missing ownership turns an interface into an organizational deadlock.

**Decisive evidence:** service catalogue owner proof

Across the Python and TypeScript tracks, the invariant is: Course 8 selects Design C. The contract is owned by Artifact Service as verifier and Analysis Control as issuer under an agreed profile. A capability does not transfer run authority; it authorizes one bounded artifact effect.
