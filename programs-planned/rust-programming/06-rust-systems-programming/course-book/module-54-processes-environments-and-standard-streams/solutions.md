# Reasoned solutions — Module 54: Processes, Environments, and Standard Streams

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

## Prediction analysis

### Prediction 1

**Problem.** User text is interpolated into `sh -c`. Which boundary was lost?

**Reasoned answer.** Argument data became shell syntax with expansion and command-language semantics.

### Prediction 2

**Problem.** `Command::output` is used. What happens to child stdin by default?

**Reasoned answer.** It is closed rather than inherited, while stdout and stderr are captured.

### Prediction 3

**Problem.** stdout is decoded with `String::from_utf8`. The child emits binary bytes. What should the API return?

**Reasoned answer.** Keep bytes or return an explicit decoding error only when text is part of the child contract.

### Prediction 4

**Problem.** The parent reads stdout fully, then stderr. Why can this hang?

**Reasoned answer.** The child can block on a full stderr pipe while the parent waits for stdout EOF.

### Prediction 5

**Problem.** `ExitStatus::code()` returns `None`. Did the process succeed?

**Reasoned answer.** Check `success`; `None` means no portable numeric code, often abnormal termination.

### Prediction 6

**Problem.** The child is spawned with inherited environment. Is execution reproducible?

**Reasoned answer.** Not necessarily; ambient variables can alter behavior and disclose secrets.

### Prediction 7

**Problem.** A `Child` is dropped after spawn. Has lifecycle completion been established?

**Reasoned answer.** No. Explicit wait/reaping policy is required.

### Prediction 8

**Problem.** A bare program name is captured. Does it identify one executable globally?

**Reasoned answer.** No. Resolution can depend on PATH, current directory, and platform rules.

## Construction guidance

### Command request

The representation keeps OS-native argument boundaries. Rendering a display command is separate and never reparsed.

### Bounded error

Store configured limit and observed byte counts; keep spawn/wait `io::Error` as sources and status as structured data.

### API choice

`status` suits inherited I/O, `output` suits finite no-input capture, and `spawn` is required for interactive or managed lifecycle protocols.

### Cleanup

Attempt termination only under the wrapper’s policy, then wait to reap. Cleanup errors should be attached without hiding the primary failure.

### Compiler transfer

Do not pass a composed shell line; use a fixed compiler path or explicit resolution policy and record the exact arguments used.

## Boundary-trace reference

A strong solution trace for this module must trace executable identity, each argument value, environment inheritance, current directory, standard-stream configuration, child handle, wait operation, exit status, stdout bytes, stderr bytes, and cleanup. Distinguish data captured after exit from resources bounded during execution. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- building one shell command string;
- quoting interpolated untrusted arguments;
- decoding stdout lossily before deciding the product policy;
- treating nonzero exit as process-launch failure;
- claiming `Command::output` enforces a hard peak-memory bound;
- forgetting to wait or define child cleanup;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Process-contract proof table

| Fact | Representation or operation | What it does not prove |
|---|---|---|
| executable request | one `OsString` program plus ordered `OsString` arguments | that a bare program name resolves to the same binary on every host |
| environment policy | clear/inherit/set decisions stored explicitly | that the invoked program ignores other machine state |
| lifecycle completion | successful wait or `output` completion | that the child’s domain work succeeded |
| child result | `ExitStatus` plus stdout/stderr bytes | that a numeric exit code exists on every termination path |
| stored-output limit | check after capture | a hard peak-memory bound while a hostile child is running |

A shell string collapses executable identity and argument boundaries into a second language. Quoting is then part of the product’s security contract and differs by shell. Direct `Command` construction avoids that grammar entirely.

## Deadlock and cleanup clinic

When the parent manually reads stdout to completion before reading stderr, a child can fill the stderr pipe and block while the parent waits for stdout EOF. `Command::output` handles the ordinary concurrent capture case internally, but it buffers output. A hard streaming limit requires concurrent draining, a limit state shared by the drainers, child termination, and a final wait so the process is reaped.

After spawn succeeds, every error path must account for the live child. “Drop the `Child`” is not a portable proof that execution ended or the process was reaped. The repair policy should state whether the parent requests termination, waits, preserves the first error, and reports cleanup failure separately.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can derive process behavior from the chosen `Command` method, preserve byte streams and argument boundaries, explain the pipe-deadlock scenario, and state what the standard library does not provide as a portable sandbox.

Then perform this destructive regression check: replace direct argument passing with a shell string and demonstrate one input whose meaning changes before the child program receives it. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.
