# LedgerFlow

## Course role

LedgerFlow parses append-only ledger events, preserves diagnostics and source order, reduces valid events into deterministic state, retains an immutable audit history, exposes borrowed queries, and keeps filesystem and terminal effects outside the core.

LedgerFlow is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- Every pipeline stage states item type, ownership, cardinality, order, and failure policy.
- Rejected rows preserve physical source evidence without corrupting accepted state.
- Reductions maintain a named accumulator invariant after every accepted event.
- Structural sharing preserves old audit versions without accidental mutable aliases.
- Pure analysis decides effects; the outer shell performs them in a deterministic order.
- Optimization claims distinguish laziness, allocation, copying, and retention honestly.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
|---:|---|---|
| 31 | Closures, Capture, and Callable Contracts | Distinguish function items, function pointers, and anonymous closure types |
| 32 | The Iterator Model | Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers |
| 33 | Iterator Algebra and Pipeline Shape | Derive the item type and cardinality effect of common iterator adapters |
| 34 | Folds, Scans, and Short-Circuiting | Design a fold accumulator with a precise prefix invariant |
| 35 | Option, Result, and Fallible Traversal | Compose optional and fallible transformations while preserving ownership and error meaning |
| 36 | Custom Iterators and Collection Protocols | Implement a correct custom `Iterator` by defining state and exhaustion behavior |
| 37 | Recursive Data and Structural Sharing | Define recursive algebraic data with the appropriate indirection |
| 38 | Functional Core and Effect Isolation | Separate deterministic domain decisions from filesystem, time, environment, and terminal effects |
| 39 | Combinator Laws and Cost Models | Design domain combinators that preserve type and error meaning |
| 40 | Functional Architecture Synthesis | Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries |

## Reading route

1. Read the LedgerFlow contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

LedgerFlow is the Course 4 capstone: a deterministic, standard-library-only command-line analyzer for append-only ledger events.

It is intentionally not a banking product. The domain is small enough to inspect, but it is rich enough to require every major Course 4 decision:

- closures with honest call contracts;
- lazy borrowed queries;
- shape-changing iterator pipelines;
- fail-fast and accumulated traversal;
- a failure-atomic fold over account state;
- a custom persistent audit structure;
- explicit diagnostic and effect boundaries;
- deterministic rendering;
- law and counterexample tests;
- an imperative shell around a value-oriented core.

## Input grammar

```text
LEDGERFLOW-V1
<event-id>\t<account-id>\t<kind>\t<amount-in-cents>\t<note>
```

Kinds are `open`, `deposit`, `withdraw`, and `close`. Blank lines and lines whose first non-whitespace character is `#` are ignored after the header. The parser preserves physical line numbers.

Example:

```text
LEDGERFLOW-V1
1\tacct-a\topen\t0\tprimary account
2\tacct-a\tdeposit\t5000\topening funds
3\tacct-a\twithdraw\t5000\tsettlement
4\tacct-a\tclose\t0\tcomplete
```

## Commands

```text
ledgerflow check <events.tsv>
ledgerflow summary <events.tsv>
ledgerflow account <events.tsv> <account-id>
ledgerflow events <events.tsv> [account-id]
ledgerflow demo
ledgerflow help
ledgerflow version
```

Exit classes:

- `0`: command completed and the analyzed source contains no error diagnostics;
- `1`: analysis completed, but one or more data errors were reported;
- `2`: usage, query, or I/O failure prevented the requested command.

Warnings do not produce exit class `1` by themselves.

## Proof route

From this directory:

```bash
cargo fmt -- --check
cargo clippy --all-targets -- -D warnings
cargo test --all-targets
cargo test --doc
cargo build --release
bash scripts/demo.sh
```

The course-level `make capstone-confirm` runs the same boundary.

## Design boundary

The parser and analyzer accumulate independent diagnostics, but one event never partially mutates account state. A syntactically valid event ID becomes reserved before state transition; a later event with the same ID is rejected as a duplicate even if the first event was rejected by a state rule. This policy is deliberate and tested.

Read the capstone engineering book under `course-book/capstone/` before modifying the architecture.

## Verification

```bash
cargo test
cargo fmt -- --check
cargo clippy --all-targets -- -D warnings
```
