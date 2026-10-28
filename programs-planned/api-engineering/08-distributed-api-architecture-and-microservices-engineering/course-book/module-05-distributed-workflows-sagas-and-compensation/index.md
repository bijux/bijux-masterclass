# Distributed Workflows, Sagas, Compensation, and Process Managers

**Module 05 of 10**

> **Governing question:** How do we preserve business intent when one workflow crosses services that cannot share a transaction?

## Place in the program

Course 7 introduced typed internal RPC but deliberately refused to equate a remote method with an independently owned service. Course 8 now uses ownership, data, failure, release, and operational evidence to decide which capabilities deserve distribution.

## Learning outcomes

- distinguish local ACID transactions from distributed workflow guarantees
- choose orchestration or choreography from ownership and visibility needs
- design idempotent saga steps and stable command identities
- write compensations that restore business meaning rather than pretend to erase history
- handle timeout, duplicate, reordering, and crash recovery in process managers
- identify workflows that should be redesigned instead of wrapped in a saga

## Capstone result

Implement the artifact-publication and run-completion saga with durable step identity, semantic locks, compensation, timeout handling, and operator-visible reconciliation.


## There is no cross-service rollback button

A local database transaction can commit or roll back its writes together. Once Artifact Service commits bytes and Analysis Control later rejects completion, no database can atomically erase both histories. A saga is not a distributed transaction that restores the past. It is a durable business process that moves forward through local transactions and, when necessary, performs compensating actions.

The distinction matters. Deleting an artifact may be wrong if it was retained for audit. The compensation may mark it orphaned, revoke access, schedule expiry, and record why Control rejected it.

## The artifact completion saga

The capstone workflow is:

```text
Analysis Control
  mint upload capability for run + attempt + checksum
        |
Worker Plane
  upload artifact
        |
Artifact Service
  commit artifact and publish ArtifactStored
        |
Analysis Control process manager
  validate current attempt and attach artifact
  complete run and publish AnalysisRunCompleted
        |
Notification Service
  create delivery attempts
```

The saga owner is Analysis Control because run completion is the business outcome. Artifact Service owns its local store step. Notification is a downstream reaction, not part of the run-completion success condition.

## Stable identities

Every retryable step needs stable identity:

- saga id: run + attempt;
- artifact effect: run + attempt + checksum;
- ArtifactStored event id: artifact id + version;
- CompleteRun command id: run + attempt + artifact;
- notification effect: subscription + event id.

Stable identity lets a service return the original outcome or ignore a duplicate. Random identity per attempt turns retries into new effects.

## Process manager state

A process manager records enough state to resume:

```text
new
artifact-stored
completed
compensation-required
compensated
manual-review
```

It also records processed message ids and a history of decisions. The process manager is not the authority for artifact bytes or run state; it coordinates owned local transactions.

## Failure schedules

### Timeout before Artifact Service receives bytes

Retry is safe with the same capability and effect identity, subject to expiry and byte limits.

### Timeout after Artifact Service commits

The worker cannot know whether storage succeeded. It retries with the same run, attempt, and checksum. Artifact Service returns the existing artifact.

### Artifact stored, but lease became stale

Analysis Control rejects completion. The process manager requests compensation: mark the artifact orphaned and schedule retention cleanup. The stale worker cannot overwrite the current run.

### Completion committed, response lost

A retry with the same command id returns the completed outcome. Reconciliation can compare run reference and artifact owner state.

### Notification consumer unavailable

The run remains completed. Durable event retention and consumer position determine later recovery.

## Orchestration versus choreography

Use orchestration when one business outcome has a clear owner, steps require timeout and compensation, and operators need one place to inspect progress. Use choreography when independent reactions to a fact do not form one coordinated transaction.

The artifact/run workflow uses a process manager. Notification delivery uses choreography: it consumes `AnalysisRunCompleted` and owns its retry lifecycle. Making Notification part of the saga would reintroduce synchronous or operational coupling.

## Semantic locks and reservations

Long-running workflows often need to prevent conflicting operations. A semantic lock is domain state such as `completion_pending` or a current attempt generation. It is not a distributed mutex held across the network.

The current lease generation fences stale workers. An upload capability binds to that attempt. Analysis Control still rechecks the attempt at completion because capability issuance does not freeze the world.

## Compensation quality

A good compensation is:

- idempotent;
- owned by the service that owns the affected fact;
- safe after repeated messages;
- explicit about irreversible effects;
- observable;
- bounded by retention and policy;
- able to escalate to manual review.

A generic `undo()` method hides the important semantics.

## When not to use a saga

Redesign the workflow if:

- every step needs immediate global consistency;
- compensation is impossible and partial completion is unacceptable;
- the workflow crosses many services because boundaries are wrong;
- the process manager needs private database access to every service;
- users cannot understand intermediate states;
- operational repair would require bespoke data editing.

Sometimes the correct answer is to keep the capability cohesive.

## Python and TypeScript implications

Both reference tracks implement the same state transitions and duplicate handling. Python uses an enum-backed dataclass. TypeScript uses a string-union state. Shared schedule vectors, not source similarity, define parity.

## Evidence required before Module 6

Demonstrate happy path, duplicate storage, timeout-after-commit reconciliation, stale-attempt compensation, and idempotent completion. Explain why Notification Delivery is outside the saga’s success condition.
## A saga is durable decision state, not a sequence diagram

A sequence diagram shows the happy path. A process manager must survive every interruption between steps. Its durable record needs enough information to decide what to do after restart:

```text
saga_id
business key
current state
expected run attempt
artifact id, when known
processed message and command ids
next action
retry schedule
compensation status
last error classification
manual-review reason
version
```

The state transition and the outgoing command should be committed under one local authority, commonly with an outbox. Otherwise a crash can advance state without emitting the action or emit the action without recording state.

## Failure schedule for artifact completion

The capstone workflow is:

```text
mint capability
→ store artifact
→ observe ArtifactStored
→ complete run under current attempt
→ publish AnalysisRunCompleted
→ Notification consumes completion
```

Now enumerate failures.

### Failure before artifact commit

The upload fails or times out before Artifact commits. The worker may retry with the same effect identity `(run, attempt, checksum)`. No compensation is needed because no durable artifact exists.

### Artifact committed, response lost

The worker sees a timeout but Artifact stored the object. A retry returns the existing artifact for the same effect identity. Creating another artifact would be incorrect.

### Artifact stored, run attempt became stale

Control rejects completion because another lease generation owns the run. The artifact is real but no longer attachable to the current run outcome. The process manager requests `ExpireOrphanArtifact`. It does not delete blindly; retention and audit may require an orphan state first.

### Run completed, completion response lost

A repeated completion command returns the already completed result if the same artifact is attached. If a different artifact is proposed, the owner returns a conflict.

### Completion event duplicated

Notification’s inbox deduplicates by event identity. It may create exactly one delivery effect per `(consumer, event, effect-version)`.

### Notification permanently fails

Run completion remains true. Notification owns dead-letter custody and manual resolution. The saga does not compensate a successful analysis because a receiver rejected delivery.

A reliable workflow design covers these schedules before implementation.

## Exactly-once effects require stable identity

Transport may deliver more than once. The application can still create one effect by using a stable identity stored with the effect.

Examples:

```text
artifact publication:
    run_id + attempt_id + sha256

run completion:
    run_id + attempt_id

notification delivery:
    subscription_id + event_id + delivery_profile_version

compensation:
    saga_id + compensation_name
```

A random identifier generated on every retry does not deduplicate. The identity must derive from the business effect or be durably assigned before the first attempt.

## Compensation is a business action

Compensation is not database rollback after other services have observed state. It is a new action with its own preconditions, failures, and audit trail.

Compensations fall into several categories:

- **inverse** — restore the previous state, when truly possible;
- **semantic release** — release a reservation or mark an object orphaned;
- **forward correction** — create a new fact that supersedes the bad outcome;
- **manual review** — stop automatic action where reversal is unsafe.

Deleting an artifact may not be a valid inverse if retention policy, audit, or external download has occurred. The capstone marks it orphaned or expired under Artifact ownership.

A compensation must be idempotent. It also needs authorization: the process manager cannot acquire a superuser credential merely because it is internal.

## Orchestration and choreography

### Orchestration

A process manager owns progress and sends explicit commands. Advantages:

- workflow state is visible;
- timeouts and compensation are centralized;
- the next step is explicit;
- debugging is easier for long-running business flows.

Costs:

- the orchestrator can become over-centralized;
- services may become command handlers with weak autonomy;
- workflow changes depend on the process-manager contract.

### Choreography

Services react to events without one controller. Advantages:

- local autonomy;
- simple event-driven extensions;
- reduced central coordination for independent reactions.

Costs:

- the overall workflow can become invisible;
- cycles and accidental cascades appear;
- completion and timeout ownership may be unclear;
- incident diagnosis requires strong event evidence.

Course 8 uses orchestration for artifact completion because there is a clear business outcome, timeout, current-attempt guard, and compensation. Notification remains choreography: it independently reacts to completion and does not determine whether the workflow succeeded.

## Semantic locks and reservations

A database lock cannot span a long workflow. Instead, the domain may represent intent explicitly:

```text
run attempt is current until lease expiry
artifact capability valid for one attempt and checksum
subscription change has an effective version
storage reservation expires at a declared time
```

These are semantic locks. Other operations can observe and respect them without holding a database transaction open.

The danger is treating an expired semantic lock as sufficient proof that no effect occurred. A worker may complete after a network delay. Fencing tokens or lease generations ensure stale actors cannot commit authoritative state.

## Timeout does not reveal outcome

When a cross-service command times out, the caller knows only that it did not receive a response. The callee may have:

- never received the command;
- rejected it;
- committed it and lost the response;
- still be processing;
- committed part of a faulty non-atomic implementation.

The next action should query by effect identity or safely retry under idempotency. “Timeout means failed” is not a valid distributed state transition.

## Manual review is a designed terminal state

Some ambiguity cannot be repaired automatically without unacceptable risk. A mature workflow can enter `manual-review` with:

- stable case identity;
- immutable evidence links;
- current owner;
- permitted repair actions;
- deadline or escalation;
- no automatic retry storm.

Manual review is not an excuse for missing design. It is a controlled response to states where automation lacks sufficient authority or evidence.

## Process-manager boundary in the capstone

Analysis Control owns the process manager because it owns the final run decision and current attempt. Artifact Service owns artifact effects and compensation execution. Notification is outside the completion saga because its outcome does not change run truth.

This design keeps the process manager from becoming a universal workflow engine. A process manager should own one business outcome, not every interaction in the organization.
