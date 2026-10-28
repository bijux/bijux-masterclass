# Checkpoint 05 — Mutations, Idempotency, Concurrency, and Domain Results

Do not continue until every condition is supported by executable or inspected evidence.

- [ ] Every mutation delegates the authoritative command to its owning service and stores no gateway business state.
- [ ] Idempotency keys and request fingerprints survive retries at the source-service boundary.
- [ ] Reusing a key with different input returns a typed conflict rather than another effect.
- [ ] Expected-version checks reject stale cancellation without changing run state.
- [ ] Mutation success and problem union members remain machine-distinguishable and preserve clientMutationId.
- [ ] Lab 05 proves one logical effect under replay, conflict on changed input, and no hidden graph-only deduplication table.

**Gate:** run `make module-05-proof`. A green command without the lab report and the listed evidence does not count.
