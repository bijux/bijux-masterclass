# Worked Answers — Module 05: Distributed Workflows, Sagas, Compensation, and Process Managers

Use these solutions to audit your reasoning for **Distributed Workflows, Sagas, Compensation, and Process Managers**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is a saga not a distributed rollback transaction?

Completed local transactions remain historical facts. Compensation is a new business action that addresses their consequences.

**Decisive evidence:** saga history and compensation record

The chapter’s decisive distinction is this: A local database transaction can commit or roll back its writes together. Once Artifact Service commits bytes and Analysis Control later rejects completion, no database can atomically erase both histories. A saga is not a distributed transaction that restores the past. It is a durable business process that moves forward through local transactions and, when necessary, performs compensating actions.

## 2. Who should own the artifact completion process manager?

Analysis Control, because run completion is the business outcome and it owns the authoritative transition. Artifact Service owns only its local storage step.

**Decisive evidence:** saga ownership record

In the cumulative capstone, the rule becomes concrete: The saga owner is Analysis Control because run completion is the business outcome. Artifact Service owns its local store step. Notification is a downstream reaction, not part of the run-completion success condition.

**Evidence.** Interrupt each saga step and retry order, inspect stable command identity, semantic lock, compensation, durable state, and reconciliation findings.

## 3. What stable identity makes artifact storage idempotent?

Run id, attempt id, and checksum identify the intended storage effect. Repeating the same effect returns the existing artifact.

**Decisive evidence:** artifact effect identity test

A useful way to reason about the boundary is: Control rejects completion because another lease generation owns the run. The artifact is real but no longer attachable to the current run outcome. The process manager requests ExpireOrphanArtifact. It does not delete blindly; retention and audit may require an orphan state first.

## 4. What happens when Artifact Service commits but the worker times out?

Retry with the same effect identity or reconcile by that identity. Do not create a new random artifact id for each attempt.

**Decisive evidence:** after-commit ambiguity schedule

The implementation consequence is: Analysis Control owns the process manager because it owns the final run decision and current attempt. Artifact Service owns artifact effects and compensation execution. Notification is outside the completion saga because its outcome does not change run truth.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 5. Why must Control recheck the lease after issuing an upload capability?

The attempt can become stale during upload. Capability issuance grants storage authority, not permanent completion authority.

**Decisive evidence:** stale-attempt test

The important nuance is: Course 8 uses orchestration for artifact completion because there is a clear business outcome, timeout, current-attempt guard, and compensation. Notification remains choreography: it independently reacts to completion and does not determine whether the workflow succeeded.

**Evidence.** Test workload identity, delegated tenant/user context, audience-bound capability, expiry, tampering, cross-tenant use, and owner-side authorization.

## 6. What is the compensation for a stale artifact?

Mark it orphaned or inaccessible, retain audit history, and expire it under policy. Blind deletion may violate retention and evidence requirements.

**Decisive evidence:** orphan compensation record

Under concurrency or failure, the distinction becomes: Use orchestration when one business outcome has a clear owner, steps require timeout and compensation, and operators need one place to inspect progress. Use choreography when independent reactions to a fact do not form one coordinated transaction.

## 7. Why is Notification outside the run-completion saga?

Notification is an independent reaction to the committed fact. Its unavailability must not change whether the run completed.

**Decisive evidence:** critical-path and event ownership proof

The design remains honest only if: The saga owner is Analysis Control because run completion is the business outcome. Artifact Service owns its local store step. Notification is a downstream reaction, not part of the run-completion success condition.

**Evidence.** Interrupt each saga step and retry order, inspect stable command identity, semantic lock, compensation, durable state, and reconciliation findings.

## 8. When is orchestration preferable to choreography?

When one business outcome has a clear owner, steps need timeout/compensation visibility, and operators need one durable state machine.

**Decisive evidence:** workflow decision record

The consumer-facing consequence is: Use orchestration when one business outcome has a clear owner, steps require timeout and compensation, and operators need one place to inspect progress. Use choreography when independent reactions to a fact do not form one coordinated transaction.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 9. What makes a compensation idempotent?

A stable action id and owner-side record ensure repeated requests return the same business result without repeating side effects.

**Decisive evidence:** duplicate compensation vector

The operational consequence is: The state transition and the outgoing command should be committed under one local authority, commonly with an outbox. Otherwise a crash can advance state without emitting the action or emit the action without recording state.

**Evidence.** Interrupt each saga step and retry order, inspect stable command identity, semantic lock, compensation, durable state, and reconciliation findings.

## 10. Why can a distributed mutex be weaker than a lease generation?

A mutex only coordinates holders temporarily; a durable generation fences stale attempts even after disconnect or pause.

**Decisive evidence:** stale worker fencing test

The strongest engineering interpretation is: Long-running workflows often need to prevent conflicting operations. A semantic lock is domain state such as completion pending or a current attempt generation. It is not a distributed mutex held across the network.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 11. When should a workflow be redesigned rather than wrapped in a saga?

When every step needs immediate global consistency, compensation is impossible, or the process manager needs private access to many databases. Those symptoms suggest a wrong boundary.

**Decisive evidence:** workflow complexity review

The defect-oriented view is: Analysis Control owns the process manager because it owns the final run decision and current attempt. Artifact Service owns artifact effects and compensation execution. Notification is outside the completion saga because its outcome does not change run truth.

## 12. What requires manual review in a saga?

An irreversible or ambiguous effect that cannot be safely classified or compensated automatically. Manual review is a legitimate terminal state, not a hidden exception.

**Decisive evidence:** manual-review escalation evidence

Across the Python and TypeScript tracks, the invariant is: The danger is treating an expired semantic lock as sufficient proof that no effect occurred. A worker may complete after a network delay. Fencing tokens or lease generations ensure stale actors cannot commit authoritative state.
