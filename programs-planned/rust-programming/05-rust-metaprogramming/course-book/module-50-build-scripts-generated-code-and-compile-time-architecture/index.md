# 50 — Build Scripts, Generated Code, and Compile-Time Architecture

**Course 5, day 10 · Module 50 of 60**  
`█████████████████░░░` **50/60**

[← Module 49: Function-Like Procedural Macros and Typed DSLs](../module-49-function-like-procedural-macros-and-typed-dsls/index.md) · [Course 5 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 51: Binary Data Contracts: Bytes, Endianness, and Checked Parsing →](../../../06-rust-systems-programming/course-book/module-51-binary-data-contracts/index.md)

## The question

> How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

## Why this comes now

Modules 41–49 built every stable macro form from a conservative selection model: declarative patterns, recursion, paths, diagnostics, raw procedural tokens, derives, attributes, and typed DSLs. One source remains outside Rust syntax: checked external data. Cargo build scripts can validate and translate that data before compiling the package.

The final module is not “another generator.” It is an architecture review. Every compile-time layer must own one distinct relationship, declare its inputs, produce deterministic output, and survive an attempt to delete it.

## What you will be able to do

- Explain the Cargo build-script lifecycle and communication protocol.
- Read host and target configuration correctly.
- Declare rebuild inputs with `cargo::rerun-if-changed` and `cargo::rerun-if-env-changed`.
- Write generated files only under `OUT_DIR`.
- Validate external data before emitting Rust.
- Produce deterministic, escaped, atomic generated source.
- Distinguish checked-in source, generated source, runtime data, and build metadata.
- Review a multi-generator architecture for duplicate authority, hidden effects, and compatibility risk.

## Core model

### The build-script lifecycle

Cargo recognizes a package build script through `build.rs` or an explicit manifest path:

```toml
[package]
build = "build.rs"
```

Before compiling the package, Cargo compiles the build script for the **host** and executes it. The script communicates with Cargo by printing lines beginning with `cargo::` to standard output.

After successful execution, Cargo compiles the package, which may include generated Rust from the directory named by the `OUT_DIR` environment variable.

A minimal generated include is:

```rust
include!(concat!(env!("OUT_DIR"), "/exit_codes.rs"));
```

The build script is not part of the final runtime executable unless equivalent code is also linked elsewhere. Its output can affect compilation, linking, configuration, and embedded constants.

### Host and target are different

The build script runs on the host machine. The package may be compiled for another target.

Inside `build.rs`, this is often wrong for target decisions:

```rust
if cfg!(target_os = "linux") {
    // describes the build-script host
}
```

Cargo provides target information through environment variables such as:

- `TARGET`;
- `HOST`;
- `CARGO_CFG_TARGET_OS`;
- `CARGO_CFG_TARGET_ARCH`;
- `CARGO_CFG_TARGET_ENDIAN`;
- `CARGO_CFG_TARGET_POINTER_WIDTH`.

Read those when generation depends on the target. CommandForge’s exit-code table is target-independent, so the build script deliberately ignores target configuration. Unused variability is easier to reproduce.

### Declare change triggers

Without explicit directives, Cargo conservatively watches package files. A build script should narrow its true inputs:

```rust
println!("cargo::rerun-if-changed=config/exit_codes.tsv");
println!("cargo::rerun-if-changed=build.rs");
```

The second line is often unnecessary because Cargo already recompiles and reruns a changed build script, but it can express that no other package files should trigger the script when the external table is the only data input.

For environmental input:

```rust
println!("cargo::rerun-if-env-changed=COMMANDFORGE_PROFILE");
```

Do not emit broad directory triggers if one file is authoritative. Do not read environment variables without declaring them. Hidden inputs create stale or irreproducible output.

### Write only to `OUT_DIR`

Cargo provides a package-specific output directory. Generated and intermediate files belong there.

```rust
let out_dir = std::env::var_os("OUT_DIR")
    .ok_or("Cargo did not provide OUT_DIR")?;
let output = std::path::PathBuf::from(out_dir).join("exit_codes.rs");
```

Do not rewrite checked-in `src/generated.rs` during ordinary builds. That creates dirty working trees, concurrent-build races, permission problems, and unclear source ownership.

`OUT_DIR` may persist across reruns. Do not assume it is empty. Write the complete target file each time, and do not depend on unrelated leftovers.

### External data needs a schema

CommandForge reads:

```text
USAGE	64	invalid command usage
INPUT	65	invalid input data
INTERNAL	70	internal command failure
```

Define the schema before parsing:

```text
row         = name TAB integer TAB description newline
name        = ASCII uppercase letter (`ASCII uppercase letter` | digit | `_`)*
integer     = decimal value in 1..=255
description = nonempty UTF-8 text without tabs or line breaks
```

Validation rules:

- exactly three fields per nonblank row;
- no blank rows if the format forbids them;
- unique names;
- unique numeric codes;
- allowed name characters;
- range-checked code;
- nonempty description;
- stable order policy;
- physical line number in every error.

Do not generate partial output after a validation failure.

### Parse, validate, normalize, generate

The same phase discipline used for procedural DSLs applies:

```text
read bytes/text
    ↓
parse rows with line numbers
    ↓
validate field-local rules
    ↓
validate cross-row uniqueness
    ↓
normalize one model
    ↓
generate deterministic Rust
    ↓
write complete output
```

Keep parsing and generation in ordinary functions so unit tests can call them without a Cargo build.

A normalized row might be:

```rust
struct ExitCodeRow {
    name: String,
    code: u8,
    description: String,
    line: usize,
}
```

The physical line remains for diagnostics but does not need to appear in generated output.

### Deterministic ordering

Choose one rule:

- preserve source order;
- sort by numeric code;
- sort by name.

CommandForge preserves source order because the file is curated as documentation and the generated list command should match it. Duplicate checks use maps only for lookup, not for output iteration.

Determinism also requires:

- no timestamps;
- no random identifiers;
- no filesystem enumeration without sorting;
- no locale-dependent formatting;
- no absolute construction paths embedded in output;
- stable newline policy;
- stable string escaping;
- output determined only by declared inputs and generator version.

### Generate valid Rust safely

Do not interpolate external text directly into quotes:

```rust
// wrong when description contains `"`, `\`, or a newline
writeln!(file, "(\"{}\", {}, \"{}\")", name, code, description)?;
```

Use Rust’s debug string formatting for string literals in a small generator:

```rust
writeln!(
    output,
    "    ({name:?}, {code}, {description:?}),"
)?;
```

`{:?}` produces an escaped Rust-compatible string representation for ordinary strings. For larger generators, a token-generation library or a dedicated serializer may be preferable.

Generate a header stating that the file is derived and naming its source:

```rust
// @generated from config/exit_codes.tsv by build.rs.
// Do not edit this file directly.
```

This is not a substitute for deterministic output; it clarifies ownership.

### Atomic output

A build failure should not leave a truncated file that a later step might include. Write to a temporary file in `OUT_DIR`, flush, then rename over the destination:

```rust
let temporary = output.with_extension("rs.tmp");
std::fs::write(&temporary, generated)?;
std::fs::rename(&temporary, &output)?;
```

On some platforms, replacing an existing destination may require removal or a platform-aware strategy. Because `OUT_DIR` is package-private build output, a simple complete rewrite is usually sufficient; document platform assumptions and test the supported environments.

The key invariant is: package compilation sees either the previous complete file or the new complete file, never a half-written stream.

### Build errors should be actionable

Returning an error from `main` or printing `cargo::error=` can stop the build. Prefer structured ordinary errors internally and render one concise message at the entry boundary.

A useful failure is:

```text
config/exit_codes.tsv:4: duplicate code 65; first declared on line 2
```

A weak failure is:

```text
thread 'main' panicked at build.rs:88: called Result::unwrap()
```

Build scripts are tools used during every clean build. Their diagnostics deserve the same product quality as runtime parsing.

### Generated code versus runtime data

A build script is justified when:

- external data is authoritative at source-control time;
- invalid data should stop compilation;
- runtime loading is unnecessary or undesirable;
- generated constants/types improve integration;
- rebuild frequency is acceptable.

Use runtime loading when:

- data changes after deployment;
- users supply it;
- invalid input should be handled without rebuilding;
- the file is large or optional;
- recompilation would be operationally expensive.

Use a separate explicit generator command when:

- several languages consume the output;
- generated files should be reviewed and checked in;
- generation requires tools unavailable in normal builds;
- build reproducibility policy forbids arbitrary build-script execution.

The mechanism follows source ownership and operational needs, not preference.

### Compile-time architecture map

CommandForge now contains five layers:

| Layer | Source of truth | Generated surface | Must not own |
|---|---|---|---|
| diagnostic `macro_rules!` | variant/code/message declarations | enum and lookup methods | command behavior |
| `CommandArgs` derive | argument struct fields and helper attributes | flag decoder and usage | command names |
| handler attribute | one function signature and description | descriptor and wrapper | catalog order |
| catalog DSL | command name → descriptor declarations | ordered table and lookup | handler body |
| build script | exit-code TSV | constants and table | runtime command errors beyond mapping |

The runtime library owns:

- `ArgError` and `CommandError` behavior;
- dispatch execution;
- help rendering;
- command domain logic;
- CLI exit decisions.

This map prevents overlapping authority. If two layers own the same fact, delete or redesign one.

### The architectural deletion review

For each layer, answer:

1. What exact relation drifts without it?
2. What handwritten Rust replaces it?
3. How many facts, not lines, would be duplicated?
4. What new language and generated API does the layer introduce?
5. What build dependencies and execution permissions does it add?
6. What are its failure phases?
7. Is the compile-time diagnostic materially better than a runtime or type-checking error?
8. Can a simpler layer absorb its responsibility without overlap?

Possible conclusions:

- keep the diagnostic macro because it synchronizes variants, codes, messages, and reverse lookup;
- keep the derive because argument fields otherwise require repetitive flag state and missing-value logic;
- keep the attribute only if local signature validation and descriptor generation remain separate from catalog names;
- keep the DSL because it detects duplicate literal command names and generates deterministic lookup;
- keep the build script because the checked-in TSV is the authoritative external registry;
- delete any helper macro whose only result is fewer braces.

### Build dependencies and supply-chain review

Build scripts and proc macros execute during compilation. Audit:

- exact direct dependencies;
- enabled features;
- lockfile state;
- licenses;
- update policy;
- transitive build-executed code;
- filesystem and environment access;
- network policy;
- minimum Rust version;
- compile-time cost.

Course 5 pins `syn`, `quote`, and `proc-macro2` for reproducible examples. A production project should update deliberately with compile-pass, compile-fail, runtime, and downstream tests—not through unreviewed version drift.

### Cross-compilation and reproducibility tests

At minimum:

- build from a clean checkout;
- build twice and compare generated bytes;
- touch an unrelated file and confirm the build script does not rerun unnecessarily;
- change the TSV and confirm it does rerun;
- test malformed rows and duplicate keys;
- build with a different target where available;
- ensure no absolute source path appears in generated output;
- ensure output does not depend on local timezone or locale;
- confirm a read-only source tree still works because output stays in `OUT_DIR`.

## Use the idea in a complete program

The final CommandForge increment completes the exit-code generator and then performs the full architecture review.

The CLI supports:

```text
commandforge list
commandforge explain <command>
commandforge run <command> [flags]
commandforge demo
commandforge help
commandforge version
```

Exit behavior uses generated constants:

- success;
- command rejection or usage failure as defined by the product;
- invalid input;
- internal failure.

The build table supplies numeric mapping and descriptions. Runtime code decides which category applies.

The independent [Generated Code Build](../../labs/module-10-generated-code-build/README.md) isolates deterministic parsing and `OUT_DIR` generation before the capstone combines all five compile-time layers.

## Practice sequence

1. Trace a build script from Cargo decision to included Rust.
2. Replace host `cfg!` assumptions with target environment input where needed.
3. Declare exact rerun inputs.
4. Parse and validate an external table with physical line diagnostics.
5. generate identical bytes twice and compare hashes.
6. Write through a temporary file under `OUT_DIR`.
7. Complete the generated-code laboratory.
8. Finish CommandForge and conduct the deletion review for every compile-time layer.

## Ready to continue

Finish when you can defend:

- every source of truth;
- every generated surface;
- every compile-time dependency;
- every environmental input;
- every rebuild trigger;
- deterministic ordering and escaping;
- host-versus-target assumptions;
- failure atomicity of generation;
- runtime behavior left outside macros;
- the reason each generator survives deletion.

The final standard is not “I can write macros.” It is:

> I can design, test, constrain, and delete compile-time machinery until the remaining system has one honest authority per fact.

## Primary Rust references

- Cargo Book, build scripts: <https://doc.rust-lang.org/cargo/reference/build-scripts.html>
- Cargo Book, environment variables: <https://doc.rust-lang.org/cargo/reference/environment-variables.html>
- Rust Reference, procedural macros: <https://doc.rust-lang.org/reference/procedural-macros.html>
- Standard library `include!`: <https://doc.rust-lang.org/std/macro.include.html>
- Standard library `env!`: <https://doc.rust-lang.org/std/macro.env.html>

## Continue

1. Complete the [Module 50 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 50 — Generated Code Build](../../labs/module-10-generated-code-build/README.md) from its public contract.
3. Apply the Module 50 increment in the [CommandForge engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
