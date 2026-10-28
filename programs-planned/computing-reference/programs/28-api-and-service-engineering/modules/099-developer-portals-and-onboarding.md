---
module_id: API-099
program: API & Service Engineering
level: 2
module_number: 99
title: Developer Portals and Onboarding
status: complete
last_verified: 2026-09-02
---

# Developer Portals and Onboarding

## One-Page Review

### Governing question

How can an API program turn discovery, evaluation, access, first successful integration, production approval, operation, support, and retirement into a secure measurable self-service journey whose information stays consistent with the real service?

### Essential definitions

- A **developer portal** is the discoverable product surface that connects API catalog, contracts, documentation, access workflows, environments, credentials, tools, lifecycle, support, status, and ownership.
- **onboarding** is the end-to-end process from a consumer need to a correctly secured, observable, supportable production integration—not merely account creation.
- **time to first meaningful success (TTFMS)** is elapsed time until a new consumer completes a representative task and understands the outcome; a trivial unauthenticated ping is not meaningful success.
- A **catalog entry** is a versioned metadata view of an API/product including owner, lifecycle, audience, contracts, environments, dependencies, support and policy links.
- A **golden path** is a supported default journey that minimizes decisions while leaving explicit escape paths for justified needs.
- A **sandbox** is an isolated environment with documented fidelity, data, limits, reset and differences from production.
- **registration** establishes a consumer/application identity and metadata; **credential issuance** grants a bounded secret/key/certificate/token mechanism. Neither automatically authorizes every API action.
- A **documentation contract** is the governed consistency relation among machine-readable contract, examples, SDKs, portal content, policy, runtime behavior and lifecycle state.
- A **self-service boundary** automates routine safe decisions while escalating risk-bearing decisions to an accountable owner.

### Central model, mechanism, or theorem

Let onboarding stages be discover $D$, evaluate $E$, register $R$, obtain/configure credentials $C$, integrate/test $I$, production approve $P$, and operate $O$. With conditional completion probabilities $p_i$ and stage service/wait times $s_i,w_i$,

$$
P(O)=\prod_i p_i, \qquad T_{onboard}=\sum_i(s_i+w_i).
$$

A 90% success rate at each of seven stages yields $0.9^7\approx47.8\%$ end-to-end completion. Optimize the whole journey: remove unnecessary stages, automate safe waits, improve failure recovery, and measure cohorts by consumer task/audience without collecting unnecessary personal data.

### Critical invariants

Every published API has a valid owner/support/lifecycle/audience, canonical immutable contract/version, base environments, auth/scopes, limits, data classification, status/SLO, changelog/deprecation and runnable task-oriented quickstart. Portal views are derived or verified against authoritative sources and expose freshness/provenance. Search results never advertise orphaned/retired/private APIs to the wrong audience.

Registration, approvals and credentials use verified identities, least privilege, separation of duties where needed, secret-safe display/storage, rotation/revocation and audit. Sandbox examples cannot cause production effects; production promotion verifies contract/security/capacity/support prerequisites. Docs/examples/SDKs are tested through the same public boundary. Portal/catalog outage does not silently weaken runtime security, and emergency human support remains available. Onboarding metrics measure correct outcomes and friction, not vanity page views.

### Common failures

Portal as link farm; catalog with no owner/lifecycle; duplicate handwritten specs; search ranks deprecated API; quickstart uses admin token; secrets in URLs/source/browser storage; credential shown repeatedly; shared sandbox tenant/data; sandbox accepts behavior production rejects; generated SDK treated as universal; examples omit errors/idempotency/pagination; `curl 200` called success; approvals via untracked chat; scope names without tasks; public/internal audience leak; stale quotas/base URLs; no version/deprecation migration; support link with no response target; status page hiding dependencies; onboarding analytics exposing users; inaccessible UI; portal availability coupled to API runtime; and removing old docs before consumers migrate.

### Compact example

A partner finds Payments v2, completes verified organization/application registration, receives a sandbox-bound client credential once, follows “create idempotent payment and retrieve outcome,” then requests production scopes. The workflow validates callback/domain ownership, contract test, quota/capacity tier, support contacts and key rotation before production issuance. Portal records a 42-minute TTFMS and two approval wait days separately. **Conclusion:** the portal orchestrates evidence and ownership across the full integration lifecycle; it is not the authority for payment effects.

### Connections

[Outside-In Requirements](011-outside-in-api-requirements.md), [Executable Documentation](027-examples-and-executable-documentation.md), [Mocking and Exploration](029-mocking-and-consumer-exploration.md), [OAuth Flows](043-oauth-authorization-flows.md), [Scope Design](045-scope-and-permission-design.md), [Rate Limits](039-rate-limits-and-quotas.md), [Deprecation and Sunset](084-deprecation-and-sunset.md), [Consumer Evidence](085-consumer-inventory-and-usage-evidence.md), [API Product Ownership](089-api-product-ownership.md), and [Contract Testing](094-contract-testing.md) define the portal's inputs. Readiness review verifies the result.

## Governing Question

How should teams design a portal/catalog and onboarding operating model that serves distinct consumer personas, preserves authoritative truth and security, makes the golden path genuinely executable, and improves through evidence across the API lifecycle?

## Why This Matters

An API is unusable if intended consumers cannot find it, understand whether it fits, obtain correct access, complete a representative task, handle errors, and reach an owner. Integration cost becomes organization-wide duplication: meetings, copied snippets, shared credentials, unofficial gateways, stale SDKs and risky production experiments.

A portal can compress this cost by joining catalog, task documentation, live contract, sandbox, registration, credentials, policy, support and lifecycle. Internal platforms also need this product surface; “the source is in another repository” does not scale to hundreds of teams.

But centralization can centralize error. A stale portal can be more dangerous than missing docs because it looks authoritative. Self-service credentials can expand privilege. A try-it console can leak tokens or execute production mutations. A catalog can expose internal topology. Metrics can reward page views while users abandon approval queues.

The durable design treats onboarding as a socio-technical workflow with sources of truth, trust boundaries, measurable stages, owners, exceptions and recovery—not a website redesign.

## Prerequisites and Retrieval

Retrieve [Outside-In Requirements](011-outside-in-api-requirements.md), [API Contracts](021-api-contracts-and-behavioral-guarantees.md), [OpenAPI](023-openapi-structure.md), [Examples and Executable Documentation](027-examples-and-executable-documentation.md), [Contract-First and Code-First](028-contract-first-and-code-first-workflows.md), [Mocking](029-mocking-and-consumer-exploration.md), [Credential Handling](042-credential-and-token-handling.md), [OAuth Flows](043-oauth-authorization-flows.md), [Scope Design](045-scope-and-permission-design.md), [AsyncAPI Contracts](063-asyncapi-contracts.md), [Deprecation](084-deprecation-and-sunset.md), [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md), [Contract Governance](088-schema-registries-and-contract-governance.md), [Product Ownership](089-api-product-ownership.md), and [Contract Testing](094-contract-testing.md).

Retrieve consumer personas/tasks/journeys and support evidence; API/service catalog and authoritative metadata sources; contracts/docs/examples/SDKs; identities/organizations/apps/credentials/scopes; approval policies; sandbox/production differences; quotas/pricing/terms/data classification; versions/changelog/deprecation/usage; status/SLO/runbooks; search analytics and zero-result queries; onboarding funnel/times/errors/tickets; accessibility/localization; portal architecture/availability/security/privacy; owners and governance.

## Learning Objectives

After completing this module, you can:

1. distinguish a developer portal, API catalog, documentation site, service catalog, gateway console and support system;
2. map persona-specific onboarding from discovery through production operation and retirement;
3. define authoritative metadata, provenance, freshness, validation and ownership for every portal surface;
4. design task-oriented quickstarts, reference docs, concepts, errors, examples, SDKs and migration guides as tested products;
5. automate application registration, approval, credential issuance, scope/quota selection, rotation and revocation safely;
6. specify sandbox fidelity, isolation, data, reset, limitations and production promotion evidence;
7. build accessible search/navigation and audience/tenant authorization without leaking private APIs;
8. model portal availability, control-plane failure, abuse, supply chain, analytics privacy and recovery;
9. measure TTFMS, conversion, wait/service time, failure recovery, support and integration outcomes; and
10. govern lifecycle/change/deprecation so documentation and tools evolve with deployed consumers.

## Core Exposition

### Segment consumers by task and trust

Identify internal service teams, web/mobile developers, external public developers, contracted partners, integrators, administrators, auditors and support. Their discovery rights, technical depth, legal/organization verification, sandbox data, credentials, approval and support differ.

For each persona, write jobs: evaluate fit, estimate cost/limits, authenticate, create an order, subscribe to an event, recover from error, rotate key, migrate version, diagnose outage. Organize around these tasks rather than provider org chart or endpoint alphabet.

Map trust boundaries: anonymous/public, authenticated developer, verified organization, registered application, sandbox, production, privileged/high-risk data. Audience authorization applies to catalog metadata and documentation as well as runtime APIs. Search indexes/caches must enforce it.

### Define portal versus authority

The portal is a composed view and workflow. Canonical API contract may live in a governed registry/repository; runtime gateway owns enforcement; identity system owns users/apps/credentials; product record owns audience/lifecycle/terms; service catalog owns owner/system relation; status system owns incidents; support system owns tickets.

Define each field's source, update path, validation, freshness SLO and conflict rule. Avoid copying descriptions/scopes/limits into multiple editable databases. Derived views show source revision and last verified time.

Backstage's current software catalog documentation describes centralized ownership/metadata harvested from owner-maintained descriptors and cautions that a catalog can be a caching/view mechanism rather than the ultimate source for every fact. The general lesson is explicit provenance, not adoption of a particular product.

Portal unavailability must not change runtime authorization, rate limits or contract. Preserve offline/exported docs/SDKs where justified and an emergency support/access-revocation path. Conversely, stale cached portal content must clearly show age and not issue unsafe credentials.

### Build a governed API catalog

Required record: stable ID/name/title/description; product/domain/system; owning team and support/on-call; lifecycle/audience; interface style/protocol; canonical contract/version/digest; environment/base discovery; auth/scopes; data classification/residency; quotas/pricing/terms; SLO/status; dependency/replacement; changelog/deprecation/sunset; documentation/SDKs; consumer inventory and last verification.

Validate owner exists, contract resolves, links render, environment issuer/base URL is allowed, lifecycle transitions follow policy, private entries have audience rules, and deprecated entries name migration/replacement. Reject orphan records instead of displaying false authority.

Search by consumer vocabulary, capability/task, domain, protocol, lifecycle, audience and owner. Synonyms and zero-result queries reveal terminology gaps. Rank supported/current APIs above experimental/deprecated; never hide lifecycle badges.

Catalog graph helps navigate owner, API, service, system, resource and consumer, but it is not runtime dependency truth unless sourced/verified accordingly. Avoid leaking internal topology to external audiences.

### Design documentation layers

Start with “Is this for me?”: capability, audience, use cases/non-goals, maturity, region/data, price/quota, prerequisites and alternatives. Then a task quickstart that achieves representative meaningful success. Follow with concepts, auth, operation/reference, errors, pagination/idempotency/concurrency, limits/performance, events/ordering/replay, SDKs, testing, production checklist, operations/status/support and lifecycle/migration.

Machine-readable OpenAPI/AsyncAPI/GraphQL/Protobuf artifacts are authoritative inputs for operation/schema reference and tools. They do not fully express business semantics, task sequence, authorization meaning, consistency, billing, safe retries or operational policy. Add human explanation without duplicating generated field tables.

Use docs-as-code or another owner-reviewed versioned workflow so docs change with contract/implementation. Backstage TechDocs is a current example of documentation stored alongside code; the durable requirements are review, versioning, preview, validation, ownership and publication provenance.

Preserve documentation for supported older versions and deep-link stable anchors. Show “applies to” API/environment/SDK versions and last verification. Deprecation banners link to migration and deadlines, not merely “deprecated.”

### Make examples executable and safe

Examples use non-secret placeholders, current base discovery, least scopes, realistic task data, explicit expected status/body/headers and errors. Cover idempotency, pagination, rate limiting, retries/deadlines and outcome lookup where relevant.

Continuously run quickstarts and snippets against controlled sandbox through public gateway/auth. Validate from a clean consumer environment. Contract tests keep examples/SDK shapes aligned; integration tests catch configuration and dependency drift.

A browser “try it” console is a privileged client: restrict origins/CSP, prevent token persistence/leak to analytics, redact history, bind environment visibly, default read-only/synthetic, confirm mutations, protect CSRF/SSRF, rate limit and isolate tenants. Never let pasted production secrets enter third-party analytics.

Examples must teach error recovery, not just happy `200`. A meaningful success verifies the task outcome and gives a way to inspect/undo/reset it.

### Offer SDK and tooling without hiding HTTP

Generated SDKs reduce serialization/auth/retry boilerplate, but declare language/runtime/contract versions, support tier, release cadence, dependencies, signing/provenance, compatibility and deprecation. Test generated packages against the real contract and examples before publication.

Teach the underlying protocol/contract enough to debug SDK behavior. Do not silently embed unsafe retries, infinite timeouts, global credentials or telemetry. Provide minimal direct-request path as diagnostic reference.

CLI, collections, mocks and templates need the same provenance/lifecycle/security as SDKs. Scan dependencies and packages; prevent namespace/package substitution; sign/reproduce releases where supported.

### Register applications and issue credentials

Separate human developer identity, organization, application/client, environment and credential. Verify email/domain/organization and ownership according to risk. Application record includes owner/support contacts, redirect/callback/webhook URIs, purpose, environments, data/scopes, quota, lifecycle and security metadata.

RFC 7591 defines an OAuth dynamic client registration protocol; automation does not imply open anonymous registration. Use initial access tokens/software statements/approval as policy requires. RFC 8414 defines authorization-server metadata discovery; clients must validate issuer exactly. Portal should derive supported endpoints/methods from trusted authority rather than transcribing them.

Credential types match client: public clients avoid secrets they cannot protect; confidential workloads use appropriate key/certificate/private-key mechanisms. Display secrets once, never log or put in URL/source; offer secure retrieval/delivery, expiry, rotation overlap, revocation and compromised-key response.

Scopes/permissions are task/resource/action bounded, not opaque provider internals. Default least privilege, explain data/effects, and require approval only where risk demands it. Sandbox credentials cannot call production; production issuance is a separate evidence gate.

### Design approvals as policy, not queues

Automate low-risk decisions using declared predicates: verified owner/application, allowed callback domain, training/terms where required, scope/data tier, security profile, quota/cost, contract integration test, support contacts and rotation readiness. Policy result includes reasons and remediation.

Escalate high-risk data, money movement, privileged administration, unusual quota, external publication or exceptions to named accountable approvers. Record request/evidence/decision/conditions/expiry. No approvals in untracked chat.

Measure service time separately from wait time. If a two-minute review waits five days, optimizing the form misses the constraint. Set response objectives, substitution/escalation, expiry and appeal.

Production promotion checks exact application/environment, scopes, callbacks/webhook verification, quota/capacity, idempotency/retry, monitoring/support and key rotation; it does not merely copy sandbox credentials.

### Specify sandbox fidelity

Document protocol/contract/version parity, auth/scopes, rate limits, data/tenant isolation, deterministic fixtures, external fakes, time/asynchrony, failure controls, persistence/reset, availability/SLO, unsupported behaviors and promotion differences.

Use per-consumer synthetic tenants/data and exact resets. Prevent cross-consumer discovery and production egress/effects. Provide known scenarios for success/error/retry/webhook/event, plus self-service cleanup.

Monitor drift by running the same contract/quickstart suite against sandbox and production-safe endpoints; exceptions have owners/expiry. A sandbox that always succeeds teaches unsafe assumptions.

Capacity/load testing needs a dedicated policy/environment; onboarding sandboxes should protect fairness and provide explicit quotas rather than becoming accidental benchmarks.

### Support operation and lifecycle

Portal continues after first call: application/credential inventory, usage/quota/billing, audit, rotation/revocation, incidents/status, changelog, deprecations, migration, tickets/community and runbooks. Show consumer-specific impact without leaking other tenants.

Support entry captures safe diagnostics: application ID/environment, operation/route, time, request/trace ID, error/problem code, SDK/version—not secrets/body by default. Publish response expectations and escalation for production incidents/security.

Status distinguishes portal, auth/registration, gateway/API, sandbox and dependencies. A green portal does not mean API health; an unavailable portal must not block credential revocation or incident communication.

Deprecation targets known application owners through multiple channels, includes replacement/diff/migration tests/deadline, and tracks usage evidence. Preserve old docs/SDKs until support ends; mark them clearly. Archive/remove credentials/catalog entries safely after verification.

### Make the experience accessible and global

Use semantic navigation, keyboard operation, contrast, focus/error identification, screen-reader labels, captions/text alternatives, responsive layout and non-color status. W3C WCAG 2.2 supplies current accessibility criteria; test with automation and humans.

Localize task content where required while keeping protocol tokens/error codes stable. Dates/time zones, currencies, addresses, Unicode and legal/region differences must be explicit. Search synonyms and language fallback should not mix incompatible versions.

Design for slow networks and constrained devices: compact pages, downloadable specs/docs, resumable flows, no required heavyweight console for credential rotation.

### Secure the portal and supply chain

Threat-model account takeover, organization/app ownership spoofing, private catalog enumeration, credential theft, malicious specs/Markdown/examples, stored XSS, SSRF through URL import/try-it, package substitution, webhook verification abuse, quota fraud, analytics leakage and admin misuse.

Apply MFA/strong sessions for sensitive actions, reauthentication, least-privilege admin, separation of duties, audit, rate/abuse controls, content sanitization, URL allowlists/network isolation, dependency/package integrity, CSP and secret scanning. Do not render arbitrary contract content with unsafe HTML or fetch arbitrary references server-side.

Back up and rehearse recovery of catalog/workflow state; credentials remain governed by identity authority. Validate import processors and stale-cache behavior. Incident response can revoke applications/credentials and publish notices without the normal portal path.

### Measure the onboarding funnel responsibly

Define events at stage outcomes: search/discovery; relevant API viewed; quickstart begun; registration validated; credential issued; first valid authenticated call; first meaningful task outcome; production request/approval/issuance; first production success; active healthy integration; rotation/migration.

Measure conditional conversion, time and failure reason by bounded persona/audience/API/cohort; separate service and wait time. With seven 90% conditional stages, end-to-end is $0.9^7\approx0.478$. Improving the worst stage or removing unnecessary steps has compounding effect.

Track zero-result search, doc task completion, snippet failures, auth/error codes, support contacts before success, approval aging, sandbox drift, credential exposure/revocation, production defects, time to migrate and consumer satisfaction. Page views/downloads are supporting signals, not success.

Minimize analytics data; use consent/purpose/retention/access policy, pseudonymize where appropriate, and never capture credentials/request bodies. Internal developer analytics can still be sensitive employment data.

### Operate improvement as a product loop

Observe onboarding sessions/support tickets/search failures, run usability/accessibility studies, test quickstarts from clean environments, review incidents and prioritize friction by task impact and risk. Assign portal/API/identity/support ownership and SLOs.

Use progressive rollout for navigation, registration and SDK changes; retain rollback and dual paths. A/B testing must not expose consumers to weaker security or incompatible documentation.

Publish roadmap/changelog for portal behavior. Retire features only with usage/support evidence. The successful endpoint is independently operating consumers with safe lifecycle—not fewer clicks at any cost.

## Definitions and Notation

Let stages $i\in\{D,E,R,C,I,P,O\}$ have entrants $n_i$, completers $n_{i+1}$, conditional conversion $p_i=n_{i+1}/n_i$, service time $s_i$, and wait time $w_i$. End-to-end completion is $\prod_i p_i$ for the same defined cohort, while total elapsed flow time is $\sum_i(s_i+w_i)$.

A **portal record** is a derived/authoritative metadata view with provenance. **TTFMS** ends at a task-level verified outcome. **drift** is disagreement among contract/runtime/docs/examples/SDK/sandbox/policy. **production promotion** is a policy decision about a particular consumer application and evidence set, not a global API release.

## Mechanisms, Invariants, or Proof Structure

**Funnel-product derivation.** Since $p_i=P(stage_{i+1}\mid stage_i)$, the chain rule gives end-to-end completion as their product for a consistently defined cohort. Seven stages at 0.9 yield 0.4783, showing locally “good” stages can produce poor total completion.

**Flow-time accounting.** Every stage contributes active service and queue/wait. Reducing a two-minute form to one minute barely changes a five-day approval flow; automation or queue ownership is the leverage.

**Authority counterexample.** Portal cache says scope X is available after the identity authority removed it. Issuance/runtime rejects the consumer. Therefore a rendered portal value cannot be treated as authority without provenance/freshness/conflict behavior.

**Meaningful-success argument.** A health/ping `200` exercises reachability but not task schema, authz, effects, idempotency or outcome. It cannot entail integration readiness; TTFMS must end at a representative task and verified result.

## Alternatives and Trade-Offs

A centralized portal improves discovery/consistency but can become bottleneck/blast radius; federated owner sources scale ownership but need schema, validation and search. Use authoritative federated metadata with a governed aggregated experience.

Generated reference stays synchronized with contract but lacks tasks/meaning. Handwritten guides explain intent but drift. Generate structural reference and test owner-written concepts/tasks against exact versions.

Automatic registration/approval reduces wait and toil but can automate privilege mistakes. Manual review adds judgment but becomes opaque queue. Encode low-risk policy and reserve human approval for explicit risk/exception.

Shared sandbox is cheap but leaks/interferes; per-consumer environments isolate but cost and drift. Logical tenant isolation with synthetic data plus dedicated high-fidelity environments can balance.

First-party SDKs improve experience but multiply languages/releases/security burden. Tier support by usage/risk; offer contract and community SDK guidance without implying unsupported guarantees.

## Failure Modes and Misconceptions

- “Portal equals documentation” omits access, lifecycle, support and operation.
- “Catalog entry means supported” ignores owner/lifecycle/evidence.
- “Generated reference is complete” omits task and semantic guarantees.
- “Fewer clicks is better” can remove necessary security understanding.
- “Self-service means no policy” automates privilege escalation.
- “Sandbox is production-like” requires explicit verified dimensions.
- “A ping is first success” does not prove a consumer task.
- “SDK hides complexity” can hide unsafe retries/auth/version behavior.
- “Secret shown in browser is safe” ignores history/extensions/analytics.
- “Hashed user ID is anonymous” can remain linkable/guessable.
- “Search can index everything” leaks private API metadata.
- “Portal outage is API outage” indicates dangerous coupling.
- “Deprecation banner migrated consumers” lacks usage evidence.
- “Page views prove adoption” measures attention, not correct integration.

## Worked Examples

### Example 1

Seven onboarding stages each convert 90%; total is $0.9^7\approx47.8\%$. Registration improves to 99%, but a 60% production approval still dominates. **Conclusion:** optimize the full funnel.

### Example 2

Approval takes two minutes of work after five days queued. Form redesign saves one minute; policy automation saves nearly five days. **Conclusion:** separate wait from service time.

### Example 3

Search ranks retired Orders v1 above v2. Lifecycle-aware ranking/banner/migration and usage targeting correct it. **Conclusion:** discoverability must include lifecycle truth.

### Example 4

Quickstart stores admin token in source. Replace with sandbox app, least scope, runtime secret injection and rotation lesson. **Conclusion:** examples teach security behavior.

### Example 5

Sandbox accepts payment without idempotency while production requires it. Shared contract/quickstart parity test fails. **Conclusion:** document and continuously test fidelity.

### Example 6

Portal cache lists removed OAuth method. RFC 8414 issuer metadata is authoritative and exact issuer validation rejects mismatch. **Conclusion:** derive capability from trusted authority.

### Example 7

Try-it console sends pasted token to analytics replay. Revoke, purge, disclose, disable sensitive capture and redesign isolation. **Conclusion:** portal UX is a security boundary.

### Example 8

Generated Python SDK adds automatic POST retry without idempotency. SDK contract/failure tests reject release. **Conclusion:** SDK policy is part of API behavior.

### Example 9

Internal catalog reveals private fraud API to contractor search. Audience-filter index and authorization tests close leak. **Conclusion:** metadata itself can be sensitive.

### Example 10

Portal is down during credential compromise. Independent identity revocation and status/support path still work. **Conclusion:** control-plane failure must not prevent safety response.

## Cross-Program Connections

[Human-computer and software design concerns](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supply task models, domain language and usable boundaries.

[Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies docs/release pipelines, artifact provenance, SLOs, incident/status, progressive delivery and recovery.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies identity, credentials, least privilege, trust boundaries, secret/data handling, audit, abuse resistance and incident response.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies portals/catalogs as products, golden paths, templates, self-service workflows, ownership, policy and developer-experience measurement.

[Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies environment provisioning, identity integration, sandbox isolation, networking, quotas, observability and cost.

## References

1. OpenAPI Initiative, [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html), 19 September 2025.
2. AsyncAPI Initiative, [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0).
3. Backstage, [Software Catalog](https://backstage.io/docs/features/software-catalog/).
4. Backstage, [TechDocs](https://backstage.io/docs/features/techdocs/).
5. IETF, [RFC 7591: OAuth 2.0 Dynamic Client Registration Protocol](https://www.rfc-editor.org/rfc/rfc7591.html), July 2015.
6. IETF, [RFC 8414: OAuth 2.0 Authorization Server Metadata](https://www.rfc-editor.org/rfc/rfc8414.html), June 2018.
7. W3C, [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/), 5 October 2023.

## Exercises

### Exercise 1

Map the onboarding stages, authority, evidence, risks and metrics for an external partner integrating a payment API from discovery through first production operation.

### Exercise 2

Stage conversions are 80%, 90%, 75%, 95%, 85%, 60%, and 90%. Compute end-to-end conversion and identify how to prioritize improvements without using conversion alone.

### Exercise 3

Design a secure self-service application registration, sandbox credential, scope/quota approval, rotation and production promotion workflow.

### Exercise 4

Compare authoritative repository/registry data, a central catalog cache, handwritten portal content, generated references and runtime discovery; define conflict/freshness behavior.

### Exercise 5

Diagnose a portal incident with stale docs, leaked try-it tokens, cross-tenant sandbox data, orphan API owner, broken SDK, five-day approval queue and hidden deprecation usage.

## Answers to the Exercises

### Answer 1

Discovery authority is audience-filtered product/catalog record with owner/lifecycle; evidence is search relevance and supported API. Evaluation uses canonical contract plus task concepts, data/region/terms/limits and status. Registration verifies developer organization and application/callback/support metadata through identity/client registry. Credential issuance uses sandbox-only least-privilege credential shown/delivered securely once with audit/rotation/revoke. Integration runs task quickstart through gateway/auth in isolated synthetic tenant, verifies idempotent payment and outcome plus errors. Production approval evaluates organization/app ownership, scopes/data/risk, callback/webhook, contract/security/capacity/quota/support/rotation; records policy decision. Production issuance is separate credential/environment. First operation measures correct effect and telemetry/support readiness. Track conditional conversion, service/wait, failure/recovery and tickets per stage, TTFMS and time to production; never capture tokens/card data. Authorities remain identity/gateway/payment state—not portal cache.

### Answer 2

Product is $0.80\times0.90\times0.75\times0.95\times0.85\times0.60\times0.90\approx0.235$, about 23.5%. The 60% stage is a candidate, but prioritize by consumer value, preventable failure volume, time/cost, security necessity, persona mix and downstream impact. A low conversion may be correct risk rejection; a high conversion may hide unsafe approval. Decompose reasons, service versus wait time, recovery, cohorts and support contacts. Improve discovery/registration too because product effects compound. Remove unnecessary steps, automate safe policy and test tasks, while preserving risk controls. Recompute using consistent cohorts and verify first meaningful/production outcomes rather than page events.

### Answer 3

Authenticate developer strongly, verify organization/domain and application owner/support/callback/webhook metadata. Policy validates audience/purpose/data, redirects, app type and requested sandbox scopes; issue short-lived/rotatable sandbox-bound credential via secure one-time delivery, never URL/log/source, with audit/revoke. Provision isolated synthetic tenant/fixtures/quotas/reset; run contract quickstart and negative auth/idempotency tests. Production request references exact app and evidence, requires task-bounded scopes, quota/capacity, security profile, terms where applicable, callback/webhook ownership, support/on-call and rotation; automate low risk, route exceptions/high-risk scopes to named approver with expiry. Issue separate production credential/key/certificate, test overlap rotation and compromise revocation, notify owners, inventory last use and retire dormant apps through policy.

### Answer 4

Contract repository/registry is authority for interface/version/digest; identity/gateway discovery is authority for issuer/endpoints/methods; product/service records own audience/lifecycle/owner/support/terms; runtime telemetry owns observed usage/health. Catalog ingests validated references and is an indexed cache/view with source revision/freshness. Generated reference derives from exact contract. Handwritten tasks/concepts are owner-reviewed/versioned and tested against contract/runtime. Portal composes them, showing provenance/version/last verified. On conflict fail publication or mark unavailable/stale; never silently choose. Credential workflows query authority at decision time. Define freshness SLO and bounded last-known-good for nonsecurity content; security/lifecycle/issuer changes invalidate cache. Preserve versioned old docs while supported and test reconciliation/alerts.

### Answer 5

Stabilize: revoke leaked tokens, purge/redact analytics/artifacts and investigate use; disable try-it sensitive capture/mutations. Isolate sandbox tenants, stop unsafe access, preserve evidence and notify affected consumers. Mark stale docs/SDK unavailable with exact versions and publish corrected known-good path. Assign incident owner for orphan API and freeze new production grants/deprecation removal. Provide tracked approval triage/escalation without weakening policy. Reconcile canonical contract/runtime/issuer/limits, rerun quickstarts and SDK contract/security tests, validate audience search. Diagnose five-day queue by wait/service/reason and automate safe predicates. Restore consumer usage inventory and targeted deprecation/migration. Durable controls: source provenance/freshness gates, owner/lifecycle validation, per-tenant sandbox/reset tests, CSP/token isolation/no session replay, package signing/dependency scans, approval SLO/backup, usage evidence and portal/identity independent revocation/status recovery drill.
