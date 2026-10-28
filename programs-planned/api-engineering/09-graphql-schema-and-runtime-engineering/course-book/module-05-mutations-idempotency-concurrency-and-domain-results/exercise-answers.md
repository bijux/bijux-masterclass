# Worked Answers — Module 05: Mutations, Idempotency, Concurrency, and Domain Results

Use these solutions to audit your reasoning for **Mutations, Idempotency, Concurrency, and Domain Results**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Does serial top-level mutation execution make two fields atomic?

No. It orders their execution but does not create one transaction or rollback earlier committed effects.

**Decisive evidence.** Execute a mutation containing two top-level fields and force the second to fail. Observe that serial ordering does not create one cross-service transaction or automatic rollback of the first effect.

The chapter’s decisive distinction is this: GraphQL serializes top-level mutation fields in the selected operation. That guarantee prevents two sibling mutation fields from executing concurrently within one request. It does not make them atomic. If the first field commits and the second fails, the first effect remains unless the domain exposes an explicit compensation workflow.

## 2. Why use one input object per mutation?

It gives a stable namespace for idempotency, expected version, client correlation, and future optional inputs.

**Decisive evidence.** Diff two schema releases while adding optional mutation parameters. A single input object localizes evolution, supports `clientMutationId`, and gives one coercion boundary.

In the cumulative capstone, the rule becomes concrete: Mutations accept one named input object. This gives the operation room for idempotency keys, expected versions, client mutation identifiers, and future optional fields. The result is a typed union of success and domain problem objects. The transport-level errors array remains for request and unexpected execution failures.

## 3. Where should an idempotency record live?

With the service that owns the command transaction. A gateway-only record can diverge from committed business state.

**Decisive evidence.** Replay after gateway restart or against another gateway instance. The same source-owned record must return the original outcome; a gateway-local record fails this proof.

A useful way to reason about the boundary is: Course 2 made Analysis Control the owner of idempotent run submission. The graph mutation forwards the client's idempotency key and the semantic input. It must not generate a new key on retry, store a gateway-only replay record, or treat a repeated network response as a new command.

## 4. What happens when a client retries with the same key and same input?

The owner returns the original logical result and the graph marks it replayed rather than creating another run.

**Decisive evidence.** Send the identical key and canonical input twice. The second result must mark replay, return the same logical object, and create no additional source effect.

The implementation consequence is: A client loses the first StartAnalysis response and repeats the operation with the same idempotency key. The gateway forwards the same key and input. Analysis Control returns the original run with replayed: true. Changing the algorithm under that key returns a typed conflict rather than a second run.

## 5. What happens when the same key carries changed input?

The mutation returns a typed conflict because the key is already bound to another semantic request.

**Decisive evidence.** Reuse the key with one changed semantic input. The owner must return a typed conflict and leave the first command binding unchanged.

The important nuance is: clientMutationId is an echo for client correlation. It is not the idempotency key. An idempotency key is bound to authenticated principal, operation, and normalized semantic input at the source service. Reusing a key with different input is a conflict. Generating a new key in the graph gateway on each attempt destroys retry safety.

## 6. Why is expectedVersion checked in Analysis Control?

Only the owner can compare and mutate atomically against current state. A gateway pre-check has a race.

**Decisive evidence.** Race two cancellations against the same run version. Analysis Control must atomically accept at most one, because it owns both current state and the version comparison.

Under concurrency or failure, the distinction becomes: Cancellation includes expectedVersion. The graph decodes the global run ID and delegates compare-and-swap to Analysis Control. Reading version 4 and later sending a mutation does not authorize the gateway to assume version 4 is current. Only the owning service can check and mutate atomically.

## 7. Distinguish CONFLICT from PRECONDITION_FAILED.

Conflict means the command is incompatible with current domain state; precondition failure means the supplied version is stale.

**Decisive evidence.** Exercise a terminal-state conflict and a stale expected version. Clients must receive distinct stable codes because the recovery action differs.

The design remains honest only if: Expected business outcomes belong in the schema when clients are expected to branch on them. The capstone mutation unions contain success objects and MutationProblem with stable codes such as CONFLICT and PRECONDITION FAILED.

## 8. When should a domain problem be in data rather than errors?

When it is an expected client-actionable outcome such as validation, conflict, or stale version.

**Decisive evidence.** Return a typed union member for expected business rejection that callers can branch on. Reserve GraphQL execution errors for inability to execute or complete the field.

The consumer-facing consequence is: GraphQL specifies that top-level mutation fields execute serially. It does not create a cross-field database transaction, a distributed saga, or automatic rollback. Each mutation field delegates one business command to its owning service and receives the committed outcome.

## 9. What belongs in the GraphQL errors array for a mutation?

Request failures, authorization execution failures, downstream unavailability, or unexpected internal errors—not every domain rejection.

**Decisive evidence.** Inject resolver failure, authorization failure, malformed input, and expected domain conflict. Only the first three categories that prevent or break execution belong in `errors`; the domain conflict stays in mutation data.

The operational consequence is: If “create project and start its first analysis” must be atomic as a domain concept, Analysis Control should own a command that implements that invariant. The graph should not orchestrate two service calls and call the result a transaction.

## 10. Why preserve clientMutationId?

It lets a client correlate local action and response, especially when several mutations are in flight; it is not the idempotency key.

**Decisive evidence.** Replay a mutation after response loss and compare client state. The echoed identifier must let the client correlate the response without becoming the durable idempotency key.

The strongest engineering interpretation is: Top-level mutation serialization protects ordering within one operation, but a lost HTTP response can still cause a client retry. Idempotency remains required. Client libraries should retry only operations with explicit policy and stable keys; a generic “retry all mutations” interceptor is unsafe.

## 11. Can the gateway retry startAnalysis automatically?

Only under the source retry policy and with the same stable idempotency key and remaining deadline.

**Decisive evidence.** Allow automatic retry only when the operation is registered as idempotent, the same key and input are preserved, and remaining deadline/retry budget permits it. Otherwise the gateway must not guess.

The defect-oriented view is: The gateway does not cache a successful response as the authority. It may cache transport-independent metadata for efficiency only if the source remains authoritative and error semantics are preserved. If the first response is lost after the source commits, a retry must still obtain the committed run.

## 12. Why avoid a generic updateRun mutation?

It exposes an anemic patch surface, weakens invariant ownership, and makes authorization and compatibility harder than explicit commands.

**Decisive evidence.** Review the source state machine. Expose named commands such as cancel or start rather than a generic patch that lets clients request illegal or owner-ambiguous transitions.

Across the Python and TypeScript tracks, the invariant is: Input fields can require policy too. A support operator may be allowed to cancel a run only with an audited reason. A client may be allowed to choose an algorithm from a tenant-specific allowlist. Schema validity alone cannot express these rules.
