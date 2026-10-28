PYTHON ?= python3
COURSES := 01-rust-foundations 02-rust-ownership-lifetimes-memory 03-rust-traits-generics-architectural-design 04-rust-functional-programming 05-rust-metaprogramming 06-rust-systems-programming 07-rust-concurrency-parallelism 08-rust-async-networked-services 09-rust-performance-production-engineering

.PHONY: help audit links rust-source-audit static-proof progress compiler-labs check test starters fmt clippy docs c-header proof clean
help:
	@echo 'make audit | links | rust-source-audit | static-proof | progress | compiler-labs | check | test | starters | fmt | clippy | docs | c-header | proof'

audit:
	$(PYTHON) tools/audit.py
links:
	$(PYTHON) tools/check_links.py
rust-source-audit:
	$(PYTHON) tools/check_rust_sources.py
static-proof: audit links rust-source-audit c-header
progress:
	$(PYTHON) tools/progress.py
compiler-labs:
	$(PYTHON) tools/run_compiler_labs.py
check:
	@set -e; for c in $(COURSES); do cargo check --manifest-path $$c/Cargo.toml --workspace --all-targets; done
test:
	@set -e; for c in $(COURSES); do cargo test --manifest-path $$c/Cargo.toml --workspace --all-targets; cargo test --manifest-path $$c/Cargo.toml --workspace --doc; done
starters:
	@set -e; find $(COURSES) -path '*/starter/Cargo.toml' -print | while read f; do cargo check --manifest-path $$f --all-targets; done
fmt:
	@set -e; for c in $(COURSES); do cargo fmt --manifest-path $$c/Cargo.toml --all -- --check; done
clippy:
	@set -e; for c in $(COURSES); do cargo clippy --manifest-path $$c/Cargo.toml --workspace --all-targets -- -D warnings; done
docs:
	mkdocs build --strict -f mkdocs.yml
c-header:
	$(PYTHON) tools/check_c_header.py
proof: static-proof fmt clippy check test starters compiler-labs docs
clean:
	rm -rf ../rust-programming-site .progress.json
	@set -e; for c in $(COURSES); do cargo clean --manifest-path $$c/Cargo.toml 2>/dev/null || true; done
