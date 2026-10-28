PYTHON ?= python3

.PHONY: help check test starters compiler-labs fmt clippy docs proof clean
help:
	@echo 'make check | test | starters | compiler-labs | fmt | clippy | docs | proof'
check:
	cargo check --workspace --all-targets

test:
	cargo test --workspace --all-targets
	cargo test --workspace --doc
starters:
	@set -e; find labs -path '*/starter/Cargo.toml' -print | while read f; do cargo check --manifest-path $$f --all-targets; done
compiler-labs:
	$(PYTHON) ../tools/run_compiler_labs.py $(notdir $(CURDIR))
fmt:
	cargo fmt --all -- --check
clippy:
	cargo clippy --workspace --all-targets -- -D warnings
docs:
	cd .. && mkdocs build --strict -f mkdocs.yml
proof: check fmt clippy test starters compiler-labs docs
clean:
	cargo clean
