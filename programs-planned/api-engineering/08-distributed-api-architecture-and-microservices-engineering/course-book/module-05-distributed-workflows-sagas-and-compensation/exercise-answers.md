# Worked answers — Distributed Workflows, Sagas, Compensation, and Process Managers

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. Why is a saga not a distributed rollback transaction?

Completed local transactions remain historical facts. Compensation is a new business action that addresses their consequences.

**Decisive evidence:** saga history and compensation record

## 2. Who should own the artifact completion process manager?

Analysis Control, because run completion is the business outcome and it owns the authoritative transition. Artifact Service owns only its local storage step.

**Decisive evidence:** saga ownership record

## 3. What stable identity makes artifact storage idempotent?

Run id, attempt id, and checksum identify the intended storage effect. Repeating the same effect returns the existing artifact.

**Decisive evidence:** artifact effect identity test

## 4. What happens when Artifact Service commits but the worker times out?

Retry with the same effect identity or reconcile by that identity. Do not create a new random artifact id for each attempt.

**Decisive evidence:** after-commit ambiguity schedule

## 5. Why must Control recheck the lease after issuing an upload capability?

The attempt can become stale during upload. Capability issuance grants storage authority, not permanent completion authority.

**Decisive evidence:** stale-attempt test

## 6. What is the compensation for a stale artifact?

Mark it orphaned or inaccessible, retain audit history, and expire it under policy. Blind deletion may violate retention and evidence requirements.

**Decisive evidence:** orphan compensation record

## 7. Why is Notification outside the run-completion saga?

Notification is an independent reaction to the committed fact. Its unavailability must not change whether the run completed.

**Decisive evidence:** critical-path and event ownership proof

## 8. When is orchestration preferable to choreography?

When one business outcome has a clear owner, steps need timeout/compensation visibility, and operators need one durable state machine.

**Decisive evidence:** workflow decision record

## 9. What makes a compensation idempotent?

A stable action id and owner-side record ensure repeated requests return the same business result without repeating side effects.

**Decisive evidence:** duplicate compensation vector

## 10. Why can a distributed mutex be weaker than a lease generation?

A mutex only coordinates holders temporarily; a durable generation fences stale attempts even after disconnect or pause.

**Decisive evidence:** stale worker fencing test

## 11. When should a workflow be redesigned rather than wrapped in a saga?

When every step needs immediate global consistency, compensation is impossible, or the process manager needs private access to many databases. Those symptoms suggest a wrong boundary.

**Decisive evidence:** workflow complexity review

## 12. What requires manual review in a saga?

An irreversible or ambiguous effect that cannot be safely classified or compensated automatically. Manual review is a legitimate terminal state, not a hidden exception.

**Decisive evidence:** manual-review escalation evidence
