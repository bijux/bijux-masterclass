---
module_id: CONPAR-034
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 34
title: Async/Await State Machines
status: complete
last_verified: 2026-08-29
---

# Async/Await State Machines

## One-Page Review

### Governing question

What state, ownership, control-flow, scheduling, and cleanup obligations does a compiler preserve when apparently sequential async code suspends and later resumes?

### Essential definitions

- An **async function** is syntax whose invocation and result follow a language-specific asynchronous protocol.
- An **await expression** either obtains an available outcome or suspends the enclosing async computation until the operand can advance.
- A **suspension point** is a boundary where control returns to a caller or executor while selected local state remains live.
- A **coroutine frame** is stored state containing a program counter, live locals, child awaiter/future state, and cleanup metadata.
- **Lowering** translates high-level async control flow into an explicit state machine or equivalent continuation representation.
- A **resumption** advances the frame from a suspended state after readiness or completion notification.
- **Spill/liveness analysis** determines which values must survive in the frame across suspension.
- **Cancellation safety** means abandoning at a permitted suspension state preserves declared invariants and cleanup obligations.
- **Affinity** constrains where a continuation may resume, such as a UI actor, event loop, or executor.
- A **suspension-safe resource** can remain held across await without deadlock, invalid borrowing, starvation, or protocol corruption.

### Central model, mechanism, or theorem

Split async control flow at every await. Ordinary instructions form transitions; each await can produce either immediate progress or a suspended state. The frame stores a state label `pc`, all locals live into a later state, the current child operation, and cleanup obligations. Resumption supplies a value or error and continues at the matching label. The transformation preserves source control flow only if every terminal path, exception edge, cancellation edge, and `finally`/defer action is represented.

### Critical invariants

Only the state matching `pc` executes. Values used after await remain valid and owned. The awaited operation registers a useful resumption before suspension becomes externally visible. State is committed before untrusted completion can reenter. Each resume is consumed at most once. Exceptions enter the correct handler; cleanup executes under the language's exit/cancellation rules. No synchronous lock or thread-affine borrow crosses suspension without proof. Scheduler affinity and context are restored explicitly. Dropping/cancelling the frame cannot imply rollback of already-published effects.

### Common failures

Code assumes await starts a new thread; treats sequential awaits as parallel; holds a mutex or database transaction across remote I/O; stores a reference into a movable frame; forgets an exception edge; runs heavy work before the first await; assumes every await actually suspends; resumes twice; loses actor/executor affinity; abandons partially written protocol state; leaks frame-retained buffers; recursively builds unbounded async chains; or believes `finally` makes remote effects transactional.

### Compact example

`profile = await load(id); decision = await check(profile); return decision` lowers to states START, WAIT_PROFILE, WAIT_POLICY, DONE. START stores `id` and begins/observes `load`. Profile resumption stores `profile` before beginning `check`. Policy resumption returns the decision and retires the frame. The frame never needs variables dead before their next suspension, but it must retain cleanup and error destinations.

### Connections

[Futures and Promises](033-futures-and-promises.md) supplies the one-result protocol; [Callbacks and Inversion of Control](032-callbacks-and-inversion-of-control.md) supplies resumption hazards. The [program roadmap](../ROADMAP.md) next examines cooperative scheduling.

## Governing Question

How can engineers derive, inspect, and test the machine hidden behind async/await so that suspension does not conceal unsafe lifetime, reentrancy, cancellation, capacity, or failure behavior?

Async/await changes control-flow representation, not the laws of concurrency.

## Why This Matters

Async/await makes nonblocking workflows readable as direct style. A network transaction can use local variables, loops, `try`/`catch`, and structured cleanup instead of manually nested callbacks. Compilers and runtimes preserve the continuation between events.

That convenience hides decisive machinery. Code before the first suspension may run synchronously or only when a lazy future is polled. An await may complete immediately. Locals can outlive the source stack. A task may resume on another worker. Cancellation can destroy the frame between two external effects. A lock held across await can block every peer that would make progress.

Languages choose different protocols. ECMAScript async functions return promises and await uses promise-resolution machinery. C# compilers use an async method builder and awaiter pattern. Rust async bodies produce poll-driven futures, with pinning relevant to stored borrows. Python native coroutines implement `__await__`-based suspension. C++ coroutines expose promise types and suspension customization. Swift async functions interact with tasks and executors. The portable insight is the segmented state machine; details require the exact language specification.

## Prerequisites and Retrieval

Retrieve:

- task and stack distinctions from [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md);
- deadlock/progress from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- reproducible schedules from [Determinism and Reproducibility](007-determinism-and-reproducibility.md);
- safe publication from [Acquire-Release Ordering](027-acquire-and-release-ordering.md);
- run-to-completion from [Event Loops and Nonblocking Execution](031-event-loops-and-nonblocking-execution.md);
- callback reentrancy from [Callbacks and Inversion of Control](032-callbacks-and-inversion-of-control.md); and
- future ownership from [Futures and Promises](033-futures-and-promises.md).

Retrieval prompt: for any local variable in an async function, ask whether it is used after the next possible suspension; if yes, identify its frame lifetime and transfer requirements.

## Learning Objectives

After completing this module, a learner can:

1. lower a small async function into states and transitions;
2. derive the frame fields using liveness across suspension;
3. distinguish invocation, initial execution, suspension, readiness, and resumption;
4. trace return, exception, cancellation, and cleanup edges;
5. explain immediate-completion reentrancy and double-resume defense;
6. detect unsafe locks, borrows, transactions, and permits across await;
7. reason about pinning, transferability, actor/executor affinity, and context;
8. analyze cancellation at each suspension state and external commit point;
9. compare sequential awaits with explicitly overlapping child work; and
10. test the lowered machine using deterministic event injection.

## Core Exposition

### Direct style becomes segmented control flow

Consider:

`a = await first(); b = transform(a); c = await second(b); return combine(a, c)`.

The compiler splits the function into segments: entry through first await, first resumption through second await, and second resumption through return. A program-counter field chooses the segment. `a` remains live across the second await, so it is stored in the frame. `b` may be consumed when `second` is formed and need not survive if no later operation uses it.

Lowering can use switch-based state machines, continuations, coroutine intrinsics, heap frames, stack promotion, or optimizations that erase states. The semantic audit does not depend on emitted layout. It asks which state and transition must exist in any behavior-preserving implementation.

### Invocation and initial execution differ by language

In ECMAScript, calling an async function starts evaluating its body and returns a promise; execution proceeds synchronously until an await or return. In Rust, calling an async function constructs a future whose body ordinarily does not advance until poll. C# execution begins synchronously and commonly returns to the caller when an incomplete await is reached.

Therefore “async function call starts later” and “async function call runs now” are both unsafe universal claims. Document the language and runtime. Heavy CPU work before the first await can block a JavaScript event loop or C# caller even though the method is marked async. A lazy future can do nothing when created and dropped.

### Await has a fast and suspended path

An await first interrogates its operand under the language's await protocol. If the operand is already complete, the machine may continue without externally visible suspension, subject to language scheduling rules. If incomplete, it records a continuation/waker, commits its next `pc`, and returns control.

The registration and state update must prevent lost wakeups and reentrant corruption. If completion can invoke a continuation inline, setting `pc` after registration is wrong: resumption can observe the old state. Robust designs arrange state before exposure or use a protocol whose registration handles the race atomically.

“Await is a yield” is imprecise. An await of ready data may not provide fairness. A deliberate scheduler yield has its own contract.

### Frame fields come from liveness

A source local belongs in the coroutine frame when some path defines it before suspension and uses it afterward. Parameters, temporaries, loop indices, exception state, child awaiters, and cleanup guards may all become fields. Values dead before suspension can remain ordinary stack temporaries or disappear.

This explains memory retention. A large buffer referenced after a distant await remains reachable even if source code looks stack-local. Narrow scopes, extract the small derived value, or explicitly release the buffer before suspension. Measure real compiler/runtime behavior before claiming exact frame size; optimization can change representation.

Frame liveness also controls transfer traits. In Rust, a non-`Send` value held across await can make the generated future non-`Send`; if dropped before await it need not. In actor systems, retained isolated state may constrain executor affinity. The right repair is often to shorten lifetime, not add an unsafe transfer assertion.

### Suspension is not thread blocking

When an async state machine suspends, it returns the worker to its scheduler. The frame persists elsewhere. A blocking call instead keeps an OS thread occupied. Async syntax cannot convert a blocking database driver, DNS lookup, mutex acquisition, CPU loop, or foreign call into nonblocking work.

Use an appropriate asynchronous API, a bounded blocking pool, or explicit parallel worker. Offloading has queue capacity, cancellation, context, and shutdown costs. Never place unbounded blocking work onto the executor that must resume other state machines.

### Sequential syntax and concurrency

Two consecutive `await` expressions ordinarily start/observe the second only after the first completes:

`x = await load_x(); y = await load_y()`.

If independent work should overlap, create/start both under an owner, then await an aggregate or join each with failure cleanup. This is safe only when eager/lazy start semantics and capacity are known. Creating a lazy Rust future does not run it; joining/polling drives both. Creating JavaScript async operations may start both immediately.

Readable direct style therefore describes dependencies, not an automatic parallelization plan.

### Exceptions are transition edges

An awaited failure is injected at the suspension expression under the language's rules. The machine must route it through the source-level `catch`, `finally`, defer, destructor, or rejection path. A failure before the first await and one after resumption may be captured differently internally but must satisfy the public async contract.

Each continuation segment can throw. The state machine must terminally reject/fail once, release owned resources, and avoid invoking later states. A `catch` that returns normally converts failure into success. Cleanup failure may replace, suppress, aggregate, or attach to the primary error depending on language; write policy explicitly when multiple failures matter.

### Cleanup spans suspended states

Source `try/finally`, `defer`, context managers, and language destructors become frame cleanup obligations. Normal return and exception have structured exit paths. Cancellation is more variable: dropping a Rust future destroys stored fields; cancelling a task in another language may inject an exception at a suspension point; abandoning an unowned promise may run no producer cleanup at all.

Do not claim `finally` rolls back external state. It can release local handles or send compensation. A partially transmitted frame, committed transaction, remote command, or published event remains unless its protocol provides reversal.

Cleanup code can itself await in some languages. That introduces more states and can fail or be cancelled. Define whether cleanup is shielded, bounded, retried, and joined during shutdown.

### Cancellation is destruction at a cut

Draw a cut at every suspension. For each cut, list frame fields, held resources, external effects, peer expectations, and restart safety. Cancellation can occur at any allowed cut, not only where business logic prefers.

An async message send might suspend after reserving capacity but before copying bytes, after copying into a local buffer, or after the peer can observe a prefix. Restart may duplicate an operation. A cancellation-safe primitive either leaves no externally ambiguous partial state or returns enough ownership/state for recovery.

Structured task scopes help by naming who requests cancellation and joins termination. They do not make every awaited operation cancellation-safe.

### Locks, borrows, and transactions across await

Holding a synchronous mutex guard across await is usually hazardous. The task suspends while retaining exclusion; the operation needed for resumption may need the same lock. On a single worker, a blocking contender can stop the executor. Even an async mutex permits suspension but may create excessive critical sections and head-of-line blocking.

Prefer `lock -> validate/copy/move -> unlock -> await -> lock -> revalidate/commit`. Revalidation is essential because shared state can change during suspension. When atomicity must span external I/O, use a protocol—version, reservation, lease, transaction with bounded lifetime—not a local lock held indefinitely.

Borrowed views must remain valid for the whole suspended lifetime. Some languages reject such code statically; others permit references whose owner can disappear. Prefer owned immutable snapshots or explicit lifetime ownership.

### Pinning and address-sensitive frames

A generated frame can contain a child awaiter that refers to another field in the same frame. Moving the frame after such internal relationships form would invalidate addresses. Rust's `Pin<&mut Self>` makes this constraint explicit for `Future::poll`; `Unpin` means the type does not rely on pinning for movement safety.

Pinning does not imply thread safety, cancellation safety, completion, or `Send`. Other languages hide frame placement in managed runtimes, but native interop and unsafe code still must respect coroutine lifetime and address rules.

### Executor and actor affinity

Await does not universally mean “resume on the same thread” or “resume anywhere.” C# can capture a synchronization context; library code may opt out under defined APIs. Swift actors isolate executor-bound state. JavaScript jobs run through an agent/event loop. Rust executors can move `Send` tasks while local tasks stay confined.

State the required executor, not an assumed thread identity. UI mutation, device drivers, thread-local state, and foreign libraries may require an explicit hop. Conversely, excessive context capture can serialize scalable library code.

### Reentrancy and immediate completion

Even though source code appears linear, an await protocol can interact with inline completion or scheduled continuation. Before exposing a continuation, move the frame to a valid suspended state. On resume, atomically claim the expected state. Duplicate or stale resumes must not execute a segment twice.

Immediate completion also affects recursion. A long chain that always continues inline can grow a native stack in some libraries; trampolining or job scheduling bounds it. Other implementations loop inside one poll. Verify rather than infer from syntax.

### Context and debugging

Traditional stack traces lose contiguous native call frames across suspension. Runtimes may reconstruct logical async stacks or attach parent task information, but optimizations and detached work can break the chain. Carry operation IDs, trace context, deadline, and task ownership through the async context mechanism appropriate to the runtime.

Do not use ambient context as the sole authorization source without a defined propagation and clearing contract. A reused worker thread's locals are not automatically the logical task's context.

Debug a stuck async task with a state ledger: current `pc`, awaited child, wake/completion owner, scheduler queue, retained resources, cancellation flag, and last transition. “Waiting in await” is not causal enough.

### Performance without mythology

Async frames can reduce blocked threads but add allocation, scheduling, indirection, context, and retained-state costs. Compilers may stack-promote, fuse, specialize, or eliminate frames; runtimes may pool objects. Exact overhead is empirical for a toolchain and workload.

Reduce suspension count only after measurement. Combining operations can reduce hops but harm fairness, cancellation granularity, or latency. CPU-bound parallelism still requires processors and scheduling; async alone supplies concurrency, not speedup.

### Testing the machine, not the syntax

Test each suspension state with a controllable child operation. Exercise immediate and deferred completion, value and error, duplicate/stale resume defense, cancellation at every cut, cleanup failure, context/affinity, and shutdown. Assert external effects and resource counts, not just returned value.

A deterministic scheduler or manually driven model makes transitions reproducible. Stress and model checking can explore races but do not replace state invariants. Compiler-generated frames need not be inspected byte-for-byte; behavior and owned state provide the durable contract.

## Definitions and Notation

Let suspension states be `S={s_0,...,s_n}` plus terminal `DONE` and `FAILED`. Frame `F=(pc,L,A,C)` contains program counter `pc`, live locals `L`, active awaiter/child `A`, and cleanup stack `C`.

At await `i`, liveness set `LiveOut(i)` contains values used on a path after suspension. A correct lowering retains every such value: `LiveOut(i) subseteq fields(F_i)`. It may retain more, at memory cost.

Transition `δ(s_i, outcome)` maps a value to the next segment, an error to a handler/failure state, and a cancellation request to a language-defined cleanup/abandon path. For a one-shot continuation token `r`, execution count must satisfy `uses(r) <= 1`.

Let `E_i` be external effects possible before suspension `i`. Dropping `F_i` destroys owned frame state but does not imply `undo(E_i)`.

## Mechanisms, Invariants, or Proof Structure

For each async function:

1. split control flow at every possible suspension;
2. enumerate entry, waiting, handling, cleanup, and terminal states;
3. compute values live across each cut;
4. identify child operation, completion owner, and wake/resume mechanism;
5. commit `pc` before exposing a possibly reentrant continuation;
6. route value, error, cancellation, and duplicate resume separately;
7. audit locks, borrows, permits, transactions, and affinity in each frame;
8. list external effects already visible at each cancellation cut;
9. prove cleanup ownership on normal, exceptional, cancellation, and shutdown paths;
10. bound blocking work, frame retention, runnable work, and resumption cost;
11. preserve trace/deadline/authority context explicitly; and
12. test fast, suspended, adversarial, and late-completion paths.

The executable model manually lowers two awaits. The driver supplies child outcomes; the frame persists request and profile state between calls.

<!-- bijux-verify: {"id":"async-state-machine-lowering","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"step1=pending:profile\nstep2=pending:policy\nstep3=ready:allow\nrequest_id=req-7\nprofile_role=operator\ntransition_count=3\nfinal_state=done\n","stderr":""}} -->
```python
class AccessMachine:
    def __init__(self, request_id):
        self.state = "start"
        self.request_id = request_id
        self.profile = None
        self.transitions = 0

    def advance(self, outcome=None):
        if self.state == "start":
            self.state = "wait_profile"
            self.transitions += 1
            return "pending:profile"
        if self.state == "wait_profile":
            self.profile = outcome
            self.state = "wait_policy"
            self.transitions += 1
            return "pending:policy"
        if self.state == "wait_policy":
            decision = "allow" if self.profile == "operator" and outcome else "deny"
            self.state = "done"
            self.transitions += 1
            return f"ready:{decision}"
        return "invalid:terminal"

machine = AccessMachine("req-7")
print(f"step1={machine.advance()}")
print(f"step2={machine.advance('operator')}")
print(f"step3={machine.advance(True)}")
print(f"request_id={machine.request_id}")
print(f"profile_role={machine.profile}")
print(f"transition_count={machine.transitions}")
print(f"final_state={machine.state}")
```

Limitations: this single-threaded model accepts only successful, correctly ordered outcomes. It stipulates manual resumption and does not model a compiler, real await protocol, exceptions, lost wakeups, duplicate resumes, concurrency, pinning, cancellation, cleanup, affinity, memory ordering, optimization, or external effects.

## Alternatives and Trade-Offs

**Synchronous direct style** is simplest when blocking is bounded and dedicated-thread capacity is acceptable.

**Callbacks** expose resumption explicitly and can fit low-level boundaries, but manually encode state, errors, and cleanup.

**Promise/future chains** make transitions and branching visible but become verbose for loops and structured exception handling.

**Async/await** restores direct syntax while retaining a state machine. It can hide frame retention and lifecycle if engineers ignore lowering.

**Generators/coroutines** support multiple yields or bidirectional control; a one-result async function has a narrower terminal protocol.

**Virtual/lightweight threads** can preserve stackful blocking style, shifting continuation storage to runtime stacks. They simplify some code but do not remove capacity, cancellation, transaction, or remote-effect questions.

**Explicit actor state machines** make mailbox transitions and affinity obvious, at more ceremony. They are preferable when each event is a durable protocol step rather than an implementation detail.

**One large async function** centralizes control flow but retains more state and mixes responsibilities. Smaller owned operations reduce frames and improve tests, though excessive fragmentation obscures the end-to-end protocol.

## Failure Modes and Misconceptions

- “Async means another thread.” It may use one event loop, many workers, or no execution until polled.
- “Every await yields fairly.” Ready operands may continue immediately.
- “Two awaits run concurrently.” Sequential source normally encodes dependency.
- “Locals remain on the caller's stack.” Live values belong to a persistent frame or equivalent continuation.
- “The compiler saves every local.” Only semantically live state is required, though implementations may retain more.
- “Finally makes cancellation transactional.” It cannot reverse arbitrary external effects.
- “An async mutex makes a long critical section good.” It prevents worker blocking, not contention or protocol coupling.
- “Resume occurs on the same OS thread.” Affinity is runtime/API-specific.
- “Dropping a future rolls back I/O.” Local destruction cannot revoke observed remote effects.
- “Pin means thread-safe.” It constrains movement, not races or transfer.
- “Awaiting blocking work makes it nonblocking.” The underlying operation decides.
- “A successful return proves cleanup succeeded.” Cleanup errors need an explicit policy.
- “Async stack traces always reconstruct causality.” Detached tasks and context loss can break them.
- “State-machine lowering proves source correctness.” It preserves behavior, including design defects.

## Worked Examples

### Example 1

An async method computes `token`, awaits a profile, and never uses `token` afterward. Liveness need not retain `token`. If logging after the await references it, it becomes a frame field and can retain its backing credential object longer. Narrow the logged representation before suspension.

### Example 2

A JavaScript async handler parses a ten-million-item array before its first await. The handler blocks its event loop despite returning a promise. Chunk or offload CPU work under bounded ownership; merely inserting `await Promise.resolve()` may keep microtasks ahead of other event-loop phases and is not a universal fairness strategy.

### Example 3

Two independent fetches are written `a=await fetchA(); b=await fetchB()`. Latencies add. Starting both first and joining overlaps them, but now the parent owns two live operations and must observe the sibling after one fails. Performance repair introduces lifecycle obligations.

### Example 4

A continuation is registered before `pc` changes from START to WAIT. The child completes inline and invokes resume, which sees START and launches the child twice. Set a reentrancy-safe state before registration or use an atomic registration protocol that resolves completion-versus-subscription races.

### Example 5

A task holds a synchronous mutex guard while awaiting a network response. Another task needs the guard to process that response. Copy the request state and unlock before I/O; after resumption, reacquire and validate a version before commit. Replacing the mutex mechanically with an async mutex retains the logical cycle.

### Example 6

A parser holds a borrowed slice across await while the producer can recycle its buffer. In a statically checked language this can fail compilation; in an unsafe/managed interop boundary it can become corruption. Copy the required bytes or transfer ownership for the complete frame lifetime.

### Example 7

A Rust future stores an inner operation borrowing its own buffer. Once polling establishes the relationship, moving the outer frame could invalidate it. Pin-aware storage and projection preserve address stability; this says nothing about whether cancellation after a partial write is safe.

### Example 8

An operation writes a request, then awaits a response. Timeout drops the local frame after the server may have committed. A retry without an idempotency key duplicates the action. Record the commit ambiguity and use deduplication/status recovery rather than treating cancellation as rollback.

### Example 9

An async cleanup closes two resources sequentially. The first close fails and the function exits, leaking the second. Cleanup must attempt both, retain a primary/aggregate error under policy, use bounded waits, and remain owned during shutdown. Syntax alone supplies no multi-resource failure policy.

### Example 10

An infusion controller awaits confirmation after commanding a pump rate. Cancellation between command transmission and acknowledgement destroys local continuation state but may leave the pump applying the new rate. Safety requires command identity, independent sensed-state verification, fail-safe control, bounded communication, and recovery defined by the device protocol. Named clinical, controls, embedded, functional-safety, cybersecurity, human-factors, and regulatory reviewers must approve evidence; this chapter cannot.

## Cross-Program Connections

- **Compilers:** lowering uses control-flow graphs, liveness, frame layout, and exception edges.
- **Programming languages:** effect systems, ownership, pinning, and actors restrict which values cross suspension.
- **Operating systems:** nonblocking readiness and completion create the events that resume frames.
- **Distributed systems:** cancellation cuts expose ambiguous remote commits and require idempotency.
- **Databases:** holding transactions across await increases lock time and failure uncertainty.
- **Security:** logical context must cross suspension without privilege leakage into reused workers.
- **Reliability:** structured scopes own frames through cancellation and cleanup.
- **Performance engineering:** frame retention, scheduler hops, blocking pools, and fairness require measurement.

## References

1. ECMA International. “ECMAScript Language Specification: Async Function Definitions.” <https://tc39.es/ecma262/multipage/ecmascript-language-functions-and-classes.html#sec-async-function-definitions>.
2. ECMA International. “ECMAScript Language Specification: Await.” <https://tc39.es/ecma262/multipage/ecmascript-language-functions-and-classes.html#await>.
3. Microsoft. “Task Asynchronous Programming Model.” <https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/task-asynchronous-programming-model>.
4. Microsoft. “C# Language Specification: Async Functions.” <https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/classes#1515-async-functions>.
5. Rust Project. “The Rust Reference: Await Expressions.” <https://doc.rust-lang.org/reference/expressions/await-expr.html>.
6. Rust Project. “Asynchronous Programming in Rust: Pinning.” <https://rust-lang.github.io/async-book/04_pinning/01_chapter.html>.
7. Python Software Foundation. “PEP 492 — Coroutines with async and await syntax.” <https://peps.python.org/pep-0492/>.
8. ISO C++ Foundation. “Working Draft, Standard for Programming Language C++: Coroutines.” <https://eel.is/c++draft/dcl.fct.def.coroutine>.
9. Swift Project. “SE-0296: Async/await.” <https://github.com/swiftlang/swift-evolution/blob/main/proposals/0296-async-await.md>.
10. Swift Project. “SE-0338: Clarify the Execution of Non-Actor-Isolated Async Functions.” <https://github.com/swiftlang/swift-evolution/blob/main/proposals/0338-clarify-execution-non-actor-async.md>.

## Exercises

### Exercise 1

Lower `x=await first(); y=x+1; z=await second(y); return x+z` into states. List frame fields at each suspension.

### Exercise 2

Why is “await always yields to other work” invalid? Give an immediate-completion defect and a robust design rule.

### Exercise 3

A task holds a synchronous lock across a remote await. Analyze the progress and consistency risks and propose a state/version protocol.

### Exercise 4

Build a cancellation ledger for an async operation that reserves an ID, sends a remote create request, and awaits acknowledgement. State restart safety at each cut.

### Exercise 5

An autonomous vehicle sends an async brake command. The task is cancelled after transmission but before acknowledgement, and software treats frame destruction as rollback. Diagnose the claim and specify required human review evidence.

## Answers to the Exercises

### Answer 1

Use START, WAIT_FIRST, WAIT_SECOND, DONE, and FAILED/cleanup states. START begins or polls `first`; WAIT_FIRST accepts `x`, computes `y`, and begins/polls `second(y)`; WAIT_SECOND accepts `z` and returns `x+z`. The first suspended frame needs its child plus control/cleanup state; `x` does not yet exist. The second needs `x` and the second child; `y` need not survive if consumed while constructing that child. Real lowering may retain extra fields.

### Answer 2

The await operand may already be ready, so execution can continue without a fairness boundary under the language protocol. Code that sets state after await registration or relies on yielding to let another task initialize can reenter or observe half-state. Commit invariants before awaiting, never use await as synchronization without a specified primitive, and use a scheduler yield whose fairness/phase contract is explicit when yielding is required.

### Answer 3

The guard excludes peers for an unbounded remote duration; a peer needed for completion can deadlock, and blocking acquisition can stall executor workers. Under the guard, copy/move an owned request snapshot and version, then unlock. Await remotely. Reacquire, compare version and lifecycle state, then commit, retry, or reject as policy dictates. Use a reservation/lease if external exclusivity is required; bound and observe it.

### Answer 4

Before reservation, cancellation is locally safe. After reserving an unpublished local ID, cleanup can release it if the allocator contract permits. After sending, the remote create may commit even without acknowledgement; dropping the frame cannot decide. Retry needs an idempotency key tied to the reserved ID or a status lookup. After correlated acknowledgement, the owner records the result and completes cleanup. Every cut lists local fields, remote visibility, cancellation action, late response owner, and recovery deadline.

### Answer 5

Destroying a local continuation removes future local execution; it cannot retract bytes or physical braking action. The protocol needs uniquely identified commands, stale/duplicate handling, actuator-state sensing, acknowledgement correlation, independent safety interlocks, bounded loss behavior, and a safe degraded state. Production evidence requires named vehicle-systems, braking/controls, embedded, functional-safety, cybersecurity, human-factors, test-track, and regulatory reviewers; requirements and hazard traceability; hardware-in-the-loop, fault-injection, timing, and environmental tests; applicable-standard assessment; and signed residual-risk acceptance. No deployment approval is claimed here.
