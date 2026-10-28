# Module 53 — UDP: Datagrams, Loss, Duplication, Reordering, and Correlation

**Progress: 53/100**

## The governing question

> How do you build a small request/response or discovery protocol when the transport preserves datagram boundaries but does not promise delivery, order, uniqueness, connection state, or application identity?

## Why this module comes now

TCP forced you to add message boundaries to an ordered stream. UDP makes the opposite trade: message boundaries are preserved, but most other conveniences disappear. One datagram is one delivery unit, yet it may never arrive, may arrive more than once, may arrive after a later datagram, or may come from an unexpected endpoint.

This contrast is pedagogically important. It separates message framing from reliability and reveals which guarantees belong to the application rather than the transport. ServiceWire will use UDP only for optional local discovery, where bounded messages and explicit trust limits are more important than delivery certainty.

## Observable outcomes

By the end of the module, you can:

- bind and close `dgram` sockets under one owner;
- distinguish connected UDP convenience from connection-oriented transport semantics;
- design a bounded versioned datagram format;
- correlate responses with a cryptographically random nonce or request ID;
- validate peer endpoint policy;
- retry under one total deadline;
- ignore stale, duplicate, malformed, oversized, and unrelated responses;
- define duplicate request handling and replay-cache bounds;
- assess amplification risk;
- state clearly which discovery facts are unauthenticated.

## The datagram ledger

| Dimension | Required decision |
|---|---|
| wire version | how incompatible formats are rejected |
| message type | request, response, error, or heartbeat |
| request identity | nonce or request ID and its entropy |
| peer policy | exact endpoint, any endpoint on local host, or controlled subnet |
| payload bound | maximum datagram bytes before parsing |
| attempts | maximum number and schedule |
| total deadline | one budget across all attempts |
| duplicate policy | ignore, replay cached response, or reject |
| stale policy | what happens after operation completion |
| amplification | response size relative to request and spoofability |
| trust | what the response proves and does not prove |

## UDP preserves datagrams

A call to `socket.send()` submits one datagram. A receiver's `'message'` event receives one datagram, not an arbitrary fragment of several datagrams. The operating system may truncate oversized messages according to platform and buffer conditions, so the application should keep its format well below practical datagram limits and enforce its own small maximum.

Preserving message boundaries does not establish reliability. A protocol should assume:

```text
loss
duplication
reordering
delay
unexpected sender
malformed payload
```

even when localhost tests appear perfectly reliable.

## “Connected UDP” is an endpoint filter, not TCP

Node can connect a UDP socket to a default peer. This simplifies `send()` and usually filters received datagrams by peer. It does not create a handshake, ordered stream, retransmission, congestion control, or peer lifecycle.

Use the phrase **connected UDP socket** carefully. It describes local socket configuration, not a reliable connection protocol.

## Versioned bounded syntax

ServiceWire discovery uses a small UTF-8 text contract:

```text
SERVICEWIRE-DISCOVER-V1<TAB><nonce>
SERVICEWIRE-HERE-V1<TAB><nonce><TAB><base-url><TAB><version>
```

The nonce is 32 lowercase hexadecimal characters. The request contains no client-controlled payload beyond the nonce. The response is bounded and must not exceed a configured maximum.

Parsing should occur in layers:

1. reject a datagram above `maxDatagramBytes`;
2. decode UTF-8 strictly;
3. split exact fields;
4. validate protocol token;
5. validate nonce syntax;
6. validate URL and version;
7. apply peer policy;
8. correlate with the outstanding request.

A syntactically valid response with the wrong nonce is unrelated, not a protocol success.

## Request identity and entropy

A request ID must be unpredictable when spoofed responses matter. A sequential integer can be guessed. A random 128-bit nonce is sufficient for this teaching protocol:

```ts
import { randomBytes } from 'node:crypto';

export function createNonce(): string {
  return randomBytes(16).toString('hex');
}
```

The nonce identifies one discovery operation, not the service itself. It should not be used as an authorization credential.

## One deadline across retries

Retry does not reset the caller's budget. Define:

```text
deadline = now + totalBudget
attempt 1 immediately
attempt 2 after bounded delay if time remains
attempt 3 only if time remains
```

A retry schedule might be fixed or exponential with bounded jitter. For deterministic tests, inject the clock and delay function.

The receiver remains active across attempts. A late response to attempt one may legitimately complete the operation if it has the correct nonce and peer policy and arrives before the overall deadline. Attempts are transmission events; the nonce identifies the semantic operation.

## Correlation before acceptance

A listener may receive:

- a response for the current nonce;
- a response for an earlier completed operation;
- a request from another client;
- arbitrary local traffic;
- malformed bytes;
- a valid response from an unaccepted peer.

Only the first qualifying response settles the operation. Later duplicates must not settle again. Cleanup removes the message listener, retry timers, abort listener, and socket ownership.

A useful operation state:

```ts
type DiscoveryState =
  | { readonly kind: 'waiting'; readonly nonce: string; readonly attempts: number }
  | { readonly kind: 'succeeded'; readonly endpoint: URL }
  | { readonly kind: 'expired' }
  | { readonly kind: 'cancelled' }
  | { readonly kind: 'failed'; readonly cause: Error };
```

Implementation may use local mutable state, but the state transitions should be testable.

## Duplicate requests and replay caches

A responder may receive the same request several times because the client retries or the network duplicates it. For a pure discovery response, generating the same response again is safe. For a state-changing UDP protocol, duplicate suppression or idempotency becomes essential.

A bounded replay cache might index request ID to terminal response:

```text
key: peer identity + request ID
value: canonical response + expiry
```

It needs:

- maximum entry count;
- retention duration;
- eviction policy;
- same-ID/different-request conflict behavior;
- memory accounting.

The laboratory includes a replay cache even though ServiceWire discovery itself can recompute a small pure response. The exercise prepares you for message-driven systems in Course 7.

## Peer endpoint policy

The `rinfo` object identifies the observed source address and port. Decide what counts as an acceptable peer:

- exact configured address and port;
- any address returned by a trusted resolver;
- loopback only;
- one controlled subnet;
- any sender for a public discovery protocol.

Do not compare textual IP forms naïvely when IPv4-mapped IPv6 addresses or normalization matter. Keep the policy narrow for local discovery.

Even an accepted source address is not strong identity on an unauthenticated UDP network. Source addresses can be spoofed in some environments, and a local attacker can answer a broadcast or multicast request.

## Amplification risk

A tiny spoofed request that causes a large response can be used to reflect traffic toward a victim. Keep unauthenticated responses small and avoid returning peer-controlled bulk data.

A useful ratio:

```text
amplification = response bytes / request bytes
```

ServiceWire's response is short and contains only configured endpoint and version. The responder also applies a rate or concurrency policy if exposed beyond a tightly controlled local environment.

## Binding and broadcast

A UDP socket binds independently of TCP/HTTP listeners. Port zero is again useful in tests. Broadcast or multicast introduces additional platform and network-interface behavior; this course's implementation uses explicit host and port for deterministic local study.

If you design broadcast discovery as an independent extension, document:

- which interfaces participate;
- whether broadcast is enabled;
- response jitter to avoid bursts;
- authentication limits;
- rate limiting;
- advertised address selection.

## Worked case — loss, duplicate, and stale response

Timeline:

```text
0 ms   client sends nonce N
40 ms  responder reply is lost
100 ms client retransmits N
120 ms responder sends reply A
125 ms duplicated reply B is produced
130 ms A arrives and completes operation
145 ms B arrives
```

A correct client:

- records two attempts;
- accepts A because nonce and peer match and deadline remains;
- removes or disables completion after success;
- ignores B;
- closes the socket if it owns a per-operation socket;
- reports one endpoint.

A client that creates a new nonce for every retransmission could ignore a valid late response to the original operation and create multiple semantic requests. Retransmission normally retains semantic identity.

## Errors are not all terminal

Malformed or unrelated datagrams should often be ignored and counted rather than terminating discovery. A valid response with the correct nonce but invalid endpoint may be a protocol failure. A socket error or expired deadline is terminal.

The policy must prevent an attacker from terminating discovery merely by sending one malformed unrelated packet.

## Common wrong models

### “Datagram means delivered message”

It means the receiver observes a message boundary if a datagram arrives. Delivery is not guaranteed.

### “Retry creates a new request”

A retransmission commonly carries the same semantic request identity. New identity can duplicate effects.

### “The first response wins”

The first correctly correlated response under peer and format policy wins.

### “Discovery tells me who is authorized”

It reveals a responding endpoint under an unauthenticated convenience protocol.

### “Localhost tests prove no duplicates”

They prove only that one test schedule did not produce them.

## Decision procedure

1. Define the bounded wire format.
2. Choose semantic request identity.
3. State peer acceptance policy.
4. Define one total deadline.
5. Define attempt schedule and maximum.
6. Correlate before accepting.
7. Decide malformed-packet policy.
8. Decide duplicate and stale behavior.
9. Bound responder state and response size.
10. State authentication and amplification limits.

## ServiceWire increment

Add optional UDP discovery:

```text
SERVICEWIRE-DISCOVER-V1 <nonce>
SERVICEWIRE-HERE-V1 <nonce> <advertised-url> <version>
```

The discovery component owns its socket and closes during shutdown. It advertises the configured client URL, not the wildcard bind. The result is never treated as authorization.

## Case study — reliability built above an unreliable datagram

Suppose a client sends a status query over UDP. The request contains a random nonce, and the server echoes that nonce in its response. The client sends up to three attempts within one 300 ms deadline.

```text
attempt 1 request lost
attempt 2 reaches server; response lost
attempt 3 reaches server; response reaches client
```

The client sees one response. The server may have processed the request twice. Correlation proves that the response belongs to the operation; it does not prove that the operation executed once.

For a read-only status query, duplicate execution is harmless. For a command that mutates state, you need an idempotency design or a replay cache at the receiver. A bounded replay cache might map `(peer identity, nonce)` to a terminal response. Its contract must define:

- how peer identity is constructed;
- how long records remain valid;
- maximum records and bytes;
- behavior after eviction;
- whether a duplicate while the first request is still running attaches to the in-progress result;
- whether the response is byte-identical or semantically reconstructed.

Without those choices, “retry UDP” silently changes application semantics.

### Datagram conservation

For each received datagram, exactly one of these should happen:

```text
ignored as unrelated traffic
rejected as malformed
accepted as a new request
recognized as a duplicate and replayed
matched to one pending client operation
```

The categories must not overlap. A malformed datagram should not create a pending record. An unrelated response should not consume a retry budget. A duplicate response after the client operation has completed should be ignored without resurrecting state.

### Why source addresses are weak identity

UDP exposes source address and port. They are useful correlation evidence but weak authentication. NAT, port reuse, spoofing, local routing, and application proxies can all complicate the relationship between source tuple and principal identity. Service discovery in this course therefore treats UDP as a convenience mechanism. The advertised URL still undergoes ordinary URL validation, TLS verification where applicable, and application authorization.

### One deadline and bounded retransmission

A retry schedule must fit inside the caller’s deadline. For example:

```text
budget: 300 ms
attempt 1 at 0 ms
attempt 2 at 50 ms
attempt 3 at 150 ms
deadline at 300 ms
```

The third timer must not schedule a fourth attempt after the deadline. When the operation settles, both the deadline timer and retry timer must be cleared before the socket closes. The completion function should be idempotent because a response, socket error, deadline, and retry timer can race.

### Reasoning table

| Question | Required answer |
|---|---|
| What is the message boundary? | one UDP datagram |
| What identifies the logical operation? | validated nonce or request ID |
| What bounds waiting? | one monotonic operation deadline |
| What bounds network activity? | maximum attempts and datagram size |
| What proves single execution? | nothing, unless receiver-side idempotency is added |
| What proves authorization? | a separate authenticated application mechanism |

If the design cannot fill this table, it is not yet a protocol; it is only a packet format.

## Ready to continue

You are ready for HTTP when you can explain why message boundaries, reliability, correlation, identity, and authorization are five different concerns.

## Primary Node.js references

- [UDP/datagram sockets](https://nodejs.org/docs/latest-v24.x/api/dgram.html)
- [Crypto random bytes](https://nodejs.org/docs/latest-v24.x/api/crypto.html#cryptorandombytessize-callback)
- [Buffer](https://nodejs.org/docs/latest-v24.x/api/buffer.html)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-53-reliable-datagram-protocol/README.md)
- [ServiceWire engineering guide](../capstone.md)
