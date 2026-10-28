# Module 9 Workbook

## A. Ordering prediction

Predict the trace:

```ts
console.log('start');
setTimeout(() => console.log('timer'), 0);
queueMicrotask(() => console.log('microtask'));
Promise.resolve().then(() => console.log('promise'));
console.log('end');
```

State which parts are guaranteed by the basic model and which deeper ordering questions are deferred.

## B. Promise ownership audit

Find every unobserved promise:

```ts
async function run(paths: string[]): Promise<void> {
  paths.forEach(async (path) => {
    await save(path);
  });
  notify().catch(console.error);
}
```

Repair for (a) sequential saving and (b) concurrent aggregate saving. Decide whether notification failure is part of success.

## C. CLI grammar

Specify accepted and rejected token sequences for one subcommand with required, optional, repeated, and mutually exclusive options. Then implement parsing separately from execution.

## D. Missing-file policy

Write a loader that returns an empty value only for `ENOENT`, adds path context to other failures, and treats malformed content as validation failure.

## E. Independent laboratory

Complete [Async File Index](../../labs/module-09-async-file-index/README.md). It must preserve deterministic output order and reject directories above its declared entry bound.

## F. StudyLedger transfer

Complete the CLI and async repository. Add process tests for help, successful plan, malformed command, corrupted storage, and failed mutation.

## G. Reconstruction

Explain promise settlement, microtask ordering, sequential versus overlapping start, `Promise.all`, unhandled rejection, cooperative abort, process exitCode, and narrow missing-file handling.

## H. Scheduling trace

Predict the output and ownership of synchronous logs, promise reactions, a zero-delay timer, and an asynchronous filesystem read. Do not assign a precise relative order between timer and I/O unless the setup establishes it.

Repair these two defects:

```ts
files.forEach(async file => index.push(await stat(file)));
return index;
```

```ts
void save(path, ledger);
console.log('saved');
```

The first repair must choose sequential or concurrent start explicitly. The second must make save rejection observable.

## I. CLI grammar exercise

Specify tokens for `complete <id> --minutes <n> [--note <text>]`. Decide behavior for repeated `--minutes`, unknown options, extra positionals, a note beginning with `--`, and missing values.

## J. StudyLedger checkpoint

Connect `parseArgs`, application orchestration, promise-based storage, stdout/stderr, and exit status. Add a process test for one usage failure and one complete mutation lifecycle.
