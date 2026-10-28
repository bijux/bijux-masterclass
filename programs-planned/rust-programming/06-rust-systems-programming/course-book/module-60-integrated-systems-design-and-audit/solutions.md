# Reasoned solutions — Module 60: Integrated Systems Design, Testing, and Audit

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

## Prediction analysis

### Prediction 1

**Problem.** All end-to-end tests pass, but no truncation tests exist. Which parser property remains weakly evidenced?

**Reasoned answer.** Bounds behavior at every intermediate field and payload boundary.

### Prediction 2

**Problem.** The archive output changes because directory iteration order changes. Which contract is missing?

**Reasoned answer.** A deterministic explicit ordering policy.

### Prediction 3

**Problem.** Miri passes one test. Is every safe public path sound?

**Reasoned answer.** No. Only executed paths under that tool configuration were checked.

### Prediction 4

**Problem.** A Linux path test passes. Does it establish Windows prefix handling?

**Reasoned answer.** No. Target-specific semantics require target-specific evidence.

### Prediction 5

**Problem.** One unsafe line is undocumented but appears obvious. Is line count a sufficient audit?

**Reasoned answer.** No. The proof must state all preconditions and their evidence.

### Prediction 6

**Problem.** A new format version silently accepts unknown flag bits. What evolution risk appears?

**Reasoned answer.** Old readers may misinterpret semantics they do not understand.

### Prediction 7

**Problem.** The C ABI adds a field to a public struct without versioning. What can break?

**Reasoned answer.** Foreign callers compiled against the old size/layout can become incompatible.

### Prediction 8

**Problem.** A timeout feature is requested. Should a polling loop be presented as a portable sandbox?

**Reasoned answer.** No. Define the limited timeout claim or defer to platform/process-control work.

## Construction guidance

### Boundary map

Every arrow names representation, owner, validation, error, and lifetime. Shared facts must have one source of truth.

### Threat table

Malformed bytes are rejected and bounded; hostile namespace races are limited by the fresh-tree assumption; untrusted process containment is out of scope; invalid foreign pointers remain caller safety obligations.

### Test matrix

Run codec tests everywhere, path/process/ABI tests on each supported family, Miri on focused unsafe code, sanitizers on supported native targets, and external C compilation where a compiler exists.

### Unsafe audit

Constructor establishes the invariant, methods borrow from it, no reallocation occurs, and drop follows the exact allocation state. Every failure before construction leaves no owner.

### Packet transfer

The independent product must specify bytes first, bound every count, keep ordinary parsing safe, and justify any unsafe or FFI feature by a real boundary.

## Boundary-trace reference

A strong solution trace for this module must build one end-to-end ledger crossing bytes, domain values, staged files, native paths, child-process data, manual storage, ABI reports, and opaque sessions. For every transition, name the owner, validation, failure state, cleanup, compatibility effect, and strongest honest success claim. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- auditing each module in isolation while ignoring cross-layer assumptions;
- letting the CLI reinterpret a format rule;
- claiming portability from one target test;
- treating all failures as one string;
- expanding the unsafe core during integration;
- adding features without updating the compatibility and threat model;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Integrated claim ledger

A final systems review should contain one row for every externally visible claim:

| Claim | Establishing layer | Destructive regression |
|---|---|---|
| malformed lengths cannot cause unchecked slicing | binary decoder | remove one checked range and feed a truncation fixture |
| a failed pre-commit write preserves the old archive | storage transaction | inject failure before rename and compare destination bytes |
| logical names cannot express traversal | archive-name parser | add `..`, empty, backslash, and drive-marker fixtures |
| captured arguments preserve boundaries | process request model | include spaces, empty strings, and shell metacharacters |
| safe callers cannot violate raw-buffer invariants | owning wrapper | attempt aliasing, double ownership, and post-drop access through public APIs |
| C failure leaves initialized output | ABI adapter | trigger every error status and inspect all report fields |
| opaque sessions release exactly once | foreign lifecycle | enumerate, stop early, free, and reject use-after-free in the C contract tests |

The ledger separates evidence from confidence. A passing happy-path test is not evidence for failure atomicity, portability, or panic containment unless it attacks the corresponding transition.

## Cross-layer counterexample

Consider adding compressed entries. The parser must validate compressed and declared uncompressed lengths; cumulative budgets must use the expansion limit; extraction must avoid publishing a partial file; the C report may need a new versioned field; and process capture is irrelevant. Treating compression as “just another payload flag” would miss allocation, denial-of-service, compatibility, and commit-state changes.

The correct final defense traces one feature from bytes through validated domain state, persistence, safe API, unsafe core, ABI, CLI, and tests. It also names the strongest claim deliberately not made—for example adversarial race-proof extraction or hard hostile-child memory bounds—so the product remains honest at its platform boundary.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready to complete Course 6 when you can defend FrameVault boundary by boundary, identify claims that depend on target evidence, repair an unseen unsafe or I/O defect without weakening the product, and implement an independent binary utility under the same proof discipline.

Then perform this destructive regression check: add one new entry kind from wire format through CLI and FFI, then deliberately omit one layer and confirm that the traceability matrix exposes the incomplete change. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.
