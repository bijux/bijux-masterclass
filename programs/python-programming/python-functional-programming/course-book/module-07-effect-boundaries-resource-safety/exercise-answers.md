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

## Resource safety: close a partial read

The generator body does not run at construction, so the open trace is initially
empty. The first `next` enters the adapter's `with open` block, and the second
`next` reuses that same file. Calling `close` injects generator finalization at
the suspension point and exits the context manager.

Common wrong turns:

- converting to a list exhausts the iterator and avoids the partial-consumption
  case;
- testing only `csv_file.closed` after function return may pass because of
  implementation-specific cleanup;
- opening the file before returning the generator makes construction eager;
- closing the raw file behind the adapter violates ownership.

The proof establishes deterministic cleanup for cooperative early termination.
It does not cover process crashes or a consumer that abandons the iterator
without closing it.

## Functional logging: separate trace construction from emission

Add `trace_value("first_doc", "d1", level="TRACE")` before the final
`writer_pure`. Writer concatenates entry tuples in semantic execution order, so
the new entry follows the count and precedes the returned document list.

Common wrong turns:

- calling `logger.log` inside an `and_then` callback performs an effect in the
  description;
- returning log strings instead of the document list changes the primary value;
- sorting entries after construction destroys execution order;
- checking only the final logger contents misses premature emission.

The empty logger assertion distinguishes accumulating data from emitting it.
The final equality proves the shell forwarded every entry in order. This does
not prove a console, file, or remote logger will successfully persist output.

## Static capabilities: make time an explicit dependency

Call `record_ingest` three times with the same `MonotonicTestClock` and
`CollectingLogger`. Starting at midnight UTC, the expected suffixes end in
`.000001+00:00`, `.000002+00:00`, and `.000003+00:00`.

Common wrong turns:

- constructing a new test clock for every call repeats the first timestamp;
- calling `datetime.now` bypasses the declared capability;
- injecting full storage or application configuration grants irrelevant
  authority;
- asserting only that timestamps differ misses the adapter's exact contract.

The test proves deterministic composition of these two capabilities. Static
annotations make the allowed effect surface reviewable. It does not prove the
production clock is perfectly synchronized or the production logger is
available.
