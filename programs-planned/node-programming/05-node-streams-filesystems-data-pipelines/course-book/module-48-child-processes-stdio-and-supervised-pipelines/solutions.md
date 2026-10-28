# Module 48 Reasoned Solutions — Child Processes, Stdio, and Supervised Pipelines

These are reasoning standards, not a mandate to copy one implementation. A different design is correct when it proves the same public behavior, ownership, bound, failure, and completion contracts.

## 1. Prediction reasoning

### Shell interpolation

The decisive relationship is **program identity and arguments are separate data**. spawn(program, args) directly requests one executable with an argument vector. exec runs a command through a shell and therefore introduces shell parsing, quoting, expansion, and injection concerns. A product that does not require shell syntax should not construct one command string. On Windows and POSIX, executable resolution and quoting differ; direct spawning preserves the clearest contract.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Shell parsing converts data into syntax and introduces injection and portability problems. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Undrained stderr

The decisive relationship is **a child owns several terminal surfaces**. The error event reports failure to spawn or certain process-level errors. The exit event reports that the process exited and gives code or signal. The close event occurs after the stdio streams are closed. A data pipeline that needs every stdout byte must not treat exit alone as completion. Conversely, a closed stdout stream does not prove a successful exit code.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. Stdio can still contain unread bytes; close is the stronger process-plus-stdio observation. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Exit before close

The decisive relationship is **stderr is a stream with its own capacity policy**. Ignoring stderr can allow the child to block when the pipe buffer fills. Capturing all stderr can exhaust memory. The supervisor should drain it while retaining at most a configured number of bytes, recording whether truncation occurred. Diagnostic bytes may not be valid UTF-8; decode with an explicit replacement or fatal policy.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. The child can block or valuable failure evidence can be lost. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.
### Spawn failure

The decisive relationship is **abort is a process-tree policy**. Passing an AbortSignal to spawn can request child termination, but application policy still needs a grace period, escalation, and complete close observation. On some platforms, terminating the immediate child does not automatically terminate grandchildren. A production command runner must define whether it creates a process group or job object; this course keeps the claim to the direct child unless the platform-specific strategy is implemented.

For the stated case, do not stop at the visible value. Trace the source owner, any alias or queue, and the next terminal transition. A failed child may have emitted a partial candidate. The smallest useful experiment isolates this one rule and avoids unrelated configuration or type errors.

## 2. Repair reasoning

### Sequential stdio

A principled repair begins with: **Decide whether shell syntax is truly required; default to direct spawn.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Unbounded diagnostics

A principled repair begins with: **Specify the executable-resolution, environment, and working-directory policy.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.
### Premature commit

A principled repair begins with: **Bound retained stdout or stream it; always drain stderr with a retention limit.** The repair must keep incremental operation and the original product behavior. It should introduce the missing validation, owner, bound, or state transition instead of using `as`, collecting the complete source, swallowing an error, or deleting cancellation.

The acceptance test should fail against the weak design for the exact reason named in the prompt. After repair, the owning promise must settle only after the relevant resource or stage reaches its documented terminal state.

## 3. Focused construction review

A strong submission makes the module’s difficult relationship visible in function boundaries and tests. For this module, review the construction in this order:

1. Decide whether shell syntax is truly required; default to direct spawn.

2. Specify the executable-resolution, environment, and working-directory policy.

3. Bound retained stdout or stream it; always drain stderr with a retention limit.

4. Own stdin completion, stdout completion, stderr drain, and child close together.

5. Define acceptable exit codes and signal outcomes separately from byte validity.

6. Test spawn failure, early child exit, nonzero exit with output, stderr flood, abort, and destination failure.

Use deterministic fault injection. Exact byte, item, write, line, or lifecycle counts identify the causal boundary more clearly than timers.

Treat counters as evidence only when categories are disjoint and satisfy a stated conservation relationship.

## 4. Laboratory acceptance — Supervised Child Filter

The laboratory is complete only when all of these invariants are supported by executable evidence:

- No shell command string is constructed.
- Spawn failure is observed before stdio tasks become orphaned.
- Stdin, stdout, and stderr progress concurrently.
- Retained stderr is bounded while the complete stream is drained.
- Only zero exit with complete stdio produces a successful result.

The reference is one possible proof. Compare the first meaningful difference and keep your simpler design when it establishes the same invariants. Do not import abstraction without a requirement.

## 5. FlowLedger transfer

Add FlowLedger’s through command. It must preserve raw byte backpressure, reject nonzero child status, retain bounded stderr, abort the direct child, and commit stdout only after process and stream success agree.

Confirm that representation names, limits, causal errors, cancellation, accounting, CLI text, and process tests describe one feature. A passing unit test does not repair a stale public contract.

## 6. Independent transfer standard

Design an image-conversion wrapper around a native tool. State argument validation, executable policy, output-size limits, stderr retention, timeout, exit handling, and stage replacement.

A strong answer identifies the external authority, validates before retention or allocation, states the owner of every live resource, and names the exact event that changes visible product state. It also states at least one intentionally unsupported guarantee.

## 7. Defense standard

Defend the design in both directions: map each product claim to its mechanism and evidence, then map each Node event or return value to the narrower fact it proves.

Replace “the stream handled it” with representation, owner, bound, and terminal state.
