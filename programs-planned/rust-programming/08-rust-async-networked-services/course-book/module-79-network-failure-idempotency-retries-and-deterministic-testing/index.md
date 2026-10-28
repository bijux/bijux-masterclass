# Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing

**Course 8, day 9 · Module 79 of 80**

**79/80** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [JobWire guide](../capstone.md)

## The question

> When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?

## Why this comes now

A bounded, cancellation-aware service can still duplicate work. The client sends a request, the server commits it, and the response is lost. The client sees a timeout or disconnect and cannot infer whether nothing happened, work is in progress, or the operation completed. Blind retry creates a second semantic effect. Never retry leaves recoverable work unresolved.

This is not primarily a socket problem. It is a distributed-knowledge problem. The client and server observe different events. Course 8 resolves it with an application protocol: an idempotency key, request fingerprint, authoritative server record, bounded retention, and retry policy derived from failure class and overall deadline.

Testing this behavior requires control over time and I/O. Real sleeps and “try several times” tests are weak because they depend on scheduler and machine speed. Deterministic async tests use paused time, scripted peers, explicit gates, and exact assertions about attempt count, commit count, and terminal result.

## What you will be able to do

- classify failures by phase, scope, retryability, and commit ambiguity;
- distinguish idempotent operation semantics from retrying an HTTP or TCP request;
- design idempotency keys with scope, fingerprint, in-progress state, terminal result, and retention;
- reject key reuse with different request content;
- attach duplicate callers to one in-progress operation or return a defined status;
- calculate retry attempts under one overall deadline;
- use exponential backoff and jitter without synchronized retry waves;
- prevent retries for protocol, validation, and permanent domain failures;
- test time with Tokio’s paused clock;
- script connect, partial response, disconnect, retry, and duplicate scenarios causally.

## Core model

### Failure is information, not one Boolean

Classify a failure along several dimensions:

| Dimension | Examples |
|---|---|
| phase | resolve, connect, handshake, write, wait, parse, domain |
| scope | request, connection, service, dependency |
| permanence | transient, permanent, unknown |
| commit knowledge | definitely before commit, definitely after commit, ambiguous |
| retry safety | safe without key, safe only with key, unsafe |
| budget | enough time for another attempt or exhausted |

A type such as `NetworkError(String)` erases the policy inputs. Preserve structured causes internally and render controlled public errors at the boundary.

### Transport errors cannot reveal remote commit reliably

Consider:

```text
client writes complete request
server receives and commits
server writes response
connection resets before client receives it
```

The client sees failure after its local write. It cannot distinguish this schedule from one where the server crashed before reading. TCP reliability does not provide application transaction visibility.

A response acknowledging the commit resolves the uncertainty when received. When it is lost, the client needs an application-level recovery identity.

### Idempotency is a server-side semantic contract

An operation is idempotent when repeated applications have the same intended semantic effect as one application. That property can be inherent—setting a value to a specific state—or implemented through an idempotency record for an otherwise non-idempotent action.

A useful record is:

```text
(scope, idempotency key) → {
    request fingerprint,
    state: in-progress | completed | failed-terminal,
    result or public error,
    created/expires,
}
```

The scope might be tenant, authenticated principal, or service-wide namespace. The fingerprint covers every field that changes meaning. It should use canonical request representation so semantically identical requests compare consistently.

### Duplicate handling has three cases

1. **Unknown key:** validate, commit the record as in-progress, and start one operation.
2. **Known key, same fingerprint:** return cached terminal result or attach to the in-progress operation.
3. **Known key, different fingerprint:** reject with a stable key-conflict error.

Do not overwrite the first record. That would allow a key collision to redirect a retry to different work.

For in-progress duplicates, choices include:

- await the same result through bounded waiters;
- return `IN_PROGRESS` with a retry hint;
- return a status location or operation ID.

Waiting is convenient but each waiter consumes memory and a connection. Bound waiters per key or prefer status recovery.

### Retention is part of correctness

If idempotency records expire after one minute but clients retry for five minutes, duplicate effects can occur after eviction. Align:

- maximum client retry window;
- clock-skew assumptions when wall time is involved;
- server retention duration;
- maximum record count and memory;
- restart persistence requirements.

An in-memory record is valid only within one process lifetime. JobWire states that scope explicitly. A production multi-process service would use durable shared authority or route all identical keys to one owner.

### Retry only failures whose policy permits it

A conservative table:

| Failure | Retry? |
|---|---|
| invalid request | no |
| unsupported version | no |
| unknown operation | no |
| server busy | yes, within deadline and attempt limit |
| connect refused | perhaps |
| disconnect before any request bytes | perhaps |
| disconnect after write | only with idempotency semantics |
| malformed server response | usually no; protocol defect |
| internal temporary error explicitly marked retryable | perhaps |
| overall deadline expired | no |

The client should not infer retryability only from I/O error kind. Phase and protocol response matter.

### Backoff needs an overall deadline

A retry policy has:

- maximum attempts;
- initial delay;
- multiplier;
- maximum delay;
- jitter strategy;
- per-attempt stage caps;
- overall deadline;
- retryable failure predicate.

Before sleeping or starting another attempt, check remaining budget. The final attempt still needs time to complete. A good client may stop before the formal deadline when remaining time cannot cover the minimum useful attempt.

### Jitter avoids synchronized waves

If thousands of clients retry at exact powers of two, a recovering service receives periodic bursts. Jitter spreads retries. The jitter source should be injectable in tests. This course can use deterministic values rather than a random dependency; production can use a suitable randomness source.

Document the algorithm, for example full jitter:

```text
delay = random(0 .. min(max_delay, base * 2^attempt))
```

Jitter does not replace server backpressure or retry limits.

### Retry loop owns one semantic request

The client should construct the request and idempotency key once, then reuse them across attempts. Generating a new key for every retry creates new operations. Generating one request ID for every retry may or may not be correct depending on correlation policy; request IDs often identify each wire attempt while the idempotency key identifies the semantic operation.

A retry ledger records:

| Attempt | Request ID | Idempotency key | Failure | Commit ambiguity | Delay | Remaining budget |
|---:|---|---|---|---|---:|---:|
| 1 | r-1 | k-9 | reset after write | yes | 40 ms | 900 ms |
| 2 | r-2 | k-9 | busy | server retained record | 90 ms | 700 ms |
| 3 | r-3 | k-9 | cached success | resolved | none | 580 ms |

### Deterministic async tests control the cause

Useful tools:

- `#[tokio::test(start_paused = true)]` or explicit time pausing;
- `time::advance` for timers and backoff;
- local `TcpListener` bound to an ephemeral loopback port;
- `tokio::io::duplex` for in-memory byte streams where socket semantics are not under test;
- notifications to place server state before disconnect;
- scripted attempt closures returning exact failure sequences;
- counters for commit count, attempt count, and waiter count;
- test-only fault injection at named protocol phases.

A timeout around the entire test is still useful as a hang detector. It should not be the only evidence that shutdown or retry works.

### Time abstraction belongs at policy boundaries

Tokio’s paused clock works for Tokio timers. Domain code that calls `std::time::SystemTime::now()` directly can remain nondeterministic. Prefer passing an `Instant`, deadline, or clock capability into policy code. Use wall clock only when the protocol or persistence format requires civil time.

Do not create a broad clock trait merely to demonstrate abstraction. One function parameter returning `Instant` may be sufficient.

### Retry tests need semantic assertions

A strong idempotency test asserts:

```text
wire attempts = 2
server commits = 1
handler executions = 1
final client result = original result
key conflict = rejected
retained records <= configured maximum
```

A test that only observes “eventually succeeded” can pass despite duplicate side effects.

## Use the idea in a complete program

The retry loop below is generic over the attempt function and deterministic jitter source:

```rust
use std::{future::Future, time::Duration};
use tokio::time::{self, Instant};

#[derive(Debug, Clone, Copy)]
pub struct RetryPolicy {
    pub max_attempts: u32,
    pub initial_delay: Duration,
    pub max_delay: Duration,
}

pub async fn retry_with_deadline<T, E, F, Fut, R, J>(
    deadline: Instant,
    policy: RetryPolicy,
    mut attempt: F,
    mut retryable: R,
    mut jitter: J,
) -> Result<T, E>
where
    F: FnMut(u32) -> Fut,
    Fut: Future<Output = Result<T, E>>,
    R: FnMut(&E) -> bool,
    J: FnMut(Duration, u32) -> Duration,
{
    let mut number = 1;
    let mut base = policy.initial_delay;

    loop {
        let result = attempt(number).await;
        match result {
            Ok(value) => return Ok(value),
            Err(error) => {
                if number >= policy.max_attempts || !retryable(&error) {
                    return Err(error);
                }
                let now = Instant::now();
                if now >= deadline {
                    return Err(error);
                }
                let delay = jitter(base.min(policy.max_delay), number);
                if now + delay >= deadline {
                    return Err(error);
                }
                time::sleep(delay).await;
                number += 1;
                base = base.saturating_mul(2).min(policy.max_delay);
            }
        }
    }
}
```

The function returns the last concrete error when no retry fits. A product may instead return a wrapper preserving attempts and deadline exhaustion. The attempt closure must reuse the semantic idempotency key. The loop cannot make a non-idempotent operation safe by itself.

## Practice sequence

1. Classify JobWire failures by phase and commit knowledge.
2. Define idempotency scope, fingerprint, and retention.
3. Implement same-key/same-request, same-key/different-request, and in-progress behavior.
4. Write one overall retry deadline.
5. Inject deterministic jitter.
6. Script disconnect after commit and prove one execution.
7. Test paused-time backoff without wall-clock sleeps.
8. State in-memory idempotency limitations.

## Ready to continue

Continue only when you can explain:

- why disconnect after write creates ambiguous commit;
- what server state makes retry safe;
- why a fingerprint belongs beside the key;
- which failures are permanent;
- how retry delay and attempts fit one deadline;
- what deterministic tests control;
- which idempotency claims fail after process restart.

## Primary Rust references

- Tokio time and test-time documentation;
- Tokio networking and I/O contracts from prior modules;
- application protocol definitions for idempotency, retryability, and status recovery.

## Continue

Complete the [workbook](workbook.md), use the [reasoned solutions](solutions.md) only after freezing your own answer, build [Idempotent Retry Client](../../labs/module-09-idempotent-retry-client/README.md), and add the ninth [JobWire increment](../capstone.md#increment-9-resolve-ambiguous-failure). Then continue to [Module 80](../module-80-integrated-async-service-architecture-testing-and-audit/index.md).
