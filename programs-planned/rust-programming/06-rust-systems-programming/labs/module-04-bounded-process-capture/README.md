# Laboratory 54 — Bounded Process Capture

This is the independent product for **Course 6, Module 54: Processes, Environments, and Standard Streams**. Read the [module chapter](../../course-book/module-54-processes-environments-and-standard-streams/index.md) and complete its [workbook](../../course-book/module-54-processes-environments-and-standard-streams/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a structured process request and finite-output capture adapter. Program, arguments, working directory, and environment changes remain separate OS strings. Output remains bytes and nonzero status remains structured.

## Why this laboratory exists

This lab makes process invocation a structured protocol: executable identity, argument boundaries, environment policy, working directory, lifecycle, status, stdout bytes, and stderr bytes. It deliberately avoids a shell so quoting folklore cannot substitute for an argument vector. The size policy must also distinguish accepted stored output from peak memory consumed by `Command::output`.

## Contract

The capture uses `Command::output`, closes stdin, captures stdout/stderr, and rejects a combined result above a configured storage limit. It does not invoke a shell or claim to stop output growth before the child exits. The request may clear inherited environment or apply explicit overrides.

## Required milestones

1. Model program and arguments as `OsString` values.
2. Configure current directory and environment from explicit policy.
3. Capture stdout and stderr separately as bytes.
4. Represent success, numeric exit, and other termination without inventing a code.
5. Return a typed output-limit error with observed sizes.

## Adversarial cases

- empty program
- missing executable
- nonzero exit
- binary stdout
- large combined output
- non-UTF-8 program display where target permits
- environment clear versus inherit

## Evidence to produce

- a request table showing program, each argument, environment mutation, and current directory separately;
- tests using a deterministic child that writes distinct binary stdout and stderr;
- cases for success, nonzero exit, signal-or-platform status, empty program, and spawn failure;
- a test that rejects captured output above the storage limit;
- a written statement that the post-capture limit is not a hostile-child memory bound.

## Prohibited shortcuts

Do not concatenate a shell command line, pass user text to `sh -c`, merge stdout with stderr, force arbitrary stream bytes through UTF-8, treat every nonzero child exit as spawn failure, or advertise a hard memory bound while using `Command::output`. Keep host `OsString` arguments distinct from the portable representation chosen for stored captures.

## Transfer

Adapt the request model to a compiler invocation and record which ambient variables are intentionally inherited.

## Comparing with the reference

Compare the observed child request and response, not surface syntax. Verify that both implementations preserve argument order, environment semantics, raw stream bytes, and nonzero status. Then identify whether either API accidentally turns a storage-acceptance limit into a stronger resource-control claim.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

> How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
