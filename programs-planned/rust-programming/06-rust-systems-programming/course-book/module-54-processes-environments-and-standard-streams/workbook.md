# Workbook — Module 54: Processes, Environments, and Standard Streams

[Chapter](index.md) · [Laboratory](../../labs/module-04-bounded-process-capture/README.md) · [FrameVault guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Processes, Environments, and Standard Streams** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?* Preserve your first prediction and record decisive facts in a **process boundary contract**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 53 — Paths, Names, and Platform Boundaries that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?**
3. Draw the smallest **process boundary contract** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

User text is interpolated into `sh -c`. Which boundary was lost?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

`Command::output` is used. What happens to child stdin by default?

For **Prediction 2**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

stdout is decoded with `String::from_utf8`. The child emits binary bytes. What should the API return?

For **Prediction 3**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

The parent reads stdout fully, then stderr. Why can this hang?

For **Prediction 4**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

`ExitStatus::code()` returns `None`. Did the process succeed?

For **Prediction 5**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

The child is spawned with inherited environment. Is execution reproducible?

For **Prediction 6**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

A `Child` is dropped after spawn. Has lifecycle completion been established?

For **Prediction 7**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A bare program name is captured. Does it identify one executable globally?

For **Prediction 8**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Trace executable identity, each argument value, environment inheritance, current directory, standard-stream configuration, child handle, wait operation, exit status, stdout bytes, stderr bytes, and cleanup. Distinguish data captured after exit from resources bounded during execution.

For **Processes, Environments, and Standard Streams**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- building one shell command string;
- quoting interpolated untrusted arguments;
- decoding stdout lossily before deciding the product policy;
- treating nonzero exit as process-launch failure;
- claiming `Command::output` enforces a hard peak-memory bound;
- forgetting to wait or define child cleanup;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Represent a command request without any shell syntax.

Required evidence: Use `OsString` program, ordered `Vec<OsString>` arguments, optional cwd, and explicit environment changes.

### Construction 2

Design a bounded capture error that retains stdout and stderr sizes.

Required evidence: Distinguish spawn, wait, nonzero status, and output-limit failures.

### Construction 3

Choose among `status`, `output`, and `spawn` for three protocols.

Required evidence: Justify based on stdin, output, and lifecycle needs.

### Construction 4

Explain the minimum safe cleanup after an error occurs with a live child.

Required evidence: Consider kill request, wait, and preserving the original error.

### Construction 5

Transfer the model to invoking a compiler from a build tool.

Required evidence: Address argument identity, environment, current directory, output limits, and diagnostic bytes.

### Interleaved reasoning pass

1. For **Construct commands from a program plus arguments, not an interpolated shell line**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the process boundary contract.
2. For **Control environment inheritance and current-directory policy explicitly**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the process boundary contract.
3. For **Distinguish `status`, `output`, `spawn`, `wait`, `try_wait`, and `wait_with_output`**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the process boundary contract.
4. For **Treat stdout and stderr as independent byte streams**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the process boundary contract.

5. Identify one guarantee from an earlier course that a careless implementation of **Processes, Environments, and Standard Streams** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Bounded Process Capture](../../labs/module-04-bounded-process-capture/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a request table showing program, each argument, environment mutation, and current directory separately;
- tests using a deterministic child that writes distinct binary stdout and stderr;
- cases for success, nonzero exit, signal-or-platform status, empty program, and spawn failure;
- a test that rejects captured output above the storage limit;
- a written statement that the post-capture limit is not a hostile-child memory bound.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

### Laboratory acceptance trace

Before opening the reference implementation for **Bounded Process Capture**, record:

- the public behavior that demonstrates **Construct commands from a program plus arguments, not an interpolated shell line**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

### Capstone invariant trace

For the Module 54 FrameVault increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Why are program and arguments separate values?
2. Which environment variables are inherited, cleared, or set deliberately?
3. What does an exit status prove and not prove?
4. Where would concurrent pipe draining become necessary?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Build a command request that runs the current test binary with one argument containing spaces, one empty argument, a cleared environment plus one explicit variable, and separate stdout/stderr output. Preserve bytes and optional exit code. Add a post-capture limit and label it accurately. Then sketch—not implement—the ownership and liveness state needed for a hard streaming limit that drains both pipes and terminates an overproducing child.

### Closed-book defense

In five minutes, answer “How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?” using the **process boundary contract**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside FrameVault. A list of APIs without the deciding relationship is incomplete.
