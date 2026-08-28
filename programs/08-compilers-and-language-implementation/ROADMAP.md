# 08. Compilers & Language Implementation

**Program code:** `COMP`

**Purpose:** Develop end-to-end command of interpreters, compilers, intermediate representations, analyses, optimization, code generation, runtimes, and production toolchains.

**Level-II professional outcome:** Ready to implement and maintain language front ends, transpilers, static analyzers, bytecode engines, optimizing compilers, DSL toolchains, and runtime components.

**Prerequisites:** Programming Languages & Semantics Levels I-II; data structures and algorithms; systems programming basics; computer architecture basics.

**Primary ownership:** lexing and parsing; name and type analysis; interpreters; IR design; dataflow analysis; optimization; code generation; runtimes and GC; JIT compilation; compiler tooling and correctness.

**Explicit exclusions:** general language semantics (Program 01); metaprogramming APIs (Program 06); computer-architecture design (Program 23).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Language Toolchain and Lexical Analysis

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Language Implementation Pipelines** | `001-language-implementation-pipelines.md` |
| 002 | **Source Text, Encodings, and Position Tracking** | `002-source-text-encodings-and-position-tracking.md` |
| 003 | **Tokens and Lexical Specifications** | `003-tokens-and-lexical-specifications.md` |
| 004 | **Regular Expressions and Finite Automata** | `004-regular-expressions-and-finite-automata.md` |
| 005 | **Hand-Written Lexers** | `005-hand-written-lexers.md` |
| 006 | **Generated Lexers** | `006-generated-lexers.md` |
| 007 | **Whitespace, Comments, and Layout Rules** | `007-whitespace-comments-and-layout-rules.md` |
| 008 | **Lexical Errors and Recovery** | `008-lexical-errors-and-recovery.md` |
| 009 | **Incremental Lexing** | `009-incremental-lexing.md` |
| 010 | **Testing and Benchmarking a Lexer** | `010-testing-and-benchmarking-a-lexer.md` |

### Block 02 — Parsing and Syntax Representation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Context-Free Grammars for Parsing** | `011-context-free-grammars-for-parsing.md` |
| 012 | **Ambiguity, Precedence, and Associativity** | `012-ambiguity-precedence-and-associativity.md` |
| 013 | **Recursive-Descent Parsing** | `013-recursive-descent-parsing.md` |
| 014 | **Pratt Parsing for Expressions** | `014-pratt-parsing-for-expressions.md` |
| 015 | **LL Parsing and Predictive Tables** | `015-ll-parsing-and-predictive-tables.md` |
| 016 | **LR Parsing and Shift-Reduce Decisions** | `016-lr-parsing-and-shift-reduce-decisions.md` |
| 017 | **Parser Generators** | `017-parser-generators.md` |
| 018 | **Concrete Syntax Trees and Abstract Syntax Trees** | `018-concrete-syntax-trees-and-abstract-syntax-trees.md` |
| 019 | **Syntax Error Recovery and Diagnostics** | `019-syntax-error-recovery-and-diagnostics.md` |
| 020 | **Incremental and Error-Tolerant Parsing** | `020-incremental-and-error-tolerant-parsing.md` |

### Block 03 — Names, Types, and Semantic Analysis

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Scopes and Symbol Tables** | `021-scopes-and-symbol-tables.md` |
| 022 | **Name Resolution and Shadowing** | `022-name-resolution-and-shadowing.md` |
| 023 | **Declarations, Definitions, and Imports** | `023-declarations-definitions-and-imports.md` |
| 024 | **Type Representation** | `024-type-representation.md` |
| 025 | **Type Checking Expressions and Statements** | `025-type-checking-expressions-and-statements.md` |
| 026 | **Constraint Generation and Unification** | `026-constraint-generation-and-unification.md` |
| 027 | **Subtyping and Conversion Rules** | `027-subtyping-and-conversion-rules.md` |
| 028 | **Overload Resolution** | `028-overload-resolution.md` |
| 029 | **Definite Assignment and Control-Flow Checks** | `029-definite-assignment-and-control-flow-checks.md` |
| 030 | **Producing Precise Semantic Diagnostics** | `030-producing-precise-semantic-diagnostics.md` |

### Block 04 — Interpretation and Intermediate Representation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Tree-Walking Interpreters** | `031-tree-walking-interpreters.md` |
| 032 | **Environment and Store Representation** | `032-environment-and-store-representation.md` |
| 033 | **Closures and Function Calls** | `033-closures-and-function-calls.md` |
| 034 | **Bytecode Design** | `034-bytecode-design.md` |
| 035 | **Stack-Based Virtual Machines** | `035-stack-based-virtual-machines.md` |
| 036 | **Register-Based Virtual Machines** | `036-register-based-virtual-machines.md` |
| 037 | **Three-Address Code** | `037-three-address-code.md` |
| 038 | **Control-Flow Graph Construction** | `038-control-flow-graph-construction.md` |
| 039 | **Static Single Assignment Form** | `039-static-single-assignment-form.md` |
| 040 | **Lowering High-Level Constructs into Core IR** | `040-lowering-high-level-constructs-into-core-ir.md` |

### Block 05 — Code Generation and Runtime Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Instruction Selection** | `041-instruction-selection.md` |
| 042 | **Calling Conventions** | `042-calling-conventions.md` |
| 043 | **Stack Frames and Function Prologues** | `043-stack-frames-and-function-prologues.md` |
| 044 | **Register Allocation Foundations** | `044-register-allocation-foundations.md` |
| 045 | **Spilling and Reloading** | `045-spilling-and-reloading.md` |
| 046 | **Object Files, Symbols, and Relocations** | `046-object-files-symbols-and-relocations.md` |
| 047 | **Linking and Loading** | `047-linking-and-loading.md` |
| 048 | **Runtime Representation of Values** | `048-runtime-representation-of-values.md` |
| 049 | **Exceptions and Stack Unwinding** | `049-exceptions-and-stack-unwinding.md` |
| 050 | **Generating Executable Code for a Small Language** | `050-generating-executable-code-for-a-small-language.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Program Analysis

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Dataflow Analysis Frameworks** | `051-dataflow-analysis-frameworks.md` |
| 052 | **Reaching Definitions** | `052-reaching-definitions.md` |
| 053 | **Live-Variable Analysis** | `053-live-variable-analysis.md` |
| 054 | **Available Expressions** | `054-available-expressions.md` |
| 055 | **Dominators and Dominance Frontiers** | `055-dominators-and-dominance-frontiers.md` |
| 056 | **Alias and Points-To Analysis** | `056-alias-and-points-to-analysis.md` |
| 057 | **Interprocedural Analysis** | `057-interprocedural-analysis.md` |
| 058 | **Call-Graph Construction** | `058-call-graph-construction.md` |
| 059 | **Abstract Interpretation in Compiler Analysis** | `059-abstract-interpretation-in-compiler-analysis.md` |
| 060 | **Balancing Analysis Precision and Compile Time** | `060-balancing-analysis-precision-and-compile-time.md` |

### Block 07 — Optimization

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Constant Folding and Propagation** | `061-constant-folding-and-propagation.md` |
| 062 | **Dead-Code Elimination** | `062-dead-code-elimination.md` |
| 063 | **Common-Subexpression Elimination** | `063-common-subexpression-elimination.md` |
| 064 | **Copy Propagation and Sparse Conditional Constants** | `064-copy-propagation-and-sparse-conditional-constants.md` |
| 065 | **Loop-Invariant Code Motion** | `065-loop-invariant-code-motion.md` |
| 066 | **Strength Reduction and Induction Variables** | `066-strength-reduction-and-induction-variables.md` |
| 067 | **Function Inlining** | `067-function-inlining.md` |
| 068 | **Escape Analysis and Scalar Replacement** | `068-escape-analysis-and-scalar-replacement.md` |
| 069 | **Vectorization and Loop Transformation** | `069-vectorization-and-loop-transformation.md` |
| 070 | **Phase Ordering and Optimization Profitability** | `070-phase-ordering-and-optimization-profitability.md` |

### Block 08 — Advanced Code Generation and JIT Compilation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Graph-Coloring Register Allocation** | `071-graph-coloring-register-allocation.md` |
| 072 | **Linear-Scan Register Allocation** | `072-linear-scan-register-allocation.md` |
| 073 | **Instruction Scheduling** | `073-instruction-scheduling.md` |
| 074 | **Machine Description and Target Lowering** | `074-machine-description-and-target-lowering.md` |
| 075 | **Position-Independent Code** | `075-position-independent-code.md` |
| 076 | **Deoptimization Metadata** | `076-deoptimization-metadata.md` |
| 077 | **Tracing JIT Compilation** | `077-tracing-jit-compilation.md` |
| 078 | **Method-Based Tiered JIT Compilation** | `078-method-based-tiered-jit-compilation.md` |
| 079 | **Inline Caches and Speculative Optimization** | `079-inline-caches-and-speculative-optimization.md` |
| 080 | **On-Stack Replacement and Runtime Recompilation** | `080-on-stack-replacement-and-runtime-recompilation.md` |

### Block 09 — Runtime Systems and Memory Management

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Runtime Object Models** | `081-runtime-object-models.md` |
| 082 | **Garbage-Collection Root Discovery** | `082-garbage-collection-root-discovery.md` |
| 083 | **Mark-Sweep Collection** | `083-mark-sweep-collection.md` |
| 084 | **Copying and Generational Collection** | `084-copying-and-generational-collection.md` |
| 085 | **Incremental and Concurrent Collection** | `085-incremental-and-concurrent-collection.md` |
| 086 | **Write Barriers and Remembered Sets** | `086-write-barriers-and-remembered-sets.md` |
| 087 | **Thread Runtimes and Safepoints** | `087-thread-runtimes-and-safepoints.md` |
| 088 | **Foreign Calls and Runtime Transitions** | `088-foreign-calls-and-runtime-transitions.md` |
| 089 | **Dynamic Loading and Reflection Support** | `089-dynamic-loading-and-reflection-support.md` |
| 090 | **Measuring Runtime Latency, Throughput, and Memory** | `090-measuring-runtime-latency-throughput-and-memory.md` |

### Block 10 — Production Language Tooling and Correctness

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Source Maps and Debug Information** | `091-source-maps-and-debug-information.md` |
| 092 | **Language Servers and Incremental Analysis** | `092-language-servers-and-incremental-analysis.md` |
| 093 | **Formatter and Refactoring Infrastructure** | `093-formatter-and-refactoring-infrastructure.md` |
| 094 | **Build Systems and Incremental Compilation** | `094-build-systems-and-incremental-compilation.md` |
| 095 | **Cross-Compilation and Multi-Target Toolchains** | `095-cross-compilation-and-multi-target-toolchains.md` |
| 096 | **Reproducible Compilation** | `096-reproducible-compilation.md` |
| 097 | **Compiler Fuzzing and Differential Testing** | `097-compiler-fuzzing-and-differential-testing.md` |
| 098 | **Translation Validation and Verified Compilation** | `098-translation-validation-and-verified-compilation.md` |
| 099 | **Security Boundaries in Parsers, Compilers, and Runtimes** | `099-security-boundaries-in-parsers-compilers-and-runtimes.md` |
| 100 | **Reviewing a Language Toolchain for Correctness, Diagnostics, and Evolution** | `100-reviewing-a-language-toolchain-for-correctness-diagnostics-and-evolution.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
