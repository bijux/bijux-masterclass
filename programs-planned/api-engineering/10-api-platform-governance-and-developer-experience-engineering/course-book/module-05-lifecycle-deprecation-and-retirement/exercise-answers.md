# Worked Answers — Module 05: Lifecycle, Compatibility, Deprecation, and Retirement

Use these solutions to audit your reasoning for **Lifecycle, Compatibility, Deprecation, and Retirement**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is deprecation not a documentation annotation?

It is a managed change involving replacement, consumers, notice, migration, runtime traffic, support, and retirement evidence. An annotation can communicate state but cannot perform the workflow.

The chapter’s decisive distinction is this: A deprecation record names the affected version, replacement or exit path, behavioral differences, owner, notice dates, consumers, migration status, support plan, runtime removal plan, and archive plan. Consumers need a way to verify migration before production cutover. Owners need a feedback loop for blocking defects in the replacement.

## 2. What is the difference between deprecated and retired?

Deprecated remains available but is no longer recommended and has an exit plan. Retired is no longer available for normal use and has completed runtime removal and archival obligations.

In the cumulative capstone, the rule becomes concrete: The capstone defines proposed, experimental, active, deprecated, and retired. Each transition has required evidence. A proposed API needs an owner and contract before experiment. Active publication requires compatibility, security, reliability, documentation, and support evidence. Deprecation requires a replacement or exit plan, consumer inventory, migration guide, and notice end. Retirement requires zero blocking consumers, approval, runtime removal, and archival plan.

## 3. Why track actual consumers?

Without consumer identity, version, criticality, and last use, notice is guesswork. Consumer evidence determines impact and whether retirement is safe.

A useful way to reason about the boundary is: Notice begins only when consumers have a usable migration route. A long notice with no replacement documentation is delay, not support. A shorter notice can be adequate for a low-criticality experimental API with no consumers. The policy sets a minimum baseline, while criticality and contractual commitments can require more.

## 4. Can zero traffic prove zero consumers?

No. Telemetry can be incomplete, seasonal consumers may be idle, and offline generated clients may exist. Combine registration, runtime evidence, support records, and owner attestation.

The implementation consequence is: Unknown traffic can come from shared credentials, NAT, scripts, or unregistered services. Improve identity before retirement. If uncertainty remains, decide through explicit risk authority. Do not fabricate “zero consumers” by limiting the query to registered records.

**Evidence.** Combine contract compatibility, usage and declared-consumer evidence, migration status, notice, owner approval, and rollback before advancing lifecycle.

## 5. What should a migration guide include?

Behavioral differences, contract changes, code or configuration actions, test evidence, timeline, rollback considerations, and a clear way to report completion.

The important nuance is: During migration, run old and new versions in parallel when possible. Compare contract tests, business outcomes, error rates, and performance. A consumer can report “complete” only after production or representative evidence, not merely a successful code generation. Keep rollback until irreversible data or routing changes occur.

## 6. When may an emergency shorten notice?

Only under an explicit security or safety incident with impact analysis, authorized risk acceptance, consumer communication, and a documented replacement or containment route.

Under concurrency or failure, the distinction becomes: A severe security issue may make continued operation riskier than rapid removal. Emergency policy still requires an incident record, affected-consumer analysis, approved risk decision, containment path, and communication. “Security” is not a magic word that bypasses accountability.

**Evidence.** Require exact catalog, contract, policy, consumer, runtime, documentation, and outcome evidence rather than feature count or portal appearance.

## 7. Why retain retired contract artifacts?

Historical clients, incidents, audits, and data interpretation may depend on the old semantics. Retirement removes support and runtime availability, not history.

The design remains honest only if: Retired contracts, docs, changelogs, SDK versions, and migration records remain discoverable as historical artifacts. A consumer debugging an old event or audit record needs the semantics that existed then. The catalog marks retired state; the registry preserves identity.

**Evidence.** Combine contract compatibility, usage and declared-consumer evidence, migration status, notice, owner approval, and rollback before advancing lifecycle.

## 8. What is a blocking consumer?

A consumer whose criticality, migration status, or approved exception means retirement would cause unacceptable harm. The definition must be policy-driven, not improvised at the meeting.

The consumer-facing consequence is: The lifecycle engine evaluates Analysis HTTP 1.1. Required retirement documents exist, but one blocking consumer remains. The result is blocked. A committee cannot override the machine by changing the status field; it must resolve the consumer, approve an explicit exception, or accept emergency risk through the designated path.

## 9. How should unknown consumers affect retirement?

Treat them as uncertainty requiring investigation or risk acceptance. Unknown does not equal safe.

The operational consequence is: A migration campaign has cohorts, milestones, and escalation. Start with willing low-risk consumers to validate guides and tooling. Address critical consumers early because they may need longer lead time. Track states such as discovered, contacted, planned, testing, complete, exception, and unknown.

**Evidence.** Combine contract compatibility, usage and declared-consumer evidence, migration status, notice, owner approval, and rollback before advancing lifecycle.

## 10. Why version lifecycle policy?

Notice periods, evidence requirements, and transition authority can change. A versioned policy explains which rules governed a past decision.

The strongest engineering interpretation is: evaluate transition checks allowed edges and required evidence. deprecation impact calculates affected and blocking consumers from the inventory. These functions are intentionally separate: lifecycle policy defines what is required, while consumer data supplies current impact.

**Evidence.** Evaluate categorical policy with fresh evidence, force a blocker and review state, and verify exception owner, compensating control, expiry, and closure path.

## 11. Who approves retirement?

The API owner proposes; affected consumers confirm or are handled through policy; platform verifies evidence and runtime plan; the designated governance or risk authority approves according to criticality.

The defect-oriented view is: Track migration as states such as uncontacted, acknowledged, planning, testing, complete, and waived-with-risk-acceptance. “Email sent” is not migration. Critical consumers may need rehearsals, dual-read comparison, or rollback plans. The platform coordinates evidence; each consumer and API owner remain accountable for their work.

## 12. What is the retirement of Analysis HTTP 1.1 currently blocked by?

`consumer-legacy-cli` still reports active production use and migration is only scheduled. The replacement exists, but consumer completion evidence does not.

Across the Python and TypeScript tracks, the invariant is: The capstone has a legacy CLI on Analysis HTTP API 1.1. It is active in production and migration is scheduled, so retirement remains blocked even though API 1.2 has been available for months.

**Evidence.** Combine contract compatibility, usage and declared-consumer evidence, migration status, notice, owner approval, and rollback before advancing lifecycle.
