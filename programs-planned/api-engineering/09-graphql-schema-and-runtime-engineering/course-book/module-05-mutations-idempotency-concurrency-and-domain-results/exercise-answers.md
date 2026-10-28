# Worked answers — Mutations, Idempotency, Concurrency, and Domain Results

Compare the decision rule and evidence, not just wording.

## 1. Does serial top-level mutation execution make two fields atomic?

No. It orders their execution but does not create one transaction or rollback earlier committed effects.

**Decisive evidence.** Execute a mutation containing two top-level fields and force the second to fail. Observe that serial ordering does not create one cross-service transaction or automatic rollback of the first effect.

## 2. Why use one input object per mutation?

It gives a stable namespace for idempotency, expected version, client correlation, and future optional inputs.

**Decisive evidence.** Diff two schema releases while adding optional mutation parameters. A single input object localizes evolution, supports `clientMutationId`, and gives one coercion boundary.

## 3. Where should an idempotency record live?

With the service that owns the command transaction. A gateway-only record can diverge from committed business state.

**Decisive evidence.** Replay after gateway restart or against another gateway instance. The same source-owned record must return the original outcome; a gateway-local record fails this proof.

## 4. What happens when a client retries with the same key and same input?

The owner returns the original logical result and the graph marks it replayed rather than creating another run.

**Decisive evidence.** Send the identical key and canonical input twice. The second result must mark replay, return the same logical object, and create no additional source effect.

## 5. What happens when the same key carries changed input?

The mutation returns a typed conflict because the key is already bound to another semantic request.

**Decisive evidence.** Reuse the key with one changed semantic input. The owner must return a typed conflict and leave the first command binding unchanged.

## 6. Why is expectedVersion checked in Analysis Control?

Only the owner can compare and mutate atomically against current state. A gateway pre-check has a race.

**Decisive evidence.** Race two cancellations against the same run version. Analysis Control must atomically accept at most one, because it owns both current state and the version comparison.

## 7. Distinguish CONFLICT from PRECONDITION_FAILED.

Conflict means the command is incompatible with current domain state; precondition failure means the supplied version is stale.

**Decisive evidence.** Exercise a terminal-state conflict and a stale expected version. Clients must receive distinct stable codes because the recovery action differs.

## 8. When should a domain problem be in data rather than errors?

When it is an expected client-actionable outcome such as validation, conflict, or stale version.

**Decisive evidence.** Return a typed union member for expected business rejection that callers can branch on. Reserve GraphQL execution errors for inability to execute or complete the field.

## 9. What belongs in the GraphQL errors array for a mutation?

Request failures, authorization execution failures, downstream unavailability, or unexpected internal errors—not every domain rejection.

**Decisive evidence.** Inject resolver failure, authorization failure, malformed input, and expected domain conflict. Only the first three categories that prevent or break execution belong in `errors`; the domain conflict stays in mutation data.

## 10. Why preserve clientMutationId?

It lets a client correlate local action and response, especially when several mutations are in flight; it is not the idempotency key.

**Decisive evidence.** Replay a mutation after response loss and compare client state. The echoed identifier must let the client correlate the response without becoming the durable idempotency key.

## 11. Can the gateway retry startAnalysis automatically?

Only under the source retry policy and with the same stable idempotency key and remaining deadline.

**Decisive evidence.** Allow automatic retry only when the operation is registered as idempotent, the same key and input are preserved, and remaining deadline/retry budget permits it. Otherwise the gateway must not guess.

## 12. Why avoid a generic updateRun mutation?

It exposes an anemic patch surface, weakens invariant ownership, and makes authorization and compatibility harder than explicit commands.

**Decisive evidence.** Review the source state machine. Expose named commands such as cancel or start rather than a generic patch that lets clients request illegal or owner-ambiguous transitions.
