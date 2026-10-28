# Capstone release process

A candidate is proposed with immutable artifacts. The renderer produces environment-specific sets and digests. Policy checks compatibility, protected resources, secrets, and target capability. Promotion updates one environment reference. Reconciliation applies owned fields. Health and progressive analysis produce observations. The release engine classifies accepted, rejected, review-required, or not-executed.

Every failure leaves a durable record and a cleanup path. A rollback is itself a reviewed release with a predecessor and compatibility decision.

## Extended reader notes

The reference release process has seven stages: build immutable artifacts; create an environment candidate; render and bind the exact desired set; run static, policy, compatibility, restore, and security gates; promote through representative fleet waves; reconcile and measure actual exposure; publish a categorical dossier.

Failure at a blocker gate rejects the candidate. Missing required environment evidence yields `not-executed`. Bounded ambiguity yields `review-required` and needs named approval. Promotion never rebuilds artifacts. A revert creates a new desired-state commit. After the rollback frontier, the process requires a forward fix.
