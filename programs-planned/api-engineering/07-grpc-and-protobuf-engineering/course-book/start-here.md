# Start here

## Prerequisites

Complete Courses 1–6 or demonstrate the same incoming guarantees. You should already be able to reason about HTTP contracts, durable transactions, authorization, deadlines, telemetry, capacity, events, outbox/inbox behavior, and replay. Course 7 does not reteach those subjects. It shows how they constrain a new synchronous and streaming internal boundary.

You need basic Python and TypeScript reading ability. Choose one primary implementation track. Use the second for cross-language contract review and shared-vector verification rather than duplicating every framework detail.

## First commands

```bash
make doctor
make predecessor-proof
make orientation-proof
make capstone-tour
```

`doctor` reports tools and evidence classes. The dependency-light route uses Python, Node, TypeScript, checked-in descriptors, and generated-equivalent surfaces. The full route additionally uses protoc or Buf, Python gRPC tools, the TypeScript gRPC stack, TLS fixtures, and grpcurl.

## Study rule

Read the chapter before opening implementation code. For each module:

1. state the governing question in your own words;
2. predict the failure before running the lab;
3. implement or review the primary track;
4. compare the second track at the contract boundary;
5. preserve the named evidence;
6. pass the checkpoint before moving forward.

## Non-negotiable distinctions

Keep these separate:

- local call versus remote call;
- transport success versus application success;
- timeout versus no effect;
- stream connection versus durable authority;
- binary wire compatibility versus source, JSON, and behavioral compatibility;
- channel identity versus end-user authorization;
- HTTP API version versus event API version versus RPC API version versus service release;
- dependency-light model evidence versus live network and infrastructure evidence.

Begin with [Orientation](module-00-orientation/index.md).
