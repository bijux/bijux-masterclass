# 54 — Processes, Environments, and Standard Streams

**Course 6, day 4 · Module 54 of 90**  
`██████████████████░░` **54/90**

[← Module 53: Paths, Names, and Platform Boundaries](../module-53-paths-names-and-platform-boundaries/index.md) · [Course 6 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 55: Unsafe Rust as a Proof Boundary →](../module-55-unsafe-rust-and-safety-proofs/index.md)

## The question

> How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?

## Why this comes now

Files and paths establish the external namespace. Process creation adds another system boundary: program selection, argument encoding, environment inheritance, current directory, standard streams, lifecycle, and exit status. Module 54 keeps command construction structured and treats output as bytes. Concurrency is still a later course; this module uses high-level process operations and explains where complex streaming requires concurrent I/O.

## What you will be able to do

- Construct commands from a program plus arguments, not an interpolated shell line.
- Control environment inheritance and current-directory policy explicitly.
- Distinguish `status`, `output`, `spawn`, `wait`, `try_wait`, and `wait_with_output`.
- Treat stdout and stderr as independent byte streams.
- Explain pipe deadlocks and choose an API consistent with the I/O protocol.
- Represent exit status without assuming every termination has a portable integer code.

## Core model

### A process command is structured data

`Command::new` accepts the program separately from each argument:

```rust
let output = std::process::Command::new(program)
    .args(arguments)
    .output()?;
```

Do not build `format!("{program} {user_input}")` and pass it to a shell. Shell parsing adds quoting, expansion, redirection, pipelines, and command substitution. Escaping correctly is platform- and shell-specific, and untrusted input can become executable syntax.

Direct process spawning is not automatically safe: the selected executable can still be untrusted, arguments can trigger dangerous behavior in that program, and Windows batch-file handling has special caveats. The key improvement is that Rust and the operating system preserve argument boundaries rather than reparsing one string as a command language.

### Program resolution is part of the trust model

A bare program name may be resolved through `PATH` or platform rules. A privileged or reproducible tool should decide whether it accepts that ambient lookup or requires an absolute configured path. The current directory and environment can also influence dynamic libraries, configuration, locale, and child behavior.

FrameVault’s capture command accepts the program as an `OsString`, does not invoke a shell, and records the exact supplied program and arguments. It does not claim that a bare name identifies the same executable on every machine.

### Environment inheritance should be deliberate

By default a child inherits the parent environment with explicit modifications. Secrets, proxies, locale, tracing flags, and tool-specific variables can change behavior. Reproducible execution may begin with `env_clear` and add a small allowlist; ordinary developer tools may intentionally inherit.

Environment keys and values are `OsStr`/`OsString`, not necessarily UTF-8. A capture format that records them must choose an encoding or reject unrepresentable values. FrameVault records only explicitly requested environment overrides and renders nonportable values for diagnostics rather than embedding the entire ambient environment.

### Choose the process API from the I/O protocol

`status` waits and inherits standard streams unless configured otherwise. `output` waits and captures stdout and stderr, with stdin closed. `spawn` returns a `Child` for interactive or long-running control. `wait` reaps the child and returns status. `try_wait` polls without blocking. `wait_with_output` consumes the child and collects configured pipes.

The API choice should follow the protocol. A finite command with no stdin and bounded expected output fits `output`. An interactive protocol needs explicit stdin/stdout handling and usually concurrent I/O. A daemon-like child needs lifecycle, shutdown, and ownership rules beyond one call.

### Stdout and stderr are bytes

`Output` contains `Vec<u8>` for stdout and stderr. The child may emit arbitrary bytes or use an encoding unrelated to UTF-8. Decode as text only when the command contract says so.

Keep streams separate. Concatenating them after completion destroys their temporal interleaving but at least preserves channel identity if framed separately. Capturing a true interleaved event stream requires concurrent reads and timestamps or sequence numbers. FrameVault stores stdout and stderr as distinct length-prefixed byte fields and does not pretend to reconstruct exact interleaving.

### Pipe capacity can create deadlock

A classic deadlock occurs when the parent writes a large stdin while the child writes enough stdout to fill its pipe, and neither side reads the stream the other needs. Similarly, reading stdout to completion before reading stderr can block if stderr fills.

`Command::output` and `wait_with_output` handle the common finite no-input capture. If you manually drive multiple pipes, you need concurrent I/O, nonblocking facilities, or a protocol that bounds and orders writes. Course 7 teaches threads and synchronization; Course 8 adds asynchronous I/O. Course 6 identifies the boundary and refuses to hide it behind a naïve sequential loop.

### Child ownership includes reaping

Dropping `Child` does not universally guarantee that the operating-system process is waited on. A long-running program that spawns and forgets children can accumulate unreaped process state on some systems.

Own the child until its lifecycle completes. Define what happens if the parent operation is cancelled or an error occurs after spawn. `kill` requests forced termination but platform details differ, and successful kill does not replace `wait` when reaping is required. A robust wrapper can attempt kill, then wait, while preserving the primary error.

### Exit status is more than an integer

`ExitStatus::success` is portable. `code()` returns `Option<i32>` because a process may terminate without a conventional exit code, for example through a signal on Unix. Platform extension traits expose additional information.

Do not map `None` to zero or an arbitrary negative number without documenting that representation. FrameVault records a portable status category plus an optional numeric code and preserves the platform-rendered status text for inspection.

### Windows command lines require specific caution

Unix process APIs pass an argument vector. Windows process creation uses a command-line string interpreted by the child’s parsing convention. Rust applies quoting for common conventions, but programs with custom parsers and batch files can behave differently. The standard-library documentation specifically warns about `.bat` and `cmd.exe` behavior.

A cross-platform tool should test the exact target programs it supports, restrict untrusted inputs where parsing conventions are unusual, and avoid claiming that one argument list has identical interpretation by every executable.

### Resource limits and timeouts are not a one-call portable feature

The standard library does not provide a universal child timeout, memory limit, CPU quota, sandbox, or process-group termination API. A loop around `try_wait` plus sleep can implement a simple elapsed-time policy, but robust termination of descendants and resource containment require platform facilities or specialized crates.

FrameVault’s first capture command waits for completion and documents that it is unsuitable for untrusted or unbounded commands. The module teaches honest boundary recognition rather than a misleading portable sandbox.

### Record enough context to reproduce, but not secrets by accident

A command capture should store:

- program and argument boundaries;
- selected working directory policy;
- explicit environment overrides;
- exit status category and code;
- stdout and stderr bytes;
- capture format version.

It should not automatically store the entire inherited environment. Reproduction and confidentiality compete. The capture schema must say what it records and what remains ambient.

### A command capture schema

FrameVault does not store a shell command string. It stores a structured payload:

```text
program-len      u32 little-endian
program          UTF-8 bytes
argument-count   u32 little-endian
repeat argument-count times:
    argument-len u32 little-endian
    argument     UTF-8 bytes
status-kind      u8: 0=success, 1=exit-code, 2=other-termination
status-code      i32 little-endian, meaningful only for kind 0 or 1
stdout-len       u64 little-endian
stdout           bytes
stderr-len       u64 little-endian
stderr           bytes
```

This format deliberately accepts only program and arguments representable as UTF-8. The process API itself uses `OsString`; the archive boundary may reject a capture after execution if a supplied native argument cannot be stored. A stronger product could define platform-tagged native encodings, but version 1 remains portable and honest.

The output limit is checked on `stdout.len() + stderr.len()` with checked addition after `Command::output` returns. That bounds stored data but not peak child output already captured by the standard library. A truly untrusted child requires streaming limits and termination, which in turn require concurrency or asynchronous I/O. The course explicitly does not mislabel post-hoc rejection as a resource sandbox.

### Lifecycle matrix

| Protocol | Suitable API | Main risk |
|---|---|---|
| finite, no stdin, bounded expected output | `output` | memory growth before limit check |
| inherited terminal interaction | `status` | ambient terminal and environment |
| explicit managed child | `spawn` + `wait` | cleanup and reaping on every path |
| piped stdin plus stdout/stderr | `spawn` with concurrent I/O | pipe deadlock |
| polling timeout | `spawn` + `try_wait` | descendant cleanup and platform semantics |

Selecting `spawn` creates a live-resource state machine. Write it explicitly:

```text
configured → spawned → running → exited → reaped
                    ↘ termination-requested ↗
```

An error after `spawn` does not erase the running child. The wrapper still owns a cleanup obligation.

### Environment policy example

For reproducible tool invocation:

```rust
let mut command = Command::new(program);
command
    .args(args)
    .current_dir(working_directory)
    .env_clear()
    .env("PATH", controlled_path)
    .env("LANG", "C")
    .env("LC_ALL", "C");
```

This can also break programs that need `HOME`, system variables, dynamic-library paths, or Windows environment entries. An allowlist must be product-specific. The correct lesson is not “always clear the environment”; it is “ambient inheritance is a decision.”

### Self-child testing

Cross-platform process tests should avoid assuming `echo`, `sh`, `cmd`, or `true` exists. The FrameVault test binary can invoke its own executable with a hidden deterministic subcommand that writes known bytes to stdout and stderr and exits with a requested code. This preserves argument boundaries and makes tests independent of shell tools.

The hidden mode is not part of the public CLI documentation. It is still ordinary product code and must validate its inputs without panic.

## Use the idea in a complete program

FrameVault adds a command-capture record. `capture` invokes a program directly through `Command`, closes stdin, captures bounded stdout and stderr, records the supplied program and arguments as UTF-8 only when representable, and stores a portable exit-status model. It rejects captures whose combined output exceeds the configured limit and documents that untrusted long-running commands require later containment work.

The matching independent laboratory is [Bounded Process Capture](../../labs/module-04-bounded-process-capture/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) by predicting the exact program, argument vector, environment, status, stdout bytes, and stderr bytes at every boundary. Build the Bounded Process Capture lab, then inspect FrameVault's capture format for any accidental shell parsing, text conversion, or hidden memory-bound claim.

## Ready to continue

You are ready when you can derive process behavior from the chosen `Command` method, preserve byte streams and argument boundaries, explain the pipe-deadlock scenario, and state what the standard library does not provide as a portable sandbox.

## Primary Rust references

- [Rust standard library: process module](https://doc.rust-lang.org/std/process/index.html)
- [Rust standard library: Command](https://doc.rust-lang.org/std/process/struct.Command.html)
- [Rust standard library: Child](https://doc.rust-lang.org/std/process/struct.Child.html)
- [Rust standard library: Output](https://doc.rust-lang.org/std/process/struct.Output.html)

## Continue

1. Complete the [Module 54 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 54 — Bounded Process Capture](../../labs/module-04-bounded-process-capture/README.md) from its public contract.
3. Apply the Module 54 increment in the [FrameVault engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
