# 11 — Places, Move Paths, and Advanced Borrowing

**Course 2, day 1 · Module 11 of 90**  
`████░░░░░░░░░░░░░░░░` **11/90**

[← Module 10: Integration and Independent Change](../../../01-rust-foundations/course-book/module-10-integration-and-independent-change/index.md) · [Course 2 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 12: Lifetime Relationships and Borrowed APIs →](../module-12-lifetime-relationships-and-borrowed-apis/index.md)

## The question

> Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?

## Why this comes now

Course 1 treated a value as the unit of ownership. Advanced APIs often borrow or move only a field, an index, or a projection, so Course 2 begins by refining the unit of analysis from values to places and move paths. This precision eliminates many clone-based workarounds before lifetime notation becomes more demanding.

## What you will be able to do

- Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.
- Model loans over places and explain when fields, indices, slices, and method receivers can or cannot be borrowed disjointly.
- Use reborrowing, non-lexical lifetime shortening, two-phase borrowing, and split APIs without relying on folklore.
- Sequence validation and mutation so failure does not expose prohibited partial state.
- Repair ownership conflicts by changing topology or phases before considering Clone, RefCell, or unsafe code.

## Core model

### From variables to places

Course 1 often asks “which binding owns this value?” Advanced borrowing requires a smaller unit: a **place expression** identifies a storage location that may be projected through fields, dereferences, or indices. Examples include `record`, `record.title`, `items[index]`, and `(*pointer).field`. Moves and loans apply to places and move paths, not merely to variable names.

```rust
struct Pair {
    left: String,
    right: String,
}

let pair = Pair {
    left: String::from("L"),
    right: String::from("R"),
};
let left = pair.left;
println!("{}", pair.right);
```

`pair.left` is moved; `pair.right` remains initialized and may be used. The whole `pair` cannot be used as a complete value. A move-path trace records initialization state for the root and projections.

This distinction also explains why named struct fields can often be borrowed disjointly while two dynamic index operations cannot. The compiler knows `pair.left` and `pair.right` never overlap. It cannot infer from arbitrary runtime integers that `slice[a]` and `slice[b]` are disjoint.

### Loans over places

For each borrow, record:

```text
borrowed place:
kind: shared | exclusive
created at:
last use:
operations forbidden while active:
reborrowed through:
```

A shared loan over `document.text` need not always freeze unrelated fields, but method calls can borrow a receiver more broadly depending on the signature and compiler-visible access. API design affects the granularity of loans.

```rust
fn rename_and_count(document: &mut Document, title: String) -> usize {
    document.title = title;
    document.text.len()
}
```

This single `&mut Document` is simple but grants broad capability. If callers need simultaneous access to independent components, a split method or field-level operation may be better.

### Reborrowing and shortening

When a mutable reference is passed to a function, Rust generally creates a shorter reborrow:

```rust
fn use_twice(value: &mut String) {
    append_period(value);
    append_period(value);
}

fn append_period(value: &mut String) {
    value.push('.');
}
```

The first call does not permanently move `value`; it lends exclusive access for the call. Non-lexical lifetime analysis lets a loan end at its final use, but it does not weaken exclusivity.

Two-phase borrowing explains selected method-call patterns such as:

```rust
let mut values = vec![10, 20];
values.push(values.len());
```

The receiver's mutable borrow can be reserved, the argument evaluated with shared access, and the mutable borrow activated for the call. This is a compiler-defined behavior for particular implicit borrows, not a general mode that library authors can activate around arbitrary code.

### Split access instead of cloning

For two distinct indices:

```rust
pub fn get_two_mut<T>(
    values: &mut [T],
    first: usize,
    second: usize,
) -> Option<(&mut T, &mut T)> {
    if first == second || first >= values.len() || second >= values.len() {
        return None;
    }

    if first < second {
        let (left, right) = values.split_at_mut(second);
        Some((&mut left[first], &mut right[0]))
    } else {
        let (left, right) = values.split_at_mut(first);
        Some((&mut right[0], &mut left[second]))
    }
}
```

The split operation encodes non-overlap into two distinct slices. Validation occurs before any mutation. The function returns two simultaneous exclusive references because their places are proven disjoint.

### Failure-atomic transfer

Suppose balances move between accounts. A weak implementation debits the source, then discovers the destination is invalid or the credit overflows. A stronger sequence is:

1. validate distinct identities and bounds;
2. read enough owned/copy evidence to validate arithmetic;
3. obtain disjoint mutable access;
4. compute both next values;
5. write both values only after every fallible check passes.

```rust
pub fn transfer(
    balances: &mut [u64],
    from: usize,
    to: usize,
    amount: u64,
) -> Result<(), TransferError> {
    let (&source, &destination) = get_two(balances, from, to)?;
    let next_source = source.checked_sub(amount).ok_or(TransferError::Insufficient)?;
    let next_destination = destination.checked_add(amount).ok_or(TransferError::Overflow)?;
    let (source, destination) = get_two_mut(balances, from, to).ok_or(TransferError::InvalidIndex)?;
    *source = next_source;
    *destination = next_destination;
    Ok(())
}
```

The exact helper types can vary. The important design is phase separation: fallible validation precedes visible mutation.

### Derive it yourself

A store has `Vec<Entry>` plus a `HashMap<Key, usize>`. Implement `rename_key` without holding an immutable map lookup across a map mutation and without leaving the vector/map inconsistent on duplicate key. Write the place/loan graph first. Decide which evidence must be copied into owned small values before mutation.

### Misconception clinic

- The borrow checker does not track only identifiers; it tracks access to places and projections.
- NLL shortens loans; it does not permit conflicting aliases.
- Two-phase borrowing is narrow and implicit, not a general transaction mechanism.
- Copying a small durable index before mutation can be sounder than preserving a long borrow. “No copy” is not the goal; coherent topology is.

Basic explanations often say that Rust “borrows values.” More precise reasoning starts from *places*. A place expression identifies a location that can be read from, written to, moved from, or borrowed. Examples include:

```rust
account
account.balance
accounts[3]
*pointer
pair.0
```

The distinction matters because the compiler does not merely ask whether two references mention the same variable. It asks whether the places they cover may overlap.

### Values and places

In this assignment:

```rust
let total = account.balance;
```

`account.balance` is evaluated as a place, then its value is read. If the field is `u64`, the read copies it. If the field is `String`, the same syntax normally moves the field out of the struct.

In this borrow:

```rust
let balance = &mut account.balance;
```

no field value is moved. A mutable loan is created for the projected place `account.balance`. While that loan is active, operations that could conflict with that field are rejected.

The compiler can prove that named struct fields are disjoint:

```rust
struct Account {
    balance: i64,
    label: String,
}

let mut account = Account {
    balance: 50,
    label: String::from("reserve"),
};

let balance = &mut account.balance;
let label = &account.label;
*balance += 10;
println!("{label}: {balance}");
```

The shared borrow of `label` does not overlap the mutable borrow of `balance`. Both originate from `account`, but their projected places are distinct.

### Indexing is less transparent

The same reasoning does not automatically apply to arbitrary indexed expressions:

```rust,compile_fail
let mut balances = [10, 20];
let left = &mut balances[0];
let right = &mut balances[1];
*left += *right;
```

A human sees distinct literal indices. The indexing operation is implemented through `IndexMut`, and the compiler conservatively treats both borrows as access through the whole indexed container. The correct safe abstraction is `split_at_mut`, which proves disjointness by returning two nonoverlapping slices:

```rust
let mut balances = [10, 20];
let (left, right) = balances.split_at_mut(1);
left[0] += right[0];
```

The key lesson is not “the compiler is dumb.” The lesson is that a safe API can carry a proof that surface syntax does not.

### Loans are permissions, not hidden copies

A shared borrow grants read access while excluding mutation that could invalidate the view. A mutable borrow grants exclusive access. The owned value remains in place; the borrower receives permission constrained by type and lifetime.

This permission model explains why a reference can be small while restricting a large structure. Borrowing `&mut accounts[0]` may prevent access to the vector through its original binding even though only one element is conceptually needed. The compiler must uphold vector-level invariants such as possible reallocation and trait-defined indexing behavior.

### Projection through references

Suppose a function receives `&mut Account`:

```rust
fn credit(account: &mut Account, amount: i64) {
    account.balance += amount;
}
```

The field access is shorthand for dereferencing the reference and projecting the field. The mutable borrow of the whole account is *reborrowed* for the field operation. The original caller's access is suspended for the duration of the call but not consumed.

### A practical inspection sequence

When a conflict appears, write:

1. the base place (`accounts`);
2. every projection (`[source]`, `.balance`);
3. the loan kind;
4. the point of last use;
5. the operation that may overlap.

For this code:

```rust,compile_fail
let selected = &accounts[source];
accounts[target].balance += 10;
println!("{}", selected.label);
```

The shared loan remains active through the `println!`. The mutation through indexing may overlap the borrowed element because `source` and `target` are runtime values. A preserving repair must establish inequality and split the collection, or copy only the small information actually needed before mutation.

The correct question is not “How do I silence E0502?” It is “What disjointness fact does the product guarantee, and how can the API expose that fact?”

Rust tracks moves at finer granularity than entire variable names. A *move path* corresponds roughly to a place and its projections. This allows one field to be moved while other fields remain usable.

```rust
struct Record {
    title: String,
    priority: u8,
}

let record = Record {
    title: String::from("audit"),
    priority: 3,
};

let title = record.title;
println!("priority = {}", record.priority);
println!("title = {title}");
```

The whole `record` cannot be used after the partial move because it is not fully initialized, but the untouched `priority` field remains available.

### Destructuring makes move intent explicit

```rust
let Record { title, priority } = record;
```

Both fields are moved or copied according to their types. Pattern bindings can borrow selected fields:

```rust
let Record {
    ref title,
    priority,
} = record;

println!("{title}: {priority}");
```

Here `title` is borrowed and `priority` is copied. Understanding binding modes is essential when patterns interact with a type that implements `Drop`.

### Why `Drop` changes field moves

Safe Rust generally forbids moving a field out of a type that implements `Drop`:

```rust,compile_fail
struct Guard {
    name: String,
}

impl Drop for Guard {
    fn drop(&mut self) {
        println!("releasing {}", self.name);
    }
}

let guard = Guard { name: String::from("lease") };
let name = guard.name;
println!("{name}");
```

The destructor receives `&mut self` and is entitled to observe a valid `Guard`. If safe code could remove `name` first, `drop` would run on a partially invalid value. Course 4 will use `Option::take` and `mem::take` to move owned state out while leaving a valid replacement.

### Initialization is a control-flow fact

The compiler tracks whether a binding is definitely initialized along every path:

```rust
let message: String;
if condition() {
    message = String::from("yes");
} else {
    message = String::from("no");
}
println!("{message}");
```

If one branch does not initialize `message`, the later use is rejected. The same principle applies after conditional moves.

Internally, the compiler may use *drop flags* to remember which portions require destruction. You should understand the behavior, but not depend on a specific implementation representation. The language-level guarantee is that initialized values are dropped appropriately and moved-out values are not dropped again.

### Move is semantic; bytes may behave differently

Ownership transfer is a language event. The compiler may optimize away physical copies, or a move of `String` may copy only its small control block while leaving the heap buffer in place. Conversely, Module 20 will distinguish this semantic move from *mechanical movement* to a new address, which matters for pinning.

### Repairing partial-move designs

When code needs one owned field and later needs the whole struct, options include:

- borrow the field instead of moving it;
- destructure and use all fields separately;
- replace the field with a valid default using `mem::take`;
- store the field in `Option<T>` and call `take` to represent absence explicitly;
- redesign the method to consume the whole struct and return the pieces.

Cloning the field can be correct when the product needs two independent values. It is not the general repair for a move path you have not understood.

### Case: extracting a staged command

A parser may own both raw text and a parsed command. If execution needs to consume the command but diagnostics still need raw text, represent that directly:

```rust
struct ParsedLine {
    raw: String,
    command: Option<Command>,
}

impl ParsedLine {
    fn take_command(&mut self) -> Option<Command> {
        self.command.take()
    }
}
```

The `Option` is not a workaround. It models a state transition: the command may be present before execution and absent afterward, while `ParsedLine` remains valid and destructible.

A mutable reference is not usually “used up” when passed to another function. Rust creates a shorter *reborrow*.

```rust
fn append_mark(text: &mut String) {
    text.push('!');
}

let mut title = String::from("audit");
let access = &mut title;
append_mark(access);
access.push('?');
assert_eq!(access, "audit!?");
```

Conceptually, the call creates `&mut *access` for the duration required by `append_mark`. During that reborrow, `access` cannot be used independently. After it ends, the original exclusive reference is usable again.

### Lifetime shortening

References can often be used for less time than the lifetime appearing in their type. The compiler selects regions based on actual use. This is the practical effect associated with non-lexical lifetimes (NLL): a borrow may end at its final relevant use rather than at the closing brace of the variable's lexical scope.

```rust
let mut values = vec![1, 2, 3];
let first = &values[0];
println!("{first}"); // final use of the shared borrow
values.push(4);      // accepted
```

Adding a later use changes the region:

```rust,compile_fail
let mut values = vec![1, 2, 3];
let first = &values[0];
values.push(4);
println!("{first}");
```

The compiler is not reacting to the order of declarations alone. It must keep the loan active until the reference's last use.

### Scope remains a design tool

NLL does not make explicit scopes obsolete. Guard types such as `RefMut`, mutex guards in later courses, and custom leases are values whose `Drop` releases permission. Binding such a guard can keep runtime or compile-time access active. A small block communicates the intended release point:

```rust
{
    let item = records.get_mut(index).ok_or(Error::Missing)?;
    item.normalize();
}
records.sort_by_key(Record::priority);
```

The block prevents later refactoring from accidentally extending the borrow.

### Two-phase borrows

Some method-call patterns work because the compiler treats a mutable borrow in two phases: reservation and activation. The familiar example is:

```rust
let mut values = vec![10, 20];
values.push(values.len());
```

The mutable receiver borrow is reserved, `values.len()` performs a shared borrow to compute the argument, and the mutable borrow activates for `push` afterward.

A hand-written equivalent may fail:

```rust,compile_fail
let mut values = vec![10, 20];
let receiver = &mut values;
let length = values.len();
receiver.push(length);
```

Do not build broad design assumptions around two-phase borrow implementation details. Treat it as a language-supported ergonomic behavior for certain implicit mutable borrows. When a design is unclear, separate read and write phases explicitly.

### Reborrow versus moving the reference

Mutable references themselves are not `Copy`. In generic contexts, assignment can move one:

```rust
fn use_twice(value: &mut String) {
    let first = &mut *value;
    first.push('1');

    let second = &mut *value;
    second.push('2');
}
```

The explicit `&mut *value` requests a reborrow. Passing `value` to an ordinary function usually inserts the reborrow you intend, but explicit syntax is useful when learning or when generic moves become confusing.

### The shortest valid loan

A reliable design rule is:

> compute owned or copyable facts first, acquire the exclusive borrow as late as possible, release it as early as the invariant allows.

This reduces both compiler conflict and human uncertainty. It also prepares for `RefCell`, where holding a guard too long changes a compile-time inconvenience into a runtime panic.

Rust permits simultaneous mutable access when nonoverlap is proved. The form of the data determines which proofs are available.

### Struct fields

Named fields are statically disjoint:

```rust
struct Ledger {
    debit_total: i64,
    credit_total: i64,
}

fn post(ledger: &mut Ledger, amount: i64) {
    let debits = &mut ledger.debit_total;
    let credits = &mut ledger.credit_total;
    *debits += amount;
    *credits += amount;
}
```

This works because both projections are known and nonoverlapping.

A method can make the proof reusable:

```rust
impl Ledger {
    fn totals_mut(&mut self) -> (&mut i64, &mut i64) {
        (&mut self.debit_total, &mut self.credit_total)
    }
}
```

The method's safe implementation is itself the proof boundary. Callers cannot accidentally receive two references to the same field.

### Slices

For runtime indices, split around one index and select from opposite halves:

```rust
fn two_mut<T>(slice: &mut [T], a: usize, b: usize) -> Option<(&mut T, &mut T)> {
    if a == b || a >= slice.len() || b >= slice.len() {
        return None;
    }

    if a < b {
        let (left, right) = slice.split_at_mut(b);
        Some((&mut left[a], &mut right[0]))
    } else {
        let (left, right) = slice.split_at_mut(a);
        Some((&mut right[0], &mut left[b]))
    }
}
```

The order of returned references follows the requested `a, b`, not the lower/higher index order. That detail belongs to the product contract and must be tested.

### Collections with stronger APIs

Some containers offer entry or multi-access APIs that encode disjointness. Prefer those over extracting raw references through repeated lookup. For a `HashMap`, the entry API can combine lookup and mutation without repeating a hash or holding a separate reference:

```rust
use std::collections::HashMap;

fn increment(counts: &mut HashMap<String, u64>, key: String) {
    *counts.entry(key).or_insert(0) += 1;
}
```

When a standard API does not express the required simultaneous access, consider a staged operation: remove one value, mutate the other, then reinsert with rollback on error. The design must preserve state if any step fails.

### Splitting `self`

A common conflict occurs when one method borrows a field and then calls another method requiring `&mut self`:

```rust,compile_fail
struct Engine {
    queue: Vec<Job>,
    completed: Vec<Job>,
}

impl Engine {
    fn process_first(&mut self) {
        let job = self.queue.first_mut().unwrap();
        self.record_completion(job);
    }

    fn record_completion(&mut self, job: &Job) {
        // ...
    }
}
```

The second method claims authority over the entire engine, including the already-borrowed queue. Repairs include:

- make `record_completion` accept only `&mut Vec<Job>` and the data it needs;
- move the job out of the queue before calling;
- split fields into locals: `let Self { queue, completed } = self;`;
- calculate an owned completion record, end the first borrow, then mutate the second field.

Changing a helper from `&mut self` to a field-level parameter is often not “less object-oriented.” It is a more accurate capability boundary.

### Unsafe is not required for common splitting

Rust's standard library implements splitting abstractions using unsafe internals, but users should prefer their safe contracts. Writing pointer arithmetic because the compiler cannot prove indexed disjointness is Course 6 work and requires a soundness argument far beyond “the indices are different.”

Many borrow conflicts are symptoms of an operation that mixes discovery, validation, mutation, and publication in one scope. Separating phases often improves both proof and product behavior.

### Four phases

A robust mutation can be organized as:

1. **discover** — find indices, IDs, or keys using shared access;
2. **validate** — compute all conditions that can fail without changing state;
3. **mutate** — acquire the narrowest exclusive access and perform an infallible core change;
4. **publish** — release internal borrows, then notify observers or format results.

Example transfer:

```rust
fn transfer(accounts: &mut [Account], from: usize, to: usize, amount: u64) -> Result<(), Error> {
    if from == to {
        return Err(Error::SameAccount);
    }
    if amount == 0 {
        return Err(Error::ZeroAmount);
    }

    let source_balance = accounts.get(from).ok_or(Error::MissingSource)?.balance;
    accounts.get(to).ok_or(Error::MissingTarget)?;
    if source_balance < amount {
        return Err(Error::InsufficientFunds);
    }

    let (source, target) = two_mut(accounts, from, to).ok_or(Error::InvalidPair)?;
    source.balance -= amount;
    target.balance += amount;
    Ok(())
}
```

All expected failures occur before mutation. After the two mutable references are acquired, the arithmetic must be valid. Checked arithmetic may be part of validation if overflow is possible.

### Borrow scopes reveal transactional boundaries

A borrow is not a transaction, but its scope can define the region in which an invariant is temporarily broken. If two fields must change together, keep both mutable references in one small block and restore the invariant before they end.

```rust
{
    let (source, target) = two_mut(accounts, from, to).ok_or(Error::InvalidPair)?;
    source.balance -= amount;
    target.balance += amount;
}
// total balance invariant restored here
```

### Callbacks are publication boundaries

Do not invoke arbitrary callbacks while a mutable borrow or `RefMut` guard is active unless reentrancy is explicitly supported. A callback may try to inspect or mutate the same object, create a runtime borrow panic, or observe an intermediate invariant.

Prefer:

```rust
let event = {
    let account = accounts.get_mut(index).ok_or(Error::Missing)?;
    account.balance += amount;
    Event::Credited { index, amount, balance: account.balance }
};
observer(event);
```

The borrow ends before publication.

### Remove–modify–reinsert

For maps, ownership can replace a difficult mutable borrow:

```rust
let mut source = accounts.remove(&from).ok_or(Error::MissingSource)?;
let result = (|| {
    let target = accounts.get_mut(&to).ok_or(Error::MissingTarget)?;
    // validate and mutate
    Ok(())
})();
accounts.insert(from, source);
result
```

This sketch is incomplete if target mutation can occur before a later failure. A proper design must validate first or use a rollback guard. The important point is that moving a value out can establish exclusive ownership, but it introduces restoration obligations.

### Invariants before ergonomics

Do not select a borrow repair solely because it compiles. Evaluate:

- can any error leave partial state;
- can a callback observe an intermediate state;
- does the repair allocate or clone unnecessarily;
- does it widen mutation authority;
- is the invariant visible in tests and API shape?

The borrow checker prevents aliasing violations. It does not automatically prove domain atomicity.

Method receivers are capability declarations.

- `self` consumes the value and may dismantle it;
- `&self` permits observation and methods backed by interior mutability;
- `&mut self` permits exclusive mutation of the whole reachable value;
- explicit receivers such as `self: Box<Self>` or `self: Rc<Self>` describe ownership through a pointer and appear in later designs.

### Avoid whole-object authority by habit

A helper that requires only one field should not automatically take `&mut self`:

```rust
fn normalize_titles(titles: &mut [String]) {
    for title in titles {
        title.make_ascii_lowercase();
    }
}
```

Calling a field-level function allows other disjoint fields to remain borrowed. It also makes testing and reuse clearer.

### Return values can end borrows

Instead of mutating two fields through nested method calls, compute a value from one and apply it to another:

```rust
impl Workspace {
    fn rebuild_summary(&mut self) {
        let summary = compute_summary(&self.documents);
        self.summary = summary;
    }
}
```

The shared borrow used by `compute_summary` ends before assignment. A method returning an owned summary often produces a cleaner phase boundary than a helper taking `&mut Workspace`.

### Borrowed return ties up authority

This method returns a borrow from `self`:

```rust
fn selected(&self) -> Option<&Document> {
    self.documents.get(self.selected_index?)
}
```

As long as the result is live, mutation of the workspace may be restricted. That is correct: mutation could invalidate the returned view. If callers need both the selected information and later mutation, consider returning a stable ID or a copied small field rather than an owned clone of the whole document.

### Consume to transition ownership

Builders and state transitions can consume `self`:

```rust
impl Draft {
    fn publish(self) -> Published {
        Published {
            title: self.title,
            body: self.body,
        }
    }
}
```

Consumption proves the draft cannot be used after publication and permits field moves without cloning.

### Explicit lifetimes are not always more precise

Do not add names unless the relationship requires them:

```rust
fn title(&self) -> &str
```

Elision correctly ties the output to `self`. Writing `fn title<'a>(&'a self) -> &'a str` is equivalent but noisier. Module 12 will derive when multiple inputs or reference-bearing types require explicit relationships.

### Signature review questions

For each parameter, ask:

1. Must the function destroy or retain this value?
2. Must it mutate the value or only inspect it?
3. Does the output borrow from this input?
4. Does the caller need the input afterward?
5. Would an ID or small copied fact free the caller from a long borrow?
6. Is a whole-object receiver hiding disjoint field access?

A good signature is a proof surface. It exposes enough authority for the operation and no more.

Cloning is neither forbidden nor free. The problem is using it before understanding what relationship the code should have.

### Four meanings of clone

A clone can represent:

1. a genuine second value required by the domain;
2. a snapshot isolated from future mutation;
3. another `Rc` owner of the same allocation;
4. an accidental workaround for an unresolved borrow.

Only the fourth is inherently suspect, but it is common in early Rust code.

### Diagnosis sequence

When `.clone()` appears near a borrow error:

#### 1. Identify what is duplicated

Cloning a `String` duplicates its heap buffer. Cloning an `Rc<T>` duplicates only the counted handle and extends liveness. Cloning a `Copy` type is usually just a copy with noisier intent.

#### 2. Identify the desired postcondition

Does the caller need two independent strings, or one string and a temporary view? Does the data need to outlive its original owner, or only the current statement?

#### 3. Try structural repairs

- borrow a field rather than the whole value;
- return a reference tied to an owner;
- calculate before mutating;
- use a stable ID;
- split the collection;
- move the whole value and return it;
- store optional state and `take` it.

#### 4. Reintroduce clone with a semantic name

If duplication is required, make it visible:

```rust
let snapshot_title = document.title.clone();
```

The name communicates that a second owned value is intentional.

### Example: event publication

Weak design:

```rust
let document = &mut workspace.documents[index];
document.title.push('!');
notify(document.clone());
```

The clone may duplicate a large body merely because the mutable borrow is inconvenient. Better:

```rust
let event = {
    let document = &mut workspace.documents[index];
    document.title.push('!');
    Event::Renamed {
        id: document.id,
        title: document.title.clone(),
    }
};
notify(event);
```

Now the clone is limited to the event's owned title because the event must outlive the borrow. An even better domain may let `Event` use `Rc<str>` or a stable ID, but that is a topology decision considered later.

### Clone budget

For every lab and capstone module, maintain a short clone audit:

- source line;
- type cloned;
- allocation behavior;
- semantic reason;
- alternative considered.

The goal is not zero clones. The goal is zero unexplained clones.

A booking service owns a `Vec<Seat>`. Each seat contains a passenger name, a class, and an optional reservation token. The operation `move_reservation(from, to)` must transfer one token from an occupied source to an unoccupied target while preserving both passenger records.

The direct implementation borrows two indexed elements and is rejected. Before changing code, state the product conditions:

```text
from and to are in range
from != to
source has a token
target has no token
no state changes on failure
on success, exactly one token changes owner
```

### Phase 1 — validate without durable mutable loans

Bounds and equality can be checked from lengths/indices. Occupancy facts can be inspected through short shared borrows:

```rust
let source_has_token = seats.get(from).and_then(|s| s.token.as_ref()).is_some();
let target_is_empty = seats.get(to).is_some_and(|s| s.token.is_none());
```

Do not retain `&Seat` variables through the mutation phase. Copy Boolean facts or return typed errors immediately.

### Phase 2 — obtain disjoint mutable places

Order indices and split at the larger:

```rust
let (source, target) = if from < to {
    let (left, right) = seats.split_at_mut(to);
    (&mut left[from], &mut right[0])
} else {
    let (left, right) = seats.split_at_mut(from);
    (&mut right[0], &mut left[to])
};
```

The tuple preserves semantic source/target order even though the physical split order changes. The proof is structural: the returned slices do not overlap.

### Phase 3 — move, do not clone

The token has one owner. Transfer it with `Option::take`:

```rust
let token = source.token.take().ok_or(Error::SourceVacant)?;
target.token = Some(token);
```

Because earlier validation established both conditions, `take` should succeed. For defense in depth, do not use `unwrap` in production code. More importantly, ask whether any operation after `take` can fail. Assignment to an already validated `Option` is infallible. Logging that can allocate or fail must be prepared first.

### Partial-move variant

Suppose `Seat` itself is removed from the vector and its token moved out. If `Seat` implements `Drop`, moving its token field directly is restricted. Keeping the field as `Option<Token>` and taking it leaves a complete destructible `Seat`.

### Receiver design

A method `SeatMap::move_reservation(&mut self, ...)` is correct because the operation may mutate two internal seats and must serialize against other map access. Returning `(&mut Seat, &mut Seat)` publicly would expose more mutation authority than needed. Keep the splitting proof internal and expose a domain transition.

### Review conclusion

The borrow checker did not obstruct a known-safe operation. It required the program to represent the missing facts: non-aliasing, phase separation, and a single infallible ownership transfer.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Represent workspace slots with generational handles and keep mutable access narrower than the whole workspace. Stale identity and current ownership are separate concerns. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-01-borrow-surgery/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 12 when you can:

- answer the module question—“Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Place expressions](https://doc.rust-lang.org/reference/expressions.html#place-expressions-and-value-expressions)
- [Rust Reference: Borrow expressions](https://doc.rust-lang.org/reference/expressions/operator-expr.html#borrow-operators)

[← Module 10](../../../01-rust-foundations/course-book/module-10-integration-and-independent-change/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 12 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md)

## Continue

1. Complete the [Module 11 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 11 — Borrow Surgery](../../labs/module-01-borrow-surgery/README.md) from its public contract.
3. Apply the Module 11 increment in the [Memory Workspace engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
