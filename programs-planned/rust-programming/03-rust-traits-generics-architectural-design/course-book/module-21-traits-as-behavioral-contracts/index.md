# 21 — Traits as Behavioral Contracts

**Course 3, day 1 · Module 21 of 90**  
`███████░░░░░░░░░░░░░` **21/90**

[← Module 20: Pinning and Address-Sensitive Design](../../../02-rust-ownership-lifetimes-memory/course-book/module-20-pinning-and-address-sensitive-design/index.md) · [Course 3 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 22: Associated Types and Type Families →](../module-22-associated-types-and-type-families/index.md)

## The question

> What behavior truly belongs in a shared contract, and which laws must every implementation preserve?

## Why this comes now

Courses 1 and 2 established what values mean and how they live. Course 3 asks how multiple types may promise the same behavior. Traits begin as behavioral contracts with laws and receiver semantics, not as bags of methods or Rust's version of base classes.

## What you will be able to do

- Define a trait whose methods express a coherent behavioral contract.
- Distinguish inherent behavior, free functions, and trait behavior.
- Apply bounds, `where` clauses, default methods, supertraits, and UFCS correctly.
- Detect traits that merely rename data access or create false substitutability.
- Test semantic laws shared by multiple implementations.

## Core model

### A trait is a promise about behavior

A Rust trait is often introduced as “an interface.” That phrase is useful only if it is immediately made precise. A trait is not merely a list of method names. It is a promise that every implementing type can be used according to one coherent behavioral contract.

Consider a reporting system:

```rust
pub trait Report {
    fn title(&self) -> &str;
    fn body(&self) -> String;
}
```

This compiles, but the contract is still weak. May `title` be empty? Is `body` deterministic? Does it include the title? Can calling `body` mutate hidden state? The compiler checks that implementations provide compatible signatures; it does not prove the semantic laws that make implementations substitutable.

A better design begins with the operation the caller needs. Suppose the caller must render any report into an existing buffer and must receive the number of bytes appended:

```rust
use std::fmt;

pub trait Render {
    fn render_into(&self, out: &mut String) -> fmt::Result;

    fn rendered(&self) -> Result<String, fmt::Error> {
        let mut out = String::new();
        self.render_into(&mut out)?;
        Ok(out)
    }
}
```

`render_into` is the primitive operation. `rendered` is a default derived from it. This arrangement has two advantages:

1. Implementors have one essential behavior to define.
2. The default method has one meaning for every implementation because it is expressed in terms of the primitive.

A default method is strongest when it is a theorem of the required methods. A default that guesses domain policy—such as silently truncating output or inventing a fallback label—usually belongs elsewhere.

### Decide whether a trait is needed at all

Before declaring a trait, ask where variation exists.

Use an **inherent method** when the operation belongs to one concrete type and there is no meaningful substitution boundary:

```rust
impl Submission {
    pub fn is_empty(&self) -> bool {
        self.text.trim().is_empty()
    }
}
```

Use a **free function** when the behavior is an algorithm over inputs rather than a capability of one receiver:

```rust
pub fn normalize_label(input: &str) -> String {
    input.split_whitespace().collect::<Vec<_>>().join(" ")
}
```

Use a **trait** when multiple types must satisfy one caller-visible contract, when generic code needs a named capability, or when another crate should be able to provide an implementation.

A trait that only mirrors fields is usually abstraction without substitutability:

```rust
trait HasName {
    fn name(&self) -> &str;
}
```

`HasName` can be legitimate, but only if a real algorithm works for every name-bearing type and the meaning of “name” is coherent. If one implementation returns a display label, another a database key, and another a filename, the common method name hides different contracts.

### Receiver choice is part of the contract

The receiver says what an operation may do to the implementing value.

```rust
trait Queue {
    type Item;

    fn len(&self) -> usize;              // shared observation
    fn push(&mut self, item: Self::Item); // exclusive mutation
    fn into_items(self) -> Vec<Self::Item> // consumes the implementor
    where
        Self: Sized;
}
```

Choose `&self` when the caller should retain the value and only shared access is required. Choose `&mut self` when the call mutates the value in place. Choose `self` when the operation is a state transition, conversion, or finalization that should make the old value unavailable.

Do not select a receiver merely because it makes one implementation easy. A method that consumes `self` forces every caller and every implementation to accept that ownership policy. A method that uses `&mut self` excludes use through shared references and affects whether the trait can be used behind certain wrappers. Receivers are architecture.

### Trait bounds are requirements on the implementation body

A generic function may use only operations justified by its bounds:

```rust
pub trait Score {
    fn score(&self) -> u32;
}

pub fn best<T>(items: &[T]) -> Option<&T>
where
    T: Score,
{
    items.iter().max_by_key(|item| item.score())
}
```

The bound is not decoration. It is the proof available inside `best`. Add the weakest sufficient bound. Requiring `T: Clone + Debug + Display + Score` because one early version printed and duplicated items damages reuse and communicates a false contract.

Place short bounds near the parameter when that improves readability:

```rust
fn label<T: Display>(value: T) -> String { ... }
```

Use a `where` clause when relationships are longer, involve associated types, or would make the signature unreadable:

```rust
fn load_all<S>(source: &mut S) -> Result<Vec<S::Item>, S::Error>
where
    S: Source,
    S::Item: Validate,
{
    // ...
}
```

### Supertraits should express a genuine prerequisite

A supertrait says that implementing one contract requires another:

```rust
use std::fmt::Display;

pub trait Diagnostic: Display {
    fn code(&self) -> &'static str;
}
```

This is appropriate if every diagnostic must be renderable through `Display`. It is not appropriate to build a tall hierarchy merely to group methods. Trait hierarchies are not class inheritance. Each supertrait becomes a requirement on implementors and can affect dyn compatibility, public evolution, and testing.

Prefer small contracts that callers compose through bounds:

```rust
fn emit<T>(value: &T)
where
    T: Diagnostic + Send,
{
    // ...
}
```

rather than a new `SendableDiagnostic` trait that adds no behavior.

### Ambiguity is solved by naming the contract

A type can implement multiple traits with the same method name. Method syntax uses lookup rules, but fully qualified syntax lets you state the exact contract:

```rust
trait HumanName {
    fn name(&self) -> &str;
}

trait FileName {
    fn name(&self) -> &str;
}

struct Record {
    person: String,
    file: String,
}

impl HumanName for Record {
    fn name(&self) -> &str { &self.person }
}

impl FileName for Record {
    fn name(&self) -> &str { &self.file }
}

let record = Record {
    person: "Ada".into(),
    file: "ada.txt".into(),
};

assert_eq!(HumanName::name(&record), "Ada");
assert_eq!(FileName::name(&record), "ada.txt");
```

Fully qualified syntax is not a workaround. It is an explicit statement of which behavioral vocabulary the call uses.

### Laws are tested across implementations

Suppose a trait represents normalization:

```rust
pub trait Normalize {
    fn normalize(&self, input: &str) -> String;
}
```

The useful contract may include:

- **idempotence:** normalizing a normalized value changes nothing;
- **stability:** equal inputs produce equal outputs;
- **domain preservation:** output contains no forbidden separators;
- **non-invention:** normalization does not add semantic tokens absent from the input.

Write one contract-test function and run it against every implementation:

```rust
fn normalization_contract<N: Normalize>(normalizer: &N) {
    for input in ["a", " a  b ", "A/B"] {
        let once = normalizer.normalize(input);
        let twice = normalizer.normalize(&once);
        assert_eq!(once, twice, "normalization must be idempotent");
    }
}
```

This does not mathematically prove the law for all strings, but it places the semantic obligation in executable form and prevents each implementation from inventing unrelated behavior.

### A disciplined trait-design procedure

When extracting a trait from concrete code:

1. Name the caller that needs substitution.
2. List the smallest operations that caller performs.
3. Choose receivers from ownership and mutation requirements.
4. Separate primitive operations from derived defaults.
5. Write semantic laws in prose.
6. Implement the trait for at least two meaningfully different types.
7. Write contract tests shared by both implementations.
8. Delete any method that exists only because one implementation happened to have it.

If the second implementation feels artificial, the trait may be premature. If the two implementations cannot agree on the meaning of a method, the contract is incoherent. If callers immediately downcast to recover concrete behavior, the abstraction erased information they still needed.

#### Begin with the pressure, not the keyword

Suppose two concrete types can produce a risk score:

```rust
struct Purchase { amount_cents: u64, foreign: bool }
struct Login { failed_attempts: u32, new_device: bool }

impl Purchase {
    fn risk_score(&self) -> u8 {
        let amount = (self.amount_cents / 10_000).min(7) as u8;
        amount + if self.foreign { 3 } else { 0 }
    }
}

impl Login {
    fn risk_score(&self) -> u8 {
        self.failed_attempts.min(7) as u8 + if self.new_device { 3 } else { 0 }
    }
}
```

The repeated method name does not yet justify a trait. Ask who needs to treat both values uniformly. If the program only renders purchases in one subsystem and logins in another, two inherent methods may be the most honest design.

Now add a generic decision function:

```rust
fn requires_review<T: RiskScore>(value: &T) -> bool {
    value.risk_score() >= 7
}
```

The caller no longer cares whether it received a purchase or login. It depends on one capability. That is the design pressure a trait resolves.

```rust
trait RiskScore {
    fn risk_score(&self) -> u8;
}
```

#### A trait opens a relationship

An inherent method belongs to one type. A free function belongs to one operation. An enum closes the participant set to variants known by the enum author. A trait defines a relationship that multiple types may implement, subject to coherence.

This gives a practical comparison:

| Mechanism | Best fit |
|---|---|
| Inherent method | Behavior is intrinsic to one type and callers know that type. |
| Free function | Behavior combines values or does not define a lasting type capability. |
| Enum | Participant set is closed and variants should be exhaustively matched. |
| Trait | Participant set is open or generic callers need a common promise. |

Traits are not automatically “more extensible.” A public trait can create a large compatibility burden. Every required method becomes work for implementors, and every blanket implementation can reserve implementation space that downstream crates might otherwise use.

#### A useful first test

Before declaring a trait, write two concrete implementations and one caller that genuinely benefits from not naming their concrete types. Then state the shared law in prose. For `RiskScore`, a possible law is:

> The score is always in `0..=10`, and larger values indicate no less review urgency than smaller values.

If you cannot state a shared law, the types may only share a spelling coincidence.

#### Wrong model: “traits remove duplication”

A trait declaration can add duplication: each implementation may repeat an algorithm. Traits remove *caller dependence on concrete implementations*; they do not necessarily remove implementation code. Shared helper functions or composition may be needed for algorithm reuse.

#### Type checking proves shape, not meaning

The compiler verifies that every `RiskScore` implementation returns `u8`. It cannot infer that a score must remain within ten or that higher values mean greater urgency. Those are semantic laws supplied by documentation, tests, and review.

A serious trait definition therefore contains three layers:

1. **Syntactic contract:** method names, receivers, parameters, associated items, and return types.
2. **Semantic contract:** meaning, invariants, ordering, idempotence, error behavior, and side effects.
3. **Evolution contract:** whether downstream crates may implement the trait and what future changes remain possible.

```rust
/// Computes review urgency on a scale from 0 through 10.
///
/// Implementations must be deterministic for an unchanged value and must
/// never return a value greater than 10.
trait RiskScore {
    fn risk_score(&self) -> u8;
}
```

#### Law tests

When several implementations share laws, write a reusable test function:

```rust
fn assert_risk_laws<T: RiskScore>(value: &T) {
    let first = value.risk_score();
    let second = value.risk_score();
    assert!(first <= 10);
    assert_eq!(first, second);
}
```

This is not a proof for all possible values, but it makes the semantic contract executable across representative cases. The individual implementation tests still need domain-specific examples.

#### Receivers communicate capability

- `&self` promises observation through shared access, though interior mutability may still change hidden state.
- `&mut self` requires exclusive access and communicates mutation of the receiver's logical state.
- `self` consumes the implementing value and is appropriate for transitions or finalization.
- associated functions without `self` describe construction or type-level behavior, but are unavailable through ordinary trait-object dispatch unless excluded with `Self: Sized`.

Choose the receiver from the contract. Do not begin with the receiver that makes an implementation easiest.

#### Avoid accidental laws

A default method, a returned collection order, or a specific error string can become a de facto promise even if documentation is silent. Public examples and tests teach users what to rely on. If order is unspecified, test sets rather than sequences and say so explicitly.

#### Contract review questions

- Are valid inputs defined?
- Is failure represented, panicked, or impossible?
- Is the operation deterministic?
- Can it mutate hidden state?
- Is repeated invocation meaningful?
- Must implementations preserve ordering or identity?
- Can downstream crates implement the trait?
- Which methods can be added later without breaking them?

#### Common failure

A trait named `Manager`, `Processor`, or `Service` often collects unrelated operations because the noun sounds architectural. Split by capability. A type may implement `Load`, `Validate`, and `Render` without every generic caller receiving all three powers.

#### Inherent and trait implementations are different namespaces

An inherent implementation attaches methods directly to a type:

```rust
struct Report(String);

impl Report {
    fn render(&self) -> &str { &self.0 }
}
```

A trait implementation establishes a relationship:

```rust
trait Render {
    fn render(&self) -> String;
}

impl Render for Report {
    fn render(&self) -> String { self.0.clone() }
}
```

Calling `report.render()` chooses the inherent method when one is applicable. This can surprise readers who expect the trait method. Ambiguity among trait methods may require qualification.

#### Method lookup is capability-sensitive

Rust considers the receiver type after autoderef and autoref, then searches inherent and visible trait methods. Importing a trait can make its methods available in method-call syntax without changing the type itself.

```rust
mod text {
    pub trait WordCount {
        fn word_count(&self) -> usize;
    }

    impl WordCount for str {
        fn word_count(&self) -> usize {
            self.split_whitespace().count()
        }
    }
}

use text::WordCount;
assert_eq!("one two".word_count(), 2);
```

The import is not cosmetic. It brings the trait into the method-resolution context.

#### Implement for the semantic owner

Implement a trait for the type that can uphold its laws without hidden global knowledge. A wrapper can establish a different interpretation:

```rust
struct CaseInsensitive<'a>(&'a str);

trait Key {
    fn canonical(&self) -> String;
}

impl Key for CaseInsensitive<'_> {
    fn canonical(&self) -> String { self.0.to_lowercase() }
}
```

Implementing a “case-insensitive” contract directly for `str` would pretend that all strings share that interpretation.

#### Generic implementations

An implementation can itself be conditional:

```rust
struct Logged<T>(T);

impl<T: Render> Render for Logged<T> {
    fn render(&self) -> String {
        format!("[render] {}", self.0.render())
    }
}
```

This is a blanket implementation over all `T` satisfying a bound. It is powerful and consumes coherence space. Module 23 treats the compatibility consequences in depth.

#### Review habit

For each `impl Trait for Type`, write one sentence explaining why this crate owns the relationship and one counterexample that the implementation must reject. This prevents “implementation because it compiles” from substituting for a contract.

#### Bounds are requirements imposed by the body

Start without bounds and let operations reveal the capabilities needed:

```rust
fn accepts_any_type<T>(_value: &T) -> &'static str {
    // This body uses no operation that requires a trait capability.
    "no bound required"
}
```

A correct design chooses only the capabilities the algorithm uses:

```rust
use std::fmt::Display;

fn render_pair<T>(left: &T, right: &T) -> String
where
    T: Display,
{
    format!("{left} | {right}")
}
```

Do not add `Clone`, `Debug`, `Default`, or `'static` because a compiler suggestion appeared in an earlier design. Excess bounds reject valid callers and become public API commitments.

#### Bound locations

Equivalent basic bounds can appear inline or in a `where` clause:

```rust
fn show<T: Display>(value: T) { println!("{value}"); }

fn show_where<T>(value: T)
where
    T: Display,
{
    println!("{value}");
}
```

Use `where` clauses when relationships involve multiple parameters, associated types, or lifetimes:

```rust
fn collect_labels<I>(items: I) -> Vec<String>
where
    I: IntoIterator,
    I::Item: Display,
{
    items.into_iter().map(|item| item.to_string()).collect()
}
```

The important skill is not formatting. It is reading the clause as a set of propositions the caller must satisfy.

#### Supertrait bounds

A trait may require another trait:

```rust
trait Identified {
    fn id(&self) -> &str;
}

trait Auditable: Identified {
    fn audit_line(&self) -> String {
        format!("id={}", self.id())
    }
}
```

This means every `Auditable` implementor must also implement `Identified`. It does not copy methods or fields. Adding a supertrait to a public trait can break every downstream implementation.

#### `Self: Sized` as a capability boundary

Methods that construct or consume concrete `Self` values often need `Self: Sized`:

```rust
trait Named {
    fn name(&self) -> &str;

    fn boxed(self) -> Box<Self>
    where
        Self: Sized,
    {
        Box::new(self)
    }
}
```

The method remains available to sized implementors but is excluded from the dispatchable trait-object surface. This distinction becomes central in Module 25.

#### Defaults encode policy, not merely convenience

A default method supplies shared behavior in terms of required operations:

```rust
trait Summary {
    fn title(&self) -> &str;

    fn summary(&self) -> String {
        format!("{}…", self.title().chars().take(40).collect::<String>())
    }
}
```

This is appropriate only if the default obeys the trait's semantic contract for every implementation. A default that is merely “usually fine” creates subtle divergence: some implementors override it, callers cannot know which semantics they receive, and tests may validate only the default path.

#### Required core, derived surface

A robust pattern is a small required core with derived convenience operations. The required methods expose the primitive behavior; defaults compose them. This reduces implementor work while keeping one semantic center.

```rust
trait ByteSource {
    fn next_byte(&mut self) -> Option<u8>;

    fn drain(&mut self) -> Vec<u8> {
        let mut out = Vec::new();
        while let Some(byte) = self.next_byte() {
            out.push(byte);
        }
        out
    }
}
```

The default `drain` has a clear law because it is defined entirely by `next_byte`.

#### Supertraits express prerequisite capability

Use a supertrait when every use of the specialized trait legitimately depends on the prerequisite. Do not use supertraits to build a nominal hierarchy such as `Animal: LivingThing: Entity` unless each layer defines a real independent contract.

Prefer capability composition:

```rust
trait Readable { fn read(&self) -> String; }
trait Writable { fn write(&mut self, value: &str); }
trait Storage: Readable + Writable {}

impl<T: Readable + Writable> Storage for T {}
```

The final blanket implementation states that `Storage` adds no new law beyond the conjunction. If `Storage` does add semantic guarantees—durability, atomicity, consistency—it needs explicit documentation and perhaps methods.

#### Evolution warning

Adding a required method breaks implementors. Adding a default method is usually source-compatible for implementors, but it can still create method-name ambiguity or alter downstream method resolution. Adding a supertrait is breaking. Public defaults deserve the same review as public required methods.

#### One type can satisfy several contracts with the same method name

```rust
trait HumanName { fn name(&self) -> &'static str; }
trait FileName { fn name(&self) -> &'static str; }

struct Record;
impl HumanName for Record { fn name(&self) -> &'static str { "Ada" } }
impl FileName for Record { fn name(&self) -> &'static str { "record.tsv" } }
```

`record.name()` is ambiguous when both traits are in scope. Fully qualified syntax states the relationship explicitly:

```rust
let person = HumanName::name(&record);
let file = FileName::name(&record);
```

The most general form is:

```rust
let person = <Record as HumanName>::name(&record);
```

#### Associated functions need more qualification

Without a receiver, method lookup has no value from which to infer the implementation:

```rust
trait ParseDefault { fn default_value() -> Self; }
struct Port(u16);
impl ParseDefault for Port { fn default_value() -> Self { Port(8080) } }

let port = <Port as ParseDefault>::default_value();
```

#### UFCS is a diagnostic tool

Universal function call syntax is not only for resolving collisions. It makes autoderef and trait selection visible during debugging. Replace `value.method()` with `Trait::method(&value)` or `<Type as Trait>::method(&value)` to determine which contract is intended.

#### A naming collision may reveal a design problem

Two legitimate contracts can share a method name. Repeated ambiguity across an API may instead indicate that traits are too broad or names too generic. `run`, `process`, and `handle` carry little semantic information. Prefer names that state the domain operation when contracts differ materially.

#### The getter trait

```rust
trait HasName { fn name(&self) -> &str; }
```

This trait is justified only if generic code genuinely operates on many independently modeled named values. Adding one trait per field creates a structural pseudo-object system and leaks representation through tiny capabilities.

#### The one-implementation trait

A trait with one implementation is not automatically wrong. It can define a test boundary, downstream extension point, or stable contract. But “we may need another implementation” is weak evidence. Start concrete unless the variation is already a requirement or the boundary is intentionally public.

#### The god trait

```rust
trait RepositoryManager {
    fn load(&self, id: u64) -> String;
    fn save(&mut self, value: String);
    fn delete(&mut self, id: u64);
    fn render(&self) -> String;
    fn validate(&self) -> bool;
}
```

The trait mixes persistence, presentation, and validation. Generic callers receive more authority than they need, test doubles must fake unrelated behavior, and future changes affect every implementation. Split around consumer needs, not around a vague managerial noun.

#### The marker-without-semantics trait

An empty trait can be useful when membership itself is a capability and implementation is controlled. It is harmful when it merely tags unrelated types without a law. An enum or data field may be more inspectable.

#### The inheritance-shaped hierarchy

Traits can have supertraits, but they do not own state or provide class inheritance. Deep chains often force implementors to satisfy irrelevant methods. Prefer small capabilities and composition.

#### The “box it” repair

When generic types become difficult, replacing them with `Box<dyn Trait>` may compile by erasing type information. It also changes dispatch, allocation, ownership, object lifetime, and extensibility. Diagnose the original requirement before choosing erasure.

#### The lawless adapter

A blanket implementation such as `impl<T: Display> Audit for T` looks convenient. It claims that every displayable type has valid audit semantics and prevents downstream implementations for those types. Convenience is not sufficient justification for consuming that relationship.

A concrete invoice exporter has two output formats:

```rust
fn export_text(invoice: &Invoice) -> String { /* ... */ }
fn export_tsv(invoice: &Invoice) -> String { /* ... */ }
```

A weak refactor immediately creates `trait Exporter { fn export(&self, invoice: &Invoice) -> String; }`. A stronger process asks:

1. **Who selects the format?** If it is a compile-time command implementation, a generic type may suffice. If a configuration file selects formats at run time, later dynamic dispatch may be justified.
2. **What does success mean?** Is the output guaranteed UTF-8? deterministic? terminated by a newline? free of tabs in fields?
3. **Can export fail?** Returning `String` hides encoding or validation failures.
4. **Does the exporter need state?** A delimiter or locale may belong to the implementor.
5. **Is the set closed?** If only two formats are allowed by the product, an enum can preserve exhaustive handling.

A contract-first design might be:

```rust
trait Exporter {
    type Error;

    fn export(&self, invoice: &Invoice) -> Result<String, Self::Error>;
}
```

That associated error choice is deferred to Module 22. For Module 21, use a shared `ExportError` and document deterministic output.

#### Comparison

- **Enum:** clearest when formats are product-defined and closed.
- **Generic `E: Exporter`:** best when the caller chooses one exporter type at construction and benefits from knowing it.
- **`dyn Exporter`:** best when a heterogeneous collection or run-time selection is required and the associated items can be fixed.

The trait itself is not the architecture. The selection point and evolution story determine the architecture.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Define the Review Engine's source, rule, and reporter contracts with behavioral laws. Separate required methods from defaults and identify what tests must enforce. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-01-contract-boundaries/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 22 when you can:

- answer the module question—“What behavior truly belongs in a shared contract, and which laws must every implementation preserve?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Define a trait whose methods express a coherent behavioral contract;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Traits](https://doc.rust-lang.org/reference/items/traits.html)
- [The Rust Book: Traits](https://doc.rust-lang.org/book/ch10-02-traits.html)

[← Module 20](../../../02-rust-ownership-lifetimes-memory/course-book/module-20-pinning-and-address-sensitive-design/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 22 →](../../../03-rust-traits-generics-architectural-design/course-book/module-22-associated-types-and-type-families/index.md)

## Continue

1. Complete the [Module 21 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 21 — Contract Boundaries](../../labs/module-01-contract-boundaries/README.md) from its public contract.
3. Apply the Module 21 increment in the [Review Engine engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
