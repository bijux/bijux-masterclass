# Course 6 reference — Rust Systems Programming

## Boundary ledger

For every external operation, write:

```text
external representation | owner/resource state | checked facts | unchecked facts |
state transition | failure effect | cleanup owner | strongest honest success claim
```

Never create a stronger Rust value before proving its validity conditions.

## Binary parsing

- write the byte grammar and limits before code;
- use explicit widths and endianness;
- prove ranges before slicing;
- use checked arithmetic before length conversion or allocation;
- separate structural validity, text encoding, integrity, and domain rules;
- reject unexpected trailing bytes unless the format allows them;
- emit one canonical encoding when compatibility and reproducibility matter.

A checksum detects accidental corruption under its stated model. It does not authenticate a hostile sender.

## File-state vocabulary

| Operation | What it may establish |
|---|---|
| `write` | some prefix accepted; short writes are legal |
| `write_all` | all bytes passed to the writer or an error |
| `flush` | user-space buffering pushed to the underlying writer |
| file sync | a request to synchronize file data/metadata subject to platform/filesystem contracts |
| rename/replace | pathname installation semantics subject to target rules |
| directory sync | stronger persistence evidence for directory-entry changes where supported |

Same-directory staging plus complete write, flush, sync, close, and rename can provide a strong pre-commit failure-atomicity story. Do not call it universally crash-durable without a target-specific protocol and evidence.

## Paths and processes

Native paths are not guaranteed UTF-8. Keep `Path`/`OsStr` identities native and convert only for display with an explicit lossy policy. A validated relative logical name is not by itself a race-proof sandbox; filesystem lookup may change.

Launch a process with program plus argument vector, not a shell string. Decide environment inheritance, current directory, stdin, stdout/stderr capture, wait policy, and size limits explicitly. A nonzero child status is process data unless your product contract classifies it as invocation failure.

## Unsafe ledger

For each unsafe operation, state:

1. what compiler check is being bypassed;
2. exact preconditions;
3. which safe constructor or state transition establishes them;
4. why they remain true for the operation’s duration;
5. panic and partial-initialization behavior;
6. cleanup path;
7. why safe callers cannot violate the invariant.

Keep unsafe blocks small enough that every operation can be connected to a fact. `unsafe` permits an operation; it does not prove it sound.

## Raw storage and allocation

Track allocation identity, layout, alignment, bounds, initialization, aliasing, and lifetime separately. `MaybeUninit<T>` represents storage that may not yet contain a valid `T`; only the initialized prefix may be read or dropped. Manual allocation owners must deallocate with the exact layout used to allocate and model zero-size state deliberately.

## FFI contract

For every exported function, align the Rust and C declarations and document:

- ABI and representation (`extern "C"`, `repr(C)` where required);
- pointer nullability, alignment, readable/writable length, and overlap;
- ownership transfer and exactly-once release;
- string encoding and termination;
- initialized output behavior on failure;
- stable status codes;
- callback duration and retention rules;
- reentrancy and concurrency limits;
- panic containment.

Opaque handles are foreign-owned capabilities backed by one Rust allocation. Borrowing operations must not free; free consumes exactly once; callbacks may not retain temporary views unless a separate ownership transfer exists.

## Claim discipline

Classify systems claims as language guarantee, library contract, target-conditioned behavior, filesystem/OS contract, foreign-code obligation, current observation, or unsupported assumption. The strongest honest wording is part of correctness.

## Course 6 completion

You are ready for Course 7 when you can decode hostile bytes safely, describe transactional file states, preserve native path and process boundaries, write and review a safety ledger, implement one owning unsafe abstraction, align a C header with Rust exports, and defend the entire FrameVault boundary without treating successful compilation as proof of external behavior.
