---
module_id: COMP-003
program: Compilers & Language Implementation
level: 1
module_number: 3
title: Tokens and Lexical Specifications
status: complete
last_verified: 2026-08-29
---

# Tokens and Lexical Specifications

## One-Page Review

### Governing question

How should a language define the boundary between decoded source text and parser-visible tokens so that recognition, diagnostics, tooling, security, and language evolution remain deterministic?

### Essential definitions

- A **token kind** is a parser-visible category such as `IDENTIFIER`, `INTEGER`, `PLUS`, or `EOF`.
- A **lexeme** is the exact source spelling consumed for one token or trivia item.
- A **token value** is an optional interpreted payload, such as an integer value or decoded string contents; it is not the lexeme.
- A **lexical specification** defines the source alphabet, token languages, disambiguation policy, trivia, errors, and relevant lexical state.
- **maximal munch** selects a longest valid token prefix at the current position.
- **rule priority** resolves ties among token rules that match the same longest prefix.
- A **keyword** is a reserved spelling with grammatical meaning; a **soft/contextual keyword** is interpreted as keyword only in stated contexts.
- **trivia** is source material such as whitespace or comments that may be ignored by the grammar but retained for formatting and provenance.
- A **lexical mode** is finite scanner state that changes which rules are active, as in strings, templates, or nested interpolation.
- A **lexical error** identifies source that no active token or trivia rule may consume under the current language version and mode.

### Central model, mechanism, or theorem

Let the decoded source be $s\in\Sigma^*$, and let ordered token/trivia rules define languages $L_1,\ldots,L_k\subseteq\Sigma^+$. At offset (p), form

$$
C(p)=\{(i,x)\mid x\ne\epsilon\land x\text{ is a prefix of }s[p:]\land x\in L_i\}.
$$

Choose a candidate with maximum (|x|); among equal-length candidates choose the smallest declared priority (i). Emit or retain its classified record, advance by (|x|), and repeat. If (C(p)) is empty, report a bounded lexical error and advance only according to the recovery contract. Rules must not accept the empty string, or scanning may fail to progress.

### Critical invariants

- Every non-EOF token consumes a nonempty, contiguous source span in the declared coordinate system.
- Token spans are ordered, nonoverlapping, and tied to the exact source revision from COMP-002.
- Rule selection is deterministic under documented longest-match, priority, keyword, and mode policies.
- The raw lexeme remains recoverable even when a normalized or decoded token value is stored.
- Trivia and comments are either retained with ownership or intentionally discarded under an explicit consumer contract.
- An EOF token is zero-width at the source end and emitted exactly once when required by the parser API.
- Escape decoding, numeric conversion, identifier normalization, and overflow policy do not silently change source ownership.
- Error recovery guarantees progress, bounded work, and stable diagnostic spans.
- Tokenization is versioned with language edition, feature flags, Unicode tables, and preprocessing state.
- Passing token tests establishes only the tested implementation behavior, not equivalence to every language specification or downstream parser correctness.

### Common failures

Common failures are defining tokens by examples instead of exact languages; applying first-match before longest-match; allowing an empty rule; losing lexemes after value conversion; treating keywords and identifiers inconsistently; attaching skipped comments to no owner; accepting malformed escapes or numeric separators; confusing Unicode normalization with decoding; letting lexer modes leak across errors; tokenizing from stale source positions; performing unbounded work on hostile literals or comments; and assuming that a successful lex proves the program is syntactically or semantically valid.

### Compact example

With rules `EQEQ = "=="`, `EQ = "="`, and an `IDENT` rule for a letter-or-underscore followed by alphanumerics-or-underscores, source `rate==target` becomes `IDENT("rate")`, `EQEQ("==")`, `IDENT("target")`, `EOF`. Maximal munch chooses `EQEQ` over `EQ`; priority is irrelevant because the lengths differ. If `let` is first recognized by `IDENT` and then classified through a reserved-word table, its lexeme remains `let` while its kind becomes `LET`.

### Connections

[COMP-001](001-language-implementation-pipelines.md) establishes the front-end contract, and [COMP-002](002-source-text-encodings-and-position-tracking.md) supplies decoded source snapshots and spans. COMP-004 proves regular-language and automata foundations; COMP-005 and COMP-006 implement handwritten and generated scanners. [PLS-003](../../01-programming-languages-and-semantics/modules/003-grammars-parse-trees-and-abstract-syntax.md) distinguishes lexical from phrase grammar.

## Governing Question

What must a lexer promise to its parser and tools when several token rules can begin at the same character, literals have internal structure, whitespace may be significant, Unicode changes the alphabet, and incomplete source must still produce useful diagnostics?

Lexing is often summarized as “turn characters into tokens.” That phrase hides the real design decisions. Which characters are legal in an identifier? Does `>>` mean one operator or two closers? Does `1..2` contain a floating literal or two integer literals separated by a range operator? Are comments discarded, attached to neighboring tokens, or represented explicitly? When does an escape become a character value? Can the lexer consult parser context? The lexical specification must answer these questions or deliberately assign them to another phase.

## Why This Matters

Tokens form a stability boundary. The parser, formatter, syntax highlighter, refactoring engine, linter, incremental cache, debugger, and macro system may all depend on token identity and spans. A tokenization change that appears local can alter parse trees, compatibility, diagnostics, formatting, source maps, or security review.

Lexers also process attacker-controlled text before semantic validation. Unterminated strings, enormous numeric literals, deep comment nesting, pathological Unicode, and mode-switching delimiters can consume memory or time. Confusable spellings and invisible controls can mislead humans even when recognition is deterministic. Production specifications therefore need resource, provenance, recovery, and display boundaries alongside recognition rules.

## Prerequisites and Retrieval

You should understand sets, strings, prefixes, ordered choice, half-open spans, Unicode scalar values, and the source contract in [COMP-002](002-source-text-encodings-and-position-tracking.md). Retrieve these facts:

1. A source file is decoded under a declared policy before scalar-oriented lexical rules apply.
2. A span identifies bytes or another documented unit in one immutable source revision.
3. A grammar can be ambiguous even when tokenization is deterministic.
4. A parser consumes token kinds and often token payloads, not merely source substrings.
5. Error recovery is part of an interface contract, not evidence that malformed source is valid.

## Learning Objectives

After completing this module, you should be able to:

- distinguish token kinds, lexemes, interpreted values, spans, trivia, and synthetic tokens;
- specify token languages and document maximal-munch and priority rules;
- explain keyword classification, soft keywords, and identifier normalization boundaries;
- design literal tokens without losing raw spelling or deferring illegal ambiguity;
- represent whitespace, comments, line continuations, and EOF deliberately;
- identify cases requiring lexical modes or controlled parser feedback;
- define progress-preserving lexical error recovery and resource budgets;
- reason about token-stream determinism and source-span coverage;
- build tests for overlaps, boundaries, malformed inputs, Unicode, and language editions;
- audit a tokenization change for parser, formatter, IDE, macro, and security impact.

## Core Exposition

Begin by naming the lexical input alphabet. A byte-oriented language can define tokens over bytes, but a Unicode source language commonly defines them over decoded scalar values while storing byte spans. The Unicode version and any permitted identifier profile are semantic inputs. Grapheme clusters and rendered glyphs are normally wrong units for token recognition because lexical spelling must not depend on fonts or display shaping.

The output should be richer than a pair of kind and text. A durable token record often contains

$$
Token=(kind,span,lexeme,value,trivia,flags,origin).
$$

Not every implementation stores every field inline. The invariant is that consumers can recover what their contract promises. `INTEGER` may carry a parsed magnitude while retaining spelling `0xff_ff`; a string may carry decoded contents while diagnostics still point to the raw escape; a macro token may carry an expansion origin chain.

**Token languages and progress.** Each rule recognizes a set of nonempty strings. Fixed punctuation has singleton languages: (L_{PLUS}=\{+\}). An identifier rule might start with an identifier-start character and continue with identifier-continue characters. A decimal-integer rule may constrain separators and suffixes. The rule language must distinguish recognition from later meaning: spelling `count` can be an identifier token even before name resolution decides which declaration it denotes.

No ordinary rule may accept $\epsilon$. If an empty token wins without advancing, the scanner loops forever. EOF is exceptional: it is a synthetic zero-width observation at the already reached end, emitted once under API state rather than repeatedly recognized by a source regex. Inserted recovery tokens are likewise parser artifacts with explicit synthetic provenance, not ordinary source-consuming tokens.

**Longest match and priority.** At a source offset, several rules may match prefixes. The common policy is maximum length, then declaration priority. Thus `==` beats `=` because it consumes more source. If both `IF` and `IDENT` match `if` with equal length, priority can select `IF`; alternatively the scanner can recognize `IDENT` and reclassify it through a reserved-word table. Both are valid if specified consistently.

“First regex wins” is incomplete unless the engine itself computes the longest match for the selected rule set. Checking rules sequentially and accepting the first prefix would tokenize `==` as two `=` tokens when `EQ` appears first. Generated scanner systems may combine rules into one automaton yet retain rule order only as a tie-break. COMP-004 and COMP-006 develop those mechanisms.

Longest match is not universally correct for every language construct. A language may include explicit exceptions or lexical goals. The specification should name them instead of relying on folklore. When adding an operator, analyze every prefix and extension relationship with existing operators and literals.

**Keywords and identifiers.** Reserved keywords cannot be used as ordinary identifiers in the applicable language context. A robust implementation often recognizes the complete identifier lexeme, then consults a versioned keyword map. This avoids matching keyword prefixes: `ifelse` stays one identifier rather than `IF` followed by `IDENT`.

Soft or contextual keywords preserve compatibility by becoming grammatical markers only in selected positions. The scanner can emit a general identifier plus spelling, letting the parser reinterpret it; or it can accept a controlled lexical goal from the parser. The choice affects incremental parsing and tooling. Syntax highlighters should not color every spelling as reserved when the language does not.

Unicode identifiers need exact start/continue sets, normalization policy, escape rules, and version. Decoding source and normalizing identifiers are separate operations. Preserve original spelling and span while storing a comparison key if the language equates normalized forms. Confusable detection is a security diagnostic or policy layer; visual similarity is not token equality by default.

**Punctuation and operators.** Fixed delimiters and operators create overlapping prefixes: `.`, `..`, `...`; `>`, `>=`, `>>`, `>>=`; `/`, `//`, `/*`; `:`, `::`, `:=`. Enumerate the vocabulary, choose maximal match, and test every prefix boundary. A parser may later split a compound token in a narrow grammatical situation, but that transformation needs source-preserving provenance and a documented ownership boundary.

Operator characters do not need one token each. Some languages permit user-defined symbolic operators and lex a maximal operator sequence into one generic token. Others reserve a closed list. That language-design choice controls compatibility and parser complexity.

**Numeric literals.** A numeric token specification must define bases, decimal points, exponents, digit separators, prefixes, suffixes, case, and adjacency. Recognition and conversion should be separable. The lexer can reject malformed separator placement while a later literal phase checks magnitude, target type, rounding, overflow, and edition-specific suffix meaning.

Boundary cases expose hidden policy. With a range operator `..`, source `1..2` should often become `INTEGER(1)`, `DOTDOT`, `INTEGER(2)`, not a malformed float followed by a dot. A numeric regex that greedily accepts a trailing decimal point can steal the first range dot. Define a float language and operator priority together; do not repair the result accidentally in the parser.

Keep the raw spelling. Decimal `10`, hexadecimal `0xA`, separator form `1_0`, and suffixed `10u8` may denote related values but have different formatting, macro, diagnostic, and compatibility meaning. Conversion of million-digit integers requires a size budget before expensive arbitrary-precision arithmetic.

**Strings, characters, and escapes.** A string token may include delimiters and raw escape spelling while its value contains decoded scalars or bytes. The specification must define valid escapes, delimiter escaping, line breaks, continuation, raw strings, interpolation boundaries, and malformed-input behavior. Escape validity should point to the exact offending span.

Interpolated strings usually require modes. In text mode, `${` may end a text token and enter expression mode; braces in expression mode obey language syntax; the matching close brace returns to text mode. Nested strings or templates may push more modes. Mode stacks require maximum depth or resource policy and deterministic recovery when EOF arrives before closure.

Do not interpret arbitrary source escapes twice. A lexer that decodes a string and a later code generator that decodes it again can change backslashes or create injection. Store raw and interpreted forms with clear ownership.

**Whitespace, comments, and trivia.** Some whitespace merely separates tokens; some terminates statements or determines indentation. Comments may act like whitespace, doc attributes, directives, or source retained by formatters. COMP-007 treats layout mechanisms deeply; this module establishes that “skip it” is not a sufficient cross-tool contract.

Lossless tooling can retain trivia as explicit tokens or attach leading/trailing trivia to significant tokens. Attachment policy must handle file headers, trailing comments, blank lines, EOF comments, and edits between tokens. A parser optimized for compilation may receive only significant tokens while a parallel lossless stream feeds formatting. Both views must share spans and source revision.

Comments can overlap operator prefixes and can nest in some languages. A block-comment recognizer must define nesting, newline tracking, EOF error, and maximum resource use. Regex shorthand that ignores nesting may contradict the language. Documentation comments should preserve exact spelling and normalization rules needed by the documentation tool.

**Lexical modes and feedback.** Pure tokenization is a function of source and language configuration. Real languages sometimes need finite lexical state: string delimiters, template interpolation, indentation stacks, or embedded sublanguages. Model the state explicitly:

$$
(tokens,state')=Lex(source,state,configuration).
$$

Avoid unconstrained parser-to-lexer feedback because it makes tokenization history-dependent and complicates caching. If the language standard defines lexical goals, expose a finite named goal at token requests and include it in cache keys. JavaScript regular-expression literals versus division are a classic example of lexical interpretation depending on syntactic context.

Preprocessors and macros can also change the token stream. Keep physical-source lexing distinct from expansion-token production. Token pasting, generated identifiers, and conditional inclusion require origin chains and language-specific rules; they are not reasons to discard the original tokenization.

**Errors and recovery.** When no rule matches, the lexer should emit a diagnostic with the unexpected source span, expected lexical category if useful, mode, and recovery action. Consuming one Unicode scalar usually guarantees progress for an isolated invalid character. For an unterminated string or comment, consuming to a synchronization boundary may reduce cascades, but the behavior must be bounded and tested.

An `ERROR` token can let the parser continue while preserving bad text. Another API can return diagnostics alongside normal tokens. Either way, downstream phases must know whether tokens are complete, recovered, or synthetic. Never silently drop an unrecognized character: `x@y` becoming `x y` can change meaning and conceal corruption.

Recovery state matters. At newline or EOF, a scanner may reset a string mode, preserve it for an IDE continuation, or emit a synthetic delimiter. Batch and interactive modes may differ, but their token contracts must be named. Incremental relexing must restart from a state known to determine subsequent tokens and continue until both tokens and outgoing state converge with cached data.

**Determinism and coverage.** For fixed source, revision, language version, Unicode version, features, preprocessing inputs, initial mode, and resource policy, tokenization should be deterministic unless the language explicitly says otherwise. Every consumed source interval should be owned by a token, trivia, or error record. Significant tokens appear in order and never overlap.

A useful coverage invariant is

$$
[0,|s|)=\biguplus spans(tokens,trivia,errors),
$$

after translating all spans to one coordinate system. Synthetic tokens have empty spans and are excluded from physical coverage. This invariant catches dropped bytes and duplicated ownership but does not prove correct classification.

**Testing the specification.** Derive boundary tables for every pair of rules with overlapping prefixes. Test the empty source, one-character inputs, every fixed-token prefix, keyword prefixes/suffixes, adjacent tokens without whitespace, every literal delimiter, valid/invalid escapes, separator placement, EOF in every mode, Unicode start/continue boundaries, comments, maximum lengths, and error recovery.

Use differential tests only when another implementation targets the same language edition and configuration. Property tests can assert ordered nonoverlapping spans, progress, coverage, concatenated lexeme recovery, idempotent token serialization where defined, and clean-versus-incremental equivalence. Fuzzing needs time, memory, token-count, mode-depth, and diagnostic-count budgets.

The model below demonstrates longest match, tie priority, keyword reclassification, trivia retention, spans, EOF, and one-character error recovery. It uses ASCII-only rules intentionally; it is not a complete lexer, regex/automata proof, Unicode identifier implementation, or parser.

<!-- bijux-verify: {"id":"lexical-rule-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source=let rate==12.5\ntokens=LET:let@0:3 IDENT:rate@4:8 EQEQ:==@8:10 NUMBER:12.5@10:14 EOF:@14:14\ntrivia=WS: @3:4\nerror=unexpected '@' at 2\npolicy=longest_then_rule_order\n","stderr":""}} -->
```python
import re

rules = (
    ("WS", r"[ \t\r\n]+"),
    ("EQEQ", r"=="),
    ("EQ", r"="),
    ("NUMBER", r"[0-9]+(?:\.[0-9]+)?"),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
)
keywords = {"let": "LET"}


def scan(source):
    tokens = []
    trivia = []
    index = 0
    while index < len(source):
        candidates = []
        for priority, (kind, pattern) in enumerate(rules):
            match = re.match(pattern, source[index:])
            if match:
                candidates.append((len(match.group()), -priority, kind, match.group()))
        if not candidates:
            return tokens, trivia, f"unexpected {source[index]!r} at {index}"
        length, _, kind, lexeme = max(candidates)
        end = index + length
        record = (kind, lexeme, index, end)
        if kind == "WS":
            trivia.append(record)
        else:
            if kind == "IDENT" and lexeme in keywords:
                record = (keywords[lexeme], lexeme, index, end)
            tokens.append(record)
        index = end
    tokens.append(("EOF", "", index, index))
    return tokens, trivia, None


def show(records):
    return " ".join(f"{kind}:{lexeme}@{start}:{end}" for kind, lexeme, start, end in records)


source = "let rate==12.5"
tokens, trivia, error = scan(source)
print(f"source={source}")
print("tokens=" + show(tokens))
print("trivia=" + show(trivia))
_, _, bad_error = scan("x @")
print(f"error={bad_error}")
print("policy=longest_then_rule_order")
```

## Definitions and Notation

Let $s=c_0\ldots c_{n-1}\in\Sigma^*$ be a decoded source sequence whose boundaries map to COMP-002 byte offsets. A lexeme at position (p) is half-open slice (s[p:q]), $p<q\le n$.

An ordered lexical rule is (R_i=(name_i,L_i,channel_i,action_i)), where $L_i\subseteq\Sigma^+$, `channel` distinguishes significant token, trivia, or diagnostic ownership, and `action` computes a kind/value/mode transition without changing the consumed span.

The candidate set is

$$
C(p,m)=\{(i,q)\mid s[p:q]\in L_i\text{ and }R_i\text{ is active in mode }m\}.
$$

Selection orders candidates lexicographically by maximum (q-p), then minimum priority (i). A configuration (K) includes language edition, feature flags, Unicode data, preprocessing policy, limits, and initial mode. Thus tokenization is a partial function

$$
Lex_K:(Source,Revision)\to(Token^*,Trivia^*,Diagnostic^*,FinalState).
$$

It becomes operationally total when every unmatched position has a progress-preserving error action. This totality does not mean every input is lexically valid.

## Mechanisms, Invariants, or Proof Structure

**Progress.** Every ordinary selected rule consumes (q-p>0). Every recovery action either consumes a nonempty source interval or terminates. Therefore a finite source cannot cause an infinite loop solely through zero-length emissions. EOF is emitted through separate one-shot API state.

**Deterministic choice.** Candidate lengths are finite integers and priorities are totally ordered. If rule order is unique, maximum length plus minimum priority selects at most one rule. Mode transitions and semantic actions must also be deterministic for the complete token stream to be deterministic.

**Span coverage.** Maintain cursor (p). Emitting record ([p,q)) followed by cursor assignment (p:=q) makes physical records adjacent and nonoverlapping. If errors use the same rule and EOF occurs only at (n), induction over scanner steps establishes coverage of ([0,n)).

**Keyword boundary.** Recognize the maximal identifier before consulting a keyword map. Therefore `letdown` is classified once from full spelling and cannot be split into `LET` plus `IDENT` merely because it has a keyword prefix.

**Value/lexeme separation.** Literal conversion is a function from recognized spelling and language configuration to a value or bounded diagnostic. Keeping the original span and spelling lets formatting, macro, audit, and error consumers operate even if conversion fails.

**Mode convergence for incrementality.** A relexed suffix can reuse cached tokens only after both the token boundary sequence and outgoing lexical state agree at a safe checkpoint. Matching text alone is insufficient if an unterminated construct changed the mode.

**Empirical boundary.** The executable model exercises one ASCII rule set and two inputs. Passing output calibrates its selection and span bookkeeping; it does not prove the stated specification, the Python regex engine, Unicode policy, or production resource behavior.

## Alternatives and Trade-Offs

**Reserved-token rules versus identifier reclassification.** Dedicated keyword rules make kinds direct but depend on tie priority. Reclassification centralizes identifier spelling and simplifies keyword-prefix behavior. Soft keywords usually favor parser interpretation.

**Lossy versus lossless token streams.** Dropping trivia reduces compiler memory and parser traffic. Retention supports exact formatting, refactoring, documentation, and comments. Dual views or compact span-backed trivia can balance the needs.

**One token versus parser splitting.** Maximal compound operators simplify lexing. Grammar contexts such as nested type closers may prefer splitting. Parser splitting increases cross-phase coupling and must preserve exact subspans.

**Decoded versus deferred literal values.** Early conversion gives the parser useful payloads and early diagnostics. Deferral preserves target/type context and avoids expensive work. A hybrid recognizes structure lexically, records raw spelling, and performs typed conversion later.

**Stateless versus modeful scanning.** Stateless rules are easy to cache and reason about. Modes express templates, raw delimiters, indentation, and embedded languages but expand state, recovery, and incremental invalidation obligations.

**Lexer-owned versus parser-informed context.** Lexer ownership yields a stable reusable stream. Finite parser goals can match a language standard but make token requests contextual. Unbounded semantic feedback should not be smuggled into lexing.

**Strict failure versus recovery tokens.** Batch compilation can stop at the first lexical error. Editors benefit from bounded recovery and partial streams. Both need honest diagnostics; recovery must never silently declare malformed text valid.

## Failure Modes and Misconceptions

1. **“Tokens are just strings.”** Kinds, spans, values, trivia, origins, modes, and recovery status are distinct data.
2. **“Put longer operators first and the problem is solved.”** That simulates some overlaps but does not specify general longest match or tie behavior.
3. **“A regex that can match empty is harmless.”** It can violate progress and loop at one offset.
4. **“Keywords should match before identifiers.”** Without full-identifier matching, keyword prefixes can split valid identifiers.
5. **“Whitespace is never syntax.”** Newlines, indentation, continuation, and comment placement can be language-significant.
6. **“Discarded trivia has no users.”** Formatters, refactorings, doc tools, source maps, and audits may require it.
7. **“The numeric value is the token.”** Raw spelling carries base, separators, suffix, formatting, and precise error information.
8. **“Unicode decoding defines identifier equality.”** Identifier profiles, escapes, normalization, and confusable policy are separate versioned choices.
9. **“Maximal munch resolves every language.”** Standards can define lexical goals, exceptions, or contextual splitting.
10. **“An error character can be skipped silently.”** Dropping it can join or separate surrounding tokens and conceal changed meaning.
11. **“Lexer modes are implementation details.”** Their transitions affect tokenization, recovery, caching, and denial-of-service limits.
12. **“EOF is another empty regex.”** EOF needs one-shot end-state semantics; a reusable empty match destroys progress.
13. **“If lexing succeeds, parsing will succeed.”** A valid token sequence may violate phrase grammar or later static semantics.
14. **“Matching another compiler proves correctness.”** The reference may target another edition, share a defect, or differ legitimately.

## Worked Examples

### Example 1

**Question:** How is `===` tokenized when rules include `===`, `==`, and `=`?

**Reasoning:** All three match prefixes at the first offset. Their lengths are three, two, and one. Maximal munch selects `===` without consulting rule priority.

**Conclusion:** Priority breaks equal-length ties; it does not override a longer candidate.

### Example 2

**Question:** Why should `ifelse` not become `IF` followed by `IDENT(else)`?

**Reasoning:** The identifier language consumes the full seven-character spelling. Keyword classification occurs only after maximal identifier recognition; `ifelse` is not equal to reserved spelling `if`.

**Conclusion:** Keyword recognition must respect identifier boundaries.

### Example 3

**Question:** What records should remain after lexing hexadecimal `0x0A_FF`?

**Reasoning:** The token keeps raw span/spelling `0x0A_FF`; structural validation checks prefix and separators; conversion may store magnitude 2815. A formatter or macro still needs the original spelling.

**Conclusion:** Lexeme and interpreted value serve different consumers.

### Example 4

**Question:** How can `1..2` expose a lexical-specification defect?

**Reasoning:** If a float rule accepts `1.` without requiring a following digit, longest match may consume `1.` and leave `.2`. If the language owns `..` as range, its literal boundary rules should yield `INTEGER`, `DOTDOT`, `INTEGER`.

**Conclusion:** Specify literal and operator boundaries together.

### Example 5

**Question:** Where does a comment belong in a lossless stream for `x /*why*/ + y`?

**Reasoning:** Its span must be retained as explicit trivia or attached under a stable leading/trailing rule. Deleting it from the only representation prevents exact formatting and documentation analysis.

**Conclusion:** Trivia ownership is an API decision, not an afterthought.

### Example 6

**Question:** What should happen at `"bad\\q"` if `\q` is not an escape?

**Reasoning:** The lexer can emit a string/error record while diagnosing the two-character escape span. It should retain raw source and avoid silently converting `\q` to `q`.

**Conclusion:** Malformed escape policy must preserve causal spelling and progress.

### Example 7

**Question:** Why is `${x + "}"}` not handled by searching for the next `}`?

**Reasoning:** Template text enters expression mode; the inner string delimiter changes how `}` is interpreted; only a close brace at the correct nested state exits the interpolation.

**Conclusion:** Interpolation needs explicit lexical/syntactic state rather than delimiter substring search.

### Example 8

**Question:** Can the parser always receive one fixed tokenization of `/a+/g` and `a / b`?

**Reasoning:** In languages with regex literals and division sharing `/`, the standard may use syntactic lexical goals to decide which token language is active. The goal must be finite, explicit, versioned, and included in incremental state.

**Conclusion:** Contextual lexing is acceptable when it is a specified interface, not hidden feedback.

### Example 9

**Question:** What does the coverage invariant reveal if source `a@b` yields only `IDENT(a)` and `IDENT(b)`?

**Reasoning:** Their spans do not cover the `@` interval. The missing ownership proves the scanner silently discarded input, although it does not by itself prescribe the correct token kind.

**Conclusion:** Coverage detects lost source independently of classification correctness.

### Example 10

**Question:** A configuration language controls industrial equipment. What is required beyond a lexer test suite?

**Reasoning:** Language reviewers must approve token, unit, comment, normalization, and version rules. Security reviewers must test confusables, resource exhaustion, malformed encodings, and diagnostic spoofing. Parser/semantic reviewers must prove the accepted token stream receives the intended units and constraints. Domain and safety reviewers must validate limits, fail-safe behavior, traceability, deployment identity, and recovery. This chapter claims none of those external approvals.

**Conclusion:** Correct token boundaries are necessary but cannot establish system-level safety or configuration meaning.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns the language-level distinction between lexical and phrase structure.
- [Metaprogramming](../../06-programming-languages-metaprogramming/ROADMAP.md) consumes and produces tokens through preprocessing, macros, quoting, and expansion provenance.
- [Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md) supplies determinism, progress, and induction principles for scanner arguments.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) contributes property, differential, fuzz, mutation, and regression evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) examines confusables, invisible controls, parser differentials, resource exhaustion, and untrusted-input boundaries.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) depends on explicit versioned lexical grammars for protocols, query languages, and configuration formats.

## References

1. Robert Nystrom, [*Crafting Interpreters: Scanning*](https://craftinginterpreters.com/scanning.html). Token representation, lexemes, keywords, literals, errors, and a handwritten scanner.
2. LLVM Project, [*My First Language Frontend with LLVM: Kaleidoscope Introduction and the Lexer*](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html). Official compact lexer and token-interface tutorial.
3. Python Software Foundation, [*The Python Language Reference: Lexical Analysis*](https://docs.python.org/3/reference/lexical_analysis.html). Current normative rules for lines, indentation, identifiers, literals, operators, and delimiters.
4. Rust Project, [*The Rust Reference: Tokens*](https://doc.rust-lang.org/reference/tokens.html). Current normative token, literal, suffix, punctuation, and reserved-form rules.
5. Ecma International, [*ECMAScript Language: Lexical Grammar*](https://tc39.es/ecma262/multipage/ecmascript-language-lexical-grammar.html). Normative lexical goals, tokens, identifiers, literals, and comments.
6. Go Project, [*The Go Programming Language Specification: Lexical Elements*](https://go.dev/ref/spec#Lexical_elements). Normative token, semicolon, identifier, keyword, operator, and literal rules.
7. Vern Paxson et al., [*Flex Manual: How the Input Is Matched*](https://westes.github.io/flex/manual/Matching.html). Longest-match and rule-order behavior in a production lexer generator.
8. ANTLR Project, [*ANTLR4 Documentation: Lexer Rules*](https://github.com/antlr/antlr4/blob/master/doc/lexer-rules.md). Official modes, commands, fragments, priority, and longest-match guidance.
9. Unicode Consortium, [*Unicode Standard Annex #31: Unicode Identifiers and Syntax*](https://www.unicode.org/reports/tr31/). Versioned identifier profiles, normalization, and syntax recommendations.
10. Unicode Consortium, [*Unicode Technical Standard #39: Unicode Security Mechanisms*](https://www.unicode.org/reports/tr39/). Confusable detection, identifier restriction, and mixed-script security mechanisms.

## Exercises

### Exercise 1

Given ordered rules `DOTDOTDOT="..."`, `DOTDOT=".."`, `DOT="."`, `FLOAT=[0-9]+\.[0-9]+`, and `INTEGER=[0-9]+`, tokenize `1...2`, `1..2`, `1.2`, and `1.` under maximal munch. Identify any lexical error.

### Exercise 2

Design token records for `let café = 0x0A_FF // count` that support parsing, exact formatting, Unicode-aware name comparison, and diagnostics. State which representations must remain distinct.

### Exercise 3

Prove progress and deterministic selection for a finite ordered rule set whose languages exclude the empty string, assuming recovery consumes one scalar when no rule matches. State what the argument does not prove.

### Exercise 4

Specify lexical modes and recovery for strings with `${...}` interpolation, nested ordinary strings inside expressions, and EOF in every mode. Include incremental-relexing checkpoints and depth limits.

### Exercise 5

Prepare a verification plan for changing a language from reserved keyword `async` to a contextual keyword while keeping old source compatible. Cover token streams, parsing, tooling, versions, hostile cases, evidence, and human review.

## Answers to the Exercises

### Answer 1

`1...2` yields `INTEGER("1")`, `DOTDOTDOT("...")`, `INTEGER("2")`. `1..2` yields `INTEGER("1")`, `DOTDOT("..")`, `INTEGER("2")`. `1.2` yields `FLOAT("1.2")` because it is longer than the integer prefix. `1.` yields `INTEGER("1")`, `DOT(".")`; it is not a float because the rule requires at least one digit after the point. Every character is owned, so none of these inputs has a lexical error. Equal-length priority is not needed in these examples.

### Answer 2

Emit significant tokens `LET`, `IDENT`, `EQ`, `INTEGER`, `EOF`; retain whitespace and `// count` as trivia. Every record carries the immutable source/revision and byte span. `IDENT` retains raw UTF-8 spelling `café` plus a separately versioned comparison key if the language normalizes identifiers. `INTEGER` retains `0x0A_FF`, structural metadata or parsed magnitude, and conversion diagnostics separately. Do not conflate raw bytes, decoded scalars, normalized identifier key, rendered glyphs, numeric magnitude, trivia, or parser meaning. Exact formatting reconstructs source from ordered token/trivia spans rather than normalized values.

### Answer 3

At cursor (p<n), either the candidate set is nonempty or it is empty. If nonempty, every candidate length is positive and the finite set has a maximum length; unique rule priorities select one among maximum-length candidates, so the next cursor (q>p) is deterministic. If empty, recovery consumes one scalar, again advancing to a later boundary. Because the source has finitely many scalar boundaries, repeated steps reach (n); a one-shot EOF action terminates. The argument proves scanner-step progress and choice determinism given deterministic actions. It does not prove rule-language correctness, intended classification, conversion correctness, resource bounds of regex matching, Unicode conformance, parser correctness, or implementation equivalence.

### Answer 4

Use modes `TEXT`, `INTERPOLATION`, and `STRING`, with a stack recording delimiter kind and brace depth. `${` in `TEXT` emits text/delimiter records and pushes `INTERPOLATION`; `{` and `}` there adjust depth, and only the matching depth-zero close returns to `TEXT`. A quote in interpolation pushes `STRING`, whose escapes prevent embedded quotes/braces from changing interpolation state. EOF in any nonbase mode emits an unterminated-construct diagnostic tied to the opening delimiter and either returns a recovered partial stream or stops under batch policy. Cap stack depth, token length, diagnostics, and total work. Store restart checkpoints only where the complete mode stack is known; after an edit, relex until token boundaries and outgoing stack agree with the cached stream.

### Answer 5

Pin old and new editions. In the old edition, `async` retains its reserved-token behavior. In the new edition, lex the full spelling as `IDENT` (or a token carrying contextual-candidate metadata) and let only specified parser states interpret it as keyword. Build golden cases for declarations, uses named `async`, keyword-prefix identifiers, comments/trivia, malformed constructs, macros, formatting, highlighting, rename, completion, and incremental edits. Differentially compare unchanged old programs under their original edition and test explicit migration diagnostics where meaning changes. Fuzz ambiguous surrounding syntax with resource limits. Review cache keys and serialized token compatibility so edition and lexical goal are included. Language-design reviewers approve grammar/compatibility; compiler and tooling reviewers approve parser and IDE behavior; security reviewers assess spoofing and parser differentials. Passing tests supports the tested implementations but does not prove all-source compatibility or external approval.
