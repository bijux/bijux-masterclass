# Module 32 — Promises, Async Functions, and Task Ownership

> **Question:** Who owns an asynchronous operation after it has started, and how does the program prove that every promise eventually becomes an observed outcome?

## Why this comes now

Module 31 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- explain the synchronous prefix and suspended continuation of an async function;
- distinguish a promise value from ownership of the operation that produced it;
- identify floating promises and unobserved rejections;
- choose among sequential await, eager concurrent start, all, allSettled, race, and any;
- build a task nursery that records identity and joins every accepted task;
- preserve source identity and deterministic result order independently of completion order;

## 1. An async function begins now

Calling an `async` function invokes it immediately. Its body runs synchronously until it returns, throws, or reaches an `await` whose operand is not already handled as a continuation. The call returns a promise representing the eventual completion. This means an async function can validate arguments, mutate state, allocate memory, or throw before the caller has a chance to attach broader orchestration.

Do not use “async means later” as a mental model. Divide the function into a synchronous prefix and one or more continuation segments. Each `await` establishes a scheduling boundary and a new opportunity for cancellation, interleaving, or external observation. When two async functions are called before either is awaited, both synchronous prefixes run and both operations may already be in flight.

This is the foundation for distinguishing sequential and concurrent code. `await first(); await second();` starts the second only after the first completes. `const a = first(); const b = second(); await Promise.all([a, b]);` starts both before joining them. The shape of the source determines start time, not the eventual use of `Promise.all`.

## 2. A promise is a result handle, not a lifecycle owner

A promise says that one computation will eventually fulfill or reject. It does not automatically say which component must observe the outcome, cancel the operation, retain its identity, or wait before shutdown. Those are architecture responsibilities.

A floating promise is an operation whose result is not connected to an owner. Writing `void sendTelemetry()` merely tells TypeScript that the value is intentionally ignored. It does not catch rejection, establish retry, or join the work before process exit. Fire-and-forget is only honest when the component also defines failure handling and lifetime. Often the right abstraction is a task registry or nursery that records every accepted operation and later joins them.

Unhandled rejections are process-level failure signals, not a substitute for local ownership. Attaching a global handler can improve diagnostics, but it cannot reconstruct which command, request, or batch item should receive the failure. Handle errors where semantic identity is still available.

## 3. Promise combinators encode different policies

`Promise.all` fulfills when all inputs fulfill and rejects when the first observed input rejects. It does not cancel the other operations. They may continue changing external state after the aggregate has rejected. `Promise.allSettled` waits for every input and preserves one terminal settlement per input. `Promise.race` reports the first settlement, but losing operations remain alive unless the caller cancels them. `Promise.any` reports the first fulfillment and rejects with an aggregate only when every input rejects.

Choose a combinator from the product policy. Use `all` when the aggregate result is useless after one failure but still account for continuing side effects. Use `allSettled` for complete batch reporting. Use `race` for a competition only when losers have defined cleanup. Use `any` for redundant providers only when failures from losing providers remain observable enough for operations.

Combinators operate on promises, not on abstract work. By the time a promise enters the array, its producer may already have started. Limiting concurrency therefore requires controlling when producers are invoked, not applying `Promise.all` to an already-created million-element array.

## 4. Error ownership and causal identity

An async failure should retain the identity needed to act on it. A nursery entry should know the task ID, registration order, start time if relevant, and failure cause. Replacing every rejection with `false` or `undefined` destroys the distinction among cancellation, domain failure, programmer error, and unavailable dependency.

Use typed outcomes at the orchestration boundary:

```ts
type Outcome<T> =
  | { readonly status: 'fulfilled'; readonly value: T }
  | { readonly status: 'rejected'; readonly error: unknown };
```

The rejected branch intentionally begins with `unknown`. The task boundary may preserve the original reason and render it later through a safe error-description function. Do not assume every rejection reason is an `Error`; JavaScript permits rejecting with any value. A public library may choose to normalize reasons, but normalization is a policy that should preserve `cause` or original context where possible.

## 5. Registration order, completion order, and deterministic reports

Concurrent operations complete in schedule-dependent order. A stable product often needs a different order: source order, task ID order, or dependency order. Keep identity separate from arrival.

A simple pattern stores an index beside every task and writes the terminal outcome into that slot. Event emission may occur in completion order for live observation, while the final report iterates source order. This is not cosmetic. Deterministic reports make tests reliable, diffs meaningful, retries explainable, and operational comparisons possible.

Do not sort by completion timestamp as a substitute for identity. Clocks can collide or move, and completion order is often exactly the nondeterministic dimension you should not expose as the authoritative result.

## 6. A task nursery pattern for Node.js

Node.js does not provide one built-in structured-concurrency nursery for promises. You can still build the discipline.

A nursery has an open state in which tasks may be registered, a closed state in which no new work is accepted, and a join operation that observes every registered settlement. Registration catches rejection immediately by converting it into a typed outcome, preventing a window of unhandled rejection before the later join. The nursery retains semantic identity and registration order.

```ts
class Nursery<T> {
  #open = true;
  #tasks: Array<Promise<Outcome<T>>> = [];

  spawn(run: () => Promise<T>): number {
    if (!this.#open) throw new Error('nursery is closed');
    const index = this.#tasks.length;
    this.#tasks.push(run().then(
      value => ({ status: 'fulfilled', value } as const),
      error => ({ status: 'rejected', error } as const),
    ));
    return index;
  }

  async join(): Promise<readonly Outcome<T>[]> {
    this.#open = false;
    return Promise.all(this.#tasks);
  }
}
```

A production nursery also needs duplicate identity policy, cancellation, bounded admission, and repeated-join semantics. Modules 33 and 38 add those responsibilities.

## 7. Weak repairs that hide orphaned work

Several common repairs only silence tools. Prefixing a call with `void` suppresses a no-floating-promises rule but creates no owner. Adding `.catch(console.error)` observes rejection but may still allow shutdown to cut the task off. Wrapping a rejection in `Promise.resolve` does not recover. Awaiting tasks one by one after starting them may delay observation of later failures and can still leave unclear cancellation behavior.

The principled question is: which scope promises that every accepted operation reaches one terminal state? That scope must retain the handles, define the failure policy, and join or cancel before it ends. If no such scope exists, the architecture has an orphan regardless of whether the checker is quiet.

## 8. What this changes in TaskHarbor

TaskHarbor accepts a manifest of named jobs. Each accepted job receives one index and exactly one terminal outcome. The scheduler owns all job promises; handlers never launch nested floating work. Live events may arrive in completion order, but `taskharbor run` renders terminal outcomes in manifest order.

The Module 32 capstone increment introduces a nursery for a flat set of jobs before dependencies and cancellation are added. It must prove that success, rejection, and a thrown non-Error reason are all observed, and that closing the nursery prevents late registration.

## 9. Deep case study: the request handler that returns too early

A handler accepts ten uploads, starts one promise per upload with `files.map(store)`, awaits `Promise.race`, and returns the first result. The other nine operations continue. Some still hold file descriptors; some later reject after the response has been sent; none has a component that can cancel or join them. The code has a result handle for the first settlement but no lifecycle owner for the accepted batch.

Repair begins before choosing a combinator. Decide the product policy. If all uploads must finish, own every task and await complete settlement. If the first success is enough, request cancellation of losers and still await their terminal cleanup. If one failure invalidates the batch, stop further admission, signal already-running work, and join it. `race`, `any`, and `all` report aggregate settlement; they do not supply those lifecycle actions automatically.

The crucial distinction is **settlement ownership**. A promise can be observed by several callers, but one scope must remain responsible for deciding when the operation is no longer allowed to outlive the parent. A nursery or supervisor makes that responsibility explicit.

## 10. Promise ownership ledger

For every started operation, record:

| Field | Question |
|---|---|
| source identity | which input or command caused this task? |
| start authority | which component was allowed to invoke the producer? |
| result handle | where is the promise retained? |
| cancellation authority | which controller may request stop? |
| terminal observer | which scope converts fulfillment or rejection into a typed outcome? |
| join boundary | what must await before the parent can return? |
| cleanup | what listener, timer, file, or permit remains until settlement? |

A floating promise is a missing row in this ledger, not merely a linter style issue.

## 11. Deterministic reporting over nondeterministic completion

Concurrency makes completion order variable. Product output need not be variable. Attach a stable source index before starting work, store each terminal outcome at that index, and render only after the parent joins. Live progress events may reflect actual completion; the authoritative summary can remain source ordered. Keeping those two surfaces separate prevents observers from becoming a hidden ordering authority.

## 12. Rejection is a terminal signal, not an ownership policy

A promise can reject correctly while the surrounding program still handles it incorrectly. Attaching `.catch(console.error)` observes rejection but may erase source identity, convert failure into apparent success, and let the parent return before cleanup completes. Conversely, rethrowing every rejection may be appropriate inside a task wrapper but harmful at a process-global boundary. The right handling point is the scope that owns the operation’s product meaning.

Node’s process-level unhandled-rejection behavior is a last-resort diagnostic boundary, not a task supervisor. Installing a global handler does not tell the program which request, batch, or lifecycle phase owned the promise. Course 4 components should make rejection ownership local and typed. The executable may still install a final policy for truly unowned failures, but encountering it indicates a defect or an explicitly fatal condition.

## 13. Settlement, completion, and cleanup

Promise settlement means the promise has fulfilled or rejected. Product completion may require more. A task that rejects while its `finally` block asynchronously releases a resource does not become safely joinable until that cleanup is awaited. A wrapper that races task work against a deadline must continue owning both branches until timer and listener cleanup finish. A nursery outcome should therefore represent the terminal state after the task wrapper’s cleanup contract, not merely the first visible error.

This distinction matters for resource permits. Suppose a producer acquires a semaphore permit, starts an operation, and releases in `finally`. A parent that observes rejection but does not await the wrapper may admit new work before the permit is actually released or may exit while cleanup is pending. The wrapper promise—not a nested raw operation promise—is the unit the supervisor owns.

## 14. Error identity and causal context

Do not reduce `unknown` rejection to a string at the ownership boundary. Preserve the original value or wrap it with a causal `Error` using `cause`. Add source ID, attempt, or operation metadata in the typed outcome. Rendering belongs later. This separation allows tests and higher layers to classify typed failures without parsing text while still giving the CLI a stable human-facing message.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Owned Promise Nursery](../../labs/module-32-owned-promise-nursery/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 32 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 33](../module-33-cancellation-abort-signals-deadlines-and-time-budgets/index.md)
