# Module 31 Reasoned Solutions — Scheduling, Fairness, and Blocking

## A. Partial-order reasoning

`A` and `G` are synchronous and therefore appear before any scheduled callback. `B` is next-tick work. `C` and `D` are ECMAScript microtasks, ordered by their enqueue order within this turn. The exact relation between the zero-delay timer and immediate is context dependent; a product test should not require one universal order. The defensible answer is a partial-order graph, not one memorized six-character output.

Scheduling both from an I/O callback changes which phases are next and often makes the immediate observable first, but the larger lesson remains: derive the relation from the scheduling context and documented phase contract. Do not promote one trace into a cross-context guarantee.

## B. Blocking analysis

The file read allows Node to service other work while the operating system or worker pool completes it. After resumption, parsing and sorting are synchronous JavaScript. The event loop cannot run an eligible health timer until both regions return. Repairs include rejecting or bounding input, partitioning interruptible validation with `setImmediate` yields, using a streaming parser in Course 5, or moving CPU work to a worker in Course 8. Each repair changes a different boundary; no single `await` makes arbitrary CPU work asynchronous.

`await Promise.resolve()` schedules the continuation as another microtask. A self-replenishing microtask chain can continue ahead of timers and I/O, so it does not establish the required fairness boundary.

## C. Atomic transition

The invalid state is `status === 'running'` with no `startedAt`. Compute the timestamp and publish both fields synchronously, then perform the audit write. If auditing fails afterward, the system must report “state transition committed; observation failed,” not roll the state back unless rollback is an explicit safe transaction. Alternatively, write the audit before publication, but then the audit must describe an intended transition that may still fail. The architecture must choose one authority and one failure meaning.

## D. Cooperative construction

A principled implementation validates `chunkSize`, pushes results synchronously inside each bounded chunk, checks the signal at chunk boundaries, and awaits a promise backed by `setImmediate` between chunks. The evidence should use a trace such as `['mapping-started', 'other-immediate', 'mapping-finished']`, not a fragile duration threshold. Cancellation latency is at most one chunk plus one mapping call, which belongs in the public design record.

## E. Laboratory and capstone

The observatory should separate guaranteed relations from recorded observations. Its capped microtask loop demonstrates that repeatedly replenishing a priority queue delays ordinary phases; it does not define exactly how many callbacks every Node release will run before another phase. In TaskHarbor, a trace listener may be absent or fail without changing terminal task state. Source indices, not event arrival, determine the final report.

## F. Transfer defense

For the million-string search, source ordering can be preserved by appending matches in traversal order. Abort is checked between chunks. A `setImmediate` yield gives ordinary phases a chance to run. When each item is expensive, chunking no longer changes total CPU consumption and may still violate latency goals; worker threads become the appropriate later-course mechanism. The key is to state the limit rather than claim cooperative scheduling is parallelism.

## G. Portability and budget solutions

The complete-order test combines several unrelated assumptions. The language claim can require synchronous labels before promise continuations. A Node claim can verify that a timer never fires before its requested threshold or that recursive next-tick work delays an explicitly scheduled ordinary phase. The application claim should assert its own state-before-event relation. A full trace can still be retained as observatory output, but failure to match it is not automatically a product defect.

Using worst-case cost, 20 ms divided by 40 µs gives a maximum of roughly 500 records per chunk. That also satisfies the ordinary budget because 500 × 3 µs is about 1.5 ms. The calculation is only a model: allocation, garbage collection, and nonlinear records can change it. An adaptive loop can stop a chunk when monotonic elapsed time reaches its slice, while preserving source order by continuing from the next index. Cancellation is checked at each adaptive boundary. Tests should control the yield hook and output sequence rather than assert exact wall-clock duration.

The evidence set is strong only when every artifact has a claim. A trace without a stated guarantee is a demonstration. A budget without an adversarial workload is optimism. A passing result-order test under only one completion schedule is incomplete evidence.
