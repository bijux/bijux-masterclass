---
module_id: COMP-002
program: Compilers & Language Implementation
level: 1
module_number: 2
title: Source Text, Encodings, and Position Tracking
status: complete
last_verified: 2026-08-29
---

# Source Text, Encodings, and Position Tracking

## One-Page Review

### Governing question

How can a language implementation turn source bytes into text while preserving exact, interoperable locations for lexing, diagnostics, editing, incremental updates, and generated-code provenance?

### Essential definitions

- A **byte sequence** is the file or transport payload before text interpretation.
- A **character encoding form** maps Unicode scalar values to code-unit sequences; UTF-8, UTF-16, and UTF-32 use 8-, 16-, and 32-bit code units respectively.
- A **Unicode code point** is an integer in the Unicode codespace; a **Unicode scalar value** excludes surrogate code points.
- A **grapheme cluster** approximates a user-perceived character and can contain multiple scalar values.
- A **source buffer** is an immutable or revision-identified byte sequence plus its decoding and file-identity contract.
- A **byte offset** identifies a boundary between bytes, usually zero-based in a source buffer.
- A **span** is a half-open interval $[start,end)$ in one declared coordinate system.
- A **line index** maps line-start byte offsets to line numbers and supports reverse lookup.
- A **display column** depends on tabs, grapheme segmentation, width policy, fonts, and rendering; it is not a stable storage coordinate.
- A **position encoding** states whether a protocol column counts UTF-8 code units, UTF-16 code units, Unicode scalar values, or another defined unit.

### Central model, mechanism, or theorem

Preserve a canonical source identity and byte-coordinate span:

$$
SourceId\times Revision\times [b_s,b_e).
$$

Decode bytes under an explicit policy to scalar values while retaining boundary maps. Derive consumer positions:

$$
byte\ offset\xrightarrow{line\ index}(line,byte\ in\ line)
\xrightarrow{decode}(line,column_{unit}).
$$

Conversions are partial: an offset inside a multibyte encoding sequence is not a scalar boundary; a protocol position can exceed a line or split a UTF-16 surrogate pair. Reject or repair only under an explicit contract.

### Critical invariants

- The original bytes, encoding decision, source identity, and revision remain recoverable while any span refers to them.
- Every stored span names its coordinate system and uses ordered in-bounds boundaries.
- Token and AST spans align to valid boundaries required by the language implementation.
- Newline recognition is defined independently from physical byte decoding.
- Line/column conversion is versioned with the source snapshot; stale positions never silently target a new revision.
- Normalization, newline folding, tab expansion, and replacement decoding never destroy origin mapping.
- Protocol peers negotiate or agree on one position encoding.
- Diagnostics distinguish physical source ranges from generated/expanded origin chains.

### Common failures

Common failures include calling bytes, code points, UTF-16 units, graphemes, and columns “characters”; indexing UTF-8 by scalar count; counting an emoji as one UTF-16 unit; treating CRLF as two lines; accepting ill-formed source with undocumented replacement; normalizing text before retaining origin offsets; measuring tabs with one fixed visual width; using one-based columns in a zero-based protocol; attaching a span to the wrong revision; and slicing source with a position from another encoding.

### Compact example

UTF-8 source $aé\n$ has four bytes, three scalar values, and one newline. The line-ending byte offset is 3, while the scalar column before the newline is 2. Offset 2 lies inside `é` and is not a valid scalar boundary. A diagnostic span stored as bytes $[1,3)$ can precisely recover `é`; the rendered column is a derived view.

### Connections

Retrieve [COMP-001's representation pipeline and provenance contract](001-language-implementation-pipelines.md). [COMP-003](../ROADMAP.md) consumes decoded source and spans to define tokens. This module connects to [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md), [Network Engineering](../../24-network-engineering/ROADMAP.md), and [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

What exactly is a source location when a file contains variable-width encodings, combining marks, tabs, mixed line endings, generated fragments, and concurrent editor revisions?

“Line 3, column 12” is not enough. Column 12 might mean bytes, UTF-16 code units, Unicode scalar values, grapheme clusters, terminal cells, or an editor-specific visual position. The same source can yield different numbers under each definition. A compiler needs stable slicing and provenance; an editor protocol needs negotiated positions; a human needs a useful rendered highlight. One representation should not pretend to satisfy all three without conversion.

## Why This Matters

Bad position accounting corrupts the interface between every front-end phase. A lexer token can slice the wrong bytes. A parser diagnostic can underline half an emoji. A rename operation can edit a combining mark but leave its base character. An incremental cache can reuse facts for the wrong revision. A macro error can point into generated text that the author cannot edit.

Encoding errors are also security and availability concerns. Ill-formed sequences, overlong inputs, bidi controls, visually confusable identifiers, extreme combining sequences, or adversarial line counts can stress tools and mislead reviewers. Correct handling does not mean banning international source. It means separating decoding, identifier policy, display, and security review under explicit versioned standards.

## Prerequisites and Retrieval

You should know bytes, arrays, binary and hexadecimal notation, strings, sorting and binary search, half-open ranges, immutable snapshots, and the pipeline in [COMP-001](001-language-implementation-pipelines.md). Retrieve:

1. A file is bytes until an encoding contract interprets it.
2. A Unicode scalar value may occupy multiple UTF-8 or UTF-16 code units.
3. Rendering depends on more than encoded text.
4. A half-open interval permits empty spans and composes without off-by-one overlap.
5. Cached metadata is valid only for the source revision from which it was derived.

## Learning Objectives

After completing this module, you should be able to:

- distinguish bytes, code units, code points, scalar values, grapheme clusters, glyphs, and display cells;
- specify a source decoding policy including BOM and malformed-input behavior;
- design immutable source identities and revision-bound half-open spans;
- construct and query a line-start index under a declared newline policy;
- convert byte offsets to UTF-8, UTF-16, and scalar columns safely;
- reject offsets that split an encoded scalar value;
- explain why normalization and newline folding need origin maps;
- negotiate editor-protocol position encodings and validate incoming ranges;
- represent macro/generated locations with origin chains;
- test source infrastructure against multilingual, malformed, large, and incremental cases.

## Core Exposition

### Start with source bytes

File APIs return bytes. A language specification or implementation policy decides how they become source characters. Some languages mandate UTF-8 and reject ill-formed input; others allow an encoding declaration, implementation-defined decoding, or a restricted source character set. Record the selected language version because source policies evolve.

Decoding should report the earliest offending byte range and avoid silently replacing malformed sequences unless replacement is explicitly part of an editor-recovery contract. Batch compilation commonly rejects malformed input. An IDE may preserve the bytes and surface a recoverable diagnostic so the user can repair the file. These modes can share a decoder but must not claim identical acceptance.

A byte-order mark is data whose treatment is language-specific. UTF-8 does not need a BOM for byte order. A source policy may remove a leading U+FEFF, reject it elsewhere, or treat it as content. Do not strip arbitrary occurrences. If a transformation removes a BOM, record the physical-to-logical offset mapping.

### Separate Unicode units

The Unicode codespace contains code points; scalar values exclude the surrogate range. UTF-8 encodes a scalar in one to four 8-bit code units. UTF-16 uses one 16-bit code unit for Basic Multilingual Plane scalars and a surrogate pair for supplementary scalars. Therefore “length” requires a unit.

The string $e\u0301$ contains two scalar values—a base letter and combining acute accent—but normally one extended grapheme cluster under Unicode text-segmentation rules. Precomposed `é` contains one scalar. The strings can be canonically equivalent without being byte-identical. An emoji family can contain several scalars joined into one extended grapheme cluster. A font can render multiple graphemes as one glyph or one grapheme with multiple glyphs.

Compilers commonly use bytes or code units as canonical offsets because slicing and storage are direct. Human-facing cursor motion may use extended grapheme clusters. Terminal or editor display columns additionally depend on tab stops, East Asian width, emoji presentation, control characters, bidi layout, font shaping, and policy. Preserve the stable coordinate and derive the presentation.

### Source identity, snapshots, and spans

A durable span is not merely two integers. Use

$$
Span=(source\_id,revision,start,end,unit),
$$

with $0\le start\le end\le length_{unit}(source)$. The unit is often fixed to bytes inside one compiler, but external APIs should still document it. An empty span represents insertion points and zero-width synthetic tokens.

Source IDs distinguish physical files, virtual editor buffers, generated sources, command-line snippets, macro expansions, and embedded languages. Avoid using a path as the only identity: paths can be renamed, reused, case-folded, or mapped through workspaces. The source manager can associate a stable internal ID with URI/path metadata and content digest.

Immutable snapshots make positions meaningful under edits. An edit creates a new revision; it does not mutate what an old diagnostic span denotes. A client may translate spans through an edit history, but translation is partial when text was deleted or ambiguously replaced. Tag every request and response with the applicable document version where the protocol permits.

Half-open intervals simplify adjacency: tokens $[0,3)$ and $[3,4)$ share a boundary without overlap. Length is $end-start$. Containment and intersection are well-defined, and an EOF span can be $[n,n)$.

### Newlines and line indexes

Define which sequences terminate a source line. Common policies recognize LF, CRLF as one terminator, and possibly lone CR or additional Unicode separators. The lexical grammar may treat newline characters differently inside comments or string literals, but physical line indexing typically scans the whole source independently so diagnostics remain total.

Store `line_starts = [0, ...]` as sorted byte offsets. When a recognized terminator ends, append the next byte offset if it is within or exactly at EOF according to the chosen empty-final-line policy. To locate byte offset $b$, binary-search the greatest line start $\le b$. This yields a zero-based line and byte-in-line.

Decide whether a file ending in a newline has a final empty line. Many editor protocols model the position after the terminator as the start of another line. Whatever the choice, make round trips and EOF behavior consistent.

Line indexes cost $O(n)$ to build and $O(\log L)$ per lookup for $L$ lines. Sequential lexing can track line state in $O(1)$ per consumed unit, but random diagnostics and IDE queries still benefit from an index. Incremental indexes can update affected regions, provided clean-rebuild equivalence is tested.

### Column conversion

From line start $s$ to byte offset $b$, validate that both are encoding boundaries and decode the slice. A UTF-8 protocol column is the count of UTF-8 code units—equivalent to bytes for valid UTF-8. A scalar column counts decoded scalar values. A UTF-16 column sums one for BMP scalars and two for supplementary scalars.

Conversion in the opposite direction must reject a requested column that lands inside a multibyte UTF-8 sequence or UTF-16 surrogate pair. Clamping can be appropriate for a rendering convenience, but it must not silently alter a source edit. Protocol ingestion should fail predictably or follow its specified recovery rule.

LSP illustrates why this matters. Modern clients and servers can advertise supported position encodings; historical/default behavior uses UTF-16 units. A server using UTF-8 byte columns internally must convert at its protocol boundary and include the negotiated encoding in session state. Never infer the peer's unit from observed ASCII-only files.

### Normalization, identifiers, and origin maps

Unicode normalization maps canonically or compatibility-equivalent sequences into declared forms. It changes code-unit sequences and therefore offsets. A language may normalize identifiers for comparison, restrict them according to Unicode identifier profiles, or preserve spellings while comparing a canonical form. These are language semantics, not a generic decoder decision.

Retain the original source spelling and byte span even if name resolution uses a normalized key. Diagnostics, formatting, refactoring, and security review need both. A normalization origin map relates output boundaries to source intervals; mapping can be one-to-many or many-to-one.

Security policies may flag mixed scripts, confusables, default-ignorable characters, or bidi controls. Such checks depend on Unicode version and language context. A code point being permitted by a Unicode identifier profile does not prove that a specific language accepts it or that two identifiers are safe to present indistinguishably.

### Tabs, width, and rendered diagnostics

Logical columns should not bake in display width. A tab advances to a configured tab stop based on the current display column. Combining marks may add no independent cell; wide characters may use two cells in some environments; emoji and bidi text vary by renderer. Diagnostics should carry source spans and let the renderer calculate a best-effort highlight under a documented width policy.

For terminal excerpts, sanitize or visibly escape control characters that could move the cursor, alter direction, or forge output. Preserve the original text separately. The renderer should cap line length and combining sequences to avoid denial of service while indicating truncation honestly.

### Generated and expanded source

Macros, preprocessors, templates, and embedded languages create positions not directly owned by one physical file. Model a generated span plus an origin chain: invocation span, definition/template span, input-model location, and transformation identity. Choose a primary location based on who can fix the defect; retain related locations for explanation.

An origin map need not force one generated byte to exactly one source byte. Synthetic punctuation can point to an insertion anchor; duplicated expansions can share one origin; combined tokens can cite multiple spans. The invariant is honest provenance, not invented precision.

### Incremental edits and protocol boundaries

An edit range arrives in a protocol unit and document version. Validate version, convert both endpoints to canonical byte boundaries against that exact snapshot, verify ordering, then apply the replacement to form a new immutable revision. Update or rebuild the line index. Do not convert against already-mutated text.

Multiple edits can be specified relative to the same original document or applied sequentially; protocols differ. Sort/rebase only as the protocol defines. Overlapping edits, stale versions, split encodings, and out-of-range positions require explicit errors rather than guessed intent.

### Verification strategy

Property tests should round-trip every valid boundary:

$$
byte\to(line,column_u)\to byte.
$$

Test ASCII, every UTF-8 length, supplementary UTF-16 pairs, combining sequences, ZWJ emoji, RTL text, tabs, NUL policy, BOM, LF/CRLF/CR, empty source, final newline, very long lines, many lines, and malformed sequences. Mutation tests should reveal off-by-one and CRLF-splitting defects.

Differential tests can compare decoding and Unicode segmentation against version-matched conformance data. Clean and incrementally updated line indexes must answer identically. Fuzz byte input with strict resource limits. Validate spans at subsystem boundaries; debug assertions alone are insufficient for untrusted protocol positions.

The following deterministic model stores UTF-8 byte offsets, indexes LF and CRLF, and derives scalar and UTF-16 columns. It intentionally rejects a byte inside a UTF-8 scalar. It does not implement grapheme segmentation, display width, normalization, incremental edits, or a complete editor protocol.

<!-- bijux-verify: {"id":"source-position-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bytes=12 line_starts=0,4,11\nbyte=0 line=0 utf8=0 scalar=0 utf16=0\nbyte=3 line=0 utf8=3 scalar=2 utf16=2\nbyte=5 line=1 utf8=1 scalar=1 utf16=1\nbyte=9 line=1 utf8=5 scalar=2 utf16=3\nbyte=11 line=2 utf8=0 scalar=0 utf16=0\nbyte=2 invalid=utf-8 continuation boundary\n","stderr":""}} -->
```python
text = "aé\nx😀\r\nz"
source = text.encode("utf-8")

line_starts = [0]
index = 0
while index < len(source):
    if source[index:index + 2] == b"\r\n":
        index += 2
        line_starts.append(index)
    elif source[index:index + 1] in (b"\n", b"\r"):
        index += 1
        line_starts.append(index)
    else:
        index += 1

def position(byte_offset):
    prefix = source[:byte_offset]
    try:
        prefix.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("utf-8 continuation boundary") from error
    line = max(i for i, start in enumerate(line_starts) if start <= byte_offset)
    segment = source[line_starts[line]:byte_offset].decode("utf-8")
    utf16 = len(segment.encode("utf-16-le")) // 2
    return line, byte_offset - line_starts[line], len(segment), utf16

print(f"bytes={len(source)} line_starts=" + ",".join(map(str, line_starts)))
for byte_offset in (0, 3, 5, 9, 11):
    line, utf8, scalar, utf16 = position(byte_offset)
    print(f"byte={byte_offset} line={line} utf8={utf8} scalar={scalar} utf16={utf16}")
try:
    position(2)
except ValueError as error:
    print(f"byte=2 invalid={error}")
```

## Definitions and Notation

Let source bytes be $B=b_0\ldots b_{n-1}$. Byte boundaries are integers $[0,n]$. A span $[i,j)$ denotes bytes $b_i\ldots b_{j-1}$, with $0\le i\le j\le n$.

Let $D_E$ be partial decoder for encoding $E$. $D_E(B)$ either yields scalar sequence $S$ plus boundary information or a decoding error with causal byte span. Let $L=[\ell_0,\ldots,\ell_{k-1}]$ be strictly increasing line starts with $\ell_0=0$.

For valid boundary $b$, $line(b)=\max\{q\mid \ell_q\le b\}$. A position under unit $u$ is $P_u(b)=(line(b),count_u(B[\ell_{line(b)}:b]))$.

An origin relation $O\subseteq Span_{generated}\times Span_{source}$ permits one-to-many provenance. A function is insufficient when generated content combines or duplicates origins.

## Mechanisms, Invariants, or Proof Structure

**Boundary proof.** A stored UTF-8 token span is sliceable only if both endpoints are zero, EOF, or not continuation bytes and strict decoding has established well-formedness. Rejecting offset 2 in the model demonstrates one causal case, not a universal decoder proof.

**Line lookup proof.** Since $L$ is sorted, the predecessor line start exists because $\ell_0=0$ and is unique. CRLF must be consumed as one terminator before checking single CR or LF.

**Round-trip invariant.** For every canonical valid byte boundary $b$, conversion $Q_u(P_u(b))=b$, where $Q_u$ rejects non-boundary columns. Tests must cover every supported unit.

**Snapshot invariant.** A span with revision $r$ may be dereferenced only against content revision $r$ or after an explicit validated translation.

**Origin invariant.** Every diagnostic over generated text has a generated span and at least one honest source/transformation origin or is explicitly labeled synthetic/internal.

**Resource invariant.** Decoding, indexing, conversion, and rendering enforce byte, line, nesting, expansion, and output limits without changing accepted semantics below the limits.

## Alternatives and Trade-Offs

**Byte offsets versus code-unit offsets.** Bytes align with UTF-8 storage and hashing. UTF-16 units align with some runtimes and historical protocols. Either works internally if declared and converted safely; bytes are often the simplest canonical file coordinate.

**Eager versus lazy line indexes.** Eager indexing gives predictable queries and costs one scan. Lazy indexing reduces work for unused files but complicates concurrency and latency. Incremental indexing improves editor performance with a larger correctness surface.

**Strict rejection versus recovery decoding.** Batch compilation benefits from strict deterministic rejection. Editors need continued service over temporarily malformed buffers. Preserve bytes and mark recovered regions so acceptance is never confused.

**Normalization versus spelling preservation.** Normalized keys simplify defined equality. Original spellings preserve diagnostics and round trips. Strong designs retain both with origin mapping.

**Grapheme versus scalar cursoring.** Grapheme navigation is closer to user perception and version-sensitive. Scalar or code-unit positions are simpler protocol coordinates. UI semantics and storage semantics need not match.

## Failure Modes and Misconceptions

1. **Unicode code point means character on screen.** Grapheme and rendering behavior can combine several points.
2. **UTF-8 offset equals scalar index.** It does only through ASCII prefixes.
3. **UTF-16 column equals code-point column.** Supplementary scalars consume two units.
4. **CRLF contains two line breaks.** A declared CRLF policy normally treats it as one terminator.
5. **Normalizing identifiers is offset-neutral.** Normalization can change code-unit count.
6. **Tabs have intrinsic width.** Their visual advance depends on current column and policy.
7. **A path uniquely identifies source.** Revisions, virtual buffers, generated files, and renames disprove this.
8. **Clamping a bad position is harmless.** It can edit a different token or split user text.
9. **A diagnostic needs only a primary range.** Macro and generated failures often need origin chains.
10. **ASCII tests validate Unicode positions.** All common coordinate systems coincide on ASCII and hide the defect.

## Worked Examples

### Example 1

**Question:** Count units in `A😀é` encoded as UTF-8.

**Reasoning:** There are three scalar values. UTF-8 uses 1+4+2=7 bytes. UTF-16 uses 1+2+1=4 code units. Typical extended grapheme segmentation yields three clusters.

**Conclusion:** “Length 3” is meaningful only after naming scalar or grapheme units.

### Example 2

**Question:** Is UTF-8 byte offset 2 valid in `aé`?

**Reasoning:** `a` occupies byte 0; `é` occupies bytes 1 and 2. Boundaries are 0,1,3. Offset 2 is a continuation-byte position.

**Conclusion:** Reject the offset rather than slicing invalid UTF-8.

### Example 3

**Question:** Build line starts for bytes representing $a\r\nb\n$.

**Reasoning:** Start with 0. Consume CRLF as one terminator and append 3. Consume LF after `b` and append 5. Under a final-empty-line policy the starts are [0,3,5].

**Conclusion:** Newline and EOF policies determine the index contract.

### Example 4

**Question:** Convert the position after emoji in line `x😀`.

**Reasoning:** From line start, UTF-8 count is 1+4=5, scalar count is 2, and UTF-16 count is 1+2=3.

**Conclusion:** One physical boundary has several correct external columns.

### Example 5

**Question:** Why store $e\u0301$ rather than normalize it before lexing?

**Reasoning:** A language may define normalized identifier comparison, but diagnostics and edits must address original bytes. Normalizing first changes two-scalar spelling and offsets; retain source and derive a comparison key with an origin relation.

**Conclusion:** Semantic normalization and source preservation are compatible layers.

### Example 6

**Question:** An LSP client sends line 0, character 3 for `x😀`. What byte boundary is that?

**Reasoning:** Under UTF-16, character 3 is after `x` and the surrogate pair, hence UTF-8 byte offset 5. Under UTF-8 units it would point inside the emoji. The negotiated session encoding decides.

**Conclusion:** Never interpret a protocol column without its position encoding.

### Example 7

**Question:** Can an old diagnostic span be used after inserting a byte before it?

**Reasoning:** Not directly. Its revision names old content. Translation through the exact edit can shift the range, but deletion or overlapping replacement may invalidate it.

**Conclusion:** Snapshot identity prevents stale-location corruption.

### Example 8

**Question:** Where should a macro-generated type error point?

**Reasoning:** The generated node has an expansion span; the actionable primary location is often the invocation argument. Related locations can cite macro definition and generated fragment, with an expansion trace.

**Conclusion:** Provenance is a relation, not a fabricated one-to-one offset.

### Example 9

**Question:** A medical configuration compiler highlights a dose unit using verified byte spans. Is the diagnostic clinically safe?

**Reasoning:** Correct spans prove location mechanics only. Unit semantics, schema validity, clinical bounds, generated-code trace, deployment identity, and fail-safe behavior remain. No external academic, clinical, regulatory, or practitioner review is claimed. Named qualified humans must review requirements, terminology, transformations, tests, hazards, and applicable assurance before use.

**Conclusion:** Exact source provenance is necessary but not clinical validation.

### Example 10

**Question:** How should a terminal diagnostic render a line containing bidi controls and thousands of combining marks?

**Reasoning:** Keep the original span, show a bounded sanitized excerpt with controls visibly escaped or annotated, cap rendering work, and report truncation. Offer raw/code-point detail separately.

**Conclusion:** Safe rendering can preserve evidence without executing text as terminal control.

## Cross-Program Connections

- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns byte-safe decoding, slices, and revision storage.
- [Metaprogramming](../../06-programming-languages-metaprogramming/ROADMAP.md) requires expansion and generated-source origin chains.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies property, fuzz, conformance, and mutation evidence.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) faces analogous encoding, collation, normalization, and offset contracts.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) transports protocol positions and encoded source snapshots.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) reviews confusables, controls, malformed input, and diagnostic spoofing.

## References

1. Unicode Consortium. [The Unicode Standard, Version 17.0.0](https://www.unicode.org/versions/Unicode17.0.0/), September 2025; especially Core Specification Chapters 2, 3, and 5. Consulted 2026-08-29.
2. Unicode Consortium. [Unicode Standard Annex #29: Unicode Text Segmentation, Revision 47](https://unicode.org/reports/tr29/), Unicode 17.0.0, 2025-08-17. Consulted 2026-08-29.
3. Unicode Consortium. [Unicode Standard Annex #15: Unicode Normalization Forms](https://unicode.org/reports/tr15/). Unicode 17.0.0 edition consulted 2026-08-29.
4. Unicode Consortium. [Unicode Standard Annex #31: Unicode Identifiers and Syntax](https://unicode.org/reports/tr31/). Unicode 17.0.0 edition consulted 2026-08-29.
5. Microsoft. [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/), position and position-encoding definitions; site reports latest specification 3.18 on 2026-08-29.
6. The Rust Project. [The Rust Reference: Input Format](https://doc.rust-lang.org/reference/input-format.html). Consulted 2026-08-29.
7. Python Software Foundation. [Python 3.14 Language Reference: Lexical Analysis](https://docs.python.org/3/reference/lexical_analysis.html). Consulted 2026-08-29.
8. Aho, Alfred V., Monica S. Lam, Ravi Sethi, and Jeffrey D. Ullman. *Compilers: Principles, Techniques, and Tools*, 2nd ed. Addison-Wesley, 2007.

## Exercises

### Exercise 1

For $é😀\n$ in UTF-8, list byte, scalar, UTF-16, and likely extended-grapheme counts before the newline.

### Exercise 2

Design a line-start index for $a\r\nb\rc\n$ under a policy recognizing CRLF, lone CR, and LF. Include the final empty line.

### Exercise 3

An editor sends UTF-16 position (0,2) for line `😀x`. Convert it to a UTF-8 byte offset and explain why position (0,1) must be rejected for an exact edit.

### Exercise 4

Compare storing canonical byte spans with storing line/column pairs for an incremental compiler. Address slicing, edits, conversion cost, stale positions, and protocol interoperability.

### Exercise 5

Design the source-location assurance review for a railway configuration compiler that accepts multilingual identifiers, expands templates, and sends diagnostics through LSP. Separate automated evidence from named human review.

## Answers to the Exercises

### Answer 1

Before the newline, `é` uses two UTF-8 bytes, one scalar, one UTF-16 unit, and one likely extended grapheme. `😀` uses four UTF-8 bytes, one scalar, two UTF-16 units, and one likely extended grapheme. Totals are six UTF-8 bytes, two scalars, three UTF-16 units, and two extended grapheme clusters. The newline adds one byte/scalar/UTF-16 unit but is excluded by the question.

### Answer 2

Start at byte 0. `a` occupies 0; CRLF occupies 1–2, so append 3. `b` occupies 3; lone CR at 4 ends the line, append 5. `c` occupies 5; LF at 6 ends it, append 7. The starts are [0,3,5,7], where 7 denotes the final empty line at EOF. A scanner must test CRLF before lone CR.

### Answer 3

`😀` is two UTF-16 code units and four UTF-8 bytes. UTF-16 position (0,2) is immediately after it, so the canonical byte offset is 4. Position (0,1) lies between its surrogate units and has no Unicode-scalar/UTF-8 boundary. An exact edit must reject it rather than guess before or after the emoji.

### Answer 4

Byte spans directly slice immutable UTF-8 buffers, compose as half-open ranges, and remain compact. A line index derives human/protocol positions when needed. Line/column pairs require a unit and newline policy, are slower to turn back into slices, and are especially ambiguous across UTF encodings. Both become stale after edits unless revision-tagged; neither should be silently reused. Canonical revision-bound bytes plus negotiated boundary conversion centralizes validation. The trade-off is conversion/index cost, mitigated by line-start and per-line caches whose revision is explicit.

### Answer 5

Automation validates strict decoding, BOM policy, Unicode-version-pinned identifier rules, normalization origin maps, confusable/control diagnostics, every valid UTF-8/UTF-16 round trip, CRLF/CR/LF behavior, revision rejection, template origin chains, negotiated LSP encodings, malformed/split positions, resource limits, deterministic rebuilds, and diagnostic snapshot tests. Fuzzing covers hostile byte input and extreme combining/bidi cases; integration tests trace one source identifier through expansion to generated artifact.

Automated location correctness does not prove railway terminology, configuration semantics, safe defaults, hazard coverage, operator comprehension, generated behavior, timing, deployment identity, or compliance. No external academic, railway, regulatory, or practitioner review is claimed. Named qualified humans must review the language and identifier policy, template transformations, requirements trace, hazards, human-factors rendering, tool qualification evidence, deployment controls, and applicable railway assurance obligations.
