# 49 — Function-Like Procedural Macros and Typed DSLs

**Course 5, day 9 · Module 49 of 60**  
`████████████████░░░░` **49/60**

[← Module 48: Attribute Macros and Item Transformation](../module-48-attribute-macros-and-item-transformation/index.md) · [Course 5 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 50: Build Scripts, Generated Code, and Compile-Time Architecture →](../module-50-build-scripts-generated-code-and-compile-time-architecture/index.md)

## The question

> How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?

## Why this comes now

A derive reads an existing Rust item. An attribute transforms one attached item. A function-like procedural macro owns its entire input language and can coordinate relationships across many declarations. That makes it the right mechanism for command catalogs, route tables, query schemas, and other small compile-time DSLs—but only when the language is simpler than the duplication it removes.

Modules 46–48 supplied the execution boundary, structural parsing, spans, and preservation discipline. Module 49 combines them into a full compiler-like pipeline without pretending to become a general compiler.

## What you will be able to do

- Design a bounded custom grammar with explicit compatibility space.
- Implement `syn::parse::Parse` for syntax nodes rather than splitting strings.
- Separate syntax AST, semantic validation, normalized model, and generation.
- Detect duplicates and cross-entry conflicts with useful multi-span errors.
- Preserve source order or define canonical order deliberately.
- Generate compact Rust whose type checker owns type-level obligations.
- Test parsing and validation independently from compiler fixtures.
- Decide when a DSL should instead be runtime data or a build-time file.

## Core model

### A DSL must earn its language

A custom invocation such as:

```rust
command_catalog! {
    pub static COMMANDS;
    pub fn find_command;
    {
        "add" => ADD_HANDLER;
        "slug" => SLUG_HANDLER;
    }
}
```

creates a new language. Even though it resembles Rust, the accepted grammar and meaning are defined by the macro crate.

Before implementation, compare alternatives:

```rust
pub static COMMANDS: &[CommandSpec] = &[
    CommandSpec::new("add", ADD_HANDLER),
    CommandSpec::new("slug", SLUG_HANDLER),
];
```

The ordinary table may already be sufficient. The DSL is justified only if it adds compile-time relationships ordinary values cannot establish cleanly—such as duplicate literal rejection, generated lookup code, or coordinated public metadata—without hiding runtime behavior.

For CommandForge, the function-like macro owns exactly three cross-command facts:

- command names;
- uniqueness of those names;
- deterministic catalog order and lookup generation.

It does not own handler bodies, argument fields, or exit codes.

### Write the grammar first

Use a small notation before writing parser code:

```text
catalog       = table-declaration lookup-declaration `{` entry+ `}`
table-declaration  = visibility `static` identifier `;`
lookup-declaration = visibility `fn` identifier `;`
entry         = string-literal `=>` path `;`
visibility    = Rust visibility fragment
identifier    = Rust identifier
path          = Rust path
```

Then answer edge cases:

- Is an empty catalog legal?
- Is a trailing semicolon required? Here every entry has one.
- Are attributes allowed on entries?
- Are command names arbitrary strings or restricted identifiers?
- Are duplicate paths legal? Yes; one handler descriptor may serve aliases if product policy permits.
- Are duplicate names legal? No.
- Is order source order or sorted order? Source order.
- Can the static be mutable? No.
- Is `pub(crate)` accepted? Yes through `syn::Visibility`.

Grammar decisions create compatibility constraints. Reject unknown syntax rather than accepting and ignoring it.

### Parse into syntax types

Define syntax-only structures:

```rust
struct CatalogInput {
    table_visibility: syn::Visibility,
    table_name: syn::Ident,
    lookup_visibility: syn::Visibility,
    lookup_name: syn::Ident,
    entries: Vec<CatalogEntry>,
}

struct CatalogEntry {
    command: syn::LitStr,
    handler: syn::Path,
}
```

Implement `Parse`:

```rust
impl syn::parse::Parse for CatalogInput {
    fn parse(input: syn::parse::ParseStream<'_>) -> syn::Result<Self> {
        let table_visibility = input.parse()?;
        input.parse::<syn::Token![static]>()?;
        let table_name = input.parse()?;
        input.parse::<syn::Token![;]>()?;

        let lookup_visibility = input.parse()?;
        input.parse::<syn::Token![fn]>()?;
        let lookup_name = input.parse()?;
        input.parse::<syn::Token![;]>()?;

        let content;
        syn::braced!(content in input);

        let mut entries = Vec::new();
        while !content.is_empty() {
            entries.push(content.parse()?);
        }

        if entries.is_empty() {
            return Err(content.error("a command catalog requires at least one entry"));
        }

        Ok(Self {
            table_visibility,
            table_name,
            lookup_visibility,
            lookup_name,
            entries,
        })
    }
}
```

Each `CatalogEntry::parse` requires a string literal, `=>`, a path, and `;`. The parser owns syntax only. It does not yet check duplicates.

#### Why not parse `TokenStream::to_string()`?

String splitting cannot reliably preserve:

- nested generic paths;
- raw strings;
- punctuation spacing;
- groups;
- source spans;
- future Rust token forms.

A token parser works with the compiler’s lexical structure and can attach errors to the actual source token.

### Build a syntax AST, then a normalized model

The syntax AST retains source-specific forms and spans. A normalized model contains only what generation needs.

```rust
struct CommandModel {
    name: String,
    name_literal: syn::LitStr,
    handler: syn::Path,
}
```

Normalization may:

- validate nonempty names;
- reject whitespace or unsupported characters;
- compute a canonical lookup key;
- preserve the source literal for diagnostics and emitted text;
- record source order.

Do not normalize away evidence needed for errors. Keep the original span-bearing syntax node alongside derived values.

### Semantic validation is cross-entry reasoning

Duplicate detection requires a symbol table:

```rust
let mut first_by_name = std::collections::BTreeMap::<String, syn::LitStr>::new();
let mut errors: Option<syn::Error> = None;

for entry in &entries {
    let name = entry.command.value();
    if let Some(first) = first_by_name.get(&name) {
        let mut error = syn::Error::new(
            entry.command.span(),
            format!("duplicate command name `{name}`"),
        );
        error.combine(syn::Error::new(
            first.span(),
            "first declared here",
        ));
        push_error(&mut errors, error);
    } else {
        first_by_name.insert(name, entry.command.clone());
    }
}
```

`BTreeMap` is used here for deterministic behavior, though source-order iteration is already deterministic. A `HashMap` could perform lookup, but generated ordering must not depend on hash iteration.

Other semantic rules may include:

- reserved command names;
- duplicate method/path pairs;
- conflicting aliases;
- incompatible options;
- references to the same generated identifier;
- unreachable entries under first-match semantics.

Only check what the syntax model can know honestly.

### Multiple spans improve relationship errors

A duplicate has two relevant locations. Pointing only to the second declaration says what to change, but identifying the first explains the relationship.

`syn::Error::combine` can emit multiple compile errors. Keep messages stable and causal:

```text
error: duplicate command name `add`
  --> catalog.rs:12:5

error: first declared here
  --> catalog.rs:8:5
```

Do not report every later duplicate against every earlier duplicate. Choose one primary declaration and one message per repeated occurrence to avoid quadratic diagnostic noise.

### Normalize before generating

Generation should not contain validation branches. By the time `quote!` runs, the model should satisfy its invariants:

- at least one entry;
- names valid and unique;
- stable source order;
- all paths parsed;
- table and lookup names and visibilities known.

Then generation is mechanical:

```rust
quote! {
    #table_visibility static #table_name: &[::commandforge::CommandSpec] = &[
        #(
            ::commandforge::CommandSpec::new(
                #command_names,
                #handler_paths,
            )
        ),*
    ];
}
```

A separate generated lookup can use a `match`:

```rust
pub fn find_command(name: &str) -> Option<&'static CommandSpec> {
    match name {
        "add" => Some(&COMMANDS[0]),
        "slug" => Some(&COMMANDS[1]),
        _ => None,
    }
}
```

This preserves source order in the slice and provides direct lookup. For a small fixed catalog, generated match code is clear. For thousands of entries, generated size and compile time require measurement; a runtime sorted table may be better.

### Keep runtime behavior ordinary

The catalog should not generate handler bodies. It stores function pointers or descriptors and calls ordinary functions.

This separation keeps:

- domain errors in runtime types;
- unit tests independent of macro expansion;
- ownership visible in normal signatures;
- command logic debuggable without reading generated tokens;
- the DSL focused on cross-command relationships.

A DSL that embeds business logic expressions becomes harder to test and evolve. Prefer paths to ordinary behavior over miniature expression languages.

### Generated code should be smaller than the model

A warning sign is a DSL that expands into enormous repeated wrappers. Ask whether a runtime generic helper can centralize behavior while generation emits only metadata.

Good split:

```text
macro generates:
    compact CommandSpec entries

ordinary runtime library owns:
    argument decode contract
    dispatch loop
    error rendering
    help rendering
```

Bad split:

```text
macro generates:
    complete parser
    complete formatter
    repeated error mapping
    repeated business logic
    repeated I/O
```

Generation should coordinate structure, not duplicate algorithms in every expansion.

### AST and model tests

Test parsing without invoking rustc for every case:

- minimal valid catalog;
- multiple entries;
- `pub`, `pub(crate)`, and private visibility;
- nested handler paths;
- missing `static`;
- missing braces;
- wrong name token;
- missing arrow;
- missing semicolon;
- empty body.

Test semantic validation separately:

- duplicate name;
- invalid empty name;
- reserved name;
- source-order preservation;
- legal repeated handler path.

Test generation structurally or through compiled fixtures. Avoid relying only on `TokenStream::to_string()` equality; whitespace and formatting are not the contract. You can parse generated tokens back into `syn::File` or compile a fixture and assert runtime behavior.

### DSL evolution

A custom language needs a change policy.

Safer extension patterns:

- add a new optional keyword with a default;
- add an explicitly delimited section;
- add attributes in a previously rejected position;
- add a new entry form that begins with a reserved keyword.

Risky changes:

- reinterpret previously accepted arbitrary tokens;
- change separator meaning;
- alter first-match arm behavior;
- change source-order semantics;
- silently accept unknown fields;
- change a literal from data to syntax.

Rejecting unused syntax today preserves room for future versions.

### When a DSL should be runtime data

Use a runtime parser or deserializer instead when:

- configuration changes without recompilation;
- untrusted users supply the language;
- errors must be handled at runtime;
- the data is large or frequently updated;
- multiple tools need the same schema;
- compile time and binary regeneration are undesirable;
- the source of truth belongs outside Rust code.

Use a build script when external data is authoritative but must become compile-time constants. Module 50 handles that boundary.

### Keep syntax ownership narrower than product ownership

A DSL should own only the relationships that its syntax can state and validate honestly. CommandForge's catalog owns command names, source order, and descriptor association. It does not own argument decoding, command-domain behavior, terminal output, or process exit policy. Those remain ordinary Rust because ordinary Rust already expresses them clearly and tests them directly.

This boundary matters when the product changes. Adding a command should require one catalog entry and one ordinary handler, but changing runtime error wording should not require editing the parser. Conversely, duplicate command names are a catalog error and should be rejected before generated Rust reaches ordinary type checking. Each rule belongs to the narrowest phase with enough information to enforce it accurately.

A useful review table is:

| Fact | Earliest honest owner |
|---|---|
| token punctuation and entry termination | parser |
| duplicate literal command names | semantic validator |
| descriptor path existence and visibility | Rust name resolution |
| descriptor value type | Rust type checker |
| command business invariant | ordinary handler |
| output destination and exit status | application shell |

Trying to move every row into the macro makes diagnostics worse and couples unrelated behavior to syntax. Leaving every row to generated Rust wastes the DSL's strongest advantage: domain-specific validation before expansion. Good metaprogramming is therefore not maximal compile-time work. It is accurate placement of authority.

## Use the idea in a complete program

CommandForge’s catalog syntax is:

```rust
command_catalog! {
    pub static COMMANDS;
    pub fn find_command;
    {
        "add" => ADD_HANDLER;
        "slug" => SLUG_HANDLER;
        "repeat" => REPEAT_HANDLER;
        "contains" => CONTAINS_HANDLER;
    }
}
```

The macro:

- requires one or more entries;
- requires explicit semicolon termination;
- preserves source order;
- rejects duplicate command-name literals with both spans;
- rejects empty names and whitespace-containing names;
- permits repeated descriptor paths only when names differ;
- generates the `CommandSpec` slice and `find_command` match;
- uses the runtime crate’s stable support path;
- does not parse command-line values or execute handlers.

The independent [Route Table DSL](../../labs/module-09-route-table-dsl/README.md) uses method/path pairs to exercise two-dimensional duplicate detection and deterministic dispatch generation.

## Practice sequence

1. Write a DSL grammar before parser code.
2. Implement separate syntax structs with `Parse`.
3. Normalize source strings while retaining span-bearing literals.
4. Detect duplicates with primary and secondary source locations.
5. Ensure generation has no validation branches.
6. Compare generated match lookup with a runtime table design.
7. Complete the route-table laboratory.
8. Implement CommandForge’s command catalog and remove any duplicate command-name source.

## Ready to continue

Continue when you can show:

- a written grammar;
- syntax AST types;
- semantic invariants;
- a normalized model;
- multi-span relationship diagnostics;
- deterministic order policy;
- compact generated Rust;
- a compatibility plan;
- a reason the language belongs at compile time.

Do not continue if parsing, validation, and generation occur in one function or if the DSL accepts arbitrary tokens that it ignores.

## Primary Rust references

- Rust Reference, function-like procedural macros: <https://doc.rust-lang.org/reference/procedural-macros.html#function-like-procedural-macros>
- `syn::parse::Parse`: <https://docs.rs/syn/3.0.3/syn/parse/trait.Parse.html>
- `syn::parse::ParseStream`: <https://docs.rs/syn/3.0.3/syn/parse/type.ParseStream.html>
- `syn::Error`: <https://docs.rs/syn/3.0.3/syn/struct.Error.html>
- `quote!`: <https://docs.rs/quote/1.0.47/quote/macro.quote.html>

## Continue

1. Complete the [Module 49 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 49 — Route Table DSL](../../labs/module-09-route-table-dsl/README.md) from its public contract.
3. Apply the Module 49 increment in the [CommandForge engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
