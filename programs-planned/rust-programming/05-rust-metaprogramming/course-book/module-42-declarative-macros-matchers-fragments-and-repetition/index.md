# 42 — Declarative Macros: Matchers, Fragments, and Repetition

**Course 5, day 2 · Module 42 of 90**  
`██████████████░░░░░░` **42/90**

[← Module 41: Metaprogramming Boundaries and the Expansion Model](../module-41-metaprogramming-boundaries-and-expansion-model/index.md) · [Course 5 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 43: Recursive Macro Parsing and Token-Tree Techniques →](../module-43-recursive-macro-parsing-and-token-tree-techniques/index.md)

## The question

> How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?

## Why this comes now

Module 41 established that generation needs a source-of-truth argument and an ordinary-Rust reference. The first implementation mechanism is `macro_rules!` because it is integrated into the language, dependency-free, and intentionally limited. Its limitations are pedagogically useful: you must think in token patterns, fragment categories, repetition shape, and expansion position rather than pretending to inspect arbitrary Rust semantics.

Before recursive parsing, hygiene, or procedural macros, you need exact control over the declarative core.

## What you will be able to do

- Read a matcher as a grammar rather than as textual substitution.
- Choose fragment specifiers according to the accepted public language.
- Design unambiguous separators, delimiters, optional clauses, and cardinality.
- Keep matcher and transcriber repetition at compatible nesting depths.
- Preserve caller expression evaluation count and source order.
- Explain edition-sensitive fragment behavior and follow-set restrictions.
- Decide when a declarative grammar has become too complex for `macro_rules!`.

## Core model

### `macro_rules!` matches token structure

A declarative macro contains ordered rules. Each rule has a **matcher** and a **transcriber**:

```rust
macro_rules! pair {
    ($left:expr, $right:expr) => {
        ($left, $right)
    };
}
```

The matcher describes a token language. `$left:expr` means “one syntactically valid expression fragment,” not “some text until the comma.” The parser recognizes the fragment according to Rust grammar, then the comma separates it from the next fragment.

The transcriber does not paste raw characters. It reuses captured syntax inside newly produced tokens.

A macro invocation is matched one rule at a time. The first successful matcher supplies the expansion. The engine does not backtrack within a successful partial strategy to discover the API you intended. Rule order and grammar shape therefore matter.

```rust
macro_rules! classify {
    (none) => { None::<i32> };
    ($value:expr) => { Some($value) };
}
```

The specific token `none` should appear before the broad expression rule. In other designs, an identifier may also be a valid expression, and broad arms can make later arms unreachable or surprising.

### Fragment specifiers are API decisions

Common fragment kinds include:

- `ident` — an identifier or keyword accepted in identifier position;
- `path` — a type or value path;
- `ty` — a type;
- `expr` — an expression;
- `stmt` — a statement;
- `pat` and `pat_param` — patterns with edition-sensitive distinctions;
- `item` — an item;
- `block` — a block expression;
- `literal` — a literal expression token;
- `meta` — attribute contents;
- `vis` — possibly empty visibility;
- `lifetime` — a lifetime token;
- `tt` — one token tree.

The narrowest adequate fragment usually gives the clearest invocation and earliest error. If an API requires a type, use `ty`; accepting arbitrary token trees would postpone errors until the generated code is parsed.

```rust
macro_rules! typed_default {
    ($type:ty = $value:expr) => {{
        let value: $type = $value;
        value
    }};
}
```

This grammar states that the left side must parse as a type and the right side as an expression. Compare it with an unstructured version:

```rust
macro_rules! weak_typed_default {
    ($($anything:tt)*) => {
        /* later code must somehow interpret everything */
    };
}
```

`tt` is useful for forwarding syntax or implementing a deliberate token parser. It is not a universal escape hatch. Overusing it moves failures away from the source construct and makes the public grammar impossible to describe precisely.

#### Edition-sensitive fragments

Fragment behavior belongs to the edition in which the macro is **defined**. In Rust 2024, `expr` can match top-level underscore expressions and const block expressions; `expr_2021` exists when a macro needs the earlier boundary. Similarly, `pat` changed in Rust 2021 to include top-level or-patterns, while `pat_param` retains the narrower form.

Do not memorize these as trivia. Record the edition as part of a public macro’s compatibility surface. Upgrading the defining crate’s edition can alter which invocations match even when caller code is unchanged.

### Delimiters and separators define readability

Macro invocations can use parentheses, brackets, or braces. Delimiters should communicate the shape of the input:

- parentheses often suit one expression-like operation;
- brackets often suit list-like expressions;
- braces often suit item families or DSL blocks.

Inside a repetition, separators make boundaries explicit:

```rust
macro_rules! names {
    ($( $name:ident ),* $(,)?) => {
        &[ $( stringify!($name) ),* ]
    };
}
```

The matcher accepts zero or more identifiers separated by commas and an optional trailing comma. The transcriber mirrors the same repetition.

The operators are:

- `*` — zero or more;
- `+` — one or more;
- `?` — zero or one, without a separator.

Cardinality is product behavior. If an empty declaration is nonsensical, use `+` or a separate error arm. Accepting zero entries and failing later in generated code is weaker than expressing the grammar directly.

### Repetition depth is structural

A metavariable captured inside a repetition must be used at a compatible repetition depth. Consider:

```rust
macro_rules! tuples {
    ($( $left:expr => $right:expr ),+ $(,)?) => {
        [$(($left, $right)),+]
    };
}
```

`$left` and `$right` are captured once per entry and transcribed together once per entry. Their lengths and nesting structure remain aligned.

This is invalid:

```rust,compile_fail
macro_rules! broken {
    ($( $value:expr ),*) => {
        $value
    };
}
```

The transcriber asks for one `$value`, but the matcher captured a sequence. Rust rejects the repetition mismatch rather than selecting an arbitrary element.

Nested repetitions require the same reasoning at each level:

```rust
macro_rules! matrix {
    ($( [$( $value:expr ),* $(,)?] ),* $(,)?) => {
        [$( [$( $value ),*] ),*]
    };
}
```

Here `$value` lives two repetition levels deep. Flattening or moving it outside either level changes its structural meaning.

### Local ambiguity is an API defect

`macro_rules!` does not perform arbitrary lookahead to resolve ambiguous token ownership. A classic ambiguous shape is:

```rust,compile_fail
macro_rules! ambiguous {
    ($($name:ident)* $last:ident) => {};
}

ambiguous!(alpha beta gamma);
```

At `alpha`, the matcher cannot know whether the identifier belongs to the repetition or should be reserved for `$last`. More future tokens could resolve the intent, but the declarative matcher does not speculate that way.

Repair the language, not the compiler:

```rust
macro_rules! clear {
    ($($name:ident),* ; $last:ident) => {};
}

clear!(alpha, beta; gamma);
```

The semicolon is not noise. It creates an unambiguous boundary and improves diagnostics.

When syntax becomes hard to delimit, that is evidence about the DSL. A language requiring hidden lookahead or contextual interpretation may belong in a procedural parser rather than a more ingenious matcher.

### Follow-set restrictions protect future Rust grammar

Some fragments can be followed only by specific tokens in a matcher. An `expr` fragment, for example, cannot be followed by every arbitrary token. These restrictions prevent a macro definition from relying on a boundary that a future Rust expression could legally absorb.

Prefer conventional separators such as commas, semicolons, and `=>` where permitted. Do not design syntax around parser accidents.

A stable macro API should survive the language growing new expression or pattern forms. Follow-set rules force that conservatism at definition time.

### Expansion must preserve expression semantics

The most dangerous declarative bugs are not matcher failures. They are valid expansions with surprising runtime behavior.

#### Evaluate each caller expression once

```rust
macro_rules! insert_pairs {
    ($map:expr; $( $key:expr => $value:expr ),+ $(,)?) => {{
        let map = &mut $map;
        $(
            let key = $key;
            let value = $value;
            map.insert(key, value);
        )+
    }};
}
```

This expansion evaluates the map expression once, then each key and value once in source order. A weaker macro might repeat `$map`, `$key`, or `$value`, changing effects and move behavior.

#### Preserve source order deliberately

Rust evaluates statements in order, but a macro can rearrange repeated expressions in its transcriber. If an invocation accepts effectful expressions, document and test the order.

```rust
use std::cell::RefCell;

let events = RefCell::new(Vec::new());
let key = || {
    events.borrow_mut().push("key");
    1
};
let value = || {
    events.borrow_mut().push("value");
    2
};
```

A strong macro test asserts both the final collection and `events == ["key", "value"]`.

#### Avoid hidden control flow

A macro that emits `return`, `break`, `continue`, or `?` affects the caller’s control flow. Sometimes that is the contract, but it must be explicit. A function cannot return from its caller; a macro can emit a `return` token into caller code.

```rust
macro_rules! require_some {
    ($value:expr) => {
        match $value {
            Some(value) => value,
            None => return Err("missing value"),
        }
    };
}
```

This may be useful in private code, but it is a poor public abstraction if the name and documentation do not advertise caller-level early return.

### Expression blocks and temporary scope

Double braces are common in expression macros:

```rust
macro_rules! measured {
    ($value:expr) => {{
        let temporary = $value;
        (temporary, std::mem::size_of_val(&temporary))
    }};
}
```

The outer braces delimit the transcriber. The inner block becomes the generated expression and scopes helper bindings.

A generated block can change temporary lifetime relative to an unbraced expansion. This is often desirable, but it is part of semantics. Hand-expand and reason about drop order when references or guards are involved.

Generated helper names can also collide or become visible in diagnostics. Hygiene reduces some capture problems, but it does not remove the need for small scopes and intentional naming. Module 44 treats this in depth.

### Designing a typed collection macro

The Module 42 laboratory builds:

```rust
let map = typed_map! {
    String => u64;
    "alpha".to_owned() => 1,
    "beta".to_owned() => 2,
};
```

The grammar makes several decisions explicit:

- key type and value type are required once;
- there is at least one entry;
- entries use `=>` and comma separation;
- a trailing comma is accepted;
- each key and value is an expression;
- output is a `BTreeMap`, so iteration order is key order rather than insertion order;
- input expressions evaluate once in source order;
- duplicate keys use `BTreeMap::insert` semantics: later entries replace earlier values.

The type header is not needed merely for inference. It is part of the lab because it makes conversion policy explicit and gives errors at the assignment points generated for each expression.

A strong expansion is conceptually:

```rust
{
    let mut result: std::collections::BTreeMap<String, u64> =
        std::collections::BTreeMap::new();

    {
        let key: String = "alpha".to_owned();
        let value: u64 = 1;
        result.insert(key, value);
    }

    {
        let key: String = "beta".to_owned();
        let value: u64 = 2;
        result.insert(key, value);
    }

    result
}
```

Write this expansion before writing the macro. It reveals ownership, order, duplicate policy, and the path that must resolve.

### Matcher arms as diagnostics

A broad fallback arm can improve an error when used carefully:

```rust
macro_rules! nonempty_names {
    ($( $name:ident ),+ $(,)?) => {
        &[ $( stringify!($name) ),+ ]
    };
    () => {
        compile_error!("nonempty_names! requires at least one identifier")
    };
}
```

Do not add `($($tokens:tt)*)` to every macro. A catch-all can hide the compiler’s more precise “expected expression” or “no rules expected this token” diagnostic. Use a fallback only when you can identify a meaningful misuse and point to a clear repair.

### When `macro_rules!` is no longer the right parser

Move toward a procedural macro when several of these become true:

- the grammar requires semantic duplicate detection;
- error spans must point to multiple related declarations;
- many recursive states are required;
- syntax needs context-sensitive interpretation;
- matcher ambiguity forces awkward punctuation unrelated to the domain;
- generated code requires substantial item inspection;
- compile errors mostly come from deep fallback expansions;
- maintenance requires mentally simulating a parser rather than reading a grammar.

Declarative macros are excellent when their limits align with the language. Do not measure success by how far you can push those limits.

## Use the idea in a complete program

CommandForge’s first generated layer is a declarative diagnostic catalog. The invocation will eventually own a variant, numeric code, and message:

```rust
commandforge::diagnostic_catalog! {
    pub enum DiagnosticCode {
        Usage = 64 => "invalid command usage";
        Input = 65 => "invalid input data";
        Internal = 70 => "internal command failure";
    }
}
```

Before implementing it, define the contract:

- one or more entries;
- semicolon-terminated declarations;
- identifier variant names;
- integer literal codes;
- string literal messages;
- generated enum, `code`, `message`, `from_code`, and `Display`;
- declaration order preserved in a generated constant slice;
- duplicate codes are not detectable reliably with plain matching and must be tested or moved to a later mechanism if compile-time semantic rejection is required.

This last point is important. Do not claim a check the mechanism does not perform.

The independent [Typed Map Macro](../../labs/module-02-typed-map-macro/README.md) focuses on repetition shape, evaluation, ownership, and duplicate semantics without the additional public-API surface of the capstone.

## Practice sequence

1. Annotate ten matchers with their accepted grammar in EBNF-like prose.
2. Replace three `tt` fragments with narrower fragments and compare diagnostics.
3. Repair one ambiguous matcher by changing the public syntax.
4. Hand-expand nested repetition and mark each metavariable’s depth.
5. Instrument an expression macro to prove evaluation count and order.
6. Write one targeted `compile_error!` arm and reject one unnecessary catch-all.
7. Build the typed-map laboratory and defend its duplicate policy.
8. Implement the declarative diagnostic catalog for CommandForge.

## Ready to continue

Continue when you can read a `macro_rules!` definition and state:

- its grammar and cardinality;
- the role of every separator;
- the fragment class of every metavariable;
- the repetition depth of every capture;
- the expansion category;
- expression evaluation count and order;
- ownership consequences;
- the point at which the grammar should migrate to procedural parsing.

Do not continue if your debugging method is to change `expr` to `tt`, add catch-all arms, or raise recursion limits without explaining the grammar.

## Primary Rust references

- Rust Reference, macros by example: <https://doc.rust-lang.org/reference/macros-by-example.html>
- Rust Reference, fragment specifiers and edition differences: <https://doc.rust-lang.org/reference/macros-by-example.html#metavariables>
- Rust Reference, repetition: <https://doc.rust-lang.org/reference/macros-by-example.html#repetitions>
- Rust Reference, follow-set ambiguity restrictions: <https://doc.rust-lang.org/reference/macros-by-example.html#follow-set-ambiguity-restrictions>

## Continue

1. Complete the [Module 42 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 42 — Typed Map Macro](../../labs/module-02-typed-map-macro/README.md) from its public contract.
3. Apply the Module 42 increment in the [CommandForge engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
