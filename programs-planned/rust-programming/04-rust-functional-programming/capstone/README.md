# LedgerFlow

This directory contains the executable capstone for Course 4. The reader-facing design and ten-step learning route are in the [capstone chapter](../course-book/capstone.md).

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
