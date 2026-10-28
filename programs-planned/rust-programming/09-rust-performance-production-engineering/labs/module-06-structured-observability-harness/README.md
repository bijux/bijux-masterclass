# Laboratory 86 — Structured Observability Harness

**Course 9 · Module 86: Observability: Structured Tracing, Metrics, and Diagnostic Context**

[Chapter](../../course-book/module-86-observability-structured-tracing-metrics-and-diagnostic-context/index.md) · [Workbook](../../course-book/module-86-observability-structured-tracing-metrics-and-diagnostic-context/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Observability: Structured Tracing, Metrics, and Diagnostic Context**: What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally? The product must make **Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **signal dictionary** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a small request-decision component whose telemetry can answer a bounded set of operator questions without exposing a secret. The product returns a typed `Event`, records stable outcome metrics, and emits structured tracing fields. It is deliberately small enough that every signal can be reviewed.

The scenario has one request ID, one bounded operation name, a `Secret`, and an overload decision. A request is either accepted or rejected because capacity is unavailable. The event must preserve correlation and outcome while the secret remains usable by domain logic but redacted from diagnostics.

## Signal contract

Use a closed `Outcome` enum and a stable `as_str` mapping. `Event` should carry:

- stable event name;
- request correlation ID;
- bounded operation;
- typed outcome;
- numeric bounded fields such as queue depth.

`Metrics` counts outcomes by the closed vocabulary. It must not create labels from request ID, secret content, tenant, path, or free-form error text.

The `Secret` type owns the sensitive value. Its `Debug` representation must be redacted. Any method that exposes the value should be explicit and used only at the domain boundary. Returning a redacted wrapper while separately storing the raw value in `Event` does not satisfy the contract.

## Construction route

1. Define the operator questions: Was the request accepted? Was overload the cause? Which operation? Which request trace should be inspected?
2. Define the closed outcome vocabulary before writing messages.
3. Implement the secret wrapper and redacted formatting.
4. Create a request span with stable fields and record the final outcome.
5. Emit a bounded event for the decision.
6. Update aggregate metrics from the typed event rather than reparsing text.
7. Test stable field values, outcome counts, and secret absence.

## Tests that matter

Inject a sentinel such as `DO-NOT-LOG-THIS`. Format the `Secret`, event, and any public error path; capture tracing output if your design permits; assert the sentinel never appears. Test every `Outcome` maps to one stable string. Record multiple events and verify exact counts.

Avoid brittle tests that assert a full human sentence when prose is not part of the public schema. Test event name, fields, codes, and redaction boundaries instead.

## Cardinality review

For each event or metric field, list the maximum number of values. `operation` and `outcome` should be bounded by code. Request IDs are acceptable trace correlation fields under controlled retention, but not metric labels. Queue depth is a numeric observation, not a label. Explain what would happen if a full error message were used as a label.

## Adversarial cases

Test accepted and overloaded outcomes, several operation values, secret strings containing quotes/newlines, zero and large request IDs, and repeated events. Ensure secret redaction is stable even through derived debug output on containing types.

## Transfer

Add a third typed outcome for invalid input and a bounded error code. Decide which context belongs in the aggregate metric and which belongs in the event. Preserve the rule that raw input is never recorded.

## Completion

The laboratory is complete when an operator can distinguish outcome classes and correlate a request, metrics have bounded cardinality, secrets are redacted by type design, and tests protect the schema without coupling to incidental prose.

Inspect `solution/` only after writing your own signal contract. Compare authority, cardinality, and redaction. More emitted fields are not automatically more observable.

## Operational-question test

Define five questions an operator should be able to answer, such as: Which stage is slow? Is overload causing rejection? Is one tenant responsible for retained series growth? Did a snapshot finish writing? Are invalid records increasing? For each question, list the exact span fields, metrics, or structured events required and the aggregation that produces the answer.

Add tests or a capture harness proving that success, invalid input, capacity rejection, internal failure, and completed snapshot transmission emit distinct evidence. Check units, monotonicity, terminal-event timing, and field cardinality. Deliberately inject one secret-like value and prove it does not appear in logs or metric labels. The observability design is incomplete if it can describe a request but cannot reconstruct its terminal outcome.

## Cost and failure review

Measure the instrumentation path under disabled, human-readable, and structured-output configurations. Record event volume, bytes emitted, and any measurable latency change under the same workload. Then break the subscriber or output sink deliberately and state whether application work continues, blocks, or fails. The chosen behavior must be explicit. Diagnostic generation may be lossy under a declared policy, but it may not create unbounded memory growth or silently alter domain results.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Structured Observability Harness**.
2. Draw the smallest **signal dictionary** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer.
- Design stable event names and fields that preserve causal context across async and threaded work.
- Choose metric types and label sets without creating unbounded cardinality.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 86 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **signal dictionary**. Defend why your design is simpler than one plausible alternative under the new requirements.
