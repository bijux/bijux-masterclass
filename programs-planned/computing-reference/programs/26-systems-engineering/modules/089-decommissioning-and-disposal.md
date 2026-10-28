---
module_id: SYSENG-089
program: Systems Engineering
level: 2
module_number: 89
title: Decommissioning and Disposal
status: complete
last_verified: 2026-08-31
---

# Decommissioning and Disposal

## One-Page Review

### Governing question

Can the organization deliberately end or transfer a system's services, dependencies, authorities, information, physical assets, support obligations, and hazards while preserving required continuity and records—and produce evidence that no unmanaged capability, access, data, material, contract, or liability remains?

### Essential definitions

- **Decommissioning** is the controlled transition that removes a system or capability from authorized service and resolves its interfaces, dependencies, identities, information, support, assets, and residual obligations.
- **Retirement** is the lifecycle decision that a system, item, service, or capability will no longer be sustained for its former operational purpose under stated effectivity.
- **Disposal** is the authorized final disposition of property or material through reuse, transfer, donation, sale, recycling, reclamation, destruction, demilitarization, return, abandonment where lawful, or other governed means.
- **Deactivation** places a system into a defined nonoperational condition; it may be reversible and is not automatically decommissioning.
- **Service transition** moves users, workload, data, authority, interfaces, and support to a successor, alternative process, or deliberately terminated state.
- **Sanitization** renders access to target data on media infeasible for a stated level of effort using an applicable method; deletion, formatting, encryption, and physical destruction are not interchangeable claims.
- **Demilitarization** renders specified defense articles unusable for their originally intended military purpose according to governing authority; the concept does not apply universally.
- A **closure ledger** records every retirement obligation, exact object/effectivity, disposition, owner/authority, evidence, residual risk, and completion state.
- **Residual ownership** assigns responsibility for retained archives, field assets, environmental monitoring, legal claims, supplier/customer obligations, vulnerabilities, or hazards after routine operations cease.
- **Retirement closure** is the authorized determination that all applicable ledger entries are complete or explicitly transferred/accepted with durable evidence and no undocumented dependency remains.

### Central model, mechanism, or theorem

Represent the decommissioning scope as a typed dependency graph $G=(V,E,\tau)$ containing services, users, interfaces, identities, data, physical assets, suppliers, facilities, support resources, records, hazards, and obligations. For every node and relationship in retirement effectivity $R$, define disposition

$$
d(v)=(action, owner, authority, evidence, residual, retention, state).
$$

Closure requires more than all planned actions marked done:

$$
Close(R)\Rightarrow coverage(R)=1\land open_{critical}=0\land transfers_{accepted}=true\land evidence_{retrievable}=true.
$$

Even this is bounded by discovery quality. Independent observation must challenge the declared inventory and verify that retired capabilities, access paths, data copies, and physical items cannot silently return.

### Critical invariants

- Define the retirement decision, authority, effectivity, timing, success criteria, reversibility, service obligations, and residual owners before execution.
- Maintain safe, secure, supported operation until the agreed cutoff; retirement status does not excuse degraded controls.
- Inventory declared and observed services, users, interfaces, dependencies, identities, data/media, assets, locations, variants, suppliers, spares, tools, facilities, contracts, hazards, and records.
- Trace every consumer and external obligation; absence of recent traffic does not prove absence of dependency.
- Preserve continuity through successor acceptance, alternate process, notified termination, or explicit risk acceptance; test migrations and fallback.
- Classify information by ownership, sensitivity, privacy, integrity, authenticity, retention, legal hold, license, format, provenance, and future interpretation needs.
- Select media sanitization/disposal methods by media, data sensitivity, threat, reuse destination, verification, custody, and applicable policy; record evidence.
- Resolve physical ownership, inventory, custody, contamination/hazardous material, export/demilitarization, counterfeit/security features, reuse value, recycling, and environmental requirements.
- Revoke or transfer identities, credentials, keys, certificates, network paths, domains, accounts, secrets, licenses, remote/vendor access, and signing/automation authorities.
- Update interfaces, registries, catalogs, monitoring, incident/recovery plans, documentation, training, contracts, finances, baselines, risks, and asset/configuration records.
- Preserve only required artifacts and knowledge in durable, accessible, integrity-protected forms with funded ownership and tested retrieval.
- Verify closure through independent inventory/discovery, negative tests, successor reconciliation, physical inspection, sanitization records, residual-risk acceptance, and post-cutoff monitoring.

### Common failures

Common failures include powering off without decommissioning; assuming a replacement means consumers migrated; treating zero traffic as no dependency; deleting a database while exports, backups, caches, logs, replicas, test copies, and vendor systems remain; retaining everything “just in case”; destroying records under legal hold; formatting media and calling it sanitized; forgetting cloud resources, domains, DNS, certificates, API keys, service accounts, automation, and recovery environments; selling or donating equipment with data or controlled capability; recycling hazardous assets through unverified chains; disposing spares while field obligations remain; terminating suppliers before obtaining data and rights; archiving bits without tools or semantics; and closing the project while residual security, environmental, contractual, or customer ownership is unnamed.

### Compact example

A synthetic closure ledger contains eight required domains. Seven are complete, but `external_credentials` remains open, so retirement authorization is rejected. After revocation evidence is recorded, all eight are complete and the fixture reports eligibility for a declared metadata gate. The check does not discover missing items, validate authority or evidence, verify sanitization, or prove real closure.

### Connections

Decommissioning/disposal connect lifecycle decisions, service transition, configuration and asset management, interfaces, data governance and records, cybersecurity/privacy, supply/property, environmental/safety, contracts/finance, operations/incident/recovery, verification/validation, obsolescence, support, knowledge preservation, and successor-system acceptance.

## Governing Question

What must stop, move, persist, be rendered inaccessible, be physically dispositioned, or remain owned when the system leaves service—and how will evidence demonstrate that outcome without breaking a valid obligation?

Retirement is a system change with negative-space requirements: after closure, unauthorized behavior, access, dependency, cost, hazard, and ambiguity must not remain. It is also a continuity event. Users may need a successor; data may need migration or preservation; field items may remain; regulators and investigators may need trustworthy records long after operators leave.

## Why This Matters

Systems rarely disappear at one boundary. A service is removed while scheduled jobs still call it. Hardware leaves a facility while vendor access survives. A database is migrated while backups and analytics retain older personal data. A program office closes while customers, spares, repair contracts, orbital assets, hazardous materials, or certification records persist. Unplanned remnants produce outages, breaches, fraud, unnecessary cost, environmental harm, and loss of evidence.

NASA's Systems Engineering Handbook describes closeout as implementing decommissioning/disposal planning, archiving information, capturing lessons, and resolving returned data/assets. It identifies Decommissioning and Disposal Readiness Reviews in its lifecycle. NASA software guidance expects retirement plans to address archival, closure, equipment, sensitive information, licenses, and lessons. These are NASA-specific processes, but the underlying disciplines—planned cessation, controlled disposition, evidence, and residual ownership—generalize.

NIST SP 800-88 Rev. 2, published in September 2025, treats media sanitization as a program tied to information sensitivity, media, intended disposition, controls, and verification. It stresses that sanitization decisions begin during system development and occur beyond final disposal. Sanitization solves confidentiality for specified media and effort; it does not by itself address records retention, integrity, asset custody, cloud replicas, application accounts, or operational closure.

## Prerequisites and Retrieval

Before authorizing or auditing decommissioning/disposal, retrieve:

1. retirement rationale, decision authority, scope/effectivity, target cutoff, success/abort criteria, allowed reversibility, funding, schedule, stakeholders, and residual ownership model;
2. service and mission obligations, users/customers, SLAs/contracts, regulations, safety/security/privacy, records/legal holds, accessibility, support warranties, field commitments, and successor acceptance criteria;
3. authoritative and observed architecture/configuration: products, services, interfaces, dependencies, workflows, data flows, external endpoints, variants, serials/lots, releases, sites, field units, spares, repairs, recovery, and unsupported exceptions;
4. identities and access: people/roles, service accounts, API keys, secrets, certificates, signing keys, tokens, domains/DNS, network routes, firewall rules, VPN/vendor access, physical badges/locks, automation, repositories, registries, and emergency paths;
5. information inventory: operational data, databases, object/file stores, endpoints/devices, removable media, backups/snapshots, replicas, caches, logs, queues, analytics, test/training copies, paper, suppliers, archives, models, source/build artifacts, and provenance;
6. information obligations: ownership, classification/sensitivity, privacy/purpose, retention/minimization, legal hold, intellectual property/license, export, integrity/authenticity, evidentiary value, format/tool dependencies, access, and final disposition authority;
7. physical/property inventory: owner, accountable record, location/custody, configuration, data-bearing media, controlled technology, serial/lot, condition, reuse/resale value, spares/consumables, hazardous/regulated material, contamination, packaging/transport, and disposal route;
8. support and enabling capabilities: suppliers/contracts, facilities/utilities, tools/calibration, maintenance, spare/repair channels, cloud/subscriptions/licenses, workforce/knowledge, documentation/training, monitoring, incident response, backup/recovery, and insurance;
9. transition plans: successor mapping, compatibility, data/record migration, reconciliation, user/customer notice, training, parallel operation, freeze/cutover, monitoring, fallback, rollback/forward recovery, final transaction, and acceptance;
10. sanitization/disposal plan by data/media/asset type with method, tool/version, verification, custody, witness/roles, certificates, failed-item handling, reuse recipient, environmental/property chain, and exception authority;
11. closure evidence: successor results, user/access reports, configuration and asset reconciliation, zero/expected traffic observations, vulnerability and cost scans, physical inspections, inventory receipts, sanitization verification, archive retrieval tests, contract/license closure, risk transfer/acceptance, and lessons;
12. post-close plan: monitoring duration, residual incidents/claims, archive stewardship, environmental/site monitoring, retained field support, audit response, contact succession, funding, escalation, and final review.

Perform a **retirement thread** from one operational outcome through every user, interface, data store/copy, identity, physical component, supplier/tool, support process, recovery path, record, hazard, contract, successor, and residual owner. Test both forward disappearance and backward reconstruction.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish deactivation, decommissioning, retirement, transfer, reuse, sanitization, demilitarization, disposal, and archival;
2. define retirement scope, effectivity, authority, success criteria, residual ownership, and closure ledger;
3. discover consumers, hidden dependencies, identities, data copies, physical assets, support resources, contracts, hazards, and records;
4. design successor/service and data transitions with reconciliation, acceptance, monitoring, and fallback;
5. classify information and select preservation, transfer, minimization, sanitization, or destruction under applicable obligations;
6. plan safe, secure, lawful, environmentally responsible property disposition with chain of custody;
7. revoke digital/physical authority and remove network, automation, supplier, and recovery access paths;
8. preserve interpretable configuration, evidence, knowledge, provenance, tools, rights, and records where required;
9. verify closure through positive and negative evidence across actual populations and residual risks;
10. design systems for future exit, portability, sanitization, material recovery, and controlled retirement.

## Core Exposition

**Plan retirement at inception.** Architecture determines whether data can be exported, media sanitized, components separated, hazardous materials identified, interfaces withdrawn, suppliers exited, and evidence interpreted. Include retirement requirements, cost, rights, formats, design-for-demise/disassembly, records, and residual ownership before acquisition or deployment.

**Establish decision authority and effectivity.** State who may terminate service, dispose property, destroy records, accept environmental/security risk, transfer data, revoke identities, and approve closure. Retirement can apply to one version, site, serial population, customer, contract, service region, or whole system. Prevent a global “retired” label from hiding valid field obligations.

**Maintain integrity until cutoff.** Continue required patching, monitoring, backups, configuration, maintenance, incident response, support, safety, and regulatory controls. A planned end date can increase attack and failure exposure as staff leave and suppliers disengage. Freeze only what is necessary and define emergency change authority.

**Build a typed closure inventory.** Merge CMDB/asset/configuration, service catalogs, code/dependency, API gateway/DNS, identity, network, cloud billing, data catalogs/lineage, backup, supplier/contracts, facility/property, maintenance, finance, records, and operational observation. Reconcile declared sources with discovery and physical inspection. Track unknowns and ownership gaps as open obligations.

**Map consumers and obligations.** Identify direct and indirect users, batch jobs, external customers, devices, integrations, reports, regulators, auditors, incident teams, support organizations, successors, and archives. Review business/mission cadence and seasonal use. Zero recent traffic is supporting evidence only when observation coverage and expected use are understood.

**Choose the target end state.** Each capability is migrated, replaced by an alternate process, intentionally terminated with stakeholder acceptance, retained in bounded support, transferred with accepted ownership, or archived for interpretation. Define service, performance, safety/security, data, accessibility, contractual, and support acceptance—not just technical reachability.

**Engineer successor transition.** Baseline old/new configurations and contracts. Test compatibility, capacity, correctness, failure, security/privacy, recovery, user work, and operations. Migrate cohorts if appropriate; reconcile transactions, entitlements, balances, histories, interfaces and customer outcomes. Define final write/cutoff, in-flight work, late arrivals, fallback and last safe rollback. Successor online does not mean predecessor unused.

**Inventory information by copy and medium.** Trace authoritative and derived data through databases, replicas, backups, snapshots, caches, queues, logs, exports, analytics, test/training, endpoints, paper, vendor platforms, portable media, model artifacts, source/build systems, and archives. Classify each copy's purpose, owner, sensitivity, retention, legal hold, provenance, integrity, license, destination, and disposition.

**Separate retention from accessibility.** Retained records need durable formats, metadata, provenance, integrity protection, search/access, authorization, privacy/security, funding, tools, keys or verification chains, and stewardship succession. Avoid retaining active credentials or unnecessary sensitive data merely because records remain. Test retrieval and interpretation with someone outside the original team.

**Select sanitization deliberately.** Determine whether media will remain in organizational control, be reused, transferred, sold, recycled, returned, or destroyed; classify data and threat; identify media technology and sanitization capabilities. Choose applicable clear, purge, destroy, or other governed technique, then verify results and custody. Cryptographic erase depends on implementation and key coverage; factory reset or file deletion may omit remapped blocks, replicas, metadata, or external copies.

**Handle cloud and managed services.** Export required data and configuration, verify provider deletion commitments/certificates where applicable, remove snapshots/replicas/log sinks/keys, revoke federation and support access, close network links, release addresses/domains, stop billing, and retain contract/audit evidence. Provider deletion does not remove downstream exports or client caches; organizational evidence is bounded by provider visibility.

**Revoke authority comprehensively.** Disable people, service and machine accounts; API keys/tokens; certificates/signing; secrets; automation/schedulers; repository/package/container access; DNS/domains; routes/firewalls/VPN; vendor remote support; physical badges/keys; break-glass and recovery credentials. Transfer authorities needed by successors explicitly. Monitor attempted post-cutoff use to find hidden dependencies or malicious persistence.

**Disposition physical property safely.** Resolve ownership and accountable records. Identify data media, controlled/export-sensitive capability, hazardous materials, contamination, batteries/chemicals, pressure/energy, radioactivity, counterfeit-sensitive marks, safety devices, spares and installed/site assets. Evaluate reuse, transfer, donation, sale, reclamation, recycling, demilitarization or destruction under applicable rules. Maintain custody, qualified vendors, manifests/receipts and downstream assurance.

**Protect supply and field obligations.** Do not dispose spares, tools, data or supplier rights while supported field units, warranties, investigations, repair, certification, or customer contracts depend on them. If ownership transfers, reconcile exact inventory, configuration, open anomalies, licenses, records, support dates and authority. A recipient's pickup is not proof it accepted technical responsibility.

**Close facilities and environments.** Safe and isolate energy, process materials, equipment, labs, test ranges, networks and utilities. Decontaminate, inspect, monitor residual environmental conditions, update drawings/site records, remove signage/access, transfer property, and preserve emergency information. Physical demolition can destroy evidence or expose hazards if performed before characterization.

**Update control planes and knowledge.** Remove the system from catalogs, monitoring, on-call, incident/recovery, vulnerability, patch, capacity, change, dependency, data, privacy and asset processes at the correct time. Update architecture/interface docs, runbooks, training, baselines, risks and customer support. Preserve final configuration and decisions so future investigations know what actually existed.

**Verify negative outcomes.** Positive evidence proves successor function and archive retrieval. Negative evidence searches for what should no longer exist: traffic, DNS, reachable ports, active accounts, credentials, cloud resources/cost, unapproved data copies, property, vendor access, scheduled jobs, monitoring alerts, repair demand, hazardous energy and old stock. Absence claims need adequate observation window and independent sources.

**Manage anomalies and exceptions.** Failed sanitization, inaccessible device, disputed ownership, unknown data, late consumer, legal hold, stranded asset, missing supplier record, or environmental finding blocks affected closure. Quarantine and assign authority. Do not force a green ledger by marking unknowns out of scope without accepted ownership and rationale.

**Conduct readiness and closure reviews.** Before cutoff, confirm scope, stakeholders, successor, hazards/threats, migration, archive, sanitization, property, access, support, contracts, evidence, fallback and resources. After execution, review observed closure, deviations, residuals, ownership, monitoring and lessons. Reviews authorize bounded decisions; checklists do not transfer liability automatically.

**Measure meaningful outcomes.** Track unknown dependencies/assets/data, migration reconciliation, failed or late consumers, active identities after cutoff, residual cloud/licensing cost, sanitization exceptions, property chain gaps, archive retrieval, environmental actions, unsupported field obligations, closure age, post-retirement incidents and open residual risks. A fast close can mean efficient planning or missed scope.

**Design for future exit.** Prefer stable interfaces, portable documented data, export tools, separable media/components, material declarations, unique asset/configuration identity, automated inventory, revocable scoped credentials, supplier exit/data rights, tested restore/transfer, modular support, archival formats, and reversible deactivation where appropriate. Exit readiness is part of system integrity.

The following fixture checks one declared closure ledger.

<!-- bijux-verify: {"id":"decommissioning-closure-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"closure_domains=8\ninitial_complete_domains=7\ninitial_open_domains=external_credentials\ninitial_authorization=reject_open_retirement_obligation\nafter_revocation_complete_domains=8\nafter_revocation_open_domains=0\nafter_revocation_authorization=eligible_for_declared_metadata_gate\nstatus=synthetic_closure_ledger_consistent\nevidence=declared_boolean_status_only\n","stderr":""}} -->
```python
ledger = {
    "service_transition": True,
    "data_and_records": True,
    "physical_assets": True,
    "internal_identities": True,
    "external_credentials": False,
    "contracts_and_licenses": True,
    "hazards_and_environment": True,
    "archives_and_residual_owner": True,
}

def open_domains(items):
    return sorted(name for name, complete in items.items() if not complete)

initial = open_domains(ledger)
print(f"closure_domains={len(ledger)}")
print(f"initial_complete_domains={len(ledger) - len(initial)}")
print("initial_open_domains=" + ",".join(initial))
print("initial_authorization=reject_open_retirement_obligation")

ledger["external_credentials"] = True
after = open_domains(ledger)
print(f"after_revocation_complete_domains={len(ledger) - len(after)}")
print(f"after_revocation_open_domains={len(after)}")
print("after_revocation_authorization=eligible_for_declared_metadata_gate")
print("status=synthetic_closure_ledger_consistent")
print("evidence=declared_boolean_status_only")
```

The fixture trusts declared booleans and scope. It does not discover obligations, authenticate evidence, validate authority or transfer acceptance, verify sanitization/property custody, observe deleted resources, test successors/archives, assess hazards, or prove closure.

## Definitions and Notation

Let retirement scope $R=(capability,effectivity,time,authority)$ and closure graph $G=(V,E,\tau)$. Each $v\in V_R$ requires disposition $d(v)$ with action, owner, authority, evidence, residual risk, retention and state. Relationships also require disposition: removing a service node while an interface edge remains can break a consumer.

Let inventory coverage be $c=|V_{dispositioned}|/|V_{known,required}|$. Even $c=1$ is conditional on discovery completeness and classification correctness. Unknown nodes are not in the denominator, so independent discovery and post-cutoff observation are essential.

Sanitization claim $S=(media,data,method,tool,verification,custody,threat)$ is bounded to identified media/data and threat effort. It neither proves record-law compliance nor removal of copies outside scope.

## Mechanisms, Invariants, or Proof Structure

A defensible decommissioning argument follows this chain:

1. establish retirement decision, authority, effectivity, service/records/property/environmental obligations, success criteria and residual owners;
2. maintain required operation/control while building declared and observed inventories of capabilities, users, dependencies, identities, information, assets, support, contracts and hazards;
3. assign each object and relationship to migrate, transfer, terminate, retain, sanitize, reuse, dispose or monitor with evidence and authority;
4. validate successor or termination outcomes, data/record transition, compatibility, capacity, operations, fallback and stakeholder acceptance;
5. preserve interpretable required records and sanitize/minimize information copies using media-, sensitivity-, threat- and destination-appropriate controls;
6. revoke digital/physical authority and remove network, automation, supplier and recovery paths;
7. disposition property/material through controlled custody, safety, environmental, security/export and accounting processes;
8. reconcile field/support obligations, contracts/licenses, facilities, configuration/asset/control-plane records and residual risks;
9. verify positive continuity/preservation and negative absence through independent discovery, inspection, tests and post-cutoff monitoring;
10. authorize bounded closure only when exceptions are resolved or explicitly transferred/accepted with funded durable ownership.

The conclusion is limited by discovery, provider/vendor visibility, evidence authenticity, observation duration, changing obligations and retained populations. Closure of routine operation does not eliminate all future responsibility.

## Alternatives and Trade-Offs

**Immediate cutoff versus staged transition.** Immediate removal reduces dual operation and attack surface but risks stranded consumers and irreversible loss. Staging enables discovery and reconciliation but adds cost, data divergence, ambiguity and extended exposure. Use bounded stages with exit criteria.

**Archive versus migrate versus destroy.** Archive preserves history but creates long-term privacy, security, format, ownership and cost obligations. Migration keeps information usable but can alter semantics/provenance. Destruction reduces exposure but may violate evidence, customer or legal needs. Classify by data/record purpose, not one system-wide rule.

**Reuse/transfer versus destruction.** Reuse conserves value and materials but requires sanitization, configuration, safety, ownership and recipient acceptance. Destruction can control sensitive capability but increases environmental/material loss. Apply property, security/export, safety and environmental authority.

**Cryptographic erase versus media destruction.** Cryptographic erase can be fast and preserve reuse when implementation and key coverage are trustworthy. Destruction may better bound confidentiality for unsupported/damaged media but sacrifices value and requires controlled debris. Media technology and threat decide.

**Retain legacy support versus force migration.** Retention protects field/customer obligations but prolongs vulnerabilities, skills, spares and cost. Forced migration reduces variants but can impose unsafe or contract-breaking transition. Define effectivity, support horizon and accepted exceptions.

**Internal disposal versus qualified vendor.** Internal work improves direct control but needs facilities, competence and permits. Vendors provide scale/specialization but add custody, downstream, evidence and contract risk. Audit and retain appropriate chain records.

## Failure Modes and Misconceptions

- **“Powered off means retired.”** Identities, data, dependencies, property, cost, access, contracts and hazards can persist.
- **“The successor is live, so migration is done.”** Reconcile every consumer, transaction, entitlement, record, site and recovery path.
- **“No recent traffic means unused.”** Seasonal, failure-only, offline and batch consumers may be invisible; evaluate observation coverage.
- **“Delete means sanitized.”** Media, remapping, backups, replicas, metadata, provider behavior and threat determine the claim.
- **“Encrypting data solves disposal.”** Key coverage/custody, plaintext copies, metadata, implementation and future cryptanalysis assumptions matter.
- **“Archive everything.”** Unnecessary retention adds privacy, security, cost, license and interpretation burden.
- **“Destroy everything.”** Legal hold, certification, incidents, customers, intellectual property, field support and historical evidence may require preservation.
- **“The vendor owns disposal risk.”** The accountable owner retains duties for custody, data, property, environmental and contractual evidence.
- **“Donation is harmless reuse.”** Sanitize, assess safety/export/control, transfer title, remove branding/keys and confirm recipient acceptance.
- **“Accounts were disabled.”** Tokens, keys, certificates, automation, vendors, break-glass, domains, routes and physical access remain candidates.
- **“Project closure ends ownership.”** Archives, hazards, field assets, claims and monitoring need named funded successors.
- **“A complete checklist proves completeness.”** It proves only declared entries; independent discovery must challenge scope.

## Worked Examples

### Example 1

A service shows zero interactive traffic for ninety days, but a quarterly financial close and disaster-recovery workflow still depend on it. Calendar and recovery testing reveal the hidden consumers before cutoff. Observation duration and scenario coverage bound an absence claim.

### Example 2

A database migrates to a successor. Counts match, yet time-zone interpretation changes and old backups, analytics exports and test snapshots retain personal data. Semantic reconciliation and copy-specific retention/sanitization replace a database-only closure.

### Example 3

Cloud resources are deleted, but DNS, OAuth trust, vendor support, service accounts, log exports, snapshots and reserved costs remain. Independent identity/network/billing scans and attempted-use monitoring find and disposition each remnant.

### Example 4

Laptops are donated after factory reset. Policy and media assessment show the reset is not an approved sanitization method for the installed storage and data sensitivity. Applicable sanitization, verification, custody and asset transfer occur before reuse.

### Example 5

A laboratory is closed with batteries, pressure vessels, chemicals, calibrated sources and contaminated equipment. Characterization precedes demolition; energy is isolated, hazardous chains documented, monitoring assigned and site records updated.

### Example 6

A field fleet remains supported after production retirement. Spares, firmware, repair tools, supplier data, certificates and training are retained for named serials until their end dates. Global retirement applies only to production, not the supported population.

### Example 7

A proprietary archive contains valid evidence but its reader license is ending. The organization preserves rights and controlled reader, exports to durable formats, validates representative and boundary records, records transformation loss, and tests independent retrieval.

### Example 8

A certificate authority is retired. Issuance stops first, but revocation/status endpoints, trust anchors, signed artifacts, audit evidence, emergency validation and relying-party migration persist. Key destruction occurs only under the applicable cryptographic and records plan.

### Example 9

Equipment is sold with a radio and controlled diagnostic capability. Property, export/security, sanitization, spectrum, branding and safety authorities require removal or demilitarization of specified functions and documented custody before sale.

### Example 10

All ledger boxes are green, but post-cutoff monitoring sees an unknown nightly request. Closure reopens, preserves evidence and finds an acquired subsidiary's scheduler. The consumer migrates and monitoring repeats; the ledger is evidence-driven, not irreversible ceremony.

## Cross-Program Connections

- **Platform engineering:** cloud inventory, identities, DNS/network, automation, observability, cost, recovery, package registries and old-platform removal define digital decommissioning.
- **API and service engineering:** consumers, versions, deprecation, contracts, fallback, traffic observation, data/state and endpoint withdrawal determine safe service retirement.
- **Data engineering:** lineage, copies, retention, legal hold, migration semantics, archives, privacy, sanitization and reproducibility govern information disposition.
- **Object-oriented/functional programming:** package/runtime/toolchain preservation, dependency removal, interface consumers, build provenance and executable archival affect software retirement.
- **Security/privacy:** least retention, identity/key revocation, sanitization, chain of custody, monitoring, incident evidence and attack-surface removal are central.
- **Supply/property/environment:** title, serials, spares, controlled technology, hazardous materials, reuse, recycling, demilitarization and disposal chains govern physical closure.
- **Verification/validation:** successor acceptance, migration reconciliation, archive retrieval, sanitization verification, negative tests and residual-risk decisions form closure evidence.
- **Lifecycle/knowledge:** configuration history, lessons, records, rights, funding and residual owners preserve accountability after teams and systems disappear.

## References

1. NASA, [Systems Engineering Handbook, Revision 2](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), including closeout and readiness-review guidance.
2. NASA, [Systems Engineering in Phase E, Appendix T](https://www.nasa.gov/reference/appendix-t-systems-engineering-in-phase-e/), accessed 2026-08-31.
3. NASA Software Engineering Handbook, [SWE-075 — Plan Operations, Maintenance, Retirement](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695456/SWE-075%2B-%2BPlan%2BOperations%2BMaintenance%2BRetirement), accessed 2026-08-31.
4. NIST, [SP 800-88 Rev. 2, Guidelines for Media Sanitization](https://csrc.nist.gov/pubs/sp/800/88/r2/final), published September 2025.
5. U.S. Department of Defense, [Materiel Disposition](https://www.acq.osd.mil/asds/log/disp.html), accessed 2026-08-31.
6. U.S. Department of Defense, [Disposition and Demilitarization Policy Issuances](https://www.acq.osd.mil/asds/log/policy_vault_issuances.html), accessed 2026-08-31.
7. NASA, [Technical Data Management, Systems Engineering Handbook section 6.6](https://www.nasa.gov/reference/6-6-technical-data-management/), accessed 2026-08-31.
8. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
9. NASA, [Technical Reviews and Decision Gates, Systems Engineering Handbook section 6.7.2.3](https://www.nasa.gov/reference/6-7-technical-assessment/), accessed 2026-08-31.
10. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.

## Exercises

### Exercise 1

Design a decommissioning plan for an autonomous warehouse service spanning robots, cloud, APIs, data/models, facilities, operators, customers, suppliers, spares, recovery and hazardous batteries.

### Exercise 2

A closure ledger has 24 known required entries: 19 complete with verified evidence, 2 transferred with documented recipient acceptance, 1 retained under approved residual ownership, 1 open critical item, and 1 unknown. Compute declared disposition coverage under two denominator treatments and decide whether closure is supportable.

### Exercise 3

Create an information disposition plan for a regulated service with databases, object storage, logs, backups, analytics exports, test data, endpoints, paper records, vendor copies and legal holds.

### Exercise 4

Design positive and negative closure evidence for retiring an API, identity provider and cloud platform after successor migration.

### Exercise 5

Audit a claim that physical disposal is complete because a recycler issued pickup receipts for all inventoried equipment.

## Answers to the Exercises

### Answer 1

Define retirement effectivity by customer/site, robot serial, service version and contract; authority for service, data, property, battery/environment, security and residual support; cutoff, fallback and post-close monitoring. Keep old services secure/supported until transition. Inventory users, robots/spares/repairs, APIs/jobs, cloud/network/DNS/identity, schemas/data/models/logs/backups/test copies, facilities/chargers/tools, supplier/vendor access, contracts/licenses, credentials, records and batteries/electronics.

Migrate customers and robot cohorts to successor or accepted termination. Test mixed versions, capacity, safety, identity, data semantics, offline robots, recovery and operator procedures; reconcile missions, entitlements, balances and records. Establish final sync/cutoff, late arrivals and rollback/forward recovery. Export/retain required configuration, evidence, model/data provenance and incidents; sanitize unnecessary copies/media under classification and destination; test archive retrieval.

Revoke service/vendor/robot credentials, certificates, domains/routes, automation and physical access; delete verified cloud resources/cost. Transfer or disposition robots, spares, tools and facilities; safely discharge/package/recycle batteries through qualified chains; sanitize controllers; update property/configuration. Preserve support for explicitly retained field assets. Verify successor outcomes and absence through discovery, traffic/identity/billing scans, physical inspection, sanitization/property receipts, archive test and monitored attempted use. Assign residual legal/environmental/archive owners and close only after exceptions resolve.

### Answer 2

If transferred-with-acceptance and approved retained items count as completed dispositions, 22 of 24 known required entries are dispositioned: $22/24\approx91.67\%$. The open critical item is not complete. The “unknown” is itself one known ledger entry describing unresolved scope, so it remains incomplete.

If analysis treats the unknown as evidence that at least one additional object exists beyond the 24 declared entries, the optimistic denominator is at least 25 and known dispositions cover at most $22/25=88\%$. The real denominator may be larger. Neither treatment supports closure: a critical item remains open and discovery completeness is contradicted by an unknown.

Quarantine affected operations/assets, assign owner/authority, discover the unknown, trace dependencies/effectivity and obtain evidence-backed disposition. Resolve or explicitly transfer the critical obligation only to an empowered accepting owner; critical risk cannot disappear through a percentage. Re-run independent inventories and post-cutoff tests. Coverage is workflow visibility, not proof of safety, legality, sanitization, continuity or completeness.

### Answer 3

Create a data map by copy, owner and medium: primary/replica databases, snapshots/backups, object versions, logs/traces, queues/caches, analytics exports, reports, test/training subsets, endpoint/removable media, paper and vendor/subprocessor systems. For each, record data classes/subjects, purpose, provenance, integrity/evidentiary need, retention schedule, legal hold, privacy/consent, license/IP, location/jurisdiction, access, successor/archive destination and deletion/sanitization authority.

Migrate required operational records with semantic mapping, control totals, referential/constraint checks, boundary sampling, provenance and recipient acceptance. Preserve held/regulatory records in durable formats with metadata, integrity, least access, funded steward, tools/keys and tested retrieval. Minimize or destroy expired/unnecessary information; propagate disposition to replicas, backups according to policy, analytics/test/vendor copies, endpoints and paper. For unavoidable backup aging, restrict access and prevent restoration into production without reapplying deletion obligations.

Choose media sanitization based on sensitivity, media technology, custody and reuse destination; verify and record method/tool/failed media. Obtain bounded provider/vendor evidence and audit rights. Revoke accounts/keys, close data flows, update catalogs/lineage/privacy records and monitor post-close access/cost. Legal holds override routine destruction until released by authority; release triggers controlled reclassification and disposition.

### Answer 4

Positive evidence: successor API contract/conformance, capacity/failure/recovery and representative consumer tests; identity authentication/authorization/revocation/federation/break-glass and audit results; data/entitlement reconciliation; customer and operational acceptance; backup/restore; exact configuration manifests; migrated monitoring/runbooks/support; and cohort/effectivity completion including offline/disaster-recovery clients.

Negative evidence: old API receives no expected traffic over a justified period and returns controlled retirement behavior; DNS/routes/firewalls/load balancers and service discovery no longer expose it; accounts, tokens, keys, certificates, federation, vendor/break-glass and automation are revoked; cloud inventory, regions/projects, snapshots/images/registries/log sinks and bills show no unapproved resources; vulnerability/attack-surface scans are clean; scheduled jobs and clients do not retry; old data copies are retained or sanitized per plan; recovery tests cannot resurrect unauthorized old state.

Use independent sources—gateway/network, identity, cloud inventory/billing, code/config search, customer inventory and attempted-use monitoring—and preserve raw evidence/coverage limits. Seed controlled tests where safe to prove alarms. Investigate any post-cutoff request rather than suppressing it. Closure remains bounded by observation duration, external-provider visibility and accepted residual archives/contracts.

### Answer 5

Pickup receipts prove custody transfer at one point for listed items, not lawful or complete disposal. Reconcile physical serials, asset register, locations, installed/field/spare/repair inventory and configuration to ensure nothing missing, substituted or unrecorded. Confirm title/disposal authority, recipient qualifications, contract, downstream chain, intended reuse/recycling/destruction, export/security/demilitarization, environmental permits and final certificates.

For each asset identify data-bearing media, embedded storage, keys/certificates, controlled functions, radio, hazardous materials, contamination, batteries, pressure/energy, safety markings and reusable parts. Verify applicable sanitization method/tool/result and failed-media handling before custody loss; factory reset or recycler promise is insufficient. Remove organizational identities/access, inventory labels where required and vendor service links. Validate packaging, transport and hazardous manifests.

Check that no field support, legal hold, incident, warranty, certification, customer, spares or recovery obligation required the item. Inspect recycler audit reports and downstream evidence proportionate to risk; sample certificates against serials/weights and exceptions. Update property/configuration/environmental/financial records and assign residual liability. Closure follows reconciliation and final disposition evidence, not pickup alone.
