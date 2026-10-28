# Instructor notes

The course book is authoritative. Do not replace its progression with a framework-first lecture.

## Teaching discipline

- Require an interaction decision before allowing a new service or method.
- Ask which state is authoritative after every injected failure.
- Treat field numbers, enum numbers, package names, and method shapes as release assets.
- Keep HTTP, events, local calls, and gRPC responsibilities visible.
- Let learners choose one primary language track; use the second for invariant comparison.
- Reject demos that lack deadline, retry, resource, or rollback evidence.
- Never present an unavailable external tool as a passed proof.

## Common misconceptions

1. gRPC implies microservices.
2. Generated stubs make remote calls local.
3. Binary compatibility means safe release.
4. HTTP/2 flow control bounds application memory.
5. Cancellation rolls back a committed transaction.
6. `UNAVAILABLE` makes every call retryable.
7. A private network authenticates a peer.
8. A healthy channel proves a healthy application.
9. Reflection is the source of truth.
10. Faster internal transport permits public semantic drift.
