---
module_id: PLS-003
program: Programming Languages & Semantics
level: 1
module_number: 3
title: Grammars, Parse Trees, and Abstract Syntax
status: complete
last_verified: 2026-08-29
---

# Grammars, Parse Trees, and Abstract Syntax

## One-Page Review

### Governing question

How does a language turn a token sequence into a structural representation that preserves every syntactic distinction needed for meaning while discarding surface detail only by an explicit, testable abstraction?

### Essential definitions

- A **grammar** is a finite system of productions describing how symbols may be composed into phrases.
- A context-free grammar is a tuple `G=(N,Σ,P,S)`: nonterminals `N`, terminals `Σ`, productions `P`, and start symbol `S`.
- A **sentential form** contains terminals and nonterminals reachable during derivation; a **sentence** contains only terminals.
- A **derivation** replaces a nonterminal using a production. Leftmost and rightmost derivations choose which remaining nonterminal to expand next.
- A **parse tree** witnesses a derivation: internal nodes are nonterminals, children match one production, and the ordered leaf terminals form the input's **yield**.
- A grammar is **ambiguous** when some sentence has two structurally distinct parse trees, not merely two derivation orders for the same tree.
- **precedence** says which operator groups more tightly; **associativity** says how repeated operators of one precedence group.
- BNF is a grammar metalanguage; EBNF adds conveniences such as optionality, repetition, and grouping. Notation conventions must be stated because dialects differ.
- A **concrete syntax tree (CST)** retains surface-oriented structure, often including punctuation, tokens, trivia, and recovery nodes; terminology varies across tools.
- An **abstract syntax tree (AST)** represents language constructs while omitting grammar scaffolding and punctuation whose roles are already encoded structurally.
- **lowering** maps one representation to a more abstract or implementation-oriented one while preserving the required interpretation and provenance.
- A **well-formedness constraint** may be grammatical, contextual/static, or semantic; parse success alone does not make a valid program.
- An **error node** preserves an invalid or missing region explicitly so tooling does not silently treat recovery as valid source.

### Central model, mechanism, or theorem

For grammar `G`, the generated language is `L(G)={w∈Σ* | S⇒*w}`. A parse tree `t` is valid for `w` when every internal expansion belongs to `P` and `yield(t)=w`. An abstraction function `α:T_G⇀A` maps accepted concrete trees into abstract syntax `A`; it may be many-to-one because parentheses, separators, or alternative spellings can denote the same abstract construct. Correct abstraction preserves distinctions needed by later static and dynamic semantics, source diagnostics, and tools. If `α(t1)=α(t2)`, that equality is justified only relative to the information intentionally forgotten.

### Critical invariants

Every terminal/nonterminal and EBNF operator has declared meaning. The root uses the intended goal symbol and consumes the entire significant input. Each parse-tree node corresponds to a permitted production and its yield matches token order exactly. Precedence and associativity are structural, not post-hoc intuition. Ambiguity is rejected, deliberately represented, or resolved by documented policy. Epsilon and repetition guarantee parser progress. CST losslessness includes trivia/error provenance when promised. AST constructors carry all semantic operands and distinctions. Lowering is total for accepted concrete forms or emits a bounded diagnostic. Source spans remain traceable. Contextual restrictions are not misreported as grammar facts. Grammar and AST schema changes are versioned and tested together.

### Common failures

Authors call a regular expression a complete language grammar; mix characters and tokens; confuse grammar notation with the object language; forget a start or end condition; use ambiguous expression productions; assume tree shape follows mathematical convention; equate leftmost/rightmost derivations with different parses; erase parentheses before encoding grouping; use `*` around a nullable phrase and permit zero-progress repetition; claim an AST can reproduce comments it discarded; put name/type rules into ad hoc parser actions; accept trailing tokens; recover by inventing a valid node silently; expose grammar helper nodes as a stable API; or change a grammar without checking old programs and downstream AST consumers.

### Compact example

The ambiguous grammar `E→E+E | E*E | n` gives `n+n*n` both `Add(n,Mul(n,n))` and `Mul(Add(n,n),n)`. Refactoring into `Expr→Term ("+" Term)*`, `Term→Factor ("*" Factor)*` makes multiplication bind tighter; folding each repetition left gives an AST whose structure records that decision.

### Connections

[Lexical Structure, Tokens, and Concrete Syntax](002-lexical-structure-tokens-and-concrete-syntax.md) supplies terminals and source spans. The next chapter, *Names, Bindings, and Environments*, is indexed in the [program roadmap](../ROADMAP.md) and adds contextual meaning to identifiers. The [Compilers and Language Implementation roadmap](../../08-compilers-and-language-implementation/ROADMAP.md) studies implementation from the compiler perspective. These boundaries separate language structure from parser-engineering ownership.

## Governing Question

What evidence shows that an accepted token sequence has one intended structure and that the representation handed to later phases has neither lost a meaningful distinction nor invented validity?

The answer requires three contracts: a grammar contract for admitted terminal sequences, a tree contract for structural witnesses and source fidelity, and an abstraction contract for translating concrete structure into semantic constructs.

## Why This Matters

Structure determines meaning before evaluation begins. `1 + 2 * 3` and `(1 + 2) * 3` use the same numerals and operators, yet their trees encode different computations. A dangling `else`, chained comparison, type annotation, pattern, or indentation block is understandable only after grouping decisions are explicit.

The same boundary serves many consumers. A compiler wants an AST convenient for name resolution and evaluation. A formatter wants comments, delimiters, and original spelling. A refactoring tool needs both semantic structure and precise source ranges. An editor must represent incomplete code without claiming it parses normally. A macro system may preserve token trees before ordinary parsing.

Poorly designed representations spread accidental grammar details throughout a toolchain. Conversely, an AST that abstracts too aggressively destroys information needed for diagnostics, compatibility, security review, or source transformation. The durable practice is to define each representation by what it guarantees and what it intentionally forgets.

## Prerequisites and Retrieval

Retrieve finite sets, sequences, rooted ordered trees, relations, induction, and simple regular-language ideas. From [Programs, Languages, and Observable Behavior](001-programs-languages-and-observable-behavior.md), recall that a representation has meaning only relative to a language and observer. From [Lexical Structure, Tokens, and Concrete Syntax](002-lexical-structure-tokens-and-concrete-syntax.md), retrieve token kind, lexeme, trivia, half-open span, lexical error, and end-of-input.

Preparation ledger: name the token alphabet; grammar notation/dialect; start symbols for file, expression, type, pattern, or interactive input; concrete grouping/separator rules; precedence and associativity; contextual restrictions; CST fidelity and recovery promises; AST schema and provenance; consumers; compatibility policy; resource limits; and tests for accepted, rejected, ambiguous, incomplete, and historical inputs.

## Learning Objectives

After completing this module, a learner can:

1. define a context-free grammar and distinguish grammar symbols from its metalanguage;
2. construct derivations, parse trees, and yields for short token sequences;
3. distinguish ambiguity from alternative traversal or derivation order;
4. encode operator precedence and associativity structurally;
5. translate common EBNF repetition/option forms into ordinary productions;
6. distinguish parse trees, CSTs, ASTs, token trees, and later IRs by contract;
7. design an AST schema and a provenance-preserving lowering function;
8. separate context-free syntax from contextual/static well-formedness;
9. test grammar acceptance, tree shape, recovery, round trips, compatibility, and resource bounds; and
10. constrain safety-critical syntax claims to named human review and system validation.

## Core Exposition

### Grammars describe languages over symbols

A grammar is itself written in a metalanguage. In `Expr ::= Expr "+" Term | Term`, `Expr` and `Term` are nonterminals, quoted `"+"` is a terminal, `::=` introduces a production, and `|` separates alternatives in that chosen notation. The punctuation of BNF is not automatically punctuation in the described language.

A context-free grammar `G=(N,Σ,P,S)` has disjoint finite sets of nonterminals and terminals, a finite production relation `P⊆N×(N∪Σ)*`, and start symbol `S∈N`. “Context-free” means the left side of each production is one nonterminal; applying it does not inspect neighboring symbols. This property says nothing by itself about deterministic or efficient parsing.

The one-step relation `⇒` replaces one occurrence of a production's left side with its right side. Its reflexive transitive closure `⇒*` permits zero or more steps. The language is the terminal strings derivable from `S`. If tokens rather than characters are terminals, `Σ*` is a sequence of token kinds/values as defined by the grammar interface.

Multiple start symbols can be deliberate: a whole file, interactive statement, expression, type, or pattern may have different surrounding requirements. A successful whole-file parse must also consume the explicit end marker; otherwise a parser could accept a valid prefix and ignore dangerous trailing input.

### Derivations and parse trees are related but distinct

Consider:

`Expr → Term ExprTail`

`ExprTail → "+" Term ExprTail | ε`

`Term → INTEGER`

A leftmost derivation for `INTEGER + INTEGER` always expands the leftmost remaining nonterminal. A rightmost derivation expands the rightmost. Both can witness the same parse tree. Derivation order describes a proof sequence; tree shape records which production instances contain which children.

A parse tree is rooted at the start symbol. For every internal nonterminal node, its ordered children are exactly one right-hand side; epsilon can be represented explicitly or by an empty child list under a declared convention. Reading terminal leaves left to right gives the yield. These facts support structural induction: prove a property for each production assuming it holds for recursive children.

Do not identify a tree only by pretty-printed parentheses. Production identity, symbol, child order, source span, and parser invocation/generation may matter. Two parses of identical text can yield structurally equal but distinct tree objects.

### BNF and EBNF need explicit dialects

EBNF compresses recurring grammar patterns. A notation may use `[x]` or `x?` for optionality, `{x}` or `x*` for zero-or-more, `x+` for one-or-more, and parentheses for grouping. ISO/IEC 14977 defines one EBNF, while Python, Rust, W3C specifications, parser generators, and PEG systems use related but nonidentical operators.

`A → x?` can be expanded as `A → x | ε`. `A → x*` can become `A → x A | ε`; `x+` can become `x A` where `A` represents `x*`. These transformations preserve the generated terminal language when performed correctly, but they can change parse-tree scaffolding and parser behavior.

Beware nullable repetition. If `x⇒*ε`, then repeating `x*` can choose another occurrence without consuming input. A mathematical grammar may still denote a language, but a naive parser loop can fail to progress or create infinitely many empty derivations. Require each successful loop iteration to consume input or make a separately bounded state transition.

Ordered choice in parsing-expression grammars (PEGs) is not CFG alternation: the first successful alternative commits according to PEG semantics. Lookahead and cut operators also add operational meaning. Copying a production between notations without translating these rules changes the language.

### Ambiguity is structural

The grammar `E→E+E | E*E | n` is ambiguous because `n+n*n` has two parse trees with different grouping. It is not enough that a parser implementation happens to choose multiplication first; that policy must be part of the grammar or a declared disambiguation rule.

Refactor by precedence levels:

`Expr → Term ("+" Term)*`

`Term → Factor ("*" Factor)*`

`Factor → INTEGER | "(" Expr ")"`

Now `*` occurs inside a `Term`, while `+` joins terms. Repetition still needs an associativity policy when lowered. Folding `a-b-c` left yields `Sub(Sub(a,b),c)`; folding right yields `Sub(a,Sub(b,c))`. Exponentiation is often right-associative; comparisons may be nonassociative or use a special chained form. Tree structure—not typography—records the contract.

Precedence declarations in parser tools can resolve conflicts without rewriting productions, but the resulting structure must be documented and tested. Generalized parsers may preserve a parse forest for deliberate ambiguity. Natural-language-style or extensible syntax may need later selection, but most programming-language constructs benefit from an unambiguous public grammar.

Ambiguity differs from grammar nondeterminism in an implementation and from multiple derivation orders for one tree. To demonstrate ambiguity, exhibit one terminal sentence and two non-isomorphic parse trees or distinct production structure.

### Parse and abstract two expressions

The executable parser below consumes pre-tokenized arithmetic. Its EBNF-shaped loops build a concrete tree retaining `+`, `*`, and parentheses; lowering folds repetitions left and removes grouping punctuation after encoding the grouping in AST structure. It demonstrates only this finite grammar and does not prove a general parser, error recovery, numeric semantics, or language correctness.

<!-- bijux-verify: {"id":"expression-cst-to-ast","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source=1+2*3\ncst=Expr(Term(Factor(1)),+,Term(Factor(2),*,Factor(3)))\nast=Add(Int(1),Mul(Int(2),Int(3)))\nvalue=7\nsource=(1+2)*3\ncst=Expr(Term(Factor((,Expr(Term(Factor(1)),+,Term(Factor(2))),)),*,Factor(3)))\nast=Mul(Add(Int(1),Int(2)),Int(3))\nvalue=9\n","stderr":""}} -->
```python
def node(name, children):
    return (name, children)

def peek(state):
    if state["position"] == len(state["tokens"]):
        return "EOF"
    return state["tokens"][state["position"]][0]

def take(state, kind):
    actual_kind, lexeme = state["tokens"][state["position"]]
    if actual_kind != kind:
        raise ValueError("unexpected token")
    state["position"] += 1
    return lexeme

def parse_factor(state):
    if peek(state) == "INTEGER":
        return node("Factor", [take(state, "INTEGER")])
    opening = take(state, "LPAREN")
    expression = parse_expression(state)
    closing = take(state, "RPAREN")
    return node("Factor", [opening, expression, closing])

def parse_term(state):
    children = [parse_factor(state)]
    while peek(state) == "STAR":
        children += [take(state, "STAR"), parse_factor(state)]
    return node("Term", children)

def parse_expression(state):
    children = [parse_term(state)]
    while peek(state) == "PLUS":
        children += [take(state, "PLUS"), parse_term(state)]
    return node("Expr", children)

def parse(tokens):
    state = {"tokens": tokens, "position": 0}
    tree = parse_expression(state)
    if state["position"] != len(tokens):
        raise ValueError("trailing token")
    return tree

def render(tree):
    if isinstance(tree, str):
        return tree
    name, children = tree
    return name + "(" + ",".join(render(child) for child in children) + ")"

def lower(tree):
    name, children = tree
    if name == "Factor":
        if len(children) == 1:
            return node("Int", [children[0]])
        return lower(children[1])
    operator = "Add" if name == "Expr" else "Mul"
    result = lower(children[0])
    for index in range(2, len(children), 2):
        result = node(operator, [result, lower(children[index])])
    return result

def evaluate(tree):
    name, children = tree
    if name == "Int":
        return int(children[0])
    left = evaluate(children[0])
    right = evaluate(children[1])
    return left + right if name == "Add" else left * right

cases = [
    ("1+2*3", [("INTEGER", "1"), ("PLUS", "+"), ("INTEGER", "2"), ("STAR", "*"), ("INTEGER", "3")]),
    ("(1+2)*3", [("LPAREN", "("), ("INTEGER", "1"), ("PLUS", "+"), ("INTEGER", "2"), ("RPAREN", ")"), ("STAR", "*"), ("INTEGER", "3")]),
]
for source, tokens in cases:
    concrete = parse(tokens)
    abstract = lower(concrete)
    print(f"source={source}")
    print(f"cst={render(concrete)}")
    print(f"ast={render(abstract)}")
    print(f"value={evaluate(abstract)}")
```

The two CSTs retain punctuation and grammar-layer nodes. The ASTs use only `Int`, `Add`, and `Mul`; parentheses disappear, but their effect survives in nesting. `1+(2*3)` could map to the same AST as `1+2*3`. That many-to-one result is appropriate for evaluation but insufficient for a lossless formatter.

### Parse tree, CST, AST, token tree, and IR

Terminology is not perfectly standardized. In this module, a parse tree is the formal derivation witness. A CST is a practical surface-faithful tree that may compress some grammar artifacts yet retains tokens, punctuation, trivia, errors, and source ranges needed by tools. Tree-sitter, for example, describes its output as a CST and distinguishes named from anonymous token nodes.

An AST is specified by semantic constructors rather than by every grammar production. `If(condition, then_branch, else_branch?)`, `Call(callee, arguments)`, and `Let(pattern, initializer?)` are stable domain nodes. Fields are named; alternatives use explicit constructors; optional and repeated children have declared cardinality; every node carries source provenance or a mapping back to concrete structure.

A token tree groups balanced delimiters without deciding the full expression or statement grammar, useful for macro boundaries. A typed high-level IR may resolve names, insert implicit conversions, or desugar surface forms. A control-flow IR organizes blocks and jumps. These are later abstractions. Calling every tree an AST hides which invariants actually hold.

### Design the abstraction function

Define lowering by cases over accepted concrete productions. For each production, state the AST constructor, child mapping, synthesized values, discarded tokens, span calculation, and diagnostic conditions. Test totality: every accepted non-error CST alternative must lower or be deliberately rejected by a later documented well-formedness check.

Do not let parser-generator helper productions leak into the AST API. Lists such as `ArgTail` should become a field `arguments: [Expr]`. Punctuation can disappear once order and grouping are structural. Preserve exact literal spelling separately when diagnostics, formatting, overflow, macros, or compatibility need it.

Some surface forms desugar: `for` may become iteration protocol calls; compound assignment may become read/operate/write; pattern sugar may expand. Early desugaring reduces later cases but can lose source intent or duplicate evaluation incorrectly. First create an AST that faithfully represents the language construct; perform semantics-preserving desugaring with its own contract and provenance.

AST schema is an interface. Compilers, linters, language servers, formatters, macro tools, indexers, debuggers, serializers, and plugins may consume it. Version constructors and fields, document stability, and avoid serializing implementation-internal node layouts as permanent interchange formats accidentally.

### Separate grammar from contextual validity

Context-free syntax can describe `break;` as a statement but cannot by itself conveniently require an enclosing loop. It can parse an identifier without deciding whether it is declared, parse two declarations without enforcing uniqueness, and parse an assignment without knowing whether its target is mutable. Those belong to binding, static semantics, typing, or other contextual phases.

Some specifications use grammar parameters, semantic predicates, parser feedback, or multiple lexical goals. These can express practical constraints but must be distinguished from the underlying notation. A grammar plus prose/early-error rules often defines the accepted language more accurately than either alone.

Do not postpone basic delimiter or operator structure to arbitrary semantic code, either. Phase placement should give clear ownership, deterministic diagnostics, and reusable representations. PLS-004 develops names and environments; later modules develop static and dynamic semantics.

### Preserve invalid and incomplete source honestly

Batch compilation may stop after a syntax error, but editors parse after every keystroke. Recovery can insert a missing token, delete unexpected input, synchronize at delimiters or statement boundaries, or preserve alternatives. The result is not an ordinary valid parse.

Represent missing, unexpected, skipped, and error regions explicitly with spans and expected-set diagnostics. A lowered partial AST should contain error constructors that later tools treat conservatively. Never execute, refactor, sign, or authorize an error-recovered tree as though the source passed normal grammar.

Recovery must progress: consume input, insert from a bounded budget, close a bounded construct, or stop. Limit nesting, parse-forest size, ambiguity, nodes, diagnostics, lookahead, recursion, and recovery work. Malicious input can otherwise turn syntax services into denial-of-service paths.

Incremental parsing adds a correspondence invariant: parsing the edited text incrementally must yield the same accepted/error structure as a full parse under the same grammar and configuration, modulo documented node identity reuse. Reuse only nodes whose text, context, and grammar state remain valid.

### Verify grammars and representations

Create positive tests for every production and alternative, boundary tests for optional/empty/repeated forms, negative tests for missing/extra/misordered tokens, and shape tests for precedence/associativity. Test entire-input consumption and all start symbols. Known ambiguous strings should be rejected or yield the declared resolution/forest.

Property tests generate derivation-bounded valid sentences and mutate them. Round-trip goals differ: `print(parse(source))` may canonicalize, while a CST byte round trip promises exact recovery. AST pretty-print/reparse should preserve abstract structure under a declared equivalence, not necessarily original text.

Differential tests compare independent parsers or specification examples, but agreement does not prove correctness and shared grammars share defects. Fuzz invalid/truncated/deep/wide inputs. Measure maximum depth, nodes, time and diagnostics. Validate CST→AST totality, spans, trivia ownership, literal spelling, error-node containment, and schema consumers.

Grammar evolution needs compatibility corpora. Adding an alternative can make formerly invalid text valid, change ambiguity, steal tokens from old constructs, alter error recovery, or change AST shapes. Record language version/feature mode in parse evidence. Never silently parse old source under new rules when reproducibility or security requires the original version.

### Security, operations, and high-stakes limits

Parsers process untrusted text. Bound input, token, nesting, repetition, ambiguity, recovery and output tree size. Validate arithmetic in offsets and counts; prevent stack exhaustion; preserve encoding and source provenance; isolate native parser plugins; fuzz; and avoid rendering hostile controls invisibly. Diagnostics and trees can expose source secrets and paths, so govern artifacts.

For safety-critical DSLs, grammar correctness only establishes structural acceptance. Domain vocabulary, units, ranges, cross-field constraints, authority, timing, physical behavior, human factors and deployment validation remain separate. Named language/grammar, parser/toolchain, domain, safety, security/privacy, operations, quality/regulatory, accessibility/human-factors, ethics and independent validation reviewers must approve applicable evidence. No such external review is claimed here.

## Definitions and Notation

- `G=(N,Σ,P,S)`: context-free grammar.
- `N`: nonterminals; `Σ`: terminals, with `N∩Σ=∅`.
- `P`: productions `A→β`, where `A∈N` and `β∈(N∪Σ)*`.
- `S`: designated start symbol.
- `⇒`, `⇒*`: one-step and zero-or-more-step derivation.
- `ε`: empty string, distinct from an end-of-input terminal.
- `L(G)={w∈Σ* | S⇒*w}`: language generated by `G`.
- `yield(t)`: terminal leaves of ordered tree `t`, left to right.
- `T_G`: valid parse trees under `G`; `A`: abstract syntax domain.
- `α:T_G⇀A`: partial abstraction/lowering function with diagnostics outside its accepted domain.
- **nullable**: a nonterminal `A` with `A⇒*ε`.
- **ambiguity witness**: one `w∈L(G)` with two structurally distinct parse trees.
- **provenance**: source/token spans, spelling, version, and concrete correspondence carried through abstraction.

## Mechanisms, Invariants, or Proof Structure

### Grammar proof

State token alphabet, notation semantics, start symbol and productions. For representative accepted sentences, exhibit derivations and trees; for rejected boundaries, identify the first impossible sentential form or explicit policy. Demonstrate ambiguity absence for critical operator forms by grammar structure or preserve declared alternatives.

### Tree-validity proof

Check root/goal, production identity at every internal node, ordered children, terminal yield, complete input consumption, span nesting/coverage, and explicit epsilon/error conventions. For CST claims, check token/trivia/error round trip.

### Abstraction proof

Define `α` for every accepted production, prove constructors receive required operands in order, encode precedence/grouping before discarding punctuation, preserve literal/source provenance, and distinguish normal from recovered input. Use structural induction over concrete trees for local invariants.

### Consumer/compatibility proof

Validate AST schema consumers, pretty-print/reparse equivalence, full/incremental correspondence, resource bounds, historical corpus, grammar versions and negative tests. Diff parse/AST shapes when rules change.

### Claim-boundary proof

Report grammar/notation/version, tokens/start goals, disambiguation, contextual exclusions, recovery/resource limits, tested corpus, tools, unavailable coverage, artifacts and reviewers. Never generalize parse success to type, semantic, domain, security or safety correctness.

## Alternatives and Trade-Offs

| Representation or approach | Strength | Principal limitation |
|---|---|---|
| BNF/CFG | declarative language and derivation model | notation verbosity; ambiguity/parsing properties separate |
| EBNF | concise optionality/repetition/grouping | dialect differences; hides expanded tree shape |
| PEG | deterministic ordered choice and lookahead | order changes meaning; not CFG alternation |
| precedence declarations | compact expression grammar | resolution can be less visible than structural levels |
| generalized parse forest | preserves genuine ambiguity | memory/selection/consumer complexity |
| lossless CST | formatting, refactoring, recovery fidelity | larger, grammar-coupled representation |
| AST | stable semantic constructs and simpler analysis | cannot reconstruct discarded concrete detail |
| token tree | delimiter grouping before full grammar | insufficient for ordinary semantic analysis |
| early desugaring | fewer constructs downstream | loses source intent; correctness burden |
| late desugaring | faithful diagnostics/tooling | more cases across intermediate phases |

## Failure Modes and Misconceptions

- **“A grammar is a parser.”** it defines structure; implementation strategy and errors need more.
- **“EBNF has one universal notation.”** declare the dialect and operator semantics.
- **“Tokens are characters.”** grammar terminals may be categorized lexical elements.
- **“Any derivation difference means ambiguity.”** different expansion orders may yield one tree.
- **“A parser's chosen tree proves the grammar unambiguous.”** the implementation may impose hidden policy.
- **“Precedence comes from arithmetic tradition.”** encode or declare it.
- **“Left recursion means left associativity automatically.”** parser and lowering rules still matter.
- **“Parentheses can be discarded immediately.”** first encode their grouping effect.
- **“CST and parse tree are universal synonyms.”** define practical fidelity and compression.
- **“AST means every tree after parsing.”** constructor invariants determine abstraction level.
- **“ASTs can reproduce source.”** only retained provenance/trivia can support that claim.
- **“Parse success means valid program.”** binding, types, effects and domain rules remain.
- **“Recovery creates a valid AST.”** error provenance must remain explicit.
- **“Nullable repetition is harmless.”** it can cause nonprogress/infinite derivations.
- **“Accepting a prefix is enough.”** full goals require end-of-input.
- **“Generated parsers remove review.”** grammar, conflicts, actions, limits and schemas need evidence.
- **“Two parsers agreeing proves correctness.”** shared specification defects remain possible.
- **“A safe grammar makes a safe DSL.”** domain semantics and system assurance remain.

## Worked Examples

### Example 1

**Derivation.** Under `S→"a" S "b" | ε`, `S⇒aSb⇒aaSbb⇒aabb`. The tree nests one pair per recursive production. **Conclusion:** derivation and tree witness membership of `aabb`.

### Example 2

**Rejection.** The same grammar cannot derive `abab`: after producing the first outer `a`, its matching `b` must be the final terminal. **Conclusion:** production nesting constrains global shape.

### Example 3

**Ambiguity witness.** `n+n*n` under `E→E+E|E*E|n` yields both Add-with-Mul-right and Mul-with-Add-left trees. **Conclusion:** one sentence and two structures prove ambiguity.

### Example 4

**Precedence refactor.** `Expr→Term(+Term)*`, `Term→Factor(*Factor)*` yields `Add(n,Mul(n,n))` only. **Conclusion:** grammar levels encode binding power.

### Example 5

**Associativity.** Left-folding `10-3-2` yields `(10-3)-2=5`; right-folding yields `10-(3-2)=9`. **Conclusion:** repeated operators need explicit fold structure.

### Example 6

**EBNF expansion.** `Args→Expr(","Expr)*` expands to `Args→Expr Tail`, `Tail→"," Expr Tail | ε`. **Conclusion:** compact notation hides helper productions but not language structure.

### Example 7

**CST versus AST.** Both `1+2*3` and `1+(2*3)` may lower to the same AST while CSTs differ in parentheses/trivia. **Conclusion:** abstraction is intentionally many-to-one.

### Example 8

**Contextual rule.** `break;` parses as a statement at top level but later lacks an enclosing loop. **Conclusion:** syntax acceptance and contextual validity have different owners.

### Example 9

**Recovery.** For `f(1,,2)`, a CST records the unexpected comma/error region; lowering does not invent a normal argument. **Conclusion:** tooling can continue without asserting validity.

### Example 10

**Railway movement-authority DSL.** Grammar must distinguish route, signal, point, train, direction, speed, distance, time, unit and configuration tokens; encode precedence/grouping; reject ambiguous or recovered commands before actuation; preserve source/signature/version provenance; and bound parser resources. Named railway signaling/domain, grammar/parser/toolchain, real-time/control, functional-safety/cybersecurity, operations/maintenance, quality/regulatory/certification, human-factors/accessibility, ethics and independent validation reviewers must approve the complete system; none is claimed here. **Conclusion:** an unambiguous parse cannot authorize train movement.

## Cross-Program Connections

- **Compiler implementation:** lexer/parser generators, LL/LR/GLR/PEG algorithms, conflicts and error recovery realize grammar contracts.
- **Theory of computation:** formal languages, closure, pumping, decidability and grammar classes deepen expressiveness analysis.
- **Metaprogramming:** tokens, token trees, CSTs and ASTs define what macros can inspect and transform.
- **Software design:** AST schemas are domain models and long-lived consumer interfaces.
- **Testing:** generators, mutation, differential checks and corpus compatibility verify syntax boundaries.
- **Security:** parser differentials, ambiguity, resource exhaustion and source deception are attack surfaces.
- **Data/API engineering:** schemas and wire grammars also separate structural parsing from domain validation.
- **Editors/tooling:** lossless and incremental trees support highlighting, formatting and refactoring.
- **Formal methods:** derivation and structural induction turn grammar rules into proof cases.
- **Safety engineering:** grammar evidence is one layer beneath domain and system assurance.

## References

1. ISO/IEC, *ISO/IEC 14977:1996 — Syntactic Metalanguage — Extended BNF*, confirmed current in 2023. <https://www.iso.org/standard/26153.html>
2. Noam Chomsky, “Three Models for the Description of Language,” *IRE Transactions on Information Theory*, 1956. <https://chomsky.info/wp-content/uploads/195609-.pdf>
3. Alfred V. Aho et al., *Compilers: Principles, Techniques, and Tools*, second edition, Addison-Wesley, 2007. <https://www.pearson.com/en-us/subject-catalog/p/compilers-principles-techniques-and-tools/P200000003468>
4. Dick Grune and Ceriel J. H. Jacobs, *Parsing Techniques: A Practical Guide*, second edition, Springer, 2008. <https://dickgrune.com/Books/PTAPG_2nd_Edition/>
5. Bryan Ford, “Parsing Expression Grammars: A Recognition-Based Syntactic Foundation,” POPL, 2004. <https://bford.info/pub/lang/peg.pdf>
6. Python Software Foundation, *Python 3.14 Language Reference: Notation*, current documentation; retrieved 2026-08-29. <https://docs.python.org/3/reference/introduction.html#notation>
7. Python Software Foundation, *Python 3.14 `ast` — Abstract Syntax Trees*, current documentation; retrieved 2026-08-29. <https://docs.python.org/3/library/ast.html>
8. Rust Project, *The Rust Reference: Grammar Notation*, current documentation; retrieved 2026-08-29. <https://doc.rust-lang.org/stable/reference/notation.html>
9. Ecma International, *ECMAScript 2026 Language Specification: Syntactic Grammar*, current draft; retrieved 2026-08-29. <https://tc39.es/ecma262/#sec-syntactic-grammar>
10. Tree-sitter Project, *Basic Parsing: Named and Anonymous Nodes*, current documentation; retrieved 2026-08-29. <https://tree-sitter.github.io/tree-sitter/using-parsers/2-basic-parsing.html>

## Exercises

### Exercise 1

For `S→"(" S ")" S | ε`, give a leftmost derivation and parse tree for `()()`, state its yield, and explain whether changing to a rightmost derivation necessarily changes the tree.

### Exercise 2

Prove ambiguity of `E→E"-"E | INTEGER` with one sentence. Then design an unambiguous left-associative EBNF grammar and show the AST/value for `10-3-2`.

### Exercise 3

Design CST and AST schemas for function calls with optional type arguments, positional/named arguments, trailing commas, comments and missing-token recovery. State the lowering and round-trip contracts.

### Exercise 4

Create a grammar-verification plan for adding a pipeline operator `|>` to a language that already has `|`, `||`, lambdas, patterns and comparisons. Include lexical, ambiguity, precedence, AST, recovery, compatibility, security and resource evidence.

### Exercise 5

Transfer the chapter to a clinical medication-order DSL. Specify grammar, concrete/abstract representations, units/contextual validation, error handling, security, evidence and named human reviewers without claiming clinical authorization.

## Answers to the Exercises

### Answer 1

Let the terminals be parentheses. A leftmost derivation is `S⇒(S)S⇒()S⇒()(S)S⇒()()S⇒()()`. A tree has root `S`; its first production creates `(`, an epsilon `S`, `)`, and a continuation `S`; that continuation repeats the same production and ends with epsilon. Reading terminal leaves gives `()()`. A rightmost derivation can expand the continuation before the nested `S`, but for this chosen production structure it can still witness the same tree. Derivation step order alone is not an ambiguity witness; ambiguity requires two distinct trees for one yield. Check every internal child sequence against one production and the root against the intended whole-input goal.

### Answer 2

`10-3-2` has two trees under the original grammar: `Sub(Sub(Int(10),Int(3)),Int(2))` and `Sub(Int(10),Sub(Int(3),Int(2)))`; their values are 5 and 9, so the grammar is ambiguous. Use `Expr→INTEGER ("-" INTEGER)*` and specify that lowering folds the repeated pairs left. The CST retains `10`, `-`, `3`, `-`, `2`; lowering starts `Int(10)`, produces `Sub(Int(10),Int(3))`, then `Sub(Sub(Int(10),Int(3)),Int(2))`, value 5. EBNF repetition alone describes a sequence; the explicit lowering fold establishes associativity for the AST consumer.

### Answer 3

The CST `Call` owns callee, optional `<` type-argument list `>`, `(`, separated argument items, optional trailing comma, `)`, all trivia/comments, exact tokens/spans and `Missing`/`Unexpected` nodes. Each argument CST distinguishes positional expression from `name = expression`; separators and comments remain independently anchored. The AST is `Call(callee, type_args[], args[], span)` with `Positional(expr)` and `Named(name,expr)` constructors; punctuation/trivia move to provenance rather than semantic children. Lowering rejects or propagates any recovery node, checks that positional-after-named policy in the appropriate contextual phase, preserves argument order and literal/name spans, and never invents an expression. CST byte slices round-trip exactly; AST pretty-print/reparse promises equivalent `Call` structure under canonical formatting, not original comments or commas. Schema versions and source mappings are explicit.

### Answer 4

Lexically verify maximal munch makes `|>` one token without changing `|`/`||` boundaries, comments or patterns. Define operand categories, precedence relative to comparisons/lambdas/logical operators, and associativity; enumerate short mixed expressions and use conflict/ambiguity tools plus hand-derived trees. Add a distinct `Pipeline(left,right)` AST or documented desugaring that evaluates operands exactly once in the required order. Test missing operands, chained operators, line breaks, delimiters and recovery nodes without silently reinterpreting invalid text. Parse the historical corpus under old/new versions; identify formerly invalid text that becomes valid and old diagnostics/tree changes. Fuzz every token prefix, deep chains and adversarial nesting with time/node/diagnostic limits. Compare independent implementation and specification examples, run AST consumer tests/pretty-print equivalence, review injection or misleading-rendering risks, pin feature/version mode, and preserve unavailable platform/tool coverage. A zero-conflict parser report alone is not semantic or compatibility proof.

### Answer 5

Use a versioned UTF-8 lexical profile and grammar with explicit productions for patient/order identifiers, coded medication, route, dose quantity, unit, frequency/rate, duration, start/stop conditions, comments and signatures. Reserve unambiguous ASCII structural delimiters; encode decimal and unit attachment precisely; forbid implicit precedence between dose, rate and duration. A lossless CST retains spelling, comments, signatures, source/version and error nodes; an AST uses constructors such as `MedicationOrder(subject, medication_code, dose, route, schedule, provenance)` with typed quantity/unit syntax but does not assert clinical validity. Contextual phases validate authorization, patient/medication identity, formulary, unit dimensions/conversions, ranges, allergies/interactions, timing and device capability against authoritative versioned data.

Reject incomplete or recovered syntax before ordering or actuation; never autocorrect a drug or unit silently. Bound text, numeric digits, nesting, alternatives and diagnostics; test confusables, decimal separators, `mg`/`mcg`, missing fields, duplicate/contradictory clauses, hostile input, parser differentials, round trips, historical versions and end-to-end fail-safe behavior. Authenticate/sign and audit source/AST transitions, protect patient data, and isolate parser artifacts. Named pharmacy, prescribing, nursing, medication-safety, clinical-informatics/terminology/units, grammar/parser/toolchain, device/integration, cybersecurity/privacy, quality/regulatory, human-factors/accessibility/localization, ethics and independent clinical/technical validation reviewers must approve the full system. No external review, clinical validity, regulatory approval or authorization to prescribe/administer is claimed.
