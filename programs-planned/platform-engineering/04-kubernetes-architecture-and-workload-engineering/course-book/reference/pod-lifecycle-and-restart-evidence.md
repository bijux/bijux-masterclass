# Pod lifecycle and restart evidence

A Pod is a scheduling and shared-fate boundary, not a durable machine. Diagnosing it requires separating object phase, container state, conditions, restarts, and controller replacement.

## Container states

A container is waiting, running, or terminated. The current state can be running while `lastState` records an OOM termination. Restart count is cumulative for the container in that Pod incarnation.

Common termination evidence includes exit code, signal, reason, start/finish times, and message. Application logs may disappear across restart unless previous logs or external collection are preserved.

## Pod conditions

Important conditions include scheduling, initialization, readiness, and containers ready. Custom readiness gates can require controller-owned conditions. A Pod can be Running while `Ready=False`.

## Backoff

Repeated container failure increases restart delay. Deleting the Pod resets the Pod identity and backoff history but does not repair the failing template. This can make an incident look temporarily better while increasing churn.

## Node loss and unknown state

The control plane may not know immediately whether a process on an unreachable Node is still running. Controllers must handle delayed certainty. Workloads that produce external effects need fencing or idempotency beyond Pod identity.

## Evidence sequence

Record Pod UID, Node, phase, conditions, each container current and last state, restart count, image ID, resource limits, probes, events, and controller owner. Only then decide whether restart, replacement, rescheduling, or desired-state change matches the failure.
