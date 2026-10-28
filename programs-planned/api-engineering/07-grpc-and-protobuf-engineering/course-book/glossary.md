# Glossary — gRPC and Protobuf Engineering

These terms have precise meanings in Course 7. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## RPC

A remote invocation with request/response semantics whose network, deadline, retry, and compatibility behavior must remain explicit.

## service definition

The Protobuf declaration of named RPC methods, their input/output message types, and streaming shapes.

## message

A Protobuf record with numbered fields and wire-level evolution rules; it is not a language-specific class.

## field number

The stable numeric wire tag identifying a Protobuf field; once published, it must not be reused for a different meaning.

## presence

Whether the wire and generated API can distinguish “not provided” from a field’s default value.

## unknown field

A wire field not recognized by the current schema version; preserving it can be essential for compatible forwarding.

## oneof

A Protobuf construct expressing that at most one member of a group is selected, with presence represented by the selected case.

## binary compatibility

Whether old and new implementations can exchange Protobuf wire bytes without misparsing or losing required meaning.

## source compatibility

Whether generated language APIs continue compiling; it is different from wire compatibility.

## JSON mapping

The standardized textual representation for Protobuf messages, with its own names, number encodings, and compatibility risks.

## metadata

Per-call key-value context used for credentials, tracing, idempotency, and routing; it is separate from the typed message body.

## status code

The canonical gRPC outcome category carried in trailers, distinct from transport success and rich error details.

## rich error

A structured error status containing typed details that clients can interpret without parsing human text.

## deadline

The absolute time by which the caller no longer needs the RPC result and which should propagate through downstream work.

## cancellation

The termination signal associated with a no-longer-needed call or stream; handlers must release work and preserve valid durable state.

## retry policy

The bounded rules deciding whether and when a failed RPC attempt may be repeated without duplicating unsafe effects.

## streaming RPC

An RPC in which the client, server, or both send multiple messages over one call lifetime.

## flow control

HTTP/2 and application-level mechanisms that bound how much data a sender can have outstanding relative to receiver capacity.

## channel

A long-lived client-side abstraction managing connections, name resolution, balancing, and RPC creation.

## reflection

A runtime service exposing descriptors for inspection and tooling; it does not replace governed source schemas or release evidence.
