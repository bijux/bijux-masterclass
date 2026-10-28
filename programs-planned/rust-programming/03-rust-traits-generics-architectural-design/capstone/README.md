# Review Engine

This directory contains the executable capstone for Course 3. The reader-facing design and ten-step learning route are in the [capstone chapter](../course-book/capstone.md).

Review Engine evaluates ordered submissions against an ordered runtime policy. It is the Course 3 capstone and a complete standard-library-only library and CLI.

## Architecture

| Boundary | Mechanism | Reason |
|---|---|---|
| submission source | generic `Source` with associated item/error | one source selected per engine; associated errors remain precise |
| reporter | generic `Reporter` with associated output/error | caller retains concrete report output |
| policy rules | `Vec<Box<dyn Rule>>` | heterogeneous ordered rules selected from policy text at run time |
| built-in construction | `RuleFactory` registry | typed validation occurs before rule erasure |
| severity | enum | closed product domain with exhaustive rendering |
| engine construction | typestate builder | library callers cannot build without source, reporter, and policy |
| closure rule | local `RuleFn<F>` newtype | coherence-safe adaptation plus stable rule identity |
| built-in marker | sealed trait | downstream code may implement `Rule`, but cannot claim built-in status |

## Input format

`submissions.tsv` contains five tab-separated columns:

```text
id    owner    score    comma-separated-tags    title
```

Example:

```text
S-001	ada	92	rust,cli	A dependable command-line tool
S-002	root	55	prototype	Unreviewed draft
```

## Policy format

```text
min-score	70
require-tag	rust
title-length	5	80
deny-owner	root
```

Blank lines and lines beginning with `#` are ignored.

## Commands

```bash
review-engine check submissions.tsv policy.txt
review-engine list-rules
review-engine explain min-score
review-engine demo
```

Exit status:

- `0`: command succeeded and policy accepted all submissions;
- `1`: evaluation succeeded but at least one error-severity finding rejected a submission;
- `2`: usage, input, policy, or I/O failure.

## Verification

```bash
cargo fmt --manifest-path Cargo.toml -- --check
cargo clippy --manifest-path Cargo.toml --all-targets -- -D warnings
cargo test --manifest-path Cargo.toml --all-targets
cargo test --manifest-path Cargo.toml --doc
cargo build --manifest-path Cargo.toml --release
bash scripts/demo.sh
```

