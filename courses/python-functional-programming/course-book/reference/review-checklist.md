# FP Review Checklist (Module 09)

- Purity: no hidden I/O, globals, randomness, timestamps in core paths.
- Immutability: public dataclasses are frozen; no mutable defaults; no leaked internal mutation.
- Stdlib-first: prefer `itertools` / `functools` / `operator` before adding new helpers.
- Errors: use `Result`/`ErrInfo` and explicit policies; avoid broad `except Exception` in core.
- Streaming: avoid unbounded buffering; if concurrency is used, ensure bounded policies.
- Ports/adapters: ports return effect descriptions; interpreters live in shells/adapters only.
- Tests: add properties for laws/guarantees when introducing new operators/policies.

