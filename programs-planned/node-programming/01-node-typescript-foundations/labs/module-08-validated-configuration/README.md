# Laboratory 8 — Validated Configuration

## Product and purpose

Configuration is external data even when it was written by a developer. This lab builds a decoder that accumulates useful independent issues and constructs one trusted value only after all required facts hold.

## Entry standard

Reconstruct the trust pipeline from JSON text to `unknown`, root shape, field checks, cross-field rules, and final construction. Predict the Module 8 cases and decide which independent issues can be collected together. The starter includes the target type and a minimal result shape; it provides no evidence that external values satisfy either.

## Public contract

The root is a non-null non-array object. Mode is scan or rewrite; concurrency is 1–32; maxInputBytes is 1–100,000,000; logLevel is a closed vocabulary; outputDirectory is required and nonempty only in rewrite mode. Unknown keys are errors. JSON syntax failure is separate from validation failure.

## Required construction sequence

Implement small shape and numeric predicates, deterministic path-aware issue collection, cross-field outputDirectory policy, and final construction. Test multiple simultaneous issues, null, arrays, unknown keys, valid scan without directory, valid rewrite with trimmed directory, and malformed JSON with preserved cause.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Use malformed JSON, `null`, arrays, missing keys, explicit `undefined` in trusted calls, wrong primitive types, out-of-range numbers, multiple independent field failures, unknown root and nested keys, and mode-dependent directory errors. Verify deterministic issue order and causal syntax errors while ensuring no partial configuration escapes on failure.

## Prohibited shortcuts

Do not return a partial Config, default invalid fields, use `as ProcessorConfig`, throw for each ordinary issue, or stop at the first independent field error. Do not report child paths after the root prerequisite has failed.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when malformed JSON, structural defects, field-domain defects, and cross-field defects remain distinct; issue paths and order are deterministic; unknown keys follow the stated policy; and only a fully validated fresh object becomes `ProcessorConfig`. Compare the dependency order of checks with the reference rather than copying helper names.

## Independent transfer

Add a nested retry object with bounded attempts and delay. Preserve paths such as `retry.attempts`, reject unknown nested keys, and keep the main validator decomposed.

Draw the nested validation dependency tree. Define issue order, unknown-key policy, mode interactions, and final construction before adding fields; tests should show that an invalid retry object never produces a partial trusted value.
