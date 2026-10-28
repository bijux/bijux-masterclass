---
module_id: API-084
program: API & Service Engineering
level: 2
module_number: 84
title: Deprecation and Sunset
status: complete
last_verified: 2026-09-02
---

# Deprecation and Sunset

## One-Page Review

### Governing question

How does an API provider move a supported consumer from an old contract to a replacement, with discoverable notice, unchanged behavior during the promised window, measurable migration, safe extensions/exceptions, and deterministic retirement rather than surprise failure?

### Essential definitions

- **deprecation** declares that a contract remains available but should receive no new dependencies and existing consumers should migrate.
- The **deprecation date** is when deprecated status takes effect; deprecation itself does not remove or silently weaken behavior.
- **sunset** is the planned time after which the contract is expected to become unavailable or unsupported.
- **retirement** is the executed removal/disablement after readiness and authorization; a sunset date is a plan, not proof that retirement is safe.
- A **replacement** is the supported target contract and migration path, not merely a newer name.
- A **notice window** spans deprecation notice through sunset and must cover contractual, client-release, dormant-workload, replay, and recovery horizons.
- **migration evidence** identifies consumers, use, state, artifacts, and tested outcomes that have moved—not only reduced request volume.
- A **sunset exception** is a scoped, owned, time-bounded extension or emergency deviation with explicit risk and communication.

### Central model, mechanism, or theorem

Let $T_a$ be announcement, $T_d$ deprecation, $T_s$ sunset, and $T_r$ executed retirement, with

$$
T_a\le T_d\le T_s\le T_r.
$$

Let $H$ be the maximum required support horizon across agreements, client release/adoption, dormant jobs, queued/replayed work, rollback, and disaster recovery. Ordinary retirement requires $T_s-T_a\ge H$ plus conjunctive readiness evidence: replacement equivalence, credible inventory, migration of every required consumer/state/path, notice delivery, operational readiness, and authorized exception resolution. Traffic decay alone cannot satisfy the conjunction.

### Critical invariants

The deprecated surface keeps its promised correctness, security, availability, limits, and error behavior until sunset unless a governed emergency exception says otherwise. Deprecation scope, reason, replacement, semantic differences, migration steps, dates/timezone, support, owner, and terminal behavior agree across runtime, specification, SDKs, portal, changelog, and direct notice.

New adoption is discouraged or gated without harming existing entitled consumers. Every known consumer has an owner/status/deadline and replacement tests. Dormant, batch, partner, offline, webhook, replay, failover, backup, and rollback paths are accounted for. Dates do not move silently; exceptions are explicit. Retirement returns a stable actionable outcome, preserves audit/evidence, and removes old code/data/routing only after recovery horizons permit.

### Common failures

Equating deprecated with disabled; adding warnings that alter signed payloads unexpectedly; announcing only in a blog; marking OpenAPI/GraphQL deprecated without a replacement; no machine runtime signal; `Sunset` earlier than `Deprecation`; vague timezone; repeatedly extending dates; measuring calls but not consumers; 99.9% migration hiding a critical quarterly job; blocking new use by breaking existing clients; letting old behavior rot before sunset; replacement lacks parity/capacity/auth; deleting schemas/idempotency/state needed for replay; retiring one region first accidentally; returning `404` without migration context; automatic client fallback; emergency break mislabeled sunset; and leaving adapters/routes/permissions forever after migration.

### Compact example

An endpoint is announced on 1 January, deprecated on 1 February, and planned to sunset on 1 August. Responses carry the standards-defined `Deprecation` date, a `Link` to a migration guide, and `Sunset`; OpenAPI/SDK/docs agree. By July, 99.9% of calls use the replacement, but the remaining old traffic is a quarterly settlement job. Retirement stays blocked until that owned critical consumer migrates and its dormant execution is tested. **Conclusion:** traffic percentage is not retirement evidence by itself.

### Connections

[Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), [Additive and Breaking Changes](082-additive-and-breaking-changes.md), and [Versioning Strategies](083-versioning-strategies.md) define the compatibility boundary and target. The next module builds the consumer inventory and usage evidence needed to make sunset decisions defensible.

## Governing Question

What lifecycle, notice, evidence, migration, exception, and terminal-response controls let a provider retire an API surface without silently breaking supported consumers, state, operations, security, or recovery?

## Why This Matters

Deprecation is often treated as an annotation and sunset as a date. Neither moves a consumer. An integration needs a replacement whose semantics it understands, code and state changes, test environments, release approval, and time to deploy. Mobile/offline clients, quarterly jobs, partners, webhooks, archived events, disaster tools, and rollback artifacts may not appear in recent traffic.

Keeping everything forever also causes harm. Deprecated handlers accumulate vulnerabilities, obsolete dependencies, inconsistent authorization, test burden, operational incidents, and cognitive load. Teams avoid improvements because they cannot prove who uses old behavior. A lifecycle must create credible movement and a justified terminal point.

The standards make an important distinction. RFC 9745 defines an HTTP `Deprecation` response field and `deprecation` link relation and states that declaring deprecation does not itself change the resource's behavior. RFC 8594 defines `Sunset` to communicate when a resource is expected to become unresponsive. Notice and removal are different events.

A durable program combines normative policy, exact scope, replacement design, multi-channel and runtime notice, owned inventory, migration tooling, evidence, capacity/security operations, exception governance, and deterministic retirement/cleanup. It protects consumers during transition while preventing “temporary” legacy from becoming permanent.

## Prerequisites and Retrieval

Retrieve [Errors with Stable Meaning](003-status-codes-and-error-meaning.md), [Headers and Metadata](004-headers-and-metadata.md), [Content Negotiation](005-content-negotiation.md), [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [OpenAPI Structure](023-openapi-structure.md), [GraphQL Schema Design](055-graphql-schema-design.md), [Event Versioning](069-event-versioning.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), [Additive and Breaking Changes](082-additive-and-breaking-changes.md), and [Versioning Strategies](083-versioning-strategies.md).

Retrieve stability/support agreements; exact deprecated surface and replacement; contract/SDK/docs/catalog artifacts; consumer registry, auth principals, telemetry and data-retention limits; partner/mobile/offline/batch/replay/failover/recovery populations; current Deprecation/Sunset/link/spec annotations; dates/timezones; migration guides/tools/test environments; replacement parity/capacity/security; old state/schema/idempotency/tokens; exceptions; communication contacts/channels; rollback plan; and post-retirement cleanup/archival obligations.

## Learning Objectives

After completing this module, you can:

1. distinguish announcement, deprecation, sunset, retirement, removal, and post-retirement cleanup;
2. calculate a notice window from contractual, consumer, dormant, replay, rollback, and recovery horizons;
3. define exact scope, replacement semantics, terminal behavior, ownership, and dates;
4. publish coherent runtime HTTP, OpenAPI, GraphQL, SDK, portal, changelog, and direct notices;
5. preserve behavior/security/SLOs for existing consumers while preventing new dependency growth;
6. build per-consumer migration plans with test, release, state, and effect evidence;
7. distinguish request-volume decay from credible consumer and recovery-path retirement evidence;
8. govern extensions and urgent security/legal/corruption exceptions transparently;
9. rehearse sunset, stable terminal outcomes, rollback, capacity, and incident response; and
10. remove obsolete routes, code, state, permissions, docs, alerts, and artifacts without destroying audit/replay evidence.

## Core Exposition

### Define lifecycle states and transitions

Use explicit states such as proposed, active/stable, deprecated, sunset-scheduled, retired, and removed/archived. Define entry criteria, allowed changes, support/SLO, owner, and exit evidence for each. Preview/experimental channels can have different policy but still need dates and terminal behavior.

Announcement makes an upcoming lifecycle change discoverable. Deprecation says stop creating dependencies and begin migration while the contract still works. Sunset states expected unavailability. Retirement performs that policy decision. Physical code/data removal can follow later after rollback, backup, replay, audit, and incident horizons expire.

Do not collapse state into one Boolean `deprecated`. A field can be marked deprecated with no sunset yet; a version can have a sunset but remain operational; a route can be retired while archives/adapters remain for audit.

Transition state is authoritative and consistent across catalog, contract, runtime, SDK, docs, support, and operations. Conflicting dates destroy trust.

### Scope the deprecation exactly

Name service/version/interface/operation/method/path/media type/header/field/enum/error/SDK symbol/event/webhook/channel/region/tenant scope. Avoid “v1 is deprecated” when only one operation is affected, or “field deprecated” when its enum value is the target.

State whether the notice applies to the individual resource URI or a wider API family. RFC 9745's HTTP field applies to the resource identified by the response unless wider scope is documented. Ensure clients can map runtime notice to the correct contract element.

Record stability level and governing policy/agreements. A stable public API, internal service, beta feature, and security-vulnerable operation may have different notice obligations. Exceptions do not broaden silently.

Freeze new expansion of the deprecated scope. Necessary security/reliability corrections continue, but do not add attractive new features that create fresh migration debt.

### Design the replacement before notice

A replacement must be available or have a credible release schedule, ownership, capacity, security, documentation, SDKs, test environment, and migration support. Describe semantic differences, not just map old route to new route.

Provide field/operation/error/auth/ordering/pagination/consistency/idempotency/side-effect mapping. State which behavior cannot be preserved and what consumer decision changes. Include data/state migration, webhook/event subscriptions, credentials/scopes, quotas, network allowlists, and observability.

Test that the replacement serves actual use cases and boundaries. A technically newer API that omits a critical workflow is not a replacement. Shadow safe reads and reconcile commands through idempotent/simulated paths.

Do not deprecate with “contact us” as the only migration guide. Make common migration self-service and reserve support for exceptions.

### Derive the notice window

Let $H$ be the maximum of contractual minimum, consumer development/release/adoption, partner procurement, mobile/offline update, longest dormant/batch interval, queued-message/webhook retry/replay, rollback artifact, and disaster/backup horizon—plus contingency appropriate to risk.

The window begins when actionable notice and a usable replacement are available, not when an internal ticket was created. If the migration guide or SDK arrives later, the effective notice window starts later for affected consumers.

Dates include exact instant/timezone. Ensure $T_a\le T_d\le T_s$ and RFC 9745's requirement that `Sunset` not precede `Deprecation`. Avoid end-of-month ambiguity and choose operationally staffed times rather than peak/freeze periods.

A uniform minimum may be policy, but higher-risk/slow consumers need longer. Preview may permit shorter windows if that promise was explicit before use. Do not retroactively declare a stable surface preview.

### Publish machine-readable HTTP notice

RFC 9745 defines `Deprecation` as a Structured Field date, plus the `deprecation` link relation for documentation. Send it on responses in scope, with an authenticated HTTPS migration/policy link. It can announce a future or past deprecation date.

RFC 8594 defines `Sunset` as an HTTP-date indicating expected unresponsiveness. Use it only when a credible date exists. Keep it at or after deprecation. The `sunset` link relation can point to lifecycle information.

Do not invent incompatible date formats under those standard field names. Test gateways, proxies, CORS exposure, SDK access, caches, signatures, and duplicate-header behavior. Adding headers should not mutate signed canonical input unexpectedly; update signature policy coherently.

Runtime notice reaches active traffic but not dormant consumers. It complements rather than replaces direct and artifact channels.

### Mark specifications, schemas, and SDKs

OpenAPI's operation `deprecated` flag tells consumers to refrain from use; pair it with replacement/date/migration extensions or linked documentation under local policy. Keep exact baseline artifacts and generated portal/SDK warnings synchronized.

GraphQL provides `@deprecated` with a reason for fields and enum values. Give a useful replacement in the reason, preserve resolver behavior during the window, and use observed operation documents before removal. Schema introspection warnings cannot reach persisted/dormant clients alone.

For Protobuf/SDKs, use supported deprecation annotations to generate compiler/editor warnings without removing symbols or changing wire behavior prematurely. Avoid warning-as-error rollout that instantly breaks builds unless contractually staged.

Events/webhooks include catalog/schema documentation and direct subscriber notice; do not change historical event meaning. Keep old schemas/readers through retention/replay or provide governed upcasters.

### Communicate through independent channels

Use runtime headers/metadata, API portal/catalog, normative spec, SDK/compiler warnings, changelog/release notes, dashboards, account/email/webhook notifications, partner managers, support tickets, and direct owner outreach. Each covers different populations and failure modes.

Messages state: exact scope and consumer identity if known; reason; announcement/deprecation/sunset/retirement dates; unchanged pre-sunset guarantee; replacement; semantic/auth/quota differences; migration/test steps; support/exception process; terminal behavior; and owner/status page.

Repeat notice at meaningful milestones without alert fatigue. Track delivery, bounce, acknowledgement, and owner response. Public broadcast cannot prove the responsible engineering team received or acted.

Use one canonical lifecycle record to generate channels so dates/links do not drift. Human overrides are audited.

### Stop new adoption safely

Deprecation should prevent new consumers from deepening debt while existing entitled clients continue normally. Hide deprecated options from “recommended” docs/code generators, warn on new registrations, require an exception for new credentials/subscriptions, and steer discovery to the replacement.

Do not reject every unrecognized client as “new” or throttle the deprecated endpoint to make migration happen. Those are behavior changes before sunset. Use identity/registration evidence and preserve contractual traffic.

Internal policy can block new code references in CI or platform catalogs while allowing maintained existing dependencies. Waivers name owner, need, expiry, and migration plan.

Avoid adding new features to the old surface except necessary safety/compatibility support. Feature parity should converge toward the replacement.

### Build a credible consumer inventory

Combine registration/catalog ownership, auth principal/API key/OAuth client/mTLS identity, gateway/service telemetry, SDK/user-agent/version, contract repositories, partner/support records, webhook subscriptions, mobile releases, batch schedulers, data lineage, network policy, and direct attestation.

Map technical identity to accountable owner, business criticality, use cases/operations/fields, environment/region, volume and last/next expected use, replacement target, migration status, blocker, test evidence, and deadline. Shared credentials weaken attribution and must be decomposed.

Respect privacy and data-retention law. Hash/pseudonymize where possible; do not collect payloads unnecessarily. Document blind spots such as NAT, proxies, relays, sampling, header loss, or offline clients.

API-085 expands this discipline. For sunset, inventory credibility is a gate, not a nice-to-have spreadsheet.

### Interpret usage evidence carefully

Request percentage can hide low-volume critical consumers. Unique identities can hide many end users behind one gateway. No calls in 30 days says little about quarterly, annual, disaster, or replay paths. Sampling can miss rare use; failed/rejected calls may still represent dependence.

Track volume, unique consumers, operations/fields, business effects, error/result, SDK/version, environment/region, last seen, expected cadence, and criticality. Compare with inventory and direct confirmation.

If $U=120$ known consumers and $M=114$ migrated, $m=95\%$, not “nearly done” by default. The remaining six may dominate risk. Weighting helps prioritization but retirement requires every required consumer resolved or explicitly excepted.

A drop to zero can mean traffic shifted, telemetry broke, sampling changed, auth failed, or clients gave up. Validate instrumentation and replacement uptake/business parity.

### Manage migration as owned work

Assign provider and consumer owners. Each consumer plan covers code/config, credentials/scopes, network, data/state, SDK/spec, semantic differences, test fixtures, capacity, release window, canary, rollback, and confirmation.

Provide adapters, linters, codemods, dual-read tools, test sandbox, traffic shadow/comparison, replay fixtures, compatibility reports, and office hours where cost justifies them. Migration automation itself is versioned/tested.

Track states such as identified, contacted, acknowledged, planned, in development, tested, canary, migrated, verified, exception, and unknown. Evidence links to artifact/version/deployment and observed replacement use, not a verbal “done.”

Keep old and new effect identity/idempotency coherent during retry/cutover. Dual invocation must not create two payments/messages.

### Verify replacement parity and capacity

Parity is defined by relevant semantics: accepted inputs, values/units, errors, ordering, completeness, consistency, auth, side effects, idempotency, latency, limits, and audit—not byte equality unless required.

Shadow safe reads and compare. For writes, use simulation, one authoritative execution with dual encoding, or controlled idempotent canaries. Reconcile counts, state, and business outcomes. Investigate mismatches rather than normalize them away.

Load-test expected transferred traffic and bursts, including old consumers that migrate near deadline. Ensure quotas, rate limits, dependencies, caches, and support/on-call can absorb cutover. Replacement overload at sunset converts planned migration into incident.

Test new credentials/scopes and least privilege. Do not copy broad legacy access blindly.

### Preserve the deprecated service during the window

Continue security patching, dependencies, correctness, SLO monitoring, incident response, capacity, backup/recovery, docs, and support as promised. RFC 9745 states deprecation itself does not change resource behavior.

Do not intentionally add latency, errors, or reduced quotas to coerce migration unless policy explicitly made that a separate scheduled breaking step. Such tactics make evidence unreliable and harm supported consumers.

Freeze risky feature growth and simplify internals only through compatibility-tested changes. Keep old version included in disaster recovery and failover rehearsal until retired.

Track maintenance cost and vulnerabilities to inform urgency/exception decisions, not as permission for silent abandonment.

### Govern exceptions and date changes

A sunset extension request includes consumer/owner, criticality, blocker, completed work, requested end, risk of extension versus retirement, security/support feasibility, mitigation, milestones, and escalation. Approve the smallest scope and time.

Do not move the global date repeatedly for one consumer when a scoped adapter/allowlist or isolated extension is safer. Conversely, do not create a hidden permanent VIP endpoint. Publish externally relevant changes and synchronize all signals.

Emergency security, privacy, legal, corruption, or severe reliability risks may require shortened/absent notice. Label the breaking exception, restrict only unsafe shapes where possible, provide stable actionable errors/migration, communicate directly, and monitor impact.

Every exception has expiry and review. Missed milestones escalate before the final hour.

### Define retirement readiness as a conjunction

Require all applicable gates:

- exact scope and authorization approved;
- replacement stable, secure, documented, supported, capacity-tested, and semantically verified;
- credible inventory with every required consumer migrated, retired, or approved exception;
- old and replacement usage/business outcomes reconciled;
- direct/runtime/artifact notice obligations satisfied;
- dormant/batch/offline/partner/webhook/replay/failover/recovery paths resolved;
- state, idempotency, tokens, queues, backups, and rollback artifacts safe;
- terminal response, dashboards, alerts, support, rollback/abort, and incident staffing rehearsed; and
- cleanup/archive plan approved.

A date or 99.9% traffic migration cannot override a failed critical gate. Record decision evidence and approvers.

### Execute sunset progressively and reversibly

Before retirement, dry-run reports and optionally shadow rejection decisions without affecting responses. Canary retirement by owned low-risk population/region only if contract/policy permits and cross-region behavior remains explicit. Watch replacement capacity and business metrics.

At $T_r$, stop accepting old work consistently across edges/regions. Return the documented stable terminal response—often `410 Gone` when permanent and appropriate—with a machine error and authenticated migration link. Do not redirect unsafe methods automatically or silently run a different version.

Preserve correlation and distinguish retired from auth/not-found without leaking sensitive existence. Keep a rapid abort/temporary restore path if policy/security and state allow; rehearse it. Some migrations are roll-forward only and must say so.

Drain in-flight/queued work according to original contract. Avoid cutting long-running operations or webhook retries at an arbitrary wall clock without lifecycle semantics.

### Clean up without destroying evidence

After stable retirement and required rollback window, remove route/routing rules, adapters, code, dependencies, feature flags, schemas from active generation, credentials/scopes, quotas, alerts, dashboards, docs defaults, test environments, support runbooks, and ownership entries. Verify no hidden calls.

Retain immutable contract artifacts, changelog, migration guides, decision/evidence, audit logs, and historical schemas/readers needed by legal, replay, backup, or incident investigation. “Removed from serving” does not mean erase history.

Delete deprecated state/data only under retention/privacy policy with reconciliation and recovery proof. Reclaim names/tags cautiously; Protobuf field numbers and event meanings must not be reused.

Measure the intended benefit: vulnerability/dependency removal, reduced incidents/on-call/test cells, lower capacity/cost, and fewer unknown consumers. Close exceptions and postmortem surprises.

## Definitions and Notation

Let $T_a$, $T_d$, $T_s$, and $T_r$ be announcement, deprecation, sunset, and executed retirement instants. Let $H=\max(H_{contract},H_{release},H_{dormant},H_{replay},H_{rollback},H_{recovery})$ plus governed contingency. Ordinary notice requires $T_s-T_a\ge H$.

Let $U$ be credibly inventoried required consumers and $M$ confirmed migrated, so $m=M/U$ when $U>0$. Let $Q_o$ and $Q_n$ be old/replacement request volume, but neither proves unique consumer migration. Let $P$ be parity matches among $D$ compared occurrences; $p=P/D$ measures the chosen comparator only.

A **deprecation signal** communicates lifecycle without changing behavior. A **terminal response** is the documented outcome after retirement. A **dormant consumer** has legitimate low-frequency/contingency use. A **migration blocker** is an owned condition preventing tested cutover. **Retirement readiness** is a conjunction of evidence gates, not one score.

## Mechanisms, Invariants, or Proof Structure

**Timeline invariant.** Announcement cannot follow deprecation, sunset cannot precede deprecation, and executed ordinary retirement cannot precede sunset: $T_a\le T_d\le T_s\le T_r$. If a standard header or channel disagrees, consumers cannot plan reliably; correct the source-of-truth record before proceeding.

**Horizon lower bound.** A consumer/recovery path that legitimately activates every $H_i$ time units can be absent throughout a shorter observation/notice window. Taking the maximum across governed horizons is necessary to expose each ordinary path at least once or explicitly test/attest it. It is not sufficient without inventory and readiness evidence.

**Traffic counterexample.** Suppose 999,000 of 1,000,000 calls migrated, yielding 99.9%. The remaining 1,000 calls can be one legally critical settlement job. Therefore request-weighted migration cannot prove risk-weighted or consumer-complete migration.

**Readiness conjunction.** If replacement capacity/security fails, a consumer remains, notice was not delivered, or recovery still references the old contract, retirement can cause harm even when every other gate passes. Hence retirement is an AND decision; averaging scores can mask a fatal zero.

Operational invariants are: deprecation does not degrade behavior; scope/replacement/dates coherent; notice actionable and multi-channel; new adoption controlled; consumers owned; evidence includes dormant/recovery; migration singular and tested; exceptions bounded; retirement rehearsed; and cleanup preserves required history.

## Alternatives and Trade-Offs

Long notice windows protect slow consumers but prolong vulnerability, dependencies, cost, and product complexity. Short windows reduce debt but require stronger inventory, tooling, direct coordination, and stability contracts. Risk and obligations determine the horizon.

Service-wide deprecation is simple but can force unrelated migration. Element-level deprecation narrows impact but creates many timelines and tooling complexity. Scope at the smallest coherent contract boundary.

Runtime headers reach active clients with exact context; specs/SDK warnings shift development behavior; direct outreach creates accountability; public docs reach unknown consumers. Use several because none is sufficient alone.

Hard sunset creates certainty and prevents permanent legacy, but can cause outage if evidence is weak. Repeated extensions preserve availability but destroy deadline credibility. Use gated decisions and scoped exceptions.

Provider adapters reduce consumer burden but prolong internal complexity and may be lossy. Consumer migration gives clean ownership but can be slow. Time-bounded adapters with telemetry often bridge the window.

Returning `410` gives clear permanent removal when appropriate; `404` may preserve non-disclosure but is less actionable. Redirects help safe reads but can alter method/auth/cache semantics. Choose a documented, security-reviewed terminal contract.

## Failure Modes and Misconceptions

- “Deprecated means unsupported.” It remains supported under its stated window.
- “A deprecated header removes the endpoint.” Notice and behavior are separate.
- “Sunset is the deprecation date.” They are distinct and ordered.
- “The replacement is obvious.” Semantic/auth/state differences need a guide and tests.
- “A blog post is notice.” Active/dormant owners may never see it.
- “Runtime headers reach everyone.” Dormant clients make no requests.
- “Marking OpenAPI/GraphQL is enough.” Generated artifacts and direct ownership remain.
- “99.9% of calls migrated.” One critical low-volume consumer may remain.
- “Zero traffic proves unused.” Telemetry may fail and contingency jobs may sleep.
- “Last seen is the owner.” Shared credentials/proxies distort identity.
- “Degrade the old API to motivate.” That breaks the pre-sunset guarantee and evidence.
- “Move the date quietly.” Conflicting signals destroy planning trust.
- “An exception has no end.” That creates a shadow permanent API.
- “Retirement can redirect everything.” Unsafe methods/effects may change.
- “Delete schemas with the route.” Replay/audit/backup may still need them.
- “Security means no lifecycle record.” Emergency changes still need scope, communication, and evidence.
- “Cleanup is optional.” Residual routes, permissions, code, and alerts preserve risk/cost.

## Worked Examples

### Example 1

Announcement is 1 January, deprecation 1 February, sunset 1 August, and retirement 3 August after a staffed canary. The dates satisfy $T_a\le T_d\le T_s\le T_r$; a six-month dormant cycle also fits the notice horizon.

### Example 2

Responses include a standards-form `Deprecation` date, a `Link` with `rel="deprecation"` to the migration guide, and a later `Sunset` HTTP-date. A test deliberately swaps dates and fails configuration because sunset cannot precede deprecation.

### Example 3

Of 120 known consumers, 114 are verified migrated: $m=114/120=95\%$. The six remaining identities are individually owned; the service is not retired merely because the percentage looks high.

### Example 4

999,000 of 1,000,000 calls use the replacement, or 99.9%. The remaining 1,000 belong to one quarterly settlement job. Its criticality and dormant cadence block retirement until a scheduled rehearsal passes.

### Example 5

One gateway identity contributes 70% of requests but represents 300 downstream clients; ten individual identities contribute only 0.1% but include disaster tooling. Request and identity weighting tell different stories, so the inventory maps gateways to actual owners/use cases.

### Example 6

An SDK marks `oldSearch` deprecated and suggests `search`, while the server continues old behavior. A compiler warning-as-error policy would instantly break builds, so enforcement is introduced through the consumer's agreed release policy rather than by removing the symbol.

### Example 7

A GraphQL field is marked `@deprecated(reason: "Use displayName")`, but telemetry shows 37 persisted operations still select it. The provider migrates those owners and validates replacement semantics before schema removal.

### Example 8

A new webhook type replaces an old one. A wildcard subscriber receives both during dual publication and would apply the effect twice. Shared occurrence/effect identity and subscription migration prevent duplication before the old type sunsets.

### Example 9

After retirement, an old safe-read route returns documented `410 Gone` with stable code `api_version_retired` and an authenticated migration link. It never silently routes to the new version; unsafe writes are not redirected.

### Example 10

A regulated partner cannot meet the global sunset. A 30-day allowlisted extension preserves only its existing operations/volume, adds milestones and monitoring, receives security approval, and expires automatically. The public sunset date and other consumers do not drift.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies strangler/adapter transitions, ownership, and legacy removal boundaries.

[Database Engineering](../../18-database-engineering/ROADMAP.md) provides state migration, reconciliation, backup/restore horizons, retention, and safe cleanup.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) covers mixed versions, queued/replayed work, idempotency, duplicate effects, partial retirement, and recovery.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs old-version maintenance, auth/scope migration, non-disclosure, emergency breaks, and exceptions.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects lifecycle baselines, stakeholders/suppliers, transition criteria, risk acceptance, and verification evidence.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns catalogs, runtime headers, spec/SDK annotations, consumer telemetry, notification automation, gates, routing, and terminal controls.

## References

1. IETF, [RFC 9745: The Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745.html).
2. IETF, [RFC 8594: The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594.html).
3. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
4. OpenAPI Initiative, [OpenAPI Specification 3.1.0](https://spec.openapis.org/oas/v3.1.0).
5. GraphQL Foundation, [GraphQL Specification, October 2021](https://spec.graphql.org/October2021/).
6. Google, [AIP-181: Stability Levels](https://google.aip.dev/181).
7. Kubernetes, [Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/).

## Exercises

### Exercise 1

Design a timeline for deprecating a stable endpoint used by monthly partners, quarterly finance, offline mobile clients, 180-day replay, 90-day rollback artifacts, and one-year backups. Distinguish serving retirement from historical reader retention.

### Exercise 2

Create a coherent notice package for an HTTP operation, OpenAPI/SDK, GraphQL field, and webhook type. Include scope, standard headers/links, replacement, dates, direct communication, and unknown/dormant consumers.

### Exercise 3

Given 99.95% replacement traffic, 80 of 82 known consumers migrated, one shared gateway with unknown downstreams, and no disaster exercise in nine months, decide retirement readiness and required evidence.

### Exercise 4

Design a sunset execution/runbook covering dry run, canary, replacement capacity, in-flight work, terminal response, auth/non-disclosure, observability, abort/restore, incident staffing, and regional consistency.

### Exercise 5

Govern an emergency security flaw in a deprecated API two months before its planned sunset when some inputs cannot be made safe without rejection. Define exception, communication, migration acceleration, and cleanup.

## Answers to the Exercises

### Answer 1

Compute ordinary notice from the maximum relevant migration/activation horizon, not average traffic. Quarterly finance and 180-day replay require at least those windows; offline adoption/partner agreements may require longer. One-year backups do not necessarily require serving the endpoint for a year if current recovery code can restore/migrate and a historical reader/schema remains offline, so separate serving sunset from artifact retention. Announce only when the replacement, guide, SDK, and test path exist. Set exact deprecation/sunset/retirement instants with contingency and staffed execution. Inventory/test monthly, quarterly, offline, replay, rollback, failover, and restored-backup paths. Retire serving after all required consumers/queued work migrate and rollback is safe; retain immutable contracts, schemas/upcasters/readers, audit, and recovery tooling for the one-year backup/legal horizon before physical cleanup.

### Answer 2

Create one lifecycle record naming exact operation/field/type scope, reason, unchanged pre-sunset guarantee, replacement semantic/auth/quota differences, announcement/deprecation/sunset/terminal dates, owner, support, and exception route. HTTP responses use RFC 9745 `Deprecation`, `Link rel="deprecation"`, and RFC 8594 `Sunset` with valid ordered dates. OpenAPI marks the operation deprecated and links the guide; SDK symbols warn without disappearing. GraphQL uses `@deprecated` with actionable replacement and preserves resolution. Webhook catalog/schema and subscriber notices cover dual-publish identity/deduplication. Generate portal/changelog/runtime artifacts from the record and directly contact registered owners. Inventory telemetry, wildcard subscribers, dormant/offline/replay paths, and track delivery/acknowledgement/migration evidence.

### Answer 3

Not ready. Traffic percentage is request-weighted, two known consumers remain, the shared gateway makes the denominator incomplete, and the disaster path has not been exercised within its possible cadence. Identify/migrate or explicitly retire/except the two consumers; decompose or obtain accountable attestation for gateway downstreams; validate telemetry; run disaster/failover/recovery against the replacement and terminal behavior; reconcile business outcomes and replacement capacity; and resolve state/idempotency/rollback/backup horizons. Only the conjunction of required gates can authorize retirement. The 99.95% figure helps prioritize, but cannot override unknown or critical paths.

### Answer 4

Freeze the source-of-truth record/config and run a shadow rejection report listing every affected identity/operation. Verify notices, replacement parity/security/capacity/quotas, dashboards/alerts/support, and regional/catalog propagation. Drain or preserve original semantics for in-flight long operations, queues, retries, and idempotency outcomes. Canary owned low-risk consumers/one region only when policy permits, while preventing cross-region silent fallback. At retirement return the documented security-reviewed terminal response—often `410` with stable code/link for permanently gone public-safe routes—without redirecting unsafe writes. Monitor old attempts, replacement errors/tails/goodput, business effects, auth disclosure, and unknown identities. Staff incident/support owners, define stop conditions, and rehearse restore if safe or explicit roll-forward if state/security forbids rollback.

### Answer 5

Classify the unsafe-input rejection as an emergency breaking security exception, not routine deprecation. Identify the narrowest vulnerable shapes/operations/tenants and preserve safe requests. Return a stable machine error and remediation link; never reveal exploit details beyond policy. Backport other fixes to the old/replacement APIs, notify known owners/security/legal/support directly, update runtime/spec/SDK/portal signals, and accelerate migration with tooling/canaries. A temporary allowlist exists only if compensating controls make it demonstrably safe, with owner, scope, volume, milestones, monitoring, approval, and short expiry. Track rejection/attack/false-positive/business impact. At sunset execute the rehearsed terminal plan, then remove vulnerable code/permissions/dependencies while retaining audit and required historical artifacts.
