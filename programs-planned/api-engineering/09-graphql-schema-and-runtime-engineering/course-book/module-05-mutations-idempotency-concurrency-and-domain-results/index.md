# Mutations, Idempotency, Concurrency, and Domain Results

**Module 05 of 10**

> **Governing question:** How do graph mutations preserve the durable command guarantees of the owning service?

## Place in the program

Courses 1–8 established the contract, durable implementation, security, operations, performance, asynchronous events, typed RPC, and distributed ownership. Module 05 applies those guarantees to the graph interface; none are reset at the GraphQL boundary.

## Learning outcomes

- distinguish mutation serialization from transactionality

- design input and payload types

- preserve source idempotency

- delegate optimistic concurrency

- model domain results separately from execution errors

## Capstone result

Expose idempotent create/start/cancel mutations over owning services.

## A mutation field is not the transaction

GraphQL specifies that top-level mutation fields execute serially. It does not create a cross-field database transaction, a distributed saga, or automatic rollback. Each mutation field delegates one business command to its owning service and receives the committed outcome.

Clients should not submit unrelated state changes in one operation expecting all-or-nothing behavior. If atomicity is a domain requirement, the owning service exposes one command that owns that transaction or workflow.

## Input and payload design

Mutations accept one named input object. This gives the operation room for idempotency keys, expected versions, client mutation identifiers, and future optional fields. The result is a typed union of success and domain problem objects. The transport-level `errors` array remains for request and unexpected execution failures.

A client-correctable conflict is data, not an exception. `MutationProblem` includes a stable code and optional field. Internal stack traces never become problem messages.

## Preserve idempotency authority

Course 2 made Analysis Control the owner of idempotent run submission. The graph mutation forwards the client's idempotency key and the semantic input. It must not generate a new key on retry, store a gateway-only replay record, or treat a repeated network response as a new command.

The success payload includes `replayed` so tests and clients can observe the source-service decision. Reusing a key with changed input returns a typed conflict.

## Optimistic concurrency stays source-local

Cancellation includes `expectedVersion`. The graph decodes the global run ID and delegates compare-and-swap to Analysis Control. Reading version 4 and later sending a mutation does not authorize the gateway to assume version 4 is current. Only the owning service can check and mutate atomically.

A stale version produces `PRECONDITION_FAILED`; a terminal state produces `CONFLICT`. Keeping these distinct lets clients decide whether to refetch or stop.

## Serial execution and client retries

Top-level mutation serialization protects ordering within one operation, but a lost HTTP response can still cause a client retry. Idempotency remains required. Client libraries should retry only operations with explicit policy and stable keys; a generic “retry all mutations” interceptor is unsafe.

The graph response may include a successful committed mutation alongside an execution error in a later top-level mutation. This is another reason not to imply transaction semantics from one GraphQL document.

## Mutation execution does not create a distributed transaction

GraphQL serializes top-level mutation fields in the selected operation. That guarantee prevents two sibling mutation fields from executing concurrently within one request. It does not make them atomic. If the first field commits and the second fails, the first effect remains unless the domain exposes an explicit compensation workflow.

This has three design consequences:

- one business atomicity boundary should usually be one source-owned command field;
- clients must not group unrelated mutations and assume rollback;
- mutation payloads and documentation must make committed outcomes observable.

If “create project and start its first analysis” must be atomic as a domain concept, Analysis Control should own a command that implements that invariant. The graph should not orchestrate two service calls and call the result a transaction.

## Input envelopes and evolution

A mutation accepts one input object because that object is a versionable command envelope. It can contain:

- client mutation correlation;
- idempotency key;
- expected version;
- command parameters;
- optional future fields.

This pattern avoids a long argument list whose independent additions are harder for clients to manage. It also lets the server validate relationships among values. The input object is still a public contract; do not pass an internal command DTO through without review.

`clientMutationId` is an echo for client correlation. It is not the idempotency key. An idempotency key is bound to authenticated principal, operation, and normalized semantic input at the source service. Reusing a key with different input is a conflict. Generating a new key in the graph gateway on each attempt destroys retry safety.

## Typed domain outcomes versus execution errors

Expected business outcomes belong in the schema when clients are expected to branch on them. The capstone mutation unions contain success objects and `MutationProblem` with stable codes such as `CONFLICT` and `PRECONDITION_FAILED`.

Use a typed result for:

- validation that depends on current domain state;
- an idempotency-key/input mismatch;
- a stale expected version;
- an illegal state transition;
- a command target that is deliberately concealed as not found.

Use a GraphQL execution error for:

- an unexpected source-service protocol failure;
- a deadline or dependency failure that prevents a field from completing;
- an internal invariant violation;
- authorization failure under the course error policy.

Do not expose stack traces, SQL messages, internal service names, or exception classes in either channel. Error `extensions` use stable bounded codes and correlation identifiers.

## Idempotency through the graph boundary

The full retry path is:

```text
client chooses stable key
    ↓
graph validates shape and forwards exact semantic input
    ↓
Analysis Control atomically claims or finds the key
    ↓
first request commits command outcome and replay record
    ↓
retries receive the same outcome
```

The gateway does not cache a successful response as the authority. It may cache transport-independent metadata for efficiency only if the source remains authoritative and error semantics are preserved. If the first response is lost after the source commits, a retry must still obtain the committed run.

The course test sends the same `StartAnalysis` mutation twice and expects one run plus `replayed: true` on the repeat. It then changes `algorithm` under the same key and expects a typed conflict. Merely observing equal IDs is insufficient; the source call evidence must show one logical creation.

## Optimistic concurrency

`CancelAnalysisInput.expectedVersion` carries the version previously observed by the client. The graph decodes the global ID and forwards the expected version to Analysis Control, which performs compare-and-swap in the same transaction as the state transition.

The gateway must not:

- read the run and decide locally that the version matches;
- convert version to a floating-point number;
- retry a precondition failure automatically;
- overwrite the client's value with the newest one;
- treat terminal-state conflict and stale-version conflict as the same outcome.

A stale version tells the client to refetch and reconsider. A terminal-state conflict tells the client that the requested transition is no longer legal. These are different recovery paths.

## Authorization and commands

Mutation authorization has at least three layers:

1. may this principal invoke the command class?
2. may this principal act on this tenant and resource?
3. does the current resource state permit the command?

The graph can perform an early policy check to reject obviously forbidden demand, but the owning service repeats the authoritative resource-level decision in the transaction. This avoids time-of-check/time-of-use gaps and protects non-GraphQL callers.

Input fields can require policy too. A support operator may be allowed to cancel a run only with an audited reason. A client may be allowed to choose an algorithm from a tenant-specific allowlist. Schema validity alone cannot express these rules.

## Multi-field mutation example

Consider:

```graphql
mutation Risky($project: CreateProjectInput!, $run: StartAnalysisInput!) {
  createProject(input: $project) { ... }
  startAnalysis(input: $run) { ... }
}
```

The top-level fields execute serially, but `startAnalysis` may fail after the project commits. The response can contain data for `createProject` and a problem for `startAnalysis`. A client that assumed rollback now owns an unexpected project.

Better choices are:

- issue two explicit operations and handle the intermediate state;
- expose one domain command if the invariant truly requires one atomic workflow;
- use an asynchronous process manager if completion spans services and compensation is meaningful.

GraphQL does not remove the distributed-systems decisions from Courses 2, 6, and 8.

## Mutation review checklist

Before release, verify:

- one field maps to one source-owned command or declared workflow;
- input semantics distinguish correlation, idempotency, and concurrency;
- retries preserve the same idempotency key and normalized input;
- source authority performs atomic checks and writes;
- expected domain outcomes are typed and stable;
- unexpected failures preserve GraphQL error semantics;
- authorization is enforced both at the graph boundary and owner transaction;
- no client can infer transactionality from serial top-level execution;
- old persisted mutations execute unchanged against the candidate release.

## Worked capstone review

A client loses the first `StartAnalysis` response and repeats the operation with the same idempotency key. The gateway forwards the same key and input. Analysis Control returns the original run with `replayed: true`. Changing the algorithm under that key returns a typed conflict rather than a second run.

## Python and TypeScript implications

Both gateways pass stable idempotency and expected-version values to Analysis Control. Typed unions in SDL map to dictionaries or discriminated objects in the reference tracks.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-05-*.json`; prose claims without its oracle do not pass.
