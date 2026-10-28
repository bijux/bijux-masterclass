# Module 80: Integrated Async Service Architecture, Testing, and Audit

**Course 8, day 10 · Module 80 of 90**

**80/90** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [JobWire guide](../capstone.md)

## The question

> Can the complete service be explained as one coherent set of lifecycle, protocol, capacity, cancellation, failure, compatibility, and operational contracts rather than as a pile of async APIs?

## Why this comes now

A network service can have individually reasonable parts and still fail where those parts meet. A bounded codec sits behind an unbounded accept loop. A graceful connection task calls an unbounded broker. An idempotency record exists but expires before the client retry budget. A health route is correct but waits behind saturated work. A shutdown token reaches every task, yet the top-level owner drops handles without joining them.

The final module is therefore not another feature. It is integration and adversarial review. You will produce a service dossier that names every authority, state transition, bound, deadline, commit point, failure scope, shutdown phase, and compatibility claim. Then tests attack the joins between mechanisms.

This is also the point where architectural restraint matters. Not every service needs a custom future, multiplexed protocol, dynamic task graph, retry loop, HTTP API, and multiple background workers. JobWire includes them because the course must exercise the mechanisms. A production design should remove mechanisms not justified by its product contract.

## What you will be able to do

- construct a complete async service dossier;
- trace one request from accepted socket through terminal response and cleanup;
- identify the authoritative owner of protocol, broker, idempotency, metrics, and shutdown state;
- calculate end-to-end resource bounds and expose assumptions;
- audit every await point for cancellation consequences;
- verify that shutdown reaches and joins all tasks;
- separate authoritative state from advisory observations;
- design an adversarial test matrix around mechanism intersections;
- distinguish deterministic semantics from scheduler-dependent timing;
- state non-guarantees, deployment scope, and the next architectural change required for multi-process operation.

## Core model

### The service dossier has nine ledgers

A complete review contains:

1. **Future-state ledger** — suspension states, retained values, wake sources, and drop behavior.
2. **Task-tree ledger** — parent, child, cancellation source, join owner, and terminal policy.
3. **Frame ledger** — encoding, maximum, buffered states, EOF, and chunk invariance.
4. **Protocol-state ledger** — legal messages, transitions, response, commit, and error scope.
5. **Connection ledger** — socket, permits, deadlines, reader/writer ownership, and close path.
6. **Capacity ledger** — every place work or bytes can accumulate.
7. **Cancellation ledger** — every significant await, abandonability, and recovery rule.
8. **Retry/idempotency ledger** — semantic identity, fingerprint, retention, failure class, and attempt budget.
9. **Operational dossier** — health semantics, metrics, compatibility, deployment scope, and non-guarantees.

These documents should be concise enough to maintain and concrete enough to challenge code. They are not process bureaucracy. They are compressed product reasoning.

### One request trace exposes integration defects

Trace a successful JobWire submission:

```text
1. listener holds connection capacity
2. accept returns socket and peer observation
3. connection task owns socket and permit
4. bounded codec yields HELLO
5. state machine enters Ready(V1)
6. bounded codec yields SUBMIT
7. parser validates IDs, operation, and payload
8. connection waits for broker mailbox capacity within deadline
9. broker checks idempotency key and fingerprint
10. broker inserts InProgress: application commit
11. bounded scheduler starts one job
12. operation produces bounded result
13. broker stores terminal record and releases job capacity
14. reply reaches connection or survives for retry
15. connection renders and writes response within deadline
16. client receives correlated result
17. connection continues or closes
18. task, socket, and permit terminate under owner
```

Now trace every failure cut between steps. At each cut ask:

- Did the operation commit?
- Is retry safe?
- Which state owner can answer?
- Does the connection remain synchronized?
- Which resources release?
- What public error is possible?
- Which test proves the claim?

A design that cannot answer one cut is incomplete even if its happy path is correct.

### Authority prevents split-brain inside one process

For each fact, name one authority:

| Fact | Authority |
|---|---|
| connection protocol state | connection task |
| frame buffer | framed transport owned by connection task |
| accepted connection count | semaphore permits plus supervisor snapshot |
| idempotency records | broker task |
| active job scheduling | broker/job scheduler |
| terminal job result | broker record |
| readiness state | supervisor-owned/watch snapshot |
| shutdown reason and phase | top-level supervisor |

Metrics may observe authority; they do not replace it. An atomic active-job count can be advisory while the scheduler’s permits are authoritative. A health snapshot can be stale while broker state remains correct.

### Resource envelope is multidimensional

A service-level bound should include:

```text
connection permits × per-connection retained bytes
+ broker queue × request size
+ active jobs × (input + working set + result)
+ idempotency records × record/result size
+ HTTP connections × request/response limits
+ task/channel/allocator overhead
```

The result is a conservative model, not exact heap accounting. State exclusions such as kernel buffers, runtime internals, allocator fragmentation, and OS socket structures.

Also bound counts that do not reduce to bytes:

- tasks;
- timers;
- file descriptors;
- DNS attempts;
- retry attempts;
- waiters per idempotency key;
- shutdown grace duration.

A bound without overload behavior is incomplete. State what the peer observes when each maximum is reached.

### Determinism is semantic, not schedule replication

JobWire should guarantee:

- canonical frame and message encoding;
- one semantic result per idempotency key/fingerprint;
- stable public error codes;
- deterministic stats field order;
- exact terminal task accounting;
- tests independent of scheduling and chunking.

It does not guarantee:

- which connection is accepted first;
- which job completes first;
- exact wake/poll counts;
- exact retry timing under real jitter;
- identical thread assignment;
- zero delay at capacity.

Do not attempt to freeze scheduler behavior to make the product “deterministic.” Project nondeterministic execution into deterministic semantic outcomes.

### Test the intersections

Unit tests prove local functions. Service defects live at intersections:

| Intersection | Adversarial test |
|---|---|
| framing × EOF | truncated payload at connection close |
| protocol × state | `SUBMIT` before `HELLO` |
| capacity × deadline | broker slot becomes available after deadline |
| commit × disconnect | close after broker insertion before response |
| idempotency × conflict | same key with changed payload |
| shutdown × admission | connection attempt during drain |
| shutdown × blocking | active blocking job exceeds grace |
| HTTP × saturation | health remains responsive while job queue full |
| slow writer × capacity | active job permit releases before response drains |
| retry × eviction | retry window compared with record retention |

Use fault-injection points with names, not arbitrary sleeps. A test-only gate such as `AfterCommitBeforeReply` makes the causal schedule explicit.

### Service errors form a hierarchy

A useful hierarchy distinguishes:

```text
configuration/startup
listener/accept
connection transport
frame/protocol
request validation
admission/overload
application/domain
retry/deadline
shutdown/join
invariant/panic
```

The top-level policy decides process exit. Connection-local errors do not stop the service. Broker authority failure may. Panics are contained and reported, but repeated invariant failure may transition readiness to failed and trigger shutdown.

Public protocol codes remain stable even when internal error types become richer.

### Compatibility has several surfaces

JobWire has:

- binary frame representation;
- text protocol grammar;
- protocol version negotiation;
- public error codes;
- HTTP route/status/body format;
- CLI syntax and exit behavior;
- idempotency scope and retention semantics;
- configuration fields and defaults.

Changing an internal task type is not a compatibility event. Changing how long an idempotency key is honored may be. Record compatibility by observable surface, not source-file location.

### Multi-process deployment changes authority

JobWire’s broker and idempotency records are in one process. Adding replicas behind a load balancer breaks process-local idempotency unless identical keys reach one authority or records move to shared durable storage. Health also needs instance versus fleet semantics. Connection counts become per instance. Graceful shutdown interacts with load-balancer draining.

The course capstone states its single-process scope instead of implying distributed guarantees. Recognizing the next broken assumption is part of architectural maturity.

### Audit async-specific code smells

Review for:

- `tokio::spawn` without retained ownership;
- unbounded channels or task-per-request waiting;
- synchronous blocking on runtime workers;
- locks or guards held across `.await` without a deliberate invariant;
- `select!` branches whose cancellation behavior is unknown;
- fresh timeouts at every stage instead of one deadline;
- socket reads treated as messages;
- `collect()` on unbounded bodies;
- retries with new idempotency keys;
- shutdown that signals but does not join;
- health routes blocked behind work queues;
- debug-formatted public responses;
- tests using sleeps as the only schedule control.

Each smell is a question, not an automatic lint. The code may be justified, but the justification should name the contract.

### The final defense is product-centered

A good architecture defense does not enumerate libraries. It says:

- one connection task owns protocol state and framed I/O;
- one broker owns semantic commits and idempotency;
- finite capacities are enforced before commitment;
- timeouts derive from one request deadline;
- duplicate attempts converge on one record;
- HTTP health reads an operational snapshot;
- shutdown stops admission, drains, aborts, and joins;
- tests control chunking, time, commit position, saturation, and task termination;
- process-local limitations are explicit.

Libraries are evidence that mechanisms exist. The design is the relationship among them.

## Use the idea in a complete program

A service dossier can be represented as data and validated in tests. This small type forces every configured limit to be nonzero and estimates retained payload bytes without pretending to count runtime overhead.

```rust
#[derive(Debug, Clone, Copy)]
pub struct Limits {
    pub connections: usize,
    pub frame_bytes: usize,
    pub broker_queue: usize,
    pub active_jobs: usize,
    pub result_bytes: usize,
    pub idempotency_records: usize,
    pub http_connections: usize,
}

#[derive(Debug, PartialEq, Eq)]
pub enum LimitError {
    Zero(&'static str),
    Overflow,
}

impl Limits {
    pub fn validate(self) -> Result<Self, LimitError> {
        for (name, value) in [
            ("connections", self.connections),
            ("frame_bytes", self.frame_bytes),
            ("broker_queue", self.broker_queue),
            ("active_jobs", self.active_jobs),
            ("result_bytes", self.result_bytes),
            ("idempotency_records", self.idempotency_records),
            ("http_connections", self.http_connections),
        ] {
            if value == 0 {
                return Err(LimitError::Zero(name));
            }
        }
        Ok(self)
    }

    pub fn retained_payload_upper_bound(self) -> Result<usize, LimitError> {
        let connection = self.connections
            .checked_mul(self.frame_bytes)
            .ok_or(LimitError::Overflow)?;
        let queued = self.broker_queue
            .checked_mul(self.frame_bytes)
            .ok_or(LimitError::Overflow)?;
        let active = self.active_jobs
            .checked_mul(self.frame_bytes.checked_add(self.result_bytes)
                .ok_or(LimitError::Overflow)?)
            .ok_or(LimitError::Overflow)?;
        let retained = self.idempotency_records
            .checked_mul(self.result_bytes)
            .ok_or(LimitError::Overflow)?;
        connection
            .checked_add(queued)
            .and_then(|value| value.checked_add(active))
            .and_then(|value| value.checked_add(retained))
            .ok_or(LimitError::Overflow)
    }
}
```

The estimate excludes protocol structs, hash-map overhead, task allocations, kernel buffers, HTTP bodies, and allocator behavior. A trustworthy report lists those exclusions next to the number.

## Practice sequence

1. Complete all nine JobWire ledgers.
2. Trace one successful request and every failure cut.
3. Calculate the resource envelope and exclusions.
4. Mark authoritative versus advisory state.
5. Build the intersection test matrix.
6. Review public compatibility surfaces.
7. Run shutdown under idle, active, saturated, and failed states.
8. Defend the single-process scope and next scaling change.

## Ready to continue

Course 8 is complete only when you can:

- reconstruct the service without starting from framework code;
- identify every task owner and join path;
- state every message and state transition;
- name every capacity and overload result;
- locate every commit and ambiguous-failure boundary;
- explain health and metrics honestly;
- demonstrate cancellation and shutdown causally;
- state what the service does not guarantee.

## Primary Rust references

- all primary references named in Modules 71–79;
- Tokio and Hyper documentation for the exact versions pinned by the course workspace;
- JobWire’s own protocol, configuration, and compatibility documents as normative product contracts.

## Continue

Complete the [workbook](workbook.md), use the [reasoned solutions](solutions.md) only after freezing your own answer, build [Async Service Audit](../../labs/module-10-async-service-audit/README.md), finish the [JobWire capstone](../capstone.md), and complete the [final review](../final-review.md). Course 9 continues with profiling, benchmarking, observability, security, packaging, CI, and production release engineering.
