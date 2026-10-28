# Glossary — OpenAPI Contract Engineering

These terms have precise meanings in Course 1. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## API contract

A machine-readable and human-reviewable statement of the requests a provider accepts, the responses it may return, and the meanings consumers may rely on.

## operation

One method-and-path interaction in an HTTP API, with its parameters, request bodies, responses, security requirements, and stable identity.

## resource

A conceptual entity or collection addressed through the API; it is not the same thing as a database row or framework model.

## representation

A concrete serialized view of a resource or result, selected through a media type and shaped by a schema.

## media type

An identifier such as `application/json` that states the format and interpretation of a message body.

## parameter serialization

The rules that turn path, query, header, or cookie values into HTTP text and reconstruct typed values from that text.

## Schema Object

OpenAPI’s schema vocabulary for describing valid instances; in OpenAPI 3.1 and later it is aligned with JSON Schema dialect semantics.

## instance

The concrete JSON value, parameter value, or message being evaluated against a schema.

## operationId

A stable, unique identifier for an API operation used by tools, generated clients, links, workflows, and implementation maps.

## reference resolution

The process of locating the target of a `$ref` using the correct base URI and document context.

## bundle

A deterministic OpenAPI artifact in which externally split description fragments have been collected into a publishable document while preserving reference meaning.

## mock

A contract-driven substitute that returns described examples or generated values without proving that a real provider behaves the same way.

## conformance

Evidence that a provider or consumer behaves according to the contract for the interactions actually tested.

## compatibility

The effect of a contract change on existing producers and consumers, evaluated in the correct request or response direction.

## breaking change

A change that can cause a previously conforming consumer or provider to fail, reject data, misinterpret data, or lose a relied-upon behavior.

## Overlay

A separate OpenAPI Overlay document that applies ordered changes to a base description without copying and manually forking the whole contract.

## Arazzo

A specification for describing multi-step API workflows, including dependencies and values passed from one operation to another.

## callback

An outbound request whose destination is supplied or derived during an initiating API operation.

## webhook

An event-oriented inbound operation advertised by the API independently of one particular initiating request.

## provider

The running system that receives API requests and is responsible for satisfying the published contract.
