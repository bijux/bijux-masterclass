---
module_id: PLAT-039
program: Platform Engineering
level: 1
module_number: 39
title: Database and Data-Service Access
status: complete
last_verified: 2026-09-02
---

# Database and Data-Service Access

## One-Page Review

### Governing question

How should a platform grant, deliver, observe, rotate, revoke, and retire application access to databases and other stateful data services while preserving least privilege, server identity, connection budgets, transaction semantics, tenant boundaries, and recoverable operations?

### Essential definitions

- A **data-service access contract** is the versioned platform interface joining a logical service, data namespace, workload identity, role, endpoint policy, transport policy, pool budget, transaction expectations, observability, and lifecycle owner.
- A **logical data-service identity** names the intended service and role, such as the writable orders database; it is not a particular host, Pod, address, or current primary.
- **Authentication** establishes a principal; **authorization** determines what that principal may do. Successful login is not proof of appropriate privilege.
- A **database role** is an authorization identity to which object, schema, function, row-policy, and administrative privileges may be granted.
- A **credential lease** is a time-bounded authorization artifact with issuance, renewal, expiry, and revocation semantics; its expiry does not necessarily terminate established sessions.
- A **connection pool** reuses a finite set of server connections for client work. Session, transaction, and statement pooling preserve different state and application semantics.
- A **connection budget** allocates the database's finite concurrent sessions across services, replicas, processes, pools, migrations, administration, failover, and recovery reserve.
- **Transaction isolation** constrains which concurrent effects a transaction may observe; it does not make arbitrary retries safe.
- **replica lag** is the separation between an accepted write and its visibility on a replica under the service's replication model.
- **expand-contract migration** introduces a compatible new schema before moving producers/consumers and removes the old schema only after evidence shows it is unused.

### Central model, mechanism, or theorem

For access request $q=(s,n,w,o,e)$, the catalog resolves logical data service $s$, namespace $n$, workload identity $w$, requested operation class $o$, and environment $e$ to contract revision $c$. Admission succeeds only when policy authorizes $w$ for a least-privilege role, an authenticated and server-verified transport reaches an acceptable endpoint, connection demand fits the allocated budget, and the application uses compatible pool, transaction, consistency, and migration semantics. This chain authorizes a bounded capability; it does not prove queries are correct, replicas are fresh, credentials have left memory, or old sessions have closed.

### Critical invariants

- Applications request logical service capabilities, not durable node addresses or administrator credentials.
- The platform derives database identity and role from authenticated workload identity and reviewed policy; client-supplied labels are not authorization evidence.
- Runtime, migration, read-only, operational, and break-glass duties use separate roles and separately audited paths.
- TLS verifies the intended server/service identity, not merely encryption to whichever endpoint answered.
- Network reachability and database authorization are independent controls; neither substitutes for the other.
- Pools are bounded end to end and their aggregate worst-case demand leaves capacity for failover, migrations, monitoring, and emergency work.
- Pool mode is compatible with session-local state, prepared statements, advisory locks, temporary objects, and transaction boundaries actually used by the client.
- Retries replay the whole transaction only for classified retryable outcomes and only when application effects are idempotent or otherwise replay-safe.
- Read routing states freshness and read-after-write guarantees; reachable replicas are not assumed current.
- Schema change authority, compatibility window, rollback, locking/resource budget, and retirement evidence are explicit.
- Telemetry identifies service/role/operation and bounded query shape without recording credentials, connection strings, query literals, parameters, or sensitive rows.
- Rotation, revocation, incident isolation, access review, and deprovisioning are rehearsed against live-session and cached-credential behavior.

### Common failures

Shipping a shared superuser password; embedding a fixed host; treating authentication as authorization; trusting a connection because it is encrypted without verifying hostname; allowing runtime code to migrate schemas; multiplying default pools across replicas until failover exhausts sessions; inserting a transaction pooler under session-dependent clients; retrying only the last statement; reading a stale replica immediately after a write; assuming credential TTL closes established sessions; using network policy as row authorization; relying on row-level security while privileged roles bypass it; logging SQL parameters; rotating credentials without testing reconnection; and deleting a catalog entry while sessions, grants, exports, or backups remain.

### Compact example

The `orders-api` requests `orders/write` through a catalog contract. Its signed workload identity is authorized to obtain a short-lived runtime role limited to named schemas and operations; migrations use a separate deployment role. Service discovery returns verified TLS parameters and acceptable primary endpoints rather than one node. Each application instance has a small pool, and the admission calculation includes replica count, rolling surge, migration connections, administrator reserve, proxy capacity, and database limits. Transactions classify serialization/deadlock failures and replay whole idempotent units. Replica reads are allowed only for explicitly stale-tolerant paths. Database spans record system, namespace, bounded operation, status, wait, and pool signals while sanitizing query text and excluding parameters. Rotation tests new admission, renewal, reconnect, old-credential rejection, and separately terminates old sessions where policy requires it.

### Connections

This capability consumes environment, identity, secret-delivery, connectivity, and observability contracts from [PLAT-033](033-environment-provisioning.md) through [PLAT-038](038-observability-provisioning.md). It supplies governed state access to later reliability, SLO, incident, security, compliance, cost, and developer-portal capabilities, and connects directly to database systems, distributed systems, security, and data engineering.

## Governing Question

What platform product lets a workload ask for the right data capability and receive only the identity, reachability, authorization, connection capacity, consistency behavior, and operational evidence it needs—without forcing every team to rediscover database security and failure semantics?

A database is not just an endpoint and password. Access crosses catalog ownership, workload authentication, secret issuance, DNS/service discovery, TLS, network policy, database roles and grants, pools, transactions, replicas, schema evolution, telemetry, incident controls, and eventual removal. A locally successful connection can still be globally unsafe.

The platform should offer a paved access workflow and explicit contract. Database administrators or managed-service owners retain responsibility for engine configuration, backup/recovery, physical replication, and privileged administration. Application teams retain responsibility for domain schemas, correct transactions, query behavior, compatibility, and data classification. Platform engineering integrates these responsibilities without pretending to own all of them.

## Why This Matters

Stateful services amplify mistakes. An overly broad role can alter every tenant, a pool storm can deny unrelated workloads, a retry can duplicate a payment, a migration can lock a hot table, a stale read can violate a user promise, and an exposed query parameter can leak regulated data into telemetry.

The happy path hides lifecycle risk. Credentials expire, certificates rotate, primaries fail over, replicas lag, endpoints move, application replicas surge, proxies restart, schemas change, and teams disappear. Access that was safe at admission may become stale, orphaned, or incompatible.

Standardization reduces this risk only when it preserves semantics. A universal proxy is harmful if it silently changes session behavior. Automatic read splitting is harmful if the application assumes read-after-write. Dynamic credentials are harmful if renewal failure produces a synchronized reconnect storm. The platform product must expose meaningful choices and non-guarantees.

Data access is also a governance boundary. The platform needs owner, purpose, environment, data classification, tenant scope, approvals, expiry, audit, and retirement evidence. It should make least-privilege access easier than copying a privileged connection string.

## Prerequisites and Retrieval

Retrieve relational database roles and grants, schemas and object ownership, TLS certificates and hostname verification, workload identity, secret leases, DNS/service discovery, firewall and Kubernetes NetworkPolicy semantics, connection pooling, file descriptors, transactions and ACID properties, isolation anomalies, idempotency, deadlocks and serialization failures, primary/replica replication, lag, schema migration, expand-contract compatibility, row-level security, quotas and timeouts, structured telemetry, audit logging, incident response, backup/restore, retention, and managed-service shared responsibility.

You should distinguish login from authorization; logical service from endpoint; client connection from database session; lease expiry from session termination; encrypted TLS from verified server identity; pool wait from query latency; transaction retry from statement retry; primary discovery from transparent connection migration; availability from freshness; network isolation from object/row authorization; migration authority from runtime authority; query shape from query values; and catalog retirement from complete data erasure.

## Learning Objectives

After completing this module, you should be able to:

1. define a versioned data-service access contract and ownership model;
2. map authenticated workload identities to least-privilege runtime, read, migration, and emergency roles;
3. design verified transport, service discovery, endpoint selection, and network controls;
4. calculate end-to-end pool budgets and select compatible pooling modes;
5. specify transaction, retry, timeout, cancellation, and overload semantics;
6. make primary/replica routing and consistency guarantees explicit;
7. govern schema migrations, tenant boundaries, telemetry, audit, and access review;
8. test rotation, revocation, failover, reconnection, and retirement under adverse conditions; and
9. operate database access as a discoverable, supportable platform product.

## Core Exposition

### Treat access as a product contract

Begin with a catalog entry, not a secret. Identify service owner, engine/provider, environment, logical database or namespace, data classification, residency, tenant model, availability tier, acceptable operations, consistency needs, migration owner, support path, cost center, and retirement policy.

An access request names a capability such as `orders/write`, `orders/stale-read`, or `analytics/append`; it should not ask for `db-17.internal:5432`. The catalog maps durable intent to changing endpoints, policies, roles, and operational controls.

Version the contract. Include workload selectors, role profile, endpoint/service name, TLS trust and identity requirements, authentication mechanism, network policy, pool allocation, timeouts, transaction expectations, replica policy, schema authority, observability, lease behavior, incident contacts, and non-guarantees.

Expose status separately from desired configuration: admitted identity, issued role, policy revision, current endpoint class, lease expiry/renewal, last rotation exercise, pool consumption, failed checks, and deprecation date. Do not expose raw credentials in the portal or status API.

### Establish ownership and separation of duties

The application owner defines domain data, query behavior, transaction boundaries, compatibility, and acceptable staleness. The platform owns the access API, identity integration, secret delivery, connectivity templates, pool guardrails, baseline telemetry, and lifecycle workflow. The database/provider owner governs engine availability, privileged roles, physical topology, backup/recovery, and engine-specific limits.

Record one accountable owner at every boundary. Shared responsibility without named decisions becomes nobody's responsibility during failover or a destructive migration.

Separate runtime, read-only, migration, operational diagnostic, replication, backup, and administrative roles. A runtime service should not create extensions, alter roles, grant privileges, bypass tenant policy, or drop schemas merely because deployment tooling needs those rights.

Break-glass access must be time-bounded, approved or retrospectively reviewed under declared emergency policy, strongly authenticated, session/query audited, and automatically revoked. It is not the normal workaround for missing platform functionality.

### Resolve logical service identity

Discovery should return endpoints that satisfy a requested role, such as writable primary or eligible read replica. PostgreSQL libpq can consider multiple hosts and `target_session_attrs`; selection still creates a connection to one server. That established connection does not migrate automatically when leadership changes.

Keep topology out of application configuration where possible, but do not conceal behavior the client must understand. State whether DNS, driver multi-host logic, managed endpoint, or proxy performs selection; what health evidence it uses; how long caches live; and how failover affects in-flight transactions.

Use distinct logical names when guarantees differ. A read-only endpoint with bounded or unbounded lag is not interchangeable with the write endpoint. An analytics warehouse and operational replica may expose similar SQL while carrying different freshness, workload, and governance contracts.

Test negative selection: no primary, all replicas too stale, certificate mismatch, partial DNS, proxy healthy but database unavailable, and endpoint advertising the wrong service role. Fail closed when identity or required role cannot be established.

### Authenticate workloads, not configuration labels

Use a verifiable workload identity rooted in the runtime trust system. Map namespace, service account, deployment identity, environment, and where justified artifact or policy claims to an authorized access profile. Do not trust a client-supplied `team`, `tenant`, or `role` field by itself.

Authentication may use database-native certificates, signed tokens, cloud identity, or a broker that issues database credentials. The choice must bind the authenticated workload to the intended database role and leave auditable issuance evidence.

PostgreSQL authentication selects a method by connection source, requested database, and requested user through ordered `pg_hba.conf` records. That admission mechanism is not a grant model. After login, privileges and row policies still decide allowed actions.

Avoid shared credentials across applications or environments. They prevent reliable attribution, force coordinated rotation, broaden incidents, and make selective revocation difficult.

### Issue and deliver leased credentials safely

Dynamic database credentials reduce long-lived secret reuse by creating a role or credential per service/lease under controlled creation statements. A secrets broker needs narrowly governed database-administrator capability to create, alter, and revoke those credentials; compromise of that broker path is highly consequential.

Define lease TTL, maximum TTL, renewal window, jitter, retry/backoff, cache behavior, fail-open/fail-closed policy, clock assumptions, and what occurs after expiry. Consumers must reload credentials and establish new connections before old credentials become unusable.

Lease revocation usually prevents new authentication with the revoked credential. It may not close sessions that already authenticated. If incident policy requires termination, separately identify and terminate sessions, drain pools, invalidate proxies, and verify application reconnection.

Deliver secret material through a memory-conscious channel with strict file/socket permissions, bounded caches, no environment/command-line exposure where avoidable, and redaction from events and crash output. Reference material by stable secret identity; never put passwords in Git, image layers, portals, tickets, or connection-string telemetry.

Rotation is a protocol: issue new, distribute, acknowledge/reload, establish and test new sessions, stop issuance of old, reject new old-credential login, drain or terminate old sessions, revoke old, and verify. Overlap may preserve availability but temporarily broadens valid credentials, so bound it.

### Authorize with least-privilege roles and ownership

Model privileges from operations and objects: connect to database, use schema, select/insert/update/delete named tables, execute named functions, use sequences, and read metadata only when required. Avoid broad ownership, superuser, database-create, role-create, replication, and blanket future-object grants for runtime clients.

Database object ownership often carries implicit alteration/drop powers. Use a controlled owner role that applications cannot assume; grant runtime privileges from that owner. Configure default privileges deliberately for objects created by the migration role, and test future-object behavior rather than assuming it.

Make destructive or bulk operations explicit. An application that ordinarily writes one tenant's rows may need a different governed job role for backfill or retention deletion, with lower concurrency and stronger audit.

Periodically reconcile requested, issued, effective, and used privileges. Remove unused grants after an evidence window and owner review. Detect direct manual grants, role membership drift, orphaned accounts, default-privilege changes, and privilege escalation through functions or ownership.

### Verify transport and server identity

TLS encryption protects traffic only to the peer actually connected. The client must validate a trusted certificate chain and match the intended hostname/service identity. An encrypted connection with disabled hostname validation can still reach an impostor or wrong internal endpoint.

Distribute trust anchors as governed configuration, separate from client credentials. Define certificate renewal overlap, revocation expectations, minimum protocol/cipher policy where appropriate, and behavior during trust-bundle rotation.

Do not silently downgrade from verified TLS to encrypted-but-unverified or plaintext because a certificate fails. Surface actionable errors without disclosing connection strings or credentials.

Client certificates may authenticate a transport identity, but the database still needs an intentional mapping to a role. Certificate subject strings are not automatically least-privilege authorization.

### Constrain network paths independently

Allow only intended workload namespaces/identities or network sources to reach the data service and port, with controlled egress, ingress, DNS, proxy, and cross-region paths. Managed services may require provider firewall, private endpoint, security group, or routing controls beyond Kubernetes.

NetworkPolicy is address/protocol/port reachability policy under the cluster networking implementation. It does not understand database schemas, SQL operations, rows, or role membership. Database authorization remains mandatory.

Observe denied and unexpected paths without treating source IP as stable workload identity in environments with NAT, proxies, or dynamic scheduling. Bind authorization to cryptographic workload identity where possible.

Document shared intermediaries. A proxy can collapse source addresses, terminate TLS, hold credentials, multiplex tenants, and become an authorization or audit boundary. Its compromise and outage domain must be included in the threat and reliability model.

### Budget connections end to end

Database sessions consume memory, process/thread slots, locks, transaction state, file descriptors, and scheduling capacity. The server's configured maximum is not an allocation target; reserve capacity for replication, health checks, migrations, administration, failover, and recovery.

Let service $i$ run $r_i$ ordinary replicas, allow surge $u_i$, and open at most $p_i$ server connections per replica. A conservative application demand bound is

$$D_{app}=\sum_i (r_i+u_i)p_i.$$

If proxy, migration, monitoring, administration, replication, and emergency reserves are $D_{proxy}$, $D_{mig}$, $D_{mon}$, $D_{admin}$, $D_{repl}$, and $R$, require

$$D_{app}+D_{proxy}+D_{mig}+D_{mon}+D_{admin}+D_{repl}+R \le C_{safe},$$

where $C_{safe}$ is an empirically safe database capacity, not simply `max_connections`. Account for multiple worker processes, tenants, database/user-specific pools, regions, deployment generations, and failover topology.

A proxy may accept many client sockets while holding fewer server sessions. Its client limit, file descriptors, queue, pool partitioning, authentication cost, and server pool must all be sized. High client acceptance does not create database capacity.

Apply acquisition deadlines and bounded queues. An unlimited wait queue moves overload into application memory and latency. Expose active, idle, waiting, timed-out, created, closed, and error counts by bounded service/role identity.

### Choose a pooling mode compatible with clients

Session pooling assigns one server connection for an entire client session and preserves session features, at lower multiplexing efficiency. Transaction pooling returns the server connection after each transaction and can break session-local assumptions. Statement pooling is more restrictive and prevents multi-statement transactions.

Inventory session state: `SET` behavior, prepared statements, temporary tables, session advisory locks, `LISTEN`, cursors, session authentication changes, and driver-specific initialization. PgBouncer documents which features are incompatible or conditionally supported by mode and configuration.

Do not place a transaction pooler under an ORM merely because simple tests pass. Exercise prepared statements, migrations, long transactions, cancellations, errors, reconnect, and every session feature used by production code.

Reset or discard server state between tenants according to pooler semantics. Cross-client leakage of search path, role, locale, timeout, or temporary state is a correctness and security defect.

### Define transaction and retry semantics

The contract states expected isolation, read/write transaction mode, maximum duration, statement/lock/idle-transaction timeouts, cancellation propagation, retryable error classes, maximum attempts, backoff/jitter, and idempotency mechanism.

Isolation levels constrain anomalies but do not remove conflicts. PostgreSQL serialization failures and deadlocks can require retrying the complete transaction from the beginning because every read and decision may depend on the failed execution.

Statement-only retry is unsafe when earlier statements changed state or influenced application decisions. Keep the retry boundary outside the transaction callback and make external effects—messages, HTTP calls, files—transactionally coordinated, idempotent, or delayed until commit evidence.

Commit outcome can be ambiguous when the connection fails. A blind replay may duplicate work. Use application operation keys, unique constraints, transactional outbox/inbox patterns, or a queryable result identity appropriate to the domain.

Long or idle transactions retain locks and old snapshots, obstruct cleanup, and consume pool capacity. Bound them and instrument age. Do not solve slow work by increasing every timeout without understanding lock and resource effects.

### Make replica consistency explicit

Classify reads: must observe the caller's prior write, must be linearizable/current enough for a decision, may be bounded-stale, or may be eventually consistent. Route only the latter classes to replicas unless the database/service provides a tested stronger mechanism.

Replica reachability and read-only status do not prove freshness. Measure replay position/time under engine semantics, distinguish clock-based approximations from log-position evidence, and define behavior when lag exceeds the contract: primary fallback, wait, stale/error response, or feature degradation.

Failover changes endpoint roles and may lose or reorder observations under the service's durability model. Reconnect and re-evaluate the endpoint; do not assume an established socket changes from old primary to new primary.

Cross-region reads trade latency and survivability against freshness, egress, residency, and conflict models. Make region and consistency part of the logical capability instead of an invisible routing optimization.

### Govern schema migrations separately

Migration tooling uses a dedicated identity and role, not the application's runtime credential. It should acquire an owned deployment/migration lease, record schema revision, enforce time and lock budgets, and emit start/result evidence without logging sensitive SQL values.

Prefer expand-contract: add compatible structures, deploy code that can tolerate old and new, backfill with bounded load and checkpoints, switch reads/writes, prove old consumers absent, then remove obsolete structures. Transactional DDL support does not make every migration instantaneous or rollback-safe.

Estimate locks, table rewrites, index build behavior, replication lag, disk amplification, and recovery time using the actual engine/version and representative data. A migration that passes on an empty staging database proves little about production load.

Prevent concurrent incompatible migrations. Define roll-forward and rollback boundaries, especially after irreversible data transformation. Backups support recovery but are not a substitute for compatibility or rehearsed restore.

### Enforce tenant and data boundaries in layers

Choose database-per-tenant, schema-per-tenant, table partition/key, or shared-table policies from isolation, scale, operations, and cost. Each model changes pool multiplication, migration fan-out, backup/restore, noisy-neighbor, and deletion behavior.

Row-level security can restrict rows using policies, but policy correctness, role attributes, ownership, bypass privileges, functions, session context, and maintenance paths matter. Treat it as defense in depth and test both allowed and denied cross-tenant queries.

Do not rely on client-supplied tenant identifiers without binding them to authenticated authorization context. Set tenant context in a way compatible with the selected pool mode and reset behavior.

Encryption, tokenization, masking, and column privileges may protect sensitive fields, but query results, indexes, replicas, backups, exports, logs, and caches share the lifecycle. Classify the entire path.

### Bound queries, work, and overload

Set per-role/service connection, statement-time, lock-time, transaction-time, memory, CPU/IO, queue, and concurrency controls supported by the engine or proxy. Limits should protect shared capacity without turning ordinary variance into widespread retries.

Cancellation must propagate from request deadline through driver and database. Closing a client request without cancelling database work leaves invisible load. Conversely, cancellation acknowledgement may race with commit, so preserve ambiguous-outcome handling.

Use admission control and workload classes for interactive requests, background jobs, migrations, analytics, and administration. One bulk export should not consume all connections or IO needed for user transactions.

Detect overload through pool wait, connection errors, server saturation, lock waits, long transactions, rejected work, replica lag, proxy queue, and deadline exhaustion. Coordinate retry budgets so clients, proxies, drivers, and service meshes do not multiply attempts.

### Observe access without leaking data

Record catalog/contract revision, logical service, database system and namespace where safe, role class, endpoint role/region, operation class, pool wait, connection setup, transaction outcome, retry count, cancellation, timeout, and server status/error type with bounded values.

OpenTelemetry database span conventions permit database system, namespace, operation, status, and sanitized query information. Query text must be sanitized, parameter values excluded by default, and a low-cardinality query summary preferred for aggregation. A logical operation span may cover retries while attempt detail remains bounded.

Never record passwords, tokens, certificate keys, full connection strings, raw bind parameters, result rows, unbounded SQL literals, or tenant/personal identifiers without a separately governed need. Hashing an unbounded sensitive value does not make it low-cardinality or necessarily anonymous.

Correlate database evidence with workload, environment, artifact, configuration, access-contract, credential-policy, schema, and deployment revisions. Do not use trace ID as an authentication principal.

Audit issuance, role/grant changes, break glass, migrations, destructive jobs, policy decisions, and administrative access. Audit systems need integrity, access, retention, and clock semantics distinct from debug telemetry.

### Test the complete access path

Static validation checks contract schema, owner, workload selector, role profile, forbidden privileges, TLS verification, endpoint mode, pool calculation, timeouts, telemetry policy, and retirement date. Admission tests prove both permitted and denied identities.

Integration tests connect through the real discovery, TLS, authentication, proxy, and role path. Assert allowed and forbidden database operations, tenant boundaries, session-state reset, timeout/cancellation, retry classification, and sanitized telemetry.

Failure exercises cover broker unavailable, lease renewal failure, old/new credential overlap, forced revocation, pool saturation, database restart, proxy restart, DNS/cache delay, certificate mismatch, no primary, replica lag, failover during transaction, ambiguous commit, migration lock, and audit-pipeline impairment.

Measure recovery rather than just initial success: time to reconnect, number of synchronized attempts, demand spike, old sessions remaining, transaction outcomes, stale reads, and user impact. A successful health check is not proof that application transactions recovered.

### Operate rotation, incident response, and revocation

Provide runbooks and automation for planned credential/certificate rotation, primary failover, pool drain, role restriction, workload isolation, query cancellation, session termination, and break-glass investigation. Every action states blast radius and rollback/roll-forward conditions.

During suspected credential compromise, stop new issuance, narrow network access, revoke authentication material, terminate relevant sessions when required, rotate broker/admin paths, inspect role/grant drift, and preserve audit evidence. Rotation alone leaves established sessions and copied data unaddressed.

Avoid global restarts as the default response. Target logical access identity, role, database, service, tenant, or connection generation where possible. Verify containment from database sessions and policy evidence, not only automation success.

After recovery, reconcile desired/effective grants, credential generations, open sessions, endpoints, schema revision, replica health, telemetry, and catalog status. Incident work often creates temporary exceptions that must expire.

### Retire access and data deliberately

Retirement starts with consumer inventory and a deprecation window. Stop new clients, prove no required reads/writes, drain pools, terminate residual sessions, revoke leases and static credentials, remove role membership/grants, delete roles where safe, remove network and proxy routes, and archive audit evidence.

Coordinate schema/data disposition with retention, legal hold, backup, replica, cache, export, and analytics owners. Removing live access is not proof of immediate erasure from every governed copy.

Remove service discovery, monitors, alerts, cost allocation, documentation, and support ownership only after confirming they have no remaining consumers. Preserve enough tombstone metadata to prevent accidental reuse of a retired identity.

Test that the retired workload cannot authenticate, connect, assume the role, or access data from expected network paths. Record residual backup/retention limits and the accountable owner until final disposition.

### Present one coherent platform API

The platform API might expose `DataService`, `DataAccess`, `RoleProfile`, `PoolBudget`, `MigrationRun`, and `AccessRetirement` resources. Defaults should be secure, visible, and overridable only through reviewed policy.

The developer portal shows capabilities, owners, guarantees, examples, client configuration references, current status, pool use, lease health, migration/schema revision, incidents, and deprecation—never raw secret values.

Scorecards should measure contract ownership, workload identity, least privilege, verified TLS, bounded pools, transaction semantics, rotation/revocation exercises, telemetry/audit, and retirement ownership. A green score is evidence of declared and tested controls, not proof of correct data behavior.

Treat engines and providers as adapters behind the contract, not as perfectly interchangeable implementations. Preserve engine-specific semantics for roles, authentication, pooling, isolation, replication, migrations, cancellation, and session termination.

The following executable inventory is synthetic governance evidence. It counts declared controls and does not demonstrate database correctness, policy effectiveness, availability, freshness, confidentiality, or successful revocation.

<!-- bijux-verify: {"id":"database-access-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"contracts 10\ncatalog_owned 10\nworkload_identity 9\nleast_privilege_role 9\ntls_verified 9\npool_budgeted 8\ntransaction_semantics 8\nrotation_revocation_tested 7\naudit_observed 9\nretirement_owned 8\n","stderr":""}} -->
```python
access_contracts = [
    ("orders", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("payments", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("catalog", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("identity", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("shipping", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("support", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("search", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("recommendations", 1, 1, 1, 1, 1, 1, 0, 1, 1),
    ("analytics", 1, 1, 1, 1, 0, 0, 0, 1, 0),
    ("legacy-reporting", 1, 0, 0, 0, 0, 0, 0, 0, 0),
]
fields = [
    "catalog_owned", "workload_identity", "least_privilege_role",
    "tls_verified", "pool_budgeted", "transaction_semantics",
    "rotation_revocation_tested", "audit_observed", "retirement_owned",
]
print("contracts", len(access_contracts))
for index, field in enumerate(fields, start=1):
    print(field, sum(row[index] for row in access_contracts))
```

## Definitions and Notation

Let access request $q=(s,n,w,o,e)$ contain logical service $s$, namespace $n$, authenticated workload identity $w$, operation class $o$, and environment $e$. Catalog resolution under contract revision $c$ yields role profile $a$, endpoint policy $h$, transport policy $t$, pool policy $p$, transaction/consistency policy $x$, and lifecycle policy $l$.

Let $A(w,a,c)$ mean the policy engine authorizes identity $w$ for role profile $a$ under revision $c$. This predicate depends on verified claims and policy; it is not implied by a successful network connection or client label.

Let $V(h,t)$ mean endpoint selection found an acceptable service role and TLS verified the intended identity under trust policy $t$. It does not imply the endpoint is current, performant, or free from compromise beyond the trust assumptions.

For service $i$, ordinary replicas $r_i$, surge replicas $u_i$, and maximum server connections per replica $p_i$ give conservative demand $(r_i+u_i)p_i$. Summed demand plus proxy, migration, monitoring, administration, replication, and emergency reserves must not exceed empirically safe capacity $C_{safe}$.

Let transaction attempt $T_j$ read state, compute decisions, write state, and possibly coordinate external effects. A retryable database error permits a fresh attempt only if the complete unit is replay-safe. It does not authorize repeating only failed statement $k$ or duplicating effects already committed externally.

For write log position or equivalent commit marker $L_w$ and replica replay marker $L_r$, visibility may require $L_r\ge L_w$ under engine semantics. Time-based lag is an approximation and depends on clocks, propagation, and measurement points.

## Mechanisms, Invariants, or Proof Structure

The database-access assurance chain is:

1. catalog the logical service, namespace, owner, data class, purpose, guarantees, and lifecycle;
2. authenticate the workload and authorize a reviewed least-privilege role profile;
3. issue and deliver bounded credentials or identity assertions with renewal and revocation semantics;
4. discover an acceptable endpoint and verify transport plus intended server identity;
5. permit only required network paths while retaining database object/row authorization;
6. admit bounded connections through a pooling mode compatible with client session behavior;
7. execute under declared transaction, retry, timeout, cancellation, consistency, and migration semantics;
8. observe bounded operational evidence and protected audit records without leaking data or credentials;
9. exercise rotation, failover, revocation, session termination, recovery, and incident controls; and
10. deprecate, drain, revoke, remove, and govern residual data copies through retirement.

The chain is conditional. It does not prove the application chose correct SQL, a database engine is defect-free, a replica is fresh, a migration is fast, a credential never leaked, a policy expresses business intent, an audit stream is complete, or retained copies were erased.

The invariants are logical capability addressing, identity-derived authorization, separated roles, verified TLS, layered network/database controls, finite connection demand, pool compatibility, whole-transaction replay safety, explicit replica freshness, governed schema authority, sanitized evidence, and tested lifecycle controls.

## Alternatives and Trade-Offs

**Static versus dynamic credentials:** static credentials are simple and can survive broker outages, but persist, spread, and rotate poorly. Dynamic credentials improve attribution and bounded issuance while adding broker privilege, renewal, reconnection, and revocation complexity.

**Direct connections versus proxy/pooler:** direct drivers preserve engine/session semantics and remove a hop. A proxy centralizes pooling, discovery, policy, and telemetry but adds capacity, state, identity, compatibility, and failure domains.

**Session versus transaction pooling:** session pooling supports session-local features at higher server-session cost. Transaction pooling multiplexes efficiently but requires transaction-clean clients and careful prepared-statement/session-state behavior.

**Database roles per service versus shared roles:** per-service roles improve attribution and revocation. Shared roles reduce objects and configuration but broaden blast radius and obscure accountability.

**Primary reads versus replicas:** primary reads provide simpler read-after-write behavior but load the write path. Replica reads scale and localize traffic while adding lag, routing, failover, and consistency decisions.

**Database-, schema-, or row-based tenancy:** stronger physical/logical separation improves some isolation and restore workflows but multiplies pools, migrations, and cost. Shared tables scale operations efficiently but demand rigorous authorization and noisy-neighbor controls.

**Application versus platform migrations:** application-owned migrations keep domain context near code. A platform runner can standardize leases, credentials, audit, and guardrails but must not pretend engine-specific risk is generic.

**Fail closed versus cached continuity:** refusing access when identity/secret control planes fail limits unauthorized admission. Carefully bounded cached material may preserve availability, but extends exposure and requires explicit expiry and incident semantics.

**Provider abstraction versus engine-native features:** a common contract improves usability and governance. Lowest-common-denominator APIs can hide essential isolation, replication, pool, and cancellation behavior; expose adapter-specific guarantees honestly.

## Failure Modes and Misconceptions

- **“It connected, so it is authorized.”** login authenticates a role; grants and policies determine allowed actions.
- **“TLS is enabled, so the server is trusted.”** encryption without chain and hostname/service verification can protect a connection to the wrong peer.
- **“NetworkPolicy protects the data.”** it constrains reachability, not SQL operations, database objects, or rows.
- **“A short TTL kills compromised access.”** expiry blocks later use according to the authority, but established sessions may remain.
- **“Rotation succeeded because the broker issued new credentials.”** applications may still cache old material or retain old sessions.
- **“The proxy solves connection limits.”** it redistributes and queues demand; database, proxy, client socket, and file-descriptor limits remain.
- **“Default pool size is per service.”** it often multiplies across replicas, processes, users, databases, regions, and deployment generations.
- **“Transaction pooling is transparent.”** session state, advisory locks, temporary objects, `LISTEN`, cursors, and prepared statements may change or fail.
- **“Retry the failed statement.”** transaction decisions and prior writes require replaying a safe whole unit.
- **“Serialization retry makes external effects exactly once.”** messages or HTTP calls can duplicate unless coordinated or idempotent.
- **“A multi-host driver transparently migrates sessions.”** it selects a host for a connection; existing sockets and transactions remain tied to that server.
- **“A reachable replica is fresh.”** health and freshness are different observations.
- **“Row-level security guarantees tenant isolation.”** policy, role bypass, ownership, functions, context, and pooling can undermine it.
- **“Runtime and migration privileges can be combined for convenience.”** that makes every application compromise a schema-control compromise.
- **“Query telemetry is harmless after hashing parameters.”** hashes may remain identifying and high-cardinality; parameters should be excluded by default.
- **“Removing the catalog object retires access.”** credentials, grants, sessions, routes, exports, replicas, and backups may persist.

## Worked Examples

### Example 1

Three services share one superuser password in a Kubernetes Secret. An incident cannot identify the caller or revoke one service. Separate workload-derived roles with named grants and leased credentials isolate admission and audit. Conclusion: shared administrator credentials destroy least privilege and attribution.

### Example 2

A client uses TLS encryption but disables hostname verification to survive a certificate mismatch. Traffic is encrypted to an unintended proxy. Correct trust distribution and exact server-name verification fail the connection safely. Conclusion: encryption is not server identity.

### Example 3

Twenty application replicas each default to a 20-connection pool during a rolling surge, exceeding a 300-session safe budget. A five-connection allocation, surge-aware admission, proxy sizing, and reserved emergency capacity prevent collapse. Conclusion: pools multiply across deployment topology.

### Example 4

A transaction pooler is introduced under a client that sets `search_path` once per session. Later transactions run on different server connections and reach the wrong schema. Transaction-local setup or session pooling restores semantics. Conclusion: pool mode is an application contract.

### Example 5

A serialization failure occurs after reading balance and writing an outbox row. Retrying only the update duplicates or contradicts prior decisions. A whole-transaction callback with operation key and transactional outbox safely replays. Conclusion: retry boundaries follow transaction causality.

### Example 6

After creating an order, the UI reads from a healthy replica and reports “not found.” Routing the read-after-write path to primary or waiting on a commit/replay marker preserves the promise. Conclusion: availability does not imply freshness.

### Example 7

A 15-minute credential expires, but the application's pool keeps authenticated sessions for hours. Incident responders assume access ended. Explicit pool drain and database session termination close the gap. Conclusion: credential validity and session lifetime are separate.

### Example 8

A runtime role owns tables so migrations are easy. A vulnerable query path can drop or alter them. A non-login owner role and separate migration identity retain deployment capability without runtime ownership. Conclusion: object ownership is privilege.

### Example 9

Database spans include raw SQL with email and token parameters. Sanitized query summaries, excluded bind values, bounded operation attributes, restricted audit, and redaction tests prevent telemetry leakage. Conclusion: observability must preserve data boundaries.

### Example 10

A team deletes its `DataAccess` resource, but a manually granted role, proxy route, and idle session remain. Reconciliation, drain, session termination, grant removal, negative access tests, and residual-backup ownership complete retirement. Conclusion: declarative deletion needs lifecycle proof.

## Cross-Program Connections

- **Database Systems:** roles, grants, ownership, isolation, locks, replication, query planning, and schema evolution define engine semantics.
- **Distributed Systems:** discovery, leases, failover, clocks, retries, ambiguous outcomes, replication, and partial failure shape access.
- **Computer Security:** workload identity, least privilege, TLS, network segmentation, secret handling, tenant isolation, audit, and break glass govern trust.
- **Software Engineering:** domain transactions, idempotency, compatibility, client libraries, contract tests, and ownership determine correct use.
- **Data Engineering:** schemas, lineage, backfills, freshness, retention, exports, and deletion extend the access lifecycle.
- **Reliability Engineering:** budgets, overload, failover, recovery, runbooks, SLOs, and incident drills turn access into an operable capability.
- **Cloud Computing:** managed endpoints, private networking, IAM integration, regional topology, provider limits, and shared responsibility affect implementations.
- **Governance and Privacy:** purpose, approvals, classification, residency, access review, legal holds, and erasure constrain who may use data and how.

## References

1. PostgreSQL Global Development Group, “Client Authentication,” current documentation, retrieved 2026-09-02. https://www.postgresql.org/docs/current/client-authentication.html
2. PostgreSQL Global Development Group, “The pg_hba.conf File,” current documentation, retrieved 2026-09-02. https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
3. PostgreSQL Global Development Group, “Privileges,” current documentation, retrieved 2026-09-02. https://www.postgresql.org/docs/current/ddl-priv.html
4. PostgreSQL Global Development Group, “Row Security Policies,” current documentation, retrieved 2026-09-02. https://www.postgresql.org/docs/current/ddl-rowsecurity.html
5. PostgreSQL Global Development Group, “SSL Support,” current documentation, retrieved 2026-09-02. https://www.postgresql.org/docs/current/libpq-ssl.html
6. PostgreSQL Global Development Group, “Database Connection Control Functions,” current documentation, retrieved 2026-09-02. https://www.postgresql.org/docs/current/libpq-connect.html
7. PostgreSQL Global Development Group, “Transaction Isolation,” current documentation, retrieved 2026-09-02. https://www.postgresql.org/docs/current/transaction-iso.html
8. PgBouncer Project, “Features,” current documentation, retrieved 2026-09-02. https://www.pgbouncer.org/features.html
9. PgBouncer Project, “Configuration,” current documentation, retrieved 2026-09-02. https://www.pgbouncer.org/config.html
10. HashiCorp, “Database Secrets Engine,” Vault documentation, retrieved 2026-09-02. https://developer.hashicorp.com/vault/docs/secrets/databases
11. HashiCorp, “Lease, Renew, and Revoke,” Vault documentation, retrieved 2026-09-02. https://developer.hashicorp.com/vault/docs/concepts/lease
12. OpenTelemetry, “Semantic Conventions for Database Client Spans,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/semconv/database/database-spans/
13. Kubernetes, “Network Policies,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/services-networking/network-policies/

## Exercises

### Exercise 1

Define data-service access contract, logical service identity, authentication, authorization, database role, credential lease, pool mode, connection budget, transaction isolation, replica lag, and expand-contract migration. State one non-guarantee for each.

### Exercise 2

Trace an `orders-api` request from catalog admission through workload identity, role authorization, credential issuance/delivery, discovery, TLS, network policy, pool acquisition, transaction execution, replica choice, telemetry/audit, rotation, revocation, and retirement. Identify every owner and failure boundary.

### Exercise 3

A platform shares one superuser password, uses fixed hosts with unverified TLS, trusts namespace labels, gives runtime schema ownership, configures 30 connections per replica without surge accounting, inserts transaction pooling under session-state clients, retries failed statements, routes every read to replicas, logs query parameters, and assumes TTL expiry closes sessions. Diagnose at least fifteen failures and correct them.

### Exercise 4

Design data-service access for a multi-region payments platform with strict tenant isolation, write-primary semantics, nearby stale-tolerant reporting, 99.99% authorization availability, short-lived credentials, online migrations, intermittent control-plane/network failure, and regulated audit/retention. Include capacity, consistency, incident, and testing decisions.

### Exercise 5

Migrate a fleet from static direct database connections to workload-issued credentials and a transaction pooler without losing availability, attribution, transaction correctness, or rollback. Design discovery, compatibility inventory, pool budgets, credential overlap, canaries, schema/migration handling, telemetry, failover tests, rollback, and retirement evidence.

## Answers to the Exercises

### Answer 1

A data-service access contract versions identity, role, endpoint, transport, pool, semantic, evidence, and lifecycle choices but cannot prove implementations comply. Logical service identity names intended capability but does not guarantee a healthy endpoint. Authentication establishes a principal but not allowed operations. Authorization grants operations but cannot prove business intent or bug-free policy. A database role groups privileges but may inherit or own unexpected power. A credential lease bounds authority-defined validity but may not end established sessions. Pool mode defines server-connection reuse but cannot make incompatible session behavior safe. A connection budget allocates capacity but depends on topology and measured safe limits. Isolation constrains concurrent observations but does not make external effects replay-safe. Replica lag describes separation under a measurement model but may not prove user-visible freshness. Expand-contract preserves compatibility when followed, but does not eliminate locking, load, or irreversible transformation risk.

### Answer 2

The application owner requests `orders/write` with data class, consistency, transaction, and schema needs. The platform catalog validates owner, environment, authenticated workload selector, role profile, pool and lifecycle policy; database owner approves engine privileges and safe capacity. A broker maps verified identity to a leased runtime role, records issuance, and delivers material through a protected reloadable channel. Discovery resolves a writable logical endpoint; the driver verifies certificate chain/name and network controls permit only the intended path. A bounded pool acquires before deadline and resets state according to mode. The application executes a whole replay-safe transaction under declared isolation, timeouts, cancellation, and operation key. Read-after-write stays on primary or waits for verified replay; stale-tolerant reads may use replicas. Sanitized spans expose connection/pool/operation outcomes while restricted audit records issuance, grants, migration, and emergency access. Rotation proves new sessions, drains old, revokes old credentials, and terminates sessions when required. Retirement inventories consumers, stops admission, drains, revokes, removes grants/routes/roles, runs negative tests, and leaves residual data copies with retention owners. Failure boundaries include identity, policy, broker, delivery, DNS, TLS, network, proxy, pool, database, transaction, replication, telemetry, audit, and human ownership.

### Answer 3

The shared superuser destroys least privilege, attribution, selective rotation, and incident containment; issue per-workload runtime roles with named grants. Fixed hosts couple clients to topology and bypass role-aware failover; use logical discovery with explicit primary/replica semantics. Unverified TLS encrypts to an unknown peer; verify trust chain and hostname/service identity. Namespace labels are forgeable configuration, not authenticated identity; use signed workload claims and reviewed mapping. Runtime schema ownership enables alteration/drop and escalation; use a non-login owner plus separate migration role. Thirty connections multiply across replicas, processes, surge, regions, and generations; calculate aggregate safe demand with reserves and deadlines. Transaction pooling breaks session state unless setup is transaction-local and compatible; inventory features, test them, or use session pooling. Statement retry can violate transaction causality; replay the complete idempotent unit for classified errors. Replica routing violates current/read-after-write needs and ignores lag; classify reads and define fallback/wait/error. Query parameters in telemetry leak secrets and personal data; exclude them, sanitize text, and use bounded summaries. TTL expiry may block new logins while pools retain sessions; reload, drain, revoke, terminate, and verify. Additional defects include missing role-use reconciliation, credential-renewal policy, cancellation/ambiguous-commit handling, proxy/queue budgets, audit integrity, migration locks, and retirement tests.

### Answer 4

Create separate logical capabilities for payment writes/current reads and stale-tolerant regional reporting, each with owner, tenant, region, residency, and recovery guarantees. Verified regional workload identity obtains short-lived per-service roles; runtime, migration, reporting, operations, and break glass remain separate. A highly available broker path uses bounded renewable leases, jittered refresh, protected cached continuity only for an explicit window, and revocation/session-termination runbooks. Private network paths and exact TLS identity complement database grants and tenant enforcement; cross-tenant allowed/denied tests cover RLS or physical boundaries, privileged bypass, pool reset, jobs, and restores. Primary endpoints serve writes and current reads; reporting replicas expose lag evidence and fail according to policy when too stale. Pool budgets include regional replicas, rolling surge, proxy pools/clients/file descriptors, migrations, replication, monitoring, administration, failover, and emergency reserve; deadlines/cancellation and coordinated retry budgets protect overload. Online expand-contract migrations use a separate role, lease, lock/time/load limits, replica-lag guards, checkpoints, and roll-forward plan. Audit covers issuance, policy/grant change, tenant access, migrations, break glass, and revocation under regulated retention; ordinary telemetry sanitizes SQL and parameters. Exercises inject broker/region partition, renewal failure, certificate rotation, pool saturation, failover mid-transaction, ambiguous commit, replica lag, migration lock, audit impairment, forced revocation, and restore/retirement conditions, measuring user authorization outcomes and recovery.

### Answer 5

Inventory every client, driver, process/replica multiplier, session feature, transaction boundary, prepared statement, migration path, role/grant, fixed endpoint, timeout/retry, and observability consumer. Introduce logical discovery and exact TLS verification while direct static access remains a bounded rollback path. Create per-workload least-privilege roles and canary dynamic issuance; dual-valid credential overlap is short, audited, and paired with reload/reconnect evidence. Calculate transaction-pool server budgets plus client sockets, file descriptors, per-database/user pool fragmentation, surge, jobs, migrations, admin, failover, and reserve. Replay compatibility fixtures for session state, prepared statements, temporary objects, locks, `LISTEN`, cancellations, long transactions, ambiguous commit, and complete transaction retries. Migrations keep a separate direct or compatible controlled role. Progress low-risk services, then regions/tiers, comparing pool wait, session count, connection setup, transaction/status errors, retry/duplicate evidence, database load, and sanitized audit attribution. Failure tests restart proxy/database, remove primary, delay DNS, expire/revoke leases, saturate pools, and interrupt commit. Rollback drains the new path and restores the still-valid direct configuration without reversing schema. Retirement requires all clients switched, static credentials rejected, old sessions terminated, direct routes and grants removed, no old-path use through the evidence window, negative access tests passed, and residual secrets/audit/data copies assigned to governed deletion or retention.
