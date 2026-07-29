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
