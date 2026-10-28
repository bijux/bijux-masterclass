---
module_id: META-002
program: Programming Languages: Metaprogramming
level: 1
module_number: 2
title: Compile-Time, Build-Time, Load-Time, and Run-Time Metaprogramming
status: complete
last_verified: 2026-08-29
---

# Compile-Time, Build-Time, Load-Time, and Run-Time Metaprogramming

## One-Page Review

### Governing question

How should an engineer place program inspection, generation, transformation, and specialization across compile time, build time, load time, and run time so that dependencies, authority, diagnostics, caching, and failures remain explicit?

### Essential definitions

- A **phase** is an execution environment and ordering boundary relative to a named subject artifact, not merely a wall-clock interval.
- **Compile-time metaprogramming** runs as part of translating or statically analyzing the subject program and can emit syntax, declarations, types, constants, diagnostics, or residual code.
- **Build-time metaprogramming** runs under the build graph to produce or transform source, resources, configuration, or binary inputs before a downstream action.
- **Load-time metaprogramming** acts while an artifact is resolved, imported, linked into, defined within, or initialized by a runtime.
- **Run-time metaprogramming** inspects, creates, replaces, interprets, or specializes program behavior after the subject execution has begun.
- A **phase distinction** says which values and bindings are available at each stage and which computations may cross from one stage to another.
- **cross-stage persistence** makes a value produced earlier available later through embedding, serialization, linkage, or another explicit mechanism.
- A **residual program** is code left for a later stage after earlier-stage computation.
- A **phase environment** includes tools, target, filesystem, environment variables, network, secrets, clock, randomness, privileges, and limits visible at that stage.
- **invalidation** determines which declared input changes require a phase to run again and which cached output is no longer valid.

### Central model, mechanism, or theorem

For subject artifact $A$, model phase $p$ as

$$
F_p:(R_p,E_p,I_p)\rightarrow(O_p,D_p,\Pi_p),
$$

where $R_p$ is program representation, $E_p$ phase environment, $I_p$ declared inputs, $O_p$ residual output, $D_p$ diagnostics, and $\Pi_p$ provenance. Phase order is a dependency graph, not always the simple line

$$
author\prec build\prec compile\prec load\prec run.
$$

A compiler can invoke a compiled macro; a running virtual machine can JIT-compile code; a build action can compile a generator before executing it. Correctness requires every edge to carry an explicit representation and only values available at its source phase.

### Critical invariants

- Name the subject artifact before naming its phase.
- A phase may depend only on bindings and declared capabilities available in its phase environment.
- Outputs crossing phases are validated, versioned, and traceable to inputs and toolchain.
- Cache keys cover every input that can affect output; undeclared reads invalidate reproducibility claims.
- Earlier failure improves feedback only if diagnostics map to the originating user input.
- Moving work earlier does not automatically make it safe, deterministic, cheap, or semantically valid.
- Load- and run-time transformations preserve runtime concurrency, initialization, identity, and security invariants.
- Generated code is tested at both the generator phase and consumer phase.

### Common failures

Common failures are calling every pre-deployment action “compile time,” reading runtime configuration in a compile-time computation, hiding network access in a build script, caching output without environment/tool versions, treating import execution as pure loading, assuming load order is fixed, generating code at startup on every instance, embedding secrets into residual artifacts, losing source spans, confusing JIT compilation time with the original build, and moving validation earlier while leaving a later bypass.

### Compact example

A schema generator runs as build action $G$, reads `api.yaml` and generator version $v$, emits `client.rs` plus a digest, then the Rust compiler type-checks the result. The correct cache key contains the schema bytes, $v$, target options, and relevant configuration. A generator success does not imply that emitted code compiles; compilation success does not imply that a deployed service accepts the same schema version.

### Connections

Retrieve [META-001's subject, representation, operation, phase, and claim model](001-programs-about-programs.md). [META-003](../ROADMAP.md) develops staging and binding-time analysis. Phase boundaries connect to [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md), [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

When should a computation about a program occur, and what evidence shows that its chosen stage has the values, authority, reproducibility, diagnostics, and performance properties the system requires?

“Do it at compile time” often compresses several distinct proposals: reject an invalid expression during type checking, expand a macro, evaluate a constant, run a schema generator before compilation, execute an annotation processor, transform bytecode as a class loads, or specialize a hot path inside a running virtual machine. These mechanisms differ in representation, available knowledge, privileges, caching, and observable failure. Phase-aware design makes those differences reviewable.

## Why This Matters

Phase placement determines who pays and who can recover. A compile-time rejection can prevent an invalid artifact from existing, but may slow every developer build. A build generator can unify boilerplate, but undeclared filesystem reads make incremental builds stale. A load-time agent can instrument third-party bytecode without source, but participates in initialization and carries process authority. A run-time proxy can adapt to live configuration, but pushes errors and overhead into production requests.

Metaprograms also form a supply chain. Their code executes under compiler, build worker, loader, or application credentials. Their outputs may be checked in, cached, signed, deployed, or generated repeatedly. A phase label without an input/capability model hides both correctness and security obligations.

## Prerequisites and Retrieval

You should understand the program-representation model from [META-001](001-programs-about-programs.md), compilation and linking at an introductory level, modules/imports, build dependency graphs, caching, lexical scope, and basic threat modeling. Retrieve:

1. A program can be data at one phase and executable authority at another.
2. A transformation has both its own execution and the later execution of its result.
3. Build reproducibility requires all output-affecting inputs to be declared or controlled.
4. Static availability is different from runtime availability.
5. Earlier detection and better diagnosis are separate properties.

## Learning Objectives

After completing this module, you should be able to:

- define compile-, build-, load-, and run-time metaprogramming relative to a subject;
- draw a phase dependency graph for nested generators, compilers, loaders, and JITs;
- identify representations, bindings, effects, credentials, and limits at each phase;
- explain cross-stage persistence and residual programs;
- distinguish rejection time, generation time, artifact time, and observation time;
- design complete cache keys and invalidation rules for generators;
- compare early and late placement by information, cost, portability, diagnostics, and security;
- trace load/import hooks without assuming that loading is effect-free;
- specify evidence at both meta-execution and residual-execution levels;
- diagnose phase confusion in a production pipeline.

## Core Exposition

### Phase is relative to a subject

Choose the artifact whose lifecycle is being described. A procedural macro is compiled before it runs during compilation of another crate. It is run time for the macro executable and compile time for the subject crate. A compiler built by a build action is an output of one compilation and a tool in another. A JIT compiler runs after application startup while compiling a method that has not yet executed in native form. These statements are compatible because phase names are relative.

Use qualified phrases: “compile time of the subject module,” “build time of the release artifact,” or “load time of class C in process P.” Wall-clock order alone is insufficient because builds execute independent nodes concurrently, modules load lazily, and runtime code can initiate further compilation.

### Compile-time metaprogramming

Compile-time mechanisms participate in language translation or static analysis. Examples include syntax macros, derive systems, templates that instantiate declarations, constant evaluation, compiler plugins, and annotation processing. Inputs can include tokens, syntax trees, typed program elements, compiler options, target information, and explicitly permitted files. Outputs can include syntax, typed declarations, constants, diagnostics, object-code contributions, or a residual program.

The advantage is access to language structure and the ability to reject an artifact before execution. The costs are compiler coupling, build latency, complex diagnostics, resource blowups, and temptation to read hidden environment state. Rust's current Reference, for example, specifies procedural macros as compile-time functions over token streams and warns that they have compiler-like filesystem/resource access. That is one concrete model, not a universal sandbox guarantee.

A compile-time calculation cannot generally inspect a value that will be received only from a production request. It can generate code parameterized by that future value or embed an earlier value through an allowed cross-stage mechanism. This is the fundamental phase-separation rule: later data cannot flow backward without changing the system, such as adding profiling feedback and a subsequent rebuild.

### Build-time metaprogramming

A build phase is governed by an artifact dependency graph rather than necessarily by a language front end. It can compile interface definitions, generate clients, render configuration, bundle assets, create version metadata, transform sources, or invoke another compiler. The output becomes an input to later graph nodes.

Build-time generation is appropriate when the source of truth is external to the subject language, multiple languages consume one schema, or the generator should be replaceable independently of a compiler. It owes declared inputs and outputs, hermeticity policy, deterministic normalization, provenance, bounded resources, and diagnostics that map to the source model.

Cargo build scripts illustrate explicit communication with a build orchestrator: the script runs before package compilation and can emit instructions that affect compilation. Other build systems use action sandboxes and declared dependency edges. The durable rule is that reading a file does not automatically make it a cache dependency. Every output-affecting read, environment value, tool executable, target option, locale, or randomness source must enter either the key or a controlled invariant.

Generated files may be checked in or ephemeral. Checked-in output permits direct code review and offline consumers but creates drift and merge noise. Ephemeral output keeps derivation clear but requires the toolchain at every build. In either policy, regeneration and drift checks establish that the declared source of truth actually controls the artifact.

### Load-time metaprogramming

Load time begins when a runtime resolves and brings a program unit into an execution context. Depending on the platform, the process may locate an artifact, validate it, create a module/class object, link references, run transformers, initialize state, and publish bindings. These events can be lazy, repeated under distinct loader identities, concurrent, or partially failed.

Python's import system demonstrates that import is not merely reading bytes: finders locate a module specification, loaders create and execute module state, `sys.modules` caches identities, and hooks can alter discovery. Java instrumentation permits trusted agents to transform class bytecode at load time and, under supported conditions, retransform already loaded classes. These examples expose load-time power and risk: transformation order, loader identity, initialization effects, reentrancy, cache state, and agent trust become semantic concerns.

Load-time work sees deployment-specific artifacts and some process configuration, which compile time may not know. It delays failure until startup or first use, complicates reproducibility, and runs with process authority. Keep hooks minimal, deterministic relative to declared deployment inputs where possible, observable, ordered, and safe under partial initialization.

### Run-time metaprogramming

Run-time mechanisms operate after the subject execution begins. Reflection, dynamic proxy creation, eval-like interpretation, tracing, adaptive specialization, method replacement, runtime code generation, and JIT compilation fall here when they inspect or change program behavior.

Late placement gains live types, values, workload profiles, configuration, and resources. It pays with latency, additional failure modes, concurrency coordination, dynamic attack surface, and harder predeployment coverage. Generated machine code still needs memory-permission discipline, code-cache bounds, architecture validation, unwind/debug metadata, and safe publication to executing threads. A reflective call still needs authorization and domain validation; metadata existence is not permission.

Run-time generation should expose fallback behavior. If specialization fails or a code cache is exhausted, can the system use an interpreter or generic implementation? If a dynamic proxy cannot bind a method, does startup fail, the first request fail, or a feature degrade? The choice is application policy, not a property implied by “runtime.”

### Cross-stage persistence and residualization

An earlier phase can pass information forward by emitting source, serializing data, embedding constants, creating object metadata, linking a resource, or generating code. This is cross-stage persistence. The carrier must specify representation, version, integrity, confidentiality, and ownership. Embedding an environment value into an executable is not free caching; it changes when that value can be updated and may leak secrets.

Partial evaluation divides inputs into early-known static values $s$ and later dynamic values $d$:

$$
specialize(P,s)=P_s,\qquad \llbracket P_s\rrbracket(d)\approx\llbracket P\rrbracket(s,d).
$$

The residual program $P_s$ should preserve the claimed observations for admissible $d$. Specialization can reduce runtime work but multiply variants, code size, compile cost, and invalidation obligations.

### Phase environment, authority, and trust

For each phase, inventory read/write paths, network, secrets, subprocesses, environment, clock, randomness, target, toolchain, and resource limits. Compiler plugins and build scripts are executable dependencies, not inert libraries. Load agents and runtime plugins often share application authority. Least privilege, dependency review, isolation, signed provenance, and output validation apply at every phase.

Never embed credentials merely because an earlier phase can read them. Separate values needed to construct the artifact from values needed only to deploy or operate it. Treat untrusted schemas, templates, plugins, and generated syntax as data until validated; compiling generated code is an authority transition.

### Caching and invalidation

Let output $O=F(I,E,T)$, where $I$ is declared content, $E$ permitted environment, and $T$ toolchain/target. A sound cache key $K$ must distinguish any changes in those domains that can change $O$, or the system must prove them irrelevant/normalized. Completeness matters more than hashing algorithm choice.

Over-invalidation wastes time; under-invalidation serves stale artifacts. Dynamic dependency discovery can be sound if the first execution records reads and the build system validates them before reuse. Nondeterministic timestamps in generated headers defeat byte-for-byte reuse unless normalized or explicitly modeled.

### Diagnostics and evidence

Earlier is useful only when the message reaches the author. Preserve source spans through expansion, schema locations through generated code, phase traces through nested invocations, and tool versions in reports. Distinguish:

- meta-execution failure: generator/macro/agent crashes or times out;
- representation failure: output is malformed;
- consumer failure: emitted artifact fails later compilation/loading;
- semantic failure: both phases succeed but behavior violates contract;
- environmental failure: undeclared or unavailable capability changes the result.

Verify each boundary. Test the metaprogram over valid and malformed representations; validate generated structure; compile/load the residual output; run behavioral tests; compare clean rebuilds; exercise invalidation; enforce size/time limits; and review privileges. No single phase-local success establishes end-to-end correctness.

The following deterministic model executes four phase actions only when their dependencies and declared inputs are available. It produces a provenance trace. It does not invoke a real compiler, build system, loader, or runtime, so it cannot demonstrate their caching, security, or concurrency behavior.

<!-- bijux-verify: {"id":"phase-dependency-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"build: schema -> generated_source\ncompile: generated_source -> module_image\nload: module_image -> loaded_module\nrun: loaded_module,request -> response\navailable=generated_source,loaded_module,module_image,request,response,schema\n","stderr":""}} -->
```python
available = {"schema", "request"}
phases = (
    ("build", ("schema",), "generated_source"),
    ("compile", ("generated_source",), "module_image"),
    ("load", ("module_image",), "loaded_module"),
    ("run", ("loaded_module", "request"), "response"),
)

for phase, required, produced in phases:
    missing = set(required) - available
    if missing:
        raise RuntimeError(f"{phase}: missing {sorted(missing)}")
    available.add(produced)
    print(f"{phase}: {','.join(required)} -> {produced}")

print("available=" + ",".join(sorted(available)))
```

## Definitions and Notation

Let $P=\{b,c,l,r\}$ denote build, compile, load, and run phases for one named subject. The relation $p\prec q$ means an output of $p$ is required before action $q$; it is a dependency relation, not necessarily total chronological order.

For phase $p$:

- $R_p$: input program representation;
- $I_p$: declared content/configuration inputs;
- $E_p$: allowed environment and capabilities;
- $T_p$: toolchain and target identity;
- $O_p$: residual outputs;
- $D_p$: diagnostics;
- $\Pi_p$: provenance linking output to inputs and execution.

A cache is sound with respect to function $F_p$ when equal keys imply equivalent reusable outputs under the promised observation:

$$
K_p(x)=K_p(y)\Rightarrow F_p(x)\approx F_p(y).
$$

This is a specification obligation; observing several cache hits is not a proof.

## Mechanisms, Invariants, or Proof Structure

**Availability invariant.** If $q$ consumes value $v$ produced at $p$, then $p\prec q$, and an explicit carrier preserves $v$'s relevant meaning. A runtime request cannot be a compile-time input in the same build.

**Provenance invariant.** Every residual artifact maps to generator/macro/agent version, source inputs, target, configuration, and transformation trace sufficient for diagnosis and policy.

**Cache-completeness argument.** Suppose generator output reads schema $S$, template $M$, option $C$, and tool $T$. A key omitting $M$ permits two executions with the same key and different output after the template changes, contradicting sound reuse. Therefore $M$, or a proved-equivalent normalized identity, must enter the key.

**Residual-equivalence obligation.** When specialization claims preservation, evaluate the original under static $s$ and dynamic $d$, and the residual under $d$, under the same stated observation relation. Effects, errors, and termination cannot be silently excluded.

**Load publication invariant.** A transformed unit is validated and fully initialized according to platform rules before other threads can observe it as usable. Failure leaves a defined cache/registry state rather than a half-published identity.

**Authority invariant.** A phase receives no broader write, network, secret, or execution privilege than its declared task requires. Generated bytes do not inherit trust solely from having been produced earlier.

## Alternatives and Trade-Offs

**Compile time versus build time.** Compiler integration provides language-aware syntax, types, and diagnostics. An external build generator supports multiple languages and independent versioning. Compiler coupling and build-graph visibility decide more than “earlier is faster.”

**Build time versus checked-in generation.** Ephemeral outputs avoid drift; checked-in outputs enable review and distribution without generators. Both require provenance and regeneration checks.

**Load time versus build-time instrumentation.** Load-time transformation adapts to deployed classes/configuration and third-party artifacts. Ahead-of-time instrumentation is more reproducible and moves failure earlier but may not see final deployment composition.

**Run time versus earlier specialization.** Runtime specialization uses live profiles and hardware. Earlier specialization improves startup predictability and artifact inspection. Hybrid systems need code-cache, fallback, and version policies.

**Eager versus lazy loading.** Eager loading concentrates failures at startup and consumes resources early. Lazy loading reduces startup work but moves failure into first-use paths and adds concurrency/cache complexity.

**Powerful phase hooks versus declarative inputs.** General code handles unusual cases but expands authority and nondeterminism. Declarative schemas constrain expressiveness and enable validation, caching, and tooling.

## Failure Modes and Misconceptions

1. **Before deployment means compile time.** Build generation, packaging, linking, and deployment are distinct phases.
2. **Compile-time code is harmless.** It may have compiler credentials and filesystem access.
3. **Imports only bind names.** Many module systems execute initialization and permit hooks.
4. **Runtime metaprogramming is necessarily reflection.** JITs, proxies, evaluators, and code generators also qualify.
5. **Earlier always improves performance.** It can multiply variants and slow every build.
6. **A deterministic generator guarantees a reproducible build.** Toolchain, inputs, environment, ordering, and downstream actions also matter.
7. **A content hash of the main schema is a complete cache key.** Templates, imports, options, tools, and targets may also affect output.
8. **Generated code that compiles is correct.** Consumer behavior and domain conformance remain.
9. **Load order is globally fixed.** Lazy loading, distinct loaders, hooks, and concurrency can change it.
10. **Phase names imply security boundaries.** Isolation exists only when a platform and policy enforce it.

## Worked Examples

### Example 1

**Question:** Is a Rust procedural macro build-time or compile-time?

**Reasoning:** Relative to the macro crate, it was compiled and now executes. Relative to the subject crate whose token stream it consumes and produces, it runs during compilation. Cargo also orchestrates both as build graph nodes.

**Conclusion:** Qualify the subject; one action can occupy different relative phases.

### Example 2

**Question:** Classify a schema client generator invoked before the compiler.

**Reasoning:** It is a build-time metaprogram over a schema representation. Its generated source then becomes compile-time input. The generator must report schema locations, and CI must compile and test the output.

**Conclusion:** Build success and consumer compilation are separate evidence boundaries.

### Example 3

**Question:** Why can a compile-time macro not embed tomorrow's request header?

**Reasoning:** The request does not exist in the compile phase's available values. The macro can emit residual code that reads the header later, or a later rebuild can embed a previously observed value. Pretending otherwise violates phase availability.

**Conclusion:** Later values require residual computation or a new dependency edge.

### Example 4

**Question:** Find the missing cache dependency when a generator reads `schema.json` and `template.txt` but keys only the schema.

**Reasoning:** Change the template while preserving the schema. The key remains equal, yet output changes. This is a direct counterexample to sound reuse.

**Conclusion:** Every output-affecting input needs a key identity or controlled invariant.

### Example 5

**Question:** Is Python module import load-time metaprogramming?

**Reasoning:** Custom finders/loaders can create and execute module objects, synthesize code, and alter resolution while a program imports. Ordinary import execution is not automatically a metaprogram, but a hook that processes program representations is. Cache identity and partial initialization matter.

**Conclusion:** Timing alone does not classify the operation; program-processing behavior does.

### Example 6

**Question:** Compare bytecode instrumentation before packaging with Java class-load transformation.

**Reasoning:** Ahead-of-time instrumentation yields inspectable, cacheable artifacts and earlier failure. Load-time transformation sees deployed classes and loader context but runs with process authority and can interact with initialization and ordering.

**Conclusion:** Choose based on required deployment knowledge and assurance, not convenience alone.

### Example 7

**Question:** A JIT compiles a hot method after ten thousand calls. Which phase is it?

**Reasoning:** It is run time for the application and compilation time for that method representation. Profile data is available only then. Correct publication, deoptimization, code-cache limits, and fallback belong to its contract.

**Conclusion:** Nested phase labels describe JIT behavior without contradiction.

### Example 8

**Question:** Should a database password be embedded by a build generator?

**Reasoning:** The build worker's ability to read a secret does not make embedding necessary. The artifact broadens distribution and fixes rotation time to rebuild time. Prefer runtime secret delivery with least privilege unless an explicit threat model proves another design.

**Conclusion:** Cross-stage persistence changes confidentiality and lifecycle.

### Example 9

**Question:** A hospital loads a runtime plugin that alters medication-rule classes. Does signature verification make it safe?

**Reasoning:** Signature verification supports origin/integrity, not clinical correctness, compatible transformation order, initialization safety, authorization, rollback, or hazard control. No external academic, clinical, regulatory, or practitioner review is claimed. Named qualified humans must review requirements, plugin supply chain, transformation scope, tests, runtime isolation, audit/rollback, and applicable medical assurance before use.

**Conclusion:** Load-time authority demands an end-to-end safety and governance case.

### Example 10

**Question:** Move a regex construction from every request to build time or application startup?

**Reasoning:** If the pattern is invariant and known to the build, build-time validation can reject it early and embed a representation compatible with the runtime. If deployment configuration supplies it, startup compilation preserves configurability and keeps failure before traffic. Runtime per-request construction is appropriate only when requests truly define patterns and resource/security limits are enforced.

**Conclusion:** Place work at the earliest phase that actually has the required value and compatible semantics.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies binding, observation, and undefined-behavior foundations for staged claims.
- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) owns translation pipelines and JIT mechanisms.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) uses plugin and extension boundaries whose initialization and authority must be explicit.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) governs hermetic build graphs, caches, artifacts, provenance, and rollout.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains loading, process authority, memory permissions, and concurrency.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) treats compilers, generators, agents, and plugins as supply-chain and capability-bearing code.

## References

1. The Rust Project. [The Rust Reference: Procedural Macros](https://doc.rust-lang.org/stable/reference/procedural-macros.html). Consulted 2026-08-29.
2. The Rust Project. [The Cargo Book: Build Scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html). Consulted 2026-08-29.
3. Python Software Foundation. [Python 3.14.7 Language Reference: The Import System](https://docs.python.org/3/reference/import.html). Consulted 2026-08-29.
4. Oracle. [Java SE 26 API: `java.lang.instrument`](https://docs.oracle.com/en/java/javase/26/docs/api/java.instrument/java/lang/instrument/package-summary.html). Consulted 2026-08-29.
5. Taha, Walid, and Tim Sheard. “Multi-Stage Programming with Explicit Annotations.” *Proceedings of PEPM '97*, 1997, pp. 203–217. [DOI: 10.1145/258993.259019](https://doi.org/10.1145/258993.259019).
6. Flatt, Matthew. “Composable and Compilable Macros: You Want It When?” *ICFP 2002*, pp. 72–83. [DOI: 10.1145/581478.581486](https://doi.org/10.1145/581478.581486).
7. Jones, Neil D., Carsten K. Gomard, and Peter Sestoft. *Partial Evaluation and Automatic Program Generation*. Prentice Hall, 1993. [Author-hosted edition](https://www.itu.dk/~sestoft/pebook/).

## Exercises

### Exercise 1

For a protobuf-like schema compiler run before a Java compiler, identify subject, meta-operation, representation, build output, and the next consumer phase.

### Exercise 2

Draw the dependency order for a build that first compiles a generator, runs it over a schema, compiles generated source, then uses a JIT at application run time. Explain why one total phase label is inadequate.

### Exercise 3

A generator cache key includes the schema digest and generator version but omits imported schema files, target architecture, and a formatting template. Diagnose when each omission is unsound and propose the corrected key.

### Exercise 4

Compare build-time and load-time instrumentation for observability probes across reproducibility, deployment knowledge, startup failure, privileges, rollback, and diagnostics.

### Exercise 5

Design a review for a railway-control application that loads signed transformation plugins at startup and can dynamically attach an agent during incidents. Separate automatable phase checks from evidence requiring named human review.

## Answers to the Exercises

### Answer 1

The subject is the client/server source API that will be generated and consumed. The metaprogram is generation from a structured interface schema, not source-to-source preservation. Its input representation is the schema AST/model plus imports/options. It is a build-time action relative to the Java artifact and emits Java source, provenance, and diagnostics. The Java compiler is the next consumer; it must parse/type-check the output. Later integration tests must verify wire and domain conformance.

### Answer 2

The dependency order is: generator source $\prec$ generator compilation $\prec$ generator execution with schema $\prec$ generated source $\prec$ application compilation $\prec$ application load/start $\prec$ hot execution/profile collection $\prec$ JIT compilation $\prec$ native residual execution. Generator compilation is compile time for the generator and build time for the application; JIT is run time for the application and compile time for the method. Relative labels plus dependency edges preserve both truths.

### Answer 3

Imported schemas are unsound to omit whenever their definitions affect output. Target architecture is unsound to omit if layout, conditional generation, ABI, or emitted flags depend on it; if output is proved target-neutral, record that invariant instead. The template is unsound to omit whenever its bytes influence generated text. A corrected key contains digests of the complete transitive schema closure and template, generator executable/version and dependencies, all output-affecting options/environment, target identity when relevant, and output-format/schema versions. The build must also validate that dependency discovery itself is complete.

### Answer 4

Build-time instrumentation produces inspectable and cacheable artifacts, fails before deployment, and can use source maps, but does not see final loader topology or late third-party classes. Load-time instrumentation sees deployed bytecode and loader/module context and can cover dynamically discovered units, but it adds startup/first-use failure, transformation-order interactions, and process-level privilege. Build rollback replaces the artifact; load rollback must restore transformer configuration and may require restart/retransformation. A strong design uses build-time probes when deployment knowledge is unnecessary and reserves load hooks for a demonstrated need, with provenance and source mapping in both.

### Answer 5

Automation verifies plugin signature chain and allowlist, digest-pinned provenance, supported application/plugin versions, deterministic transformation fixtures, bytecode validity, declared target classes, transformation ordering, resource limits, clean failure, logs, rollback rehearsal, and that dynamic attachment is disabled except through an authenticated audited incident capability. It exercises cold/eager/lazy loading, concurrent initialization, duplicate loads, partial failure, and residual behavior.

Those checks do not establish railway safety, operational authorization, timing bounds, fail-safe behavior, independence of safeguards, or that incident attachment is appropriate. No external academic, railway, regulatory, or practitioner review is claimed. Named qualified humans must review the hazard analysis, requirements trace, transformation semantics, timing and integration evidence, supply-chain governance, operator procedure, access controls, rollback/recovery, and applicable railway assurance obligations. Approval must identify the reviewer and scope; a valid signature on a plugin is not a safety approval.
