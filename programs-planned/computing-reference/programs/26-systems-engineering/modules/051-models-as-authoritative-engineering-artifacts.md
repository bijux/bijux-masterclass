---
module_id: SYSENG-051
program: Systems Engineering
level: 2
module_number: 51
title: Models as Authoritative Engineering Artifacts
status: complete
last_verified: 2026-08-31
---

# Models as Authoritative Engineering Artifacts

## One-Page Review

### Governing question

What governance, semantics, configuration, evidence and access make a model authoritative for a stated engineering claim and use—without falsely treating one tool, repository, diagram or simulation as universally true?

### Essential definitions

- A **model** is a purposeful representation of selected system concepts and relationships under declared abstractions, semantics and assumptions.
- A **model element** is an addressable semantic object such as a requirement, function, state, interface, component, measure, verification case or relationship; its diagram symbol is a view of that object.
- A **view** presents model content for stakeholder concerns using declared selection, transformation and rendering rules. A view may be generated, manually curated or external.
- An **engineering claim** is a proposition used for design, analysis, decision, implementation, verification, operation or assurance, such as “IF-041 owns the telemetry schema in baseline B3.”
- An **authoritative source** is the governed source designated to answer a defined class of claims for a defined scope, baseline and use. Authority is assigned, not inferred from file location or tool popularity.
- An **authoritative source of truth** is a governed set of current and historical models/data with defined ownership, configuration, access, semantics and resolution rules. It may be federated; “truth” does not mean infallibility.
- An **authority map/register** resolves each governed claim class or element to exactly one controlling source/version at a baseline, plus stewards and conflict/escalation rules.
- A **technical baseline** is an approved configuration of model/data content at a lifecycle point. A working branch, latest save or live dashboard is not automatically a baseline.
- **Provenance** records origin, authorship, method, source inputs, transformations, timestamps, tool/schema versions and custody sufficient to interpret and reproduce content.
- **Semantic consistency** means linked concepts preserve compatible identity, meaning, units, cardinality, direction, state, time and configuration across sources.
- **Model credibility** is evidence-based confidence that a model is adequate for a specified intended use; it is not a global property of the file.
- A **derived artifact** is generated from authoritative content by a controlled transformation. Its freshness and traceability can be checked; it is authoritative only if explicitly designated.
- **Digital thread** is the governed trace of identities, relationships, transformations and configurations across lifecycle information—not merely a set of hyperlinks.
- A **model debt** is a known gap in semantic quality, automation, evidence, configuration, usability or maintainability that increases future engineering risk.

### Central model, mechanism, or theorem

Represent an authority assignment for claim $q$ in baseline $b$ and intended use $u$ as

$$
\mathcal{A}(q,b,u)=(s,v,o,p,c),
$$

where $s$ is the controlling source, $v$ its exact version/configuration, $o$ accountable owner/steward, $p$ applicable policy and $c$ conflict/change procedure. A well-governed baseline requires one resolvable authority for each governed claim:

$$
|\operatorname{resolve}(q,b,u)|=1.
$$

This uniqueness does not require one physical database. A federated authoritative set can include requirements, system, discipline-analysis, interface, verification, risk and configuration sources, provided identities and transformations are controlled. Credibility is use-specific:

$$
Credible(M,u,E)\not\Rightarrow Credible(M,u',E').
$$

### Critical invariants

- Every authoritative claim has a stable identity, defined semantic meaning, scope, baseline, intended uses, controlling source/version and accountable owner.
- Authority is granular and explicit; a repository cannot silently claim all requirements, behavior, geometry, analysis, risk, verification and as-operated facts.
- Source models, derived views, exports, reports, caches and copies are distinguishable, and precedence is defined when they disagree.
- Model structure, schema/metamodel, units, identifiers, naming, relationship semantics and validation rules are governed and versioned.
- Changes follow authorization, review, impact analysis, configuration control, audit history and downstream propagation appropriate to consequence.
- Links are semantic and traversable, not untyped URLs; broken, ambiguous, cyclic and cross-baseline relationships are detected.
- Model claims expose assumptions, abstractions, applicability, evidence, uncertainty and credibility for intended use.
- Verification of model implementation, validation against reality or stakeholder need, and accreditation/acceptance for a use remain distinct.
- Human-readable views are available for relevant concerns, but no view silently edits or outranks its source.
- Access is sufficient for decision and review while protecting security, privacy, export, proprietary and safety-sensitive content.
- Tool, vendor, schema and organization boundaries have exchange, retention, migration and exit strategies.
- The authoritative set includes current and historical baselines; “latest” never erases the record of what supported a prior decision or build.
- Deployed/as-built/as-operated evidence reconciles with design intent through governed updates rather than optimistic synchronization claims.
- Automation reports its scope and failure; a green structural check does not establish semantic correctness or real-world validity.

### Common failures

Common failures include calling the largest repository the single source of truth; declaring every model authoritative; treating diagrams as models; confusing the latest edit with an approved baseline; allowing duplicate IDs or multiple controlling requirements; exporting PDFs and then editing them; copying interface values into local models without ownership; linking by filename rather than identity/configuration; trusting automatic synchronization without conflict policy; generating code from unreviewed models; accepting simulations outside validated domains; hiding assumptions in tool properties; measuring model quality by element count; requiring a specialist tool to see a decision; losing supplier semantics behind proprietary formats; giving broad write access to solve collaboration; prohibiting all writes and creating shadow models; ignoring operational evidence; migrating tools without semantic reconciliation; and deleting old baselines after a model is “cleaned up.”

### Compact example

Baseline B3 assigns requirements R-12 and R-18 to a requirements source, functions and blocks to a system model, verification V-9 to a verification source, and risk RK-3 to a risk register. Stable IDs create five controlled cross-source links. Three stakeholder views are generated; an interface matrix is detected as stale because it predates its source revision. The stale export is not used for integration. A change to IF-4 proceeds through its owning system source, impact analysis, approval and regeneration; local copies do not become competing authorities.

### Connections

SYSENG-001–050 supply the system definitions, requirements, architecture, interfaces, verification, risk and decision content that models represent. SYSENG-052–060 deepen specific model types and integration. Later Level II work depends on authoritative identity, baseline, evidence and change semantics; without them, model-based engineering becomes diagram-based inconsistency.

## Governing Question

For each consequential statement being used now, can a competent engineer determine what it means, which configured source controls it, who may change it, what evidence supports it, which downstream artifacts depend on it, and whether the representation is credible for this exact decision or operation?

If the answer is “open the modeling tool and ask the expert,” the organization has a model but not an authoritative engineering capability. Authority is a socio-technical contract implemented through semantics, repositories, access, configuration, review and accountability.

## Why This Matters

Model-based work can replace disconnected documents with linked engineering knowledge, but it can also centralize ambiguity. A wrong requirement copied into five diagrams looks consistent; an obsolete export appears polished; a simulation result acquires false authority when its intended-use limits disappear; and a vendor repository can become operationally indispensable without usable exchange or retention.

NASA-HDBK-1009A, active in 2025, integrates system modeling with NASA systems-engineering processes and covers model planning, organization, metamodel, construction, and generation of diagrams/tables for defined work products. NASA configuration management requires product and product information to remain consistent across controlled baselines, while technical data management governs identification, access, protection, exchange, retention and future use. NASA-STD-7009B makes model/simulation credibility and intended-use acceptance explicit.

DoDI 5000.97 directs programs to maintain configured digital models through the lifecycle, update them with relevant real-world data, and establish current, consistent, enduring authoritative sources. The earlier DoD Digital Engineering Strategy describes an authoritative source as the current and historical technical baseline connected across models/data. Neither source promises a magic database. SysML 2.0 supplies current language and API foundations for semantic modeling and interchange; standards improve exchange only when projects govern profiles, identity, versions and meaning.

## Prerequisites and Retrieval

Before declaring model authority, retrieve:

1. system boundary, lifecycle, product/configuration hierarchy, ConOps, stakeholder concerns, reviews, decisions and technical baselines;
2. model-management plan, information architecture, data/model inventory, owners/stewards, authority and precedence register, RACI, review/change rules and access classifications;
3. modeling purposes and intended uses, languages, profiles/metamodels, schemas, ontologies, units, identifier/naming rules, style and validation constraints;
4. repositories, branches/workspaces, baselines/releases, tool/plugin/API versions, generated artifacts, transformations, CI checks, backups and audit logs;
5. requirements, functions, behavior, interfaces, architecture, geometry, discipline analyses, verification, hazards/risks, cost/schedule and operations sources with cross-links;
6. V&V, credibility, uncertainty, calibration, test/field/operational evidence, assumptions, applicability limits and acceptance authorities;
7. contracts, supplier deliverables, intellectual-property and export/security/privacy controls, exchange formats, tool licenses, retention and exit/migration plans;
8. known inconsistencies, stale views, duplicates, unresolved ownership, manual transcriptions, model debt and prior incidents.

Use a retrieval test: a diagram says interface voltage is 28 V, a spreadsheet says 24–32 V and a supplier model says 30 V nominal. Ask which claim each value makes, which configured interface definition controls it, which requirement/tolerance and operating mode apply, when each artifact was produced, what transformation created it, and who resolves conflict. Opening the newest file is not governance.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish model, model element, view, export, analysis result and physical/operational evidence;
2. define authority at claim, scope, baseline and intended-use granularity;
3. design a federated authoritative-source architecture with explicit precedence and ownership;
4. govern stable identity, semantics, metamodels, units, relationships and cross-model configuration;
5. separate working changes from approved technical baselines and preserve history;
6. define provenance, transformation and freshness for derived artifacts;
7. establish intended-use credibility through verification, validation, uncertainty and acceptance evidence;
8. control access, collaboration, review, change, impact and downstream propagation;
9. evaluate interoperability, contracts, proprietary formats, retention and migration risk;
10. audit authoritative models for conflicts, stale content, broken links, shadow sources and outcome divergence.

## Core Exposition

**Begin with claims and uses.** Do not begin by selecting a tool. Inventory consequential questions: which requirement is approved, which component owns a function, which interface contract applies, which analysis supports margin, which verification result closes an obligation, and which deployed configuration operates. Classify who uses each answer and for what decision. Authority can then be designed around knowledge, not repository boundaries.

**Define the system and information boundary.** State lifecycle, product levels, variants, suppliers, enabling systems and operational configurations. A vehicle system model may not control manufacturing geometry; a product-lifecycle source may not control operational hazard status. Define external authoritative systems and what links cross the boundary.

**Assign granular authority.** Create a register keyed by stable claim class or element identity, baseline and use. Name source, version-resolution rule, owner/steward, approver, permitted editors, review cadence, conflict path and retention. Require one controlling source for each governed claim at a baseline, while permitting many nonauthoritative analyses and views.

**Prefer federation over false monoliths.** Requirements, architecture, CAD, analysis, verification and operations often need different semantics and specialist tools. Integrate them through stable identities, controlled mappings, APIs/exchanges, configurations and governance. Centralize only where the semantic and operational case supports it. Federation is not permission for duplicate authority.

**Govern the metamodel.** Define element and relationship types, required properties, cardinalities, units, state/mode/time semantics, inheritance, allowed cycles and constraints. Version profiles and libraries. Test migrations against representative models. A syntactically valid file can still express the wrong domain meaning.

**Use stable identity independent of display.** A human-readable name can change; a stable ID supports traceability. Define uniqueness scope, namespaces, version/configuration semantics, tombstones and rules for clone/split/merge. Never reuse a retired identifier for a different concept. Distinguish identity of a concept from identity of a revision.

**Separate model from view.** Diagrams, tables, documents, dashboards and review slides select and render model content. Record source queries, transformations, source baseline, generator/tool version and time. Make generated content visibly read-only or round-trip governed. If a view can edit source, define write semantics and conflict control explicitly.

**Control working and approved states.** Branches/workspaces enable exploration; baselines authorize use. Define proposed, reviewed, approved, released, superseded and retired states with transition authority. Tag exact model, libraries, profiles, external references and transformations. A review must know which immutable configuration it reviewed.

**Preserve provenance.** For imported or computed content, record source, author/system, acquisition time, method, configuration, unit transformations, calibration, uncertainty, assumptions and license. Trace a displayed value backward to evidence and forward to decisions and implementations. Provenance is not merely a creation timestamp.

**Make cross-model links semantic.** State relationship type, endpoint identity, direction, baseline compatibility and ownership. A requirement satisfied by a block differs from a test verifying it; a risk affecting an interface differs from an analysis assuming it. Validate endpoint existence, allowed types, cardinality and configuration. Detect orphan, ambiguous and cyclic structures where prohibited.

**Define precedence and conflict resolution.** When sources disagree, do not let last-write-wins choose engineering truth. Identify which claim each source controls, block unsafe propagation, notify owners, preserve both observations, assess impact and authorize resolution. Record temporary deviations and downstream exposure. Automated merges need domain-aware rules or human review.

**Treat authority as responsibility.** Owners must maintain semantics, access, review, freshness and response time. Authority without resources creates stale bottlenecks; unrestricted collaboration creates silent corruption. Use least privilege, protected baselines, proposed changes, review workflows and emergency rules. Audit privileged actions.

**Define model quality by use.** Useful checks include required fields, uniqueness, well-formed relationships, completeness against scope, consistency, trace coverage, unit/dimensional validity, unreachable states, interface compatibility and stale evidence. Element count, diagram count or zero validation warnings alone does not establish usefulness.

**Establish credibility for analyses.** For behavioral, performance, safety or physics models, state intended use and decision consequence; document conceptual model, assumptions, input data, code/tool/configuration, verification, validation, calibration, uncertainty/sensitivity, domain of validity, peer/independent review and acceptance. Evidence sufficient for concept screening may not support certification or operational control.

**Keep model truth and world truth distinct.** An internally consistent model expresses the approved understanding; the system can still differ. Reconcile as-built, as-tested and as-operated observations through configuration/status accounting and governed changes. Never auto-update design intent from telemetry without authority and interpretation.

**Automate bounded checks.** CI can parse, validate schemas, execute constraints, detect duplicates/broken links, compare baselines, regenerate views and run analysis cases. Pin toolchains and capture logs. Fail closed for material errors, but define exception/waiver flow. A passed job proves only the declared checks on the declared inputs.

**Make reviews model-capable.** Provide concern-oriented views, navigation, change sets, source/evidence drill-down and accessible exports. Freeze review baseline and record comments/decisions against stable elements. Do not require every stakeholder to master a proprietary notation; translate without losing traceability.

**Manage derived products.** Generate specifications, interface matrices, test plans, bills, code/configuration or dashboards only through controlled transformations. Label source baseline and freshness. Compare generated output, prohibit untracked manual edits, and test generators. If a document must be contractually authoritative, declare precedence and round-trip obligations.

**Integrate suppliers and contracts.** Specify deliverable content, semantics, identifiers, versions, native and neutral formats, APIs, validation, pedigree, rights, protection, acceptance, updates and exit. A PDF satisfies visualization, not necessarily reuse or traceability. Validate imports; do not assume a standard exchange preserves every tool-specific meaning.

**Protect sensitive knowledge.** Classify elements and views, enforce attribute/role-based access, segment exploit details, encrypt, audit and retain. Provide decision-capable summaries. Avoid both uncontrolled replication and overrestriction that forces shadow sources. Include privacy, export, proprietary and records obligations.

**Plan tool and semantic migration.** Inventory dependencies, profiles, scripts, APIs, licenses and skills. Export canonical/neutral forms where adequate; archive readers and environments when necessary. Reconcile element counts, identity, semantics, relationships, units, diagrams, behavior and checks—not just successful file import. Preserve old baselines and migration evidence.

**Operate and retire the authoritative set.** Monitor freshness, conflicts, link health, access, usage, generator failures, model debt and divergence from deployed evidence. During retirement, retain decision/build/safety records under policy, preserve interpretable formats and ownership, revoke unnecessary access and document successor sources. A tool shutdown is not information retirement.

The following checker audits a declared authority registry and generated views. It demonstrates unique authority and detects one stale derived view. It cannot determine whether the six claims are correct, the owners legitimate or the models credible for real engineering use.

<!-- bijux-verify: {"id":"authoritative-model-registry-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"registered_claims=6\nauthoritative_sources=4\nunique_authority=1\nbaselined_claims=6\ncross_source_links=5\nbroken_links=0\nderived_views=3\nstale_views=1\nstale_view_ids=interface-matrix\nstatus=authority_registry_consistent\nevidence=declared_registry_only\n","stderr":""}} -->
```python
registry = {
    "R-12": ("requirements", "B3", 7),
    "R-18": ("requirements", "B3", 7),
    "F-07": ("system-model", "B3", 11),
    "IF-04": ("system-model", "B3", 11),
    "V-09": ("verification", "B3", 5),
    "RK-03": ("risk-register", "B3", 8),
}
links = [("R-12", "F-07"), ("F-07", "IF-04"), ("R-18", "IF-04"),
         ("V-09", "R-12"), ("RK-03", "IF-04")]
views = {
    "requirements-table": ("requirements", 7, 7),
    "interface-matrix": ("system-model", 11, 10),
    "verification-matrix": ("verification", 5, 5),
}

sources = {source for source, _, _ in registry.values()}
unique = len(registry) == len(set(registry))
baselined = sum(baseline == "B3" for _, baseline, _ in registry.values())
broken = sum(left not in registry or right not in registry for left, right in links)
stale = [name for name, (_, source_revision, generated_revision) in views.items()
         if source_revision != generated_revision]

print(f"registered_claims={len(registry)}")
print(f"authoritative_sources={len(sources)}")
print(f"unique_authority={int(unique)}")
print(f"baselined_claims={baselined}")
print(f"cross_source_links={len(links)}")
print(f"broken_links={broken}")
print(f"derived_views={len(views)}")
print(f"stale_views={len(stale)}")
print("stale_view_ids=" + ",".join(stale))
consistent = unique and baselined == len(registry) and broken == 0
print("status=" + ("authority_registry_consistent" if consistent else
                   "authority_registry_needs_work"))
print("evidence=declared_registry_only")
```

The registry passes while one view is stale because derived-view detection is working. Passing does not authorize use of that stale matrix; the workflow must regenerate it or explicitly control an exception before integration.

## Definitions and Notation

Let model artifact

$$
M=(id,purpose,scope,semantics,content,provenance,configuration,owner,history).
$$

Let $Claims(M)$ be propositions expressed or computed by $M$, and $Use(M)$ its declared intended uses. Authority relation $controls(s,q,b,u)$ means source $s$ governs claim $q$ for baseline $b$ and use $u$; it does not imply that every claim in $s$ is validated.

A derived artifact $d=T(M_b)$ records transformation $T$, source baseline $b$, tool/environment and digest. Freshness requires its recorded source revision to equal the governed source revision or to satisfy an explicit compatibility policy.

Model-to-reality discrepancy for observable $y$ is

$$
e=y_{observed}-y_{predicted},
$$

interpreted only with measurement uncertainty, configuration alignment and applicability. A discrepancy can indicate model error, implementation deviation, measurement error or an unmodeled condition.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—authority design.** Inventory claims/uses and assign controlling sources, baselines, owners, access, precedence and conflict handling.

**Mechanism 2—semantic/configuration control.** Govern identity, metamodels, units, links, profiles, working states, approved baselines and history.

**Mechanism 3—credibility and evidence.** Preserve provenance, assumptions, intended use, V&V, uncertainty, validation, operational reconciliation and acceptance.

**Mechanism 4—delivery and collaboration.** Control views, transformations, reviews, suppliers, access, automation, interoperability and migration.

**Mechanism 5—lifecycle assurance.** Audit freshness, conflicts, broken links, shadow sources, model debt, world divergence, retention and successor authority.

The structure guarantees neither truth nor correctness. It makes authority and evidence inspectable so errors, limits and disagreements can be found and governed.

## Alternatives and Trade-Offs

**One repository** simplifies discovery and access but can force weak semantics and create operational concentration. **Federation** preserves domain tools but increases identity, link and configuration burden. Choose deliberately and retain one authority per governed claim.

**Native rich formats** preserve tool semantics. **Open/neutral exchanges** improve longevity and supplier independence but may lose behavior, layout or extensions. Validate semantic round trips and archive necessary environments.

**Live models** support continuous visibility. **Released baselines** support stable decisions, contracts and audits. Use both with explicit status; never make “latest” stand for “approved.”

**Automated synchronization** reduces transcription and latency. **Controlled manual reconciliation** handles ambiguous meaning. Automate only deterministic mappings with observable failures and conflict quarantine.

**Fine-grained access** protects sensitive elements but complicates views and links. **Broad access** aids collaboration but expands exposure. Tailor access to claim, role and use while preventing shadow copies.

**Executable/generative models** can detect errors and produce consistent artifacts. They also amplify defects. Pin, review, test, qualify where needed and retain generated evidence.

## Failure Modes and Misconceptions

**“Authoritative means correct.”** It identifies the controlling answer; the answer remains challengeable and correctable through governance.

**“Single source means single tool.”** Authority can be federated. A monolith can still contain contradictions and stale data.

**“The model is the diagram.”** Diagrams are concern-oriented views; semantics live in governed elements and relationships.

**“All linked data are synchronized.”** Links can cross incompatible versions, units and meanings. Validate configurations and transformations.

**“Generated means trustworthy.”** A deterministic generator faithfully amplifies wrong source content or code.

**“V&V makes a model universally valid.”** Credibility is for stated use, domain, evidence and consequence.

**“More detail is higher maturity.”** Unjustified detail can conceal uncertainty and increase maintenance burden.

**“Write access creates collaboration.”** Collaboration needs proposal, review, ownership and conflict handling, not uncontrolled mutation.

**“Neutral export eliminates lock-in.”** Exchange may omit extensions, behavior, layout, APIs and history; prove the migration.

**“Operations should match the model.”** Reconcile both directions: the product may deviate, or the approved model may be wrong or obsolete.

## Worked Examples

### Example 1

**Contradictory interface values.** The interface model controls voltage range; a generated specification is stale and a supplier analysis controls only nominal input. Integration stops until the view regenerates and supplier evidence is assessed against the controlled range.

### Example 2

**Federated authority.** Requirements, architecture, CAD, verification and risk sources retain domain ownership. Stable IDs and a baseline manifest assemble a review configuration without copying every claim into one database.

### Example 3

**Diagram edit.** A reviewer annotates a PDF block diagram. The comment becomes a proposed change linked to the element; it does not silently change allocation or create a competing model.

### Example 4

**Duplicate requirement.** Two repositories claim R-204. The authority register identifies the controlled source; change processing retires or maps the shadow ID and assesses every downstream link before reuse.

### Example 5

**Simulation reuse.** A thermal model validated for vacuum steady state is proposed for transient atmospheric operation. Prior credibility does not transfer; intended use, physics, boundary conditions, evidence and uncertainty are reassessed.

### Example 6

**Generated configuration.** A deployment model produces infrastructure code. Source, generator and libraries are baselined; structural, security and representative environment tests precede release. Generation is traceable, not self-approving.

### Example 7

**Supplier black box.** A supplier supplies plots but no usable model or uncertainty. The contract is corrected to require intended use, inputs/outputs, versions, pedigree, validation and exchange/rights sufficient for independent lifecycle decisions.

### Example 8

**Unauthorized direct edit.** An engineer changes a baselined mass property to make a margin pass. Audit detects it; the baseline is restored, impact assessed, evidence corrected and change reviewed. A correct new value still needs authorized provenance.

### Example 9

**Operational divergence.** Telemetry shows higher power than the design model. The team aligns configuration and measurement uncertainty, investigates implementation/environment/model causes, and updates authority only after disposition—not by auto-importing an average.

### Example 10

**Tool retirement.** A program exports neutral model content, archives native baselines/readers, tests identity/relationship/unit/behavior parity, updates authority mappings and retains prior decision configurations. “Import succeeded” is not migration acceptance.

## Cross-Program Connections

**Platform engineering.** Service catalogs, templates, policies and runtime inventories form federated authoritative sources; desired state and observed state require explicit reconciliation.

**API and service engineering.** Schemas, interface contracts, behavior models and deployed endpoints need stable versions, ownership, generated-artifact rules and compatibility evidence.

**Data engineering.** Catalogs, schemas, lineage, transformations and quality rules embody authority and provenance; replicated tables must not become silent masters.

**Object-oriented programming.** Code, class models and generated sources require clear precedence and round-trip policy; diagrams that drift from implementation lose decision value.

**Functional programming.** Types, algebraic models, specifications and property tests can make semantics executable, but formal conformance remains bounded by modeled assumptions and effects.

## References

1. NASA, *NASA Systems Modeling Handbook for Systems Engineering*, NASA-HDBK-1009A, active 2025. <https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009>
2. NASA, *Systems Engineering Handbook, Section 1.0: Introduction*, current web edition. <https://www.nasa.gov/reference/1-0-introduction/>
3. NASA, *Systems Engineering Handbook, Section 6.5: Configuration Management*, current web edition. <https://www.nasa.gov/reference/6-5-configuration-management/>
4. NASA, *Systems Engineering Handbook, Section 6.6: Technical Data Management*, current web edition. <https://www.nasa.gov/reference/6-6-technical-data-management/>
5. NASA, *Standard for Models and Simulations*, NASA-STD-7009B, active 2024. <https://standards.nasa.gov/standard/nasa/nasa-std-7009>
6. NASA, *NASA Handbook for Models and Simulations*, NASA-HDBK-7009B, active 2026 index. <https://standards.nasa.gov/systems-and-subsystem-test>
7. U.S. Department of Defense, *DoDI 5000.97: Digital Engineering*, 2023. <https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/500097p.PDF>
8. U.S. Department of Defense, *Digital Engineering Strategy*, 2018. <https://ac.cto.mil/wp-content/uploads/2019/06/2018-Digital-Engineering-Strategy_Approved_PrintVersion.pdf>
9. Object Management Group, *Systems Modeling Language Specification Version 2.0*, 2025. <https://www.omg.org/spec/SysML/2.0>
10. NIST, *On Enabling a Model-Based Systems Engineering Discipline*, official publication record. <https://www.nist.gov/publications/enabling-model-based-systems-engineering-discipline>

## Exercises

### Exercise 1

Design an authority map for requirements, system architecture, interfaces, CAD, safety analysis, verification results and deployed configuration across five repositories. Include baselines, conflicts, changes and access.

### Exercise 2

A project says its SysML repository is the single source of truth, but teams edit generated spreadsheets, suppliers deliver PDFs, simulations use copied parameters and operators maintain a separate runtime inventory. Audit and redesign the arrangement.

### Exercise 3

Define a credibility package for reusing a battery degradation model from laboratory design optimization to operational remaining-life decisions in a different climate and duty cycle.

### Exercise 4

Plan migration from a proprietary modeling tool to a new platform while preserving 12 years of baselines, custom profiles, scripts, supplier links, generated specifications and review evidence.

### Exercise 5

An authoritative model is internally consistent, but the as-built system fails an interface test and telemetry conflicts with predicted behavior. Describe the investigation and controlled updates without assuming which artifact is wrong.

## Answers to the Exercises

### Answer 1

Start with claim classes and uses, not repositories. Requirements source controls approved stakeholder/technical requirements and rationale by product baseline. The system model controls logical behavior, allocations, architectural elements and internal logical interfaces. The interface-control source controls released external contracts and negotiated versions. Product-lifecycle/CAD sources control part geometry, material and manufacturing definition. The safety source controls hazards, causes, controls, verification obligations and acceptance status. The verification source controls procedures/configurations/results and closure; runtime configuration management controls installed/as-operated instances. State exceptions where a contract makes a document controlling.

For each class record stable namespace/IDs, source/repository, exact baseline/version resolver, scope/product/variant, owner/steward, approver/technical authority, permitted editors, status workflow, review cadence, intended uses, retention, access/protection, and precedence/conflict route. A baseline manifest pins all repositories, profiles/libraries, external references, transformations and tool versions. Cross-links have typed semantics, endpoint configurations and owners. Derived views carry source digest/revision and cannot be edited as silent masters.

Changes begin in the controlling source through proposal, evidence, impact traversal, affected-owner review, authorization and new baseline. Regenerate outputs and verify propagation; quarantine conflicts rather than last-write-wins. Emergency deviations retain authority, time limit and retrospective review. Attribute/role-based access protects safety, supplier, export or security data while decision-capable views avoid shadow copies. Audit duplicates, ambiguous authority, stale views, broken/cross-baseline links, privileged edits, unpropagated changes and deployed divergence.

### Answer 2

Inventory actual claims and flows. Identify which SysML elements are genuinely governed, which spreadsheets are derived or manually authoritative, what supplier PDFs can support, which simulations control analysis versus consume inputs, and whether runtime inventory is observed evidence or configured authority. Capture IDs, owners, baselines, transformations, write paths, users, decisions and conflicts. Freeze dangerous round trips and locate shadow edits before deleting anything.

Redesign as a federated authoritative set. Assign requirements/architecture/behavior to appropriate governed model packages, interface or supplier contractual claims to controlled sources, simulation parameters/results to versioned analysis sources with provenance, and installed state to configuration/operations sources. Keep one authority per claim/baseline/use. Link through stable identities and typed mappings. Generated spreadsheets become read-only stamped views or acquire an explicit controlled round-trip workflow. Supplier PDFs remain evidence/views unless the contract supplies semantic data and change obligations.

Pin model, profile, library, code, data and tool configurations; define working versus approved states. Validate duplicate IDs, required properties, units, links, stale generations and baseline assemblies in CI. Establish intended-use credibility for simulations and prohibit uncontrolled copied inputs. Reconcile desired and observed runtime state through governed change/status accounting, not automatic overwrite.

Provide accessible concern views, training, supported APIs/exchanges, least privilege and review workflows so teams do not recreate shadows. Define conflicts, emergency edits, backups, retention and vendor exit. Record known model debt and migrate incrementally with evidence. The result may still use the SysML repository centrally, but its authority is bounded and integrated rather than asserted globally.

### Answer 3

Define the new decision: remaining-life estimate for which battery chemistry, cell/module/pack configuration, age, sensors, climate, duty/charging profile, maintenance and consequence. Contrast original laboratory design-optimization purpose, population, controlled cycles, temperature, state-of-charge, measurement and loss function. Identify operations, safety, maintenance, warranty and dispatch users and accountable acceptance authority.

Preserve conceptual equations/algorithms, assumptions, parameter provenance, training/calibration data, code/environment, numerical verification, sensitivity, identifiability and uncertainty. Assess domain shift in temperature/humidity, vibration, charge rate, depth/cycle irregularity, calendar aging, manufacturing lots, sensor noise/bias/missingness, balancing/control, repair and abuse. Check extrapolation and coupled degradation modes. Separate state estimation from future-use forecast.

Acquire representative field and environmental test evidence under controlled configurations. Verify implementation and data pipelines; validate predictions against held-out cells/packs, time horizons and relevant boundary/adversarial cases. Report calibration, error distributions, false early/late retirement, subgroup/lot performance, confidence/coverage and limits rather than average accuracy only. Compare simpler baselines and expert/inspection evidence. Conduct independent safety/domain review proportional to consequence.

Define operational acceptance thresholds, conservative decision margins, unavailable/out-of-domain behavior, human presentation, fallback inspection/replacement, monitoring and update/change authority. Version every model/data/configuration and link each decision to its output. Pilot with bounded authority. Reopen on drift, residual/calibration threshold, incident/near miss, new chemistry/control/lot/climate/duty cycle, sensor change or evidence conflict. Prior laboratory V&V remains evidence but does not accredit the new use.

### Answer 4

Create an immutable inventory of native projects, baselines/branches, element IDs, profile/metamodel versions, libraries, diagrams/tables, relationships, units, constraints, simulations, scripts/plugins/APIs, generated outputs, external links, permissions/audit history, review decisions and contractual records. Classify legal, safety, security, proprietary, export and retention needs. Preserve licensed native environments/readers and backups before transformation.

Define target semantics and a mapping specification for every element/property/relationship, identity/version/status, unit, stereotype/profile, layout, behavior and extension. Decide what becomes native, neutral, archived or manually reconstructed. Prototype representative difficult models and round trips. Build repeatable extract-transform-load tooling with logs, checksums and source-to-target mapping. Never identify success by file import alone.

Reconcile counts and stable IDs, but also required properties, relationship direction/cardinality, units, namespaces, constraints, state behavior, parametric results, cross-repository links, views and generated outputs. Execute old/new validation suites and benchmark analysis cases. Sample semantic review by domain owners; independently inspect safety-critical and supplier boundaries. Record known losses and controlled exceptions.

Run parallel read-only comparison for selected baselines, freeze/cut over through change authority, update the authority register and integrations, regenerate specifications, train users and monitor errors/shadow work. Preserve prior baselines, tool/runtime, transformation code, evidence and decision references according to retention. Update contracts, access and exit rights. Decommission only after restore, audit, operational support and successor ownership pass; retain a rollback plan and superseding decision record.

### Answer 5

Stop unsafe integration or operation according to consequence, preserve the failed item/test setup/software/configuration, raw measurements, telemetry, model baselines and audit history, and notify interface/product/safety/configuration authorities. Do not edit the model to match one observation or reject the hardware because the model is authoritative.

Verify identity and alignment: serial/lot, hardware/software/calibration, interface version, mode/state/time, environment, loads, units/sign/reference frame, tolerances, measurement chain, test procedure and model inputs/configuration. Repeat or independently instrument where justified without erasing the first result. Characterize uncertainty and reproducibility. Inspect manufacturing/as-built records, deviations/waivers, installation, wiring, firmware and supplier changes. Inspect model assumptions, boundary/initial conditions, parameters, numerical implementation, transformations and domain validity.

Form competing causal hypotheses: implementation nonconformance, test/measurement error, wrong configuration mapping, model-form/parameter error, requirement/interface ambiguity, unexpected interaction or environmental/operational condition. Use targeted analysis/tests and evidence to discriminate. Trace impact to requirements, hazards, margins, other units, verification closure, decisions and operations. Treat apparent common cause and safety risk conservatively under proper authority.

Disposition through governed change: correct/rework product, correct/calibrate test, revise requirement/interface, update model and credibility evidence, accept a bounded deviation/risk, or combine actions. Each update occurs in its controlling source with review, rationale, configuration and downstream propagation. Re-run affected V&V and validation, regenerate views and reconcile installed state. Preserve old baselines and failure evidence. Monitor recurrence and reopen if discrepancy, configuration, environment or outcome thresholds change.
