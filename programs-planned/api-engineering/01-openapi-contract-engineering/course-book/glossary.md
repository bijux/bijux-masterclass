# Glossary — OpenAPI Contract Engineering

Use this glossary alongside `program-book/glossary.md`. Program terms keep one meaning across all six courses; the entries below add course-specific distinctions.

Terms are defined as used in this program. When an Internet or OpenAPI specification gives a narrower normative meaning, the chapter and standards page name it.

## API contract

The reviewed set of client-observable operations, inputs, outputs, errors, security requirements, and compatibility commitments.

## OpenAPI Description

A document or connected document set conforming to the OpenAPI Specification and describing an HTTP API.

## OpenAPI version

The specification version used to interpret the description, such as 3.1.2 or 3.2.0; it is not the public API version.

## Public API version

The release identity of the client-facing contract, such as API 1.1, governed by compatibility policy.

## Path Item Object

The OpenAPI object associated with one path template and containing operations or shared parameters.

## Operation Object

The OpenAPI object describing one HTTP operation, including parameters, request body, responses, security, callbacks, and metadata.

## operationId

A globally unique, consumer-facing operation identity often used by generators; renaming it can break clients.

## Parameter

Input carried in a path, query string, header, or cookie and described with explicit serialization rules.

## Request body

Content sent as the HTTP message body, described by requiredness, media type, schema, and examples.

## Representation

A media-type-specific expression of a resource or outcome carried in an HTTP message.

## JSON Schema dialect

The vocabulary and semantics used to interpret schema keywords; modern OpenAPI uses JSON Schema 2020-12-aligned behavior.

## Constraint

A schema rule limiting accepted instances, such as requiredness, length, range, pattern, or object closure.

## Composition

Logical schema combination through keywords such as allOf, anyOf, oneOf, and not; it is not object-oriented inheritance.

## Discriminator

Metadata helping select among schema alternatives; alternatives must still be logically valid and distinguishable.

## Reference

A URI-based pointer to another object or schema; resolution uses the containing document and base URI rules.

## Bundle

A deterministic derived description that resolves external document structure into a portable artifact without becoming editable source.

## Dereference

Replacement of references with target content; it can expand recursion and is not always appropriate for tools.

## Problem Details

The RFC 9457 media type and object shape for machine-readable HTTP error information.

## Idempotency key

A client-supplied identifier binding a retryable unsafe request to one logical outcome under a defined fingerprint and retention policy.

## ETag

An HTTP entity tag representing a selected representation version and used with conditional requests.

## Precondition

A condition such as If-Match that must hold before a mutation is applied.

## Conformance

Agreement between observed provider behavior and the canonical contract; document validity alone does not establish it.

## Mock

A contract-driven simulated provider useful for early consumer work but not proof of complete runtime behavior.

## Generated client

Consumer code derived from the contract; generation success does not prove runtime compatibility or correct ergonomics.

## Compatibility

Whether a proposed change preserves existing consumer assumptions, evaluated differently for requests and responses.

## Overlay

A separate ordered transformation document used to derive an audience-specific OpenAPI view without copying canonical source.

## Arazzo workflow

A machine-readable description of operation sequences and data dependencies required to achieve an API outcome.

## Callback

An outbound operation described within another operation and parameterized by runtime expressions.

## Webhook

An API-initiated event operation described independently of a specific inbound operation.

## Streaming representation

A response whose items arrive sequentially, such as server-sent events or JSON Lines, with framing and lifecycle semantics.
