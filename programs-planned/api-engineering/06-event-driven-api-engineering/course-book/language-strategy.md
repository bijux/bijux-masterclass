# Language Strategy — Event-Driven API Engineering

## Strategy

Choose one primary track for the complete build and lab repairs. Use the second as an idiomatic comparison and shared-vector parity reference. The course deliberately avoids making learners type the same architecture twice.

## What must match

- public messages and documented statuses;
- named state, security, reliability, performance, event, RPC, architecture, graph, or governance decisions owned by this course;
- canonical bytes when signatures, digests, wire compatibility, or cross-language identity depends on them;
- accepted, rejected, and review-required release classifications;
- shared negative vectors and evidence boundaries.
- the Course 6 outcome: Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.

## What may differ

broker clients, acknowledgement APIs, serialization types, and worker concurrency differ; compare canonical events, delivery state, inbox effects, and replay outcomes.

## Reading implementation examples

For each example:

1. name the invariant before reading code;
2. identify the owner and state boundary;
3. find the negative test;
4. find cleanup and failure behavior;
5. compare the second track only after you can explain the first;
6. never infer a protocol rule from one framework default.
