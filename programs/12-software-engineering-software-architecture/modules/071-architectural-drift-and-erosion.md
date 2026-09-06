---
module_id: SARCH-071
program: Software Engineering: Software Architecture
level: 2
module_number: 71
title: Architectural Drift and Erosion
status: complete
last_verified: 2026-09-06
---

# Architectural Drift and Erosion

## One-Page Review

### Governing question

How can an organization distinguish useful architectural evolution from accidental divergence, detect consequential erosion across source, data, deployment, runtime, and organizational structures, and choose whether to accept, constrain, repair, migrate, or retire what it observes?

### Essential definitions

- **architectural intent** is the set of consequential principles, decisions, relations, responsibilities, and quality assumptions meant to govern a system;
- the **observed architecture** is the structure and behavior evidenced in implemented and operating artifacts, not merely a reconstructed diagram;
- **architectural drift** is divergence between relevant intent and observed reality; it is a discrepancy to explain, not automatically a defect;
- **architectural erosion** is cumulative damage to important architectural properties or the system's capacity for safe, economical evolution;
- a **violation** is an observed relation or behavior forbidden by an applicable architectural constraint;
- **conformance** is a stated relation between a named architectural model and named observations under an explicit mapping and rule set;
- a **reflexion model** compares a hypothesized high-level model with facts extracted from a lower-level artifact, classifying convergence, divergence, and absence;
- an **absence** is a required architectural relation not found in the observation set; absence may indicate missing implementation or incomplete observation;
- a **waiver** is an authorized, scoped, owned, expiring exception whose risk and removal or acceptance conditions are recorded;
- **architecture debt** is a present architectural compromise that creates expected future cost, constraint, or risk; it is not a synonym for every inconsistency.

### Central model, mechanism, or theorem

Let $P$ be permitted high-level relations, $R\subseteq P$ required relations, $O$ observed mapped relations, and $\mu$ the mapping from implementation elements to architectural elements. Then

$$
C=O\cap P,\qquad D=O\setminus P,\qquad A=R\setminus O.
$$

$C$ contains convergences, $D$ divergences, and $A$ absences. Under this deliberately simple model, conformance requires $O\subseteq P$ and $R\subseteq O$. The result is conditional on the scope, observation method, mapping, and freshness of $P$, $R$, and $O$. A count of divergences is not a measure of architectural harm.

### Critical invariants

- intent and observation have named versions, scopes, owners, and evidence times;
- rules express consequential constraints, not aesthetic preferences disguised as law;
- source dependencies are not treated as the whole architecture;
- mappings preserve unknown and ambiguous cases rather than forcing false precision;
- permitted does not mean required, and unobserved does not necessarily mean absent;
- drift is investigated before the implementation or the intent is declared wrong;
- severity reflects affected qualities, authority, propagation, reversibility, and exposure, not raw violation count;
- emergency exceptions are visible, bounded, owned, tested, and retired or accepted deliberately;
- repair includes updating obsolete intent when evidence supports the implemented design;
- enforcement never substitutes for architecture ownership, operational learning, or an evolution strategy.

### Common failures

Common failures include declaring every code dependency architectural; comparing current code with a stale diagram; hiding configuration, data, identity, batch, support, and runtime paths; treating an optional relation as required; equating zero detected violations with conformance; ranking risk by rule counts; suppressing a beneficial implementation because the intent is obsolete; allowing permanent emergency waivers; adding fitness functions without owners; forcing uncertain mappings; rebuilding before understanding causality; measuring coupling once without a trend or denominator; and calling architecture debt a moral failure rather than an economic and risk decision.

### Compact example

An intended checkout architecture permits `web -> orders`, `orders -> payments`, and `orders -> catalog`, and requires the first two relations. Runtime traces reveal `web -> payments`. The relation is a divergence, but the trace alone does not establish erosion. Investigation shows a support-only refund path bypasses the order authority, produces duplicate refund decisions during retries, and has no expiring waiver. The team restores the order boundary, adds a runtime rule for the refund path, and records the missing support-console view. The decision rests on authority and failure consequences, not on one red edge.

### Connections

[SARCH-064](064-architecture-fitness-functions.md) supplies executable constraint feedback, [SARCH-065](065-dependency-and-coupling-metrics.md) supplies carefully bounded structural measures, and [SARCH-070](070-running-an-evidence-based-architecture-review.md) supplies evidence and decision discipline. [SARCH-072](../ROADMAP.md) next develops principles for purposeful evolutionary architecture.

## Governing Question

Software must change while architecture is expected to preserve important reasoning across change. That creates an apparent contradiction: if every divergence is prohibited, the architecture fossilizes; if every local change is accepted, system-wide properties can disappear by accumulation. The governing problem is therefore not how to freeze a design. It is how to keep intent, evidence, and reality in a controlled conversation.

Architectural drift is best treated as a discrepancy requiring classification. The implementation may be defective, the architecture description may be stale, the mapping may be wrong, or the environment may have changed. Erosion is the stronger conclusion: an important property, boundary, rationale, or ability to evolve has actually deteriorated. Reaching that conclusion requires evidence of consequence, not merely a comparison tool.

## Why This Matters

Most damaging erosion is locally rational. A team bypasses a service to meet a deadline, shares a database table to repair an incident, adds a synchronous call to simplify one workflow, or grants a broad identity because the least-privilege path is unavailable. Each change may be small and reversible in isolation. Together they can create cycles, hidden authorities, correlated failures, deployment lockstep, inconsistent data ownership, and a growing cost of change.

Architecture descriptions also drift. A pristine model may describe a system that never existed, omit operational and administrative paths, or preserve constraints whose rationale expired. Enforcing such a model can increase risk. A reliable drift practice therefore treats architecture documents, rules, mappings, observations, and conclusions as fallible, versioned evidence.

The issue is broader than source code. Modern systems express architecture through package graphs, API and event contracts, schemas, migration jobs, infrastructure definitions, network policy, identity grants, service discovery, feature flags, deployment topology, observability, runbooks, supplier behavior, and team ownership. A static dependency scan can pass while runtime authority and failure containment have already eroded.

## Prerequisites and Retrieval

Retrieve architecture, architecture description, element, relation, principle, rationale, stakeholder concern, quality attribute, constraint, module, component, connector, dependency, coupling, cohesion, cycle, authority, data ownership, interface contract, runtime trace, topology, configuration, policy, invariant, fitness function, technical debt, expected loss, change coupling, version control, causal inference, and residual risk.

From SARCH-064, recall that a fitness function is an objective, executable evaluation of an architectural characteristic, with explicit scope and ownership. From SARCH-065, recall that coupling metrics describe selected graph projections and do not directly measure quality. From SARCH-070, retrieve baselining, evidence provenance, claim limits, and decision authority. This chapter applies those ideas to architecture evolution; it does not replace security, safety, privacy, legal, financial, or domain-specific assurance.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish drift, erosion, conformance violation, software aging, architecture debt, and legitimate evolution;
2. construct and interpret a bounded reflexion model with permitted, required, observed, and uncertain relations;
3. recover architectural evidence from source, configuration, data, deployment, runtime, identity, operations, and organizational artifacts;
4. evaluate mapping quality, observation coverage, model freshness, and rule ownership before claiming conformance;
5. detect structural, behavioral, data, operational, security, and organizational forms of erosion;
6. combine automated constraints, trend measures, change history, incidents, and qualitative investigation;
7. distinguish correlation, symptom, mechanism, and causal explanation in erosion evidence;
8. prioritize discrepancies by consequence and learning value rather than raw count;
9. choose among accepting new reality, updating intent, containing, repairing, migrating, or retiring a structure;
10. govern exceptions and architectural knowledge so that change remains possible without silent decay.

## Core Exposition

**Define the comparison before running a tool.** Architecture is not one graph. Select the concern and viewpoint: compile-time dependency, runtime call, data authority, deployment containment, trust, recovery, ownership, or another consequential relation. Name the system boundary, architecture revision, implementation and deployment revisions, environment, observation window, and excluded paths.

A rule such as “presentation must not depend on persistence” is incomplete until `presentation`, `depend`, and `persistence` are operationally mapped. Does a generated client count? Does a shared schema count? Does a runtime message through an intermediary count? Does a test fixture count? Different answers can be legitimate, but hidden answers make results irreproducible.

**Distinguish prescription from description.** A prescriptive model states intended constraints and required structure. A descriptive model records structure inferred or observed from artifacts. Neither is automatically authoritative about the other. The intended model may contain rationale unavailable in code; the observed model may reveal operational mechanisms absent from documentation.

ISO/IEC/IEEE 42010:2022 distinguishes an architecture from an architecture description expressing it [1]. This matters operationally: a diagram can be internally consistent yet inaccurate about the deployed system. Conversely, an extraction can accurately report a source graph while omitting behavior, data, environment, and rationale that belong to the architecture.

**Use drift as a neutral trigger.** Perry and Wolf distinguished drift from erosion in their foundational treatment: drift involved change insensitive to architecture, while erosion involved violations of architectural design concepts [2]. Later literature uses the terms inconsistently and sometimes combines them [3]. This chapter uses drift for detected divergence and reserves erosion for evidenced architectural deterioration. State a project's vocabulary because a label does not settle the diagnosis.

Drift can be beneficial. An implementation may introduce an effective boundary discovered through production learning, replace an obsolete integration, or route around an invalid assumption. The appropriate response may be to revise the intended architecture and its rationale. A drift detector that can only say “change the code” is a brittle policy engine, not an evolution mechanism.

**Build a reflexion model.** Software reflexion models compare a high-level model with facts extracted from an implementation through an explicit mapping [4]. Begin with a small model relevant to the current question. Define high-level elements and permitted and required relations. Extract lower-level facts, map their endpoints, aggregate mapped facts, and classify the result.

Convergence means an observed mapped relation is permitted. Divergence means an observed relation is not permitted. Absence means a required relation was not observed. An optional permitted relation that is not observed is neither a violation nor an absence. Preserve the lower-level facts behind each aggregate edge so reviewers can inspect causes and avoid repairing an abstraction artifact.

**Treat mapping as evidence.** Mapping files often dominate the result. Names rarely correspond cleanly to architectural elements. Generated code, shared libraries, plug-ins, reflection, dynamic loading, foreign-function interfaces, build-time processors, infrastructure resources, and third-party services complicate classification. A file or service may participate in multiple concerns.

Allow unmapped and ambiguous facts. Report their proportion and potential consequence. A forced mapping produces clean-looking but invalid conclusions. Review changes to mapping rules like code because moving one package pattern can make hundreds of apparent violations disappear without changing the system.

**Observe more than source.** Static source analysis can expose import, call, inheritance, data-flow, and package relations within supported languages. Build manifests and dependency locks expose supply and version relations. Contract registries and schema histories expose compatibility. Database grants, queries, change-data capture, and lineage expose data authority and bypasses.

Infrastructure definitions, orchestrator state, routing, network policy, and service discovery expose deployment and communication. Traces, logs, profiles, and telemetry expose exercised runtime paths. Identity policy exposes who can act as whom. Version-control and issue history expose change coupling and ownership. Incidents, recovery exercises, and runbooks expose failure and human dependencies. No single layer is a complete observation.

**Reconcile declared and deployed state.** A repository may declare one topology while a controller, operator, manual override, or supplier implements another. Compare desired configuration, admitted configuration, current state, and observed traffic. Use stable identities across renames and deployments. Record collection time because autoscaling, failover, feature flags, and progressive delivery make observations temporal.

An unobserved runtime edge is not necessarily absent: the path may be rare, disabled, sampled out, or hidden by encryption. A static edge is not necessarily exercised. An infrastructure declaration is not proof of admission or enforcement. Conclusions inherit these observation limits.

**Detect structural erosion.** Structural signals include forbidden dependencies, cycles across intended layers, broad fan-out from a supposedly isolated element, duplicated adapters, shared mutable state, and dependency concentration. Trends matter: a stable, justified exception differs from growing cross-boundary access.

Normalize measures when system size changes and retain the graph behind them. Ten violations among twenty relations are different from ten among twenty thousand, but neither ratio measures severity. One forbidden dependency that bypasses payment authority may dominate a hundred harmless logging imports.

**Detect behavioral and temporal erosion.** An architecture can preserve its boxes and arrows while losing its guarantees. Retries may become non-idempotent, ordering assumptions may leak, timeouts may exceed callers' budgets, backpressure may disappear, or a formerly asynchronous path may become synchronous. Trace state transitions, queues, deadlines, and failure propagation rather than checking only relation existence.

Behavioral erosion often emerges only under concurrency, overload, partition, recovery, or adversarial input. Couple conformance rules with targeted experiments and operational evidence. A green dependency graph cannot establish bounded latency, correct recovery, or single authority.

**Detect data and authority erosion.** Shared tables, cross-domain queries, replication consumers, spreadsheets, support exports, caches, and analytics jobs can create undeclared data contracts. Identify which component is authoritative for each decision, who may write, how invariants cross boundaries, and how schema evolution reaches consumers.

Security boundaries erode when broad service identities, shared secrets, transitive trust, support impersonation, emergency roles, or permissive network paths accumulate. A permitted network edge does not authorize every operation on it. Examine identity, capability, policy decision, audit, and revocation relations.

**Detect operational erosion.** Deployment independence can disappear even when source modules remain separate. Shared release trains, coordinated flags, fragile startup ordering, global control planes, common capacity pools, or coupled rollback can impose lockstep. Recovery may depend on one expert, undocumented sequence, unavailable credentials, or a third party outside the stated recovery objective.

Measure actual deployment and recovery behavior. Change failure, queueing, and incident data may reveal consequences, but they require definitions and confounder analysis. A slower delivery trend can result from regulatory change, team turnover, or a larger product rather than architecture alone.

**Detect organizational erosion without reducing organization to a graph.** Ownership gaps, excessive cross-team coordination, review queues, conflicting incentives, and lost rationale can make violations more likely. Change-coupling and authorship data can identify investigation targets. They do not establish individual fault or dictate team reorganization.

Architecture is a socio-technical property. If the only compliant path requires a month of coordination, teams will create bypasses. Repair may require a self-service interface, clearer authority, staffing, or changed incentives as well as code movement. Avoid surveillance metrics and involve affected teams in interpretation.

**Use trends as prompts, not verdicts.** Possible indicators include divergence count and density, waiver age, cyclic-dependency mass, instability, change coupling, cross-boundary schema access, coordinated-deployment rate, recovery dependency count, and time to perform representative changes. Define numerator, denominator, extraction, scope, and expected direction.

Prefer control limits, baselines, and annotated time series over universal thresholds. A discontinuity after a tool change may be measurement drift. A rising metric may follow intentional decomposition before later convergence. Review representative underlying cases before attributing cause.

**Connect discrepancy to consequence.** For each candidate, ask which stakeholder concern and architectural rationale it threatens; how the mechanism operates; under what conditions it matters; how widely it propagates; whether it is reversible; and what evidence supports the link. Distinguish the observed fact, the inferred mechanism, the predicted consequence, and the accountable judgment.

A rule violation can be harmless because the rule is obsolete. A conforming structure can still fail because the model omitted a concern. Erosion is not proven by tooling alone. Evidence becomes stronger when static structure, runtime behavior, change history, incidents, and controlled experiments converge through different failure modes.

**Prioritize by risk and option loss.** Rank work using severity, likelihood or exposure, uncertainty, propagation potential, reversibility, rate of accumulation, regulatory or safety obligations, and cost of learning. Do not multiply arbitrary ordinal colors into a fake risk number. Record why a small structural discrepancy receives high priority or a large set receives low priority.

Irreversibility deserves special attention. A private code dependency may be removed locally; a published schema, copied data, customer contract, or embedded-device protocol may persist for years. Act early where continued adoption narrows options, even when current incident frequency is low.

**Choose a response deliberately.** Possible dispositions are:

- **confirm:** the observation is permitted and the model remains useful;
- **remap or reobserve:** the discrepancy came from incomplete or invalid evidence;
- **update intent:** the implemented change is preferable and its consequences are accepted;
- **waive temporarily:** keep a bounded exception while satisfying stated controls and expiry;
- **contain:** place an adapter, facade, policy boundary, or isolation mechanism around the divergence;
- **repair:** restore the intended relation, authority, contract, or behavior;
- **migrate:** move through intermediate states toward a different architecture;
- **retire:** remove an element or capability whose continued accommodation causes disproportionate erosion;
- **accept residual risk:** an authorized owner accepts a bounded consequence with review triggers.

Response is an architecture decision. Preserve rationale, alternatives, evidence, owner, deadline, affected rules, and validation. A mass refactor without a validated target can exchange known drift for unknown breakage.

**Govern exceptions as first-class architecture.** A waiver names the exact rule, affected elements, business reason, risk, compensating controls, owner, creation and expiry dates, removal condition, and monitoring. It must be queryable beside violations. Renewal requires new evidence and authority, not automatic date extension.

Emergency work may justify a faster decision, not invisible structure. Capture the exception during response, test its safety boundary, and review it after stabilization. If repeated emergencies require the same bypass, investigate whether the prescribed path is inadequate.

**Make rules maintainable.** A rule needs a stable identifier, rationale, concern, scope, owner, implementation, severity logic, examples, exceptions, and change policy. Test the detector on known conforming and violating fixtures. Monitor false positives, false negatives, execution cost, and mapping churn.

Keep the rule set small enough to understand. Layer local fast checks with slower cross-repository and runtime checks. Some principles remain reviewable claims rather than executable rules; pretending otherwise creates shallow proxies. SARCH-064 provides the deeper discipline for fitness functions.

**Recover architecture when intent is missing.** Architecture recovery extracts and organizes evidence; architecture discovery hypothesizes significant concepts and rationale; reconciliation compares and decides between models and reality. Start with a consequential question rather than attempting a complete reverse-engineered picture.

Interview maintainers and operators, inspect decision and incident history, cluster static and dynamic facts, and test hypotheses against representative changes. Label inferred boundaries and confidence. Recovery is interpretation supported by tools, not a mechanical revelation of the one true architecture.

**Prevent recurrence through path design.** Documentation and review help, but the easiest safe path should embody important constraints. Stable interfaces, scoped identities, ownership metadata, contract tests, isolated data stores, dependency rules, deployment automation, and self-service platform capabilities can make compliance cheaper than bypass.

Prevention must preserve learning. Rules that block all novel relations can suppress necessary evolution. Provide a visible exception path, rapid feedback, accountable review, and a route for changing obsolete intent. The goal is governed adaptability.

**Verify repair at several layers.** Removing a source dependency does not prove removal of the runtime call, data copy, identity grant, operational procedure, or organizational coordination it represented. Define closure evidence before repair. Re-run extraction, tests, runtime observation, and representative change or recovery exercises as appropriate.

Watch for displacement: an indirect dependency through a shared library may satisfy a direct-edge rule while retaining the same coupling. Verify the stakeholder concern and mechanism, not merely the metric. Continue monitoring long enough to see relevant operating conditions.

**Preserve history without preserving dysfunction.** Store architecture model versions, mapping changes, rule revisions, waiver decisions, observations, and repair evidence with stable identifiers. History explains why a divergence appeared and prevents repeatedly rediscovering context. It also supports learning about which controls work.

Do not turn the ledger into a shame register. Architectural decisions reflect constraints at their time. Review them prospectively: what is true now, what consequences matter, what options remain, and what action provides the best evidence-adjusted outcome?

## Definitions and Notation

Let:

- $H$ be the set of high-level architectural elements in the chosen viewpoint;
- $L$ be lower-level implementation or operational elements;
- $\mu:L\rightharpoonup 2^H$ be a partial, possibly multi-valued mapping;
- $P\subseteq H\times H$ be permitted directed relations;
- $R\subseteq P$ be required relations;
- $F_L\subseteq L\times L$ be extracted lower-level facts;
- $O\subseteq H\times H$ be observed relations derived from $F_L$ and $\mu$;
- $C=O\cap P$ be convergences;
- $D=O\setminus P$ be divergences;
- $A=R\setminus O$ be absences;
- $U$ be unmapped or ambiguous facts excluded from a definite classification;
- $W$ be active waivers, each bound to a rule, scope, owner, risk, and expiry;
- $t_i$ be an observation time and $M_i=(H_i,P_i,R_i,\mu_i,O_i)$ the versioned comparison at that time.

The partial arrow in $\mu$ means some lower-level elements may be unmapped. Multi-valued mapping permits a lower-level element to participate in more than one high-level concern, but the aggregation rule must then be explicit. These sets are analytical models, not the architecture itself.

## Mechanisms, Invariants, or Proof Structure

**Classification derivation.** For any observed relation $e\in O$, either $e\in P$ or $e\notin P$. Therefore $O=(O\cap P)\cup(O\setminus P)=C\cup D$, and $C\cap D=\varnothing$. Required relations are permitted by assumption, $R\subseteq P$. An element of $R$ not in $O$ belongs to $A$. Consequently the simple conformance predicate is

$$
\operatorname{conforms}(M)\iff D=\varnothing\land A=\varnothing.
$$

This is a theorem about the declared sets only. It does not prove the system satisfies a quality attribute, that extraction is complete, that mappings are valid, or that the intended model is desirable.

**Executable classification.** The following toy computation makes set semantics reproducible.

<!-- bijux-verify: {"id":"classify-reflexion-relations","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"convergences=orders->catalog,orders->payments,web->orders\ndivergences=web->payments\nabsences=none\nconforms=false\n","stderr":""}} -->
```python
permitted = {
    ("web", "orders"),
    ("orders", "payments"),
    ("orders", "catalog"),
}
required = {("web", "orders"), ("orders", "payments")}
observed = {
    ("web", "orders"),
    ("orders", "payments"),
    ("orders", "catalog"),
    ("web", "payments"),
}

def render(relations):
    return ",".join(f"{source}->{target}" for source, target in sorted(relations)) or "none"

convergences = observed & permitted
divergences = observed - permitted
absences = required - observed
print(f"convergences={render(convergences)}")
print(f"divergences={render(divergences)}")
print(f"absences={render(absences)}")
print(f"conforms={str(not divergences and not absences).lower()}")
```

Execution verifies this finite example under the recorded interpreter. It does not validate the sets, mapping, intent, or architecture of a real system.

**Counterexample to count-based severity.** Suppose model $M_1$ has 100 forbidden logging imports with no authority or failure effect, while $M_2$ has one forbidden administrative write to the payment ledger. Since $|D_1|=100>|D_2|=1$, any rule that equates divergence count with severity ranks $M_1$ higher. Yet under a loss or integrity concern, $M_2$ can be decisively worse. Therefore raw divergence count cannot generally order architectural risk.

**Freshness invariant.** A conformance conclusion is valid only for the compared revisions, rule set, mapping, extraction method, environment, and observation interval. When any material member changes, the old result becomes historical evidence rather than a current guarantee.

**Waiver invariant.** An active waiver can alter enforcement disposition but does not remove the underlying relation from $D$. Keeping waived divergence visible preserves trend, aggregate exposure, and expiry checks. Deleting it from observation would confuse authorization with conformance.

**Causal review.** If divergence $d$ and delivery delay rise together, the observation supports association. Claiming $d$ caused delay requires a mechanism and consideration of alternatives such as workload, staffing, policy, measurement, and product-scope changes. Before costly repair, seek a natural comparison, controlled change, incident trace, or other discriminating evidence.

## Alternatives and Trade-Offs

**Static enforcement versus runtime observation.** Static checks are fast, reproducible, and useful before merge, but miss dynamic dispatch, configuration, deployed topology, and actual behavior. Runtime evidence captures exercised paths and conditions but suffers sampling, coverage, instrumentation, and temporal limits. Use both when the concern crosses both layers.

**Allowlist versus denylist.** An allowlist makes permitted structure explicit and detects novel relations, but requires model maintenance and can obstruct exploration. A denylist is easier to introduce but recognizes only known hazards. Use allowlists for stable critical boundaries and narrower denylists or review triggers where legitimate variation is high.

**Central rules versus federated ownership.** Central governance can make cross-system constraints coherent and visible. It can also become slow and context-poor. Federated teams respond quickly and own local mechanisms, but may optimize away system-wide properties. Assign rules to the narrowest authority capable of owning their consequences, with common evidence formats and escalation.

**Prevent versus detect versus repair.** Typed interfaces, frameworks, isolation, and policy enforcement prevent selected structures but constrain design and require investment. Detection preserves flexibility but permits exposure between introduction and response. Repair handles known damage but becomes expensive after adoption spreads. A portfolio is usually stronger than one universal strategy, consistent with the erosion-control survey's conclusion that no single strategy suffices [3].

**Restore intent versus revise intent.** Restoration is appropriate when rationale and consequences remain valid. Revision is appropriate when evidence shows the new structure better serves current concerns. The decision must compare alternatives and update rules and descriptions atomically enough to avoid making the next comparison meaningless.

**Local refactor versus evolutionary migration.** A local refactor can remove a contained dependency quickly. Widely published contracts, shared data, and operational coupling require compatibility windows, parallel evidence, and staged migration. SARCH-073 through SARCH-080 develop these modernization mechanisms.

**Quantitative dashboard versus case review.** Trends enable coverage over large estates, while case review exposes rationale and consequence. Dashboards without cases invite gaming; cases without systematic detection miss scale. Use measures to sample and prioritize, then preserve inspectable evidence for decisions.

## Failure Modes and Misconceptions

1. **“Any difference is erosion.”** Difference first establishes drift; erosion requires a damaged architectural concern or evolutionary capacity.
2. **“The document is the architecture.”** A description is evidence and intent, not the operating entity itself.
3. **“The code is the truth.”** Code omits runtime configuration, data, people, suppliers, and rationale; it can also faithfully implement a harmful design.
4. **“Zero findings proves conformance.”** Detection may have incomplete rules, mapping, languages, paths, or observation windows.
5. **“More violations means more risk.”** Counts ignore severity, authority, propagation, exposure, and reversibility.
6. **“Permitted means required.”** Optional relations may be absent without nonconformance.
7. **“Not observed means absent.”** Rare paths, sampling, disabled features, and collection failures can hide relations.
8. **“A waiver makes a violation conforming.”** It authorizes bounded exposure; the divergence and risk remain visible.
9. **“A proxy metric is the architectural property.”** Cycle count, coupling, or deployment frequency may inform a claim but is not maintainability, safety, or autonomy itself.
10. **“Architecture tests remove the need for architects.”** Tests execute encoded judgments; humans still own concerns, rules, interpretation, and change.
11. **“The intended model is always right.”** It may be stale, incomplete, infeasible, or contradicted by better evidence.
12. **“Runtime traces are complete.”** They cover observed traffic under instrumentation and sampling, not every possible path.
13. **“Refactoring the edge repairs the problem.”** Coupling may move behind a facade, shared database, event, identity, or deployment process.
14. **“Architecture recovery is automatic.”** Extraction supports hypotheses; naming boundaries and rationale requires interpretation.
15. **“One root cause explains erosion.”** Accumulation commonly involves incentives, missing capabilities, obsolete intent, weak feedback, and local trade-offs.
16. **“Debt must always be repaid.”** Some debt is rational to retain when expected repair cost exceeds bounded consequence and option loss.
17. **“Teams caused the violation.”** Organizational evidence must be interpreted without individual blame or surveillance shortcuts.
18. **“A rebuild resets architecture.”** Without changed constraints and feedback, a replacement can reproduce the same erosion.

## Worked Examples

### Example 1

**Situation.** A reflexion model declares $P=\{(W,O),(O,P),(O,C)\}$, $R=\{(W,O),(O,P)\}$, and observes $O_b=\{(W,O),(O,P),(W,P)\}$.

**Reasoning.** The convergences are $C=O_b\cap P=\{(W,O),(O,P)\}$. The divergence is $D=O_b\setminus P=\{(W,P)\}$. Every required relation is observed, so $A=R\setminus O_b=\varnothing$. The model therefore fails its conformance predicate only because of the direct web-to-payment relation. Investigation must still determine whether the relation is real, whether the rule applies, and what consequence follows.

**Conclusion.** Set classification identifies a discrepancy precisely; it does not by itself establish erosion or prescribe repair.

### Example 2

**Situation.** A dependency scanner reports that a generated payment client in the web package imports a payment schema, apparently creating `web -> payments`.

**Reasoning.** The generated type contains only a value definition used by an orders client; no payment endpoint is reachable. Mapping the schema package entirely to the payment runtime component conflates type provenance with runtime authority. The team splits the mapping into contract ownership and runtime invocation viewpoints. The contract relation remains visible, while the supposed direct call disappears. A separate contract rule checks whether web should depend on a payment-owned type.

**Conclusion.** Repairing a mapping error is not hiding a violation when the revised viewpoints preserve the actual dependency and concern.

### Example 3

**Situation.** Source and build graphs contain no direct inventory-to-pricing call, but production traces show one during flash-sale fallback.

**Reasoning.** The call is selected by a remote feature flag and made through a generic HTTP client, so static name resolution misses it. Traces cover only 10% of requests, and the fallback occurs rarely. The team combines service-discovery configuration, flag history, and targeted exercise evidence to confirm the edge. It adds an explicit contract and runtime detector rather than declaring static analysis defective for a relation outside its evidence model.

**Conclusion.** Cross-layer observation can expose real architectural relations that one artifact cannot represent.

### Example 4

**Situation.** The intended model permits but does not require `reports -> archive`. No archive call appears during a seven-day observation.

**Reasoning.** Since the relation is in $P$ but not $R$, its absence is not in $A=R\setminus O$. Furthermore, the monthly retention job was outside the observation window. Reporting an architectural absence would make two errors: confusing permission with obligation and treating a limited trace as complete.

**Conclusion.** Optionality and observation coverage must be explicit to avoid false nonconformance.

### Example 5

**Situation.** During an incident, operations grants the support console direct write access to order state, bypassing the command service.

**Reasoning.** Immediate restoration justifies an emergency path only within accountable authority. The waiver names the grant, affected tables, commands allowed, compensating audit, owner, expiry in 48 hours, and revocation evidence. Post-incident review finds that retrying a console action can violate order-state invariants. The grant is revoked, a constrained repair command is added to the service, and an identity-policy rule monitors reintroduction.

**Conclusion.** A visible expiring waiver preserves emergency capability while preventing an operational exception from silently becoming architecture.

### Example 6

**Situation.** Across six months, services A, B, and C acquire relations $A\to B$, $B\to C$, and finally $C\to A$; releases increasingly require coordination.

**Reasoning.** The last edge creates a strongly connected component, but the graph alone does not prove deployment coupling. Change history shows 70% of changes touching C now require coordinated A deployment, and a rollback exercise fails because schema versions advance in lockstep. Interviews identify a shared temporal assumption. The repair introduces version-tolerant contracts and removes the rollback dependency before splitting code.

**Conclusion.** A cycle is a useful signal; combined behavioral and delivery evidence identifies the mechanism that matters.

### Example 7

**Situation.** Analytics begins reading an operational customer table directly, although the intended architecture requires published events.

**Reasoning.** The direct query reduces initial latency but makes column semantics, deletion behavior, and access privileges implicit contracts. A schema change breaks reports, while replicated sensitive fields outlive a deletion workflow. The concern is not merely a forbidden SQL edge: data authority, privacy lifecycle, and schema evolution have eroded. The team creates a governed analytical projection, backfills it with reconciliation, removes the grant, and verifies deletion propagation.

**Conclusion.** Data and authority evidence can reveal erosion invisible in application-source dependencies.

### Example 8

**Situation.** Implementation introduces a regional queue per tenant even though the intended diagram shows one global queue.

**Reasoning.** The change appears divergent. Evidence shows it contains noisy-neighbor overload, preserves per-tenant ordering required by the domain, and improves regional recovery. The original global queue was a provisional decision whose rationale assumed uniform workloads. Review accepts the new design, updates the architecture description and capacity model, and adds constraints against cross-tenant queue sharing.

**Conclusion.** When observed architecture better satisfies current concerns, correcting intent is the sound repair.

### Example 9

**Situation.** A dashboard reports that forbidden dependencies rose from 20 to 35 after a repository reorganization.

**Reasoning.** The extraction version changed, files doubled, and package naming rules were revised. Recomputing both revisions with the same extractor yields 18 and 19 comparable divergences. Of those, one new edge crosses an identity boundary and deserves investigation; the remaining dashboard increase is measurement drift. The team versions mappings and annotates the time series at tool changes.

**Conclusion.** Trend interpretation requires stable definitions, denominators, and extraction methods.

### Example 10

**Situation.** A portfolio has 180 low-consequence UI import violations, three shared-ledger writers, an undocumented recovery dependency, and a stale model for a service scheduled for retirement.

**Reasoning.** Count-based ranking would start with UI imports. Consequence analysis instead prioritizes shared-ledger authority because inconsistent writes are difficult to reverse, then tests recovery because outage propagation is uncertain. The retiring service receives a bounded waiver and access freeze rather than costly structural restoration. UI violations are grouped into a tool-supported migration after a new interface is available.

**Conclusion.** Effective remediation orders work by consequence, option loss, uncertainty, and system horizon—not visual noise.

## Cross-Program Connections

- [SEPAT](../../11-software-engineering-patterns/ROADMAP.md) supplies dependency-inversion, facade, adapter, and anti-corruption structures used to contain erosion without assuming a pattern alone resolves governance.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) connects deployment, telemetry, incident, recovery, and change evidence to observed operational architecture.
- [CONPAR](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) explains temporal behavior, shared state, ordering, and races that can erode guarantees while static structure remains unchanged.
- [DBE](../../18-database-engineering/ROADMAP.md) supplies schema, transaction, replication, and authority mechanisms needed to analyze data-boundary erosion.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) extends ownership, lineage, contracts, and governance across analytical and operational data estates.
- [SYSENG](../../26-systems-engineering/ROADMAP.md) connects configuration, baselines, interfaces, verification, lifecycle, and socio-technical change beyond software source.
- [API](../../28-api-and-service-engineering/ROADMAP.md) develops contract compatibility and service-boundary evidence used during architecture evolution.
- [PLAT](../../29-platform-engineering/ROADMAP.md) shows how self-service paths and guardrails can make important constraints economical to follow.

## References

1. ISO/IEC/IEEE. *ISO/IEC/IEEE 42010:2022, Software, Systems and Enterprise—Architecture Description*. 2nd ed., November 2022. Official record checked 2026-09-06. https://www.iso.org/standard/74393.html
2. Dewayne E. Perry and Alexander L. Wolf. “Foundations for the Study of Software Architecture.” *ACM SIGSOFT Software Engineering Notes* 17, no. 4 (1992): 40–52. https://doi.org/10.1145/141874.141884
3. Lakshitha de Silva and Dharini Balasubramaniam. “Controlling Software Architecture Erosion: A Survey.” *Journal of Systems and Software* 85, no. 1 (2012): 132–151. https://doi.org/10.1016/j.jss.2011.07.036
4. Gail C. Murphy, David Notkin, and Kevin J. Sullivan. “Software Reflexion Models: Bridging the Gap between Design and Implementation.” *IEEE Transactions on Software Engineering* 27, no. 4 (2001): 364–380. https://doi.org/10.1109/32.917525
5. David L. Parnas. “Software Aging.” In *Proceedings of the 16th International Conference on Software Engineering*, 279–287, 1994. https://doi.org/10.1109/ICSE.1994.296790
6. Stephen G. Eick, Todd L. Graves, Alan F. Karr, J. S. Marron, and Audris Mockus. “Does Code Decay? Assessing the Evidence from Change Management Data.” *IEEE Transactions on Software Engineering* 27, no. 1 (2001): 1–12. https://doi.org/10.1109/32.895984
7. John Rosik, Andrew Le Gear, Jim Buckley, Muhammad Ali Babar, and Dave Connolly. “Assessing Architectural Drift in Commercial Software Development: A Case Study.” *Software: Practice and Experience* 41, no. 1 (2011): 63–86. https://doi.org/10.1002/spe.999
8. Paul Clements, Felix Bachmann, Len Bass, David Garlan, James Ivers, Reed Little, Paulo Merson, Robert Nord, and Judith Stafford. *Documenting Software Architectures: Views and Beyond*. 2nd ed. Addison-Wesley, 2010.
9. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.
10. Robert C. Martin. *Clean Architecture: A Craftsman’s Guide to Software Structure and Design*. Pearson, 2017.

## Exercises

### Exercise 1

Define architectural drift, erosion, violation, conformance, and architecture debt. Explain why using them as synonyms produces a bad remediation decision.

### Exercise 2

Let $P=\{(A,B),(B,C),(A,D),(D,C)\}$, $R=\{(A,B),(B,C)\}$, and $O=\{(A,B),(A,C),(D,C)\}$. Compute $C$, $D$, and $A$, then state the bounded conformance result.

### Exercise 3

A team sees dependency violations rise from 12 to 40 while the codebase triples and the analyzer begins inspecting generated clients. Delivery lead time also rises. Diagnose what can and cannot be inferred, and specify the next evidence you would collect.

### Exercise 4

Design a multi-layer drift-detection system for an order platform. Include source, contracts, data, deployment, runtime, identity, waivers, ownership, and closure evidence. Explain which checks block changes and which only trigger review.

### Exercise 5

A regional rail signaling estate contains thirty-year-old control software, modern supervisory services, supplier devices, manual fallback, and strict safety responsibilities. A recovered model differs substantially from old documentation. Propose a safe drift-and-erosion assessment and remediation policy without claiming that software architecture review certifies railway safety.

## Answers to the Exercises

### Answer 1

Architectural drift is a discrepancy between applicable intent and observed reality; it is a prompt for investigation. Erosion is evidenced deterioration of important architectural properties or evolutionary capacity. A violation is an observation forbidden by a named applicable constraint. Conformance is a bounded relation between named models and evidence under a mapping and rule set. Architecture debt is a present compromise that creates expected future cost, constraint, or risk.

Treating them as synonyms converts detection directly into condemnation. A mapping error, obsolete model, or beneficial innovation could be “repaired” back into a worse design. Conversely, calling a dangerous authority bypass mere drift can understate harm. A sound sequence is classify discrepancy, validate evidence, connect it to concern and mechanism, judge consequence, then select a response.

### Answer 2

The convergences are

$$
C=O\cap P=\{(A,B),(D,C)\}.
$$

The divergence is

$$
D=O\setminus P=\{(A,C)\}.
$$

The required absence is

$$
A=R\setminus O=\{(B,C)\}.
$$

Under the declared set model, conformance fails because both $D$ and $A$ are nonempty. The unobserved permitted relation $(A,D)$ is optional and therefore is not an absence. The result does not prove real-system erosion until scope, mapping, observation coverage, intent validity, and consequences are reviewed.

### Answer 3

The raw increase does not establish worsening architecture. The denominator changed, analyzer coverage expanded, and generated clients may map differently. Lead time is associated temporally but may be affected by product scope, staffing, review policy, incidents, or measurement changes.

Re-run both revisions with one extractor and mapping; separate generated from handwritten facts; normalize by relevant relations while retaining absolute critical cases; inspect a stratified sample; and version rule changes. Then trace whether new edges cross authority or failure boundaries. Define lead time consistently, segment work types and teams, inspect change coupling and coordination, and seek incident or controlled-change evidence for mechanisms. A model answer must preserve uncertainty and cannot infer causation from the two trends alone.

### Answer 4

The system maintains versioned high-level elements, rules, mappings, waivers, and owners. Fast merge checks enforce stable critical source rules such as forbidden domain-to-adapter imports and secret scanning. Contract checks validate compatibility and producer ownership. Database grants and lineage detect cross-domain reads and writes. Infrastructure and admission-state comparisons detect topology and network-policy drift. Runtime traces and service discovery detect dynamic edges; identity-policy analysis detects excessive capabilities. Deployment records expose coordinated releases.

Critical authority, destructive compatibility, or nondelegable security constraints block when detection and mapping are sufficiently reliable. Noisy runtime novelty, coupling trends, uncertain mappings, and socio-technical indicators trigger review. Every finding retains lower-level evidence, scope, owner, severity rationale, waiver status, and expiry. Closure requires re-extraction plus concern-specific evidence—for example grant revocation, runtime absence over a representative interval, invariant tests, and recovery exercise. Acceptable alternatives may use different tools, but evaluation requires multi-layer coverage, uncertainty handling, explicit enforcement authority, and evidence-based closure.

### Answer 5

First establish accountable railway engineering, safety, cybersecurity, operations, supplier, maintenance, accessibility, and regulatory authorities; software reviewers cannot assume their powers. Baseline exact software, device, configuration, route, operating-mode, and documentation revisions. Preserve evidence and change controls. Build small viewpoints around safety responsibilities, command authority, timing, failure containment, degraded modes, manual fallback, supplier interfaces, and recovery.

Recover static dependencies, protocols, configurations, device inventories, identities, logs, maintenance procedures, incident history, and operator knowledge. Keep ambiguous mappings explicit. Compare prescriptive and observed relations without declaring old documentation correct. For each discrepancy, construct a hazard- and concern-linked argument through qualified domain processes; test only in authorized simulation, laboratory, shadow, or controlled environments. Do not inject failures into live signaling under an architecture exercise.

Prioritize unauthorized command paths, single points that defeat containment, undocumented fallback assumptions, obsolete supplier dependencies, and irreversible interfaces. Responses may update descriptions, add monitoring, constrain identities, isolate legacy components, introduce verified adapters, or migrate incrementally with compatibility and rollback evidence. Waivers require safety authority, scope, controls, expiry, and review. Independent assurance and legally required validation remain separate. A strong answer protects service and evidence, makes uncertainty visible, and explicitly avoids claiming railway safety certification.
