---
module_id: SYSENG-008
program: Systems Engineering
level: 1
module_number: 8
title: Assumptions, Constraints, and External Dependencies
status: complete
last_verified: 2026-08-30
---

# Assumptions, Constraints, and External Dependencies

## One-Page Review

### Governing question

Which propositions, restrictions, and externally supplied capabilities must hold for the system to achieve its objectives—and how will the team detect, respond to, and govern their failure or change?

### Essential definitions

- An **assumption** is a proposition treated as true for a bounded analysis, design, plan, or decision although its truth is not fully established for the relevant conditions.
- A **validated assumption** has evidence adequate for its claim, scope, horizon, and consequence; it does not become universally true.
- An **invalidation trigger** is an observable condition requiring an assumption, model, design, or decision to be reviewed.
- A **constraint** restricts the admissible solution or operation space and derives from an authorized source such as physics, law, policy, stakeholder need, interface, budget, schedule, technology, or prior system.
- A **hard constraint** is non-compensable within the decision: violation makes an alternative inadmissible. A **soft constraint** may be traded under named authority.
- A **design choice** is selected by the team; it must not be mislabeled as an external constraint to prevent reconsideration.
- An **external dependency** is an entity, resource, service, condition, authority, or capability outside the chosen control boundary whose behavior is needed for an objective.
- A **dependency guarantee** states the behavior relied upon, including interface, semantics, capacity, quality, timing, continuity, change notice, and failure response.
- A **contingency** is a prepared response if the premise or dependency fails; **fallback** supplies reduced or alternate capability; **exit path** removes or substitutes the dependency.
- **TBD** identifies missing definition; **TBR** identifies a provisional value or claim requiring resolution. Both need owner, rationale, consequence, due date, and closure evidence.
- **Margin** is deliberate separation between expected/allocated demand and a limiting constraint; it is not a substitute for exposing uncertainty.

### Central model, mechanism, or theorem

Represent each objective or requirement as a claim supported by evidence and premises:

$$
Claim \Leftarrow Evidence \land Assumptions \land ConstraintsSatisfied
\land DependencyGuarantees.
$$

For decision/release horizon (T), readiness requires:

$$
Ready(T) \Rightarrow
\bigwedge_{a\in A_c} Valid(a,T)
\land \bigwedge_{c\in C_h} Satisfied(c)
\land \bigwedge_{d\in D_c}[Guaranteed(d,T)\lor AcceptableFallback(d,T)].
$$

This is a necessary governance rule for declared critical records, not proof that the register is complete or the system is safe. Trace objectives transitively through assumptions, constraints, interfaces, suppliers, enabling systems, and shared causes. A change at any node triggers impact analysis and revalidation of affected claims.

### Critical invariants

- Every material premise is explicit, uniquely identified, scoped, owned, evidenced, time-bounded, and linked to affected claims.
- Assumptions are not requirements, facts, wishes, estimates, risks, or design choices.
- Every constraint has a source, authority, rationale, applicability, hardness, and verification method.
- Hard versus soft is decided by authorized consequence, not wording or team preference.
- External does not mean unmanageable; dependency obligations and controls remain assigned internally.
- Contracts describe both required guarantees and behavior when guarantees are absent.
- Transitive and common-cause dependencies remain visible.
- Evidence age and environmental change can invalidate previously supported premises.
- No TBD/TBR crosses its authorized gate without explicit acceptance and consequence.
- Safety, security, legal, ethical, privacy, and clinical assumptions require applicable independent authority.

### Common failures

Failures include hiding assumptions in prose or spreadsheets; writing “supplier available” without capacity or outage semantics; converting an architectural preference into a constraint; calling a target a hard limit; treating a contract as proof of runtime behavior; monitoring uptime while relying on semantic correctness; ignoring identity, time, power, people, data, certificates, regulation, and support dependencies; testing a direct supplier but not its subcontractors; using stale evidence after scale or mode changes; closing a TBR by deleting it; double-counting shared fallbacks; and accepting residual dependency risk without named authority.

### Compact example

A service claims it can authenticate 20,000 requests per second. The claim assumes a traffic shape, clock accuracy, token size, key-cache hit rate, and identity-provider behavior. A regulatory constraint forbids retaining certain attributes. An external identity service must publish keys within a bounded interval and survive the service's request rate. The claim is not verified merely because a load test passed: the test must cover the assumptions, the privacy constraint must be checked, and identity failure/change paths must be exercised. If traffic, tokens, keys, law, or provider behavior changes, the evidence must be reconsidered.

### Connections

Retrieve boundaries, stakeholder value, feedback, openness, and uncertainty from Modules 001–007. Continue to operational scenarios and problem framing. Later requirements, interfaces, architecture, trade studies, risk, configuration, verification, validation, lifecycle, and systems-of-systems modules formalize these records and change controls.

## Governing Question

Every engineering conclusion rests on premises. Some are physical: a load stays below a limit. Some are operational: trained staff respond within five minutes. Some are institutional: a license remains valid. Some are supplied: an identity provider returns correct keys. The most dangerous premises are not necessarily false; they are invisible, unowned, stale, or applied outside the conditions supported by evidence.

The governing question is therefore not “do we have assumptions?” but “which claims fail when each premise changes, who can detect that change before consequence, and what response is prepared?” Assumptions, constraints, and dependencies belong in the engineering model because they shape requirements, architecture, verification, risk, operations, and lifecycle decisions.

## Why This Matters

An assumption can silently become an interface contract, capacity allocation, safety premise, or operating procedure. If it is never named, downstream teams may treat it as a fact. A constraint can eliminate otherwise attractive architectures; if its source is unclear, teams either violate a genuine obligation or overconstrain the design. An external dependency can determine availability and integrity even when procurement paperwork calls it “out of scope.”

NASA's systems engineering guidance calls for assumptions to accompany requirements and to be confirmed before baselining, while recording unresolved values with rationale, owner, action, and due date. ISO/IEC/IEEE 15288 and 29148 place assumptions, constraints, interfaces, enabling systems, and traceability in lifecycle and requirements work. NIST SP 800-160 warns that assumptions valid in one operating environment can be transferred invalidly to another and emphasizes trustworthy behavior under external conditions.

Management is not clerical. A list of assumptions without claim links does not support impact analysis. A supplier SLA without an operational monitor does not reveal semantic corruption. A fallback that shares identity, region, power, network, certificate authority, operator, or deployment pipeline with the primary can fail at the same time. Engineering must connect documentary obligations to observable system behavior and decision authority.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a boundary separates control authority from environmental influence, not relevance;
2. an interface is a governed exchange with semantics and failure behavior;
3. stakeholder objectives determine whether a restriction is mandatory or tradeable;
4. uncertainty type determines whether to measure, investigate, deliberate, bound, or adapt;
5. validation asks whether the system succeeds in its intended context;
6. feedback can amplify dependency failure through retries, queues, and operator action;
7. lifecycle modes introduce different environments and enabling systems.

Take the statement “the network is reliable.” Identify which network, paths, locations, modes, traffic, performance measures, duration, evidence, and decision it supports. Replace it with bounded propositions: packet loss below a threshold during nominal regional operation; recovery within a deadline after a single link failure; emergency voice preserved during data congestion. Each can now be linked, tested, monitored, and invalidated.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish assumptions, constraints, requirements, estimates, design choices, risks, and dependencies;
2. write assumption records with scope, evidence, owner, expiry, and invalidation triggers;
3. classify physical, regulatory, interface, resource, schedule, technology, and organizational constraints;
4. determine hard versus soft status using authorized sources and consequences;
5. map direct, transitive, shared, and enabling-system dependencies;
6. specify dependency guarantees and failure semantics;
7. compute margin and expose unsupported precision;
8. manage TBD/TBR items through explicit gates and closure evidence;
9. perform assumption- and dependency-driven impact analysis;
10. design monitoring, contingencies, fallbacks, exits, and appropriate external review.

## Core Exposition

**Separate record types.** An assumption says what is provisionally treated as true. A requirement says what must be achieved or constrained. An estimate quantifies an uncertain value. A hypothesis proposes a relationship to test. A design decision selects an alternative. A risk connects uncertainty to objectives and consequences. Conflating them obscures authority and closure.

“Users have broadband” is an assumption. “The system shall complete the workflow at 1 Mbps” is a performance requirement that may reduce reliance on it. “Median bandwidth will be 8–12 Mbps” is an estimate. “Compression improves completion” is a hypothesis. “Use codec X” is a design decision. “Low bandwidth prevents emergency reporting” is a risk scenario. Link them without rewriting one as another.

**Write a complete assumption record.** Use:

$$
a=(id,proposition,scope,mode,horizon,basis,confidence,owner,claims,
consequence,trigger,verification,expiry,status).
$$

The proposition must be falsifiable enough to observe. “Normal demand” is weak; “five-minute arrivals remain below 4,000 requests except declared campaign events through quarter end” can be checked. Scope names boundary, population, configuration, location, and lifecycle mode. Basis distinguishes measurement, contract, expert judgment, model, precedent, or hope.

**Treat validation as conditional.** Evidence can support an assumption for a horizon without proving it universally. Record sample, conditions, method, sensitivity, and alternatives. Evidence expires when time, scale, configuration, population, supplier, regulation, or environment changes materially. A validated assumption can become stale without becoming historically wrong.

**Define invalidation triggers.** Triggers can be calendar expiry, capacity threshold, configuration change, model residual, supplier notice, law revision, new stakeholder group, incident, environmental range, or anomaly trend. Connect triggers to review automation and responsible humans. A dashboard without an action owner only makes invalidity visible.

**Expose assumption chains.** Requirement R may rely on performance model M, which assumes workload W and supplier latency L; L may rely on a region and network. Trace transitively. Cycles are warnings: a demand forecast may assume a price that the architecture cost determines. Resolve jointly or explore scenarios rather than pretending an evaluation order removes the loop.

**Identify constraints by source.** Physical laws and environment impose mass, energy, geometry, temperature, and timing limits. Law, regulation, contract, policy, standards, and ethics impose obligations. Existing systems impose interfaces and compatibility. Resources impose cost, schedule, staff, facilities, and supply limits. Stakeholder needs can constrain access, language, location, or acceptable harm.

**Challenge alleged constraints.** Ask: who imposed it, where is the authoritative source, when and where does it apply, what happens on violation, and who can waive or change it? “We must use vendor X” may be contract, policy, sunk-cost preference, or unexamined habit. Only the first two may be externally imposed, and even they have scope and authority.

**Separate hard and soft.** A hard constraint removes an alternative within the current decision. Physics cannot be waived; legal or safety obligations require competent authority and may be non-compensable. Budget or schedule can be hard at one gate but renegotiable by a sponsor. Label the authority, not just `hard=true`. Soft constraints belong in trade criteria with weights or thresholds that remain visible.

**Verify constraints.** A citation proves a source exists, not that the design complies. Translate the constraint into applicable conditions and measurable evidence while preserving the governing text and interpretation authority. Verify mass by a controlled budget and measurement; privacy through data-flow analysis and tests; schedule through dependency-aware evidence; human access through representative validation.

**Manage margin.** If limit is (L) and current best estimate or allocation is (x), margin may be (L-x), with percentage convention explicitly stated. Keep uncertainty separate. A mass margin of 10 kg is not meaningful without confidence in estimates, growth, correlation, configuration, and when margin is consumed. Allocate, track, forecast, and define escalation thresholds.

**Model external dependencies.** Create a dependency record:

$$
d=(provider,capability,consumers,guarantee,interface,authority,
observation,failure,common\ causes,contingency,exit,owner).
$$

Provider can be supplier, regulator, operator, user, natural environment, utility, clock, certificate authority, data source, training organization, repair facility, or another product. External ownership does not remove the internal owner responsible for understanding and treating reliance.

**Write guarantees precisely.** State functional semantics, data meaning, identity, timing, throughput, capacity, availability, durability, geographic/legal boundary, quality, change compatibility, support, recovery, and evidence. Specify degraded and absent behavior. “API available 99.9%” omits whether results are correct, timely, compatible, authorized, and recoverable.

**Distinguish contract from behavior.** Procurement terms establish recourse and incentives. Architecture must handle actual behavior. Observe conformance, validate semantics, test faults, and retain evidence. A supplier can meet monthly availability while failing during the only mission window. Align measures and remedies with stakeholder objectives.

**Trace transitive dependencies.** A service depends on a database that depends on storage, identity, time, DNS, certificates, network, power, software supply, operators, and regional control planes. Inventory by scenario and objective rather than attempting an infinite universe. Ask suppliers for relevant critical dependencies and change/failure evidence; do not assume their boundary equals yours.

**Find common causes.** Two providers may share cloud region, upstream carrier, codebase, certificate authority, data source, deployment tool, owner, or geopolitical exposure. A manual fallback may use the same unavailable identity system. Model failure domains and exercise simultaneous loss. Diversity is evidenced separation, not two logos.

**Design contingencies and exits.** Avoidance removes reliance. Control reduces likelihood or consequence. Buffering uses inventory, caching, queues, time, or capacity. Fallback supplies reduced capability. Substitution changes provider. Graceful degradation protects priority objectives. Exit includes data portability, interface replacement, knowledge, licenses, credentials, records, migration time, and contractual rights. Each option creates costs and new assumptions.

**Govern TBD and TBR.** A placeholder must state why unresolved, candidate range/value, decisions affected, worst credible consequence, responsible owner, evidence needed, due date, and gate. Resolution means evidence and decision are recorded and dependent artifacts updated—not merely replacing text. Unresolved critical items require explicit gate authority.

**Use executable register checks carefully.** The example below flags stale/unverified/invalid assumptions, unsatisfied hard constraints, and critical dependencies lacking both a current guarantee and fallback. It prevents a narrow class of governance omission. It cannot discover hidden premises, judge evidence quality, interpret law, establish safety, or decide acceptable risk.

<!-- bijux-verify: {"id":"premise-and-dependency-readiness","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assumptions_total=4\nassumptions_valid=1\nassumptions_stale=1\nassumptions_unverified=1\nassumptions_invalid=1\nhard_constraints=2\nhard_constraints_unsatisfied=1\ncritical_dependencies=3\ncritical_dependencies_uncovered=1\nblocking_items=A-id-capacity,A-record-format,C-mass,D-weather\nrelease_ready=false\nevidence=declared_register_only\n","stderr":""}} -->
```python
today = 120
assumptions = [
    {"id": "A-weather-window", "status": "validated", "checked": 100, "max_age": 60},
    {"id": "A-traffic-shape", "status": "validated", "checked": 30, "max_age": 60},
    {"id": "A-id-capacity", "status": "unverified", "checked": None, "max_age": 30},
    {"id": "A-record-format", "status": "invalid", "checked": 115, "max_age": 30},
]
constraints = [
    {"id": "C-law", "hard": True, "satisfied": True},
    {"id": "C-mass", "hard": True, "satisfied": False},
    {"id": "C-cost-target", "hard": False, "satisfied": False},
]
dependencies = [
    {"id": "D-identity", "critical": True, "guaranteed": True, "fallback": False},
    {"id": "D-time", "critical": True, "guaranteed": False, "fallback": True},
    {"id": "D-weather", "critical": True, "guaranteed": False, "fallback": False},
]

counts = {"valid": 0, "stale": 0, "unverified": 0, "invalid": 0}
blocking = []
for assumption in assumptions:
    status = assumption["status"]
    if status == "validated":
        status = "stale" if today - assumption["checked"] > assumption["max_age"] else "valid"
    counts[status] += 1
    if status in {"unverified", "invalid"}:
        blocking.append(assumption["id"])

hard = [constraint for constraint in constraints if constraint["hard"]]
unsatisfied = [constraint for constraint in hard if not constraint["satisfied"]]
blocking.extend(constraint["id"] for constraint in unsatisfied)
critical = [dependency for dependency in dependencies if dependency["critical"]]
uncovered = [
    dependency
    for dependency in critical
    if not dependency["guaranteed"] and not dependency["fallback"]
]
blocking.extend(dependency["id"] for dependency in uncovered)

print(f"assumptions_total={len(assumptions)}")
for status in ("valid", "stale", "unverified", "invalid"):
    print(f"assumptions_{status}={counts[status]}")
print(f"hard_constraints={len(hard)}")
print(f"hard_constraints_unsatisfied={len(unsatisfied)}")
print(f"critical_dependencies={len(critical)}")
print(f"critical_dependencies_uncovered={len(uncovered)}")
print(f"blocking_items={','.join(sorted(blocking))}")
print(f"release_ready={str(not blocking).lower()}")
print("evidence=declared_register_only")
```

**Integrate with configuration and change.** Baseline assumptions, constraints, dependency contracts, and evidence with the architecture they justify. When a trigger fires, identify affected requirements, hazards, models, tests, operations, training, suppliers, and acceptance evidence. Reopen decisions intentionally; never silently edit history.

**Integrate with operations.** Convert material premises into monitors where observable: capacity, latency, error semantics, clock skew, certificate expiry, staffing, environmental range, inventory, license status, or policy version. Define alert ownership and response. Some assumptions need periodic audit or exercise because they are not continuously measurable.

**Escalate responsibly.** Engineers can expose conditional claims and evidence. They cannot unilaterally waive law, accept public harm, determine clinical efficacy, legitimize surveillance, or approve safety risk. Record applicable technical and nontechnical authority and preserve dissent when evidence or values remain contested.

## Definitions and Notation

Let (A_c) be critical assumptions, (C_h) hard constraints, and (D_c) critical external dependencies for a claim set and horizon (T).

For assumption (a):

$$
Valid(a,T)=Supported(a,E)\land ScopeMatches(a)\land T\le Expiry(a)
\land \neg Triggered(a).
$$

`Supported` is an evidence judgment under named method and authority, not a Boolean truth oracle.

For constraint (c), let $g_c(x)\le0$ express a quantitative admissibility condition where appropriate. Margin is:

$$
m_c=-g_c(x),
$$

so positive margin is inside the limit under the stated sign convention. For a simple upper limit $x\le L$, (m=L-x). Uncertainty in (x), (L), correlation, and model form remains separate.

For dependency (d), an assumption-guarantee contract is:

$$
EnvironmentAssumption_d \Rightarrow ProviderGuarantee_d.
$$

The consumer must verify that its environment satisfies the provider's assumptions and that the provider guarantee is adequate for consumer objectives. Composition fails when contracts are semantically mismatched even if syntax agrees.

Let a directed claim graph (G=(V,E)) connect objectives, requirements, assumptions, constraints, dependencies, decisions, and evidence. The impact set of changed node (v) is the reachable dependent set:

$$
Impact(v)=\{u\mid v\leadsto u\}.
$$

Graph reachability is only as complete and current as recorded edges.

## Mechanisms, Invariants, or Proof Structure

Use this premise-and-dependency procedure:

1. **Frame claim and horizon.** Name objective, configuration, boundary, modes, stakeholders, consequence, and authority.
2. **Elicit premises.** Ask what must already be true for each requirement, model, test, schedule, and decision to hold.
3. **Classify records.** Separate assumptions, estimates, hypotheses, constraints, decisions, dependencies, risks, TBDs, and TBRs.
4. **Trace sources and effects.** Link authoritative source, evidence, claims, hazards, interfaces, and downstream artifacts.
5. **Specify scope and observables.** Define population, conditions, units, tolerances, semantics, horizon, monitor, and trigger.
6. **Map dependency chains.** Include enabling systems, suppliers, people, authorities, common causes, and lifecycle modes.
7. **Design treatment.** Validate, constrain, add margin, monitor, buffer, diversify, degrade, fall back, substitute, or exit.
8. **Set closure gates.** Assign owner, evidence, due date, review independence, and authorization for unresolved items.
9. **Exercise failure and change.** Test absence, delay, corruption, incompatibility, overload, recovery, and simultaneous causes.
10. **Baseline and revalidate.** Preserve decision history and reopen affected claims when triggers fire.

Five invariants guide review.

**Explicitness invariant.** A material premise never exists only in narrative implication or individual memory.

**Authority invariant.** Constraint hardness, waiver, TBR acceptance, and residual consequence have named decision authority.

**Traceability invariant.** Every critical record links upstream source/evidence and downstream affected claims.

**Failure-semantics invariant.** Every critical dependency specifies degraded, absent, corrupt, delayed, and changed behavior as applicable.

**Freshness invariant.** Evidence has scope and expiry; configuration or environmental change triggers reassessment.

## Alternatives and Trade-Offs

**Validate assumption versus design it out.** Evidence may be cheap when the premise is stable. Removing dependence can produce a more robust design but add cost or constrain value. Compare lifetime verification cost and failure consequence.

**Contract versus technical control.** Contracts allocate obligation and remedy. Technical controls detect, tolerate, or recover from actual behavior. High-consequence reliance commonly needs both.

**Primary/fallback versus independent diversity.** A fallback improves resilience only if it covers required objectives and avoids the same failure domains. Stronger independence costs integration, testing, operational skill, and data consistency.

**Margin versus precision.** Better evidence can reduce uncertainty and required reserve. Margin buys tolerance but consumes resources. Use sensitivity to decide whether to learn or reserve.

**Hard constraint versus trade criterion.** Treating everything as hard eliminates design space. Treating obligations as weighted criteria permits invalid compensation. Preserve source authority and non-compensable thresholds.

**Continuous monitoring versus periodic review.** Monitoring detects observable drift quickly but adds infrastructure and can miss semantics. Reviews handle qualitative, regulatory, and organizational change but have latency. Combine them by trigger type.

**Standard interface versus provider-specific optimization.** Standardization supports substitution and exit. Provider-specific features can improve performance but increase lock-in and migration complexity. Price optionality explicitly.

**Early resolution versus deferred commitment.** Resolving critical uncertainty early prevents rework. Deferral preserves options when evidence will improve naturally. Do not defer past the point at which alternatives or safe verification disappear.

## Failure Modes and Misconceptions

1. **An assumption is probably true.** Probability without scope, evidence, horizon, and consequence is not governable.
2. **Validated means fact.** Evidence is conditional and can expire.
3. **The requirement makes the assumption true.** Normative text cannot establish an environmental condition.
4. **Architecture choice is a constraint.** Team decisions remain reconsiderable unless an external authority makes them binding.
5. **External means out of scope.** Reliance remains inside the system's outcome and risk model.
6. **An SLA guarantees mission success.** Measures may be misaligned, averaged, or semantically incomplete.
7. **Two suppliers are independent.** Shared infrastructure, software, authority, or geography can defeat redundancy.
8. **Fallback exists because a diagram shows it.** Capability, state, data, access, capacity, and exercised recovery must be evidenced.
9. **Monitoring controls the dependency.** Observation without response authority does not treat failure.
10. **TBD/TBR is harmless documentation debt.** It can hide undecided interfaces, hazards, budgets, and acceptance criteria.
11. **Margin covers any uncertainty.** Unknown bias, wrong model, and common cause can consume it unexpectedly.
12. **A complete register proves safety.** Completeness and acceptability require domain evidence and authority beyond a list.

## Worked Examples

### Example 1

**Question:** How should a foundation design handle an assumed soil bearing capacity?

**Assumptions:** Early design uses 200 kPa based on nearby borings; site-specific strata, groundwater, variability, and construction effects are not yet characterized.

**Reasoning:** Record the value as provisional, not a fact: location, depth, loading mode, settlement criterion, basis, uncertainty, affected loads and geometry, owner, geotechnical investigation, due gate, and consequence. Explore designs across a credible range and preserve adjustment options. Site investigation can validate or revise the premise; construction observations can still trigger reassessment. A code minimum and safety factor are constraints/controls, not evidence that the assumed soil matches the site.

**Evidence limit:** Nearby data support preliminary exploration only. Qualified geotechnical analysis, representative sampling, laboratory/in-situ tests, groundwater/environmental assessment, and applicable authority are required.

**Conclusion:** A provisional physical premise must be bounded, traced, investigated, and prevented from hardening invisibly into architecture.

### Example 2

**Question:** Is a data-retention rule a hard constraint?

**Assumptions:** A service operates in multiple jurisdictions and processes records with different legal and contractual categories.

**Reasoning:** Locate governing text, applicability, effective date, record class, jurisdiction, exceptions, conflicts, interpretation owner, and waiver authority. One rule may require deletion while another requires preservation. Translate each applicable obligation into data classification, lifecycle, hold, deletion, audit, and evidence requirements without replacing the source. If violation is not compensable within the product trade, treat it as hard. A preferred 30-day default may remain a design decision or soft objective.

**Evidence limit:** Engineering analysis cannot establish legal interpretation. Counsel/privacy authority, data owners, records specialists, security, and affected stakeholders may need review.

**Conclusion:** Constraint hardness follows applicable authority and consequence, not a generic “compliance” label.

### Example 3

**Question:** Is a fixed budget a constraint or an objective?

**Assumptions:** The sponsor authorizes a ceiling for the current decision gate but can revise scope or funding through governance.

**Reasoning:** Within the gate, the ceiling can be a hard admissibility constraint for the project team. At portfolio level, cost, scope, schedule, and value may be traded by the sponsor. Record amount, currency/date basis, included lifecycle costs, contingency, confidence, escalation, and authority. Do not conceal an overrun by narrowing the boundary. Conversely, do not reject a high-value alternative as physically impossible when sponsor action could change the ceiling.

**Evidence limit:** A point estimate is not compliance. Cost model, uncertainty, dependencies, inflation, schedule coupling, reserve policy, and independent review determine confidence.

**Conclusion:** Hardness is relative to decision authority and horizon; the same budget can be binding locally and negotiable upstream.

### Example 4

**Question:** What must be modeled when authentication depends on an external identity provider?

**Assumptions:** Login, token validation, signing-key publication, time, DNS, certificates, network, and provider administration cross the boundary.

**Reasoning:** Specify identity semantics, tenant/configuration, key rotation, cache duration, clock tolerance, throughput, latency, outage behavior, revocation, compromise notice, compatibility, data location, support, and recovery. Map transitive dependencies and shared control plane. Decide which functions require live provider access and which can use bounded cached evidence. Exercise provider outage, stale/incorrect key, clock skew, DNS/certificate failure, rate limiting, account misconfiguration, and compromised administration. Assign local owner and fallback authority.

**Evidence limit:** Contract and nominal login tests do not establish correctness or resilience. Fault tests, monitoring, configuration attestation, incident evidence, and security/privacy review are needed.

**Conclusion:** The dependency is a bundle of guarantees and failure paths, not a box labeled “IdP.”

### Example 5

**Question:** Can satellite time use GPS with an internal oscillator as fallback?

**Assumptions:** GPS may be unavailable, jammed, spoofed, or degraded; the oscillator drifts with temperature and age; some functions tolerate more error than others.

**Reasoning:** Allocate time accuracy by mission function and outage duration. Characterize oscillator holdover under environmental range and aging, detect inconsistent sources, define trust/selection logic, and specify recovery without unsafe time jumps. GPS and ground correction may share antenna, processing, or authority. Monitor offset and uncertainty, not simply source presence. The fallback is adequate only for a bounded duration and function set; beyond it the system must degrade or enter safe mode.

**Evidence limit:** Bench drift and nominal GPS reception do not cover radiation, aging, spoofing, antenna fault, simultaneous loss, or recovery transients. Applicable mission and safety authority must accept limits.

**Conclusion:** Fallback claims require quantified capability, independence, transition behavior, and expiration.

### Example 6

**Question:** How should a team handle a supplier's transitive software dependencies?

**Assumptions:** A purchased component includes libraries, build services, signing, update distribution, vulnerability intelligence, and maintainer support.

**Reasoning:** Identify components and versions, provenance, licenses, build/signing trust, critical maintainers/services, update authority, disclosed vulnerabilities, end-of-support, and replacement path. Prioritize by mission consequence and exposure rather than collecting an infinite tree without decisions. Require relevant supplier evidence and change notice, verify artifacts, monitor material changes, and exercise update/rollback. Two products sharing the same library or signing service have common cause even if purchased separately.

**Evidence limit:** An inventory describes declared composition at a point in time; it does not prove absence of hidden code, integrity, exploitability, maintainer continuity, or timely remediation.

**Conclusion:** Manage transitive reliance as evolving assurance and lifecycle evidence, not a one-time component list.

### Example 7

**Question:** Why did a validated traffic assumption fail after launch?

**Assumptions:** Load testing validated 2,000 requests per second with a recorded distribution, payload, cache state, and client retry policy.

**Reasoning:** Launch changed scale and behavior: marketing synchronized arrivals, larger payloads reduced service rate, cold caches increased dependency calls, and retries formed reinforcing load. The old evidence may have been correct within its scope yet transferred outside it. Trace each assumption to capacity and queue claims, compare production residuals, and update tests with correlation, burst, payload, cache, retry, and dependency scenarios. Add triggers before saturation and cap amplification.

**Evidence limit:** Production observation after harm does not validate a universal model. Controlled replay, shadow load, staged exposure, dependency tests, and uncertainty ranges support revised claims.

**Conclusion:** Validation expires when population, configuration, interaction, or mode leaves the supported envelope.

### Example 8

**Question:** What makes a TBR acceptable at a design review?

**Assumptions:** Final sensor latency is unknown; a provisional 80 ms drives controller stability analysis and interface budgets.

**Reasoning:** Record candidate range, basis, sensitivity, affected requirements/models/tests, worst consequence, supplier evidence plan, owner, due date, and last reversible design point. Analyze stability across the range and reserve timing margin. If values above 100 ms make the architecture unsafe and supplier evidence arrives after hardware freeze, the TBR cannot pass without redesign, alternate sensor, or authorized gate exception. Closure requires measured/qualified latency, updated model and allocations, and reverified conclusions.

**Evidence limit:** Replacing “TBR” with a number does not close it. Evidence must match configuration, temperature, load, network, processing, and tail requirements.

**Conclusion:** A placeholder is governed uncertainty with consequences and a closure path, not permission to postpone thought.

### Example 9

**Question:** How should an operational staffing assumption be engineered?

**Assumptions:** Safe recovery assumes two trained operators respond within ten minutes at all hours.

**Reasoning:** Define qualifications, independence, location, access, alert delivery, response-time distribution, workload, fatigue, language, decision rights, simultaneous incidents, and training currency. Link the assumption to hazards, procedures, interfaces, and validation. Evidence may include rosters, drills, access tests, and observed response, but staffing changes and rare conditions trigger review. If sustained staffing is not credible, redesign for longer autonomous safety, remote support, simplified recovery, or reduced operation.

**Evidence limit:** A policy and signed training record do not prove availability or performance under stress. Human-factors, safety, labor, operational, and applicable regulatory review may be required.

**Conclusion:** People are system elements and dependencies whose capacity and conditions must be modeled without treating them as deterministic components.

### Example 10

**Question:** How should a medical device manage an assumption about hospital network availability?

**Assumptions:** The device can perform a safety-critical local function but uses the network for identity, configuration, records, monitoring, and updates across diverse hospitals.

**Reasoning:** Separate functions by required connectivity and outage duration. Define local safe behavior, cached authorization limits, configuration provenance, record buffering, time, alarm delivery, reconciliation, update policy, capacity, cybersecurity, privacy, and recovery. Validate across network loss, latency, partial reachability, incorrect data, certificate/identity failure, power events, maintenance, and emergency workflows. Record which claims depend on hospital controls and what installation evidence is mandatory.

**Evidence limit:** Laboratory network tests and vendor agreements do not establish clinical workflow, local infrastructure, safety, legal compliance, or acceptable residual risk. No external clinical, regulatory, academic, or practitioner review is claimed.

**Conclusion:** High-consequence external assumptions require bounded local safety, installation-specific evidence, monitoring, and named independent authority.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) turns premises into quality-attribute drivers, boundaries, tactics, and decision records.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) manages source, schema, quality, lineage, timeliness, and supplier assumptions.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) addresses trust boundaries, external systems, supply chains, assurance, and contested environments.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) models partial failure, time, coordination, and dependency semantics.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) specifies compatibility, capacity, failure contracts, and change behavior.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) governs dependencies and guarantees between platform and consuming teams.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, May 2023. Consulted 2026-08-30.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, November 2018. Consulted 2026-08-30.
3. NASA. [*NASA Systems Engineering Handbook*, Rev. 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Consulted 2026-08-30.
4. NASA. [Systems Engineering Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), including requirements validation and interface outlines. Consulted 2026-08-30.
5. Ron Ross, Mark Winstead, and Michael McEvilley. [*Engineering Trustworthy Secure Systems*](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), NIST SP 800-160 Vol. 1 Rev. 1, November 2022. Consulted 2026-08-30.
6. SEBoK Editorial Board. [System Requirements](https://sebokwiki.org/wiki/System_Requirements), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
7. SEBoK Editorial Board. [Requirements Management](https://sebokwiki.org/wiki/Requirements_Management), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
8. International Organization for Standardization. [ISO 31000:2018 — Risk management — Guidelines](https://www.iso.org/standard/65694.html), second edition, 2018. Consulted 2026-08-30.

## Exercises

### Exercise 1

Rewrite these statements as governed records: “traffic will be normal,” “we have to use vendor X,” “the network is reliable,” “operators will handle failures,” and “the interface is standard.” Classify each record and state evidence, owner, trigger, consequence, and closure path.

### Exercise 2

A vehicle has a 1,000 kg hard mass limit. Current best estimates are structure 410±20, propulsion 260±15, payload 210±10, avionics 65±8, and harness/fluids 35±12 kg, where ranges are not yet assigned a probability meaning. Compute nominal margin and explain what can and cannot be inferred.

### Exercise 3

Map direct, transitive, and common-cause dependencies for a public API that uses cloud compute, managed database, identity, DNS, certificates, time, observability, source/build/update services, operators, and a third-party data source. Design two credible failure exercises.

### Exercise 4

Create a TBR closure plan for a battery's minimum cold-temperature endurance. Include range, affected claims, evidence, environmental and aging conditions, due gate, last reversible point, margin, failure response, and authority.

### Exercise 5

Review assumptions, constraints, and dependencies for an automated railway-door control capability. Cover physical, software, electrical, sensing, human, operational, maintenance, accessibility, safety, security, regulatory, supplier, emergency, and retirement concerns.

## Answers to the Exercises

### Answer 1

“Traffic will be normal” becomes a demand assumption with measurable arrival, burst, payload, geography, client/retry, mode, horizon, evidence, capacity claims, monitor, expiry, and saturation trigger. “We have to use vendor X” is unresolved until an authoritative contract/policy and waiver scope prove a constraint; otherwise it is a design choice. “The network is reliable” becomes dependency guarantees for availability, latency, loss, capacity, semantics, partitions, recovery, location, and modes. “Operators will handle failures” becomes staffing, skill, access, workload, response, authority, and procedure assumptions plus human-system requirements. “The interface is standard” becomes named version/profile, semantics, options, compatibility, conformance evidence, and provider change dependency.

Each record needs a local owner even when source is external, downstream claim/risk links, consequence if false, evidence type and scope, invalidation triggers, review date, and treatment. Closure can mean validating within bounds, converting an authorized obligation to requirements, designing out reliance, implementing/validating fallback, or recording explicit gate acceptance. Deleting or rewording the premise is not closure.

### Answer 2

Nominal estimated mass is (410+260+210+65+35=980) kg, so nominal margin is (1000-980=20) kg, or 2% of the limit if percentage is defined against the limit. The component ranges sum to 65 kg under worst-direction interval addition, yielding a possible 1,045 kg total and -45 kg margin if all upper deviations can coincide. That bound may be conservative, but no root-sum-square or probability of violation is justified because distribution, coverage, bias, and dependence meanings are absent.

Trace estimate maturity and common growth causes, define each range, update configuration, and perform sensitivity. Protect reserve, reduce or redesign mass, or obtain better evidence before committing. The nominal 20 kg does not establish compliance. Final acceptance requires controlled configuration, measurement/validated prediction, uncertainty treatment, and authorized margin policy.

### Answer 3

Direct dependencies include compute, database, identity, DNS/certificates/time, telemetry, operators, and data provider. Transitive dependencies include regions/zones, network, storage, control planes, certificate authority, upstream DNS, time sources, power, build runners, registries, signing keys, source hosts, alert delivery, staff identity/access, and the data provider's sources. Common causes include shared region/network/control plane, identity, DNS, certificate authority, code/library, deployment pipeline, account, data source, operator team, and geopolitical/legal exposure.

Exercise one removes identity and DNS while tokens/keys expire: observe cached verification bounds, administrative access, alerts, safe read/write behavior, recovery, and audit. Exercise two corrupts/delays third-party data while the managed database throttles and clients retry: observe semantic validation, stale-data policy, load amplification, priority degradation, operator action, rollback, and customer effects. Predefine guardrails, owners, stop/recovery, evidence, and no-production alternatives for unacceptable consequence.

### Answer 4

Record a provisional endurance range, cell chemistry/configuration, state of charge, load profile, temperature dwell/ramp, wind/thermal conditions, age/cycles, manufacturing variation, measurement uncertainty, heater/control policy, and safety limits. Trace mission duration, reserve, thermal, power, shutdown, rescue/recovery, and acceptance claims. Run sensitivity across the range and define margin and a conservative operating envelope.

The plan names representative chamber and aged-sample evidence, model correlation, sample rationale, responsible battery/thermal/test/safety owners, due gate, and the last point to change cell capacity, insulation, heater, mission, or fallback. Define what happens if endurance is below threshold and who can accept reduced mission or redesign. Closure updates the value/range, evidence, models, allocations, hazards, requirements, tests, operations, and decision record; a number alone is insufficient.

### Answer 5

Assumptions cover train speed/state, platform geometry, passenger behavior, obstruction detectability, sensor environment, power, timing, braking/interlocks, operator attention, maintenance quality, software/hardware configuration, communications, emergency response, accessibility needs, and lifecycle support. Constraints derive from vehicle/platform geometry and dynamics, applicable railway/safety/accessibility/security law and standards, stopping/service objectives, interfaces, power, evacuation, and authorized operating rules. Dependencies include sensors, actuators, train control, power, time, passenger information, operators, maintainers, tools, suppliers, configuration/update, spare parts, infrastructure, emergency services, and regulators.

Specify safe-state and degraded behavior for missing, delayed, inconsistent, obstructed, spoofed, or failed inputs; door/traction interlocks; manual/emergency release; detection limits; timing/capacity; maintenance access; audit; and recovery. Trace common causes and mode changes through boarding, movement, fault, evacuation, maintenance, update, and retirement. Evidence requires hazard analysis, independent safety assurance, requirements/interface verification, fault injection, environmental and human-factors/accessibility validation, cybersecurity, maintenance trials, configuration control, supplier assurance, and operational exercises. Automation cannot approve acceptable residual risk, accessibility, regulation, worker/passenger legitimacy, or emergency authority. Named railway safety, operations, human-factors/accessibility, software, electrical/mechanical, cybersecurity, maintenance, regulatory, and emergency authorities must review applicable claims. No external safety, regulatory, academic, or practitioner review is claimed.
