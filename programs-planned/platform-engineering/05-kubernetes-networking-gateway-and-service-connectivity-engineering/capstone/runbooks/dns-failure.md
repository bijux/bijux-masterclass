# Runbook — Kubernetes DNS failure

1. Capture the exact application name, record type, search list, and `ndots` value.
2. Query the absolute name for A and AAAA over UDP and TCP.
3. Record response code, TTL, server, and cache layer.
4. Compare normal or headless answers with Service and EndpointSlice state.
5. Prove NetworkPolicy access to the actual DNS endpoints.
6. Do not restart CoreDNS until authoritative, cache, transport, and client evidence are preserved.
7. After repair, verify both fresh and previously cached clients.
