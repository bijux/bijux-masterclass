# CommandForge

CommandForge is the cumulative product for Rust Course 5. It is a small command framework whose compile-time layers each have one authority:

- `diagnostic_catalog!` owns diagnostic variants, stable diagnostic codes, messages, reverse lookup, and catalog order.
- `#[derive(CommandArgs)]` owns repetitive decoding derived from an ordinary argument struct and its field helper attributes.
- `#[command_handler]` validates a handler boundary, preserves the function, and generates a typed descriptor.
- `command_catalog!` owns cross-command name uniqueness, catalog order, descriptor association, and lookup generation.
- `build.rs` owns checked external exit-code data and generates Rust under `OUT_DIR`.
- ordinary Rust owns command behavior, application routing, output, and errors.

## Commands

```text
commandforge list
commandforge explain <command>
commandforge run add --left <i64> --right <i64>
commandforge run slug --text <text>
commandforge run repeat --text <text> [--times <u32>]
commandforge run contains --text <text> --needle <text>
commandforge demo
commandforge help
commandforge version
```

## Verification

```bash
cargo test --manifest-path Cargo.toml --all-targets
cargo test --manifest-path Cargo.toml --doc
cargo clippy --manifest-path Cargo.toml --all-targets -- -D warnings
cargo run --manifest-path Cargo.toml -- demo
```

Read `../course-book/capstone.md` before modifying the architecture. The guide explains the source-of-truth map, generated surfaces, negative contracts, testing strategy, and each module increment.
