---
module_id: SDRE-002
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 2
title: Dependency Resolution and Locking
status: complete
last_verified: 2026-08-29
---

# Dependency Resolution and Locking

## One-Page Review

### Governing question

How does a delivery system turn dependency declarations into a complete, repeatable, integrity-checked graph while preserving deliberate updates, platform differences, provenance, and an honest boundary between locked inputs and trustworthy artifacts?

### Essential definitions

- A **dependency manifest** declares dependency intent: names/coordinates, version constraints, sources, features, groups, platform markers, and overrides.
- A **direct dependency** is declared by the root project; a **transitive dependency** is introduced by another selected dependency.
- A **dependency graph** has resolved package/component identities as vertices and requirement relationships as edges.
- **resolution** selects concrete dependency identities and versions that satisfy the resolver’s rules and the applicable constraints.
- A **version constraint** defines an admissible set; its meaning depends on the ecosystem’s version syntax and compatibility rules.
- A **resolver** is the versioned algorithm and policy that interprets manifests, repository metadata, platform/configuration, and prior lock state to produce a graph or conflict.
- A **lockfile** records a previously resolved graph sufficiently for a compatible installer to reconstruct/verify the intended dependency selection.
- A **frozen/locked install** consumes lock state and fails rather than silently re-resolving or rewriting it when inputs disagree.
- **integrity metadata** binds an expected identity to fetched bytes, commonly with a cryptographic digest; it does not by itself establish publisher trust, safety, or correctness.
- An **override/replacement/patch** deliberately substitutes or constrains normal resolution and therefore belongs in review, lock evidence, and update policy.
- A **dependency update** is a source change to the resolved input graph, even when application source is unchanged.

### Central model, mechanism, or theorem

Let manifest constraints be $M$, available repository metadata at time $t$ be $U_t$, resolver/tool version be $R_v$, target/configuration be $X$, and prior lock hints be $L_0$. Resolution is:

$$
G=\operatorname{resolve}(M,U_t,R_v,X,L_0)
$$

or a conflict. A lock serializes selected graph $G$ plus source/integrity and relevant configuration. Frozen installation checks:

$$
\operatorname{consistent}(M,L,R_v,X)\land
\operatorname{digest}(fetched_i)=L.digest_i
$$

for every required node. This improves repeatability of dependency inputs. It does not freeze compilers, operating systems, install scripts, external services, or the final artifact unless those are separately controlled.

### Critical invariants

- Resolve the full transitive graph for every relevant dependency group, feature set, target, runtime, and platform.
- Treat ecosystem identity as more than a short name: include namespace/source/registry, version or immutable revision, and content integrity.
- Commit governed lockfiles where the project’s delivery model expects repeatable applications/tools; document library-consumer policy explicitly.
- Use frozen/locked mode in verification and release; fail on manifest-lock inconsistency, missing nodes, changed bytes, unsupported lock format, or unexpected resolution.
- Pin the package-manager/resolver version and all configuration that changes graph shape.
- Keep source registries, mirrors, authentication, trust roots, proxies, and offline caches governed and observable.
- Review lock diffs as dependency source changes: direct and transitive additions/removals, sources, hashes, features, scripts, licenses, advisories, target support, and graph reach.
- Regenerate conflicted lockfiles from reviewed manifests under the governed resolver; do not hand-merge opaque graph state.
- Separate intended locked graph, fetched content, installed graph, packaged artifact, SBOM, scan, and runtime-loaded graph.
- Update deliberately; a stale locked vulnerability is repeatable, not safe.

### Common failures

Common failures include using floating ranges in release builds without a lock; locking only direct dependencies; assuming an exact direct version fixes transitives; accepting a lockfile generated with unrecorded flags; using a mutable branch or URL; trusting a name without source identity; treating a checksum as publisher authorization; running install scripts with release credentials; sharing caches across trust boundaries; silently resolving after a merge; deleting a lockfile to repair conflicts; producing locks on one platform that omit another platform’s graph; scanning a manifest instead of installed/artifact content; updating all transitives without reviewing graph changes; and never updating because the build is reproducible.

### Compact example

The manifest permits `web >=3,<4`. Today the resolver selects `web 3.8.2`, whose selected parser is `parse 2.4.1`. The lock records both nodes, their exact sources/digests, edges, platform conditions, and lock/resolver format. CI uses frozen mode. When `parse 2.4.2` appears, ordinary CI still consumes `2.4.1`; an explicit update job proposes the new graph, runs policy/tests/scans, and commits the reviewed lock diff. If the registry serves different bytes for `2.4.1`, integrity verification fails rather than accepting them.

### Connections

[SDRE-001](./001-from-source-change-to-deployable-artifact.md) places the resolved graph in the artifact transformation. [SYSP-001](../../05-programming-languages-systems-programming/modules/001-from-source-text-to-process-image.md) explains platform/ABI constraints. [STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) governs verification evidence. [SDRE-003](../ROADMAP.md) adds hermetic and reproducible build requirements beyond locking.

## Governing Question

Which identities, constraints, algorithms, metadata, configurations, and verification steps must be controlled so that dependency installation is repeatable enough for release—and how can dependencies still be updated, audited, and repaired without weakening that guarantee?

Dependency management is a graph transformation with code-execution and supply-chain consequences. “We depend on library A” hides A’s transitives, optional/peer/build dependencies, generated/native code, sources, platform branches, install scripts, and resolver decisions. A production lock makes one graph reviewable and repeatable, but only within a declared ecosystem and execution boundary.

## Why This Matters

Two builds from identical application source can select different dependencies because a compatible release appeared, metadata changed, a mirror differed, the resolver version changed, or a platform marker evaluated differently. The resulting artifacts may compile differently, fail at runtime, change licensing, or incorporate a vulnerability.

Dependencies also execute with build authority. Package-manager lifecycle scripts, build backends, code generators, compiler plugins, and native build steps can read files, contact networks, and alter output. Content integrity helps detect substitution; it does not prove that selected content is benign.

A lock creates a controlled change boundary. Normal verification consumes it without mutation; update work intentionally changes it and receives code-review-quality evidence. This separates “does this source still build with the accepted graph?” from “should we move to a new graph?”

## Prerequisites and Retrieval

Retrieve:

- directed graph, vertex, edge, reachability, transitive closure, cycle, constraint intersection, and satisfiability;
- semantic-version-like ranges, exact version, tag, branch, revision, pre-release, and yanked/deprecated release;
- package registry, repository, namespace, coordinate, mirror, proxy, cache, and checksum;
- build/runtime/development/test/optional/peer dependency and platform/feature marker;
- cryptographic digest, signature, trust root, authorization, provenance, and immutable identity;
- manifest, lockfile, package manager, resolver, installer, artifact, SBOM, and vulnerability advisory;
- deterministic, repeatable, reproducible, hermetic, offline, and frozen.

You should be able to explain why `>=1,<2` is a set rather than a version, why `1.4.3` without a source/digest is not complete content identity, and why the same lock may produce different installed trees when platform or installer configuration differs.

## Learning Objectives

After completing this module, you should be able to:

1. model dependency resolution as constrained graph selection;
2. distinguish declared, resolved, fetched, installed, packaged, and runtime-loaded dependency sets;
3. explain how major resolver policies differ without assuming one universal algorithm;
4. design a lock schema that captures transitive edges, sources, integrity, conditions, and resolver context;
5. enforce frozen installation and diagnose manifest-lock divergence;
6. reason about features, optional/peer dependencies, targets, native artifacts, and multi-platform locks;
7. review overrides, mutable sources, mirrors, caches, install scripts, and integrity evidence as trust decisions;
8. conduct narrow, explainable dependency updates and resolve lock conflicts safely;
9. connect locks with SBOM, vulnerability/license analysis, provenance, artifact identity, and runtime observation;
10. create qualified human review paths for high-consequence dependency changes.

## Core Exposition

### Distinguish intent from selection

A manifest should express what the project intends to depend on and which changes it considers compatible. A constraint such as $1.4\le v<2.0$ denotes a set. Resolution chooses one concrete version after considering constraints from the root and transitive packages, exclusions, replacements, target conditions, features, repository metadata, and resolver policy.

This separation lets published libraries describe compatibility to consumers while applications record a tested composition. It also explains why editing one direct constraint can change many transitive nodes. The resolver is not merely downloading what was typed; it computes a graph.

Ecosystems differ. Some choose the newest version satisfying all ranges, some can install multiple versions, some hoist or deduplicate, some use nearest/first declarations, and Go’s module system uses minimal version selection: the highest minimum requirement encountered for each module forms the build list. Peer and optional rules add other constraints. Never apply a Cargo, npm, Gradle, Python, or Go mental model to another tool without checking its current specification.

### Define dependency identity completely

A package name is ambiguous without its ecosystem namespace and source. The same spelling can exist in a public registry, private registry, local path, Git repository, or mirror. A complete resolved identity commonly needs:

- ecosystem/coordinate and normalized namespace/name;
- exact version or immutable source-control revision;
- canonical source/registry/repository identity;
- content digest(s), signature/attestation references where used;
- dependency edges and relevant groups/features;
- target/environment markers and artifact variant;
- license and provenance identifiers when governed.

Mutable tags, branches, “latest,” changing/snapshot modules, and unversioned URLs make resolution time-sensitive. A lock may record the commit or returned digest, but the fetch path must verify it. A Git tag alone can be moved; a registry can delete or replace content unless immutability and integrity checks intervene.

Identity also extends to native/prebuilt variants. One package version may select wheels, archives, binaries, or source builds by OS, architecture, runtime ABI, and libc. Recording only the version can hide different bytes and execution paths.

### Construct the transitive graph

Let a selected component be $p@v$. Its metadata contributes conditional edges to other constraints. Resolution expands requirements until a fixed point, selects versions according to policy, and rejects unsatisfied conflicts—or sometimes installs multiple versions where permitted.

The relevant closure may differ by task:

- production runtime dependencies;
- build and code-generation dependencies;
- development/test/lint/documentation tools;
- optional features/extras/groups;
- platform-specific dependencies;
- plugins/peer dependencies supplied by a host;
- dynamic runtime modules or system packages outside the language manager.

Do not call development dependencies harmless. They execute in CI and can alter generated code or steal release credentials. Conversely, not every locked development package ships in the artifact. Maintain graph classifications and verify the actual package contents.

Feature unification can change enabled code without changing package versions. Resolver configuration, workspace membership, selected groups, omit/include flags, and target markers therefore belong beside the lock. A frozen install created under one configuration may fail or silently differ under another unless the tool records and validates these choices.

### Understand what a lock records

A useful lock is a machine-generated serialization of resolution state, not a second hand-authored manifest. Depending on the ecosystem, it records exact versions, source locations, content hashes, dependency edges, markers, features, or install layout. Its format/version matters because compatible package-manager versions must interpret it consistently.

At minimum, the lock should allow the installation tool or verifier to answer:

1. Which exact nodes and edges were selected for this root/configuration?
2. From which authorized sources will bytes be fetched?
3. Which integrity values must those bytes satisfy?
4. Which platform, feature, group, resolver, and lock-format assumptions apply?
5. Is the lock consistent with the current manifest?

Some files commonly confused with locks cover only part of this. Go’s `go.sum` records hashes for downloaded module metadata/content and can contain multiple versions; the selected build list follows `go.mod` plus minimal version selection. A checksum list is not necessarily a complete frozen graph. Read the ecosystem semantics.

### Use frozen installation as a release gate

A normal developer install may update a lock to accommodate changed manifest constraints. That convenience is inappropriate for verification and release because resolution changes become unreviewed side effects. Frozen mode should:

- require an existing supported lock;
- validate manifest, workspace, configuration, and lock consistency;
- avoid rewriting manifest or lock;
- install exactly the locked graph applicable to the target;
- verify source and content integrity;
- fail on unexpected/missing/extra nodes according to the tool’s model.

For npm, current `npm ci` requires a lock, errors when it disagrees with `package.json`, removes an existing `node_modules` tree, and does not rewrite manifest or lock. Flags that shaped the lock, such as peer/install-link behavior, must also be supplied—preferably in committed project configuration.

Frozen does not mean hermetic. The installer can still consult registries, execute scripts, use host tools, select native variants, read configuration, and write timestamps. Locking is one input-control layer; the next module addresses hermetic/reproducible builds.

### Verify content, sources, and availability

Version selection answers “which release?” Integrity answers “did fetched bytes match the recorded bytes?” Source policy answers “was this an authorized origin?” Signature/provenance policy asks “who/what produced this content under which process?” Vulnerability/license review asks other questions. Keep these claims separate.

A digest catches accidental or malicious byte substitution when the expected digest is trusted. It does not show that the package author is legitimate, the code is safe, or the chosen version lacks known vulnerabilities. If an attacker changes both artifact and lock in an authorized source change, review and signing policy must detect that.

Repository order can create dependency-confusion risk if an internal name resolves from a public registry. Bind namespaces to allowed sources; do not fall back silently. Govern mirrors and proxies because they influence availability and content. For private packages, authentication configuration must not enter the lock or artifact as a secret.

Deletion/yanking creates availability concerns. A lock can name bytes no longer retrievable. Use governed caches or artifact repositories with retention, integrity re-verification, and provenance; do not treat a developer’s warm cache as durable supply-chain evidence.

### Treat install-time execution as privileged

Dependencies may execute install hooks, build scripts, native compilation, generators, plugin discovery, or metadata preparation. These run before application tests and often with network/filesystem credentials. A content-locked malicious script remains malicious repeatably.

Inventory executable hooks, disable them by default where the ecosystem/workflow permits, allowlist necessary scripts, isolate network and credentials, use read-only sources, constrain outputs, and retain logs/provenance. Review changes to script presence and build backend even when public APIs appear unchanged.

Generated/native outputs must be bound to the artifact evidence. A lock identifies source inputs; it does not automatically identify compiler flags, system headers, or binaries downloaded by a script from an undeclared URL.

### Handle platforms and multiple environments

One logical dependency set may resolve differently for Linux, Windows, macOS, CPU architectures, runtimes, or accelerator/toolchain variants. Strategies include:

- a universal lock containing conditional nodes and hashes for all governed targets;
- separate named locks per target or deployment class;
- one resolution produced on a canonical platform plus explicit target supplements;
- container/base-environment locking combined with language locks.

The correct choice depends on ecosystem semantics. In every case, enumerate supported target matrices, ensure locks cover them, and test frozen installation in each. A universal lock produced only on one platform can omit dependencies whose markers were never evaluated.

Production, test, and tool groups should be explicit. Keeping them in one lock improves whole-repository visibility but may increase conflicts/noise. Separate locks reduce scope but can select incompatible shared tools and multiply update work. Record ownership and consistency checks.

### Update locks deliberately

A lock is a change-control mechanism, not a permanent freeze. Establish update triggers: security advisory, bug, compatibility need, support deadline, scheduled freshness window, toolchain/platform change, or dependency removal.

A controlled update:

1. begins from clean governed manifests and resolver configuration;
2. chooses scope—one direct dependency, one transitive, one group, or deliberate full refresh;
3. records resolver/repository/time inputs and reason;
4. generates a deterministic readable lock diff;
5. explains every added, removed, source-changed, feature-changed, and version-changed node;
6. evaluates licenses, advisories, provenance, scripts, platform/runtime requirements, and API/behavior change;
7. runs appropriate build, test, compatibility, performance, security, and operational evidence;
8. commits manifest and lock changes atomically when inseparable.

“Automated update” should mean automated proposal and evidence, not unreviewed release. Conversely, waiting indefinitely increases patch size and accumulates unsupported/vulnerable versions. Small frequent reviewed updates reduce graph-change ambiguity.

### Resolve manifest and lock merges safely

Lockfiles encode global resolution. Two branches can each add a compatible direct dependency yet produce a conflicted combined graph. Selecting both textual sides may create impossible edges or stale hashes.

Resolve manifests and source intent first. Then regenerate the lock from the merged manifest using the governed resolver/configuration, inspect the semantic graph diff against both parents, and run frozen verification. Do not delete the lock and accept whatever “latest” happens to resolve without reviewing the resulting graph.

Stable formatting and sorted entries improve diff review. Generated noise is not harmless when it hides a source or transitive change; pinning resolver versions reduces gratuitous rewrites.

### Connect lock, SBOM, artifact, and runtime

The lock is intended resolution input. An SBOM should describe the artifact or deployed subject under a defined method. They can differ because platform conditions omit nodes, bundlers remove/inline code, static linking combines components, install scripts download content, system packages enter, plugins load dynamically, or unused locked tools never ship.

Reconcile:

$$
manifest\ intent \rightarrow locked\ graph \rightarrow fetched/installed\ graph
\rightarrow packaged\ artifact \rightarrow deployed/runtime\ graph.
$$

Bind each evidence set to identities and timestamps. Scan the graph/artifact actually relevant to release. A lockfile advisory scan is useful early evidence but cannot prove the deployed artifact contains exactly that set or that a vulnerability is exploitable/non-exploitable.

## Definitions and Notation

Let package coordinate $p$ identify an ecosystem name plus governed source namespace. Let $V_p$ be available versions observed in repository universe $U_t$. Each requirement $r=(p,C_r,\gamma_r)$ contains version constraint $C_r\subseteq V_p$ and applicability condition $\gamma_r(X)$ over target/configuration $X$.

A resolved graph is $G=(N,E)$, with nodes

$$
n=(p,v,source,digest,variant,features)
$$

and requirement edges. A single-version resolver must choose $v_p\in\bigcap C_r$ for all applicable requirements on $p$, subject to its policy; multi-version ecosystems may instead select several compatible node identities and placement rules.

A lock serialization $L=lock(G,R_v,X,S)$ records graph, resolver version, configuration, and source policy $S$ to the degree its ecosystem supports. Define a frozen-install predicate:

$$
Frozen(M,L)=consistent(M,L)\land closed(L)\land sourcesAllowed(L)
\land allDigestsMatch(L)\land configMatch(L).
$$

This predicate does not imply artifact reproducibility or dependency safety. It establishes selected graph consistency and fetched-content integrity under stated inputs.

## Mechanisms, Invariants, or Proof Structure

Use this delivery mechanism:

1. **Declare:** express direct requirements, groups, sources, targets, features, and overrides.
2. **Constrain:** define compatible sets and non-negotiable platform/security policies.
3. **Resolve:** run a pinned resolver against governed metadata for a declared target/configuration.
4. **Lock:** serialize complete selected graph, edges, sources, integrity, conditions, and format/context.
5. **Review:** inspect semantic graph changes, executable hooks, provenance, licenses, advisories, and target requirements.
6. **Fetch:** use authorized registries/mirrors and verify content identity before execution.
7. **Install:** use frozen mode in an isolated controlled context; record actual graph and script/build effects.
8. **Verify:** build/test/scan the exact relevant graph and bind evidence to artifact identity.
9. **Promote:** promote the artifact, not a newly resolved/rebuilt dependency graph.
10. **Update/retire:** propose narrow graph changes, revalidate, remove unused dependencies, and retain rollback evidence.

The invariants are transitive closure, complete identity, frozen failure on drift, resolver/configuration identity, source/integrity separation, reviewable updates, and locked-to-artifact correspondence.

The following teaching resolver computes a single-version graph for a tiny repository, choosing the highest tuple version satisfying all accumulated half-open constraints. It demonstrates transitive constraint intersection only. It does not implement Semantic Versioning, pre-releases, metadata, multiple versions, features, platforms, sources, integrity, cycles, or any real package-manager policy.

<!-- bijux-verify: {"id":"toy-dependency-resolution","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"addon 2.1.0 constraints=>=2.0.0,<3.0.0\nlib 1.5.0 constraints=>=1.0.0,<2.0.0;>=1.4.0,<2.0.0\nlock nodes=2 edges=1\n","stderr":""}} -->
```python
available = {
    "addon": [(2, 0, 0), (2, 1, 0)],
    "lib": [(1, 2, 0), (1, 5, 0), (2, 0, 0)],
}
root = {
    "addon": [((2, 0, 0), (3, 0, 0))],
    "lib": [((1, 0, 0), (2, 0, 0))],
}
requires = {
    ("addon", (2, 0, 0)): {"lib": ((1, 3, 0), (2, 0, 0))},
    ("addon", (2, 1, 0)): {"lib": ((1, 4, 0), (2, 0, 0))},
}

constraints = {name: list(ranges) for name, ranges in root.items()}
selected = {}
while True:
    next_selected = {}
    for name, ranges in constraints.items():
        candidates = [
            version
            for version in available[name]
            if all(lower <= version < upper for lower, upper in ranges)
        ]
        if not candidates:
            raise RuntimeError(f"unsatisfied dependency: {name}")
        next_selected[name] = max(candidates)

    next_constraints = {name: list(ranges) for name, ranges in root.items()}
    for node in next_selected.items():
        for child, requirement in requires.get(node, {}).items():
            next_constraints.setdefault(child, []).append(requirement)
    if next_selected == selected and next_constraints == constraints:
        break
    selected, constraints = next_selected, next_constraints

def version_text(version):
    return ".".join(map(str, version))

for name in sorted(selected):
    rendered = ";".join(
        f">={version_text(lower)},<{version_text(upper)}"
        for lower, upper in constraints[name]
    )
    print(f"{name} {version_text(selected[name])} constraints={rendered}")

edge_count = sum(len(requires.get(node, {})) for node in selected.items())
print(f"lock nodes={len(selected)} edges={edge_count}")
```

The fixed-point recomputes dependencies after a version choice changes because different versions can declare different edges. A production resolver needs a rigorously specified conflict/selection algorithm and stable metadata snapshot.

## Alternatives and Trade-Offs

**Exact manifest versions without a lock** look simple but often fail to freeze transitives, sources, hashes, variants, or layout. A complete lock remains useful for applications. In ecosystems such as Go, manifest and checksum/module-selection semantics differ; use native guarantees rather than forcing a foreign pattern.

**One global monorepo lock** gives a coherent graph and one review surface but creates merge contention and broad updates. **Per-project locks** isolate ownership and changes but can duplicate vulnerable versions and let shared tooling drift. Choose by release unit and add cross-lock policy/audits.

**Newest-compatible resolution** accelerates fixes and freshness but increases unplanned change. **Minimal/lowest resolution** can reveal declared minimum support but may retain old defects and differs from what consumers choose. Test the supported policy boundaries deliberately; do not confuse one selected graph with the whole compatibility range.

**Online resolution** sees current releases/advisories but depends on mutable external metadata. **Offline/vendor resolution** improves availability/control but demands mirror freshness, storage, provenance, and removal processes. Govern exact metadata/content snapshots either way.

**Broad automated updates** reduce staleness but create large graphs and weak attribution. **Narrow updates** are reviewable but sometimes cannot satisfy coupled constraints. Start narrow, explain forced transitives, and schedule periodic coherent refreshes.

**Ignoring install scripts** reduces code-execution risk but can make packages unusable or produce different artifacts. **Allowing all scripts** expands the trusted computing base. Prefer explicit allowlists, sandboxing, least privilege, and replacement of opaque download-at-install behavior.

**Universal multi-platform locks** centralize consistency but grow complex. **Target-specific locks** accurately capture variants but require synchronized policy and updates. Whichever approach is native, test every supported target in frozen mode.

## Failure Modes and Misconceptions

- **“The manifest lists our dependencies.”** It commonly lists only direct intent; the resolved transitive graph is larger.
- **“Exact direct versions are enough.”** Transitive ranges, build tools, sources, variants, and scripts can still move.
- **“A lock guarantees reproducible builds.”** It controls selected dependency inputs; toolchains, environment, scripts, timestamps, and other inputs remain.
- **“The lock is the SBOM.”** It may include non-shipped tools and omit system, generated, vendored, bundled, or dynamic components.
- **“The checksum makes the package trusted.”** It verifies equality to expected bytes, not publisher identity, safety, authorization, or license.
- **“Frozen means offline.”** Frozen selection may still fetch locked content and consult configured infrastructure.
- **“Same version means same bytes.”** Source, variant, mutable registry behavior, or missing integrity can differ.
- **“One lock works everywhere.”** Conditional dependencies and native variants require explicit target coverage.
- **“Delete the lock when merging.”** That discards accepted graph state and can introduce unrelated newest-compatible changes.
- **“Never update a working lock.”** Reproducible vulnerability, incompatibility, or unsupported code is still a delivery risk.
- **“Update only the named package.”** Its metadata may force transitive additions/removals and feature changes.
- **“Dev dependencies do not affect production.”** They can execute in privileged CI and alter generated/package output.
- **“A cache is an integrity control.”** A poisoned or incorrectly keyed cache can substitute content unless verified.
- **“A passing install validates the dependency.”** It proves limited installer success, not API behavior, security, license, performance, or operational fitness.

## Worked Examples

### Example 1

**Question:** A manifest says `A >=1,<2`. Yesterday it selected 1.4; today 1.5. Is source unchanged?

**Reasoning:** Application source and manifest text are unchanged, but repository universe/time produced a different graph. Behavior, transitives, license, runtime requirements, and bytes can change. A governed lock would retain 1.4 until an explicit update.

**Conclusion:** Resolution output is a build input and dependency updates are source changes.

### Example 2

**Question:** Direct dependency B is pinned to 2.3.0. Can its graph still drift without a lock?

**Reasoning:** B’s published metadata may permit C `>=4,<5`. A later resolution can select a new C release. Exact B does not identify C, its source, or its bytes.

**Conclusion:** Repeatability requires transitive closure, not direct pins alone.

### Example 3

**Question:** A frozen install reports that manifest and lock disagree. Should CI regenerate the lock?

**Reasoning:** Regeneration changes source/evidence and may choose new transitives. CI should fail with a diagnostic. An authorized dependency-change workflow updates manifest/lock, reviews the graph, and reruns evidence.

**Conclusion:** Release verification consumes lock state; it does not repair it silently.

### Example 4

**Question:** A locked package’s checksum matches. Is it safe to run its install script with registry credentials?

**Reasoning:** The checksum proves equality to reviewed/recorded bytes only if the expected digest is trusted. Those exact bytes can contain a malicious script. Isolate execution, remove unnecessary credentials/network, review/allowlist hooks, and verify outputs.

**Conclusion:** Integrity is necessary evidence, not behavioral authorization.

### Example 5

**Question:** Why does a lock made on Linux fail to cover a Windows release?

**Reasoning:** Conditional markers may select different packages; native artifacts differ by OS/architecture/ABI; generation may omit branches not evaluated on Linux. Use a universal format proven to include all targets or a governed Windows-specific lock, then frozen-install/test it.

**Conclusion:** Lock scope must include the release target matrix.

### Example 6

**Question:** Two branches both change the lock. Is choosing both textual conflict sides safe?

**Reasoning:** Each lock represents a globally resolved graph under a different manifest. Textual union can contain stale versions, hashes, edges, and unreachable nodes. Merge manifests, regenerate under the pinned resolver, inspect semantic differences, and verify frozen installation.

**Conclusion:** Resolve dependency intent, then regenerate and review graph state.

### Example 7

**Question:** An advisory flags a locked parser used only by a documentation tool. Does production contain it?

**Reasoning:** The lock shows intended graph membership, not artifact inclusion. Trace dependency group and build execution; inspect SBOM/artifact and whether the tool processes hostile inputs in CI. Production exploitability and build-pipeline exposure are different risks.

**Conclusion:** Use lock findings to scope investigation, not infer runtime composition automatically.

### Example 8

**Question:** A registry deletes a locked version, but one runner’s cache still builds. Is the release reproducible?

**Reasoning:** One warm cache is accidental availability and may be unverified. Retain content in a governed immutable mirror/artifact repository, verify digest/provenance, exercise clean/offline restoration, and record retention/exit policy.

**Conclusion:** A lock names content; durable supply requires governed retrieval.

### Example 9

**Question:** May a dependency bot merge a routine patch automatically into aircraft-control build tools?

**Reasoning:** Automation can propose graph changes and evidence, but version labels do not bound behavior, install scripts, generated output, toolchain semantics, or assurance impact. No external aviation, safety, academic, regulatory, or practitioner review is claimed. Named qualified software, toolchain, supply-chain security, safety, quality/independent-assurance, domain, and regulatory authorities must review affected graph, provenance, generated/artifact differences, verification independence, hazards, residual risk, and release authorization.

**Conclusion:** High-consequence dependency changes require qualified authority beyond an automated green graph.

### Example 10

**Question:** After removing a direct dependency, why do some of its transitives remain locked?

**Reasoning:** Another reachable node may still require them; the tool may retain hashes/metadata for selection; or the lock is stale. Use dependency explanation/reachability tools and native tidy/update behavior, compare actual graph, and remove only under governed regeneration.

**Conclusion:** Explain graph reachability before classifying lock entries as unused.

## Cross-Program Connections

- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) explains toolchain/plugin/generated-code dependency effects.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) evaluates changes in resolved behavior and oracle trust.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns dependency confusion, malicious packages, signatures, provenance, and vulnerability-risk analysis.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies configuration, traceability, supplier, and lifecycle control.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) provides governed registries, caches, update services, and developer workflows.
- [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) controls builder platforms, mirrors, identity, and network boundaries.

## References

1. Rust Project. [Cargo Reference: Dependency Resolution](https://doc.rust-lang.org/cargo/reference/resolver.html), current documentation. Resolver versions, feature behavior, conflicts, and `Cargo.lock` production; consulted 2026-08-29.
2. Rust Project. [Cargo Guide: `Cargo.toml` vs. `Cargo.lock`](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html), current documentation. Manifest intent and lockfile roles; consulted 2026-08-29.
3. Go Project. [Go Modules Reference](https://go.dev/ref/mod), current documentation. Minimal version selection, module graph pruning, `go.mod`, `go.sum`, proxies, checksum database, replacements, and workspaces; consulted 2026-08-29.
4. Python Packaging Authority. [`pylock.toml` Specification](https://packaging.python.org/en/latest/specifications/pylock-toml/), defined originally by PEP 751. Reproducible Python-environment lock format, packages, environments, groups, artifacts, and hashes; consulted 2026-08-29.
5. npm, Inc. [`npm ci`](https://docs.npmjs.com/cli/commands/npm-ci/), npm CLI current documentation. Frozen clean-install behavior, manifest-lock consistency, configuration flags, scripts, and omit/include behavior; consulted 2026-08-29.
6. npm, Inc. [`npm install`](https://docs.npmjs.com/cli/install/), npm CLI current documentation. Lock precedence, manifest-versus-lock update behavior, install algorithms, and configuration; consulted 2026-08-29.
7. Gradle, Inc. [Dependency Locking](https://docs.gradle.org/current/userguide/dependency_locking.html), current Gradle User Manual. Configuration-scoped lock state, strict validation, update modes, and limitations; consulted 2026-08-29.
8. Russ Cox. [“Minimal Version Selection”](https://research.swtch.com/vgo-mvs), 2018. Primary algorithm rationale and construction for Go’s dependency-selection model.

## Exercises

### Exercise 1

Distinguish the manifest, resolved graph, lock, installed graph, SBOM, and artifact for a small command-line application with two direct dependencies.

### Exercise 2

Trace resolution where root requires A `>=1,<2` and B `>=2,<3`; selected B 2.4 requires A `>=1.6,<3`; available A versions are 1.5, 1.8, and 2.1. State the accepted version under a newest-satisfying single-version teaching policy and what the lock must record.

### Exercise 3

Diagnose a release job that runs an updating install, trusts a shared warm cache, omits install-script policy, and scans only direct manifest entries.

### Exercise 4

Design a lock/update strategy for a monorepo shipping Linux and Windows applications plus a published library, with separate production and development dependency groups.

### Exercise 5

Design dependency-change assurance for unfamiliar infusion-pump firmware. Separate automated graph/integrity evidence from qualified human review and release authority.

## Answers to the Exercises

### Answer 1

The manifest declares acceptable direct constraints, groups, sources, features, and platform conditions. The resolver expands transitive metadata and selects a concrete graph for a resolver version/configuration/repository state. The lock serializes that selection, including exact identities, edges, sources, hashes, conditions, and format information supported by the ecosystem. The installed graph is what fetching, marker evaluation, variants, scripts, and installer layout actually produced. The SBOM is an evidence artifact describing components in a named source/build/artifact/deployment subject under a method. The application artifact is the packaged bytes; it may bundle some dependencies, link others, omit development tools, and acquire runtime/system dependencies.

Record and reconcile identities across all six. Neither manifest nor lock alone proves artifact composition; SBOM accuracy needs its own generation/verification evidence.

### Answer 2

The applicable A constraints intersect:

$$
[1.0,2.0)\cap[1.6,3.0)=[1.6,2.0).
$$

Available 1.8 satisfies the intersection; 1.5 is below it and 2.1 violates the root upper bound. Under the stated newest-satisfying teaching policy, select A 1.8 and B 2.4. A real package manager may have materially different multi-version, pre-release, conflict, feature, or ordering semantics.

The lock should record root identity/context; exact A 1.8 and B 2.4 coordinates; authorized sources; content hashes/artifact variants; B-to-A edge; relevant groups, target markers/features; resolver/lock format and configuration where supported. Frozen installation must verify manifest consistency and bytes instead of reselecting.

### Answer 3

The update-capable install can mutate dependency source during verification, so results are not bound to a pre-reviewed graph. A shared warm cache can cross project/trust/target boundaries and mask deleted dependencies; without integrity verification its contents are not authoritative. Install scripts execute dependency code with build authority. Direct-entry scanning misses transitives, build tools, actual installed variants, and packaged/runtime divergence.

Require a committed governed lock and frozen clean install; pin package manager and graph-shaping configuration; use authorized sources/mirrors and verify hashes; key/isolate caches by content, source, target, toolchain, and trust; sandbox or explicitly allow scripts with least privilege and retained evidence; record actual installed graph; generate/verify artifact-bound SBOM; scan direct/transitive build/runtime graphs and artifact; fail closed on drift/missing evidence. Move updates to a separate reviewable workflow.

### Answer 4

Choose lock boundaries aligned with release units while preserving cross-project visibility. Use target-specific Linux/Windows locks if the native format cannot reliably encode all conditional artifacts; otherwise use one universal lock and prove both target installations in frozen CI. Keep production and development groups explicit in each lock or one coherent workspace lock. Development packages remain in supply-chain review because they execute, even when absent from shipped SBOMs.

For the published library, declare honest compatible ranges for consumers and test at least locked known-good plus declared boundary/fresh resolution policies. Do not assume the library’s repository lock controls consumer resolution. Pin resolver versions/configuration; bind private namespaces to internal sources; govern overrides/scripts/caches. Update narrowly and frequently with semantic graph diffs, cross-target builds/tests, API/ABI compatibility, provenance/license/advisory review, and artifact/SBOM reconciliation. Merge manifests first and regenerate locks rather than textually combining graph state.

### Answer 5

Automation can verify manifest-lock consistency; full transitive closure across target/tool configurations; exact source/revision/artifact hashes; signatures/provenance policy; approved registry namespaces; license/advisory policy; install/build-script allowlists and sandbox logs; compiler/plugin/code-generator identities; deterministic lock regeneration; frozen offline restoration; source/generated binary/artifact diffs; SBOM correspondence; tests, static analysis, and trace links bound to artifact digest. Reproduce critical generated output through an independent controlled route and compare with reviewed tolerances/semantics.

No external academic, clinical, regulatory, medical-device, safety, or practitioner review is claimed. Named qualified firmware, hardware, compiler/toolchain, supply-chain security, clinical/domain, safety/risk, cybersecurity, quality/independent-assurance, manufacturing/service, and applicable regulatory authorities must review supplier change, provenance, executable hooks, compiler/generator effects, requirements/hazards, verification independence, target hardware behavior, residual risk, rollback/field-update consequences, and safety-case impact. Automation may block or escalate; it cannot accept clinical/safety risk. Explicit qualified release authority must approve the exact artifact/evidence set, and unresolved critical dependency identity, evidence, or hazard impact blocks release.
