# Module 07 Exercise Answers

Use these answers after running the corresponding proof. Compare the boundary
reasoning, failure analysis, and preserved contracts rather than copying
assertions.

## Ports and adapters: substitute storage without changing behavior

The domain-facing function accepts `StorageRead`, iterates its typed results,
and derives identifiers from successful `RawDoc` values. It has no reason to
know whether those values came from CSV text, memory, a database, or another
adapter.

Add the same third logical document to the CSV and memory fixtures. Filtering
by category belongs after the port returns `RawDoc`; parsing CSV rows belongs
inside `FileStorage`. The two adapters should then produce the same ordered
identifier list.

Common wrong turns:

- checking `isinstance(storage, FileStorage)` couples behavior to
  infrastructure;
- passing raw CSV text into the domain function moves parsing across the
  boundary;
- comparing only counts can hide ordering or identity differences;
- asserting the adapters have identical internal state confuses implementation
  with observable contract.

The proof establishes substitutability for this read behavior. It does not show
that both adapters have the same performance, persistence, concurrency, or
failure characteristics.

## Effect interfaces: prove description before execution

Compose a second `io_map` over the identifier-producing plan:

```python
counted = io_map(plan, len)
```

This builds another `IOPlan`; it does not inspect the iterator or execute the
storage capability. `perform(counted)` drives the original delayed read once,
then applies both pure mappings and returns `Ok(2)`.

Common wrong turns:

- writing `io_delay(delayed_read())` passes an already executed `Result`
  instead of a thunk;
- calling `list(storage.read_docs(...))` before construction makes the read
  eager;
- invoking `perform` inside a domain helper hides the interpreter boundary;
- asserting only the final count misses premature or repeated reads.

The trace proves deferral and one execution for this interpretation. It does
not prove the effect is safe to replay; idempotency is a separate contract.

## Capability protocols: request the least authority

The counting function needs only `read_docs`, so its parameter should remain
`StorageRead`. `ReadOnlyDocs` satisfies that protocol structurally. Adding a
dummy `write_chunks` method would broaden authority only to satisfy a need the
function does not have.

Common wrong turns:

- annotating the parameter as full `Storage` permits writes unnecessarily;
- inheriting a concrete adapter couples the domain to infrastructure;
- using `Any` makes the example run while discarding static evidence;
- relying only on `hasattr` checks one object at runtime, not call-site
  discipline.

The behavioral test proves the read-only adapter works. Strict mypy proves the
assignment matches the declared protocol and would reject a write through that
narrowly typed reference. Neither proves the adapter's external data source is
available or trustworthy.
