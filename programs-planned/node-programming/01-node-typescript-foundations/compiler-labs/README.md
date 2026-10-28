# Type-Checker and Runtime Investigations

These eighty small programs isolate the boundary between TypeScript checking, emitted JavaScript, Node execution, and product design. Predict before running the supplied investigation route. A failure counts only when it occurs for the intended causal reason recorded in `manifest.json`.

## Outcome vocabulary

- `typecheck-pass` — strict TypeScript should accept the source.
- `typecheck-fail` — strict TypeScript should reject the source for the named relationship.
- `run-pass` — the emitted JavaScript should complete with the exact output.
- `run-fail` — the emitted JavaScript should fail for the specified runtime reason.

## Distribution

| Outcome | Cases |
|---|---:|
| `typecheck-pass` | 39 |
| `typecheck-fail` | 31 |
| `run-pass` | 2 |
| `run-fail` | 8 |

## Investigation method

1. Read the title and source without opening the manifest explanation.
2. Predict the phase and result.
3. State the causal rule in one sentence.
4. Run `make investigations`.
5. Repair the requirement, not merely the diagnostic.
6. Compare your repair with both the principled and weak repairs in the manifest.

## Case catalog

| ID | Module | Category | Question |
|---|---:|---|---|
| `m01-c01` | 1 | `typecheck-pass` | Runtime version remains a string |
| `m01-c02` | 1 | `typecheck-fail` | Runtime string assigned to a number |
| `m01-c03` | 1 | `typecheck-pass` | Satisfies checks a package-shaped value |
| `m01-c04` | 1 | `typecheck-fail` | Type-only import used as a runtime value |
| `m01-c05` | 1 | `typecheck-pass` | Type annotations erase before execution |
| `m01-c06` | 1 | `run-fail` | Unsafe assertion at an external boundary |
| `m01-c07` | 1 | `typecheck-pass` | Top-level await in an ESM module |
| `m01-c08` | 1 | `typecheck-fail` | Nonexistent named Node export |
| `m02-c01` | 2 | `typecheck-pass` | Restricted decimal parsing |
| `m02-c02` | 2 | `typecheck-fail` | String concatenation mistaken for arithmetic |
| `m02-c03` | 2 | `typecheck-pass` | Object.is exposes special number semantics |
| `m02-c04` | 2 | `run-fail` | Unchecked property after null JSON |
| `m02-c05` | 2 | `typecheck-fail` | Indexed access can be absent |
| `m02-c06` | 2 | `typecheck-pass` | Guarded indexed access |
| `m02-c07` | 2 | `typecheck-fail` | Truthiness does not choose a union member |
| `m02-c08` | 2 | `typecheck-pass` | Explicit total control flow |
| `m03-c01` | 3 | `typecheck-pass` | Closure owns private mutable state |
| `m03-c02` | 3 | `typecheck-fail` | Callback result contract mismatch |
| `m03-c03` | 3 | `typecheck-pass` | Explicit receiver method |
| `m03-c04` | 3 | `run-fail` | Extracted method loses its receiver |
| `m03-c05` | 3 | `typecheck-fail` | Implicit this is not a contract |
| `m03-c06` | 3 | `typecheck-pass` | Explicit this parameter |
| `m03-c07` | 3 | `typecheck-fail` | Variable may be used before assignment |
| `m03-c08` | 3 | `typecheck-pass` | Bounded callback invocation |
| `m04-c01` | 4 | `typecheck-pass` | Readonly public object view |
| `m04-c02` | 4 | `typecheck-fail` | Mutation through readonly field |
| `m04-c03` | 4 | `typecheck-pass` | Aliases observe the same object |
| `m04-c04` | 4 | `run-fail` | Shallow copy does not isolate nested state |
| `m04-c05` | 4 | `typecheck-fail` | Readonly array passed to mutating API |
| `m04-c06` | 4 | `typecheck-pass` | Path-local immutable update |
| `m04-c07` | 4 | `typecheck-fail` | Unchecked array element mutation |
| `m04-c08` | 4 | `typecheck-pass` | Freeze is shallow at runtime |
| `m05-c01` | 5 | `typecheck-pass` | Exhaustive discriminated union |
| `m05-c02` | 5 | `typecheck-fail` | State-specific field without narrowing |
| `m05-c03` | 5 | `typecheck-pass` | Unknown narrowed by a runtime guard |
| `m05-c04` | 5 | `typecheck-fail` | Property access on unknown |
| `m05-c05` | 5 | `typecheck-pass` | Literal preservation with satisfies |
| `m05-c06` | 5 | `typecheck-fail` | Missing union branch reaches assertNever |
| `m05-c07` | 5 | `typecheck-fail` | Broad string is not a closed vocabulary |
| `m05-c08` | 5 | `run-fail` | Assertion allows impossible runtime state |
| `m06-c01` | 6 | `typecheck-pass` | Generic key index preserves relationships |
| `m06-c02` | 6 | `typecheck-fail` | Generic result unrelated to input |
| `m06-c03` | 6 | `typecheck-fail` | Map lookup remains optional |
| `m06-c04` | 6 | `run-fail` | Duplicate-key policy is observable |
| `m06-c05` | 6 | `typecheck-pass` | Stable sorted copy |
| `m06-c06` | 6 | `typecheck-fail` | Reduce accumulator type mismatch |
| `m06-c07` | 6 | `typecheck-pass` | Deterministic grouping order |
| `m06-c08` | 6 | `typecheck-pass` | Generic predicate keeps element type |
| `m07-c01` | 7 | `typecheck-pass` | Explicit JavaScript import specifier |
| `m07-c02` | 7 | `typecheck-fail` | Extensionless relative ESM import |
| `m07-c03` | 7 | `typecheck-pass` | Type-only module edge |
| `m07-c04` | 7 | `typecheck-fail` | Type-only name used at runtime |
| `m07-c05` | 7 | `typecheck-fail` | Named export has no default |
| `m07-c06` | 7 | `typecheck-pass` | Re-exported public surface |
| `m07-c07` | 7 | `run-pass` | Live ESM binding |
| `m07-c08` | 7 | `typecheck-pass` | Circular initialization hazard avoided by contract |
| `m08-c01` | 8 | `typecheck-pass` | Unknown configuration validation |
| `m08-c02` | 8 | `typecheck-fail` | Unknown catch value property access |
| `m08-c03` | 8 | `run-fail` | Unsafe configuration assertion |
| `m08-c04` | 8 | `typecheck-pass` | Error narrowed before causal wrapping |
| `m08-c05` | 8 | `typecheck-fail` | Exact optional property rejects explicit undefined |
| `m08-c06` | 8 | `typecheck-pass` | Absent optional property omitted |
| `m08-c07` | 8 | `typecheck-fail` | Validation result requires narrowing |
| `m08-c08` | 8 | `typecheck-pass` | Collected validation issues |
| `m09-c01` | 9 | `run-pass` | Promise reaction ordering |
| `m09-c02` | 9 | `typecheck-fail` | Async function return annotation |
| `m09-c03` | 9 | `typecheck-fail` | Forgotten await changes the value type |
| `m09-c04` | 9 | `typecheck-pass` | Promise.all preserves tuple positions |
| `m09-c05` | 9 | `typecheck-pass` | Rejected top-level operation |
| `m09-c06` | 9 | `typecheck-pass` | AbortSignal is an explicit input |
| `m09-c07` | 9 | `typecheck-fail` | Callback API does not return a promise |
| `m09-c08` | 9 | `typecheck-pass` | Promise filesystem boundary |
| `m10-c01` | 10 | `typecheck-pass` | Dependency shape supports deterministic testing |
| `m10-c02` | 10 | `typecheck-fail` | Missing return path |
| `m10-c03` | 10 | `typecheck-pass` | Fake implements the real boundary |
| `m10-c04` | 10 | `run-fail` | Test oracle detects a violated invariant |
| `m10-c05` | 10 | `typecheck-fail` | Mock has the wrong asynchronous signature |
| `m10-c06` | 10 | `typecheck-pass` | Exhaustive application result |
| `m10-c07` | 10 | `typecheck-fail` | Readonly dependency cannot be replaced |
| `m10-c08` | 10 | `typecheck-pass` | Orchestration preserves effect order |
