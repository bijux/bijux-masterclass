---
module_id: SARCH-079
program: Software Engineering: Software Architecture
level: 2
module_number: 79
title: Decommissioning Architectural Components
status: complete
last_verified: 2026-09-06
---

# Decommissioning Architectural Components

## One-Page Review

### Governing question

How can an organization remove an architectural component and its obligations without losing required behavior or records, stranding hidden consumers, reviving stale authority during recovery, leaking sensitive data, or leaving the cost and attack surface behind?

### Essential definitions

- **decommissioning** is the governed removal of a component from operational responsibility and the disposition of every dependency, authority, asset, and obligation it carried;
- a **retirement unit** is a bounded component plus the interfaces, data, identities, operations, contracts, and recovery paths that must be resolved together;
- a **consumer** is any human or machine that depends on the component's behavior, data, identity, timing, or side effects;
- **last authority** is the final position, epoch, or accepted operation after which the component may no longer decide or mutate production state;
- a **drain** allows admitted work to reach a classified terminal outcome before shutdown;
- **quiescence** is a controlled state in which no new authoritative work enters and in-flight work is resolved;
- **data disposition** assigns each data class to migrate, retain, archive, sanitize, destroy, or hold under accountable policy;
- **media sanitization** renders access to target data infeasible for a stated level of effort and medium;
- a **retirement gate** is a noncompensable condition that must pass before a removal action;
- **negative evidence** is evidence from absence, such as no observed calls, whose strength depends on coverage and assumptions;
- a **tombstone route** rejects or explains obsolete access after removal rather than silently reviving the old path;
- a **retirement dossier** binds scope, decisions, evidence, approvals, residual risks, asset disposition, and post-removal observation.

### Central model, mechanism, or theorem

For retirement unit $c$, let obligations $Q(c)$ cover authority, consumers, work, data, identity, dependencies, operations, recovery, records, contracts, people, and assets. Let $e(q)$ be accepted evidence for obligation $q$. Readiness is a conjunction:

$$
ready(c)=\bigwedge_{q\in Q(c)} accepted(e(q)).
$$

A high average score cannot offset one failed hard gate. Observing zero calls also does not prove no consumer. Under a stationary Poisson assumption, observing zero events for duration $T$ gives one-sided upper rate $\lambda_u=-\ln(\alpha)/T$ at confidence $1-\alpha$. The calculation is only a model; seasonal, disabled, or uninstrumented callers violate its assumptions.

### Critical invariants

- replacement or retirement preserves every approved outcome and explicitly rejects obsolete behavior;
- exactly one current authority exists before, during, and after shutdown;
- every in-flight request, message, batch, and external effect reaches a known terminal class;
- consumers receive authenticated, scoped migration or rejection behavior;
- retained records preserve meaning, provenance, access, integrity, readability, and required duration;
- deleted data, media, keys, replicas, caches, backups, and exports follow approved disposition;
- credentials, routes, certificates, trust, privileges, and control inheritance are removed or reassigned;
- recovery cannot restore retired authority, vulnerable images, or stale configuration;
- operational, supplier, license, ownership, and support obligations close explicitly;
- post-removal observation detects unexpected access without keeping the old component authoritative.

### Common failures

Common failures include equating zero traffic with zero dependency; observing only HTTP while missing batch, files, database access, and recovery; deleting before retention review; retaining everything “just in case”; turning off compute while credentials, DNS, data, and backups remain; allowing fallback to resurrect the old writer; treating a sunset date as enforcement; ignoring in-flight or delayed work; destroying cryptographic keys without checking copies and legal holds; assuming cloud deletion sanitizes every underlying medium; removing telemetry before observation; ending supplier contracts before export and evidence; deleting expertise before runbooks and records transfer; and claiming completion while transition machinery persists.

### Compact example

A billing API receives no normal calls for thirty days. Inventory nevertheless finds a quarterly adjustment job, a support replay tool, an old disaster image, database credentials, retained invoices, and a partner contract. The team migrates the job, disables and tests the replay path, fences the last billing epoch, proves the new recovery plan, assigns invoice retention and deletion, revokes access, publishes authenticated sunset guidance, and returns an explicit tombstone response. Zero observed calls was one input; closure of every obligation established retirement.

### Connections

[SARCH-075](075-strangler-and-parallel-run-architectures.md) supplies diversion and authority transfer, [SARCH-076](076-data-migration-architecture.md) supplies data disposition inputs, and [SARCH-078](078-replatforming-rehosting-refactoring-and-rebuilding.md) supplies the modernization decision. [SARCH-080](../ROADMAP.md) next coordinates evolution across releases.

## Governing Question

Starting a replacement is visible and politically attractive; removing the displaced system is quieter and often deferred. Yet the promised economic, security, and cognitive benefits appear only when old obligations end. A powered-off server can still exist as a recoverable image, trusted identity, retained data set, contractual dependency, vulnerable library, DNS name, support procedure, or hidden source of authority.

Decommissioning is therefore an architectural state transition. It must preserve required outcomes and records while making obsolete paths impossible or explicitly rejected. The evidence problem is asymmetric: one discovered caller disproves “unused,” but no observed call cannot prove universal absence. The architecture combines inventory, telemetry, controlled denial, stakeholder evidence, historical analysis, and recovery rehearsal rather than trusting one dashboard.

## Why This Matters

Incomplete retirement retains cost and risk. Old credentials and network paths can become quiet attack routes. Forgotten replicas and exports expand sensitive-data exposure. Disaster recovery can restore an obsolete writer and split authority. A license or supplier obligation continues after traffic ends. Operators must understand two systems, and future teams may route around a failure into a component whose assumptions no longer hold.

Removal itself can cause harm. Rare annual or emergency workflows may be absent from the observation window. Historical formats may be needed for audit, appeal, safety investigation, or legal retention. Deleting media without appropriate sanitization can leak data; destroying data under hold can violate obligations. Decommissioning needs the same rigor as introduction, plus explicit disposal authority.

Current authoritative sources reinforce these boundaries. The official ISO record states that ISO/IEC/IEEE 14764:2022 includes the related disposal process [1]. NIST SP 800-88 Revision 2, finalized in September 2025 and checked 2026-09-06, defines sanitization relative to access feasibility and effort rather than as a generic delete command [3]. RFC 8594 defines an HTTP Sunset hint and explicitly does not guarantee exact availability before or after its date [6].

## Prerequisites and Retrieval

Retrieve architecture component, dependency, consumer, source of authority, invariant, inventory, lineage, retention, legal hold, archive, backup, replica, cache, encryption, cryptographic erase, identity, credential, certificate, trust anchor, least privilege, route, DNS, service discovery, quiescence, drain, in-flight work, idempotency, fencing, tombstone, deprecation, sunset, recovery point objective, recovery time objective, rollback, roll forward, asset register, configuration item, contract, license, observability, negative evidence, Poisson process, confidence bound, and residual risk.

SARCH-071 supplies drift discovery, SARCH-073 compatibility and deprecation, SARCH-075 traffic transfer, SARCH-076 data migration, and SARCH-078 strategy selection. This chapter owns architectural retirement coordination; specialized records, privacy, security, hardware, environmental, procurement, and legal decisions remain with their responsible disciplines.

## Learning Objectives

After completing this module, you should be able to:

1. define a retirement unit and complete obligation inventory;
2. distinguish traffic absence from evidence of dependency closure;
3. declare last authority, quiesce admission, drain work, and fence stale actors;
4. plan consumer migration, authenticated sunset, and post-removal rejection;
5. assign data and media disposition without confusing retention with accessibility or deletion with sanitization;
6. remove identities, routes, trust, inherited controls, and recovery resurrection paths;
7. close operational, contractual, financial, and knowledge obligations;
8. use negative evidence and confidence bounds without overstating certainty;
9. sequence reversible disablement and irreversible disposal under gates;
10. assemble a retirement dossier and verify benefits after removal.

## Core Exposition

**Define the retirement outcome and unit.** Name the capability or component, present owner, users, authority, promised replacement or intentionally removed outcome, reason, horizon, and expected benefit. A deployment name alone is too narrow. Include its endpoints, jobs, stores, topics, files, identities, certificates, dashboards, runbooks, contracts, backups, and support procedures.

Specify what “gone” means. A public endpoint may be absent while records remain in a governed archive. Source code may remain for reproducibility while builds and deployment authority end. A protocol identifier may stay reserved to prevent unsafe reuse. Distinguish remove, retain inactive, archive, quarantine, and transfer.

**Assign accountable decisions.** Identify component owner, successor owner, data and records owners, security and privacy authorities, operations, finance, procurement, legal or regulatory interpretation, affected users, and final removal authority. One approval meeting does not substitute for each decision's competence.

Build a decision log with scope and evidence. Explicitly record unresolved exceptions and expiry. Do not use “business approved” to blur which person or role accepted which residual risk.

**Inventory consumers across every interface.** Inspect gateways, service discovery, DNS, certificates, network flows, database audit, message subscriptions, file transfers, object-store access, scheduled jobs, source dependencies, configuration, secrets, exports, reports, support tools, mobile clients, partners, and manual procedures. Include failed and unauthorized attempts because they predict post-removal behavior.

Search historical windows spanning seasonal and regulatory cycles where feasible. Interview operators and consumers. Examine disaster and replay paths, not only normal production. Inventory evidence has false negatives; combine independent views and state their coverage.

**Map authority and state.** Identify every fact the component can decide or mutate, including indirect external effects. Name the successor or explain why the behavior ends. Record the last accepted source position, transaction, message, and authority epoch. Replicas and caches remain nonauthoritative unless intentionally promoted.

Prevent dual authority. Route changes do not fence queued workers or direct credentials. Use conditional authority epochs, leases under valid assumptions, access revocation, or another enforcement at the decision boundary. Recovery must honor the new epoch.

**Classify behavior rather than copy it blindly.** For each consumer outcome, decide preserve, replace, redirect, archive, or reject. Legacy behavior may be required, defective, obsolete, or a workaround. Characterization provides evidence; domain and policy authority decides meaning.

Keep compatibility long enough for governed migration, not indefinitely. Publish deadlines and alternatives, observe versions, contact owners, and enforce progressive gates. Unknown callers need a deliberate quarantine or denial policy, not silent fallback.

**Communicate deprecation and sunset precisely.** A deprecation signal says use is discouraged; a sunset signal communicates likely future unavailability. RFC 9745 standardizes an HTTP Deprecation response field and can be combined with RFC 8594 Sunset information [7]. These are communication mechanisms, not consumer migration or enforcement.

Authenticate migration guidance and scope it to the affected resource or contract. Provide replacement, compatibility, support, test, and failure information. Do not reuse a retired name or endpoint for unrelated semantics; stale clients may interpret the new behavior dangerously.

**Build an evidence ledger for consumers.** Give each known consumer an identity, owner, interface, version, criticality, last observed use, migration state, validation, and closure evidence. Classify unknown and unowned traffic. A consumer is complete only when it has migrated, been retired with authority, or has an approved bounded exception.

Traffic counts alone are weak. Instrumentation can miss routes, sampling can hide rare calls, and disabled clients can return later. Configuration and contractual evidence can contradict telemetry. Preserve these contradictions for resolution.

**Use negative evidence carefully.** Under a stationary Poisson model, zero observed calls for $T$ limits the rate rather than proving it is zero. For 95% confidence, $\alpha=0.05$ gives $\lambda_u\approx2.996/T$. Thirty zero-call days leave an upper bound near 0.0999 calls per day—about one per ten days under the model.

Real consumers may be annual, bursty, correlated, disabled, or uninstrumented, so the assumption often fails. Use the calculation to expose weak inference, not to authorize removal. Controlled rejection, schedule inventory, owner confirmation, and historical evidence can be more discriminating.

**Exercise progressive disablement.** Stop new onboarding, mark deprecated, shadow or mirror, reduce cohorts, make the component read-only, reject test identities, disable bounded consumers, then quiesce production as appropriate. Each state has entry evidence, monitoring, duration, stop conditions, and recovery.

Fault injection must be authorized and bounded. A test that simply kills the component can harm users and still miss delayed effects. Exercise replacement, rejection, alarms, support, and recovery together.

**Quiesce and drain work.** Close admission at a defined boundary. Inventory requests, transactions, messages, timers, leases, uploads, sessions, workflows, and external operations already admitted. Give each a terminal classification: completed by old, transferred, compensated, cancelled under policy, quarantined, or unresolved.

A queue depth of zero does not cover work held by consumers, retries, dead-letter stores, scheduled timers, or lost acknowledgments. Preserve idempotency identities and reconciliation. Set a last-authority position and reject work bearing an earlier epoch after transfer.

**Plan data disposition by class.** For each authoritative, derived, cached, logged, analytical, backup, and exported dataset, define purpose, owner, sensitivity, jurisdiction, retention, hold, successor, format, access, integrity, deletion, and proof. “Archive all” increases exposure; “delete all” can destroy required evidence.

Retained data must remain interpretable. Preserve schema, code lists, units, time basis, provenance, integrity checks, access decisions, and a tested reader. An unreadable backup is not a useful archive. Conversely, archived data must not quietly become a production authority.

**Distinguish logical deletion from sanitization.** Deleting a record, dropping a volume, destroying a key, clearing a device, purging media, and physically destroying media offer different assurances. Choose from data sensitivity, medium, reuse, threat, contracts, and applicable policy. NIST SP 800-88r2 provides current sanitization guidance but does not replace organization-specific authority [3].

Cryptographic erase depends on complete key coverage, no remaining plaintext copies, effective key destruction, sound cryptography, and the threat model. Snapshots, replicas, caches, exports, logs, and support attachments may hold other copies. Record method, target, verification, operator, tool/version, exception, and chain of custody where needed.

**Remove identity and trust.** Inventory human and workload identities, API keys, passwords, signing and encryption keys, certificates, service accounts, roles, groups, firewall rules, trust policies, federation, hardware tokens, break-glass paths, and vendor access. Revoke or reassign each deliberately.

Order matters. Preserve authorized export and evidence access until disposition completes, then revoke. Remove successor dependence on old trust before shutdown. Monitor attempted use after revocation and investigate rather than automatically restoring access.

**Remove addressing and routing safely.** Drain load balancers, gateways, service discovery, DNS, queues, topics, file endpoints, firewall rules, and static client configuration. Consider cache and TTL behavior. A tombstone endpoint can return explicit failure or migration guidance with no old authority.

Do not leave permissive redirects forever. They can preserve vulnerable clients, confuse identity, and block name reuse. Define their owner, minimal data exposure, service objective, telemetry, and expiry.

**Rebuild recovery around the successor.** Update backups, restore automation, replicas, disaster sites, images, infrastructure definitions, dependency manifests, incident plans, exercises, and recovery access. Test that recovery produces one current authority and does not reconnect retired routes or credentials.

Old images may contain vulnerable software and secrets. Retain them only for an explicit purpose with isolation, access, integrity, and expiry. A rollback artifact is not a neutral archive; if it can return to production, it retains operational risk.

**Review inherited controls and dependencies.** Other systems may inherit authentication, logging, network, key management, time, configuration, or compliance evidence from the retiring component. Removing it can silently invalidate their control story. NIST SP 800-37 Rev. 2 calls for system disposal within lifecycle risk management [5], while SP 800-53 includes component-disposal controls [4].

Transfer or replace common capabilities before removal. Update asset registers, architecture descriptions, threat models, data-flow records, ownership catalogs, and risk assessments. Do not keep a component solely because undocumented inheritance was discovered; make the dependency explicit and decide it.

**Close operational obligations.** Remove or rewrite alerts, dashboards, synthetic checks, log routes, on-call ownership, runbooks, capacity reservations, patching, vulnerability scanning, deployment pipelines, artifact repositories, configuration, and change procedures. Retain post-removal monitoring for rejected or unexpected access.

Avoid deleting telemetry first to make the dashboard quiet. Record the final health, incident, performance, and access evidence needed by the dossier. Then retire monitoring in an order that keeps remaining risks observable.

**Close supplier and financial obligations.** Inventory licenses, support, domains, certificates, reserved capacity, leased hardware, hosting, maintenance, escrow, data processing, audit rights, and termination or export clauses. Confirm final bills and credits. Preserve evidence required for disputes or audit.

Terminate only after data export, verification, and successor recovery. Supplier account deletion can remove logs or configuration needed to establish what happened. Procurement dates must follow technical and records gates, not substitute for them.

**Transfer knowledge and human work.** Operators may perform reconciliations, approvals, corrections, and exception handling outside code. Move legitimate controls to the successor, improve harmful workarounds, and retire obsolete tasks. Train support and affected users on failure and recovery, not only normal behavior.

Update role descriptions and ownership. Do not make people redundant before capturing required operational knowledge and meeting legal or labor obligations. Documentation alone may not transfer tacit diagnostic skill; rehearsals reveal gaps.

**Sequence irreversible actions last.** Prefer reversible denial and quiescence before destructive data or media disposition. Set the last rollback point and verify successor recovery. After irreversible deletion, the response to a missed consumer is forward repair, not restoration by wish.

Use an explicit runbook with prerequisites, actor, command or action, target identity, expected evidence, stop condition, and rollback or compensation. Peer-check broad or destructive targets. The decommission plan authorizes a specific scope, not arbitrary cleanup.

**Assemble and review the retirement dossier.** Bind architecture scope, inventories, consumer dispositions, authority transfer, drain reconciliation, data decisions, sanitization evidence, identity revocation, dependency replacement, recovery tests, operational closure, contracts, approvals, exceptions, and post-removal observation.

Internal review establishes organizational evidence, not external certification. Preserve exact versions and dates for current standards or tools. Record unavailable checks honestly. A signature without supporting evidence is weak; evidence without accountable acceptance is incomplete.

**Observe after removal and realize benefits.** Monitor rejected calls, name resolution, credentials, queues, support requests, data access, security findings, cost, and successor outcomes. Unexpected use triggers triage and forward repair under policy, not automatic resurrection of retired authority.

Compare realized cost, attack surface, cognitive load, incident burden, and change outcome with the baseline. Delete transition routes and migration stores when their purpose ends. Decommissioning completes when the durable architecture and obligations match the approved end state.

## Definitions and Notation

Let:

- $c$ be a retirement unit;
- $Q(c)$ be its finite, versioned set of known obligation gates;
- $e(q)$ be evidence for obligation $q$;
- $accepted(e(q))$ be an accountable Boolean gate decision;
- $K$ be known consumers and $U$ unresolved or unknown traffic classes;
- $w_c$ be the last authoritative source position;
- $e_a$ be the new authority epoch;
- $W$ be admitted in-flight work at quiescence;
- $D$ be data classes and $disp(d)$ their approved dispositions;
- $T$ be a complete observation duration;
- $N(T)$ be observed events in that duration;
- $\alpha$ be a one-sided tail probability;
- $\lambda_u$ be a model-based upper event rate after observing zero events.

Readiness is conjunctive over the declared gates. The gate set itself can be incomplete, so configuration, telemetry, history, interviews, contracts, and controlled denial provide independent discovery evidence. For a stationary Poisson process, $P(N(T)=0)=e^{-\lambda T}$; solving $e^{-\lambda_uT}=\alpha$ yields $\lambda_u=-\ln(\alpha)/T$.

## Mechanisms, Invariants, or Proof Structure

**Conjunction proof.** Retirement asserts that every required obligation is resolved. If some $q\in Q(c)$ lacks accepted evidence, the universal claim is false even when all other gates pass. Therefore an average readiness score cannot establish retirement.

**Zero-event derivation.** Under the explicit stationary Poisson assumption, the probability of zero observations is $e^{-\lambda T}$. Set this probability to tail value $\alpha$, take natural logarithms, and solve: $-\lambda_uT=\ln(\alpha)$, hence $\lambda_u=-\ln(\alpha)/T$. Longer complete observation narrows the modeled upper rate; it never proves structural absence, and assumption violations invalidate the interpretation.

**Executable retirement gate.** This finite example preserves failed and pending gates and computes the thirty-day 95% zero-call upper rate.

<!-- bijux-verify: {"id":"evaluate-retirement-gates","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ready=false\nblockers=['contracts', 'recovery']\nzero_call_upper_per_day=0.0999\n","stderr":""}} -->
```python
from math import log

gates = {
    "traffic": "passed",
    "writers": "passed",
    "jobs": "passed",
    "records": "passed",
    "recovery": "failed",
    "credentials": "passed",
    "contracts": "pending",
}
blockers = sorted(name for name, status in gates.items() if status != "passed")
upper_rate = -log(0.05) / 30
print(f"ready={str(not blockers).lower()}")
print(f"blockers={blockers}")
print(f"zero_call_upper_per_day={upper_rate:.4f}")
```

Execution verifies one finite gate evaluation and calculation. It does not validate gate completeness, Poisson assumptions, consumer absence, or authorization to remove a real component.

**Authority invariant.** After epoch $e_a$ becomes current, the retired component and every delayed work item bearing an earlier epoch must be unable to commit. DNS removal or process shutdown alone does not satisfy the invariant because old instances, queues, restore images, and credentials can survive.

**Drain invariant.** Every item admitted before quiescence belongs to exactly one terminal class with durable identity. Dropping an item from a queue or metric does not classify its business effect. Lost-response and duplicate cases require reconciliation against authoritative state and external systems.

**Data-disposition invariant.** Every copy of data class $d$ follows an approved $disp(d)$ consistent with retention, hold, access, recovery, and sanitization authority. This is a lifecycle claim across replicas and exports, not a claim about one primary store.

## Alternatives and Trade-Offs

**Immediate shutdown versus progressive disablement.** Immediate removal shortens exposure but concentrates discovery risk. Progressive denial yields evidence and recovery options but prolongs dual cost and attack surface.

**Redirect versus tombstone.** Redirects reduce consumer interruption but can preserve obsolete semantics and trust. Tombstones make failure explicit but require consumer handling. Both need authentication, telemetry, ownership, and expiry.

**Archive versus migrate.** Migration keeps data operational and accessible but expands active scope. Archive can simplify operation but needs durable interpretation, access, integrity, and tested retrieval.

**Logical deletion versus media sanitization.** Logical deletion supports ordinary lifecycle behavior; sanitization addresses recovery from media under a threat model. The appropriate method follows policy, medium, reuse, and sensitivity.

**Long observation versus controlled denial.** More observation helps with recurring traffic but may never cover rare paths. Bounded denial provides stronger behavioral evidence but raises consequence and must be authorized.

**Retain rollback versus remove attack surface.** A rollback window reduces early transition risk while retaining obsolete software, data, and credentials. Set an explicit last reversible point and isolate retained artifacts.

## Failure Modes and Misconceptions

1. **“Powered off means retired.”** data, trust, recovery, contracts, and routes remain.
2. **“Zero calls proves zero consumers.”** absence depends on coverage and demand assumptions.
3. **“Thirty days covers usage.”** annual, seasonal, disabled, and emergency paths contradict it.
4. **“A sunset date enforces migration.”** it communicates intent and may change.
5. **“A redirect is harmless.”** it can preserve vulnerable identity and semantics.
6. **“Queue depth zero means drained.”** work can exist in consumers, retries, timers, or external systems.
7. **“Routing fences writers.”** direct credentials and restored instances bypass routing.
8. **“Archive means retain bytes.”** future meaning, integrity, access, and readability are required.
9. **“Delete means sanitize.”** abstraction and medium determine recoverability.
10. **“Destroying one key erases all copies.”** other keys and plaintext copies may remain.
11. **“Keep everything for safety.”** excess retention creates cost and exposure.
12. **“Delete everything to reduce risk.”** holds, records, audit, and recovery can forbid it.
13. **“Managed infrastructure handles disposal.”** owners still define scope and verify evidence.
14. **“Recovery is unrelated.”** restore can resurrect obsolete authority and vulnerabilities.
15. **“Remove monitoring first.”** it destroys evidence when risk is changing.
16. **“Cancel the contract at shutdown.”** export, logs, support, and proof may disappear.
17. **“Documentation transfers all knowledge.”** rehearsal exposes tacit operational gaps.
18. **“New service live means old service retired.”** every old obligation must close.

## Worked Examples

### Example 1

**Situation.** An API shows zero calls for thirty instrumented days.

**Reasoning.** Under the stationary Poisson model, the 95% upper rate is $-\ln(0.05)/30\approx0.0999$ calls per day, not zero. A quarterly client also violates the stationarity inference. The team checks historical logs, contracts, configuration, and owners, then performs an authorized tombstone exercise.

**Conclusion.** Negative telemetry bounds a model; it does not prove dependency absence.

### Example 2

**Situation.** A replacement receives all interactive traffic, but an annual tax job calls the old database directly.

**Reasoning.** Gateway evidence missed a bypass and the annual cycle. The job is inventoried, migrated with characterized calculations and data authority, exercised on representative history, and its credentials revoked. The retirement window includes the relevant cycle or stronger controlled evidence.

**Conclusion.** Interface coverage and time coverage are separate retirement obligations.

### Example 3

**Situation.** Operators stop an order service while 300 messages are in flight.

**Reasoning.** Some consumers committed orders before acknowledgment, so blindly replaying all 300 can duplicate effects. Admission closes; stable message identities are reconciled against authoritative orders and external payments; each item is completed, replayed idempotently, compensated, quarantined, or escalated.

**Conclusion.** Draining classifies business outcomes, not merely transport buffers.

### Example 4

**Situation.** DNS points to the successor, but a restored disaster image starts the retired writer.

**Reasoning.** The image holds credentials and ignores current routing. A data-boundary authority epoch rejects it; recovery automation, images, secrets, firewall policy, and runbooks are updated. A recovery exercise proves the successor remains sole authority.

**Conclusion.** Decommissioning must prevent recovery from resurrecting stale authority.

### Example 5

**Situation.** A team proposes deleting seven years of invoices when retiring billing storage.

**Reasoning.** Records and legal owners classify invoices, holds, supporting events, access, retention, and permitted deletion. Required records move to an integrity-protected readable archive with schema and provenance; eligible operational copies are disposed of under approved methods.

**Conclusion.** Component retirement does not decide records disposition automatically.

### Example 6

**Situation.** A storage volume is deleted through a provider API and recorded as sanitized.

**Reasoning.** Logical resource deletion does not itself establish the underlying-medium assurance. The owner maps data sensitivity, medium, reuse, provider evidence, encryption and key coverage, replicas, snapshots, and contract to an approved sanitization method based on NIST SP 800-88r2 and applicable policy.

**Conclusion.** Sanitization is a threat-model and evidence claim, not a synonym for resource deletion.

### Example 7

**Situation.** A retired authentication broker supplied identity to five other systems.

**Reasoning.** Removing it would invalidate inherited authentication, audit, keys, and emergency access. Each relying system moves to a successor trust path, validates claims and revocation, updates threat and control records, and tests failure before the broker's signing keys and routes retire.

**Conclusion.** Common-control inheritance makes consumers broader than application calls.

### Example 8

**Situation.** Procurement cancels a SaaS contract on the planned shutdown date.

**Reasoning.** Administrators lose access to audit logs, configuration, export, and vendor-assisted verification before evidence is complete. The sequence is corrected: export and validate data, preserve required logs, close integrations, prove successor recovery, document disposition, then terminate under contractual notice.

**Conclusion.** Commercial closure must follow technical and records gates.

### Example 9

**Situation.** An old hostname is immediately reused for an unrelated internal service.

**Reasoning.** Cached DNS and static clients send old credentials and payloads to new semantics, risking disclosure and unintended action. The name remains reserved or serves a minimal authenticated tombstone through the stale-client horizon; telemetry drives owner outreach before final removal.

**Conclusion.** Identifier reuse can turn retirement residue into a security and correctness fault.

### Example 10

**Situation.** Six months after cutover, old dashboards, pipelines, replicas, licenses, and on-call pages remain.

**Reasoning.** The organization still pays, patches, responds, and interprets conflicting signals. Owners close each obligation, remove transition machinery, measure realized cost and incident load, and preserve only approved archival evidence. Unexpected calls go to a forward-repair process, not automatic restoration.

**Conclusion.** Realized benefit and removed obligations complete decommissioning.

## Cross-Program Connections

- [SEME](../../10-software-engineering-methods-and-evolution/ROADMAP.md) owns maintenance, legacy understanding, program evolution, and disposal process.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) develops rollout, observability, incident response, backup, restore, and operational readiness.
- [DBE](../../18-database-engineering/ROADMAP.md) supplies database archival, replication, backup, transaction, and storage evidence.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) owns information lifecycle, lineage, retention, governance, and archival meaning.
- [SEC](../../25-security-engineering/ROADMAP.md) owns sanitization, identity, key, threat, evidence, vulnerability, and supplier-security controls.
- [SYSENG](../../26-systems-engineering/ROADMAP.md) develops lifecycle transition, configuration, stakeholder, verification, disposal, and asset reasoning.
- [API](../../28-api-and-service-engineering/ROADMAP.md) owns protocol deprecation, sunset, consumer migration, and tombstone behavior.
- [PLAT](../../29-platform-engineering/ROADMAP.md) supplies inventory, self-service deletion, policy, telemetry, identity, and cost-allocation mechanisms.

## References

1. ISO/IEC/IEEE. “ISO/IEC/IEEE 14764:2022 Software engineering — Software life cycle processes — Maintenance.” Official record checked 2026-09-06. https://www.iso.org/standard/80710.html
2. ISO/IEC/IEEE. *ISO/IEC/IEEE 12207:2017 Systems and software engineering — Software life cycle processes*. 2017.
3. Ramaswamy Chandramouli and Eric Hibbard. *NIST SP 800-88 Revision 2: Guidelines for Media Sanitization*. September 2025. Checked 2026-09-06. https://doi.org/10.6028/NIST.SP.800-88r2
4. NIST. *SP 800-53 Revision 5, Security and Privacy Controls for Information Systems and Organizations*, including SR-12 Component Disposal. September 2020, update 1 December 2020.
5. NIST. *SP 800-37 Revision 2: Risk Management Framework for Information Systems and Organizations*. December 2018.
6. Erik Wilde. “The Sunset HTTP Header Field.” RFC 8594, May 2019. https://www.rfc-editor.org/rfc/rfc8594.html
7. Thomas Fossati and Erik Wilde. “The Deprecation HTTP Response Header Field.” RFC 9745, March 2025. https://www.rfc-editor.org/rfc/rfc9745.html
8. Ian Cartwright, Rob Horn, and James Lewis. “Transitional Architecture.” 28 March 2022. Checked 2026-09-06. https://martinfowler.com/articles/patterns-legacy-displacement/transitional-architecture.html
9. Michael Nygard. *Release It!*. 2nd ed. Pragmatic Bookshelf, 2018.
10. Jez Humble and David Farley. *Continuous Delivery*. Addison-Wesley, 2010.
11. Sam Newman. *Monolith to Microservices*. O'Reilly Media, 2019.
12. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.

## Exercises

### Exercise 1

Define decommissioning, retirement unit, consumer, last authority, drain, quiescence, data disposition, media sanitization, retirement gate, negative evidence, tombstone route, and retirement dossier.

### Exercise 2

Assuming a stationary Poisson process, derive the 99% one-sided upper daily call rate after observing zero calls for 60 complete days. Interpret the result and name three reasons the model may not apply.

### Exercise 3

A service has zero gateway traffic, but retains a queue subscription, write credential, database replica, restore image, and annual report. Diagnose the retirement claim and specify the next safe actions.

### Exercise 4

Design a decommission plan for a payment component. Include scope, consumers, authority, in-flight work, external effects, data, records, identities, routes, recovery, security, suppliers, operations, progressive disablement, irreversible actions, evidence, and post-removal monitoring.

### Exercise 5

A university retires a student-record system containing active enrollment, historical grades, disability accommodations, disciplinary restrictions, research extracts, alumni access, legal holds, and decades of backups. Propose a governed architecture without claiming that technical evidence decides academic policy, lawful retention, accessibility adequacy, privacy, or records authority.

## Answers to the Exercises

### Answer 1

Decommissioning removes a component from operational responsibility and disposes of every obligation it carried. A retirement unit is the component plus interfaces, data, identities, operations, contracts, and recovery resolved together. A consumer depends on behavior, data, identity, timing, or effects. Last authority is the final accepted position or epoch. A drain resolves admitted work; quiescence admits no new authoritative work. Data disposition assigns migrate, retain, archive, sanitize, destroy, or hold. Media sanitization makes access infeasible for a stated effort and medium. A retirement gate is noncompensable. Negative evidence comes from absence and depends on coverage. A tombstone route explicitly rejects obsolete access. A retirement dossier binds scope, decisions, evidence, approvals, disposition, risks, and observation.

### Answer 2

For zero events, $P(N(T)=0)=e^{-\lambda T}$. At 99% confidence, $\alpha=0.01$ and $T=60$, so

$$
\lambda_u=-\ln(0.01)/60=4.605170\ldots/60=0.0767528\ldots
$$

or about 0.0768 calls per day. This is roughly one call per thirteen days as an upper rate under the model, not proof of no consumer. The model may fail because calls are seasonal rather than stationary, instrumentation misses a route, or a consumer is disabled during observation. Correlated bursts, scheduled annual work, and incomplete observation are other valid reasons.

### Answer 3

The claim is false because gateway traffic covers only one interface and five obligations remain. The queue can deliver work, the credential permits authority, the replica holds data and perhaps access, the image can resurrect old behavior, and the annual report is a consumer outside the window.

Stop new dependencies but do not destroy evidence. Inventory queue positions and delayed work; migrate, cancel under authority, or drain each item idempotently. Move the report and validate its semantics and records obligations. Fence old writes at the authoritative boundary, then revoke the credential after authorized export and reconciliation. Assign replica data disposition. Replace recovery with a tested successor plan and isolate or dispose of the old image. Exercise bounded denial, monitor unexpected access, and pass all gates before irreversible removal.

### Answer 4

Define the payment capability, endpoints, jobs, stores, networks, identities, partners, operators, and expected successor outcome. Inventory interactive, batch, replay, dispute, refund, settlement, reconciliation, fraud, support, and recovery consumers. Declare one authority per payment and a last source position and epoch. Stop admission, drain in-flight requests and messages by stable identity, and reconcile lost responses against processors, ledgers, and customer-visible state. External charges require compensation and accountable review, not deletion.

Classify ledgers, tokens, personal data, logs, backups, replicas, exports, and evidence by retention, hold, migration, archive, access, deletion, and sanitization. Migrate readers and writers, publish authenticated deprecation and sunset, operate a bounded tombstone, revoke keys and credentials, remove routes and trust, and ensure no fallback or restore image can write under the old epoch. Test successor backup, restore, replay, settlement, and processor recovery.

Close monitoring, runbooks, on-call, pipelines, licenses, processor and hosting contracts only after evidence is preserved. Progress through read-only and cohort denial with financial, security, availability, latency, reconciliation, and support gates. Perform destructive disposition only after the last rollback point and peer-checked authorization. The dossier records every terminal work item, data decision, approval, exception, and tool result. Post-removal monitoring covers rejected calls, credentials, queues, disputes, settlement, costs, and successor outcomes; unexpected work triggers forward repair rather than silent resurrection.

### Answer 5

Establish accountable registrar, academic, accessibility, disability-services, privacy, security, records, legal, research-governance, alumni, operations, and affected-community roles. Inventory enrollment, grades, transcripts, accommodations, restrictions, appeals, holds, extracts, integrations, identity, portals, manual work, backups, recovery, and historical code lists. Classify each outcome as migrated, retained in a governed archive, intentionally ended, or explicitly rejected.

Preserve stable identity, provenance, corrections, effective time, access decisions, sealed or restricted states, accessibility metadata, and readable historical formats. Give every data class an authorized retention, hold, access, archive, deletion, and sanitization decision across replicas, extracts, support copies, and backups. Research extracts retain purpose and governance; alumni access does not make the archive operational authority. Migrate active authority with reconciliation and fencing, drain requests, and test successor recovery without restoring the old writer.

Progressively disable bounded cohorts and interfaces only with approved academic-calendar coverage and support. Replace common identity and reporting dependencies, revoke old trust, close contracts and operations, retain explicit tombstones, and observe unexpected access. The dossier can prove bounded technical preservation, disposition, access mechanisms, and system behavior. Academic policy, lawful retention, disability accommodation, accessibility adequacy, disciplinary authority, research use, and privacy require decisions by responsible institutions, professionals, affected people, and applicable processes.
