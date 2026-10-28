# 43 — Recursive Macro Parsing and Token-Tree Techniques

**Course 5, day 3 · Module 43 of 90**  
`██████████████░░░░░░` **43/90**

[← Module 42: Declarative Macros: Matchers, Fragments, and Repetition](../module-42-declarative-macros-matchers-fragments-and-repetition/index.md) · [Course 5 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros →](../module-44-hygiene-scope-paths-and-cross-crate-macros/index.md)

## The question

> How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?

## Why this comes now

Module 42 treated one matcher as a grammar and one repetition as a structured sequence. Some useful declarative languages need state: an optional section changes what may follow, tokens must be accumulated before emission, or entries are consumed one at a time. `macro_rules!` can model those cases through recursive expansion.

Recursion is also where declarative metaprogramming becomes dangerous. A token-tree muncher can hide nontermination, duplicate work, poor errors, and an accidental language no one can maintain. This module therefore teaches recursive parsing together with a migration rule: knowing when to stop using it is part of mastery.

## What you will be able to do

- Model recursive macro rules as parser states and transitions.
- Prove that each recursive step consumes input or reaches a base case.
- Use internal arms and accumulators without exposing implementation syntax.
- Distinguish token-tree recursion from arbitrary semantic parsing.
- Control expansion depth and avoid accidental quadratic work.
- Design targeted failure states instead of swallowing unknown tokens.
- Decide when a procedural parser is the smaller and safer mechanism.

## Core model

### Recursion is parser execution

A recursive declarative macro is easiest to understand as a small state machine. The invocation supplies an input token stream. An internal rule consumes a prefix, updates parser state, and invokes the macro again with the unconsumed suffix.

A minimal token counter illustrates the shape:

```rust
macro_rules! count_tokens {
    () => { 0usize };
    ($head:tt $($tail:tt)*) => {
        1usize + count_tokens!($($tail)*)
    };
}

assert_eq!(count_tokens!(alpha + beta), 3);
```

The recursive arm consumes one token tree as `$head` and passes only `$tail`. The empty-input arm terminates.

The central proof obligation is:

> For every recursive arm, what strictly decreases?

Usually it is the number of unconsumed token trees. If the recursive call receives the same input, the grammar does not progress:

```rust,compile_fail
macro_rules! never_finishes {
    ($($tokens:tt)*) => {
        never_finishes!($($tokens)*)
    };
}
```

Raising `recursion_limit` does not repair this macro. It only postpones detection.

### Public arms and internal states

A common convention marks internal parser states with a token such as `@parse`, `@acc`, or `@emit`:

```rust
macro_rules! sum_literals {
    ($($input:tt)*) => {
        sum_literals!(@acc 0u64; $($input)*)
    };

    (@acc $total:expr;) => {
        $total
    };

    (@acc $total:expr; $next:literal $(, $($rest:tt)*)?) => {
        sum_literals!(@acc $total + $next; $($($rest)*)?)
    };
}
```

The public arm accepts the documented language. Internal arms encode implementation state. The `@acc` token is not special Rust syntax; it is merely a token pattern unlikely to collide with the public grammar.

Do not treat internal arms as private in the same sense as module-private functions. A caller can attempt to invoke them if the macro is visible. The convention prevents accidental overlap and communicates intent, but the public contract should still be robust if internal-looking tokens are supplied. Exported recursive macros need especially careful arm ordering and diagnostics.

### Accumulators carry syntax, not values

During expansion, an accumulator is captured token structure. It is not a runtime variable unless the final expansion creates one.

```rust
macro_rules! make_tuple {
    ($($input:tt)*) => {
        make_tuple!(@collect [] $($input)*)
    };

    (@collect [$($out:expr,)*]) => {
        ($($out,)*)
    };

    (@collect [$($out:expr,)*] $next:expr; $($rest:tt)*) => {
        make_tuple!(@collect [$($out,)* $next,] $($rest)*)
    };
}
```

The bracketed accumulator is a sequence of expression fragments to be transcribed later. Nothing is evaluated while the macro is recursively matching. Evaluation happens only in the expanded tuple expression.

This distinction prevents a common wrong model: “the macro loops over expressions.” It does not execute those expressions. It repeatedly transforms token structure until it emits Rust that will later execute.

### Token trees are grouped lexical structure

A `tt` fragment matches one token tree:

- an identifier;
- a literal;
- one punctuation token;
- a delimited group and everything nested inside it.

The group is one token tree even if it contains many tokens.

```rust
macro_rules! one_tree {
    ($value:tt) => { stringify!($value) };
}

assert_eq!(one_tree!((alpha + beta)), "(alpha + beta)");
```

Without the parentheses, `alpha + beta` is three token trees and does not match one `$value:tt`.

Recursive parsers work at this structural level. They can distinguish keywords you choose, delimiters, identifiers, literals, and fragments recognized by the Rust parser. They do not gain arbitrary lookahead or type information merely because recursion is involved.

### Design parser states before rules

Before writing a token muncher, make the state graph explicit.

The Module 43 laboratory accepts:

```rust
state_machine! {
    pub enum PublicationState {
        states: [Draft, Review, Published];
        transitions:
            Draft => Review;
            Review => Draft;
            Review => Published;
    }
}
```

A useful parser decomposition is:

```text
Start
  ├─ expect visibility
  ├─ expect `enum`
  ├─ expect enum identifier
  └─ enter body

Body
  ├─ parse `states: [...] ;`
  └─ enter transitions

Transitions
  ├─ parse `From => To ;`, consume one entry, remain in state
  ├─ reach `}`, emit Rust
  └─ reject unknown token with a targeted message
```

In this lab, most outer structure can be matched in one public arm. Recursion is used for the transition list so the progress rule is visible and the generated membership expression can be accumulated.

Writing the state graph first reveals whether `macro_rules!` is appropriate. If the graph contains dozens of states, contextual backtracking, or semantic symbol tables, use a procedural parser.

### A recursive boolean expansion

Declarative macros cannot conveniently emit arbitrary fragments such as a bare sequence of match arms in every context. An expression-oriented recursion is often simpler.

```rust
macro_rules! transition_allowed {
    ($current:expr, $next:expr;) => {
        false
    };

    ($current:expr, $next:expr;
        $from:ident => $to:ident;
        $($rest:tt)*) => {
        matches!(
            ($current, $next),
            (Self::$from, Self::$to)
        ) || transition_allowed!(
            $current,
            $next;
            $($rest)*
        )
    };
}
```

Each recursive step consumes one transition declaration. The base case yields `false`. The final generated expression is a chain of short-circuiting boolean operations.

This has clear runtime semantics:

- `current` and `next` must not be expanded repeatedly if they are effectful expressions;
- a method should bind them once before invoking the helper;
- transitions are checked in source order;
- the first matching pair short-circuits;
- cost is linear in the number of declared transitions.

The expansion is acceptable for a small fixed machine. For hundreds of transitions, generated match arms or a table may be more appropriate. The macro design includes the runtime cost of the emitted structure.

### Avoid repeated parsing work

A naïve TT muncher often has quadratic matching behavior. At each recursive call, the matcher may scan a large remaining suffix to find a shape. Consuming one token at a time through a broad `$($tail:tt)*` can amplify compile time for large inputs.

You do not need compiler-internal complexity formulas to use a practical rule:

- keep declarative DSLs small and bounded;
- consume meaningful units, not one punctuation token when an entry can be captured at once;
- avoid many overlapping recursive arms with broad prefixes;
- measure compile time before claiming a large declarative language is cheap;
- migrate to a procedural parser when input size or grammar complexity grows.

A parser that is elegant for ten declarations may be hostile at ten thousand.

### Error states belong in the grammar

A recursive macro should not silently discard unsupported tokens.

Weak design:

```rust
macro_rules! parse_flags {
    (@parse $($known:tt)* ; $unknown:tt $($rest:tt)*) => {
        parse_flags!(@parse $($known)* ; $($rest)*)
    };
}
```

The fallback consumes anything it does not understand. Misspelled configuration becomes invisible.

Better design:

```rust
macro_rules! parse_flags {
    (@parse [$($known:ident,)*]) => {
        &[$(stringify!($known)),*]
    };

    (@parse [$($known:ident,)*] + $next:ident $($rest:tt)*) => {
        parse_flags!(@parse [$($known,)* $next,] $($rest)*)
    };

    (@parse [$($known:ident,)*] $unexpected:tt $($rest:tt)*) => {
        compile_error!(concat!(
            "expected `+ <identifier>`, found `",
            stringify!($unexpected),
            "`"
        ))
    };
}
```

The targeted error owns a real parser state. It is not a universal catch-all attached without context.

Remember that `compile_error!` reports at the invocation expansion; it may not give the same fine-grained span quality as `syn::Error::new_spanned` in a procedural macro. That difference is one migration signal.

### Recursion limits are not design parameters

Rust limits recursive expansion. Deep legitimate macros may require a crate-level `#![recursion_limit = "..."]`, but changing the limit should follow a proof:

- input size is intentionally bounded;
- every step consumes a known unit;
- the required depth is proportional to that bound;
- compile-time cost is acceptable;
- a flatter repetition or procedural parser would not be simpler.

If users must guess a larger limit after ordinary inputs, the macro API is exposing its implementation pathology.

### Recursive macros and evaluation count

A token can be transcribed at every recursive level accidentally.

```rust
macro_rules! bad_trace {
    ($value:expr;) => { $value };
    ($value:expr; $head:tt $($tail:tt)*) => {{
        let _ = $value;
        bad_trace!($value; $($tail)*)
    }};
}
```

The caller expression may execute once per token plus the base case. Bind before recursion in generated runtime code, or carry an identifier referring to one binding rather than retranscribing the original expression.

```rust
macro_rules! trace_once {
    ($value:expr; $($tokens:tt)*) => {{
        let value = $value;
        trace_once!(@walk value; $($tokens)*)
    }};
    (@walk $value:ident;) => { $value };
    (@walk $value:ident; $head:tt $($tail:tt)*) => {
        trace_once!(@walk $value; $($tail)*)
    };
}
```

The public arm evaluates once. Internal recursion moves only token identifiers.

### When recursion is appropriate

A recursive declarative parser is reasonable when:

- the input is small and intentionally bounded;
- the grammar is prefix-decidable;
- states can be named clearly;
- each step consumes a whole entry;
- semantic validation is minimal;
- error messages remain local and understandable;
- generated code is compact;
- no external dependency is justified.

It is not a badge of expertise. The best macro may be the one that uses a single repetition and leaves validation to generated types.

### Migration criteria

Move to a function-like procedural macro when you need:

- duplicate-name or cross-entry validation;
- multiple accumulated errors;
- precise spans on related tokens;
- a typed AST with reusable phases;
- context-sensitive grammar;
- clearer asymptotic parsing for large input;
- normalization before generation;
- testable parsing without compiling every fixture.

Do not wait until the recursive macro is unreadable. Migrate when the model becomes clearer as ordinary parser code.

## Use the idea in a complete program

CommandForge does not need recursive `macro_rules!` parsing for its final command catalog; Module 49 will use a typed procedural DSL because duplicate detection and cross-entry diagnostics are required. That rejection is itself part of the capstone.

Module 43 contributes a smaller declarative helper: a private parser for field-option syntax in a diagnostic declaration. You will compare two designs:

1. a recursive `macro_rules!` helper handling a tiny bounded option list;
2. a direct explicit grammar with no recursion.

Keep the direct grammar unless the recursive form removes a real repeated relation. Record the rejected design in the capstone notes. Production architecture improves when you can explain why a powerful technique is absent.

The independent [State Machine DSL](../../labs/module-03-state-machine-dsl/README.md) is the place to construct and test recursion fully. It generates an enum and transition check from one declaration, proves progress for each recursive step, and rejects malformed transition syntax at the parser boundary.

## Practice sequence

1. Draw the state graph for three recursive macros before reading their rules.
2. Mark the decreasing input measure in every recursive arm.
3. Repair one unchanged-input recursion without increasing the recursion limit.
4. Convert one token-at-a-time muncher into entry-at-a-time consumption.
5. Instrument a recursive expansion to prove a caller expression runs once.
6. Add a targeted failure state for an unsupported token.
7. Build and test the state-machine laboratory.
8. Write a migration memo explaining why CommandForge’s catalog belongs in Module 49 rather than in a TT muncher.

## Ready to continue

Continue when you can explain a recursive macro as:

- a finite set of parser states;
- a public grammar and internal state grammar;
- a decreasing measure;
- a base case;
- an accumulator shape;
- a generated runtime structure and cost;
- a set of targeted failure states;
- a clear threshold for procedural migration.

Do not continue if recursion is “working” only because the input is tiny, the recursion limit was raised, or unknown tokens are ignored.

## Primary Rust references

- Rust Reference, macro matching and transcription: <https://doc.rust-lang.org/reference/macros-by-example.html>
- Rust Reference, token trees and macro invocation: <https://doc.rust-lang.org/reference/macros.html>
- Rust Reference, macro repetition: <https://doc.rust-lang.org/reference/macros-by-example.html#repetitions>
- Rust Reference, macro scoping: <https://doc.rust-lang.org/reference/macros-by-example.html#scoping-exporting-and-importing>

## Continue

1. Complete the [Module 43 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 43 — State Machine DSL](../../labs/module-03-state-machine-dsl/README.md) from its public contract.
3. Apply the Module 43 increment in the [CommandForge engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
