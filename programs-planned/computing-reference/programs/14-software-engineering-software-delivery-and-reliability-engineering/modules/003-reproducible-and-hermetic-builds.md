---
module_id: SDRE-003
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 3
title: Reproducible and Hermetic Builds
status: complete
last_verified: 2026-09-06
---

# Reproducible and Hermetic Builds

## One-Page Review

### Governing question

How can a build be isolated from undeclared influences and independently repeated to produce the same artifact bytes—and what do those properties establish, fail to establish, and cost?

### Essential definitions

- a **declared input** is source, dependency, toolchain, parameter, target, or controlled datum intentionally included in the build identity;
- an **undeclared input** is any influential value absent from that identity, such as wall-clock time, working path, locale, host file, ambient variable, network response, or stale output;
- a **hermetic build** can observe only declared inputs through enforced isolation and fails when an undeclared input is requested;
- a **deterministic build step** maps the same effective inputs to the same output rather than sampling randomness or depending on scheduling;
- a **reproducible build claim** states that qualifying invocations from materially equivalent inputs produce bit-for-bit identical defined outputs;
- **repeatability** often means repetition by the same actor or setup; **independent reproduction** deliberately changes builders or environments;
- **normalization** replaces irrelevant variation with a canonical representation, such as a source-derived timestamp or sorted archive order;
- an **input closure** is the transitive set of everything allowed to influence output;
- a **build trace** records attempted reads, tool executions, network access, and produced outputs;
- a matching digest establishes byte equality under the chosen algorithm and artifact boundary, not correctness, safety, provenance, or authorization.

### Central model, mechanism, or theorem

Model a build as

$$
A=B(I,P,U,N),
$$

where $I$ is declared input, $P$ target platform, $U$ ambient undeclared state, $N$ internal nondeterminism, and $A$ defined artifact bytes. Hermeticity enforces independence from $U$; determinism controls $N$. Reproducibility is an observed relation:

$$
(I_1,P_1)\equiv(I_2,P_2)\Longrightarrow bytes(A_1)=bytes(A_2).
$$

Hermeticity and determinism make reproducibility easier to reason about, but none implies software correctness. A flawed compiler can produce the same flawed binary perfectly.

### Critical invariants

- define the artifact boundary and equivalence claim before comparing outputs;
- pin source, dependencies, build definitions, toolchains, target, features, and relevant platform data;
- deny ambient network, host filesystem, clock, locale, user, path, randomness, and previous-output access unless declared;
- start from a clean controlled output tree and make every generator an explicit build action;
- normalize only semantically irrelevant data; preserve timestamps or randomness when they are product behavior;
- sort unordered inputs, stabilize serialization, and control concurrency-sensitive generation;
- compare final artifact bytes, not success messages, file names, or source revisions;
- reproduce with meaningfully independent infrastructure when using equality as tamper evidence;
- retain mismatches and negative results rather than publishing only successful pairs;
- bind evidence to artifact, source, build definition, input set, builder identities, and time;
- fail closed when required inputs are unavailable rather than silently fetching substitutes;
- treat reproducibility as one evidence claim, never as proof of security or correctness.

### Common failures

Common failures include embedding current time; archiving files in filesystem order; recording absolute paths; locale-sensitive sorting; reading user configuration; downloading a mutable URL; resolving dependencies during the build; reusing dirty outputs; racing generators; using an unpinned compiler or base image; calling a container hermetic despite network and host mounts; comparing different artifact scopes; rebuilding twice on one compromised worker; normalizing meaningful data; and equating reproducibility with supply-chain trust.

### Compact example

Two builds use the same source and lockfile, but one archive records /home/lee/work, local time, and one directory order while another records /build/src, UTC, and another order. The build adopts relative paths, a source-derived epoch, stable timezone, sorted entries, pinned compression, and a clean isolated toolchain. Independent builders then produce the same digest. This supports byte reproducibility for the declared target; it does not prove source or compiler benign.

### Connections

[SDRE-001](001-from-source-change-to-deployable-artifact.md) defines artifact identity and build-once promotion. [SDRE-002](002-dependency-resolution-and-locking.md) supplies the resolved dependency graph. [SDRE-004](../ROADMAP.md) next uses correct input identities for incremental build caching.

## Governing Question

A developer often says, “It builds on my machine.” That statement hides the machine, clock, local files, caches, network, tool versions, and scheduler. If any can change output without changing declared inputs, the artifact cannot be derived or audited confidently.

Hermeticity controls what a build may observe. Reproducibility checks whether equivalent inputs actually produce identical outputs. They reinforce each other but are not synonyms. This module develops both from first principles, shows their non-implications, and explains the bounded evidence they add to delivery.

## Why This Matters

Reproducible artifacts make differences diagnostic. If two qualifying parties build equivalent declared inputs and obtain different bytes, something in the input closure, toolchain, nondeterminism, or execution remains unexplained. If they match, consumers gain evidence that published bytes correspond to a repeatable transformation—but only to the degree the rebuild is independent and input identities are trustworthy.

Hermetic builds support correct caching, parallel execution, remote builders, and disaster recovery. An action depending only on declared inputs can move or repeat without inheriting a workstation. Fail-closed isolation also reveals dependencies that would otherwise remain latent until a clean runner or network outage.

The Reproducible Builds project defines reproducible builds around verifiably identical binary outputs from given source [1]. SLSA specification 1.2 treats provenance and build integrity as scoped supply-chain properties and allows reproducible builds as one support for trustworthy provenance [2]. Neither claims matching bytes prove correct or harmless software.

## Prerequisites and Retrieval

Retrieve immutable source revision, transitive dependency graph, lockfile, checksum, toolchain, build definition, target platform, artifact boundary, content digest, cache key, environment, filesystem metadata, locale, timezone, randomness, concurrency, network, clean build, provenance, signature, and promotion.

From SDRE-001 retrieve build transformation and distinctions among source, build, artifact, release, and deployment identities. From SDRE-002 retrieve frozen resolution, authorized sources, content integrity, platform conditions, install-time execution, and the difference between locked and packaged graphs.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish hermeticity, determinism, repeatability, and reproducibility;
2. enumerate hidden inputs across clock, path, locale, filesystem, environment, network, toolchain, and concurrency;
3. define an artifact boundary and materially equivalent input relation;
4. design isolation that denies or declares ambient dependencies;
5. normalize timestamps, paths, ordering, ownership, and archive metadata safely;
6. diagnose byte differences from an outer container to embedded objects;
7. construct an independent rebuild experiment with honest evidence limits;
8. explain why hermetic, deterministic, and reproducible do not imply one another;
9. define a narrower semantic claim when bit reproducibility is inappropriate;
10. connect these properties to caching, provenance, incidents, and supply-chain defense.

## Core Exposition

**Define the claim first.** Name the source identity, dependency closure, build definition, toolchain, parameters, target, and output set. “The package reproduces” might mean one executable, archive, OCI manifest graph, debug symbols, or release bundle. Comparing one binary while ignoring an installer that embeds time is not full release reproducibility.

Define material equivalence. Must builders use exactly the same compiler bytes, or can independent compilers implementing one version qualify? Are signatures detached, embedded deterministically, or outside the claim? Record the answer rather than moving the boundary until results match.

**Enumerate input closure.** Visible inputs include source, lockfile, compiler, linker, generators, scripts, target and flags. Hidden inputs commonly include:

- current time, timezone, locale and collation;
- absolute paths, user/host names, home configuration and environment variables;
- file timestamps, ownership, permissions, attributes and enumeration order;
- default shell, umask, resource limits, system headers and runtime libraries;
- CPU features, kernel behavior and filesystem case sensitivity;
- network metadata/content, name resolution, mirrors and license services;
- random seeds, process IDs, addresses, temporary names and parallel scheduling;
- prior outputs, compiler caches and undeclared generated files;
- repository metadata used to construct versions.

Trace actual reads and executions where possible. Build files express intent; system, sandbox, network, and process traces reveal behavior. Convert every legitimate observation into a declared input or controlled service.

**Enforce hermeticity.** Expose a read-only input tree, empty output tree, pinned tools, explicit environment, fixed target, bounded resources, and no network unless acquired data is already declared and content-addressed. Resolve and fetch before building, verify digests, then execute offline.

Allowing network only to a registry is not hermetic: metadata, mutable names, time and resolver behavior can change output. A container is not proof either; it can mount host paths, inherit variables, read clocks, contact networks, or select a mutable base image. State enforced controls and observed access.

Fail closed. If a compiler requests an undeclared header, report it. Silently reading the host preserves convenience by destroying the input model.

**Control time.** Archives, documentation, object formats, package metadata, compression headers and images can embed current time. Removing every timestamp is not always correct: users may need source or protocol time.

Use a governed source-derived timestamp. The SOURCE_DATE_EPOCH specification defines a distribution-independent Unix timestamp for tools to consume instead of current build time and describes timestamp clamping [3]. It is an input and convention, not proof every tool honors it. Preserve real build time in detached provenance where useful.

**Control paths and identities.** Compilers may embed debug paths, source roots, module-cache names and commands. Build under a canonical root or use supported prefix remapping. Prefer mapping ephemeral roots to a stable virtual prefix rather than stripping information needed for debugging.

Host names, user names, process IDs and temporary paths follow the same rule. Decide whether each is product data, evidence data, or irrelevant variation. Preserve product data; move evidence to detached records; normalize irrelevant variation.

**Control ordering and serialization.** Sets have no inherent order, but archives, symbol tables, generated registries and linked objects do. Filesystem and hash-map order can vary. Sort by an explicit bytewise or fixed-locale key before serialization.

Pin archive and compression formats/options. Normalize ownership, permissions, attributes and times only when nonsemantic. “Sort everything” is wrong when order defines precedence.

Parallelism exposes missing dependency edges and write races. Do not merely force one worker: fix the graph so independent actions may run in any order while conflicts have explicit edges. Record if the build reproduces only serially.

**Control randomness.** Randomized algorithms, identifiers, layout, sampling, encryption keys and profile-guided processes can affect bytes. If randomness is irrelevant, supply a declared deterministic seed. If unpredictability is required, bit reproducibility may be wrong for that output.

Never reuse deterministic cryptographic keys or nonces just to match bytes. Prefer a reproducible unsigned payload with detached signing when formats allow. Authenticate the variable wrapper separately.

**Pin toolchain and platform.** An application lockfile does not identify compiler, linker, generator, package manager, system headers, runtime, base image, firmware tools, or compressor. Address each by immutable identity and include target/configuration.

Exact tools ease narrow reproduction but two builds using one compromised compiler share failure. Ken Thompson's trusting-trust attack shows a compiler can reproduce malicious behavior absent from inspected source [8]. Higher assurance may use independently bootstrapped toolchains or diverse double compilation [9]. Application reproducibility alone does not eliminate toolchain trust.

Platform behavior remains influential: kernel interfaces, CPU detection, case sensitivity and limits matter. Isolate/emulate it, declare it, or test variants and narrow the claim.

**Separate the properties.** A hermetic generator can race writers and produce different order: hermetic but nondeterministic. A nonhermetic build can fetch a stable undeclared file for months: observed reproducibility without input closure. A deterministic compiler can embed a path: one output for each real input, but declared equivalence omits one. A pinned faulty compiler can produce reproducibly incorrect output.

**Run independent reproduction.** Reconstruct immutable declared inputs. Use a builder independent enough to challenge the failure or threat of interest. Vary path, clean filesystem, user, timezone, locale, host, workers and infrastructure while holding declared inputs equivalent. Disable network and caches or content-verify every returned object.

Compare complete artifact bytes by cryptographic digest. On mismatch, retain outputs, logs, traces, tool versions, input manifests and environment. Locate the first structural difference from the outer archive through nested members and executable sections.

On match, record identities and limitations. Two jobs on one runner image offer less independence than different organizations reconstructing source. Equality argues against some variation or substitution, not all compromise.

**Diagnose systematically.** Inspect outer metadata, member order and timestamps, then generated files, debug/symbol tables, embedded paths, object order, compression and signatures. Change one suspected dimension and predict the difference.

Do not postprocess blindly until hashes match. That can conceal mechanism, invalidate signatures or corrupt semantics. Fix the producer. If normalization is necessary, make it a declared transformation and test semantics.

**Use results during incidents.** A match means published bytes are consistent with the reconstructed transformation; source or common tool compromise can remain. A mismatch means hidden input, nondeterminism, reconstruction error, or build/publication compromise exists. Neither result identifies cause by itself.

Retain historical tools, sources, dependencies, definitions and platform descriptions for supported releases. A theoretically reproducible artifact cannot be operationally rebuilt after its compiler disappears.

**Connect to caching.** Hermetic deterministic actions support content-addressed caching when the key covers every semantic input. Reproducibility tests that model. Under-specified keys can return wrong bytes; over-specified keys reduce hits. A warm cache can hide an undeclared dependency until eviction.

**Keep evidence claims separate.** Provenance states how an artifact was produced; reproduction can challenge it. A signature authenticates a statement or bytes; it does not make a build reproducible. Reproducible output can be unsigned, and signed output can be unreproducible. Later modules own provenance, SBOMs, and signing.

**Handle irreducible outputs honestly.** Some outputs contain secure randomness, hardware measurements, live external data, or signed timestamps. Isolate a deterministic core, make randomness explicit, detach wrappers, define a semantic equivalence test, or declare the output nonreproducible.

Semantic equivalence is weaker than byte equality. Define parser, ignored fields, behavior checks and threat limitations. Never call byte-different outputs reproducible without stating the alternative relation.

**Adopt proportionate scope.** Prioritize release artifacts, privileged tools, bootstrap components, long-lived binaries, and high-impact services. Start by eliminating clock, path, order, network and dirty-tree inputs. Measure rates over a declared corpus and retain mismatches; a rising percentage is useful but not a security grade.

## Definitions and Notation

Let $I$ be declared input closure, $P$ target platform, $U$ ambient state, $N$ internal nondeterministic choice, and $A$ artifact bytes. A build invocation is $A=B(I,P,U,N)$.

For an equivalence relation $\equiv$, a reproduction trial passes when

$$
(I_1,P_1)\equiv(I_2,P_2)\land bytes(A_1)=bytes(A_2).
$$

Hermeticity is noninterference: inaccessible $U$ cannot change or enable output. Determinism means one output for the same effective inputs. Let $h(A)$ be a collision-resistant digest; equal digests are practical evidence of byte equality under algorithm and serialization assumptions.

## Mechanisms, Invariants, or Proof Structure

**Non-implication counterexamples.**

1. Hermetic does not imply reproducible: a sandboxed generator uses permitted scheduling to order records.
2. Observed reproducibility does not imply hermetic: an undeclared mutable URL happened not to change.
3. Deterministic does not imply reproducible under declared inputs: output embeds an undeclared path.
4. Reproducible does not imply correct: a faulty pinned compiler deterministically miscompiles source.

**Byte equality proposition.** If artifact serialization is fixed and digest collision resistance is accepted, equal digests give practical evidence of equal bytes. The conclusion does not extend to source identity, behavior, safety, or provenance.

**Executable demonstration.** The first packager embeds root, time and caller order. The normalized packager uses a virtual root, source epoch and sorted paths. The read-set check models hermeticity separately.

<!-- bijux-verify: {"id":"demonstrate-build-controls","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ambient_equal=False\nnormalized_equal=True\nundeclared=['/etc/locale.conf', 'https://example.invalid/tool']\nhermetic_before=False\nhermetic_after=True\n","stderr":""}} -->
```python
files = {"b.txt": "B", "a.txt": "A"}

def ambient_package(root, built_at, order):
    body = [f"root={root}", f"time={built_at}"]
    body.extend(f"{name}:{files[name]}" for name in order)
    return "\n".join(body)

def normalized_package():
    body = ["root=/src", "time=1700000000"]
    body.extend(f"{name}:{files[name]}" for name in sorted(files))
    return "\n".join(body)

left = ambient_package("/home/lee/project", 1700000300, ["a.txt", "b.txt"])
right = ambient_package("/builder/work", 1700000900, ["b.txt", "a.txt"])
print(f"ambient_equal={left == right}")
print(f"normalized_equal={normalized_package() == normalized_package()}")

declared = {"/src/a.txt", "/src/b.txt", "/tools/compiler"}
observed = declared | {"/etc/locale.conf", "https://example.invalid/tool"}
undeclared = sorted(observed - declared)
print(f"undeclared={undeclared}")
print(f"hermetic_before={not undeclared}")
declared |= set(undeclared)
print(f"hermetic_after={not (observed - declared)}")
```

The last line says only the modeled read set is declared. Declaring a mutable URL does not make content immutable or acquisition safe; fetch it by verified identity before the isolated action.

## Alternatives and Trade-Offs

**Same versus diverse toolchains.** Identical tools reduce variation and ease diagnosis; diverse lineage challenges compiler compromise but can introduce legitimate differences.

**Canonical environment versus portability.** One pinned environment stabilizes releases; deliberate environment variation reveals accidental coupling. Use both for different evidence.

**Byte versus semantic equivalence.** Bytes give crisp identity. Semantic comparison supports variable wrappers but needs a trusted parser and explicit ignored fields.

**Strict sandbox versus convenience.** Denial reveals missing inputs but can slow migration. Use observable migration modes, then enforce fail-closed release builds.

**Normalization versus fidelity.** Removing irrelevant metadata helps equality. Removing meaningful time, ownership, order, or randomness changes behavior.

**Clean versus incremental builds.** Clean builds strengthen isolation evidence; incremental builds accelerate feedback. Periodically compare them.

## Failure Modes and Misconceptions

- **“Hermetic means reproducible.”** Internal nondeterminism can remain.
- **“Reproducible means hermetic.”** Stable undeclared inputs can hide.
- **“Containerized means hermetic.”** Containers can access ambient state.
- **“A lockfile pins the build.”** Toolchains, generators and platforms matter.
- **“Same commit means same inputs.”** Dependencies and parameters differ.
- **“Same filename means same artifact.”** Compare defined bytes.
- **“A matching hash proves correctness.”** It supports byte identity only.
- **“Two rebuilds are independent.”** They may share compromise.
- **“Set the clock and finish.”** Paths, order, locale and races remain.
- **“Remove every timestamp.”** Some timestamps are product data.
- **“Single-thread the build.”** That can hide dependency defects.
- **“Postprocess until match.”** Blind normalization can corrupt semantics.
- **“Deterministic signatures are safe.”** Nonce reuse can expose keys.
- **“A cache hit proves reproducibility.”** It can avoid execution.
- **“One successful pair proves forever.”** Future inputs and releases change.

## Worked Examples

### Example 1

**Clock variation.** Two archives differ in member times and a generated banner. The team derives one packaging epoch from source, clamps irrelevant times, and moves real build time to provenance. **Conclusion:** control time representation without erasing evidence.

### Example 2

**Debug path.** An executable embeds /home/ana/src on one builder and /work/9/src on another. Compiler prefix mapping rewrites both to /src while source maps preserve meaning. **Conclusion:** virtual paths beat stripping useful information.

### Example 3

**Locale.** A generator sorts a, ä, and z using host locale. Builders differ. It adopts a specified bytewise key because display order is nonsemantic. **Conclusion:** locale is declared product input or accidental variation.

### Example 4

**Hermetic but nondeterministic.** Isolated workers append to one file as they finish. No ambient read occurs, yet order changes. Workers receive separate outputs followed by ordered merge. **Conclusion:** isolation cannot replace concurrency correctness.

### Example 5

**Reproducible but nonhermetic.** Ten builds fetch a stable mutable tool URL; the eleventh changes. The tool is fetched and verified by digest before offline build. **Conclusion:** repeated luck is not input closure.

### Example 6

**Meaningful randomness.** A build creates a signing key. Fixing its seed would reproduce bytes while reusing secret material. Key generation moves to deployment and the unsigned payload reproduces. **Conclusion:** security semantics outrank a metric.

### Example 7

**Dirty output.** Warm incremental builds include an undeclared generated schema; clean CI lacks it. The graph gains an explicit generator edge and release starts empty. **Conclusion:** clean execution tests the dependency model.

### Example 8

**Independent mismatch.** Publisher and rebuilder differ. Nested comparison finds a compressor referenced by path rather than digest. Pinning it resolves the mismatch. **Conclusion:** preserve and localize differences.

### Example 9

**Shared compromise.** Two CI jobs match but use one compiler image. A higher-assurance project uses independent compiler lineage and diverse double compilation. **Conclusion:** independence is relative to the threat.

### Example 10

**Semantic exception.** A notarization envelope embeds authorized time and randomized signature. The unsigned payload matches; verification checks payload digest, signature and time while documenting wrapper variability. **Conclusion:** narrow the claim explicitly.

## Cross-Program Connections

- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) owns compiler, linker and bootstrap internals.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns experimental validity and behavior testing.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns compiler trust, sandbox threats, signatures and supply-chain attack analysis.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns build-platform product design.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies configuration identity and verification evidence.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains processes, filesystems, namespaces, clocks and scheduling.

## References

1. Reproducible Builds project, “Definitions,” current documentation. [Official documentation](https://reproducible-builds.org/docs/definition/). Retrieved 2026-09-06.
2. SLSA, *Specification 1.2 — Build Track Basics*, current specification checked 2026-09-06. [Official specification](https://slsa.dev/spec/v1.2/build-track-basics).
3. Chris Lamb and Ximin Luo, *SOURCE_DATE_EPOCH Specification*, revision 1.1, November 2017. [Official specification](https://reproducible-builds.org/specs/source-date-epoch/).
4. Reproducible Builds project, “Timestamps, Build Path, Locales, and Stable Inputs,” current guidance. [Official documentation](https://reproducible-builds.org/docs/).
5. Bazel project, “Hermeticity,” current concepts checked 2026-09-06. [Official documentation](https://bazel.build/basics/hermeticity).
6. Eelco Dolstra, *The Purely Functional Software Deployment Model*, PhD thesis, Utrecht University, 2006. [Institutional record](https://dspace.library.uu.nl/handle/1874/7540).
7. Eelco Dolstra, Merijn de Jonge, and Eelco Visser, “Nix: A Safe and Policy-Free System for Software Deployment,” LISA XVIII, 2004. [USENIX paper](https://www.usenix.org/legacy/events/lisa04/tech/full_papers/dolstra/dolstra.pdf).
8. Ken Thompson, “Reflections on Trusting Trust,” *Communications of the ACM* 27(8), 1984. [DOI record](https://doi.org/10.1145/358198.358210).
9. David A. Wheeler, *Fully Countering Trusting Trust through Diverse Double-Compiling*, PhD dissertation, George Mason University, 2009. [Author record](https://dwheeler.com/trusting-trust/).
10. National Academies of Sciences, Engineering, and Medicine, *Reproducibility and Replicability in Science*, National Academies Press, 2019. [DOI record](https://doi.org/10.17226/25303).

## Exercises

### Exercise 1

**Distinguish properties.** Classify hermeticity, determinism, and observed reproducibility for a sandboxed random build, a networked build fetching unchanged mutable content, a deterministic compiler embedding its working path, and a pinned clean build matching on independent hosts. Explain evidence limits.

### Exercise 2

**Trace hidden inputs.** A documentation archive differs in member order, formatted date, translated month, owner ID, compression header, and source path. Identify each input, decide declare/normalize/preserve, and give a verification procedure.

### Exercise 3

**Diagnose a mismatch.** Two release image digests differ. Design an investigation from image index/configuration through layers, archives, generated code, compiled objects, and signatures. State what evidence to preserve.

### Exercise 4

**Design a hermetic build.** Design fetch, resolve, build, test, package, reproduce, sign, and publish boundaries for a multi-platform command-line tool with generated protocol code and native dependencies.

### Exercise 5

**Transfer to firmware.** A medical-device firmware build needs a proprietary compiler/license service, calibration constants, secure-boot signature, device key, and regulated traceability. Define honest claims, exceptions, evidence, retention, and release blockers.

## Answers to the Exercises

### Answer 1

The sandboxed random build can be hermetic but is nondeterministic and generally will not reproduce. The networked build is nonhermetic even while its response remains stable; matching trials support only observed reproduction. The path-embedding compiler can be deterministic over real inputs but is not reproducible under a declaration omitting path. The pinned clean build has hermeticity evidence only if isolation/traces show ambient reads denied and stronger reproduction evidence if hosts are meaningfully independent. Matching bytes never prove correctness, safe source, uncompromised tools, or future results.

### Answer 2

Member order likely comes from filesystem enumeration and should use specified order if nonsemantic. Date should use source epoch or move to provenance. Month name comes from locale; use fixed machine format unless localization is product behavior. Normalize owner only when installation semantics do not require it. Pin compressor/options and normalize irrelevant headers. Remap ephemeral source path to a virtual root while retaining debugging meaning.

Build from equivalent inputs in clean isolated roots while varying path, user, locale, timezone, clock, creation order, and workers. Deny network, capture reads/processes, compare final digests, recursively inspect mismatches, and test that normalization preserves content and installation.

### Answer 3

Confirm artifact boundary, source, lock, definition, toolchain, parameters and platform. Preserve both images, manifests, input manifests, logs, traces, commands, environments, tools, cache policy, and builder identities. Compare index, selected manifest, configuration and layer digests. Unpack the first differing layer without discarding metadata and inspect names, order, time, ownership, permissions, attributes and content. Recurse into packages, generated files, debug tables, paths, object order and compression; separate embedded signatures. Predict and vary one cause, fix the producer, retest behavior, then reproduce independently.

### Answer 4

Resolve with immutable source, manifests, target matrix, repository snapshots, policy and pinned resolver. Fetch every archive, generator, native library, compiler and sysroot by verified digest into content-addressed storage. Build receives only that read-only closure, explicit environment, source epoch, virtual path, target and empty output; network and host reads fail.

Generated protocol code is keyed by schema and generator. Native dependencies and sysroots are target-specific; each target has its own artifact digest and a release manifest binds the set. Trust-namespaced caches cover every semantic input. Tests run on exact packages in representative runtimes. Independent builders reproduce targets. Detached signatures and provenance bind final digests; incomplete publication is unselectable. Missing input, undeclared access, failed test, unexplained mismatch, or unverifiable digest fails the applicable gate.

### Answer 5

Declare compiler, plugins, sysroot, source, build definition, parameters and calibration dataset. If the license service only authorizes execution, isolate and trace it; if its response affects bytes, content-bind the response or admit nonhermeticity. Retain licensed offline tools where contracts allow.

Claim bit reproduction for unsigned common firmware under the named toolchain and calibration class when independent builders match. Personalized calibration/key output is a distinct artifact. Generate private keys outside general build and never fix cryptographic randomness for equality. Treat secure-boot signature/time as detached or an explicitly variable authenticated wrapper.

Evidence includes hashes, access traces, clean builds, path/time/locale variation, byte comparison, diverse-tool analysis where feasible, hardware-in-loop tests, calibration validation, signing audit, provenance, and retention exercises. Block release on unexplained mismatch, missing historic inputs, influential undeclared service response, invalid calibration identity, absent hardware evidence, key-policy failure, or regulatory traceability gap. Legitimate safety, quality, security, clinical, and regulatory authorities decide release.
