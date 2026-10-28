# Glossary — Event-Driven API Engineering

These terms have precise meanings in Course 6. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## command

A request that an owner consider performing an action; it expresses intent and may be accepted or rejected.

## domain event

An immutable fact meaningful inside a domain model, named in the past tense and owned by the domain that established it.

## integration event

A stable, externally published fact intended for independent consumers rather than internal domain implementation.

## message envelope

The governed metadata surrounding a payload, including identity, type, source, time, subject, correlation, causation, partition, and schema version.

## producer

The component authorized to publish a particular message type and accountable for its semantic correctness.

## consumer group

A logical subscriber whose members share delivery work and one progression through each partition.

## partition

An ordered shard selected by a stable key; ordering claims generally hold only within one partition.

## offset

A broker or log position used to identify progression through a partition, not the business identity of an event.

## acknowledgement

A consumer’s signal that the current delivery attempt reached the required durable boundary and need not be redelivered.

## redelivery

A later attempt to deliver the same message identity after timeout, failure, negative acknowledgement, or consumer recovery.

## at-least-once

A delivery property in which a message may be delivered more than once, requiring consumers to tolerate duplicates.

## outbox

Durable publication intent committed atomically with the producer’s business state.

## inbox

Consumer-side durable state recording message/effect identities so duplicate deliveries do not duplicate effects.

## effect identity

A stable key representing the business effect produced by a message, often including consumer and effect-version context.

## replay

Intentional reprocessing of retained historical messages within a bounded scope and side-effect policy.

## upcaster

A deterministic read-time transformation that maps an older event shape into the current consumer model without rewriting history.

## event time

The time the represented fact occurred according to the producer’s domain, distinct from ingestion or processing time.

## watermark

An estimate of event-time completeness used to decide when a window may be emitted while allowing bounded lateness.

## late event

An event arriving after a window result has been emitted or after the allowed-lateness policy, requiring correction or quarantine.

## dead letter

A message placed into explicit operational custody after bounded retries or permanent failure, together with reason and recovery metadata.
