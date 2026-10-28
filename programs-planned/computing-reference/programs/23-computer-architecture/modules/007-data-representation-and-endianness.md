---
module_id: CA-007
program: Computer Architecture
level: 1
module_number: 7
title: Data Representation and Endianness
status: complete
last_verified: 2026-09-04
---

# Data Representation and Endianness

## One-Page Review

### Governing question

How can hardware and software agree on the meaning of bits across registers, memory, instructions, files, networks, devices and heterogeneous machines without confusing abstract values with their stored or transmitted encodings?

### Essential definitions

- A **representation** maps an abstract value or state into one or more bit patterns under a declared interpretation.
- A **bit** is a binary digit; a **byte** is the architecture or format's addressed group, conventionally eight bits in modern interfaces.
- A **word** is an architecture-dependent natural data unit and does not imply one portable byte count.
- **endianness** specifies how significance-ordered bytes of a multibyte scalar map to increasing byte addresses or stream positions.
- **little-endian** stores the least-significant byte at the lowest address; **big-endian** stores the most-significant byte there.
- **bit numbering** labels bit positions within a field or register and is separate from byte endianness.
- **alignment** constrains an object's address relative to its size or ABI requirement; **padding** occupies layout space that is not a declared member value.
- **sign extension** and **zero extension** widen signed two's-complement and unsigned values respectively.
- An **object representation** is the stored bytes of a typed object; its mathematical value may not determine every padding or NaN payload bit.
- A **serialization format** defines a stable byte sequence independent of native in-memory layout.
- A **canonical encoding** selects one allowed representation for deterministic comparison, hashing or signing.
- A **tagged or self-describing representation** carries type or format information; an untagged representation depends on external schema.

### Central model, mechanism, or theorem

For bytes `b_0 ... b_(n-1)` in increasing address order, unsigned decoding is

`little = sum(b_i * 256^i)` and `big = sum(b_i * 256^(n-1-i))`.

The bytes `01 02 03 04` therefore decode as `0x04030201` little-endian and `0x01020304` big-endian. Neither byte sequence nor integer has an intrinsic endianness without a storage/transfer mapping and interpretation. Safe boundaries specify width, byte order, signedness, alignment, field layout, validity, version and error behavior explicitly.

### Critical invariants

- Abstract value, type, encoded bits, byte sequence and address layout are named separately.
- Every multibyte interchange field has fixed width, byte order and signed or unsigned interpretation.
- Loads and stores respect architectural alignment, access width, atomicity and fault rules.
- Widening and narrowing use declared signedness before any information is discarded.
- Struct padding, bit-field allocation and native pointers never leak into portable wire or disk formats accidentally.
- Parsers validate length, offset, tag, version, range, alignment and arithmetic before access or allocation.
- Canonicalization occurs before hashing or signing and rejects alternate encodings when uniqueness is required.
- Dumps, traces and debugger views record architecture, ABI, format and acquisition context.

### Common failures

Frequent failures are calling a value little-endian, reversing bits instead of bytes, assuming word means 32 bits, reading unaligned bytes through a typed pointer, serializing a native struct, relying on compiler bit-field order, sign-extending an unsigned value, zero-extending a negative value, applying byte swap twice, mixing host and protocol order in arithmetic, assuming instruction and data endianness always match, treating UTF-8 code units as characters, hashing noncanonical encodings, trusting length-plus-offset arithmetic that overflowed, and interpreting a memory dump without the target architecture and type layout.

### Compact example

Memory addresses 100 through 103 contain bytes `01 02 03 04`. A 32-bit little-endian load returns `0x04030201`; a big-endian load returns `0x01020304`. Storing either decoded value back with the same byte-order rule reproduces the original bytes. Reversing bit order within each byte would be a different transformation and is not implied by endianness.

### Connections

Data representation connects integer and floating-point formats, instruction encoding, ABIs, compilers, memory systems, device registers, DMA, networking, storage formats, text, cryptography, debugging and secure parsing.

## Governing Question

Bits acquire meaning only through a contract. The pattern `0xffffffff` can be unsigned 4,294,967,295, signed -1, a floating-point NaN, four encoded bytes, a mask or part of an instruction. Hardware routes bits; an ISA, ABI, type system or protocol supplies interpretation.

The governing question is how to preserve that interpretation across boundaries. In a register, bit position maps directly to arithmetic significance. In byte-addressed memory, those bits split into bytes. A file or network protocol orders bytes again. A compiler may insert padding between object members. Each layer needs an explicit mapping.

## Why This Matters

Representation bugs corrupt data silently. A byte-swapped length can allocate gigabytes. A sign-extension error can turn a safe offset into a negative address. A serialized struct can change when compiler, ABI or architecture changes.

Hardware-software interfaces amplify ambiguity. Device manuals may number register bits most-significant first while byte lanes follow host or bus order. DMA buffers can contain protocol-order headers and native-order descriptors together.

Security depends on unique and bounded interpretation. If two encodings represent the same logical message, a validator, cache and signature verifier can disagree. If offset arithmetic wraps, bounds checks can approve an out-of-range access.

## Prerequisites and Retrieval

Before studying this module, be able to:

- convert among binary, hexadecimal and unsigned integers;
- interpret two's-complement and floating-point fields;
- explain registers, memory addresses, loads and stores;
- distinguish a value from a variable or storage location;
- perform bounded integer arithmetic.

Retrieve field names, widths and signedness; byte order; bit numbering; alignment and atomicity; address size; ABI and calling convention; struct layout; instruction encoding; load/store extension; unaligned behavior; device and bus lane rules; DMA descriptor format; file/wire schema and version; text encoding and normalization; float format and NaN rules; canonicalization; length/offset limits; checksum or signature coverage; parser error behavior; producer/consumer architectures; debug format; captured bytes; and exact compiler, firmware, protocol and artifact versions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish abstract values, bit patterns, bytes and object layouts;
2. decode and encode multibyte integers in either byte order;
3. separate byte order from bit numbering and textual display order;
4. explain alignment, padding and ABI-dependent layout;
5. apply sign/zero extension and narrowing correctly;
6. specify stable instruction, device, file and network fields;
7. avoid unsafe native-struct serialization and type-punning;
8. design canonical and versioned encodings;
9. validate binary parsers against overflow and malformed inputs;
10. reconstruct representations from dumps with adequate context.

## Core Exposition

### Begin with abstract values

An integer, instruction, character or pointer is an abstract entity under one specification. Its representation is a bit pattern. Multiple representations can denote one value, and one pattern can denote different values under different types.

Write the interpretation next to raw data. `0xff` without width and signedness is incomplete evidence.

### Define bits by position

In an unsigned binary field, bit `i` contributes `2^i`. The least-significant bit has weight one. This significance order exists before the field is split into bytes.

Documentation may draw bit 31 at the left and bit 0 at the right. Diagram direction is typography, not byte-address order.

### Define byte-addressed memory

Modern ISAs usually assign an address to each byte. A multibyte load gathers consecutive bytes and maps them to result significance according to data endianness.

Address order is objective within the machine. “First byte” must say lowest address, transmission order or display order.

### Decode little-endian scalars

At address `A`, byte `b_0` contributes the lowest eight bits, byte `b_1` the next eight and so on. The unsigned value is the positional sum with powers `256^i`.

Hex dumps list increasing addresses conventionally, so a little-endian scalar's printed byte pairs appear least-significant first.

### Decode big-endian scalars

At address `A`, `b_0` is the most-significant byte. Reading the byte stream left to right resembles conventional hexadecimal scalar notation.

This visual convenience does not make big-endian mathematically superior. Both mappings preserve the same values when encode and decode agree.

### Separate byte and bit order

Byte endianness says how groups of eight significance bits map to addresses. Bit numbering in a byte or serial-link bit transmission is a different rule.

Do not reverse every bit when converting endian. Swap byte positions while leaving each byte's numerical bits intact unless another protocol explicitly transforms bit order.

### Avoid calling values endian

The mathematical integer 1 has no endianness. Its four-byte encoding might be `01 00 00 00` or `00 00 00 01`.

Registers are often described by bit significance rather than addressed byte layout. Endianness becomes relevant when bytes map to storage or transport positions.

### Treat width as part of meaning

The pattern `ff` is 255 unsigned or -1 signed in eight bits. In sixteen bits, `00ff` is 255 under both signed and unsigned interpretation.

Protocol fields require fixed width. A “native long” changes across ABIs and must not define persistent data.

### Apply zero extension

Widening an unsigned field prepends zero bits. This preserves its nonnegative mathematical value.

A load-byte-unsigned instruction uses zero extension. The same stored byte can feed a signed load with different high result bits.

### Apply sign extension

Widening a two's-complement field repeats the old sign bit. Eight-bit `0xff` becomes `0xffff` at sixteen bits and remains -1.

Signedness must be known before extension. Applying sign extension to an unsigned identifier whose top bit is one changes its value.

### Narrow deliberately

Narrowing to low bits implements modulo `2^N` for integers. It can discard sign, high address, length or flag information.

Check range before narrowing when the contract requires preservation. Do the check in a width that cannot already have overflowed.

### Distinguish representation from arithmetic

Byte swapping changes encoding, not the intended abstract value when paired with the opposite decoder. Adding numbers while one remains byte-swapped is meaningless under the intended contract.

Convert fields from external to host interpretation once at the boundary, operate on values, then encode once on output. Track types or wrappers to prevent double conversion.

### Understand alignment

An object aligned to `k` bytes begins at an address divisible by `k` under the ABI rule. Alignment can simplify datapaths, cache access and atomicity.

Some ISAs trap misaligned loads; some complete them in hardware; some split accesses with performance or atomicity consequences. Portable parsers should copy/decode bytes rather than dereference unaligned typed pointers.

### Separate access width and alignment

A four-byte field can be stored unaligned in a packed protocol. That does not authorize a native four-byte load from its address.

Read individual bytes or use a defined unaligned-access primitive, then decode. Compiler assumptions about typed-pointer alignment can create undefined behavior even if hardware tolerates it.

### Understand object padding

Compilers insert padding so members and arrays meet ABI alignment. Tail padding makes each array element's next instance aligned.

Padding bytes are not necessarily initialized or stable. Comparing or hashing raw structs can observe indeterminate or irrelevant state and leak prior memory contents.

### Treat struct layout as ABI state

Member offsets depend on type sizes, alignment, packing directives, ABI and compiler rules. Reordering fields can change size and cache behavior.

Use ABI tools and static assertions for hardware interfaces. Use explicit serialization for files and networks. Packed structs can create unaligned accesses and do not solve endianness.

### Avoid portable assumptions about bit-fields

Language bit-fields may have implementation-defined allocation order, container choice, signedness and padding. They are unsuitable as an unqualified external register or wire layout.

Use masks and shifts on fixed-width integers, then encode bytes explicitly. Verify compiler output only as implementation evidence for a frozen target.

### Decode instruction fields

An ISA fixes instruction length, field positions and immediate assembly. Memory byte order determines how instruction bytes are fetched where variable endianness exists.

Field diagrams label significance positions, not necessarily order in a dump. Reconstruct the instruction word first, then extract opcode, register and immediate fields.

### Handle split immediate fields

An immediate can be scattered across instruction positions for encoding efficiency. Concatenate pieces in their defined significance order, then sign-extend from the immediate's own width.

Do not sign-extend each fragment separately or use instruction byte order as field significance order.

### Interpret load/store semantics

Loads name access width and extension: byte, halfword, word or wider; signed or unsigned where applicable. Stores commonly write selected low source bits into addressed byte lanes.

Partial stores preserve other bytes but can race with readers or devices. Atomicity and coherence are separate from byte order.

### Define atomic fields

A naturally aligned word may be atomically loaded on a target while an unaligned word tears across transactions. Wider structures often require locks, versioning or atomic instructions.

Endianness does not create atomicity. A reader can observe a mixture of old and new bytes regardless of their significance order.

### Specify device-register views

MMIO registers define offsets, access widths, byte enables, reset values, side effects and bit fields. A bus bridge may transform lanes between CPU and device views.

Never infer register behavior from a memory dump alone. Read the device and architecture contract, including whether narrower accesses are forbidden or destructive.

### Handle mixed-endian interfaces

A system can use one native data order while a device descriptor or packet field uses another. Individual subfields can have fixed protocol order.

Annotate each boundary. Do not apply a blanket swap to a buffer containing bytes, little-endian counters and big-endian network fields together.

### Design DMA descriptors

Descriptors contain addresses, lengths, flags and ownership shared with a device. Define byte order, width, alignment, reserved bits and publication protocol.

Convert CPU pointers to device-visible addresses through the platform mapping. Use barriers and ownership transitions; correct field encoding does not guarantee the device sees writes in order.

### Define network byte order

Network protocols traditionally define multibyte fields in big-endian order unless their specification says otherwise. Application formats may choose little-endian or variable encodings.

Use protocol-specific readers and writers. “Network order” is not a substitute for citing the field schema.

### Design file formats explicitly

Persistent formats outlive a process and possibly the architecture. Include a magic value, format version, fixed-width types, byte order, lengths and integrity coverage.

Define unknown fields, optional sections, alignment, duplicate keys and partial writes. Native object layout is not a durable format.

### Use self-describing formats selectively

Tags and lengths allow readers to skip unknown fields and evolve schemas. They add overhead and parser complexity.

An untagged compact format can be safe with an external versioned schema. “Self-describing” still needs semantic definitions and limits.

### Canonicalize when uniqueness matters

Some encodings permit several byte sequences for one logical value: nonminimal integers, field reordering or duplicate mappings. Hashes and signatures operate on bytes, so equivalent values can produce different digests.

Define canonical order, shortest forms and duplicate rejection before signing. Validate canonical input rather than silently normalizing after authorization if ambiguity can be exploited.

### Parse lengths without overflow

For buffer size `n`, offset `o` and length `l`, checking `o+l <= n` can fail if addition wraps. Prefer `o <= n` and `l <= n-o` in a sufficiently wide unsigned domain.

Validate nested counts before multiplication and allocation. Limit recursion, total objects and decompressed size.

### Validate tags before interpretation

A union or variant needs a tag defining which payload layout is active. Check tag and length before reading the payload.

Unknown tags follow an explicit reject or skip rule. Reinterpreting bytes as a default type can create out-of-bounds or confused semantics.

### Treat text as encoded data

UTF-8 encodes Unicode scalar values into one to four bytes. Bytes, code points, grapheme clusters and displayed glyphs are different units.

String length and slicing must name the unit. Validate malformed sequences. Normalization can make distinct code-point sequences equivalent for selected comparison, but changes bytes and security boundaries.

### Keep character order separate from endianness

UTF-8 has defined byte sequences and no host-dependent byte order for its code units. Reversing string bytes for little-endian machines corrupts text.

UTF-16 and UTF-32 byte serialization need byte-order rules or markers. Code-unit order within a character follows the encoding specification.

### Represent floating point exactly

Floating-point formats define sign, exponent, fraction and special classes. Serializing by numeric text can lose NaN payload, signed zero or exact round-trip unless the text format guarantees it.

Raw IEEE interchange bits can preserve encoding when format and byte order are fixed. The consumer must still implement the same special-value policy.

### Represent pointers cautiously

A pointer may include address, tag, capability bounds, authentication or provenance not preserved by casting to an integer. Its size can differ from an integer register.

Never store process pointers as portable file or network identities. Use stable object IDs and reconstruct authorized references.

### Understand debug and object formats

Executable and debug formats record class, machine, byte order, sections, symbols and type/layout metadata. A debugger uses these plus the exact binary to interpret memory.

Wrong ABI or type version can produce plausible but false field values. Preserve build IDs and module load information with dumps.

### Read hexadecimal dumps methodically

Record base address and list bytes in increasing addresses. Group bytes only after identifying the field boundary and width. Apply the declared decoder, then signed or floating interpretation.

Do not visually reverse an entire record. Decode each field according to its own schema and alignment.

### Test cross-endian behavior

Use golden byte vectors independent of host layout. Encode values and compare exact bytes; decode bytes and compare values; round-trip both directions.

Run on native and emulated opposite-endian targets when possible. Include unaligned offsets, extrema, malformed lengths, unknown versions and mixed-order records.

### Use differential and property tests

Compare independent encoders and decoders. Assert decode(encode(value)) equals value for representable inputs and encode(decode(bytes)) equals canonical bytes for valid canonical input.

Round-trip alone can let two implementations share the same reversed mistake. Golden vectors and independent specification derivation remain necessary.

### Verify hardware boundaries

At RTL, verify byte enables, lane steering, loads, stores and extension. At integration, trace bus transactions, DMA and device interpretation.

Check synthesis, timing and physical lane mapping. Fault injection and logic analyzers cover wiring/configuration errors absent from a software parser model.

## Definitions and Notation

- `b_i`: byte at increasing address or stream position `i`.
- `n`: field width in bytes.
- `U_LE`: unsigned little-endian decoding of a byte sequence.
- `U_BE`: unsigned big-endian decoding of a byte sequence.
- `A`: base address of an object or field.
- **LSB/MSB:** least- and most-significant bit under a numeric field interpretation.
- **least/most-significant byte:** byte containing the lowest/highest numeric bit positions.
- **object representation:** bytes occupied by a typed object under an ABI or language model.
- **padding:** storage positions without declared member value semantics.
- **alignment:** permitted address multiple or boundary for an object/access.
- **host order:** native mapping of the executing architecture, insufficient as persistent schema.
- **wire order:** order specified by a transport or protocol field.
- **canonical form:** unique permitted byte representation for a logical value under a schema.
- **golden vector:** independently specified bytes and expected interpretation.
- **round trip:** encode followed by decode, or decode followed by canonical encode.

## Mechanisms, Invariants, or Proof Structure

1. **Meaning claim:** define abstract value, type and valid domain.
2. **Field invariant:** fix width, signedness, bit positions and special encodings.
3. **Byte invariant:** map significance to increasing address or stream position.
4. **Access invariant:** respect alignment, width, atomicity and fault behavior.
5. **Extension invariant:** widen or narrow under an explicit signedness and range policy.
6. **Layout claim:** bind object offsets and padding to an exact ABI where required.
7. **Boundary invariant:** convert external encoding exactly once before value operations.
8. **Serialization invariant:** avoid native padding, pointers and implementation-defined fields.
9. **Version invariant:** define unknown field, tag and version behavior.
10. **Parser invariant:** validate lengths, arithmetic, nesting and allocation before access.
11. **Canonical invariant:** one logical signed/hashed value has one accepted encoding.
12. **Device invariant:** preserve descriptor lanes, ownership, ordering and address mapping.
13. **Evidence invariant:** combine golden, property, differential and cross-target tests.
14. **Diagnostic invariant:** retain architecture, ABI, schema, address and build context.
15. **Change invariant:** revalidate after ISA, ABI, compiler, protocol or device change.

## Alternatives and Trade-Offs

- **Little versus big endian:** either maps scalars consistently; interoperability depends on an explicit shared choice.
- **Native versus fixed wire order:** native order avoids local swaps; fixed order makes persistent exchange portable.
- **Aligned versus packed layout:** alignment improves access and atomicity; packing saves bytes and creates unaligned work.
- **Struct serialization versus field encoding:** raw structs are fast and ABI-bound; explicit fields are portable and auditable.
- **Fixed-width versus variable integer:** fixed width enables direct indexing; variable encoding saves small-value space and adds canonical rules.
- **Tagged versus external schema:** tags aid evolution; external schemas reduce per-value overhead.
- **Self-describing versus compact format:** self-description supports tooling; compact formats reduce bandwidth and parser surface.
- **Sign extension versus zero extension:** each preserves a different intended interpretation.
- **Reject versus skip unknown fields:** rejection is strict; skipping supports forward evolution and needs bounded lengths.
- **Copy-decode versus unaligned cast:** copy/decode is portable; casts can be fast and invoke alignment/aliasing hazards.
- **Canonical versus permissive decoding:** canonical input gives unique bytes; permissive input improves compatibility and ambiguity.
- **Text versus binary numbers:** text is human-accessible; binary preserves fixed fields and can be denser.
- **Raw float bits versus decimal text:** raw bits preserve encoding; text can be portable but needs round-trip and special-value rules.
- **Stable IDs versus serialized pointers:** IDs survive processes; pointers are direct and bound to one address context.
- **Round-trip versus golden-vector testing:** round trips test composition; golden vectors detect shared inverse mistakes.

## Failure Modes and Misconceptions

1. **“An integer is little-endian.”** only its byte representation under a mapping is.
2. **“Endian conversion reverses every bit.”** ordinary scalar conversion reverses byte positions.
3. **“Hex display order is memory order.”** tools choose display conventions.
4. **“Word always means four bytes.”** word size is architecture and interface dependent.
5. **“All bytes are eight bits historically and universally.”** modern protocols should state octets explicitly.
6. **“Bit 0 is stored at the lowest address.”** bit numbering and byte addressing are separate.
7. **“Packed structs solve portability.”** byte order, field rules and alignment remain.
8. **“Compiler bit-fields map directly to device diagrams.”** allocation is implementation dependent.
9. **“If hardware supports unaligned access, a typed cast is safe.”** language alignment and aliasing still apply.
10. **“Alignment determines endianness.”** they are independent properties.
11. **“Sign extension preserves every high-bit-set value.”** only signed two's-complement interpretation.
12. **“Narrowing is harmless for small current inputs.”** future or malicious values can exceed range.
13. **“Byte swap twice is defensive.”** it restores wrong native assumptions inconsistently.
14. **“Network order applies to every payload.”** each protocol specifies its own fields.
15. **“Instruction diagrams show byte sequence.”** they usually show bit significance.
16. **“Atomic word access follows from correct byte order.”** atomicity is a separate guarantee.
17. **“MMIO behaves like ordinary RAM.”** widths, side effects and ordering differ.
18. **“A DMA address is a CPU pointer.”** translation and device visibility can differ.
19. **“Native structs are acceptable private files.”** upgrades and tools outlive the current ABI.
20. **“Self-describing means semantically complete.”** field meaning and limits still need schema.
21. **“Equivalent values always hash identically.”** alternate encodings produce different bytes.
22. **“Offset plus length check cannot overflow.”** fixed-width addition can wrap.
23. **“One Unicode code point is one visible character.”** grapheme clusters can contain several.
24. **“UTF-8 changes with host endian.”** its byte encoding is defined independently.
25. **“Round-trip tests prove the format.”** inverse bugs can agree with each other.
26. **“A plausible dump value is correctly decoded.”** architecture, ABI, version and type context are required.

## Worked Examples

### Example 1

Bytes `01 02 03 04` decode to `0x04030201` little-endian and `0x01020304` big-endian. Both decoders consume the same address order.

### Example 2

Byte `ff` loaded unsigned into 32 bits becomes `0x000000ff`; loaded signed becomes `0xffffffff`. Memory did not change.

### Example 3

A six-byte structure occupies eight bytes because the ABI aligns one member and adds tail padding. Hashing raw storage includes bytes outside member values.

### Example 4

A packed four-byte length begins at offset one. Byte decoding is safe; dereferencing an aligned integer pointer there violates some language/ISA contracts.

### Example 5

An instruction immediate is split across four bit ranges. Reassembling by significance then sign-extending works; reversing instruction bytes per fragment does not.

### Example 6

A device descriptor has little-endian lengths and a byte-array MAC address. Swapping the whole descriptor corrupts the address order.

### Example 7

A parser checks `offset+length <= size` in 32 bits. Crafted values wrap to a small sum. Subtraction-based bounds checking rejects them safely.

### Example 8

Two nonminimal encodings decode to the same integer but hash differently. A signed-message format rejects the noncanonical form before verification.

### Example 9

Reversing UTF-8 bytes on a little-endian host corrupts a multibyte code point. Host byte order is irrelevant to the UTF-8 stream.

### Example 10

A dump shows a plausible pointer under the wrong ABI. Matching build ID and debug type reveals those bytes are padding plus half of another field.

## Cross-Program Connections

- **Integer arithmetic:** width, signedness, extension and truncation determine values.
- **Floating point:** field classes and byte layout preserve exact interchange encodings.
- **Instruction sets:** fetch, decode, loads, stores and immediates expose representation.
- **Compilers and ABIs:** type size, alignment, padding and calling conventions define object layout.
- **Operating systems:** executable loading, system calls, memory dumps and device access consume ABIs.
- **Networking:** protocol byte order and bounded parsers enable heterogeneous exchange.
- **Storage:** file formats, checksums, crash records and versions must outlive native layout.
- **Security:** canonicalization, integer overflow and parser validation prevent ambiguity and memory errors.
- **Distributed systems:** stable serialization supports mixed architectures and rolling upgrades.
- **Debugging:** symbols, types, build identity and target order reconstruct raw memory.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), instruction fields, integer registers, load/store widths, extension and endian considerations; retrieved 2026-09-04.
2. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), data types, bit/byte order, instructions, alignment and memory access; retrieved 2026-09-04.
3. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), data types, byte order, alignment, instruction and system-register semantics; retrieved 2026-09-04.
4. System V ABI, [Generic ABI](https://gabi.xinuos.com/), object-file class, byte order, data representation, sections and executable structure; retrieved 2026-09-04.
5. DWARF Debugging Information Format Committee, [DWARF Version 5 Standard](https://dwarfstd.org/dwarf5std.html), type, location, address and data-representation metadata; retrieved 2026-09-04.
6. Unicode Consortium, [Unicode Standard 17.0](https://www.unicode.org/versions/Unicode17.0.0/), code points, encodings, normalization and conformance; retrieved 2026-09-04.
7. IETF, [RFC 8949: Concise Binary Object Representation](https://www.rfc-editor.org/rfc/rfc8949.html), typed binary encoding, byte order, well-formedness and deterministic serialization; retrieved 2026-09-04.
8. IETF, [RFC 3629: UTF-8](https://www.rfc-editor.org/rfc/rfc3629.html), byte-sequence encoding and malformed-sequence constraints; retrieved 2026-09-04.
9. IEEE, [IEEE 754-2019 — Standard for Floating-Point Arithmetic](https://standards.ieee.org/ieee/754/6210/), interchange formats, encodings and special values; retrieved 2026-09-04.

## Exercises

### Exercise 1

Decode bytes `01 02 03 04` as unsigned 32-bit little- and big-endian values, round-trip each, and decode byte `ff` under signed and unsigned eight-bit interpretation.

### Exercise 2

Design a versioned binary record with magic, version, flags, signed timestamp, payload length and checksum. Specify offsets, byte order, alignment, canonical rules and parser checks.

### Exercise 3

Given a DMA descriptor containing a 64-bit address, 16-bit length, byte-array identifier and ownership flags, define publication and decode rules between a little-endian CPU and a fixed-format device.

### Exercise 4

Build a cross-architecture test plan for an executable parser and a network protocol. Include golden vectors, opposite-endian execution, alignment, malformed values and diagnostics.

### Exercise 5

Construct an assurance plan for binary commands controlling an infusion device. Cover representation, validation, authentication, faults, evidence and named review.

## Answers to the Exercises

### Answer 1

Little-endian decoding gives `0x04030201`; big-endian gives `0x01020304`. Encoding each value with the decoder's matching order returns bytes `01 02 03 04`. Eight-bit `ff` is unsigned 255 and signed two's-complement -1.

<!-- bijux-verify: {"id":"byte-order-round-trip","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bytes=01020304\nlittle=0x04030201\nbig=0x01020304\nlittle_round_trip=01020304\nbig_round_trip=01020304\nu8_ff=255\ni8_ff=-1\n"}} -->
```python
raw = bytes.fromhex("01 02 03 04")
little = int.from_bytes(raw, "little", signed=False)
big = int.from_bytes(raw, "big", signed=False)

print(f"bytes={raw.hex()}")
print(f"little=0x{little:08x}")
print(f"big=0x{big:08x}")
print(f"little_round_trip={little.to_bytes(4, 'little').hex()}")
print(f"big_round_trip={big.to_bytes(4, 'big').hex()}")
print(f"u8_ff={int.from_bytes(bytes([0xFF]), 'big', signed=False)}")
print(f"i8_ff={int.from_bytes(bytes([0xFF]), 'big', signed=True)}")
```

The code uses Python's declared conversion APIs and illustrates fixed cases. It does not establish a target ABI, instruction behavior, device lane mapping or parser safety.

### Answer 2

Use four fixed magic bytes, one version byte, one flags byte with reserved zeros, a signed 64-bit timestamp, an unsigned 32-bit payload length, payload bytes and a 32-bit checksum over the canonical header and payload. Choose network big-endian for numeric fields and no implicit padding; offsets follow the byte schema, not a native struct. Require the shortest supported record and reject unknown mandatory flags, nonzero reserved bits and duplicate optional sections.

Verify magic and supported version before interpreting later fields. Check header availability, then `payload_length <= total_size-header-checksum` without wrapping. Limit payload before allocation, validate timestamp domain, ensure exact record length, and verify checksum only after safe bounds selection. Define whether unknown future versions reject or are dispatched to another parser. Signatures, if added, cover the canonical versioned bytes.

### Answer 3

Specify every numeric field in the device's fixed byte order; do not assume CPU native order. Encode the 64-bit device-visible DMA address and 16-bit length with field writers. Copy the identifier bytes unchanged in protocol order. Define flag bit positions within their numeric container and reserved values.

The CPU allocates and maps buffers, writes address, length and flags, executes the platform-required memory barrier, then transfers ownership with one final field or doorbell. It does not modify owned descriptors until the device returns them. The device decodes fields, validates address/length and writes completion before returning ownership under its ordering rules. Test byte lanes with golden descriptors, boundary lengths, unaligned ring bases if allowed, IOMMU remap, reset, stale DMA, malformed flags and opposite-endian host emulation.

### Answer 4

For executables, include both supported object classes and byte orders, section/string/symbol/relocation bounds, alignment, overlapping regions, unknown machines, truncated files and exact expected diagnostics. Compare parsed structure with an independent tool and preserve raw bytes and format version. For the network protocol, provide canonical golden messages for every field type and boundary, plus noncanonical and malformed variants.

Run encoders/decoders on native opposite-endian hardware or emulation and compare exact bytes. Vary unaligned input buffer offsets, maximum lengths, overflow combinations, unknown tags/versions, invalid text, duplicate fields and nested depth. Property-test round trips and canonical re-encoding, differential-test independent implementations, fuzz under resource limits and retain crashes, seeds, coverage and sanitizer results. Golden vectors prevent mutually inverse byte-order bugs from passing alone.

### Answer 5

Freeze command schema, units, ranges, byte order, signedness, version, sequence, device identity, expiration and authenticated coverage. Use a canonical format and reject alternate/nonminimal encodings. Validate total length, every offset and count, tags, reserved bits, numeric range, dosage cross-field constraints and freshness before state change. Bind authentication to exact canonical bytes and device/session context; make replay handling durable.

Trace decoded values through software, bus and controller registers with golden vectors. Inject truncation, byte swaps, bit flips, length overflow, duplicated fields, invalid Unicode labels, stale commands and interrupted transfer. Verify safe rejection, audit and independent physical limits. Named clinical, pharmacy, medical-device, protocol, hardware, firmware, security, safety, human-factors, verification, quality, regulatory and independent-assurance authorities review their scopes. This course module supplies no medical authorization or certification.
