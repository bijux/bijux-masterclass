# Final review — Course 6: Rust Systems Programming

## Part A — representation and state

1. Write a versioned byte grammar with limits and canonical encoding.
2. Trace a truncation failure to the first missing offset.
3. Explain why `repr(C)` does not make file bytes a Rust value.
4. Draw a file-replacement state machine and commit point.
5. Distinguish flush, file synchronization, rename, and directory synchronization.
6. Explain why a validated path string is not a race-proof sandbox.
7. Construct a child process without a shell and state environment policy.

## Part B — unsafe proof

For each operation—raw slice creation, pointer arithmetic, `MaybeUninit` read, allocation, deallocation—write exact preconditions, establishing code, duration, cleanup, panic behavior, and safe-caller protection. Reject “the pointer is non-null” as a complete proof.

## Part C — FFI

Design a C validator and opaque session API. Specify:

- C and Rust declarations;
- representation;
- null/alignment/length/overlap rules;
- output initialization on failure;
- status codes;
- ownership transfer;
- callback retention and reentrancy;
- exactly-once free;
- panic containment.

Compile a tiny C and C++ consumer against the header on the targets you claim.

## Part D — adversarial matrix

Test truncation at every byte boundary, oversized declared lengths, trailing bytes, checksum mismatch, symlink ancestors, short writes, cleanup failure, non-UTF-8 native paths where supported, nonzero child exit, null-plus-zero FFI input, invalid output pointer cases that the C contract can state, callback early stop, and double-free prevention at the safe wrapper level.

## Part E — independent construction

Build a packet archive with checked decoding, transactional storage, a native-path import boundary, direct child capture, one manually allocated owner, stateless C validation, and an opaque read session. Include a claim table that labels every success statement as portable, target-conditioned, or external.

Course 6 is complete when every external or unsafe assumption has one named owner and one safe boundary, and when you can state what the implementation still cannot guarantee.
