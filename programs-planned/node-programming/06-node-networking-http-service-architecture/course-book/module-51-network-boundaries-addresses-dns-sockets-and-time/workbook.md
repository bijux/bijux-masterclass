# Module 51 Workbook — Network Boundaries, Addresses, DNS, Sockets, and Time

Write predictions before running code.

## 1. Predict

1. A server listens on `{ host: "0.0.0.0", port: 0 }`. Which values are known before `listening`, and which become known only afterward?
2. A URL contains `https://[::1]:8443/v1/jobs`. Identify scheme, hostname, port, path, and candidate address.
3. A resolver returns IPv6 then IPv4. The first attempt uses 700 ms of an 800 ms deadline. How much budget may the second attempt receive?
4. `socket.setTimeout(500)` fires. Has Node destroyed the socket? Has the product operation necessarily exceeded its overall deadline?
5. A certificate names `service.test`, while the connector selected `127.0.0.1`. Which identity should HTTPS verify when the logical URL is `https://service.test`?

## 2. Diagnose and repair

### Free-port race

A test opens a temporary server, reads its port, closes it, and then starts the real server on that port. Explain the race and replace it with a port-zero design.

### Reset deadline

A connector gives every address candidate the caller's full timeout. Repair the algorithm while retaining per-candidate error evidence.

### Wildcard advertisement

A server prints `http://0.0.0.0:PORT` as the URL clients should use. Separate bound and advertised endpoints.

### Lost hostname

A client resolves a host, replaces the URL hostname with the IP, and later disables TLS verification. Restore the logical identity without deleting deterministic local addressing.

## 3. Focused construction

1. Implement `parseServiceEndpoint(input: string)`.
2. Reject unsupported schemes, credentials, fragments, and invalid ports.
3. Implement `Deadline` using a monotonic clock.
4. Define an injected `Resolver`.
5. Implement `listenEphemeral()` and report the actual port.
6. Implement a sequential candidate planner that never exceeds one deadline.
7. Record bounded causal failure information for each candidate.

## 4. Independent laboratory

Build the [Address Resolution Observatory](../../labs/module-51-address-resolution-observatory/README.md).

Before coding, submit:

- the endpoint ledger;
- the connection-attempt state machine;
- the deadline algorithm;
- the cleanup owner;
- tests for mixed address families, empty resolution, timeout, cancellation, and successful fallback.

## 5. ServiceWire transfer

Add endpoint and deadline types to ServiceWire. Keep logical host, bound endpoint, and advertised URL distinct. The server must bind to port zero in tests and publish the actual port only after successful startup.

## 6. Independent transfer

Design a client for a service-discovery result that provides several endpoints. State which facts are trusted, which are merely candidates, how TLS identity is preserved, and how one deadline covers discovery and connection.

## 7. Closed-book defense

1. Why is a hostname not an address candidate?
2. Why is `0.0.0.0` not usually an advertised client host?
3. What does port zero solve?
4. Why must every losing connection attempt be observed?
5. Which clock is appropriate for deadlines, and why?

## 8. Architecture trace — one logical endpoint, three failed candidates

A resolver returns `::1`, `127.0.0.2`, and `127.0.0.1`. The first times out, the second refuses, and the third succeeds. The total budget is 250 ms.

Produce a table with one row per phase and columns for: logical hostname, candidate, phase start, remaining budget, terminal evidence, cleanup action, and retry decision. Then answer:

1. Which failures may be aggregated without losing causality?
2. At what point does the successful socket become the sole returned owner?
3. Which listeners and timers still exist after settlement?
4. How would a staggered two-candidate strategy change the cleanup proof?
5. Which value is passed to TLS as `servername`?

## 9. Boundary reconstruction

Write a small connector interface that accepts an injected resolver and connector function. It must not expose raw DNS callbacks to callers. Define the success and aggregate-failure result types before writing implementation code. Add tests for empty resolution, cancellation during the first attempt, and a late losing-socket error.

## 10. Failure-evidence design

Define an aggregate `ConnectFailure` that can represent: resolver returned no candidates, every candidate failed, the caller cancelled, and the overall deadline expired. For the “every candidate failed” case, retain a bounded ordered list containing address, family, phase, error code, and elapsed time. Explain why the aggregate should not expose live socket objects or raw callback errors.

Now decide what the caller may safely retry. Distinguish configuration failure, candidate-local transport failure, identity-verification failure, and caller cancellation. Write the retry function as a pure decision over evidence; do not embed it inside socket callbacks.
