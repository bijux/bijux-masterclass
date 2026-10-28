# Course 8 → Course 9 handoff

Course 8 exports eight exact files describing service ownership, data authority, dependency budgets, consistency, and the safe GraphQL boundary. Course 9 treats these files as immutable predecessor evidence.

The graph layer may compose public service capabilities. It may not:

- read private service databases;
- move business state into the gateway;
- infer authorization from graph traversal;
- hide partial service failure as an empty list;
- execute unbounded list fan-out;
- weaken source-service idempotency or concurrency rules.

Run `make predecessor-proof` before beginning the course.
