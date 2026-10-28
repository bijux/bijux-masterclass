---
module_id: SARCH-036
program: Software Engineering: Software Architecture
level: 1
module_number: 36
title: Client-Server Architecture
status: complete
last_verified: 2026-09-06
---

# Client-Server Architecture

## One-Page Review

### Governing question

How should clients request capabilities from servers across an independently failing communication boundary while preserving authority, compatibility, state, capacity, security, and honest outcome semantics?

### Essential definitions

- A **client** initiates an interaction to request a capability; a **server** accepts requests and supplies that capability under a contract. These are roles in an interaction, not permanent machine types.
- A **request** communicates intent, target, parameters, identity, context, and sometimes content; a **response** communicates the server's protocol and application outcome.
- A **service interface** defines available operations and their semantics; a **protocol** defines message exchange and coordination rules.
- An **endpoint** is an addressable communication boundary; **service discovery** maps a logical service identity to reachable endpoints.
- A **session** relates interactions across time under an identity and lifecycle; it may be represented at client, server, shared store, or token.
- A **stateless server interaction** derives processing from the request and authoritative resources rather than hidden conversational state from earlier requests.
- An **intermediary** forwards, transforms, caches, authenticates, balances, observes, or filters an exchange between client and server.
- A **timeout** is a local decision to stop waiting; it does not prove the remote operation failed or was cancelled.
- **idempotency** means repeating the same identified operation has the same relevant intended effect as applying it once.
- **backpressure** and **admission control** constrain work before queues and resources become unstable.

### Central model, mechanism, or theorem

Model one logical operation $o$ as client attempts $a_1,\ldots,a_k$. Each attempt has lifecycle

$$
resolve\rightarrow connect\rightarrow authenticate\rightarrow send\rightarrow queue\rightarrow process\rightarrow commit\rightarrow respond.
$$

Observation can stop at any boundary. If a client times out after sending, the server may not have received, may be processing, may have committed, or may have responded with a lost response. Safe retry therefore depends on stable operation identity and effect semantics, not merely on a transport error.

For a stable service, Little's Law relates mean in-system work $N$, completed arrival rate $\lambda$, and mean time $W$ as $N=\lambda W$ under its assumptions. It is an accounting relation, not an overload-control policy.

### Critical invariants

- define client and server roles per interaction and identify the authority for every operation;
- separate logical service identity, discovery, endpoint, instance, process, and deployment;
- specify request, response, error, streaming, cancellation, and compatibility semantics;
- distinguish operation identity from attempt, connection, request, trace, and session identity;
- place durable state and session authority explicitly; do not rely on accidental process memory;
- treat timeout and disconnect as ambiguous remote outcomes unless the protocol establishes more;
- permit retry only under a stable identity and safe duplicate or outcome-query behavior;
- bound queues, connections, payloads, work, concurrency, and per-client resource use;
- propagate deadlines and cancellation without claiming cancellation guarantees remote rollback;
- authenticate endpoints and callers, authorize every operation, validate input, and minimize data;
- make intermediary transformations, caching, identity forwarding, and failure visible;
- observe logical operations, attempts, phases, server outcomes, committed effects, and saturation separately.

### Common failures

Common failures include treating client and server as fixed tiers; embedding endpoint addresses in policy; assuming a successful connection means service readiness; hiding server-side session in one instance; retrying timed-out writes blindly; using trace IDs as idempotency keys; trusting forwarded identity from any proxy; allowing unbounded queues or payloads; multiplying load with nested retries; caching personalized responses without correct variation; breaking old clients during rolling deployment; treating disconnect as cancellation; and reporting request counts without separating logical operations from attempts.

### Compact example

A client submits charge operation `chg-17`, sends the request, and times out. The server may have committed the charge. Retrying with a new identity can double-charge; retrying with `chg-17` lets the server return the existing outcome or perform the effect once under its idempotency contract. A trace ID links observations but does not replace the business operation identity.

### Connections

[SARCH-035](035-event-driven-architecture.md) contrasts fact publication and asynchronous reaction with directed requests. [SARCH-037](../ROADMAP.md) next develops microkernels and plugins. API and Service Engineering owns detailed protocol/API contracts; Network Engineering owns transport; Distributed Systems owns remote failure models and coordination.

## Governing Question

Client-server architecture assigns one participant the role of requesting a capability and another the role of supplying it. The simplicity is powerful: browsers use web servers, applications use databases, agents use control planes, and services call other services. A stable interface can separate implementation and enable many clients.

The communication boundary changes reasoning. Messages can be delayed, duplicated, reordered, refused, or lost. Client and server versions coexist. Intermediaries alter paths. Server capacity is finite. A timeout leaves uncertainty about remote effects. The governing question is how to design the relationship rather than merely connect two endpoints.

## Why This Matters

Client-server separation supports centralized authority, shared capabilities, independent implementation, access control, resource pooling, and scaling. It can isolate data and policy from user devices and allow many clients to evolve against a common contract.

It also creates availability dependencies, latency, partial failure, version skew, hot spots, attack surfaces, and operational burden. Stateful sessions can defeat load balancing. Retries can amplify overload. A thin client can become unusable offline; a thick client can duplicate policy and expose sensitive state.

Architecture must make the interface, state, authority, lifecycle, and evidence explicit. “The client calls the server” is a topology statement, not a reliability or correctness argument.

## Prerequisites and Retrieval

Retrieve process, host, endpoint, address, name, client, server, request, response, protocol, interface, connection, session, state, discovery, load balancer, proxy, cache, authentication, authorization, timeout, deadline, cancellation, retry, idempotency, partial failure, queue, concurrency, capacity, compatibility, and observability.

From SARCH-017 retrieve interoperability; SARCH-023 and SARCH-024 provide connectors and runtime interactions; SARCH-025 provides deployment; SARCH-035 provides asynchronous alternatives, identity, delivery, and outcome reasoning. Distinguish static dependency, runtime call, network path, and deployment placement.

## Learning Objectives

After completing this module, you should be able to:

1. define client and server as interaction roles rather than machine categories;
2. separate logical service identity, discovery, endpoint, instance, and connection;
3. specify request-response, one-way, and streaming interaction lifecycles;
4. place resource, session, cache, and client state deliberately;
5. reason about timeout ambiguity, retry, idempotency, and unknown outcomes;
6. design admission, queue, connection, and concurrency limits;
7. evaluate proxies, gateways, load balancers, and caches as semantic intermediaries;
8. preserve authentication, authorization, privacy, and trust across hops;
9. evolve clients and servers through mixed versions and rollback;
10. review operational evidence without confusing attempts, transport, and business effects.

## Core Exposition

**Treat client and server as roles.** A browser is client to an application server; that application becomes client to a database. A peer can be server for one operation and client for another. The terms do not imply hardware size, ownership, trust, or permanence.

State the system of interest and direction for each interaction. “Frontend” and “backend” can obscure multiple authorities and intermediaries. Name the requested capability and the participant authorized to decide it.

**Separate service identity from location.** A logical service has stable meaning and contract. Discovery maps that identity to endpoint records. An endpoint identifies a reachable protocol boundary. An instance is one running realization. A deployment unit and host are different again.

Hard-coding instance addresses into client policy couples identity to topology. Discovery can use configuration, naming systems, registries, or intermediaries. It needs freshness, authentication, failure, caching, rollout, and fallback semantics; a resolved address is not evidence that the endpoint is healthy or authorized.

**Define the interface before transport detail.** An operation contract states intent, target, input, identity, authorization, preconditions, result, errors, side effects, concurrency, idempotency, deadlines, and compatibility. Transport maps these semantics into messages.

HTTP semantics are standardized independently of a particular wire version in RFC 9110 [1]. RPC, database, and custom protocols have different models. A successful transport exchange does not mean the application accepted or committed the requested effect.

**Model the full attempt lifecycle.** Resolution, connection establishment, cryptographic negotiation, authentication, request transfer, server admission, queueing, processing, dependency work, commit, response transfer, and client interpretation consume time and can fail.

Instrument phase boundaries where they support diagnosis. A generic timeout hides whether scarcity was in DNS, connection pools, TLS, server queue, database locks, or response transfer. Yet tracing every internal event can be costly and sensitive; choose stable bounded attributes.

**Separate logical operation from attempts.** One user action may produce retries, redirects, hedges, proxy attempts, and dependency calls. Assign a stable operation identity when effects or outcome lookup require it. Each attempt gets its own identity and timing.

A trace or correlation identifier helps join observations but is not necessarily unique under business semantics, retained long enough, authenticated, or conflict-checked. An idempotency key needs scope, principal, operation, request fingerprint, lifetime, and stored outcome behavior.

**Understand remote ambiguity.** Birrell and Nelson's RPC work emphasized making remote calls resemble procedure calls while handling communication and binding [2]. The resemblance has limits. A local exception usually provides stronger knowledge of execution than a remote timeout.

After send, a timeout can correspond to no receipt, queued work, active work, committed effect, or lost response. “Retry on timeout” is safe only when the operation is idempotent under the same identity, the server can return an existing result, or reconciliation contains duplicates.

**Choose interaction form.** Unary request-response fits bounded work with one result. Server streaming fits a sequence of results after one request. Client streaming uploads a sequence under one operation. Bidirectional streaming supports ongoing exchange but needs independent direction, framing, flow control, cancellation, and reconnect state.

One-way messages reduce response coupling but still need acceptance and outcome semantics if work matters. If independent consumers react to a fact, event-driven architecture may be clearer. Do not call an asynchronous command an event merely because no immediate response is awaited.

**Place authoritative resource state.** Servers often centralize data and policy, but state may be partitioned, replicated, cached, or computed. Define the authority and freshness. A response from a replica can be valid yet stale; a cached response can outlive authorization or state.

Clients can retain drafts, optimistic views, and offline changes. Reconnection requires identity, version, conflict, and merge policy. “Server authoritative” does not answer how the user sees or reconciles uncommitted local work.

**Design session state.** A session relates exchanges through identity and lifecycle. Server-local sessions are simple but create affinity and loss during instance failure. Shared session stores support routing flexibility while adding a dependency and consistency cost. Client-carried tokens reduce server lookup but complicate revocation, size, confidentiality, and key rotation.

Prefer explicit resource and operation state when it has durable domain meaning. Do not hide a long business workflow inside an expiring web session. Define idle and absolute expiry, renewal, logout, concurrent use, fixation protection, failover, and recovery.

**Aim for stateless interaction where useful.** A stateless request carries enough context for any eligible server to process it against authoritative resources. This enables flexible load balancing and recovery. It does not mean the system has no state; the state is explicit and externally governed rather than accidental process memory.

Do not repeat large context or sensitive data solely to claim statelessness. Server-side state can be appropriate for streaming, transactions, leases, or coordinated workflows. Make affinity and failure semantics visible.

**Design concurrency at the server.** Servers multiplex connections and requests through processes, threads, event loops, workers, or actors. A connection is not a worker and concurrent streams may share one connection. Bound connections, active work, queues, memory, file descriptors, and dependency pools.

Per-client and per-tenant fairness matters. One client with slow uploads, expensive queries, or many streams can exhaust shared resources. Set size, time, rate, and concurrency limits at the earliest trusted boundary and align downstream limits to avoid moving the queue.

**Use admission control before collapse.** When offered load exceeds sustainable capacity, unbounded queues increase latency and memory until timeouts and retries amplify demand. Reject, shed, degrade, or queue within a defined bound. Return retry guidance only when clients can use it safely.

Little's Law $N=\lambda W$ relates mean in-system work, completed arrival rate, and mean time for a stable observed system [3]. If throughput is 200 requests/s and mean time is 0.25 s, mean in-system work is 50. It does not tell which queue is safe, predict percentiles, or apply unchanged during an unstable overload interval.

**Coordinate client and server time budgets.** The user objective bounds total operation time. Allocate resolution, connection, queue, processing, dependencies, and response. Propagate the remaining deadline rather than resetting a full timeout at every hop.

Cancellation is a request to stop. The server may already have committed, may be unable to interrupt safely, or may finish cleanup later. Define whether clients query outcome, receive a terminal response, or reconcile asynchronously. Never equate socket closure with rollback.

**Control retries and hedges.** Retry only transient failures and safe operations. Bound attempts, elapsed time, and load; add backoff and jitter. Respect server overload signals. Retry at one coordinated layer rather than at client, proxy, server, and dependency simultaneously.

Hedging can reduce tail latency by sending a second attempt but increases load and duplicate risk. It needs stable identity, cancellation, capacity, and evidence that tail benefit outweighs amplification. Do not hedge writes without strong effect semantics.

**Balance load with state awareness.** Load balancers select endpoints by algorithms and health signals. Round robin, least work, hashing, locality, and weighted methods serve different traffic. Health probes must reflect readiness to perform relevant work without turning deep dependency failure into synchronized removal.

Affinity can preserve local session or cache but creates hotspots and difficult failover. Consistent hashing reduces remapping but does not guarantee balanced work. When an instance drains, stop new admission, preserve or transfer required session/stream state, and bound termination.

**Treat intermediaries as architectural components.** Proxies, gateways, meshes, caches, and load balancers can terminate encryption, authenticate, route, retry, transform, compress, enforce limits, or observe. Each creates an additional trust, compatibility, capacity, and failure boundary.

Document hop-by-hop versus end-to-end metadata. Strip untrusted forwarding headers at the trusted edge and establish authenticated identity context. Preserve original authority and scheme only through governed mechanisms. A client must know which service it is authenticating, not merely which IP answered.

**Cache with semantic keys.** Client, proxy, and server caches trade freshness for latency and load. Define cache key, variants, authorization, validator, expiry, invalidation, negative results, and failure behavior.

Never cache personalized or tenant-specific responses under a shared key. A cache hit proves stored representation reuse, not current authoritative state. Clients making critical decisions may require revalidation, version constraints, or direct authority access.

**Version for coexistence.** Client releases can persist for years; server instances roll gradually; proxies and caches retain old data. Compatibility must cover old-client/new-server, new-client/old-server during rollback, persisted representations, and mixed intermediary behavior.

Prefer additive changes with defined defaults and tolerant handling where semantics permit. Removing fields, changing units, tightening validation, reusing error codes, or changing side effects can break clients without a syntax failure. Inventory clients and observe actual use, but unknown use remains uncertainty.

**Design security end to end.** Authenticate the intended server and the calling principal. Authorize each operation and resource, not merely the connection. Validate method, target, metadata, content type, size, schema, and semantic constraints. Protect confidentiality and integrity across every hop.

NIST SP 800-207 states zero-trust principles that avoid granting implicit trust based solely on network location [4]. Internal clients and proxies can be compromised. Constrain credentials, audiences, lifetimes, delegation, and forwarding. Minimize sensitive request, response, logs, traces, and caches.

**Handle errors as protocol and domain outcomes.** Distinguish malformed request, unauthenticated, unauthorized, absent, conflict, precondition failure, rate limited, dependency unavailable, deadline exceeded, and unknown result. Stable errors help clients decide whether to correct, retry, reconcile, or stop.

Do not expose internal stack traces or collapse every problem into generic failure. A proxy error and authoritative business rejection have different meaning even if both reach the client as non-success.

**Observe both sides.** On clients, record logical operation, attempts, selected endpoint class, phase timings, deadlines, cancellations, and interpreted outcome. On servers, record admission, queue, handler, dependency, commit, response, saturation, and rejection. Correlate across trusted boundaries.

Count attempts separately from logical demand. A retry storm can double server traffic while user operations remain constant. Reconcile operation identities to committed effects where correctness matters. Traces sample paths; they are not a transaction ledger.

**Test mixed failure and versions.** Contract-test request, response, error, authentication, authorization, idempotency, and streaming. Test old/new matrices, rollback, large and malformed messages, slow clients, connection exhaustion, overload, retry, cancellation, server restart, lost responses, stale discovery, proxy changes, and cache variation.

Fault injection must target lifecycle boundaries: before receipt, during queueing, before and after commit, during response, and during client interpretation. Verify terminal business outcomes rather than treating a returned timeout as proof of failure.

**Know the style's limits.** Client-server centralizes a service and creates a dependency on it. Peer-to-peer, event-driven, replicated local-first, batch transfer, or embedded architecture may better fit disconnected, symmetric, broadcast, or latency-critical problems.

Styles compose. A server may be a modular monolith, use event-driven integration, expose streaming APIs, and call other servers. Name the architecture at each boundary rather than applying one label to the entire system.

## Definitions and Notation

Let clients $C$ request logical operations $O$ from service $S$. Discovery $d(S,t)$ returns eligible endpoints at time $t$. An endpoint maps to a server instance under a deployment version and health state.

For logical operation $o$, attempts $A(o)=\{a_1,\ldots,a_k\}$ share stable effect identity when retry semantics require it. Each attempt records phase times $t_{resolve},t_{connect},t_{auth},t_{send},t_{queue},t_{process},t_{commit},t_{respond}$ where observable.

Let $state(o)\in\{not\_received,accepted,processing,committed,rejected,unknown\}$ from an authority's perspective. Client observation `timeout` maps to a set of possible remote states unless the protocol supplies a terminal outcome query.

For a stable measurement interval, Little's Law gives $N=\lambda W$. For phase budget $B$, necessary budgeting requires $\sum_i b_i\le B$ under compatible definitions; parallel phases and distributions require a richer model.

## Mechanisms, Invariants, or Proof Structure

**Role invariant.** Client and server identify initiator and provider for one interaction. Neither role implies trust, authority over all state, or fixed deployment.

**Identity invariant.** Logical operation, attempt, connection, session, trace, principal, resource, and effect identities are typed and not substituted without a declared mapping.

**Ambiguous-outcome argument.** If observation stops after request transmission but before a terminal authoritative response, executions with no receipt and with committed effect can be observationally identical to the client. Therefore timeout alone cannot decide whether retry duplicates an effect.

**Capacity invariant.** Every finite resource has admission and release rules. Offered work exceeding sustainable service results in a declared rejection, degradation, or bounded backlog rather than silent unbounded growth.

**Session invariant.** Required conversational state has one authority, lifecycle, failover, expiry, and security policy. Load balancing cannot assume local state that the selected instance lacks.

**Intermediary invariant.** Every transformation, retry, cache, identity-forwarding, and termination behavior is part of the end-to-end contract or explicitly transparent within bounded semantics.

**Compatibility invariant.** Every supported client/server/intermediary combination preserves the declared operation semantics under rolling deployment and rollback, not merely message parsing.

**Evidence invariant.** Connection, transport success, server response, commit record, and observed business outcome support different claims and are never treated as interchangeable.

## Alternatives and Trade-Offs

**Thin versus thick clients.** Thin clients centralize policy and updates but depend more on connectivity and server latency. Thick clients support responsiveness and offline work but duplicate state, compatibility, and security responsibilities.

**Stateless requests versus server sessions.** Stateless interaction simplifies routing and recovery but can repeat context and shift state to tokens or stores. Server sessions support efficient conversation while adding affinity, lifecycle, and failover.

**Direct endpoint versus intermediary.** Direct calls reduce hops and ambiguity. Intermediaries centralize discovery, routing, security, caching, and policy but add failure, trust, latency, and version surfaces.

**Synchronous response versus asynchronous outcome.** Synchronous calls give immediate results and simple control when work is bounded. Asynchronous acceptance handles long work and disconnection but requires operation resources, status, notification, cancellation, and retention.

**Central authority versus local replicas.** Central authority simplifies consistency and policy. Client or edge replicas improve latency and availability while requiring version, conflict, staleness, and reconciliation.

**Affinity versus free routing.** Affinity benefits local sessions and caches but creates imbalance and failover cost. Free routing needs shared or client-carried state and consistent authorization.

**Retry versus fail fast.** Retry masks brief faults but adds latency and load and can duplicate effects. Fail-fast protects capacity and exposes failure but can reduce success during transient recovery.

## Failure Modes and Misconceptions

1. **“Client and server are fixed machine types.”** They are roles in a particular exchange.
2. **“The endpoint is the service.”** Endpoints are current addressable realizations of logical capability.
3. **“Connection success means readiness.”** Authentication, admission, dependencies, and policy can still fail.
4. **“Stateless means no state.”** It means no hidden conversational dependency in the server interaction.
5. **“Timeout means the server did nothing.”** The effect may already be committed.
6. **“A trace ID is an idempotency key.”** Trace and effect identities have different scope and lifecycle.
7. **“Retries improve availability for free.”** They consume budgets and capacity and can amplify overload.
8. **“Disconnect cancels work.”** Remote commit or cleanup may continue.
9. **“Load balancing removes hotspots.”** affinity, skew, and expensive work can remain.
10. **“A proxy is transparent.”** It can retry, cache, transform, authenticate, and fail.
11. **“Internal networks are trusted.”** Identity and authorization remain necessary under the threat model.
12. **“Parsing compatibility means behavioral compatibility.”** validation, errors, side effects, and timing can change.
13. **“Queueing always increases resilience.”** Unbounded queues produce latency and collapse.
14. **“Server success proves business completion.”** Downstream or asynchronous effects may remain unresolved.
15. **“Every distributed relationship should be client-server.”** Broadcast, offline, symmetric, or event-driven forces may fit other styles.

## Worked Examples

### Example 1

**Situation.** A desktop client directly calls one calculator server with a versioned arithmetic interface.

**Reasoning.** Define operation, numeric domain, overflow, rounding, error, deadline, and server identity. The client role initiates; the server role calculates. If the same process later calls another service, it becomes a client in that interaction.

**Conclusion.** Even a minimal client-server design begins with role and semantic contract, not machine labels.

### Example 2

**Situation.** A payment request times out after send.

**Reasoning.** The server could have committed and lost the response. Retry with the same authenticated operation identity and request fingerprint; the authority returns the stored result or completes it once. If unsupported, query outcome or reconcile before another charge.

**Conclusion.** Timeout creates an unknown outcome that transport retry alone cannot resolve.

### Example 3

**Situation.** Three server instances handle stateless catalogue reads behind a load balancer.

**Reasoning.** Each request carries identity and query context and reads a declared replica. Any ready instance can answer. The design still has state in catalogue storage, discovery, cache, and authorization. Define replica freshness and cache variation.

**Conclusion.** Stateless interaction improves routing without making the system stateless.

### Example 4

**Situation.** Login session state lives only in instance A, but a later request reaches B.

**Reasoning.** B cannot reconstruct the conversation. Use governed affinity with failure consequences, a shared session authority, or client-carried protected state. Define expiry, revocation, failover, and concurrent use. Do not route blindly.

**Conclusion.** Session placement is an architectural state and availability decision.

### Example 5

**Situation.** A proxy caches a personalized account response under the path alone.

**Reasoning.** Another user's request can receive the first representation. Disable shared caching or include every authorized variant dimension in a safe key and response policy. Ensure identity headers are trusted only from the authenticated edge and that caches do not store prohibited data.

**Conclusion.** Cache keys and authorization semantics must agree.

### Example 6

**Situation.** A server completes 200 requests/s with mean in-system time 0.25 s.

**Reasoning.** Under stable Little's Law assumptions, mean concurrent in-system work is $N=200\times0.25=50$. This does not determine the safe connection limit or p99 latency. Inspect service distributions, queues, resources, and overload behavior before setting admission.

**Conclusion.** Mean concurrency accounting supports capacity reasoning but is not a sizing policy by itself.

### Example 7

**Situation.** A new server rejects a field old clients routinely send, while rollback servers cannot read new stored values.

**Reasoning.** Parsing success was not the whole compatibility matrix. Restore tolerant old-client behavior, version stored semantics, dual-read/write where safe, and test old/new clients, candidate/rollback servers, caches, and persistent state. Observe use before eventual removal.

**Conclusion.** Client-server evolution includes behavior and state across mixed versions.

### Example 8

**Situation.** An internal service trusts `X-User` from every caller because the gateway normally sets it.

**Reasoning.** A caller that bypasses or impersonates the gateway can forge identity. Strip the header at the trusted edge, authenticate the gateway or use end-to-end identity, bind user context cryptographically or through a governed channel, and authorize the resource at the server.

**Conclusion.** Forwarded identity is trustworthy only through an authenticated delegation design.

### Example 9

**Situation.** A client cancels a bidirectional stream while the server is committing the final item.

**Reasoning.** Cancellation stops the client's interest, not necessarily the commit. Define per-item identity and acknowledgment, half-close behavior, remaining deadline, server cancellation points, terminal status, and outcome lookup after reconnect. Release buffers and permits on both sides.

**Conclusion.** Streaming cancellation requires an outcome and resource protocol in both directions.

### Example 10

**Situation.** An emergency dispatch client connects field units to a regional server over intermittent networks.

**Reasoning.** Define command and incident identities, authority, priority, deadlines, acknowledgments, offline queue bounds, duplicate-safe dispatch, stale maps, operator override, and reconciliation. Use authenticated endpoints and protected location data. Preserve a local degraded procedure when the server is unreachable and test partitions, reconnect, overload, clock error, and human interpretation.

**Conclusion.** High-consequence client-server systems need explicit disconnected operation and independent safety procedures.

## Cross-Program Connections

- **API and Service Engineering:** resource, method, schema, error, authentication, retry, idempotency, compatibility, and streaming contracts deepen the interface.
- **Network Engineering:** naming, addressing, DNS, TCP, QUIC, TLS, connection behavior, congestion, and routing underpin communication.
- **Distributed Systems:** partial failure, clocks, replication, consistency, leases, consensus, retries, and reconciliation govern remote behavior.
- **Security Engineering:** endpoint identity, principal authentication, authorization, delegation, confidentiality, and input validation define trust.
- **Operating Systems:** sockets, processes, descriptors, scheduling, buffering, and resource limits define server mechanics.
- **Database Engineering:** transaction, session, pool, replica, cache, and stored-procedure clients demonstrate state and failure choices.
- **Software Delivery and Reliability Engineering:** discovery, load balancing, health, rollout, telemetry, overload, and incident recovery govern production.
- **Human-Computer Interaction:** offline state, progress, ambiguous outcome, cancellation, error, and accessibility shape client experience.

## References

1. IETF, *RFC 9110: HTTP Semantics*, June 2022. https://www.rfc-editor.org/rfc/rfc9110
2. Andrew D. Birrell and Bruce Jay Nelson, “Implementing Remote Procedure Calls,” *ACM Transactions on Computer Systems*, vol. 2, no. 1, 1984. https://doi.org/10.1145/2080.357392
3. John D. C. Little and Stephen C. Graves, “Little's Law,” in *Building Intuition: Insights From Basic Operations Management Models and Principles*, Springer, 2008.
4. NIST, *SP 800-207: Zero Trust Architecture*, August 2020. https://doi.org/10.6028/NIST.SP.800-207
5. Roy Thomas Fielding, *Architectural Styles and the Design of Network-based Software Architectures*, doctoral dissertation, University of California, Irvine, 2000. https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm
6. Maarten van Steen and Andrew S. Tanenbaum, *Distributed Systems*, 4th ed., distributed-systems.net, 2023. https://www.distributed-systems.net/index.php/books/ds4/
7. George Coulouris et al., *Distributed Systems: Concepts and Design*, 5th ed., Addison-Wesley, 2011.
8. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.

## Exercises

### Exercise 1

Precisely distinguish client, server, logical service, endpoint, instance, discovery, request, response, operation identity, attempt identity, session, and intermediary.

### Exercise 2

A stable service completes 480 requests/s with mean in-system time 125 ms. Compute mean in-system work using Little's Law. Explain at least four limits on using that result for capacity configuration.

### Exercise 3

Diagnose a client that resets a five-second timeout at each of four hops, retries three times at both gateway and SDK, sends a new idempotency key per attempt, and treats disconnect as cancellation. Produce a coherent policy.

### Exercise 4

Compare server-local sessions, a shared session store, and protected client-carried session state for an online learning system. Address routing, failure, consistency, security, revocation, size, privacy, and operations.

### Exercise 5

Transfer client-server architecture to a remote mine-safety system with underground clients, intermittent links, regional servers, sensor data, evacuation commands, local interlocks, operator consoles, software upgrades, and strict audit requirements. Define architecture and evidence.

## Answers to the Exercises

### Answer 1

A **client** initiates one interaction; a **server** supplies its requested capability. A **logical service** is the stable capability and contract. An **endpoint** is an addressable communication boundary; an **instance** is one running realization. **Discovery** maps logical identity to eligible endpoints.

A **request** communicates intent and context; a **response** communicates protocol and application outcome. **Operation identity** binds attempts to one intended effect; **attempt identity** distinguishes transmissions. A **session** relates interactions over a lifecycle. An **intermediary** forwards or changes routing, security, caching, retries, representation, or observation between roles.

### Answer 2

$125$ ms is $0.125$ s, so $N=\lambda W=480\times0.125=60$ mean requests in the measured system. The value does not give a percentile or peak; identify which queues and phases the time includes; require a stable interval where arrival and completion rates balance; and account for workload mix, service-time variance, dependencies, retries, streams, resource consumption, and per-tenant skew.

It also does not choose a safe connection or concurrency limit, predict behavior during overload, or prove 60 workers are needed because requests may wait asynchronously. Use phase distributions, saturation curves, load tests, queue-age objectives, and failure tests before configuring admission.

### Answer 3

Begin with one five-second end-to-end deadline derived from the user objective. Propagate remaining time through gateway, service, and dependencies; reserve response and cleanup time. Centralize retry policy so SDK and gateway do not multiply attempts. Bound attempts and total elapsed time, retry only transient safe cases, apply backoff and jitter, and honor overload signals.

Generate one operation/idempotency identity per intended effect and reuse it across attempts, with authenticated scope and request fingerprint. Give each attempt a separate trace/attempt identity. On timeout or disconnect after send, treat outcome as unknown; cancel best-effort, then query authoritative outcome or reconcile. Test commit-before-lost-response, nested dependencies, server restart, overload, late completion, and cleanup.

### Answer 4

Server-local sessions minimize lookup and can hold rich transient state, but require affinity and lose or strand state on failure and drain. Define replication or accept loss. A shared session store allows free routing and centralized expiry/revocation but adds latency, consistency, capacity, security, and a critical dependency.

Protected client-carried state reduces server storage and supports routing, but every request carries size, keys must rotate, revocation is harder, and exposed tokens must minimize personal data. Integrity protection does not necessarily provide confidentiality. Stale claims persist until expiry unless checked against authority.

For learning progress with durable meaning, use authoritative resource state rather than a session. Keep only conversational navigation or draft state in the session, define concurrent devices and expiry, and test failover, fixation, theft, revocation, key overlap, store outage, old clients, and privacy. A hybrid can use a short protected session identifier with shared authoritative state.

### Answer 5

Define logical services and regional endpoint discovery separately from instances. Underground clients carry device/operator identity, signed software/configuration version, bounded offline queues, command and observation identities, monotonic subject versions, and explicit stale state. Requests and streams specify size, priority, deadline, acknowledgment, retry, duplicate, and reconnect behavior.

Regional servers authenticate devices and operators, authorize commands, validate sensor provenance, bound admission by mine and priority, and persist outcomes. Evacuation commands use stable identities, per-zone order, repeated delivery, operator acknowledgment, and reconciliation. Server timeout never proves a field device did not act. Local physical interlocks and evacuation procedures remain authoritative when connectivity or software fails.

Use controlled intermediaries, endpoint authentication, least-privilege credentials, protected location and personnel data, auditable delegation, and signed updates with rollback. Isolate safety traffic from bulk telemetry. Version clients, servers, schemas, and stored state for rolling upgrade and rollback.

Test loss, delay, duplication, reorder, clock faults, partitions, reconnect, regional failover, overload, stale discovery, compromised clients, unauthorized commands, lost responses after commit, upgrade interruption, local interlocks, operator comprehension, and audit reconstruction. Record exact environments and residual risks; simulation and drills do not prove all physical mine conditions.
