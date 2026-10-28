# Memory Workspace — Course 2 capstone

The capstone supports the course-book. It exists to force cross-layer transfer after each mechanism has been understood in isolation.

## Product

**Memory Workspace** is an in-memory document workspace with handles, snapshots, edit sessions, and caches.

## Ten increments

1. **Module 11:** Represent workspace slots with generational handles and keep mutable access narrower than the whole workspace. Stale identity and current ownership are separate concerns.
2. **Module 12:** Expose document views and search excerpts that borrow from workspace-owned text. Derive every output lifetime from the owner that actually supplies the bytes.
3. **Module 13:** Normalize temporary queries through a scoped callback so borrowed results cannot escape. The API should permit useful work while making invalid retention unexpressible.
4. **Module 14:** Add staged edit sessions whose owned candidate state can be committed or abandoned. A failed commit must preserve the documented state without relying on fallible destructors.
5. **Module 15:** Introduce immutable snapshots and conditional query ownership. Use `Box` or `Cow` only where the product needs indirection or conditional allocation.
6. **Module 16:** Store snapshots with strong ownership, expose weak observers, and define eviction. Draw the liveness graph and prove that observers do not keep snapshots alive.
7. **Module 17:** Add a revision-aware line cache with short `RefCell` guard scopes and explicit hit/miss behavior. No callback may run while a mutable runtime borrow is held.
8. **Module 18:** Produce a memory report with formulas, target observations, and explicit exclusions. Do not present `size_of` observations as a complete allocation or ABI account.
9. **Module 19:** Review runtime generational handles against a branded alternative. Explain which invalid combinations each technique prevents and which stale-state problem remains runtime data.
10. **Module 20:** Conduct an address-sensitivity review and reject pinning unless an invariant truly depends on stable location. Defend the simpler architecture when handles and indirection suffice.

## How to use the capstone

Do not read the finished implementation before attempting an increment. Begin with the public behavior, write the failure-path test, identify the types whose invariants change, and then implement the smallest coherent change. After the change passes, inspect the finished code to compare architecture rather than copy syntax.

## Product Contract

`memory-workspace` is a single-process, single-threaded document workspace. It stores mutable live documents, exposes borrowed read views, supports optimistic staged edits, caches line boundaries, creates immutable shared snapshots, and allows weak observers to detect whether a snapshot is still alive.

The product is intentionally smaller than a text editor and more demanding than a record CRUD exercise. Its purpose is to force several ownership mechanisms to cooperate without hiding behind a framework.

### Required behavior

A workspace can:

- add a document with a title, text, and optional tags;
- return a stable handle for the current occupation of a slot;
- reject a handle after its slot has been removed and reused;
- return a `DocumentView<'_>` borrowing the live document;
- return a borrowed line after lazily computing line boundaries;
- begin an edit by cloning current user-visible state into an owned `EditSession`;
- commit only when the session's expected revision still matches the live revision;
- return the owned session to the caller when commit fails;
- search all live text and return borrowed matches plus durable byte ranges;
- create one shared immutable snapshot per `(handle, revision)` key;
- issue a `Weak` watcher that does not keep a snapshot alive;
- evict a cache entry without invalidating other strong snapshot owners;
- report counted payloads and clearly labeled representation observations;
- execute a deterministic tab-separated scenario through the real binary.

### Invariants

The implementation must preserve the following invariants at every public boundary.

#### Handle validity

A `DocumentHandle` denotes one slot generation, not merely a vector index. A handle is valid exactly when:

```text
handle.slot is in bounds
AND slot.generation == handle.generation
AND slot.document is occupied
```

Removal increments the generation before the slot can be reused. A stale handle must not accidentally resolve to a new document occupying the same index.

#### Document validity

A title contains at least one non-whitespace character and contains no tab or line separator. Tags are nonempty after trimming, contain no script separators, and are unique within a document. Text may be empty and may contain line breaks.

#### Revision monotonicity

A new document begins at revision zero. Every successful commit increments the revision exactly once. Rejected commits change neither document content nor revision. Revision overflow is a typed error.

#### Snapshot immutability

A snapshot owns a frozen title, text, tag sequence, handle, and revision. Later edits to the live document cannot alter existing snapshots. Repeated requests for the same snapshot key return clones of one `Rc` allocation while the cache entry exists.

#### Cache coherence

A line cache is valid only for the document revision recorded inside the cache. Successful edits invalidate it. Read-only line queries may populate or reuse it without requiring `&mut Workspace`.

#### Failure atomicity

A failing validation, stale handle, revision conflict, or revision overflow must leave live document state unchanged. A commit failure returns the edit session so the caller may inspect, repair, merge, or retry it.

### Deliberate exclusions

The capstone does not persist live workspace state between processes, provide concurrent editing, normalize Unicode, implement full-text indexing, expose self-referential structures, dereference raw pointers, or promise exact allocator consumption. Those omissions are not excuses; they define the proof boundary. A design is stronger when it states what its evidence does not establish.

### Why standard-library-only

The course forbids helper crates in this capstone. A parser framework, arena crate, cache crate, error derive, or serialization library could reduce code, but it would also conceal the ownership decisions under study. Later courses should use ecosystem tools where they improve production quality. Here, you must be able to point to the exact owner, borrower, reference count, runtime borrow gate, and destruction event.

## Ownership and Lifetime Map

Before reading functions, draw the durable ownership graph. The graph explains more than a directory tree because it identifies which edges preserve liveness, which edges merely borrow, and which edges can be invalidated.

```text
Workspace
├── Vec<Slot>
│   └── Slot
│       ├── generation: u64
│       └── Option<Document>
│           ├── String title
│           ├── String text
│           ├── Vec<String> tags
│           ├── RefCell<Option<DocumentCache>>
│           └── Cell counters
└── HashMap<SnapshotKey, Rc<DocumentSnapshot>>
    └── shared immutable snapshot allocation

ScriptEngine
├── owns Workspace
├── alias -> DocumentHandle                 [value edge]
├── alias -> Rc<DocumentSnapshot>           [strong edge]
└── alias -> SnapshotWatcher -> Weak<...>    [non-owning liveness edge]
```

Several public values are temporary and are therefore absent from this durable graph:

- `DocumentView<'a>` borrows strings and tags from one live `Document`;
- `MatchView<'a>` borrows a title and matched text from live documents;
- `EditSession` owns independent staged copies and can outlive a workspace borrow;
- `CommitFailure` owns the rejected session and the typed error;
- the normalized query inside `with_normalized_query` may be borrowed or locally owned, but the callback cannot export its reference.

### Classify each edge

Use four labels.

#### Owning edge

Dropping the source may drop the target when no other owners remain. `Workspace -> Document` and `Rc<DocumentSnapshot> -> snapshot allocation` are owning edges.

#### Shared strong edge

Multiple edges participate in liveness. Every `Rc` clone increments the strong count. The snapshot cache and script aliases may both keep the same allocation alive.

#### Weak edge

A `Weak` value can ask whether an allocation remains alive but does not keep it alive. This is the watcher relationship.

#### Borrowed edge

A reference is permission constrained by a lifetime. `DocumentView<'a>` does not participate in destruction of its document. Its type prevents use after the corresponding workspace borrow ends.

### Lifetime ledger for a view

Consider:

```rust
let view = workspace.view(handle)?;
println!("{}", view.title());
```

The important relationship is not that `view` has a named lifetime in source. The public signature is conceptually:

```rust
fn view<'workspace>(
    &'workspace self,
    handle: DocumentHandle,
) -> Result<DocumentView<'workspace>, WorkspaceError>
```

The output borrow is tied to the `&self` receiver. The handle contributes identity but no borrowed storage. The compiler can shorten `'workspace` to the actual use region of `view`.

### Why handles and views coexist

A handle and a view solve different problems:

- a handle is owned, copyable identity that may survive mutations but can become stale;
- a view is non-stale access to current data, but it prevents conflicting mutation while active.

Trying to make one replace the other weakens the design. Returning references as durable identity creates lifetime pressure and inhibits mutation. Returning only handles forces every field read through a lookup and cannot express a temporary proof that the referred data remains present for a scope.

### Destruction trace

At `ScriptEngine` destruction:

1. field drop order follows declaration order after the destructor body, if any;
2. the workspace drops its slots and its snapshot cache;
3. script-owned `Rc` aliases may keep snapshots alive until their map is dropped;
4. watchers drop only weak counts;
5. every document drops strings, tags, cache, and counters through normal field destruction;
6. no custom `Drop` implementation is required.

The precise order among maps is not a product contract. The liveness graph is. No semantic cleanup depends on a particular `HashMap` element order.

### Design review questions

For every proposed feature, answer:

1. Does it create a new durable owner?
2. Can it create a cycle?
3. Does it export a borrow or an owned snapshot?
4. Which mutation invalidates it?
5. Is invalidation enforced statically, dynamically, or by generation/revision checks?
6. What remains alive after the originating API call returns?
7. What is dropped if the operation fails halfway?

These questions are the capstone's architecture language. File names are secondary.

## Generational Handles and Slot Reuse

A vector index is not a durable identity. If a document at index `0` is removed and a later document reuses index `0`, an old index silently identifies the wrong object. A reference would prevent this confusion while it remains valid, but a reference cannot serve as long-lived, mutation-friendly identity across arbitrary workspace operations.

The capstone uses:

```rust
pub struct DocumentHandle {
    slot: usize,
    generation: u64,
}
```

Each `Slot` stores the generation associated with its current or next valid occupation. Lookup compares both components.

### State transition

A slot follows this simplified protocol:

```text
Vacant(g) --add--> Occupied(g)
Occupied(g) --remove--> Vacant(g + 1)
Vacant(g + 1) --add--> Occupied(g + 1)
```

The old handle `(index, g)` is rejected once the slot moves to generation `g + 1`, even if the index is reused immediately.

### Why generation increments on removal

Incrementing at removal establishes invalidity before reuse. This matters because a vacant slot is still an observable internal state. If generation changed only during a later insertion, code between removal and insertion could distinguish a vacant current handle from a stale handle inconsistently. The chosen protocol makes removal the invalidation event.

### Overflow is not hand-waved

A generation is finite. The implementation uses `checked_add`. If `u64::MAX` is reached, removal returns `GenerationOverflow` rather than wrapping and potentially making ancient handles valid again. A vacant maximum-generation slot is not selected for reuse.

In practice, exhausting 64-bit generations is implausible. The typed branch still matters because the correctness argument depends on non-repetition. “It will never happen” is not an implementation of that invariant.

### Borrow structure of lookup

The immutable route is layered:

```text
view(handle)
  -> resolve(handle)
      -> slot(handle)
          -> bounds check
          -> generation check
      -> occupation check
  -> Document::view(handle)
```

The mutable route mirrors it with `slot_mut` and `resolve_mut`. This separation ensures that generation validation occurs before a mutable document reference is exposed.

### Why not store references in aliases

`ScriptEngine` stores `HashMap<String, DocumentHandle>`, not `HashMap<String, &Document>`. A reference would tie the engine's internal map to a borrow of its own workspace, producing a self-referential structure: one field would point into another field of the same movable owner. Handles replace address-based identity with logical identity plus validation.

### Why not `Rc<RefCell<Document>>` for every document

That representation would make every alias a strong owner and every mutation dynamically checked. Removal from the workspace would not necessarily remove the document because aliases could keep it alive. It would also erase the distinction between product identity and liveness. The current design centralizes ownership in the workspace, uses ordinary `&mut` for document mutation, and introduces reference counting only for immutable snapshots that genuinely have shared liveness.

### Stale, vacant, and unknown are distinct

The error taxonomy preserves different diagnoses:

- `UnknownSlot`: the index has never existed;
- `StaleHandle`: the index exists but generation differs;
- `VacantSlot`: generation matches but no document occupies it.

Public callers do not usually fabricate a current-generation handle to a vacant slot because fields are private, but preserving the distinction makes internal invariants and tests clearer.

### Acceptance checks
The critical test sequence is:

1. add document A and retain handle `h1`;
2. remove A;
3. add document B and obtain `h2`;
4. assert `h1.slot() == h2.slot()`;
5. assert generations differ;
6. assert `view(h1)` returns `StaleHandle`;
7. assert `view(h2)` returns B.

A test that merely checks that removal works does not prove the ABA-style identity problem has been addressed.

## Borrowed Views and Search Results

The workspace should permit rich observation without cloning every title and document body. It therefore returns view types containing references into live documents.

```rust
pub struct DocumentView<'a> {
    handle: DocumentHandle,
    title: &'a str,
    text: &'a str,
    tags: &'a [String],
    revision: u64,
}
```

The view owns only small metadata. Its text-bearing fields borrow the document selected through the workspace borrow.

### Receiver-derived lifetime

The signature:

```rust
pub fn view(
    &self,
    handle: DocumentHandle,
) -> Result<DocumentView<'_>, WorkspaceError>
```

uses lifetime elision, but the derivation is exact: the output borrows from `&self`. It does not borrow from the handle. While a view remains in use, code cannot mutably borrow the workspace in a way that might alter or remove the underlying document.

This is not an inconvenience added by the compiler. It is the API's consistency guarantee. A view cannot silently observe a title before a mutation and text after the mutation.

### Search returns two forms of evidence

`MatchView<'a>` includes:

- borrowed title;
- borrowed exact matched substring;
- owned byte range;
- handle and revision;
- optional zero-based line number.

The borrowed substring makes immediate rendering allocation-free. The range plus `(handle, revision)` is durable evidence that can be copied into an owned result if a caller needs to retain it. A production design might expose a dedicated owned `MatchRecord` conversion; the course keeps the distinction visible.

### Why ranges are byte ranges

Rust strings are UTF-8. `str::match_indices` returns byte offsets that lie on valid character boundaries for a matched `&str`. Slicing with the resulting range is safe because both boundaries originate from the string search operation. The capstone never treats an arbitrary character count as a byte index.

The range is meaningful only for the exact document revision. After an edit, the same byte range may identify different text or no valid boundary. This is why the result carries revision metadata rather than pretending a range is timeless identity.

### Search and internal caching

For each match, the document asks its line cache which line contains the start byte. The search method has only `&self`, yet cache population may occur through `RefCell`. The returned `MatchView` borrows the document strings, not the temporary `Ref` guard used to inspect cached ranges. No reference into the cache escapes.

That distinction is essential. Returning `&Range<usize>` from inside a `RefCell` without returning the guard would be invalid because the runtime borrow token would be dropped. The implementation clones the small `Range` where needed and returns references only to ordinarily borrowed document fields.

### Borrow-compatible rendering

A caller can render search results while the result vector is live:

```rust
let matches = workspace.search("memory");
for item in &matches {
    println!(
        "{}:{} {}",
        item.handle,
        item.line.map_or(0, |line| line + 1),
        item.matched,
    );
}
```

It cannot commit an edit through `&mut workspace` before the borrowed results' last use. The normal repair is not cloning the entire workspace. Finish observation, extract owned identifiers/ranges if required, then mutate.

### Empty and normalized queries

Search trims leading and trailing whitespace without allocation when possible. Runs of internal whitespace are collapsed to one ASCII space; that branch owns a normalized `String` through `Cow::Owned`. An empty normalized query returns no matches. Search remains exact and case-sensitive after whitespace normalization. The capstone does not claim Unicode normalization, grapheme-aware matching, or case folding.

### Design alternative: iterator return

An iterator could avoid allocating the vector of `MatchView` values. Implementing a nested iterator over slots and `match_indices` would make the lifetime and closure state more complex and would shift focus toward advanced iterator construction, which belongs later in the program. Returning a vector of small borrowed records keeps the ownership proof visible. The vector allocates record storage, but not copies of document text.

### Proof obligation

Tests must establish both semantic and borrowing behavior:

- every returned `matched` slice equals the source range;
- line numbers are correct across line boundaries;
- surrounding query whitespace is normalized without forcing ownership;
- repeated or non-ASCII internal whitespace enters the owned normalization branch;
- empty queries return no results;
- a compile-fail specimen shows that borrowed results cannot remain usable after mutable workspace access.

## Staged Edits, Revisions, and Failure Atomicity

Editing is where ownership topology becomes product behavior. Mutating a live document field by field would expose partial state if validation or later work failed. Holding `&mut Document` across user code would also prevent the workspace from performing other operations and would create difficult panic behavior.

The capstone uses an owned staging object:

```rust
pub struct EditSession {
    handle: DocumentHandle,
    expected_revision: u64,
    title: String,
    text: String,
    tags: Vec<String>,
}
```

`begin_edit` borrows the workspace briefly, validates the handle, and clones current editable state into the session. The borrow ends when the function returns. The caller can then modify the owned session without holding any reference into the workspace.

### Why cloning is correct here

Earlier modules treat reflexive cloning as a design smell. This use is semantic duplication: the live document and the working draft must coexist independently. An edit may be abandoned, may conflict, or may be repaired after validation failure. Borrowing the live strings would not provide isolation, and moving them out would damage the source before commit.

The right question is not “does this clone?” It is “does the product require two independently owned versions?” Here it does.

### Optimistic revision check

The session records the revision observed at creation. Commit succeeds only when the current document revision equals `expected_revision`.

```text
begin at revision 4
session expects 4
another commit advances live document to 5
old session commit sees actual 5 and fails
```

Although the capstone is single-threaded, two sessions can coexist and model stale work. The mechanism prepares you to reason about optimistic concurrency without introducing threads.

### Consuming commit

`Workspace::commit` consumes `EditSession`. On success, owned strings move into the live document without another clone. On failure, `CommitFailure` returns both:

```rust
pub struct CommitFailure {
    pub error: WorkspaceError,
    pub session: EditSession,
}
```

This is a valuable ownership pattern: consume an operation token, and return it when the transition cannot complete. The caller retains the work instead of losing it behind an error.

### Commit order

A correct commit order is:

1. validate staged title and tags without touching live state;
2. resolve the handle mutably;
3. compare expected and actual revision;
4. compute the next revision with checked arithmetic;
5. move staged fields into the document;
6. assign the new revision;
7. invalidate derived cache state;
8. return a receipt.

Every fallible check occurs before the destructive moves. After the first field move, the implementation should have no remaining fallible operation.

### Panic behavior

If user code panics while an `EditSession` is being modified, stack unwinding drops the session's owned working strings. The live workspace was never mutably borrowed and remains unchanged. No custom destructor is needed.

Commit itself does not call user callbacks. Its mutation sequence contains no expected panic after validation. A memory-allocation panic or process abort lies outside ordinary recoverable guarantees, but Rust still prevents use-after-free.

### Why this is RAII even without custom `Drop`

RAII means resource lifetime follows value lifetime. The session owns the provisional state. Dropping the session means abandoning that state. A custom `Drop` implementation would be harmful if it tried to auto-commit: destructors cannot return recoverable errors, run during unwinding, and should not hide major product transitions.

### What `CommitReceipt` proves

A successful receipt contains handle and resulting revision. It is owned, small, and durable. It does not borrow the document, so the caller may continue mutating the workspace. To read committed content, the caller asks for a new view.

### Tests that matter

- staged changes are invisible before commit;
- successful commit advances exactly one revision;
- two concurrent sessions cause the stale one to fail;
- failure returns the exact staged content;
- validation failure leaves live state unchanged;
- panic during session editing leaves live state unchanged;
- successful edit invalidates line cache and the next query records a miss.

These tests prove protocol semantics. A test that only changes text once proves almost nothing about the ownership design.

## Shared Snapshots and Weak Observation

A live document is centrally owned and mutable. A snapshot is immutable historical state that may have multiple simultaneous consumers. The two objects therefore use different ownership mechanisms.

`DocumentSnapshot` owns compact, immutable data:

```rust
pub struct DocumentSnapshot {
    key: SnapshotKey,
    title: Box<str>,
    text: Box<str>,
    tags: Box<[Box<str>]>,
}
```

A workspace cache maps `SnapshotKey` to `Rc<DocumentSnapshot>`. The script engine may also hold `Rc` clones under user aliases.

### Why `Rc`

The capstone is explicitly single-threaded. `Rc` provides non-atomic reference counting and communicates that values must not cross thread boundaries. `Arc` would add thread-safe reference counting but would not make the contained design generally thread-safe; the workspace also uses `Cell` and `RefCell`. Choosing `Arc` “for the future” would obscure the actual contract.

### Cache identity

The key is `(DocumentHandle, revision)`. A document revision is immutable after it has been superseded, so that pair identifies one historical value. Repeated snapshot calls return `Rc::clone` of the same allocation while the cache entry remains.

The API does not promise pointer identity after eviction. If all strong owners are dropped and a later request reconstructs the same revision—normally impossible after live editing, but possible in a richer history store—the semantic key matters more than address identity.

### `Weak` as observation without liveness

`SnapshotWatcher` owns:

```rust
key: SnapshotKey,
weak: Weak<DocumentSnapshot>,
```

A watcher can call `upgrade` to obtain a temporary strong owner when the snapshot is alive. If every `Rc` has been dropped, `upgrade` returns `None`.

This distinction prevents an observer from becoming a hidden retention path. A metrics registry, UI selection marker, or cache index often needs to detect liveness without deciding liveness.

### Strong-count reasoning

Suppose a snapshot has:

- one `Rc` in the workspace cache;
- one script snapshot alias;
- one local variable;
- two watchers.

The strong count is three. The weak count includes two watchers and an implementation-internal weak reference associated with the control block, depending on how the library reports counts. Product logic should not rely on exact weak-count internals. Dropping watchers cannot destroy the payload; dropping all three strong owners does.

### Eviction is not destruction

`evict_snapshot` removes the cache's strong edge. Other `Rc` aliases may keep the allocation alive. This is why the method returns only whether a cache entry was removed, not whether the snapshot was destroyed.

The demonstration sequence makes the distinction visible:

1. cache owns snapshot;
2. script alias owns snapshot;
3. watcher observes weakly;
4. edit creates a newer live revision;
5. cache entry for old revision is evicted;
6. script alias is dropped;
7. watcher reports expired.

If step 6 is omitted, the watcher must still report alive.

### Cycle analysis

The snapshot graph cannot form a cycle because `DocumentSnapshot` contains no `Rc` back to the workspace or another snapshot. The cache points one way. Watchers are weak. This should be documented, not assumed from “we used `Weak` somewhere.”

In a tree or graph, cycle prevention requires identifying exactly which conceptual edges own children and which observe parents. A single misplaced strong parent link can leak an entire component.

### Why boxed slices

Snapshots are immutable and do not need spare vector or string capacity. Converting owned strings to `Box<str>` and the tag vector to `Box<[Box<str>]>` communicates fixed-size ownership and may avoid retained capacity. It does not guarantee a particular allocator footprint. The memory report counts payload bytes and labels target-specific type sizes separately.

## Interior Caches and Runtime Borrow Discipline

Line lookup is logically read-only: asking for line 12 should not change the document's semantic text, title, tags, or revision. Computing line boundaries lazily does mutate derived implementation state. This is a justified interior-mutability use.

Each document stores:

```rust
cache: RefCell<Option<DocumentCache>>,
cache_hits: Cell<u64>,
cache_misses: Cell<u64>,
```

`Cell<u64>` supports copy-in/copy-out counter updates. `RefCell` supports storing and replacing a non-`Copy` cache through `&Document`.

### Semantic versus representational mutation

The API classifies mutation by observable product meaning, not by whether bytes change somewhere in memory.

- changing text is semantic mutation and requires `&mut Workspace` through a commit;
- populating line ranges is representational mutation and occurs behind `&Workspace`;
- incrementing diagnostics counters is representational mutation.

This distinction must be defended. “Caching” is not an automatic license to place arbitrary state in `RefCell`.

### Runtime borrow protocol

`RefCell` enforces the same high-level exclusivity rule at runtime:

- any number of active `borrow()` guards, or
- exactly one active `borrow_mut()` guard.

Violation panics. The implementation deliberately keeps guards short:

1. inspect whether a current-revision cache exists;
2. drop the shared guard at the end of the expression;
3. compute ranges outside any mutable guard;
4. acquire `borrow_mut()` only to replace the option;
5. release it before returning borrowed document text.

Holding a `Ref` across a call that may need `borrow_mut` would convert an ordinary query into a runtime panic.

### Revisioned validity

`DocumentCache` stores the revision from which its ranges were derived. `ensure_cache` considers a cache hit only when revisions match. Successful commit also removes the cache explicitly.

The revision check is defense in depth. Explicit invalidation makes intent clear and releases memory. Revision comparison protects against future code paths that might forget invalidation.

### Returning text, not cache references

`line` obtains an owned `Range<usize>` by cloning the small range from the cache, drops the `Ref` guard, then slices ordinary document text:

```text
cache guard -> cloned byte range -> guard dropped -> &self.text[range]
```

The returned `&str` is tied to `&Document`, not to a runtime guard. This is a core design technique when interior metadata identifies data stored outside the cell.

By contrast, if the text itself were inside `RefCell<String>`, a plain `&str` could not escape the borrow guard. The API would need to return `Ref<'_, str>`, use a callback, or return owned data.

### Panic-safety boundary

A `RefCell` borrow conflict panics. The capstone avoids exposing methods that allow arbitrary user closures while a guard is active. It also does not catch `RefCell` panics as domain errors. A runtime borrow conflict indicates a programming defect in this design, not invalid user input.

The laboratory for this module includes a deliberately reentrant cache that panics. The repair shortens guards and separates computation from installation.

### Why not `OnceCell`

A one-time cell is suitable when a value, once computed, never becomes stale. Document line ranges change after every text edit. The cache needs replacement and revision tracking, so `RefCell<Option<_>>` expresses the actual lifecycle. A future design could use a revision-keyed `OnceCell` per immutable snapshot, where one-time initialization would be truthful.

### Why not require `&mut self`

Requiring mutable access for every line read would prevent simultaneous read views, complicate search, and expose an implementation detail in the semantic API. Interior mutability is warranted because the cache does not alter the logical value and because runtime borrow scopes are tightly controlled and tested.

## Scoped Normalization and `Cow`

Queries often need normalization. Trimming may return a slice of the original input with no allocation, while a more complex normalization could require an owned temporary. `Cow<'a, str>` represents either form.

The internal helper is conceptually:

```rust
fn normalize_query(raw: &str) -> Cow<'_, str> {
    let trimmed = raw.trim();
    let canonical = trimmed
        .chars()
        .try_fold(false, |previous_was_space, character| {
            if character.is_whitespace() {
                if previous_was_space || character != ' ' {
                    None
                } else {
                    Some(true)
                }
            } else {
                Some(false)
            }
        })
        .is_some();

    if canonical {
        Cow::Borrowed(trimmed)
    } else {
        Cow::Owned(trimmed.split_whitespace().collect::<Vec<_>>().join(" "))
    }
}
```

Leading and trailing whitespace can be removed by borrowing the subslice returned by `trim`; no allocation is needed. Internal whitespace normalization is different. A tab, newline, non-ASCII whitespace character, or repeated space is collapsed to one ASCII space, which requires a new `String`. The two `Cow` variants therefore correspond to a real cost distinction rather than an artificial teaching branch.

### The escape problem

If a function simply returned `&str`, a borrowed result could come from `raw`, but an owned temporary created inside the function could not be returned by reference. Returning `Cow` solves that by returning ownership when required.

A different design uses a scoped callback:

```rust
pub fn with_normalized_query<R>(
    &self,
    raw: &str,
    operation: impl for<'query> FnOnce(&'query str) -> R,
) -> R
```

The higher-ranked bound means the callback must work for whatever short lifetime the method chooses. When normalization creates an owned local string, the callback receives a reference valid only during the call. It cannot select that reference as `R` and export it.

### Who chooses the lifetime

This distinction is central:

```rust
fn ordinary<'a, R>(value: &'a str, f: impl FnOnce(&'a str) -> R) -> R
```

Here, the caller participates in choosing `'a` through the input.

```rust
fn scoped<R>(f: impl for<'a> FnOnce(&'a str) -> R) -> R
```

Here, the callee may instantiate `'a` freshly. The callback must be valid for every such choice. It cannot assume `'a` is long enough to escape.

### Useful results

The callback may return values independent of `'query`:

- length;
- hash;
- parsed owned command;
- `String` clone;
- Boolean predicate;
- an index into external data.

It cannot return `&'query str` as a fixed `R`. A rustdoc `compile_fail` specimen preserves that negative proof.

### Why keep both `search` and scoped normalization

`search` calls normalization internally and returns borrows from workspace documents, not from the query. `with_normalized_query` isolates the HRTB mechanism for study and for callers that need custom immediate work on the normalized query.

The two APIs teach a useful separation: a temporary input borrow can guide a computation whose outputs borrow from an entirely different owner.

### `Cow` is not universal

Do not replace every `&str`/`String` decision with `Cow`. It adds a sum type and branching. Use it when a function naturally produces borrowed data in common cases and owned data in others, and callers can benefit from receiving either without losing the relationship.

For stored document titles, ownership is mandatory; `Cow` would merely move lifetime complexity into the workspace. For immediate normalized queries, temporary dual ownership is meaningful.


## Memory Reporting Without False Guarantees

The capstone reports memory-related facts, but it separates three categories that are often carelessly merged.

### Semantic payload counts

These are counts derived from product data:

- bytes currently used by title contents;
- bytes currently used by text contents;
- bytes currently used by tag contents;
- number of cached line ranges;
- number of snapshot cache entries;
- snapshot payload bytes.

For UTF-8 strings, `len()` reports bytes, not user-perceived characters. The field names say “bytes” explicitly.

### Capacity observations

`String::capacity()` and `Vec::capacity()` report element storage currently reserved by those containers. Summing string capacities is useful for comparing payload length with retained capacity, but it is not exact process memory.

It excludes allocator metadata, allocation rounding, control blocks, map buckets unless counted separately, stack frames, executable pages, fragmentation, and temporary allocations. The report publishes those exclusions.

### Type representation observations

`size_of::<T>()` and `align_of::<T>()` report the current target/toolchain representation of the named type. `TypeObservation` labels each row as observed, not guaranteed.

For example, observing the size of `Option<DocumentHandle>` does not establish a language-level niche guarantee unless the Reference documents one for the involved types. A future compiler, target, or field change may alter size.

### Deduplicating shared allocations

Multiple `Rc` values may point to one snapshot allocation. Counting every strong handle as a distinct payload would overstate snapshot data. The report uses `Rc::ptr_eq` to identify unique snapshot payload allocations reachable from the workspace cache.

It still does not count the `Rc` control block exactly. That layout is an implementation detail of the standard library. The report says so.

### Shallow versus deep size

`size_of::<String>()` measures the inline owner representation, not the heap buffer. `size_of::<Rc<DocumentSnapshot>>()` measures the inline smart pointer, not the snapshot payload or control block. The capstone displays these observations alongside separately calculated payload counts so you cannot mistake one for the other.

### Why not use heap profiling here

A profiler or allocator instrumentation would provide richer empirical data and belongs in Course 9. Course 2 focuses on representation contracts and ownership topology. The capstone teaches how to state limited measurements honestly before using more powerful tools.

### Required language in reports

A good report says:

> On target X with toolchain Y, `T` was observed to have size S and alignment A. The Rust layout contract does or does not guarantee the relevant relation. Heap payload accounting includes fields P and excludes categories E.

A bad report says:

> `Rc<T>` costs exactly N bytes.

The second statement usually conflates the inline pointer, control block, allocator behavior, and payload.

### Overflow and accounting

The current capstone uses ordinary `usize` sums for compact educational data. A hardened telemetry system should choose an explicit overflow policy—checked accumulation, saturation, or wider counters—and test it. Memory accounting is observational; it must not corrupt product state if a metric cannot be represented.

### Interpretation exercise

Given:

```text
live_documents = 3
text_payload_bytes = 900
live_string_capacity_bytes = 2048
snapshot_cache_entries = 4
unique_snapshot_allocations = 3
```

valid conclusions include:

- live text contains 900 UTF-8 bytes;
- live document strings collectively reserve at least the reported container capacities;
- at least two cache entries or handles may share one allocation if the counting domain includes duplicates;
- retained capacity exceeds current payload.

Invalid conclusions include:

- the process uses exactly 2048 bytes for strings;
- each snapshot has one unique allocation;
- memory fragmentation is 1148 bytes;
- the representation is identical on every target.

## Why This Design Does Not Use Pinning

Course 2 culminates in pinning, but mastery includes refusing it when no address-sensitive invariant exists. `memory-workspace` deliberately does not pin documents, snapshots, sessions, or slots.

### Mechanical movement is not semantic invalidation here

A `Document` may move when the `Vec<Slot>` reallocates. Its `String` owner fields move as small handles while their heap buffers may remain elsewhere. No field stores a pointer to the document's own address, no external registry records that address, and no API promises stable placement. Moving the `Document` value preserves every semantic invariant.

A `DocumentView` borrows fields. While the view is in use, a mutable workspace operation that could reallocate slots is rejected. Static borrowing—not pinning—provides the required stability for the view's scope.

### Handles are logical identity

Long-lived identity uses `(slot, generation)`, not an address. A handle remains copyable even if the vector reallocates. Lookup re-establishes a fresh borrow after validating identity.

This is often superior to address-based design:

- values remain movable;
- containers can grow normally;
- serialization is possible;
- no projection API is required;
- no unsafe code is needed;
- stale identity is diagnosed explicitly.

### Snapshots do not need stable addresses

`Rc<DocumentSnapshot>` happens to place its payload in a heap allocation that is not moved while the allocation lives, but the public contract does not depend on the address. Consumers use immutable data and semantic keys. Wrapping the snapshot in `Pin<Rc<_>>` would add no protection relevant to the product.

### Interior mutability is not address sensitivity

`RefCell` and `Cell` change how mutation permission is checked. They do not create a requirement that the containing object remain at one address. These mechanisms solve orthogonal problems.

### What would create a pinning requirement

A future feature might register a document node with a C library that stores its address, or create a self-referential parser state holding pointers into its own buffer. Such a feature would require:

1. a documented address-sensitive invariant;
2. initialization only after stable placement;
3. safe methods taking `Pin<&Self>` or `Pin<&mut Self>` as appropriate;
4. projection rules for pinned fields;
5. a destructor compatible with the pinning drop guarantee;
6. a small audited unsafe core if raw self-references are constructed.

That work belongs to systems programming and unsafe abstraction review, not to this safe capstone.

### Why `Box::pin` would not prove need

Any value can be placed in `Pin<Box<T>>`. For `T: Unpin`, callers can recover ordinary mutable access and move the value out by replacement. The wrapper is operationally unnecessary. Even for `!Unpin`, adding `PhantomPinned` without an invariant creates ceremony, not safety.

### The design review record

The capstone should preserve a short architecture decision:

```text
Decision: do not pin workspace entities.
Reason: no semantic relationship depends on object address.
Long-lived identity uses generational handles.
Borrowed access uses ordinary reference lifetimes.
Shared historical state uses Rc ownership.
Revisit only if an external or self-referential invariant is introduced.
```

This negative decision is part of the final defense. You must be able to distinguish “heap allocated,” “not currently moved,” “not safely movable,” and “pinned by contract.”

## Script Grammar and Executable Shell

The binary exists to exercise the library through a real process boundary. It does not become a second domain implementation. `main.rs` selects a built-in scenario or reads a script file, delegates to `ScriptEngine`, prints deterministic lines, and returns an exit code.

### Invocation

```bash
cargo run -p memory-workspace -- demo
cargo run -p memory-workspace -- script capstone/scripts/demo.memory-workspace
cargo run -p memory-workspace -- help
cargo run -p memory-workspace -- version
```

Unknown argument shapes produce a nonzero exit status and a usage message on standard error.

### Grammar

Scripts are UTF-8 text. Commands are separated by lines. Fields are separated by literal tab characters. Empty lines and lines whose first non-whitespace character is `#` are ignored.

```text
ADD<TAB>document-alias<TAB>title<TAB>text
SHOW<TAB>document-alias
EDIT<TAB>document-alias<TAB>expected-revision<TAB>replacement-text
RENAME<TAB>document-alias<TAB>expected-revision<TAB>title
TAG<TAB>document-alias<TAB>expected-revision<TAB>tag
SEARCH<TAB>query
SNAPSHOT<TAB>snapshot-alias<TAB>document-alias
WATCH<TAB>watcher-alias<TAB>snapshot-alias
DROP-SNAPSHOT<TAB>snapshot-alias
EVICT<TAB>document-alias<TAB>revision
CHECK-WATCH<TAB>watcher-alias
REMOVE<TAB>document-alias
MEMORY
LIST
```

The format intentionally forbids tabs inside fields through title/tag validation. Text in the small script language is one line; multiline document content is available through the library API, not encoded with escape processing here.

### Alias ownership

The engine maintains three separate maps:

- document aliases own `DocumentHandle` values;
- snapshot aliases own strong `Rc` values;
- watcher aliases own `Weak` wrappers.

Aliases are globally unique across these maps. This makes demonstration traces unambiguous and prevents a command from resolving the same spelling through the wrong ownership category.

### Error preservation

Parser errors remain typed: invalid arity, revision syntax, unknown alias category, unknown command, and workspace domain failures are distinct. Whole-script execution wraps the original error in `AtLine { line, source }` rather than converting every failure into one string category.

That wrapper preserves both context and source taxonomy. `Display` adds human-readable line information; `Error::source` exposes the underlying error for structured inspection.

### Deterministic output

`LIST` sorts handles before rendering because map or internal vector traversal order should not leak as unstable output. Search traverses slots in index order and match positions in source order. The demonstration can therefore be checked by tests without depending on hash iteration order.

### Why no quoting language

A robust general CLI format would need escaping, quoting, Unicode considerations, and possibly a parser crate. The capstone script is an executable test protocol, not a user-facing interchange standard. Its narrow grammar keeps parsing transparent and lets the course focus on ownership categories.

### Process-level tests
Integration tests launch the actual binary using Cargo's `CARGO_BIN_EXE_memory-workspace` path. They verify:

- the demo exits successfully;
- output contains a memory report;
- a weak watcher eventually expires;
- a real temporary script file is read and executed;
- invalid invocation exits unsuccessfully.

Library tests cannot prove that argument routing, standard streams, and exit codes are wired correctly. The process boundary needs its own evidence.

## Testing and Proof Matrix

A memory-oriented course must test more than returned values. It must preserve negative evidence, liveness evidence, failure-state evidence, and representation disclaimers.

### Behavioral tests

| Requirement | Primary evidence |
|---|---|
| add/view round trip | public integration test |
| stale handle rejection | remove–reuse sequence |
| exact search slices | range-to-source assertion |
| line lookup | multi-line public test |
| staged isolation | view before commit |
| successful revision | receipt and post-view |
| conflict recovery | returned session contents |
| snapshot immutability | old/new snapshot comparison |
| snapshot sharing | `Rc::ptr_eq` |
| weak expiry | eviction plus last-strong-drop |
| cache invalidation | hit/miss sequence across edit |
| script routing | engine and binary tests |
| memory labels | report field/exclusion assertions |

### Negative compile tests
Ordinary runtime tests cannot express “this reference must not escape” or “this pinned value must not be moved through safe access.” Those claims live in rustdoc `compile_fail` specimens and the compiler laboratory.

Examples include:

- using a `DocumentView` after mutably borrowing the workspace;
- returning the temporary borrow passed to `with_normalized_query`;
- obtaining `&mut PinnedTracker` from `Pin<&mut PinnedTracker>` when it is `!Unpin`;
- mixing branded handles from independent arena invocations;
- exporting a borrow from a scoped visitor.

Every negative specimen must fail for the intended reason. A syntax error is not proof of the ownership property.

### Panic-path tests
`RefCell` borrow violations and deliberate panic-unwinding cases are tested with `catch_unwind` only where panic is the mechanism under study. Domain validation errors remain `Result`; they are not tested as panics.

When using `catch_unwind`, wrap only values whose unwind-safety contract is understood. `AssertUnwindSafe` is a local assertion, not a universal repair. After the panic, inspect the state whose consistency was promised.

### Liveness checks
Reference counts should be tested through semantic observations, not fragile exact counts unless the test controls every owner. `Rc::ptr_eq`, `Weak::upgrade`, and object-drop probes are stronger than asserting a count in code that may acquire temporary clones.

### Destruction checks
The capstone relies mostly on ordinary field destruction. Independent labs use drop logs and lease guards to prove exactly-once cleanup. The capstone's relevant destruction proof is that dropping an edit session leaves live state unchanged and that dropping strong snapshot owners allows weak expiry.

### Tooling route

From the course root:

```bash
cargo fmt --all -- --check
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
cargo test --workspace --doc
cargo doc --workspace --no-deps
cargo build --workspace --release
make compiler-labs
make capstone-confirm
```

Passing only `cargo test` is insufficient. Compile-fail evidence, lint policy, documentation examples, process tests, and release construction cover different failure surfaces.

### Mutation review

For each mutating capstone method, reviewers answer:

1. What validation runs before state change?
2. What values are moved?
3. Can any operation fail after the first move?
4. Which derived state becomes stale?
5. Which borrows are active?
6. What does a panic drop?
7. What evidence observes the failure state?

### False-confidence patterns

Reject these claims:

- “The borrow checker proves the cache is logically fresh.” It proves reference safety; revision logic proves freshness.
- “`Rc` prevents leaks.” Cycles can leak; topology prevents cycles here.
- “The value is boxed, so it is pinned.” Allocation and pinning are different.
- “`size_of` proves heap cost.” It reports inline representation.
- “The session has `Drop`, so it is RAII.” The capstone session does not need custom `Drop`; ownership itself supplies RAII.
- “No test failed, so stale handles are impossible.” Only the remove/reuse adversarial path addresses that invariant.

## Code-Reading Walkthrough

Read the capstone in dependency order rather than opening `main.rs` first.

### 1. `handle.rs`

Establish the identity type and its parse/display boundary. Confirm that fields are private, accessors are value-returning, and parsing cannot construct malformed numeric components. Ask what prevents a caller from forging a current generation; the answer is not secrecy alone—workspace lookup still validates occupation.

### 2. `cache.rs`

Study line-range construction independently of interior mutability. Check CRLF handling, empty text, trailing newline behavior, and byte offsets. Pure derivation is separated from cache installation so no runtime borrow guard is held during computation.

### 3. `model.rs`

Trace owned fields and derived state. For every method, label whether it:

- returns a receiver-derived borrow;
- copies diagnostic metadata;
- mutates through `Cell`/`RefCell`;
- clones a small range to release a guard;
- invalidates representation state after semantic mutation.

Pay particular attention to the difference between `DocumentView<'_>` and `RemovedDocument`. Removal returns ownership; viewing returns borrows.

### 4. `edit.rs`

Verify that an edit session has no references into the workspace. This is what lets sessions coexist and survive between operations. Mutation methods change only owned working fields.

### 5. `snapshot.rs`

Draw the allocation graph for `Rc<DocumentSnapshot>` and `Weak<DocumentSnapshot>`. Confirm that snapshot content has no back-reference to the workspace. Inspect why `Box<str>` and boxed slices express fixed immutable ownership without making layout promises.

### 6. `workspace.rs`

This is the protocol center. Read methods in state-transition order:

```text
add -> view/line -> begin_edit -> commit -> search -> snapshot -> remove
```

For `commit`, mark the last fallible check and the first destructive move. For `snapshot`, mark the point where the immutable document borrow ends before mutating the snapshot cache. For `remove`, mark the generation increment and movement of `Document` into `RemovedDocument`.

### 7. `memory.rs`

Separate payload computations from `size_of` observations. List every excluded category. Inspect `Rc::ptr_eq` use and confirm it deduplicates allocations rather than semantic keys.

### 8. `script.rs`

Classify each alias map by ownership edge. Follow an `EDIT` command through alias lookup, revision parsing, session creation, staged mutation, consuming commit, and deterministic receipt rendering. Confirm that line wrapping preserves source errors.

### 9. `lib.rs`

Review the public surface. Internal modules remain private; selected types are re-exported. Ask whether public fields expose invariants. `MatchView` and report types expose data records deliberately; document internals do not.

### 10. `main.rs`

The binary should remain a shell. It reads environment arguments and files, delegates, renders, and maps outcome to `ExitCode`. Domain mutation does not belong here.

### 11. Tests

Read tests after the implementation so each can be mapped to an invariant. Identify missing adversarial cases rather than merely counting assertions.

### Reconstruction exercise

Close the source and reconstruct these signatures from the product requirements:

```text
Workspace::view
Workspace::begin_edit
Workspace::commit
Workspace::search
Workspace::snapshot
Workspace::with_normalized_query
SnapshotWatcher::upgrade
```

For every parameter and return component, justify ownership, lifetime, and failure behavior. Then compare to the code. A mismatch is more instructive than memorizing the actual signature.

### One complete trace

Trace the demo from allocation to destruction:

1. `ADD` moves title/text into a live document;
2. `SHOW` creates and drops a borrowed view;
3. `SNAPSHOT` allocates immutable owned data and two strong edges emerge;
4. `WATCH` creates a weak edge;
5. `EDIT` clones live state into a session, then moves modified state back on commit;
6. old snapshot remains unchanged;
7. `SEARCH` returns temporary borrowed matches and populates line cache;
8. `EVICT` removes one strong edge;
9. `DROP-SNAPSHOT` removes the last strong edge;
10. watcher upgrade fails;
11. engine destruction drops workspace, aliases, watchers, and remaining data.

If you cannot narrate this trace precisely, the capstone is not mastered even if every test passes.

## Independent Extension Examination — Document Labels and Snapshot Comparison

The final implementation task is intentionally not pre-solved in the reference capstone. Add a cross-layer feature while preserving the existing ownership topology.

### Feature contract

Add two script commands:

```text
UNTAG<TAB>document-alias<TAB>expected-revision<TAB>tag
COMPARE<TAB>left-snapshot-alias<TAB>right-snapshot-alias
```

#### `UNTAG`

- begins an ordinary staged edit;
- verifies the expected revision;
- removes exactly the requested tag;
- returns a typed “tag not present” domain error rather than silently committing;
- on success advances revision exactly once;
- on any failure leaves the live document unchanged and preserves the session where useful.

#### `COMPARE`

- borrows two snapshot aliases without cloning snapshot payloads;
- reports whether title, text, and tags are individually equal;
- reports signed byte-length deltas for text and total payload;
- performs no live-workspace lookup;
- does not change strong ownership except for unavoidable short-lived borrows of the map-held `Rc` values;
- produces deterministic output.

### Required design work

Before coding, submit:

1. updated ownership graph;
2. signatures for any new domain types;
3. error-taxonomy change;
4. commit-order analysis for `UNTAG`;
5. argument for whether comparison output should borrow data or own scalar results;
6. proof that `COMPARE` does not preserve liveness beyond existing aliases.

### Constraints

- no new dependency;
- no `Rc<RefCell<DocumentSnapshot>>`;
- no mutation of snapshots;
- no conversion of all errors to strings;
- no `clone()` of snapshot title/text merely to compare them;
- no exact reference-count assertion in public behavior tests;
- no weakening of handle or revision validation;
- no pinning.

## Oral Defense and Transition

The capstone defense is a technical examination, not a presentation. You receive code locations and scenarios and must derive behavior without running the program.

### Ownership questions

1. Who owns live document text after `add`?
2. What exactly is duplicated by `begin_edit`, and why is duplication required?
3. Which values move during successful commit?
4. What owns a snapshot after the cache entry is evicted but a script alias remains?
5. Can a watcher destroy or preserve a snapshot?
6. Why does a document alias store a handle instead of a reference or `Rc<Document>`?
7. What is dropped after a panic while editing?

### Lifetime questions

1. Derive the elided lifetime of `Workspace::view`.
2. Why may a `DocumentView` not remain usable across `Workspace::remove`?
3. What does `MatchView<'a>` borrow, and what does it own?
4. Why can a cloned byte range escape a `RefCell` guard while a reference into the cache cannot?
5. Who chooses the lifetime in `with_normalized_query`?
6. Why can the callback return `String` but not the temporary `&str`?
7. Does `DocumentHandle` carry a lifetime? Why not?

### Runtime-borrow questions

1. Which cache operations can panic because of `RefCell` misuse?
2. Where are guards deliberately shortened?
3. Why is the returned line tied to document text rather than the cache guard?
4. What invariant makes cache mutation logically compatible with `&self`?
5. What alternative API would be required if text itself lived in `RefCell<String>`?

### Representation questions

1. What does `size_of::<String>()` include and exclude?
2. Why is `Box<str>` suitable for immutable snapshot text?
3. Does `Rc` guarantee the control-block layout?
4. What does `Rc::ptr_eq` prove?
5. Why are byte length and character count different?
6. Which report values are semantic counts and which are observations?

### Variance and marker questions

The capstone does not expose a branded arena, but you must still classify:

- `DocumentView<'a>` with respect to `'a`;
- `&'a mut T` with respect to `'a` and `T`;
- `RefCell<T>` with respect to `T`;
- `fn(&'a str)` with respect to `'a`;
- what a hypothetical `PhantomData<&'a Document>` would tell the compiler.

Then explain why no custom marker is required in the actual capstone.

### Pinning questions

1. Which capstone values move during vector reallocation?
2. Why is that movement semantically safe?
3. Does `Rc` make pinning automatic?
4. What invariant would have to be added before `Pin` became relevant?
5. Why would `PhantomPinned` alone be insufficient?
6. How do generational handles replace address identity?

### Failure scenarios

For each scenario, state the exact error and post-state:

- unknown slot;
- stale generation;
- vacant current slot;
- invalid title at add;
- invalid tag during commit;
- stale revision;
- generation overflow;
- revision overflow;
- unknown snapshot alias;
- malformed script arity;
- panic while editing;
- snapshot cache eviction while another strong owner exists.

### Transition to Course 3

Course 2 establishes ownership mechanisms. Course 3 will ask how to expose behavior across many types through traits, associated types, generic contracts, trait objects, typestate, and OOP-style composition. The transition should not blur responsibilities:

- Course 2 decides who owns data and how validity is enforced;
- Course 3 decides which behaviors are abstracted and how implementations substitute;
- Course 6 later audits unsafe code, raw-pointer invariants, FFI, and low-level layout-dependent interfaces;
- Course 9 later measures allocation and performance empirically.

You are ready only when ownership topology is a design input, not a compiler problem postponed until implementation.

## Architecture Decisions and Bounded Claims

### Cross-mechanism proof table

| Mechanism | Product responsibility | Evidence | Failure mode kept visible |
|---|---|---|---|
| generational handle | reject stale identity after slot reuse | stale-handle integration test | unknown, vacant, stale, generation exhaustion |
| borrowed view | expose live data without allocation | API lifetime and compile-fail reasoning | mutation cannot overlap the view |
| edit session | isolate candidate state from live state | panic/conflict/failure tests | typed error plus returned session |
| revision check | reject stale optimistic commits | concurrent-session test | expected and actual revision |
| `Rc` snapshot | share immutable historical state | pointer-identity and immutability tests | allocation remains alive while any strong owner exists |
| `Weak` watcher | observe without extending liveness | eviction/drop test | `upgrade` returns `None` after final owner drops |
| bounded retention | cap workspace-owned snapshots | FIFO limit and zero-limit tests | external owners are excluded from the bound |
| `RefCell` cache | derive line ranges through shared API | hit/miss and invalidation tests | runtime borrow discipline remains an obligation |
| HRTB + `Cow` | lend normalized temporary storage safely | borrowed/owned path tests and compile-fail derivation | temporary borrow cannot escape |
| memory report | expose useful bounded observations | arithmetic and exclusion tests | exact heap use is explicitly not claimed |
| pinning decision | avoid needless address-stability obligations | architecture defense | stable logical identity is not stable address |

### Defense prompts

1. Why is `EditSession` ownership preferable to a long-lived mutable borrow?
2. Why does a weak observer need `upgrade` rather than a Boolean liveness promise?
3. What can still keep a snapshot alive after FIFO eviction?
4. Why is `RefCell` appropriate for the cache but not for the authoritative document fields?
5. Which report fields are semantic counts, which are capacities, and which are target observations?
6. How would a second thread invalidate the current ownership graph?
7. Which concrete requirement would justify introducing `Pin`, and why is that requirement absent here?

The implementation-facing records are `capstone/ARCHITECTURE.md` and `capstone/LIMITATIONS.md`.

## Acceptance route

From the course root:

```bash
cargo test -p memory-workspace
cargo clippy --workspace --all-targets -- -D warnings
cargo fmt --all -- --check
```

The program should also pass the manual demonstration described in [`capstone/README.md`](../capstone/README.md).
