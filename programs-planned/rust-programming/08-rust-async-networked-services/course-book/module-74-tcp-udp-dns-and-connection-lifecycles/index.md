# Module 74: TCP, UDP, DNS, and Connection Lifecycles

**Course 8, day 4 · Module 74 of 80**

**74/80** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [JobWire guide](../capstone.md)

## The question

> What lifecycle does each network transport actually provide, and where should connection admission, name resolution, deadlines, half-close, datagram loss, and peer identity be represented?

## Why this comes now

Module 73 established that a byte stream does not contain application messages until a codec frames it. The next step is to own the transport itself. A listener can accept faster than the service can process. DNS can delay before a socket exists. TCP can close one direction while the other remains usable. A write can succeed locally while the peer later rejects the data. UDP preserves datagram boundaries but does not guarantee delivery, order, uniqueness, or connection state.

Network APIs are easy to call and easy to overinterpret. “Connected” does not mean authenticated. “Write completed” does not mean the peer committed the request. “Peer address” does not mean durable identity. “Timeout” does not undo transport or application effects. This module gives each transport event a precise place in the lifecycle.

## What you will be able to do

- distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close;
- acquire connection admission before spawning unbounded tasks;
- explain the limits of socket backlog as application backpressure;
- model DNS resolution and multi-address connection attempts under one deadline;
- distinguish TCP ordered bytes from application request completion;
- use split socket halves without losing one owner for connection shutdown;
- define idle, stage, and overall connection deadlines separately;
- explain UDP datagram preservation and its delivery non-guarantees;
- treat peer addresses as routing observations rather than authentication;
- write a connection ledger with every close and error path.

## Core model

### A listener is an admission boundary, not a work queue

A TCP listener asks the operating system to queue some pending connection handshakes. The backlog is finite, platform-dependent, and not a substitute for application limits. Once `accept` returns a socket, the application owns a live resource and usually a peer address observation.

The unsafe architecture is:

```text
loop:
    socket = accept
    spawn connection task
```

If clients arrive faster than tasks finish, accepted sockets and tasks grow without a product bound. The service should acquire an admission permit before or immediately after accept according to its desired overload behavior. Acquiring before accept limits accepted live sockets but may leave the OS backlog to absorb demand. Acquiring after accept can accept and then reject quickly, but the service must bound the time and resources between those events.

A common bounded loop is:

```text
acquire connection permit
select accept or shutdown
on accept success:
    move socket and permit into tracked connection task
on accept failure:
    release permit and classify error
```

The permit’s destructor closes the accounting path when the connection task ends.

### Accept errors have scope

Not every accept error should terminate the service, and not every error should be retried forever. Classify:

- temporary resource pressure;
- interrupted operation;
- invalid listener state;
- permission or configuration failure;
- shutdown-induced closure;
- repeated unknown failure.

A retry loop needs a delay or rate limit to avoid spinning on persistent failure. A production service should expose the policy rather than silently `continue` on every error.

### Connecting is a sequence, not one instant

A client hostname may resolve to several addresses. The connection operation can include:

```text
validate input
resolve name
choose/order candidates
attempt candidate 1
attempt candidate 2
perform protocol handshake
```

A timeout applied separately to every step can multiply the user’s intended budget. Prefer an overall deadline and derive remaining time for resolution, connect attempts, and handshake. Record which phase failed.

Happy-eyeballs-style racing can reduce latency across address families, but it introduces multiple live attempts and cancellation. Even a simple sequential client should distinguish DNS failure from connection refusal and protocol negotiation failure.

### TCP provides ordered reliable bytes, within limits

TCP provides an ordered byte stream while the connection exists. It retransmits and suppresses duplicates at the transport layer. It does not provide application messages, request IDs, transaction commits, authentication, or infinite delivery guarantees.

A successful local write generally means bytes were accepted by the local socket stack, not that the peer application read or committed them. A successful response parse is stronger evidence because it is application-level acknowledgement. Even then, the protocol must define what the response acknowledges.

Connection reset, timeout, or process failure can leave the client uncertain whether a request committed. Module 79 resolves that ambiguity with idempotency.

### Half-close is directional

TCP’s two byte directions can close independently. When a read returns EOF, the peer has closed its sending direction. The local side may still be able to write. Calling shutdown on the local write half communicates that no more bytes will be sent while still permitting reads.

Whether a protocol uses half-close is a product choice. Simple request/response protocols often use an explicit `QUIT` and then close both directions. Streaming protocols may use write shutdown as an end-of-request marker. Define the meaning rather than treating EOF as one universal “connection gone” event.

When a connection is split into owned read and write halves, give one connection supervisor authority over:

- cancellation;
- writer close;
- reader EOF;
- protocol terminal state;
- task joins;
- permit release.

Independent halves must not become independent lifecycles.

### Deadlines answer different questions

A timeout is an operation wrapper. A deadline is a policy budget. Several time concepts may coexist:

| Time policy | Meaning |
|---|---|
| connect deadline | maximum time to resolve and establish transport |
| handshake deadline | maximum time to negotiate protocol readiness |
| request deadline | overall budget for one application request |
| idle timeout | maximum time with no defined activity |
| write-stall timeout | maximum time output may fail to advance |
| shutdown grace | time allowed for in-flight work to finish |

Do not reset an overall request budget at every stage. Carry a deadline and derive remaining duration. Define “activity” for idle timeout: any byte, any complete frame, or any valid protocol message. Counting arbitrary bytes lets a malicious peer keep a connection alive by dribbling input.

### UDP preserves datagrams and little else

A UDP receive returns one datagram up to the supplied buffer size and its source address. Datagram boundaries are meaningful. If the buffer is too small, truncation behavior is platform/API-dependent and must be handled or avoided with a product maximum.

UDP does not guarantee:

- delivery;
- ordering;
- uniqueness;
- congestion-safe retransmission;
- connection establishment;
- source-address authenticity;
- path stability.

A “connected” UDP socket primarily fixes a default peer and filters incoming datagrams by address at the socket layer. It does not create TCP semantics.

A reliable protocol over UDP must add sequence numbers, acknowledgement, retransmission, duplication handling, congestion policy, fragmentation limits, and security. That is not a small wrapper around `recv_from`.

### Peer address is an observation

`SocketAddr` is useful for logging, routing, and rate-limiting within a stated threat model. NAT, proxies, load balancers, tunnels, address reuse, and spoofing (especially with UDP) prevent it from serving as a durable authenticated identity.

If identity matters, obtain it from a security protocol, token, mutual certificate, or trusted proxy contract. Keep transport peer and authenticated principal as separate fields.

### The connection ledger

For every connection state, record:

| State | Owned resources | Admission permit | Deadline | Legal I/O | Close path |
|---|---|---|---|---|---|
| accepted | socket, peer observation | held | handshake | framed read/write | reject or negotiate |
| ready | framed transport, broker client | held | idle/request | protocol messages | `QUIT`, EOF, error, shutdown |
| draining | writer, pending replies | held | shutdown grace | finish selected output | close after drain |
| terminal | none | released | none | none | task joined |

A connection is not finished merely because its read loop returns. Writer ownership, child tasks, broker waiters, and permit release must also terminate.

## Use the idea in a complete program

A bounded echo service illustrates admission, task ownership, and deadlines. It is not a production protocol, but its lifecycle is explicit.

```rust
use std::{io, sync::Arc, time::Duration};
use tokio::{
    io::{AsyncReadExt, AsyncWriteExt},
    net::{TcpListener, TcpStream},
    sync::Semaphore,
    task::JoinSet,
    time::timeout,
};
use tokio_util::sync::CancellationToken;

pub async fn serve(
    listener: TcpListener,
    max_connections: usize,
    idle: Duration,
    shutdown: CancellationToken,
) -> io::Result<()> {
    let permits = Arc::new(Semaphore::new(max_connections));
    let mut tasks = JoinSet::new();

    loop {
        let permit = tokio::select! {
            () = shutdown.cancelled() => break,
            permit = Arc::clone(&permits).acquire_owned() => {
                permit.map_err(|_| io::Error::other("admission closed"))?
            }
        };

        let accepted = tokio::select! {
            () = shutdown.cancelled() => {
                drop(permit);
                break;
            }
            result = listener.accept() => result,
        };

        match accepted {
            Ok((stream, _peer)) => {
                let child = shutdown.child_token();
                tasks.spawn(async move {
                    let _permit = permit;
                    handle(stream, idle, child).await
                });
            }
            Err(error) => {
                drop(permit);
                return Err(error);
            }
        }
    }

    shutdown.cancel();
    while let Some(result) = tasks.join_next().await {
        match result {
            Ok(Ok(())) => {}
            Ok(Err(_connection_error)) => {}
            Err(_panic_or_cancel) => {}
        }
    }
    Ok(())
}

async fn handle(
    mut stream: TcpStream,
    idle: Duration,
    shutdown: CancellationToken,
) -> io::Result<()> {
    let mut buffer = [0_u8; 1024];
    loop {
        let read = tokio::select! {
            () = shutdown.cancelled() => return Ok(()),
            result = timeout(idle, stream.read(&mut buffer)) => {
                result.map_err(|_| io::Error::new(io::ErrorKind::TimedOut, "idle timeout"))??
            }
        };
        if read == 0 {
            return Ok(());
        }
        timeout(idle, stream.write_all(&buffer[..read]))
            .await
            .map_err(|_| io::Error::new(io::ErrorKind::TimedOut, "write stalled"))??;
    }
}
```

This example intentionally rejects several production claims. Its idle timer resets per read operation and counts any bytes as activity. It closes on timeout. It does not retry accept errors. It waits indefinitely for tasks during shutdown. Later modules strengthen those policies.

## Practice sequence

1. Draw the accept-to-terminal connection lifecycle.
2. Compare acquiring a permit before and after accept.
3. Carry one overall deadline through resolve, connect, and handshake stages.
4. Demonstrate TCP half-close with a local test.
5. Define idle activity at frame or protocol-message level.
6. Build a bounded echo service with tracked tasks.
7. Explain why a peer address is not an authenticated identity.
8. Contrast TCP stream framing with UDP datagram semantics.

## Ready to continue

Continue only when you can explain:

- where application admission occurs;
- why backlog and connection permits solve different problems;
- why successful write is not remote commit;
- what EOF says about one TCP direction;
- how an overall deadline differs from repeated stage timeouts;
- which UDP guarantees do not exist;
- who closes and joins every connection task.

## Primary Rust references

- Tokio `TcpListener`, `TcpStream`, owned halves, `UdpSocket`, and `lookup_host` documentation;
- Tokio time and semaphore documentation;
- Rust standard-library `SocketAddr`, TCP, and UDP semantics;
- platform documentation when behavior is explicitly operating-system dependent.

## Continue

Complete the [workbook](workbook.md), use the [reasoned solutions](solutions.md) only after freezing your own answer, build [Deadline Echo Service](../../labs/module-04-deadline-echo-service/README.md), and add the fourth [JobWire increment](../capstone.md#increment-4-own-the-connection-lifecycle). Then continue to [Module 75](../module-75-protocol-state-machines-versioning-and-defensive-parsing/index.md).
