# Lab — Build the Analysis Events message taxonomy

## Objective

Convert the inherited Analysis Runs workflow into a minimal, owned asynchronous interface without selecting a transport as the design driver.

## Setup conditions


1. Run `make predecessor-proof` and preserve API 1.2 and profiles 1.0.
2. Read `capstone/event-case/message-taxonomy.yaml` and the Course 5 workflow identities.
3. Select one user journey: run submission through artifact publication.
4. Create `work/module-01/` with the decision-journal files from `start-here.md`.
5. Do not start NATS or edit the AsyncAPI document during the first pass.


## Failure action and investigation


Draw the workflow as synchronous calls, internal commands, domain transitions, integration events, queries,
and notifications. For every proposed public event, write its fact, authoritative owner, durable proof,
legitimate consumers, retention need, subject, correlation, causation, and partition identity.

Plant two deliberately bad candidates: one imperative “event” and one row-change message. Run a peer or
self-review that rejects them for named reasons. Update the taxonomy and catalogue only after the review.


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


## Cleanup and reset


Revert the two rejected candidates, remove temporary channels, and reset generated reports. Keep the final
decision record and catalogue changes. Confirm that the predecessor handoff remains byte-identical.


## Completion gate


The lab passes only when every public event has one owner, one durable oracle, a stable fact-oriented name,
explicit identities, a consumer rationale, and a rejection explanation for the synchronous alternative.
“The broker can do it” is not accepted as evidence.
