---
module_id: SEPAT-033
program: Software Engineering: Patterns
level: 1
module_number: 33
title: Interpreter as an Object Pattern
status: complete
last_verified: 2026-08-28
---

# Interpreter as an Object Pattern

## One-Page Review

### Governing question

When is it appropriate to represent a small language's grammar as an object structure whose nodes interpret themselves, and how must syntax, semantics, ambiguity, termination, resource bounds, diagnostics, security, evolution, and evidence be controlled?

### Essential definitions

- A **language** is a set of valid sentences plus rules assigning meaning to them.
- A **grammar** defines syntactic structure through terminal and nonterminal productions.
- A **terminal expression** represents an atomic grammar element; a **nonterminal expression** represents a composite production.
- An **abstract syntax tree (AST)** records semantic structure after irrelevant concrete syntax is removed.
- An **environment/context** maps names and capabilities to values available during interpretation.
- **evaluation semantics** define how an expression and context produce a value, effect, or error.
- **ambiguity** exists when one input has more than one valid parse/meaning under a grammar.
- **precedence** and **associativity** determine grouping of operators.
- **object Interpreter** is the GoF pattern where grammar constructs are classes/objects with interpretation behavior; it is not synonymous with every language runtime.
- A **resource budget** bounds input, tokens, tree nodes/depth, steps, allocation, output, recursion, and external effects.

### Central model, mechanism, or theorem

Let expression grammar be

$$
e ::= literal(v)\mid variable(x)\mid add(e,e)\mid multiply(e,e)\mid less(e,e).
$$

Define evaluation judgment $\langle e,\rho\rangle\Downarrow v$, where environment $\rho$ maps names to typed values. For example, if both operands evaluate to integers (a,b), then $\langle add(e_1,e_2),\rho\rangle\Downarrow a+b$. Correctness requires syntax construction and evaluation to match a versioned language specification; object shape alone proves neither. Termination for the finite pure tree follows by structural descent only if evaluation visits proper subexpressions and no node introduces unbounded recursion/effects.

### Critical invariants

- One versioned specification defines lexical rules, grammar, types, evaluation order, errors, effects, and limits.
- Parsing consumes the intended complete input or reports a located error; trailing text never disappears silently.
- AST nodes are valid, immutable or safely owned, and contain no arbitrary executable host-language objects.
- Evaluation order, scoping, numeric behavior, short-circuiting, and error propagation are deterministic where promised.
- All untrusted inputs have bounded length, token count, nesting, nodes, steps, allocation, output, and effect capabilities.
- Names and operations are allowlisted; evaluation never falls through to host `eval`, reflection, filesystem, network, or process access.
- Diagnostics preserve source spans and stable error categories without exposing secrets or internal stack details.
- Grammar/AST/schema versions, persisted forms, caches, and migrations evolve atomically and compatibly.

### Common failures

Common failures include conflating parsing with evaluation, one class per punctuation token, ambiguous precedence, accepting prefixes with ignored suffixes, left recursion in naive recursive descent, exponential backtracking, stack exhaustion on deep trees, unbounded numeric/string/regex cost, implicit coercions, mutable shared environments, missing source locations, leaking host exceptions, permitting arbitrary function lookup, interpreting serialized class names, evaluating policy with stale identity, persisting unversioned ASTs, and extending a small object grammar until a parser generator/compiler is clearly more appropriate.

### Compact example

Objects represent `((x + 2) < (3 * 4))`. Under environment `x=5`, structural evaluation computes `5+2=7`, `3*4=12`, then `7<12=True`. Seven AST nodes are visited. The example is already parsed and pure; it proves nothing about text parsing or hostile-input bounds.

### Connections

[SEPAT-032](032-command.md) represents intent as data; Interpreter gives structured language data operational meaning. [SEPAT-034](../ROADMAP.md) traverses collections without exposing representation, and [SEPAT-041](../ROADMAP.md) separates new operations from stable node variants. Interpreter connects to [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Is the language small and stable enough that one object per grammar construct yields clearer semantics than a table/generated parser, and what formal and operational constraints keep interpretation correct and safe?

The GoF pattern makes grammar structure visible in an object hierarchy and distributes interpretation across nodes. It works well for compact expression languages but scales poorly when grammar size, operations, optimization, tooling, or hostile inputs grow.

## Why This Matters

Search filters, eligibility expressions, configuration predicates, formatting templates, routing rules, and simple formulas often need a limited language. Hard-coded conditionals spread syntax and semantics; unrestricted general-purpose evaluation creates severe security and governance risks.

A purpose-built interpreter can provide a small auditable capability language. Its language becomes a public contract: precedence, rounding, error text, limits, and persisted expressions can outlive the code that first implemented them.

## Prerequisites and Retrieval

You should understand grammars, tokens, ASTs, recursion, environments, types, evaluation order, complexity, and input validation. Retrieve these facts:

1. A parser maps concrete input to structure; an evaluator assigns meaning to valid structure.
2. AST structure can encode precedence/associativity so evaluation need not rediscover them.
3. Recursive descent terminates only when each recursive call consumes input or descends structurally.
4. “Does not execute code” does not imply safe for untrusted input; memory/CPU/stack exhaustion remain possible.
5. Host-language integers, decimals, strings, regexes, and Unicode each have domain-specific semantics and costs.
6. Adding a node variant is easy in an Interpreter hierarchy; adding many new operations across all variants can be costly.

## Learning Objectives

After completing this module, you should be able to:

- define a small language's concrete grammar, AST, and evaluation judgment;
- implement terminal/nonterminal expression objects with explicit typed semantics;
- separate lexing/parsing, validation, evaluation, and effects;
- analyze precedence, ambiguity, termination, and complexity;
- enforce depth/step/allocation/output/capability budgets;
- design source-located diagnostics and safe versioned persistence;
- distinguish object Interpreter from Visitor, Composite, parser combinators, rule engines, and generated parsers;
- recognize when to replace the pattern with industrial language tooling.

## Core Exposition

### Specify the language before classes

Write lexical categories, grammar productions, precedence/associativity, types, evaluation order, coercions, errors, effects, and limits. Examples are useful but not a specification.

Reserve unknown syntax rather than guessing. Decide whether identifiers are case-sensitive, how Unicode is normalized, and whether keywords can appear as names.

### Separate concrete and abstract syntax

Parentheses, commas, comments, and whitespace matter to parsing but often disappear from the AST. AST nodes represent semantic constructs such as `Add(left,right)`.

Preserve source spans on nodes or a side table for diagnostics/audit. Generated expressions still need provenance distinct from user-authored spans.

### Parse the whole input

The lexer produces bounded tokens with spans. The parser returns one AST only after consuming end-of-input. Recovery may collect errors for editors, but execution must not run an invalid partially recovered tree.

Avoid ad hoc token splitting for quoting, escapes, Unicode, nested syntax, or comments. Use a parser technique whose grammar class and complexity are understood.

### Encode precedence and associativity

Grammar layers or precedence declarations distinguish `2+3*4` from `(2+3)*4`. Left-associative subtraction parses `10-3-2` as `(10-3)-2`, not `10-(3-2)`.

Ambiguity must be rejected or resolved by documented rules. “Whichever branch succeeds first” becomes compatibility behavior and may create pathological backtracking.

### Define typed evaluation

Each node states accepted operand types, result type, evaluation order, and failure. Avoid broad implicit coercion: string-to-number, timezone, unit, and locale conversions can change meaning.

Use an explicit result algebra such as value, type error, unknown name, limit exceeded, forbidden operation, or external failure. Preserve source span and cause policy.

### Keep the environment capability-safe

Map names to owned values or narrowly scoped callable capabilities. Do not expose host globals, reflection, object attributes, modules, database sessions, or arbitrary functions.

Authorization applies to each resource/effect at evaluation time. A parse-time allowlist cannot freeze user authority or dynamic policy.

### Prove or enforce termination

Pure finite AST evaluation terminates by decreasing subtree size if every rule evaluates only proper children a finite number of times. Variables must not recursively expand without cycle/step checks.

Loops, recursion, user functions, regex, comprehensions, and external calls require additional termination/fuel/time policies. A timeout alone may not stop noncooperative host work.

### Bound resources before and during evaluation

Limit input bytes/code points, token length/count, nesting, AST nodes/depth, identifier/string/numeric size, evaluation steps, call depth, collection/output size, external calls, and deadline. Enforce cheap limits early.

Prefer iterative traversal for adversarial depth where practical. Use checked arithmetic or explicit integer/decimal semantics; enormous powers or concatenations can exhaust memory even in a pure language.

### Isolate effects

Keep the expression core pure when possible. Represent external operations through allowlisted capabilities with authorization, budgets, idempotency, deadlines, cancellation, and audit.

Separate planning from execution for queries/policies: evaluation can produce a validated plan that a controlled executor performs. Never concatenate interpreted strings into SQL, shell, templates, or URLs.

### Design diagnostics as API

Errors include stable code, source span, safe message, expected constructs/types, and bounded context. Separate user-facing detail from internal cause/correlation.

Do not reveal secrets, filesystem paths, stack traces, policy internals, or whether a forbidden resource exists. Recovery suggestions must not change executed meaning silently.

### Version grammar and persisted ASTs

Persist source plus language version and integrity/provenance when feasible. If persisting ASTs, use allowlisted versioned node schemas, not class names or arbitrary object serialization.

Grammar changes can reparse old source differently. Golden examples, differential tests, versioned parsers, explicit migration, and cache-key language version prevent silent reinterpretation.

### Test beyond happy examples

Use grammar examples/counterexamples, lexer/parser properties, round-trip where defined, AST invariants, semantic unit tests, differential/reference evaluation, metamorphic properties, fuzzing, malformed/deep/large inputs, and limit tests.

For effects, test authorization, injection boundaries, cancellation, retries, and failure. Measure time/memory/stack across adversarial distributions, not just average valid expressions.

### Know when the pattern stops fitting

Move to parser generators, parser combinators, bytecode/VM, or dedicated rule/query systems when grammar grows, diagnostics/tooling matter, multiple operations proliferate, optimization is required, or inputs are hostile/high-volume.

Generated parsers do not solve semantic security automatically, but they provide explicit grammar tooling and tested parsing algorithms. Preserve the language specification during migration.

## Definitions and Notation

Let environment $\rho:Name\rightharpoonup Value$ be partial. Evaluation uses judgment $\langle e,\rho,b\rangle\Downarrow(v,b')$, where fuel $b\in\mathbb{N}$ decreases at each visited node; zero fuel yields `LimitExceeded`.

For tree (e), size $|e|=1+\sum |child|$ and height $h(e)=1+\max h(child)$, with terminal height one. A pure structural evaluator visits (O(|e|)) nodes when each node evaluates each child once and primitive operations have bounded cost; big integers/strings and lookup/effect costs invalidate constant-operation assumptions.

Parsing function is $parse_v:Text\to AST_v\mid SyntaxErrors$. Complete consumption requires the accepted derivation end at EOF. Semantic function (eval_v) is version-indexed; changing (v) can change parse or meaning and is therefore a compatibility decision.

## Mechanisms, Invariants, or Proof Structure

### Language design procedure

1. Define purpose, trust boundary, version, and non-goals.
2. Specify lexical grammar, syntax, precedence, types, errors, effects, and budgets.
3. Build lexer/parser that consumes complete bounded input with spans.
4. Validate immutable allowlisted AST nodes.
5. Evaluate under explicit environment/capabilities and fuel/deadline.
6. Preserve safe diagnostics, provenance, and audit.
7. Test semantics, grammar, adversarial limits, versions, and effects.
8. Replace object interpretation when scale/tooling/operations demand it.

### Executable mechanism

This already-parsed pure AST demonstrates grammar objects, left-to-right structural evaluation, rendering, and node counting. It is not a text parser or sandbox.

<!-- bijux-verify: {"id":"interpreter-expression-objects","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"expr=((x + 2) < (3 * 4))\nresult=True nodes=7\n","stderr":""}} -->
```python
class Literal:
    def __init__(self, value):
        self.value = value

    def evaluate(self, environment):
        return self.value

    def render(self):
        return str(self.value)

    def nodes(self):
        return 1


class Variable:
    def __init__(self, name):
        self.name = name

    def evaluate(self, environment):
        if self.name not in environment:
            raise ValueError("unknown variable")
        return environment[self.name]

    def render(self):
        return self.name

    def nodes(self):
        return 1


class Binary:
    symbol = "?"

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def render(self):
        return "(" + self.left.render() + " " + self.symbol + " " + self.right.render() + ")"

    def nodes(self):
        return 1 + self.left.nodes() + self.right.nodes()


class Add(Binary):
    symbol = "+"

    def evaluate(self, environment):
        return self.left.evaluate(environment) + self.right.evaluate(environment)


class Multiply(Binary):
    symbol = "*"

    def evaluate(self, environment):
        return self.left.evaluate(environment) * self.right.evaluate(environment)


class Less(Binary):
    symbol = "<"

    def evaluate(self, environment):
        return self.left.evaluate(environment) < self.right.evaluate(environment)


expression = Less(Add(Variable("x"), Literal(2)), Multiply(Literal(3), Literal(4)))
print("expr=" + expression.render())
print("result=" + str(expression.evaluate({"x": 5})) + " nodes=" + str(expression.nodes()))
```

Production nodes would be immutable, typed, source-located, budgeted, and constructed only by a bounded validated parser or trusted builder.

### Proof obligations

For the pure grammar, prove evaluation determinism/type preservation/termination relative to explicit rules if those claims are required. For parsing, prove or test grammar coverage, ambiguity resolution, EOF consumption, and complexity. Security requires complete capability and resource analysis, not absence of host `eval` alone.

The snippet proves one finite AST computation and node count only.

## Alternatives and Trade-Offs

| Approach | Strength | Main trade-off |
|---|---|---|
| Object Interpreter | direct grammar-to-class mapping | many classes; slow evolution across operations |
| Visitor over AST | separates operations from nodes | harder new node variants |
| Parser combinators | compositional parsing in host language | performance/error complexity varies |
| Generated parser | grammar tooling and scalable syntax | generated build/runtime complexity |
| Pratt parser | concise expression precedence | specialized technique |
| Bytecode/VM | repeated execution and optimization | compiler/runtime complexity |
| Decision table/rule engine | declarative policy/conflicts | governance/explainability cost |
| Host-language `eval` | broad power | unacceptable authority/injection risk for untrusted input |

Choose by language size, change axis, trust, performance, tooling, and team expertise—not the number of example productions.

## Failure Modes and Misconceptions

### “The AST is the grammar”

The AST omits concrete syntax and cannot alone specify tokenization, precedence, ambiguity, or full-input acceptance.

### “No `eval` means safe”

Deep/large inputs, huge arithmetic, regex, allocations, and capabilities can exhaust resources or cause harmful effects.

### “Recursion always terminates on a tree”

Only structural descent over a finite acyclic tree does. Cyclic graphs, variable expansion, functions, or child reevaluation can diverge.

### “Errors can be host exceptions”

Host messages are unstable and may leak internals. Translate to source-located stable language errors while retaining safe causes.

### “A parser can ignore the remaining text”

Prefix acceptance can hide injection or user mistakes. Require EOF unless the surrounding protocol explicitly owns the suffix.

### “Every grammar rule needs an interpreter class”

Concrete-syntax helper productions may collapse into one AST node; one class per punctuation rule adds noise.

### “The pattern scales to any DSL”

Large languages need grammar tooling, multiple passes, symbol/type analysis, optimization, and robust recovery. Replace the object pattern before it becomes accidental compiler infrastructure.

## Worked Examples

### Example 1

`2+3*4` parses as `Add(2,Multiply(3,4))` and evaluates to 14; `(2+3)*4` evaluates to 20. **Conclusion:** AST construction, not evaluator guesswork, encodes precedence.

### Example 2

A parser accepts `x < 10 DROP` by stopping after the valid prefix. Requiring EOF reports the trailing token. **Conclusion:** Complete consumption is a security and correctness invariant.

### Example 3

A naive rule `expr → expr + term | term` recurses before consuming input. Rewriting or using a parser supporting left recursion restores progress. **Conclusion:** Grammar shape interacts with parsing algorithm.

### Example 4

A 100,000-level nested expression overflows recursive evaluation. Parse-depth/node limits reject it early; iterative traversal handles permitted depth. **Conclusion:** Pure syntax still needs resource budgets.

### Example 5

A policy language exposes arbitrary object attributes, allowing secret traversal. Replacing the environment with allowlisted typed values/capabilities closes it. **Conclusion:** Host object access destroys sandbox boundaries.

### Example 6

`false and expensive()` must short-circuit without evaluating the right child. A generic eager `Binary` base violates the language spec. **Conclusion:** Evaluation order belongs to each construct's semantics.

### Example 7

An old persisted formula is reparsed after precedence changes and yields a different result. Versioned source/parser or migrated AST preserves meaning. **Conclusion:** Grammar changes are data compatibility changes.

### Example 8

A regex operator permits catastrophic patterns on attacker text. A restricted engine/pattern subset plus input/time limits replaces raw host regex. **Conclusion:** Delegated primitives inherit their complexity and threat model.

### Example 9

Adding pretty-print, type-check, optimize, lint, and evaluate methods to every node makes each new operation invasive. Visitor or external passes become preferable. **Conclusion:** Choose representation by dominant change axis.

### Example 10

A dosage-rule DSL appears mathematically simple but depends on units, patient context, contraindications, rounding, provenance, and clinical governance. It is not deployed from this pattern alone. **Conclusion:** An interpreter implementation cannot establish clinical validity.

## Cross-Program Connections

- **Programming Languages and Semantics:** grammars, operational semantics, typing, scoping, determinism, and effects are foundational.
- **Functional Programming:** algebraic data types, folds, parser combinators, and immutable environments offer direct formulations.
- **Theory of Programming:** induction, termination measures, type preservation, and equivalence support proofs.
- **Compilers:** lexing, parsing, ASTs, semantic analysis, IR, optimization, VMs, and diagnostics extend beyond the pattern.
- **Algorithms:** parsing complexity, memoization, graph traversal, and adversarial resource analysis matter.
- **Testing and Quality:** grammar properties, differential/metamorphic tests, fuzzing, limit tests, and golden versions provide evidence.
- **Database Engineering:** query languages, plans, expression evaluation, types, and injection boundaries are related.
- **Security Engineering:** allowlists, resource exhaustion, sandbox/capability design, and safe diagnostics constrain execution.
- **API Engineering:** versioned DSL contracts, error schemas, pagination/query limits, and compatibility affect consumers.
- **Systems Engineering:** rule languages in high-stakes domains require domain validation and independent control evidence.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Interpreter intent, structure, applicability, and consequences.
2. Alfred V. Aho, Monica S. Lam, Ravi Sethi, and Jeffrey D. Ullman, *Compilers: Principles, Techniques, and Tools*, second edition, Pearson, 2006, ISBN 978-0-321-48681-3. Provides lexical, parsing, syntax-tree, semantic-analysis, and code-generation foundations.
3. Terence Parr, Sam Harwell, and Kathleen Fisher, [“Adaptive LL(*) Parsing: The Power of Dynamic Analysis”](https://www.antlr.org/papers/allstar-techreport.pdf), OOPSLA 2014. Provides ANTLR 4 parsing strategy, grammar analysis, and performance/correctness results.
4. Robert Nystrom, [*Crafting Interpreters*](https://craftinginterpreters.com/representing-code.html), 2021 online edition. Provides original-language implementation exposition for AST representation and evaluation.
5. Python Software Foundation, [`ast` documentation](https://docs.python.org/3/library/ast.html), Python 3.14, accessed 2026-08-28. Warns that even restricted literal evaluation can exhaust memory, CPU, or stack on untrusted inputs.
6. OWASP Foundation, [Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html), accessed 2026-08-28. Provides allowlist, length/range, structured validation, and ReDoS guidance.
7. Unicode Consortium, [Unicode Standard Annex #31: Unicode Identifiers and Syntax](https://unicode.org/reports/tr31/), Unicode 17.0.0, 2025. Defines identifier profiles and syntax security/interoperability foundations.

## Exercises

### Exercise 1

Derive the executable evaluation and node count formally, and state exactly what is unproved.

### Exercise 2

Extend the grammar with Boolean `and` and equality. Specify precedence, types, short-circuiting, errors, and evaluation rules.

### Exercise 3

Design a bounded parser/evaluator contract for untrusted filter expressions, including diagnostics and operational telemetry.

### Exercise 4

Plan migration from object Interpreter to generated parser plus external semantic passes without changing version-one meaning.

### Exercise 5

Review an unfamiliar clinical-rule interpreter proposal without claiming clinical correctness or regulatory suitability.

## Answers to the Exercises

### Answer 1

The tree has root `Less`; left `Add` has `Variable(x)` and `Literal(2)`, while right `Multiply` has literals 3 and 4: (1+(1+1+1)+(1+1+1)=7) nodes. Under $\rho(x)=5$, variable evaluates 5, literal 2 evaluates 2, and add gives 7. Literals 3 and 4 multiply to 12. Less compares 7<12 and yields true. Rendering adds explicit parentheses and symbols to produce the shown string.

This proves one finite, already-built, well-typed, acyclic AST under one environment. It does not prove text parsing, precedence rules, unknown-name diagnostics, type errors, overflow/big-number cost, evaluation fuel/depth, immutability, security, concurrency, serialization, version compatibility, or arbitrary-expression termination.

### Answer 2

Define precedence from tightest to loosest: primary, multiplication, addition, comparison/equality, then `and`; forbid chained comparison or define it explicitly. AST adds `Equal(left,right)` and `And(left,right)`. Equality requires same compatible type under a documented relation and returns Boolean. `And` requires Boolean left/right and evaluates left first; if false it returns false without evaluating right, otherwise evaluates right and returns it if Boolean.

Rules: if $e_1\Downarrow false$, `And(e1,e2)` yields false without a judgment for (e_2); if $e_1\Downarrow true$ and $e_2\Downarrow b$, result is (b). Non-Boolean operand yields source-located type error at the offending expression. Equality defines numeric/string/Boolean behavior without implicit cross-type coercion. Tests cover precedence such as `1+2==3 and false`, short-circuit with forbidden/failing right side, all type pairs, errors/spans, and budget consumption only for visited nodes.

### Answer 3

Define allowed tokens/operators/functions/types, Unicode identifier profile/normalization, complete-input grammar/version, precedence, and stable errors. Bound input bytes/code points, token and identifier length, token count, nesting, AST nodes/depth, numeric/string/collection size, evaluation steps, output, external calls, and absolute deadline. Reject invalid UTF encoding and unknown syntax/types; use checked arithmetic and restricted regex or no regex.

Parser returns immutable source-located allowlisted nodes only after EOF and validation. Evaluator uses typed owned values and capability references, not host globals/attributes/reflection; authorization is checked at effect time. Telemetry records language version, outcome/error code, tokens/nodes/depth/steps, duration, limit triggered, and bounded operator/function IDs without source text/secrets. Tests include grammar examples/counterexamples, fuzzing, deep/wide/huge numbers/strings, ambiguous prefixes, Unicode confusables per policy, catastrophic primitives, authorization, cancellation, and load/soak.

### Answer 4

Freeze a version-one lexical/grammar/semantic specification and golden corpus containing source, tokens, AST canonical form, value/error/spans, steps, and edge cases. Characterize undocumented behavior before deciding whether it is supported. Implement generated v1 lexer/parser that produces the same owned AST schema; differential-test old versus new across golden, generated, fuzzed, malformed, and adversarial inputs.

Move evaluation, type checking, rendering, linting, and optimization into explicit passes incrementally, retaining the object evaluator as an oracle during shadow operation. Preserve source/language version and original text; never reparse persisted v1 under v2 silently. Compare outcome and resource telemetry, canary consumers, and retain rollback. Only after equivalence criteria pass should the old parser/evaluator be removed. New syntax ships under an explicit compatible extension or v2 with migration tooling and cache keys including language version.

### Answer 5

Define clinical purpose, population, inputs with units/ranges/provenance/time, rule authority/version, missing/conflicting data, output meaning, rounding/uncertainty, override, and failure behavior before grammar design. Restrict language capabilities; no arbitrary host calls, dynamic network access, reflection, or hidden mutable state. Bind each evaluation to authenticated user/patient/context and exact rule/data versions, with audit and safe unavailable behavior. Independent clinical controls remain outside the interpreter.

Evidence requires authoritative clinical requirements and traceability, independent dimensional/numerical recomputation, reference datasets with provenance, boundary/population/contraindication cases, formal/type/range/termination analysis where tractable, parser/evaluator differential and fuzz testing, resource and security testing, version/migration validation, usability/human-factors review, simulator/workflow trials, and controlled release/rollback. Named clinicians and relevant specialists, clinical informatics, statistics, software verification, cybersecurity/privacy, human factors, quality, regulatory, operations, and independent reviewers approve. This pattern, implementation, and tests establish no clinical validity, patient safety, or regulatory fitness.
