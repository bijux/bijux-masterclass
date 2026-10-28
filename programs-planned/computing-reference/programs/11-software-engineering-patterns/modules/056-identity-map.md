---
module_id: SEPAT-056
program: Software Engineering: Patterns
level: 2
module_number: 56
title: Identity Map
status: complete
last_verified: 2026-08-28
---

# Identity Map

## One-Page Review

### Governing question

How can one persistence scope guarantee a single coherent object representation for each entity identity while handling tenant/type/composite keys, repeated materialization, partial loads, staleness, refresh, dirty state, detach/merge, memory lifetime, and concurrent transactions without pretending to be a global cache or lock?

### Essential definitions

- An **Identity Map** keeps every loaded object in a map and returns the same object whenever that persistence identity is requested again within its scope.
- **persistent identity** is the datastore-facing identity, usually mapped type plus primary-key value and any tenant/shard discriminator.
- **object identity** means two references designate the exact same in-memory instance; it differs from value equality.
- A **persistence context** is the scope that manages identities, lifecycle, snapshots, and synchronization.
- **materialization** constructs/populates objects from rows; identity resolution reconciles repeated rows with existing instances.
- A **partial load** populates only some mapped attributes or relationships; its completeness state must be explicit.
- **expiry** marks loaded attributes stale so a later access/reload must obtain current data under the active transaction.
- **refresh** replaces eligible managed state from an authoritative read, under rules for dirty data and versions.
- A **detached** object has persistent identity but is no longer managed by the original context.
- **merge** copies eligible detached state into the one managed instance for that identity; it must not create a second managed representation.

### Central model, mechanism, or theorem

Let scoped identity key be \(k=(u,t,s,p)\): persistence unit/context discriminator \(u\), mapped identity type \(t\), tenant/shard scope \(s\), and normalized primary-key tuple \(p\). Identity Map is a partial function

\[
M:K\rightharpoonup O,
\quad M(k)=o_1\land M(k)=o_2\Rightarrow o_1=o_2.
\]

For materialized row \(r\) with key \(k\), resolution returns existing \(M(k)\) and reconciles only permitted missing/expired state, or constructs/registers one object if absent. This guarantees scoped representation uniqueness. It does not guarantee freshness, cross-context identity, database isolation, optimistic conflict detection, authorization, or global singleton identity.

### Critical invariants

- Key construction includes mapped identity type, normalized composite primary key, and required tenant/shard/persistence-unit scope; no cross-tenant collision is possible.
- Each key maps to at most one managed object, and one managed object cannot silently change persistent key.
- All tracked repository/materializer paths consult/register through the same map before exposing an entity.
- Repeated join rows enrich/reuse the existing instance without duplicating entities or double-adding children.
- Loaded/unloaded/expired/dirty state is tracked per attribute/relationship where partial loading exists; absence is not confused with unloaded.
- Refresh never silently overwrites dirty intent; version and merge policy decide conflict, preserve, discard, or explicit resolution.
- Identity-map lifetime matches one bounded persistence/Unit of Work context and is not shared concurrently without a designed synchronization model.
- Close/clear/detach makes later lazy access and mutation semantics explicit; managed references do not escape accidentally.
- Bulk/native writes, triggers, other transactions, and second-level caches have an expiry/refresh/version protocol.
- Authorization and tenant filtering occur before/while loading; possessing a cached object is not continuing authority to act.

### Common failures

Common failures include keying only by numeric ID, omitting tenant/shard/type, using mutable natural keys, global maps, sharing sessions across threads/tasks, assuming identity map is a database cache, stale objects after another transaction commits, partial objects treated as complete, join rows producing duplicate collection entries, overwriting local dirty state during refresh, two detached copies merged last-write-wins, changing hash/equality after generated ID assignment, bulk SQL followed by stale flush, lazy loading after close, unbounded retention, weak-reference surprises, proxy/subclass key mismatch, soft-deleted objects remaining actionable, cached authorization, serialization of managed proxies, and believing same object instance prevents lost updates.

### Compact example

One map keys customers by tenant, mapped type, and ID. Loading T1/Customer/7 twice performs one store read and returns the same instance; T2/Customer/7 is distinct. After local T1 name mutation and external version advance, expiry plus reload reads the row but refuses to overwrite the dirty managed instance, reporting a refresh conflict.

### Connections

[SEPAT-055](055-unit-of-work.md) owns the map's lifecycle and persistence coordination; [SEPAT-057](../ROADMAP.md) introduces Data Mapper materialization. Identity Map connects to [Database Engineering](../../18-database-engineering/ROADMAP.md), [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), and [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md).

## Governing Question

What exact identity key, scope, and reconciliation protocol ensure that repeated persistence reads refer to one coherent object without turning that local coherence mechanism into a stale, insecure, unbounded, or concurrency-unsafe cache?

Identity Map solves an aliasing problem: if two objects represent the same row/entity in one business operation, independent mutations can conflict invisibly. Returning one managed instance makes in-scope object relationships and change tracking coherent.

## Why This Matters

Queries commonly repeat the same entity: an order/customer join repeats the customer per row; two repositories load the same account; a graph has cycles; a command reads a resource through separate policies. Without identity resolution, one persistence identity becomes several objects with divergent fields, collection membership, events, and versions.

The map also avoids redundant materialization and primary-key reads. Yet it intentionally reuses state. If another transaction updates the database, the existing instance may remain stale. The pattern trades duplicate representations for scoped consistency and therefore must be paired with isolation, versions, refresh rules, and short lifetimes.

ORM sessions/persistence contexts usually contain an identity map, but their precise type keys, weak-reference behavior, query population, proxy handling, expiry, merge, and concurrency rules differ. Framework documentation and integration tests are part of the contract.

## Prerequisites and Retrieval

You should understand reference identity, equality/hashing, primary/composite/natural keys, inheritance, tenant/shard routing, Unit of Work, Data Mapper, transactions/isolation, optimistic versions, lazy loading, and caches. Retrieve these facts:

1. Same primary-key value in two tables/types or tenants need not denote the same entity.
2. A mathematical map returns at most one value per key; key correctness determines the meaning of uniqueness.
3. Repeated reads under weak isolation can see different database versions even if an object map returns one older instance.
4. An optimistic version detects stale writes only when enforced in the datastore mutation.
5. Null field value differs from “attribute not loaded.”
6. A detached copy and a managed instance can represent different historical revisions of one entity.
7. Authorization can expire/change independently of object lifetime.

## Learning Objectives

After completing this module, you should be able to:

- distinguish persistent, domain, object, natural, surrogate, and reference identity;
- define collision-free identity keys for types, inheritance, composite IDs, tenants, shards, and persistence units;
- implement lookup-first materialization and repeated-row relationship assembly;
- model loaded, unloaded, expired, dirty, removed, and detached state without ambiguity;
- specify refresh and merge behavior that does not silently discard local or concurrent changes;
- pair identity resolution with Unit of Work, versions, locks, isolation, and repository boundaries;
- handle generated IDs, equality/hashing, proxies, bulk/native SQL, triggers, and second-level cache invalidation;
- bound map lifetime, memory, lazy loading, and concurrent-task ownership;
- test identity coherence, staleness, partial loads, merge conflicts, security scope, and real ORM behavior;
- recognize when immutable projections or explicit set processing should bypass identity management.

## Core Exposition

### Separate kinds of identity

Persistent identity targets stored state, usually type and primary key. Domain identity may have a different scope: an account number plus bank, a patient identifier plus assigning authority, or an order ID plus tenant. Object identity is runtime reference sameness. Value equality compares attributes.

Document mappings among them. A surrogate database key can coexist with a meaningful domain identifier; neither should silently substitute for the other in authorization, external contracts, or equality.

### Construct a complete identity key

At minimum, key by mapped identity root/type and normalized primary key. Add tenant, shard, temporal branch, soft-delete generation, or persistence-unit discriminator when the same raw key can denote different stored entities. Normalize composite components without lossy string concatenation.

For inheritance, decide whether base/proxy/subclass loads share one root identity key. Different tables with ID 7 must not collide; one polymorphic entity loaded through base and subclass should not duplicate. Follow the mapper's identity semantics.

### Keep persistent keys stable

Primary identity should not change while managed. Mutable email, username, or external label is a poor map key even when unique today. If a domain allows identity correction, model an alias/rekey workflow with reference migration rather than mutating a dictionary key invisibly.

Generated IDs create a pre-persistence interval. Track new objects separately by object/temporary identity; after insert returns the permanent key, register atomically and reject collisions. Equality/hash design must not corrupt sets when IDs appear.

### Resolve before materializing

Given a row, compute identity key first. If absent, allocate an object shell, register it before recursively materializing relationships (to break cycles), then populate validated attributes. If present, reuse it and populate only attributes allowed by completeness/expiry policy.

Registration-before-recursion prevents A→B→A from constructing a second A. If population fails, remove/quarantine the incomplete shell and fail the UoW; never expose half-materialized objects.

### Assemble join rows without duplicates

A join returns repeated parent columns. Resolve the parent once, then resolve each child and attach under relationship identity. Use a relationship membership set/key or mapper bookkeeping so repeated join multiplicity does not append the same child twice.

SQL row count and entity count differ. Pagination over joined rows can truncate entity collections; use appropriate two-stage queries or loader strategies and test cardinality.

### Track completeness explicitly

Partial projection may omit attributes for performance/security. Track loaded attribute set or use a distinct immutable projection type. Do not fill omitted values with null/default and later persist them as real changes.

When later rows contain additional fields, populate only previously unloaded attributes or explicitly expired clean fields. If two rows disagree under one snapshot, treat it as mapping/query/integrity evidence, not “last row wins.”

### Define query population semantics

Many identity maps return the existing object and do not automatically overwrite its attributes on every query. This preserves local changes and one transaction's view but surprises callers expecting a reload. Provide explicit refresh/populate-existing semantics.

State whether a primary-key `get` hits the map without SQL, whether ordinary queries still execute but resolve into mapped instances, and how locks/loader options affect existing entries.

### Distinguish freshness from identity

Same instance does not mean current database state. Under snapshot isolation, older state may be intentional; under read committed, repeated queries can see newer rows while map values stay older unless refreshed. Choose semantics based on transaction and operation.

Use short contexts, optimistic versions, explicit refresh/expiry, or locks. Do not auto-refresh everything and overwrite pending changes. Do not market Identity Map as a freshness cache.

### Expire and refresh carefully

Expiry marks specified fields/entity stale; next access or explicit reload consults the database under current transaction. Refresh applies authoritative row values to clean/expired state and updates version/snapshot. It may discard unflushed changes in some frameworks.

If dirty, default to conflict or require explicit discard/rebase policy. For a removed object or unauthorized tenant, refresh should not resurrect actionability. A missing row yields typed deleted/not-found state.

### Coordinate dirty tracking

Identity Map supplies the object registry used by Unit of Work snapshots and dirty sets. A mapper should never track two snapshots for one identity. Store original version and persistent projection alongside the entry, not as mutable object identity.

If an object changes through untracked aliases, the map cannot help. Use immutable values, instrumentation, snapshots, or explicit registration as described by Unit of Work.

### Enforce optimistic versions at write time

Map entry version is evidence of the loaded revision. Update/delete with `WHERE key=? AND version=?`, increment version, and require one row. Another context has a different object instance and can commit first; only the guarded database write detects it.

On conflict, roll back/discard or expire/reload and re-run the domain decision. Never copy the new version token onto stale state and retry blindly.

### Handle detach and merge

Closing/clearing detaches objects. Detached data crossing UI/API/message boundaries should usually become explicit DTO/command values rather than serialized ORM proxies. Lazy attributes may be unavailable and included fields can be attacker-controlled.

Merge resolves identity to the managed instance, validates source version/authority/schema, then copies only allowed intended changes. It returns/uses the managed instance; the detached source does not become a second managed representative. Two detached copies require conflict policy, not last writer wins.

### Design equality and hashing

Entity domain equality often uses stable domain identity; persistence framework identity may use mapped key. New objects without IDs complicate this. Strategies include assigned stable IDs at creation, reference equality while transient, or immutable business identity with explicit scope.

Never base hash on mutable attributes or switch hash while an object resides in a set/map. Test proxy/subclass symmetry, transitivity, tenant scope, and serialization.

### Bound lifecycle and memory

Use one map per short UoW/request/operation. Strong references retain every loaded graph; weak references can let clean unreferenced instances disappear, changing repeated-reference behavior after garbage collection depending on framework. Know the policy.

For large streams/batches, use read-only projections, chunked UoWs, clearing/expiring at safe boundaries, or stateless access. Do not load a million entities into one map simply for deduplication.

### Do not share concurrently

An identity map plus managed mutable objects is usually single-thread/task ownership. Concurrent operations can race on dictionary, population, dirty flags, lazy loads, and transaction connection. Give each concurrent task its own UoW/context.

Cross-context objects are distinct by design. Communicate IDs or immutable values, not live managed references; coordinate writes with the datastore.

### Integrate tenant and authorization scope

Tenant belongs in the key and every query predicate when storage identifiers can overlap. A cached T1 object must never satisfy a T2 lookup. Repository/mapper verifies tenant before registration and prevents cross-tenant relationships.

Identity presence is not authorization. Recheck actor-resource-action/state at each operation; permissions, ownership, consent, and classification may change while the object remains managed.

### Handle soft deletion and temporal identity

If soft deletion means the entity remains same identity but inactive, mark state and deny normal actions; do not return an old active cached representation. Expire on delete events/commands within the UoW. If identifier reuse creates a new generation, include generation or prohibit reuse.

Temporal/as-of queries may represent different versions of one logical entity simultaneously. Use immutable temporal projection keys including valid/transaction time rather than putting historical and current views under one mutable identity key.

### Synchronize bulk/native changes and triggers

Bulk/native SQL and triggers can alter rows without updating entries. Run bulk work in an empty/separate context or expire/refresh all affected identities; increment versions and generate audit/events under explicit policy. Never later flush stale objects over bulk changes.

Database-generated fields/triggers require returned values or refresh after flush. Update snapshots only after successful synchronization.

### Distinguish first- and second-level caches

Identity Map is first-level, mandatory for context coherence, and contains live mutable managed objects. A second-level/distributed cache stores serialized state across contexts and needs versioning, invalidation, tenant isolation, eviction, and consistency policy. It must materialize into each context's one instance.

Never share a live entity object across sessions via a global cache. Cache authorization-sensitive results only with correct subject/resource/policy/version scope and revocation semantics—or avoid doing so.

### Observe behavior

Record context lifetime, map size/high-water mark, hits/misses/materializations, duplicate-row resolutions, partial/expired/refresh counts, dirty-refresh conflicts, detach/merge conflicts, lazy loads, evictions/clears, version conflicts, tenant-key mismatches, and bytes where measurable. Bound labels and do not log sensitive entity values.

Unexpected hit rate can mean stale overscoped contexts; low hit rate can expose repository/context fragmentation. Metrics need interpretation, not optimization in isolation.

### Test the real mapper/context

Test repeated primary-key loads and separate queries return the same reference, while separate contexts return different references. Cover composite/type/tenant/shard keys, inheritance/proxies, joins and duplicate children, cycles, partial then full load, null versus unloaded, dirty refresh, expiry, missing/deleted rows, generated IDs, equality/hash, detach/merge, lazy after close, weak/strong retention, bulk SQL, triggers, and optimistic races.

Use the actual ORM/version/database for population and isolation semantics. Security tests attempt cross-tenant same-ID lookups and authority changes. Fault-inject materialization failure so incomplete shells never escape.

## Definitions and Notation

Let identity key domain

\[
K=U\times T\times S\times P,
\]

where \(U\) is persistence-unit/mapping discriminator, \(T\) mapped identity root, \(S\) tenant/shard/temporal scope, and \(P\) normalized primary-key tuple. Map \(M:K\rightharpoonup O\) must satisfy functionality:

\[
\forall k,o_1,o_2:\;(k,o_1)\in M\land(k,o_2)\in M\Rightarrow o_1=o_2.
\]

Each entry additionally tracks loaded attributes \(L_k\), expired attributes \(E_k\), dirty attributes \(D_k\), and revision \(v_k\), with required distinction \(L_k\subseteq A\), \(E_k,D_k\subseteq L_k\), and a policy preventing refresh of \(D_k\) without explicit resolution.

Resolution \(\rho(M,r)\) for row \(r\) with \(k=\mathrm{key}(r)\) either constructs/registers one \(o\) if \(k\notin\mathrm{dom}(M)\), or returns existing \(M(k)\) and reconciles allowed attributes. It never adds a second value for \(k\).

## Mechanisms, Invariants, or Proof Structure

### Identity Map procedure

1. Define mapped identity root, normalized composite key, tenant/shard/persistence-unit/temporal scope, and generated-ID policy.
2. Create one single-owner map per bounded Unit of Work/persistence context.
3. On lookup/materialization, compute key first, resolve existing entry, or register a shell before recursive population.
4. Track loaded/unloaded/expired/dirty/version state; deduplicate join relationships by identity.
5. Keep domain/object/value/persistence equality distinct and keys/hash stable.
6. Resolve freshness through isolation, expiry/refresh, locks, and optimistic guarded writes—not map presence.
7. Merge detached intent into the one managed instance with schema, authority, version, and field policy.
8. Synchronize/clear after bulk/native/trigger changes; separate second-level cache semantics.
9. Close/detach deterministically, prevent concurrent sharing/lazy escape, and bound memory.
10. Test actual mapper/ORM/database identity, population, staleness, conflict, security, and failure behavior.

### Executable finite model

The finite example keys by tenant, mapped type, and ID; returns one instance for repeated T1 reads; separates the same raw ID in T2; and refuses to refresh dirty T1 state after a newer row is read. It does not implement transactions, partial attributes, relationships, weak references, authorization, optimistic writes, or a real ORM.

<!-- bijux-verify: {"id":"identity-map-customers","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"same=True reads=1 name=Ada\ntenant_isolated=True t2_name=Grace size=2\ndirty_name=Augusta refreshed=False reads=3 version=3\n","stderr":""}} -->
```python
class Customer:
    def __init__(self, tenant, customer_id, name, version):
        self.tenant = tenant
        self.customer_id = customer_id
        self.name = name
        self.version = version
        self.dirty = False

    def change_name(self, name):
        self.name = name
        self.dirty = True


class CustomerMapper:
    def __init__(self, rows):
        self.rows = rows
        self.objects = {}
        self.expired = set()
        self.reads = 0
        self.last_refreshed = None

    def key(self, tenant, customer_id):
        return (tenant, "Customer", customer_id)

    def load(self, tenant, customer_id):
        identity = self.key(tenant, customer_id)
        if identity in self.objects and identity not in self.expired:
            self.last_refreshed = False
            return self.objects[identity]
        self.reads += 1
        row = self.rows[identity]
        if identity not in self.objects:
            customer = Customer(tenant, customer_id, row["name"], row["version"])
            self.objects[identity] = customer
            self.last_refreshed = True
        else:
            customer = self.objects[identity]
            if customer.dirty:
                self.last_refreshed = False
                return customer
            customer.name = row["name"]
            customer.version = row["version"]
            self.expired.discard(identity)
            self.last_refreshed = True
        return self.objects[identity]

    def expire(self, customer):
        self.expired.add(self.key(customer.tenant, customer.customer_id))


rows = {
    ("T1", "Customer", 7): {"name": "Ada", "version": 3},
    ("T2", "Customer", 7): {"name": "Grace", "version": 5},
}
mapper = CustomerMapper(rows)
first = mapper.load("T1", 7)
again = mapper.load("T1", 7)
print(f"same={first is again} reads={mapper.reads} name={first.name}")
other = mapper.load("T2", 7)
print(f"tenant_isolated={first is not other} t2_name={other.name} size={len(mapper.objects)}")
first.change_name("Augusta")
rows[("T1", "Customer", 7)] = {"name": "Ada-remote", "version": 4}
mapper.expire(first)
mapper.load("T1", 7)
print(f"dirty_name={first.name} refreshed={mapper.last_refreshed} reads={mapper.reads} version={first.version}")
```

### Finite invariant argument

**T1 first/repeat.** First load reads/registers one object at key `(T1, Customer, 7)`. Second load finds nonexpired key and returns that exact object without a read; functionality and `reads=1` hold.

**Tenant isolation.** T2 produces distinct key `(T2, Customer, 7)`, one additional read/object, so raw ID collision does not alias; map size is two.

**Dirty expiry.** Local mutation marks T1 dirty. After the backing row advances, expiry forces a third read, but refresh detects dirty intent and returns the existing object without overwriting name/version. Thus one representation remains and local intent is preserved, while the stale version 3 exposes the need for explicit conflict resolution.

This finite argument assumes serial calls, immutable identity fields, valid complete rows, and no materialization exception. Refusing refresh is not conflict resolution and does not make a later write safe; production must compare version 3 with database 4 in a guarded update or reload/rebase deliberately.

### Evidence classification

Execution is empirical evidence for three lookups plus one expired lookup. Key distinctness, read counts, reference identity, and dirty-refresh behavior can be recomputed. It proves no database isolation, mapping fidelity, authorization, concurrency, memory, or cross-context property.

## Alternatives and Trade-Offs

| Approach | Identity behavior | Best fit | Main risk |
|---|---|---|---|
| No map/data records | New value per row/query | Read-only transformations | Duplicate mutable entity representations |
| First-level Identity Map | One live object per scoped key | Unit of Work/domain graph | Staleness and memory if overscoped |
| Global object map | One live object process-wide | Rare single-owner simulations | Concurrency, staleness, leaks, tenant/security |
| Second-level cache | Serialized state across contexts | Repeated reads with policy | Invalidation/version/privacy complexity |
| Immutable projections | Purpose-built values | Queries/reporting/large streams | No tracked entity behavior |
| Event-sourced aggregate cache | Aggregate by stream/version | Event-sourced command handling | Replay/invalidation/concurrency complexity |

Identity Map belongs on tracked entity materialization paths. Read-only SQL projections, analytics, bulk pipelines, and value objects usually do not need managed reference identity.

## Failure Modes and Misconceptions

- **“Primary key alone is enough.”** Type, tenant, shard, persistence unit, and temporal/generation scope may be required.
- **“Identity Map is a global cache.”** It is a short-lived coherence mechanism for one context.
- **“Same instance means fresh.”** Reuse can intentionally retain older state.
- **“Same instance prevents concurrent updates.”** Other contexts/processes have other instances; datastore concurrency control is required.
- **“Natural keys never change.”** Model corrections/aliases explicitly or use stable surrogate/domain identity.
- **“Null means not loaded.”** Attribute completeness needs separate metadata or projection types.
- **“Every query refreshes objects.”** Many ORMs preserve existing managed attributes unless explicitly refreshed/expired.
- **“Refresh is harmless.”** It can erase local changes; dirty/version policy is required.
- **“Merge attaches the detached object.”** Common semantics copy into/return a managed representative; callers must use it.
- **“Last detached copy wins.”** Different revisions require conflict detection and domain resolution.
- **“Entity equality can switch after insert.”** Changing hash while stored corrupts hash collections.
- **“Join row equals entity.”** Repeated rows must resolve one entity and deduplicate relationships.
- **“Clear solves bulk updates automatically.”** It detaches objects; escaped references remain stale and untracked.
- **“Possessing an object proves authorization.”** Authority is re-evaluated per action/context.
- **“A passing fake proves ORM identity behavior.”** Proxy, population, weak references, merge, and isolation need real integration evidence.

## Worked Examples

### Example 1

**Situation.** Tables `Customer` and `Order` each have row ID 42 and map uses numeric ID only.

**Reasoning.** Second load collides and returns wrong type. Include mapped identity root/type in key; validate materializer type. In inheritance, use the framework's shared root identity for one polymorphic entity.

**Conclusion.** Key space must distinguish unrelated types while unifying polymorphic representations intentionally.

### Example 2

**Situation.** Tenants T1 and T2 both have account ID 9.

**Reasoning.** A global `(Account,9)` key leaks T1 object into T2 request. Key/query by tenant and enforce tenant context server-side; separate contexts and database defenses add protection.

**Conclusion.** Tenant is an identity and security dimension, not merely a filter.

### Example 3

**Situation.** A parent-child join returns parent P in 20 rows and child C twice through another join.

**Reasoning.** Resolve P once and each child by key; relationship membership keyed by child identity prevents duplicates. Do not paginate raw joined rows as if they were parents.

**Conclusion.** Identity resolution must cover graph assembly and join cardinality.

### Example 4

**Situation.** A summary query loads ID/name only; later code interprets missing `credit_limit` as zero and saves.

**Reasoning.** Null/default was used for unloaded. Track loaded attributes and lazy/full-load before access, or return a distinct immutable `CustomerSummary` that is never writable.

**Conclusion.** Partial entity state must not masquerade as complete persistent state.

### Example 5

**Situation.** Another transaction commits a new name, but a repeated query returns the old managed name.

**Reasoning.** Identity resolution reused the existing instance; freshness depends on transaction/isolation/population rules. Explicitly refresh/expire clean state, or retain snapshot semantics. A version guards later mutation.

**Conclusion.** Reuse and freshness are orthogonal policies.

### Example 6

**Situation.** Local code edits address, then refresh loads newer database row and silently erases it.

**Reasoning.** Dirty attribute overlaps refreshed state. Reject/require explicit discard, or compare base/local/remote for a domain-approved merge. Never overwrite by generic “database wins” default without contract.

**Conclusion.** Dirty refresh is a three-way conflict, not ordinary cache replacement.

### Example 7

**Situation.** Two browser tabs submit detached customer objects from versions 4 and 5.

**Reasoning.** Map resolves one managed instance, but merge must validate expected version and allowlisted command fields. Version 4 is stale after 5 commits; last submission cannot overwrite blindly.

**Conclusion.** Identity Map selects the target instance; optimistic/domain policy resolves detached revisions.

### Example 8

**Situation.** An object enters a hash set before its generated ID; equality/hash changes after insert.

**Reasoning.** The set bucket no longer matches the hash. Assign stable ID at creation, use reference identity while transient and never mix states in hashed collections, or define immutable scoped business identity.

**Conclusion.** Generated identity and language equality contracts require deliberate design.

### Example 9

**Situation.** A bulk SQL update closes accounts, then stale managed instances flush `status=open`.

**Reasoning.** Bulk path bypassed map/snapshots. Isolate bulk work or expire/refresh affected keys and increment versions; guarded flush should conflict rather than reopen.

**Conclusion.** Alternate writers require synchronization and version protocol.

### Example 10

**Situation.** A cached clinical record remains in a long context after consent is revoked and a correction is posted.

**Reasoning.** Object presence proves neither freshness nor continuing authority. Use short context, reauthorize action, load/lock expected current revision, represent correction history, and deny stale/withdrawn access; obtain named clinical/privacy/security review.

**Conclusion.** High-stakes identity coherence must be bounded by temporal, authorization, and evidence semantics.

## Cross-Program Connections

- [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md) develops object identity, equality, aliasing, inheritance, and lifecycle.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) develops keys, transactions, isolation, locks, constraints, and cache interactions.
- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) distinguishes entity/value/domain identity and bounded contexts.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies tenant isolation, action authorization, disclosure, and cache security.
- [SEPAT-055](055-unit-of-work.md) owns the map's scope and snapshots; [SEPAT-057](../ROADMAP.md) uses it during row-object mapping.

## References

1. Martin Fowler, [“Identity Map”](https://martinfowler.com/eaaCatalog/identityMap.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
2. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. Identity Map, Unit of Work, Data Mapper, Lazy Load, and related patterns.
3. Jakarta Persistence Team, [*Jakarta Persistence 3.2 Specification*](https://jakarta.ee/specifications/persistence/3.2/jakarta-persistence-spec-3.2.html), April 2024. Persistence-context identity and entity lifecycle semantics.
4. SQLAlchemy Project, [“Session Basics”](https://docs.sqlalchemy.org/en/21/orm/session_basics.html), SQLAlchemy 2.1 documentation, accessed 2026-08-28. Concrete identity-map lookup/population/expiry behavior.
5. Hibernate ORM, [*Hibernate ORM User Guide*](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html), accessed 2026-08-28. Persistence contexts, entity copies, merge, dirty checking, and optimistic locking.
6. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Entity identity, aggregates, repositories, and bounded contexts.
7. Barbara Liskov and Jeannette M. Wing, [“A Behavioral Notion of Subtyping”](https://doi.org/10.1145/197320.197383), *ACM TOPLAS* 16(6), 1994. Behavioral substitutability relevant to proxy/subclass identity behavior.
8. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992.
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Transactions, caches, versions, and distributed-state limitations.
10. OWASP Foundation, [“Authorization Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-28. Action authorization and server-side enforcement.

## Exercises

### Exercise 1

Trace the executable map if T1 is loaded, expired while clean after the backing row changes to name `Ada-remote` version 4, then loaded twice. Give object identity, reads, name/version, and refresh flags.

### Exercise 2

Design an identity-key schema for a SaaS system with tenant-local composite `(region, account_number)` keys, polymorphic `PersonalAccount`/`BusinessAccount`, two shards, soft deletion with prohibited key reuse, and historical as-of projections.

### Exercise 3

Specify a materialization algorithm for orders/lines/products from a joined result. Cover shells/cycles, repeated rows, relationship deduplication/order, partial attributes, contradictions, failures, and pagination.

### Exercise 4

Two detached copies edit disjoint-looking fields from version 10 while a bulk update changes status/version. Design the merge/conflict protocol, Unit of Work behavior, security checks, and evidence. Explain why field-level auto-merge may still be wrong.

### Exercise 5

Review identity handling for a high-stakes longitudinal patient system with multiple assigning authorities, merged/split records, corrections, consent changes, temporal views, and concurrent clinicians. Separate what Identity Map guarantees from required domain, security, database, and human review.

## Answers to the Exercises

### Answer 1

First T1 load creates object O from Ada/version 3 and reads=1. Expiry while clean plus backing change makes the next load read again, update the same O to `Ada-remote`/4, clear expiry, and set `last_refreshed=True`; reads=2. The following load returns the exact same O without reading, keeps name/version, and sets `last_refreshed=False`; reads remains 2. Identity is stable while population/freshness state changes.

### Answer 2

Use managed current-entity key `(persistence_unit, AccountRoot, tenant_id, shard_id, region, normalized_account_number)`. Both subclasses resolve under `AccountRoot` so base/subclass queries cannot create duplicates; runtime type is validated/upgraded only under mapper rules. Shard routing is derived server-side and included because equal tenant/local keys on different shards must not alias during migration/dual reads. Tenant is mandatory in lookup/query and authorization.

Soft deletion retains the same identity with inactive state/version; prohibited key reuse avoids generation ambiguity. If reuse were allowed, include immutable generation ID. Historical views are immutable projections keyed by current logical identity plus as-of valid/transaction time or revision, stored separately from the current mutable entity map. Composite parts are typed/normalized tuples, never concatenated strings. Tests cover all collision pairs, subclass/base loads, shard migration, deletion, and temporal/current coexistence.

### Answer 3

For each row, compute order key first. Resolve or allocate/register an order shell before relationships; populate only unloaded clean fields and verify repeated scalar columns agree. Resolve line by `(OrderRoot/order scope, line_id)` and product by its own type/tenant/key. Attach a line once using relationship identity while preserving declared line-position order; attach shared product reference without duplicating product objects. Registration-before-recursion handles cycles.

Track loaded attributes separately from null. A partial row cannot mark omitted fields loaded; a later full row may fill them. Contradictory repeated values under one expected snapshot cause mapping/integrity failure, not last-row wins. On construction/population exception, invalidate/discard the entire UoW so shells do not escape. Raw joined-row pagination is unsafe for complete parent collections; first page order IDs deterministically, then load the graph for those keys or use a verified loader strategy. Tests cover duplicate joins, empty children, cycles, partial/full order, null, contradictions, and page boundaries.

### Answer 4

Receive explicit commands/patches, not arbitrary detached entities. Authenticate and authorize actor-resource-action/tenant at execution; bind each to entity ID, base version 10, and allowlisted intended fields. Start a fresh UoW, load the one managed current instance and version. Because bulk update advanced status/version, both submissions conflict before copying. Re-evaluate domain preconditions and current authority against the new status.

If policy permits, perform a three-way comparison of base, submitted intent, and current state. “Disjoint columns” may still interact through invariants (address affects tax/eligibility; status forbids edits), derived fields, audit, or authorization, so merge is domain-specific. Apply an approved transition to managed instance, guarded by current version; persist audit/idempotency/outbox and commit. On zero rows, discard and repeat conflict handling. Evidence includes version-race integration tests, bulk-update expiry/version behavior, property/domain scenarios, authorization matrix, same/different patches, and no silent lost update.

### Answer 5

Identity key must include assigning authority plus patient identifier—or preferably an immutable enterprise record/entity ID with governed links to source identifiers—along with tenant/jurisdiction and persistence context. Identity Map guarantees only one managed representation per such key within one context. It does not decide whether two source records are one person, whether a merge/split is clinically correct, which historical fact is valid, whether consent authorizes access, or whether another transaction changed data.

Model merge/split as versioned, auditable domain workflows preserving provenance, aliases, correction lineage, effective/recorded time, and reversible adjudication; never mutate keys or erase history. Temporal views use immutable revision/as-of keys separate from current entity. Each clinical operation uses a short context, rechecks patient/clinician/action/purpose/consent, loads expected revision, and performs guarded writes; concurrent conflicts trigger clinical re-evaluation. Cache/identity entries expire on correction/consent events but event delivery alone is not the security boundary.

Test key collisions across authorities/tenants, merge/split histories, temporal/current coexistence, duplicate loads, stale versions, consent revocation, cross-patient access, partial records, rollback, and concurrent edits. Named health-information-management/identity experts, clinicians, patient safety, privacy/legal/regulatory, security, human-factors, database, and operations reviewers approve matching/merge rules and workflows. Identity Map tests cannot validate patient linkage or clinical truth.
