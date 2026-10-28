# Worked answers — Governance as Code, Evidence, Scorecards, and Exceptions

## 1. Why should governance rules produce pass, review, or fail rather than one score?

A score hides decision semantics. A blocker ownership or security failure must reject publication even if many minor checks pass. Review identifies accountable judgment rather than pretending uncertainty is success.

## 2. What makes a rule suitable for automation?

Its input is authoritative and machine-readable, its outcome is deterministic, and false positives or negatives are understood. Architectural intent and unusual risk often require human review.

## 3. Why must exceptions expire?

An exception is temporary risk acceptance, not a permanent alternative policy. Expiry forces reassessment as context, ownership, and controls change.

## 4. What is a compensating control?

A measure that reduces the risk created by not meeting the original rule. It must address the actual threat, not merely restate that the team will be careful.

## 5. Why is a green badge insufficient evidence?

Without rule version, input, source, timestamp, and decision, a badge cannot be reproduced or audited. It may also be stale.

## 6. Who owns a governance exception?

The entity owner requests it, an authorized risk owner approves it, and both the platform and governance system track scope and expiry. The platform team should not self-approve business risk by default.

## 7. Why should policy rules be versioned?

Changing a rule changes release outcomes. Versioning permits reproducibility, migration, and explanation of why an entity changed status without changing its own artifact.

## 8. How can scorecards harm teams?

They can create gaming, average away critical defects, reward metadata volume, and punish teams for irrelevant checks. Scorecards should support decisions and expose evidence, not rank teams.

## 9. What is federated governance at rule level?

The platform supplies common rule machinery and organization-wide invariants; domain owners define protocol and business-specific checks within a bounded policy contract.

## 10. When is manual review mandatory?

When evidence is ambiguous, consumer impact is context-dependent, a review-required compatibility change appears, or an exception changes residual risk beyond an automatic rule’s authority.

## 11. How does evidence freshness affect policy?

Expired security, reliability, or performance evidence should reduce readiness or block release according to risk. A historical pass is not permanent.

## 12. Why must policy failure occur before expensive publication work?

Early feedback saves owner time and avoids generating docs, SDKs, and runtime changes for a candidate already invalid on ownership or compatibility.
