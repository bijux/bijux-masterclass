---
module_id: SEPAT-041
program: Software Engineering: Patterns
level: 1
module_number: 41
title: Visitor
status: complete
last_verified: 2026-08-28
---

# Visitor

## One-Page Review

### Governing question

How can new operations be added across a stable family of element types without placing every operation inside those types, while dispatch completeness, traversal, return/error typing, mutation, cycles, compatibility, and effects remain explicit?

### Essential definitions

- An **element hierarchy** is the closed or slowly changing set of concrete data/object variants.
- A **visitor** groups one operation's behavior for every supported concrete element type.
- **double dispatch** selects behavior using both the runtime element type and visitor type: the element's `accept` chooses the visitor's type-specific method.
- The **operation matrix** has element variants as rows and operations as columns; Visitor makes adding columns cheap and adding rows expensive.
- A **traversal policy** defines who visits children, in what order, with what context, and how sharing/cycles are handled.
- An **accumulating visitor** returns or updates a result; a **transforming visitor** constructs/replaces elements.
- The **expression problem** concerns extending both data variants and operations with static safety and modularity.
- A **default/fallback visit** handles unrecognized elements generically, trading compatibility for exhaustiveness.

### Central model, mechanism, or theorem

For element variant (E_i) and visitor (V), dispatch is

$$
accept(E_i,V)=V.visit_i(E_i).
$$

If the element set is (E=\{E_1,...,E_m\}), an exhaustive visitor defines one compatible case per (E_i). Adding operation (O_{n+1}) requires a new visitor column with (m) cases but no element changes; adding variant (E_{m+1}) requires updating the visitor interface and every exhaustive visitor. This change-axis result does not establish traversal termination, operation correctness, or effect safety.

### Critical invariants

- Each concrete element dispatches to exactly its corresponding type-specific visitor operation without downcast/string-type switches.
- Visitor method input, result, error, context, mutability, and resource contracts are coherent across the operation family.
- Exhaustiveness or fallback semantics are explicit; unknown/new variants cannot be silently skipped where completeness matters.
- Traversal ownership and order are singular and documented; children are not accidentally visited twice or omitted.
- Shared nodes/cycles use identity, visited-state, path, depth/node/work budgets, and termination rules as required.
- Read-only visitors cannot mutate elements; transformations preserve invariants and identity/sharing policy through validated replacement.
- Stateful visitors have per-run ownership, reset, concurrency, and partial-failure semantics.
- External/plugin visitors receive only authorized bounded data/capabilities and cannot bypass element invariants.

### Common failures

Common failures include `accept` calling the wrong overload, generic `visit(any)` with casts, defaults that silently ignore new variants, returning unrelated types from cases, visitor and element both traversing children, recursive traversal of cyclic graphs, one global mutable accumulator reused across threads, mutation while iterating children, partial rewrites after failure, retaining elements past lifetime, visitor effects repeated on shared nodes, exposing private representation, adding element types weekly, deep boilerplate where pattern matching is exhaustive, and treating a successful tree walk as compiler/domain correctness.

### Compact example

An expression hierarchy with Literal, Add, and Multiply supplies only `accept`. Independent evaluator, node-counter, and formatter visitors traverse the same tree `(2 + (3 * 4))`, producing 14, five nodes, and an explicitly parenthesized representation.

### Connections

[SEPAT-040](040-template-method.md) varies controlled steps in one inherited skeleton; [SEPAT-042](../ROADMAP.md) supplies behavior for absence. Visitor connects to [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md), [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), and [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md).

## Governing Question

Is the element family more stable than the operations applied to it, and if so, what dispatch, traversal, result, mutation, failure, and evolution contract lets operations live outside the elements without losing safety?

Visitor trades one kind of extensibility for another. It is powerful for compiler AST passes, document models, protocol messages, and object structures with stable variants and frequent analyses—but a poor default for rapidly evolving element schemas.

## Why This Matters

Placing evaluation, rendering, validation, serialization, metrics, optimization, and export methods on every element bloats domain types and couples unrelated dependencies. Visitor groups each operation coherently while preserving type-specific behavior.

The price is visible: every new element variant touches every exhaustive visitor. Traversal and effects can also become hidden in callbacks. The design must choose the dominant change axis and make the operation matrix honest.

## Prerequisites and Retrieval

You should understand dynamic dispatch, overloading, algebraic data types, trees/graphs, recursion, ownership, mutation, and contracts. Retrieve these facts:

1. Ordinary single dispatch selects by receiver runtime type, not all argument runtime types in many OO languages.
2. Overload selection and override dispatch can occur at different stages; language rules matter.
3. A tree has unique parent paths; a graph may share nodes or contain cycles.
4. Traversal order affects stateful operations, diagnostics, effects, and transformations.
5. Exhaustive pattern matching offers a different encoding of the same variant-operation matrix.
6. A pass over syntax/IR needs semantic invariants beyond reaching every node.

## Learning Objectives

After completing this module, you should be able to:

- derive Visitor from the operation matrix and change axes;
- implement and explain double dispatch without reflective type switches;
- design typed result, context, error, and state ownership;
- assign traversal ownership and handle deep/shared/cyclic structures;
- separate read-only analysis, accumulation, effects, and transformation;
- evolve element/visitor protocols with exhaustiveness and compatibility choices;
- compare Visitor with pattern matching, virtual element methods, folds, and pass pipelines;
- test dispatch, traversal, invariants, budgets, concurrency, migration, and effects.

## Core Exposition

### Draw the operation matrix

List concrete element variants as rows and operations as columns. If rows are stable and columns grow, Visitor localizes each new operation. If rows grow frequently, an algebraic data type with exhaustive pattern matches still forces every operation update, while open polymorphic element methods may localize new rows but scatter new operations.

Do not adopt Visitor only to avoid `instanceof`. The change/evolution requirement determines whether its ceremony is worthwhile.

### Understand double dispatch precisely

Client calls `element.accept(visitor)`. Dynamic dispatch selects the concrete element's `accept`; that method calls `visitor.visitConcrete(this)`. The statically specific `this` parameter selects the corresponding visitor case, then dynamic dispatch selects the concrete visitor implementation.

This is a disciplined protocol, not general multiple dispatch. Adding a catch-all `visit(Element)` may bypass type-specific methods depending on language overload rules; test actual language semantics.

### Keep elements minimal but valid

Elements expose `accept` and typed access to state the visitor legitimately needs. They still own construction invariants and mutation APIs. Visitor must not reach into raw mutable representation merely because it is “internal.”

Immutable element values make parallel analyses and transformations easier. Source spans, stable IDs, types, and annotations should have explicit ownership rather than being hidden side tables with unbounded lifetime.

### Choose result and error models

Classic interfaces use `void`, encouraging mutable visitor fields. Modern designs may parameterize result (R), error (E), and context (C): `accept(visitor, context) -> Result<R,E>`. Ensure every case has a coherent result meaning.

For heterogeneous operations, define separate visitor interfaces instead of `Object/any`. A formatter returns text, evaluator returns value/error, validator returns diagnostics, and transformer returns a compatible node.

### Assign traversal ownership once

In **external traversal**, the visitor's `visitAdd` explicitly calls `accept` on children. This lets each operation choose order/pruning but repeats traversal code. In **internal traversal**, elements or a walker visit children and call visitor hooks; traversal is uniform but less customizable.

Do not combine both unintentionally. State whether the hook is preorder, postorder, enter/leave, and whether a visitor may skip, stop, or replace children.

### Handle deep structures

Recursive visitors use call stack proportional to height (h). Adversarial or generated depth can overflow. Bound depth/node/work or use an explicit stack with enter/exit frames.

An iterative postorder traversal stores continuation state. Tail recursion is not a portable assumption across languages/toolchains.

### Distinguish trees from graphs

Shared subtrees may be visited once per edge or once per identity; both can be correct for different operations. A DAG size/count operation must state whether it counts occurrences or unique nodes. Effects should rarely repeat silently for aliases.

Cycles require a visited/color map (`unseen`, `active`, `done`) or domain-specific fixed point. Detecting an active node can report a cycle/path; marking only after recursion does not terminate.

### Manage visitor state

Prefer explicit per-run context/accumulator returned from traversal. If a visitor stores fields, construct one per run or define reset and thread confinement. Partial failure must not leave a reusable visitor with stale state.

Memoization keys include node identity/version plus relevant context. Bound caches and avoid retaining entire object graphs accidentally.

### Separate analysis from transformation

Read-only visitors consume immutable elements and return results. A transforming visitor should construct a new valid tree/graph, returning unchanged nodes for structural sharing when safe. Validate replacement type, ownership, source metadata, and invariants.

In-place mutation during child iteration can invalidate traversal and expose half-rewritten structures on failure. Use plan/build/validate/commit or framework-defined transformer semantics.

### Treat effects as a different operation class

A visitor that writes files, sends messages, or mutates databases couples traversal order/retry to external effects. Prefer collecting a bounded effect plan, validating it, then applying through explicit capability/transaction/workflow boundaries.

If effects occur during visits, define idempotency, identity, ordering, retry, partial failure, cleanup, cancellation, and shared-node semantics. A second traversal may repeat effects.

### Enforce completeness

An exhaustive visitor interface makes a new element a compile error across all implementations in statically checked closed builds. This cost is valuable when omission is dangerous. A default visitor eases compatibility but risks silently skipping security, serialization, or billing-relevant variants.

Use defaults only with explicit semantics such as “unknown nodes produce unsupported diagnostic,” not empty success. Version plugin protocols and reject unsupported element schema ranges.

### Evolve across package/process boundaries

In a monorepo, coordinated visitor updates may be feasible. For third-party visitors, adding a required method is breaking. Options include versioned interfaces, capability negotiation, acyclic visitor interfaces, fallback with mandatory unknown handling, or stable serialized IR plus external pattern matching.

Do not expose arbitrary runtime objects to remote/untrusted visitors. Use bounded validated data schemas and narrow capabilities; serialization does not make code safe.

### Compare language-native alternatives

Algebraic data types plus exhaustive pattern matching make cases visible and often reduce boilerplate for closed variants. Folds/catamorphisms capture uniform recursive structure. Multimethods provide language-level multiple dispatch. Type classes/traits/extensions can attach operations differently.

Visitor remains useful where OO polymorphic elements, binary boundaries, or separately named operation objects fit the architecture. Prefer the language's clearest exhaustive mechanism, not the pattern name.

### Organize pass pipelines

Compiler/analysis systems often have many passes with prerequisites, preserved analyses, invalidation, and transformation invariants. A Visitor may implement one pass's dispatch, while a pass manager owns order, caching, concurrency, instrumentation, and invalidation.

Do not place pass scheduling inside nodes or infer analysis preservation from successful visits. Verify IR before/after transformations and invalidate dependent analyses correctly.

### Test the matrix and traversal

Create one sentinel element per concrete type and a recording visitor; assert exact type-specific dispatch. Test every visitor against every row, including unknown/versioned variants. Test empty/single/deep/wide/shared/cyclic structures, order, pruning/early stop, errors, cancellation, budgets, mutable/state reuse, concurrency, and result invariants.

For transformations, property-test well-formedness and semantic preservation where claimed; differential-test interpreter/compiler outputs; fault-inject effects and cleanup. Mutation tests can confirm omission/reordered traversal is detected.

## Definitions and Notation

Let element variants (E=\{E_1,...,E_m\}), operations (O=\{O_1,...,O_n\}), and behavior matrix $B:E\times O\to R\cup Error$. Visitor (V_j) implements column (O_j).

Double dispatch law:

$$
accept(e_i,V_j)=V_j.visit_i(e_i)=B(E_i,O_j,e_i).
$$

For tree (T=(N,child)), occurrence traversal count satisfies

$$
count(n)=1+\sum_{c\in child(n)}count(c).
$$

For graphs, unique count uses visited identity set; occurrence and unique counts differ under sharing. Termination needs finite reachable graph and a strictly growing bounded visited set or a decreasing work measure.

## Mechanisms, Invariants, or Proof Structure

### Visitor design procedure

1. Draw element-operation matrix and verify elements are the stable axis.
2. Define one `accept`/type-specific case per variant with typed result/error/context.
3. Assign traversal ownership, order, pruning, depth/work, sharing, and cycle semantics.
4. Separate analysis/accumulation, transformation, and effects into distinct visitors.
5. Define per-run state, memoization keys/bounds, concurrency, and cancellation.
6. Choose exhaustive evolution or explicit unknown/version compatibility.
7. Protect invariants/capabilities and integrate pass/effect managers outside elements.
8. Test every matrix cell, structure boundary, transformation property, evolution, and failure.

### Executable mechanism

This immutable expression tree delegates only concrete-type dispatch. Three independent visitors own recursive traversal and coherent results. It does not model source parsing, types, overflow, cycles, shared nodes, transformations, or effects.

<!-- bijux-verify: {"id":"visitor-expression-operations","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"value=14\nnodes=5\nformat=(2 + (3 * 4))\n","stderr":""}} -->
```python
class Literal:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_add(self)


class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_multiply(self)


class Evaluator:
    def visit_literal(self, node):
        return node.value

    def visit_add(self, node):
        return node.left.accept(self) + node.right.accept(self)

    def visit_multiply(self, node):
        return node.left.accept(self) * node.right.accept(self)


class NodeCounter:
    def visit_literal(self, node):
        return 1

    def visit_add(self, node):
        return 1 + node.left.accept(self) + node.right.accept(self)

    def visit_multiply(self, node):
        return 1 + node.left.accept(self) + node.right.accept(self)


class Formatter:
    def visit_literal(self, node):
        return str(node.value)

    def visit_add(self, node):
        return f"({node.left.accept(self)} + {node.right.accept(self)})"

    def visit_multiply(self, node):
        return f"({node.left.accept(self)} * {node.right.accept(self)})"


expression = Add(Literal(2), Multiply(Literal(3), Literal(4)))
print(f"value={expression.accept(Evaluator())}")
print(f"nodes={expression.accept(NodeCounter())}")
print(f"format={expression.accept(Formatter())}")
```

### Dispatch and evaluation argument

Root Add calls each visitor's `visit_add`; Multiply and Literals call their corresponding cases. Evaluation computes $3\cdot4=12$, then (2+12=14). Occurrence count is Add 1 + Literal 1 + Multiply subtree `(1+1+1)=3`, totaling five. Formatter's recursive cases add explicit parentheses/operators.

This proves the shown finite acyclic tree under one language execution. It does not prove dispatch completeness for future classes, integer/domain semantics, termination on arbitrary graphs, or compiler correctness.

### Evidence layers

Review dispatch completeness, operation semantics, traversal/termination, state/concurrency, transformations, effects, and compatibility independently. Reaching every node is necessary but insufficient evidence for most semantic passes.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation | Prefer when |
|---|---|---|---|
| Element virtual methods | Easy new element variant | Every new operation touches elements | Few cohesive stable operations |
| Visitor | Easy new operation column | New variant updates all visitors | Stable variants, frequent operations |
| Pattern matching on ADT | Concise exhaustive cases | New variant updates every match | Closed data and language support |
| Fold/catamorphism | Central recursive shape | Awkward nonuniform/contextual traversal | Uniform structural computations |
| Multimethods | Native multi-argument dispatch | Language/runtime ambiguity/availability | Operation depends on multiple runtime types |
| Reflection/type map | Open registration | Runtime safety and discoverability cost | Dynamic plugin environment with validation |
| Pass manager plus typed IR | Scheduling/invalidation/analysis ownership | Infrastructure complexity | Large compiler/analysis pipelines |

## Failure Modes and Misconceptions

- **“Visitor is just a type switch.”** Correct double dispatch uses element-specific `accept` and typed cases.
- **“It is open for extension.”** It is open for new operations and closed/expensive for new element variants.
- **“A default visit preserves compatibility.”** It may silently omit semantically required behavior.
- **“Elements should traverse children.”** Either elements/walker or visitor owns traversal; choose once.
- **“Tree recursion works for graphs.”** Sharing changes counts/effects and cycles require visited/fixed-point semantics.
- **“One visitor instance is reusable.”** Mutable accumulators/caches need reset, ownership, and thread rules.
- **“Transformers can mutate in place.”** Traversal invalidation and partial failure can corrupt structures.
- **“Successful dispatch proves the operation.”** Semantic correctness, types, invariants, and effects need separate evidence.
- **“Private access is harmless.”** Visitor can destroy element encapsulation if given raw representation.
- **“Remote visitors are ordinary visitors.”** They need data protocols, version negotiation, isolation, and resource bounds.
- **“Visitor and Double Dispatch modules are duplicates.”** Visitor is an operation-organization pattern using double dispatch; double dispatch itself is a broader mechanism.
- **“Compilers are visitors.”** Real pass systems also require analyses, invalidation, scheduling, verification, and diagnostics.

## Worked Examples

### Example 1

Three element rows and three operation columns require nine behaviors. Adding a formatter adds one three-case column without element changes. **Conclusion:** Visitor optimizes operation extension.

### Example 2

Adding Divide requires `accept`, `visit_divide` in the interface, and updates to evaluator/counter/formatter. **Conclusion:** New variants expose Visitor's closed-row cost.

### Example 3

`Multiply.accept` mistakenly calls `visit_add`; expression evaluates 7 rather than 14. A recording matrix test catches the wrong dispatch. **Conclusion:** `accept` correctness is a first-class invariant.

### Example 4

Elements traverse children and the visitor also recurses, so every descendant is processed twice. Assigning traversal exclusively to visitors fixes counts/effects. **Conclusion:** Traversal has one owner.

### Example 5

A shared DAG subtree is referenced twice. Occurrence formatter expands twice, while unique-cost analysis memoizes identity once. **Conclusion:** Sharing semantics depend on the operation.

### Example 6

A graph visitor marks nodes only after visiting neighbors and loops on A→B→A. Marking active before descent detects the cycle/path. **Conclusion:** Cycle termination needs a progress invariant.

### Example 7

A constant-folding visitor mutates children before later validation fails, leaving a hybrid tree. Building a new validated tree preserves failure atomicity. **Conclusion:** Transformations need commit semantics.

### Example 8

A visitor sends one message per node and retry repeats the first half after failure. Collecting an effect plan with stable identities separates traversal from delivery. **Conclusion:** Effects should not hide inside replayable traversal.

### Example 9

A plugin compiled for schema v2 sees a v3 element and default-skips it during security scanning. Mandatory unsupported diagnostics fail closed. **Conclusion:** Compatibility defaults must match consequence.

### Example 10

A medical-rule AST validator reaches all nodes but uses unvalidated units/thresholds and lacks clinical evidence. **Conclusion:** Exhaustive traversal is not domain validity.

## Cross-Program Connections

- **Object-Oriented Programming:** dynamic dispatch, overloading, generics, encapsulation, and inheritance implement Visitor.
- **Programming Languages and Semantics:** algebraic data types, pattern matching, folds, multimethods, and expression-problem research offer alternatives.
- **Compilers and Language Implementation:** AST/IR analyses, transformations, source spans, pass managers, and verification are central uses.
- **Data Structures Engineering:** tree/graph traversal, sharing, cycles, memoization, and complexity govern execution.
- **Functional Programming:** immutable trees, folds, recursion schemes, and persistent transformations reduce state hazards.
- **Concurrency and Parallel Programming:** per-run state, immutable elements, memoization, and partition/reduction constrain parallel visitors.
- **Security Engineering:** plugin isolation, capability minimization, unknown variants, resource budgets, and validation apply.
- **Testing and Quality Engineering:** matrix, property, differential, mutation, fault, and compatibility tests provide evidence.
- **API Engineering:** visitor interfaces are versioned extension protocols across package/plugin boundaries.
- **Systems Engineering:** high-stakes analyses require semantic/domain assurance beyond structural coverage.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Visitor intent, structure, applicability, and consequences.
2. Philip Wadler, [“The Expression Problem”](https://homepages.inf.ed.ac.uk/wadler/papers/expression/expression.txt), 1998. Defines the extensibility problem for adding data variants and operations under static safety/separate compilation.
3. Matthias Felleisen and Daniel P. Friedman, *A Little Java, A Few Patterns*, MIT Press, 1998, ISBN 978-0-262-56115-0. Develops object-oriented interpretation and Visitor-style recursive structures pedagogically.
4. Alfred V. Aho et al., *Compilers: Principles, Techniques, and Tools*, second edition, Pearson, 2006, ISBN 978-0-321-48681-3. Provides AST, semantic analysis, intermediate representation, optimization, and compiler correctness foundations.
5. Python Software Foundation, [`ast.NodeVisitor` and `NodeTransformer`](https://docs.python.org/3/library/ast.html#ast.NodeVisitor), Python 3.14.7, accessed 2026-08-28. Documents current AST visitor/transformer traversal and grammar-evolution behavior.
6. LLVM Project, [Using the New Pass Manager](https://llvm.org/docs/NewPassManager.html), accessed 2026-08-28. Documents current pass/analysis managers, invalidation/preservation, pipelines, and instrumentation for LLVM IR.
7. Oracle, [Java Language Specification §15.12: Method Invocation Expressions](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.12), Java SE 25, accessed 2026-08-28. Defines overload resolution and invocation behavior relevant to double-dispatch implementations.
8. Barbara Liskov and Jeannette Wing, [“A Behavioral Notion of Subtyping”](https://doi.org/10.1145/197320.197383), *ACM TOPLAS* 16(6), 1994. Provides behavioral contract foundations for element and visitor implementations.

## Exercises

### Exercise 1

Trace the executable tree and derive dispatch, evaluation, count, and formatting results with proof limits.

### Exercise 2

Design a typed visitor API supporting results, errors, context, early stop, and explicit traversal ownership.

### Exercise 3

Design a cycle-safe transforming visitor for a shared graph while preserving identity/sharing and failure atomicity.

### Exercise 4

Compare Visitor, exhaustive pattern matching, folds, virtual element methods, and pass managers for a compiler IR.

### Exercise 5

Review an unfamiliar high-stakes analysis visitor without claiming semantic or domain correctness.

## Answers to the Exercises

### Answer 1

Root Add dispatches to each `visit_add`; its left Literal dispatches `visit_literal`; right Multiply dispatches `visit_multiply`, whose two Literals dispatch literal cases. Evaluator computes 3×4=12 then 2+12=14. Counter assigns one per occurrence: root one + left one + right subtree (Multiply one + two literals) three = five. Formatter returns literals as digits and binary cases as parenthesized child strings, yielding `(2 + (3 * 4))`.

This proves the exact finite acyclic expression under the shown classes/visitors and Python execution. It does not prove completeness for future element classes, arbitrary visitor correctness, type/overflow semantics, parsing, cycles/sharing, transformations, effects, concurrency, or compiler correctness.

### Answer 2

Define `Visitor[C,R,E]` with one `visit_X(node: X, context: C) -> Outcome[R,E]` per concrete element. Define `WalkControl` separately for `Continue`, `SkipChildren`, and `Stop(R)` if early stopping is needed. Choose external traversal: a reusable walker owns preorder/postorder/enter-leave and calls visitor hooks, or each visitor owns recursion; do not mix. For uniform walker, hooks return local result/control and a documented combiner reduces child results.

Contract context ownership/immutability, result meaning, typed errors, cancellation/deadline, node/source lifetime, call order/count, shared/cycle identity, depth/node/work limits, and whether failure returns partial diagnostics. Exhaustive visitors require all cases; unknown version returns explicit unsupported error. Test every matrix cell, empty/deep/wide/shared/cyclic structures, every order/control outcome, error/cancel at each point, result combiner laws, state reuse, concurrency, and unknown variants.

### Answer 3

Treat input as immutable graph with stable node IDs and version. Maintain color map and memo `oldID -> new node placeholder/result`. On first node, mark active and allocate a builder/placeholder only if the representation safely supports cycles; recursively transform edges; an edge to active node links the existing placeholder under allowed cycle policy; done node reuses memo, preserving sharing. Validate each transformed node and whole-graph referential/type/domain invariants before publishing a new root/version.

Do not mutate the live graph. Bound nodes, edges, depth/stack, allocations, and work; propagate cancellation/errors and discard the unpublished build on failure. If immutable cyclic construction cannot safely use placeholders, build an intermediate ID/edge table then validate/freeze. Define identity preservation versus deliberate replacement and metadata mapping. Test self/two-node cycles, diamonds, disconnected/unreachable data, invalid edge rewrite, exception/cancel/resource limit at each node, memo correctness, deterministic order, concurrent readers, and semantic equivalence properties.

### Answer 4

Use Visitor when IR variants are stable OO classes and new analyses/operations are frequent; accept coordinated cost for new variants. Use exhaustive pattern matching over an algebraic IR when the language offers closed variants and concise/compiler-checked cases. Use folds for uniform recursive computations where one algebra captures traversal; nonlocal control/context and graph sharing may strain it. Use virtual element methods for a few operations intrinsic to each element, especially when new variants dominate.

Use a pass manager above any dispatch mechanism when many analyses/transformations have prerequisites, caching, preserved/invalidated results, pipelines, instrumentation, concurrency, and verification. A compiler may use pattern matching/Visitor inside passes and a manager outside. Decide by row/column change frequency, binary/plugin boundaries, traversal diversity, IR stability, performance, and language support; retain IR verifier and differential/semantic tests regardless.

### Answer 5

Define analysis purpose, element/schema coverage, input invariants/provenance/version, traversal order/sharing/cycle policy, context, result/error meaning, soundness/completeness claim, numeric/timing/resource assumptions, and action boundary. Verify every concrete/unknown variant has an intentional case, no default silently omits consequence-bearing elements, traversal terminates within bounds, diagnostics identify source/version, and results are independently validated before action.

Evidence includes authoritative domain requirements/traceability, line-by-line case review, formal soundness/termination arguments where tractable, independent recomputation, curated positive/negative/boundary/adversarial corpus, generated/property/metamorphic/differential tests, deep/shared/cyclic/resource/fault cases, historical defect replay, schema migration, concurrency, security/privacy, operational shadowing, and human workflow review. Named domain, formal/algorithm, software verification, security, human-factors, quality/regulatory, and operations reviewers approve. Dispatch exhaustiveness and traversal tests alone establish no semantic soundness, domain validity, safety, or regulatory fitness.
