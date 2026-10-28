# Ten-Day Study Plan

This course is designed for two calendar weeks: five dense study days, one repair Saturday, one rest Sunday, then five more study days. The schedule assumes roughly eight to ten focused hours per instructional day. Shorten individual blocks when concentration drops; do not remove prediction, independent construction, or reconstruction.

## Daily rhythm

| Time | Work |
|---|---|
| 08:30–09:00 | Closed-book retrieval from the previous day |
| 09:00–10:30 | First half of the authoritative chapter; run only the smallest examples |
| 10:45–12:00 | Finish the chapter; build the day’s reasoning table or diagram |
| 13:00–14:00 | Predict the eight investigation cases before using tools |
| 14:00–15:00 | Run, diagnose, and repair incorrect predictions |
| 15:15–17:15 | Independent laboratory construction |
| 17:30–18:45 | StudyLedger increment |
| 19:30–20:15 | Tests, comparison against contract, and solution review |
| 20:15–20:30 | Write retrieval prompts and one remaining uncertainty |

The evening block should not become another reading session. Produce executable evidence or reconstruct the model.

## Day 1 — Runtime, toolchain, and ESM

**Morning:** Build the four-artifact model: TypeScript source, static program, emitted JavaScript, running process. Inspect package metadata and strict compiler configuration. Trace one `.js` import from source to ESM resolution.

**Afternoon:** Predict Module 1 investigations. Complete Runtime Report. Intentionally introduce a missing extension, type-only import defect, and runtime assertion failure, then identify the phase that owns each.

**Capstone:** Establish StudyLedger’s package, ESM entry, library entry, help, version, and first process test.

**Exit evidence:** a source-to-process diagram and a clean explanation of why type stripping is not type checking.

## Day 2 — Values, coercion, and invariants

**Morning:** Build an acceptance–conversion–domain table for numbers. Predict truthiness, `||`, `??`, equality, `NaN`, safe integers, and Unicode length measures.

**Afternoon:** Complete Usage Quote Policy. Use table-driven tests to expose accidental conversion. Rewrite one nested parser into guard clauses whose successful path has a named invariant.

**Capstone:** Add exact ID, planned-minute, actual-minute, topic, note, and reason normalization policies. Keep raw tokens out of the domain.

**Exit evidence:** the complete accepted language for each numeric token and a defense of zero/missing distinction.

## Day 3 — Functions, closures, callbacks, and receivers

**Morning:** Fill a callable contract ledger: timing, count, order, retention, concurrency, failure, receiver. Trace closure binding capture and method extraction.

**Afternoon:** Complete Callback Budget. Record exact callback sequences, not only final results. Rewrite an async `forEach` once sequentially and once with aggregate ownership.

**Capstone:** Inject clock, load, and save functions at the application boundary. Test call count and effect order.

**Exit evidence:** a receiver invocation table and an explanation of why callback types do not encode invocation policy.

## Day 4 — Identity, aliasing, and updates

**Morning:** Draw heap graphs for nested objects and arrays. Compare mutation, shallow copy, structural sharing, freezing, and serialization.

**Afternoon:** Complete Inventory Transform. Assert both semantic values and `===` identity behavior. Build a failure case that proves the original graph remains unchanged.

**Capstone:** Implement immutable session transitions and retain prior ledgers in tests.

**Exit evidence:** before/after identity diagram for one nested update and a candidate-publication explanation.

## Day 5 — Domain modeling and narrowing

**Morning:** Replace optional-field state bags with discriminated unions. Practice narrowing unknown values and audit a deliberately dishonest type predicate.

**Afternoon:** Complete Review Workflow. Add a temporary fifth state and use compiler failures to locate policy surfaces; then implement the state properly.

**Capstone:** Finalize planned, active, completed, and abandoned session variants and exhaustive rendering.

**Exit evidence:** transition graph, legal function signatures, and hostile cases that static types cannot reject at the JSON boundary.

## Repair Saturday

Do not add new content. Rebuild one earlier lab from its README in a fresh directory. Complete forty mixed investigations. Rewrite every mistaken prediction as a corrected rule. Reconstruct StudyLedger’s current dependency graph and remove any layer violation.

A useful Saturday output is a two-page “JavaScript and TypeScript facts I previously conflated” note.

## Rest Sunday

No new module. Light review is optional. The purpose is consolidation, not accumulating more pages.

## Day 6 — Collections, iteration, and generics

**Morning:** Choose collections from operations. Create stage tables for adapter chains and prefix invariants for reductions. Review order, duplicate policy, and mutation.

**Afternoon:** Complete Record Query. Test duplicate positions, narrowed published results, source order, and generic type preservation.

**Capstone:** Add list, search, and summary with stable ID ordering and explicit case behavior.

**Exit evidence:** collection decision table and a summary prefix invariant.

## Day 7 — Modules, packages, and public APIs

**Morning:** Trace ESM linking, evaluation, live bindings, and cycles. Review package entry points and top-level side effects.

**Afternoon:** Complete Package Boundary. Test public behavior through the entry module and inspect export metadata. Break one artificial cycle.

**Capstone:** Curate `src/index.ts`, mark type-only edges, and verify domain code imports no Node APIs.

**Exit evidence:** runtime/type-only module graph and a statement of which paths are supported API.

## Day 8 — Errors, validation, and persistence

**Morning:** Build the trust pipeline from text to unknown value to validated domain. Design path-aware issues and error-cause boundaries. Discuss version changes before coding them.

**Afternoon:** Complete Validated Configuration. Challenge it with multiple independent failures and malformed JSON.

**Capstone:** Implement V1 decoding, canonical encoding, missing-file policy, and same-directory replacement. Add hostile fixtures.

**Exit evidence:** validation dependency tree and the strongest accurate save-semantics claim.

## Day 9 — Promises, event-loop ordering, CLI, and files

**Morning:** Trace basic stack/microtask/timer behavior, promise ownership, sequential and concurrent starts, abort signals, and process exit.

**Afternoon:** Complete Async File Index. Ensure every started promise has one owner and final output is sorted independently of completion order.

**Capstone:** Implement command grammar, real async repository, process binding, streams, and exit statuses. Run the complete lifecycle as a child process.

**Exit evidence:** promise ownership graph and process contract table.

## Day 10 — Testing, architecture, and independent change

**Morning:** Build an evidence matrix. Review test isolation, temporary resources, fakes, interaction assertions, invariant tests, and architectural direction.

**Afternoon:** Complete Reading Ledger from its product contract. Do not copy StudyLedger modules. Then complete the final review.

**Capstone:** Choose one independent feature, write an impact map, implement it, and defend compatibility.

**Exit evidence:** a working independent product, an oral defense, and a written list of non-contracts.

## After the ten days

Run the complete proof route from a clean checkout. Revisit the final review after one week without rereading the solutions first. Delayed reconstruction is stronger evidence than immediate familiarity.

## Managing a dense day without reducing it to page completion

The course is intentionally dense, but density is useful only when it produces retrievable models. Use three stopping rules:

1. **Stop reading when prediction quality collapses.** Recopying a paragraph is not recovery. Close the chapter, draw the relevant graph or table from memory, and compare it with the source.
2. **Stop coding when repairs become random.** Record the observed phase, actual value or diagnostic, violated contract, and next smallest experiment. Random edits train superstition.
3. **Stop a module when a hard dependency remains weak.** A clean laboratory with an unexplained assertion, cast, swallowed rejection, or shared mutable alias is not a pass.

Keep one notebook with four recurring artifacts:

```text
phase table       source -> checker -> emission -> resolver -> runtime -> product
value table       raw value -> conversion -> validation -> trusted value
identity graph    bindings -> object identities -> mutable paths
ownership graph   promise/effect -> owner -> terminal observation
```

These are not administrative records. They externalize reasoning that otherwise disappears into intuition.

## Using the references and solutions correctly

The reference desk is for recall after you have learned a concept, not for replacing the chapter. The solution set is for causal comparison after you have produced a complete attempt. A useful comparison records three things:

- what your design got right;
- what hidden assumption the reference exposes;
- which difference is merely stylistic and should not be copied.

Never rewrite a working independent solution simply to resemble the reference. The goal is to preserve the product contract with explainable boundaries, not to converge on one file layout.

## Delayed retention route

One week after Day 10, complete this ninety-minute check without rereading:

1. draw the source-to-process and JSON-to-domain pipelines;
2. predict one closure, aliasing, union, ESM, and promise case;
3. implement a small decoder from `unknown`;
4. explain why success belongs after an awaited save;
5. outline the architecture of a persistent CLI unrelated to StudyLedger.

Return only to the concepts that fail this check. Delayed retrieval is a stronger signal than immediate familiarity at the end of a ten-hour day.
