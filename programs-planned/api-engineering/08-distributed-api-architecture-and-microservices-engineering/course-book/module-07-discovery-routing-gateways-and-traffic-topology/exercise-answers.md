# Worked answers — Discovery, Routing, Gateways, and Traffic Topology

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. What is the difference between service discovery and load balancing?

Discovery yields eligible endpoints and metadata. Load balancing chooses among them. Neither decides business semantics.

**Decisive evidence:** registry selection trace

## 2. Why should draining instances be removed from new traffic before process exit?

They need time to finish accepted requests and streams without receiving additional work. Liveness alone cannot express this state.

**Decisive evidence:** lifecycle routing test

## 3. What belongs in the edge gateway?

Public TLS, credential normalization, request budgets, protocol adaptation, routing, bounded composition, and public error translation—not domain transitions or private database access.

**Decisive evidence:** gateway responsibility audit

## 4. Why is one retry layer per edge important?

Multiple transparent layers multiply attempts and hide load. One accountable layer can apply idempotency, deadline, and observability correctly.

**Decisive evidence:** retry amplification test

## 5. How should a canary key be chosen?

Use a stable key such as tenant or resource when consistency matters, so the same flow does not bounce unpredictably between versions.

**Decisive evidence:** deterministic canary vector

## 6. Why can shadowing a write be dangerous?

The candidate may create duplicate or external effects. Writes need dry-run, effect suppression, or shared stable identity and comparison without authority.

**Decisive evidence:** shadow side-effect policy

## 7. What does a service mesh not know?

Business idempotency, resource ownership, compensation semantics, authoritative state, and whether a retry after commit is safe.

**Decisive evidence:** mesh/application responsibility matrix

## 8. When should an unhealthy instance remain live?

A process may be live for diagnostics and graceful recovery while not ready or accepting business traffic. Restarting it may make recovery worse.

**Decisive evidence:** liveness/readiness/drain evidence

## 9. Why filter instances by supported version before balancing?

Routing to a healthy but incompatible provider creates semantic failure. Eligibility includes contract compatibility.

**Decisive evidence:** version-aware routing test

## 10. What is wrong with gateway-to-database access for fast composition?

It bypasses service ownership, couples schemas, weakens authorization, and prevents independent evolution.

**Decisive evidence:** data access audit

## 11. How is failover different from retry?

Failover selects another eligible instance or region; retry repeats an operation. Both still require one deadline and safe effect semantics.

**Decisive evidence:** routing and retry ownership trace

## 12. Why does DNS stability not prove application readiness?

DNS maps names to addresses; it can outlive process readiness or include endpoints whose business dependencies are unavailable.

**Decisive evidence:** health observation test
