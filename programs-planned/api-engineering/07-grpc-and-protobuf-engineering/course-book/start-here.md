# Start Here — gRPC and Protobuf Engineering

## Why this course exists now

Course 7 begins only after this boundary is trusted: The Course 6 HTTP API 1.2 and Analysis Events API 1.0 handoff with profiles and migrations through 012. Its new responsibility is **engineer typed internal invocation and streaming**, and every exercise must preserve the inherited behavior while making that responsibility explicit.

## Prerequisite gate

Before editing the capstone:

1. verify the incoming handoff;
2. read the version and profile state in [Capstone](capstone.md);
3. confirm which live infrastructure is available;
4. select the implementation strategy in [Language strategy](language-strategy.md);
5. create a learning journal for hypotheses, failed predictions, and retained evidence.

For **gRPC and Protobuf Engineering**, the journal’s first page should answer: *How should typed internal capabilities be modeled and operated when remote calls can fail ambiguously, stream for long periods, and evolve across language boundaries?*

If the predecessor proof fails, stop. A successor built on an untrusted boundary cannot make a stronger claim.

## Module learning loop

For every numbered module:

1. read the chapter from its governing question through its synthesis;
2. redraw the protocol, state machine, data flow, or ownership boundary;
3. answer all twelve exercises before opening the answers;
4. inspect only the implementation paths named by the chapter or lab;
5. predict the lab’s first failing oracle;
6. run the baseline, introduce the controlled fault, and retain raw evidence;
7. repair the owning mechanism in the primary track;
8. compare the same invariant in the second track;
9. complete the checkpoint before moving on.

## Course evidence

The principal evidence for this course is described in [Evidence model](evidence-model.md). The current version state is: HTTP API 1.2 and Events API 1.0 preserved; RPC API 1.0 introduced; proto3 baseline; Edition 2024 frontier; migrations 001–015.

## Getting unstuck

When Course 7 evidence disagrees, classify the fault as schema model, field presence, wire compatibility, status mapping, deadline, retry, stream state, identity, channel lifecycle, or generation evidence, then use the cheapest authoritative oracle. Unavailable infrastructure narrows the result to what was actually observed.

## First commands

```bash
make doctor
make predecessor-proof  # when this course has a predecessor
make core-proof
```

Then complete [Orientation](module-00-orientation/index.md).
