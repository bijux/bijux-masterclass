# Worked Answers — Module 04: Governance as Code, Evidence, Scorecards, and Exceptions

Use these solutions to audit your reasoning for **Governance as Code, Evidence, Scorecards, and Exceptions**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why should governance rules produce pass, review, or fail rather than one score?

A score hides decision semantics. A blocker ownership or security failure must reject publication even if many minor checks pass. Review identifies accountable judgment rather than pretending uncertainty is success.

The chapter’s decisive distinction is this: This model prevents two common errors. First, a numeric score cannot average a critical failure into apparent health. Second, uncertainty is not silently converted into approval. Review names the human decision still required.

## 2. What makes a rule suitable for automation?

Its input is authoritative and machine-readable, its outcome is deterministic, and false positives or negatives are understood. Architectural intent and unusual risk often require human review.

In the cumulative capstone, the rule becomes concrete: New policies should begin in observation mode against a representative portfolio. Measure false positives, missing metadata, remediation cost, and owner understanding. Then introduce warning, review, and blocker phases with a published effective date. Emergency blocker rules are justified for immediate organization-wide risk, but still require clear remediation and ownership.

## 3. Why must exceptions expire?

An exception is temporary risk acceptance, not a permanent alternative policy. Expiry forces reassessment as context, ownership, and controls change.

A useful way to reason about the boundary is: An exception without expiry becomes an alternative policy. Repeated exceptions for the same condition indicate one of three things: the rule is wrong, the paved road is missing a capability, or teams are avoiding necessary work. The platform product review must decide which, rather than automatically renewing.

## 4. What is a compensating control?

A measure that reduces the risk created by not meeting the original rule. It must address the actual threat, not merely restate that the team will be careful.

The implementation consequence is: An exception is a time-bounded decision to accept a named residual risk. It requires the rule, subject, reason, owner, approver, compensating control, creation time, expiry, and closure path. The Course 10 RPC documentation exception is valid because an interactive browser example is inappropriate for a bidirectional worker stream; checked command-line and Python transcripts are the compensating evidence. The exception does not remove all documentation requirements and it expires.

## 5. Why is a green badge insufficient evidence?

Without rule version, input, source, timestamp, and decision, a badge cannot be reproduced or audited. It may also be stale.

The important nuance is: Evidence should be reproducible where possible. Link the exact contract digest, tool version, configuration, fixture, and report. When a check is environment-backed, state what was not executed. “Pipeline green” is not a portable evidence record because the pipeline definition and inputs can change.

**Evidence.** Evaluate categorical policy with fresh evidence, force a blocker and review state, and verify exception owner, compensating control, expiry, and closure path.

## 6. Who owns a governance exception?

The entity owner requests it, an authorized risk owner approves it, and both the platform and governance system track scope and expiry. The platform team should not self-approve business risk by default.

Under concurrency or failure, the distinction becomes: Protect policy repositories, exception approvals, and evidence stores. An attacker who can create a fake exception or overwrite evidence can bypass every API control without touching service code. Apply access control, review, immutable history, and audit to governance artifacts themselves.

## 7. Why should policy rules be versioned?

Changing a rule changes release outcomes. Versioning permits reproducibility, migration, and explanation of why an entity changed status without changing its own artifact.

The design remains honest only if: Policy changes are contracts with API owners. Version the policy pack, publish a changelog, test it against known fixtures, and provide a way to reproduce the decision locally. A centralized rule that changes unpredictably creates release instability. Governance as code is valuable because it can be reviewed and replayed, not because code is automatically objective.

## 8. How can scorecards harm teams?

They can create gaming, average away critical defects, reward metadata volume, and punish teams for irrelevant checks. Scorecards should support decisions and expose evidence, not rank teams.

The consumer-facing consequence is: Organization-wide rules cover ownership, immutable releases, incident contact, and supply-chain evidence. Protocol owners contribute specialized compatibility checks. Domain teams may add business constraints. The platform provides execution, schemas, evidence storage, and exception workflow. This division allows local expertise without each team inventing a different governance mechanism.

## 9. What is federated governance at rule level?

The platform supplies common rule machinery and organization-wide invariants; domain owners define protocol and business-specific checks within a bounded policy contract.

The operational consequence is: Organization-wide rules cover ownership, immutable releases, incident contact, and supply-chain evidence. Protocol owners contribute specialized compatibility checks. Domain teams may add business constraints. The platform provides execution, schemas, evidence storage, and exception workflow. This division allows local expertise without each team inventing a different governance mechanism.

## 10. When is manual review mandatory?

When evidence is ambiguous, consumer impact is context-dependent, a review-required compatibility change appears, or an exception changes residual risk beyond an automatic rule’s authority.

The strongest engineering interpretation is: A review form should present the subject, exact automated findings, consumer impact, precedent, residual risk, and proposed decision. Avoid asking reviewers to rediscover evidence across ten tools. Record the rationale and expiry of conditions. Reviewers should be selected by decision authority, not merely by availability.

## 11. How does evidence freshness affect policy?

Expired security, reliability, or performance evidence should reduce readiness or block release according to risk. A historical pass is not permanent.

The defect-oriented view is: Evidence can become invalid because time passes, the subject changes, or the verifier changes. Bind evidence to a subject digest or entity revision. A security test for API 1.1 should not automatically satisfy API 1.2. Reliability evidence can remain relevant across a documentation-only contract release if the runtime subject is unchanged, but that reuse should be explicit.

## 12. Why must policy failure occur before expensive publication work?

Early feedback saves owner time and avoids generating docs, SDKs, and runtime changes for a candidate already invalid on ownership or compatibility.

Across the Python and TypeScript tracks, the invariant is: A failed rule should explain what was inspected, why it failed, how to reproduce, and the smallest valid remediation. “Policy check failed” creates support load and encourages bypass. Early feedback in the owner workflow is more valuable than a final release-board rejection.
