# Study plan

The course is designed for ten dense teaching days plus orientation.

| Period | Work |
|---|---|
| 08:30–09:00 | retrieval review and predecessor invariant check |
| 09:00–11:00 | chapter reading and worked wire or protocol analysis |
| 11:15–12:30 | Python implementation reading |
| 13:30–14:45 | TypeScript comparative reading |
| 15:00–17:30 | capstone lab |
| 18:30–19:30 | exercises before answers |
| 19:30–20:30 | evidence review and checkpoint |

Do not use the schedule to rush. A module is complete only when its evidence is intelligible. A green command whose oracle you cannot explain is not mastery.

## Primary-track choice

Choose Python when you want the complete live reference in this package, including an actual gRPC server and client. Choose TypeScript when your main goal is the Node service ecosystem; the dependency-light core is complete, while the full network adapter requires the pinned npm packages. In either case, read the other track’s boundary decisions and run the shared vectors.

## Assessment

- module checkpoints: 30%;
- exercises and design reviews: 20%;
- capstone mechanisms: 30%;
- final release and defense: 20%.

A numeric score cannot compensate for a failed compatibility, security, deadline, stream-bound, or authority gate.


## Self-learning protocol

This course is dense because each module combines contract semantics, runtime behavior, failure analysis, and evidence. Use a three-pass method rather than reading once from top to bottom.

### Pass 1 — build the mental model

Read the main chapter without opening code. Draw the interaction or state machine from memory. Write the authoritative state and the uncertain remote observation for every failure example. At this stage, do not memorize API calls. The goal is to explain why the mechanism exists.

### Pass 2 — trace one implementation

Choose Python or TypeScript as the primary track. Follow one request from generated message or semantic adapter through authentication, status mapping, application state, and response. For streams, write the legal frame sequence and every queue or byte boundary. Add comments only where the code cannot be understood from names and structure.

### Pass 3 — falsify the claim

Run the lab and try to break the mechanism. Predict the wrong outcome before injecting the fault. Inspect authoritative state rather than accepting the client exception as the oracle. Preserve the required evidence and state what it proves and does not prove.

## Daily completion questions

At the end of every module, answer:

1. What new promise does this module add?
2. Which predecessor promise constrains it?
3. What is the authoritative state after failure?
4. Which ambiguity remains at the caller?
5. Which identifier allows reconciliation?
6. Which resource is bounded?
7. Which compatibility dimension matters?
8. Which security decision occurs at the durable boundary?
9. Which proof would catch a tempting defect?
10. Which claim still requires an environment-backed route?

If you cannot answer these without searching across the repository, reread the chapter and implementation reading before the checkpoint.

## Suggested two-week rhythm

### Week one

- Day 1: boundary and ownership;
- Day 2: Protobuf semantic model;
- Day 3: wire and compatibility;
- Day 4: unary outcomes;
- Day 5: deadlines and retries.

Use the weekend for one integration review: explain how a public HTTP CreateRun request becomes an internal unary call and how response loss is reconciled.

### Week two

- Day 6: streaming and backpressure;
- Day 7: security;
- Day 8: channel and server lifecycle;
- Day 9: generation and governance;
- Day 10: cross-protocol release and final defense.

Do not add Course 8 microservices during this course. The final dossier is evidence for a later decision, not permission to split immediately.

## Learning journal format

For each module keep one page:

```text
Governing question:
Decision rule:
Authoritative state:
Primary failure:
Incorrect tempting solution:
Evidence produced:
Evidence limitation:
Python/TypeScript difference:
Open question:
```

This journal makes the final defense substantially easier. It also exposes shallow understanding early: a blank “authoritative state” or “evidence limitation” usually means the learner has followed commands without owning the engineering argument.

## Pair or review practice

When studying with another learner, assign one person as provider reviewer and one as consumer reviewer. The provider reviewer defends schema and service behavior. The consumer reviewer challenges source compatibility, deadline value, retries, unknown fields, and status semantics. Switch roles for the streaming lab.

For solo study, perform the consumer review one day later without reading the provider notes. Delayed retrieval is more effective than immediately rereading the answer.

## When to use external tooling

Use `protoc`, Buf, grpcurl, live TLS, PostgreSQL, and the full TypeScript network stack after the dependency-light mechanism is understood. External tools should strengthen an existing claim, not replace reasoning. Record versions, commands, output, and environment. If the tool is absent, complete the local proof and retain the route as not executed.

## Definition of mastery

Mastery is not the ability to write a `.proto` file from memory. It is the ability to review a proposed remote boundary, model its wire semantics, predict ambiguous failure, constrain time and resources, protect identity and state, evolve consumers safely, operate the channel and server lifecycle, and introduce or remove the RPC path without changing the public or event promises.
