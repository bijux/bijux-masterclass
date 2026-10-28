# Laboratory 1 — Address Resolution Observatory

**Module 51**

## Product

Build an address-resolution and connection-planning observatory. It parses a service endpoint, accepts an injected resolver, evaluates candidate addresses under one deadline, and records which candidate was selected or why the candidate set was exhausted. The laboratory does not make public Internet requests; every resolver and connector behavior is controlled by the test.

## Governing question

> How can a client preserve logical service identity while testing address selection, fallback, and one end-to-end deadline deterministically?

## Public surface

- `parseEndpoint(text)` returns a validated logical endpoint.
- `planConnection(endpoint, resolver, connector, options)` returns one selected candidate and bounded attempt records.
- `listenEphemeral(host)` starts a real local listener and reports the actual bound endpoint.
- `Deadline` exposes remaining monotonic time without mutable countdown state.

## Required invariants

- The logical hostname is never replaced by a candidate address.
- All resolution and connection work shares one absolute deadline.
- At most one candidate result wins; every losing attempt closes.
- Port zero is observed only after listening succeeds.
- Candidate failure records are bounded and contain no secrets.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Parse schemes, hostnames, IPv6 literals, and explicit/default ports.
2. Introduce the injected resolver and candidate family types.
3. Add a fake monotonic clock and deadline.
4. Implement deterministic sequential fallback.
5. Start a local server on port zero and observe its actual endpoint.
6. Add cancellation and prove cleanup.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- empty resolver result
- mixed IPv4 and IPv6 candidates
- first candidate refused, second succeeds
- deadline exhausted before fallback
- cancellation during connection
- wildcard bind versus advertised URL
- invalid URL credentials or fragment

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- using public DNS in tests
- resetting the full timeout for each candidate
- advertising `0.0.0.0` as a client URL
- replacing the logical hostname with the selected IP
- probing a free port and reopening it

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. candidate trace showing remaining budget
2. test proving second attempt never begins after expiry
3. actual port-zero listener test
4. cancellation test with no open socket
5. explanation of logical, bound, peer, and advertised endpoint

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Adapt the observatory to a service-discovery response containing three candidate URLs. Preserve the configured TLS identity, define candidate order, and show how discovery and connection consume one shared deadline.

The transfer is not complete when only type names change. Reconstruct the protocol, state, capacity, time, and terminal ledgers for the new domain.

## Using the starter

The starter compiles and exposes the domain vocabulary, configuration validation, and one baseline test. It does not implement the difficult mechanism. Extend it without weakening strict TypeScript settings.

Run:

```bash
npm run typecheck
npm test
```

## Comparing with the reference

Open `reference/` only after your normal and adversarial tests pass. Compare:

1. state representation;
2. bound enforcement point;
3. cleanup ownership;
4. failure classification;
5. test evidence.

Adopt a reference difference only when it proves an invariant your design misses or makes the same contract materially easier to inspect.
