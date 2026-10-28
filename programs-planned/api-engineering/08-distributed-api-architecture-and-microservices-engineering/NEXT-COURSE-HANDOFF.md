# Course 8 → Course 9 handoff

Course 9 will introduce GraphQL as a governed graph-access layer over a distributed platform. It must not bypass service ownership, perform unbounded fan-out, or turn the gateway into a second domain model.

Course 8 therefore exports:

- the service catalogue and ownership map;
- public HTTP, event, and RPC interface references;
- query composition and staleness policies;
- authorization-context rules;
- topology and dependency graphs;
- version-skew and release evidence;
- the final extraction decision record;
- a GraphQL boundary brief that identifies safe graph roots and forbidden joins.
