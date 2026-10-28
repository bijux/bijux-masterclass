# 47 — Custom Derive Macros and Structural Generation

**Course 5, day 7 · Module 47 of 90**  
`████████████████░░░░` **47/90**

[← Module 46: Procedural Macro Execution and TokenStream Engineering](../module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) · [Course 5 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 48: Attribute Macros and Item Transformation →](../module-48-attribute-macros-and-item-transformation/index.md)

## The question

> How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?

## Why this comes now

Module 46 established the procedural execution boundary and token pipeline. A custom derive is the narrowest structured procedural form: the source type already exists, and the macro adds implementations or metadata without replacing the declaration. That constraint makes derives the right place to learn `syn::DeriveInput`, data-shape inspection, helper attributes, generic preservation, and generated bounds.

Attribute macros and custom DSLs come later because they own more syntax and can transform more aggressively.

## What you will be able to do

- Parse `DeriveInput` and distinguish structs, enums, and unions.
- Support only documented item shapes and reject others at useful spans.
- Inspect named, unnamed, and unit fields without losing source order.
- Parse derive helper attributes and reject unknown or duplicate options.
- Preserve lifetimes, type parameters, const parameters, and `where` clauses.
- Add only necessary generated bounds.
- Generate lawful trait or inherent implementations through `quote!`.
- Explain the runtime-crate path and dependency-renaming contract.

## Core model

### What a derive receives

A derive macro is declared with:

```rust
#[proc_macro_derive(FieldNames, attributes(field_names))]
pub fn derive_field_names(input: TokenStream) -> TokenStream {
    /* ... */
}
```

The input is the complete token stream of the annotated struct, enum, or union. `syn::DeriveInput` represents the common outer structure:

```rust
pub struct DeriveInput {
    pub attrs: Vec<Attribute>,
    pub vis: Visibility,
    pub ident: Ident,
    pub generics: Generics,
    pub data: Data,
}
```

The derive does not receive resolved type information. It sees syntax such as `Vec<T>`, a path, not proof that the path names the standard vector type. It sees `Alias`, not the target of a type alias. It sees attributes, not arbitrary semantic meaning unless you define and parse helper attributes.

### A derive should add, not secretly redefine

The original item remains in the program. The macro emits additional items after it, typically an implementation:

```rust
#[derive(FieldNames)]
struct Record {
    id: u64,
    label: String,
}
```

Conceptually expands to:

```rust
struct Record {
    id: u64,
    label: String,
}

impl FieldNames for Record {
    const FIELD_NAMES: &'static [&'static str] = &["id", "label"];
}
```

The derive cannot remove fields, change visibility, rewrite the item, or inject attributes into the original declaration. If transformation is required, use an attribute macro and accept the larger preservation contract.

This limitation is a feature. A derive has a clear source of truth: the declared type structure.

### Inspect data shape explicitly

`syn::Data` has variants for struct, enum, and union. A derive must decide which are supported.

```rust
match input.data {
    syn::Data::Struct(data) => { /* inspect fields */ }
    syn::Data::Enum(data) => { /* inspect variants */ }
    syn::Data::Union(union) => {
        return syn::Error::new_spanned(
            union.union_token,
            "FieldNames cannot be derived for unions",
        )
        .to_compile_error();
    }
}
```

For structs, fields can be:

- `Fields::Named`;
- `Fields::Unnamed`;
- `Fields::Unit`.

Do not silently treat unsupported forms as empty. If `FieldNames` promises source field identifiers, tuple fields and unit structs have no such identifiers. Reject them with a message that names the supported shape.

The Module 47 lab supports named structs only. That boundary keeps the generated contract meaningful.

### Preserve source order

`syn` retains field order. If generated metadata exposes field names, preserve declaration order unless the API explicitly requires canonical sorting.

```rust
let names = fields.named.iter().filter_map(|field| {
    field.ident.as_ref().map(|ident| {
        syn::LitStr::new(&ident.to_string(), ident.span())
    })
});
```

Sorting alphabetically would be deterministic, but it would change the relationship from source structure to metadata. Determinism does not always mean sorting; it means one documented stable rule.

### Helper attributes are a language

The derive declaration can reserve helper attributes:

```rust
#[proc_macro_derive(FieldNames, attributes(field_names))]
```

Then fields may use syntax such as:

```rust
#[derive(FieldNames)]
struct Account {
    id: u64,
    #[field_names(skip)]
    cache: String,
    #[field_names(rename = "display_name")]
    name: String,
}
```

Define the grammar precisely:

```text
field_names-attribute = `field_names` `(` option `)`
option = `skip` | `rename` `=` string-literal
```

Decide whether `skip` and `rename` are mutually exclusive. Reject duplicate attributes and unknown keys. Do not ignore misspellings such as `#[field_names(skpi)]`; silent acceptance destroys future syntax space and hides errors.

`syn::Attribute::parse_nested_meta` supports conventional structured attributes:

```rust
attr.parse_nested_meta(|meta| {
    if meta.path.is_ident("skip") {
        options.skip = true;
        return Ok(());
    }
    if meta.path.is_ident("rename") {
        let value = meta.value()?;
        let literal: syn::LitStr = value.parse()?;
        options.rename = Some(literal);
        return Ok(());
    }
    Err(meta.error("expected `skip` or `rename = \"...\"`"))
})?;
```

Keep attribute parsing in an ordinary helper returning `syn::Result<FieldOptions>`. It is easier to unit test than logic embedded in `quote!` interpolation.

### Generics must survive intact

A derive for this type:

```rust
struct Envelope<'a, T, const N: usize>
where
    T: Clone,
{
    name: &'a str,
    values: [T; N],
}
```

must generate an implementation with the same generic parameter declarations, type arguments, and `where` clause.

`syn::Generics::split_for_impl` produces three pieces:

```rust
let (impl_generics, type_generics, where_clause) =
    input.generics.split_for_impl();
```

Then:

```rust
quote! {
    impl #impl_generics ::field_names_core::FieldNames
        for #name #type_generics
        #where_clause
    {
        const FIELD_NAMES: &'static [&'static str] = &[#(#field_names),*];
    }
}
```

The positions are different:

- `impl_generics` includes declarations such as `<'a, T, const N: usize>`;
- `type_generics` includes arguments such as `<'a, T, N>`;
- `where_clause` preserves existing constraints.

Copying `#generics` into both positions is a common error because declaration syntax and use syntax are not interchangeable.

### Add bounds only when generated code needs them

The `FieldNames` implementation only emits string literals from identifiers. It does not use field values or field types, so it needs no additional bounds.

A different derive that formats every field might need `FieldType: Display`. Add those predicates to a cloned `Generics` value:

```rust
let mut generics = input.generics.clone();
let where_clause = generics.make_where_clause();
for field_type in field_types {
    where_clause
        .predicates
        .push(syn::parse_quote!(#field_type: ::std::fmt::Display));
}
```

This is more accurate than requiring every generic parameter `T: Display`, because a generic parameter may not appear in a formatted field, or a field type may be `Wrapper<T>` with a different implementation boundary.

Generated bounds are public constraints. Overconstraining a derive is an API defect even when examples compile.

### Do not imitate type checking through syntax matching

Suppose you want to support `Option<T>` fields specially. Inspecting the last path segment for the identifier `Option` may be a documented syntax convention, but it does not prove the path resolves to `std::option::Option`. It could be:

```rust
use another_crate::Option;
```

or a type alias.

There are three honest designs:

1. avoid special handling and generate generic trait-based code;
2. document that the derive recognizes a syntactic path form and accept the limitation;
3. require an explicit helper attribute that states intent.

Course 5’s `CommandArgs` derive later detects syntactic `Option<T>` because optional flags need structural generation. The capstone documents that supported type language rather than claiming semantic type recognition.

### Trait implementation versus inherent metadata

A derive can generate an implementation of a runtime trait:

```rust
pub trait FieldNames {
    const FIELD_NAMES: &'static [&'static str];
}
```

This creates a composable contract and lets generic code use the metadata. It also requires a stable path to the runtime crate.

An inherent associated constant avoids the runtime trait path:

```rust
impl Record {
    pub const FIELD_NAMES: &'static [&'static str] = &["id", "label"];
}
```

But it can collide with an existing associated item and is less useful in generic code.

The lab uses a runtime trait to make the path contract explicit. The starter and solution use a fixed local crate name; the chapter identifies dependency renaming as a production concern rather than hiding it.

### Error spans should identify the unsupported construct

Examples:

- union rejection should point at `union` or the item;
- tuple-struct rejection should point at the unnamed fields;
- duplicate helper option should point at the second option;
- empty rename should point at the string literal;
- unknown helper key should point at the key;
- conflicting `skip` and `rename` should combine both relevant spans if practical.

Do not return a generic error at the derive name when a field attribute caused the problem.

### Generated names and collisions

A trait implementation introduces no arbitrary helper item names. When helpers are necessary, prefer a private associated function or a distinctive module tied to the type name. Check whether the derive can be applied more than once through re-exports or aliases and whether two generated surfaces collide.

Custom derives should be idempotent only when the contract says so. Applying the same derive twice usually creates conflicting implementations and should remain an ordinary compiler error.

### Testing a derive

A complete derive suite includes:

#### Valid item shapes

- simple named struct;
- generic struct;
- lifetimes and const generics;
- existing `where` clause;
- skipped field;
- renamed field;
- raw identifiers if supported;
- preserved source order.

#### Invalid item shapes

- tuple struct;
- unit struct if names are required;
- enum;
- union;
- duplicate helper attribute;
- unknown helper key;
- conflicting options;
- invalid literal type.

#### Downstream contract

- trait path resolves;
- generated implementation is usable from generic code;
- no extra trait bounds appear;
- visibility behaves as documented.

Unit-test parsing helpers and normalized field models. Use compile fixtures for item-shape and generated-code evidence.

## Use the idea in a complete program

CommandForge’s `CommandArgs` derive uses the struct fields as the source of truth for command-line flags.

The supported source language is intentionally bounded:

```rust
#[derive(CommandArgs)]
struct RepeatArgs {
    #[arg(help = "text to repeat")]
    text: String,

    #[arg(default = "1", help = "number of repetitions")]
    times: u32,
}
```

The derive will:

- support named structs only;
- map `field_name` to `--field-name` unless `name = "..."` overrides it;
- support required `T: FromStr` fields;
- support syntactic `Option<T>` as optional flags;
- support string defaults parsed through the field type;
- reject duplicate, unknown, or conflicting helper options;
- generate `CommandArgs::decode` and a static usage string;
- preserve generics and existing `where` clauses;
- add only the bounds required by generated parsing.

The independent [Field Names Derive](../../labs/module-07-field-names-derive/README.md) is deliberately smaller. It isolates item inspection, helper attributes, order, generics, and runtime-trait generation before the capstone adds parsing behavior.

## Practice sequence

1. Parse a `DeriveInput` and classify its data shape.
2. Preserve generic declarations, type arguments, and `where` clauses separately.
3. Add one helper-attribute grammar with unknown-key rejection.
4. Generate a trait implementation with no unnecessary bounds.
5. Write compile-fail cases for every unsupported item shape.
6. Test source-order preservation and renamed/skipped fields.
7. Complete the field-names derive laboratory.
8. Implement CommandForge’s bounded `CommandArgs` derive and its generated usage contract.

## Ready to continue

Continue when you can state:

- exactly which item shapes the derive accepts;
- what structural facts it can know;
- which semantic facts remain for type checking;
- how helper attributes are parsed and validated;
- how generics and `where` clauses survive;
- which bounds are generated and why;
- which runtime path the expansion assumes;
- how unsupported input is diagnosed.

Do not continue if the derive drops generics, ignores unknown attributes, or recognizes types by spelling while claiming semantic certainty.

## Primary Rust references

- Rust Reference, derive macros: <https://doc.rust-lang.org/reference/procedural-macros.html#derive-macros>
- `syn::DeriveInput`: <https://docs.rs/syn/3.0.3/syn/struct.DeriveInput.html>
- `syn::Data`: <https://docs.rs/syn/3.0.3/syn/enum.Data.html>
- `syn::Attribute::parse_nested_meta`: <https://docs.rs/syn/3.0.3/syn/struct.Attribute.html#method.parse_nested_meta>
- `quote!`: <https://docs.rs/quote/1.0.47/quote/macro.quote.html>

## Continue

1. Complete the [Module 47 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 47 — Field Names Derive](../../labs/module-07-field-names-derive/README.md) from its public contract.
3. Apply the Module 47 increment in the [CommandForge engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
