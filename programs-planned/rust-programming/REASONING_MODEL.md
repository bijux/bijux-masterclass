# One reasoning model for all nine courses

Rust becomes easier when every mechanism is investigated with the same questions. The vocabulary becomes richer across the program, but the reasoning does not restart when the topic changes.

## 1. What exists?

Name the values, types, resources, syntax, bytes, handles, threads, tasks, queues, buffers, connections, protocol states, and external actors. Distinguish:

- a Rust value from its byte representation;
- a declaration from generated code;
- a logical path from the host object a later lookup may resolve;
- a thread from the work it currently owns;
- a future value from the task that polls it;
- a byte stream from the messages a protocol reconstructs;
- a synchronization primitive from the product condition it protects;
- a transport endpoint from an authenticated or durable identity.

A vague noun such as “state,” “data,” “worker,” or “connection” is not enough when several obligations are hidden inside it.

## 2. Who owns it, and who may act on it?

Record the unique owner or liveness roots. Then record temporary permissions: shared inspection, exclusive mutation, consumption, callback access, foreign borrowing, cross-thread transfer, shared synchronized access, task-local possession, or protocol authority.

The artifact evolves through the program:

```text
ownership ledger
    → place and loan graph
        → liveness graph
            → capability and dispatch map
                → dataflow map
                    → source-of-truth map
                        → boundary and safety ledger
                            → thread ownership and join map
                                → future state, task tree, and connection map
                                    → workload, cost, signal, threat, and release map
```

## 3. What contract is promised?

Write the invariant before the implementation.

- A function promises inputs, outputs, failure, and visible state.
- A trait adds laws across implementations.
- An iterator adds item shape, order, cardinality, and termination.
- A macro adds an accepted language and generated surface.
- An unsafe wrapper or FFI function adds obligations Rust cannot verify automatically.
- A concurrent component adds synchronization, progress, shutdown, and schedule-independence claims.
- A future adds suspension states, wake sources, output, and drop behavior.
- A network service adds framing, protocol transitions, capacity, deadlines, retries, and remote-failure semantics.

A mechanism is justified only when it makes that contract easier to state and preserve.

## 4. How does information and authority flow?

Trace type, ownership, cardinality, order, state, failure, effects, and authority from input to output. Parsers, iterator pipelines, state machines, build scripts, binary codecs, channels, brokers, and services become reviewable when every stage has an explicit input, output, and owner.

For concurrency, include publication edges:

```text
producer writes value
    → synchronization event
        → consumer observation
```

For async execution, include readiness edges:

```text
task polls future
    → future returns Pending and registers current waker
        → readiness source changes state and wakes
            → executor schedules another poll
```

For protocols, include authority transitions:

```text
bytes received
    → complete bounded frame
        → syntactically valid message
            → legal message in current protocol state
                → admitted application command
                    → terminal or committed result
```

## 5. When is the fact established?

Identify the decisive phase or event:

- source parsing;
- macro matching or procedural parsing;
- name resolution;
- type and borrow checking;
- build execution;
- runtime validation;
- lock acquisition, channel receive, or atomic synchronization;
- future poll, wakeup, task completion, or join;
- complete frame decode or protocol transition;
- application admission or commit;
- operating-system action;
- foreign-code or remote-peer behavior.

A later phase cannot retroactively prove an earlier assumption. A successful compile does not validate a file format. A successful TCP write does not prove remote application commit. A timeout does not prove no effect occurred. A healthy listener does not prove the broker can accept work.

## 6. What can fail, block, suspend, or remain live?

Follow ordinary and exceptional paths.

- What happens after partial mutation or partial I/O?
- Which guard or owner performs rollback or cleanup?
- Which operation can block or suspend?
- What predicate or readiness event permits progress?
- Who triggers wakeup during shutdown?
- Can panic, disconnect, cancellation, deadline expiry, or foreign failure strand a resource or task?
- Is every spawned thread or task joined, drained, aborted, or deliberately detached?
- If a future is dropped here, which local and external effects remain?

Failure atomicity, cancellation safety, and liveness are product properties, not consequences of choosing a fashionable primitive or runtime.

## 7. What order is promised?

Name all relevant orders:

- source and input order;
- iteration and reduction order;
- completion and join order;
- message send, arrival, and protocol order;
- byte order and frame order;
- macro expansion and generated declaration order;
- filesystem visibility and durability order;
- atomic modification order;
- retry-attempt and idempotency-record order;
- final rendering order.

Do not preserve an order accidentally. Either define it, normalize it, or state that it is unspecified.

## 8. What bounds the work?

Make every possible accumulation point visible:

- input size and item count;
- allocation and retained history;
- threads and tasks;
- channel and broker queues;
- active permits;
- receive and send buffers;
- frame and body size;
- connections and in-flight requests;
- idempotency records and duplicate waiters;
- retry attempts, backoff, and total deadline.

A bounded component inside an unbounded pipeline does not make the product bounded.

## 9. What evidence supports the claim?

Choose evidence that matches the contract:

- compiler prediction for type-system behavior;
- unit and integration tests for observable behavior;
- compile-fail cases for rejected APIs;
- law tests for substitutability and reduction;
- golden and adversarial data for formats;
- state-transition tests for failure atomicity;
- controlled byte chunking for frame decoders;
- paused or injected time for deadline and retry behavior;
- scripted peers for disconnect and ambiguous-commit cases;
- explicit task joins and shutdown traces for lifecycle claims;
- target-conditioned measurements for layout or platform claims;
- a safety ledger for unsafe operations;
- a matching header and consumer for FFI;
- Loom or Miri where their models apply, without claiming more than they establish.

## The maturity path

| Course | The shared question becomes… |
|---:|---|
| 1 | What type, owner, state, and failure path does this complete ordinary program give each value? |
| 2 | Which place, lifetime, cleanup obligation, and liveness edge makes the memory design valid? |
| 3 | Which contract and variation mechanism lets several implementations remain lawful and evolvable? |
| 4 | How do data, failure, state, demand, and effects compose without hidden work? |
| 5 | Which declaration owns generated syntax, and in which phase can misuse be rejected? |
| 6 | Which external assumptions remain, and how does one safe boundary contain them? |
| 7 | Which facts remain true across every legal schedule, and what synchronizes, terminates, and normalizes the work? |
| 8 | Which future, task, frame, protocol, capacity, cancellation, and commit contracts remain true when peers and timing are only partly observable? |
| 9 | Which measured cost, resource bound, signal, security control, artifact identity, and operating policy make the product defensible under real load? |

Use this model in every workbook and design review. The goal is not to memorize ninety isolated features. The goal is to reason through unfamiliar Rust systems with one increasingly powerful method.


## 9. What is measured, and what is operated?

Course 9 adds a final distinction to every earlier proof: the difference between behavior guaranteed by the program and behavior observed for a particular artifact, workload, and environment.

For a production claim, record:

```text
semantic authority
workload and corpus
measurement boundary
toolchain, target, profile, and features
resource envelope
signal and interpretation
failure and recovery policy
artifact and configuration identity
```

A benchmark cannot prove compatibility. A profile cannot prove a capacity envelope. A dashboard cannot prove authoritative state. A security scanner cannot prove the absence of abuse paths. A successful rollout cannot prove a future rollout will be safe. Each tool supplies one kind of evidence, and the architecture must still explain how the pieces fit.

## 10. What changes after the observation?

A production change is incomplete until its operational consequence is owned. State:

- the expected benefit;
- the resource or risk that may move elsewhere;
- the regression or alert that detects failure;
- the removal or rollback trigger;
- the compatibility impact;
- the person or component responsible for the next decision.

This closes the reasoning loop from source code to operated artifact.
