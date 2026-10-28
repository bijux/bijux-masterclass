# Reference — OpenGitOps principles mapped to Atlas

**Declarative:** Atlas stores desired resources and release policies, not imperative production shell sessions. One-shot operations are represented by durable Jobs and operation records.

**Versioned and immutable:** commits and OCI digests identify source and artifacts. Branches and tags are workflow selectors only.

**Pulled automatically:** in-environment controllers observe source and apply scoped state. CI publishes candidates rather than holding broad production credentials.

**Continuously reconciled:** controllers compare desired and observed state repeatedly, classify drift, and report status. Continuous reconciliation does not authorize deletion of protected data or imply user correctness.

## Extended reader notes

The OpenGitOps principles are best used as design questions. **Declarative** asks whether desired state can be compared and reconciled without replaying an imperative history. **Versioned and immutable** asks whether a decision can be reconstructed exactly. **Pulled automatically** asks which identity observes and acts inside the target boundary. **Continuously reconciled** asks how drift is detected, classified, repaired, or escalated after the pipeline exits.

Each principle has a failure boundary. Declarative state does not make a destructive migration reversible. Git immutability does not make a referenced image tag immutable. Pull-based operation does not make the controller’s credentials safe. Continuous reconciliation does not justify overwriting fields owned by another manager. Use the principles to expose missing mechanisms, not as a maturity badge.

For Atlas, a design satisfies the principles only when the immutable source and artifact subjects are recorded, the renderer output is reproducible, controller authority is scoped, source unavailability is distinguished from an empty desired set, and emergency changes have a route back to reviewed desired state.
