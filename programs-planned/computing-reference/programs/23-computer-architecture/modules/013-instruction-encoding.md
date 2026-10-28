---
module_id: CA-013
program: Computer Architecture
level: 1
module_number: 13
title: Instruction Encoding
status: complete
last_verified: 2026-09-04
---

# Instruction Encoding

## One-Page Review

### Governing question

How can an ISA map instruction semantics and operands onto bit strings so hardware decodes unambiguously, tools emit and relocate correctly, extensions coexist, and malformed or unsupported encodings fail safely?

### Essential definitions

- An **instruction encoding** is a bit-string representation of an architectural operation and its operands.
- An **opcode** is a field or pattern that selects an operation class or decoding subtree.
- A **format** defines instruction length and the positions or derivations of fields.
- A **field** is a named set of encoding bits interpreted as a register index, function selector, immediate fragment or other attribute.
- A **decode mask** identifies constrained bits; a **match value** gives the required values under that mask.
- A **major opcode** selects a broad class; secondary function fields refine the operation.
- A **fixed-length encoding** gives ordinary instructions one size; a **variable-length encoding** permits multiple sizes.
- A **prefix-free boundary rule** lets a decoder determine instruction length without ambiguous consumption.
- A **canonical encoding** is the preferred or sole byte representation for a semantic instruction under stated rules.
- A **reserved encoding** is intentionally unassigned or constrained for future use.
- An **illegal encoding** is not a legal instruction in the active ISA/profile and must receive specified behavior.
- An **alias** is alternate assembly syntax, or sometimes an alternate encoding, associated with related semantics.
- A **relocation** records a link-time transformation of instruction fields whose final value is not yet known.
- **instruction endianness** governs how instruction bytes map into memory; field numbering governs bits within the decoded instruction word.
- A **decode collision** occurs when two simultaneously enabled definitions accept the same bit string without an intentional priority or equivalence rule.

### Central model, mechanism, or theorem

For active profile `P`, define partial functions

`Decode_P : Bytes x Address -> (Instruction, Length) or Illegal`

and

`Encode_P : Instruction -> Bytes`.

Sound round-trip behavior requires `Decode_P(Encode_P(I)) = I` for every canonical encodable instruction `I`, modulo explicitly normalized aliases. Decode determinism requires every aligned byte stream and enabled profile to yield at most one legal semantic instruction and length. Reserved, malformed and unsupported patterns follow an explicit illegal-instruction path without ordinary instruction side effects.

### Critical invariants

- Length is determined before the decoder consumes fields beyond the instruction.
- Simultaneously enabled mask/match patterns are disjoint or intentionally ordered and semantically justified.
- Every field slice, concatenation, sign bit, inserted bit and scale is exact.
- Encoder and decoder agree on register indices, immediates and canonical forms at every boundary.
- Instruction byte order and bit numbering are never conflated with data endianness.
- Reserved encodings cannot silently execute implementation-specific privileged actions.
- Extension allocation, discovery and profile composition preserve collision freedom.
- Assemblers, linkers, disassemblers, models and RTL are verified against the same versioned encoding source.

### Common failures

Frequent failures are treating assembly text as machine encoding, drawing fields from least significant bit on one page and most significant bit on another, forgetting that immediate fragments are reordered, sign-extending from the wrong bit, assuming instruction and data endianness are identical concepts, decoding by opcode alone, allowing wildcard masks to overlap, treating reserved patterns as no-ops, accepting disabled extensions, consuming bytes before validating length, assuming every semantic instruction has one spelling or one encoding, relocating a scaled displacement without alignment checks, letting assembler and disassembler share the same bug, and declaring a few round trips proof of decoder completeness.

### Compact example

In a RISC-V-style 32-bit I format, `addi x5,x6,-8` uses opcode bits `6:0=0x13`, destination bits `11:7=5`, function bits `14:12=0`, source bits `19:15=6`, and a 12-bit immediate `0xff8` in bits `31:20`, producing word `0xff830293`. Decoding extracts the fields and sign-extends bit 31 to recover `-8`. The byte sequence in little-endian instruction memory is `93 02 83 ff`; byte order does not reverse the bit positions inside the assembled 32-bit word.

### Connections

Instruction encoding connects ISA semantics, register operands, fetch alignment, decode hardware, assemblers, disassemblers, compilers, linkers, binary rewriting, extensions, formal models, security and compatibility.

## Governing Question

Semantics says what an instruction does; encoding says which bits request it. The boundary must serve hardware that wants regular fast decode, compilers that want expressive operands, and an ecosystem that must preserve binaries for decades.

The governing question is how to allocate finite bit space without ambiguity. Every convenient new field consumes something: opcode capacity, immediate range, register names, instruction density or decoder simplicity. Once deployed, an encoding becomes a compatibility obligation.

## Why This Matters

A decoder bug can transform untrusted bytes into the wrong operation or privilege effect. A relocation bug can branch to the wrong address only after linking. A collision between optional extensions can make the same binary mean two different things on supposedly compatible machines.

Encoding also shapes performance and energy. Fixed fields can shorten decode paths; compact instructions reduce fetch bandwidth; variable length can create boundary and predecode complexity. Those are implementation effects layered on an architectural byte contract.

Evidence must span the toolchain. An assembler/disassembler round trip can hide a shared error. Independent tables, executable semantics, RTL assertions, negative tests and real binary traces cover different failure classes.

## Prerequisites and Retrieval

Before studying this module, be able to:

- manipulate binary and hexadecimal fixed-width values;
- identify register, immediate and opcode operands;
- distinguish instruction syntax, encoding and semantics;
- explain sign extension, alignment and byte order;
- reason about a partial function and disjoint sets.

Retrieve ISA/profile/version; supported instruction lengths; fetch alignment; instruction byte order; bit-number convention; every format diagram; opcode and function allocations; mask/match tables; register field widths; immediate reconstruction rules; legality predicates; reserved/custom spaces; extension dependencies; discovery mechanism; aliases and canonicalization; assembler options; object attributes; relocation definitions; linker relaxation rules; disassembler policy; executable model; RTL decoder; architecture tests; generated encoding database; binary corpus; silicon errata; and exact tool/hardware revisions.

## Learning Objectives

After completing this module, you should be able to:

1. separate semantic operations, assembly syntax and binary encodings;
2. extract and assemble fixed-width instruction fields;
3. reconstruct contiguous and scattered immediates correctly;
4. compare fixed-length and variable-length encoding schemes;
5. prove mask/match decode patterns disjoint or intentionally prioritized;
6. explain reserved, illegal, custom and extension encoding spaces;
7. distinguish instruction byte order from field bit numbering;
8. analyze relocations, relaxation, aliases and canonical forms;
9. design independent encoder/decoder and negative-test evidence;
10. govern encoding changes without breaking binary compatibility.

## Core Exposition

### Separate three representations

An instruction has semantic identity, assembly representation and byte representation. One semantic operation may have aliases; one mnemonic may select different encodings based on operands or mode.

Write transformations explicitly: parse assembly to an instruction object, encode that object to bytes, decode bytes to an instruction object, and pretty-print it. Each boundary can normalize or reject input under documented rules.

### Establish bit-number convention

Architecture diagrams commonly number the least significant bit zero, but not universally. State the convention beside every format and in generated data.

A field labeled `31:20` means a slice of a decoded word, not twelve sequential bytes and not an instruction-memory order. Mixing notations creates plausible but wrong decoders.

### Determine length first

A variable-length decoder needs a rule that identifies length from an available prefix and address. The rule must handle truncated fetches, page boundaries and unsupported long forms.

Do not read arbitrary maximum length and then retroactively decide what counted. Memory faults on bytes beyond the actual instruction must not become architectural faults unless the fetch contract permits them.

### Compare fixed-length encodings

Fixed length simplifies indexing, alignment and parallel field extraction. Regular positions can reduce muxing and decode delay.

The cost is code density or limited field capacity. A fixed 32-bit word cannot simultaneously maximize opcode space, register count and immediate range.

### Compare variable-length encodings

Variable length assigns short encodings to common operations and longer forms to richer operands. It can improve cache and fetch efficiency.

It complicates instruction boundary discovery, branch targets, parallel decode and recovery after corruption. Length prefixes and predecode metadata become critical evidence surfaces.

### Design formats around common paths

Formats often keep register fields in stable positions across operation classes. This lets hardware begin register selection before all function bits resolve.

Scattered immediates may preserve those stable fields. The semantic cost is borne by assembler, decoder, relocation and verification logic, which must agree on reconstruction.

### Decode with mask and match

Represent a definition as `(word & mask) == match`, with the invariant `match & ~mask == 0`. A table can be generated into software and hardware forms.

The pattern alone may be insufficient. Mode, length, enabled extensions, register restrictions and reserved fields contribute legality predicates.

### Prove collision freedom

Two patterns collide when a word can satisfy both masks. A quick criterion is `((match_a ^ match_b) & (mask_a & mask_b)) == 0`; if true, constrained shared bits do not distinguish them and additional predicates require analysis.

Intentional priority is a semantic rule, not a substitute for review. Record why the more specific form wins and whether disabled extensions change resolution.

### Use decoding trees carefully

Hardware may decode a major opcode, then function and operand fields. Software may use generated tables or tries. These are implementations of the same accepted set.

An optimization that tests fewer bits must prove equivalent to the normative mask and legality predicate. Otherwise a reserved form can leak into a broad operation class.

### Encode register operands

An `n`-bit register field names up to `2^n` patterns, but not all patterns need be legal for every instruction. Specialized classes and compressed formats may use subsets or remapped “prime” registers.

The encoder must reject unavailable names rather than truncate an index. The decoder must distinguish an illegal name from a legal architectural register.

### Encode immediate operands

Define immediate formation as a pure bit-vector function: select fragments, concatenate in specified order, append implied low zeros, then sign- or zero-extend.

Range checking is the inverse obligation. The encoder or relocation must verify representability, required alignment and any forbidden values before discarding high or low bits.

### Understand scaling

Branch and load displacements may encode units larger than bytes. An implied low zero doubles signed range for a fixed field while restricting alignment.

Always distinguish encoded integer, scaled displacement and final address. Error messages and relocation records should identify which boundary failed.

### Handle signed immediates

For a `k`-bit signed field, valid values normally span `-2^(k-1)` through `2^(k-1)-1` before any scale. Encoding uses the low `k` bits of the two’s-complement value after range checking.

Decoding sign-extends from the semantic sign bit, which may be stored in a nonadjacent instruction position for scattered formats.

### Handle reserved fields

Reserved bits can require zero, one or a constrained value. They preserve future expansion and can distinguish related formats.

Ignoring reserved fields expands the accepted language of the decoder. Future extensions can then conflict with deployed implementations that treated those words as existing instructions.

### Distinguish illegal and unsupported

An encoding may be defined by the architecture but unavailable because an extension is disabled. For the active profile, it still follows the specified unsupported/illegal-instruction behavior.

Discovery must agree with decode enablement. Advertising an extension while rejecting its encodings, or accepting it while reporting absent, breaks software dispatch.

### Allocate extension space

Standard, reserved and custom spaces need ownership. A registry or machine-readable opcode repository reduces collisions across contributors.

Extension composition is a product-space problem: test every supported combination, including dependencies and exclusions. Collision freedom in isolation is insufficient.

### Treat aliases precisely

An assembly alias can map a familiar spelling to a base encoding. Disassemblers may print the alias or canonical base form according to policy.

If two encodings have identical semantics, state whether both are canonical, one is deprecated or one is merely tolerated. Binary rewriting depends on this distinction.

### Define canonicalization

Canonical encoding supports reproducible builds, signatures, hashing and stable disassembly. The encoder should select one permitted representation for a normalized instruction object.

Decoders may accept noncanonical but legal forms. Round-trip tests must therefore state whether they preserve bytes or normalize semantics.

### Separate bytes and fields

Instruction endianness maps addressed bytes into an instruction word. After assembly, field positions use the architecture’s bit numbering.

Do not “reverse each field” on a little-endian machine. For word `0xff830293`, increasing memory addresses hold `93`, `02`, `83`, `ff`, while opcode remains word bits `6:0`.

### Address alignment and boundaries

The ISA defines valid instruction-address alignment and how supported lengths affect it. A target can be aligned for a compressed instruction but not for a fixed 32-bit-only profile.

Fetch across cache lines or pages is an implementation problem with architectural fault consequences. Determine actual length and access permissions under the specified ordering.

### Integrate assemblers

An assembler parses operands, chooses a format, checks constraints and emits bytes plus relocations. Pseudo-instructions may expand into several real instructions.

Diagnostics are part of tool quality: out-of-range immediate, illegal register, disabled extension and ambiguous syntax should not silently truncate or choose a surprising form.

### Integrate object files

Object attributes record architecture and extension assumptions. Sections carry bytes; symbols and relocations describe values to resolve later.

The object format does not replace ISA encoding. It preserves enough intent for a linker to finish field construction without guessing from raw instruction bits.

### Apply relocations safely

A relocation defines how a symbol/addend-derived value maps into one or more instruction fields. It must specify PC base, rounding, pairing and overflow checks.

Split high/low sequences require linked consistency. Moving or relaxing one half without its partner can produce a plausible but incorrect address.

### Understand linker relaxation

Relaxation replaces a sequence with a shorter or more direct encoding when final distances allow. It changes bytes while preserving semantics under stated assumptions.

Debug information, exception tables, signatures and branch offsets must be updated. Disable relaxation where byte identity is itself part of an assurance artifact unless accounted for.

### Build disassemblers defensively

A disassembler should never overread the available buffer, and it must make illegal/truncated data visible. Choosing a mnemonic is presentation; identifying accepted length and semantics is architecture.

Security tooling should retain raw bytes and active profile because printed aliases can hide distinctions relevant to auditing.

### Generate from one reviewed database

A machine-readable source can generate masks, match values, field extractors, assembler tables and collision checks. Generation reduces manual drift.

It does not eliminate correlated errors. Review the source schema and compare at least one independent semantic model or decoder.

### Verify round trips

For legal canonical instructions, test decode-after-encode semantic equality. For accepted noncanonical bytes, test encode-after-decode against documented normalization.

Exercise boundary registers and immediates, every format, disabled extensions, reserved fields, truncated buffers and all instruction lengths.

### Verify negative space

The illegal space is often much larger than the legal space. Random words, targeted near misses and formal enumeration can prove broad masks do not accept reserved patterns.

Observe the architectural result: illegal trap with correct faulting address and no ordinary state effects. A decoder merely returning “unknown” is not full processor evidence.

### Compare independent implementations

Run binaries through assembler, disassembler, executable model, RTL and independent simulators. Compare decoded operation, operands, length and committed effects.

Independence matters. If all consumers import one faulty field map, agreement demonstrates consistency but not correctness against the normative specification.

### Analyze decode security

Malformed bytes are attacker-controlled in many systems. Decoder tables need bounds safety; hardware illegal paths need privilege and side-effect discipline.

Speculative decoding of illegal or cross-boundary bytes can also affect microarchitectural state. Functional trap correctness and side-channel analysis are separate evidence claims.

### Govern compatibility

Never reassign a deployed legal encoding to incompatible semantics within a compatible profile. Deprecation can change tool preferences while old binaries retain meaning.

Record extension version, opcode database revision, assembler/linker options, relaxation, binary digest, model, RTL and silicon revision. Errata remain attached to affected artifacts.

## Definitions and Notation

- `B`: finite byte sequence at an instruction address.
- `P`: active ISA profile, mode and enabled-extension set.
- `Decode_P(B,A)`: partial decode returning semantic instruction and length or `Illegal`.
- `Encode_P(I)`: canonical byte encoding of semantic instruction `I`.
- `word[h:l]`: inclusive bit slice after bytes are assembled into a word.
- `mask`, `match`: constrained-bit selector and required value.
- `legal(I,P)`: additional operand, mode and extension legality predicate.
- `len`: instruction length in bytes.
- `imm_enc`: integer represented directly by immediate field fragments.
- `disp`: scaled displacement used by semantics.
- `A`: instruction address.
- `target`: address derived from base and displacement.
- `Reloc(S,A,addend)`: link-time value transformation for symbol `S`.
- `canonical(I)`: selected representation for a normalized instruction.
- `Illegal`: architectural decoding outcome, not an ordinary no-op.

All hexadecimal instruction words use bit zero as the least significant bit. Byte sequences are listed in increasing memory-address order.

## Mechanisms, Invariants, or Proof Structure

1. **Length obligation:** prove every available byte prefix and profile selects at most one supported instruction length without overread.
2. **Bit-number obligation:** prove format diagrams, extractors and emitted bytes share one explicit bit convention.
3. **Pattern obligation:** prove each decoder tests every required opcode, function and reserved bit.
4. **Collision obligation:** prove simultaneously enabled patterns are disjoint or governed by reviewed semantic priority.
5. **Register obligation:** prove register fields encode and decode exactly the legal architectural names.
6. **Immediate obligation:** prove fragment concatenation, sign/zero extension, inserted bits and scaling are inverse within representable range.
7. **Range obligation:** prove encoder and relocation reject overflow, underalignment and forbidden values before truncation.
8. **Endian obligation:** prove memory bytes assemble to the intended word independently of field numbering and data-byte rules.
9. **Legality obligation:** prove reserved, malformed and disabled-extension patterns reach the specified illegal path.
10. **Canonical obligation:** prove every semantic instruction has a deterministic selected encoding and documented alias normalization.
11. **Relocation obligation:** prove symbol, addend, PC base, split fields, overflow and relaxation preserve intended values.
12. **Toolchain obligation:** prove assembler, linker and disassembler agree with the active profile and machine-readable attributes.
13. **Processor obligation:** prove decoded operation, operands and length drive the ISA-permitted transition or precise illegal trap.
14. **Independence obligation:** compare generated consumers with an independently derived model or normative-table audit.
15. **Lifecycle obligation:** bind specifications, opcode databases, tools, binaries, RTL, tests, hardware and errata to exact versions.

## Alternatives and Trade-Offs

1. **Fixed versus variable length:** fixed forms simplify boundaries; variable forms improve density.
2. **Uniform versus specialized formats:** uniform fields shorten common decode; specialization expands operand range.
3. **Large opcode versus large operands:** opcode capacity supports features; operand fields support registers and immediates.
4. **Contiguous versus scattered immediates:** contiguous fields simplify tools; scattered fields preserve common register positions.
5. **Explicit versus implied bits:** explicit bits increase flexibility; implied alignment extends range.
6. **Dense versus sparse allocation:** density conserves space; sparsity simplifies decode and future growth.
7. **Single-level versus hierarchical opcodes:** flat decode is direct; hierarchy partitions ownership and formats.
8. **Standard versus custom space:** standards maximize portability; custom regions enable product-specific operations.
9. **One encoding versus semantic aliases:** uniqueness aids reproducibility; aliases can improve density or compatibility.
10. **Strict versus permissive decoding:** strict rejection preserves future space; permissiveness may tolerate legacy binaries but creates ambiguity.
11. **Static versus profile-dependent legality:** static tables are simple; profiles support scalable optional features.
12. **Assembler expansion versus hardware operation:** pseudo-instructions save ISA space; native encodings may improve performance or atomicity.
13. **Link-time fixed code versus relaxation:** fixed bytes aid assurance; relaxation improves density and reach.
14. **Generated versus handwritten decoders:** generation reduces drift; independent handwritten logic can expose source errors.
15. **Canonical display versus friendly aliases:** canonical text exposes encoding identity; aliases improve readability.

## Failure Modes and Misconceptions

1. “A mnemonic uniquely identifies bytes.” Operands, mode, aliases and alternative lengths matter.
2. “Machine encoding is assembly without spaces.” Parsing and semantic selection intervene.
3. “Opcode bits alone identify every instruction.” Function, mode, length and legality fields refine decode.
4. “Field diagrams all number bits the same way.” The convention must be stated.
5. “Little endian reverses bits inside every field.” It orders addressed bytes, not semantic slices.
6. “Instruction and data endianness must match.” Architectures define these contracts independently.
7. “A 32-bit instruction always advances PC by four.” Length, control flow and traps determine PC.
8. “Variable length can be decided after full fetch.” Overread faults and boundaries make length ordering architectural.
9. “Wildcard decoder patterns are harmless.” Overlap can admit reserved or competing operations.
10. “The most specific pattern naturally wins.” Priority must be specified and verified.
11. “Unused bits are don’t-care bits.” They may be reserved for compatibility.
12. “Reserved encoding means no-op.” It normally follows illegal or constrained behavior.
13. “Unsupported extensions can be decoded anyway.” Discovery and execution must agree.
14. “Register fields accept every bit pattern.” Formats can restrict or remap names.
15. “Out-of-range registers safely truncate.” Truncation silently selects another register.
16. “Immediate bits always appear contiguously.” Many formats scatter or permute them.
17. “Sign extension starts at the instruction MSB.” It starts at the immediate’s defined sign bit.
18. “Dropping a low displacement bit loses information.” It is valid only with a proven alignment constraint.
19. “Relocations merely paste addresses into fields.” They apply bases, addends, scaling, pairing and overflow rules.
20. “Relaxation changes only performance.” It changes bytes, addresses and dependent metadata.
21. “Assembler-disassembler round trip proves correctness.” Shared tables can reproduce the same bug.
22. “Disassembly text preserves every binary distinction.” Aliases and normalization can hide bytes.
23. “Random legal tests cover illegal space.” Targeted near misses and reserved patterns are required.
24. “A software decoder returning unknown proves a precise trap.” Processor side effects and trap state remain untested.
25. “Extension patterns that work alone compose safely.” Cross-extension collisions can emerge.
26. “An erratum workaround redefines the encoding.” The affected silicon remains a documented deviation.

## Worked Examples

### Example 1

`add x3,x1,x2` in a RISC-V-style R format has word `0x002081b3`: opcode `0x33`, destination 3, function3 0, sources 1 and 2, and function7 0.

### Example 2

`addi x5,x6,-8` has word `0xff830293`; bits `31:20` contain two’s-complement `0xff8`, which sign-extends to `-8`.

### Example 3

Little-endian memory stores word `0xff830293` as bytes `93 02 83 ff`. Opcode extraction still applies to assembled word bits `6:0`.

### Example 4

Two patterns with masks `0x7f` and matches `0x13` and `0x33` cannot collide because constrained opcode bits differ. Patterns sharing `0x13` require function or legality separation.

### Example 5

A 12-bit signed immediate admits `-2048..2047`. Encoding 2048 by retaining low twelve bits would decode as `-2048`, so the encoder must reject it.

### Example 6

A branch encoding that omits displacement bit zero must reject odd byte targets. Appending zero during decode restores the aligned byte displacement.

### Example 7

A compressed format can remap a three-bit field onto registers 8 through 15. Treating it as names 0 through 7 is a format bug, not an ABI choice.

### Example 8

A disabled optional-extension word matches its registered bit pattern but is illegal for active profile `P`; decode enablement and discovery must agree.

### Example 9

A linker replaces a long address sequence with a shorter PC-relative form only after checking final distance, alignment and metadata updates.

### Example 10

An illegal near miss changes one reserved function bit in an otherwise legal add. A correct full mask rejects it; an opcode-only decoder may execute add incorrectly.

## Cross-Program Connections

- **Register operands:** field widths and remappings determine addressable register sets.
- **Datapaths:** stable field positions and decode outputs drive operand selection and control.
- **Fetch systems:** length and alignment determine boundary discovery and bandwidth.
- **Compilers:** instruction selection must choose representable operands and extensions.
- **Assemblers:** syntax, pseudo-operations, constraints and canonicalization produce bytes.
- **Linkers:** relocations and relaxation complete address-dependent fields.
- **Formal methods:** partial functions, disjoint patterns and round trips yield proof obligations.
- **Security:** malformed bytes, illegal paths and speculative decode are attack surfaces.
- **Compatibility:** allocated and reserved spaces govern binary longevity.
- **Systems engineering:** registries, generated artifacts, versions and errata govern the encoding lifecycle.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), base formats, field placement, immediates and opcode organization; retrieved 2026-09-04.
2. RISC-V International, [C Extension for Compressed Instructions](https://docs.riscv.org/reference/isa/unpriv/c-st-ext.html), 16-bit encodings, compact register mappings and variable-length composition; retrieved 2026-09-04.
3. RISC-V International, [RISC-V Opcodes Repository](https://github.com/riscv/riscv-opcodes), machine-readable encodings, masks, matches and collision checks; retrieved 2026-09-04.
4. GNU Binutils, [Using as](https://sourceware.org/binutils/docs/as/), assembler syntax, machine-dependent options, object emission and diagnostics; retrieved 2026-09-04.
5. LLVM Project, [llvm-mc](https://llvm.org/docs/CommandGuide/llvm-mc.html), machine-code assembly, disassembly and encoding inspection; retrieved 2026-09-04.
6. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), A64 instruction encoding, decoding and reserved behavior; retrieved 2026-09-04.
7. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), variable-length instruction formats, prefixes, opcodes and operands; retrieved 2026-09-04.
8. WebAssembly Community Group, [WebAssembly Binary Instructions](https://webassembly.github.io/spec/core/binary/instructions.html), binary opcode and immediate encoding for a typed virtual instruction set; retrieved 2026-09-04.

## Exercises

### Exercise 1

Decode R-format word `0x002081b3` and I-format word `0xff830293` into opcode, register, function and immediate fields.

### Exercise 2

Implement a small encoder/decoder for those `add` and `addi` formats, round-trip both words and reject an unsupported opcode.

### Exercise 3

Prove whether two mask/match definitions overlap, then extend the analysis with profile-dependent legality predicates.

### Exercise 4

Design negative tests for fixed 32-bit and optional compressed 16-bit encodings across buffer, alignment, reserved and disabled-extension boundaries.

### Exercise 5

Construct assurance for allocating and deploying a new arithmetic extension through specification, opcode registry, tools, RTL, verification and fielded hardware.

## Answers to the Exercises

### Answer 1

For `0x002081b3`, bits `6:0=0x33`, `11:7=3`, `14:12=0`, `19:15=1`, `24:20=2` and `31:25=0`, selecting `add x3,x1,x2`. For `0xff830293`, bits `6:0=0x13`, `11:7=5`, `14:12=0`, `19:15=6` and `31:20=0xff8`; 12-bit sign extension yields `-8`, selecting `addi x5,x6,-8`.

In little-endian memory, the words appear as `b3 81 20 00` and `93 02 83 ff`. Those byte sequences reconstruct the same words before field extraction.

### Answer 2

The following toy uses actual R- and I-format field positions for only two operations. It checks range before encoding and rejects every other opcode/function combination.

<!-- bijux-verify: {"id":"instruction-encoding-round-trip","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"word=0x002081b3 bytes=b3812000 decoded=add x3,x1,x2\nword=0xff830293 bytes=930283ff decoded=addi x5,x6,-8\nword=0x00000000 decoded=illegal\n"}} -->
```python
def encode_add(rd, rs1, rs2):
    assert all(0 <= r < 32 for r in (rd, rs1, rs2))
    return (rs2 << 20) | (rs1 << 15) | (rd << 7) | 0x33


def encode_addi(rd, rs1, immediate):
    assert 0 <= rd < 32 and 0 <= rs1 < 32
    assert -2048 <= immediate <= 2047
    return ((immediate & 0xFFF) << 20) | (rs1 << 15) | (rd << 7) | 0x13


def decode(word):
    opcode = word & 0x7F
    rd = (word >> 7) & 0x1F
    funct3 = (word >> 12) & 0x7
    rs1 = (word >> 15) & 0x1F
    if opcode == 0x33 and funct3 == 0 and (word >> 25) == 0:
        rs2 = (word >> 20) & 0x1F
        return f"add x{rd},x{rs1},x{rs2}"
    if opcode == 0x13 and funct3 == 0:
        immediate = (word >> 20) & 0xFFF
        if immediate & 0x800:
            immediate -= 0x1000
        return f"addi x{rd},x{rs1},{immediate}"
    return "illegal"


for word in (encode_add(3, 1, 2), encode_addi(5, 6, -8), 0):
    byte_text = word.to_bytes(4, "little").hex()
    if decode(word) == "illegal":
        print(f"word=0x{word:08x} decoded=illegal")
    else:
        print(f"word=0x{word:08x} bytes={byte_text} decoded={decode(word)}")
```

This establishes two round trips and one rejection only. It is not a complete RISC-V decoder and supplies no relocation, compressed-instruction, processor or conformance evidence.

### Answer 3

Two pure mask/match patterns overlap exactly when their jointly constrained bits do not disagree: `((ma ^ mb) & (maska & maskb)) == 0`, assuming each match has zeros outside its mask. If the expression is nonzero, at least one shared constrained bit requires opposite values, so no word satisfies both.

If patterns overlap structurally, prove their legality predicates mutually exclusive for every supported profile, or define and justify semantic priority. Repeat after every extension-set change. A solver or exhaustive enumeration over unconstrained fields can produce a witness word when overlap exists.

### Answer 4

Test empty and one-byte buffers; every truncated 16/32-bit prefix; instruction fetch at final bytes of accessible pages; aligned and misaligned addresses; legal compact and full forms; reserved quadrant/major opcodes; legal patterns with one reserved bit flipped; minimum/maximum registers and immediates; and disabled extensions. Verify exact consumed length, no buffer overread, correct fault priority and precise illegal trap without ordinary writes.

Cross cache/page boundaries and extension combinations. Fuzz raw bytes, but retain targeted witnesses and compare independent decoders. Bind results to instruction-endian mode, profile, model, RTL and hardware versions.

### Answer 5

Allocate from governed extension space and prove collision freedom against every supported standard, custom and reserved pattern. Freeze formats, mask/match values, operand legality, semantics, privilege, discovery, version and illegal behavior. Update the normative specification and machine-readable opcode database under review.

Generate assembler, disassembler and compiler support; define object attributes and relocations; implement RTL decode and executable semantics independently enough to expose correlated defects. Run round-trip, negative-space, cross-extension, formal decode and committed-trace tests. Preserve binary corpora and verify unsupported systems trap safely. Track tool, core and silicon adoption plus errata. Named ISA, registry, compiler, binary-tools, formal, RTL, verification, security, compatibility and independent-assurance authorities review their scopes. This module supplies no certification.
