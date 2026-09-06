---
module_id: SDRE-008
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 8
title: Generating and Verifying Software Bills of Materials
status: complete
last_verified: 2026-09-06
---

# Generating and Verifying Software Bills of Materials

## One-Page Review

### Governing question

How can a producer generate and verify an SBOM that accurately describes the components of one exact software artifact, with explicit identity, relationships, lifecycle context, and known limits?

### Essential definitions

- a **software bill of materials (SBOM)** is a formal, machine-readable record of software components and their supply-chain relationships;
- the **subject** or **root component** is the exact product or artifact whose composition the SBOM describes;
- a **component** is a separately identifiable software unit, not necessarily a deployed package or a vulnerability;
- a **relationship** states how components connect, such as dependency, containment, or derivation;
- a **component identifier** is an ecosystem coordinate or other lookup key; a **hash** binds exact bytes;
- **generation context** states when and from what evidence the SBOM was produced, such as source, build, or deployed analysis;
- **breadth** states which component kinds are in scope; **depth** states how far relationships are traversed;
- **completeness** is a bounded claim relative to declared scope, lifecycle stage, and observable evidence;
- **freshness** asks whether the SBOM still represents the exact subject under evaluation;
- **structural validation** checks syntax and schema; **semantic validation** checks identities, relationships, scope, and consistency;
- a **vulnerability match** is a separate inference that combines SBOM identity with advisory data;
- **VEX** communicates an analysis of whether a vulnerability affects a product; it does not repair an inaccurate SBOM.

### Central model, mechanism, or theorem

Model an SBOM as a labeled directed graph

$$
G=(V,E,r,\sigma,\kappa),
$$

where $V$ is the component set, $E$ typed relationships, $r$ the root subject, $\sigma$ the declared scope and generation context, and $\kappa$ evidence supporting each identity. Verification requires schema validity, a digest-bound root, unique stable identities, referential integrity, relationship semantics, and a justified completeness claim.

For expected in-scope components $V_\sigma$, measured recall is

$$
R=\frac{|V\cap V_\sigma|}{|V_\sigma|},
$$

but $V_\sigma$ is often unknown. A tool cannot honestly infer perfect completeness merely because every emitted edge resolves.

### Critical invariants

- bind the SBOM to an immutable release or artifact digest;
- declare SBOM format and version explicitly;
- identify the author, creation time, generation tool, and lifecycle context;
- use ecosystem-native identifiers plus hashes when available;
- give each local node a unique identity and every relationship a resolvable endpoint;
- distinguish direct, transitive, embedded, dynamically loaded, generated, and service dependencies;
- state breadth, depth, exclusions, and unknowns;
- generate as close as practical to the authoritative build evidence;
- merge multiple evidence sources with provenance rather than silently overwriting conflicts;
- validate schema, graph integrity, subject binding, identity quality, and sampled ground truth;
- regenerate for changed artifacts; never relabel an old SBOM as current;
- treat an SBOM as inventory evidence, not proof of vulnerability, exploitability, license compliance, or safety.

### Common failures

Common failures include scanning only the source manifest, omitting resolved transitive components, listing build-only tools as runtime without context, missing vendored or statically linked code, double-counting renamed packages, using names without namespaces or versions, dangling graph edges, claiming complete when dynamic plugins are invisible, attaching one SBOM to several differing artifacts, accepting schema-valid nonsense, mutating a signed SBOM, leaking private coordinates, and treating absence from the SBOM as proof of absence from the product.

### Compact example

Application `pay:4.2.0` at digest `a1` directly depends on library `parse:2.1.0` at `p2`; `parse` depends on `unicode:15.1` at `u7`. The build SBOM contains three uniquely identified nodes and two typed edges, binds root `pay` to `a1`, records the generator and build context, and declares transitive runtime depth. A verifier rejects the document if the `parse -> unicode` edge names a missing node or the downloaded application hashes to `a2`. It still cannot infer that no runtime plugin will later load.

### Connections

[SDRE-007](007-build-metadata-and-provenance.md) records how the subject was built. [SDRE-009](../ROADMAP.md) next authenticates artifact and evidence bytes. Security Engineering owns vulnerability and adversarial conclusions drawn from verified composition.

## Governing Question

An SBOM answers “what software components are represented in this product, according to this evidence and scope?” It does not automatically answer whether the components are vulnerable, reachable, licensed acceptably, supported, authentic, or safe. Those decisions require additional data and policy.

The core delivery challenge is correspondence. The document must describe the exact artifact being released, not a nearby source tree, yesterday's dependency lock, or an image tag that later moved. Its component graph must be internally coherent, and its completeness claim must be limited to what the generating evidence can observe.

## Why This Matters

When a component becomes vulnerable, responders need to locate potentially affected releases before deep analysis. Procurement and license review need comparable component identities. Maintainers need to explain embedded, generated, or inherited software across a product family. Without durable composition records, each incident begins with rediscovery.

CISA's 2025 minimum-elements document defines fields including SBOM author, producer, component name and version, software identifiers, component hash, license, dependency relationship, tool name, timestamp, and generation context [1]. Minimum fields improve exchange but do not guarantee accuracy or completeness. SPDX 3.0.1 defines a broader standard and data model for BOM information [2], while CycloneDX 1.7 models components, services, dependency graphs, compositions, lifecycle stages, and other supply-chain information [3]. Choose a supported format deliberately and validate against its exact version.

The 2025 CISA publication builds on the NTIA 2021 minimum-elements baseline [5]. CISA's SBOM-types guidance separately distinguishes design, source, build, analyzed, deployed, and runtime viewpoints [6]. These classifications describe evidence vantage points; they do not make two independently generated graphs equivalent.

## Prerequisites and Retrieval

Retrieve artifact digest, release identity, package coordinate, dependency resolver, lockfile, static linking, dynamic loading, vendoring, container layer, transitive closure, directed graph, node, edge, schema, serialization, namespace, package URL, CPE, license expression, provenance, attestation, signature, vulnerability advisory, reachability, false positive, and false negative.

From SDRE-002 retrieve declared and resolved dependency graphs. From SDRE-005 retrieve artifact graphs and immutable repositories. From SDRE-007 retrieve provenance subjects, generators, and evidence trust. Do not use this chapter to replace dependency-resolution or vulnerability-analysis reasoning.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish an SBOM from a manifest, lockfile, provenance statement, vulnerability report, and VEX;
2. define subject, component, identity, relationship, scope, depth, and generation context;
3. select authoritative evidence for source, build, and deployed SBOMs;
4. represent direct, transitive, embedded, generated, and service relationships;
5. merge component evidence without losing conflicts or origin;
6. bind an SBOM to an exact artifact or release manifest;
7. validate serialization, schema, graph, identity, and subject consistency;
8. evaluate bounded completeness using ground truth and adversarial fixtures;
9. manage freshness, distribution, privacy, correction, and retention;
10. use verified SBOM data as input to vulnerability and license workflows without overstating conclusions.

## Core Exposition

**Define the subject.** “The application” is ambiguous when a release contains archives, binaries, container indexes, platform images, plugins, and configuration. Name the root with an immutable release coordinate and digest. If one SBOM covers a release bundle, its relationship to every artifact must be explicit. If each artifact receives its own SBOM, the release manifest links them.

An SBOM generated from commit `c7` does not necessarily describe binary `a1`: build flags, conditional dependencies, generated code, vendoring, or packaging may differ. Bind the final document to the built subject and preserve the evidence used to derive composition.

**Choose generation context.** A source SBOM sees declared manifests and vendored source but may not know the resolver's exact selection. A build SBOM can observe resolved inputs, generated code, statically linked objects, and packaging decisions. An analyzed SBOM scans completed artifacts and may find embedded content absent from manifests, but identification can be heuristic. A deployed SBOM can include selected plugins and services, yet represents changing runtime state.

No single context is universally superior. Generate a build SBOM from authoritative resolver and linker evidence, compare it with artifact analysis, and preserve conflicts. State which context produced each fact. CISA's current minimum elements explicitly include generation context because consumers need this distinction [1].

**Model identity carefully.** A component name alone is weak: `core`, `requests`, or `libssl` can refer to unrelated objects. Combine supplier or namespace, ecosystem name, version, package URL or another stable locator, and cryptographic hash when bytes are available. Record platform and variant qualifiers when identity depends on them.

Hashes identify exact bytes, not logical equivalence, licensing, or origin. Ecosystem coordinates aid advisory matching but can be mistyped or reassigned. Maintain both rather than forcing one to do every job. When two tools disagree about identity, retain both observations and a reviewed resolution rather than silently merging on name.

**Represent relationships.** A flat list loses causality. Distinguish `root depends on library`, `archive contains file`, `binary statically links object`, `component generated from source`, and `service calls external API`. Direction and type matter. Every edge endpoint must resolve to a node or a documented external reference.

Directness is relative to the subject and generation mechanism. A library may be transitively resolved but physically embedded. A build dependency may never ship. An optional dependency may be selectable only under a feature flag. Represent these distinctions when the format supports them; otherwise document the loss.

**Define bounded completeness.** Breadth answers which categories are included: first-party, third-party, open source, commercial, files, snippets, firmware, services, build tools, or runtime plugins. Depth answers how far relationships extend. Generation context answers what evidence was visible. An honest claim is “complete for resolved runtime packages in lockfile L and statically linked objects observed by linker map M,” not simply “complete.”

CycloneDX 1.7 supports compositions that characterize completeness [3]. A completeness field remains a claim requiring evidence. Schema validation proves that the claim is expressible, not that it is true.

**Generate from authoritative evidence.** Resolver outputs and lockfiles identify selected packages. Compiler and linker traces reveal static inputs. Image manifests and package databases expose installed content. Language metadata reveals module coordinates. File analysis can find unmanaged binaries. Runtime inventories reveal plugins and services. Each sensor has blind spots and a trust boundary.

Normalize into the selected standard only after preserving source evidence. Record generator name and version, configuration, creation time, subject, and conflicts. Reproducible generation is desirable: the same evidence and normalization rules should yield semantically equivalent graphs even if harmless serialization order changes.

**Validate in layers.** First parse safely with size and recursion limits. Validate the declared format version and schema. SPDX 3.0.1 requires both structural JSON-LD validation and semantic validation against its ontology and shapes for conforming JSON-LD [4]. Then check unique local identifiers, resolvable edges, allowed relationship types, required root, component identity fields, timestamps, and document metadata.

Next recompute the subject digest, compare component hashes where bytes are accessible, and reconcile the graph with resolver, linker, packaging, and artifact evidence. Sample known-positive fixtures that must appear and known-negative fixtures that must not. Validate authentication separately if the SBOM is attested or signed. A structurally valid document can still describe the wrong artifact.

**Measure without pretending omniscience.** If a controlled fixture has expected set $V_\sigma$, compute recall and precision. In production, the true set is often unknown, so use differential checks: compare generators, compare source/build/artifact contexts, inject canary components, and investigate deltas. Absence becomes evidence only within the sensor's demonstrated scope.

For an expected set of 20 runtime components, finding 18 yields $R=18/20=0.90$. If the generator also reports 2 false components, precision is $18/20=0.90$. These figures describe one fixture, tool version, and scope—not universal performance.

**Separate downstream analysis.** Matching component identifiers to advisories produces candidates. Version ranges, backports, distro patches, forks, configuration, reachability, and exploitability determine actual response. VEX can communicate an affected-status analysis, but must bind the same product identity and evidence. Likewise, an SPDX license expression records license data; legal compliance remains a governed conclusion.

**Operate the record.** Publish the SBOM beside the immutable release or through a discoverable API. Apply access policy when private package names reveal architecture. Authenticate documents where the threat model requires it. Retain historical versions for support and incident response. A correction creates a new identified SBOM that records what it supersedes; it does not invisibly change an authenticated historical statement.

## Definitions and Notation

- $G=(V,E,r,\sigma,\kappa)$: SBOM graph;
- $V$: component nodes with local and external identities;
- $E\subseteq V\times L\times V$: typed relationship edges with label set $L$;
- $r\in V$: root subject;
- $\sigma$: breadth, depth, lifecycle context, and exclusions;
- $\kappa(v)$: evidence supporting component $v$'s identity;
- $V_\sigma$: actual components within declared scope;
- $TP$, $FP$, $FN$: true-positive, false-positive, and false-negative component identifications.

When controlled ground truth exists,

$$
precision=\frac{TP}{TP+FP},\qquad recall=\frac{TP}{TP+FN}.
$$

If a denominator is zero, define and report the handling rule; do not silently present an undefined metric as perfect.

## Mechanisms, Invariants, or Proof Structure

**Referential-integrity invariant.** For every internal edge $(u,l,v)\in E$, both $u$ and $v$ exist in $V$ and $l$ has defined semantics. This is necessary for a traversable graph but insufficient for factual correctness.

**Subject-binding proposition.** If the verifier recomputes accepted digest $H(a)=d_r$ and the SBOM root evidence binds $r$ to $d_r$, then the composition claim addresses presented bytes $a$ up to digest and boundary assumptions. The proposition says nothing about whether $V$ is complete.

**Monotonic-evidence warning.** Adding a detected node can improve recall but can reduce precision; deleting an uncertain node can do the reverse. Therefore graph size is not a quality metric. Review against bounded ground truth and retain uncertainty.

**Executable graph check.** This teaching model checks local graph integrity, expected fixture membership, root binding, and duplicate external identity. It does not implement SPDX or CycloneDX validation, hash bytes, authenticate a document, or prove completeness.

<!-- bijux-verify: {"id":"verify-sbom-graph-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=True\ndangling_edge=False\nmissing_expected=False\nduplicate_identity=False\nwrong_subject=False\nauthenticity_proven=False\n","stderr":""}} -->
```python
expected = {"pkg:pay@4.2.0", "pkg:parse@2.1.0", "pkg:unicode@15.1"}
nodes = {
    "root": "pkg:pay@4.2.0",
    "parse": "pkg:parse@2.1.0",
    "unicode": "pkg:unicode@15.1",
}
edges = {("root", "depends", "parse"), ("parse", "depends", "unicode")}

def valid(candidate_nodes, candidate_edges, subject):
    endpoints_exist = all(a in candidate_nodes and b in candidate_nodes for a, _, b in candidate_edges)
    identities = list(candidate_nodes.values())
    return (
        endpoints_exist
        and set(identities) == expected
        and len(identities) == len(set(identities))
        and subject == "sha256:a1"
    )

print(f"accepted={valid(nodes, edges, 'sha256:a1')}")
print(f"dangling_edge={valid(nodes, edges | {('root', 'depends', 'missing')}, 'sha256:a1')}")
print(f"missing_expected={valid({'root': nodes['root'], 'parse': nodes['parse']}, {('root', 'depends', 'parse')}, 'sha256:a1')}")
print(f"duplicate_identity={valid(nodes | {'alias': nodes['parse']}, edges, 'sha256:a1')}")
print(f"wrong_subject={valid(nodes, edges, 'sha256:a2')}")
print("authenticity_proven=False")
```

## Alternatives and Trade-Offs

**SPDX versus CycloneDX.** Both are standardized, expressive ecosystems with overlapping capabilities and different models and tooling. Choose based on consumer contracts, supported profiles, validation, and lossless required semantics—not brand preference.

**Source versus build versus analyzed SBOM.** Source generation is early and explainable; build generation sees actual resolution; artifact analysis finds packaged reality. Combining them exposes disagreement but requires evidence provenance and reconciliation.

**Package versus file granularity.** Package nodes keep graphs manageable and support advisory matching. File and snippet detail can reveal embedded code and licenses but greatly increases size and ambiguity. Match granularity to decisions.

**One aggregate versus per-artifact SBOM.** An aggregate simplifies release exchange; per-artifact records bind platform variants precisely. A release manifest can link both, provided no scope is implied silently.

**Public versus restricted distribution.** Broad sharing accelerates response. Private identifiers can reveal architecture or suppliers. Minimize sensitive fields and use governed access rather than weakening identity fields unpredictably.

## Failure Modes and Misconceptions

- **“A lockfile is an SBOM.”** It records resolver state for one ecosystem, not necessarily shipped composition.
- **“A flat package list is enough.”** Relationships and root context carry meaning.
- **“Schema-valid means accurate.”** Syntax cannot prove correspondence.
- **“More nodes means better.”** False positives can grow with recall.
- **“No match means not present.”** The generator may have a blind spot.
- **“A hash identifies the package name.”** It identifies bytes under a boundary.
- **“A package URL identifies exact bytes.”** Add hashes where available.
- **“Build dependencies are runtime components.”** Preserve relationship and lifecycle context.
- **“One SBOM covers all platform artifacts.”** Bind variants explicitly.
- **“Dynamic plugins are in the build graph.”** Runtime evidence may be required.
- **“The SBOM proves a vulnerability.”** It supplies identity evidence for analysis.
- **“VEX replaces composition.”** It communicates an affected-status conclusion.
- **“A signature fixes incompleteness.”** It authenticates the incomplete document.
- **“Regeneration may overwrite history.”** Preserve identified corrections.
- **“Completeness is a Boolean.”** It is a bounded, evidenced claim.

## Worked Examples

### Example 1

**Lockfile gap.** A lockfile lists 18 language packages, but the binary statically links a C library installed by the builder. A build SBOM combines resolver output with the linker map and records each evidence origin. **Conclusion:** one ecosystem manifest may omit shipped components.

### Example 2

**Dangling edge.** The document says `app dependsOn parser`, but `parser` has no node or external reference. Schema parsing succeeds, graph validation fails, and the producer regenerates from preserved evidence. **Conclusion:** every relationship endpoint must resolve.

### Example 3

**Renamed duplicate.** Two scanners report `openssl` and `libssl` with the same package URL and hash. Blind concatenation double-counts them. Reconciliation retains both observations, selects one canonical node, and records aliases. **Conclusion:** merge by evidenced identity, not display name alone.

### Example 4

**Wrong artifact.** A valid SBOM for Linux AMD64 is attached to an ARM64 archive under the same release version. The root digest mismatch rejects it. **Conclusion:** version equality cannot substitute for subject binding.

### Example 5

**Optional plugin.** A server may load database drivers from an operator directory. The build SBOM declares plugins out of scope; deployment inventory records selected driver digests. **Conclusion:** bounded incompleteness is safer than a false universal claim.

### Example 6

**Fixture measurement.** Ground truth contains 20 components. A tool finds 18 true and 2 false: precision and recall are both $18/20=0.90$. Repeating under another packaging mode is required before generalizing. **Conclusion:** metrics belong to a stated fixture and scope.

### Example 7

**Vulnerability candidate.** An advisory range matches a component version, but the distribution backported the fix without changing the upstream version string. The responder checks supplier advisory, package hash, patch provenance, and VEX. **Conclusion:** version matching starts investigation; it does not finish it.

### Example 8

**Container excess.** Package-database scanning lists build tools left in a final image. They are truly shipped even if unused. A multi-stage build removes them, a new image digest and SBOM are produced, and attack surface shrinks. **Conclusion:** the SBOM can reveal packaging reality rather than intended runtime use.

### Example 9

**Correction.** A released SBOM omitted a vendored library. The producer issues a newly identified corrected SBOM linked to the same artifact digest, records that it supersedes the old document, and alerts consumers. **Conclusion:** correct evidence without rewriting authenticated history.

### Example 10

**Service dependency.** A SaaS product calls an external payment API whose implementation bytes the producer cannot enumerate. The SBOM records the service relationship and scope rather than inventing its component tree. **Conclusion:** model externally observable dependencies at the boundary actually known.

## Cross-Program Connections

- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns vulnerability, exploitability, signing, and adversarial conclusions.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns ingestion, normalization, lineage, and querying of large SBOM collections.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns durable graph storage and transactional correction records.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns service dependency and exchange interfaces.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns reliable organization-wide generation and distribution capabilities.

## References

1. Cybersecurity and Infrastructure Security Agency, *Minimum Elements for a Software Bill of Materials (SBOM)*, August 2025. [Official publication](https://www.cisa.gov/sites/default/files/2025-08/2025_CISA_SBOM_Minimum_Elements.pdf). Checked 2026-09-06.
2. SPDX Project, *System Package Data Exchange Specification 3.0.1*, scope and data model. [Official specification](https://spdx.github.io/spdx-spec/v3.0.1/). Checked 2026-09-06.
3. OWASP Foundation and Ecma International, *CycloneDX Specification 1.7*, released 2025-10-21 and published as ECMA-424 on 2025-12-10. [Official overview](https://cyclonedx.org/specification/overview/). Checked 2026-09-06.
4. SPDX Project, *SPDX 3.0.1 Model and Serializations*, structural and semantic validation requirements. [Official specification](https://spdx.github.io/spdx-spec/v3.0.1/serializations/). Checked 2026-09-06.
5. National Telecommunications and Information Administration, *The Minimum Elements for a Software Bill of Materials*, July 12, 2021. [Official report](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom).
6. Cybersecurity and Infrastructure Security Agency, *Types of Software Bill of Materials (SBOM) Documents*, April 2023. [Official publication](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf).

## Exercises

### Exercise 1

**Distinguish records.** Explain how a dependency manifest, lockfile, build provenance, SBOM, vulnerability report, and VEX differ for one release.

### Exercise 2

**Trace a graph.** Given root `A`, edges `A->B`, `A->C`, `B->D`, and a missing node `D`, perform structural, graph, identity, and subject checks in order.

### Exercise 3

**Diagnose disagreement.** A source generator reports 42 components, a build generator 39, and artifact analysis 41. Design a reconciliation investigation without selecting the largest list automatically.

### Exercise 4

**Design production generation.** Define evidence sources, scope, identities, validation, authentication, publication, correction, and retention for a multi-platform application release.

### Exercise 5

**Transfer to an extensible device.** Design composition records for firmware with compiled libraries, a bootloader, device-specific configuration, and field-installed plugins.

## Answers to the Exercises

### Answer 1

A manifest declares allowed direct dependencies; a lockfile records one resolver outcome. Provenance claims how digest-identified outputs were produced from resolved inputs. An SBOM describes the subject's component and relationship graph within a declared context. A vulnerability report matches and analyzes advisories against identities. VEX communicates an affected-status conclusion and rationale for a product-vulnerability pair. They may link to the same release, but no record substitutes for the others: a lock can omit packaged native code, provenance need not enumerate composition, and an SBOM alone cannot prove exploitability.

### Answer 2

Parse with resource limits and validate the declared schema first. Require unique node identifiers and valid relationship types. `B->D` has a dangling internal endpoint, so graph integrity fails; do not infer or delete `D` silently. If repaired, validate external identities and hashes for `A`, `B`, `C`, and `D`, recompute the presented artifact digest, and require it to match root `A`. Only then evaluate the declared breadth, depth, generation context, and authentication. Passing later checks cannot compensate for the dangling edge.

### Answer 3

Normalize identifiers without discarding original observations, then compute set and edge differences. Inspect whether source-only nodes are optional, development, or excluded by build flags; whether build-only nodes are generated, resolver-selected, or statically linked; and whether artifact-only nodes are vendored, base-image, renamed, or false identifications. Compare lockfiles, linker maps, package databases, image layers, and hashes. Test controlled positive and negative fixtures for each tool version. Resolve each conflict with evidence, label remaining uncertainty, and define which contexts the resulting aggregate covers. Count alone says nothing about precision.

### Answer 4

Bind either one SBOM per artifact digest or an aggregate to an immutable release manifest covering every platform. Generate from resolver outputs, versioned configuration, compiler/linker traces, packaging databases, and artifact analysis. Identify components with namespaces, versions, ecosystem locators, variants, and hashes; type every relationship. Declare runtime/build breadth, transitive depth, exclusions, tool versions, and generation context.

Validate format version, schema, semantic constraints, unique IDs, edge endpoints, root digest, sampled component bytes, and controlled fixtures. Authenticate the finalized document under the release evidence policy and publish it beside the artifacts. Corrections receive new document identities and supersession links. Retain old and corrected SBOMs, source evidence, verification material, and generator configuration for the support and incident window while restricting sensitive coordinates.

### Answer 5

Use the firmware image or signed release manifest as root. Build evidence enumerates compiled libraries and generated modules; a separate containment or composition edge identifies the bootloader. Device-specific configuration is a distinct artifact or installation input rather than falsely treated as identical firmware. Its record binds a configuration-schema version and privacy-preserving digest. Field plugins require a deployed inventory with install/remove events and plugin digests because the build SBOM cannot know them.

Link the build SBOM, factory configuration record, and deployed plugin inventory through stable device-class and release identities while restricting device-specific data. Verification checks every boundary's subject, graph, authority, and freshness. Incident response queries compiled, bootloader, configuration, and plugin cohorts separately. “Complete” is stated only for each sensor's declared scope and time.
