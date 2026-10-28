# Laboratory 54 — Bounded Process Capture

**Course 6 · Module 54: Processes, Environments, and Standard Streams**

[Chapter](../../course-book/module-54-processes-environments-and-standard-streams/index.md) · [Workbook](../../course-book/module-54-processes-environments-and-standard-streams/workbook.md) · [FrameVault guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Processes, Environments, and Standard Streams**: How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result? The product must make **Construct commands from a program plus arguments, not an interpolated shell line** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **process boundary contract** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a structured process request and finite-output capture adapter. Program, arguments, working directory, and environment changes remain separate OS strings. Output remains bytes and nonzero status remains structured.

## Product-specific design pressure

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

For **Laboratory 54 — Bounded Process Capture**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Bounded Process Capture**.
2. Draw the smallest **process boundary contract** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to FrameVault so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Construct commands from a program plus arguments, not an interpolated shell line.
- Control environment inheritance and current-directory policy explicitly.
- Distinguish `status`, `output`, `spawn`, `wait`, `try_wait`, and `wait_with_output`.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 54 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **process boundary contract**. Defend why your design is simpler than one plausible alternative under the new requirements.
