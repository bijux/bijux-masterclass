---
module_id: SARCH-097
program: Software Engineering: Software Architecture
level: 2
module_number: 97
title: Architecture for Long-Lived Scientific Systems
status: complete
last_verified: 2026-09-06
---

# Architecture for Long-Lived Scientific Systems

## One-Page Review

### Governing question

How can a scientific system preserve interpretable observations, computations, uncertainty, provenance, and legitimate access for decades while instruments, software, formats, institutions, questions, and people change?

### Essential definitions

- a **scientific record** is an identified observation, transformation, result, or decision plus enough context to interpret its claim;
- **provenance** records relevant entities, activities, agents, relations, versions, and times that produced or changed a record;
- **calibration** establishes a relation between an instrument indication and reference values under stated conditions; it is not merely a correction constant;
- **lineage** traces inputs and transformations; **audit history** records governed actions; neither alone establishes scientific validity;
- **fixity** is evidence that a bit sequence has not changed relative to a recorded digest; it does not prove authenticity or meaning;
- a **persistent identifier** is intended to keep identifying an object despite location or ownership change; resolution and preservation remain separate obligations;
- a **representation-information package** supplies format, semantics, units, vocabulary, encoding, dependencies, and interpretation needed by a designated future community;
- **reproduction** reruns an analysis with the same artifacts and conditions; **replication** tests a claim with independently obtained evidence;
- **migration** changes representation while preserving declared significant properties; **emulation** recreates a required execution environment;
- a **designated community** is the future audience whose knowledge assumptions define what an archive must explain.

### Central model, mechanism, or theorem

Treat a durable scientific product as

$$
S=(O,M,P,C,E,R,G,L),
$$

where $O$ is immutable original observation, $M$ meaning and measurement context, $P$ provenance, $C$ computation, $E$ evidence and uncertainty, $R$ representation and recovery, $G$ governance and access, and $L$ lifecycle ownership. A file without this closure may be intact yet scientifically unusable.

If $N$ stored bits each have probability at most $p$ of undetected alteration during a declared interval, the union bound gives $P(\text{one or more alterations})\le Np$ without assuming independence. Multiple copies reduce independent loss, but correlated software defects, shared credentials, one institution, one format, and one geographic hazard violate that premise. Preservation therefore uses fixity checking, repair, diversity, access controls, provenance, and periodic interpretability tests—not copy count alone.

For initial volume $V_0$, annual fractional growth $g$, and $n$ years, $V_n=V_0(1+g)^n$. A 12 PB collection growing 8% annually reaches about 55.93 PB after 20 years before replicas, indexes, derived products, staging, or format migration.

### Critical invariants

- raw observation is immutable; correction creates a new identified version linked to its reason and authority;
- every numeric quantity carries phenomenon, unit, scale, uncertainty or quality status, and relevant calibration lineage;
- specimen, subject, instrument, run, software, environment, dataset, result, and publication identities cannot be silently reused;
- every published result resolves to exact input versions, transformations, parameters, code, dependencies, and material nondeterminism;
- fixity, authenticity, scientific validity, reproducibility, and replicability remain distinct claims;
- derived data can be rebuilt or its irreproducible status and retention basis are explicit;
- format migration retains source, transform, significant-property tests, comparison evidence, and reversibility boundary;
- access, consent, embargo, license, Indigenous or community governance, and deletion obligations travel with every copy and derivative;
- metadata remains interpretable after people, vendors, instruments, and institutions leave;
- backup and archive are separate: recovery restores service; preservation maintains understandable information over time;
- every retained collection has funded custody, succession, exit, and disposal authority;
- current operational convenience cannot overwrite historical meaning.

### Common failures

Common failures include saving numbers without units; overwriting a calibration correction; identifying a specimen only by freezer position; storing code without dependencies or parameters; claiming reproducibility because a container image exists; treating a checksum as proof of authenticity; copying corrupted data to every replica; keeping only a proprietary format; migrating without significant-property tests; assigning a DOI to mutable content without version policy; deleting raw data after producing an unverified derivative; losing negative results; assuming FAIR means public; retaining sensitive derivatives outside consent; restoring an old catalog over newer identifiers; depending on one expert’s memory; measuring storage but not curation cost; and promising permanent preservation without funded succession.

### Compact example

A telescope exposure stores detector bytes immutably with observation ID, instrument and configuration, target coordinates, time basis, environmental state, calibration-set IDs, acquisition software digest, checksums, and access policy. A later flat-field correction produces a versioned calibrated dataset and provenance edge rather than rewriting the exposure. The published plot identifies exact inputs, analysis code and environment, parameters, random seed policy, and uncertainty method. Annual fixity checks compare independent copies and repair from a verified source; a periodic future-user exercise proves more than byte survival.

### Connections

[SARCH-073](073-versioned-contracts-and-compatibility.md) supplies compatibility, [SARCH-076](076-data-migration-architecture.md) supplies controlled movement, [SARCH-091](091-architecture-for-regulated-and-safety-critical-systems.md) distinguishes assurance claims, [SARCH-094](094-architecture-for-machine-learning-enabled-products.md) governs learned artifacts, and [SARCH-096](096-architecture-for-offline-and-intermittently-connected-systems.md) supplies disconnected acquisition. [SARCH-098](../ROADMAP.md) next treats severe cost constraints. Data Architecture owns enterprise meaning and governance; this chapter owns the architectural synthesis for decades-long scientific observation and computation.

## Governing Question

A long-lived scientific system outlasts its first storage array, database, programming language, instrument team, funding grant, and institutional strategy. Its observations may answer questions not imagined at acquisition. Yet unlimited retention is neither affordable nor lawful, and a preserved bitstream can become meaningless when calibration, units, vocabulary, software, or community knowledge disappears.

The governing problem is continuity of justified interpretation. Architecture must preserve original evidence, make transformations traceable, support correction without revisionism, manage uncertainty, survive technology and organization change, and allow a future qualified reader to determine what a result does—and does not—show.

## Why This Matters

Scientific conclusions influence medicine, climate policy, engineering, public spending, and later research. Small semantic losses can dominate large technical success: Celsius interpreted as kelvin, local time interpreted as UTC, a changed assay kit omitted from metadata, or a corrected sample identity overwritten in place.

The FAIR principles call for scientific objects to be findable, accessible, interoperable, and reusable while explicitly remaining implementation-independent; accessible does not mean unrestricted public access [1]. The 2025 third edition of the OAIS reference model frames preservation around information, organizational responsibility, and a designated community rather than storage media alone [2]. Architecture must turn those principles into owned, testable lifecycle mechanisms without claiming that metadata or preservation proves a scientific conclusion.

## Prerequisites and Retrieval

Retrieve observation, measurement, unit, uncertainty, calibration, traceability, provenance, lineage, raw data, derived data, immutable version, persistent identifier, content digest, fixity, authenticity, schema, vocabulary, ontology, repository, archive, backup, retention, legal hold, consent, license, embargo, checksum, erasure coding, replication, migration, emulation, container, dependency, random seed, floating point, significant property, recovery point, recovery time, and designated community.

From SARCH-026 retrieve information views; SARCH-041 supplies system-of-record boundaries; SARCH-045 supplies file exchange; SARCH-053 supplies placement; SARCH-067 supplies reliability models; SARCH-073 supplies compatibility; SARCH-076 supplies migration evidence; SARCH-079 supplies decommissioning; and SARCH-091, SARCH-094, and SARCH-096 supply assurance, empirical software, and remote acquisition constraints.

## Learning Objectives

After completing this module, you should be able to:

1. define the preservation closure around an observation or computational result;
2. separate immutable acquisition, correction, calibration, derivation, interpretation, and publication;
3. design identity and provenance across samples, instruments, software, data, and people;
4. distinguish fixity, authenticity, validity, reproducibility, and replication evidence;
5. budget multi-decade storage, migration, and curation while stating model limitations;
6. preserve software and computational environments without treating packaging as sufficient proof;
7. evolve formats, schemas, units, and vocabularies through explicit semantic mappings;
8. apply access, consent, license, retention, and community governance to copies and derivatives;
9. design institutional succession, funded custody, and exit;
10. test restoration, reinterpretation, rebuild, migration, and correction with future users.

## Core Exposition

**Define the scientific object and preservation claim.** Begin with the decisions future users must make: reanalyze an observation, audit a published result, compare instruments, reproduce a computation, or understand why a record was excluded. Name the designated communities and what knowledge they may reasonably possess. “Keep files forever” is neither testable nor funded.

For each object, state significant properties, retention duration, access policy, loss tolerance, recovery objective, representation dependencies, and authoritative custodian. A quick-look image may be replaceable; a unique detector exposure, consent record, or physical-sample destruction log may not be. Preservation levels should follow scientific and governance value, not file extension.

**Separate observation from interpretation.** Raw does not mean metaphysically untouched; acquisition already depends on sensor electronics, firmware, thresholds, compression, and clocks. Define the earliest retained bitstream and record the transformations before it. Keep that original immutable, then express calibration, cleaning, quality flags, coordinate conversion, and exclusion as versioned derivations.

Correction should create a new assertion linked to the superseded one, with reason, method, evidence, and authority. Never rewrite history so later readers cannot reconstruct which dataset supported an earlier paper. Publication views may point to the current recommended version while preserving the cited historical version.

**Model measurements, not bare values.** A number needs phenomenon, unit, scale, coordinate or reference frame, time basis, uncertainty, quality status, detection limit, missingness meaning, and calibration context. Zero, below detection, not measured, and lost are not interchangeable. Units should be machine-checkable and human-readable.

NIST’s current SI material, checked 2026-09-06, reflects the seven defining constants and current prefixes while noting that SP 811 itself predates the 2019 SI revision [9]. This is a useful warning: even authoritative guidance has edition boundaries. Preserve the exact unit vocabulary and conversion rule used, not merely a link to a changing page.

**Treat calibration as lineage.** Record instrument identity and configuration, reference material, calibration procedure and software, coefficients with units and uncertainty, environmental conditions, validity interval, responsible agent, and evidence. A recalibration may change the interpretation of old observations; it should generate a new calibrated product, not overwrite acquisition.

Calibration traceability does not imply fitness for a particular scientific question. Drift, saturation, interference, sampling bias, and changed protocols remain. Carry quality flags and uncertainty through computations according to a declared model, and preserve when a propagation is analytic, simulated, heuristic, or unknown.

**Build an identity graph.** Distinguish project, protocol, instrument, component, firmware, calibration, site, specimen, subject, visit, run, observation, file, dataset version, software source, build, environment, workflow, result, figure, publication, person, organization, and policy. Reusing a freezer slot or filename as specimen identity invites silent reassignment.

Persistent identifiers improve citation and movement but do not guarantee resolution, access, correctness, or preservation. DataCite’s current Metadata Schema 4.6, checked 2026-09-06, adds project and award resource types and continues versioned metadata practice [8]. ISO/IEC 18670:2025 standardizes content-based SWHIDs for software artifacts while explicitly leaving resolution outside its scope [7]. Use identifiers with version and mutability policy, custody, and resolution monitoring.

**Capture provenance as queryable evidence.** Record entities, activities, agents, roles, plans, times, inputs, outputs, transformations, parameters, software, environment, and delegation. W3C PROV provides a recommendation for representing and interchanging provenance [4], but adopting its vocabulary does not automatically capture complete or truthful lineage.

Provenance must be generated near the action and transactionally linked where possible. Manual annotations need identity and review. Protect provenance from unauthorized rewriting while permitting correction by superseding assertion. Test queries such as “which plots used calibration C?”, “which subjects were governed by consent version V?”, and “which results depend on vulnerable library L?”

**Define computational reproducibility precisely.** A result bundle identifies exact inputs, code, build, dependencies, operating assumptions, parameters, configuration, seeds, hardware-relevant behavior, locale, time zone, concurrency, and expected outputs with tolerances. The Reproducible Builds project reserves “reproducible build” for bit-identical artifacts from the same declared source, environment, and instructions [10]. Scientific computations may instead need numeric or inferential equivalence under a declared tolerance.

A container captures selected filesystem and configuration state, not necessarily kernel, hardware, external services, licenses, random sources, or data rights. A workflow rerun can reproduce a bug. Reproducibility supports inspection; independent replication addresses a different scientific claim. Label artifact availability, successful execution, result reproduction, and scientific validation separately.

**Preserve code at several layers.** Retain human-readable source, content identity, history needed for interpretation, license, build instructions, dependency lock or closure, compilers, environment description, test oracles, executable artifact where lawful, and sample inputs/outputs. Current software may be rebuilt; obsolete software may require an emulator or retained binary.

Source availability does not ensure buildability after registries disappear. Mirror permitted dependencies and record hashes. Rehearse independent rebuilds. Choose migration, emulation, or maintained reimplementation from significant properties and risk; a rewrite can alter floating-point order, algorithms, defaults, and undocumented behavior.

**Make nondeterminism part of the record.** Random seeds help only when algorithm, generator, library, parallel schedule, and hardware semantics are controlled. Floating-point addition is not associative, so changed reduction order can change low bits and sometimes downstream thresholds. GPUs and distributed execution may contain nondeterministic operations.

Record deterministic settings, seed derivation, replicate count, output distributions, tolerances, and sensitivity. Preserve exact output when it is part of the evidence, even if reruns should be statistically rather than bitwise equivalent. Do not hide a meaningful instability behind a loose tolerance.

**Preserve negative and excluded evidence.** A database of successful runs alone creates survivorship bias. Retain failed acquisitions, invalid runs, exclusion reasons, protocol deviations, quality-control decisions, and negative results at a proportionate level. Distinguish “not observed” from “not retained.”

This does not require retaining every transient byte. Define selection policy, authority, and evidence. Sampling or disposal decisions must be reproducible and linked to collection version. Otherwise future users cannot tell whether an apparent pattern reflects nature or curation.

**Use durable representations with escape routes.** Prefer documented, widely implemented, self-describing formats where they preserve significant properties. Also retain schema, vocabulary, examples, validation tools, and independent readers. A nominally open format can be unusable if compression, extensions, coordinate conventions, or external dictionaries are undocumented.

HDF5 separates an abstract data model from its storage mapping [11]. That power can still produce institution-specific conventions no generic reader understands. Store profile, dimension semantics, chunking, filters, endianness where relevant, missing values, units, and domain conventions. Validate with more than the writer library.

**Evolve schemas and vocabularies semantically.** Version terms and definitions. Record whether a new category splits, merges, narrows, broadens, or corrects an old one. Never map unknown historical values to a current default merely to satisfy a constraint. Preserve original value and mapping confidence.

Unit conversion, coordinate transformation, taxonomic revision, disease classification, and instrument renaming may change scientific meaning. Mappings need qualified domain review and counterexamples. Queries spanning versions should state which normalization policy they use.

**Migrate formats as a scientific change.** Inventory source representation, significant properties, known reader behavior, corruption, and unsupported features. Preserve source bytes and fixity, use an identified transform and environment, produce destination with new identity, and compare structure, values, metadata, uncertainty, visual or domain properties, and round trips where meaningful.

Do not rely on file counts. A transform can preserve every row and alter units or missingness. Sample rare features and adversarial boundaries. Record losses, approximations, untranslatable objects, and the point after which source software can no longer be operated. Keep source until legitimate policy approves disposal.

**Engineer fixity and repair.** Compute authenticated or access-protected manifests at ingestion, replicate across independent failure domains, verify on a risk-based schedule, classify mismatch, and repair only from a trusted intact source. A digest collision is not the usual operational risk; wrong object association, compromised manifests, incomplete coverage, and copying corruption are often more immediate.

Scrubbing reads media and checks fixity but can add load and latent-failure exposure. Schedule by media, copy diversity, size, and consequence. Test restoration and catalog reconstruction. If every copy shares one destructive software path, geographic replication cannot save it.

**Distinguish backup from preservation.** Backup restores recent service after deletion or corruption; it is often rotating, environment-coupled, and operator-focused. Preservation maintains identified, understandable information and policy for a future community. A repository needs both when service continuity and long-term evidence matter.

OAIS names submission, archival, and dissemination information packages and preservation-description information [2]. Use the model to ask what context, provenance, fixity, reference, and access-rights information travels with content. Do not claim OAIS conformance from terminology alone.

**Plan scale and cost over decades.** Compound growth, replicas, erasure coding, indexes, derived products, checks, egress, migrations, cold retrieval, and staff curation. Storage price decline does not guarantee budget decline when volume, service expectations, and governance expand. Keep a cost per preserved and interpretable object, not only per raw terabyte.

Classify raw, canonical derived, reproducible derived, cache, and disposable staging. Verify rebuild cost and dependency availability before deleting derived data. Forecast accession and retrieval, not just steady-state bytes. Reserve migration headroom: conversion often needs source and destination simultaneously.

**Govern sensitive and community-controlled science.** FAIR accessibility may require authenticated, authorized access rather than public download [1]. Consent, purpose limitation, embargo, license, export control, species-location protection, Indigenous data sovereignty, and community agreements constrain copies, indexes, training sets, and derivatives.

De-identification can fail under linkage, and a derived model may retain governed information. Record policy and consent version in lineage; enforce access at storage, computation, export, and support; audit decisions; propagate withdrawal where legitimate; and retain only the evidence required to prove compliant action. Legal and community authorities decide real obligations.

**Design reproducible access environments.** Moving petabytes or sensitive data to each researcher may be infeasible. Bring approved computation to governed data with versioned workspaces, egress review, resource quotas, logged environment identity, and exportable provenance. Prevent mutable notebooks and hidden interactive steps from becoming the only analysis record.

Interactive exploration is valuable; publication freezes an executable or explicitly documented workflow from exact inputs. Record manual decisions as parameters or signed annotations. A clean-room rerun by someone outside the original team is stronger evidence than the author rerunning cached state.

**Make correction and retraction durable.** Scientific records can be wrong. Preserve original citation resolution, publish a linked correction or retraction with authority and reason, update recommended views, and notify known dependent products where feasible. Do not delete the evidence that a historical conclusion used.

Derived-product lineage enables impact analysis. A calibration defect may affect thousands of datasets and papers. Automate candidate identification, but qualified scientists decide materiality. Preserve counterevidence and unresolved disputes rather than encoding institutional confidence as fact.

**Design institutional succession.** Every collection needs a custodian, funding model, competencies, support horizon, key and credential succession, supplier exit, disaster recovery, and transfer package. Principal investigators retire; grants end; universities merge; cloud accounts and domains lapse.

The NIST Research Data Framework version 2.0 organizes research-data concerns across lifecycle and stakeholders [3]. Use such frameworks to expose responsibility gaps, not as proof that they are closed. Exercise custody transfer to a different team and, where possible, a different institution.

**Preserve operations and observability evidence.** Record accession backlog, validation failures, fixity coverage, replica independence, repair, media age, restore tests, format risk, unsupported dependencies, identifier resolution, schema versions, access decisions, withdrawn consent, curation queue, staffing, cost, and collections without funded successor.

Dashboards should distinguish bit health, representation health, metadata completeness, reproducibility evidence, access-policy health, and scientific-review status. One green “archive healthy” number hides incompatible claims.

**Test future interpretability.** Give a representative package to a qualified person who did not create it. Ask them to locate, access under policy, interpret units and uncertainty, trace provenance, rebuild or run the analysis, reproduce stated outputs, identify known limitations, and cite the exact version. Record questions and missing assumptions.

Repeat after format, infrastructure, policy, or staff change. Test corrupt copy repair, catalog loss, key loss, dependency disappearance, identifier outage, migration, legal hold, consent withdrawal, and institutional transfer. Preservation is an ongoing empirical service, not an ingestion event.

## Definitions and Notation

Let:

- $O_i$ be immutable original observation $i$;
- $D_j=f_j(I_j;\theta_j,E_j)$ be derived product $j$ from identified inputs $I_j$, parameters $\theta_j$, and execution environment $E_j$;
- $G=(V,E)$ be a provenance directed graph of identified entities, activities, and agents;
- $h(x)$ be a cryptographic content digest of bit sequence $x$;
- $N$ be the number of stored bits and $p$ an upper bound on alteration probability per bit for a declared interval;
- $k$ be copy count and $F_m$ a failure event shared by multiple copies;
- $V_0$ be initial logical volume, $g$ annual fractional growth, and $n$ years;
- $U=(q,u,s,r)$ describe a measurement’s quantity $q$, unit $u$, scale/reference $s$, and uncertainty or quality record $r$;
- $P_s$ be the set of significant properties promised across representation change;
- $K_t$ be the knowledge assumed of the designated community at time $t$.

Interpretability is relative to $K_t$: representation information must close the gap between stored bits and what the designated community can independently understand. That gap can grow even when $h(x)$ remains unchanged.

## Mechanisms, Invariants, or Proof Structure

**Union-bound fixity argument.** Let $A_i$ be the event that bit $i$ changes undetected during the interval, with $P(A_i)\le p$. Then

$$
P\left(\bigcup_{i=1}^{N}A_i\right)\le\sum_{i=1}^{N}P(A_i)\le Np.
$$

The first inequality is the union bound and needs no independence assumption. It provides an upper bound, not a measured storage guarantee. For $N=10^{12}$ and $p=10^{-15}$, the bound is $10^{-3}$. The model omits sector correlation, controller defects, malicious action, wrong manifests, and repair behavior.

**Replica-independence limitation.** If each of $k$ copies independently disappears with probability $p$, simultaneous loss is $p^k$. If a common event $F_m$—such as destructive credentials or faulty migration—removes all copies, total loss probability is at least $P(F_m)$. Therefore adding replicas without reducing common causes cannot establish the independent model’s exponential reduction.

**Provenance closure invariant.** A published result $D_j$ is computationally traceable only if every input, transformation, parameter, environment, manual decision, and material nondeterministic source recursively resolves to preserved identity and interpretation. A provenance graph can be acyclic and still incomplete; graph structure is necessary evidence, not scientific validation.

**Executable package validator.** This finite checker classifies a result package. It checks identity, immutable input digest, units, calibration, environment, and provenance parent before declaring the package structurally traceable. Production validation also needs signature, authorization, format, dependency, numeric, domain, and policy checks.

<!-- bijux-verify: {"id":"validate-scientific-package","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"missing-identity\ndigest-mismatch\nmissing-unit\nmissing-calibration\nmissing-environment\nmissing-parent\ntraceable\n","stderr":""}} -->
```python
import hashlib

def classify(package, raw):
    if not package.get("id"):
        return "missing-identity"
    if package.get("sha256") != hashlib.sha256(raw).hexdigest():
        return "digest-mismatch"
    if not package.get("unit"):
        return "missing-unit"
    if not package.get("calibration_id"):
        return "missing-calibration"
    if not package.get("environment_digest"):
        return "missing-environment"
    if not package.get("input_id"):
        return "missing-parent"
    return "traceable"

raw = b"detector-counts:10,11,9"
base = {
    "id": "result-42",
    "sha256": hashlib.sha256(raw).hexdigest(),
    "unit": "count",
    "calibration_id": "cal-7",
    "environment_digest": "sha256:environment",
    "input_id": "exposure-19",
}
cases = [
    base | {"id": ""},
    base | {"sha256": "wrong"},
    base | {"unit": ""},
    base | {"calibration_id": ""},
    base | {"environment_digest": ""},
    base | {"input_id": ""},
    base,
]
for case in cases:
    print(classify(case, raw))
```

**Growth derivation.** With annual retained growth $g$, the recurrence $V_{t+1}=V_t(1+g)$ yields $V_n=V_0(1+g)^n$ by repeated substitution. At $V_0=12$ PB, $g=0.08$, and $n=20$, the result is $12(1.08)^{20}\approx55.93$ PB. Replication factor three makes raw copied capacity about 167.79 PB before coding, indexes, work space, and metadata; this is a planning illustration, not a price forecast.

## Alternatives and Trade-Offs

**Preserve everything versus appraisal.** Broad retention supports unknown future questions but increases cost, privacy, attack surface, and curation burden. Appraisal reduces burden but can encode current bias. Preserve unique, irrecoverable evidence and selection provenance; make disposal governed and observable.

**Open format versus original format.** An open canonical format improves future access, while original bytes preserve source behavior and disputed semantics. Keeping both costs more but supports migration audit. Proprietary formats may retain instrument-specific features; mitigate with export, specification, reader, test corpus, and vendor exit.

**Migration versus emulation.** Migration keeps data usable on current platforms but can alter significant properties at every conversion. Emulation preserves old execution behavior but requires emulator, system images, licenses, and expertise. Many archives migrate common data while emulating selected historical computation.

**Bitwise versus semantic reproducibility.** Bitwise equality is strong for builds and exact artifacts but may be unavailable or scientifically irrelevant under floating-point parallelism. Numeric, statistical, or inferential equivalence can be valid only with explicit tolerance, oracle, and rationale; overly broad tolerance conceals defects.

**Central repository versus federated custody.** Centralization simplifies standards and preservation expertise but creates institutional and jurisdictional concentration. Federation preserves domain and regional authority but complicates discovery, identity, policy, and quality. Common profiles plus local governance can balance them.

**Data download versus governed compute.** Download maximizes researcher flexibility but may be infeasible, costly, or prohibited. Compute-to-data controls access and captures environments while introducing platform dependence and egress gates. Export portable workflows and provenance to avoid one analysis monopoly.

**Live dataset versus immutable releases.** Live correction serves current users; immutable releases support citation and reproduction. Use versioned releases plus a current pointer and explicit correction links. Never let the current pointer erase the version a claim used.

## Failure Modes and Misconceptions

- **“Raw data has no interpretation.”** Acquisition already embeds instrument, firmware, timing, and encoding choices.
- **“A checksum proves the file is correct.”** It proves equality to a chosen digest under assumptions, not authenticity, meaning, or validity.
- **“Three copies are safe.”** Common credentials, software, format, vendor, or institution can destroy all three.
- **“FAIR means public.”** Accessibility can require authorization and community governance.
- **“A DOI preserves an object.”** Identification, resolution, custody, access, and bit preservation are separate.
- **“A container reproduces the experiment.”** It omits physical acquisition and may omit kernel, hardware, services, data, and licenses.
- **“Same code and seed give the same result.”** Library, hardware, generator, concurrency, and floating-point order can differ.
- **“A provenance graph proves validity.”** It can faithfully explain a flawed method.
- **“Open format means self-explanatory.”** Profiles, units, vocabularies, and external conventions may be missing.
- **“Migration succeeded because counts match.”** Values, precision, missingness, metadata, relationships, and significant behavior can change.
- **“Derived data is always rebuildable.”** Dependencies, parameters, rights, and expertise may be gone or rebuild cost prohibitive.
- **“Negative runs are clutter.”** Selective retention can bias later inference and conceal protocol failures.
- **“Cloud durability is preservation.”** Provider durability does not supply interpretation, policy, succession, or future access.
- **“Current experts will document it later.”** Tacit knowledge leaves before a scheduled preservation project.
- **“Permanent means no further work.”** Media, formats, policy, access, people, and community knowledge continue changing.

## Worked Examples

### Example 1

**Thirty-year telescope collection.** A telescope begins at 12 PB and retains 8% more logical volume annually. The compound model gives about 55.93 PB after 20 years, not the linear 31.2 PB estimate $12(1+20\cdot0.08)$. Three full copies would require about 167.79 PB before indexes and migration workspace. The architecture retains immutable exposures, calibration lineage, documented domain formats, geographic and administrative diversity, fixity repair, and an annual outsider reinterpretation sample. **Conclusion:** long-horizon capacity compounds, while interpretable custody—not raw replication factor—is the preservation outcome.

### Example 2

**Correcting instrument calibration.** A salinity sensor’s pressure coefficient is later found wrong. Rewriting five years of calibrated values would make old publications irreproducible. The system preserves detector observations and calibration C1, creates reviewed calibration C2 with uncertainty and validity, derives dataset D2 from the same observations, links D2 as a correction of D1, and identifies affected results through provenance. Current views prefer D2; citations to D1 still resolve with a warning. **Conclusion:** correction creates lineage and impact evidence rather than mutable history.

### Example 3

**Reproducing a parallel simulation.** A climate simulation preserves source, compiler, libraries, mesh, inputs, parameters, hardware class, decomposition, random-generator family, seeds, and outputs. A rerun on newer accelerators differs in low bits because reduction order changes, but declared aggregate fields remain within pre-reviewed numeric tolerances and ensemble distributions pass specified comparisons. One threshold event does not match, so the team investigates instead of broadening tolerance after seeing the result. **Conclusion:** scientific reproduction may be tolerance-based, but the oracle must precede and expose meaningful differences.

### Example 4

**Migrating a proprietary microscopy format.** The archive converts images to a documented format. Counts and dimensions match, yet rare tiled images lose stage coordinates and one compression mode changes signed values. A feature-stratified test corpus detects both. The archive retains source bytes and reader VM, fixes the transformer, versions it, repeats pixel, metadata, coordinate, thumbnail, and domain checks, and records the remaining unsupported feature. **Conclusion:** significant-property and rare-feature evidence is stronger than file counts.

### Example 5

**Retaining failed experiments.** A materials lab publishes only successful deposition runs. Later researchers infer a broad stable temperature window, unaware that failed runs were deleted. A revised system retains compact parameters, equipment state, failure category, quality evidence, and disposal policy for every run while keeping large transient video only for selected anomalies. **Conclusion:** proportional negative-result metadata prevents a preservation policy from manufacturing survivorship bias.

### Example 6

**Specimen identity survives freezer moves.** Vial “B7” moves between three freezers and is split into aliquots. If location is identity, a restored old inventory can attach results to the wrong material. The architecture assigns immutable specimen and aliquot IDs, records parentage, custody, quantity, condition, location intervals, freeze-thaw events, assay consumption, and correction history. Barcode is a carrier, not identity itself. **Conclusion:** physical custody and derivation must form part of the scientific identity graph.

### Example 7

**Sensitive longitudinal cohort.** A cohort dataset must be reusable by approved researchers but cannot be public. Metadata and aggregate discovery remain open; person-level access occurs in governed workspaces with purpose, consent version, training, expiry, query audit, and reviewed egress. Withdrawal produces a policy event propagated to active copies and future derivatives where required, while a minimal restricted record proves the action. Linkage and trained-model risks receive separate review. **Conclusion:** FAIR accessibility and privacy can coexist only through explicit authorization and derivative governance.

### Example 8

**The only maintainer retires.** A laboratory pipeline depends on one researcher’s shell history, home directory, license server, and undocumented reference table. Before retirement, an independent team reconstructs the workflow from versioned source, mirrored lawful dependencies, environment definition, reference-data identity, tests, parameters, and operational runbook. The first transfer fails on a locale-dependent parser, revealing a hidden assumption that is then fixed and recorded. **Conclusion:** succession rehearsal converts tacit knowledge into tested institutional capability.

### Example 9

**Fixity detects correlated corruption.** A faulty migration writes identically truncated files to three regions and records new digests, so all copies agree. Comparison to the signed pre-migration manifest and semantic dimension checks reveal the loss. Repair restores from an offline source; credentials and tooling for migration and manifest approval are separated. **Conclusion:** replica agreement cannot detect a common transformation defect; independent history and semantic checks are necessary.

### Example 10

**International ocean observatory.** Countries contribute sensor, vessel, laboratory, and community observations under different governance. The architecture uses federated custody and common identity/provenance profiles, but preserves local authority, licenses, sensitive species locations, Indigenous/community terms, calibration, units, uncertainty, and embargo. Versioned releases cite exact objects; cross-version queries declare mappings. A joint board governs schema and succession, while domain scientists review scientific compatibility. **Conclusion:** durable interoperability requires shared minimum semantics plus legitimate federated governance, not forced central ownership.

## Cross-Program Connections

- [Software Engineering: Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns build, deployment, and operational reproducibility practices.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns storage, transaction, indexing, and engine migration mechanisms.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns scientific pipeline execution, quality, and operational lineage.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns vocabularies, metadata, governance, master identity, and enterprise data lifecycle.
- [Large-Scale Data Systems](../../21-large-scale-data-systems-engineering/ROADMAP.md) owns petabyte-scale processing and storage implementations.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns cryptographic, access-control, privacy, and adversarial mechanisms.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns instrument, physical sample, stakeholder, and mission lifecycle integration.
- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) owns storage-service and recovery infrastructure implementation.

## References

1. Mark D. Wilkinson et al., “The FAIR Guiding Principles for Scientific Data Management and Stewardship,” *Scientific Data* 3, 2016. [Publisher and DOI record](https://doi.org/10.1038/sdata.2016.18).
2. CCSDS, *Reference Model for an Open Archival Information System (OAIS)*, CCSDS 650.0-M-3, Issue 3, December 2024; adopted as ISO 14721:2025, edition 3. [Active CCSDS publication](https://ccsds.org/publications/allpubs/entry/3054/) and [ISO record](https://www.iso.org/standard/87471.html). Current editions checked 2026-09-06.
3. NIST, *Research Data Framework (RDaF), Version 2.0*, NIST SP 1500-18r2, 2024. [Official publication](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/1500-18/NIST.SP.1500-18r2.html). Current project version checked 2026-09-06.
4. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 30 April 2013. [Official recommendation](https://www.w3.org/TR/2013/REC-prov-o-20130430/).
5. National Academies of Sciences, Engineering, and Medicine, *Reproducibility and Replicability in Science*, National Academies Press, 2019. [Publisher record](https://doi.org/10.17226/25303).
6. Arfon M. Smith, Daniel S. Katz, Kyle E. Niemeyer, and FORCE11 Software Citation Working Group, “Software Citation Principles,” *PeerJ Computer Science* 2:e86, 2016. [DOI record](https://doi.org/10.7717/peerj-cs.86).
7. ISO/IEC, *ISO/IEC 18670:2025: SoftWare Hash IDentifier (SWHID) Specification V1.2*, April 2025. [ISO record](https://www.iso.org/standard/89985.html). Published status and scope checked 2026-09-06.
8. DataCite Metadata Working Group, *DataCite Metadata Schema Documentation*, Version 4.6, 2025. [Official version update](https://datacite-metadata-schema.readthedocs.io/en/4.6/introduction/version-update/). Current documentation checked 2026-09-06.
9. NIST, “SI Units” and *Guide for the Use of the International System of Units*. [Current SI portal](https://www.nist.gov/pml/owm/metric-si/si-units) and [SP 811 status page](https://www.nist.gov/pml/special-publication-811). Currency limitations checked 2026-09-06.
10. Reproducible Builds Project, “Definitions.” [Official project definition](https://reproducible-builds.org/docs/definition/). Current definition checked 2026-09-06.
11. The HDF Group, *HDF5 File Format Specification* and data model documentation. [Official documentation portal](https://docs.hdfgroup.org/hdf5/develop/). Current documentation location checked 2026-09-06.
12. David S. H. Rosenthal et al., “Requirements for Digital Preservation Systems: A Bottom-Up Approach,” *D-Lib Magazine* 11(11), 2005. [DOI record](https://doi.org/10.1045/november2005-rosenthal).

## Exercises

### Exercise 1

**Separate preservation claims.** A repository says, “The checksum matches, so this 18-year-old dataset is authentic, correct, and reproducible.” Separate the claims that are actually supported, unsupported, or require additional evidence.

### Exercise 2

**Recompute capacity and risk bounds.** A 4 PB logical collection grows 6% annually for 15 years and uses three full copies. Compute the projected logical and raw copied volume before overhead. For $N=10^{12}$ bits and per-bit alteration probability bounded by $10^{-15}$ over one interval, compute the union-bound upper limit and explain why three copies do not automatically cube the real risk.

### Exercise 3

**Diagnose a failed reproduction.** A containerized analysis now produces a 0.7% different estimate. The source commit and data filename match, but the image tag was mutable, the dataset was updated in place, and GPU reduction order changed. Diagnose the evidence gaps and specify a repair plan that does not retroactively declare either result correct.

### Exercise 4

**Design a format migration gate.** Design gates for migrating 25 years of geospatial observations from a proprietary format. Cover identity, source retention, significant properties, rare features, units, coordinates, missingness, transform provenance, comparison, rollback, and approval.

### Exercise 5

**Transfer to a century-scale seed observatory.** Design the architecture for a 100-year international seed and crop observatory combining physical specimens, genomes, field measurements, Indigenous and farmer knowledge, climate data, analysis software, and publications. Address the full preservation tuple, governance, identity, uncertainty, correction, access, succession, cost, migration, and future-user testing.

## Answers to the Exercises

### Answer 1

A matching checksum supports only that the current bit sequence equals the sequence represented by the chosen digest, assuming the association and digest record are trustworthy. Authenticity additionally needs provenance, custody, signatures or protected manifests, and authority. Correctness needs domain validation, calibration, units, protocol, and review. Reproducibility needs exact inputs, code, environment, parameters, nondeterminism, and an oracle; even successful reproduction would not prove scientific validity or independent replication. Interpretation also requires format and semantic representation information. Credit requires keeping these claim types separate.

### Answer 2

Logical volume is $4(1.06)^{15}\approx9.586$ PB. Three full copies require about $28.758$ PB before indexes, parity, staging, metadata, and migration space. The union bound is $Np=10^{12}\cdot10^{-15}=10^{-3}$. Cubing to $10^{-9}$ would require independent whole-copy loss events with appropriate identical probability; shared software, credentials, institution, format, migration, catalog, or hazard introduces common-cause failure. A strong plan diversifies failure domains, protects historic manifests, scrubs, repairs, and tests interpretation as well as adding copies. Small numeric rounding differences are acceptable if the method and limitations are correct.

### Answer 3

Matching a source commit and filename does not identify the container bytes, dependency closure, immutable dataset version, or hardware execution semantics. Preserve both observed results and provenance. Resolve the historical image digest if possible; identify the old dataset from snapshots, digests, or publication deposits; recover parameters and GPU/library versions; and define whether bitwise, numeric, or inferential equivalence was promised. Rebuild in controlled environments, run sensitivity across reduction orders, and compare to a predeclared scientific tolerance or independent reference. If artifacts are unavailable, label the original incompletely reproducible. Correction is a new linked result after qualified review, not an overwrite or tolerance invented after seeing 0.7%.

### Answer 4

Assign immutable IDs and fixity to every source object and retain source bytes plus a lawful reference reader. Define significant properties before conversion: arrays, types, precision, coordinate reference system and axis order, time basis, units, missing values, quality flags, compression behavior, metadata, relationships, and domain rendering. Stratify a corpus by instrument, era, rare extension, largest object, corrupt input, coordinate boundary, missingness, and numeric extremes. Version and identify transform source, build, dependencies, configuration, and operator.

Produce destination objects with new IDs linked to sources. Gate on schema validation, counts, dimensions, keyed numeric comparison under declared exactness/tolerance, coordinates, units, missingness, metadata, rare-feature behavior, independent readers, domain visualizations, and qualified geospatial review. Record every loss and quarantine unsupported files. Rehearse interrupted batches and catalog recovery. Rollback keeps current readers on source until evidence passes; disposal occurs only after a governed retention period and preservation authority approves. File-count equality alone fails.

### Answer 5

Define immutable accession records for each seed lot, plant, aliquot, field plot, observation, genome, interview or knowledge assertion, dataset release, analysis, and publication. Physical identity records parentage, custody, quantity, viability, storage history, sampling, consumption, and location intervals without using shelf position as identity. Measurements carry protocol, unit, reference frame, uncertainty, instrument and calibration; genomes retain reference assembly and pipeline provenance. Corrections supersede rather than overwrite. Exact releases link raw observations, transformations, code, dependencies, parameters, environment, nondeterminism, figures, and claims.

Governance must be federated. Indigenous nations, farmers, specimen custodians, scientists, funders, and lawful authorities define consent, collective authority, benefit, embargo, sensitive location, access, license, withdrawal, publication, and derivative-use policy. FAIR discovery does not imply open download. Governed compute may keep sensitive data in jurisdiction while exporting reviewed aggregates and provenance. Preserve multilingual terminology and version mappings without flattening distinct knowledge systems into one ontology.

Use durable documented formats plus original bytes, content and persistent identifiers, protected manifests, geographically and administratively diverse copies, fixity/repair, catalog rebuild, and tested restore. Forecast compound growth, replicas, curation, physical storage, viability testing, migration headroom, and skilled staff; appraise replaceable derivatives under visible policy. Version formats, vocabularies, units, taxonomies, consent, and software; every migration retains source, transform, significant-property comparison, limitations, and approval. A funded custody compact defines key succession, institutional transfer, supplier exit, disaster recovery, and lawful disposal.

Future-user exercises recur across generations: an independent qualified team must locate an exact release, obtain legitimate access, interpret specimen and measurement meaning, trace a published conclusion, rebuild or emulate analysis, reproduce within a declared oracle, identify uncertainty and governance limits, and cite the exact versions. Physical germination or independent field replication tests different claims from computational reproduction. A complete design preserves both scientific interpretability and legitimate community authority; it does not promise that software alone can keep a century-long scientific claim true.
