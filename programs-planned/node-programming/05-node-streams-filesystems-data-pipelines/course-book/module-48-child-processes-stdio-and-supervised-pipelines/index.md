# Module 48 — Child Processes, Stdio, and Supervised Pipelines

**Progress: 48/100**

## The governing question

> How do you integrate another executable into a Node.js data pipeline without introducing shell ambiguity, unbounded output capture, orphan processes, or incomplete terminal accounting?

## Why this module comes now

The previous modules kept execution inside one process. Real data tooling often invokes compressors, converters, or domain utilities implemented elsewhere. A child process adds executable identity, argument boundaries, environment policy, three standard streams, process lifecycle, operating-system signals, and an exit status that is not the same as stream completion.

The pipeline can now transform data inside the Node process. Module 48 introduces an external program as a stage. This adds executable resolution, argument boundaries, environment, three independent standard streams, operating-system process state, and termination signals. Course 4’s task supervision becomes process supervision; Module 43’s pressure rules must cross kernel pipes.

A child process is never “just another Transform.” It has a separate lifecycle whose success must agree with stream completion before output can commit.

## Observable outcomes

By the end of this module, you can:

- choose spawn, execFile, and exec according to shell and buffering requirements

- preserve executable and argument boundaries without command-string construction

- pipe stdin, stdout, and stderr under explicit backpressure and retention limits

- distinguish spawn error, exit, close, signal termination, and pipeline failure

- abort and join a child process without leaving descendants or partial output unowned

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| invocation | Which executable, argument vector, environment, and working directory are used? |
| stdin owner | Who writes, closes, and aborts child input? |
| stdout owner | Who drains and stages child output? |
| stderr policy | How much diagnostic data is retained and what happens beyond the limit? |
| termination | How are spawn error, exit code, signal, close, and abort distinguished? |
| commit rule | Which combination of stdio completion and child status authorizes publication? |

## Program identity and arguments are separate data

spawn(program, args) directly requests one executable with an argument vector. exec runs a command through a shell and therefore introduces shell parsing, quoting, expansion, and injection concerns. A product that does not require shell syntax should not construct one command string. On Windows and POSIX, executable resolution and quoting differ; direct spawning preserves the clearest contract.

execFile is useful for buffered results with a known maximum. For unbounded or large output, spawn exposes streams and lets backpressure govern movement. A maxBuffer option is not equivalent to a streaming pipeline; it intentionally retains output in memory up to the limit.

## A child owns several terminal surfaces

The error event reports failure to spawn or certain process-level errors. The exit event reports that the process exited and gives code or signal. The close event occurs after the stdio streams are closed. A data pipeline that needs every stdout byte must not treat exit alone as completion. Conversely, a closed stdout stream does not prove a successful exit code.

The supervising scope combines: stdin pipeline result, stdout pipeline result, bounded stderr capture, child close status, and cancellation result. It produces one typed terminal outcome only after all owned surfaces are reconciled.

## Stderr is a stream with its own capacity policy

Ignoring stderr can allow the child to block when the pipe buffer fills. Capturing all stderr can exhaust memory. The supervisor should drain it while retaining at most a configured number of bytes, recording whether truncation occurred. Diagnostic bytes may not be valid UTF-8; decode with an explicit replacement or fatal policy.

The retained diagnostic is evidence, not the complete stream. Include byte counts and truncation state so operators do not mistake a clipped message for the full child output.

## Abort is a process-tree policy

Passing an AbortSignal to spawn can request child termination, but application policy still needs a grace period, escalation, and complete close observation. On some platforms, terminating the immediate child does not automatically terminate grandchildren. A production command runner must define whether it creates a process group or job object; this course keeps the claim to the direct child unless the platform-specific strategy is implemented.

Cancellation can race with normal exit. Preserve the observed exit code or signal and the abort cause rather than flattening every case into “cancelled”.

## Child transformation is a trust boundary

Even a locally installed utility can emit malformed, oversized, or semantically invalid output. Treat child stdout as untrusted input to the next framing or validation layer. Do not assume that a zero exit status makes the bytes valid. Likewise, a nonzero exit can occur after partial stdout; the staged destination must not commit that candidate.

Environment variables, current directory, inherited descriptors, and PATH all affect behavior. Pass a deliberate environment and working directory for reproducible tools. Never forward secrets by default.

## Argument vectors preserve structure that shell strings erase

`spawn(program, args, { shell: false })` passes an executable and discrete arguments. Constructing one command string introduces quoting, escaping, expansion, and injection concerns belonging to a shell language. Use a shell only when shell syntax is a deliberate requirement, and then treat the command as code with a tightly controlled source.

Executable resolution and environment are also policy. Relying on ambient `PATH` may be acceptable for an interactive tool and inappropriate for a service. Record the working directory, inherited variables, and platform assumptions that affect the child.

## All three standard streams must make progress

Writing stdin while waiting to read stdout can deadlock when the child fills its stdout pipe and stops reading input. Ignoring stderr can create the same problem. A supervisor starts input pumping and output draining concurrently, bounds retained diagnostics, and still consumes bytes beyond the retained stderr excerpt so the pipe cannot block the child.

The destination’s backpressure must propagate through stdout. If output is staged transactionally, the child’s stdout cannot outrun the file sink indefinitely. The source-to-stdin path and stdout-to-sink path are separate pipeline promises owned by one supervisor.

## Exit, close, and commit answer different questions

A spawn error means no process was successfully started. `exit` reports termination status, while `close` occurs after stdio streams have closed. A zero exit code before stdout is fully drained is not enough to commit. Conversely, successfully draining stdout does not excuse a nonzero exit.

The commit predicate should require successful input handling where relevant, successful stdout staging, bounded stderr collection, complete child close, and an accepted exit status. Cancellation must reach the child and both pipeline directions, then the supervisor must wait for terminal cleanup rather than returning immediately after sending a signal.

## Worked case — Direct spawning with bounded stderr

```ts
import { spawn } from 'node:child_process';

export function startFilter(program: string, args: readonly string[], signal?: AbortSignal) {
  return spawn(program, [...args], {
    shell: false,
    stdio: ['pipe', 'pipe', 'pipe'],
    signal,
    windowsHide: true,
  });
}
```

This function preserves program and argument boundaries and exposes all three stdio streams for an owning supervisor. It is not itself a complete abstraction: callers must drain stderr, handle spawn error, pipe stdin and stdout, observe close, inspect code and signal, and destroy remaining streams after failure. Returning the raw ChildProcess is appropriate only to an internal layer that owns those obligations.

## Extended case analysis

A formatter writes 5 MB to stdout, 2 MB to stderr, and then exits zero. If the parent pipes stdin and awaits only the exit code while leaving stderr unread, the child may block before exit because the stderr pipe fills. A correct supervisor continuously drains stderr, retains only the configured excerpt, and records whether truncation occurred. Retention is bounded; pipe progress remains complete.

## What this mechanism establishes

A correct implementation establishes these local facts:

- No shell command string is constructed.

- Spawn failure is observed before stdio tasks become orphaned.

- Stdin, stdout, and stderr progress concurrently.

It does **not** establish the stronger claims hidden by these shortcuts:

- building a shell string from untrusted values;

- using `exec` and accepting its whole-output buffer for unbounded data;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. Decide whether shell syntax is truly required; default to direct spawn.

2. Specify the executable-resolution, environment, and working-directory policy.

3. Bound retained stdout or stream it; always drain stderr with a retention limit.

4. Own stdin completion, stdout completion, stderr drain, and child close together.

5. Define acceptable exit codes and signal outcomes separately from byte validity.

6. Test spawn failure, early child exit, nonzero exit with output, stderr flood, abort, and destination failure.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Interpolating user input into exec

Shell parsing converts data into syntax and introduces injection and portability problems.

### Waiting only for exit

Stdio can still contain unread bytes; close is the stronger process-plus-stdio observation.

### Ignoring stderr

The child can block or valuable failure evidence can be lost.

### Committing stdout before checking exit status

A failed child may have emitted a partial candidate.

## Apply the mechanism in FlowLedger

Add FlowLedger’s through command. It must preserve raw byte backpressure, reject nonzero child status, retain bounded stderr, abort the direct child, and commit stdout only after process and stream success agree.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design an image-conversion wrapper around a native tool. State argument validation, executable policy, output-size limits, stderr retention, timeout, exit handling, and stage replacement.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 48 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Supervised Child Filter** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Choose spawn, execFile, and exec according to shell and buffering requirements

- Preserve executable and argument boundaries without command-string construction

- Pipe stdin, stdout, and stderr under explicit backpressure and retention limits

- Distinguish spawn error, exit, close, signal termination, and pipeline failure

- Abort and join a child process without leaving descendants or partial output unowned
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/child_process.html](https://nodejs.org/docs/latest-v24.x/api/child_process.html)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-48-supervised-child-filter/README.md)
- [FlowLedger engineering guide](../capstone.md)
