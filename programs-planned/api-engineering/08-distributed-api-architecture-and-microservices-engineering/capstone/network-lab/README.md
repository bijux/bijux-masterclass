# Multi-process network laboratory

This laboratory runs five independent Python processes using only the standard library plus the Course 8 reference model:

- Edge Gateway;
- Analysis Control;
- Artifact Service;
- Notification Service;
- Worker Plane.

It demonstrates real loopback TCP calls, audience-bound delegated authority, one owner per effect, notification idempotency, gateway composition, and an explicit partial response after Artifact Service is terminated. The tour driver performs one bounded broker-relay step: it forwards the committed completion event under an Analysis Control service credential. This keeps notification outside the completion transaction without pretending that the standard-library lab is a message broker.

It is **mechanism evidence**, not a production topology. State is intentionally in memory so the experiment remains fast and deterministic; the service-owned PostgreSQL migration trees define the durable production-shaped boundary.

Run from the course root:

```bash
make network-lab-proof
```

## Deliberate simplifications

- The worker returns the committed artifact identity to Analysis Control over a request path instead of operating a real ArtifactStored broker consumer. The event-driven contract, outbox/inbox behavior, and replay guarantees are inherited from Course 6 and exercised by the semantic saga vectors.
- The tour driver performs the completion-event relay to Notification Service. It does not claim to implement broker retention, redelivery, or partitioning.
- HMAC request tokens make hop-by-hop identity and audience checks visible. They do not replace an operated workload-identity and mTLS system.
- State is in memory. Restart durability belongs to the owner-local PostgreSQL laboratory.

These simplifications reduce infrastructure while keeping the distributed decisions under study observable. The course never presents them as equivalent to the production-shaped topology.
