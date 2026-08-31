---
module_id: SYSENG-056
program: Systems Engineering
level: 2
module_number: 56
title: SysML Concepts
status: complete
last_verified: 2026-08-31
---

# SysML Concepts

## One-Page Review

### Governing question

How can engineers use SysML 2.0 to express one semantically coherent system model across structure, behavior, requirements, analysis, verification and stakeholder views—without confusing a language construct, a diagram, a tool database or an automated check with engineering truth?

### Essential definitions

- **SysML 2.0** is the current OMG systems modeling language. It supplies abstract syntax, textual and graphical concrete notations, semantics and standard libraries for specifying systems and related engineering concerns.
- **KerML 1.0** is the foundational modeling language beneath SysML 2.0. Its element, relationship, type, feature, specialization, occurrence and behavior semantics support the systems-oriented vocabulary added by SysML.
- A **definition** classifies what instances may be or do and can declare reusable features. A **usage** identifies how something is used in a particular context and may be typed by a definition.
- A **namespace** gives members naming context. A **package** is a namespace used to organize model elements. Imports expose members but do not by themselves establish ownership, approval or configuration compatibility.
- **Specialization** constrains a more general classifier. **Subsetting** constrains the values of a feature to values of another feature. **Redefinition** specializes a feature in a more specific context. These relationships are not interchangeable aliases.
- An **item** is an occurrence that can participate in transfer. A **part** is an occurrence with composite, system-oriented semantics. A **port** represents an interaction point. Connections, interfaces and flows express interaction relationships with different purposes.
- An **action** models performance; a **state** models condition and state-dependent behavior; a **calculation** maps inputs to results; a **constraint** is a Boolean-valued condition. Execution or simulation requires additional semantics, engines and evidence.
- A **requirement** expresses a constraint on a subject with assumptions and required constraints. A **case** specifies a subject, objective and behavior for analysis, verification or use.
- A **viewpoint** states stakeholder concerns and rules for constructing/evaluating a view. A **view** exposes selected model content under a viewpoint. A rendered diagram or table is a presentation of model content, not a second source of truth.
- **Metadata** classifies and annotates model elements with governed information. Metadata does not repair weak semantics, missing provenance or unsupported claims.
- A **model identity** is the stable identity of an element independent of a displayed name or drawing location. A **model version** or API commit identifies a configured state. Identity, name, location and version must remain distinct.
- The **Systems Modeling API and Services 1.0** standard defines project, branch, commit, element, relationship, query and related services for model access and interoperability. An API endpoint does not guarantee complete semantic exchange or tool conformance.

### Central model, mechanism, or theorem

Treat a governed model as a versioned typed graph:

$$
M_c=(E,R,T,N,L,V,c),
$$

where $E$ is a set of identity-bearing elements, $R$ typed relationships, $T$ typing and specialization constraints, $N$ namespaces and memberships, $L$ imported standard/domain libraries, $V$ views/renderings and $c$ the selected commit/configuration. For every usage $u$ typed by definition $d$,

$$
instances(u)\subseteq instances(d).
$$

For a feature $f_s$ that subsets $f_g$,

$$
values(f_s)\subseteq values(f_g).
$$

These set interpretations explain why typing, specialization and subsetting constrain meaning rather than merely decorate boxes. A useful model must also satisfy project-specific invariants $I(M_c)$ and have evidence adequate to its intended decision. Syntactic validity is necessary, but it is not semantic consistency, physical feasibility, requirement satisfaction or empirical validity.

### Critical invariants

- State the exact language, library, transformation, API and tool versions; do not label beta or vendor-specific syntax as formal SysML 2.0.
- Every governed element has stable identity, qualified name where appropriate, owner/namespace, semantic kind, lifecycle status, provenance and configuration applicability.
- Definition and usage remain distinct; a reusable definition is not silently treated as a configured instance, and a usage is not assumed to define every instance.
- Specialization, feature typing, subsetting, redefinition, binding and dependency are used for their actual semantics, not as visually convenient arrows.
- Multiplicity, direction, conjugation, quantity kind/unit, occurrence/lifetime and composite/reference semantics are explicit where consequential.
- Connections bind compatible ends in a configured context; direction and conveyed item/flow semantics agree with the interface and behavior.
- Structure, behavior, requirement, calculation, verification and analysis elements refer to the same configured subjects and authoritative properties.
- Views are generated selections of model content under declared viewpoints; information is not manually forked into independent diagrams and tables.
- Imports are controlled by package/library identity and version; name visibility never implies semantic compatibility or authority.
- Derived and implied relationships are distinguishable from authored facts, reproducible by a declared conforming rule/tool version and never silently persisted as competing authority.
- API queries and exchanges identify project, branch/commit, schema and identifiers; partial responses, pagination, access control and unsupported constructs are observable.
- Migration preserves source baseline, transformation rules, warnings, unmapped/vendor-specific content, identifiers or trace mappings, and validation evidence; no one-to-one v1/v2 equivalence is presumed.
- Passing syntax, schema, model rules or a calculation is reported only at that evidence level. Stakeholder correctness, architecture quality and real-system performance require separate review and evidence.

### Common failures

Common failures include treating SysML as a method; equating a diagram with the model; drawing before defining questions and authorities; confusing definitions with usages; using inheritance, subsetting, redefinition and binding interchangeably; copying values across views; connecting ports because lines fit; omitting item types, directions, multiplicities or modes; mixing configured variants; making names carry identity; importing changing libraries without version control; hiding vendor stereotypes or scripts behind standard-looking notation; assuming a green requirement relation proves satisfaction; treating a verification case definition as executed evidence; turning every stakeholder concern into one unreadable diagram; exporting only pictures; claiming API availability means lossless interchange; applying a v1-to-v2 transformation without semantic reconciliation; and measuring model progress by element count rather than decision coverage and defect discovery.

### Compact example

A mission-power package defines `BatteryPack`, `Controller`, `PowerPort` and `DCLink`; uses one pack and one controller in a selected system configuration; places compatible supply/input ports on them; connects those ports with one typed link; and associates each of two requirements with a verification case. A local checker can establish unique declared names, resolved typing, ownership, endpoint compatibility and verification coverage. It cannot establish conformance to the full SysML 2.0 metamodel, that the chosen requirements are correct, that the connection is physically adequate, that a case ran, or that the system passed.

### Connections

SYSENG-051 establishes model authority, SYSENG-052–055 establish requirement, behavior, structure and parametric content, and SYSENG-057–060 address consistency, simulation, reviews and tooling. SysML provides a common semantic language across those concerns; it does not replace their methods, evidence or governance.

## Governing Question

Can a reviewer select one controlled model commit and trace a stakeholder concern through requirements, configured usages, behavior, interfaces, calculations, analysis and verification—while explaining exactly which claims follow from SysML semantics, which depend on project rules, and which still require physical or empirical evidence?

The wrong governing question is “Which diagram type should we draw?” In SysML 2.0, textual and graphical forms represent an underlying model. Presentation matters, but a diagram-first workflow can conceal ambiguous identity, incompatible configurations and missing relations behind familiar shapes.

## Why This Matters

Complex systems are described by many teams and specialist tools. Natural-language documents and drawings remain useful, but duplicated facts diverge: one interface table changes, a power calculation keeps an old value, a test case points to another variant, and a decision record cites an obsolete diagram. A well-governed SysML model can make shared identity and relationships queryable, allowing a change to be assessed across multiple concerns.

OMG formally adopted SysML 2.0, KerML 1.0 and Systems Modeling API and Services 1.0 in 2025; the formal documents were published with March 2026 editorial updates. SysML 2.0 is not merely a new set of v1 diagrams. It rests on KerML, consistently uses definitions and usages, includes textual and graphical notation, defines systems-oriented libraries and has a standard model-access API. The separate normative v1-to-v2 transformation specification also signals that migration is an engineering activity with transformation rules, not a filename conversion.

NASA-HDBK-1009A, active in 2025, demonstrates how SysML-based modeling can support systems-engineering work products and stresses model planning, organization, a project metamodel, model building, and generated diagrams/tables. Its companion model uses a v1-era tool, so it is useful process evidence but not a normative source for SysML 2.0 syntax. This distinction is representative: established organizations will operate mixed estates during migration.

ISO/IEC/IEEE 42010:2022 distinguishes an entity's architecture from an architecture description and does not prescribe an architecting method or tool. The same discipline applies here. SysML can express architecture descriptions and many other system specifications, but no language can guarantee that the modeled architecture is desirable or that the model addresses the right concerns.

## Prerequisites and Retrieval

Before selecting constructs or authoring model content, retrieve:

1. intended decisions, modeling questions, stakeholders, concerns, lifecycle uses, acceptance criteria and consequences of error;
2. system-of-interest boundary, contexts, variants, modes, environments, time horizons, configurations and authoritative baselines;
3. project modeling method, ontology/domain language, package architecture, naming/identity rules, viewpoints, model kinds and review criteria;
4. approved SysML/KerML formal version, standard/domain library versions, project extensions, tool build, API/schema and conformance claims;
5. requirements, interfaces, behaviors, properties, quantities, analyses, verification artifacts, hazards, risks, decisions and external data authorities;
6. access rules, classification/export controls, supplier/IP constraints, branch/merge process, element-level change history and release policy;
7. v1 source models, profiles/stereotypes, diagram conventions, opaque behaviors, scripts, validation rules, generated documents and downstream integrations when migrating;
8. verification and validation evidence for transformations, queries, generators, calculations, simulations and rendered work products.

Use a retrieval test: “The interface is in SysML.” Ask which project and commit, which end identities, which configured usages, which port definitions/usages, which interface/connection/flow, which conveyed item and direction, which multiplicity and mode, which physical/protocol specification, which requirement and verification evidence, and which consumer/tool can retrieve the same semantics. A screenshot cannot answer most of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. explain the roles and boundaries of SysML 2.0, KerML 1.0, standard libraries, notation, transformation and API/services;
2. distinguish model, presentation, method, tool repository, architecture and evidence;
3. use packages, namespaces, memberships, imports, names and stable identities without conflating visibility, ownership and authority;
4. distinguish definitions from usages and apply typing, specialization, subsetting and redefinition correctly;
5. relate parts, items, ports, connections, interfaces, flows and allocations in a configured structure;
6. relate actions, states, calculations and constraints without assuming automatic execution or simulation;
7. structure requirements, concerns, cases, analysis, verification, views, viewpoints and metadata with bounded claims;
8. define cross-model invariants and queries that detect incomplete or inconsistent semantics;
9. evaluate API/interchange and tool-conformance claims with identity, version, schema, round-trip and failure evidence;
10. plan a governed SysML v1-to-v2 migration that preserves source, traceability, exceptions and downstream behavior.

## Core Exposition

**Separate language from engineering method.** SysML defines constructs and their meaning. A project method decides what to model, in which order, to what fidelity, under whose authority and with which reviews. A tool implements some language/version plus repository, visualization, collaboration and automation behavior. An architecture is a property/conception of the system; an architecture description is a work product. Conformance at one layer does not imply quality at another.

**Anchor the version.** “SysML” is ambiguous across v1 releases, v2 beta releases, final 2.0, vendor subsets and extensions. Put the formal language version, KerML version, library release, API/schema and tool build in the model baseline. Record unsupported or deviating constructs. Examples from a pilot repository may be excellent learning assets but do not override the formal specification.

**Understand the language stack.** KerML provides foundational syntax and semantics: elements and relationships, namespaces, types and features, classification, specialization, occurrences, behavior and libraries. SysML specializes this foundation with systems-engineering concepts including items, parts, ports, connections, flows, actions, states, calculations, constraints, requirements, cases, views and metadata. This layered design makes semantic reuse possible, but a practitioner can model effectively without editing the metamodel. Metamodel changes and language extensions require specialist governance.

**Organize by durable authority.** Packages should reflect owned domains, products, interfaces, analyses, verification and libraries rather than diagram storage. Define public/private exposure and import policy. Use qualified names for human navigation, but use stable identifiers for integration. Renaming or moving an element should not create a new engineering thing; changing its meaning might require a new identity and explicit supersession.

**Control membership and imports.** Namespace membership relates an element to its naming context. Ownership and visibility have precise language semantics; project authority adds governance beyond them. Imports make members available by name. Explicit imports improve auditability; broad recursive imports are convenient but can create collisions and silent semantic drift when libraries change. Pin library versions and check ambiguous/resolved references.

**Model definitions and usages deliberately.** A definition describes a reusable kind—for example, `BatteryPack`. A usage describes a role or occurrence in context—for example, `emergencyPack : BatteryPack` inside `ClinicPowerSystem`. The usage may specialize inherited features and assign configured values. Do not create a separate definition for every named component when usages of one definition capture the variation; conversely, do not force materially different concepts under one vague definition.

**Use specialization as constraint.** A specialized definition denotes a subset of the general definition's instances and can add constraints/features. It should obey substitutability required by the domain. Specialization is not taxonomy decoration. If `SterilePump` specializes `Pump`, it cannot discard invariants required of all pumps without exposing a modeling contradiction or correcting the generalization.

**Distinguish feature relations.** Feature typing constrains feature values by a type. Subsetting says the values of one feature are among another's values. Redefinition is a specialization of an inherited feature in a more specific context and must remain compatible. Binding/equality connects values under its semantics. A dependency merely indicates reliance. Review these relations from the set/value interpretation, not arrow appearance.

**Represent occurrences and composition.** Parts and items concern things that occur in time and may have nested occurrences. Composite ownership, reference use, multiplicity and lifetime need domain meaning. “Four sensors” may mean four installed physical units, four slots, four logical channels or a type-level cardinality. State which. Reuse of one occurrence in two composites can be physically impossible even when a drawing looks plausible.

**Model interaction points before lines.** A port represents how a usage can interact. Port conjugation reverses relevant feature directions for the opposite side. A connection relates ends; an interface can define a reusable interaction pattern; flows represent transfers of items across features. Check end ownership, multiplicity, direction, item kind, quantity/unit, protocol, timing, mode and configuration. SysML compatibility is not sufficient evidence for electrical, mechanical, safety or cybersecurity compatibility.

**Link structure and behavior.** Actions model performances with parameters, control and object flows; states model conditions and transitions; calculations have input/result parameters; constraints evaluate conditions. Bind behaviors to performers and configured properties. Preserve event ordering, concurrency, guards, termination, failure and state-dependent availability. A behavior diagram does not prove liveness, schedulability or resource adequacy unless a relevant analysis establishes them.

**Make quantitative semantics explicit.** Use quantities/units and calculation/constraint definitions consistently with SYSENG-055. A displayed equation may be descriptive, executable or both depending on implementation and binding. Declare input/output direction, numerical method, solver, tolerances and provenance. A conforming calculation syntax does not validate equations or input evidence.

**Treat requirements as constraints on subjects.** SysML 2.0 requirements can include subject, stakeholder, assumed constraints and required constraints. Keep requirement statement, identity, source, rationale, applicability, risk and authority. Requirement satisfaction relationships express modeled claims; they require verification evidence. Avoid circular arguments where a design value both defines and “verifies” its limit.

**Use cases for planned reasoning.** Analysis cases structure an objective and behavior used to analyze a subject. Verification cases identify requirements to verify and produce verdicts such as pass, fail, inconclusive or error. A case definition or usage is a specification. Record execution identity, subject configuration, method, resources, inputs, environment, result, anomalies and approval separately. “Verification case exists” is coverage, not execution or pass evidence.

**Separate concern, viewpoint, view and rendering.** Concerns articulate stakeholder interests. A viewpoint governs how a view addresses concerns, including selection and presentation rules. A view exposes model elements; a rendering produces a presentation such as a diagram or table. Generate multiple audience-specific renderings from shared semantics. Review exclusions: a clean view may omit a critical hazard or configuration distinction.

**Use allocations with declared meaning.** Allocation can relate responsibility, function to structure, logical to physical, requirement to owner, resource to consumer or other project-defined mappings. Name the relation's intended semantics and cardinality. An allocation is not automatically a design decision, implementation, trace or proof of capacity.

**Govern metadata and extensions.** Metadata can mark safety level, assurance status, source authority, lifecycle state or domain classification. Define metadata semantics, allowed targets, values, inheritance/propagation and validation. Prefer standard concepts and libraries. For extensions, record owner, namespace, version, compatibility, transformation/API representation and removal or migration policy. A vendor icon must never be the only carrier of consequential meaning.

**Distinguish authored, derived and implied facts.** Tools may calculate inherited memberships, feature chains or implied relations from language rules. Mark what users authored and what tooling derived. A derived value must be recomputable from a controlled commit and rule implementation. Avoid round trips that convert derived relationships into authored duplicates, creating conflicts.

**Use textual and graphical notation as complementary views.** Text is effective for precise declarations, reviewable diffs, search and automation. Graphics are effective for spatial overview, interaction and stakeholder communication. Neither is inherently the “real” model; both should resolve to the same identity-bearing abstract syntax. Test that edits through either representation preserve meaning. Do not assume line-oriented text merges are semantically valid.

**Query by semantics, not layout.** Useful checks ask: Which required interfaces lack typed ends? Which requirements lack verification coverage for this baseline? Which actions have no performer? Which usages type against an unapproved library? Which views expose superseded elements? Queries need selected project and commit, scope, pagination, access assumptions, schema/tool version and expected handling of partial/unknown results.

**Evaluate API claims at the right level.** Systems Modeling API and Services defines services for projects, branches, commits, elements, relationships, queries and navigation. Test identifier preservation, commit selection, branching/change behavior, relationship direction, derived content, query completeness, pagination, error responses, authorization, bulk performance and schema evolution. API conformance, language conformance, interchange fidelity and workflow integration are separate claims.

**Test interchange with semantic round trips.** Export a controlled fixture containing packages, definitions/usages, feature relationships, multiplicities, connections, behavior, requirements, cases, views, metadata and extension cases. Import it into the target, export again and compare identity, types, relationships, values, libraries and expected derived facts—not file bytes or picture similarity. Record unsupported content and loss. A round trip through the same implementation is weaker than an independent-tool test.

**Migrate v1 as a governed transformation.** Inventory profiles, stereotypes, diagrams, element IDs, instance specifications, value types/units, opaque expressions, scripts, validation rules, generated reports and integrations. Freeze the source baseline. Apply the normative transformation for supported constructs through a versioned implementation. Preserve source-to-target trace and warnings. Reconcile semantic differences and unmapped extensions manually. Rebuild views around current questions rather than forcing every old diagram to survive.

**Validate migration outcomes.** Compare requirement/interface/behavior/property/verification inventories and selected golden scenarios. Recompute analyses, regenerate governed work products and test downstream API/report/code integrations. Sample high-consequence elements and adversarial patterns. Obtain domain-owner acceptance for semantic equivalence or document intentional change. Keep the v1 source accessible until retention and audit obligations permit retirement.

**Measure useful coverage.** Track answered modeling questions, reviewed interfaces, requirements with credible verification evidence, cross-view inconsistency defects, change-impact completeness and decision latency. Element and diagram counts can encourage duplication. A smaller model with explicit scope, authority and evidence is often more useful than a vast ungoverned repository.

The following executable example checks a deliberately simplified, data-defined subset of SysML-like semantics. It is not a SysML parser and does not claim conformance to OMG abstract syntax, textual grammar, libraries, API or interchange.

<!-- bijux-verify: {"id":"declared-sysml-semantics-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"definitions=4\nusages=5\nunique_qualified_names=1\ntyped_usages=5\nowned_usages=5\nports=2\nconnections=1\nconnection_type_compatible=1\nrequirements=2\nverification_cases=2\nunverified_requirements=0\nstatus=declared_sysml_semantics_consistent\nevidence=declared_subset_only\n","stderr":""}} -->
```python
definitions = {
    "MissionPower::BatteryPack": {"kind": "part_def"},
    "MissionPower::Controller": {"kind": "part_def"},
    "MissionPower::PowerPort": {"kind": "port_def", "item": "ElectricPower"},
    "MissionPower::DCLink": {"kind": "connection_def", "item": "ElectricPower"},
}

usages = [
    {"name": "MissionPower::pack", "type": "MissionPower::BatteryPack", "owner": "MissionPower"},
    {"name": "MissionPower::controller", "type": "MissionPower::Controller", "owner": "MissionPower"},
    {"name": "MissionPower::pack::supply", "type": "MissionPower::PowerPort", "owner": "MissionPower::pack"},
    {"name": "MissionPower::controller::input", "type": "MissionPower::PowerPort", "owner": "MissionPower::controller"},
    {"name": "MissionPower::dc_link", "type": "MissionPower::DCLink", "owner": "MissionPower"},
]

connections = [{
    "name": "MissionPower::dc_link",
    "source": "MissionPower::pack::supply",
    "target": "MissionPower::controller::input",
    "item": "ElectricPower",
}]
requirements = {"REQ-POWER-01", "REQ-POWER-02"}
verification_cases = {"VC-POWER-01": "REQ-POWER-01", "VC-POWER-02": "REQ-POWER-02"}

by_name = {usage["name"]: usage for usage in usages}
typed = [usage for usage in usages if usage["type"] in definitions]
ports = [usage for usage in usages if definitions[usage["type"]]["kind"] == "port_def"]
compatible = all(
    connection["source"] in by_name
    and connection["target"] in by_name
    and definitions[by_name[connection["source"]]["type"]]["item"] == connection["item"]
    and definitions[by_name[connection["target"]]["type"]]["item"] == connection["item"]
    for connection in connections
)
covered = set(verification_cases.values())

checks = {
    "unique_names": len(by_name) == len(usages),
    "typed": len(typed) == len(usages),
    "owned": all(usage["owner"] for usage in usages),
    "compatible": compatible,
    "coverage": requirements <= covered,
}

print(f"definitions={len(definitions)}")
print(f"usages={len(usages)}")
print(f"unique_qualified_names={int(checks['unique_names'])}")
print(f"typed_usages={len(typed)}")
print(f"owned_usages={sum(bool(usage['owner']) for usage in usages)}")
print(f"ports={len(ports)}")
print(f"connections={len(connections)}")
print(f"connection_type_compatible={int(compatible)}")
print(f"requirements={len(requirements)}")
print(f"verification_cases={len(verification_cases)}")
print(f"unverified_requirements={len(requirements - covered)}")
print("status=" + ("declared_sysml_semantics_consistent" if all(checks.values()) else "declared_semantic_issue"))
print("evidence=declared_subset_only")
```

This checker would still pass if the two requirements were unnecessary, the port voltage were unsafe, both usages referred to the wrong product variant, the verification cases had never executed, or the data could not be represented by a conforming SysML tool. Those are separate reviews.

## Definitions and Notation

Let an element record at commit $c$ be

$$
e_c=(id,kind,name,qname,owner,type,status,source,applicability,version).
$$

`id` supports durable reference; `name` and qualified name `qname` support human navigation; `owner`/namespace membership supplies context; `type` and feature relations constrain semantics. Equality of names does not imply identity, and equality of identity across commits does not imply unchanged meaning.

Let $D$ be definitions and $U$ usages. A typing relation $typedBy(u,d)$ constrains $u\in U$ to instances classified by $d\in D$. Let feature $f:T\rightarrow \mathcal{P}(V)$ map each instance of type $T$ to a set of values. If $f_s$ subsets $f_g$, then for applicable instances $x$,

$$
f_s(x)\subseteq f_g(x).
$$

Redefinition adds specialization and context rules beyond a coincidental same name. Multiplicity bounds the cardinality $|f(x)|$; it does not establish availability, reliability or simultaneous existence without further semantics.

For connection $k=(ends,item,direction,mode,configuration)$, a project-level compatibility predicate can be written

$$
C(k)=C_{type}\land C_{direction}\land C_{multiplicity}\land C_{mode}\land C_{configuration}\land C_{domain}.
$$

SysML/KerML semantics support several terms in this predicate, while $C_{domain}$ may require protocol, electrical, mechanical, safety, timing or other engineering evidence.

Let $Q(M_c)$ be a query evaluated over model commit $c$. Reproducible evidence records query text/version, project, commit, scope, access principal, API/schema/tool build, page completion and result digest. Comparing $Q(M_{c_1})$ with $Q(M_{c_2})$ without preserving these conditions can confuse model change with query or access change.

## Mechanisms, Invariants, or Proof Structure

**Semantic chain.** A trustworthy claim follows a chain: stakeholder concern $\rightarrow$ modeled question $\rightarrow$ controlled definition/usage and configuration $\rightarrow$ behavior/property/interface/requirement relation $\rightarrow$ analysis or verification method $\rightarrow$ evidence $\rightarrow$ bounded conclusion. SysML provides many nodes and edges; project governance establishes authority and evidence acceptance.

**Typing invariant.** Every consequential usage resolves to an approved definition or explicitly remains untyped for a justified reason. The definition and imported libraries exist in the selected commit/version. Tool display caching cannot substitute for reference resolution.

**Configuration invariant.** Every cross-element reasoning path is configuration-compatible. A requirement for product A, a port on product B and a test result for prototype C cannot establish one claim merely because their names match.

**Interaction invariant.** Each connection's ends exist in context, multiplicities permit the link, directions and conveyed items agree, and domain constraints are verified separately. Conjugation changes the interaction perspective; it does not automatically generate a complete protocol contract.

**Requirement-evidence invariant.** A requirement has authoritative identity and subject; satisfaction claims point to applicable evidence; a verification case specification is separate from an execution/result; non-pass verdicts and anomalies remain visible; waivers/deviations have authority and scope.

**View invariant.** A view is reproducible from a selected commit, viewpoint and rendering rule. A view may omit content intentionally, but it cannot silently redefine exposed elements. Generated documents record source commit and generator version.

**Derivation invariant.** Derived/implied facts have one declared derivation rule and can be regenerated. Authored facts are not overwritten by derived convenience. Differences between tool derivations are treated as interoperability defects or declared limitations.

**Migration invariant.** Every in-scope v1 semantic item is transformed, mapped to an intentional v2 replacement, retained as governed external/legacy content, or logged as unresolved. Counts alone are insufficient; high-consequence traces and downstream behaviors are sampled and tested.

There is no proof in this chapter that these invariants make an architecture correct. They form review obligations. A syntactic validator can prove properties about an encoded artifact under its implementation and inputs; physical and stakeholder claims require additional models and observations.

## Alternatives and Trade-Offs

**SysML v2 versus continued v1.** V2 provides a newer semantic foundation, definition/usage consistency, textual notation and standard API. V1 may have mature organizational methods, profiles, tools and trained users. A mixed transition may be rational, but needs clear boundaries and no false claim that similarly named constructs are identical.

**Textual versus graphical authoring.** Text supports precise diffs, templates and automation; graphics support overview and collaborative reasoning. Text can become opaque and merge-conflicted; graphics can conceal detail and encourage layout-driven semantics. Use both against one underlying model and test semantic round trips.

**Monolithic versus federated repositories.** One repository simplifies identity and query consistency but can create scale, access and supplier-boundary problems. Federation preserves domain tools and ownership but requires identifiers, versioned contracts, transformations and partial-failure handling. “Single source of truth” should mean explicit authority, not necessarily one database.

**Standard-only versus extensions.** Standard concepts improve portability and shared understanding. Domain extensions can encode assurance, regulatory or physical semantics that the base language does not supply. Extend narrowly, version it and test its API/interchange representation; do not distort a standard construct to avoid governance.

**Generated views versus curated documents.** Generation improves freshness and provenance. Curated narrative can communicate reasoning and dissent better. Combine generated facts with controlled human rationale; mark source commit and prevent manual edits to generated facts from becoming shadow authority.

**Strict validation versus exploratory modeling.** Strict rules protect baselines; premature rigidity can block learning. Use lifecycle states and validation profiles: allow explicit unknowns in exploration, then progressively require identity, typing, configuration, evidence and review before decisions/releases.

**Automatic transformation versus manual remodeling.** Automation preserves scale and repeatability; manual remodeling can better exploit v2 concepts and retire obsolete diagrams. Apply automation to inventory and supported transformations, then use risk-ranked semantic reconciliation and targeted remodeling.

## Failure Modes and Misconceptions

**“SysML is the MBSE process.”** The language does not select questions, sequence work, assign authority or set evidence criteria. Pair it with a declared method and governance.

**“The diagram is the model.”** A diagram is a rendering or view. Inspect identities, memberships and relationships in the underlying model and regenerate presentations from a controlled commit.

**“Same name means same thing.”** Names collide and change. Use stable identity, namespace, type, source and configuration; reconcile semantic changes explicitly.

**“Specialization is just an `is-a` arrow.”** It constrains instance classification. Check inherited constraints and substitutability rather than visual taxonomy.

**“A connection means the interface works.”** It may establish modeled endpoint relationships. Verify protocol, item, direction, units, timing, capacity, faults, security and physical compatibility.

**“Satisfy means proven.”** A modeled satisfaction relation records a claim. Demand applicable verification/validation evidence and authority.

**“A verification case means verified.”** A case is a specification until an identified execution produces reviewed evidence and verdict for the configured subject.

**“All derived relations should be stored.”** Persisted derived facts can become stale duplicates. Preserve derivation rules and distinguish authored from recomputable content.

**“The standard API guarantees interoperability.”** It standardizes important model services and representations. Test supported language coverage, identity, commit semantics, queries, extensions, round trips and failures between actual implementations.

**“Transformation makes v1 and v2 equivalent.”** The normative transformation covers defined mappings; project profiles, scripts, opaque semantics and downstream assumptions still require reconciliation.

**“More model elements mean more maturity.”** Counts reward duplication. Measure decision coverage, semantic defects, evidence linkage, change impact and stakeholder utility.

## Worked Examples

### Example 1

**Definition and usage.** A rail project has one `AxleCounter` definition and 240 trackside usages. The definition owns common interfaces and constraints; each usage carries location, installed serial/configuration, environment and maintenance evidence. Creating 240 near-identical definitions would obscure common semantics. Treating the one definition as installed equipment would erase occurrence identity and configuration.

The review samples a usage, resolves its definition/library at the baseline commit, checks inherited features and confirms its as-installed evidence. The bounded conclusion is that the model represents the declared fleet structure; it does not prove every device exists or works.

### Example 2

**Subsetting versus redefinition.** A hospital system defines `careTeam` as all authorized caregivers. An intensive-care usage has `bedsideTeam subsets careTeam`; a specialized unit redefines an inherited `monitor : PatientMonitor` feature to require `CriticalCareMonitor`. The first relation constrains membership values; the second specializes an inherited feature/type in context.

Using redefinition merely to give `bedsideTeam` a new label would muddle semantics. Reviewers test value containment, compatible typing and multiplicity, then separately validate staffing policy and device qualification.

### Example 3

**Port conjugation and flow.** A power source exposes an output-oriented DC port; a controller has the compatible conjugate interaction. A connection conveys `ElectricPower`. The model query checks endpoint types, direction, item kind and configured mode.

Engineering review still checks voltage range, polarity, current/transient rating, connector keying, protection, grounding, thermal conditions and fault behavior. The green semantic query narrows defects; it does not certify the electrical interface.

### Example 4

**Behavior linked to structure.** A drone's `EmergencyLanding` action is performed by the configured flight controller, consumes sensor/navigation inputs and transitions operational state. A failure state disables one navigation source. A scenario view exposes action, performer, state guard and degraded connection.

A consistency query finds that an old action referenced a superseded controller usage. Repairing the identity link makes the model coherent. Timing, control stability and safe landing probability remain analysis/test questions.

### Example 5

**Calculation and requirement.** A thermal requirement constrains controller junction temperature under a declared hot-day mission subject. A calculation binds dissipated power, thermal resistance and ambient condition to predicted temperature; the requirement's subject and calculation inputs reference the same product variant and mission configuration.

The model evaluates the declared relation and finds positive point margin. Review then checks units, nonlinear effects, uncertainty, model validation and test evidence. Neither SysML syntax nor a positive calculated margin establishes actual compliance alone.

### Example 6

**Verification specification versus result.** A `VehicleMassTest` verification case names the vehicle subject and mass requirement, method and resources. Its existence satisfies a coverage query. A separate execution record identifies prototype serial, scale calibration, configuration, procedure revision and verdict.

When the execution returns `inconclusive` because configuration evidence is missing, the dashboard retains that verdict. Converting it to pass because the measured number was low would confuse numerical observation with applicable verification evidence.

### Example 7

**Viewpoint-governed communication.** Safety, maintenance and supplier stakeholders need different views of the same hydraulic isolation design. Their viewpoints select hazards/barriers, service access, and contractual interface content respectively. All renderings resolve to the same valve and connection identities.

A supplier view deliberately excludes internal hazard analysis but cannot redefine port pressure. The generated document records commit and viewpoint version. Separate access control and review confirm that exclusions are authorized and that each concern is addressed somewhere.

### Example 8

**API query under version.** A CI check asks for requirements lacking verification coverage on release branch commit `c`. It retrieves every page, records schema/tool version, and treats authorization-filtered or failed pages as indeterminate rather than zero results. The result digest is attached to the release evidence.

Running the same query against branch head later gives a different set. Because both commits and query conditions are retained, reviewers can attribute the difference to model changes instead of claiming the earlier audit was wrong.

### Example 9

**Interchange round trip.** Two tools exchange a fixture containing definitions/usages, ports, a redefined feature, requirement, verification case, view and safety metadata. Pictures look similar, but comparison finds lost metadata targets and newly assigned IDs. The interoperability result therefore fails despite successful import.

The team records supported subsets and blocks safety-metadata transfer until fixed. It does not manually recolor the diagram, because appearance would conceal lost semantics.

### Example 10

**V1-to-v2 migration.** A satellite model inventory finds standard v1 elements, a custom reliability profile, opaque simulation scripts and 180 generated interface tables. The team freezes source/tool versions, applies a controlled transformation, preserves source-target traces and triages warnings by consequence.

Rather than recreate every diagram, it rebuilds governed v2 viewpoints and compares requirement/interface/property/verification inventories plus golden analysis outputs. Reliability stereotypes and scripts remain explicit unresolved items until domain owners validate replacements. Migration completion is based on accepted semantic outcomes, not transformed element count.

## Cross-Program Connections

**Platform engineering.** Platform catalogs, golden paths, service/resource definitions and policy evidence benefit from definition/usage separation, configured views and API-queryable identity.

**API and service engineering.** The Systems Modeling API itself illustrates versioned resources, branches/commits, queries, schemas, pagination and partial-failure concerns. Modeled service interfaces still require protocol contracts and runtime evidence.

**Data engineering.** Model exchange is a lineage and schema-evolution problem: preserve identity, provenance, transformations, derived fields, snapshots and quality checks across tools.

**Object-oriented programming.** Class/instance and inheritance intuitions are helpful but incomplete. SysML definitions/usages, feature subsetting/redefinition, occurrences and semantic libraries should be learned on their own terms rather than forced into one programming-language object model.

**Functional programming.** Immutable model commits, pure derivations and typed transformations improve reproducibility. Repository effects, identity, merge semantics, tool conformance and empirical evidence remain explicit boundaries.

## References

1. Object Management Group, *OMG Systems Modeling Language, Version 2.0, Part 1: Language Specification*, formal/2026-03-02. <https://www.omg.org/spec/SysML/2.0/Language/PDF>
2. Object Management Group, *About the OMG Systems Modeling Language Specification Version 2.0*, formal specification and machine-readable artifacts. <https://www.omg.org/spec/SysML/2.0>
3. Object Management Group, *Kernel Modeling Language, Version 1.0*, formal/2026-03-01. <https://www.omg.org/spec/KerML/1.0/PDF>
4. Object Management Group, *About the Kernel Modeling Language Specification Version 1.0*, normative artifacts and formal history. <https://www.omg.org/spec/KerML/1.0>
5. Object Management Group, *Systems Modeling API and Services, Version 1.0*, formal/2026-03-04. <https://www.omg.org/spec/SystemsModelingAPI/1.0/PDF>
6. Object Management Group, *About the Systems Modeling API and Services Specification Version 1.0*, normative machine-readable artifacts. <https://www.omg.org/spec/SystemsModelingAPI/1.0>
7. Object Management Group, *SysML v1 to SysML v2 Transformation*, formal/2026-03-03. <https://www.omg.org/spec/SysML/2.0/Transformation/PDF>
8. OMG Systems Modeling Community, *SysML v2 Release Repository*, current reference artifacts and examples. <https://github.com/Systems-Modeling/SysML-v2-Release>
9. NASA, *NASA Systems Modeling Handbook for Systems Engineering*, NASA-HDBK-1009A, active 2025. <https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009>
10. IEEE Standards Association, *IEEE/ISO/IEC 42010-2022—Software, systems and enterprise—Architecture description*, active standard. <https://standards.ieee.org/ieee/42010/6846/>

## Exercises

### Exercise 1

Model a clinic backup-power system using definitions/usages, ports/connections, behavior, quantities, requirements and verification cases. State what automated checks can and cannot conclude.

### Exercise 2

Audit a model where every component is a definition, relationships are chosen by arrow appearance, diagrams contain copied property values, and a “satisfy” relation is treated as proof.

### Exercise 3

Design a viewpoint/view strategy for operator, safety assessor, maintainer, supplier and executive concerns without creating separate factual models.

### Exercise 4

Specify an interoperability evaluation between two SysML 2.0 tools using the standard API and file exchange. Include version, identity, semantic coverage, failure and evidence criteria.

### Exercise 5

Plan migration of a large SysML v1 repository containing custom profiles, opaque calculations, generated documents and external integrations to SysML 2.0.

## Answers to the Exercises

### Answer 1

Create a governed package and baseline. Define `ClinicPowerSystem`, `BatteryPack`, `AutomaticTransferController`, `PowerPort`, `ControlPort`, `DCLink` and relevant item/quantity definitions. Use one clinic system with configured primary/emergency battery and controller usages; do not make each installation a new definition unless it has genuinely distinct reusable semantics. Give usages stable identity, owner, configuration, multiplicity and lifecycle status.

Place typed supply/demand/control ports on the configured usages. Define connections/interfaces with conveyed item, direction, voltage/current quantity semantics, multiplicity, operating/degraded modes and external physical/protocol references. Model `DetectGridLoss`, `IsolateGrid`, `StartBackup` and `SustainCriticalLoads` actions, performers, events, state transitions, timeouts and failure/recovery paths. Bind behavior-derived loads/durations to calculations and controlled value properties.

Give each requirement authoritative identity, subject, assumptions and required constraint—for example transfer time, usable energy, isolation and critical-load availability under a declared configuration/environment. Define analysis cases for load/energy and verification cases for inspection, analysis, demonstration or test. Keep case specification separate from execution and verdict evidence.

Automated checks may establish resolved typing, unique names, ownership, allowed multiplicities, configured endpoint/item/direction consistency, unit/dimension rules, action performers, requirement-to-case coverage and reproducible point calculations. They cannot establish stakeholder completeness, correct architecture, physical connector suitability, code/control correctness, battery degradation behavior, safe isolation, actual test execution or field performance without separate domain models, implementation checks and evidence. Report each conclusion at its evidence level.

### Answer 2

Freeze the project, branch/commit, libraries, tool version and generated outputs before repair. Inventory definitions and ask which reusable kinds they classify. Convert context-specific installed/logical roles to usages typed by durable definitions, preserving source identities or trace mappings. Check that occurrences, composite/reference meaning, multiplicity and configuration match the real system.

Classify every relationship semantically. Replace appearance-driven arrows with typing, specialization, subsetting, redefinition, binding, connection, allocation, dependency or trace only when its preconditions and intended meaning hold. For specializations, review inherited constraints/substitutability; for subsets, value containment; for redefinitions, contextual feature compatibility; for connections, ends, direction, item and domain contract.

Find each copied diagram value and identify one authoritative property/source. Replace duplicates with views of, references to or reproducible generated snapshots from the authority. Record commit and rendering rule. Differences are defects to reconcile, not formatting choices.

Treat every satisfaction relation as an asserted modeled claim. Trace the requirement subject and configured design, then locate applicable verification method, execution, results, anomalies and approval. Downgrade unsupported claims to planned/unverified rather than deleting history. Add checks for unresolved type, ambiguous reference, duplicate identity, cross-variant relation, stale generated value, unsupported satisfaction and missing execution evidence. Re-review stakeholder/modeling questions; structural cleanup alone does not demonstrate coverage.

### Answer 3

Start with a concern register and common controlled semantic model. Operator concerns include modes, controls, indications, timing, degraded behavior and recovery. Safety concerns include hazards, causal paths, barriers, safety requirements and verification evidence. Maintenance concerns include replaceable units, isolation/access, diagnostic behavior, tools and procedures. Supplier concerns include only contractual interfaces, allocations, assumptions and acceptance evidence permitted by access rules. Executive concerns include decisions, capability, risk, readiness, cost/schedule and unresolved evidence without technical clutter.

Define a versioned viewpoint for each audience: stakeholders/concerns addressed, model kinds, selection/filter/exposure rules, notation/rendering, completeness/consistency checks and limitations. Construct views by exposing the same identity-bearing requirements, usages, interfaces, behaviors, risks and evidence under those rules. Use multiple renderings where graphical overview, table and textual rationale serve different questions.

Do not copy values or recreate elements in audience packages. Access-controlled views may omit sensitive facts, but omissions and their authority are explicit. Shared facts such as a port limit resolve to one configured property. Record source model commit, viewpoint/generator version and filters on each generated artifact. Review both inclusion and exclusion, run cross-view identity/value checks, and retain human rationale/dissent alongside generated content. A viewpoint structures communication; it does not guarantee that concerns are complete or resolved.

### Answer 4

Declare exact formal SysML 2.0, KerML 1.0, API 1.0, schema/machine-readable artifact, standard library, extension and both tool/build versions. Obtain each vendor's claimed conformance scope. Create a risk-ranked fixture with namespaces/imports, identities/names, definitions/usages, typing/specialization/subsetting/redefinition, multiplicities, parts/items/ports, connections/interfaces/flows, actions/states/calculations/constraints, requirements/cases, views/viewpoints, metadata, units and representative extensions.

For API tests, create/select project, branch and commit; retrieve elements and relationships by identity; navigate both directions; execute filtered queries; verify all pages; create changes/commits/branches where supported; and test missing IDs, invalid commits, authorization filtering, concurrency, partial failures and schema/version mismatch. Record requests, status/error bodies, page counts, timing, tool logs and result digests without exposing protected model content.

For file exchange, export at a controlled commit, import into tool B, export again and compare semantic graph projections: stable/source-target identity, kinds, ownership/membership, qualified names, relationships, multiplicities, values/units, library references, authored versus derived facts, and extension preservation. Repeat B-to-A and, where possible, use independent validators/reference fixtures. Similar images or file bytes are not acceptance criteria.

Predeclare mandatory, tolerated-with-warning and unsupported constructs. Fail on silent loss, changed identity, wrong relation semantics, partial results reported as complete or unreproducible derived content. Distinguish API-service, language, library and workflow evidence. Publish a bounded interoperability matrix with artifacts and unresolved risks; do not claim general tool conformance from one fixture.

### Answer 5

Establish migration decisions, scope, regulatory/contractual retention, target formal versions, tool/API/library baseline, responsible owners and acceptance criteria. Freeze and archive the v1 source repository with tool/profile versions. Inventory element kinds, diagrams/tables, packages, IDs, requirements, value types/units, allocations, behaviors, instance specifications, custom stereotypes/tag values, opaque expressions, simulation scripts, validation rules, reports, templates, code generators, APIs and consuming systems. Rank by consequence and usage, not count.

Define a mapping register: normative transformation rule where applicable, target v2 concept, identity/source-target trace policy, expected information loss, owner and validation. Test the transformation implementation on representative/adversarial fixtures before bulk use. Preserve logs and warnings. Do not force v1 block/instance/profile intuitions mechanically onto v2 definitions/usages, KerML feature relations and metadata. Replace custom concepts with standard ones only when semantics genuinely match; otherwise create governed extensions or retain an explicit external/legacy link.

Transform into controlled branches and reconcile unresolved items by domain. Rebuild package architecture, viewpoints and generated views around current decisions. Reimplement opaque calculations and scripts with declared inputs, units, algorithms and tests. Update API/report/code integrations against stable identities and commit semantics. Prevent the migration from overwriting the auditable source.

Validate structurally with inventories and referential/typing/configuration rules; semantically through risk-ranked owner review and source-target traces; computationally by recomputing golden cases and boundary scenarios; operationally by regenerating accepted work products and exercising downstream workflows; and pedagogically through user tasks/training. Record intentional differences, defects, waivers and remaining v1 dependencies. Cut over by governed configuration with rollback and monitoring. Retire v1 only after acceptance, retention and downstream obligations are satisfied; transformed element count alone is never completion evidence.
