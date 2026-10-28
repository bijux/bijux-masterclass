---
module_id: DBE-007
program: Database Engineering
level: 1
module_number: 7
title: Client-Server and Embedded Architectures
status: complete
last_verified: 2026-08-30
---

# Client-Server and Embedded Architectures

## One-Page Review

### Governing question

Where should the database engine run relative to application code and durable data, and how does that boundary change latency, concurrency, isolation, security, deployment, and recovery?

### Essential definitions

An **embedded database** is linked into or loaded by the host application and executes queries in its process, often reading a local file directly. A **client-server database** runs in a separate service process and accepts requests through a protocol. A **connection** is a stateful communication/session context; a **transaction** is a database atomicity/isolation boundary, not a network request. **Round-trip latency** is request-to-response delay across the boundary. **Failure domain** is the set of components one fault can directly disrupt.

### Central model, mechanism, or theorem

Architecture moves a boundary; it does not remove database work. Embedded execution replaces protocol/network crossings with in-process calls and direct local storage access, but shares address space, lifecycle, resources, and often file-lock constraints with the host. Client-server execution adds serialization, round trips, connection management, and service operation, but centralizes coordination and can isolate engine memory/files from clients. Choose from workload and failure evidence, not database size alone.

### Critical invariants

- The process, host, storage, and trust boundaries are drawn explicitly.
- Only supported actors open a database file for writing; network filesystems are not assumed to implement correct locks.
- Connections are bounded, authenticated where applicable, and returned to a known session state.
- Transaction boundaries minimize both remote round trips and embedded lock duration.
- Backup captures a recoverable database state, not an arbitrary file copy during writes.
- Host/application crash, server crash, storage loss, and network partition are distinguished.
- Version, file/protocol format, extensions, and migration compatibility are tested.
- Selection includes p95/p99 latency, concurrency, recovery, operational staffing, and total cost.

### Common failures

Failures include equating embedded with in-memory, placing a local database file on shared network storage, opening one file from unsupported multiple writers, assuming no network means no concurrency, issuing one remote round trip per row, opening unbounded server connections, sharing session state across tenants, copying a live database file without a backup API, treating process isolation as durability, bundling untrusted extensions, replacing the production engine with a behaviorally different test engine, and choosing client-server merely because data may grow.

### Compact example

A desktop application needing offline operation, one writer, and local durable state fits an embedded engine. A multi-host service with eight concurrent writers, centralized authorization, and independent operations does not. Four sequential SQL statements cost four protocol round trips remotely unless grouped or sent through a server-side operation; embedded calls avoid those network crossings but still pay parsing, execution, locking, and storage cost.

### Connections

[DBE-006](006-database-catalogs-and-metadata.md) explains metadata scope inside each architecture. [DBE-008](../ROADMAP.md) compares workloads whose concurrency and scan patterns drive the boundary. Operating Systems, Networks, Security, Distributed Systems, and Platform Engineering supply process, transport, storage, trust, and operational models.

## Governing Question

The same SQL surface can hide very different deployment shapes. In one, application code calls a library that executes against a local file in the same process. In another, a driver serializes requests over a socket to a separately managed server that owns storage. Both can provide transactions and durable data, but the placement of coordination, faults, privileges, and data movement differs.

The question is not which category is universally superior. It is which boundary matches the data's location, writer topology, latency budget, availability need, trust model, and operating capacity. A correct answer may also combine them: a server can use an embedded database internally, a client can keep an offline local replica, or an analytical application can query local files while authoritative writes remain centralized.

## Why This Matters

Architecture determines what can fail together. A memory-safety bug or out-of-memory condition in an embedded engine can terminate the host application; a broken client ordinarily cannot overwrite server memory directly. Conversely, a server outage can disconnect every client while an offline embedded application continues locally.

The boundary changes performance. An embedded call avoids network protocol latency and may exchange data without serialization or copying. A client-server engine keeps compute near centralized data, filters high-volume pages before returning a small result, and coordinates concurrent clients without exposing storage files. Moving the file across a network to an embedded engine often sends the wrong, high-bandwidth side of the interface over the network.

Operations differ too. Embedded engines reduce service installation and connection infrastructure but distribute files, upgrades, encryption keys, backups, integrity checks, and migrations across devices. Client-server systems centralize those duties but require capacity, patching, monitoring, access control, high availability, and incident response.

## Prerequisites and Retrieval

Retrieve processes, address spaces, threads, sockets, filesystems, locks, transactions, connection pools, serialization, caching, backups, durability, authentication, encryption, and availability. Distinguish logical concurrency from simultaneous physical execution and process failure from storage loss.

No product name decides the category forever. Some engines add remote protocols or cloud services; some server applications embed a library behind their own high-level API. Analyze the actual running boundary and supported concurrency mode for the selected version.

## Learning Objectives

After this module, you should be able to:

1. draw process, protocol, storage, trust, and failure boundaries for both architectures;
2. account for connection setup, round trips, batching, serialization, and data movement;
3. compare thread/process writer concurrency and lock ownership;
4. distinguish service isolation from data durability and availability;
5. design safe connection/session lifecycle and backpressure;
6. plan backups, migrations, upgrades, extensions, and corruption response;
7. compare centralized authorization with local file/key protection;
8. evaluate offline, multi-host, edge, desktop, analytical, and service workloads;
9. design representative failure and performance experiments;
10. justify a boundary with measured requirements and explicit limitations.

## Core Exposition

An embedded engine runs as code in the application's process. Its API may expose connections and SQL, but calls remain local function calls. Persistent state is often one or more files accessible to the process; an in-memory database is simply another storage mode. “Serverless” in this older architectural sense means no intermediary database server process, not a managed cloud billing model.

A client-server engine owns database files in one or more server processes. Clients use a wire protocol over local IPC or a network. The server parses, plans, executes, coordinates transactions, and returns results. Application filesystem paths are not server paths. The service can support many languages and hosts through protocol-compatible drivers.

The important locations are: application process, engine process, application host, engine host, durable storage, and backup/replica. Embedded does not necessarily mean single-threaded, and client-server does not necessarily mean remote: a server may run on the same host over a Unix-domain socket. Label actual placement.

In-process execution minimizes boundary cost. Parameters and result vectors may pass through memory APIs, and analytical engines can scan data already resident in the host runtime. But sharing an address space shares crashes, memory pressure, CPU scheduling, extension code, and observability. A query allocating too much memory can destabilize the application unless limits exist.

Client-server execution pays connection and request costs. A simple sequence of four dependent statements can require four round trips. Transactions do not magically batch them. Prepared statements reduce parse/planning work but not necessarily trips. Use set-based SQL, multi-row operations, pipelining where semantics allow, stored procedures sparingly, or application requests that group work. Measure result serialization and transfer, not just server execution time.

Keeping the engine near the data is often bandwidth-efficient. A client asks for a predicate and receives qualifying rows rather than reading every storage page over a network mount. Placing an embedded database file on remote shared storage can combine high I/O latency with filesystem locking/cache semantics the engine was not designed to trust.

Concurrency has several layers: calls within one connection, multiple connections in one process, multiple processes on one host, and multiple hosts. Engine documentation must own the rules. SQLite allows many readers but serializes writers per database file; WAL changes reader/writer interaction but does not turn a local file into a multi-host server. DuckDB's native read-write concurrency is principally coordinated within one process and optimized for analytical work. Product evolution can add remote modes, so version pinning matters.

Client-server systems centralize a lock manager or MVCC coordination inside the service. They usually support more independent writers, but throughput remains bounded by hot rows, indexes, storage, logging, and transaction design. More connections do not imply more capacity. Each connection consumes server/client memory and state; excess concurrency increases scheduling, lock queues, and tail latency.

A connection pool amortizes setup and bounds pressure. Its size is a control variable, not a target to maximize. On checkout, validate or reset transaction state, role, search path, time zone, temporary objects, prepared statements, and session variables as needed. Never return a failed or open transaction unknowingly. Timeouts must distinguish acquiring a pool slot, connecting, waiting on locks, executing, and reading results.

Embedded connection ownership is also important. A library may require one connection per thread or disallow concurrent use of a global connection. Forking a process after opening database state can duplicate unsafe locks or handles. Package authors should avoid hidden global databases that unrelated components accidentally share.

Process isolation is not durability. A separate server can survive one client crash and protect memory/files from stray client pointers. It can still lose data through storage failure, unflushed writes, corrupted logs, operator error, or correlated host loss. An embedded engine can provide ACID durability after power loss when its filesystem contract holds. Verify crash recovery and backups for the actual stack.

Backup must coordinate with the engine. Copying a live main file can omit journals/WAL or capture mutually inconsistent pages. Use a documented online backup API, consistent snapshot, checkpoint/backup procedure, or clean shutdown. Test restore on another environment, verify integrity and application invariants, and record encryption keys plus engine/extension versions.

Client-server high availability can use replicas, failover, and centralized backups, at significant operational complexity. Embedded deployments can replicate at the application/domain layer, sync files only through supported protocols, or accept device-local availability. Blind file synchronization during writes is not replication and can create divergent histories.

Security boundaries differ. A server authenticates clients, authorizes database objects, can terminate sessions, centralizes audit logs, and keeps files inaccessible to ordinary clients. It also exposes a network service requiring TLS, patching, credential rotation, firewalling, and denial-of-service controls. Embedded access is typically as strong as host process permissions and key management; any code executing in that process may reach the engine and perhaps the file. SQL injection remains possible in both.

Extensions enlarge trust. Server extensions execute inside a privileged engine process; embedded extensions execute inside the application. Pin, authenticate, review, and restrict extension loading. A portable database file may still depend on nonportable collations, functions, pragmas, or extensions.

Deployment favors embedded simplicity for a single application artifact, offline devices, tests, local tools, and application file formats. Yet fleet-wide schema upgrades require every installed application version to handle old/new files and interrupted migration. Client-server centralizes DDL rollout and connection compatibility, but rolling server upgrades and driver/protocol support need their own matrix.

Observability in a server commonly includes connections, locks, waits, query plans, replication, buffers, and centralized logs. Embedded applications must export engine metrics through the host, attach query context, and separate engine time from application work. A frozen UI caused by a query on its main thread is an architecture failure even if database latency is acceptable in isolation.

Selection begins with requirements: data ownership/location; number of hosts/processes/threads; reader/writer concurrency; offline behavior; transaction semantics; p50/p95/p99 latency; dataset and result sizes; security; backup/recovery objectives; HA; upgrade cadence; operational staffing; and cost. Build prototypes using production-like contention, failures, filesystems, and results. A microbenchmark on one thread cannot justify a multi-host architecture.

## Definitions and Notation

Let application `A`, engine `E`, durable storage `D`, and protocol boundary `B` occupy processes and hosts.

- Embedded: `process(A)=process(E)`; usually `host(E)=host(D)` for local-file use.
- Client-server: `process(A) != process(E)` and requests cross `B`; hosts may be equal or different.
- Request latency can be decomposed as connection/queue time plus round trips, server work, result serialization/transfer, and client processing.
- `R` is the count of causally sequential protocol round trips; batching reduces `R` only when semantics permit grouping.
- Writer topology is `(hosts, processes_per_host, threads_per_process)` plus conflict distribution.
- Failure domain `F(x)` is the set directly lost or unavailable when component `x` fails, under stated recovery mechanisms.

These are cost and failure models, not universal equalities. Network latency, caches, pooling, IPC, vectorized transfer, storage, and engine implementation alter constants.

## Mechanisms, Invariants, or Proof Structure

An architecture review should:

1. draw processes, hosts, storage, replicas/backups, and trust boundaries;
2. enumerate connections, writers, transactions, lock scope, and session state;
3. trace representative reads/writes including trips, bytes, parsing, execution, and fsync;
4. inject client, host, server, disk, network, and migration failures separately;
5. verify backup and restore under supported procedures;
6. test authentication/file permissions, encryption, extensions, and tenant isolation;
7. measure distributions under production-like concurrency and data;
8. model fleet/service upgrades and backward compatibility;
9. price operations, storage, network, and engineering ownership;
10. state why alternatives fail a named requirement.

The finite model below turns a small requirements matrix into explicit eligibility decisions. It also counts causally sequential remote trips and distinguishes process-failure scope. It does not benchmark or certify either architecture.

<!-- bijux-verify: {"id":"finite-architecture-decision","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"desktop_choice=embedded\nservice_choice=client_server\nembedded_round_trips=0\nclient_server_round_trips=4\nbatched_round_trips=1\nembedded_process_failure=('application', 'database_engine')\nclient_process_failure=('one_client',)\nserver_process_failure=('database_service', 'all_sessions')\n","stderr":""}} -->
```python
architectures = {
    "embedded": {
        "offline": True,
        "multi_host_writers": False,
        "max_simultaneous_writers": 1,
    },
    "client_server": {
        "offline": False,
        "multi_host_writers": True,
        "max_simultaneous_writers": 64,
    },
}


def eligible(architecture, workload):
    if workload["offline_required"] and not architecture["offline"]:
        return False
    if workload["writer_hosts"] > 1 and not architecture["multi_host_writers"]:
        return False
    if workload["simultaneous_writers"] > architecture["max_simultaneous_writers"]:
        return False
    return True


def choose(workload):
    candidates = [name for name, values in architectures.items() if eligible(values, workload)]
    return candidates[0] if len(candidates) == 1 else "measure_candidates"


desktop = {"offline_required": True, "writer_hosts": 1, "simultaneous_writers": 1}
service = {"offline_required": False, "writer_hosts": 3, "simultaneous_writers": 8}
statements = 4

print(f"desktop_choice={choose(desktop)}")
print(f"service_choice={choose(service)}")
print("embedded_round_trips=0")
print(f"client_server_round_trips={statements}")
print("batched_round_trips=1")
print(f"embedded_process_failure={('application', 'database_engine')}")
print(f"client_process_failure={('one_client',)}")
print(f"server_process_failure={('database_service', 'all_sessions')}")
```

The selection uses deliberately hard requirements; real choices often leave multiple eligible candidates and require measurement. The embedded writer limit is a fixture policy, not a claim about every embedded engine. Failure tuples describe immediate process availability only, not durable-data loss, restart, failover, or client retry. One batched trip assumes the four statements can be grouped safely.

## Alternatives and Trade-Offs

**Embedded local file:** Minimal deployment and trips; strong offline fit. Shares process/resources and requires supported local locking, fleet backup, and migration discipline.

**Same-host database server:** Adds process isolation, central coordination, and protocol cost without a physical network hop. Useful when multiple local processes share data.

**Remote client-server:** Centralizes multi-host writers, policy, operations, and data filtering. Adds network partitions, credentials, pools, service capacity, and HA concerns.

**Application service over embedded storage:** End users call a domain API; one service process serializes or partitions file access. This is client-server at the application boundary even though its internal database is embedded.

**Local replica/cache plus server authority:** Enables offline/low-latency reads and queued writes, but introduces synchronization, conflict, version, and privacy rules. It is a distributed system, not a free blend.

**In-memory versus persistent:** Orthogonal to the process boundary. Both embedded and server engines can use memory and disk; durability depends on logging/storage configuration and failure model.

**One file per tenant versus shared server:** Files improve isolation, portability, and per-tenant backup for modest workloads; fleets multiply migrations, open files, observability, and cross-tenant queries. Shared servers centralize resources but need strong logical isolation and noisy-neighbor control.

## Failure Modes and Misconceptions

1. Equating embedded, serverless, in-memory, and single-user.
2. Equating client-server with remote or cloud-managed.
3. Putting a database file on network storage without verified locking semantics.
4. Allowing unsupported multiple processes/hosts to write one file.
5. Assuming a local file cannot have thread/process concurrency.
6. Ignoring host process crash blast radius for embedded execution.
7. Treating server process isolation as backup or durability.
8. Sending one remote statement per row instead of set-based work.
9. Measuring server execution while omitting queue/trips/transfer/client time.
10. Opening unbounded connections during load spikes.
11. Returning dirty session/transaction state to a pool.
12. Sharing a non-thread-safe global embedded connection.
13. Forking with inherited database handles or locks.
14. Copying live files instead of using a supported backup/snapshot API.
15. File-syncing independently modified databases and calling it replication.
16. Ignoring extensions, collations, file/protocol formats, and driver versions.
17. Using a different test engine and assuming SQL/transaction equivalence.
18. Treating local file permissions as sufficient against malicious host code.
19. Exposing a server without TLS, authentication, quotas, or patching.
20. Running heavy embedded queries on an application's latency-critical thread.
21. Choosing from average latency while ignoring concurrency and tails.
22. Choosing from dataset size alone.
23. Ignoring fleet-wide migrations and key recovery for embedded files.
24. Generalizing one product/version's concurrency rules to the category.

## Worked Examples

### Example 1

**Situation:** A single-user desktop editor must work offline. **Reasoning:** Data and SQL caller are on one device, one writer is expected, and zero-administration packaging matters. **Conclusion:** An embedded persistent file is a strong candidate, subject to backup and migration tests.

### Example 2

**Situation:** Three application hosts write one customer database. **Reasoning:** Directly sharing an embedded file across hosts moves storage locking over the network and violates the selected engine's supported writer topology. **Conclusion:** Use a client-server authority or a supported distributed design.

### Example 3

**Situation:** Four dependent remote statements each wait 2 ms network RTT. **Reasoning:** Network waiting alone contributes at least roughly 8 ms before server/queue/transfer time. A safe grouped operation can pay one RTT. **Conclusion:** Protocol shape is part of query design.

### Example 4

**Situation:** A mobile app process crashes during an embedded query. **Reasoning:** The engine invocation dies with the host; recovery must reopen and validate/replay durable state. A separate server would retain service state for other clients. **Conclusion:** Process boundary changes availability blast radius, not automatically durability.

### Example 5

**Situation:** A web service creates 5,000 server connections for 200 worker slots. **Reasoning:** Idle/session memory and active contention overwhelm capacity without creating useful parallelism. **Conclusion:** Bound the pool from measured server capacity and application concurrency.

### Example 6

**Situation:** A live embedded file is copied while a transaction updates pages and WAL. **Reasoning:** The copy may combine inconsistent generations or omit required journal state. **Conclusion:** Use the engine's online backup/snapshot procedure and test restore.

### Example 7

**Situation:** A desktop fleet upgrades schema, but users can skip releases. **Reasoning:** New binaries must recognize old versions and migration interruption; old binaries must reject or safely read upgraded files. **Conclusion:** Embedded simplicity moves upgrade complexity into file/version compatibility.

### Example 8

**Situation:** An analytical Python process scans local columnar files. **Reasoning:** An embedded analytical engine avoids moving data through a remote protocol and can integrate with host memory, while one process owns writes. **Conclusion:** Embedded architecture can fit large analytical data despite not being an OLTP service.

### Example 9

**Situation:** Tests use SQLite while production uses PostgreSQL. **Reasoning:** Type coercion, nulls, constraints, concurrency, isolation, SQL syntax, and query plans differ. **Conclusion:** The embedded test double is useful only for explicitly shared behavior; production-engine integration tests remain required.

### Example 10

**Situation:** One server stores a separate embedded file per tenant behind a domain API. **Reasoning:** External callers see a client-server service; internally, tenant partitioning reduces lock contention but multiplies files, migrations, backups, and cross-tenant work. **Conclusion:** Classify each boundary and evaluate both layers.

## Cross-Program Connections

- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains processes, address spaces, scheduling, filesystems, and locks.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) explains latency, transport, TLS, failure, and connection behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies trust boundaries, authorization, key management, and extension risk.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns partitions, replication, offline synchronization, and failover.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) covers deployment, service operation, observability, and fleet upgrades.
- Later DBE modules connect architecture to workloads, transactions, storage, backups, replication, and capacity.

## References

1. PostgreSQL Global Development Group, [PostgreSQL 18 Architectural Fundamentals](https://www.postgresql.org/docs/18/tutorial-arch.html), official documentation, checked 2026-08-30. Client/server roles, processes, hosts, and request placement.
2. PostgreSQL Global Development Group, [How Connections Are Established](https://www.postgresql.org/docs/18/connect-estab.html), official internals documentation, checked 2026-08-30. Process-per-connection model and protocol execution path.
3. SQLite Project, [SQLite Is Serverless](https://www.sqlite.org/serverless.html), official documentation, checked 2026-08-30. In-process direct-file architecture and process-isolation trade-off.
4. SQLite Project, [Appropriate Uses for SQLite](https://www.sqlite.org/whentouse.html), official documentation, checked 2026-08-30. Local storage, network filesystem, writer concurrency, and workload selection guidance.
5. SQLite Project, [Write-Ahead Logging](https://www.sqlite.org/wal.html), official documentation, checked 2026-08-30. Reader/writer concurrency, checkpointing, and host/filesystem constraints.
6. DuckDB Foundation, [Why DuckDB](https://duckdb.org/why_duckdb), official architecture description, checked 2026-08-30. Embedded analytical goals, host integration, portability, and resource trade-offs.
7. DuckDB Foundation, [Concurrency](https://duckdb.org/docs/current/connect/concurrency), official documentation, checked 2026-08-30. Current single-/multi-process modes, optimistic concurrency, and file-lock cautions.

## Exercises

### Exercise 1

Draw process, host, storage, and failure boundaries for a desktop embedded database and a remote client-server database. State one benefit and one risk of each boundary.

### Exercise 2

A request performs 100 row inserts as 100 remote statements. Redesign it and explain which costs change and which database work remains.

### Exercise 3

Diagnose why directly opening one SQLite file from application processes on five networked hosts is unsafe, then propose two supported architectures.

### Exercise 4

Compare embedded and client-server choices for an offline field device that syncs with headquarters, including authority, conflict, backup, security, and upgrade rules.

### Exercise 5

Design an evidence plan for migrating a same-host embedded workload to a managed client-server service without assuming the migration is beneficial.

## Answers to the Exercises

### Answer 1

Embedded: application and engine share a process; storage is usually local. Benefit: no protocol hop and simple packaging. Risk: application and engine faults/resources share a failure domain, and the host can access the file. Client-server: engine/storage sit behind a protocol in another process/possibly host. Benefit: centralized concurrency, authorization, and client isolation. Risk: network/service failure affects clients and requires service operation. Neither diagram alone proves durability; add logs, backup, replica, and key locations.

### Answer 2

Use one multi-row insert or a parameterized bulk/copy protocol inside one deliberate transaction, subject to error/atomicity needs. Remote round trips can fall from 100 toward one or a small pipeline, and parse/commit overhead may fall. The engine still validates rows, maintains indexes/constraints/logs, acquires locks, writes pages, and may fsync. Measure total rows/bytes, errors, locks, WAL, latency distributions, and retry behavior.

### Answer 3

The embedded engines in five processes depend on network filesystem locking/cache correctness and contend through file-level mechanisms; the official guidance warns that many implementations are unreliable and the writer topology is unsuitable. Architecture one: run a client-server database owning local server storage. Architecture two: place one application service beside the SQLite file and expose a high-level network API, so only that service opens/writes it. A supported replicated database is a third, more complex option; file sync is not.

### Answer 4

Use an embedded local database as an offline replica/work queue and a central server as authoritative for shared facts, or explicitly assign field-device authority for partitioned facts. Give every change stable identity/version, define conflict policy and deletion, encrypt local data and server transport, authenticate sync, bound retained operations, reconcile gaps, and support device reset. Back up/restore central state and decide whether device-local unsynced data is recoverable. Version both file schema and sync protocol; canary interrupted upgrades and old clients. This is distributed synchronization, not one database guarantee.

### Answer 5

Capture baseline p50/p95/p99 latency, throughput, CPU/memory/I/O, lock time, file size, backup/restore results, crash behavior, deployment effort, and on-call load under representative concurrency. Build a client-server prototype with equivalent schema/constraints/data, pooling, TLS/auth, network fault injection, result transfer, backups, and restore. Test SQL/type/isolation differences and migration/cutover/rollback. Compare total cost and failure objectives, not query execution alone. Migrate only if measured multi-host concurrency, isolation, operations, availability, or governance benefits exceed network/service complexity; otherwise retain embedded architecture.
