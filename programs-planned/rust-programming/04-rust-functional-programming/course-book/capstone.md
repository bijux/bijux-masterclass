# LedgerFlow — Course 4 capstone

The capstone supports the course-book. It exists to force cross-layer transfer after each mechanism has been understood in isolation.

## Product

**LedgerFlow** is a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports.

## Ten increments

1. **Module 31:** Define LedgerFlow callbacks for filtering, mapping, and policy decisions with the weakest callable capability that matches actual invocation and capture behavior.
2. **Module 32:** Expose lazy borrowed event queries and trace when parsing, filtering, and inspection actually occur. Avoid collecting merely to make a borrow problem disappear.
3. **Module 33:** Build the ordered event-shaping pipeline and document each stage's item type, cardinality, order, borrowing, and allocation behavior.
4. **Module 34:** Reduce valid events into ledger state with an explicit prefix invariant and short-circuit on fatal violations without leaving partial mutation.
5. **Module 35:** Separate row-local diagnostics, fatal stream failures, warnings, and duplicate policy. Preserve physical source order when diagnostics from multiple phases are combined.
6. **Module 36:** Implement domain traversal for accounts or audit history where a named iterator clarifies state and exhaustion better than another anonymous chain.
7. **Module 37:** Retain persistent audit versions through structural sharing and prove which nodes are rebuilt after an update. State the memory cost without claiming zero-copy magic.
8. **Module 38:** Move filesystem and terminal operations into an effect shell around a deterministic analysis core. Represent intended effects as data where that improves testing.
9. **Module 39:** Review reusable LedgerFlow combinators with laws and counterexamples for order, identity, error propagation, and duplication. Attach honest operation-count claims.
10. **Module 40:** Add an unseen cross-cutting analysis or reporting requirement while preserving deterministic output, audit history, and explicit failure. Defend the revised dataflow end to end.

## How to use the capstone

Do not read the finished implementation before attempting an increment. Begin with the public behavior, write the failure-path test, identify the types whose invariants change, and then implement the smallest coherent change. After the change passes, inspect the finished code to compare architecture rather than copy syntax.

## 1. Product contract

LedgerFlow reads one append-only event source and produces deterministic analysis. It is a batch analyzer, not a database, transaction processor, or accounting standard.

### User-visible capabilities

The CLI must support:

```text
ledgerflow check <events.tsv>
ledgerflow summary <events.tsv>
ledgerflow account <events.tsv> <account-id>
ledgerflow events <events.tsv> [account-id]
ledgerflow demo
ledgerflow help
ledgerflow version
```

`check` renders diagnostics and a summary. `summary` renders aggregate and per-account state. `account` renders one account plus its accepted-event timeline. `events` renders accepted events, optionally filtered by account. All reports are stable for the same input and program version.

### Domain rules

An account begins absent. Legal accepted transitions are:

```text
absent --open(0)----------------------> open(balance = 0)
open(b) --deposit(n > 0)--------------> open(b + n)
open(b) --withdraw(0 < n <= b)--------> open(b - n)
open(0) --close(0)--------------------> closed(balance = 0)
```

Every other transition is rejected. Rejection must preserve the ledger produced by the preceding accepted prefix.

The amount is an integer number of cents. Course 4 deliberately avoids floating-point money and avoids currency conversion. Those choices remove unrelated ambiguity; they are not a complete monetary model.

### Analysis policy

LedgerFlow is neither purely fail-fast nor blindly permissive.

- An unsupported header stops row decoding because the format is untrusted.
- Within a correctly identified source, independent row errors accumulate.
- A row with multiple independently invalid fields reports each field error in field order.
- A syntactically valid row may carry normalization warnings.
- Duplicate IDs are rejected before state transition.
- A state-transition error rejects only that event; later events continue from the unchanged prior ledger.
- Reports may contain accepted partial state and diagnostics together.

This policy is product behavior. It is not an implementation convenience.

### Non-goals

LedgerFlow does not provide:

- concurrency or parallel reduction;
- asynchronous I/O;
- persistence beyond reading one source;
- cryptographic integrity;
- decimal currencies or exchange rates;
- multi-file ordering;
- rollback of external effects;
- unbounded streaming with constant retained memory;
- performance claims without measurement.

These exclusions protect the course boundary. Parallelism belongs to Course 7, async I/O to Course 8, and measured production engineering to Course 9.

### Acceptance examples

A valid open/deposit/withdraw/close sequence produces a closed zero-balance account and exit class `0`. An insufficient withdrawal produces diagnostic `LF014`, leaves the preceding balance unchanged, permits later valid events, and produces exit class `1`. A missing file prevents analysis and produces exit class `2` on stderr.

The important distinction is between **data failure** and **command failure**. The former is a successful analysis that found invalid input; the latter means the requested operation could not be performed.

## 2. Input grammar and source positions

A transformation pipeline cannot be more precise than its input contract. Do not begin with `split` calls. Begin with the grammar and the treatment of physical source positions.

### Grammar

```text
source      = header, newline, { ignored | event-line } ;
header      = "LEDGERFLOW-V1" ;
ignored     = blank-line | comment-line ;
comment-line= optional-space, "#", { any-character } ;
event-line  = event-id, TAB, account-id, TAB, kind, TAB, amount, TAB, note ;
kind        = "open" | "deposit" | "withdraw" | "close" ;
event-id    = nonzero unsigned decimal integer ;
amount      = signed decimal integer fitting i64 ;
```

The note occupies exactly one field. Embedded tabs are therefore not supported. Empty notes are allowed and normalize to `None`.

### Physical lines are evidence

Diagnostics refer to physical lines in the original source. Ignoring an empty or comment line must not renumber later events. This rules out an early pipeline such as:

```rust
input.lines().filter(|line| !line.trim().is_empty()).enumerate()
```

Here `enumerate` describes filtered-record position, not source line. Enumerate first, then filter:

```rust
input
    .lines()
    .enumerate()
    .filter_map(|(index, line)| {
        let physical_line = index + 1;
        // decide whether to inspect the line
    })
```

The order of adapters is part of correctness.

### Header trust boundary

A missing or unsupported header prevents row decoding. It would be easy to continue and report additional tab-shape problems, but those diagnostics would pretend that an unknown format obeyed the Course 4 grammar. Stopping at this boundary is not ordinary fail-fast parsing; it is a trust decision.

### Normalization contract

Surrounding whitespace in fields is removed. The parser emits `LF101` warnings so normalization is observable. It does not lowercase account IDs because case sensitivity is part of identity. Event kinds are matched case-insensitively after trimming because the grammar treats them as controlled keywords.

Normalization must be idempotent:

```text
normalize(normalize(x)) = normalize(x)
```

for the supported fields. The test suite should state this law over a representative domain and should include tabs/newlines as rejected account characters.

### Row shape before field parsing

Exactly five fields are required. If field count is wrong, field positions are not trustworthy, so the row produces one shape diagnostic rather than speculative field diagnostics.

When shape is valid, ID, account, kind, and amount are independent. Parse all four and accumulate their errors in schema order. This makes a malformed row maximally useful without pretending that dependent semantic checks can run.

### Design exercise

Before implementing `inspect_row`, write a table with these columns:

| Field | Normalization | Parse result | Independent? | Diagnostic code |
|---|---|---|---|---|

Then construct one row that produces four errors and one row that produces five warnings but remains accepted. If your types cannot express both outcomes, the parser result shape is incomplete.

## 3. Four-flow transformation map

LedgerFlow should be understandable before any method chain is written. The transformation map records four separate flows.

### Data flow

```text
UTF-8 source text
    -> header decision
    -> physical rows
    -> row inspections
    -> syntactically valid events
    -> identity screening
    -> state transitions
    -> accepted events + final ledger + audit trail
    -> lazy queries
    -> report values
    -> rendered text
```

### Ownership flow

- The CLI owns the input `String`.
- Parsing creates owned `Event` values because accepted events outlive line-local split slices and are retained for queries.
- `AccountId` and notes own normalized text.
- The ledger owns account keys and state.
- Queries borrow `Analysis`; they do not clone events or accounts.
- Audit versions share prior nodes through `Rc`.
- Rendering owns its final `String` but borrows all model values while constructing it.

A zero-copy row parser would be possible, but it would attach the lifetime of all events to the source buffer and complicate retained analysis. That is an explicit rejected trade-off, not an oversight.

### Failure flow

```text
header error --------------------------> stop row decoding
field-shape error ---------------------> reject one row
independent field errors --------------> accumulate for one row
normalization warning -----------------> retain event + warning
duplicate event id --------------------> reject event, retain prior state
state-transition error ----------------> reject event, recover prior ledger
query target missing -----------------> command failure
filesystem read error ----------------> shell failure
```

Failure is not one `Result` from beginning to end. Different stages require different traversal policies.

### Effect flow

The core receives text and returns values. It does not:

- read files;
- inspect environment variables;
- print;
- set process exit status;
- obtain time or randomness;
- mutate global state.

The binary shell performs argument collection, file reading, output, and exit conversion. The pure core still uses local mutation internally for efficient accumulation; effect isolation is about observable interactions, not a ban on `mut`.

### Stage contract table

Every major stage should be recorded with this schema:

| Stage | Input | Output | Ownership | Cardinality | Order | Failure | Effects |
|---|---|---|---|---|---|---|---|
| inspect source | `&str` | `SourceInspection` | borrows then allocates events | 1 to rows | physical | header/row diagnostics | none |
| analyze rows | row outcomes | `Analysis` | consumes outcomes | many to one | source | duplicate/transition diagnostics | none |
| account query | `&Analysis`, `&AccountId` | iterator of `&Event` | borrowed | filter | source | none | lazy, none |
| render | `&Analysis` | `String` | borrowed to owned text | many to one | deterministic | query overflow rendered | allocation only |

Allocation is not an external effect, but it belongs in the cost model.

### Review test

Hand this map to a reader who has not seen the implementation. They should be able to answer:

1. Why are events owned?
2. Which failures permit later rows?
3. Why is account iteration deterministic?
4. Which operations happen only when a query is consumed?
5. Where can process exit status change?

If those answers require opening source files, the architecture is not yet explicit enough.

## 4. Parsing and diagnostic topology

The parser’s central type is not `Result<Event, Error>`. That shape can express one accepted event or one rejection, but it cannot express an accepted event with warnings or a rejected row with several independent field errors.

LedgerFlow uses a row outcome equivalent to:

```rust
pub enum RowInspection {
    Accepted {
        event: Event,
        warnings: Vec<Diagnostic>,
    },
    Rejected(Vec<Diagnostic>),
}
```

This is a product-specific algebraic data type. It names the valid combinations and excludes nonsense such as an accepted row with no event.

### Why not `Vec<Result<Field, Diagnostic>>` as the public result?

That representation is useful inside field parsing, but it exposes an intermediate schema and asks every caller to reconstruct event validity. `inspect_row` should finish that responsibility and return one domain-level outcome.

### Independent and dependent validation

ID, account, kind, and integer amount parsing are independent after field count succeeds. Account-transition legality is dependent on the preceding ledger prefix. Mixing those stages causes two problems:

- parser tests need a ledger fixture;
- syntactic events cannot be reused for other analysis.

Keep row decoding and state reduction separate.

### Diagnostic order

LedgerFlow promises deterministic diagnostic order:

1. header diagnostic, if any;
2. source rows in physical order;
3. within one malformed row, schema-field order;
4. warnings before duplicate or transition errors for the same accepted row.

The order is visible behavior. A `HashMap` keyed by field name is therefore unsuitable for accumulation unless results are explicitly reordered.

### Typed diagnostics

A diagnostic contains:

- physical line;
- severity;
- stable code;
- a typed `DiagnosticKind` with structured context.

The renderer creates text at the final boundary. Earlier stages can still match `DiagnosticKind::InsufficientFunds` or inspect the first duplicate line. Stringifying at the parse site would destroy that capability.

### Fail-fast traversal still matters

The capstone accumulates source diagnostics, but the course must also prove fail-fast comprehension. `collect::<Result<Vec<_>, _>>()` remains appropriate when no useful output exists after the first error. LedgerFlow chooses accumulation because independent rows are valuable, not because accumulation is universally superior.

### Testing the topology

At minimum, include:

- empty input;
- unsupported header plus apparently valid rows, proving rows are not decoded;
- wrong field count;
- one row with four independent parse errors;
- accepted row with normalization warnings;
- blank and comment lines preserving later physical positions;
- diagnostics from multiple rows in deterministic order.

Do not assert only the number of diagnostics. Assert kind, line, severity, and order.

### Repair exercise

A proposed parser is:

```rust
input.lines()
    .skip(1)
    .filter(|line| !line.trim().is_empty())
    .map(parse_line)
    .collect::<Result<Vec<_>, _>>()
```

List every product contract it violates. Then decide whether each repair changes adapter order, result shape, ownership, or stage boundary. This exercise matters more than replacing the code mechanically.

## 5. Identity and duplicate policy

An event ID is not merely another parsed integer. It defines identity across the source, so duplicate handling needs a documented policy.

LedgerFlow reserves an ID as soon as a row is syntactically valid and reaches identity screening. It does so before attempting the account transition.

### Consequence

Given:

```text
1\ta\tdeposit\t5\taccount missing
1\ta\topen\t0\tsecond use
```

The first event is rejected because account `a` is absent. The second is rejected as a duplicate because ID `1` was already declared on the first syntactically valid event.

Another reasonable product could reserve IDs only for accepted transitions. That is not LedgerFlow’s rule. The course requires you to recognize both as coherent and to test the selected one.

### Why the order matters

These two pipelines are not equivalent:

```text
parse -> deduplicate -> reduce
parse -> reduce -> deduplicate accepted events
```

The second allows a rejected event’s ID to be reused and can also perform state work before discovering a duplicate. Adapter and stage order encode policy.

### State needed by the stage

Use a map from `EventId` to first physical line, not only a set. The duplicate diagnostic must cite both the duplicate line and the first declaration.

A `BTreeMap` is selected for predictable behavior and easy inspection. LedgerFlow does not iterate the map for user output, so a `HashMap` would also be semantically valid if only lookup mattered. The data structure choice should follow required operations, not a blanket determinism slogan.

### First-occurrence stability

The accepted-event vector preserves source order. Deduplication must therefore retain the first declaration and reject later declarations. Sorting before deduplication would change which event wins.

### Closure design

A generic `retain_first_by` helper can be useful, but LedgerFlow also needs duplicate diagnostics with first-line context. A Boolean filter closure would hide the rejected event and make diagnostic production awkward. A named fold stage with explicit state is clearer.

### Tests

Test all four distinctions:

1. duplicate after an accepted event;
2. duplicate after a transition-rejected event;
3. same account with different IDs is not duplicate identity;
4. malformed IDs do not reserve any identity because no `EventId` exists.

Also prove that duplicate rejection leaves the ledger unchanged and that later unique events continue.

### Defense question

Why is deduplication not part of `EventId::from_str`? Because parsing one token cannot know source-wide identity history. The type guarantees local validity—nonzero `u64`—while the analysis stage enforces stream uniqueness.

## 6. Ledger reducer and prefix invariant

The ledger is produced by reducing syntactically valid, unique events in source order. The accumulator is not “some map.” It has a prefix invariant.

### Prefix invariant

After processing the first `k` row outcomes:

1. every account in the ledger was created by one accepted `open` event in that prefix;
2. every stored balance is the exact checked result of accepted deposits and withdrawals for that account;
3. no closed account has a nonzero balance;
4. every event in `accepted` was applied exactly once in source order;
5. every rejected event left the ledger equal to the state after the preceding accepted event;
6. the audit trail contains one disposition for every inspected non-header row outcome.

A correct fold step must preserve all six statements.

### Failure-atomic ownership shape

An ordinary method:

```rust
fn apply(&mut self, event: &Event) -> Result<(), Diagnostic>
```

can be correct, but the caller must trust that no mutation occurred before failure. LedgerFlow makes recovery explicit by consuming the accumulator:

```rust
fn apply(self, event: &Event) -> Result<Self, TransitionFailure>
```

`TransitionFailure` returns both the unchanged ledger and the diagnostic. The implementation first plans the mutation from shared access, then applies only a successful plan. This is a two-phase value transition:

```text
validate and compute mutation -> commit mutation
```

It is not an external transaction and does not require a rollback log.

### Planning variants

The internal mutation plan has three shapes:

```text
Insert account
Set balance to computed value
Close account
```

All arithmetic and state checks happen before the mutable update. This keeps the commit phase infallible under the established private invariants.

### Why not clone the entire ledger for every event?

`fn transition(&self) -> Result<Self, _>` could clone the map and update the clone. That yields simple failure atomicity but introduces an avoidable full-map clone per accepted event. The consuming design reuses the owned accumulator and returns it on failure.

### Why a loop may be clearer than `try_fold`

The analysis policy continues after transition errors. `try_fold` is designed to short-circuit on residual failure. Encoding “recover state and continue while emitting a diagnostic” into nested residual types is possible but obscures the invariant. A direct loop or ordinary `fold` over an explicit accumulator is better.

Functional Rust is not measured by adapter density. The reducer is functional because each prefix has a defined value and failure preserves the previous value, even though the implementation mutates owned local state.

### Proof cases

- open an absent account;
- reject a second open;
- reject a transfer with nonpositive amount;
- reject transfer before open;
- reject transfer after close;
- reject insufficient withdrawal;
- reject close with nonzero balance;
- reject lifecycle event with nonzero amount;
- reject checked-add overflow;
- accept a later event after each recoverable rejection.

The most important test is not that a diagnostic appears. It is that the following accepted event observes the unchanged correct balance.

## 7. Persistent audit trail

The final analysis retains an audit disposition for every inspected row outcome. Course 4 uses this requirement to practice persistent structural transformation.

### Representation

```text
AuditTrail -> Rc<Node newest>
Node {
    entry,
    previous: Rc<Node>?,
    len,
}
```

`push` allocates one new node and points it at the prior head. The old `AuditTrail` remains valid. The suffix is shared.

This is a persistent stack, not a general immutable sequence. Its strengths are cheap prepend, cheap snapshot, and simple sharing. Its natural iteration order is newest-first.

### Chronological presentation

User reports need source order. The implementation traverses newest-first into a vector and reverses the vector. That materialization is explicit. Claiming that the persistent structure provides cheap chronological iteration would be false.

### Why keep `len` in each node?

The cached length makes `len` and exact iterator size constant-time. The invariant is:

```text
node.len = 1 + previous.len
```

Because nodes are immutable after construction, the cached value cannot become stale through public operations.

### Sharing proof

Value equality does not prove structural sharing. A unit test should compare node identity along the new trail’s tail. The implementation keeps this helper private to tests so pointer identity does not become part of the public API.

### What the audit stores

An audit entry contains:

- source line;
- optional event ID;
- optional account ID;
- accepted or rejected disposition;
- optional stable diagnostic code.

Malformed rows may have no valid event identity. Rejected state transitions do.

### Cost model

For `n` inspected rows:

- one node allocation per row outcome;
- `O(1)` push;
- `O(1)` snapshot clone through `Rc`;
- `O(n)` newest-first traversal;
- `O(n)` extra references for chronological materialization;
- shared tail retention keeps older entries alive while any version references them.

This is an analytical model, not a benchmark result.

### Persistent-history alternatives

A `Vec<AuditEntry>` is simpler and likely preferable if no historical versions must survive. Cloning the vector after each event would be quadratic in copied elements. A tree is unnecessary because the history has one predecessor per version. `Arc` is unnecessary because Course 4 is single-threaded; Course 7 will revisit thread-safe sharing.

### Transfer task

Add an operation that returns the audit trail at the last accepted event before a given physical line without exposing internal nodes. State whether it can be implemented from the retained final trail alone and what its complexity is.

## 8. Lazy borrowed query surface

Analysis retains accepted events and final account state. Queries should borrow those values and defer work until consumed.

### Account events

```rust
pub fn events_for_account<'a>(
    analysis: &'a Analysis,
    account: &'a AccountId,
) -> impl Iterator<Item = &'a Event> + 'a
```

The iterator filters in source order. It neither clones events nor allocates a result vector. A caller that needs storage can collect explicitly.

The shared lifetime in this signature is conservative: both inputs must live for the returned iterator. An alternative can use separate lifetimes with the returned lifetime bounded by both. Course 2 gives the tools to review that refinement; Course 4’s central issue is that the lazy closure captures the account reference.

### Timeline as `scan`

An account timeline is a stateful view over accepted events. `scan` carries the running balance and yields a `TimelinePoint` after each event. The output borrows the event and owns the derived balance.

`scan` is appropriate because every input may produce one output while updating hidden iterator state. A final `fold` would lose intermediate points. A mutable vector in a loop would work but would force eager materialization.

### Unexpected overflow channel

Accepted events have already passed checked ledger arithmetic, so timeline overflow should be unreachable if the analysis invariants hold. The query still returns `Result<TimelinePoint, TimelineOverflow>` rather than panicking. This turns an invariant breach into inspectable evidence.

Do not misread this as proof that every logically unreachable state needs a public error. Here the query reconstructs arithmetic independently, so preserving a failure channel is inexpensive and reviewable.

### Consumption boundaries

These operations have different costs:

```rust
query.take(1).next()      // pulls at most enough source items for one match
query.count()             // consumes the entire remaining query
query.collect::<Vec<_>>() // consumes and allocates retained references
```

The API documentation must not say merely “returns matching events.” It should say that traversal is lazy, source order is preserved, and results borrow the analysis.

### Query laws

For a fixed, effect-free analysis:

- filtering by account twice is idempotent;
- collecting the same fresh query twice yields equal references in equal order;
- `events_for_account(a).count()` equals the account’s accepted-event count;
- a timeline’s final balance equals stored final balance for an open or closed account.

The third law includes the open event; define accepted-event count consistently.

### Do not hide policy in a predicate

A generic predicate query is useful, but named domain queries communicate stable semantics. Exposing only `query(|event| ...)` forces each caller to rediscover account comparison and order guarantees. Provide a small domain surface and keep generic combinators for genuine extension points.

## 9. Functional core and imperative shell

LedgerFlow’s core is deterministic with respect to its explicit inputs. That does not mean every function is mathematically pure or that allocation is absent. It means repeated evaluation with equal explicit inputs produces equal domain outputs and does not interact with the external world.

### Core boundary

The core owns:

- argument-shape parsing independent of process globals;
- source inspection from `&str`;
- duplicate and transition analysis;
- lazy model queries;
- report construction;
- mapping data diagnostics to exit class.

The shell owns:

- `std::env::args`;
- `std::fs::read_to_string`;
- stdout and stderr writes;
- process exit conversion.

### Why `parse_args` is in the core

Collecting process arguments is an effect. Interpreting an already supplied iterator of strings is a deterministic transformation. Separating them allows direct tests of usage behavior without spawning a process. Process tests still verify the real binary boundary.

### Effect plan alternative

A larger system might have the core return:

```text
ReadFile(path)
WriteStdout(text)
WriteStderr(text)
Exit(code)
```

and a shell interpreter execute the plan. LedgerFlow uses a smaller split: the binary reads one file and passes its contents into `execute_text`. This is sufficient because there is no sequence of conditional external operations to inspect or replay.

Do not introduce an effect-plan abstraction merely because Module 38 teaches it. Abstraction is justified by product pressure.

### Error writes are effects too

A common partial split keeps successful output pure but prints errors deep inside parsing. That makes tests capture stderr and couples parsing to a CLI. Diagnostics remain values until `main` decides where to write.

### Output failure

Writing to a closed pipe can fail. The shell checks stdout and stderr write results and uses exit class `2` if output cannot be completed. The core cannot model this from source text alone.

### Determinism assumptions

The core does not use:

- current time;
- randomness;
- environment variables;
- unordered iteration for rendered data;
- locale-dependent formatting;
- global mutable state.

Integer parsing and ASCII event-kind normalization are stable under the Rust standard-library contracts used by the course.

### Test layers

- Core unit tests call `inspect_row`, `Ledger::apply`, queries, and renderers directly.
- Public integration tests use only exported library APIs.
- Process tests execute the compiled binary, create temporary fixture files, and inspect stdout, stderr, and exit status.

A process test is not a substitute for core tests; it is evidence for the shell wiring.

## 10. Deterministic report contract

Reports are part of the product interface. “Human-readable” does not mean unspecified.

### Stable ordering

- accepted events remain in source order;
- diagnostics remain in source and within-row schema order;
- account summaries use lexical `AccountId` order through `BTreeMap`;
- timeline points follow accepted source order for one account;
- audit chronology is explicitly reversed from persistent-stack order.

Changing any of these orders is a behavior change, even if the same set of facts appears.

### Summary schema

The summary contains one tab-separated key per line:

```text
LEDGERFLOW SUMMARY
rows_inspected
 events_accepted
 diagnostics
 errors
 warnings
 accounts
 open_accounts
 closed_accounts
 total_balance_cents
```

The actual output does not include the illustrative leading spaces above. Keys are stable and values are decimal integers.

`total_balance_cents` uses `i128` accumulation so the report can sum several valid `i64` account balances without overflowing at the narrower width. This does not expand individual account capacity.

### Diagnostic rendering

Each diagnostic renders:

```text
<severity>\t<code>\tline <n>\t<message>
```

Stable codes support tests and downstream inspection. Messages are intended for readers and may evolve more freely than codes, although the current format keeps them stable.

### Event rendering

Accepted events render source line, event ID, account ID, kind, amount, and note. Notes cannot contain tabs or newlines under the grammar, so the tab-separated report remains unambiguous.

### Query error rendering

The timeline query retains an arithmetic error channel even though accepted-state invariants should make it unreachable. The account renderer turns that channel into a `QUERY_ERROR` line rather than panicking. A production API might propagate a typed report error instead; the course keeps report signatures small while preserving visible failure.

### Snapshot tests versus semantic tests

A full-string snapshot catches accidental formatting changes but can become noisy. Combine it with semantic assertions:

- accounts sorted lexically;
- errors and warnings counted separately;
- data errors still produce a summary;
- repeated rendering of one `Analysis` value is byte-identical;
- filtering events does not mutate analysis.

Use snapshots for stable interface surfaces, not for every helper.

### Compatibility note

LedgerFlow does not claim a formal machine-readable report protocol. If another program needs to consume reports, define and version that grammar explicitly rather than scraping these lines. Course 9 will treat production compatibility and versioning more deeply.

## 11. Error and exit semantics

LedgerFlow has three failure domains. Collapsing them into one `Result<String, String>` would erase the user action implied by each.

### Domain diagnostics

These describe source data. They belong to `Analysis` and may coexist with accepted state. Examples include invalid fields, duplicate IDs, and illegal account transitions.

- rendered on stdout as analysis findings;
- exit class `1` if at least one error-severity diagnostic exists;
- warnings alone keep exit class `0`;
- later valid rows may still contribute state.

### Query and usage failures

These mean the requested command cannot be interpreted or satisfied, such as an invalid command shape or an account query for a nonexistent account.

- rendered on stderr;
- exit class `2`;
- no claim of completed requested report.

A different product might treat “account absent” as an empty successful query. LedgerFlow chooses a query failure because `account` asks for one required resource.

### I/O failures

The shell may fail to read the file or write output.

- rendered on stderr where possible;
- exit class `2`;
- no data-analysis conclusion is claimed.

### Why header failure is a data error

The file was read and analyzed sufficiently to determine that its declared format is unsupported. This is source data, so `check` reports it as diagnostic `LF002` and exits `1`, not `2`.

### Stable diagnostic codes

Codes `LF001`–`LF016` identify errors. `LF101` identifies normalization warnings. The numeric gap leaves room for future warning groups; it is not generated by a macro because Course 5 owns code generation.

### Typed source context

`DiagnosticKind` retains values such as requested and available amounts, first duplicate line, event kind, and account identity. The renderer is the only place that turns those values into prose.

### Testing exit behavior

Unit-test the pure mapping from `Analysis::has_errors` to `AppOutcome`. Then process-test:

- valid file -> `0`;
- data error -> `1` with stdout report;
- missing file -> `2` with stderr message;
- invalid CLI shape -> `2` with usage;
- warnings only -> `0` with warning lines where command renders diagnostics.

Do not infer exit semantics from `status.success()` alone; inspect the exact code.

## 12. Test and law strategy

Example tests establish cases. Law tests establish relationships across cases. LedgerFlow needs both.

### Unit tests by stage

#### Parser

Test shape, field accumulation, normalization warnings, physical lines, header trust, and ignored rows.

#### Reducer

Test every legal edge and every rejection edge. For rejections, compare recovered ledger with the pre-event ledger.

#### Query tests

Test borrowing, source order, partial consumption, timeline accumulation, and final-balance agreement.

#### Report tests

Test ordering, repeated equality, stable codes, and separation of warning/error counts.

### Integration properties

For representative generated event sequences that obey the grammar:

1. accepted event IDs are unique;
2. every ledger account has exactly one accepted open event;
3. no balance is negative;
4. every closed account has zero balance;
5. audit length equals inspected row outcomes;
6. accepted length plus state/duplicate rejections plus parse-rejected rows equals audit length;
7. final timeline balance equals stored balance;
8. rendering twice is byte-identical.

The standard-library-only capstone does not add a property-testing dependency. Implement small deterministic generators in tests if needed.

### Counterexamples matter

Potential law:

```text
filter(p).filter(q) == filter(both(p, q))
```

This is valid for total effect-free predicates with the same evaluation order. A stateful `q` can distinguish call counts. The course must include the counterexample, not only the pleasant equation.

Potential law:

```text
analyze(input).accepted == analyze(input).accepted
```

This is trivial for one value. The meaningful determinism property is that separate evaluations from equal text yield equal observable reports and domain state.

### Process-test discipline

Temporary fixture names include a timestamp only in the shell test setup; the program output never includes that nondeterminism. Remove fixtures after the process exits. Test exact exit classes and the minimum stable output contract.

### Mutation testing questions

Would tests fail if:

- ID reservation moved after state transition?
- diagnostics were sorted by code instead of source line?
- `take_while` consumed a boundary unexpectedly?
- a rejected withdrawal subtracted before validation?
- account rendering used `HashMap` iteration?
- `unwrap_or` eagerly built an expensive fallback report?

A strong suite distinguishes each semantic mutation.

## 13. Ten capstone increments

The capstone is constructed once, but each day must produce a coherent product increment. Do not create ten branches that merely demonstrate syntax.

### Day 1 — Callable policy

Define local normalization and rendering callbacks. Record capture places and choose `Fn`, `FnMut`, or `FnOnce` from call behavior. Evidence must include a lazy fallback test and one consuming finalizer.

### Day 2 — Borrowed lazy views

Retain accepted event values in a simple fixture model and expose borrowed account filtering. Prove that construction performs no traversal and that `take(1)` pulls only a prefix.

### Day 3 — Row-shape pipeline

Implement line numbering, ignored-line selection, field expansion, and field pairing. State cardinality and order after each adapter. Do not yet perform ledger state transitions.

### Day 4 — Prefix reducer

Implement account state and legal transitions over already valid events. Write the prefix invariant before the reducer. Rejections must recover prior state.

### Day 5 — Diagnostic topology

Replace fail-fast whole-source parsing with row accumulation, accepted-with-warning outcomes, duplicate screening, and typed transition diagnostics. Preserve ordering.

### Day 6 — Domain protocols

Implement at least one custom iterator or collection protocol that removes representation leakage. In the reference architecture this becomes the exact/fused audit iterator and generic batch collection.

### Day 7 — Persistent history

Add immutable audit versions with shared tails. Prove old versions survive and sharing is real. Document chronological materialization cost.

### Day 8 — Shell isolation

Split deterministic `execute_text` from environment, filesystem, output, and process status. Add direct core tests and real process tests.

### Day 9 — Laws and cost ledger

Add query laws, normalization idempotence, deterministic rendering tests, and a cost table. Remove at least one unjustified abstraction or performance claim.

### Day 10 — Independent integration

Complete CLI/report behavior and implement an unseen feature from the extension brief. Produce a final transformation map and defend every materialization boundary.

Each increment includes:

A commit that only renames types or inserts an adapter does not satisfy an increment.

## 14. Cost model

This page classifies expected work. It is not a measured benchmark.

Let:

- `L` be source byte length;
- `R` be inspected nonignored rows;
- `A` be accepted events;
- `C` be accounts;
- `D` be diagnostics;
- `H` be audit entries, normally equal to `R`.

### Parsing

`str::lines` and field splitting scan the source: expected `O(L)`. Accepted events allocate owned account/note strings. Per-row field vectors allocate small temporary storage in the reference implementation; a hand-written splitter could avoid that, but Course 9 should measure before optimizing.

### Identity screening

`BTreeMap<EventId, line>` lookup and insertion are `O(log R)` per syntactically valid event, producing `O(R log R)` comparison work in the worst ordinary model. A `HashMap` could offer expected constant-time operations but has different determinism and denial-of-service considerations. LedgerFlow makes no speed claim.

### Ledger reduction

Each account lookup/update in `BTreeMap` is `O(log C)`. The ledger accumulator is owned and updated in place after validation; it is not cloned per event.

### Accepted retention

The accepted-event vector retains `A` owned events. This enables later queries but means memory is not constant with source length. LedgerFlow is not an unbounded streaming analyzer.

### Queries

Account filtering scans accepted events: `O(A)` in the absence of an index. `take(k)` may stop earlier after finding `k` matches. Building a per-account index would increase construction and retained memory; the current product scale does not justify it.

### Reports

Summary scans accounts: `O(C)`. Account report scans accepted events for that account query: `O(A)`. Event rendering allocates output proportional to rendered text. Account order comes from the tree map without an extra sort.

### Closure and iterator representation

Generic closure and iterator chains are statically represented and do not inherently allocate. This does not prove they are faster than loops, nor does it guarantee all abstraction overhead is optimized away. Such claims require Course 9 measurement and compiler inspection.

### Cost review questions

1. Which retained values can be streamed instead?
2. Which report requires repeated full scans?
3. What input bound makes current choices acceptable?
4. Which optimization would change public ownership or lifetime contracts?
5. Which claim is a standard-library contract, which is an analytical model, and which would need a benchmark?

## 15. Rejected designs

A final architecture is easier to trust when rejected alternatives are explicit.

### One iterator chain from text to report

Rejected because header trust, field accumulation, duplicate policy, recoverable state rejection, persistent history, and report materialization have different contracts. A single chain would hide stage names and produce difficult residual types.

### `collect::<Result<Vec<Event>, _>>()` for the whole source

Rejected because it stops at the first malformed row and cannot represent accepted-with-warning outcomes. It remains the correct reference design for a separate fail-fast importer.

### Printing diagnostics in `parse_row`

Rejected because parsing becomes effectful, library users cannot inspect typed errors, tests must capture output, and report policy leaks into decoding.

### `HashMap` everywhere for “speed”

Rejected as an unsupported performance claim and because account output needs stable ordering. A tree map expresses the current deterministic report requirement directly.

### Clone ledger before every transition

Rejected because the consuming accumulator can preserve failure atomicity without copying every account map. Cloning would be simpler but has an avoidable cost model.

### Mutable audit vector snapshots

A single vector is suitable if only the final audit is needed. Cloning it after every event to preserve versions is rejected. The persistent stack adds one node per version and shares history.

### `Arc<Mutex<_>>` for future parallelism

Rejected because Course 4 is single-threaded and no concurrent ownership requirement exists. It would add runtime synchronization and obscure deterministic state flow. Course 7 will choose concurrency mechanisms from actual work decomposition.

### Box every closure

Rejected because most callables cross one generic boundary and need no heterogeneous storage. Boxing erases type and may allocate without product value.

### Custom `Pipe` extension trait

Rejected because ordinary binding and function composition are clearer for the few pipelines here. A broad convenience trait would expand public API and overlap Course 3’s extension-trait concerns.

### Panic on “impossible” timeline overflow

Rejected because the query independently reconstructs arithmetic. Returning an explicit error makes invariant drift observable and costs little.

### Add macros for diagnostics

Rejected in Course 4. Stable diagnostic codes are written explicitly. Course 5 may automate repetition after the representation and contracts are proven.

### Persist results to disk

Rejected because durable writes, atomic replacement, and filesystem failure protocols would distract from functional transformation. The shell only reads one file and writes terminal streams.

## 16. Independent extension: balance checkpoints

Implement this feature without opening a reference patch.

### User behavior

Add:

```text
ledgerflow checkpoints <events.tsv> <account-id> <every>
```

`every` is a positive event count. The report emits the account balance after every `every` accepted events for that account and always emits the final point when the accepted-event count is not divisible by `every`.

Example balances for four accepted account events with `every = 3`:

```text
CHECKPOINT\t3\t<event-id>\t<balance>
CHECKPOINT\t4\t<event-id>\t<balance>
```

Open and close events count. Rejected events do not.

### Required design constraints

- The query borrows `Analysis`.
- No intermediate vector may be required by the query API.
- The iterator must not recompute the account timeline from the start for each checkpoint.
- `every = 0` is a usage failure with exit class `2`.
- Source data errors still produce exit class `1` after a checkpoint report is rendered.
- Output order is accepted source order.
- The final balance must equal stored account balance.

### Review trap

A naive `filter(|(index, _)| (index + 1) % every == 0)` omits the final nondivisible point. Repairing this by collecting the whole timeline and appending its last item violates the lazy query constraint. Design iterator state that can delay one point or define a small custom adapter with an explicit pending-final contract.

### Distinction extension

For distinction, support `--include-rejected` by interleaving audit rejections without changing balance. This requires a new event/audit merge contract; do not infer it from line-number sorting without considering malformed rows that have no event ID.

## 17. Architecture defense checklist

The defense is not a tour of file names. It tests whether you can reconstruct the program’s contracts and challenge your own design.

### Data and ownership

- Why does `Event` own account and note text?
- Which public queries borrow and which materialize?
- Where does a source `String` cease to be needed?
- Why is the audit persistent while the ledger is an owned mutable accumulator?
- Which old audit values remain valid after push?

### Closure and iterator contracts

- Identify every stored or returned closure and its weakest callable capability.
- Explain why a `move` closure may still implement `Fn`.
- State the item type at each stage of account timeline construction.
- Which consumers stop early, and which exhaust the source?
- Where is a loop clearer than a combinator chain?

### Failure topology

- Why does header failure stop row decoding?
- Why can one row contain several field diagnostics?
- Why are warnings attached to accepted values?
- When is an event ID reserved?
- How does `TransitionFailure` preserve the reducer invariant?
- Which failures map to exit `1` and which to exit `2`?

### State proof

State the prefix invariant without notes. Then trace:

```text
open 0
withdraw 1
 deposit 5
withdraw 5
close 0
```

Show the ledger after every accepted or rejected step and explain why the rejected withdrawal does not affect later balance.

### Determinism and effects

- Which data structure establishes account order?
- What output order is promised for diagnostics?
- Name every external effect in the binary.
- Why is argument interpretation in the core but argument collection in the shell?
- What happens if stdout fails?

### Laws and cost

- Give one law that needs effect-free closures.
- Give its stateful counterexample.
- Distinguish lazy construction from cheap total consumption.
- Give the asymptotic model for parsing, identity screening, reduction, query, and audit chronology.
- Name one claim that requires benchmarking before publication.

### Final rejected alternatives

Defend at least four rejected designs. A strong defense states when the rejected design would become correct under different requirements.

### Final standard

Complete this section when you can:

1. derive the architecture from the product contract;
2. predict compiler and consumption behavior;
3. repair a semantic defect without weakening evidence;
4. implement the independent extension;
5. identify remaining limitations accurately.

Fluent terminology without causal derivation does not pass.

## Acceptance route

From the course root:

```bash
cargo test -p ledgerflow
cargo clippy --workspace --all-targets -- -D warnings
cargo fmt --all -- --check
```

The program should also pass the manual demonstration described in [`capstone/README.md`](../capstone/README.md).
