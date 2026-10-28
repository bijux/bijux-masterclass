# Worked answers — Release operations, incidents, final defense, and security handoff

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why should release decisions be categorical instead of averaged?

Averages allow many minor passes to hide one non-compensable failure such as protected-data deletion, untrusted artifact, or incompatible migration. Categorical outcomes preserve blocker semantics and distinguish review-required from missing evidence.

## 2. What does a sync freeze control and not control?

It controls when selected reconciliation may apply changes. It does not validate candidate correctness, stop all repository mutation, revoke credentials, or guarantee runtime stability. Image automation, secret rotation, and emergency exceptions need coordinated rules.

## 3. When is reconciliation suspension justified?

When the desired revision or controller behavior is harmful, emergency drift must remain temporarily, or an explicit release phase requires a hold. Suspension must be narrow, visible, time-bounded, owned, and paired with resumption criteria because it also stops drift repair and new fixes.

## 4. Why are application owner and data owner separate incident roles?

The application owner understands workload behavior and compatibility; the data owner controls authoritative state, migration, restore, retention, and fencing decisions. An application rollback may be safe operationally but unsafe for data. Separate responsibility prevents the delivery operator from guessing.

## 5. What is the earliest useful question in a delivery incident?

Which transition first failed: source acquisition, artifact trust, rendering, comparison, apply, health, traffic exposure, user journey, or data gate? Starting with the final red status encourages random changes and loses causality.

## 6. How should emergency live changes be handled before reconciliation resumes?

Diff them against reviewed desired state and classify each as durable, temporary, ownership transfer, protected/external, or unknown. Commit durable changes, remove temporary ones, and resolve ownership before resuming so the controller neither erases mitigation nor preserves accidental drift.

## 7. Why is fast deployment not a sufficient delivery SLO?

Speed does not measure correctness, rejection quality, drift age, rollback, or evidence completeness. A system can deploy rapidly while applying unsafe revisions. Delivery indicators must include source age, reconcile outcome, drift, abort time, protected-prune attempts, and release decision quality.

## 8. What should happen when a mutable tag changes after staging?

Production promotion must reject the candidate because the artifact subject changed. Resolve and record the new digest as a new candidate, obtain its supply-chain and test evidence, and repeat required promotion gates. Never assume semantic tag continuity.

## 9. How is a repository outage handled during controller restart?

Restore the controller, but keep the last-known-good cluster state and report source unavailable. Do not invent empty desired state or prune. Reconciliation resumes only after the repository revision and integrity are trustworthy.

## 10. What evidence is needed after a delivery credential compromise?

Credential scope and timeline, repositories and clusters accessed, commits and source artifacts observed, unauthorized changes, rotation and revocation, controller suspension/resume, narrowed replacement identities, and final no-drift proof. Unrelated broad rotation should not erase causality.

## 11. What is the purpose of the Course 8 handoff?

It gives security engineering the actual delivery identities, credentials, policy points, tenant assumptions, decryption boundaries, and break-glass roles to threat-model and harden. Without it, security becomes generic advice disconnected from the platform’s authority graph.

## 12. State the final competence Course 7 is designed to produce.

The learner can trace a production change from immutable source and artifacts through deterministic rendering, review, promotion, reconciliation, health, progressive exposure, and incident recovery; bound every actor’s authority; reject unsafe automation; and produce evidence that another engineer can independently verify.
