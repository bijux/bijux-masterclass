# Reasoned solutions — Module 59: Foreign Resources, Callbacks, and Wrapper Architecture

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

## Prediction analysis

### Prediction 1

**Problem.** Two `Session` wrappers are created from one raw handle. What ownership defect follows?

**Reasoned answer.** Both destructors can release the same foreign resource.

### Prediction 2

**Problem.** A borrowed descriptor is wrapped with `from_raw_fd` as owned. What can happen?

**Reasoned answer.** The wrapper may close a descriptor still owned elsewhere.

### Prediction 3

**Problem.** A callback stores the entry-name pointer after return. Is the name still live?

**Reasoned answer.** Not under a call-scoped borrowing contract.

### Prediction 4

**Problem.** The callback frees the session during enumeration. Which pointer becomes invalid?

**Reasoned answer.** The enumerator’s session and all data derived from it.

### Prediction 5

**Problem.** A close error is handled by panicking in `Drop`. What failure can compound?

**Reasoned answer.** A second panic during unwinding can abort, and cleanup cannot return the error.

### Prediction 6

**Problem.** The foreign function fails and `errno` is read after another call. Is the value reliable?

**Reasoned answer.** No. Ambient error state must be captured immediately.

### Prediction 7

**Problem.** An opaque pointer is copied by C. Is copying the address itself forbidden?

**Reasoned answer.** No, but ownership must not be duplicated; only one path may free it.

### Prediction 8

**Problem.** A raw-pointer wrapper is manually marked `Sync`. What proof is required?

**Reasoned answer.** The foreign handle and every operation must be safe for shared concurrent access.

## Construction guidance

### Layering

Raw declarations mirror the header; the shim contains unsafe calls and status translation; the safe wrapper owns lifecycle and lifetimes.

### Raw transfer

`into_raw` prevents drop and gives the caller one release obligation. `from_raw` is unsafe because uniqueness and validity cannot be checked.

### Callback contract

The call is synchronous and same-thread; pointers live only during invocation; callback must not free or mutate the enumerated session; nonzero stops.

### Close policy

A consuming close takes ownership, calls release, and avoids later drop; drop remains best-effort only for paths that did not explicitly close.

### Descriptor transfer

Use `AsFd`/`BorrowedFd` for a borrowed call. Only use raw ownership conversion when the foreign API truly takes responsibility.

## Boundary-trace reference

A strong solution trace for this module must trace successful open as a transfer of one allocation obligation to the foreign caller. Then trace accessor borrows, callback-scoped views, early stop, error status, and exactly-once free. Mark forbidden reentrancy, retention, concurrent access, and post-free use. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- returning an opaque pointer without a matching free contract;
- reconstructing `Box` during a borrowing accessor;
- allowing callbacks to retain temporary pointers;
- freeing or mutating the active session from inside a callback;
- treating null and freed pointers as the same state;
- making concurrent use claims without synchronization;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Opaque-session lifecycle

```text
null output slot
  -> open validates input
  -> one Box-owned Session escapes as opaque pointer
  -> zero or more borrowed operations
  -> zero or more synchronous callback enumerations
  -> exactly one free reconstructs and drops the Box
```

Every copied pointer value is not a copied ownership right. The C contract must state that the handle is single-owner, cannot be used after free, and cannot be freed concurrently with an operation or from inside an active callback.

| Operation | Ownership effect | Borrow/reentrancy rule |
|---|---|---|
| `open` | creates one foreign ownership obligation on success | output remains null on failure |
| `entry_count` | borrows session | no mutation or free during call |
| `for_each_entry` | borrows session and lends temporary name/payload views | callback must not retain views or reenter forbidden operations |
| `close` if provided | consumes logical session and may report failure | successful close prevents later cleanup duplication |
| `free` | consumes opaque ownership exactly once | best-effort destructor path must not panic across ABI |

## Callback clinic

A callback function pointer also needs a context pointer, nullability rule, return-code policy, and lifetime statement. If callback return means “stop,” distinguish deliberate early stop from callback failure. If callbacks can arrive later or on other threads, the wrapper architecture changes completely: retained context ownership, synchronization, shutdown, and `Send`/`Sync` become Course 7 concerns.

A safe Rust wrapper should turn the foreign protocol into ordinary borrowing: the session owner controls lifetime, methods borrow it, and callback views cannot escape the method call. Keep `Box::from_raw` in the one private free path; exposing it through multiple routes invites double reconstruction and double free.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can trace who owns a handle after every call, prevent borrowed and owned wrappers from being confused, define callback retention and reentrancy rules, and explain exactly why an opaque pointer can be reconstructed only once.

Then perform this destructive regression check: exercise open, accessor, callback early stop, and free; then document why a second free or callback-retained view is outside the safe contract even if one test run appears harmless. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.
