---
module_id: SARCH-086
program: Software Engineering: Software Architecture
level: 2
module_number: 86
title: Reference Architectures
status: complete
last_verified: 2026-09-06
---

# Reference Architectures

## One-Page Review

### Governing question

How can architects capture reusable architectural knowledge for a class of systems and specialize it into a target architecture without copying a diagram, laundering vendor choices into requirements, or claiming that reference conformance proves local fitness?

### Essential definitions

- a **reference model** describes important concepts and relationships in a domain at a deliberately abstract level;
- a **reference architecture** organizes reusable architectural concepts, roles, structures, responsibilities, constraints, decisions, and variability for a bounded class of entities;
- a **target architecture** expresses intended architectural decisions for a particular entity and context;
- a **reference implementation** realizes selected reference decisions in executable form and is evidence, not the definition of every valid realization;
- **specialization** resolves reference variability and local concerns into target decisions;
- an **instantiation** is a concrete architecture or system related to the reference architecture through a recorded mapping;
- a **viewpoint** establishes conventions for constructing and interpreting a view for named concerns;
- a **correspondence** states a consistency relationship among architecture description elements;
- a **conformance point** is a declared element, relation, constraint, or evidence obligation against which an instance can be assessed;
- **applicability** determines which reference content is relevant to a particular target context.

### Central model, mechanism, or theorem

Specify a governed reference architecture as

$$
R=(P,K,S,Q,V,D,M,E,A,L),
$$

where $P$ is purpose and audience, $K$ the referenced class and context, $S$ stakeholders and concerns, $Q$ concepts, roles, elements, and relations, $V$ viewpoints, views, and correspondences, $D$ decisions and constraints, $M$ variability and specialization rules, $E$ evaluation evidence, $A$ authority and adoption semantics, and $L$ lineage and lifecycle. Specialization maps each applicable reference item to adopt, adapt, omit, not-applicable, or unresolved with rationale and evidence.

### Critical invariants

- purpose, referenced class, audience, scope, assumptions, and non-goals are explicit;
- architecture, architecture description, reference architecture, and target architecture remain distinct;
- stakeholders, concerns, viewpoints, views, models, and correspondences are traceable;
- informative guidance and normative conformance points are distinguishable;
- variability names valid options, required resolutions, prohibited combinations, and extension rules;
- every target disposition preserves reference identity, version, rationale, owner, and evidence;
- non-applicability is argued; omission is not silently treated as compliance;
- vendor mappings and reference implementations are replaceable evidence unless legitimately normative;
- reference evaluation covers internal quality and usefulness across representative specializations;
- evolution addresses compatibility, migration, supersession, and retirement.

### Common failures

Common failures include calling a product diagram a reference architecture; omitting the referenced class; showing components without responsibilities; treating one view as complete; copying fashionable patterns; mixing abstract roles with concrete products; using “shall” without authority or conformance semantics; hiding variability in prose; accepting every local deviation without learning; rejecting legitimate non-fit; claiming implementation success validates the reference; measuring downloads as effectiveness; letting examples become de facto mandates; evolving diagrams without lineage; and leaving target systems bound to an obsolete version.

### Compact example

A cloud reference architecture names consumer, provider, broker, auditor, and carrier roles. A target system maps its business unit to consumer, two suppliers to provider and carrier responsibilities, an internal assurance function to selected auditor duties, and records that no broker participates. It adds local identity, recovery, locality, and exit decisions. The mapping supports communication and gap analysis; it does not make the 2011 reference a current security design or prove supplier fitness.

### Connections

[SARCH-085](085-golden-paths-and-paved-roads.md) operationalizes selected decisions as supported journeys. [SARCH-087](../ROADMAP.md) next examines the communities and forums that curate knowledge and review its use. [SARCH-030](030-creating-an-architecture-description-for-different-audiences.md) supplies architecture-description foundations.

## Governing Question

Organizations repeatedly solve related architecture problems. Without a reference, teams rediscover vocabulary, roles, boundaries, quality concerns, and failure modes. With a weak reference, teams instead inherit unexplained decisions, obsolete assumptions, and conformity theater. Reuse improves judgment only when the artifact exposes why it exists, which entities it describes, what varies, what is required, and how a concrete architecture relates to it.

A reference architecture is therefore neither a universal blueprint nor a gallery image. It is a governed architecture knowledge product for a class of entities. Its value is realized through interpretation and specialization, not copying.

## Why This Matters

ISO/IEC/IEEE 42010:2022 specifies requirements for architecture descriptions and explicitly distinguishes an entity's architecture from the work product expressing it [1]. That distinction matters twice for a reference architecture: the reusable architecture and its description are not identical, and neither is the target architecture derived for a particular system.

Terminology is not uniform. Cloutier and colleagues found inconsistent understandings of reference architecture and proposed capturing reusable why, what, and how knowledge for future developments [3]. Angelov, Grefen, and Greefhorst define a software reference architecture as a generic architecture for a class of systems and emphasize congruence among goals, context, and design [4], [5]. OASIS distinguishes an abstract reference model from a reference architecture that elaborates realization while remaining independent of a particular solution [6]. These sources support useful distinctions, but local definitions and authority must still be declared.

Reference architectures also influence procurement, policy, platforms, and system families. NIST's cloud reference architecture deliberately uses vendor-neutral actors and roles to enable communication and comparison rather than prescribing one implementation [7]. ISO/IEC 22123-3:2023 is the current published international cloud reference architecture and supersedes ISO/IEC 17789:2014 [8]. A current architecture team must therefore check publication status and scope rather than citing an old artifact because its diagram remains familiar.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, architecture, architecture description, architecture decision, view, viewpoint, model kind, correspondence, architecture framework, style, pattern, tactic, reference model, target architecture, system family, product line, variability, constraint, conformance, compliance, evidence, profile, extension, version, and provenance.

SARCH-021 through SARCH-030 supply views and communication. SARCH-061 through SARCH-070 supply evaluation. SARCH-083 and SARCH-084 supply governance and normative instruments. SARCH-085 supplies paths and implementations. This module focuses on reusable architectural knowledge and specialization; it does not prescribe a particular enterprise framework, industry standard, vendor stack, or product-line engineering method.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish reference architectures from adjacent architecture artifacts;
2. define the purpose, referenced class, context, stakeholders, concerns, and non-goals;
3. choose viewpoints and correspondence rules appropriate to the purpose;
4. express roles, responsibilities, structures, constraints, and quality consequences;
5. model variability, options, profiles, extension points, and rejection criteria;
6. declare normative and informative content with legitimate authority;
7. specialize reference content into a target architecture with traceable dispositions;
8. evaluate internal coherence and external usefulness without overclaiming;
9. govern contributions, versions, mappings, migration, and retirement; and
10. diagnose reference architecture misuse in procurement, platforms, and reviews.

## Core Exposition

**State purpose before content.** A reference may standardize vocabulary, frame procurement, enable interoperability, guide a product family, expose responsibility boundaries, support assurance, or accelerate target design. Those goals lead to different detail, authority, variability, and evaluation. “Create consistency” is too vague; state which decisions and outcomes should become more consistent, for whom, and under which conditions.

**Define the referenced class.** Name domain, entity kind, lifecycle, organizational boundary, scale, technology horizon, and excluded cases. A reference for public cloud ecosystems, medical-device software, and an organization's internal web services cannot share validity merely because each contains identity and telemetry. The class predicate is a premise for every reuse claim.

**Identify stakeholders and concerns.** Include people who own or experience consequences: users, operators, developers, product owners, security, privacy, accessibility, safety, data, finance, procurement, suppliers, regulators, and adjacent systems where applicable. Prioritize concerns by purpose. A procurement reference and a runtime resilience reference may describe the same domain through different concerns.

**Build a coherent concept and responsibility model.** Define terms, roles, responsibilities, information, interactions, and ownership. Roles should survive supplier changes. Distinguish a role from an organization, component, product, deployment unit, and person. A box labeled “platform” says little until capabilities, contracts, state, authority, and failure responsibilities are explicit.

**Choose purposeful viewpoints.** Use context, functional, information, interaction, deployment, operational, security, privacy, development, evolution, and cost viewpoints only when they frame named concerns. Define model kinds and interpretation. Use correspondence rules to detect contradictions: a logical shared service may map to one physical failure domain; an information-flow view may contradict a declared locality boundary.

**Separate universal structure from variability.** Identify required roles and relations, optional capabilities, alternative patterns, parameters, profiles, prohibited combinations, and extension contracts. Explain forces behind choices. If every item is optional, the reference provides no stable meaning. If nothing varies, it is likely a target design disguised as a reference.

**Declare prescription deliberately.** A reference can be informative, recommended, or normative for a defined adoption context. Authority comes from governance, contract, regulation, or an adopted standard—not the label *reference*. If conformance is claimed, define applicability, conformance points, evidence, versions, profiles, exceptions, and consequences. Do not use “compliant with the diagram.”

**Design for specialization.** Start a target effort by confirming class fit and local concerns. Baseline the reference version. For each applicable item, record adopt, adapt, omit, not-applicable, or unresolved; connect the disposition to target views and decisions; and explain consequences. Add local concerns absent from the reference. Specialization is design work, not parameter substitution.

**Keep abstract and concrete layers related.** Reference roles can map to several target components, and one target component can fulfill several roles. Preserve the mapping. A provider-specific example can clarify realization, but name its assumptions and show which reference semantics it implements. Multiple contrasting examples make accidental product mandates easier to detect.

**Evaluate internal quality.** Review traceability, terminology, viewpoint coverage, correspondence consistency, decision rationale, variability completeness, conformance testability, accessibility, and version integrity. Apply scenarios to the reference itself: can it represent multi-region failure, offline operation, supplier exit, data deletion, or ownership change within its promised class?

**Evaluate external usefulness.** Observe representative specializations. Measure decision clarity, unresolved concerns, design time, defects, interoperability, migration, lifecycle burden, and user comprehension. Compare with a baseline cautiously. The July 2026 systematic mapping study reports diverse evaluation approaches and emphasizes artifacts, instantiation procedures, and empirical studies [9]; this is evidence that evaluation is active and varied, not a universal method or causal guarantee.

**Treat reference implementations as experiments.** An implementation can test feasibility, expose missing interfaces, produce interoperability fixtures, and calibrate performance. It covers one technology, configuration, and environment. A successful implementation cannot prove the reference complete; a failure may challenge an assumption or merely reflect that implementation.

**Govern knowledge and authority.** Assign product ownership, editorial authority, domain contributors, affected stakeholders, assurance roles, funding, release criteria, and appeal. Publish change history and unresolved issues. Provide a route for target teams to contribute discovered gaps and variants. Avoid a central group that can publish mandates without operating feedback.

**Evolve with lineage.** Version semantics, viewpoints, conformance points, profiles, examples, and mappings. Classify changes by compatibility. Supply migration guidance for target architectures and reference implementations. Deprecate obsolete items before removal; archive evidence and explain supersession. A reference without lifecycle ownership becomes historical illustration.

## Definitions and Notation

Let $R=(P,K,S,Q,V,D,M,E,A,L)$. Purpose $P$ names decisions, outcomes, and audiences. $K$ is the predicate describing the referenced class and context. $S$ contains stakeholders and concerns. $Q$ contains concepts, roles, responsibilities, elements, and relations. $V$ contains viewpoints, views, model kinds, and correspondences. $D$ contains architectural decisions, principles, constraints, and rationale. $M$ describes variability and specialization. $E$ contains evaluation claims, methods, evidence, and limitations. $A$ declares authority, adoption, conformance, exceptions, and ownership. $L$ records versions, lineage, compatibility, migration, and retirement.

For a reference item $r$ and target architecture $t$, define a disposition

$$
d_t(r)\in\{\text{adopt},\text{adapt},\text{omit},\text{not-applicable},\text{unresolved}\}.
$$

Each applicable disposition has a rationale, owner, target trace, and evidence expectation. `Omit` means the item applies but is deliberately absent; `not-applicable` means the class or scope premise is false. They are not synonyms.

A **style** constrains families of elements and relations broadly. A **pattern** addresses a recurring problem under forces. A **reference architecture** composes architectural knowledge for a class. A **framework** supplies conventions and practices for architecture descriptions. A **template** shapes an artifact. A **golden path** operationalizes a journey. A **target architecture** makes contextual decisions. One artifact can use another without acquiring its identity.

## Mechanisms, Invariants, or Proof Structure

### Purpose and class invariant

Every reference claim traces to purpose $P$ and referenced class $K$. If a target does not satisfy $K$, the reference may still inspire questions, but conformance or fitness cannot be inferred from its content.

### Concern-view-decision invariant

Every material decision or constraint traces backward to at least one stakeholder concern and forward to affected viewpoints, variability, evaluation, and target dispositions. Decorative boxes with no concern or consequence are not architectural knowledge.

### Disposition-completeness invariant

Every applicable reference conformance point has exactly one current target disposition. `Unresolved` remains visible and cannot count as conformance. A disposition table can be structurally complete while its rationales or evidence are false, so the invariant is necessary but insufficient.

### Version-lineage invariant

Every target mapping identifies the reference identity and version. A reference update never silently changes a target architecture's declared conformance or decisions; migration is a new governed transition.

### Executable specialization audit

<!-- bijux-verify: {"id":"reference-specialization-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"complete target: pass\nmissing role: missing: auditor\nunresolved variant: unresolved: event-delivery\ninvalid disposition: invalid: carrier=ignored\n","stderr":""}} -->
```python
VALID = {"adopt", "adapt", "omit", "not-applicable", "unresolved"}

def audit(required, dispositions):
    missing = sorted(required - dispositions.keys())
    if missing:
        return "missing: " + ", ".join(missing)
    invalid = sorted(f"{key}={value}" for key, value in dispositions.items()
                     if value not in VALID)
    if invalid:
        return "invalid: " + ", ".join(invalid)
    unresolved = sorted(key for key, value in dispositions.items()
                        if value == "unresolved")
    if unresolved:
        return "unresolved: " + ", ".join(unresolved)
    return "pass"

required = {"consumer", "provider", "auditor"}
cases = {
    "complete target": {"consumer": "adopt", "provider": "adapt", "auditor": "omit"},
    "missing role": {"consumer": "adopt", "provider": "adapt"},
    "unresolved variant": {"consumer": "adopt", "provider": "adapt",
                           "auditor": "omit", "event-delivery": "unresolved"},
    "invalid disposition": {"consumer": "adopt", "provider": "adapt",
                            "auditor": "omit", "carrier": "ignored"},
}
for name, dispositions in cases.items():
    print(f"{name}: {audit(required, dispositions)}")
```

The audit checks finite record structure only. It does not decide whether `omit` is justified, whether roles are correctly mapped, whether evidence is valid, or whether the target architecture is fit.

### Proposition: reference conformance cannot prove target fitness

Assume a target conforms to every declared reference conformance point, but the reference omits a local safety concern that is outside its stated purpose. The target can conform and still be unfit for that safety-critical context. This counterexample refutes the unconditional implication from reference conformance to target fitness. Fitness additionally requires local concerns, assumptions, mechanisms, and evidence.

### Proposition: one successful instance cannot prove reference completeness

A reference omits offline synchronization, but its first target is always connected. That target can succeed without exercising the missing concern. Therefore one successful instance is compatible with an incomplete reference for the wider class. Representative diversity and adversarial scenarios are required to challenge coverage.

## Alternatives and Trade-Offs

**Reference model versus reference architecture.** A reference model offers stable conceptual vocabulary with fewer implementation commitments. A reference architecture adds roles, structures, responsibilities, decisions, and realization guidance, gaining actionability at the cost of more assumptions and lifecycle burden.

**Informative versus normative.** Informative guidance encourages broad learning and adaptation. Normative content can improve interoperability and assurance but requires legitimate authority, testable conformance points, profiles, evidence, and change control. Mixing the two silently creates arbitrary review outcomes.

**Abstract versus concrete.** High abstraction travels across technologies but may not resolve target decisions. Concrete examples improve comprehension and feasibility testing but risk product lock-in and copied assumptions. Maintain explicit mapping between reference semantics and examples.

**One cross-domain reference versus several domain references.** A broad reference creates shared language but may flatten important differences. Narrow references improve fit but multiply discovery, correspondence, and governance. Layering can work when a small foundational model has explicit domain profiles and conflict rules.

**Central curation versus federation.** Central editors preserve coherence and versioning but may lack domain evidence. Federated ownership adds expertise but risks conflicting terminology and unmaintained sections. Use contribution contracts, named maintainers, correspondence checks, and release authority.

**Build versus adopt an external reference.** External standards and industry references can reduce reinvention and enable interoperability. They carry scope, age, authority, licensing, and context assumptions. Profile or map them instead of editing away those assumptions or presenting adoption as local validation.

## Failure Modes and Misconceptions

1. **A reference architecture is a target architecture.** The target requires contextual specialization and additional decisions.
2. **A diagram is sufficient.** Purpose, concepts, concerns, rationale, variability, evidence, and lifecycle carry meaning.
3. **Reference means authoritative.** Authority must be declared and legitimate.
4. **Normative language creates authority.** Typography cannot create governance, contract, or law.
5. **Conformance proves fitness.** It proves only scoped reference claims with valid evidence.
6. **A reference implementation defines the architecture.** It is one realization and experiment.
7. **Vendor-neutral means vendor-independent.** Hidden service semantics, costs, and operations can still create dependence.
8. **All targets should use every role.** Applicability and profiles may differ, but non-applicability requires rationale.
9. **Omit and not-applicable are equivalent.** Omit accepts applicability; not-applicable rejects it.
10. **More views mean completeness.** Views help only when tied to concerns and checked for correspondence.
11. **Variability means listing options.** Valid combinations, forces, consequences, and resolution rules are also needed.
12. **Every exception weakens the reference.** A justified non-fit can reveal scope or missing variability.
13. **Usage proves effectiveness.** Mandate, habit, and lack of alternatives can drive usage.
14. **One successful target validates the class.** It may leave important variants and failures untested.
15. **An old standard remains current because it is cited.** Publication and supersession status require checking.
16. **A product mapping is harmless illustration.** Examples can become de facto procurement mandates.
17. **Updates automatically improve targets.** Target migration can introduce incompatibility and risk.
18. **Reference retirement deletes history.** Lineage, decisions, and evidence may remain necessary.

## Worked Examples

### Example 1

**Disambiguate an overloaded artifact.** A document titled “Reference Architecture” contains a cloud-provider deployment diagram and a bill of materials. It has no purpose, referenced class, stakeholder concerns, variability, or alternative mapping. Classify it as a candidate solution example, then recover provider-independent roles, contracts, state, quality drivers, and assumptions before deciding whether a reference architecture is warranted. **Conclusion:** title and visual style do not determine artifact kind.

### Example 2

**Specialize cloud ecosystem roles.** A target maps the NIST consumer role to a business unit, provider responsibilities to two suppliers, carrier duties to a network provider, and selected auditor duties to internal assurance. No broker participates, so `broker=not-applicable` is justified by the procurement model. Local identity, recovery, locality, and exit concerns are added. **Conclusion:** specialization maps and extends reference roles; it does not copy actors as components.

### Example 3

**Find a cross-view contradiction.** A logical view depicts three independent processing cells, but the deployment view places all cells behind one regional identity service and one message namespace. The recovery concern therefore contradicts the claimed failure independence. Add a correspondence rule linking logical independence to physical and administrative dependencies, then revise either the claim or topology. **Conclusion:** several views create value only when their relationships are checked.

### Example 4

**Separate informative and normative content.** A payment reference recommends asynchronous integration for resilience but requires immutable transaction identity for its adopted conformance profile. A synchronous target can adapt the recommendation with latency and recovery rationale; it cannot silently omit the identity requirement. Conformance evidence names the profile and version. **Conclusion:** prescription must be explicit at item level.

### Example 5

**Model controlled variability.** A telemetry reference permits push or pull collection, centralized or federated storage, and two retention profiles. It prohibits a pull-only design for intermittently connected devices and requires redaction before cross-boundary export. The target records selected variants and forces rather than setting arbitrary booleans. **Conclusion:** useful variability includes valid combinations, exclusions, and consequences.

### Example 6

**Prevent a vendor example becoming a mandate.** A reference example maps durable object storage, event notification, identity, and lifecycle policy to one supplier. Procurement starts treating those products as required. Publish the abstract capability mapping, add a second contrasting realization, mark provider-specific operational assumptions, and keep any mandated product choice in a separate authorized standard. **Conclusion:** examples must preserve substitutability where the reference promises it.

### Example 7

**Reject a non-fit honestly.** An internal web-service reference assumes continuous connectivity, centralized identity, and remote operations. A safety-critical field controller is disconnected for weeks and must fail predictably without central services. Treating it as “mostly compliant” would hide violated premises. Use another domain reference while retaining useful vocabulary mappings. **Conclusion:** non-fit is not a failed target; it is a boundary of the reference claim.

### Example 8

**Migrate a reference version.** Version 3 separates identity issuance from authorization and changes the required audit correspondence. Version 2 targets do not become nonconforming automatically. Owners diff semantic and conformance changes, assess each target, record migration decisions, provide coexistence dates, and retire version 2 only after obligations and evidence are handled. **Conclusion:** reference evolution is a governed target transition, not a diagram replacement.

### Example 9

**Evaluate beyond one instance.** A data-processing reference works for a small batch target. Reviewers also specialize it for streaming, multi-jurisdiction, supplier-exit, corrupted-input, and regional-isolation scenarios. The exercises reveal missing time semantics and recovery ownership. The reference is revised before wider adoption. **Conclusion:** diverse and adversarial specializations challenge class coverage better than one showcase.

### Example 10

**Transfer the method to humanitarian communications.** A reference architecture for emergency messaging names affected communities, responders, network operators, translators, authorities, and aid organizations; covers offline delivery, authenticity, privacy, accessibility, misinformation correction, and power loss; and permits regional profiles. A concrete deployment adds local languages, lawful authority, device constraints, trust relationships, and harm review. **Conclusion:** reuse can organize difficult concerns, but local legitimacy and safety cannot be inherited from the reference.

## Cross-Program Connections

- [SARCH-030](030-creating-an-architecture-description-for-different-audiences.md) supplies purpose-specific architecture descriptions and audience translation.
- [SARCH-061](061-architecture-tradeoff-analysis-method.md) supplies structured stakeholder and quality-attribute evaluation.
- [SARCH-070](070-running-an-evidence-based-architecture-review.md) supplies claim, evidence, finding, and decision discipline.
- [SARCH-084](084-standards-principles-and-guardrails.md) distinguishes informative guidance, normative requirements, conformance, and fitness.
- [SARCH-085](085-golden-paths-and-paved-roads.md) can operationalize a selected reference specialization as supported capabilities and journeys.
- [DARCH-098](../../20-data-architecture-engineering/modules/098-architecture-standards-and-reference-patterns.md) owns data-specific standards, profiles, reference patterns, and governance.
- [CLOUD-001](../../30-cloud-and-infrastructure-engineering/modules/001-cloud-service-and-deployment-models.md) applies current cloud service, deployment, actor, and responsibility models.

## References

1. ISO/IEC/IEEE. *ISO/IEC/IEEE 42010:2022, Software, systems and enterprise — Architecture description*. Edition 2, November 2022. [Official ISO record](https://www.iso.org/standard/74393.html). Retrieved 2026-09-06.
2. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed., Addison-Wesley, 2021.
3. Robert Cloutier, Gerrit Muller, Dinesh Verma, Roshanak Nilchiani, Eirik Hole, and Mary Bone. “The Concept of Reference Architectures.” *Systems Engineering* 13(1), 2010, pp. 14–27. [DOI](https://doi.org/10.1002/sys.20129).
4. Samuil Angelov, Paul Grefen, and Danny Greefhorst. “A Classification of Software Reference Architectures: Analyzing Their Success and Effectiveness.” WICSA/ECSA 2009, pp. 141–150. [IEEE record](https://ieeexplore.ieee.org/document/5290800/).
5. Samuil Angelov, Paul Grefen, and Danny Greefhorst. “A Framework for Analysis and Design of Software Reference Architectures.” *Information and Software Technology* 54(4), 2012, pp. 417–431. [DOI](https://doi.org/10.1016/j.infsof.2011.11.009).
6. OASIS. *Reference Architecture Foundation for Service Oriented Architecture Version 1.0*. Committee Specification 01, 4 December 2012. [Official specification](https://docs.oasis-open.org/soa-rm/soa-ra/v1.0/cs01/soa-ra-v1.0-cs01.html). Retrieved 2026-09-06.
7. Fang Liu, Jin Tong, Jian Mao, Robert Bohn, John Messina, Lee Badger, and Dawn Leaf. *NIST Cloud Computing Reference Architecture*. NIST SP 500-292, September 2011. [Official NIST record](https://doi.org/10.6028/NIST.SP.500-292). Retrieved 2026-09-06.
8. ISO/IEC. *ISO/IEC 22123-3:2023, Information technology — Cloud computing — Part 3: Reference architecture*. Edition 1, September 2023. [Official ISO record](https://www.iso.org/standard/82759.html). Retrieved 2026-09-06.
9. Valdemar Vicente Graciano Neto et al. “How Are Software Reference Architectures Being Evaluated? A Systematic Mapping Study.” *Information and Software Technology* 195, July 2026, 108116. [DOI](https://doi.org/10.1016/j.infsof.2026.108116). Retrieved 2026-09-06.
10. Elisa Yumi Nakagawa, Flavio Oquendo, and José Carlos Maldonado. “Reference Architectures.” In *Software Architecture 1*, Wiley, 2014. [DOI](https://doi.org/10.1002/9781118930960.ch2).
11. Nick Rozanski and Eoin Woods. *Software Systems Architecture: Working With Stakeholders Using Viewpoints and Perspectives*. 2nd ed., Addison-Wesley, 2011.
12. Neal Ford, Rebecca Parsons, and Patrick Kua. *Building Evolutionary Architectures*. 2nd ed., O'Reilly Media, 2022.

## Exercises

### Exercise 1

Distinguish reference model, reference architecture, architecture framework, reference implementation, target architecture, pattern, and template. Give one valid relationship without treating them as synonyms.

### Exercise 2

A reference requires roles `producer`, `consumer`, and `assurance`; offers push or pull delivery; and marks offline operation optional. Trace specialization for a target that uses push delivery, combines producer and consumer in one organization, omits assurance, and must work offline. Classify each disposition and identify unresolved concerns.

### Exercise 3

A vendor reference diagram is used as a mandatory procurement checklist, yet two deployed systems that match it have incompatible identity and recovery behavior. Diagnose defects in purpose, abstraction, normative semantics, viewpoints, variability, and evidence.

### Exercise 4

Design the content and governance of a reference architecture for three related internal analytics workload classes. Include purpose, class boundaries, viewpoints, variability, conformance, examples, specialization records, evaluation, and lifecycle.

### Exercise 5

Create a reference-architecture outline for regional digital identity used across public services. Address stakeholders, rights, privacy, accessibility, offline operation, federation, revocation, recovery, evidence, legitimate authority, profiles, local specialization, and limits without claiming universal legal or social validity.

## Answers to the Exercises

### Answer 1

A reference model defines abstract domain concepts and relationships. A reference architecture adds reusable architectural roles, structures, responsibilities, decisions, variability, and realization guidance for a class. An architecture framework defines conventions and practices for descriptions. A reference implementation realizes selected decisions. A target architecture makes contextual decisions for one entity. A pattern addresses a recurring problem under forces. A template shapes an artifact. A reference architecture can use a reference model's vocabulary, be described through a framework, compose patterns, be tested by reference implementations, guide target architectures, and provide content for templates. These relationships do not erase distinctions.

### Answer 2

First confirm that the target fits the reference class. `producer=adapt` and `consumer=adapt` can be justified because one organization fulfills both roles, provided responsibilities and conflicts remain explicit. Push delivery is `adopt`. `assurance=omit` is not a conformance pass if the role is required; it is a visible violation or unresolved decision requiring authority and evidence. Offline operation is optional in the reference but mandatory locally, so the target adopts that variant and adds buffering, synchronization, identity, conflict, integrity, observability, and recovery decisions. The assurance gap and any absent offline semantics remain unresolved rather than being hidden by overall similarity.

### Answer 3

The artifact lacks a declared purpose beyond procurement and probably confuses a provider solution with a class-level architecture. Its product boxes hide role, contract, state, trust, and failure semantics. Calling the list mandatory does not establish legitimate authority, applicability, profiles, or conformance evidence. A single deployment view cannot expose identity issuance, authorization, recovery authority, information consistency, or operations. Variation across identity and recovery was neither constrained nor recorded. Visual matching therefore measures product presence rather than architectural behavior. Recover provider-independent concerns and roles, add relevant viewpoints and correspondence rules, declare variability and conformance points, separate the authorized product standard, and evaluate system claims directly.

### Answer 4

Define the purpose as improving repeated decisions and interoperability for, for example, scheduled batch, interactive analysis, and governed model training. State shared and excluded contexts. Include users, data owners, platform teams, operators, privacy, security, finance, and affected subjects. Use context, information, processing, security/privacy, deployment, operations, cost, and evolution viewpoints with correspondence rules. Share identity, ownership, data contracts, lineage, policy evidence, artifact provenance, and recovery concepts; define profiles for timing, isolation, compute, and retention. Declare which points are informative or normative and how evidence works. Supply at least two contrasting realizations. Require versioned disposition records for each target. Evaluate representative and adversarial specializations plus comprehension and lifecycle burden. Govern through named owners, domain contributors, release criteria, feedback, compatibility, migration, supersession, and retirement.

### Answer 5

Purpose and authority must be jurisdiction-specific: the reference organizes questions and possible profiles but cannot create lawful authority. Stakeholders include residents, children, people without standard documents or connectivity, disabled users, service agencies, identity operators, local authorities, privacy and security bodies, civil society, support, auditors, and relying parties. Viewpoints cover rights and redress, identity proofing, credentials, federation, consent or other lawful basis, attributes, authentication, revocation, recovery, offline use, accessibility, fraud, privacy, security, operations, interoperability, and lifecycle. Profiles may vary assurance, connectivity, credential form, federation, and recovery while protecting explicit hard constraints. Every local target records dispositions, authority, impact evidence, language and accessibility testing, threat and privacy analysis, exclusions, appeal, and alternatives. Reference conformance cannot prove inclusion, fairness, legality, security, or public value; independent local review and continuing outcome evidence remain necessary.
