---
module_id: META-003
program: Programming Languages: Metaprogramming
level: 1
module_number: 3
title: Text Substitution and Its Failure Modes
status: complete
last_verified: 2026-08-29
---

# Text Substitution and Its Failure Modes

## One-Page Review

### Governing question

When does replacing placeholders with character or token sequences preserve intent, and why does substitution fail when inserted data crosses lexical, syntactic, binding, evaluation, or trust boundaries?

### Essential definitions

- **Text substitution** replaces marked regions in a character sequence with other character sequences.
- **Token substitution** replaces preprocessing tokens or token sequences; it is more structured than raw text but still lacks a full parse tree and binding information.
- A **placeholder** names an insertion site; a **replacement environment** maps placeholders to replacement values.
- **Expansion** applies substitution rules to a template or input stream, possibly once or repeatedly through rescanning.
- A **host context** is the grammar position receiving replacement text: plain text, expression, string literal, shell word, SQL value, HTML text, URL component, and so on.
- A **data/directive boundary** separates inert data from syntax that controls parsing or execution.
- **Capture** occurs when inserted or surrounding identifiers bind differently after expansion than intended.
- **duplicate evaluation** occurs when one substituted argument appears in multiple evaluated positions.
- **context-sensitive encoding** maps data into one particular grammar position so that it remains data there.
- A **structured constructor** builds typed tokens, syntax nodes, parameters, or command arguments without reparsing undifferentiated concatenated text.

### Central model, mechanism, or theorem

Let templates and replacements be strings over alphabet \(\Sigma\). A one-pass substituter is

\[
S:T\times(Name\rightharpoonup\Sigma^*)\to\Sigma^*.
\]

Let \(parse_C\) parse the result in host context \(C\). Substitution is safe for a data placeholder only if every admitted value \(v\) satisfies a boundary-preservation obligation such as

\[
parse_C(S(T,p\mapsto E_C(v)))=Expected_C(v),
\]

where \(E_C\) is correct for that exact context. Raw identity substitution \(E_C(v)=v\) cannot satisfy this across arbitrary grammars because delimiter and operator characters differ by context. Structure must be preserved by contextual encoding, typed construction, parameterization, or rejection.

### Critical invariants

- Specify whether the engine replaces characters, tokens, words, syntax nodes, or typed values.
- Define placeholder recognition, unknown-name behavior, expansion order, rescanning, recursion, and termination.
- Insert data only through an encoder or constructor for the exact receiving grammar position.
- Preserve token boundaries, expression grouping, statement shape, bindings, evaluation count, and evaluation order when those properties are claimed.
- Treat replacement values as untrusted data unless separately authorized as directives or code.
- Keep shell argument vectors, SQL parameters, DOM text nodes, and structured configuration distinct from command/query/markup strings.
- Record template, inputs, engine/version, options, output digest, diagnostics, and source mapping for generated artifacts.
- Bound output size, recursion depth, replacement count, time, and memory.

### Common failures

Common defects include operator-precedence changes, duplicated side effects, dangling `else`, comma and whitespace splitting, accidental globbing, quote termination, delimiter collision, name capture, rescanning surprises, recursive expansion, unknown placeholders left silently, injection of commands/queries/markup, double or wrong-context escaping, lost source locations, nondeterministic environment substitution, secret disclosure, and exponential output growth.

### Compact example

Replacing `{{x}}` in `{{x}} * {{x}}` with `a + b` yields `a + b * a + b`. A later expression parser groups multiplication before addition, so the result is not `(a+b)*(a+b)`. Parenthesizing each occurrence repairs this particular precedence case but still duplicates an effectful replacement such as `next_value()`. Textual grouping cannot establish single evaluation.

### Connections

[META-001](001-programs-about-programs.md) supplies representation and transformation contracts; [META-002](002-compile-time-build-time-load-time-and-run-time-metaprogramming.md) supplies phase and authority. [META-004](../ROADMAP.md) contrasts textual and syntactic structure, while Modules 011–020 develop preprocessor, expansion, capture, hygiene, diagnostics, and tests. Parsing connects to [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md).

## Governing Question

What must be true before replacing one sequence of characters or preprocessing tokens with another can be called semantics-preserving rather than merely mechanically successful?

Substitution is attractive because it is universal. Configuration templates, build files, shell scripts, documentation generators, preprocessors, email templates, SQL builders, deployment manifests, and source generators can all begin with “find a marker and insert a value.” The mechanism needs little knowledge of the target language and can be implemented in a few lines.

That ignorance is its defining limitation. A string engine does not know whether a placeholder occupies an arithmetic expression, an identifier, one shell argument, an HTML attribute, a SQL value, or a comment. A flat-token preprocessor knows token boundaries but usually not the target parser's expression tree, type system, binding graph, effect model, or domain constraints. The output can be well-formed text and still parse differently, bind differently, execute an input twice, leak a secret, or grant data the authority of code.

## Why This Matters

Text substitution sits on critical supply-chain and runtime paths. A build variable becomes part of a compiler command. A deployment template selects an image and arguments. A schema value becomes generated source. A log format incorporates external strings. A web template inserts user data into HTML and JavaScript. A migration tool emits SQL. One boundary mistake can produce compilation failures across thousands of generated files or become command, query, template, or code injection.

The lesson is not “strings are bad.” Plain text substitution is correct for genuinely plain text under a complete delimiter and encoding contract. Token macros can express portable conditional compilation that ordinary functions cannot. The discipline is to identify the receiving language and context, constrain directive authority, choose the least powerful representation, and verify both expansion and downstream interpretation.

## Prerequisites and Retrieval

You should understand strings, tokens, expressions, variables, function calls, quoting, parsing at an introductory level, and META-001's representation model. Retrieve these facts:

1. Character equality does not imply syntactic or semantic equivalence.
2. Parsing assigns structure after text or tokens are produced.
3. A value can be evaluated more than once when its source expression is copied.
4. Identical identifier spellings can refer to different bindings.
5. Data becomes authority when a later interpreter treats its characters as directives.
6. Escaping is defined relative to one grammar position, not to “strings in general.”
7. Build and runtime environments can supply hidden, mutable, or secret replacement values.

No macro-hygiene theory is required. This chapter diagnoses the limits that motivate structured and hygienic systems later.

## Learning Objectives

After completing this module, you should be able to:

- distinguish raw text substitution, preprocessing-token replacement, structured syntax transformation, and parameter binding;
- specify placeholder syntax, expansion order, rescanning, recursion, unknown-name, and error policies;
- predict precedence, grouping, statement-shape, delimiter, whitespace, and repeated-evaluation failures;
- explain why parentheses repair only a subset of expression-macro problems;
- identify lexical capture and global macro-name pollution without yet implementing hygiene;
- choose context-specific encoding or typed construction for shell, SQL, HTML, URLs, and configuration;
- design deterministic expansion with provenance, source mapping, output limits, and redaction;
- test expansion independently from parsing, compilation, execution, and domain correctness;
- identify when a function, data structure, AST constructor, prepared statement, or argument vector should replace substitution;
- review high-stakes generated configuration without claiming that successful rendering proves operational safety.

## Core Exposition

At the rawest level, substitution scans characters for delimiters such as `${name}`, `{{name}}`, or `%NAME%` and copies replacement characters into the output. The engine needs rules for escaping delimiters, duplicate names, missing values, invalid names, nesting, and encoding. Even before another language parses the result, ambiguous marker syntax can cause partial matches: `${id}` and `${id_long}` are safe only if recognition consumes explicit boundaries rather than replacing bare prefixes.

Token substitution first lexes or otherwise recognizes units. The C and C++ preprocessors are canonical examples, but calling them raw string replacement is inaccurate. Macro replacement operates on preprocessing tokens. String and character literals are already tokens during replacement, and identifiers inside them are not independently replaced. Function-like macro arguments are token sequences separated under specified parenthesis rules. The resulting tokens can be stringized, concatenated, rescanned, and eventually parsed as the target language.

Tokens prevent some character accidents but do not supply full expression structure. Consider `#define SQUARE(x) x * x`. Invocation `SQUARE(a + b)` produces tokens equivalent to `a + b * a + b`, whose later parse follows multiplication precedence. Writing `#define SQUARE(x) ((x) * (x))` preserves grouping for many expression arguments and surrounding operators. It does not preserve single evaluation: `SQUARE(next())` contains two calls.

A macro such as `MAX(a,b)` commonly expands an argument in a comparison and again in a chosen branch. One argument may execute twice, the other once, and order can follow conditional-expression rules rather than a caller's intuition. If arguments mutate state, acquire locks, read devices, allocate identifiers, or perform I/O, copying their tokens copies the evaluation sites. An inline function, generic function, or typed binding evaluates ordinary arguments according to language call rules and is preferable when phase and type requirements permit.

Statement-like substitution has separate grammar hazards. A multi-statement replacement used under `if (condition) MACRO(); else ...` can detach `else`, alter scope, or make a trailing semicolon change parsing. C idioms such as a `do { ... } while (0)` wrapper repair a narrow statement-context contract, but do not provide types, hygiene, single evaluation, or universal control-flow safety. A macro that contains `return`, `break`, `continue`, labels, or declarations must document that nonlocal behavior.

Capture arises because inserted identifiers meet a lexical environment the substitution engine does not model. A replacement introducing `tmp` can collide with a caller's `tmp`. A replacement expression containing a free `limit` can bind to a declaration near the expansion rather than the definition. Macro names can also pollute a translation unit without respecting ordinary namespace or scope rules. Prefix conventions reduce collision probability; they do not prove freshness or preserve intended binding. Structured hygienic systems attach lexical context or perform systematic renaming, developed later in this program.

Expansion order is observable. A one-pass template can insert characters resembling another placeholder and leave them inert. A recursive engine can rescan and expand them, enabling composition but also order dependence, cycles, and unintended interpretation. GNU `m4` rescans output under detailed quoting rules. C/C++ macro replacement rescans resulting preprocessing tokens with specified suppression rules. GNU `make` distinguishes recursive, simple, immediate, deferred, and secondary expansion contexts. An engine must name its rule rather than promise “variables are replaced.”

For recursive expansion, define a dependency graph whose edge \(a\to b\) means expansion of `a` can reference `b`. A cycle can diverge or be stopped by engine-specific rules. Even an acyclic graph can expand exponentially when one replacement duplicates the next repeatedly. Termination therefore needs cycle detection or a formal suppression rule plus hard budgets for depth, steps, bytes, time, and memory.

Unknown placeholders deserve failure by default in governed generation. Leaving `{{region}}` in a deployment manifest may produce a later parser error, or worse, be accepted as an unintended literal. Replacing it with empty text can collapse delimiters or broaden a value. A nullable placeholder must be declared as such and its surrounding syntax designed for absence. Diagnostics should name the template location, placeholder, available source/configuration, and phase without exposing secrets.

Whitespace and delimiters are syntax in many hosts. Substituting `Lee, Admin` into comma-separated `owner={{name}},role=editor` creates an extra field unless a CSV-aware writer quotes it. Substituting a filename containing spaces or wildcard characters into an unquoted shell word can create several arguments and pathname matches. POSIX shell expansion has a defined sequence including parameter expansion, field splitting, pathname expansion, and quote removal. Passing an argument vector to a process API avoids asking a shell to reinterpret data as command language.

Shell quoting is not a universal escape algorithm. A value inserted into a single-quoted shell word, double-quoted word, here-document, arithmetic expansion, command substitution, or nested remote command needs different reasoning. Concatenating `ssh host "command $value"` crosses local and remote parsing layers. The strongest design is to avoid a shell, pass an argument vector or structured protocol, and let the target program parse typed data. If a shell is required, fix one shell grammar and use a proven encoder for one word position—not for command fragments.

SQL values should use prepared statements or parameter binding. A quoted string escape does not safely construct identifiers, sort directions, operators, or whole clauses, and escaping rules vary by database modes and encodings. Keep the query structure static. Map a small external enum to reviewed SQL fragments when structure must vary, and bind all values through the driver. Authorization remains separate: a safely bound account ID does not prove the caller may query it.

Markup has several contexts. HTML text, quoted/unquoted attributes, URLs, CSS, JavaScript strings, and script bodies have different parsers and encoders. Encoding a value for HTML text and then inserting it into JavaScript is unsafe. Nested contexts can require ordered encodings, such as URL component encoding followed by HTML attribute encoding. Prefer APIs that construct DOM text nodes or set validated properties, and prohibit dynamic insertion into contexts for which safe encoding is not available.

Configuration templates are not automatically inert. YAML tags, anchors, folded strings, and implicit typing; JSON number/string distinctions; infrastructure expressions; CI interpolation; and deployment command fields can all introduce a second evaluation language. Quote insertion may change a scalar's type or remain insufficient if the consumer later passes it to a shell. Parse the rendered output with the exact consumer grammar, validate its schema, and inspect semantic fields before deployment.

Encoding must occur at the final context boundary. Encoding early can be undone by decoding, encoded again into visible garbage, or moved into a different context where it is ineffective. Store canonical data, not pre-escaped variants named vaguely `safe`. A value may be safe for HTML text and unsafe for a URL or script. Type wrappers such as `HtmlText`, `SqlValue`, or `ShellWord` can make the context explicit when they are constructed only by trusted encoders and cannot be confused.

Text generation also loses source structure. A compiler error at line 18,422 of a generated file is poor feedback when the defect came from one schema field. A durable generator maintains spans from output regions to template/model inputs, emits stable diagnostics before downstream parsing where possible, and records provenance. Generated output should be deterministic under declared inputs so diffs and caches remain meaningful.

Security review separates **data substitutions** from **directive substitutions**. A data placeholder must not alter parse structure. A directive placeholder intentionally controls syntax and therefore grants authority; it needs a closed vocabulary, authorization, provenance, review, and resource limits. Labeling an attacker-influenced value “template variable” does not keep it in the data plane if the consumer reparses it as code.

Testing needs multiple layers. Unit tests verify placeholder recognition, escaping, missing values, recursion, budgets, and diagnostics. Golden tests compare representative output but can approve the same mistake repeatedly. Parse/type checks prove output shape under the consumer. Behavioral tests exercise the generated artifact. Security tests insert delimiters, quotes, newlines, Unicode confusables, nulls where supported, path separators, shell metacharacters, and expansion markers. Differential tests compare structured construction with textual output. None alone proves domain validity.

The following executable example performs exactly one pass over explicit markers and never evaluates its output. It demonstrates four distinct hazards and one unknown-placeholder policy.

<!-- bijux-verify: {"id":"text-substitution-failures","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"precedence=a + b * a + b\nduplicate=next_value() + next_value()\ndelimiter=owner=Lee, Admin,role=editor\ninjection=run(\"safe\"); delete_all(); (\"\")\nmissing=hello {{unknown}}\n","stderr":""}} -->
```python
import re


marker = re.compile(r"\{\{([a-z]+)\}\}")


def substitute_once(template, bindings):
    values = dict(bindings)

    def replacement(match):
        name = match.group(1)
        return values[name] if name in values else match.group(0)

    return marker.sub(replacement, template)


print("precedence=" + substitute_once("{{x}} * {{x}}", (("x", "a + b"),)))
print("duplicate=" + substitute_once("{{x}} + {{x}}", (("x", "next_value()"),)))
print("delimiter=" + substitute_once("owner={{name}},role=editor", (("name", "Lee, Admin"),)))
print("injection=" + substitute_once("run(\"{{value}}\")", (("value", "safe\"); delete_all(); (\""),)))
print("missing=" + substitute_once("hello {{unknown}}", (("name", "Ada"),)))
```

The output establishes literal one-pass string behavior for five inputs. It does not execute the generated fragments, model C/C++ preprocessing, implement any safe encoder, or prove a shell, SQL, HTML, CSV, configuration, compiler, or deployment boundary secure.

## Definitions and Notation

Let \(T\in\Sigma^*\) be a template, \(N\) a set of placeholder names, and \(\rho:N\rightharpoonup\Sigma^*\) a partial replacement environment. A one-pass, non-rescanning expansion is

\[
S_1(T,\rho)=\text{the template with each recognized marker }m(n)\text{ replaced once by }\rho(n).
\]

The definition still requires a deterministic scan rule for overlapping markers and a policy \(U\in\{error,preserve,empty,default\}\) for \(n\notin dom(\rho)\).

A recursive expansion sequence is

\[
T_0=T,\qquad T_{i+1}=S_1(T_i,\rho),
\]

and terminates at a fixed point \(T_k=T_{k+1}\) or an engine-defined suppression state. Equality of adjacent strings is insufficient as a safety policy if output size or steps exceed budgets before the fixed point.

Let \(G_C\) be the grammar of receiving context \(C\), \(parse_C:\Sigma^*\rightharpoonup AST_C\), and \(Data_C(v)\) the intended syntax node representing data value \(v\). A contextual encoder owes

\[
parse_C(E_C(v))=Data_C(v)
\]

for every admitted \(v\), when the encoded fragment is parsed in exactly the promised context. In a larger template, the stronger noninterference obligation is that replacing one data node cannot introduce sibling or ancestor directives.

For an expression macro parameter \(x\), let \(occ_R(x)\) be the number of evaluated occurrences in replacement \(R\). If an argument expression has observable trace \(t\), substitution can repeat it \(occ_R(x)\) times subject to control flow. Single-evaluation preservation generally requires a binding, not merely parentheses.

Let provenance record

\[
\Pi=(template\ digest,input\ digests,engine\ version,options,environment\ policy,output\ digest,source\ map).
\]

Secrets are represented by redacted identity/digest under policy, not copied into logs.

## Mechanisms, Invariants, or Proof Structure

**Precedence counterexample.** Let replacement `x` be token sequence `a + b` and template `x * x`. Blind substitution yields `a + b * a + b`. Under conventional precedence it parses as `a + (b*a) + b`, not `(a+b)*(a+b)`. One example disproves universal expression-structure preservation.

**Parentheses limitation.** Replacing with `((x)*(x))` gives intended grouping for an admissible expression, but `occ_R(x)=2`. If `x=next_value()`, two calls remain. Grouping preservation and evaluation-count preservation are independent obligations.

**Context impossibility.** Suppose one universal escape function leaves alphanumeric text unchanged and claims safety in all contexts. A quote character must be encoded differently in an HTML attribute, JavaScript string, shell word, SQL literal, and URL component; encodings meaningful to one parser can be literal or control syntax to another. Therefore safety requires at least a named context and grammar, or a structured constructor that avoids textual reparsing.

**Rescan non-idempotence.** If \(\rho(a)=m(b)\) and \(\rho(b)=x\), then one pass over \(m(a)\) yields \(m(b)\), while two yield \(x\). Thus \(S_1(S_1(T,\rho),\rho)\ne S_1(T,\rho)\). Cache keys and tests must include rescan policy and step limits.

**Cycle argument.** If \(\rho(a)=m(b)\) and \(\rho(b)=m(a)\), naive recursive replacement alternates forever. A dependency-graph cycle is sufficient to reject expansion unless the engine has a formally specified suppression/quoting semantics that makes the cycle inert.

**Data/directive preservation.** Parameterized SQL sends query structure and bound values through separate protocol positions; an argument-vector API sends command and arguments as distinct array elements. These mechanisms establish a structural boundary that an identity string substitution lacks. They do not establish authorization or domain validity.

**Determinism obligation.** If output reads environment variable \(e\), then \(e\) is an input. Two expansions with equal declared inputs but different \(e\) can differ, refuting deterministic derivation. Either include a normalized identity for \(e\) in provenance/cache keys or prohibit the read.

## Alternatives and Trade-Offs

**Ordinary function versus token macro.** A function supplies parameter evaluation, scope, type checking, addressability, and debugger visibility. A token macro can operate before typing, generate declarations, or express conditional inclusion. Use the macro only for the phase or syntax capability the function cannot provide.

**Text template versus structured builder.** Text templates are readable when output is mostly fixed text and insertions occupy homogeneous data contexts. Builders and AST/DOM/configuration APIs enforce structure and context but can obscure the rendered result. Hybrid systems parse templates into typed nodes and constrain insertion categories.

**Escaping versus parameterization.** Correct contextual escaping can preserve data in markup or textual formats. Parameterization sends structure and values separately and is stronger for SQL and process invocation. It is unavailable for arbitrary identifiers or clauses, which should come from closed reviewed mappings rather than free text.

**One-pass versus recursive expansion.** One pass is easier to terminate, explain, and cache. Recursive expansion enables composition and indirection but needs quoting, cycle, ordering, and budget semantics. Do not add rescanning merely to make nested placeholders convenient.

**Unknown placeholder error versus preservation.** Failing early catches drift and misspellings. Preservation supports multi-stage templating where a later owner consumes markers, but every stage must use disjoint namespaces or explicit escaping and provenance. Silent empty replacement is safest only for fields declared optional with valid surrounding syntax.

**Checked-in versus generated output.** Checked-in text supports review and consumers without the generator but risks drift. Ephemeral output keeps one source of truth but requires reproducible tooling. Either policy needs deterministic regeneration, source mapping, and output validation.

**Directive substitution versus configuration data.** Directive substitution is maximally expressive but grants grammar control. Structured configuration narrows choices, validates earlier, and supports tooling. Prefer data models unless users genuinely need to author programs under a governed language.

## Failure Modes and Misconceptions

1. **“The C preprocessor is raw search-and-replace.”** It replaces preprocessing tokens under specified argument, stringizing, concatenation, and rescanning rules.
2. **“Token-based means syntax-safe.”** Flat tokens do not encode the final expression tree, binding graph, types, or effect count.
3. **“Parenthesize every parameter and the macro is safe.”** Parentheses do not prevent duplicate evaluation, capture, control transfer, or type problems.
4. **“A placeholder has one value.”** Rescanning, immediate/deferred expansion, environment changes, and phase placement can yield different results.
5. **“Unknown variables can become empty.”** Empty insertion can merge tokens, remove arguments, broaden paths, or produce valid unintended configuration.
6. **“Quoting is universal escaping.”** Grammar positions and nested parsers require different encoders or structured APIs.
7. **“Validation before escaping is enough.”** Encoding must match the final context, and validation cannot predict every future grammar interpretation.
8. **“Escaped means authorized.”** Syntax safety does not grant permission to access a record, execute an operation, or deploy a resource.
9. **“Templates are not code.”** Some templates contain expressions, imports, includes, or host calls and execute with generator authority.
10. **“Successful parsing proves safe output.”** The result can be syntactically valid, type-correct, and malicious or semantically wrong.
11. **“Golden output proves the generator.”** It covers selected cases and can preserve an approved defect.
12. **“Generated files need no source mapping.”** Users need diagnostics at the model/template location and reproducible provenance.
13. **“Secrets are safe if only the generator sees them.”** Expansion may embed them in artifacts, logs, caches, diffs, or diagnostics.
14. **“More expansion power is more reusable.”** Rescanning and arbitrary directives enlarge ambiguity, resource risk, and attack surface.

## Worked Examples

### Example 1

**Question:** Why does substituting `a+b` into `x*x` fail?

**Reasoning:** The engine copies tokens without an expression node. The target parser applies multiplication before addition, producing `a+(b*a)+b`. Parenthesizing the argument and whole replacement can preserve intended grouping for this expression category.

**Conclusion:** Textual adjacency is not expression composition.

### Example 2

**Question:** Does `((x)*(x))` make `SQUARE(next())` equivalent to a function call?

**Reasoning:** No. The expansion contains two `next()` calls. A normal function parameter is evaluated according to call semantics and the resulting value is reused inside the body. Parentheses change grouping, not occurrence count.

**Conclusion:** Single evaluation requires an explicit binding or ordinary call contract.

### Example 3

**Question:** Why is a C/C++ macro not accurately described as replacing arbitrary substrings?

**Reasoning:** The standard recognizes preprocessing tokens, identifies function-like invocations and arguments, treats literals as tokens, applies parameter replacement, stringizing and token concatenation, and rescans under defined rules. It still lacks final parsed and bound structure.

**Conclusion:** Token substitution is stronger than character replacement and weaker than syntax transformation.

### Example 4

**Question:** What happens when a one-pass engine inserts `{{b}}` as the value of `{{a}}`?

**Reasoning:** A strict one-pass engine leaves inserted markers inert, yielding `{{b}}`. A rescanning engine may expand again. If `b` references `a`, recursion can cycle. The template alone does not determine behavior without an engine policy.

**Conclusion:** Expansion order and rescanning are semantic configuration.

### Example 5

**Question:** Why can an unquoted shell variable turn one filename into several arguments?

**Reasoning:** After parameter expansion, the shell can perform field splitting and pathname expansion according to its grammar. Spaces create fields and wildcard characters can match filesystem entries. Supplying an argument vector bypasses that extra command-language interpretation.

**Conclusion:** A string value and one process argument are not the same representation.

### Example 6

**Question:** Can SQL quote doubling safely generate arbitrary queries?

**Reasoning:** It addresses one string-literal context under one dialect/mode. It does not safely represent identifiers, keywords, operators, clauses, encodings, or authorization. Prepared statements bind data values separately; reviewed enum mappings select any permitted structural variation.

**Conclusion:** Parameterize values and constrain syntax rather than constructing a query language from external text.

### Example 7

**Question:** Is HTML encoding sufficient for data inserted inside a script block?

**Reasoning:** No. The browser applies JavaScript parsing inside the block, and HTML entity behavior does not establish JavaScript string safety. Some locations are unsafe for dynamic insertion even with ad hoc encoding. Use a safe data transport and a script API that reads data, or avoid the context.

**Conclusion:** Encoding belongs to the final parser context.

### Example 8

**Question:** A deployment template leaves an unknown `${REGION}` marker intact. Is the failure harmless?

**Reasoning:** The consumer might reject it, accept it as a literal resource name, or pass it into yet another expansion phase. A governed generator should reject it at the originating location unless a declared later stage owns that namespace and the handoff is explicit.

**Conclusion:** Unknown markers are interface mismatches, not cosmetic warnings.

### Example 9

**Question:** How can a deterministic generator use environment configuration?

**Reasoning:** Declare an allowlisted configuration snapshot as input, normalize it, include its nonsecret values or digests in provenance/cache identity, prohibit undeclared reads, and emit the same bytes for equal inputs. Secret values should generally remain deployment-time data rather than be embedded.

**Conclusion:** Environment access is an input contract, not ambient convenience.

### Example 10

**Question:** A railway signaling configuration is generated from text templates. What evidence is required before use?

**Reasoning:** A generator reviewer must verify placeholder categories, missing-value failure, context encoders, determinism, limits, source maps, and output parsing. A signaling-domain reviewer must validate topology, routes, conflicts, timing, units, fail-safe states, and operational constraints. Security reviewers must assess input provenance, directive authority, secrets, toolchain isolation, and artifact signing. Independent safety and quality reviewers must trace requirements, hazards, tests, approvals, and deployment identity. Simulation and executable checks need boundary/adversarial cases but cannot replace named human certification. None is claimed here.

**Conclusion:** Correct rendering is only the first boundary in a safety-governed configuration pipeline.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) formalizes parsing, binding, evaluation order, effects, and contextual equivalence.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) supplies preprocessor, shell, process-argument, environment, and binary-boundary concerns.
- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) owns lexing, parsing, syntax trees, source spans, and downstream diagnostics.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) governs build templates, hermetic inputs, artifact provenance, and deployment validation.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies prepared statements, SQL dialect, identifier, transaction, and authorization contracts.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) treats data/directive boundary errors, command/code injection, least privilege, and supply-chain isolation.
- [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) applies template and configuration contracts to infrastructure plans and deployment manifests.

## References

1. ISO C++ working draft, [Macro replacement](https://timsong-cpp.github.io/cppwp/cpp.replace.general). Normative-style preprocessing-token, function-like macro, argument, and replacement rules.
2. GNU Project, [The C Preprocessor: Macro Pitfalls](https://gcc.gnu.org/onlinedocs/cpp/Macro-Pitfalls.html). Official documentation of misnesting, precedence, semicolon, side-effect duplication, and self-reference hazards.
3. The Open Group, [POSIX.1-2024 Shell Command Language, §2.6 Word Expansions](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html#tag_19_06). Authoritative expansion, field splitting, pathname expansion, and quote-removal order.
4. GNU Project, [GNU `make`: How `make` Reads a Makefile](https://www.gnu.org/software/make/manual/html_node/Reading-Makefiles.html). Official immediate, deferred, recursive, and phase-dependent expansion rules.
5. GNU Project, [GNU `m4` 1.4.20 Manual](https://www.gnu.org/software/m4/manual/m4.html). Official textual macro invocation, quoting, argument replacement, and rescanning semantics.
6. MITRE, [CWE-94: Improper Control of Generation of Code](https://cwe.mitre.org/data/definitions/94.html). Current data/directive and code-generation weakness classification and mitigations.
7. MITRE, [CWE-89: Improper Neutralization of Special Elements used in an SQL Command](https://cwe.mitre.org/data/definitions/89.html). Current SQL injection classification and parameterization guidance.
8. OWASP Foundation, [Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html). Current context-specific output-encoding and dangerous-context guidance.
9. SEI CERT C Coding Standard, [PRE00-C: Prefer inline or static functions to function-like macros](https://wiki.sei.cmu.edu/confluence/display/c/PRE00-C.+Prefer+inline+or+static+functions+to+function-like+macros). Authoritative engineering guidance on macro evaluation and type hazards.
10. Eugene Kohlbecker et al., [“Hygienic Macro Expansion”](https://doi.org/10.1145/319838.319859), LFP 1986. Primary research motivating binding-preserving structured macro expansion beyond textual substitution.

## Exercises

### Exercise 1

Expand `#define CUBE(x) x*x*x` for argument `a+1`, show the parse under ordinary precedence, and repair grouping. Then explain why the repaired macro is still unsafe for `CUBE(next())`.

### Exercise 2

Define one-pass and rescanning results for template `{{a}}` with `a={{b}}` and `b=done`. Then add `b={{a}}` and state a termination policy with explicit budgets.

### Exercise 3

Design a process-launch API that accepts executable path, argument list, environment map, and working directory without constructing a shell command. State how it handles spaces, wildcards, empty arguments, secrets, missing executables, and logging.

### Exercise 4

Design a typed web-template interface for HTML text, URL query values, and a JSON data block consumed by JavaScript. State which encoders/builders apply, which contexts are prohibited, how double encoding is prevented, and how tests exercise adversarial values.

### Exercise 5

Prepare a verification plan for a generator that produces database migration SQL from a schema model. Cover model validation, identifier policy, parameter versus directive boundaries, deterministic output, source mapping, transaction/rollback behavior, database dialect/version, hostile input, resource limits, security review, and the boundary between automation and named human approval.

## Answers to the Exercises

### Answer 1

Blind expansion yields `a+1*a+1*a+1`, parsed as `a + (1*a) + (1*a) + 1`, not \((a+1)^3\). A grouping repair is `#define CUBE(x) ((x)*(x)*(x))`, which expands to `((a+1)*(a+1)*(a+1))`. With `next()`, however, it contains three calls. Parentheses preserve expression grouping but not single evaluation, types, exceptions, or cost. An inline/generic function is the appropriate ordinary abstraction when compile-time token generation is unnecessary.

### Answer 2

One pass maps `{{a}}` to `{{b}}`; rescanning maps the second result to `done`. If `b={{a}}`, naive rescanning alternates between markers. A governed engine should build the reference graph, reject cycles with a path diagnostic, and also cap depth, replacement steps, output bytes, time, and memory for acyclic duplication. An engine with formal quote/suppression semantics may make a marker inert, but must test and document that exact rule.

### Answer 3

Accept an absolute or policy-resolved executable identifier and an array whose elements are already distinct strings. Call the operating-system process API directly, so spaces and wildcard characters remain within one argument and an empty string remains an empty argument. Accept an allowlisted environment map or inherit under an explicit policy; never log secret values, only redacted keys/digests. Validate working-directory policy and executable provenance, return structured spawn/exit/signal errors, impose time/resource limits, and log argument count plus safely redacted representations. No shell quoting or command string is involved.

### Answer 4

Use distinct types/constructors: an HTML-text encoder or DOM text node for body text; URL-component encoding for a query value followed by attribute construction by the HTML framework; and a standards-compliant JSON serializer for a non-executable data element with a content type and embedding rules that prevent closing the container. JavaScript reads and parses the data rather than receiving interpolated script source. Prohibit dynamic tag names, event-handler attributes, raw script bodies, and unvalidated URL schemes. Keep canonical unescaped data, brand encoded values by context, prevent constructors from accepting already encoded text, and test quotes, angle brackets, ampersands, slashes, Unicode separators, markup terminators, long inputs, and nested-encoding mistakes in a real parser/browser harness.

### Answer 5

Validate the schema as structured data: unique stable identifiers, supported types, nullability, defaults, dependency order, destructive-change classification, and dialect constraints. Render identifiers only through a dialect-aware identifier constructor under a conservative naming policy. Use bound parameters for runtime data; migration DDL structure is a privileged directive generated only from validated model variants. Pin generator, template, database dialect/version, options, locale, and model digest; normalize ordering and line endings; emit output digest and source maps from every statement to model fields.

Parse the output with the target dialect, execute it against disposable databases at supported versions, test upgrade from representative historical states, verify transactions where DDL supports them, and exercise rollback/forward-recovery for partial failure. Fuzz hostile names, quotes, comments, delimiters, Unicode confusables, deep dependency graphs, cycles, huge defaults, and output/resource limits. A named database reviewer must approve locking, data conversion, index cost, compatibility, backup, and recovery; a named security reviewer must approve authority and injection boundaries; an operations reviewer must approve rollout, observation, and rollback. Automation cannot establish business authorization, universal production data safety, or regulatory approval, and this answer claims no external review.
