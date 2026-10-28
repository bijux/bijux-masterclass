# Case 3 — The negative DNS cache

## Incident

A worker starts before the `atlas-api` Service is created. Its first lookup returns NXDOMAIN. Five seconds later the Service and EndpointSlices exist, and `dig` from a fresh diagnostic Pod returns the expected address. The worker continues to report “host not found” for several minutes.

## Initial wrong hypothesis

Because CoreDNS answers correctly from the diagnostic Pod, the team concludes the worker’s network namespace is broken and restarts the Pod. The restart works, but it also replaces the process and all local resolver state.

## Investigation

The team reconstructs the exact query path. The worker uses a runtime-level DNS cache with a negative TTL longer than CoreDNS’s current cache. Its first query was:

```text
atlas-api.atlas-system.svc.cluster.local A
→ NXDOMAIN
```

That answer was retained in-process. The later `dig` command bypassed the application cache and therefore observed the new authoritative state. Packet capture during a repeated application request shows no DNS packet at all; the negative answer is served locally.

A second complication appears: the application originally used the short name `atlas-api`, generating several search candidates. One candidate has its own negative cache entry. Tests using the absolute FQDN and the short name therefore differ.

## Repair

The immediate recovery expires or clears the bounded application cache through its supported interface rather than restarting the entire Pod. The application is changed to expose cache statistics and to use a suitable negative TTL. Startup ordering is not treated as a guarantee that DNS state will always exist before every client.

## Durable change

The DNS laboratory now records:

- exact question and record type;
- search expansion;
- cache layer;
- response code and TTL;
- whether a network query occurred;
- time when the Service appeared;
- time when each cache accepted the new state.

The worker retry policy uses bounded backoff and does not flood CoreDNS after expiry.

## Lesson

“DNS works now” does not describe what a specific process believes. Negative answers are state. A restart can hide the cache owner and turn an unexplained workaround into folklore. Diagnose the exact question and every cache layer.
