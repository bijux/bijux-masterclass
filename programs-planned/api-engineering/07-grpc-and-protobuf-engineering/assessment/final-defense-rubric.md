# Final defense rubric

The final defense is scored out of 100. A total score cannot compensate for a failed non-compensable gate.

| Area | Points |
|---|---:|
| Boundary and ownership judgment | 15 |
| Protobuf model and compatibility | 15 |
| Unary outcomes, deadlines, retries, and idempotency | 15 |
| Streaming, flow control, and worker fencing | 15 |
| Security and tenant isolation | 10 |
| Lifecycle, health, generation, and governance | 10 |
| Cross-protocol release and rollback | 15 |
| Evidence quality and explanation | 5 |

## Non-compensable gates

The learner must demonstrate:

1. no reused field or enum number;
2. exact 64-bit meaning in the supported TypeScript path;
3. one absolute deadline and durable idempotency for mutation retry;
4. bounded stream queues, message size, total bytes, and lifetime;
5. stale worker completion rejection;
6. tenant-aware authorization at the authoritative state boundary;
7. graceful drain and reconnection;
8. deterministic generation/descriptor evidence;
9. unchanged public HTTP and durable event semantics;
10. rollback without duplicate durable effects.
