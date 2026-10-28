# 13 — Scoped Access and Escape Prevention

**Course 2, day 3 · Module 13 of 90**  
`████░░░░░░░░░░░░░░░░` **13/90**

[← Module 12: Lifetime Relationships and Borrowed APIs](../module-12-lifetime-relationships-and-borrowed-apis/index.md) · [Course 2 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 14: RAII, Drop, Unwinding, and Failure Atomicity →](../module-14-raii-drop-unwinding-and-failure-atomicity/index.md)

## The question

> Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?

## Why this comes now

Some safe APIs must expose a temporary value while making escape impossible. Ordinary input-output lifetime notation is not always enough; the caller may need to choose a fresh borrow for each invocation. Higher-ranked callback bounds and scoped access now extend the lifetime model without introducing self-referential designs.

## What you will be able to do

- Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.
- Read and design for<'a> higher-ranked callback bounds as universal quantification over borrow duration.
- Account for closure capture and Fn, FnMut, and FnOnce requirements at scoped boundaries.
- Use callbacks and scoped APIs to prevent temporary references or brands from escaping.
- Recognize self-reference pressure and choose indices, owned state, callbacks, or later pinning only when justified.

## Core model

### Who chooses the lifetime?

Named lifetime parameters on an ordinary function are instantiated by the caller from the borrows supplied at the call. Higher-ranked bounds reverse the perspective: the function receiving a callback requires the callback to work for **every** suitable fresh borrow duration chosen by the callee.

```rust
pub fn with_trimmed<R>(input: &str, operation: impl for<'a> FnOnce(&'a str) -> R) -> R {
    let owned;
    let trimmed = input.trim();
    let normalized = if trimmed.split_whitespace().count() <= 1 {
        trimmed
    } else {
        owned = trimmed.split_whitespace().collect::<Vec<_>>().join(" ");
        &owned
    };
    operation(normalized)
}
```

The callback must accept a string slice valid for whatever scope the function provides. If normalization allocates, the borrowed slice points into a local `String`; the callback can use it during the call, but cannot return it as part of `R` because `R` is outside the quantified lifetime.

The implementation above can be expressed more directly with `Cow` later. The important mechanism is scoped access and escape prevention.

### Universal quantification

Read:

```rust
F: for<'a> FnOnce(&'a str) -> R
```

as “for every lifetime `'a` selected for a call, `F` can be invoked with `&'a str` and produce `R` not tied to that `'a`.” This is stronger than `F: FnOnce(&'some str) -> R` for one caller-selected lifetime.

A callback returning an owned count works:

```rust
let words = with_trimmed("  alpha   beta ", |text| text.split_whitespace().count());
```

Trying to store the temporary reference outside fails for the intended escape reason.

### Callable traits and capture

A closure implements one or more of:

- `Fn`: callable through shared access to its captured environment;
- `FnMut`: requires mutable access to captured state;
- `FnOnce`: may consume captured values and is guaranteed only one call.

Every closure implements `FnOnce`; some also implement `FnMut` and `Fn`. Select the weakest required bound from how the API invokes it. A scoped function that calls once can accept `FnOnce`, allowing callbacks that move owned output into another structure.

### Lending without an iterator

An ordinary `Iterator` has one fixed `Item` type not parameterized by the borrow of each `next` call. Some APIs need each yielded view tied to a short borrow of internal scratch state. A callback can express this safely:

```rust
pub fn for_each_token(input: &str, mut visit: impl for<'a> FnMut(&'a str)) {
    for token in input.split_whitespace() {
        visit(token);
    }
}
```

Here tokens borrow the stable input, so an iterator is also possible. The pattern becomes essential when a decoder reuses a buffer and each view is valid only until the next mutation. Course 10 and later unsafe/system courses revisit stronger lending abstractions.

### Escape prevention as API design

A scoped API is valuable when temporary resources must not escape:

- scratch buffers;
- transaction guards;
- temporary normalized text;
- arena brands;
- thread scopes (later course);
- short-lived borrowed views into mutable state.

The callback boundary makes the lifetime local to the operation. It should not be added merely to display HRTB syntax. If ordinary ownership is simpler, own the result.

### Self-reference pressure

A type that wants to store an owned buffer and a reference into itself creates movement and construction problems. Before reaching for pinning, consider:

- store byte ranges/indices instead of references;
- compute views on demand;
- split owner and view into separate values;
- use a callback that lends the view;
- allocate stable owned components and refer via handles;
- use a specialized crate after understanding its contract.

Pinning is justified only when an invariant truly depends on stable address; Module 20 requires that proof.

### Opaque returns

`impl Iterator + '_` or another opaque return still carries captured lifetime obligations. “Opaque” hides the concrete type from callers; it does not erase borrows. Read every `+ '_` or named bound by identifying the source owner.

### Worked derivation: scoped decoder

A decoder owns a reusable `String` buffer. A method reads/normalizes a record into the buffer and lets a callback inspect a `RecordView<'_>`. The callback may compute an owned result but cannot retain the view after the method returns or the buffer is reused. The type signature should quantify the view lifetime at the callback boundary, and the decoder must not hold a mutable buffer borrow while invoking arbitrary code if reentrancy would be possible.

### Derive it yourself

Design `with_document_text(handle, operation)` for a workspace. Decide whether the callback needs `FnOnce`, `FnMut`, or `Fn`; who chooses the text lifetime; what errors occur before callback invocation; and whether the callback may call back into the workspace.

### Misconception clinic

- `for<'a>` is universal quantification, not one very long borrow.
- A callback does not automatically prevent escape; the return type and captured destinations must be independent of the fresh lifetime.
- `FnOnce` is about capture consumption and guaranteed call count, not a special closure syntax.
- `impl Trait` can hide a concrete type while still exposing lifetime constraints.

A lifetime parameter can be quantified at different levels. The location of the quantifier determines who chooses the concrete borrow region and therefore what the implementation or callback may assume.

Consider a normal generic function:

```rust
fn inspect<'a>(text: &'a str) -> usize {
    text.len()
}
```

The caller chooses a concrete `'a` for each invocation. The function must work for that choice. This is often described as “generic over a lifetime,” but that phrase becomes insufficient when callbacks enter the design.

### One concrete callback input

Suppose a function is itself generic over the borrow of a buffer:

```rust
fn visit_once<'buffer, F>(buffer: &'buffer str, visitor: F)
where
    F: FnOnce(&'buffer str),
{
    visitor(buffer);
}
```

For this call, `'buffer` is one concrete region selected from the borrow of `buffer`. The callback is required to accept that region. Depending on the caller's surrounding types, the callback may be capable of storing the reference somewhere that also lives for `'buffer`.

That is not necessarily wrong. It is simply a different contract from “the callback may inspect temporary borrows but must not retain them.”

### A callback that must accept any supplied borrow

The latter contract uses a higher-ranked bound:

```rust
fn visit_scoped<F>(buffer: &str, mut visitor: F)
where
    F: for<'item> FnMut(&'item str),
{
    for line in buffer.lines() {
        visitor(line);
    }
}
```

Read `for<'item>` as:

> The callback must be callable for every lifetime `'item` the function chooses to supply.

The caller cannot specialize `F` to one long-lived reference type and then demand that each line survive that long. Each invocation may use a fresh, short borrow. This is universal quantification over the callback's argument lifetime.

### Quantifier order is API power

Compare the logical shapes:

```text
for some caller-chosen 'a:     F(&'a str)
for every callee-chosen 'a:    for<'a> F(&'a str)
```

The second requirement is stronger on the callback and therefore gives the producer more freedom. A value that only accepts `&'static str` satisfies neither ordinary short calls nor the higher-ranked contract. A normal closure that merely reads the argument usually satisfies the higher-ranked contract because it does not encode one particular input lifetime in its own state.

### Early-bound and late-bound intuition

Rust's full early-bound/late-bound rules involve where lifetimes appear in item signatures and bounds. For this course, use an operational distinction:

- a lifetime chosen when a function or type is instantiated is fixed for that use;
- a lifetime introduced inside `for<...>` is chosen afresh at each required call.

Do not reach for HRTBs as decoration. Write the escape policy first. If the callback should be allowed to return or retain a borrow tied to the owner's borrow, a concrete lifetime may be appropriate. If the producer must keep control and prevent retention, a higher-ranked callback is a candidate.

### A diagnostic question

When a callback signature becomes difficult, ask:

> Is the caller lending data to the function, or is the function lending data to the callback?

The side doing the lending should normally control the concrete lifetime. This question resolves many apparently mysterious annotation disputes before code is written.

A higher-ranked trait bound is written with `for<'a>` before a trait requirement:

```rust
fn with_bytes<R, F>(source: &str, operation: F) -> R
where
    F: for<'a> FnOnce(&'a [u8]) -> R,
{
    operation(source.as_bytes())
}
```

The return `R` is intentionally outside `'a`. The operation may compute an owned result, a number, or another value independent of the temporary byte slice. It may not choose `R = &'a [u8]`, because there is no one `'a` in scope when `R` is selected. This is one of the most useful escape-prevention properties of an HRTB.

### Why a borrowed return fails

This attempt is not expressible with the same `R`:

```rust,compile_fail
fn escape<'outer>(source: &'outer str) -> &'outer [u8] {
    with_bytes(source, |bytes| bytes)
}
```

The closure would need to return a reference whose type varies with each universally quantified input lifetime, while `R` is one fixed type. Rust correctly refuses to pretend those are interchangeable.

The ordinary, simpler implementation is just `source.as_bytes()`. The HRTB function is valuable only when the producer needs to bound the operation's authority or create temporary derived data.

### Fresh borrows over mutable state

HRTBs become especially useful when a method creates a sequence of short mutable borrows:

```rust
fn with_each_word_mut<F>(words: &mut [String], mut operation: F)
where
    F: for<'word> FnMut(&'word mut String),
{
    for word in words {
        operation(word);
    }
}
```

The callback cannot collect the `&mut String` values into a vector outside the call. If it could, later iterations would risk overlapping exclusive references. Instead, each borrow ends before the next iteration can safely begin.

### Returning owned summaries

A scoped API often accumulates through caller-owned state:

```rust
let mut lengths = Vec::new();
visit_scoped("one\ntwo words", |line| lengths.push(line.len()));
assert_eq!(lengths, [3, 9]);
```

The closure captures `lengths` by mutable borrow. It stores owned `usize` values, not the borrowed lines. This is the intended pattern: temporary data enters, durable conclusions leave.

### Nested higher-ranked bounds

Some APIs need a callback that receives a domain view:

```rust
struct EntryView<'a> {
    key: &'a str,
    value: &'a str,
}

fn visit_entries<F>(input: &str, mut visitor: F)
where
    F: for<'entry> FnMut(EntryView<'entry>),
{
    for line in input.lines() {
        if let Some((key, value)) = line.split_once('=') {
            visitor(EntryView { key, value });
        }
    }
}
```

The view can contain multiple references known to share the per-entry lifetime. The callback can compare or render them, but cannot make the view outlive that invocation.

### Do not overclaim what HRTBs prove

A higher-ranked callback does not prove that the callback has no side effects, does not panic, or is cheap. It only constrains type/lifetime compatibility. It may mutate captured state, perform I/O, or abort the process. Pair the lifetime contract with ordinary behavioral documentation.

### Review rule

Whenever `for<'a>` appears, explain all three points:

1. who chooses `'a`;
2. whether each call may choose a different `'a`;
3. which result types are deliberately independent of `'a`.

If those cannot be stated, the bound is probably cargo-culted.

A closure has an anonymous concrete type whose fields are the values it captures. The compiler chooses capture modes from how the body uses surrounding variables, modified by `move` when ownership transfer is requested.

### Capture is place-sensitive

Modern Rust can capture a field rather than an entire struct when the access permits it:

```rust
struct Counters {
    accepted: usize,
    rejected: usize,
}

let counters = Counters { accepted: 2, rejected: 1 };
let report = || counters.accepted;
assert_eq!(report(), 2);
```

Reason about the exact captured place and authority. A closure that only reads may capture by shared borrow. A closure that mutates captured state needs mutable access. A closure that consumes a captured value can generally be called only once.

### `Fn`, `FnMut`, and `FnOnce` describe call capability

The traits form a capability relationship:

- `FnOnce` can be called at least once by consuming the closure value;
- `FnMut` can be called repeatedly through `&mut self`;
- `Fn` can be called repeatedly through `&self`.

Every closure implements `FnOnce`. Some also implement `FnMut`; a further subset implements `Fn`. Choose the weakest requirement that matches the producer's behavior.

```rust
fn apply_once<F, R>(operation: F) -> R
where
    F: FnOnce() -> R,
{
    operation()
}
```

This function makes one call, so requiring `Fn` would reject useful closures for no benefit.

### `move` changes capture, not necessarily call trait

```rust
let label = String::from("snapshot");
let print = move || println!("{label}");
print();
print();
```

The closure owns `label`, but merely reads it. It can still implement `Fn`. By contrast:

```rust
let payload = String::from("payload");
let consume = move || payload;
let value = consume();
```

Returning `payload` moves it out of the closure, so the closure is only `FnOnce`.

### Captured references set the closure's own lifetime

A closure can satisfy a higher-ranked *argument* bound while still borrowing surrounding state:

```rust
let prefix = String::from("line");
visit_scoped("a\nb", |line| println!("{prefix}: {line}"));
```

The callback can accept lines of any supplied lifetime, but the closure value itself may not outlive `prefix`. These are independent axes: input generality and captured-state validity.

### Mutating capture can extend a borrow

```rust
let mut total = 0;
let mut add = |value: usize| total += value;
add(3);
add(4);
// `total` becomes directly usable after the final use of `add`.
println!("{total}");
```

The closure's mutable capture keeps `total` borrowed while the closure may still be called. Non-lexical lifetime analysis can end the borrow after the closure's last use. If a closure is stored in a longer-lived variable or collection, the captured borrow may last longer than expected.

### API design consequence

Callback APIs should document:

- how many times the callback is called;
- whether calls can be nested or reentrant;
- whether a panic may leave surrounding state partially updated;
- whether ordering is guaranteed;
- whether references passed to it are scoped and non-retainable.

The `Fn*` trait expresses only call mechanics. The rest is still an engineering contract.

An escape occurs when a reference derived from a temporary or controlled borrow becomes usable outside the scope where the API can guarantee its validity or exclusivity.

### Direct storage attempt

```rust,compile_fail
let mut saved: Option<&str> = None;
visit_scoped("alpha\nbeta", |line| saved = Some(line));
println!("{}", saved.unwrap_or(""));
```

With a genuinely higher-ranked visitor, the closure cannot store `line` into one fixed outer reference slot. The slot's type would need one lifetime, while the callback must accept arbitrary per-call lifetimes.

This rejection is not inconvenience. It proves the producer can reuse, mutate, or discard backing storage after each callback according to its documented contract.

### Return owned evidence

Typical escape-safe outputs include:

- indices or byte ranges;
- copied scalars;
- owned strings only when ownership is required;
- domain identifiers;
- booleans and aggregate statistics;
- commands queued for later application.

For example:

```rust
fn line_ranges(text: &str) -> Vec<std::ops::Range<usize>> {
    let mut ranges = Vec::new();
    let mut start = 0;
    for line in text.split_inclusive('\n') {
        let end = start + line.trim_end_matches('\n').len();
        ranges.push(start..end);
        start += line.len();
    }
    if text.is_empty() {
        ranges.clear();
    }
    ranges
}
```

Ranges are owned descriptions. A later method can validate and resolve them against the correct owner.

### `Box::leak` is not a lifetime conversion

`Box::leak` deliberately abandons automatic reclamation and returns a reference that may be used for an arbitrarily long lifetime if the contained type permits it. It can be legitimate for process-lifetime configuration, but it is not a repair for a design that cannot state ownership.

Turning every problematic borrow into leaked `'static` storage changes the resource contract: memory is no longer reclaimed. It also does nothing for mutable aliasing or logical staleness.

### Global storage and registries

Moving data into a global similarly changes the product. It adds process-wide coupling, synchronization concerns in later concurrent programs, difficult test isolation, and lifecycle ambiguity. A local ownership problem should not silently become global state.

### Escape through opaque types

References can escape indirectly through structs, iterators, guards, closures, and `impl Trait` returns. Always inspect the full returned type relationship:

```rust
fn words(&self) -> impl Iterator<Item = &str> + '_ {
    self.text.split_whitespace()
}
```

The iterator keeps `self` borrowed. It is an intentional escape tied to the receiver lifetime, not an uncontrolled one. The API exposes that relation and Rust prevents mutation while the iterator remains usable.

### Escape policy table

For each callback input, decide:

| Policy | Suitable shape |
|---|---|
| caller may retain view while owner remains borrowed | return/reference-bearing type with explicit receiver lifetime |
| callback may inspect but not retain | HRTB callback with owned result independent of item lifetime |
| caller needs durable location | return validated range or handle |
| caller needs independent data | return owned clone/copy with explicit cost |
| producer needs staged mutation | guard/session type with scoped borrow |

The API should make the chosen row obvious from its signature.

The standard `Iterator` trait has an associated `Item` type selected for the iterator implementation as a whole:

```rust
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

The `Item` type is not parameterized by the temporary lifetime of each `&mut self` borrow. This limits patterns where every yielded item must borrow from the iterator itself and must be released before `next` is called again.

### Why ordinary slice iterators work

A slice iterator stores a borrow of an external slice. Its item references borrow from that external owner, not from data newly borrowed out of the iterator object for only the duration of `next`. The item lifetime can therefore be part of the iterator's concrete type.

### A scratch-buffer reader is different

Imagine an object that reuses one internal `String` buffer for each record read. Returning `&str` into that buffer from ordinary `Iterator::next` would permit a caller to hold the first item and call `next` again, mutating the same buffer. The trait cannot express “the item is valid only until the next mutable borrow of the iterator.”

A scoped callback can:

```rust
struct ScratchReader {
    scratch: String,
}

impl ScratchReader {
    fn with_record<R>(&mut self, input: &str, operation: impl for<'a> FnOnce(&'a str) -> R) -> R {
        self.scratch.clear();
        self.scratch.push_str(input.trim());
        operation(&self.scratch)
    }
}
```

The output `R` cannot borrow from the per-call record. The next call is safe after the callback returns.

### Generic associated types and lending traits

Rust can express families of associated types parameterized by a borrow lifetime using generic associated types. A lending trait might contain an associated type such as `Item<'a>` with appropriate bounds. Designing such a public trait correctly involves trait-system concerns reserved for Course 3. This course's goal is to recognize the ownership need and choose a simple callback or domain-specific method when that is sufficient.

### Do not replace clear iterators unnecessarily

If data already lives in an external owner and ordinary `Iterator<Item = &'a T>` models it correctly, use the standard ecosystem. Callback-only traversal loses familiar combinators, can complicate early exit, and may reduce composability.

### Early exit in callback traversal

A callback can return `ControlFlow`:

```rust
use std::ops::ControlFlow;

fn try_visit<F, B>(text: &str, mut visitor: F) -> ControlFlow<B>
where
    F: for<'a> FnMut(&'a str) -> ControlFlow<B>,
{
    for line in text.lines() {
        if let ControlFlow::Break(value) = visitor(line) {
            return ControlFlow::Break(value);
        }
    }
    ControlFlow::Continue(())
}
```

This preserves escape prevention while allowing a caller to stop. The design cost is justified only when the scoped-lending property is real.

A self-referential value owns data and also stores a reference or pointer into that same owned data. The naive safe-Rust form is impossible because moving the outer value can relocate its inline fields, invalidating internal references.

```rust,compile_fail
struct Broken<'a> {
    text: String,
    first: &'a str,
}

fn build() -> Broken<'static> {
    let text = String::from("one two");
    let first = text.split_whitespace().next().unwrap_or("");
    Broken { text, first }
}
```

The local borrow cannot be tied soundly to the value being constructed, and returning the struct moves it.

### First alternative: recompute the view

Store only the owner:

```rust
struct Document {
    text: String,
}

impl Document {
    fn first_word(&self) -> &str {
        self.text.split_whitespace().next().unwrap_or("")
    }
}
```

This is often fast enough and has the cleanest invariants.

### Second alternative: store ranges

```rust
use std::ops::Range;

struct IndexedDocument {
    text: String,
    first: Range<usize>,
}

impl IndexedDocument {
    fn first_word(&self) -> &str {
        &self.text[self.first.clone()]
    }
}
```

The range is an owned value, independent of address. The constructor must validate UTF-8 boundaries and the mutation API must maintain or invalidate ranges.

### Third alternative: split ownership

Store backing data in a stable allocation and make views separate values that borrow the owner:

```rust
struct Corpus {
    text: Box<str>,
}

struct CorpusView<'a> {
    text: &'a str,
}
```

The owner and view are not one movable object. Ordinary lifetime relationships suffice.

### Fourth alternative: handles into an arena

A collection owns nodes; relationships use validated identifiers. Generational handles can detect stale reuse. This avoids reference cycles, address sensitivity, and widespread lifetime coupling at the cost of lookup and explicit validation.

### Fifth alternative: pinning

Pinning can support address-sensitive values when stable address is a genuine invariant. It does not automatically create internal references, project fields safely, or make self-reference easy. Module 20 teaches the contract. It should be the final option after representation alternatives are assessed.

### Mutation is the hidden requirement

Every self-reference proposal must answer:

- Can the owner mutate or reallocate its backing data?
- Which operations invalidate stored offsets?
- Can the object be cloned?
- What does assignment mean?
- How is destruction performed?
- Is stable address required before initialization or only after?

Many “lifetime problems” are actually unspecified mutation semantics. Resolve those before choosing a pointer mechanism.

`impl Trait` can hide a concrete return type while still carrying lifetime relationships. Hiding the name does not erase borrows.

```rust
struct Catalog {
    titles: Vec<String>,
}

impl Catalog {
    fn matching<'a>(&'a self, query: &'a str) -> impl Iterator<Item = &'a str> + 'a {
        self.titles
            .iter()
            .map(String::as_str)
            .filter(move |title| title.contains(query))
    }
}
```

This signature ties both `self` and `query` to one lifetime. That is valid, but potentially overconstraining: the query need only survive as long as the iterator, and the iterator captures it. A clearer modern spelling may use distinct lifetimes with an explicit bound:

```rust
impl Catalog {
    fn matching<'catalog, 'query>(
        &'catalog self,
        query: &'query str,
    ) -> impl Iterator<Item = &'catalog str> + 'query
    where
        'catalog: 'query,
    {
        self.titles
            .iter()
            .map(String::as_str)
            .filter(move |title| title.contains(query))
    }
}
```

Here the opaque iterator must remain valid for `'query`; the catalog borrow must outlive that use because yielded titles borrow the catalog.

### Capturing versus yielding

An opaque iterator can:

- capture a borrowed query;
- capture a borrow of the collection;
- yield references tied to the collection;
- own copied configuration.

These are separate relationships. Expand the hidden concrete type mentally: adapter structs store the underlying iterator and closure, and the closure stores its captures.

### `+ '_` as an API signal

```rust
fn titles(&self) -> impl Iterator<Item = &str> + '_ {
    self.titles.iter().map(String::as_str)
}
```

The anonymous lifetime says the opaque return captures some lifetime from the arguments, normally the receiver. It improves readability even when newer capture rules can infer the relation.

### Guards are opaque in a different way

A method returning a named guard makes the long borrow obvious:

```rust
struct Edit<'a> {
    target: &'a mut String,
}
```

A method returning `impl SomeTrait + '_` can conceal that a borrow remains active. Public APIs should document the continued borrow and its release condition, not force callers to reverse-engineer errors.

### Avoid lifetime compression

Using one `'a` for every input and output often compiles but creates accidental coupling. Opaque returns amplify the problem because captured state is less visible. Keep sources independent until a real outlives relation is required.

A scoped-borrow API should pass six reviews.

### 1. Ownership review

Identify the long-lived owner, the temporary view, and any durable output. If the “view” actually owns its data, a lifetime-heavy callback is likely unnecessary.

### 2. Quantifier review

Write who chooses each lifetime. For `F: for<'a> FnMut(View<'a>)`, the producer chooses a fresh valid borrow for each call and the callback must accept all of them. For `F: FnMut(View<'owner>)`, the caller and owner's borrow establish one concrete region.

### 3. Escape review

Attempt to:

- store the view in outer state;
- return it as `R`;
- insert it into a collection;
- spawn work that outlives the call;
- call the producer again while retaining the view.

The type system should reject operations that violate the intended scope.

### 4. Panic and partial-effect review

The callback may panic after mutating captured state. The producer may have mutated internal state before calling it. Define whether the operation is transactional, restartable, or intentionally partial. Module 14 provides RAII tools for stronger guarantees.

### 5. Ergonomics review

Compare against:

- ordinary borrowed return;
- ordinary iterator;
- owned result;
- range/handle result;
- explicit guard.

Use a scoped callback only when it expresses a real safety or lifecycle boundary.

### 6. Diagnostic review

Write one expected-fail test demonstrating the forbidden escape. Without negative evidence, a complicated signature may be solving an imagined problem.

### Worked decision

A tokenizer backed by immutable caller text should normally return an iterator of borrowed tokens. A parser reusing one internal scratch buffer cannot safely yield ordinary borrowed items; a scoped visitor or owned token is appropriate. A document storing token boundaries should return ranges or a view tied to `&self`. A value that must remain at a stable address for external registration may eventually require pinning.

The goal is not maximum sophistication. It is an ownership contract whose restrictions correspond exactly to product truth.

A binary decoder needs a temporary scratch vector and a temporary symbol table for each call. Returning either would expose implementation storage, but callbacks need efficient borrowed access during decoding.

### Naive return

```rust,compile_fail
fn decode(bytes: &[u8]) -> &[Token] {
    let tokens = build_tokens(bytes);
    &tokens
}
```

The vector dies at return. Returning `Vec<Token>` is valid but forces ownership when callers only need an immediate fold.

### Scoped contract

```rust
fn with_decoded<R>(
    bytes: &[u8],
    operation: impl for<'decoded> FnOnce(&'decoded [Token]) -> R,
) -> Result<R, DecodeError>
```

The decoder owns local tokens and selects `'decoded`. `R` cannot contain a borrow tied to the local slice. The callback may return counts, hashes, owned summaries, or references whose provenance is some external input captured independently.

### External provenance inside tokens

If `Token<'source>` contains slices into `bytes`, use two levels:

```rust
fn with_decoded<'source, R>(
    bytes: &'source [u8],
    operation: impl for<'list> FnOnce(&'list [Token<'source>]) -> R,
) -> Result<R, DecodeError>
```

The list borrow cannot escape. A copied token field borrowing `'source` may escape if the output type expresses `'source`.

### Scratch pooling

To reuse allocation, a decoder may checkout a `Vec<Token>` from a pool. A lease guard clears and returns the vector during normal return or unwinding. Do not hold a `RefMut` to a pool across the user callback; that creates reentrancy panic. Move the vector into a guard with a narrow return handle or central exclusive borrow if nested decoding is prohibited.

### `FnOnce`

The callback is invoked once and may consume an accumulator. `FnOnce` is therefore the minimum correct requirement. The function returns callback `Result` nested with decode failure only if the API intentionally separates them; otherwise a generic error conversion or explicit enum can flatten categories.

### Escape proof

A compile-fail specimen should try:

```rust,compile_fail
let leaked = with_decoded(bytes, |tokens| &tokens[0]);
```

Ensure failure is about lifetime escape, not missing trait implementations or invalid indexing. A positive counterpart returns `tokens[0].clone()` only if semantic ownership is desired, or an owned summary.

### Panic proof

Deliberately panic in the callback and verify pooled capacity is returned and no “checked out” flag remains. The callback's temporary references become unusable during unwinding before scratch destruction.

### Architecture decision

Choose a scoped callback when access is immediate and local resources should remain hidden. Return ownership when callers need to store decoded data, compose asynchronously, or invoke operations after the decoder call. HRTBs are not automatically superior; they encode a precise non-escape product boundary.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Normalize temporary queries through a scoped callback so borrowed results cannot escape. The API should permit useful work while making invalid retention unexpressible. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-03-scoped-visitors/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 14 when you can:

- answer the module question—“Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Higher-ranked trait bounds](https://doc.rust-lang.org/reference/trait-bounds.html#higher-ranked-trait-bounds)
- [Rust Reference: Closure expressions](https://doc.rust-lang.org/reference/expressions/closure-expr.html)

[← Module 12](../../../02-rust-ownership-lifetimes-memory/course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 14 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-14-raii-drop-unwinding-and-failure-atomicity/index.md)

## Continue

1. Complete the [Module 13 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 13 — Scoped Visitors](../../labs/module-03-scoped-visitors/README.md) from its public contract.
3. Apply the Module 13 increment in the [Memory Workspace engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
