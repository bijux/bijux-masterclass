# Module 9 — Promises, Event-Loop Ordering, CLI Boundaries, and Async Files

> **Question:** Who owns eventual work, how is rejection observed, and where do process and filesystem effects belong?

## Why this comes now

Persistence APIs return promises, and a CLI process can finish, reject, receive signals, or write to streams. Async syntax can make code appear sequential while the underlying work remains eventual. The central Course 1 rule is ownership: every started promise must be awaited, returned, aggregated, or deliberately detached with an explicit observer.

This module introduces only the event-loop model needed for reliable foundational programs. Detailed phases, async hooks, streams, servers, and structured task trees belong to later courses.

## Outcomes

You can:

- explain promise fulfillment, rejection, and observation;
- distinguish starting work from awaiting it;
- predict basic ordering among synchronous code, promise reactions, and timers;
- use `Promise.all` while preserving input-order results and understanding fail-fast rejection;
- pass and observe `AbortSignal` without claiming automatic rollback;
- parse CLI arguments into a typed command;
- use promise-based file APIs behind a repository boundary;
- map library results to stdout, stderr, and `process.exitCode`.

## 1. `async` changes the return contract

```ts
async function value(): Promise<number> {
  return 3;
}
```

Even an immediate return becomes a fulfilled promise. A thrown error becomes rejection:

```ts
async function fail(): Promise<never> {
  throw new Error('failed');
}
```

Calling an async function starts its synchronous prefix and obtains a promise. The caller owns observation of settlement.

## 2. Basic event-loop ordering

```ts
console.log('A');
Promise.resolve().then(() => console.log('B'));
setTimeout(() => console.log('C'), 0);
console.log('D');
```

The trace is `A`, `D`, `B`, `C` under the ordinary model: current synchronous code completes, promise reactions run as microtasks, then the timer becomes eligible in a later turn. Do not generalize this small model into exact ordering among every Node phase or I/O source; Course 4 covers that depth.

## 3. Sequential and concurrent starts

Sequential:

```ts
const first = await loadOne();
const second = await loadTwo();
```

`loadTwo` begins after `loadOne` fulfills.

Potentially concurrent:

```ts
const firstPromise = loadOne();
const secondPromise = loadTwo();
const [first, second] = await Promise.all([firstPromise, secondPromise]);
```

Both operations are started before awaiting the aggregate. Whether they perform work in parallel depends on the underlying APIs and runtime resources. “Concurrent” means their lifetimes overlap.

`Promise.all` returns results in input order, not completion order. It rejects when an input rejects, but other started operations are not automatically cancelled.

## 4. Unhandled rejection is an ownership defect

```ts
async function save(): Promise<void> {
  throw new Error('disk full');
}

save();
```

The promise is created and discarded. The failure has no application observer. In a CLI, the top-level route should await `main()` and set a nonzero exit status on failure.

Avoid this pattern:

```ts
items.forEach(async (item) => {
  await processItem(item);
});
```

`forEach` ignores returned promises. Use a `for...of` loop for sequential ownership or `Promise.all(items.map(processItem))` for aggregate ownership.

## 5. Cancellation is cooperative

An `AbortController` emits a request:

```ts
const controller = new AbortController();
controller.abort();
```

The operation must accept the signal and define when it checks it. Work already committed may remain committed. A caller must still observe the operation’s terminal promise.

Course 1 uses signals in the Async File Index lab to demonstrate early rejection. StudyLedger’s small single-command file operations do not need a full cancellation architecture.

## 6. CLI grammar is a boundary

Node provides `parseArgs` in `node:util`, but subcommand grammar and cross-field rules remain application policy. A parser should turn:

```text
['plan', '--topic', 'Borrowing', '--minutes', '45']
```

into:

```ts
{ kind: 'plan', topic: 'Borrowing', minutes: 45 }
```

Raw strings stop at the command module. Unknown options, duplicate options, missing values, and invalid numeric text become `CommandError`.

The parser should not load storage or execute domain transitions. Parsing and execution are separate evidence boundaries.

## 7. Process ownership

`main.ts` owns:

- `process.argv`;
- environment lookup;
- standard output and error;
- signal handling when required;
- mapping error categories to exit status.

Use `process.exitCode` rather than immediate `process.exit` in ordinary failure handling so already-scheduled stream writes and cleanup can finish.

A simple shell is:

```ts
async function main(): Promise<void> {
  try {
    const command = parseCommand(process.argv.slice(2));
    const result = await runCommand(command, dependencies);
    if (result.stdout.length > 0) process.stdout.write(result.stdout);
  } catch (error: unknown) {
    process.stderr.write(`${renderError(error)}\n`);
    process.exitCode = classifyExitCode(error);
  }
}

await main();
```

## 8. File paths and promise APIs

Use `node:path` rather than manual separator concatenation. Accept path strings at the process/config boundary and pass a deliberate repository path inward.

`node:fs/promises` operations reject with system errors. Missing-file handling checks the error code narrowly:

```ts
function isMissingFile(error: unknown): error is NodeJS.ErrnoException {
  return error instanceof Error
    && 'code' in error
    && error.code === 'ENOENT';
}
```

Even this predicate is a trusted implementation boundary and should be kept small.

## 9. Async file indexing

A bounded foundational pattern is:

```ts
const names = await readdir(directory);
const paths = names.map((name) => join(directory, name));
const entries = await Promise.all(paths.map(async (path) => {
  const info = await stat(path);
  return { path, size: info.size };
}));
return entries.sort((a, b) => a.path.localeCompare(b.path));
```

This starts one `stat` per path. That may be acceptable for a small bounded directory. Course 4/5 later introduce explicit concurrency and streaming bounds. The function must state the bound or reject directories above it rather than implying unlimited scalability.

## 10. StudyLedger increment

Complete the executable path:

- parse `process.argv` into `Command`;
- load storage only for commands that need it;
- call the clock only for time-changing commands;
- run pure domain/application behavior;
- save only after a successful mutation;
- write deterministic output;
- classify errors and set exit status;
- await every started promise.

Add process tests in temporary directories. Test stdout, stderr, exit code, and resulting file together.

## Common wrong models

### “`await` makes JavaScript synchronous”

It suspends the async function and returns control to the runtime. Other work can proceed.

### “`Promise.all` cancels the others after rejection”

It rejects the aggregate; started operations continue unless their APIs implement cancellation.

### “A timeout means the operation did not happen”

It means the observer stopped waiting by a deadline. Commit state may be ambiguous.

### “The CLI parser can execute as it parses”

That couples grammar failure to effects and makes partial behavior possible.

### “Setting a type on a promise observes rejection”

Only awaiting, returning, aggregating, or deliberate handlers own settlement.

## 11. The event loop is an ownership problem

A useful first model distinguishes the current call stack, promise reactions, timers, and I/O completions. After synchronous code finishes, queued microtasks such as promise reactions run before the next timer phase in the common simple case:

```ts
console.log('sync');
Promise.resolve().then(() => console.log('promise'));
setTimeout(() => console.log('timer'), 0);
```

This prints `sync`, `promise`, `timer`. Do not generalize one trace into a complete event-loop specification. Node also has `process.nextTick`, multiple phases, native callbacks, and version/platform details. The important Course 1 skill is to identify who owns each asynchronous completion and what ordering the product actually requires.

## 12. Promise ownership

Every started promise should have one observer responsible for its terminal outcome. Common owners are:

- the current `await` expression;
- a returned promise observed by the caller;
- a `Promise.all` or related combinator;
- an explicit background-task supervisor in later courses;
- a terminal `.catch` that intentionally reports the failure.

This is suspicious:

```ts
void saveLedger(path, ledger);
return 'saved';
```

`void` silences the unused-value warning; it does not observe rejection or establish completion. StudyLedger awaits the save before reporting success.

## 13. Sequential start versus concurrent start

These programs have different resource and failure behavior:

```ts
for (const path of paths) {
  results.push(await readFile(path, 'utf8'));
}
```

```ts
const results = await Promise.all(
  paths.map((path) => readFile(path, 'utf8')),
);
```

The first starts one read at a time. The second starts all reads during `map` and gives their promises to one owner. `Promise.all` preserves result position but does not cancel already-started operations when one rejects.

Bounded concurrency belongs to later courses; the Async File Index lab begins by imposing an entry bound before starting one stat per entry.

## 14. Cancellation by signal is cooperative

An `AbortSignal` communicates a request. It does not reverse completed effects. An operation may:

- reject before starting;
- notice after one sub-operation;
- complete before the signal arrives;
- ignore the signal if the underlying API does not support it.

State these outcomes in the function contract. A timeout implemented through cancellation does not prove that a file write, network request, or remote operation did not commit.

## 15. Command parsing is syntax work

The CLI receives an array of strings. `parseArgs` helps tokenize named options and positionals, but the application still owns:

- required options;
- duplicate-option policy;
- numeric grammar;
- command-specific positionals;
- closed vocabularies;
- help text;
- exit status.

StudyLedger requests token details and rejects a repeated option rather than silently taking the last value. The typed `Command` is produced only after all syntax-level checks pass. Parsing performs no file or domain effect.

## 16. The process edge owns streams and status

Reusable modules should not call `process.exit`. Immediate exit can truncate buffered output and makes tests difficult. The entry point sets `process.exitCode` after awaited work.

The shell contract distinguishes:

```text
stdout  successful command output
stderr  diagnostics and usage errors
0       success
1       domain, validation, storage, or unexpected failure
2       command usage failure
```

A process test is the correct evidence because it observes all three streams/status facts together.

## 17. Files are asynchronous external state

`node:fs/promises` returns promises, but the filesystem remains subject to races, permissions, platform path rules, and partial external change. Missing-file policy must inspect the error code rather than catch every failure and return empty state.

For the index lab, listing followed by `stat` has a race: an entry can disappear between operations. The correct outcome is contextual failure under the declared contract, not pretending the listing was a snapshot.

For StudyLedger, read-only commands load and validate but do not write. Mutating commands load, construct a candidate, save, and then report. That sequence is the course’s first complete asynchronous application protocol.

## Practice sequence

Complete the [workbook](workbook.md), then [Async File Index](../../labs/module-09-async-file-index/README.md). Finish StudyLedger’s process route and add process-level tests.

## Ready to continue

Continue when you can list every promise started by a command, identify its observer, and state what happens if each one rejects.

Next: [Module 10 — Testing, Architecture, Integration, and Independent Change](../module-10-testing-architecture-and-change/index.md)
