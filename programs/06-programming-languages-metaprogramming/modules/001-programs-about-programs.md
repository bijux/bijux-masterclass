---
module_id: META-001
program: Programming Languages: Metaprogramming
level: 1
module_number: 1
title: Programs About Programs
status: complete
last_verified: 2026-08-29
---

# Programs About Programs

## One-Page Review

### Governing question

What changes when a program treats another program—or itself—as input, output, or manipulable state, and which representation, phase, semantic, provenance, and trust contracts make that activity dependable?

### Essential definitions

- A **subject/object program** is the program being inspected, generated, transformed, specialized, or controlled.
- A **metaprogram** is a program whose relevant input, output, or effect concerns a representation or behavior of programs.
- The **object language** is the language being represented or produced; the **metalanguage** is the language used to express the metaprogram. The roles are relative and may use the same host language.
- **reification** makes some program property—text, tokens, syntax, types, bytecode, metadata, functions—available as data.
- A **program representation** is a contract for code-as-data: raw text, token stream, concrete syntax tree (CST), abstract syntax tree (AST), typed intermediate representation (IR), bytecode, or runtime metadata.
- **reflection** lets a running program inspect and sometimes alter program structure/behavior; **introspection** is the observational subset.
- **generation** constructs a program representation from a model; **transformation** maps one program representation to another; **specialization** fixes known inputs to produce a residual program.
- A **stage/phase** is a time and environment in which metaprogram work occurs: authoring, preprocessing, compilation, build, link, load/import, run time, or offline tooling.
- **quotation** constructs a representation without performing its represented computation; **splicing/unquotation** inserts a computed representation into a surrounding one.
- **provenance** records which source/model/generator/version/configuration produced an artifact and how diagnostics map back.
- **hygiene** preserves lexical binding during syntactic transformation unless capture is intentional and explicit.

### Central model, mechanism, or theorem

Let (P\in Prog_L) be an object program and (\rho_L(P)\in Rep_L) a representation. A metaprogram is modeled as

$$
M:Rep_L\times E_M\rightarrow Rep_{L'}\times D,
$$

where (E_M) is its phase environment and (D) includes diagnostics/evidence/provenance. If (M) claims behavior preservation, it owes a relation

$$
\llbracket P\rrbracket_L \approx_C \llbracket decode(M(\rho_L(P)))\rrbracket_{L'}
$$

for an explicit observation context (C). A generator from a schema has no original program whose behavior must be preserved; instead it must satisfy a generation contract derived from the schema. Representation and stage determine what names/types/resources are meaningful and when failures appear.

### Critical invariants

- Identify subject, meta-operation, representation, metalanguage/object language and execution phase explicitly.
- Never confuse a string containing source-like text with structured syntax or validated executable code.
- Preserve lexical binding, evaluation order, effects, types and source locations wherever the transformation claims to preserve them.
- Generated names are fresh or intentionally bound; identifiers are not equivalent merely because their spelling matches.
- Meta-phase inputs, filesystem/network/environment access and nondeterminism are declared, minimized and reproducible where required.
- The metaprogram validates its input representation and emits diagnostics at the user's originating source/model location.
- Generated artifacts carry generator/input/config/toolchain provenance and one declared source of truth.
- Code size, compile/build time, memory, recursion and variant counts have budgets.
- Untrusted program representations are data, not authority to execute; generation/compilation/execution have separate trust boundaries.
- Prefer ordinary functions/modules/types before metaprogramming unless program representation or phase control addresses a real force.

### Common failures

Common failures include “code that writes code” as the whole definition; concatenating strings and calling them ASTs; token substitution across lexical boundaries; accidental name capture; executing while intending to quote; referring to run-time values at compile time; nondeterministic generation; hidden environment/network reads; stale checked-in generated code; generator/consumer version skew; duplicated source of truth; exponential expansion; unreadable errors at generated locations; running untrusted templates/plugins with build credentials; inspecting metadata and assuming domain validity; self-modifying behavior with no audit; and using metaprogramming to avoid designing an ordinary API.

### Compact example

Represent `((2 + 3) * x)` as `("mul", ("add", 2, 3), ("var", "x"))`. A constant folder operates on nodes—not text—and produces `("mul", 5, ("var", "x"))`. Interpreting both under `x=4` yields 20. This finite trace supports one preservation claim for one input; a general optimizer still needs inductive/operator laws, effects and overflow semantics.

### Connections

Retrieve [PLS-001's distinction among program text, meaning, execution and observation](../../01-programming-languages-and-semantics/modules/001-programs-languages-and-observable-behavior.md). The successor [META-002](../ROADMAP.md) separates compile-, build-, load- and run-time staging. Syntax pipelines connect to [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md), while this program owns user-facing transformation, generation, reflection, staging, derivation and DSL engineering.

## Governing Question

How can engineers reason uniformly about macros, reflection, decorators, templates, generators, AST rewrites, specialization and embedded languages without pretending that their representations or phases provide the same guarantees?

“A program about a program” is deliberately broader than “code that writes code.” A linter reads program structure and emits diagnostics. A macro transforms syntax. A schema generator creates code from a model. A decorator replaces or annotates a runtime callable. A partial evaluator consumes a program and known inputs to produce a residual program. A serializer derived from a type description turns types into compile-time data. These activities differ, but each crosses a meta boundary where program properties become data under another computation.

The first discipline is to name five things: subject, operation, representation, stage, and claimed relationship between input and result. Without them, engineers argue past one another: a runtime decorator is “compile time” in one ecosystem's deployment story; a token macro is called “structured”; a generator is assumed semantics-preserving even though it creates a new interface from a schema.

## Why This Matters

Metaprogramming multiplies leverage. One definition can produce hundreds of types, validate an architecture rule across thousands of files, specialize a numerical kernel, or add syntax impossible to express as an ordinary function. The same leverage multiplies defects and attack surface. One generator bug propagates everywhere. One phase-dependent environment read breaks reproducibility. One captured identifier silently changes user meaning. One expansion can hide the source of a diagnostic.

Ordinary code has a primary execution story: values enter and effects/results emerge. Metaprogrammed systems have at least two: the metaprogram executes, and its inspected/generated/transformed subject is later analyzed or executed. Failures can arise in either story and at their boundary. Production engineering must preserve provenance, diagnostics, version compatibility, tool integration, security and resource budgets across both.

This course therefore treats metaprogramming as program-processing engineering, not syntactic cleverness. Later modules deepen textual versus structural transformation, reflection, generation, templates, staging, typed metaprogramming and DSLs. This foundation establishes the questions that remain valid across languages and tools.

## Prerequisites and Retrieval

Learners should retrieve:

- source text, parsing, syntax trees, static checking, compilation and execution;
- lexical scope, binding, free/bound variables and evaluation order;
- functions, modules, parametric abstraction and data representations;
- interpreters as functions over syntax and environments;
- compiler/build/import/run-time phases at an introductory level;
- deterministic builds, dependency/version contracts and source control;
- code injection, least privilege and supply-chain trust;
- equivalence as equality of selected observations rather than identical source.

Before continuing, take a decorator, macro, code generator or linter you know and identify its subject program, representation, stage, inputs, outputs/effects and strongest justified claim. “It automates boilerplate” is not yet a technical model.

## Learning Objectives

After this module, learners can:

1. define metaprogramming broadly and distinguish its principal operations;
2. identify relative object-language and metalanguage roles, including same-language cases;
3. compare text, tokens, CST, AST, typed IR, bytecode and runtime metadata;
4. distinguish inspection, generation, transformation, specialization and execution;
5. locate metaprogram work and failures across phases;
6. formulate behavioral preservation or generation-conformance claims with assumptions;
7. explain binding, hygiene, provenance, diagnostics and reproducibility obligations;
8. identify resource and security amplification at the meta boundary;
9. choose ordinary abstraction when reified program structure/staging is unnecessary;
10. design focused positive, negative and differential evidence for a metaprogram.

## Core Exposition

### Define the subject and the meta-operation

The object/meta distinction is relational. A Python program can use Python's `ast` representation to transform Python; the same implementation language occupies both roles but executes at a different meta-level. A Rust procedural macro is compiled Rust code that receives/emits token streams representing Rust items. A Haskell program using Template Haskell constructs Haskell declarations/expressions. A Java annotation processor runs during compilation and produces files/diagnostics from annotated program elements.

Classify the relevant operation:

- **inspection/analysis:** observe properties and produce facts, warnings or indexes;
- **generation:** produce a program from schema/model/specification;
- **transformation:** rewrite an existing program representation;
- **specialization:** produce a residual program using known inputs;
- **extension/intercession:** alter lookup, calls, classes or behavior at load/run time;
- **execution/interpretation:** treat a representation as instructions.

One system can combine them. A macro inspects syntax, generates syntax, then compiler analyzes it. A decorator inspects a function and returns a wrapper. “Metaprogramming” does not itself say whether output is source, callable value, diagnostic or new behavior.

### Representation determines available reasoning

**Raw text** preserves all bytes/comments/layout but has no guaranteed token/scope structure. Concatenation is easy and injection/escaping/binding mistakes common.

**Tokens** distinguish identifiers/literals/punctuation and can preserve spans. They still may not expose complete grammar, types or resolved bindings.

**CST** preserves grammatical and often formatting/comment detail, useful for source-to-source refactoring.

**AST** discards some concrete syntax to expose language constructs. Its schema is language/version-specific. An AST node spelling `x` is not a resolved binding.

**Typed/resolved IR** contains type/binding/control-flow facts and supports stronger transformations, but is coupled to compiler internals and may omit source details.

**Bytecode/machine IR** exposes execution operations after high-level meaning was lowered. Instrumentation is possible but source/domain recovery is harder.

**Runtime metadata/objects** expose loaded types/members/callables/annotations under current execution environment. They may omit source-only constructs and make observation/effect timing part of semantics.

Choose the least representation with enough structure. “Strong” is not always best: format-preserving rename wants CST; optimizer wants typed IR; configuration generator wants schema model. Crossing representations requires parsers/printers/resolvers and provenance mappings.

### Separate representation from execution

Quotation should create data representing an expression without running it. Evaluation/interpreting/compiling can later give that data behavior. Treating source text as data is safe only until a powerful consumer executes it. Validation of syntax is not proof of authorization, termination, resource use or semantic safety.

This separation explains injection. Concatenating an untrusted string into source/SQL/shell confuses data with code in the consumer's grammar. Structured constructors/parameter binding preserve the boundary only when every escape/identifier/capability is correctly modeled. Never call arbitrary evaluation a convenient parser.

Self-reference needs levels. A compiler is a program about programs; a compiler compiling its own source is bootstrapping, not a logical paradox. A macro-generating macro adds a meta-level. Label levels/stages so code produced now and code executed later do not blur.

### Make phase and environment explicit

Metaprograms run at preprocessing, expansion, type-check, build, link, load/import or runtime. Phase decides available bindings and side effects. A compile-time macro cannot generally use a runtime value; a runtime reflector cannot affect checks already completed except through language-specific dynamic behavior.

For each meta-phase record:

- inputs and their versions/digests;
- environment variables, filesystem, locale/timezone, clock/randomness and network access;
- toolchain/compiler/runtime version and target;
- generated artifacts/caches and invalidation keys;
- privileges/secrets and sandbox;
- time/memory/output-size/recursion limits;
- diagnostic/source mapping.

Reproducible static generation requires output determined by declared inputs/toolchain or nondeterminism normalized and recorded. Runtime metaprogramming can intentionally depend on live state, but observability, races, cache invalidation and authorization enter its contract.

### State semantic obligations honestly

Not every metaprogram preserves behavior. A linter reports facts. A generator creates a new implementation from a schema. A migration transformer intentionally changes API/behavior. An optimizer normally claims observational preservation under a language arithmetic/effect model.

For a transformation, state:

- accepted source representation and well-formedness;
- produced representation/language/version;
- preserved observations (result, exceptions, effects, termination, timing?);
- allowed differences;
- assumptions about overflow, aliasing, purity, evaluation order and undefined behavior;
- rejected constructs and diagnostics;
- proof/test/evidence boundary.

Textual equality is usually unnecessary; same output for three examples is insufficient. Local rewrites need laws. Constant folding `2+3` is valid only if addition semantics, overflow/errors and evaluation effects permit. Removing `0*x` is invalid when evaluating `x` has effects or can fail.

For generators, use conformance: generated client request matches schema; generated serializer round-trips supported values; old/new tool versions satisfy a compatibility matrix. One schema should be authoritative; generated output is derivative unless repository governance explicitly makes checked-in output the reviewed distribution artifact.

### Preserve binding and hygiene

Code transformations manipulate identifiers with lexical context, not strings alone. A macro introducing temporary name `result` can capture the caller's `result` or be captured by a local binder. Hygienic systems track scopes/marks/context so introduced and use-site names resolve as intended. Hygiene does not solve semantic collision in external registries, generated filenames, database names or public APIs.

Intentional capture exists—anaphoric macros, declarations introduced for caller use—but must be explicit, documented and tested. Fresh-name generation needs deterministic provenance when output is inspected. Renaming requires binding resolution, not global text replacement. Diagnostics should point to macro invocation or relevant generated fragment and preserve expansion trace for experts.

### Treat generated artifacts as supply-chain outputs

A generator is a build dependency capable of emitting trusted code. Pin/review its version and transitive dependencies, restrict permissions/network, validate source model, escape structured outputs, record provenance and scan/test generated artifacts. If user-provided templates/plugins execute, assume code execution unless a real sandbox/capability model proves otherwise.

Decide whether generated files are checked in. Checking in aids review/distribution and creates drift/merge noise; excluding them demands reproducible tool availability for every consumer. In either policy, CI regenerates and detects drift. Include stable headers/manifest with generator version/input digest/schema version—without timestamps that destroy reproducibility unless required and normalized.

### Budget leverage and comprehension

Meta-level computation can explode compile time, code size, binary variants, cache keys, errors and IDE workload. Measure expansion node/token count, generated bytes/files, specialization variants, compile/load time, peak memory, diagnostic depth and incremental invalidation. Bound recursion/inputs and fail with actionable location.

The abstraction budget includes what users must learn: phase rules, expansion tooling, generated APIs and debugging layers. Prefer an ordinary function when runtime values suffice; generics when parametric abstraction suffices; data/config when variation is declarative; a library API when syntax is not essential. Metaprogramming is justified when representation access/staging produces a material safety, consistency, performance or usability advantage.

### Verify at both levels

Evidence portfolio:

- metaprogram unit/property tests over representations;
- golden/structural expansion tests where representation shape matters;
- compile-pass/compile-fail and diagnostic span tests;
- differential execution of original/transformed program under generated inputs;
- semantic invariants/proofs for rewrite rules;
- consumer contract/compatibility tests for generated APIs;
- reproducibility check from clean environments;
- resource/adversarial/fuzz tests on malformed/deep/large inputs;
- security review/sandbox tests;
- IDE/source-map/debugging review.

Test the negative relationship. Introduce a captured name and ensure hygiene prevents it; mutate schema and ensure drift fails; exceed recursion/output budget and ensure bounded failure; feed untrusted expression and prove it is rejected as data rather than executed.

### A small structured transformation

The following model represents arithmetic as tagged tuples, interprets it, and folds only a pure constant addition. It avoids source-string evaluation.

<!-- bijux-verify: {"id":"meta-001-structured-transformation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"original=('mul', ('add', 2, 3), ('var', 'x'))\nfolded=('mul', 5, ('var', 'x'))\noriginal@x=4=20\nfolded@x=4=20\npreserved=yes\n","stderr":""}} -->
```python
def interpret(expression, environment):
    if isinstance(expression, int):
        return expression
    tag = expression[0]
    if tag == "var":
        return environment[expression[1]]
    left = interpret(expression[1], environment)
    right = interpret(expression[2], environment)
    return left + right if tag == "add" else left * right

def fold_constants(expression):
    if isinstance(expression, int) or expression[0] == "var":
        return expression
    tag = expression[0]
    left = fold_constants(expression[1])
    right = fold_constants(expression[2])
    if tag == "add" and isinstance(left, int) and isinstance(right, int):
        return left + right
    return (tag, left, right)

original = ("mul", ("add", 2, 3), ("var", "x"))
folded = fold_constants(original)
environment = {"x": 4}
before = interpret(original, environment)
after = interpret(folded, environment)
print("original=" + str(original))
print("folded=" + str(folded))
print("original@x=4=" + str(before))
print("folded@x=4=" + str(after))
print("preserved=" + ("yes" if before == after else "no"))
```

This run proves one pure integer trace in the toy language. It does not parse source, resolve names, handle effects/errors/overflow, prove the rewrite inductively, generate executable code, preserve locations, enforce staging, sandbox inputs or characterize a production toolchain.

## Definitions and Notation

Let (Prog_L) be well-formed programs in language (L), (Rep_L) representations, (
ho_L:Prog_L\rightarrow Rep_L) reification, and (decode_L:Rep_L\rightharpoonup Prog_L) partial reconstruction. Let (M) run at meta-stage (s_M) with declared environment (E_M).

An **analyzer** (A:Rep_L\rightarrow Facts\times Diagnostics) need not produce a program. A **generator** (G:Model\rightarrow Rep_L\times D) satisfies model-to-program contract (K_G). A **transformer** (T:Rep_L\rightarrow Rep_{L'}\times D) may claim observation relation (\approx_C). A **specializer** $S:Rep_L\times StaticInput\rightarrow Rep_L$ should satisfy (\llbracket S(P,a)\rrbracket(b)\approx\llbracket P\rrbracket(a,b)) within its semantic domain.

Meta-level 0 is ordinary object computation by convention; level (n+1) manipulates a representation/behavior at level (n). Levels and chronological phases are not identical: a runtime reflector is meta-level activity at runtime. **Stage correctness** means referenced values/code are available and used at their declared phase.

**Observational preservation** is relative to context (C); it may cover results/effects/exceptions/termination and deliberately exclude source layout/performance. **Reproducible generation** means equivalent declared inputs and toolchain/config yield byte- or semantically equivalent declared outputs, with the chosen equality specified.

## Mechanisms, Invariants, or Proof Structure

1. **Name roles.** Subject program/model, meta-operation, object/metalanguage, representation and output/effect.
2. **Locate stage.** Expansion/build/import/runtime environment, bindings, privileges, inputs and failure reporting.
3. **Choose representation.** Least structure sufficient for required rewrite/analysis and source fidelity.
4. **Define semantics.** Preservation, intentional change, analysis soundness/completeness scope or generator conformance.
5. **Protect binding/types/effects.** Hygiene/resolution, evaluation order, errors, types and source locations.
6. **Control authority.** Treat input/templates/plugins as untrusted; sandbox/restrict execution and pin toolchain/dependencies.
7. **Record provenance.** Source/model, generator/transformation versions, configuration, hashes and diagnostic mapping.
8. **Bound resources.** Time, memory, recursion, output/variant/code size and incremental invalidation.
9. **Verify both levels.** Meta-unit/structural tests plus generated/transformed consumer behavior, negative and compatibility evidence.
10. **Justify/remove.** Compare ordinary abstraction, document ownership/limits and migrate away if opacity/cost exceeds benefit.

For the toy fold rule, if both children of a pure `add` are integer literals and language addition is total with the same arithmetic, replacing the node with their sum preserves interpretation in every environment. A structural induction can compose that local rule with unchanged constructors. The executable example is not that proof; its language silently assumes unbounded integers and total lookup for present variables.

## Alternatives and Trade-Offs

**Ordinary functions/modules** preserve familiar tooling, runtime abstraction and explicit control flow. Prefer unless syntax/type/program representation must be manipulated.

**Parametric polymorphism/generics** express uniform reusable behavior without arbitrary code generation in many languages; some implementations perform compile-time specialization, but user-facing semantics need not be metaprogramming.

**Data/configuration** keeps variability inspectable and can be interpreted by one engine; overly powerful configuration becomes an accidental language.

**External generator** is language-neutral and reproducible at build time but creates artifact/provenance/version integration.

**Macro/syntax extension** improves domain notation and compile-time checks, but adds phase, binding, diagnostics and tooling complexity.

**Reflection/decorator/proxy** adapts loaded runtime values flexibly, with runtime errors, performance/caching and authorization concerns.

**Annotation/type derivation** centralizes schema-like metadata and boilerplate; annotations can become hidden control flow or conflict.

**Compiler plugin/IR pass** has strong semantic information and optimization leverage, while coupling tightly to compiler internals/trust.

**Embedded/external DSL** can constrain/optimize a domain, but creates language design, evolution, diagnostics and tooling obligations.

Compare transparency, error phase, expressiveness, type/binding safety, performance, reproducibility, portability, IDE support, security, versioning and exit cost—not syntax brevity alone.

## Failure Modes and Misconceptions

- **“Metaprogramming is code that writes code.”** It also inspects, transforms, specializes and intercedes over program representations/behavior.
- **“Same host language means no meta boundary.”** Roles/stages can differ inside one language/process.
- **“Text is code.”** It is bytes until parsed/interpreted; concatenation lacks grammar/binding guarantees.
- **“AST means semantics.”** Unresolved/untyped syntax lacks binding, types, effects and many language rules.
- **“Parsing makes input safe.”** Valid syntax can still execute unauthorized/nonterminating/resource-exhausting behavior.
- **“Compile-time means pure.”** Build macros/generators may read files, environment, network, clock and secrets.
- **“Reflection is just lookup.”** It can bypass static visibility, trigger initialization and expose mutable behavior depending on platform.
- **“Generation removes maintenance.”** It transfers maintenance to schema, generator, compatibility, provenance and output review.
- **“Same output on examples proves preservation.”** Evidence is finite and assumptions/operators/effects matter.
- **“Hygiene solves every collision.”** External/public names and intentional capture still need policy.
- **“Generated files should always/never be committed.”** Distribution/review/reproducibility forces decide; drift checking is required either way.
- **“Macros are zero-cost.”** Runtime work may shrink while compile/IDE/code-size/cognitive cost grows.
- **“More abstraction is always good.”** Expansion can obscure behavior and error ownership.
- **“Self-hosting proves correctness.”** A compiler compiling itself is valuable evidence, not a proof of semantic correctness or trust.
- **“One meta-framework should own everything.”** Distinct representation/phase/domain forces may require smaller mechanisms.

## Worked Examples

### Example 1

**Situation.** An API schema generator emits client types and request encoders.

**Reasoning.** Subject input is schema model, not an existing program. Generator runs at build/release time and emits source/metadata. Its claim is schema conformance and compatibility, not preservation. Pin schema/generator, record digests, compile generated code, run protocol fixtures and detect drift.

**Conclusion.** Generation is metaprogramming with a model-to-program contract rather than an input-program equivalence claim.

### Example 2

**Situation.** A linter reads ASTs and reports unchecked error values but produces no executable program.

**Reasoning.** It is a program about programs and part of the broad program-processing/metaprogramming domain. Its evidence concerns rule soundness/false positives, resolution accuracy and source spans. It should not be described as code generation.

**Conclusion.** Inspection/analysis is a distinct meta-operation with diagnostic, not behavioral-output, obligations.

### Example 3

**Situation.** A macro expands `with_temp(e)` using local identifier `temp`; caller already binds `temp`.

**Reasoning.** Text substitution can capture caller name or have introduced name captured. A hygienic syntax object/fresh resolved binding keeps identities distinct; intentional exposure would need explicit interface.

**Conclusion.** Identifier spelling is insufficient—lexical context is part of program representation.

### Example 4

**Situation.** A compile-time generator attempts to read a value computed from live customer request.

**Reasoning.** The value does not exist at build phase. Move computation to runtime, generate code accepting it as parameter, or stage only static structure. Hiding it behind environment lookup changes meaning and reproducibility rather than solving phase availability.

**Conclusion.** Stage correctness constrains which bindings can cross a meta boundary.

### Example 5

**Situation.** A Python decorator registers a function when its module imports and returns a wrapper.

**Reasoning.** Subject is runtime function object/metadata; operation inspects, registers and replaces callable at import execution. Order, repeated import/reload, wrapper identity/signature, exceptions, concurrency and registry authority matter. It is dynamic metaprogramming, not a textual compile-time macro.

**Conclusion.** Similar surface syntax can conceal different representation and phase semantics.

### Example 6

**Situation.** An optimizer changes `(2+3)*x` to `5*x`.

**Reasoning.** In the pure toy language, local addition law and structural interpretation support preservation. In a real language, integer overflow, operator overloading, exceptions and evaluation effects can invalidate it. Verify only within the declared IR semantic domain.

**Conclusion.** Transformation correctness follows from operator/representation assumptions, not visual algebra alone.

### Example 7

**Situation.** A generic parser is specialized for a fixed grammar.

**Reasoning.** Grammar is static input; byte stream remains dynamic. Residual parser should match generic parser's accept/reject/tree results for supported inputs while improving a measured cost. Generated size/compile time and grammar-version provenance are part of evidence.

**Conclusion.** Specialization trades meta-time/code-size for residual runtime performance under an equivalence contract.

### Example 8

**Situation.** Checked-in generated models differ from a clean regeneration.

**Reasoning.** Possible causes include changed schema/generator/config, nondeterminism, manual edits or undeclared environment. CI should regenerate with pinned inputs, compare, and fail with provenance; decide authoritative source rather than merging both as truth.

**Conclusion.** Drift is a source-of-truth/reproducibility failure, not cosmetic diff noise.

### Example 9

**Situation.** A compiler is compiled by an older version of itself, then recompiles its source.

**Reasoning.** Stage 0 trusted compiler builds stage 1; stage 1 builds stage 2. Comparing outputs/tests can detect instability under reproducibility assumptions. It does not eliminate the trusting-trust threat or prove language correctness; provenance and diverse verification may strengthen trust.

**Conclusion.** Bootstrapping is layered metaprogram execution with an explicit trust base, not circular magic.

### Example 10

**Situation.** A hospital policy DSL generates medication authorization code from clinician-authored rules.

**Reasoning.** Define typed rule semantics, units, priority/conflict, version/effective time, provenance, deterministic generation, source mapping and fail-closed behavior. Test model/interpreter/generated equivalence and adversarial malformed/conflicting rules. Named human pharmacists, clinical-safety, privacy/security, accessibility and regulatory reviewers approve meaning and rollout; compilation cannot decide clinical adequacy.

**Conclusion.** High-leverage metaprogramming needs technical evidence plus qualified human governance at the domain boundary.

## Cross-Program Connections

- **Programming Languages and Semantics:** denotation/observation, binding, types and equivalence define transformation claims.
- **Compilers:** lexing/parsing/IR/lowering supply representations; this program focuses on exposed meta abstractions and production use.
- **Theory of Programming:** induction, logical relations and specifications support preservation arguments.
- **Functional Programming:** algebraic syntax, folds, interpreters, purity and staged composition make transformations explicit.
- **Object-Oriented Programming:** reflection, annotations, proxies and decorators manipulate runtime/class structure.
- **Systems Programming:** build/link/load/runtime phases, ABIs and reproducibility constrain generated artifacts.
- **Security Engineering:** injection, untrusted plugins/templates, build credentials and supply-chain provenance define trust boundaries.
- **Software Delivery/Quality:** clean regeneration, compatibility fixtures, negative diagnostics and artifact evidence make generation maintainable.

## References

- Harold Abelson and Gerald Jay Sussman with Julie Sussman, [Structure and Interpretation of Computer Programs, Chapter 4: Metalinguistic Abstraction](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book-Z-H-25.html), second edition, MIT Press, 1996, retrieved 2026-08-29. Foundational treatment of evaluators and languages as program data.
- Eugene E. Kohlbecker et al., [Hygienic Macro Expansion](https://dl.acm.org/doi/10.1145/319838.319859), ACM LFP 1986. Foundational binding-preserving macro expansion.
- Tim Sheard and Simon Peyton Jones, [Template Meta-Programming for Haskell](https://doi.org/10.1145/581478.581485), ACM Haskell Workshop 2002. Typed quotation/splicing and compile-time generation foundations.
- Walid Taha and Tim Sheard, [Multi-Stage Programming with Explicit Annotations](https://doi.org/10.1145/258993.259019), ACM PEPM 1997. Formal foundation for quotation, splicing and stage discipline.
- Krzysztof Czarnecki and Ulrich Eisenecker, *Generative Programming*, Addison-Wesley, 2000. Broad generative programming, domain engineering and configuration foundations.
- Racket Project, [Macros](https://docs.racket-lang.org/guide/macros.html), Racket Guide, retrieved 2026-08-29. Current official documentation for syntax objects, pattern macros and lexical scope behavior.
- Rust Project, [Procedural Macros](https://doc.rust-lang.org/reference/procedural-macros.html), Rust Reference, retrieved 2026-08-29. Current official token-stream, hygiene/span and procedural-macro contract.
- Python Software Foundation, [`ast` — Abstract Syntax Trees](https://docs.python.org/3/library/ast.html), Python 3.14.7 documentation, retrieved 2026-08-29. Current official AST schema/manipulation/compilation interface with version-qualified nodes.
- Guy L. Steele Jr., *Common Lisp the Language*, second edition, Digital Press, 1990. Durable quotation, macro and evaluation foundations.
- Ken Thompson, [Reflections on Trusting Trust](https://dl.acm.org/doi/10.1145/358198.358210), *Communications of the ACM* 1984. Foundational trust/bootstrapping warning for program-producing programs.

## Exercises

### Exercise 1

For a linter, schema generator, syntax macro, decorator and partial evaluator, name subject, meta-operation, representation, stage, output/effect and strongest justified contract.

### Exercise 2

Trace the toy constant folder on `("add", ("mul", 2, 4), ("add", 1, 2))`. Explain why its current rule does not fully fold the expression and state one safe extension under toy semantics.

### Exercise 3

Diagnose a build generator that reads the network and clock, concatenates user strings into source, emits 50,000 files without spans, and checks outputs into source control without drift tests.

### Exercise 4

Compare an ordinary function, configuration interpreter, macro, external generator and runtime reflection for defining validated HTTP routes. Select two plausible contexts with different answers.

### Exercise 5

Design the evidence and governance boundary for an unfamiliar financial rule generator that produces executable fee calculations from analyst-authored policies. Include semantics, phases, provenance, security, compatibility, resources, diagnostics and human review.

## Answers to the Exercises

### Answer 1

Linter: subject source program; inspection/analysis over AST/resolved IR at offline/compile phase; diagnostics/facts; contract is scoped rule accuracy and correct locations, not generated behavior. Schema generator: subject schema/model; generation into source/types at build/release; artifacts/manifest; contract is schema/interface conformance and version compatibility. Syntax macro: subject invocation syntax; transformation from token/syntax object to object-language syntax during expansion; output expanded syntax/diagnostics; contract includes well-formed expansion, binding/hygiene and specified semantics. Decorator: subject loaded function/class object; runtime/import-time inspection/intercession; returns wrapper/registration/metadata effects; contract is preserved/declared callable behavior and registry/lifecycle semantics. Partial evaluator: subject program plus static input; AST/IR transformation at build/compile/JIT; residual program; contract relates residual execution on dynamic input to original execution on static+dynamic inputs under a stated semantic domain.

### Answer 2

The folder visits the outer `add`. Left `("mul",2,4)` remains a `mul` because the implemented rule folds only `add`, although its children are constants. Right `("add",1,2)` becomes `3`. The outer node is then `("add", ("mul",2,4), 3)`; its children are not both integers, so it remains. A safe toy extension folds `mul` when both children are integer literals, yielding left `8`, then outer `11`. Preservation relies on the toy interpreter's total unbounded integer multiplication/addition and absence of effects/errors. A real language requires its overflow/operator/evaluation rules.

### Answer 3

Network/clock are undeclared nondeterministic meta-phase inputs; builds vary/offline fail and fetched content may be compromised. User-string concatenation confuses data/code and permits syntax/injection/binding errors. Fifty thousand files threaten time, storage, watchers/IDE and review; no spans destroys diagnostic provenance. Checked-in outputs without drift leave schema/generator/manual edits as competing authority. Stop untrusted generation, preserve evidence, pin/cache verified inputs or forbid network, inject deterministic clock only if semantically needed, use structured constructors/escaping, set file/node/time limits and aggregate outputs. Emit source maps/provenance with generator/input/config digests, select one authoritative model, regenerate cleanly in CI and fail drift. Sandbox generator with least privilege, scan/compile/test outputs and define tool/version compatibility.

### Answer 4

Small service with a dozen static routes: ordinary function calls plus typed route-builder library/config values give explicit control flow, normal IDE/debugging and runtime validation; macros/generation are unnecessary. Large organization with an authoritative API schema across languages: external schema generator can emit server stubs/client types/docs, with pinned reproducible generation and compatibility fixtures; runtime framework still validates auth/handlers. A language-embedded macro is plausible when route syntax must be checked at compile time and ordinary types cannot express path-parameter binding ergonomically, provided hygiene/diagnostics/tooling justify it. Runtime reflection fits plugin-discovered annotated handlers where deployment-time extensibility matters, accepting startup errors/cost and strict registration/authorization. Configuration interpreter fits operator-edited routing policy, but it must not become arbitrary code execution. Context forces choose, not a universal mechanism.

### Answer 5

Define a versioned policy language with decimal currency/rounding, effective/transaction time, rule priority/conflict, jurisdictions, bounds and explicit unknown/error behavior. Parse into typed resolved IR; validate units, totality or bounded evaluation, overlapping rules and forbidden effects. Generator runs in isolated release phase from signed policy/version/config and pinned toolchain, with no ambient network/clock/secrets. Emit deterministic calculation module plus source map, manifest/digests and human-readable rule trace. Preserve original policy and generated artifact lineage.

Establish interpreter as an independently tested reference where practical; use policy fixtures, property/boundary tests, model/generated differential results, old-policy/new-engine and new-policy/old-engine compatibility matrix, compile-fail diagnostics, reproducible clean generation, fuzzed malformed/deep input, output/time/memory limits and sandbox/supply-chain review. Deployment uses shadow calculations with no charging effect, then bounded cohorts, exact ledger reconciliation, rollback/forward-correction and audit. Named human finance-domain, accounting, legal/compliance, risk, privacy/security and accessibility reviewers approve economic meaning, effective dates, discrepancies and customer remedy. Automation can prove representation/evaluation properties within its model, not fairness, regulatory adequacy or acceptable financial harm.
