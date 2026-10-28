# Reasoned solutions — Module 55: Unsafe Rust as a Proof Boundary

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

## Prediction analysis

### Prediction 1

**Problem.** An unsafe block compiles. Has the compiler confirmed its pointer preconditions?

**Reasoned answer.** No. The compiler only permits the operation; the programmer owns the proof.

### Prediction 2

**Problem.** A public function uses raw pointers internally but checks every precondition. Must it be `unsafe fn`?

**Reasoned answer.** No. Implementation unsafety does not require caller unsafety when the public contract is safe.

### Prediction 3

**Problem.** An `unsafe fn` dereferences a pointer without an inner unsafe block under the deny lint. What is missing?

**Reasoned answer.** An explicit local unsafe block that documents how the implementation discharges the operation’s obligation.

### Prediction 4

**Problem.** A private field becomes public. Why can unrelated unsafe code become unsound?

**Reasoned answer.** Safe callers may now construct states that violate invariants the unsafe code assumes.

### Prediction 5

**Problem.** A custom marker trait has no methods. Can its implementation still be unsafe?

**Reasoned answer.** Yes. Other unsafe code may rely on the semantic promise carried by the trait.

### Prediction 6

**Problem.** A test suite never crashes. Is undefined behavior excluded?

**Reasoned answer.** No. Unexecuted paths and optimizer-sensitive violations remain possible.

### Prediction 7

**Problem.** A `no_mangle` export contains only safe arithmetic. Why is the attribute unsafe?

**Reasoned answer.** Global symbol uniqueness and ABI compatibility are obligations outside local type checking.

### Prediction 8

**Problem.** A buffer length is incremented before element initialization, then initialization panics. What invariant fails?

**Reasoned answer.** Drop may treat uninitialized storage as a live element.

## Construction guidance

### Slice proof

The pointer and length must describe one live allocation, the byte range must be initialized, alignment must fit the element type, and aliasing must support the chosen shared or mutable slice.

### Block minimization

Keep bounds and distinctness checks safe; put only pointer addition and dereference inside the block.

### API safety

A safe wrapper is correct when it validates or owns every required fact. An unchecked fast path can be separately unsafe.

### Raw owner audit

Length must never exceed capacity, the allocation layout must match deallocation, initialized elements must be dropped exactly once, and zero-size cases need explicit handling.

### Callback transfer

The context must remain live and correctly typed for every invocation; retention and concurrent invocation require separate contracts.

## Boundary-trace reference

A strong solution trace for this module must create a safety ledger for each unsafe operation: exact operation, required preconditions, code establishing each precondition, validity duration, panic path, cleanup owner, and safe-caller protection. Keep the safe behavioral oracle beside the unsafe kernel. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- placing an entire function in one broad unsafe block;
- using unsafe because a safe design feels verbose;
- copying a `SAFETY` comment without connecting it to code;
- assuming tests prove absence of undefined behavior;
- making a public function safe while leaving caller obligations undocumented;
- making a function public-unsafe merely because its body contains unsafe operations;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Unsafe-proof ledger

For every unsafe operation, write one row before writing the block:

| Operation | Required fact | Established by | Preserved until |
|---|---|---|---|
| raw slice construction | non-null-or-zero, alignment, readable range, one allocation, live duration | caller contract plus checked length | returned slice’s final use |
| unchecked indexing | index is strictly below length | preceding branch or loop invariant | the access completes |
| raw ownership reconstruction | pointer came from the matching ownership escape exactly once | private wrapper state | reconstructed owner is dropped or moved |
| foreign call | ABI, pointer, aliasing, callback, and unwind contracts hold | safe adapter validation plus documented caller obligations | foreign call returns and temporary views expire |

The `SAFETY:` comment should cite concrete program facts, not restate “this is safe.” If a fact is supplied by a public caller, the public function must be `unsafe` and document that obligation under `# Safety`. If the wrapper can establish every fact itself, keep the unsafety private.

## Reachability review

Count not only unsafe blocks but safe entry points that can reach them. A two-line unchecked kernel behind a broad, under-validated safe API is a large unsafe surface. Conversely, several small blocks inside a tightly specified owner may form one coherent proof boundary.

A weak repair adds `unsafe` around a compiler error. A principled repair first writes the safe reference behavior, narrows the performance or interoperability reason safe Rust cannot express, and makes invalid inputs unrepresentable or rejected before entering the unsafe core.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can write a line-by-line safety argument, decide whether the caller or implementation owns each proof, and reject an unsafe abstraction whose private invariant, panic path, or destructor has not been analyzed.

Then perform this destructive regression check: delete one precondition check while keeping the unsafe operation and show that the safety ledger, not just a happy-path test, identifies the missing proof. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.
