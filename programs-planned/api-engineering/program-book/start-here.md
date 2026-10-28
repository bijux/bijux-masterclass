# Start Here

## Who this program is for

You should be able to read small Python or TypeScript programs, use a terminal, and follow a test failure. You do not need prior OpenAPI, PostgreSQL, OAuth, observability, performance, messaging, gRPC, microservices, GraphQL, or platform-engineering experience. Course 1 builds the initial protocol model; later courses require the preceding handoff or equivalent evidence.

## Begin with the book, not the repository tree

Repository browsing before a mental model turns study into filename archaeology. For each course:

1. read the course introduction and capstone guide;
2. complete orientation and verify the incoming handoff;
3. read one module chapter without opening its answers;
4. answer all twelve exercises in your own words;
5. inspect the narrow implementation paths named by the chapter;
6. predict the lab oracle before executing the lab;
7. complete the experiment in one primary track;
8. compare the same invariant in the second track;
9. preserve the checkpoint evidence before moving forward.

## Choose a language strategy

Course 1 uses Python/FastAPI and TypeScript/Fastify symmetrically because contract independence is the lesson. From Course 2 onward, choose one primary track for the deep implementation. Use the second as a comparison and parity reference.

Do not force identical internal architecture. Python and TypeScript have different runtime, typing, concurrency, and ecosystem idioms. Parity applies to the public outcome and named engineering invariant—not to class names or folder shapes.

## Use the smallest decisive oracle

Before editing, classify the disagreement:

- mental model;
- contract or course profile;
- implementation;
- fixture or test;
- environment comparability;
- proof strength.

A parser settles syntax, not runtime conformance. A unit test settles a local rule, not process recovery. Telemetry supports diagnosis, not authoritative business truth. A laptop benchmark supports mechanism evidence, not production capacity. Escalate only when a cheaper valid oracle passes.

## Study rhythm

Each course is ten dense teaching days over two calendar weeks. Use four cycles each day: model, transfer, experiment, defense. The middle weekend is for repair and synthesis, not hidden new curriculum. If a checkpoint fails, repair it before stacking later modules on top.

## First commands

From `programs/api-engineering`:

```bash
make doctor
make structure
make handoff-proof
```

A green dependency-light proof establishes only the checks it executed. Live infrastructure routes are separate.
