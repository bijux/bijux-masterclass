# Course 6 Learning Outcomes

The outcomes are phrased as observable work. “Understand HTTP” is not an outcome because it does not say what evidence would distinguish understanding from familiarity.

## Network boundary outcomes

By the end of Module 51, you can:

1. distinguish a logical service URL, a hostname, a DNS answer, a socket address, a bound local address, and a peer address;
2. explain why address resolution can produce several candidates and why connection policy must define order, fallback, and one overall time budget;
3. model connect, idle, operation, and shutdown time separately;
4. expose actual ephemeral listening addresses instead of guessing ports;
5. test address-family and resolution policy through injected resolution.

## Transport outcomes

By the end of Modules 52 and 53, you can:

6. reconstruct application messages from an arbitrary TCP byte stream using bounded framing;
7. model open, readable, writable, half-closed, errored, and closed connection states;
8. distinguish write acceptance from peer receipt and application commit;
9. define UDP message identity, correlation, retry, duplicate handling, and stale-response rejection;
10. explain which reliability properties an application adds above UDP and which it still cannot create.

## HTTP server outcomes

By the end of Modules 54 and 55, you can:

11. derive method, target, header, body, and response rules from an HTTP application contract;
12. treat header normalization and raw header evidence as different surfaces;
13. bound request bodies incrementally and reject unsupported transfer or media assumptions deliberately;
14. distinguish safe, idempotent, cacheable, conditional, and retriable operations;
15. build a typed route boundary that converts network input into validated application commands;
16. render stable problem details without exposing internal stack traces;
17. design idempotency records that detect same-key/different-request conflicts;
18. use entity tags and preconditions as representation-version contracts.

## HTTP client outcomes

By the end of Module 56, you can:

19. own an HTTP agent, request, response body, redirects, cancellation listeners, and retry timers as one client operation;
20. apply one absolute deadline across resolution, connection, response headers, body consumption, and retries;
21. distinguish a timeout before commit from a timeout after ambiguous commit;
22. enforce response-body limits before unbounded retention;
23. define redirect policy that revalidates origin, method, credentials, and loop limits;
24. retry only operations whose semantic and temporal policy permits another attempt.

## Secure and multiplexed transport outcomes

By the end of Modules 57 and 58, you can:

25. distinguish encryption, chain trust, hostname verification, application authorization, SNI, and ALPN;
26. diagnose certificate failures without disabling verification;
27. state what local teaching certificates do and do not prove;
28. model an HTTP/2 session separately from its concurrent streams;
29. account independently for session capacity, stream capacity, body limits, and flow control;
30. handle stream reset, session error, graceful GOAWAY, and forced session destruction.

## Long-lived delivery and service lifecycle outcomes

By the end of Modules 59 and 60, you can:

31. implement a replayable SSE stream with event identifiers, bounded history, replay-gap policy, heartbeats, and slow-subscriber limits;
32. distinguish connection liveness from event freshness;
33. define listener admission, request admission, application admission, and downstream capacity separately;
34. expose health, readiness, and overload without pretending they are the same state;
35. implement startup rollback;
36. stop acceptance before draining accepted work;
37. apply one grace deadline, then abort remaining network work and join owned tasks;
38. produce an authoritative terminal report after shutdown.

## Final product outcomes

After completing ServiceWire and the independent cancellation extension, you can:

39. maintain one coherent contract across HTTP/1.1, HTTPS, HTTP/2, SSE, UDP discovery, and a supported client;
40. defend every queue, bound, identity, retry, and terminal state in the architecture;
41. add a cross-layer protocol feature without allowing route, validation, idempotency, conditional requests, events, clients, and shutdown behavior to diverge;
42. state honestly which guarantees remain process-local and which require durable or distributed mechanisms reserved for later courses.
