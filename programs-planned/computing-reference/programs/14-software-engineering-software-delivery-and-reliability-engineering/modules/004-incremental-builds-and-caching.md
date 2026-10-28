---
module_id: SDRE-004
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 4
title: Incremental Builds and Caching
status: complete
last_verified: 2026-09-06
---

# Incremental Builds and Caching

## One-Page Review

### Governing question

How can a build reuse prior work without returning an output that a clean build from the current effective inputs would reject?

### Essential definitions

- a **build graph** is a directed graph of artifacts or actions and their dependency relations;
- an **action** transforms a declared input closure under a rule, toolchain, parameters, and platform into named outputs;
- an **incremental build** evaluates what changed and re-executes only actions whose previous results are no longer valid;
- a **clean build** begins without reusable action results or intermediate outputs;
- **invalidation** decides that a previous result may not be reused;
- a **false hit** reuses a result although a semantic input changed; it is a correctness defect;
- a **false miss** rebuilds although every semantic input is equivalent; it wastes work but ordinarily preserves correctness;
- an **action key** is a canonical identity for everything allowed to affect an action result;
- an **action cache** maps an action key to result metadata;
- a **content-addressable store** (CAS) maps a content digest to bytes;
- a **dynamic dependency** is discovered while or after an action runs and must be recorded for later invalidation;
- **cache poisoning** makes a key resolve to bytes that were not produced by the authorized equivalent action.

### Central model, mechanism, or theorem

For action $v$, let $E_v$ be its complete semantic input state and let $F_v$ be a deterministic action. A sound cache key $K$ must satisfy

$$
K(E_1)=K(E_2) \Longrightarrow F_v(E_1)=F_v(E_2).
$$

A practical key is a canonical digest of the rule identity, declared source digests, dependency-output digests, toolchain, parameters, target platform, and relevant environment. On a hit, the action cache returns output digests and the CAS supplies verified bytes. On a miss, the action executes and publishes its result only after success and digest verification.

If an influential component $x$ is omitted, choose states differing only in $x$ for which the output differs. They receive the same key but require different results, contradicting sound reuse. Including irrelevant state avoids that contradiction but causes false misses.

### Critical invariants

- every read that can affect output is represented in the dependency graph or action key;
- rules, generators, toolchains, flags, targets, and relevant environment are inputs, not invisible infrastructure;
- deletions, directory membership, symlink targets, permissions, and absence can be semantic inputs;
- dependency discovery is recorded before a result becomes reusable;
- cache entries are published atomically only after successful execution;
- downloaded bytes are verified against their content digest;
- untrusted writers cannot populate trusted cache namespaces;
- clean and cache-disabled builds remain available as correctness oracles;
- an incremental result is compared with a clean result over the same declared inputs;
- hit rate is never treated as correctness, reproducibility, or useful latency by itself.

### Common failures

Common failures include timestamp skew, undeclared headers, stale generated files, a key that omits compiler version, environment leakage, globs that ignore additions, missing deletion edges, noncanonical serialization, sharing results across incompatible platforms, publishing partial outputs, letting untrusted changes write a protected cache, trusting a claimed digest, counting metadata hits while transferring expensive blobs, and validating only warm builds.

### Compact example

A compiler action depends on source `s`, imported header `h`, compiler `c`, flags `f`, and target `p`. A cache keyed only by `(s, f)` hits after `h` or `c` changes and returns a stale object. A corrected key uses `(digest(s), digest(h), digest(c), f, p)`. Repeating identical state hits; changing source, header, compiler, flags, or target misses. A clean comparison then checks that the retrieved object equals fresh execution. The key design prevents this modeled false hit; it does not prove the dependency set complete or the compiler correct.

### Connections

[SDRE-003](003-reproducible-and-hermetic-builds.md) establishes the input closure and determinism that safe reuse needs. [SDRE-005](../ROADMAP.md) next treats repositories that retain and distribute durable artifacts rather than ephemeral action results.

## Governing Question

Fast builds depend on remembering. Correct builds depend on forgetting exactly when prior results cease to represent the current program. The hard problem is therefore not storing bytes; it is defining equivalence. Which changes are semantically relevant to one action, how are they observed, and under what authority may old output stand in for new execution?

An incremental build answers locally: keep valid results and rebuild the affected subgraph. A cache answers across invocations or machines: reuse a result indexed by an action identity. Both are optimizations of a clean build, not alternative definitions of correctness. Their contract is that reuse must be observationally equivalent to executing the action now under the same effective inputs.

## Why This Matters

Large systems can contain thousands of compilation, generation, test, packaging, and analysis actions. Repeating all of them after a one-line change wastes developer time and CI capacity. Fine-grained invalidation shortens feedback, while shared remote caches amortize work across developers and runners.

The speedup is dangerous precisely because it hides execution. A stale object may pass local tests, a deleted schema may survive in a dirty tree, or an untrusted pull request may place malicious output under a key later read by a protected release. The absence of execution also means a cache hit supplies no new evidence that today's tools would produce the same result.

Mokhov, Mitchell, and Peyton Jones model build systems by separating how dependencies are scheduled from how rebuilding is decided [1]. GNU Make documents the classic timestamp rule: a target is out of date when absent or older than a normal prerequisite [2]. Modern systems add content identities, dynamic dependencies, sandboxing, and remote action caches, but they cannot escape the central requirement: recorded dependencies must represent real influence.

## Prerequisites and Retrieval

Retrieve target, prerequisite, action, rule, dependency graph, transitive closure, digest, canonical serialization, toolchain, platform, environment, deterministic function, hermeticity, clean build, reproducible build, artifact identity, concurrency, atomic publication, authentication, authorization, and threat boundary.

From SDRE-001 retrieve the distinction among source, build, artifact, release, and deployment identities. From SDRE-002 retrieve resolved and content-verified dependency graphs. From SDRE-003 retrieve effective input closure, hermetic isolation, deterministic execution, and the limits of matching digests.

## Learning Objectives

After completing this module, you should be able to:

1. model incremental rebuilding over an action dependency graph;
2. distinguish timestamp, content, trace, and rule-based invalidation;
3. construct and review a canonical action key;
4. prove the key-completeness obligation under explicit assumptions;
5. distinguish false hits from false misses and prioritize them correctly;
6. handle generated, discovered, negative, directory, and platform dependencies;
7. separate an action cache from a content-addressable store;
8. design atomic, authenticated, trust-separated cache publication;
9. validate incremental correctness against clean and cache-disabled builds;
10. evaluate cache performance using latency and avoided work rather than hit rate alone.

## Core Exposition

**Start with the graph.** Let $G=(V,E)$ be a directed acyclic build graph for one requested output. A node may represent an artifact or an action; this chapter uses action nodes. An edge $u\to v$ means the result of $v$ can depend on output from $u$. The scheduler may execute ready nodes in parallel, but an incremental evaluator first decides which recorded results remain valid.

The graph is not merely an ordering plan. A dependency edge asserts influence. If header `types.h` changes compilation of `parser.c`, its digest must reach the compile action even if the command line names only `parser.c`. Missing edges permit false hits. Spurious edges cause false misses and enlarge the affected subgraph.

**Define effective input state.** For an action $v$, write

$$
E_v=(R_v,I_v,D_v,T_v,P_v,X_v),
$$

where $R_v$ identifies the rule or command, $I_v$ the direct declared inputs, $D_v$ dependency outputs, $T_v$ the toolchain, $P_v$ parameters and target platform, and $X_v$ other declared semantic context such as relevant environment. Values are represented by canonical identities, normally content digests plus type and path semantics where paths matter.

An input may be positive or negative. “Directory contains exactly these schema files,” “optional configuration is absent,” and “symlink resolves to this target” can affect behavior. Tracking only bytes of files opened on the successful branch misses absence and membership dependencies.

**Construct the action key.** Abstractly,

$$
K_v=H(encode(v,E_v)),
$$

where `encode` is deterministic and unambiguous and $H$ is an accepted collision-resistant digest. Names and boundaries matter: concatenating `ab|c` and `a|bc` without length or type encoding is ambiguous. Sort sets by a specified order, preserve sequence where order is semantic, and version the schema.

The digest is not magic. It compresses a modeled identity. If the model omits the compiler, digesting it perfectly still yields an unsound key. If the model includes the workstation hostname despite no influence, correctness survives but sharing collapses.

**Separate metadata from bytes.** An action cache maps $K_v$ to an action result: exit status, output names and digests, and perhaps logs or execution metadata. A CAS maps each content digest to bytes. The Remote Execution API makes this distinction explicit, addressing an `ActionResult` by action digest while addressing blobs by their own content [3]. A hit is useful only if every referenced blob is present and verifies.

On a miss, the executor receives the declared input root, command, platform, and limits, runs the action, verifies its outputs, uploads missing blobs, and publishes result metadata. Publication should be atomic from the reader's perspective. An interrupted upload must not expose a result whose blobs are absent or partial.

**Compare invalidation strategies.** Timestamp invalidation is inexpensive but interprets clock and filesystem metadata as proxies for content. GNU Make's normal prerequisite is out of date when newer than its target [2]. Clock skew, preserved timestamps, low timestamp resolution, replacement with older content, or future-dated files can violate that proxy. It remains useful in bounded local settings when its assumptions are explicit.

Content invalidation compares bytes rather than time. It detects same-time edits and avoids rebuilding when metadata changes without content. Hashing costs I/O and does not discover which files matter. Hybrid systems use filesystem observations to narrow rehashing, persistent graph state, or operating-system change journals; every shortcut adds assumptions that need adversarial tests.

**Track dynamic dependencies.** A compiler may discover imported headers only after preprocessing; a generator may read a manifest that names more files. The system can require static declaration, consume compiler depfiles, trace reads, or let rules register dependencies dynamically. Shake explicitly supports dependencies discovered after prior rules and dependencies on directory contents, environment values, and compiler versions [4]. Pluto develops sound incremental rebuilding with dynamically discovered dependencies by enforcing graph invariants during execution [5].

A discovered dependency must affect the current result and future checks. Publishing first and recording later opens a window for stale reuse. When discovery itself depends on input, the trace must be replaced when the action reruns. A warm trace is evidence about one path, not proof that every future branch has no other read. Riker illustrates a forward-build alternative that models broader POSIX filesystem state rather than only already-known files [8].

**Propagate change precisely.** Suppose generator $g$ reruns because its source changed but emits identical bytes. A content-based downstream node may remain valid because its semantic dependency output did not change. This is early cutoff: recomputation of an upstream node need not force the whole transitive consumer graph when the observed value is equal. Conversely, a rule change can invalidate outputs even when source bytes are unchanged.

**Control concurrency.** Parallel scheduling preserves correctness only if dependencies are complete and actions do not race through shared undeclared state. Each action should write a private staging area, then publish named outputs atomically after success. Two workers computing the same key may execute redundantly; either result is reusable only if the action is deterministic and equivalent. Request coalescing is a performance policy, not a substitute for those premises.

**Treat remote reuse as a trust decision.** A remote cache expands the writer and transport boundary. Authenticate readers and writers, authorize namespaces, use encrypted transport where appropriate, verify content digests after download, and isolate protected releases from untrusted contributions. Bazel's current documentation recommends care over write access and notes that a team may allow only CI to write [6]. The Remote Execution API includes an action salt to separate results potentially poisoned by buggy software or tool failures [3]. Namespace invalidation helps incident response but cannot repair artifacts already promoted.

**Test the optimizer against its specification.** The most important test compares a warm incremental build with a clean, cache-disabled build from identical declared inputs. Compare the full output boundary by digest and, where needed, behavior. Generate edit sequences containing additions, modifications, deletions, renames, permission changes, toolchain upgrades, flag changes, target changes, and failed actions. For each sequence, assert equality with the clean oracle. Reliable-build research likewise treats incremental correctness and dependency completeness as first-class design concerns [7].

Instrument rebuilding reasons: changed input, changed rule, missing result, missing blob, policy bypass, trust rejection, or nondeterministic output. A cache-hit number without these explanations makes correctness incidents difficult to diagnose.

**Measure useful economics.** Let $M$ be missed actions, $c(v)$ local execution cost, $l(v)$ lookup cost, $t(v)$ transfer cost, and $q(v)$ queue cost. A simple nonparallel estimate is

$$
T\approx\sum_{v\in V}l(v)+\sum_{v\in M}(c(v)+q(v))+\sum_{v\in hit}t(v).
$$

Real wall time follows critical paths and resource contention, not this sum. A 95% hit rate can be slow when the missed 5% contains linking or when cached blobs exceed local computation cost. Track avoided weighted work, p50/p95 latency, critical-path misses, bytes transferred, lookup errors, eviction, and correctness incidents.

## Definitions and Notation

- $G=(V,E)$: action dependency graph for a requested build;
- $pred(v)$: direct predecessors whose outputs may influence $v$;
- $E_v$: complete semantic input state of action $v$;
- $F_v(E_v)$: outputs of executing $v$ on that state;
- $K_v$: canonical action key for $v$;
- $H$: accepted collision-resistant content digest;
- $C_A$: action cache mapping action keys to result metadata;
- $C_B$: content-addressable store mapping content digests to bytes;
- $M$: actions that miss or are invalidated in one build;
- **observational equivalence**: equality under the declared output and behavior boundary;
- **sound reuse**: a hit only when current execution would be observationally equivalent;
- **minimal invalidation**: every invalid action and no semantically valid action is rebuilt, relative to the declared model.

Assume for the formal claims that action execution terminates, $F_v$ is deterministic over $E_v$, canonical encoding is injective over modeled tuples, digest collisions are outside the accepted threat model, and referenced dependency outputs are verified. Real systems must record where these assumptions weaken.

## Mechanisms, Invariants, or Proof Structure

**Sound-key proposition.** If $K$ includes a canonical identity for every component of $E$, $F$ is deterministic over $E$, and the digest/encoding assumptions hold, then equal keys imply equal modeled inputs and therefore equal outputs.

**Proof.** Let $K(E_1)=K(E_2)$. Under the collision and canonical-encoding assumptions, `encode(E1)=encode(E2)`. Injectivity yields $E_1=E_2$. Since $F$ is a function over complete $E$, substitution gives $F(E_1)=F(E_2)$. This proves sound reuse only for the modeled output boundary and assumptions.

**Omitted-input counterexample.** Suppose compiler output is $F(s,c)$ and compiler identity $c$ affects code generation, but $K=H(s)$. Choose $c_1$ and $c_2$ that emit different bytes for the same $s$. Then keys are equal while outputs differ. Thus the key is unsound. No stronger digest repairs a missing input.

**Over-inclusion argument.** Add irrelevant nonce $n$ to a complete key although $F(E,n)=F(E)$ for all $n$. Different nonces create misses but fresh execution still computes the correct output. Over-inclusion reduces performance; under-inclusion violates correctness. This asymmetry justifies conservative invalidation during uncertainty.

**Graph invariant.** Before executing $v$, every required predecessor result is valid. Before publishing $v$, every observed semantic input is included in $E_v$, every output blob verifies, and result metadata references a complete output set. A failed or cancelled action publishes no reusable result.

**Executable verification.** The following finite model uses tuples as already canonical identities so the example needs no hashing library. The sound cache includes source, header, compiler, flags, and platform. The buggy cache omits header and compiler to demonstrate a false hit.

<!-- bijux-verify: {"id":"model-action-cache","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=miss\nrepeat=hit\nsource_change=miss\ntoolchain_change=miss\nplatform_change=miss\nbuggy_false_hit=True\nclean_matches_sound=True\n","stderr":""}} -->
```python
sound_cache = {}
buggy_cache = {}

def execute(source, header, compiler, flags, platform):
    return "|".join((compiler, platform, flags, header, source)).upper()

def sound_build(source, header, compiler, flags, platform):
    key = (source, header, compiler, flags, platform)
    if key in sound_cache:
        return "hit", sound_cache[key]
    output = execute(source, header, compiler, flags, platform)
    sound_cache[key] = output
    return "miss", output

def buggy_build(source, header, compiler, flags, platform):
    key = (source, flags, platform)
    if key not in buggy_cache:
        buggy_cache[key] = execute(source, header, compiler, flags, platform)
    return buggy_cache[key]

print(f"first={sound_build('src-a', 'hdr-a', 'cc-1', '-O2', 'linux-x86')[0]}")
print(f"repeat={sound_build('src-a', 'hdr-a', 'cc-1', '-O2', 'linux-x86')[0]}")
print(f"source_change={sound_build('src-b', 'hdr-a', 'cc-1', '-O2', 'linux-x86')[0]}")
print(f"toolchain_change={sound_build('src-a', 'hdr-a', 'cc-2', '-O2', 'linux-x86')[0]}")
print(f"platform_change={sound_build('src-a', 'hdr-a', 'cc-1', '-O2', 'linux-arm')[0]}")

old = buggy_build('src-a', 'hdr-a', 'cc-1', '-O2', 'linux-x86')
wrong = buggy_build('src-a', 'hdr-b', 'cc-2', '-O2', 'linux-x86')
fresh = execute('src-a', 'hdr-b', 'cc-2', '-O2', 'linux-x86')
print(f"buggy_false_hit={wrong == old and wrong != fresh}")

sound = sound_build('src-a', 'hdr-b', 'cc-2', '-O2', 'linux-x86')[1]
print(f"clean_matches_sound={sound == fresh}")
```

This execution verifies only the tuple-keyed model under the recorded Python environment. It does not implement hashing, filesystem observation, a compiler, a CAS, sandboxing, remote transport, or hostile-writer defense.

## Alternatives and Trade-Offs

**Timestamps versus content.** Timestamps are cheap but depend on clock and metadata assumptions. Content identities are stronger for equality but cost reads and still need complete dependencies.

**Static versus dynamic dependencies.** Static declarations are reviewable before execution but can be tedious or impossible for data-dependent reads. Dynamic discovery represents reality better but requires tracing, stable recording, and careful first-run semantics.

**Fine versus coarse actions.** Fine nodes improve reuse and parallelism but add graph, scheduling, storage, and transfer overhead. Coarse nodes are simpler but invalidate more work.

**Local versus remote cache.** Local reuse has a narrow trust boundary and low latency. Remote reuse shares work across machines but adds authentication, authorization, bandwidth, eviction, availability, privacy, and poisoning risks.

**Eager versus lazy materialization.** Downloading every hit simplifies a conventional output tree. Lazy access can save bandwidth but introduces runtime availability and eviction dependencies.

**Fail open versus fail closed.** Falling back to local execution on cache unavailability preserves delivery when inputs are local. Reusing unverifiable bytes does not. A cache should be an optional performance service unless the system explicitly defines stronger availability coupling.

**Aggressive versus conservative invalidation.** Aggressive reuse improves latency but risks false hits when knowledge is incomplete. Conservative rebuilding incurs false misses while preserving the clean-build contract.

## Failure Modes and Misconceptions

- **“The source did not change.”** Headers, rules, generators, tools, flags, and targets can.
- **“Newer means different.”** Timestamp order is a proxy, not content identity.
- **“Same digest means complete key.”** A digest cannot reveal omitted inputs.
- **“All file reads are dependencies.”** Absence, directory membership, metadata, and services also matter.
- **“The depfile is always current.”** Its discovery path can change and must update atomically.
- **“A clean build is waste.”** It is the reference that exposes incremental divergence.
- **“High hit rate means fast.”** Expensive misses and transfers dominate latency.
- **“High hit rate means correct.”** An unsound key can achieve excellent hits.
- **“CAS and action cache are the same.”** One names bytes; the other names execution results.
- **“Remote cache is trusted storage.”** Writers, transport, server, and namespace are threat surfaces.
- **“Digest verification prevents poisoning.”** It verifies bytes against a name, not authorization for the action result.
- **“Eviction is corruption.”** Eviction should become a miss; dangling result metadata is an integrity failure.
- **“One warm success validates the graph.”** Stale state can mask missing edges.
- **“Parallel execution only changes speed.”** Undeclared shared state can create races and nondeterminism.
- **“Cache invalidation solves bad outputs.”** Already promoted artifacts require separate incident response.

## Worked Examples

### Example 1

**Timestamp reversal.** `model.o` was copied from another machine with a future timestamp. `model.c` changes, but a timestamp rule sees the object as newer and skips compilation. A content-based key compares source bytes and misses. **Conclusion:** timestamp soundness depends on clock and metadata assumptions.

### Example 2

**Undeclared header.** A compiler reads `config.h`, but the graph records only `main.c`. Editing the header leaves the compile key unchanged. Depfile ingestion adds the header before result publication; a clean/incremental comparison confirms equality. **Conclusion:** observed transitive reads belong in the key.

### Example 3

**Unchanged generated output.** A schema generator reruns after comments change but emits identical code. Its output digest remains equal, so downstream compilation stays valid. **Conclusion:** early cutoff avoids propagating nonsemantic changes.

### Example 4

**Directory membership.** A generator processes `schemas/*.json`. Adding `refund.json` is not a read of any previously known file. Tracking the directory's canonical member set invalidates the generator. **Conclusion:** additions require negative or membership dependencies.

### Example 5

**Toolchain upgrade.** Two compilers accept identical source and flags but emit different object bytes. A key omitting compiler identity falsely hits. Adding the compiler and sysroot digests separates results. **Conclusion:** tools are semantic inputs.

### Example 6

**Failed publication.** A worker uploads two of three output blobs, then crashes. It never publishes action-result metadata. Readers miss rather than observe a partial result. **Conclusion:** blobs may arrive incrementally, but reusable metadata must be atomic and complete.

### Example 7

**Untrusted writer.** A pull-request job can guess a release action key and upload malicious metadata. The service makes fork jobs read-only in a separate namespace; protected CI alone can write release results, and clients verify blobs. **Conclusion:** content identity does not replace writer authorization.

### Example 8

**Expensive hit.** Ninety-nine tiny actions hit remotely, but a 4 GB cached link output takes longer to download than local relinking. Policy executes that action locally while retaining smaller hits. **Conclusion:** optimize critical-path time and transfer cost, not hit count.

### Example 9

**Cross-platform collision.** An action key includes source and compiler name but omits target ABI. An x86 result is offered to an Arm build. Adding target triple, sysroot, and relevant platform properties forces a miss. **Conclusion:** platform compatibility must be encoded, not inferred from a worker label.

### Example 10

**Randomized differential test.** A harness applies file edits, additions, deletions, renames, flag changes, and compiler changes. After every operation it compares the warm result with a clean cache-disabled build. A deletion exposes a stale generated file and missing absence edge. **Conclusion:** adversarial edit sequences test the invalidation contract.

## Cross-Program Connections

- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) owns incremental compiler internals, dependency extraction, and object generation.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies graphs, hashing, maps, and traversal mechanisms.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains filesystems, timestamps, processes, permissions, and atomic rename behavior.
- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) owns consistency, replication, partial failure, and distributed storage models.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns authentication, authorization, cache poisoning threats, and cryptographic analysis.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns remote-build and cache services as developer-platform products.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns differential, property-based, and adversarial testing methods.

## References

1. Andrey Mokhov, Neil Mitchell, and Simon Peyton Jones, “Build Systems à la Carte: Theory and Practice,” *Journal of Functional Programming* 30, April 2020. [DOI and author record](https://www.microsoft.com/en-us/research/publication/build-systems-a-la-carte/). Retrieved 2026-09-06.
2. Free Software Foundation, *GNU Make Manual*, “Rule Syntax,” current manual checked 2026-09-06. [Official manual](https://www.gnu.org/software/make/manual/html_node/Rule-Syntax.html).
3. Bazel Remote APIs project, *Remote Execution API v2*, `remote_execution.proto`, current main-branch specification checked 2026-09-06. [Official specification repository](https://github.com/bazelbuild/remote-apis/blob/main/build/bazel/remote/execution/v2/remote_execution.proto).
4. Neil Mitchell, “Why Shake,” current project documentation. [Official documentation](https://shakebuild.com/why). Retrieved 2026-09-06.
5. Sebastian Erdweg, Moritz Lichter, and Manuel Weiel, “A Sound and Optimal Incremental Build System with Dynamic Dependencies,” OOPSLA 2015. [Author-hosted paper](https://www.mathematik.uni-marburg.de/~seba/publications/pluto-incremental-build.pdf). Retrieved 2026-09-06.
6. Bazel project, “Remote Caching,” current documentation checked 2026-09-06. [Official documentation](https://bazel.build/remote/caching).
7. Derrick Coetzee, Anand Bhaskar, and George Necula, “A Model and Framework for Reliable Build Systems,” Technical Report UCB/EECS-2012-27, February 2012. [UC Berkeley record](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/EECS-2012-27.html).
8. Charlie Curtsinger and Daniel W. Barowy, “Riker: Always-Correct and Fast Incremental Builds from Simple Specifications,” *2022 USENIX Annual Technical Conference*, pages 885–898, July 2022. [USENIX paper and record](https://www.usenix.org/conference/atc22/presentation/curtsinger). Retrieved 2026-09-06.

## Exercises

### Exercise 1

**Classify invalidation.** For timestamp-only, content-only, complete content-key, and trace-based systems, classify what happens after same-content touch, older-timestamp replacement, undeclared header edit, and compiler upgrade. Identify false hits and false misses.

### Exercise 2

**Derive a key.** Define an unambiguous action key for compiling one C source with transitive headers, generated configuration, compiler/sysroot, flags, target ABI, selected environment, and output schema. State every assumption behind sound reuse.

### Exercise 3

**Diagnose divergence.** A warm CI build passes while a clean build fails after a schema deletion. Give an investigation and repair procedure, including evidence to retain and tests to add.

### Exercise 4

**Design a remote cache.** Design read/write authority, namespaces, action results, CAS verification, atomic publication, eviction, failure fallback, logging, and incident invalidation for protected release CI and untrusted pull requests.

### Exercise 5

**Transfer to data products.** A feature pipeline caches transformations over source tables, query code, calendar data, privacy policy, and runtime engine. Adapt the build-cache model, identify invalidation hazards, and define a clean oracle and release gate.

## Answers to the Exercises

### Answer 1

A same-content touch creates a false miss for timestamp-only systems and normally no miss for content systems. Replacing content while preserving or reversing timestamp can false-hit under timestamps but misses under content identity. An undeclared-header edit false-hits in every system whose declared set or trace omitted that header; content hashing cannot hash an unknown dependency. A compiler upgrade false-hits unless compiler identity reaches the key or trace. A complete content key misses exactly for semantic changes under its assumptions. A trace-based system can discover the header, but only if the observed execution path reads it and the trace is recorded before reuse. Conservative uncertainty should miss rather than hit.

### Answer 2

Use a typed, length-delimited, schema-versioned encoding of rule identity; ordered command arguments; digest and logical path of the source, every transitive header, and generated configuration; compiler binary, plugins, linker where invoked, sysroot and relevant runtime data; target triple/ABI; explicitly selected environment values; working-directory semantics; output names and schema; and dependency-output digests. Sort sets canonically but preserve semantic order in arguments and search paths.

Soundness assumes this is the complete effective input closure, actions cannot read ambient state, execution is deterministic over the tuple, identities refer to verified bytes, encoding is injective, the digest assumption holds, platform properties are sufficient, and output comparison covers all observable results. A clean differential build tests these assumptions but does not prove them universally.

### Answer 3

Preserve warm and clean outputs, graph state, action keys, traces, depfiles, schema directory listings, logs, tool versions, cache decisions, source revision, and the edit sequence. Identify the first differing action rather than only the final test. Check whether deletion was modeled as directory membership or absence, whether a stale generated file survived in the output tree, and whether the generator atomically replaced its complete output set.

Repair by tracking the canonical schema member set, running the generator in a private empty directory, deleting outputs no longer declared, and publishing the complete set atomically. Invalidate affected namespaces. Add deletion, rename, empty-directory, failed-generation, warm-versus-clean, and cache-disabled differential tests. Rebuild and retest any artifact that may have consumed the stale schema; a corrected cache does not retroactively repair promoted output.

### Answer 4

Use authenticated transport and separate namespaces by repository, trust class, platform, toolchain policy, and key-schema generation. Untrusted pull requests may read an approved public namespace if confidentiality permits but cannot write protected results. Protected CI writes only after policy and execution success. The action cache maps canonical action digests to complete metadata; the CAS accepts bytes only after recomputing their digest. Publish action metadata only when all referenced blobs exist and are retained long enough for retrieval.

Eviction of a blob makes the action result unusable and therefore a miss. Cache outage falls back to authorized local execution; unverifiable output never becomes a fallback. Log actor, namespace, action digest, source context, result digests, hit/miss/rejection reason, and policy generation without leaking secrets. During poisoning, revoke writes, preserve forensic records, rotate or abandon the namespace, rebuild protected artifacts from clean trusted inputs, and assess already promoted releases.

### Answer 5

Treat each transformation as an action. Its semantic state includes source-table snapshot IDs and schemas, query and library bytes, parameters, calendar/timezone revision, privacy-policy generation, runtime engine and relevant configuration, target feature schema, and upstream output digests. Partition identities by tenant and authorization where output visibility differs.

Hazards include mutable table names, late-arriving rows, corrected history, nondeterministic queries, implicit current date, engine upgrades, unordered aggregation, privacy-policy changes, and cross-tenant poisoning. A high hit rate can mean stale features. The clean oracle recomputes from immutable snapshots with caches disabled and compares the complete feature set plus selected behavior and policy checks. Release is blocked by unexplained divergence, missing snapshot lineage, unauthorized cache provenance, policy mismatch, failed freshness bounds, or unverifiable output identity. Domain owners decide whether late data requires backfill; the cache mechanism does not make that policy decision.
