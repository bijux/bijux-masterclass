# Final Defense

The defense is a 45–60 minute technical review built around the Atlas Host Runtime rather than trivia.

## Part 1 — Normal causal path

Trace one verified client request from name resolution through route selection, TLS, HTTP authority, edge forwarding, API acceptance, filesystem transition, worker claim, result publication, and client retrieval. Name the owner and decisive evidence at every boundary.

## Part 2 — Failure diagnosis

The examiner selects two controlled faults from different domains, such as:

- worker termination after claim;
- read-only durable path;
- listener bound to the wrong address;
- wrong certificate name;
- backend connection failure;
- stale cloud metadata assumption.

Before changing the system, predict the first oracle. Preserve evidence, diagnose, repair, rerun focused proof, and verify cleanup.

## Part 3 — Replacement and recovery

Explain reboot, stop/start, termination, and replacement as distinct events. Present image identity, boot/config source, durable-state source, workload identity, route admission, rollback, and old-instance decommission evidence. A local-only learner must state which Class D observations remain unexecuted.

## Part 4 — Architecture judgment

Defend one decision that deliberately avoids a fashionable abstraction: for example, why Course 1 does not begin with Kubernetes, why the Python edge is only a semantic fixture, or why a multi-zone compute diagram does not prove zone tolerance.

## Part 5 — Course 2 handoff

Select three `PE-CF-*` requirements. Explain how Course 2 can translate each to cloud resources without changing its behavioral meaning, and which live evidence will be required.
