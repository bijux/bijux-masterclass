---
module_id: SDRE-006
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 6
title: Semantic Versioning and Release Identity
status: complete
last_verified: 2026-09-06
---

# Semantic Versioning and Release Identity

## One-Page Review

### Governing question

How can a release communicate intended compatibility while remaining an unambiguous, immutable identity for exact artifacts and evidence?

### Essential definitions

- a **release** is an authorized, immutable selection of artifacts and evidence offered to consumers;
- a **version scheme** defines valid identifiers and their ordering or precedence;
- **Semantic Versioning 2.0.0** uses `MAJOR.MINOR.PATCH`, pre-release identifiers, and build metadata relative to a declared public API;
- **backward compatibility** means defined existing consumers continue to satisfy their requirements after substitution;
- **source**, **binary**, **behavioral**, **protocol**, **data**, and **operational compatibility** are different relations;
- **precedence** orders version identifiers; it does not establish compatibility or recency of bytes;
- a **pre-release** precedes its associated normal version and may not satisfy the normal version's stability expectation;
- **build metadata** distinguishes strings but is ignored by SemVer precedence;
- a **release coordinate** is an ecosystem name bound immutably to a release;
- an **artifact digest** identifies exact bytes under a named algorithm and boundary;
- a **release manifest** binds one release identity to its artifact digests, source, interfaces, target matrix, and evidence.

### Central model, mechanism, or theorem

Keep three concepts separate:

$$
version\ signal\;v,\qquad release\ identity\;r,\qquad artifact\ set\;A(r).
$$

SemVer chooses the next core from the observed change to the declared public API: incompatible change implies major; compatible addition or deprecation implies minor; compatible bug fix implies patch. This is a producer assertion requiring evidence, not a theorem derived from the numerals.

Release identity must additionally satisfy

$$
r\mapsto A(r)\quad\text{is create-once}.
$$

Two artifacts may share SemVer precedence when their strings differ only in build metadata; therefore precedence cannot serve as exact release identity.

### Critical invariants

- declare the public contract and supported consumer population before classifying change;
- define the compatibility dimension and observation boundary;
- never modify the contents of an issued version;
- bind every release coordinate to exact artifact digests and target variants;
- treat version numbers as compatibility signals, not proof;
- test representative previous consumers and documented contracts;
- record pre-release policy and never let a floating channel impersonate a release;
- keep build metadata out of precedence decisions as SemVer requires;
- give incompatible lines distinct selectable identities where the ecosystem requires it;
- preserve withdrawn or defective release identities and mark disposition rather than rewriting history;
- separate release numbering, deployment sequence, feature flags, and database migration state;
- communicate security, safety, and operational urgency outside the three numeric fields.

### Common failures

Common failures include no declared public API, calling a behavioral break “patch” because syntax is unchanged, treating any addition as compatible, overwriting a version, sorting numerically as text, treating build metadata as higher precedence, assuming `0.y.z` guarantees compatibility, deploying `latest`, using one version for several platform-specific byte sets without a manifest, coupling version to environment, skipping old-consumer tests, and believing a major bump makes a migration safe.

### Compact example

Library `ledger` 2.4.3 adds an optional method without changing existing behavior: the producer issues 2.5.0. Removing an existing method requires 3.0.0. The release manifest for 2.5.0 binds Linux and macOS artifact digests, source identity, API description, test evidence, and publication time. `2.5.0+build.7` and `2.5.0+build.9` have equal SemVer precedence; if both exist, their full release coordinates and digests must remain distinct.

### Connections

[SDRE-005](005-artifact-repositories.md) enforces immutable coordinate-to-digest mappings. [SDRE-007](../ROADMAP.md) next records how a release was built; later delivery modules promote and deploy an exact release identity.

## Governing Question

A version number must help consumers decide whether to upgrade, yet a deployment needs exact bytes. Those are different jobs. `2.3.1` can signal a compatible bug fix under a declared policy; it cannot identify a multi-platform artifact graph, prove compatibility, say which configuration ran, or establish that a repository has not changed the bytes.

Sound release engineering uses versioning as communication and immutable manifests as identity. It defines whose compatibility matters, tests the claim, publishes new identities rather than rewriting old ones, and records the digest actually selected.

## Why This Matters

Dependency solvers, operators, and automated update systems reason from version constraints. An understated break can disrupt many consumers; an unnecessary major bump fragments ecosystems. At the same time, ambiguous identity makes test, approval, rollback, vulnerability, and incident evidence impossible to bind.

SemVer 2.0.0 requires a declared public API and says issued contents must not be modified [1]. Its major/minor/patch rules are useful only when a producer classifies change honestly. The specification itself cautions that real users should still verify upgrades. Ecosystems also add their own semantics: Go uses major-version suffixes from v2 so incompatible versions receive different import paths [2], while Python and Debian define different version syntax and comparison rules [3] and [4]. Never feed one scheme to another scheme's comparator.

## Prerequisites and Retrieval

Retrieve public API, consumer, compatibility, substitution, source compatibility, binary compatibility, behavior, protocol, schema, version, precedence, release, coordinate, pre-release, build metadata, artifact digest, manifest, deprecation, support window, migration, rollback, and evidence.

From SDRE-001 retrieve source/build/artifact/release/deployment identities. From SDRE-005 retrieve create-once repository coordinates and mutable channels. From Software Architecture retrieve contract and evolution reasoning; from Testing and Quality Engineering retrieve compatibility-test design.

## Learning Objectives

After completing this module, you should be able to:

1. parse and compare core SemVer 2.0.0 identifiers;
2. distinguish version precedence from exact identity and compatibility;
3. declare a public contract and consumer scope;
4. classify compatible fixes, additions, deprecations, and breaks;
5. analyze source, binary, behavioral, protocol, data, and operational compatibility;
6. design immutable release manifests for target-specific artifacts;
7. manage pre-releases, metadata, withdrawals, and parallel major lines;
8. test compatibility claims with old consumers and adversarial cases;
9. explain when another ecosystem scheme or calendar versioning is preferable;
10. design migration and communication around an incompatible release.

## Core Exposition

**Declare the contract.** A public API is everything consumers are entitled to rely on, not merely exported function signatures. It may include error kinds, serialization, wire messages, command flags, file formats, timing or ordering guarantees, resource ceilings, supported platforms, and documented behavior. Accidental behavior may also become a de facto dependency, but a versioning policy should state how such reliance is treated.

Define the consumer population. Compatibility with a documented client may coexist with incompatibility for reflection users, plugins, subclasses, direct database readers, or callers depending on unspecified order. Avoid the universal claim “backward compatible”; name the boundary and evidence.

**Classify dimensions.** Source compatibility asks whether old source still compiles. Binary compatibility asks whether an already-built consumer links and runs. Behavioral compatibility asks whether allowed observations remain acceptable. Protocol and data compatibility concern messages and persisted state across versions. Operational compatibility covers deployment, resources, observability, and rollback.

An optional response field is wire-compatible only if old decoders ignore unknown fields as the protocol promises. A wider accepted input may still break callers if it changes error precedence. An index change may preserve API results but violate latency objectives. Compatibility is a relation under assumptions, not a property of one artifact alone.

**Apply SemVer precisely.** For stable `X>0`, incompatible public-API change increments major and resets minor and patch. Backward-compatible public functionality or deprecation increments minor and resets patch. A backward-compatible bug fix increments patch. Version zero signals initial development; it is not a promise of compatibility [1].

Pre-release identifiers follow a hyphen and have lower precedence than the associated normal version. Numeric identifiers compare numerically, numeric precedes nonnumeric, and otherwise ASCII lexical order applies. A longer pre-release list is higher only after equal preceding identifiers. Build metadata follows `+` and is ignored for precedence.

Ignoring metadata creates a deliberate equivalence class: `1.2.3+linux.1` and `1.2.3+mac.9` have equal precedence. A solver cannot use SemVer precedence alone to choose platform bytes. Put target selection in coordinates or a release manifest.

**Make the decision from change, not effort.** A one-character change can break a contract; a large internal rewrite can be patch-compatible. Security urgency does not change compatibility classification. A compatible security fix may be a patch, but advisories and policy must carry urgency because `PATCH+1` says nothing about exploitability.

A bug fix can be incompatible with clients depending on buggy behavior. First decide what the declared contract required, then assess actual consumers and transition risk. Sometimes restoring the documented behavior in a patch is defensible; sometimes ecosystem impact warrants a major transition. Record the judgment rather than claiming numerals decide it.

**Bind release identity.** Define a release record

$$
R=(name,v,s,A,P,C,E),
$$

where $s$ is source identity, $A$ maps targets to artifact digests, $P$ identifies public contract and supported platforms, $C$ records compatibility claims, and $E$ links evidence. The repository coordinate for $R$ is create-once.

A Git tag helps locate source but is not the release artifact identity. A container tag or `stable` channel is mutable selection. A digest identifies bytes but not compatibility policy. The release record binds them without collapsing their meanings.

**Test the claim.** Build a compatibility matrix from supported previous versions and consumer types. Compile old source, run old binaries, exchange old/new protocol peers, read old data with new software, exercise rollback where supported, and compare documented behavior. Test negative cases and resource behavior. Static API-diff tools are useful evidence, not complete proof.

Compatibility is generally not transitive from sampled evidence. If 1.1 works with 1.0 and 1.2 works with 1.1, a feature deprecated in 1.1 and removed improperly in 1.2 may still break 1.0 clients. Test every supported baseline or justify a stronger contract-derived argument.

**Deprecate before removal.** Mark deprecation in a minor release, document replacement, measure or solicit usage where legitimate, provide migration tooling, and define a support window. HTTP's standardized `Deprecation` response header illustrates machine-readable communication without itself removing an endpoint [5]. Removal belongs to the next incompatible identity. A major bump communicates permission to break; it does not supply a migration, dual-read strategy, or rollback path.

**Operate parallel lines.** Maintained major lines need explicit support status, independent patch sequences, and backport evidence. Go makes v2+ part of the module path so different majors can coexist [2]. Other ecosystems solve coexistence differently or not at all. Product release numbers, protocol negotiation, and database schema versions may need independent axes.

**Withdraw without erasing.** If 2.4.1 is defective, retain its identity and bytes as policy permits, mark it withdrawn or nonselectable, publish 2.4.2 or another appropriate version, and notify consumers. Reusing 2.4.1 makes lockfiles and incident evidence lie.

## Definitions and Notation

- $V$: valid version strings under a named scheme;
- $\prec$: that scheme's precedence relation;
- $C$: set of consumer/environment states in scope;
- $Obs(p,c)$: allowed observations when provider $p$ serves consumer state $c$;
- $Req(c)$: requirements of consumer state $c$;
- $p_2\succeq_C p_1$: $p_2$ is backward compatible with $p_1$ for all scoped consumers;
- $R$: immutable release record;
- $A(R)$: target-to-artifact-digest mapping for release $R$.

Define compatibility as

$$
p_2\succeq_C p_1\iff \forall c\in C:\;Obs(p_2,c)\models Req(c).
$$

The definition is only as strong as $C$, $Obs$, and $Req$. Finite tests sample this relation; they rarely prove its universal quantifier.

## Mechanisms, Invariants, or Proof Structure

**Metadata counterexample.** SemVer states build metadata is ignored for precedence [1]. Thus `1.0.0+a` and `1.0.0+b` have equal precedence although their full strings and artifact bytes may differ. Therefore version precedence is not an injective release identifier.

**Nontransitive evidence counterexample.** Let sampled client sets be $C_{01}={a}$ and $C_{12}={b}$. Passing 1.0→1.1 for $a$ and 1.1→1.2 for $b$ says nothing about 1.0 client $a$ on 1.2. Pairwise sampled success is not transitive evidence.

**Release immutability invariant.** Once coordinate $r$ maps to manifest digest $d$, later publication either repeats $d$ or fails. This preserves the interpretation of all evidence referring to $r$.

**Executable verification.** This intentionally small comparator covers the canonical ordering example and ignores build metadata. It accepts only the teaching inputs shown; it is not a full SemVer parser.

<!-- bijux-verify: {"id":"compare-semver-precedence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"core_numeric=True\nprerelease_before_release=True\nalpha_before_alpha1=True\nbeta2_before_beta11=True\nmetadata_equal=True\nidentity_distinct=True\n","stderr":""}} -->
```python
def identifiers(text):
    public = text.split("+", 1)[0]
    core, separator, pre = public.partition("-")
    return tuple(int(part) for part in core.split(".")), pre.split(".") if separator else None

def before(left, right):
    left_core, left_pre = identifiers(left)
    right_core, right_pre = identifiers(right)
    if left_core != right_core:
        return left_core < right_core
    if left_pre is None or right_pre is None:
        return left_pre is not None and right_pre is None
    for a, b in zip(left_pre, right_pre):
        if a == b:
            continue
        if a.isdigit() and b.isdigit():
            return int(a) < int(b)
        if a.isdigit() != b.isdigit():
            return a.isdigit()
        return a < b
    return len(left_pre) < len(right_pre)

def same_precedence(left, right):
    return not before(left, right) and not before(right, left)

print(f"core_numeric={before('1.9.0', '1.10.0')}")
print(f"prerelease_before_release={before('1.0.0-rc.1', '1.0.0')}")
print(f"alpha_before_alpha1={before('1.0.0-alpha', '1.0.0-alpha.1')}")
print(f"beta2_before_beta11={before('1.0.0-beta.2', '1.0.0-beta.11')}")
print(f"metadata_equal={same_precedence('1.0.0+a', '1.0.0+b')}")
print(f"identity_distinct={'1.0.0+a' != '1.0.0+b'}")
```

## Alternatives and Trade-Offs

**Semantic versus calendar versioning.** SemVer signals public-contract change; calendar versions signal release time or train. Choose the consumer question the scheme must answer and document it.

**Accretion versus replacement.** Adding new named capabilities can preserve old meanings; changing an existing meaning concentrates migration cost. Hickey's “Spec-ulation” provides a practitioner argument for favoring compatible accretion and relaxation where the domain permits [6].

**Strict versus ecosystem-native schemes.** Uniform SemVer is simple, but Python, Debian, Go, and other ecosystems define their own syntax and ordering. Native compatibility often matters more than superficial uniformity.

**One package versus coordinated suite.** One suite version simplifies communication but can release unchanged components. Independent versions reduce churn but complicate tested compatibility matrices.

**Frequent majors versus long compatibility.** Major releases permit clarity and cleanup but impose migration and ecosystem fragmentation. Compatibility layers cost maintenance but enable gradual adoption.

**Ranges versus locks.** Ranges admit compatible updates under producer claims; locks select tested identities. Use ranges during resolution and persist exact selected release/digest for reproducibility.

## Failure Modes and Misconceptions

- **“SemVer proves compatibility.”** It communicates a claim.
- **“Public API means function signatures.”** Behavior and protocols matter.
- **“Additions never break.”** Exhaustive consumers and resource limits can break.
- **“Patch means low risk.”** Small compatible changes can be operationally risky.
- **“Major means migration-safe.”** It only signals incompatibility.
- **“Version zero is compatible enough.”** SemVer grants no stability promise.
- **“Build metadata raises precedence.”** SemVer ignores it.
- **“Version order identifies bytes.”** Digests and manifests do.
- **“Git tag equals release.”** It identifies source under separate trust assumptions.
- **“Latest is a version.”** It is a mutable selection rule.
- **“Same API means same ABI.”** Linkage and layout differ.
- **“Pairwise tests prove transitivity.”** Supported baselines still matter.
- **“Security fix always means patch.”** Compatibility and urgency are separate.
- **“Withdraw means delete.”** Preserve historical identity and evidence.
- **“One number versions everything.”** Protocol, schema, and product may evolve independently.

## Worked Examples

### Example 1

**Compatible fix.** A parser rejected a documented valid input and now accepts it without changing valid results. Old-consumer tests pass, so 2.3.4→2.3.5 is a patch claim. **Conclusion:** classify against the declared contract and evidence.

### Example 2

**Behavioral break.** A method signature is unchanged but ties now sort differently, breaking documented stable order. This is incompatible and requires a major release. **Conclusion:** syntax is not the whole API.

### Example 3

**Compatible addition.** A library adds a new optional function while existing interfaces and behavior remain supported. It issues 3.2.0 from 3.1.4. **Conclusion:** backward-compatible functionality increments minor.

### Example 4

**Deprecation.** Release 4.6.0 marks an endpoint deprecated, supplies replacement and telemetry, and preserves behavior. Removal waits for 5.0.0. **Conclusion:** migration starts before the break.

### Example 5

**Unknown field.** New server adds a response field, but an old client rejects unknown fields contrary to the assumed protocol rule. Compatibility testing fails. **Conclusion:** additions depend on consumer semantics.

### Example 6

**Build metadata.** `1.4.0+linux` and `1.4.0+macos` have equal precedence but different bytes. A release manifest selects by target and digest. **Conclusion:** precedence is not identity.

### Example 7

**Version zero.** Consumers treat 0.8→0.9 as compatible, but the producer removes an API. SemVer permits instability, yet communication was poor. The project publishes an explicit pre-1.0 policy. **Conclusion:** permitted change can still impose real cost.

### Example 8

**Security backport.** Supported lines 2.x and 3.x receive compatible fixes as 2.9.8 and 3.4.2 with separate digests and advisories. **Conclusion:** urgency and maintained-line identity are explicit.

### Example 9

**Database state.** Application 6.0 writes an irreversible schema that 5.x cannot read. The major bump signals application incompatibility but the deployment also needs expand/contract migration and rollback limits. **Conclusion:** release numbering cannot implement operational safety.

### Example 10

**Defective release.** Version 7.1.1 contains wrong artifacts. The repository marks it withdrawn, publishes 7.1.2, preserves 7.1.1 evidence, and alerts known consumers. **Conclusion:** never repair an issued identity in place.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns interface boundaries and architectural evolution.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns HTTP/API compatibility and protocol evolution.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns schema and persisted-data compatibility mechanisms.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns compatibility testing and sampling validity.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns vulnerability severity and adversarial release analysis.

## References

1. Tom Preston-Werner, *Semantic Versioning 2.0.0*. [Official specification](https://semver.org/spec/v2.0.0.html). Checked 2026-09-06.
2. Go Project, *Go Modules Reference*, version and major-module-path semantics. [Official documentation](https://go.dev/ref/mod). Checked 2026-09-06.
3. Python Packaging Authority, “Version Specifiers,” current packaging specification derived from PEP 440. [Official specification](https://packaging.python.org/en/latest/specifications/version-specifiers/). Checked 2026-09-06.
4. Debian Project, *Debian Policy Manual 4.7.4.1*, section 5.6.12, “Version.” [Official policy](https://www.debian.org/doc/debian-policy/ch-controlfields.html#version). Checked 2026-09-06.
5. David Orchard, Mark Nottingham, and Jeffrey Mogul, “HTTP API Deprecation,” RFC 9745, March 2025. [RFC Editor](https://www.rfc-editor.org/rfc/rfc9745.html).
6. Rich Hickey, “Spec-ulation,” 2016, used for the professional distinction between accretion, relaxation, and breaking change. [Author presentation record](https://www.infoq.com/presentations/speculation/).

## Exercises

### Exercise 1

**Compare identifiers.** Order `1.0.0-alpha`, `1.0.0-alpha.2`, `1.0.0-alpha.10`, `1.0.0-beta`, `1.0.0`, and `1.0.0+build.7`; explain equal precedence and distinct identity.

### Exercise 2

**Classify changes.** Classify removing a function, adding an optional function, correcting documented behavior, changing error precedence, deprecating an endpoint, and changing only build tooling. State missing assumptions.

### Exercise 3

**Diagnose a bad minor.** Version 3.6.0 was declared compatible but old clients fail. Design evidence collection, containment, correction, version choice, and communication.

### Exercise 4

**Design release identity.** Define a release manifest and compatibility matrix for a library shipped as source, Linux binaries, macOS binaries, and an OCI image across two supported major lines.

### Exercise 5

**Transfer to a device protocol.** Version a controller, device firmware, wire protocol, configuration schema, and deployment bundle that must support rolling upgrades and bounded rollback.

## Answers to the Exercises

### Answer 1

The order is `alpha < alpha.2 < alpha.10 < beta < 1.0.0`. Numeric pre-release fields compare numerically, not lexically; a longer list follows its equal prefix; nonnumeric fields compare by ASCII rules; a normal release follows its pre-releases. `1.0.0+build.7` has equal precedence to `1.0.0` because build metadata is ignored, but the strings and possibly artifacts are distinct. Therefore a solver may treat their precedence equally while a release system still needs full coordinates and digests.

### Answer 2

Removing a declared function is major. Adding an optional function is minor only if it does not break exhaustive matching, namespace constraints, performance, or other contract. Correcting documented behavior is normally patch-compatible, but actual reliance and transition risk need review. Changing observable error precedence is major if the contract or supported consumers depend on it. Deprecation is minor under SemVer. Tool-only change can be patch when public outputs remain compatible, but it still creates new artifact identity.

Missing assumptions include stable major greater than zero, declared API, consumer set, source/ABI/behavior/protocol boundary, platform matrix, and ecosystem rules. Evidence can overturn the proposed classification.

### Answer 3

Freeze automatic adoption, preserve both releases and manifests, identify failing clients and observations, compare the declared contract, inventory deployments, and retain build/test/publication evidence. Pin consumers to the last accepted digest where safe. If restoring compatibility is appropriate, publish 3.6.1; never replace 3.6.0. If the new behavior must remain, publish an incompatible major and migration plan. Mark 3.6.0 defective or withdrawn and notify consumers with affected scope, mitigations, exact digests, and follow-up tests.

### Answer 4

The manifest binds product name, SemVer, source revision, contract revision, target matrix, source archive digest, each OS/architecture binary digest, OCI index and manifest digests, build parameters, dependency-lock identity, compatibility claims, evidence links, publication time, and support state. Coordinates are create-once; target selection resolves to a digest. Test each maintained baseline using old source, old binaries where applicable, documented behavior, and image startup on supported targets. Major lines have distinct coordinates or namespaces and independent patch streams. Channels may point to releases but deployment records the resolved manifest and artifact digests.

### Answer 5

Version each contract at its ownership boundary: firmware product release, controller release, negotiated wire-protocol range, configuration-schema version, and immutable deployment-bundle manifest. During rolling upgrade, old controller/new device and new controller/old device must share a tested protocol range. Additive messages require verified unknown-field behavior. Configuration uses explicit readers/writers and migration direction. The bundle pins every digest and compatibility matrix.

An incompatible protocol or schema needs a new major identity, dual support or an ordered transition, observability, and abort criteria. Rollback is allowed only while persisted/device state remains readable by the old software. A version bump communicates the break but does not guarantee rollout safety; tested mixed-version paths, state migration, recovery artifacts, and authorized operational decisions do.
