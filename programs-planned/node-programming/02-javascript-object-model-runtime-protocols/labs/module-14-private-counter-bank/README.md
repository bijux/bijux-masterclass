# Laboratory 14 — Private Counter Bank

## Product

Build a bank of named counters whose balances are protected by JavaScript private fields. Construction, reconstruction, transfer, and brand testing must all preserve the same runtime invariant.

The laboratory demonstrates that a class is more than a TypeScript declaration and a prototype. A legitimate instance has passed the class's initialization path and carries its private brand. Setting an arbitrary object's prototype to `CounterBank.prototype` cannot create that state.

## Contract

`CounterBank.create` validates unique names and non-negative safe-integer balances. `CounterBank.fromSnapshot` validates external plain data and reconstructs through the legitimate initialization path. `transfer` changes two balances as one candidate transition and rejects insufficient funds without partial mutation. `snapshot` returns plain immutable data. `CounterBank.isCounterBank` uses the private brand rather than `instanceof` alone.

## Invariants

- names are normalized and unique;
- balances are non-negative safe integers;
- total balance is preserved by transfer;
- failed transfer changes nothing;
- callers cannot obtain the private map;
- a forged prototype object fails the private-brand test;
- snapshots are plain data and do not retain live aliases.

## Initialization investigation

Add an audited subclass whose field initializer records a marker. Trace when base private state, base constructor body, derived fields, and derived constructor body become observable. Do not call overridable methods from the base constructor.

## Transfer

Add a batch transfer method that validates every debit and arithmetic result before publishing any balance. Compare candidate-state construction with incremental rollback.
## Failure-atomic transfer method

Before mutating the private map, read both balances and compute both candidates. Validate source sufficiency and destination overflow against those candidates. Only then publish the two writes. This ordering is part of the class invariant: a thrown exception must leave the bank exactly as it was before the call. Do not implement debit, then credit, then attempt rollback. Rollback would create another transition whose own failure policy must be proved.

The snapshot is also an authority boundary. It should create new plain records, sort them deterministically, and prevent callers from using the result to mutate private state. A frozen outer array alone is not enough if its records remain mutable.

