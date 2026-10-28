# Exercises — Module 02 — AsyncAPI, CloudEvents, and Contract Architecture

Use the actual AsyncAPI and schema artifacts. Answers must separate interface semantics from transport configuration.

## 1. Correct an operation direction

A document for the analytics consumer defines `action: send` on `AnalysisRunCompleted`. Correct it and explain the perspective rule.

## 2. Separate three identities

Propose a logical channel name, NATS subject, and CloudEvents type for completed runs. Explain which may change independently.

## 3. Design a message fragment

List the minimum fields a reusable `AnalysisRunFailed` message fragment must connect: name, envelope/profile, payload schema, example, and catalogue entry.

## 4. Validate in layers

An event has a valid payload but missing `tenantid`. Identify the failing layer and explain why payload validation is insufficient.

## 5. Choose a schema URI

Compare a relative filename, a mutable GitHub raw URL, and a stable versioned schema URI. Select the public `dataschema` and define offline resolution.

## 6. Close a public payload

Explain when `additionalProperties: false` is appropriate and when an explicit extension object is safer than a completely open schema.

## 7. Audit an example

A completion example contains a local filesystem path and a real bearer token. Describe all contract, security, and documentation failures.

## 8. Model a command and an event

Describe how `StartAnalysis` and `AnalysisRunStarted` differ in operation direction, handler cardinality, rejection semantics, and retention.

## 9. Define local proof scope

Write a truthful one-paragraph claim for a custom validator that checks references and examples but not every NATS binding rule.

## 10. Plan a multi-document layout

Choose which elements belong in the entry document, message fragments, payload schemas, examples, and event catalogue.

## 11. Protect operation identity

Explain why changing an operation ID can be breaking even when the channel address and payload schema stay the same.

## 12. Review a binding

A NATS channel binding includes queue-group and retention assumptions that are actually consumer deployment policy. Decide what belongs in the API description and what belongs in operations configuration.

## Submission format

Submit Module 02 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
