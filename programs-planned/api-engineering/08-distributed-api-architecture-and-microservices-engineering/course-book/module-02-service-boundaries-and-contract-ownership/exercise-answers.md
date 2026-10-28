# Worked answers — Service Boundaries, Bounded Contexts, and Contract Ownership

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. Why is RunService plus ProjectService plus DatasetService likely worse than Analysis Control?

Run creation needs project ownership, dataset readiness, policy, idempotency, and run initialization in one decision. Splitting nouns creates remote validation and transaction choreography without independent capability ownership.

**Decisive evidence:** use-case invariant map

## 2. What makes Worker Plane a compute plane rather than a business service?

It executes work and reports attempt outcomes, but durable lease generation and run state remain owned by Analysis Control. Its local session state is disposable.

**Decisive evidence:** state authority table

## 3. Can a gateway be called a microservice? Why is that label insufficient?

It may be independently deployed, but its architectural role is edge component. The important facts are that it owns routing and normalization, owns no business state, and cannot be the sole policy enforcement point.

**Decisive evidence:** service catalogue

## 4. Why should Artifact Service not import Analysis Control domain classes?

Shared domain classes couple private models and release timing. Artifact Service needs a contract-specific mapping that preserves only the facts it requires.

**Decisive evidence:** anti-corruption mapping test

## 5. Who owns the `AnalysisRunCompleted` event contract?

Analysis Control owns the fact because it commits authoritative run completion. Consumers own their reaction, not the source event meaning.

**Decisive evidence:** event catalogue ownership

## 6. What is the difference between contract owner and state owner?

The contract owner governs interface semantics and compatibility. The state owner decides canonical business truth. They often align but must be recorded separately.

**Decisive evidence:** contract and state ownership matrix

## 7. Why are generated Protobuf messages acceptable to share while a `canCompleteRun` library is risky?

Generated messages are contract artifacts. `canCompleteRun` contains mutable business policy and would make several services co-own a decision outside a service contract.

**Decisive evidence:** shared-library classification

## 8. A service owns no data but has a distinct deployment and protocol. Is it invalid?

Not necessarily. Edge gateways and compute planes can be legitimate non-data components if their non-authoritative role and operational owner are explicit.

**Decisive evidence:** component-kind validation

## 9. How does ubiquitous language help detect a boundary?

Different precise meanings reveal separate contexts. Artifact `state` describes publication and retention; run `state` describes analysis lifecycle. Treating them as one enum couples unrelated rules.

**Decisive evidence:** language collision review

## 10. What indicates a distributed monolith even if services have separate repositories?

Shared database access, coordinated releases, chatty synchronous calls, shared domain libraries, and collective ownership show that autonomy is absent.

**Decisive evidence:** distributed-monolith rejection checklist

## 11. Who owns an artifact reference stored in Analysis Control?

Analysis Control owns the reference as part of the run representation; Artifact Service owns the artifact object. The reference is not authority over content.

**Decisive evidence:** data ownership map

## 12. Why is one accountable operational owner a completion gate?

When failure occurs, someone must decide rollback, repair, and communication. Shared or missing ownership turns an interface into an organizational deadlock.

**Decisive evidence:** service catalogue owner proof
