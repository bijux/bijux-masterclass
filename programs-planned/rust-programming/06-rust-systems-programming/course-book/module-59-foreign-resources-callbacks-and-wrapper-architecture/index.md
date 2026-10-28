# 59 — Foreign Resources, Callbacks, and Wrapper Architecture

**Course 6, day 9 · Module 59 of 60**  
`████████████████████` **59/60**

[← Module 58: C FFI: ABI, Strings, Pointers, and Error Boundaries](../module-58-c-ffi-abi-strings-and-error-boundaries/index.md) · [Course 6 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 60: Integrated Systems Design, Testing, and Audit →](../module-60-integrated-systems-design-and-audit/index.md)

## The question

> How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?

## Why this comes now

A stateless FFI function is useful but limited. Real foreign APIs return handles, borrow buffers, invoke callbacks, and separate status codes from detailed errors. Module 59 builds a layered wrapper architecture and an opaque C-facing session for FrameVault. It also connects the generic RAII work of Course 2 to operating-system and foreign resource handles.

## What you will be able to do

- Separate raw bindings, checked unsafe shims, and safe domain wrappers.
- Represent owned and borrowed foreign handles as different Rust types.
- Pair acquisition with exactly one release and define destructor failure policy.
- Design context-pointer callbacks with explicit lifetime, reentrancy, and retention rules.
- Use `OwnedFd`/`BorrowedFd` or owned/borrowed handles where platform APIs expose them.
- Expose opaque Rust-owned sessions to C without leaking Rust layout.

## Core model

### Use three layers, not one giant wrapper

A maintainable foreign interface has three responsibilities:

```text
raw declarations
    exact ABI-shaped names and types
        ↓
checked unsafe shim
    validates Rust-side conditions and translates raw outcomes
        ↓
safe domain wrapper
    owns resources, exposes lifetimes, and returns Rust errors
```

Raw bindings should be boring and close to the foreign header. The shim contains small unsafe calls and safety arguments. The safe wrapper should not expose raw pointers or foreign status conventions unless the caller genuinely needs an unsafe escape hatch.

### Owned and borrowed handles are different capabilities

A raw integer descriptor or pointer does not say whether the recipient must close it. Rust’s `OwnedFd` and `BorrowedFd<'a>` on Unix, and corresponding handle/socket types on Windows, make that distinction explicit for operating-system resources.

For a generic foreign API, create separate wrapper types:

```rust
pub struct Session {
    raw: NonNull<RawSession>,
}

pub struct SessionRef<'a> {
    raw: NonNull<RawSession>,
    _owner: PhantomData<&'a Session>,
}
```

Only `Session` releases the handle. A borrow cannot outlive the owner. Do not create an owned wrapper from a borrowed raw handle unless ownership transfer is documented.

### Acquisition must commit ownership exactly once

Foreign constructors often return a status and write a handle through an out-pointer. Initialize the slot as null, call the function, and accept ownership only when both status and pointer satisfy the contract. If the foreign API can return a handle alongside an error, its documentation must say who releases it.

The Rust constructor should not place a potentially invalid handle in a `Session` before validation. `NonNull::new` makes null rejection explicit, but still does not prove the handle points to a valid foreign object. That proof comes from the successful foreign constructor contract.

### Drop is the normal release path, not an error-reporting channel

`Drop::drop` cannot return `Result`. If foreign release can fail meaningfully, decide among:

- a consuming `close(self) -> Result<(), E>` that suppresses later drop on success;
- best-effort release in `Drop` with errors ignored or logged under a documented policy;
- an infallible or process-fatal foreign release contract.

Do not panic from `Drop` because close failed, especially during unwinding. For many OS handles, close errors cannot be recovered reliably after ownership has been consumed. The wrapper can expose explicit flush or commit operations before drop for errors the application must handle.

### Opaque C handles protect Rust layout

To let C retain a Rust-owned archive session, export an incomplete C type and pointer:

```c
typedef struct FvSession FvSession;
int32_t framevault_open(const uint8_t *data, size_t len, FvSession **out);
void framevault_free(FvSession *session);
```

Rust allocates a private `Session` with `Box::new` and returns `Box::into_raw`. The free function reconstructs the box exactly once with `Box::from_raw`. C must treat the pointer as opaque, never copy ownership into two independently freed handles, and never call functions after free.

The Rust type’s fields may change without altering the C layout because C never sees them.

### Callbacks need a context pointer and a lifetime contract

A C callback commonly carries one opaque context pointer:

```rust
pub type EntryCallback = unsafe extern "C" fn(
    context: *mut std::ffi::c_void,
    name: *const u8,
    name_len: usize,
    payload_len: u64,
) -> i32;
```

The wrapper passes a pointer to caller-owned state as `context`. Before invoking, it validates that a callback exists and that the session is live. The callback receives a borrowed name valid only for the call. A nonzero return can request early stop.

The contract must state whether callbacks are synchronous, whether they may reenter the same session, whether they may call free, and whether they can run from another thread. FrameVault chooses synchronous, same-thread, non-retaining callbacks and forbids freeing or mutating the session during enumeration.

### Reentrancy can invalidate seemingly safe assumptions

Suppose a wrapper holds a mutable borrow of internal state and invokes user code. If the callback reenters the wrapper, `RefCell` may panic or raw invariants may be violated. Even without interior mutability, a callback that frees the foreign handle can invalidate the current operation.

Design callbacks so no exclusive borrow or temporary raw pointer must survive an uncontrolled call. Copy small metadata before invoking. Use a state flag only when its semantics and panic cleanup are clear. The simplest policy is often to expose an immutable enumeration over a frozen session and document that mutation and destruction are forbidden until it returns.

### Error channels should not depend on ambient global state

C APIs sometimes use `errno`, thread-local last-error slots, or a second query function. Capture the error immediately after the failing call because later calls can overwrite it. Convert it into an owned Rust error with operation context.

For a Rust-exported C API, stable direct status codes and caller-provided report structures are easier to reason about than a global last-error string. If a textual diagnostic API is added, define ownership and thread-safety rather than returning a pointer to mutable global storage.

### Borrowed OS handles prevent accidental close

On Unix, traits such as `AsFd` return `BorrowedFd<'_>` whose lifetime is tied to the owner. `IntoRawFd` transfers responsibility out; `FromRawFd` is unsafe because the caller must prove unique ownership and a valid open descriptor. Similar APIs exist for Windows handles and sockets.

Prefer borrowing traits when passing an existing resource to another API. Raw extraction should occur at the narrow platform boundary, with ownership transfer documented. Integer equality is not a sufficient ownership model.

### Threading promises belong to the foreign contract

A foreign library may state that handles are confined to one thread, shareable for reads, or internally synchronized. Rust wrappers must reflect that in `Send` and `Sync` behavior. Raw pointers do not automatically encode the correct answer.

Course 6 does not add manual `Send` or `Sync` to its opaque session. Course 7 will revisit foreign handles under concurrency with explicit guarantees. This prevents an accidental auto-trait promise from entering the public API before it has been proved.

### A safe wrapper can still preserve an unsafe escape hatch

Advanced callers may need the raw handle for another foreign API. Expose `as_raw` as a borrowed observation when possible. An ownership-transferring `into_raw(self)` must suppress `Drop` and clearly assign release responsibility to the caller. Reconstructing with `from_raw` should be unsafe and require a unique valid owned handle.

The safe path remains complete; raw access is not required for ordinary use.

### Opaque session lifecycle

The C-visible type is incomplete:

```c
typedef struct FvSession FvSession;
```

Rust owns the actual representation:

```rust
pub struct FvSession {
    archive: Archive,
}
```

Opening uses an out-pointer so null can remain the failure value:

```rust
#[unsafe(no_mangle)]
/// # Safety
/// `out` must be writable. The input byte contract matches
/// `framevault_validate`. On success, `*out` owns one session that must be
/// passed exactly once to `framevault_free`.
pub unsafe extern "C" fn framevault_open(
    bytes: *const u8,
    length: usize,
    out: *mut *mut FvSession,
) -> i32 {
    if out.is_null() {
        return FV_INVALID_ARGUMENT;
    }
    unsafe { out.write(std::ptr::null_mut()) };
    let input = match unsafe { checked_input(bytes, length) } {
        Ok(value) => value,
        Err(code) => return code,
    };
    let archive = match decode_archive(input, Limits::ffi_default()) {
        Ok(value) => value,
        Err(_) => return FV_INVALID_ARCHIVE,
    };
    let raw = Box::into_raw(Box::new(FvSession { archive }));
    unsafe { out.write(raw) };
    FV_OK
}
```

The box transfer occurs only after every fallible parse step succeeds. There is no half-owned session. The free function accepts null as a no-op for C convenience but reconstructs any non-null pointer exactly once.

### Enumeration callback

```rust
pub type FvEntryCallback = unsafe extern "C" fn(
    context: *mut std::ffi::c_void,
    name: *const u8,
    name_len: usize,
    payload_len: u64,
) -> i32;
```

The enumeration function borrows the session immutably. For each entry, it passes `name.as_ptr()` and `name.len()`. The string remains live because the archive owns it and no mutation occurs during iteration. The callback contract forbids retention beyond invocation even though the session may remain live; this allows future implementations to use temporary encoding buffers without changing the ABI promise.

A nonzero callback result stops enumeration and is returned distinctly from library failures. The callback is called synchronously on the calling thread. It must not unwind, free the session, or reenter a mutating operation. These are not suggestions; they are the boundary contract.

### Rust-side callback test

A Rust integration test can supply an `extern "C"` callback and a context pointer to a `Vec<String>`:

```rust
unsafe extern "C" fn collect(
    context: *mut c_void,
    name: *const u8,
    name_len: usize,
    _payload_len: u64,
) -> i32 {
    let output = unsafe { &mut *(context.cast::<Vec<String>>()) };
    let bytes = unsafe { std::slice::from_raw_parts(name, name_len) };
    output.push(std::str::from_utf8(bytes).unwrap().to_owned());
    0
}
```

The test’s unsafe blocks have their own proofs: context was created from a live mutable vector and used synchronously; the name range is guaranteed by the library callback contract. This test does not replace an external C smoke test, but it exercises ownership and callback flow.

### Double-free and use-after-free remain caller violations

An opaque API can make correct use simple, but C can still copy a pointer, free twice, or call after free. Rust cannot detect those cases reliably without adding a registry, generations, or reference counting—and those mechanisms introduce their own concurrency and lifetime contracts.

The C header marks such behavior invalid. Safe Rust callers receive a separate safe wrapper that owns the raw session and frees it in `Drop`, preventing these errors in ordinary Rust code.

## Use the idea in a complete program

FrameVault adds an opaque `FvSession` C API. `framevault_open` validates and owns decoded archive data; `framevault_entry_count` reads metadata; `framevault_for_each_entry` invokes a synchronous callback with temporary name bytes; `framevault_free` consumes the handle. Rust-side tests exercise open, enumerate, early stop, and free through the exported functions without requiring a C compiler.

The matching independent laboratory is [Opaque Foreign Session](../../labs/module-09-opaque-foreign-session/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) by updating the owner of the opaque session after every successful and failed call. Build the Opaque Foreign Session lab, test early callback stop and null release, and review FrameVault for retention, reentrancy, concurrent-free, double-free, and post-free assumptions.

## Ready to continue

You are ready when you can trace who owns a handle after every call, prevent borrowed and owned wrappers from being confused, define callback retention and reentrancy rules, and explain exactly why an opaque pointer can be reconstructed only once.

## Primary Rust references

- [Rust standard library: OwnedFd](https://doc.rust-lang.org/std/os/fd/struct.OwnedFd.html)
- [Rust standard library: BorrowedFd](https://doc.rust-lang.org/std/os/fd/struct.BorrowedFd.html)
- [Rustonomicon: FFI callbacks](https://doc.rust-lang.org/nomicon/ffi.html#callbacks-from-c-code-to-rust-functions)
- [Rust standard library: Box::into_raw](https://doc.rust-lang.org/std/boxed/struct.Box.html#method.into_raw)

## Continue

1. Complete the [Module 59 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 59 — Opaque Foreign Session](../../labs/module-09-opaque-foreign-session/README.md) from its public contract.
3. Apply the Module 59 increment in the [FrameVault engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
