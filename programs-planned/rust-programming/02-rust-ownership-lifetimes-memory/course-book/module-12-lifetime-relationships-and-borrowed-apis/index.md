# Module 12 — Lifetime Relationships and Borrowed APIs

**Course 2 · Day 2 · Module 12 of 100**
`███░░░░░░░░░░░░░░░░░░░░░░` **12/100**

[Program](../../../README.md) · [Course 2](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-02-zero-copy-records/README.md) · [Memory Workspace guide](../capstone.md)

[← Module 11: Places, Move Paths, and Advanced Borrowing](../module-11-places-move-paths-and-advanced-borrowing/index.md) · [Module 13: Scoped Access and Escape Prevention →](../module-13-scoped-access-and-escape-prevention/index.md)

## The question

> What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?

## Why this comes now

After you can identify the exact place being borrowed, you can ask the deeper question: from which owner may a returned reference remain valid? Lifetimes are introduced as relationships among borrows, not as storage controls. The module develops a derivation method so annotations follow provenance instead of guesswork.

### Prerequisite bridge

Module 11 established **Places, Move Paths, and Advanced Borrowing**. Before continuing, verify that you can repair ownership conflicts by changing topology or phases before considering clone, refcell, or unsafe code. This module preserves that capability and adds the ability to translate lifetime syntax into constraints among borrows rather than durations attached to values. Module 13, **Scoped Access and Escape Prevention**, will rely on both when it asks: *Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?*

### Scope boundary

This module owns the reasoning for **lifetime relationships and borrowed apis** inside Course 2. The course remains centered on safe public APIs. It explains the memory obligations behind smart pointers, interior mutability, layout, variance, and pinning, but manual allocation, raw-pointer implementation, FFI, threads, and async execution remain later responsibilities. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Translate lifetime syntax into constraints among borrows rather than durations attached to values.
- Derive elision and explicit relationships for one-source and multiple-source APIs.
- Use lifetime shortening and subtyping in ordinary covariant borrowed views without extending provenance.
- Design structs and enums containing references while accounting for temporary and drop scopes.
- Reject unnecessary lifetime coupling and choose owned output when retention must outlive input borrowing.

## Core model

### Lifetimes are constraints among references

A lifetime parameter does not store elapsed time and does not extend a value's existence. It names a relationship the compiler must satisfy among borrows. Read a signature by asking which input allocation may be the provenance of each returned reference.

```rust
pub fn first_line(input: &str) -> &str {
    input.lines().next().unwrap_or("")
}
```

Elision derives one input lifetime and assigns it to the output. Expanded:

```rust
pub fn first_line<'a>(input: &'a str) -> &'a str
```

This says: for a call with some valid borrow `'a`, the output is borrowed from `input` and cannot be used beyond that relation. It does not say the original owner lives exactly `'a` or that the annotation keeps it alive.

### Multiple sources

```rust
pub fn choose<'a>(left: &'a str, right: &'a str, flag: bool) -> &'a str {
    if flag { left } else { right }
}
```

At a call, `'a` must be a region compatible with whichever returned reference may flow out and both input constraints. In ordinary use it can be shortened to a region no longer than the relevant borrows. The two source values need not have equal lexical scopes.

Unnecessary coupling:

```rust
pub fn left_word<'a>(left: &'a str, delimiter: &str) -> &'a str {
    left.split(delimiter).next().unwrap_or("")
}
```

The delimiter is read only during the call and is not a source of the output. Giving it `'a` would reject valid calls for no semantic reason.

### Outlives notation

`'long: 'short` means `'long` outlives `'short`; a borrow valid for the longer region can be shortened for a covariant shared-reference use. `T: 'a` means every non-static borrow contained in `T` is valid for `'a`. It does not mean an owned `T` value is kept alive until `'a`.

```rust
fn hold_for<'a, T: 'a>(value: T, _marker: &'a ()) -> T {
    value
}
```

For `T = String`, the bound is trivially satisfied because `String` contains no borrowed reference. The local `String` can still be dropped when its owner leaves scope.

### Reference-bearing types

```rust
#[derive(Debug, Clone, Copy)]
pub struct RecordView<'a> {
    pub key: &'a str,
    pub value: &'a str,
}

pub fn parse_record(line: &str) -> Option<RecordView<'_>> {
    let (key, value) = line.split_once('=')?;
    Some(RecordView {
        key: key.trim(),
        value: value.trim(),
    })
}
```

The view is useful while the input buffer remains valid. It is inappropriate for a queue that must retain records after the buffer is replaced. In that case convert to an owned record at the retention boundary.

### Temporary and drop scopes

A reference can be valid for its use even when the owner is a temporary, but temporary lifetime rules are precise and context-dependent. Do not rely on “temporaries live until the end of the statement” as a universal design method. Bind owned values explicitly when a borrow must cross statements.

```rust
let owned = format!("{}={}", "mode", "strict");
let record = parse_record(&owned).expect("well-formed generated record");
println!("{}", record.value);
```

Returning a reference to a local owner remains invalid:

```rust,compile_fail
fn invalid() -> &'static str {
    let text = String::from("local");
    &text
}
```

Adding `'static` only states an impossible requirement more loudly.

### Worked derivation: parser source and scratch state

A parser may borrow input for output but borrow a mutable diagnostics buffer only during parsing:

```rust
pub fn parse_with_diagnostics<'src>(
    source: &'src str,
    diagnostics: &mut Vec<String>,
) -> Vec<RecordView<'src>> {
    let mut records = Vec::new();
    for (line_index, line) in source.lines().enumerate() {
        match parse_record(line) {
            Some(record) => records.push(record),
            None => diagnostics.push(format!("line {} is malformed", line_index + 1)),
        }
    }
    records
}
```

The diagnostics lifetime is independent because no returned value borrows it. A one-lifetime signature tying both inputs to `'src` would needlessly extend the mutable borrow and reject callers.

### Zero-copy is a scoped property

The record fields borrow subslices of the source; they allocate no field strings. The returned `Vec` still allocates its element storage, diagnostics may allocate, and later ownership conversion allocates. State exactly which bytes are borrowed and which structures allocate.

### Derive it yourself

Design a query function returning a title borrowed from a workspace plus an owned score computed from a short-lived configuration. Annotate only the output provenance. Then redesign it for a caller that must retain the title after the workspace can mutate.

### Misconception clinic

- One named lifetime denotes a constraint variable, not equal runtime duration.
- `'static` on a reference is a strong validity requirement, not “global-ish.”
- Lifetime annotations cannot make a local owner survive return.
- Borrowed output is not automatically better; retention and mutation requirements decide ownership.

A lifetime parameter does not create storage, delay destruction, or alter runtime control flow. It names a region used by type checking so the compiler can compare the validity of references.

Consider:

```rust
fn first_word<'text>(text: &'text str) -> &'text str {
    text.split_whitespace().next().unwrap_or("")
}
```

Read this as:

> For any borrow region `'text` chosen by the caller, if the function receives a string slice valid for `'text`, the returned slice is valid for at most that same region and originates from data covered by that borrow.

The function does not promise that the returned slice lives exactly as long as the input borrow. The compiler may shorten it at the call site. Nor does it promise that the owner itself is destroyed at the end of `'text`; the owner may live much longer.

### Regions are not usually named runtime intervals

The compiler reasons over points in control flow. A source-level lifetime name summarizes constraints among those points. Saying “the lifetime starts here and ends at this brace” is often too crude, especially under non-lexical lifetime analysis.

A practical model is a set of program points at which a reference may be used. The compiler checks that the referent remains valid at every point in that set and that conflicting access does not occur.

### The caller chooses concrete lifetimes

Generic lifetime parameters are quantified. A function such as `first_word` must work for a short local borrow, a longer borrow from a struct, or a string literal. The implementation cannot assume a particular duration.

```rust
let owned = String::from("memory contracts");
let word = first_word(&owned);
println!("{word}");
```

The call instantiates `'text` with a region no longer than the borrow of `owned` and no longer than the final use of `word`.

### Output relationships matter most

Input-only lifetimes often disappear under elision. Explicit names become necessary when the output can borrow from more than one source or when a type stores references.

```rust
fn choose<'a>(left: &'a str, right: &'a str, take_left: bool) -> &'a str {
    if take_left { left } else { right }
}
```

Here the returned reference may originate from either input. The caller must supply borrows with some common region that covers the returned use. The compiler can usually choose the intersection—the shorter usable region—not force the owners to have identical physical lifetimes.

### An annotation cannot legalize an invalid source

```rust,compile_fail
fn invalid<'a>() -> &'a str {
    let local = String::from("gone");
    local.as_str()
}
```

No caller-supplied `'a` can make the local allocation survive return. The implementation cannot meet its promise.

### Write the prose contract first

Before adding names, complete:

- The returned reference points into ______.
- That owner is reached through parameter ______.
- Input ______ is used only during the call and is unrelated to the output.
- The output must not survive mutation/destruction of ______.

Then encode only those relationships. Lifetime syntax should be the final translation of an ownership argument, not the beginning of one.

Lifetime elision is not inference magic that makes relationships unknowable. It is a small set of rules for common function signatures.

### Rule 1: each elided input reference gets its own lifetime

```rust
fn compare(left: &str, right: &str) -> bool
```

Conceptually begins as:

```rust
fn compare<'left, 'right>(left: &'left str, right: &'right str) -> bool
```

There is no borrowed output, so no further relationship is needed.

### Rule 2: one input lifetime flows to all elided output references

```rust
fn trim(text: &str) -> &str
```

becomes:

```rust
fn trim<'text>(text: &'text str) -> &'text str
```

This is why the ordinary accessor `fn title(&self) -> &str` is enough when only the receiver can provide the output.

### Rule 3: a receiver lifetime flows to elided outputs

```rust
impl Document {
    fn line(&self, index: usize) -> Option<&str> { /* ... */ }
}
```

The output is tied to the borrow of `self`, even if other reference parameters exist:

```rust
fn find_after(&self, prefix: &str) -> Option<&str>
```

Conceptually:

```rust
fn find_after<'self_ref, 'prefix>(
    &'self_ref self,
    prefix: &'prefix str,
) -> Option<&'self_ref str>
```

This receiver rule is useful but can hide mistaken assumptions. Always identify the source explicitly in your lifetime ledger.

### When elision fails

```rust,compile_fail
fn choose(left: &str, right: &str, flag: bool) -> &str {
    if flag { left } else { right }
}
```

Two input lifetimes exist and no receiver decides the output. The signature must say whether the output comes from one input or either.

If it always comes from `left`, use:

```rust
fn choose_left<'left>(left: &'left str, right: &str) -> &'left str {
    let _ = right;
    left
}
```

If it may come from either, link both to a common lifetime:

```rust
fn choose_either<'a>(left: &'a str, right: &'a str, flag: bool) -> &'a str {
    if flag { left } else { right }
}
```

### Elision in path types

Reference-bearing type arguments may use `'_` when the exact inferred lifetime should be visible but unnamed:

```rust
fn view(document: &Document) -> DocumentView<'_> {
    DocumentView { document }
}
```

`'_` says “there is a lifetime parameter here; infer it from context.” It is different from omitting a required generic argument entirely.

### Elision does not mean omission from design

A reviewer should be able to expand every public elided signature. This is especially important for methods returning guards or iterators. The returned value may keep `self` borrowed for much longer than the method call appears to last.

```rust
fn titles(&self) -> impl Iterator<Item = &str> + '_
```

The `+ '_` makes the captured receiver lifetime explicit in the opaque return type. Without understanding that relation, callers may be surprised that the workspace cannot be mutated while the iterator remains live.

### Derivation exercise

For every accessor in the capstone, write the fully expanded signature in the design notes, then keep the source code elided where it remains unambiguous. Precision is not measured by punctuation count; it is measured by whether the relationship can be reconstructed.

When an API combines references, distinguish three different claims:

1. two references happen to be valid at the same program point;
2. one reference must remain valid for at least as long as another region;
3. a type may contain borrowed data that must remain valid for a region.

Rust expresses these with shared lifetime parameters and outlives bounds.

### Shared parameter: common usable region

```rust
fn common_prefix<'a>(left: &'a str, right: &'a str) -> (&'a str, &'a str) {
    let length = left.bytes().zip(right.bytes()).take_while(|(a, b)| a == b).count();
    (&left[..length], &right[..length])
}
```

The returned slices borrow from different owners but are both exposed for a common region `'a`. At a call, the compiler can choose a region no longer than either input borrow.

### Outlives relation: `'long: 'short`

Read:

```rust
'long: 'short
```

as “`'long` outlives `'short`” or “a reference valid for `'long` can be shortened for use where `'short` is required.” It does not compare owner construction times directly; it states a region inclusion constraint.

A function can make the shortening explicit:

```rust
fn shorten<'short, 'long: 'short>(value: &'long str) -> &'short str {
    value
}
```

This is mainly pedagogical because ordinary coercion often handles it.

### Type outlives: `T: 'a`

`T: 'a` means every borrowed component contained in `T` is valid for at least `'a`. It does **not** mean the value of type `T` is allocated for `'a`, and it says nothing special for types containing no non-static references.

```rust
struct Holder<'a, T: 'a> {
    value: T,
    marker: &'a (),
}
```

Modern Rust infers many obvious outlives bounds, so explicit `T: 'a` appears less frequently than older material suggests. When it appears, translate it structurally: what references might `T` contain?

### Independent sources should stay independent

Overconstrained:

```rust
struct Search<'a> {
    corpus: &'a Corpus,
    query: &'a str,
}
```

This says the corpus borrow and query borrow use one common lifetime in every `Search` value. That may be acceptable because the compiler can shorten both, but it prevents expressing a search value whose query is replaced independently without reconstructing the whole object.

More precise:

```rust
struct Search<'corpus, 'query> {
    corpus: &'corpus Corpus,
    query: &'query str,
}
```

Do not multiply lifetimes automatically; use separate names when the fields genuinely have independent validity and operations benefit from that independence.

### Returning one of several sources

When a result variant reveals which owner it borrows from, an enum can retain distinct lifetimes:

```rust
enum Found<'left, 'right> {
    Left(&'left str),
    Right(&'right str),
}
```

This is more expressive than forcing both into one `'a`, but callers must handle a result whose type carries both possibilities. Design is a trade: precision can increase type complexity.

### Outlives bounds are obligations, not repairs

Adding `'a: 'b` until code compiles can accidentally require a long-lived input the product does not possess. Derive the relation from the returned or stored reference. If there is no ownership argument for the bound, the design may need owned data, a scoped callback, or a different representation.

Rust permits a reference valid for a longer region to be used where a shorter one is required. This is the most important form of subtyping in everyday Rust.

If `'long: 'short`, then `&'long T` can usually be coerced to `&'short T`. The longer-lived reference satisfies the weaker requirement.

### Shared reference shortening

```rust
fn print_now(value: &str) {
    println!("{value}");
}

let owned = String::from("long enough");
let long = &owned;
print_now(long);
```

The call uses `long` for the shorter duration of `print_now`. No new allocation or runtime object is created.

### Mutable reference reborrowing

`&mut T` also supports shortening of its lifetime through reborrowing:

```rust
fn increment(value: &mut i32) {
    *value += 1;
}

fn twice(value: &mut i32) {
    increment(&mut *value);
    increment(&mut *value);
}
```

Each call receives a shorter exclusive reference. The original reference cannot be used during the reborrow, then becomes usable again.

### Why `&mut` is not simply “more lifetime-flexible”

Module 19 will show that `&'a mut T` is covariant in `'a` but invariant in `T`. Lifetime shortening of the reference itself is allowed; replacing the referenced *type* with one containing a shorter lifetime is not generally allowed because mutable access permits write-back.

This distinction resolves many confusing errors. For now, record separately:

- lifetime of the outer mutable reference;
- type stored behind it, which may itself contain references.

### Assignments can preserve an unexpectedly long lifetime

```rust,compile_fail
fn assign<'a>(slot: &mut &'a str, value: &str) {
    *slot = value;
}
```

The slot promises to contain a reference valid for `'a`. The unconstrained `value` may be shorter. Mutation would allow the shorter reference to escape through the longer-typed slot. The correct signature is:

```rust
fn assign<'a>(slot: &mut &'a str, value: &'a str) {
    *slot = value;
}
```

The issue is not the lifetime of `&mut` itself; it is the invariant referenced type `&'a str` under mutation.

### Reborrowing affects method chains and loops

An exclusive reference can be reborrowed for each iteration:

```rust
fn apply_all(value: &mut String, suffixes: &[&str]) {
    for suffix in suffixes {
        append(value, suffix);
    }
}
```

Passing `value` does not permanently move it on the first iteration because the call receives a reborrow. In generic contexts or assignments, explicit `&mut *value` can clarify intent.

### Shortest region, strongest usability

A public API should not force a borrow to last longer than the returned value or guard requires. Returning an owned count rather than an iterator can free mutation immediately. Returning an iterator is appropriate when lazy borrowed traversal is valuable, but callers must understand that the iterator extends the borrow.

Lifetime subtyping gives the compiler flexibility. Good API design gives the caller flexibility by avoiding unnecessary relationships in the first place.

A type that stores a reference must state that it cannot outlive the referenced data.

```rust
struct Line<'doc> {
    number: usize,
    text: &'doc str,
}
```

Read `Line<'doc>` as “a line view containing text valid for `'doc`.” The lifetime is part of the type and propagates through functions, collections, and return values.

### Implementation blocks

```rust
impl<'doc> Line<'doc> {
    fn text(&self) -> &str {
        self.text
    }

    fn split_once(&self, delimiter: char) -> Option<(&str, &str)> {
        self.text.split_once(delimiter)
    }
}
```

The accessor's output is elided to the borrow of `self`, which may be shorter than `'doc`. This is usually correct: a caller borrowing the `Line` briefly does not automatically receive a reference typed for the full underlying document lifetime.

When you need to return the stored reference at its original lifetime, consuming the view can make that relation explicit:

```rust
impl<'doc> Line<'doc> {
    fn into_text(self) -> &'doc str {
        self.text
    }
}
```

Because `self` is consumed, there is no shorter receiver borrow controlling the output.

### Multiple borrowed fields

```rust
struct Comparison<'left, 'right> {
    left: &'left str,
    right: &'right str,
}
```

Use one lifetime only if the fields are intentionally coupled. Separate parameters make it possible to retain a long-lived left value while replacing or constructing a short-lived right comparison.

### Enums preserve source identity

```rust
enum Token<'src> {
    Word(&'src str),
    Number(&'src str),
    Punctuation(char),
}
```

Owned variants do not need `'src`, but the enum as a whole carries it because some variants borrow. A vector of tokens cannot outlive the source. This is a zero-copy design with a clear ownership dependency.

### Self-referential temptation

This does not work:

```rust,compile_fail
struct Parsed {
    source: String,
    first_word: &str,
}
```

Even with a lifetime parameter, a field cannot ordinarily borrow another field of the same movable struct. Construction would need a reference before the final value is in place, and moving the struct could invalidate an internal reference. Module 13 studies alternatives; Module 20 explains when pinning enters.

### Borrowed versus owned view types

A reference-bearing view is appropriate when:

- creation is cheap and frequent;
- the owner remains naturally available;
- no mutation that invalidates the view should occur concurrently;
- the caller benefits from zero-copy slices.

An owned result is stronger when:

- it must outlive the source;
- it crosses threads or queues later;
- the source must be mutated immediately;
- the result is small relative to the coupling cost;
- retaining the source solely for the result would waste memory.

### Hidden long borrows

A struct storing `&mut T` keeps exclusive access for its entire usable lifetime. This can be useful for guards but makes the owner unavailable:

```rust
struct Editor<'a> {
    document: &'a mut Document,
}
```

Do not create long-lived reference-bearing “manager” structs casually. They often freeze the rest of an aggregate. Prefer a method-local guard, a split owner, or IDs when the relationship is not truly lexical.

Lifetime errors often arise from temporary values and destructor timing rather than named parameters.

### Borrowing a temporary

Some `let` initializers receive temporary lifetime extension:

```rust
let value = &String::from("extended for the binding");
println!("{value}");
```

The temporary `String` is kept alive for the binding's scope under the language's syntactic extension rules.

The same expression passed to a function usually lives only through the statement:

```rust
consume(&String::from("valid during call"));
```

Do not generalize from one accepted example. Temporary lifetime extension follows specific syntax rules and is not a general “borrowed temporaries live as long as needed” principle.

### Guard temporaries

Interior-mutability code can be affected by when a `Ref` or `RefMut` temporary is dropped. Binding the guard makes its scope visible; relying on a chain can produce surprising runtime borrow duration.

```rust
let length = cell.borrow().len();
```

The borrow guard normally drops at the end of the statement. By contrast:

```rust
let borrowed = cell.borrow();
let length = borrowed.len();
// guard remains live until final use / drop
```

Module 17 makes this a runtime concern.

### `&'static T`

A reference with lifetime `'static` is valid for the remainder of the program. String literals are the common example:

```rust
let label: &'static str = "built into the binary";
```

Owned allocations do not become `'static` merely because they are heap allocated. Heap location and reference validity are different dimensions.

### `T: 'static`

A type bound `T: 'static` means values of `T` contain no borrowed references shorter than `'static`. Owned `String`, `Vec<u8>`, and many structs satisfy it even though individual values are destroyed normally.

```rust
fn store_for_later<T: 'static>(value: T) {
    drop(value); // legal immediately; the bound is about borrowed components
}
```

This is a frequent source of confusion in thread and callback APIs.

### Leaking to obtain `'static`

`Box::leak` consumes a box and returns a reference whose allocation is intentionally never reclaimed through that handle:

```rust
let global: &'static mut str = Box::leak(String::from("configured").into_boxed_str());
```

This is memory-safe but leaks by design. It can be appropriate for process-long configuration created once, but it is not a repair for ordinary lifetime architecture. Repeated use creates unbounded memory retention, and the mutable `'static` reference carries enormous authority.

### Drop scopes and API reasoning

A returned reference must remain valid not only until the source variable's textual brace but through the exact drop scope of its owner. Rust 2024 narrows some temporary scopes, including `if let` temporaries and tail-expression temporaries. The course code avoids relying on subtle extension rules where an explicit owner binding communicates intent more clearly.

Borrowing avoids copying and expresses dependence. It also couples the result to an owner and may retain a larger object or block mutation. Good design evaluates both sides.

### Return a reference when identity and zero-copy matter

```rust
fn document(&self, id: DocumentId) -> Option<DocumentView<'_>>
```

A view is appropriate because the workspace owns the document, the caller wants temporary observation, and mutation should be excluded while the view is used.

### Return a small owned fact when it frees the owner

```rust
fn document_count(&self) -> usize
```

Returning `&usize` would extend a borrow for no benefit. Copyable facts should normally be returned by value.

### Return an ID when the caller needs later access

A long-lived reference into a mutable collection can make the collection unusable. A generational ID lets the caller release the borrow and request access later, with stale-handle validation.

The ID is not equivalent to a reference:

- it does not keep the target alive;
- lookup can fail;
- it can cross mutation phases;
- it can be stored without borrowing the collection.

### Return owned data across architectural boundaries

Events, background work, persistence, and independent caches often need ownership. A borrowed event ties processing to the source borrow; an owned event or shared `Rc` snapshot may be correct.

### Avoid lifetime contagion

Once a public struct stores a reference, every owner of that struct inherits the lifetime parameter. This can be desirable for view types and undesirable for domain entities. Do not store references merely to avoid one allocation if it forces the entire application state to become parameterized.

### Borrowing from multiple owners

A result that combines slices from several inputs may be precise but hard to store. Alternatives:

- return a callback-scoped view;
- return offsets paired with stable owners;
- return a small owned summary;
- store IDs rather than references;
- use `Cow` when most inputs can be borrowed but some must be normalized.

### API review checklist

1. Who owns every byte behind the output?
2. Can the output outlive that owner by mistake?
3. Which mutations are intentionally prevented while it exists?
4. Does one lifetime parameter conflate independent sources?
5. Would an ID preserve identity with less coupling?
6. Would ownership be cheaper than retaining a large source?
7. Is `'static` being used to conceal missing ownership?

The best API is not the one with the fewest allocations in isolation. It is the one whose validity and mutation constraints match the product's temporal structure.

A server configuration is parsed from one source document. A `Config<'source>` stores borrowed section and value slices. A dashboard wants a `Selection` containing a borrowed config value and a separately borrowed display label supplied by the caller.

A one-lifetime design is tempting:

```rust
struct Selection<'a> {
    value: &'a str,
    label: &'a str,
}
```

It is not automatically wrong; the compiler can choose a common short region. It becomes limiting when selections are updated or stored in contexts where value and label have independent validity.

### Derive sources

```text
value -> source configuration text
label -> dashboard-owned label table
Selection value -> borrows both
```

The precise type is:

```rust
struct Selection<'source, 'label> {
    value: &'source str,
    label: &'label str,
}
```

A method replacing only the label can preserve `'source`:

```rust
impl<'source, 'label> Selection<'source, 'label> {
    fn relabel<'next>(self, label: &'next str) -> Selection<'source, 'next> {
        Selection { value: self.value, label }
    }
}
```

With one lifetime, the returned type often shortens both fields unnecessarily.

### Query independence

A lookup query is inspected but not returned:

```rust
fn select<'source, 'config>(
    config: &'config Config<'source>,
    key: &str,
) -> Option<&'source str>
where
    'source: 'config,
```

Depending on how values are accessed and represented, a return tied to `'config` may be simpler. The key point is that `key` receives no named output lifetime. Derive the strongest valid signature by compiling narrow-scope callers.

### Reference-bearing owner

`Config<'source>` can outlive a short borrow of itself while still containing source references. Distinguish:

- lifetime of the `Config` value;
- lifetime `'source` of strings it contains;
- lifetime of `&Config<'source>` used by one method;
- lifetime of the method output.

These may coincide in a toy call and remain conceptually separate.

### Temporary labels

A `Selection` cannot outlive a locally created label. Adding `'static` would not help. Choose one of:

- own label as `String`/`Box<str>`;
- keep selection scoped;
- store an owned label identifier and look it up later;
- use `Cow` if labels are sometimes borrowed and sometimes generated.

### Testing precision

Construct source text in an outer scope and labels in nested scopes. Demonstrate that relabeling can shorten only the label component. Preserve compile-fail evidence for returning a selection containing a local label. Tests with string literals alone are weak because literals are `'static` and hide constraints.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For translate lifetime syntax into constraints among borrows rather than durations attached to values, construct one positive and one causal negative example. Mark the first decisive fact in the **lifetime constraint graph** and state which evidence could falsify the claim.

2. **Outcome 2.** For derive elision and explicit relationships for one-source and multiple-source APIs, construct one positive and one causal negative example. Mark the first decisive fact in the **lifetime constraint graph** and state which evidence could falsify the claim.

3. **Outcome 3.** For use lifetime shortening and subtyping in ordinary covariant borrowed views without extending provenance, construct one positive and one causal negative example. Mark the first decisive fact in the **lifetime constraint graph** and state which evidence could falsify the claim.

4. **Outcome 4.** For design structs and enums containing references while accounting for temporary and drop scopes, construct one positive and one causal negative example. Mark the first decisive fact in the **lifetime constraint graph** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Expose document views and search excerpts that borrow from workspace-owned text. Derive every output lifetime from the owner that actually supplies the bytes. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-02-zero-copy-records/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 13 when you can:

- answer the module question—“What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Translate lifetime syntax into constraints among borrows rather than durations attached to values;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Lifetimes](https://doc.rust-lang.org/reference/trait-bounds.html#lifetime-bounds)
- [Rust Reference: Lifetime elision](https://doc.rust-lang.org/reference/lifetime-elision.html)

[← Module 11](../module-11-places-move-paths-and-advanced-borrowing/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 13 →](../module-13-scoped-access-and-escape-prevention/index.md)

## Continue

Continue to [Module 13 — Scoped Access and Escape Prevention](../module-13-scoped-access-and-escape-prevention/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
