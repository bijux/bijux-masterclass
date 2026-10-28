---
module_id: SARCH-029
program: Software Engineering: Software Architecture
level: 1
module_number: 29
title: C4, UML, and Informal Diagram Semantics
status: complete
last_verified: 2026-09-06
---

# C4, UML, and Informal Diagram Semantics

## One-Page Review

### Governing question

How can architects choose and govern C4, UML, or informal diagrams so that viewers can recover the intended elements, relationships, scope, abstraction, and claims without inferring semantics from unexplained boxes, arrows, colors, or layout?

### Essential definitions

- A **model** is a purposeful abstraction containing selected concepts and relationships; a **diagram** is one visual rendering of a model or model fragment.
- **semantics** determines what modeled elements and relationships mean; **syntax** determines permitted constructs; **notation** maps constructs to visible marks.
- A **legend** declares the meaning of shapes, lines, arrowheads, color, borders, icons, and other encodings used in a diagram.
- An **abstraction level** states which kinds of things may appear and which details are intentionally hidden.
- C4 is an abstraction-first approach using people, software systems, containers, components, and code, with core zoom levels for context, container, component, and code views.
- In C4, a **container** means an independently runnable or deployable application or data store; it does not necessarily mean an operating-system container.
- UML is a standardized modeling language with defined abstract syntax and semantics across structural and behavioral model kinds.
- An **informal diagram** uses a locally defined visual vocabulary rather than a comprehensive standardized language.
- A **correspondence** relates elements or claims across diagrams, models, source, runtime, deployment, decisions, and evidence.
- **semantic ambiguity** exists when a viewer cannot determine one intended interpretation from the diagram and its governing material.

### Central model, mechanism, or theorem

Represent a governed diagram as

$$
D=(M,G,\iota,L,S,C,V),
$$

where $M$ is the selected model, $G$ graphical marks, $\iota:G\rightarrow M$ the interpretation mapping, $L$ the legend and notation rules, $S$ scope and abstraction, $C$ cross-model correspondences, and $V$ version and evidence context.

For every visible distinction used to support a claim, $\iota$ must be defined. If the same glyph denotes incompatible model kinds without a discriminator, interpretation is not a function and the diagram is ambiguous for that concern.

### Critical invariants

- state title, purpose, audience, concern, scope, abstraction, lifecycle state, and version;
- give every element a stable name, explicit type, responsibility, and boundary;
- label every consequential relationship with direction and semantics;
- define every meaningful shape, line, arrowhead, color, icon, position, and multiplicity;
- avoid mixing C4 abstraction levels or UML model kinds without explicit correspondence;
- distinguish logical responsibility, source module, runtime instance, deployment node, and data authority;
- show omitted detail and link to deeper or adjacent views instead of crowding one picture;
- preserve external systems, trust boundaries, failure paths, state, and control paths when relevant;
- make tool-specific or organization-specific extensions explicit;
- keep diagram source, generated rendering, model data, and reviewed version traceable;
- validate correspondence against manifests, code, configuration, tests, traces, and owners;
- treat readability and conformance as evidence, not proof of architectural correctness.

### Common failures

Common failures include untitled “boxes and arrows”; arrows with no direction or meaning; colors without legends; using spatial proximity as dependency; labeling every element “service”; mixing logical systems, code classes, processes, databases, and cloud products at one level; confusing a C4 container with a container image; drawing UML-looking shapes with non-UML meaning; using stereotypes without definitions; presenting one scenario trace as static topology; omitting external systems and trust boundaries; letting generated diagrams become stale; and claiming standardized notation makes the architecture correct.

### Compact example

A box labeled `Payments` connects to `Ledger` with a dashed arrow. Viewers cannot tell whether the boxes are systems, components, teams, or deployments, nor whether the arrow means call, event, data dependency, ownership, or future work. Add diagram type and scope, type each element, label `submits immutable posting command`, define the dashed style, identify direction and authority, and link to the runtime interaction view.

### Connections

[SARCH-021](021-context-views.md) through [SARCH-028](028-operational-views.md) provide model kinds that can be rendered with different notations. [SARCH-030](../ROADMAP.md) next composes architecture descriptions for different audiences. Modeling Languages, Software Engineering Methods, Systems Engineering, and Human-Computer concerns deepen formal syntax, semantics, assurance, and visual communication.

## Governing Question

Architecture diagrams are compressed arguments. A viewer sees a small set of marks and infers boundaries, dependencies, authority, execution, sequence, and risk. When the encoding is undefined, different viewers construct different architectures from the same picture.

The governing problem is not “Which diagramming brand is best?” It is how to select a model and notation whose semantics fit the concern, teach enough vocabulary to the audience, preserve correspondence with other views, and make ambiguity visible. C4, UML, and informal diagrams occupy different points in this design space.

## Why This Matters

Diagram errors influence decisions. A missing dependency can invalidate availability analysis. An arrow drawn backward can reverse authority. A deployment icon inside a logical view can imply false co-location. A green boundary may be read as trust, ownership, health, or approval. A class diagram can be mistaken for a runtime configuration.

Conversely, excessive formalism can exclude the audience or create detail without insight. A diagram that is semantically precise but unreadable fails communication. A simple informal view can be rigorous if its vocabulary, scope, relationships, and omissions are explicit.

Architecture work therefore separates model quality, notation quality, rendering quality, and evidence quality. No single picture needs to answer every question, but the description as a whole must let stakeholders navigate and reconcile the necessary views.

## Prerequisites and Retrieval

Retrieve architecture description, concern, stakeholder, viewpoint, model kind, model, diagram, syntax, semantics, notation, legend, abstraction, element, relationship, boundary, direction, multiplicity, role, type, instance, static, dynamic, deployment, correspondence, conformance, traceability, and evidence.

From prior modules, retrieve context, module/code, component-and-connector, runtime interaction, deployment, information, development/build, and operational views. Distinguish a modeled fact from its graphical encoding and an intended structure from observed evidence.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish model, diagram, syntax, semantics, notation, legend, and rendering;
2. explain C4 abstractions and choose useful zoom levels without conflating “container” meanings;
3. select a bounded UML subset appropriate to structural or behavioral concerns;
4. define an informal notation with unambiguous element and relationship types;
5. detect mixed abstraction, overloaded glyphs, implied semantics, and missing scope;
6. connect context, static, dynamic, deployment, data, security, and operational diagrams;
7. evaluate diagram readability separately from semantic and architectural correctness;
8. govern diagram-as-code, generated views, manual annotations, and version traceability;
9. perform audience-based and model-based diagram reviews;
10. verify correspondences using bounded repository and runtime evidence.

## Core Exposition

**Start with the model.** Decide the concern, concepts, relationships, constraints, and omissions before choosing shapes. A runtime topology model contains active components and connectors. A deployment model contains artifacts, environments, nodes, placements, and paths. Drawing both with rectangles does not make them the same model.

ISO/IEC/IEEE 42010:2022 remains the current published architecture-description edition as checked on 2026-09-06. It distinguishes architecture from its description and governs descriptions through stakeholders, concerns, viewpoints, model kinds, correspondences, and conventions [1]. This makes notation a servant of the description, not its authority.

**Separate semantics from notation.** Semantics says an element is a runtime message broker with durable, at-least-once delivery under stated conditions. Notation says it appears as a rounded blue rectangle. Changing blue to gray should not change the model unless color is defined semantically.

Every meaningful visual variable needs a rule: shape, border, fill, line, arrowhead, label, nesting, position, size, icon, and badge. Decorative styling need not carry meaning, but say so when viewers may infer it. Do not use red for both trust risk and current outage.

**Give the diagram a contract.** Include title, model kind or diagram type, entity of interest, scope, abstraction, lifecycle state, environment, version, audience, and legend. Type elements explicitly. Give each a stable name and short responsibility. Label relationships with an active phrase and direction. Define boundaries and multiplicities.

An isolated export must remain mostly understandable. Link to definitions, decisions, deeper views, and evidence, but do not make the surrounding presentation the only place where an arrow's meaning exists.

**Use C4 as an abstraction hierarchy.** The official C4 material retrieved 2026-09-06 describes people using software systems; systems contain one or more containers; containers contain components; and components are implemented by code elements [2]. Its core static diagrams zoom through system context, container, component, and code, with supporting landscape, dynamic, and deployment diagrams [3].

A context diagram shows the focal system, people, and external systems. A container diagram shows major runnable or deployable applications and data stores inside one software system. A component diagram decomposes a selected container into responsibilities. A code diagram shows implementation detail when it adds value.

Do not use every level by ritual. A small system may need context and container only. A complicated container may need several concern-specific component views. C4's official guidance says its notation is independent and recommends titles, explicit element types, relationship labels, and legends [4]. The simplicity works only when these semantics are honored.

**Disambiguate C4 container.** C4 predates and intentionally uses “container” as an architectural abstraction: an application or data store that must run or be deployed for the system to work. A C4 container might execute as a process, mobile application, serverless function set, database, or operating-system container. Map it to artifacts and deployment separately.

Similarly, a C4 component is not necessarily a UML component, runtime process, source package, or independently deployable service. Define the responsibility and map it to code and runtime views. Reusing a word does not import another notation's semantics.

**Use UML selectively.** UML 2.5.1 remains the current formal UML version in the OMG catalogue as checked on 2026-09-06 [5]. It defines an abstract syntax and semantics spanning classes, components, composite structures, packages, deployments, interactions, activities, state machines, use cases, and other model kinds.

Select the smallest subset that answers the concern. Class and package diagrams can describe static type and namespace structure. Component and composite-structure models can describe provided/required interfaces, ports, parts, and connectors. Sequence diagrams foreground ordered interaction. State machines foreground states and transitions. Deployment diagrams foreground nodes, artifacts, and communication paths.

Do not mix constructs casually. A class, component, object, lifeline, node, and actor have different semantics even when tools render them as rectangles. If using a UML profile or stereotype, define its base metaclass, properties, constraints, and visible notation. Guillemets around an invented word do not create rigorous semantics.

**Distinguish conforming UML from UML-inspired notation.** A team may borrow the stick actor, package tab, or component icon while using local meanings. That can be effective, but label it as informal or UML-inspired and provide a legend. Claim UML conformance only when the model obeys the selected UML semantics and constraints.

Partial use is normal: a valid class diagram does not need every UML feature. Record the selected subset and modeling conventions. Review model data when semantic conformance matters, because a static image may not reveal whether a tool element is actually typed as shown.

**Make informal diagrams rigorous enough.** Informal does not mean arbitrary. Define a small vocabulary such as person, external system, internal capability, runtime component, data authority, and deployed node. Define relation types such as invokes, publishes, subscribes, reads-authoritatively, replicates, deploys-to, and administers.

Use one visual encoding per type within a diagram. If relation semantics differ, use labels or distinct defined styles. Avoid “talks to,” which hides initiation, protocol, data, authority, and failure. A local notation can be easier to teach than UML and more tailored than C4, at the cost of maintaining definitions and tool support.

**Control abstraction.** A diagram level defines which kinds of elements may appear. Context should not contain private classes. A source-module view should not place a cloud region as a package. A deployment view may map runtime instances to nodes but should not imply their source imports.

Sometimes cross-level information is the concern. Then make the mapping explicit: for example, a deployment projection can show a runtime instance realizing `Order API` and running artifact digest `d7` on node `n3`. Use distinct typed relations rather than an unlabeled mixture.

**Treat containment carefully.** Nesting can mean ownership, composition, deployment, namespace, trust, geography, or visual grouping. Define it. A component drawn inside a team boundary might be read as organizational ownership when the intent was source packaging.

Containment is not automatically transitive across meanings. A process inside a virtual machine inside a region does not mean the source module is owned by the region. If nested boundaries use different dimensions, label every boundary type.

**Give relationships first-class semantics.** Name source and target types, direction, verb, cardinality or multiplicity, protocol or mechanism, and important quality obligations. A bidirectional arrow often hides two different relationships. Draw or label them separately.

Line crossing, closeness, left-to-right order, and vertical placement should carry no meaning unless defined. Layout should improve reading: stable flow direction, limited crossings, aligned peer levels, and proximity for visual grouping. But never make physical distance the sole encoding of latency, coupling, or trust.

**Show static and dynamic claims separately.** A static relation says a caller may invoke a service. A dynamic view shows one scenario order. One observed trace shows one execution. Do not number static arrows to smuggle a single sequence into topology without alternatives, concurrency, or failure.

C4 dynamic diagrams, UML interactions, message-sequence charts, or an informal event table can all express scenarios. Preserve the underlying event semantics from SARCH-024: send versus receive, guards, identity, timeout ambiguity, and permitted linearizations.

**Show boundaries by concern.** System, ownership, trust, network, deployment, transaction, consistency, and failure boundaries are different. Use distinct labels and styles. A heavy border called “internal” is insufficient if identity, administration, or data crosses it.

For security views, label actor, asset, trust, direction, protocol, authentication, authorization, sensitive data, and administrative control. For availability, expose shared dependencies and failure domains. For data, expose authority and copies. The same base model can produce separate overlays rather than one multicolored puzzle.

**Use layering and zoom without losing identity.** Stable identifiers let an element in a context view correspond to its decomposition in another view. The parent view should state where to zoom. The child should state its parent and scope. Names may become more precise, but mappings must be recorded.

C4 zoom levels offer one convention; hyperlinkable informal views or UML packages can provide others. Avoid visual “drill down” that silently changes the represented system, lifecycle state, or environment.

**Manage diagrams as governed artifacts.** Record source, owners, model version, generated rendering, dependencies, and review date. Diagram-as-code improves reviewable diffs, reuse, automation, and consistent rendering. Structured models can generate multiple views and run constraints.

Text or model source does not ensure clarity. Automatic layout can create crossings, unstable positions, or unreadable density. Generated diagrams can faithfully render a stale or wrong model. Manual edits to generated images disappear on regeneration. Keep authoritative source explicit and review the rendered output as well as its source.

**Check semantic consistency.** Within a diagram, ensure every mark maps through the legend and every relation connects permitted element types. Across diagrams, ensure stable elements retain type and identity, decompositions reconcile, and relationships do not contradict one another without state or scope explanation.

Let $type_M(m)$ be model type and $type_G(g)$ visible type. A notation rule validates $type_G(g)=encode(type_M(\iota(g)))$ for selected conventions. This structural equality does not prove the modeled claim is true; compare with manifests, code, configuration, traces, tests, owners, and decisions.

**Review with the audience.** First ask a representative viewer to explain the diagram without coaching. Note misread scope, types, direction, boundaries, acronyms, and color. Then perform model review: completeness for the concern, semantic consistency, cross-view correspondence, and evidence.

Readability and correctness are independent. A clear diagram can clearly describe the wrong architecture. A correct model can have an unreadable rendering. Track both defect classes and avoid treating aesthetic polish as validation.

## Definitions and Notation

Define a governed diagram

$$
D=(M,G,\iota,L,S,C,V),
$$

where $M=(E_M,R_M,K)$ contains model elements, relationships, and constraints; $G$ contains graphical marks; $\iota:G\rightarrow M$ interprets meaningful marks; $L$ defines visual syntax and notation; $S$ defines scope and abstraction; $C$ contains correspondences; and $V$ identifies version, lifecycle state, and evidence context.

For graphical relation $g_r$ mapped to model relation $r=(e_1,k,e_2)$, the legend must determine source, target, relationship kind $k$, and any encoded properties. If two distinct kinds $k_1,k_2$ use one identical unlabeled glyph in the same context and the viewer cannot recover the kind, the rendering loses a distinction needed by the model.

Define semantic coverage for required concern claims $Q$ as

$$
coverage(D,Q)=\frac{|\{q\in Q: represented_D(q)\}|}{|Q|}
$$

for nonempty $Q$. This checks declared representation, not truth, readability, or adequacy of the concern set.

## Mechanisms, Invariants, or Proof Structure

Use this diagram-semantics mechanism.

1. **Frame:** state audience, concern, decision, entity, scope, abstraction, state, environment, and version.
2. **Select model:** choose elements, relationships, constraints, omissions, and evidence needed for the concern.
3. **Choose language:** select C4 abstraction, bounded UML subset, or defined informal vocabulary.
4. **Define notation:** map types and properties to shapes, lines, arrows, labels, boundaries, color, and layout.
5. **Render:** optimize hierarchy, flow, crossings, density, typography, accessibility, and standalone comprehension.
6. **Link:** preserve stable identity, zoom, decomposition, adjacent views, decisions, definitions, and evidence.
7. **Check locally:** validate every element, relation, mark, legend entry, scope rule, and omitted-detail statement.
8. **Check across views:** reconcile logical, source, runtime, deployment, data, security, and operational claims.
9. **Review with people:** test interpretation with target audiences and model adequacy with domain specialists.
10. **Govern:** version source and rendering, detect drift, record review, and update after material change.

The governing invariants are explicit semantics, bounded abstraction, recoverable relationship meaning, typed boundaries, stable cross-view identity, accessible rendering, governed source, audience-tested interpretation, evidence-backed claims, and no inference from unexplained styling.

Suppose graphical encoding $encode$ is injective over the set of relationship kinds used in a diagram, and labels expose direction and endpoints. Then distinct relation kinds have distinguishable encodings. This prevents that one ambiguity class. It does not prove viewers know the legend, labels are readable, model relations are correct, or the selected kinds are sufficient.

## Alternatives and Trade-Offs

**C4 versus UML.** C4 offers a small, accessible abstraction hierarchy for software structure and zoom. UML offers broader standardized structural and behavioral semantics. C4 may be faster for mixed audiences; UML may support deeper precision and tooling. Either can be misused.

**Standard versus local notation.** Standards provide shared vocabulary, references, and tools but require selection and learning. Local notation can fit a domain and audience closely but needs durable definitions, governance, accessibility, and onboarding.

**One canonical model versus independent drawings.** A structured model improves consistency and generation but can centralize complexity and constrain expression. Independent drawings are flexible and quick but drift easily. Stable identifiers and automated checks can support a hybrid.

**Diagram-as-code versus graphical editing.** Text supports diff, review, automation, and reuse. Graphical tools support direct spatial design and stakeholder participation. Choose an authoritative source and preserve round-trip behavior or explicitly disallow it.

**Rich overlays versus separate views.** Overlays reveal correlations but can overload color and symbols. Separate views clarify one concern but require correspondence. Prefer the smallest view that supports the decision.

**Automatic versus manual layout.** Automatic layout scales and stays reproducible but can be unstable or unreadable. Manual layout improves narrative but costs maintenance and can encode accidental semantics. Review the rendering in both cases.

**Current-state versus historical diagrams.** Current views aid operation; historical versions support decisions and incidents. Version them rather than editing history in place, and label observed versus intended state.

## Failure Modes and Misconceptions

- **The box is self-explanatory.** Its type, responsibility, scope, and identity require definition.
- **An arrow means dependency.** Invocation, data flow, publication, ownership, and deployment differ.
- **Layout is semantics.** Position is presentation unless the notation defines otherwise.
- **Color is universally understood.** Meaning, contrast, printing, and color-vision accessibility need design.
- **C4 container means operating-system container.** It is an architectural application or data-store abstraction.
- **A C4 component is a deployable service.** Deployability and runtime realization require correspondence.
- **UML-looking means UML-conforming.** Borrowed shapes do not import standardized semantics.
- **A stereotype can mean anything.** Govern its base, properties, constraints, and notation.
- **One diagram should show everything.** Mixed concerns and levels destroy interpretability.
- **Generated means current.** Model source and generation triggers can be stale.
- **Diagram-as-code guarantees readable output.** Rendering still needs visual and audience review.
- **Standard notation proves architecture quality.** It improves expression, not truth or fitness.
- **No contradiction means complete.** Important external, failure, security, or operational facts may be absent.

## Worked Examples

### Example 1

**Situation.** `Payments` connects to `Ledger` with an unlabeled dashed arrow.

**Reasoning.** The elements lack types and the line lacks direction and semantics. Declare a container view, type `Payment API` as application and `Ledger` as external system/data authority, label `submits posting command over mutually authenticated protocol`, and define dashed as asynchronous command. Link to failure semantics.

**Conclusion.** Names and lines alone do not create an interpretable architecture claim.

### Example 2

**Situation.** A C4 container diagram draws three Kubernetes pods as three containers.

**Reasoning.** Pods are deployment instances, while the C4 container is the runnable application abstraction. Show one `Order API` C4 container, then map its replica instances to pods in a deployment view. If pods host different applications, model those separately for that reason—not because they are pods.

**Conclusion.** Keep C4 abstraction separate from platform container terminology.

### Example 3

**Situation.** A “UML component diagram” uses class rectangles, database cylinders, and arrows whose direction alternates between call and dependency.

**Reasoning.** Either construct a conforming selected UML model with components, interfaces, ports, and dependencies, or label the view UML-inspired and define local types. Split call direction from source dependency. The cylinder is not a UML semantic escape hatch; type the data authority explicitly.

**Conclusion.** Honest informal notation is better than falsely precise UML styling.

### Example 4

**Situation.** Blue means internal ownership, except two blue boxes mean healthy instances.

**Reasoning.** One encoding maps to incompatible properties, so interpretation is ambiguous. Use boundary or owner label for ownership and a separate status badge for observed health, with timestamp and source. Ensure meaning survives monochrome rendering.

**Conclusion.** One visual channel should not carry conflicting semantics in one context.

### Example 5

**Situation.** A context diagram includes customer, system, database tables, source classes, and cloud zones.

**Reasoning.** The picture mixes external interaction, physical schema, code, and deployment. Keep people, focal system, and external systems in context; link to data, code, and deployment views with stable identifiers. Add a small cross-view mapping only where a stakeholder question requires it.

**Conclusion.** Separate model kinds and connect them instead of collapsing abstraction.

### Example 6

**Situation.** Two boxes are close together to indicate low latency, but a renderer moves them apart.

**Reasoning.** Proximity was an undocumented semantic channel and automatic layout destroyed it. Express the latency budget as a relationship property or annotation. Use proximity only as presentation, or define a scaled quantitative notation with units and limitations.

**Conclusion.** Consequential claims need explicit labels or governed encodings, not accidental geometry.

### Example 7

**Situation.** A static view numbers calls 1–8 and omits timeout and concurrent paths.

**Reasoning.** The numbering presents one happy scenario as topology. Retain static allowed relationships in one view; create a dynamic view with sends, receives, guards, concurrency, timeout, identity, and outcomes. Link both to the same component identifiers.

**Conclusion.** Static possibility and dynamic execution are different claims.

### Example 8

**Situation.** A generated diagram adds a new service automatically but omits its administrative dependency.

**Reasoning.** The generator queries runtime traffic, so dormant and control paths are outside its evidence. Label the view as observed traffic for a window, show unknown coverage, and merge governed configuration or manual model data for administration. Do not present discovery as a complete architecture.

**Conclusion.** Generated views inherit the evidence limits of their sources.

### Example 9

**Situation.** A security review sees a heavy boundary around “platform” but no legend.

**Reasoning.** Determine whether it means ownership, network, identity, or trust. Replace it with separately labeled boundaries and show administrative crossings, workload identity, sensitive data, and external authority. A single region can contain several trust zones; one trust authority can span regions.

**Conclusion.** Boundaries must name the concern they partition.

### Example 10

**Situation.** An emergency-response map combines dispatch software, radio towers, hospitals, field teams, and weather feeds.

**Reasoning.** Use a system-context view for actors and external systems, a deployment view for radio and site failure domains, a dynamic view for dispatch acknowledgment, and an information view for incident authority and location quality. Stable identifiers connect them. Test printed, low-bandwidth, and color-deficient use with dispatchers and field staff.

**Conclusion.** High-consequence communication benefits from several reconciled, audience-tested views rather than one overloaded map.

## Cross-Program Connections

- **Systems Engineering:** SysML and assurance views extend notation to physical, behavioral, requirement, and hazard concerns.
- **Modeling and Metaprogramming:** metamodels, transformations, validation, and code generation formalize model semantics.
- **Software Engineering Methods:** stakeholder collaboration, traceability, reviews, and change governance shape diagram use.
- **Human-Computer Interaction:** perception, accessibility, cognitive load, labeling, and audience testing shape rendering.
- **Compiler Engineering:** parsing, abstract syntax, semantic analysis, and transformations provide analogies for modeling languages.
- **Security:** trust boundaries, assets, actors, data flows, and threats require precise visual semantics.
- **Platform and Cloud Engineering:** runtime discovery and infrastructure models can generate deployment views with explicit evidence limits.
- **Testing and Quality Engineering:** model validation, consistency checks, mutation, and review protocols provide evidence.

## References

1. ISO/IEC/IEEE, *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*, 2nd ed., November 2022. Official catalogue; current edition checked 2026-09-06. https://www.iso.org/standard/74393.html
2. Simon Brown, “Abstractions,” *C4 model*. Retrieved 2026-09-06. https://c4model.com/abstractions
3. Simon Brown, “Diagrams,” *C4 model*. Retrieved 2026-09-06. https://c4model.com/diagrams
4. Simon Brown, “Notation,” *C4 model*. Retrieved 2026-09-06. https://c4model.com/diagrams/notation
5. Object Management Group, *OMG Unified Modeling Language (OMG UML), Version 2.5.1*, formal/2017-12-05, December 2017. Official specification and current formal version checked 2026-09-06. https://www.omg.org/spec/UML/2.5.1/PDF
6. Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010.
7. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
8. Edward Tufte, *The Visual Display of Quantitative Information*, 2nd ed., Graphics Press, 2001.

## Exercises

### Exercise 1

Precisely distinguish model, diagram, syntax, semantics, notation, legend, abstraction level, model kind, viewpoint, and correspondence. Explain why a rendered image is not necessarily the authoritative model.

### Exercise 2

A review requires eight claims. One diagram represents six, of which one is encoded only by unexplained color. Compute declared coverage before and after excluding the ambiguous claim. Explain what neither number proves.

### Exercise 3

Diagnose a diagram containing a C4 container called `Order Service`, a UML class inside it, two cloud zones around it, and a numbered arrow to a database. Produce a coherent set of replacement views.

### Exercise 4

Compare C4, a selected UML subset, and locally defined informal notation for a team documenting a distributed medical appointment system. Address audience, semantics, dynamics, deployment, accessibility, tooling, and governance.

### Exercise 5

Transfer the method to a wildfire command system. Design an audience-tested architecture-description map for public callers, dispatchers, aircraft, ground crews, sensors, weather providers, regional control centers, and degraded communications.

## Answers to the Exercises

### Answer 1

A **model** is a purposeful abstraction; a **diagram** visually renders a model or fragment. **Syntax** defines permitted constructs; **semantics** defines their meaning; **notation** maps them to marks; a **legend** explains those marks. An **abstraction level** bounds element kinds and detail. A **model kind** establishes conventions for one type of model. A **viewpoint** frames concerns, stakeholders, model kinds, and conventions. A **correspondence** relates claims or elements across models and evidence.

An image may omit machine-readable type, hidden properties, constraints, identifiers, provenance, and source history. It can also be manually edited or stale. The authoritative artifact must be declared: structured model, text source, or controlled drawing. The rendered image remains a required communication output and must be reviewed separately.

### Answer 2

Naive declared coverage is $6/8=75\%$. If the unexplained color does not permit a viewer to recover its claim, represented coverage is $5/8=62.5\%$. The difference exposes one notation defect.

Neither percentage proves the six or five claims are true, readable, sufficient, current, or relevant. The required set of eight may itself be incomplete. Coverage is only a bookkeeping measure over a declared concern set; model, audience, correspondence, and evidence reviews remain necessary.

### Answer 3

The diagram mixes C4 application abstraction, UML code type, deployment topology, dynamic order, and data interaction. Replace it with: a C4 container view showing `Order Service` as a typed application and the database as a typed data store with a labeled allowed relationship; a component or module/code view showing the responsibility implemented by the class; a deployment view mapping service instances and database nodes to the two zones; and a runtime interaction view showing the numbered scenario, send/receive events, failure, and timeout.

Give stable identifiers to the order application, responsibility, runtime instances, artifact, nodes, and data authority, then record correspondences. If UML is used for the code view, select and follow class or component semantics. Do not nest a UML class merely because it is implemented “inside” the application. Label zone and data-authority boundaries by concern.

### Answer 4

C4 is strong for mixed clinical, product, and engineering audiences who need context and application-level zoom. Its small vocabulary is teachable, but dynamic, state, data, and safety detail needs supporting views and explicit local conventions. Clarify that container does not mean a platform container.

A selected UML subset supports precise components, interfaces, interactions, states, and deployments, with mature tools and standards. It requires training and disciplined subset/profile governance; full notation can overwhelm non-specialists. Informal notation can use domain types such as patient, clinician, scheduling authority, identity service, clinic system, notification channel, and audit authority. It is accessible when relationships and boundaries are explicitly defined, but the team owns the semantics and validators.

A practical description may use C4 for navigation, bounded UML state/sequence models for appointment lifecycle and concurrency, and simple annotated views for clinical and support reviews. Maintain stable identities and correspondences. Test screen, print, grayscale, keyboard-linked navigation, terminology, and comprehension with actual audiences. Tool choice does not replace privacy, safety, failure, and conformance evidence.

### Answer 5

Create a public context view showing callers, emergency services, the command system, weather and mapping providers, and jurisdictional neighbors. Create an operational capability view for dispatcher intake, verification, prioritization, resource assignment, acknowledgment, evacuation warning, and public communication. Type every actor and authority; label information and command direction.

Use a deployment view for regional centers, radio towers, satellite and terrestrial links, aircraft terminals, field devices, sensors, power, and failure domains. Use dynamic views for dispatch, lost acknowledgment, conflicting observation, aircraft reassignment, and degraded communications. Use an information view for incident identity, location reference, observation time, confidence, source, correction, command authority, sensitive caller data, and public alert state.

Connect all views with stable identifiers and state/environment labels. Legends distinguish system, organization, device, data authority, command, observation, and backup path. Do not use color alone; produce printable low-detail field versions and interactive drill-down versions. Test interpretation with dispatchers, pilots, ground leads, accessibility users, and incident commanders. Validate known paths against configuration and exercises while labeling discovered runtime traffic and drill evidence as time-bounded rather than complete.
