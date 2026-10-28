PYTHON ?= python3

.PHONY: help static-proof compiler-labs check test starters fmt clippy docs miri proof clean
help:
	@echo 'make static-proof | compiler-labs | check | test | starters | fmt | clippy | docs | miri | proof'

static-proof:
	$(PYTHON) ../tools/audit.py
	$(PYTHON) ../tools/check_links.py
	$(PYTHON) ../tools/check_rust_sources.py

compiler-labs:
	$(PYTHON) ../tools/run_compiler_labs.py 10-rust-advanced-mastery

check:
	cargo check --workspace --all-targets

test:
	cargo test --workspace --all-targets
	cargo test --workspace --doc

starters:
	@set -e; find labs -path '*/starter/Cargo.toml' -print | while read f; do cargo check --manifest-path $$f --all-targets; done

fmt:
	cargo fmt --all -- --check

clippy:
	cargo clippy --workspace --all-targets -- -D warnings

docs:
	mkdocs build --strict -f ../mkdocs.yml

miri:
	cargo miri test --manifest-path capstone/Cargo.toml inline_batch

proof: static-proof fmt clippy check test starters compiler-labs docs

clean:
	cargo clean
