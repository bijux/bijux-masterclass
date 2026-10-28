# Module 51 — Network Boundaries: Addresses, DNS, Sockets, and Time

**Progress: 51/100**

## The governing question

> When a program says “connect to this service,” which values are configuration, which are resolver results, which are observed socket facts, and which time budget governs the whole attempt?

## Why this module comes now

Course 5 ended at process and file boundaries. Network programming adds a peer whose address, timing, and lifecycle are not controlled by your process. Before designing HTTP, you need a precise model of the layer beneath it. Otherwise a URL, a hostname, an IP address, a bound socket, and an advertised endpoint collapse into one vague “address,” and timeout policy fragments across resolver, connect, handshake, and request code.

This module establishes the vocabulary and timing model used by every later module. It also introduces a recurring design rule:

> Preserve the logical identity supplied by the product while treating resolved addresses and socket endpoints as temporary execution evidence.

Replacing a hostname with the first observed IP may appear convenient, but it can break TLS hostname verification, virtual hosting, failover, and diagnostics. Conversely, logging only the logical URL hides which candidate actually connected.

## What you will be able to do

By the end of the module, you can:

- distinguish URL, hostname, service name, port, address candidate, local endpoint, peer endpoint, and advertised endpoint;
- explain the different semantics of `dns.lookup()` and DNS-record queries;
- inject a resolver so address-family and fallback policy are testable;
- bind to port zero and report the actual address selected by the operating system;
- derive one monotonic deadline across resolution and several connection attempts;
- separate connect timeout, idle timeout, operation deadline, and shutdown grace;
- close losing or expired sockets without leaking handles;
- explain why a wildcard listening address is not normally a client-facing URL.

## The endpoint ledger

Use this ledger for every connection design.

| Value | Example | Authority | Lifetime |
|---|---|---|---|
| logical URL | `https://api.example.test:8443` | product configuration | stable for an operation |
| hostname | `api.example.test` | parsed URL | stable for resolution and TLS |
| service port | `8443` | URL or service policy | stable for an operation |
| address candidate | `2001:db8::8`, IPv6 | resolver | one candidate set |
| selected peer endpoint | `2001:db8::8:8443` | connected socket | one connection |
| local endpoint | `[2001:db8::20]:53422` | operating system | one connection |
| bound listener | `0.0.0.0:0` before listen | server configuration | startup intent |
| actual listener | `0.0.0.0:39117` after listen | listening socket | one server lifetime |
| advertised endpoint | `https://localhost:39117` | application policy | client-facing contract |

The same text can appear in several rows while carrying different authority. `localhost` is a logical hostname. `127.0.0.1` is one possible address. A server bound to `0.0.0.0` accepts connections on multiple interfaces, but `http://0.0.0.0:39117` is not a meaningful universal destination for remote clients.

## Names are not addresses

A hostname is a logical name consumed by resolution and often by TLS identity verification. Resolution returns zero or more candidates. The order can depend on platform configuration, address-family policy, local host files, DNS, and Node options. Code that assumes exactly one answer embeds a hidden environmental dependency.

There are two broad kinds of Node DNS behavior:

- `dns.lookup()` follows operating-system name-resolution behavior and produces address candidates suitable for ordinary connections;
- functions in `node:dns/promises` such as `resolve4()` and `resolve6()` issue DNS record queries and expose DNS-specific results.

Those APIs do not have identical semantics. A service client usually wants a connection policy, not raw DNS record inspection. A diagnostic tool may deliberately expose both.

A resolver boundary should return structured candidates:

```ts
export interface AddressCandidate {
  readonly address: string;
  readonly family: 4 | 6;
}

export type Resolver = (
  hostname: string,
) => Promise<readonly AddressCandidate[]>;
```

This allows tests to supply deterministic candidate sets. It also prevents network tests from depending on the machine's current DNS configuration.

## Resolution does not establish service identity

Suppose `api.example.test` resolves to `192.0.2.44`. The address tells the socket where to connect. The hostname remains the identity the client intended to reach. For HTTPS, the hostname normally remains the server name used in certificate verification and may be used as SNI during the handshake.

A common weak repair for local tests is to replace the hostname with an IP and disable TLS verification. That removes two requirements at once. A principled local test instead uses:

- a deterministic address or local listener;
- a certificate that includes the expected hostname or IP;
- an explicit local trust anchor;
- the original logical server name.

## Candidate policy is product policy

When several candidates exist, a client needs an explicit strategy. Possibilities include:

1. sequential attempts in resolver order;
2. a preferred family followed by fallback;
3. staggered parallel attempts;
4. an environment-specific connector delegated to Node's high-level client.

The course does not prescribe one universal algorithm. It requires the policy to preserve:

- one operation deadline;
- deterministic testability;
- cleanup of every losing socket;
- bounded simultaneous attempts;
- causal failure evidence;
- the logical hostname for later protocol layers.

A sequential strategy is easier to reason about and sufficient for the laboratory. A production connector may use a more sophisticated address-selection algorithm, but complexity does not remove the same obligations.

## One deadline, many phases

A chain of per-phase timeouts can exceed the promised operation budget:

```text
DNS timeout      1 second
candidate A      1 second
candidate B      1 second
TLS handshake    1 second
HTTP headers     1 second
```

A caller who supplied a one-second deadline did not authorize five seconds. Compute one absolute monotonic deadline:

```ts
import { performance } from 'node:perf_hooks';

export class Deadline {
  readonly #at: number;

  constructor(budgetMs: number) {
    if (!Number.isFinite(budgetMs) || budgetMs <= 0) {
      throw new RangeError('budgetMs must be positive and finite');
    }
    this.#at = performance.now() + budgetMs;
  }

  remainingMs(): number {
    return Math.max(0, this.#at - performance.now());
  }

  expired(): boolean {
    return this.remainingMs() === 0;
  }
}
```

Each phase consumes from the same remaining budget. A phase may have a stricter local cap, but it cannot reset the overall promise.

Wall-clock time such as `Date.now()` can jump due to clock correction. Use a monotonic clock for durations and deadlines. Use wall-clock timestamps only when the product needs calendar time in reports or protocols.

## Connect timeout is not idle timeout

These concepts answer different questions:

- **connect timeout**: how long may transport establishment take?
- **operation deadline**: how long may the entire user-visible operation take?
- **idle timeout**: how long may the connection remain without qualifying activity?
- **request timeout**: how long may one request phase take?
- **shutdown grace**: how long may accepted work drain after quiescence?

Calling `socket.setTimeout()` does not automatically destroy a socket and does not create an end-to-end deadline. It schedules a timeout event after inactivity according to socket semantics. Your code still owns the terminal action.

An idle policy also needs an activity definition. Does any byte reset it? Only a complete frame? A heartbeat? A protocol message? A peer can defeat a byte-based idle timer by sending one byte periodically, so the correct policy depends on the protocol threat model.

## Binding and reporting actual addresses

Tests and local services should often bind to port zero:

```ts
import net from 'node:net';

export async function listenEphemeral(
  host = '127.0.0.1',
): Promise<{ readonly server: net.Server; readonly port: number }> {
  const server = net.createServer();
  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen({ host, port: 0 }, () => {
      server.off('error', reject);
      resolve();
    });
  });

  const address = server.address();
  if (address === null || typeof address === 'string') {
    server.close();
    throw new Error('expected an IP socket address');
  }
  return { server, port: address.port };
}
```

Port zero delegates selection to the operating system and avoids racy “find a free port, close it, reopen it” logic. The actual port exists only after listening succeeds.

A wildcard host such as `::` or `0.0.0.0` describes where the server accepts traffic, not necessarily what clients should dial. ServiceWire therefore keeps bound and advertised endpoints separate.

## Connection ownership

A connection attempt allocates resources before it succeeds:

- a socket object;
- listeners;
- possibly an operating-system socket;
- a timer or abort listener;
- a place in the candidate set;
- error evidence.

The owner must settle exactly once and remove every listener. If one candidate succeeds while another attempt is in progress, the losing attempt must be destroyed and observed. If the deadline expires, all pending attempts must be closed. If the caller cancels, the same cleanup path should run.

The following shape is useful:

```ts
type ConnectOutcome =
  | { readonly ok: true; readonly socket: import('node:net').Socket;
      readonly candidate: AddressCandidate }
  | { readonly ok: false; readonly candidate: AddressCandidate;
      readonly error: Error };
```

Do not flatten every candidate failure into “connection refused.” Preserve enough bounded context to distinguish timeout, refusal, unreachable network, cancellation, and exhausted candidates.

## Worked reasoning case

Configuration contains:

```text
service URL: https://servicewire.test:9443
overall budget: 900 ms
resolver candidates:
  1. 2001:db8::10
  2. 192.0.2.10
```

Resolution takes 80 ms. The IPv6 attempt fails after 500 ms. The remaining budget is approximately 320 ms. The IPv4 attempt cannot receive a fresh 900 ms. If it connects after 200 ms, the TLS handshake and request share roughly 120 ms.

The correct conclusion may be deadline failure even though the second address would succeed with more time. Product promises constrain what the client is allowed to wait for.

The trace must retain:

```text
logical host: servicewire.test
candidate tried: 2001:db8::10
candidate error: connection refused
candidate tried: 192.0.2.10
selected peer: 192.0.2.10:9443
remaining budget at selection: ...
```

That trace explains both identity and execution.

## Common wrong models

### “A URL is an address”

A URL contains scheme, authority, and target information. Resolution and connection produce additional values. Treating the URL as a socket address obscures DNS, default ports, TLS identity, and path semantics.

### “DNS returns the server”

Resolution returns candidates. It does not prove that a service listens, that TLS identifies the host, or that the application is healthy.

### “One timeout option covers the operation”

Node APIs expose several timeout mechanisms with different scopes. The application must maintain the end-to-end deadline.

### “Binding to all interfaces gives me a client URL”

A wildcard bind is a server-side acceptance policy. Advertised client endpoints require explicit host policy.

### “The first error is the final error”

Several candidates may fail differently. Preserve bounded candidate evidence and select a causal summary only after policy is exhausted.

## Decision procedure

Before implementing a network client or server, answer in order:

1. What is the logical service identity?
2. Which component resolves it?
3. What candidate order and concurrency are allowed?
4. Which value remains the TLS/HTTP identity?
5. What is the one absolute operation deadline?
6. Which local timeouts are stricter subdivisions?
7. Who owns every candidate socket?
8. What actual endpoint is reported after binding or connecting?
9. Which endpoint is advertised to other components?
10. What evidence is retained when all candidates fail?

If one answer is “whatever Node chooses,” determine whether delegation is intentional and documented or merely unexamined.

## ServiceWire increment

Add:

- `ServiceEndpoint` validation;
- explicit bound and advertised endpoint types;
- a monotonic `Deadline`;
- an injectable resolver;
- actual port reporting after port-zero binds;
- causal connection-attempt records;
- tests that do not depend on public DNS.

Do not add HTTP routes yet. This increment establishes the endpoint and time vocabulary all later adapters use.

## Practice sequence

1. Predict the values produced by parsing several URLs, including IPv6 literals.
2. Compare `dns.lookup()` with record-query APIs conceptually.
3. Implement a deterministic resolver stub.
4. Bind a server to port zero and report its actual address.
5. Implement sequential candidate attempts under one deadline.
6. Add cancellation and prove all sockets close.
7. Explain why the hostname remains distinct from the selected address.

## Case study — a dual-stack connection under one 900 ms promise

A client receives `https://catalog.example.test:8443`. Its resolver returns an IPv6 candidate and an IPv4 candidate. The product promise is not “give each phase 900 ms”; it is “either return one verified connection or a causal failure within 900 ms.” Write the operation as one timeline:

```text
0 ms      parse and validate logical endpoint
8 ms      resolver returns two candidates
8–308 ms  attempt IPv6 candidate
308 ms    IPv6 connect times out
308–420 ms attempt IPv4 candidate
420–505 ms TLS handshake using catalog.example.test as server name
505 ms    connection becomes usable
```

The IPv4 attempt does not receive a fresh 900 ms. It receives the remainder. The TLS handshake does not receive a fresh 900 ms either. The connector should record which candidate failed, but the final successful socket still belongs to the logical service identity supplied by the URL.

Now change the case: the IPv6 socket connects at 250 ms, but TLS name verification fails at 340 ms. Whether the client should try IPv4 is product policy. A failure caused by one address path may justify another candidate; a certificate name mismatch may indicate that the endpoint configuration itself is wrong. The important design move is to classify the failure before deciding whether fallback is safe.

Use a candidate-attempt record such as:

```ts
interface AttemptEvidence {
  readonly address: string;
  readonly family: 4 | 6;
  readonly phase: 'connect' | 'handshake';
  readonly outcome: 'connected' | 'timeout' | 'cancelled' | 'failed';
  readonly code?: string;
  readonly elapsedMs: number;
}
```

This record is diagnostic evidence, not a retry policy. The policy belongs in a separate decision function. Keeping those concerns separate lets tests assert the evidence produced by each attempt and then assert the selection rule independently.

### The losing-attempt problem

A staggered connector may have two sockets in progress when one succeeds. Returning the winner is only half the operation. The owner must also:

1. cancel or destroy every losing socket;
2. remove timeout and abort listeners;
3. observe late errors so they do not become unhandled events;
4. prevent a late callback from settling the operation a second time;
5. retain only bounded diagnostic evidence.

A connector that returns quickly but leaves one pending socket is not successful. It has transferred an invisible resource leak to the process.

### A decision table for endpoint failures

| Failure | Usually candidate-local? | Usually retry another candidate? | Evidence to retain |
|---|---:|---:|---|
| `ECONNREFUSED` | yes | possibly | address, family, code |
| connect timeout | yes | possibly, within remaining deadline | elapsed time and remaining budget |
| cancellation | no | no | caller or parent cancellation cause |
| malformed URL | no | no | rejected configuration field |
| certificate name mismatch | often logical-endpoint-wide | normally no without explicit policy | expected name and verification class |
| all candidates exhausted | aggregate | no | bounded list of attempt outcomes |

Do not turn this table into universal networking law. It is a starting point for making product policy reviewable.

## Reader check — reconstruct the authorities

For a client that connects to `https://localhost:9443` through `127.0.0.1`, answer without using the chapter:

- Which value controls certificate name verification?
- Which value is used by the socket connector?
- Which value should appear in a user-facing configuration error?
- Which values belong in low-level diagnostic evidence?
- Which clock should govern the 500 ms operation promise?

If any answer is “the address,” the model is still too compressed. There are several addresses and names, each owned by a different layer.

## Ready to continue

You are ready for Module 52 when you can draw the connection attempt as a state machine and name the owner of every timer, listener, candidate socket, and terminal result.

## Primary Node.js references

- [DNS](https://nodejs.org/docs/latest-v24.x/api/dns.html)
- [Net](https://nodejs.org/docs/latest-v24.x/api/net.html)
- [URL](https://nodejs.org/docs/latest-v24.x/api/url.html)
- [Performance hooks](https://nodejs.org/docs/latest-v24.x/api/perf_hooks.html)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-51-address-resolution-observatory/README.md)
- [ServiceWire engineering guide](../capstone.md)
