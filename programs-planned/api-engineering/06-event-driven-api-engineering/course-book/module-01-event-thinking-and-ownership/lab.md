# Lab — Build the Analysis Events message taxonomy

> **Module 01:** Event Thinking, Ownership, and Message Taxonomy

## Objective

Convert the inherited Analysis Runs workflow into a minimal, owned asynchronous interface without selecting a transport as the design driver.

## Why this lab matters

This lab turns the module’s governing question—**Which interactions are commands, immutable facts, queries, notifications, or private domain events, and who owns each public fact?**—into a falsifiable experiment. The event id identifies one immutable occurrence. subject identifies the domain resource the fact concerns, such as analysis-runs/run-123. correlationid groups a wider user or business journey. causationid identifies the command or event that directly caused this event. partitionkey determines the ordering domain used by the transport.

It advances the cumulative Analysis Runs Platform by requiring this result: **Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Run `make predecessor-proof` and preserve API 1.2 and profiles 1.0.
2. Read `capstone/event-case/message-taxonomy.yaml` and the Course 5 workflow identities.
3. Select one user journey: run submission through artifact publication.
4. Create `work/module-01/` with the decision-journal files from `start-here.md`.
5. Do not start NATS or edit the AsyncAPI document during the first pass.

## Hypothesis

The clean implementation should satisfy this claim: **The final catalogue contains only facts with one owner and at least one defensible independent consumer. Commands have one logical handler and remain distinguishable from facts. No public payload contains a database row, ORM object, lease token, stack trace, access token, or raw dataset content. The proposed partition key matches the smallest domain requiring order.** When the lab introduces this fault—**Plant two deliberately bad candidates: one imperative “event” and one row-change message**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Draw the workflow as synchronous calls, internal commands, domain transitions, integration events, queries,
and notifications. For every proposed public event, write its fact, authoritative owner, durable proof,
legitimate consumers, retention need, subject, correlation, causation, and partition identity.

Plant two deliberately bad candidates: one imperative “event” and one row-change message. Run a peer or
self-review that rejects them for named reasons. Update the taxonomy and catalogue only after the review.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant two deliberately bad candidates: one imperative “event” and one row-change message**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Convert the inherited Analysis Runs workflow into a minimal, owned asynchronous interface without selecting a transport as the design driver**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The final catalogue contains only facts with one owner and at least one defensible independent consumer.
Commands have one logical handler and remain distinguishable from facts. No public payload contains a
database row, ORM object, lease token, stack trace, access token, or raw dataset content. The proposed
partition key matches the smallest domain requiring order.

## Required evidence

- `work/module-01/interaction-map.md`
- `work/module-01/publication-decisions.yaml`
- `work/module-01/rejected-candidates.md`
- a diff for `message-taxonomy.yaml` and `event-catalog.yaml`
- output from `make module-proof MODULE=01 TRACK=$TRACK`
- one paragraph explaining which important interaction remains synchronous

## Interpretation and defense

1. Which state or effect is authoritative for **Event Thinking, Ownership, and Message Taxonomy**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant two deliberately bad candidates: one imperative “event” and one row-change message** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Revert the two rejected candidates, remove temporary channels, and reset generated reports. Keep the final
decision record and catalogue changes. Confirm that the predecessor handoff remains byte-identical.

## Completion gate

The lab passes only when every public event has one owner, one durable oracle, a stable fact-oriented name,
explicit identities, a consumer rationale, and a rejection explanation for the synchronous alternative.
“The broker can do it” is not accepted as evidence.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Event Thinking, Ownership, and Message Taxonomy**. A green command without the negative case and causal explanation does not satisfy this gate.
