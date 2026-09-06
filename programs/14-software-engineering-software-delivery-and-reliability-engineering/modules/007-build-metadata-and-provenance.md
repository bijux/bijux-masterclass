---
module_id: SDRE-007
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 7
title: Build Metadata and Provenance
status: complete
last_verified: 2026-09-06
---

# Build Metadata and Provenance

## One-Page Review

### Governing question

What evidence must accompany an artifact so a consumer can determine what produced it, from which resolved inputs, under which build-platform identity, and whether those facts satisfy policy?

### Essential definitions

- **build metadata** is recorded data about a build definition or one execution, such as source revision, parameters, builder identity, timestamps, and dependency digests;
- **provenance** is build metadata structured as a claim that identified subjects were produced by an identified build from identified inputs;
- an **attestation** is authenticated metadata about one or more subjects;
- a **subject** is an output artifact named by an immutable identifier, normally a cryptographic digest;
- a **predicate** contains the type-specific claim, while a **statement** binds that predicate type and content to subjects;
- an **envelope** authenticates serialized statement bytes; authentication does not make the predicate true;
- a **build type** identifies the parameterized build template and gives semantics to its parameters;
- **external parameters** are top-level inputs controlled outside the trusted build platform and requiring downstream policy checks;
- **resolved dependencies** record immutable identities for artifacts actually selected from references;
- a **builder identity** names the build platform and therefore a trust boundary, not merely an executable's product name;
- an **invocation identity** correlates one build execution with logs and operational records;
- **completeness**, **accuracy**, **authenticity**, and **policy acceptance** are separate evidence properties.

### Central model, mechanism, or theorem

Model one provenance statement as

$$
P=(S,T,X,D,B,I,Y),
$$

where $S$ is the subject digest set, $T$ the build type, $X$ external parameters, $D$ resolved dependencies, $B$ builder identity, $I$ invocation metadata, and $Y$ selected byproducts. A verifier accepts an artifact $a$ under policy $\Pi$ only if

$$
H(a)\in S\;\land\;Auth(P)\;\land\;Fresh(P)\;\land\;\Pi(T,X,D,B)=accept.
$$

Each conjunct answers a different question. A valid signature over a provenance statement with the wrong subject digest, unapproved branch, missing dependency, or untrusted builder must still fail.

### Critical invariants

- the trusted control plane generates provenance from observations it controls;
- every released artifact is bound by digest as a subject;
- mutable source and dependency references are recorded with their resolved immutable identities;
- the build type has stable documented semantics;
- every externally controlled parameter that can affect the build is exposed to policy;
- builder identity denotes the complete trust boundary relevant to the claim;
- provenance and artifacts are distributed and retained together without embedding secrets;
- consumers authenticate the envelope before trusting its statement;
- consumers verify subject, signer-builder authorization, parameters, dependencies, and applicable freshness or revocation policy;
- absence and empty values are interpreted only according to the selected schema;
- provenance is evidence about production, not proof of source correctness, artifact safety, reproducibility, or authorization to deploy.

### Common failures

Common failures include recording a branch without its commit, trusting tenant-generated metadata as platform observation, signing after an attacker can replace the predicate, naming a generic builder that hides weaker modes, accepting any valid signer for any builder, failing to bind every output, omitting downloaded scripts, confusing logs with provenance, embedding tokens or personal data, treating timestamps as source identity, accepting unexpected parameters, ignoring predicate versions, losing provenance during promotion, and treating a successful rebuild or signature as universal correctness.

### Compact example

A release artifact has digest `sha256:a1`. Its provenance names that digest as subject, a documented build type, requested source `refs/tags/v2.4.0`, resolved source commit `c7`, dependency digest `d9`, builder `https://build.example/isolated/v1`, and invocation `run-418`. The envelope authenticates the statement. Policy accepts only release tags, exact allowed builder/signer pairs, and a complete dependency set. If the same statement accompanies artifact `sha256:a2`, or if the parameter is `refs/heads/main`, verification fails even though the signature remains valid.

### Connections

[SDRE-003](003-reproducible-and-hermetic-builds.md) defines reproducibility and controlled inputs. [SDRE-006](006-semantic-versioning-and-release-identity.md) defines exact release identity. [SDRE-008](../ROADMAP.md) next records component composition, while SDRE-009 authenticates artifact and evidence bytes.

## Governing Question

An artifact digest answers “which bytes?” It does not answer “who caused these bytes to exist, using what build definition and resolved inputs?” A log may contain clues, but logs are often mutable, verbose, access-controlled, or generated partly by untrusted build steps. Release decisions need a bounded, machine-readable claim connected to exact outputs.

Build provenance provides that connection. It turns selected observations from the build control plane into a typed statement about digest-identified subjects. A consumer then authenticates the statement and evaluates its contents against an explicit policy. The important engineering work is not merely serializing fields; it is deciding which component observed each fact, what that observer is trusted to assert, and what a verifier must reject.

## Why This Matters

Without provenance, an organization may know that a package exists but not whether it came from the reviewed source, an approved release workflow, a maintained builder, or a developer laptop. Incident responders cannot reliably find outputs affected by one compromised build dependency. Rebuilders cannot determine which environment mattered. Policy engines fall back to labels and repository locations that can be moved.

SLSA 1.2 defines provenance as verifiable information describing where, when, and how software artifacts were produced [1]. Its recommended build-provenance predicate models a build platform producing digest-identified subjects through a build definition [2]. The in-toto Attestation Framework supplies distinct predicate, statement, envelope, and bundle layers [3]. These layers prevent a useful category error: the predicate expresses a claim, the statement binds it to subjects, and the envelope authenticates bytes. None alone establishes that the build was safe or the source was correct.

## Prerequisites and Retrieval

Retrieve source identity, build identity, artifact digest, release identity, content-addressed storage, dependency resolution, lockfile, hermeticity, reproducibility, cryptographic hash, signature, authentication, authorization, trust boundary, policy, principal, immutable reference, mutable reference, parameter, environment, timestamp, log, retention, and revocation.

From SDRE-001 retrieve the source-to-build-to-artifact identity chain. From SDRE-002 retrieve declared versus resolved dependencies. From SDRE-003 retrieve the relevant-input set and the limits of reproducibility. From SDRE-005 retrieve immutable repository coordinates. From SDRE-006 retrieve release manifests and create-once releases.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish ordinary build metadata, provenance, attestations, signatures, logs, and SBOMs;
2. model provenance subjects, build definitions, run details, and trust boundaries;
3. classify external parameters, internal parameters, resolved dependencies, and byproducts;
4. bind provenance to exact output digests and immutable source identities;
5. explain why builder identity represents a platform trust base rather than a tool name;
6. design provenance generation outside tenant-controlled build steps;
7. authenticate and parse an attestation without confusing authenticity with truth;
8. evaluate provenance against signer, builder, source, parameter, and dependency policy;
9. minimize sensitive metadata while preserving audit and reproducibility value;
10. diagnose missing, ambiguous, forged, stale, or misbound provenance.

## Core Exposition

**Start with questions, not fields.** Useful build metadata supports a decision. A developer diagnosing a failure needs the invocation identifier and logs. A rebuilder needs source, build instructions, toolchain, and relevant environment. A release gate needs subject digest, source revision, build type, externally controlled parameters, builder identity, and authentication. A vulnerability investigation needs resolved dependencies. Recording every environment variable is neither necessary nor safe; recording too little makes evidence non-actionable.

Ordinary metadata becomes provenance when it makes a structured production claim about identified outputs. A timestamp in `version --verbose` is metadata. A statement that builder $B$ executed build definition $(T,X,D)$ and produced subjects $S$ is provenance. Authentication can make it an attestation. The claim remains bounded by its schema, producer, and trust assumptions.

**Bind the subject first.** A verifier starts with bytes in hand and recomputes their digest. The provenance subject must contain that digest under an accepted algorithm and representation boundary. A matching filename is insufficient: names move and collide. Multi-output builds either name all release-relevant subjects or bind a manifest that transitively identifies them. Otherwise evidence for one binary may be incorrectly applied to another platform variant, debug image, or source archive.

**Separate requested from resolved inputs.** A request such as `repository=example/payments, ref=refs/tags/v2.4.0` is an external parameter. The corresponding immutable commit is a resolved dependency. Both matter: policy may require a release tag, while incident analysis needs the exact commit fetched. SLSA's build-provenance model treats external parameters as untrusted inputs that downstream consumers must verify, and records resolved artifacts separately [2].

A floating dependency URL, package range, container tag, downloaded script, compiler image, or generated configuration can affect output. Resolve it to an immutable identity and record it if the chosen schema and completeness claim include that influence. If a dependency cannot be observed, narrow the claim rather than inventing completeness.

**Give the build type semantics.** A build type is not an arbitrary label such as `ci`. It identifies a documented parameterized template: what inputs mean, which top-level parameters exist, how to invoke it, and what platform behavior is implicit. Stable semantics let a verifier know that `ref`, `target`, and `release` exhaust the externally controlled interface. If client-side code transforms versioned YAML into hidden ephemeral JSON, policy cannot reconstruct what actually reached the builder. Prefer the trusted platform retrieving versioned configuration itself.

**Place observation in the right trust boundary.** Tenant-controlled build steps can emit useful diagnostic metadata, but a compromised step can lie. Claims used to resist that step must be generated from the control plane, which observes the invocation and output digests without exposing its signing authority to the workload. SLSA Build L1 requires provenance but permits it to be incomplete or unsigned; Build L2 adds a hosted platform that authenticates its own provenance; Build L3 additionally requires stronger isolation and keeps provenance-signing secrets inaccessible to user-defined steps [4]. A level is a package-and-platform claim under the precise versioned requirements, not a badge inferred from one JSON file.

Builder identity must distinguish modes with materially different trust. A hosted isolated pool and a self-hosted privileged runner should not share one identity merely because both run the same automation product. The identity denotes the transitive trusted platform—software, configuration, infrastructure, administrators, and relevant control plane—as documented for the consumer.

**Keep definition and execution distinct.** The build definition describes the intended template and top-level inputs. Run details describe one execution: builder, invocation identity, times, and selected byproducts. An invocation identifier is valuable for locating logs, but it should remain opaque unless the builder documentation promises structure. Timestamps help sequence and investigate runs; they do not identify source and should not become uncontrolled inputs to output bytes.

Byproducts are selected supporting artifacts, such as an evaluated-configuration digest or a retained test report, that aid investigation without being primary subjects. Provenance should not enumerate every temporary file. Logs remain operational records with their own confidentiality and retention needs; they are not automatically authenticated just because provenance contains a link.

**Use typed attestation layers.** In in-toto, a predicate carries type-specific fields, a statement names subjects and `predicateType`, and an envelope handles authentication [3]. Consumers parse according to the authenticated predicate type rather than an unauthenticated filename or media-type hint. The current framework specification identifies version 1.2 as its latest tagged line as checked on 2026-09-06 [3]. SLSA build provenance uses the major-version predicate URI `https://slsa.dev/provenance/v1`; compatible minor schema changes retain that URI, so parsers must follow its forward-compatibility rules [2].

DSSE signs a pre-authentication encoding of payload type and payload, avoiding dependence on JSON canonicalization and preventing the same signature from being reinterpreted under another payload type [5]. A real verifier still needs cryptographic implementation, trusted identities, validity and revocation policy, and correct parsing. This chapter's local code deliberately performs content and policy checks only; it does not simulate authentication.

**Verify in a safe order.** Obtain artifact and provenance from their distribution convention. Recompute the artifact digest. Authenticate the envelope using trusted verification material. Parse the authenticated statement with a supported schema. Match the artifact to a subject. Check signer-builder authorization rather than accepting any valid signer. Evaluate build type, external parameters, resolved source and dependencies, builder mode, and completeness claims. Apply time, revocation, and policy-version rules where required. Return a structured failure, not a Boolean with no reason.

The logical order prevents confused-deputy failures. Parsing unauthenticated predicates before imposing resource limits can expose the verifier. Trusting a signer without checking its authority for the claimed builder lets one platform impersonate another. Checking only a builder name admits an unapproved source branch. Checking only source admits a privileged parameter such as `skip_tests=true`.

**Preserve evidence as a graph.** Release identity should link artifact digests, provenance statements, signatures or transparency evidence, SBOMs, test evidence, and policy decisions. Promotion moves an exact release and its evidence graph; it does not regenerate provenance for unchanged bytes. Retention must preserve historical predicates and the verification material or trusted timestamps needed to interpret them under the organization's policy.

**Control disclosure.** Provenance is often distributed widely. Do not include credentials, raw environment dumps, private repository URLs, personal data, or secret-bearing command lines. Prefer stable resource identifiers and digests. Put restricted logs behind access control and reference them with an invocation identity. Apply data minimization without deleting fields required for the stated verification claim.

The Reproducible Builds project recommends defining or recording relevant build-environment information and publishing a build-information product alongside artifacts [6]. That goal overlaps with provenance but is not identical: a reproducibility record optimizes rebuilding, while security provenance optimizes attributable policy verification. One format can serve both only when its fields, producer, authentication, and completeness are adequate for both purposes.

## Definitions and Notation

- $a$: artifact bytes presented to the verifier;
- $H(a)$: digest of $a$ under an accepted algorithm and byte boundary;
- $S$: set of subject resource descriptors;
- $T$: build type with documented semantics;
- $X$: externally controlled top-level parameters;
- $D$: resolved dependency descriptors;
- $B$: builder identity and corresponding trust boundary;
- $I$: invocation metadata;
- $Y$: selected byproducts;
- $P=(S,T,X,D,B,I,Y)$: parsed provenance claim;
- $Auth(P)$: authenticated envelope and authorized signer-builder relation;
- $Fresh(P)$: applicable validity, revocation, and time policy succeeds;
- $\Pi(T,X,D,B)$: consumer policy over build facts.

For an expected source revision $d_s$, allowed builder set $B_A$, permitted build type $T_A$, and required dependency set $D_R$, define

$$
\Pi(T,X,D,B)=accept
$$

only when $T\in T_A$, $B\in B_A$, $X$ contains no unexpected policy-relevant fields, the resolved source equals $d_s$, and $D_R\subseteq D$. The subset condition expresses a required minimum; claiming complete dependency capture is a stronger assertion needing its own evidence.

## Mechanisms, Invariants, or Proof Structure

**Subject-binding proposition.** Suppose the verifier recomputes $H(a)=d$, accepts only a collision-resistant digest algorithm for the artifact boundary, and finds $d$ in the authenticated subject set $S$. Then the attestation applies to the presented bytes up to the digest assumption. Filename equality alone cannot establish this result.

**Conjunctive acceptance.** Let acceptance be $M\land A\land F\land Q$, where $M$ is subject match, $A$ authentication and authority, $F$ freshness, and $Q$ content policy. Making any one term true cannot compensate for a false term. Therefore “the signature verifies” is insufficient when the artifact mismatches or policy rejects the inputs.

**Information-flow invariant.** A claim intended to constrain tenant-controlled build code must not derive solely from values supplied by that code. The trusted control plane independently observes request, resolved inputs where supported, builder mode, and output digests, then constructs and authenticates provenance after the outputs are finalized.

**Executable policy model.** The following bounded program checks subject and content policy on already authenticated data. It intentionally does not parse DSSE, verify signatures, fetch resources, or claim SLSA conformance.

<!-- bijux-verify: {"id":"check-provenance-content-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=True\nsubject_mismatch=False\nunapproved_branch=False\nmissing_dependency=False\nuntrusted_builder=False\nauthenticity_proven=False\n","stderr":""}} -->
```python
EXPECTED = {
    "subject": "sha256:a1",
    "builder": "https://build.example/isolated/v1",
    "build_type": "https://build.example/types/release/v1",
    "source": "git:c7",
    "dependency": "sha256:d9",
}

statement = {
    "subjects": {"sha256:a1"},
    "build_type": "https://build.example/types/release/v1",
    "external": {"ref": "refs/tags/v2.4.0"},
    "resolved": {"git:c7", "sha256:d9"},
    "builder": "https://build.example/isolated/v1",
}

def content_policy(p):
    return (
        EXPECTED["subject"] in p["subjects"]
        and p["builder"] == EXPECTED["builder"]
        and p["build_type"] == EXPECTED["build_type"]
        and p["external"] == {"ref": "refs/tags/v2.4.0"}
        and EXPECTED["source"] in p["resolved"]
        and EXPECTED["dependency"] in p["resolved"]
    )

def changed(path, value):
    return statement | {path: value}

print(f"accepted={content_policy(statement)}")
print(f"subject_mismatch={content_policy(changed('subjects', {'sha256:a2'}))}")
print(f"unapproved_branch={content_policy(changed('external', {'ref': 'refs/heads/main'}))}")
print(f"missing_dependency={content_policy(changed('resolved', {'git:c7'}))}")
print(f"untrusted_builder={content_policy(changed('builder', 'https://build.example/dev/v1'))}")
print("authenticity_proven=False")
```

## Alternatives and Trade-Offs

**Embedded versus detached metadata.** Embedded metadata travels with an artifact but changes its bytes and may expose details at runtime. Detached provenance can cover immutable subjects without modifying them, but distribution and retention must keep the graph discoverable.

**Minimal versus rich provenance.** Minimal fields reduce disclosure and verifier complexity. Rich resolved dependencies and environment details improve incident analysis and reproducibility. Define use cases, classify data, and record the smallest sufficient claim rather than dumping the environment.

**Self-reported versus control-plane generated.** Self-reporting is easy and useful for debugging. Control-plane generation supports claims against a compromised workload. Preserve both if needed, but label their producers and never promote self-assertion into a stronger trust claim.

**One broad versus mode-specific builder identity.** A broad identity simplifies policy but imports every mode into one trust base. Distinct identities for isolated, privileged, self-hosted, and experimental modes allow precise authorization at the cost of more governance.

**Complete capture versus best effort.** Complete external parameters can be an enforceable interface property. Transitive dependencies may remain best effort when dynamic behavior escapes observation. Reject unsupported completeness claims and improve instrumentation rather than filling gaps with guessed data.

**Rebuild evidence versus original-build provenance.** An independent matching rebuild gives evidence about reproducibility and unexpected build-time variation. Original provenance gives evidence about the actual released build. The two reinforce each other but answer different questions.

## Failure Modes and Misconceptions

- **“Metadata is provenance.”** Metadata becomes provenance only through a structured claim about identified production outputs.
- **“A signature makes the claim true.”** It authenticates bytes and signer under explicit trust assumptions.
- **“The artifact name binds the subject.”** Recompute and compare the digest.
- **“A branch is source identity.”** Record the resolved immutable revision.
- **“The workflow file describes what ran.”** Client-side expansion and external parameters may change execution.
- **“Builder means compiler.”** It denotes the relevant platform trust boundary.
- **“Any trusted signer can attest any builder.”** Authorize signer-builder pairs.
- **“Tenant-generated provenance resists a compromised tenant.”** It can lie unless independently observed.
- **“More fields are always better.”** Excess metadata leaks secrets and complicates verification.
- **“A timestamp identifies source.”** It only records a claimed time under producer assumptions.
- **“Logs are attestations.”** Logs need separate integrity, access, and retention controls.
- **“Resolved dependencies are automatically complete.”** Completeness depends on observation and schema guarantees.
- **“One subject covers the release.”** Multi-output boundaries must be explicit or transitively bound.
- **“Provenance proves reproducibility.”** A rebuild comparison tests that different claim.
- **“A SLSA-shaped document has a SLSA level.”** Requirements apply to producer, platform, consumer, and distribution behavior.

## Worked Examples

### Example 1

**Requested tag and resolved commit.** A build request contains `ref=refs/tags/v2.4.0`; the control plane resolves it to commit `c7`. Policy checks that the request used a release tag, while incident analysis and rebuild use `c7`. Recording only the tag permits later movement; recording only the commit loses the requested-policy fact. **Conclusion:** keep external parameter and immutable resolution as distinct fields.

### Example 2

**Subject mismatch.** Provenance authenticates successfully and names `sha256:a1`, but the downloaded binary recomputes to `sha256:a2`. The verifier stops before accepting content policy because the claim is about other bytes. A matching filename and repository path do not repair the mismatch. **Conclusion:** authentication without subject binding is irrelevant to the presented artifact.

### Example 3

**Hidden skip-tests parameter.** A release build type documents only `ref` and `target`, but the platform accepts client-supplied `skip_tests=true` outside recorded parameters. An attacker can influence the build without policy visibility. The interface is redesigned so every influential external value is in `externalParameters` and unexpected fields are rejected. **Conclusion:** parameter completeness is a security boundary.

### Example 4

**Downloaded script.** A versioned build script fetches `install.sh` from a mutable URL and executes it. Source identity alone omits an input capable of changing output. The platform pins, verifies, and records the script digest as a resolved dependency—or forbids the fetch. **Conclusion:** executable network inputs belong in the dependency claim.

### Example 5

**Builder-mode confusion.** Hosted isolated runners and a privileged self-hosted runner share `builder.id=ci/v1`. A policy intended for isolated builds cannot distinguish them. The platform assigns separate documented identities and signer authorization, then rejects releases from the privileged mode. **Conclusion:** builder identity must reflect security-relevant modes.

### Example 6

**Self-attestation.** A build step writes a JSON file claiming tests passed and signs it with a key mounted in that step. Compromised build code can alter both artifact and claim. Moving observation and signing into the control plane, with the key inaccessible to the workload, supports a stronger claim; the tenant report remains a byproduct. **Conclusion:** provenance strength depends on who observes and authenticates facts.

### Example 7

**Multi-platform release.** One release contains Linux AMD64, Linux ARM64, and macOS binaries. Provenance for only the AMD64 digest cannot be applied to the others. The build emits one statement with all finalized subject digests or separate statements linked by the immutable release manifest. **Conclusion:** declare the subject boundary for every deliverable.

### Example 8

**Independent rebuild.** Original provenance says source `c7`, toolchain image `t3`, and output `a1`. A separate trusted rebuilder uses the recorded inputs and also produces `a1`. This increases evidence that relevant inputs were captured and output is reproducible, but it does not prove source safety or that both builders lack common compromise. **Conclusion:** rebuild evidence complements rather than replaces provenance.

### Example 9

**Secret leakage.** A pipeline records its full command and environment, including a repository token, inside public provenance. Authentication preserves the leak. The schema instead records a non-secret credential-class identifier and approved repository URI; sensitive logs remain access-controlled. **Conclusion:** integrity controls do not provide confidentiality.

### Example 10

**Incident query.** A compiler image digest is later found compromised. The organization queries retained provenance for `resolvedDependencies` containing that digest, identifies affected release subjects, blocks promotion, and rebuilds from verified inputs. Builds whose dependency capture was labeled best effort require broader investigation. **Conclusion:** provenance supports scoped response only to the extent its recorded graph is accurate and complete.

## Cross-Program Connections

- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns signing trust, key management, threat modeling, and adversarial verification.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns the internal build platform as a product and its tenant/control-plane boundary.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns verifier interfaces and typed policy-result APIs.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns durable processing and query of provenance event collections.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns trust-boundary and interface design across the evidence graph.

## References

1. Supply-chain Levels for Software Artifacts, *SLSA Specification 1.2: Provenance*, approved specification. [Official specification](https://slsa.dev/spec/v1.2/provenance). Checked 2026-09-06.
2. Supply-chain Levels for Software Artifacts, *SLSA Specification 1.2: Build Provenance*, predicate, model, schema, and verification guidance. [Official specification](https://slsa.dev/spec/v1.2/build-provenance). Checked 2026-09-06.
3. in-toto Project, *in-toto Attestation Framework Specification 1.2*, predicate, statement, envelope, and bundle layers. [Official specification repository](https://github.com/in-toto/attestation/blob/v1.2.0/spec/README.md). Checked 2026-09-06.
4. Supply-chain Levels for Software Artifacts, *SLSA Specification 1.2: Build Track Basics*, Build L1–L3 requirements and limits. [Official specification](https://slsa.dev/spec/v1.2/build-track-basics). Checked 2026-09-06.
5. Secure Systems Lab, *Dead Simple Signing Envelope Protocol 1.0*, payload-type binding and pre-authentication encoding. [Official protocol](https://github.com/secure-systems-lab/dsse/blob/v1.0.0/protocol.md). Checked 2026-09-06.
6. Reproducible Builds Project, “Recording the Build Environment,” build-information scope and distribution. [Project documentation](https://reproducible-builds.org/docs/recording/). Checked 2026-09-06.
## Exercises

### Exercise 1

**Classify evidence.** Classify an artifact digest, CI log, source commit, build timestamp, SBOM, signed statement, and release approval as identity, metadata, provenance, attestation, composition, or policy decision. Explain overlaps without collapsing them.

### Exercise 2

**Trace verification.** Given artifact `a2`, an authenticated statement naming `a2`, requested tag `v3.1.0`, resolved commit `c8`, dependency `d4`, and builder `isolated/v2`, trace acceptance under a policy requiring those exact facts and an authorized signer-builder pair. Show where each failure would stop.

### Exercise 3

**Diagnose weak provenance.** A pipeline's final step reads environment variables, generates provenance, and signs it with a workspace key. Identify unsupported claims and redesign the observation, key custody, output finalization, and failure reporting.

### Exercise 4

**Design a schema and policy.** Design minimal provenance for a multi-platform release built from one repository, a versioned workflow, two compiler images, and a release parameter. Include privacy, distribution, retention, and verifier rules.

### Exercise 5

**Transfer to firmware manufacturing.** A cloud build produces firmware, while a factory adds device-specific configuration. Design linked provenance boundaries, identities, and verification for production, field incident response, and authorized recovery.

## Answers to the Exercises

### Answer 1

An artifact digest is byte identity under an algorithm and boundary. A CI log is operational metadata unless separately structured and authenticated as a claim. A source commit is source identity, not evidence that it was used. A build timestamp is execution metadata. An SBOM is composition metadata and may be carried as an attested predicate, but it is not automatically build provenance. A signed statement is an attestation after its envelope, signer, and subject binding verify; its predicate may be provenance. Release approval is a policy decision that should bind the exact release and evidence set. One object can participate in several roles, but each role has distinct semantics and verification.

### Answer 2

First recompute $H(a)$ and require `a2`; otherwise stop with subject mismatch. Authenticate the envelope with trusted material, then require that signer to be authorized for `isolated/v2`; a valid but unauthorized signer fails. Parse the authenticated predicate type and supported schema. Require the expected build type, external parameter `v3.1.0` with no unexpected influential field, resolved source `c8`, dependency `d4`, and builder `isolated/v2`. Apply validity, revocation, and policy-version rules. Acceptance occurs only if every conjunct passes. Each failure reports its dimension so an operator does not misdiagnose policy rejection as cryptographic failure.

### Answer 3

The step can lie about inputs, tests, builder mode, timestamps, and output identity; a workspace key is readable or usable by compromised tenant code. Finalization may also be circular if provenance is generated before the artifact stops changing. Move request capture, immutable input resolution, builder-mode observation, subject hashing after finalization, and envelope creation into the trusted control plane. Keep signing authority outside the workload. Permit the step to emit explicitly labeled byproducts, validate their format, and do not elevate them into platform-observed facts. Fail closed on missing required observations and return a structured reason while retaining restricted diagnostic logs.

### Answer 4

Use subjects for every OS/architecture artifact digest or for one manifest digest that transitively fixes them. The build definition names a documented build type and release parameter. External parameters contain repository reference, target matrix, and release mode; resolved dependencies contain source commit, workflow/configuration digest, and both compiler-image digests. Run details name a mode-specific builder, invocation ID, and bounded timestamps. Do not include tokens, raw environment, or personal data.

The control plane generates and authenticates the statement after output finalization. Distribution stores it beside the immutable release manifest. Retention keeps provenance, authentication evidence, builder documentation, and policy version for the release support and incident window. Verifiers recompute subjects, authorize signer-builder pairs, reject unexpected parameters, require approved source and workflow, enforce target-to-compiler mapping, and distinguish best-effort dependency coverage from a completeness guarantee.

### Answer 5

The cloud build attests firmware subjects, source revision, toolchain and dependency digests, build type, parameters, and cloud builder. Factory personalization is a separate transformation: its provenance names the generic firmware and approved configuration template as inputs, a device-class or privacy-preserving configuration identity, the factory station or service trust boundary, and the finalized device image or installation record as subject. A signed release manifest links accepted firmware and factory-process policies.

Production verifies both links, authorized builder identities, input/output digests, configuration policy, and device applicability before activation. Field response can query affected firmware, compiler, factory mode, and configuration cohorts without exposing secrets in public evidence. Recovery uses an authorized immutable bundle and records a new installation event; it never rewrites original provenance. Device identifiers and sensitive configuration remain in access-controlled evidence while public artifacts retain non-secret digest bindings and product-level claims.
