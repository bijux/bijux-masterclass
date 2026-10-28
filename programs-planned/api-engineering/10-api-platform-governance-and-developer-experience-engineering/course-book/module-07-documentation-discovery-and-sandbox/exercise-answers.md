# Worked Answers — Module 07: Documentation, Discovery, Sandboxes, and Consumer Onboarding

Use these solutions to audit your reasoning for **Documentation, Discovery, Sandboxes, and Consumer Onboarding**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is generated reference documentation insufficient for onboarding?

Reference lists fields and operations; it rarely explains which interface to choose, how to obtain credentials, how to complete a useful task, or what failure means. Onboarding needs task and concept material around the reference.

The chapter’s decisive distinction is this: Reference alone is not onboarding. A rendered OpenAPI page may list every operation yet leave a consumer unable to choose an interface, obtain safe credentials, or interpret asynchronous completion. Conversely, a quickstart without version-bound reference can succeed once and mislead later. The coverage record links every active API product to all required document roles.

## 2. What is time to first success?

The elapsed time from a consumer obtaining or beginning onboarding to completing a defined useful workflow in a safe environment. It is a product outcome, not merely time to open the portal.

In the cumulative capstone, the rule becomes concrete: Measure the interval from credential issue or onboarding start to a predefined successful workflow. The capstone records four minutes for the reference CLI. The metric is meaningful only when success is defined: a 202 Accepted with a valid status monitor, not any HTTP response. Track failure reasons and abandonment so the platform can distinguish docs, credentials, sandbox, contract, and service problems.

## 3. Why must examples declare a contract version?

Otherwise copied code can silently target a different release than the reader expects. Version binding makes examples reproducible and deprecation impact visible.

A useful way to reason about the boundary is: Run examples during release and periodically. If a sandbox change breaks them, that is a platform incident or documentation defect. Store outputs carefully so secrets and personal data never enter generated docs.

**Evidence.** Require exact catalog, contract, policy, consumer, runtime, documentation, and outcome evidence rather than feature count or portal appearance.

## 4. What makes a sandbox isolated?

Synthetic data, separate tenant identity, short-lived credentials, bounded resources, controlled egress, reset semantics, and no route to production state.

The implementation consequence is: A sandbox is a controlled product environment, not a copy of production. It uses synthetic data, short-lived credentials, bounded quotas, isolated tenants, non-production endpoints, visible reset behavior, and no route to import production records. Examples must be deterministic enough to teach while still exercising real contract behavior.

## 5. Why is production data in a sandbox unacceptable?

It violates the trust boundary, creates privacy and retention risk, and turns a learning environment into an uncontrolled production replica.

The important nuance is: An isolated sandbox uses synthetic data, tenant-scoped state, short-lived credentials, quotas, deny-by-default egress, and deterministic reset. It must not share production data or secrets. The platform owns sandbox control; domain owners supply synthetic scenarios and behavior.

**Evidence.** Complete a version-bound task from discovery to first success using synthetic data and expiring credentials, while measuring zero-result search and support routing.

## 6. What should documentation search optimize?

Successful task discovery and reduced time to useful evidence. Search impressions or query counts are not outcomes; zero-result and reformulation rates reveal gaps.

Under concurrency or failure, the distinction becomes: Track zero-result rate, repeated reformulation, selected result, task completion, and stale-version use. The capstone search fixture has one zero-result query out of four; that 25 percent is deliberately above the five-percent budget and creates a product backlog item. Page views alone would not reveal it.

## 7. How should four interface types be documented?

Start from consumer tasks and decision criteria, then link protocol-specific reference. Do not force consumers to understand every interface before choosing one.

The design remains honest only if: Machine-readable contracts are essential, but consumers begin with a goal: submit an analysis, observe progress, download an artifact, or subscribe to completion. The portal should organize around those tasks and explain which interface fits. Protocol reference remains available after the reader has context.

## 8. Who owns documentation semantics?

The API owner owns behavior and domain meaning. The platform owns publishing, structure, discoverability, quality checks, and common guidance. Shared editing does not erase authority.

The consumer-facing consequence is: Domain owners approve semantics and examples. Platform editors maintain structure, publishing, search, accessibility, and common style. Consumer feedback can open issues. For critical APIs, include a freshness review tied to each release and a periodic task-run check.

**Evidence.** Require exact catalog, contract, policy, consumer, runtime, documentation, and outcome evidence rather than feature count or portal appearance.

## 9. What belongs in a quickstart?

Prerequisites, safe credentials, smallest useful workflow, expected result, cleanup, version, and a path to troubleshooting. It should not hide side effects.

The operational consequence is: Consumers need different document types. An overview explains purpose, audience, owner, and boundaries. A quickstart reaches one smallest successful outcome. Task guides solve recurring goals. Reference describes complete contract details. Concepts explain models and trade-offs. Support and changelog material explain what happens when the happy path ends or changes.

## 10. Why publish failure examples?

Consumers need to recognize authorization, validation, conflict, rate, and dependency outcomes. Happy paths alone create fragile integrations.

The strongest engineering interpretation is: After the happy path, teach at least one expected failure: invalid token, idempotency conflict, stale version, rate limit, unavailable dependency, or subscription gap. Consumers who have never seen a controlled failure will build poor retry and support behavior.

**Evidence.** Require exact catalog, contract, policy, consumer, runtime, documentation, and outcome evidence rather than feature count or portal appearance.

## 11. What is an onboarding support handoff?

A documented transition from platform help—catalog, credentials, sandbox, SDK—to domain-owner help for contract semantics and business behavior.

The defect-oriented view is: Platform support handles portal, registry, template, sandbox, and publication failures. API owners handle semantics and domain behavior. Security and runtime incidents follow the escalation model from earlier courses. The catalog supplies ownership; support routes supply response expectations. A consumer should not need private organizational knowledge to find help.

## 12. How can docs become stale even when they build?

Links and syntax can remain valid while examples target old versions, owners change, runtime behavior drifts, or task outcomes no longer match. Freshness needs semantic and executable evidence.

Across the Python and TypeScript tracks, the invariant is: A search result should show owner, lifecycle, active release, last evidence refresh, support route, and audience. A result without lifecycle may direct consumers to an experiment or deprecated API. A result without ownership may be impossible to support. Ranking purely by page views can amplify old or confusing content.
