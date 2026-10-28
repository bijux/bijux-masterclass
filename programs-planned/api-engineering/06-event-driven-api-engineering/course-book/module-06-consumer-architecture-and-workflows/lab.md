# Lab — Build independent consumers and a durable run process

> **Module 06:** Consumer Architecture and Asynchronous Workflows

## Objective

Implement consumer ownership, effect separation, command-result discipline, durable timers, and duplicate-safe process transitions.

## Why this lab matters

This lab turns the module’s governing question—**How do idempotent consumers, projections, and process managers coordinate asynchronous workflows without hidden synchronous coupling?**—into a falsifiable experiment. A process manager emits a command with stable command ID, target, subject, correlation, causation, and idempotency identity. The target either rejects it through a command-result channel or later emits an authoritative fact. The manager cannot update its state to “started” merely because it published StartAnalysis.

It advances the cumulative Analysis Runs Platform by requiring this result: **Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Use the validated event catalogue and deterministic broker.
2. Create groups/effect versions for notification, analytics, audit, and run process.
3. Prepare an event trace containing duplicate requested, started, completed, failed, artifact, and stale timeout facts.
4. Configure external notification capability as a recorded outbound intent, not a real provider call.
5. Create `work/module-06/process-table.md`.

## Hypothesis

The clean implementation should satisfy this claim: **Each consumer owns one effect and group. Duplicate facts do not repeat effects. Command publication leaves the process in start-requested. Only authoritative facts advance state. Stale timer is a no-op with evidence. Out-of-order artifact data does not invent run completion. No replay path sends an external notification.** When the lab introduces this fault—**Plant a defect that advances to running immediately after command publication and show the state-machine proof rejects it**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Process the trace with all four consumers. Require analytics and audit to observe all relevant facts
independently. Require notification to create one intent. Run the process manager through requested,
start-requested, running, and completed.

Deliver a stale timeout after completion, a duplicate start fact, and artifact publication before
completion. Plant a defect that advances to running immediately after command publication and show the
state-machine proof rejects it.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a defect that advances to running immediately after command publication and show the state-machine proof rejects it**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement consumer ownership, effect separation, command-result discipline, durable timers, and duplicate-safe process transitions**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **Consumer Architecture and Asynchronous Workflows**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a defect that advances to running immediately after command publication and show the state-machine proof rejects it** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove the optimistic-command defect, reset all deterministic consumer states, cancel test timers, and clear
outbound intents. Preserve the state table, trace, and evidence.

## Completion gate

The lab passes only when independent effects remain independent, the process state is derived from
authoritative facts, timeout behavior is durable and generation-safe, and every duplicate/out-of-order input
has a defined result.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Consumer Architecture and Asynchronous Workflows**. A green command without the negative case and causal explanation does not satisfy this gate.
