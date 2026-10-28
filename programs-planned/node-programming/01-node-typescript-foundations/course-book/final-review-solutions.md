# Final Review — Answer and Evaluator Guide

This guide provides the causal standard for the final review. It is not a single implementation key for the independent products.

## Part I — Reconstruction standard

A strong reconstruction distinguishes four artifacts: TypeScript source, the static relationships computed by the selected checker, emitted JavaScript, and a running Node process. It identifies npm/package metadata and operating-system behavior as separate authorities rather than calling all of them “JavaScript.”

The numeric pipeline must validate accepted text before conversion and domain range after conversion. The equality answer must mention NaN and signed zero. The closure answer must distinguish captured binding from snapshot. The receiver answer must tie `this` to invocation form.

The identity graph must show that assignment copies an object reference, spread creates a new outer object, and nested identities remain shared until copied. The union answer must include runtime validation because static variants cannot validate JSON.

The collection answer should choose based on order, duplicates, key lookup, and membership rather than preference. A valid generic example connects input and output positions. The module graph must distinguish type-only edges and live bindings.

The trust pipeline ends with constructing a new trusted domain value, not asserting the parsed object. The promise graph must assign an observer to every started operation. The StudyLedger graph must place process, application, domain, storage, and rendering responsibilities in one direction.

## Part II — Prediction standard

A correct classification without a rule earns partial credit. The rule must explain the outcome independently of exact diagnostic wording. For runtime cases, the answer should predict actual output or failure point. For repairs, casts to `any`, double assertions, non-null assertions without proof, disabled strict flags, swallowed rejections, and catch-all fallbacks are weak unless the product explicitly permits them.

## Part III — Clinic answers

### A — false static confidence

`JSON.parse` yields a runtime value with no established Config invariant. The repair parses to unknown, checks a non-null object, validates `output`, validates `directory`, rejects unknown keys under the selected policy, and constructs a new Config. Tests include null, missing output, null output, wrong directory type, empty directory, unknown field, valid input, and malformed JSON. An assertion is not retained.

### B — hidden alias mutation

Top-level spread creates a new inventory object but reuses the items array and item identities. Mutating `inventory.items[0]` changes every alias. The repair validates ID and stock result, maps the array, creates one changed item, preserves untouched item identities, and returns a new inventory. A missing ID throws before publication; the original graph remains unchanged.

### C — unowned asynchronous work

The command claims persistence before the save completes, cannot report rejection reliably, may let the process end or continue unpredictably, and exposes success while the file remains old. The repair awaits save in the application layer and returns success only afterward. Main awaits the application and sets exit status. Tests use a rejecting fake and a real process lifecycle.

### D — graph mismatch

The likely defect is an extensionless relative import under NodeNext ESM. Confirm the local compiler and effective configuration, inspect the emitted import, ensure `package.json` says module, and change source to `./command.js`. Editor-only resolution is not Node evidence.

### E — overbroad catch

Only an `ENOENT` read error means initial empty state under the selected policy. Permission and other I/O errors become StorageIoError. JSON syntax becomes validation syntax error. Valid JSON with invalid schema becomes path-aware validation error. A catch-all fallback can later overwrite damaged or inaccessible data with an empty ledger, destroying evidence.

## Part IV — Expense Note review

Acceptable architectures vary, but the following responsibilities must remain visible:

- command parser owns tokens and exact cents grammar;
- domain owns IDs, categories, amounts, removal, and summary;
- codec owns unknown-data validation and format version;
- storage owns file effects;
- application owns use-case order;
- main owns process streams/status.

Amounts should remain integer cents. A floating-point dollar model loses the exercise’s exactness. Summary ordering and category normalization must be explicit. Missing-file behavior must not swallow other failures.

Minimum evidence includes parser boundary tests, immutable update tests, duplicate/malformed codec fixtures, temporary-directory load/save tests, save-before-success application tests, and one multi-command process test.

## Part V — StudyLedger change review

### Rename

Usually compatible with V1 because topic already exists. It needs command grammar, exact topic validation, domain update, application dispatch, help, and tests. Codec shape remains the same. The change should preserve ID, timestamps, status, and terminal detail.

### Reopen

Compatibility depends on policy. If terminal history is discarded and the resulting value is an ordinary planned session, V1 can represent it. If history must remain attached, the current union and format need new fields or a V2 event/history model.

### Labels

Strict unknown-key decoding means adding a new persisted field changes the accepted schema. V2 is the clean choice unless labels are stored outside sessions under an explicitly optional compatibility design. Define normalization, duplicate behavior, order, and matching.

### Date-range summary

No storage change is necessary if it derives from existing timestamps. The product must define which timestamp is selected per state, inclusive/exclusive bounds, UTC conversion, and invalid range behavior. Injecting current time is unnecessary unless relative ranges such as “last week” are supported.

## Part VI — Oral-defense key points

1. Interfaces, aliases, generic relationships, and narrowing facts are static; objects, strings, promises, errors, files, and process streams are runtime.
2. Assertion changes checker belief only.
3. TypeScript source describes emitted ESM paths.
4. Readonly blocks writes through one static view; other aliases may mutate.
5. Domain transition functions own legality.
6. JSON syntax says nothing about domain validity.
7. Load and save promises are awaited by application; main awaits application.
8. Summary is a pure read and requires no current-time fact.
9. Temporary replacement avoids ordinary partial visible JSON during successful single-process save; it does not prove durability or concurrent-writer correctness.
10. ENOENT has a named empty-ledger policy; other failures preserve evidence.
11. Application test with rejecting save and process test for nonzero status.
12. Paths, permissions, rename semantics, error wording, locale, and clocks can be platform conditioned.
13. Public entry exposes deliberate domain/application/storage contracts; temp names and environment selection remain private.
14. Any feature requiring new persisted meaning not representable by current strict V1 shape.
15. Lost updates and last-writer-wins replacement.

## Evaluation cautions

Do not award full credit for framework vocabulary, file-count complexity, or copied StudyLedger names. Reward accurate runtime/static separation, explicit authorities, preserved failure information, and evidence that can falsify the claim.

## Distinguishing strong, partial, and weak answers

A **strong answer** names the authority and causal mechanism. For example: “`saveLedger` returns a promise; `runCommand` awaits it before returning the success text; `main` awaits `runCommand` and maps rejection to exit status.” This can be tested and falsified.

A **partial answer** names a preferred pattern without the reason: “always await saves.” It may guide a repair but does not show that the reader can trace ownership or decide when concurrency is appropriate.

A **weak answer** uses vocabulary as a substitute for analysis: “the code is type safe,” “ESM handles it,” “immutability prevents bugs,” or “integration tests prove the application.” These claims are too broad until the exact types, resolver contract, identities, or test boundaries are stated.

## Common scoring errors

Do not over-reward extra abstraction. More interfaces, factories, folders, or generic parameters can make a Course 1 product harder to reason about. Award design credit when a boundary removes a real source of nondeterminism, isolates an external effect, preserves a relationship, or curates a public contract.

Do not penalize a clear loop merely because an iterator chain exists. The reader should choose the form that makes order, short-circuiting, accumulation, and failure visible. Functional pipeline architecture is developed in a later course.

Do not accept snapshot-style tests that merely repeat implementation output. A valuable test states a contract: invalid transition, duplicate field, preserved identity, awaited save, stable ordering, or nonzero process exit. Snapshot testing can be introduced later when its review and update policy is explicit.

## Repair decisions after the review

| Failure pattern | Required repair before Course 2 |
|---|---|
| confuses annotation or assertion with validation | rebuild one decoder from unknown and explain every check |
| cannot predict aliasing after spread/destructuring | redraw three heap graphs and add identity assertions |
| cannot assign an observer to each promise | rewrite one workflow sequentially and concurrently, then compare ownership |
| relies on editor-only imports | run emitted ESM under Node and document the resolution chain |
| catches all storage failures as empty state | restore causal error classes and test permission/malformed cases |
| independent feature changes only one layer | redo the impact map and trace compatibility, help, rendering, and process evidence |

The purpose of remediation is not to increase the numerical score. It is to restore a prerequisite relationship the next course will depend on.
