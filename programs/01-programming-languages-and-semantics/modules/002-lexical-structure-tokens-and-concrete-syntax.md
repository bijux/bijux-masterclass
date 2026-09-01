---
module_id: PLS-002
program: Programming Languages & Semantics
level: 1
module_number: 2
title: Lexical Structure, Tokens, and Concrete Syntax
status: complete
last_verified: 2026-08-29
---

# Lexical Structure, Tokens, and Concrete Syntax

## One-Page Review

### Governing question

How does a language turn encoded source text into a reproducible sequence of lexical elements without confusing characters, tokens, concrete spelling, and abstract program structure?

### Essential definitions

- A **source encoding** maps bytes or code units to source characters. Decoding precedes ordinary lexical classification and can itself fail.
- A **source character** is an element of the language's specified source-text domain, often Unicode code points after prescribed line-ending or encoding treatment.
- A **lexical grammar** states how source characters form lexical elements such as identifiers, keywords, literals, operators, delimiters, whitespace, comments, and line terminators.
- A **token** is a categorized lexical element supplied to later syntactic analysis. A token commonly carries a kind, its original **lexeme**, a source **span**, and possibly a decoded or normalized value.
- A **lexeme** is the concrete source substring recognized for one token; token kind `INTEGER` and lexeme `0xff` are different information.
- **Trivia** is concrete material such as whitespace or comments that may not affect the core grammar but remains important for source fidelity, documentation, diagnostics, and tools.
- **Concrete syntax** is the exact surface form admitted by the language, including spelling, punctuation, delimiters, layout, and sometimes trivia. Abstract syntax intentionally forgets some of it.
- **Longest match** or **maximal munch** selects the longest available legal lexical element at the current position, with a specified priority rule when several kinds match equally.
- A **lexical mode** is scanner state that changes which token rules apply, such as normal code, string content, interpolation, or nested-comment context.
- A **lexical error** occurs when source cannot be decoded or no permitted token/trivia rule accounts for the next required input under the current state.

### Central model, mechanism, or theorem

Let $B$ be source bytes, $C^*$ decoded source-character sequences, and $T^*$ token sequences. A front end begins with a partial decoding function and a partial or diagnostic-producing lexical function:

$$
decode_E:B^*\rightharpoonup C^*,
\qquad
lex_L:C^*\rightharpoonup T^*.
$$

For each token $t_i=(k_i,x_i,[a_i,b_i),v_i)$, its kind $k_i$, lexeme $x_i$, half-open source span, and interpreted value $v_i$ serve different consumers. A complete concrete source view may preserve trivia separately so that concatenating source slices in span order reproduces the decoded input. The parser consumes token distinctions; it does not recover discarded spelling automatically.

### Critical invariants

Encoding and Unicode version are explicit. Token spans cover source monotonically without silent overlap or loss, except transformations the language specifies and records. Longest-match and priority rules are deterministic or ambiguity is reported. Keyword policy distinguishes reserved, contextual, and ordinary identifiers. Literal spelling is preserved separately from value. Whitespace, comments, line terminators, and indentation follow language rules rather than folklore. Normalization and confusable handling are explicit. Invalid characters, unterminated constructs, overflow boundaries, and mode transitions produce bounded diagnostics. Tooling never claims lossless rewriting from a representation that discarded required trivia.

### Common failures

Implementers split on whitespace; equate bytes, code units, code points, and displayed characters; use host regular-expression defaults as the language definition; match `=` before `==`; classify keywords without compatibility policy; normalize identifiers silently and lose spelling; parse numeric values during lexing and discard overflow evidence; drop comments before a formatter or refactoring; treat indentation as irrelevant; assume every token rule is regular; forget end-of-input tokens; accept control or bidirectional characters invisibly; or test only ASCII and well-formed literals.

### Compact example

For `let total_2=41+1`, a simple language might emit `KEYWORD(let)`, `IDENT(total_2)`, `ASSIGN(=)`, `INTEGER(41)`, `PLUS(+)`, `INTEGER(1)`. Removing spaces does not merge tokens here because punctuation bounds them. In contrast, `letx` is one identifier under longest match, not `let` followed by `x`. The language—not visual intuition—decides both outcomes.

### Connections

The previous module separated text from behavior. The next module consumes tokens through grammars and distinguishes parse trees from abstract syntax. Compiler construction implements industrial scanners and parsers. Metaprogramming may preserve token trees and trivia. Security engineering studies source deception and supply-chain review. Unicode, editor, formatter, refactoring, and language-server behavior all depend on the lexical contract.

## Governing Question

What must be specified so that two conforming tools agree on the lexical elements in the same source text and can explain any disagreement at an exact location?

The answer includes more than token names. It includes input encoding, character repertoire, Unicode version, line handling, token definitions, precedence among definitions, longest-match behavior, comments and whitespace, literal boundaries, identifier normalization, lexical modes, synthesized layout tokens, end-of-input behavior, and recovery. Without those rules, downstream syntax and semantics are built on an unstable stream.

## Why This Matters

Every compiler, interpreter, formatter, syntax highlighter, refactoring tool, macro system, language server, linter, security scanner, and code-review interface begins with some model of source structure. If those models disagree, a file can look safe to one participant and mean something else to another. A formatter can delete comments, a highlighter can color a sequence as a string while the compiler sees code, or an editor can place a diagnostic on the wrong character because it counts UTF-16 code units while the compiler reports UTF-8 bytes.

Lexical design also affects language evolution. Reserving every plausible future keyword prevents useful names. Adding a two-character operator can change old token boundaries. Changing Unicode versions can admit new identifier characters. Extending numeric suffixes can turn a formerly invalid token into a valid one. Treating `match` as a contextual keyword can preserve programs that already use `match` as an identifier, but it moves classification into syntactic context.

Security begins at this boundary. Unicode enables programmers to name concepts in their own scripts, but visually confusable characters, mixed scripts, invisible formatting controls, bidirectional display, and normalization differences can mislead reviewers or cause tools to disagree. Unicode Standard Annex #31 supplies identifier properties and profiles; UAX #15 defines normalization; Unicode Technical Standard #39 defines security mechanisms such as confusable detection. Each language still chooses and versions its profile.

Lexical rules are semantic infrastructure even though tokens do not yet execute. If `1..2` becomes `FLOAT(1.) DOT INTEGER(2)` in one implementation and `INTEGER(1) RANGE INTEGER(2)` in another, the parser receives different programs. Deterministic, documented tokenization is a precondition for every later meaning claim.

## Prerequisites and Retrieval

Retrieve finite strings, sets, sequences, functions, regular expressions, finite-state machines, Unicode code points, half-open intervals, and basic source control. Know that UTF-8, UTF-16, and Unicode are related but not interchangeable concepts. Be able to distinguish text displayed by an editor from its encoded representation. Parsing theory beyond simple grammar notation is not required; PLS-003 owns that development.

## Learning Objectives

By the end of this module, you should be able to:

1. trace source bytes through decoding, source-character processing, lexical elements, tokens, and parser input;
2. distinguish token kind, lexeme, source span, normalized spelling, and interpreted value;
3. apply longest-match and priority rules to overlapping token definitions;
4. explain keyword, contextual-keyword, whitespace, comment, line, indentation, and end-marker policies;
5. design lexical states for strings, interpolation, raw delimiters, and comments;
6. identify where regular-language scanners suffice and where state, nesting, or parser feedback is required;
7. preserve concrete syntax and trivia for diagnostics and source-to-source tools;
8. evaluate Unicode identifier, normalization, confusable, and display-security choices; and
9. verify a bounded lexer while distinguishing executable examples from language-wide correctness or high-stakes safety.

## Core Exposition

Source often arrives as bytes, but language specifications choose different entry points. Python determines an encoding, UTF-8 by default, and decodes source before tokenization. ECMAScript specifies source text in terms of Unicode code points with its own treatment of source characters. Rust source is UTF-8 and its reference defines token productions using Unicode properties. A front end must name its actual unit; byte offsets, Unicode scalar-value indices, UTF-16 code-unit positions, and displayed grapheme columns can all differ.

Decoding failure is not an identifier error. It occurs before a legal character stream exists. Byte-order marks, encoding declarations, line-ending normalization, forbidden NUL, and ill-formed byte sequences need explicit rules. Tools should retain a mapping from normalized source positions to original storage positions when diagnostics or rewriting require it.

The lexical analyzer scans the decoded source and emits lexical elements. Common token kinds include identifiers, keywords, numeric/string/character literals, operators, punctuation, delimiters, and layout markers. Whitespace and comments may be discarded, placed on a trivia channel, attached to adjacent tokens, or emitted as tokens. The choice is part of the consumer contract.

A token is not merely its text. `INTEGER("0010")` preserves spelling, while its semantic numeric value might be ten, eight under a legacy rule, invalid because leading zeros are prohibited, or too large for a later target type. Keeping kind, lexeme, span, and optionally a cautiously decoded value lets later stages issue accurate errors and tools reproduce source. Collapsing everything to the integer ten loses information.

Spans are commonly half-open intervals $[a,b)$: a token covers positions starting at $a$ up to but not including $b$. Adjacent tokens can satisfy $b_i=a_{i+1}$ when no trivia intervenes. A complete lossless tokenization includes trivia or gaps so every source position is accounted for. Diagnostics need line/column projections, but the primary offset unit must be declared. “Column 8” is ambiguous under tabs, combining marks, wide characters, and UTF-16-based protocols.

Many token classes are regular languages and can be recognized by finite automata. A simplified ASCII identifier might begin with a letter or underscore and continue with letters, digits, or underscores; a decimal integer might contain one or more decimal digits. Scanner generators such as POSIX `lex` compile regular-expression rules into an analyzer. This theory explains fast left-to-right recognition, but a production scanner also handles rule priority, modes, Unicode tables, diagnostics, and constructs that exceed one flat regular language.

Overlapping rules require a policy. Under longest match, `total_2` is one identifier rather than `total`, `_`, `2`; `==` is one operator when both `=` and `==` are legal; and `123e4` may be one floating literal rather than integer, identifier, and integer. When two rules match the same longest substring, declaration priority or an explicit category rule chooses. A language specification should not leave this to hash-table order.

Keywords interact with identifiers. A common technique scans the longest identifier-like lexeme, then maps exact reserved spellings such as `let` to keyword kinds. Hard keywords can never be identifiers. Contextual or soft keywords remain identifier-like tokens until the parser recognizes a specific context; Python's `match`, `case`, and `type` illustrate compatibility-motivated soft keywords. Some languages offer escaped or raw identifiers so a keyword spelling can be used as a name. Each choice affects evolution, tools, and error messages.

Whitespace is sometimes trivia and sometimes syntax. Even when discarded, it separates tokens: `ab` and `a b` differ. Newlines can terminate statements, enable automatic semicolon insertion, or remain ordinary spacing inside delimiters. Python converts indentation changes into `INDENT` and `DEDENT` tokens using a stack and distinguishes physical from logical lines. Haskell-style layout and shell here-documents introduce other state. “Ignore whitespace” is therefore only a scoped rule.

Comments also require precision. A line comment usually ends at a line terminator unless inside a string. Block comments may or may not nest. Documentation comments can be trivia, tokens, or syntax transformed into attributes. A comment-like sequence inside a literal is data. Removing comments before retaining spans can join tokens: deleting the comment from `a/**/b` yields `ab`, which may be a different identifier rather than two identifiers. A safe preprocessor preserves separation and position mapping.

Literal recognition needs modes and boundary rules. A quote begins a string mode in which spaces, operator characters, and comment markers lose their ordinary role. Escapes change how a following character is interpreted. Raw strings choose another terminator discipline. Interpolated strings alternate between text and expression modes, sometimes recursively. Unterminated strings need a diagnostic whose recovery point does not consume the rest of a project unpredictably.

Numeric literals are a dense boundary. Prefixes choose radix; separators improve readability; decimals and exponents overlap dots and signs; suffixes can name types; and a leading minus is often a separate operator token rather than part of a literal. The lexer may validate lexical form while leaving range, type, and constant evaluation to later semantics. This permits an unsigned magnitude to be lexically valid even when a particular typed use overflows.

Delimiters such as parentheses, brackets, and braces can be emitted individually. Token-tree systems additionally group balanced delimiters into trees before or during macro processing. Grouping is more than flat lexing because it tracks nesting, but it remains concrete structure: one token tree can contain many tokens without yet resolving expression grammar or bindings. The legacy corpus's Rust macro material correctly treats `tt` fragments as grouped lexical structure, not evaluated values.

Some boundaries are context-sensitive. ECMAScript distinguishes division punctuators from regular-expression literals using lexical goal symbols selected by syntactic context. C++ has historically had tokenization and template-angle interactions. Interpolation switches modes. Scannerless parsers avoid a separate token stream and apply grammar directly to characters. These cases do not invalidate lexical reasoning; they require the interface between lexical and syntactic context to be explicit.

Unicode identifiers cannot be specified as “any letter” without a version and profile. UAX #31 defines stable properties such as `XID_Start` and `XID_Continue` and permits language-specific profiles. Combining marks complicate display and position. UAX #15 defines NFC, NFD, NFKC, and NFKD normalization. Python normalizes identifiers to NFKC during parsing, while other languages make different choices. Normalizing source globally would corrupt literals and comments; identifier treatment must be scoped.

Canonical equivalence and visual confusability differ. Two sequences can be canonically equivalent yet encoded differently. Two unrelated code points can look alike. UTS #39 supplies confusable and mixed-script mechanisms, but rejecting every non-ASCII identifier is not a universal solution: it excludes legitimate languages and still leaves ASCII names that humans confuse. A language or organization should choose a transparent profile, warn or reject according to risk, preserve original spelling, and make invisible controls inspectable.

Concrete syntax preservation matters beyond compilation. A compiler may discard comments and exact whitespace after producing tokens because semantics no longer needs them. A formatter, codemod, merge tool, or refactoring engine may require a concrete syntax tree or lossless token stream with trivia. It must preserve comments, directives, raw literal spellings, line endings, and error nodes or explicitly document canonical reformatting. An abstract syntax tree cannot reconstruct information it never retained.

Incremental tools add identity and recovery. Editing one character should not necessarily rescan a million-line file. A lexer can restart from safe boundaries with cached mode state, but multi-line strings, nested comments, layout stacks, and preprocessor state can expand the affected region. Correctness precedes speed: incremental output must match full lexing for the same language state, or the editor and compiler will disagree.

Lexical diagnostics should state the unexpected source slice, its span and encoding unit, current mode, expected closing delimiter or legal class, and a bounded recovery. Reject overlong tokens and pathological nesting under documented resource limits. Fuzz invalid encodings, truncated escapes, enormous literals, mixed newlines, comments at end of file, every operator prefix, Unicode boundaries, and edits around cached restart points.

The executable scanner below recognizes a deliberately tiny ASCII subset using explicit longest identifier/integer consumption. It preserves kind and lexeme and reconstructs a canonical spaced form.

<!-- bijux-verify: {"id":"tiny-lexical-structure-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"token_count=6\nkinds=KEYWORD,IDENT,ASSIGN,INTEGER,PLUS,INTEGER\nlexemes=let|total_2|=|41|+|1\nreconstructed=let total_2 = 41 + 1\n","stderr":""}} -->
```python
source = "let total_2=41+1"
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
digits = "0123456789"
tokens = []
index = 0

while index < len(source):
    character = source[index]
    if character in " \t\n":
        index = index + 1
    elif character in letters:
        start = index
        index = index + 1
        while index < len(source) and source[index] in letters + digits:
            index = index + 1
        lexeme = source[start:index]
        kind = "KEYWORD" if lexeme == "let" else "IDENT"
        tokens = tokens + [(kind, lexeme)]
    elif character in digits:
        start = index
        index = index + 1
        while index < len(source) and source[index] in digits:
            index = index + 1
        tokens = tokens + [("INTEGER", source[start:index])]
    elif character == "=":
        tokens = tokens + [("ASSIGN", character)]
        index = index + 1
    elif character == "+":
        tokens = tokens + [("PLUS", character)]
        index = index + 1
    else:
        raise ValueError("unsupported source character")

kinds = ""
lexemes = ""
reconstructed = ""
for kind, lexeme in tokens:
    kinds = kinds + ("," if kinds else "") + kind
    lexemes = lexemes + ("|" if lexemes else "") + lexeme
    reconstructed = reconstructed + (" " if reconstructed else "") + lexeme

assert reconstructed == "let total_2 = 41 + 1"
print(f"token_count={len(tokens)}")
print(f"kinds={kinds}")
print(f"lexemes={lexemes}")
print(f"reconstructed={reconstructed}")
```

Execution establishes only the encoded ASCII rules for one input. It does not support Unicode, comments, strings, indentation, overlapping multi-character operators, modes, recovery, resource limits, incremental edits, a parser, language semantics, security review, or correctness for arbitrary source.

## Definitions and Notation

Let $C$ be source characters, $K$ token kinds, and $X=C^*$ lexemes. A token is $t=(k,x,s,v)\in K\times X\times Span\times Value_\bot$, where $s=[a,b)$ and $v$ may be absent. A token stream is $\tau=t_1\ldots t_n$. Trivia stream $\rho$ records non-token source elements when needed.

For lexical rule $R_j\subseteq C^*$, define matches at position $p$ as legal prefixes of the remaining input. Longest match selects a member with maximum length; priority $j$ resolves equal length. The scanner must either advance $p$, reach end of input, or report a diagnostic. A zero-length rule in a repetition can violate progress and cause nontermination.

A source map $M$ relates transformed or normalized positions to original storage positions. A lexical mode $m\in Modes$ changes the active rule set and transition function. A **token value** is a convenience interpretation, while the lexeme remains authoritative evidence of concrete spelling. An **end marker** is a synthesized token identifying exhaustion and permitting later grammars to close layout or report unexpected end.

## Mechanisms, Invariants, or Proof Structure

Use this lexical-design chain:

1. **Specify source representation.** Encoding, BOM, forbidden sequences, Unicode version, line endings, and offset units.
2. **Partition lexical elements.** Token kinds, trivia, directives, layout markers, and end marker.
3. **Define recognition.** Rule languages, longest match, priority, boundaries, keyword policy, and modes.
4. **Preserve evidence.** Original lexeme, spans, trivia, normalized/decoded values, and source mapping appropriate to consumers.
5. **State progress.** Every successful rule consumes input or makes a bounded state transition; recovery also advances or stops.
6. **State context interfaces.** Parser-selected lexical goals, interpolation transitions, preprocessing, or scannerless integration.
7. **Design diagnostics.** Exact slice, expected class/delimiter, mode, location unit, safe recovery, and resource bound.
8. **Verify properties.** Golden streams, rule-boundary tables, differential/full-versus-incremental checks, fuzzing, round trips, and security profiles.

Proof obligations include coverage of every admitted character in each mode; deterministic tie resolution; monotonic spans; termination by decreasing remaining input or bounded state; correct recognition of every operator prefix; and, for lossless tools, reconstruction of source from ordered tokens and trivia. A generated scanner can prove none of these merely by compiling; rule interaction and language conformance remain review obligations.

## Alternatives and Trade-Offs

**Handwritten scanners** provide precise control, state, error recovery, and performance, but demand disciplined tests. **Generated scanners** derive efficient automata from declarative rules and can expose conflicts, but generator priority and host regex semantics become part of the build unless pinned and documented. **Parser combinators or scannerless parsing** unify character and grammar logic but can complicate whitespace policy, performance, and tooling boundaries.

**Discarded trivia** minimizes compiler memory and simplifies semantic trees. **Lossless tokens/CSTs** support formatting, refactoring, and exact diagnostics at greater storage and update cost. A compiler and IDE can maintain different representations only if they share conformance tests.

**Hard keywords** simplify parsing and diagnostics but consume namespace and complicate evolution. **Contextual keywords** preserve compatibility but require parser cooperation and context-aware tooling. **Escaped identifiers** provide an exit while adding spelling and display complexity.

**ASCII identifiers** are simple and reduce some confusable risks but exclude legitimate scripts. **Unicode profiles** improve expressiveness and inclusion while requiring versioning, normalization, display, security, and tool consistency. **Normalization** can make equivalent spellings equal but can collapse distinctions; preserving original lexemes remains important.

## Failure Modes and Misconceptions

- **“Lexing is splitting on whitespace.”** Punctuation, operators, strings, comments, layout, and adjacent tokens require language rules.
- **“A character is one byte or one screen column.”** Encodings, code units, combining marks, tabs, and grapheme display differ.
- **“Regular expressions define the whole lexer.”** Modes, nesting, indentation, parser feedback, preprocessing, and diagnostics add state.
- **“Longest match needs no priority.”** Equal-length matches such as keyword and identifier still require classification.
- **“Keywords are always separate rules.”** Many scanners recognize an identifier first and classify its exact lexeme afterward.
- **“Whitespace never matters in brace languages.”** It can separate tokens, terminate comments, affect directives, or trigger semicolon rules.
- **“Comments can be deleted safely.”** Deletion can join tokens, destroy documentation, shift spans, or break source tools.
- **“The numeric value is the token.”** Spelling, radix, separators, suffix, range, and later type context remain distinct.
- **“Unicode normalization prevents confusables.”** Canonical/compatibility equivalence and visual confusability are separate problems.
- **“Syntax highlighting proves compiler interpretation.”** The editor may implement a different or incomplete lexer.
- **“An AST can reproduce source.”** Not if punctuation, comments, spelling, or layout were discarded.
- **“Recovery may skip until something works.”** Unbounded skipping hides errors and destabilizes later diagnostics.

## Worked Examples

### Example 1

**Question:** How should `ifx` be tokenized when `if` is a keyword?

**Reasoning:** The identifier rule matches all three characters and longest match beats the shorter keyword spelling. Exact post-classification finds `ifx` is not `if`.

**Conclusion:** It is one identifier, not keyword `if` followed by identifier `x`.

### Example 2

**Question:** What happens if rules test `=` before `==` and accept the first match?

**Reasoning:** `==` incorrectly becomes two assignment tokens. Longest match should select the two-character operator, or rule logic must explicitly check it first.

**Conclusion:** Rule order without a declared longest-match policy is brittle.

### Example 3

**Question:** Are `10`, `0xa`, and `1_0` the same token?

**Reasoning:** They may share numeric value ten under a language, but have different lexemes, radix or separator forms, spans, and possibly token subkinds. Source tools must preserve those differences.

**Conclusion:** Token value never replaces concrete spelling.

### Example 4

**Question:** Can a compiler delete `/* units */` from `dose/* units */mg` before lexing?

**Reasoning:** Direct deletion yields `dosemg`, possibly one identifier. Treat the comment as separating trivia or preserve an equivalent boundary and source map.

**Conclusion:** Comment handling participates in token boundaries.

### Example 5

**Question:** Why does Python emit `INDENT` and `DEDENT` instead of discarding leading spaces?

**Reasoning:** Indentation groups statements. A stack compares logical-line indentation and synthesizes layout tokens, while indentation inside joined lines follows different rules.

**Conclusion:** Layout can be lexical structure consumed by the parser.

### Example 6

**Question:** Is `/ab+/g` always a regular-expression literal in ECMAScript source?

**Reasoning:** Slash can begin a regex literal or be division punctuation. ECMAScript uses lexical goals selected by syntactic context.

**Conclusion:** Some languages make the lexer-parser interface context-sensitive.

### Example 7

**Question:** Do two canonically equivalent Unicode identifier spellings necessarily have the same source bytes or display width?

**Reasoning:** No. Normalization can map different code-point sequences to an equivalent form, while original bytes, spans, and grapheme behavior differ. The language decides identifier equality.

**Conclusion:** Preserve spelling and version the normalization/profile rule.

### Example 8

**Question:** Can a formatter operate from an AST that omitted comments and parentheses?

**Reasoning:** It can generate a canonical program only if semantics and required grouping are recoverable, but it cannot place lost comments or preserve exact intentional parentheses. A lossless CST/token layer is needed for faithful edits.

**Conclusion:** Representation choice follows the source-preservation contract.

### Example 9

**Question:** A medication-order DSL accepts `dose=1Omg`, where the second character is Latin capital `O`, not zero. Can ordinary token tests establish safety?

**Reasoning:** No. The lexical profile should reject or clearly diagnose confusable unit/number spellings, but clinical meaning, unit vocabulary, decimal conventions, display, transcription, locale, dose limits, workflow, and device integration require named pharmacists, prescribers, nurses, clinical informaticians, medication-safety and human-factors specialists, accessibility/localization experts, security engineers, regulators, and independent clinical/technical reviewers. No external review is claimed.

**Conclusion:** Lexical correctness is necessary but cannot authorize clinical language use.

### Example 10

**Question:** When should a lexer stop after an unterminated string?

**Reasoning:** The language and tool mode decide. A batch compiler may report through end of logical construct; an IDE may synthesize a bounded error token at newline or file end. Recovery must guarantee progress and preserve later evidence.

**Conclusion:** Error recovery is part of the lexical contract, not an afterthought.

## Cross-Program Connections

[Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) builds scanners, parsers, source maps, error recovery, and incremental front ends. [Theory of Computation and Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) formalizes regular languages, automata, grammars, and complexity.

[Metaprogramming](../../06-programming-languages-metaprogramming/ROADMAP.md) consumes token streams and token trees while preserving staging and hygiene boundaries. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies fuzzing, differential, property, mutation, and regression methods for lexical implementations.

[Security Engineering](../../25-security-engineering/ROADMAP.md) studies source deception, malicious input, resource exhaustion, supply-chain review, and tool disagreement. [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) constrains domain-specific vocabularies whose lexical choices can create or prevent ambiguity.

## References

- Unicode Consortium, [Unicode Standard Annex #31: *Unicode Identifiers and Syntax*](https://www.unicode.org/reports/tr31/), Unicode 17.0.0, revision 43, 2025. Current identifier properties, profiles, normalization guidance, and stability rules.
- Unicode Consortium, [Unicode Standard Annex #15: *Unicode Normalization Forms*](https://www.unicode.org/reports/tr15/), Unicode 17.0.0, 2025. Normative NFC, NFD, NFKC, and NFKD framework.
- Unicode Consortium, [Unicode Technical Standard #39: *Unicode Security Mechanisms*](https://www.unicode.org/reports/tr39/), Unicode 17.0.0, revision 32, 2025. Identifier profiles, confusable detection, and mixed-script mechanisms.
- Python Software Foundation, [*The Python Language Reference: Lexical Analysis*](https://docs.python.org/3/reference/lexical_analysis.html), Python 3.14.7 documentation, retrieved 2026-08-29. Encoding, lines, indentation, tokens, longest match, identifiers, literals, and Unicode normalization.
- Rust Project, [*The Rust Reference: Tokens*](https://doc.rust-lang.org/reference/tokens.html), current online reference, retrieved 2026-08-29. Token categories, lexical productions, Unicode identifiers, literals, punctuation, delimiters, and reserved forms.
- Ecma International TC39, [*ECMAScript Language Specification: Lexical Grammar*](https://tc39.es/ecma262/multipage/ecmascript-language-lexical-grammar.html), living specification, retrieved 2026-08-29. Longest input elements, lexical goals, comments, identifiers, literals, templates, and punctuators.
- The Open Group, [*POSIX.1-2024 `lex` Utility*](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/lex.html), IEEE Std 1003.1-2024 / Issue 8. Standard scanner-generator model, regular-expression rules, rule priority, and longest matching.
- Alfred V. Aho, Monica S. Lam, Ravi Sethi, and Jeffrey D. Ullman, [*Compilers: Principles, Techniques, and Tools*, second edition](https://www.pearson.com/en-us/subject-catalog/p/compilers-principles-techniques-and-tools/P200000003468), Addison-Wesley, 2007. Canonical automata-based lexical analysis, input buffering, and syntax-analysis foundation.

## Exercises

### Exercise 1

Tokenize `let ifx=10==0x0a` under an ASCII language with identifiers, hard keyword `let`, decimal/hex integers, `=`, and `==`. Show every candidate boundary, longest-match decision, kind, lexeme, and half-open span.

### Exercise 2

Design lexical modes for ordinary code, quoted strings, raw strings with variable delimiters, interpolation, line comments, and nested block comments. State progress and recovery invariants for truncated input.

### Exercise 3

Specify a Unicode identifier profile for a new language. Address encoding, Unicode version, start/continue properties, underscore, normalization, original spelling, scripts, confusables, bidirectional controls, compatibility, diagnostics, and upgrades.

### Exercise 4

Design a lossless token representation for a formatter and incremental language server. Include tokens, trivia, byte/code-point/UTF-16 mappings, modes, error tokens, stable identities, round-trip and full-versus-incremental properties.

### Exercise 5

A hospital infusion-protocol DSL includes drug names, decimal doses, units, rates, durations, comments, and localized identifiers. Define its lexical safety profile, ambiguity tests, resource limits, diagnostics, integration evidence, and named human review required before clinical use.

## Answers to the Exercises

### Answer 1

With zero-based half-open character spans: `let` at `[0,3)` first matches the identifier pattern and is post-classified as `KEYWORD`; one space is trivia `[3,4)`; `ifx` `[4,7)` is one `IDENT` because longest match beats keyword-like prefix `if`; `=` `[7,8)` is `ASSIGN`; `10` `[8,10)` is `DECIMAL`; `==` `[10,12)` is `EQUAL` rather than two assignment tokens; `0x0a` `[12,16)` is `HEX_INTEGER` when the radix rule consumes the full legal prefix and digits. Candidate checks at `0` include identifier lengths one through three, choosing three. At `4`, lengths one through three choose three. At `7`, `==` does not match because only one `=` follows. At `10`, both `=` and `==` match, so length two wins.

The resulting significant stream is `KEYWORD(let) IDENT(ifx) ASSIGN(=) DECIMAL(10) EQUAL(==) HEX_INTEGER(0x0a) EOF`. Retain trivia and spans for round trip. If the hex rule required at least one hexadecimal digit after `0x`, `0x` alone would be a lexical error or a different sequence according to an explicitly chosen policy; never let a host integer parser decide boundaries implicitly.

### Answer 2

Normal mode recognizes identifiers, literals, punctuation, whitespace, comment openers, string openers, and interpolation-independent tokens. Quoted-string mode consumes text and escapes until the matching quote; interpolation opener pushes expression mode, which tracks nested delimiters and returns at its matching close. Raw-string mode records the opener's delimiter count and scans until the exact corresponding terminator. Line-comment mode ends at a defined line terminator. Nested block-comment mode holds a positive depth, incrementing on opener and decrementing on closer.

Every loop either consumes at least one source unit, pushes/pops a bounded mode while consuming its delimiter, reports end of input, or emits a diagnostic and stops/advances. Bound delimiter length, comment/interpolation nesting, token length, and diagnostic count. At truncated input, emit an error token from opener to recovery boundary, identify expected terminator and opening span, preserve consumed text, and unwind modes deterministically. An IDE can recover at a logical line or end marker only if full lexing of the recovered model is specified; a batch compiler can stop. Test every opener prefix, escapes before end, nested pairs, false terminators, empty content, and edits that change delimiter counts.

### Answer 3

Choose UTF-8 source and Unicode 17.0.0 explicitly. Define identifiers from a documented profile of `XID_Start XID_Continue*`, adding underscore to start/continue if desired and listing every subtraction or addition. Decide whether canonical or compatibility normalization applies; for example, NFKC can aid identifier stability but collapses compatibility distinctions. Normalize only identifier comparison, preserve original lexemes and spans, and expose the normalized symbol spelling to tooling. Specify whether canonical equivalents are one name and how persisted symbol data migrates.

Apply an inclusive language policy rather than a hidden ASCII default: state permitted script combinations by project/domain, joining-control contexts, default-ignorable and bidirectional-control treatment, mixed-number policy, and UTS #39 confusable warnings or rejection for security-critical namespaces. Make invisible characters visible in diagnostics and reviews. Warn on collisions after normalization/confusable skeleton checks without pretending confusability is equality. Pin tables in compiler, formatter, linter, and language server; test version upgrades for newly admitted characters and changed diagnostics. An upgrade is a language-compatibility event, not a library refresh.

### Answer 4

Represent each element with stable kind, original byte slice or interned lexeme, byte span, decoded code-point mapping, UTF-16 line/column projection for protocols, optional normalized/value form, lexical mode before/after, and diagnostic payload. Preserve whitespace, comments, directives, BOM/line-ending evidence, and skipped/error slices as trivia or first-class elements. Record delimiter pairing only in an additional concrete layer so flat tokens remain available. Stable identities can combine immutable source-buffer pieces and local element identity rather than absolute offsets that change after every edit.

Properties: ordered element/trivia slices reconstruct original bytes exactly where decoding permits; significant tokens match the batch compiler; spans are monotone and cover all input; no zero-length success loops exist; every diagnostic owns a source slice or end position; applying an edit and incremental rescan yields exactly the same kinds, lexemes, modes, values, and diagnostics as full rescan; restart begins only from a state whose mode/layout context is known. Fuzz byte decoding, Unicode, line endings, tokens, comments, strings, edit positions, and long inputs. A pretty-printer AST is a separate canonicalization product, not proof of round trip.

### Answer 5

Define UTF-8 and a pinned Unicode profile; reserve ASCII syntax for operators, decimal marks, unit separators, and protocol keywords while allowing reviewed localized identifiers in controlled namespaces. Drug identifiers should use authoritative codes rather than appearance alone. Distinguish digit zero from letter `O`, decimal point from locale comma, micro symbols and Greek/Latin lookalikes, `mg` from `mcg`, rate slash, whitespace, comments, signs, exponents, and unit suffixes. Reject invisible/bidirectional controls outside narrowly defined contexts, mixed-script/confusable safety-critical names, malformed normalization, adjacent number/unit forms that the grammar cannot distinguish, and unsupported abbreviations.

Retain exact lexeme, normalized identifier, source span, terminology/code binding, and unit token. Bound file, token, numeric digit, nesting, comment, and diagnostic sizes. Test every operator prefix, Unicode confusable set relevant to formulary/units, decimals and separators, truncated strings/comments, copy/paste from clinical systems, rendering across approved fonts/devices, round trips, parser integration, type/unit checking, dose-limit semantics, and corrupted/hostile inputs. Diagnostics must show escaped code points, visual location, intended vocabulary candidates without autocorrecting a medication order, and a safe rejection path.

Named review includes pharmacists, prescribers, nurses, medication-safety officers, clinical informaticians, terminology and units experts, human-factors and accessibility/localization specialists, device/integration engineers, cybersecurity, quality/regulatory and legal/privacy staff, operations/training teams, vendor representatives, affected clinical users, and independent clinical/technical assurance. Lexical validation cannot establish correct drug, patient, dose, route, timing, clinical judgment, device delivery, or workflow safety; no external approval is claimed.
