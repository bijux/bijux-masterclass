# Start here

## What you must already know

You should have completed the first eight API Engineering courses or possess equivalent competence in HTTP contracts, durable services, security, reliability, performance, events, RPC, and service boundaries. This course does not reteach those subjects. It applies them to a graph runtime.

You should be able to explain:

- which service owns project, run, artifact, and notification facts;
- why a gateway owns composition but not business state;
- how idempotency and expected-version checks survive retries;
- why partial dependency failure must be visible;
- how event sequence and replay support resumable observation;
- how a request budget is divided across remote calls.

Run:

```bash
make doctor
make predecessor-proof
make orientation-proof
```

## The learner contract

The course book is authoritative. Code, fixtures, laboratories, and reports support the book. Do not begin by browsing source files at random. Read each module chapter, answer its exercises without the answer key, run the lab, and satisfy the checkpoint.

For Courses 2–9, choose one primary implementation track. Implement and debug that track deeply. Use the second track to compare semantics and run shared-vector parity. Course 9 recommends TypeScript as the primary track when your goal is GraphQL ecosystem work, because GraphQL.js is the reference implementation and much of the production tooling is TypeScript-first. Python remains a complete comparative track and is often the better primary choice for scientific and data platforms.

## What completion means

Completion is not “the schema renders in an IDE.” You must prove:

- every field has an authority and policy;
- active operations validate against the released schema;
- list cardinality and query cost are bounded;
- repeated nested fields batch rather than create N+1 calls;
- tenant and field authorization cannot be bypassed through traversal;
- mutations preserve source-service idempotency and concurrency;
- partial failure follows declared nullability and error-path rules;
- subscriptions resume without silent gaps;
- a schema release preserves active consumers or is rejected.

The final defense is a live explanation of those guarantees using the capstone evidence.
