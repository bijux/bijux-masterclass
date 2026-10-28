# Workbook — Module 54: Processes, Environments, and Standard Streams

[Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze answers before compiling or reading the reference implementation. A correct result without the governing reason is incomplete.

## Part 1 — Predict

### Prediction 1

User text is interpolated into `sh -c`. Which boundary was lost?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

`Command::output` is used. What happens to child stdin by default?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

stdout is decoded with `String::from_utf8`. The child emits binary bytes. What should the API return?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

The parent reads stdout fully, then stderr. Why can this hang?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

`ExitStatus::code()` returns `None`. Did the process succeed?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

The child is spawned with inherited environment. Is execution reproducible?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

A `Child` is dropped after spawn. Has lifecycle completion been established?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A bare program name is captured. Does it identify one executable globally?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

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

## Part 4 — Independent laboratory

Build [Bounded Process Capture](../../labs/module-04-bounded-process-capture/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a request table showing program, each argument, environment mutation, and current directory separately;
- tests using a deterministic child that writes distinct binary stdout and stderr;
- cases for success, nonzero exit, signal-or-platform status, empty program, and spawn failure;
- a test that rejects captured output above the storage limit;
- a written statement that the post-capture limit is not a hostile-child memory bound.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Why are program and arguments separate values?
2. Which environment variables are inherited, cleared, or set deliberately?
3. What does an exit status prove and not prove?
4. Where would concurrent pipe draining become necessary?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Build a command request that runs the current test binary with one argument containing spaces, one empty argument, a cleared environment plus one explicit variable, and separate stdout/stderr output. Preserve bytes and optional exit code. Add a post-capture limit and label it accurately. Then sketch—not implement—the ownership and liveness state needed for a hard streaming limit that drains both pipes and terminates an overproducing child.
