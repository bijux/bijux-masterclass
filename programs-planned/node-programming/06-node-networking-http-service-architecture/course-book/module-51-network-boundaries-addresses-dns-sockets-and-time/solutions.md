# Module 51 Solutions — Network Boundaries, Addresses, DNS, Sockets, and Time

## Prediction reasoning

1. Before listening, the intent is wildcard host and ephemeral port selection. After the `listening` event, `server.address()` supplies the actual selected port and concrete address representation. Reporting a guessed port before that event is unsupported.
2. The scheme is HTTPS; the hostname is `::1` without brackets in the parsed URL API; the explicit port is 8443; the path is `/v1/jobs`; `::1` is already an IPv6 literal rather than a DNS name.
3. At most the remaining 100 ms, minus elapsed bookkeeping. The overall deadline is authoritative.
4. The timeout event reports inactivity under the socket's timeout configuration. It does not automatically destroy the socket. The product deadline may be shorter, longer, or already expired; the application must decide the terminal action.
5. Verify `service.test`. The IP is the transport destination; the hostname is the intended TLS identity. Local tests can route that host to a local address while preserving certificate verification.

## Repair reasoning

### Free-port race

The period between closing the probe server and binding the real server permits another process or test to claim the port. Bind the actual server directly to port zero, wait for `listening`, then read the selected port. The resource remains owned continuously.

### Reset deadline

Create one deadline before resolution. Before each attempt, compute remaining time. Stop when no budget remains. Candidate-specific timers may use the remaining duration or a stricter cap. On failure, record candidate, family, elapsed time, and bounded error classification. On success, destroy every losing attempt and remove listeners.

### Wildcard advertisement

Store:

```ts
interface BoundEndpoint {
  readonly address: string;
  readonly port: number;
  readonly family: string;
}

interface AdvertisedEndpoint {
  readonly url: URL;
}
```

The bound endpoint describes acceptance. The advertised endpoint is configured or derived under an explicit local policy such as `localhost` in tests.

### Lost hostname

Keep the original URL. Inject resolution or a custom connector that dials the selected IP while passing the original hostname to TLS as `servername` and to HTTP as the authority. Trust a local test CA instead of disabling verification.

## Focused construction notes

A good parser accepts only the schemes the product supports and rejects surprising features early. For a service endpoint, embedded credentials and fragments normally have no role. Normalize the default port explicitly so later code does not repeatedly infer it.

The deadline object should be immutable. Expose `remainingMs()` rather than a mutable countdown. Tests can inject a clock:

```ts
export interface Clock {
  nowMs(): number;
}
```

A deterministic fake clock makes timeout logic testable without sleep.

A sequential connection planner should return a structured exhausted-candidates error. It must not retain unbounded system error text. Preserve stable code, candidate, and perhaps a bounded message.

## Laboratory design

The observatory should not require external DNS. Use an injected resolver and a connector abstraction. One test returns:

```text
IPv6 candidate -> refused
IPv4 candidate -> connected
```

and proves the selected candidate and remaining budget. Another advances the fake clock so the first attempt exhausts the deadline; the second attempt must never begin.

Cancellation should close the current attempt and produce one terminal result. Repeated cancellation must be harmless.

## ServiceWire transfer

ServiceWire's runtime report should expose both:

```text
bound: 127.0.0.1:39117
advertised: http://127.0.0.1:39117
```

In a wildcard production bind, those values can differ. Tests should assert actual port acquisition rather than depend on a fixed port.

## Independent transfer

Discovery results are candidates, not trusted authorization. Preserve the service identity from configuration or a signed discovery contract. One deadline should cover discovery, candidate selection, transport establishment, and any required handshake. All losing transports must close.

## Defense summary

The module's core distinction is authority. Configuration owns logical identity. Resolution owns temporary candidates. The socket owns observed local and peer endpoints. The product owns the advertised endpoint and overall time promise. Bugs arise when one layer's value is silently promoted into another layer's authority.

## Architecture trace solution

The logical hostname remains constant across all rows. Each candidate row records its own address, family, elapsed time, and terminal evidence. A timeout or refusal can be aggregated into a bounded final failure, but the original rows must remain available so the caller can distinguish “no candidates” from “all candidates failed.”

The successful socket becomes the sole returned owner only after the completion function marks the operation settled and initiates cleanup of every loser. Settlement before loser cleanup is acceptable only when the connector still owns and observes the cleanup promises; silently abandoning them is not.

After settlement, no candidate timeout, operation deadline timer, abort listener, or losing-socket callback may remain attached. In a staggered design, several attempts can be live simultaneously, so the proof additionally needs a collection of active attempt owners and a rule that destroys all but the winner.

TLS receives the original logical hostname as `servername`, even when the socket connected to an IP candidate.

A principled connector result contains the socket plus selected-candidate evidence. Aggregate failure contains a bounded ordered list of attempts. It does not expose half-initialized sockets or raw resolver callback state.

## Failure-evidence solution

The aggregate should be a discriminated union. Cancellation and deadline are first-class terminal causes; empty resolution is distinct from failed attempts. Candidate failures retain normalized codes and phases, not live resources. Retry policy then becomes testable: malformed configuration and caller cancellation do not retry; candidate-local refusal may; identity failure normally does not unless a reviewed multi-identity policy exists. Separating evidence from policy prevents low-level callback order from deciding product behavior.
