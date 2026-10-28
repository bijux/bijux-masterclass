# Lab — Build independent consumers and a durable run process

## Objective

Implement consumer ownership, effect separation, command-result discipline, durable timers, and duplicate-safe process transitions.

## Setup conditions


1. Use the validated event catalogue and deterministic broker.
2. Create groups/effect versions for notification, analytics, audit, and run process.
3. Prepare an event trace containing duplicate requested, started, completed, failed, artifact, and stale timeout facts.
4. Configure external notification capability as a recorded outbound intent, not a real provider call.
5. Create `work/module-06/process-table.md`.


## Failure action and investigation


Process the trace with all four consumers. Require analytics and audit to observe all relevant facts
independently. Require notification to create one intent. Run the process manager through requested,
start-requested, running, and completed.

Deliver a stale timeout after completion, a duplicate start fact, and artifact publication before
completion. Plant a defect that advances to running immediately after command publication and show the
state-machine proof rejects it.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How do idempotent consumers, projections, and process managers coordinate asynchronous workflows without hidden synchronous coupling?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state. A passing command without this causal explanation is insufficient.

## Operational oracle


Each consumer owns one effect and group. Duplicate facts do not repeat effects. Command publication leaves
the process in start-requested. Only authoritative facts advance state. Stale timer is a no-op with evidence.
Out-of-order artifact data does not invent run completion. No replay path sends an external notification.


## Required evidence


- `work/module-06/consumer-architecture.md`
- `work/module-06/process-table.md`
- `work/module-06/event-trace.json`
- final states for all four consumers
- command outbox and stale-timer evidence
- planted-defect rejection
- output from `make workflow-proof`


## Cleanup and reset


Remove the optimistic-command defect, reset all deterministic consumer states, cancel test timers, and clear
outbound intents. Preserve the state table, trace, and evidence.


## Completion gate


The lab passes only when independent effects remain independent, the process state is derived from
authoritative facts, timeout behavior is durable and generation-safe, and every duplicate/out-of-order input
has a defined result.
