# Start Here — GraphQL Schema and Runtime Engineering

## Why this course exists now

Course 9 begins only after this boundary is trusted: The Course 8 distributed architecture handoff with explicit service, data, contract, and trust boundaries. Its new responsibility is **compose governed client-shaped capabilities**, and every exercise must preserve the inherited behavior while making that responsibility explicit.

## Prerequisite gate

Before editing the capstone:

1. verify the incoming handoff;
2. read the version and profile state in [Capstone](capstone.md);
3. confirm which live infrastructure is available;
4. select the implementation strategy in [Language strategy](language-strategy.md);
5. create a learning journal for hypotheses, failed predictions, and retained evidence.

For **GraphQL Schema and Runtime Engineering**, the journal’s first page should answer: *How can clients select graph-shaped data and operations without moving business ownership, authorization, cost, or consistency into an uncontrolled gateway?*

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

The principal evidence for this course is described in [Evidence model](evidence-model.md). The current version state is: HTTP, Event, and RPC APIs preserved; Analysis Graph API 1.0 introduced; GraphQL September 2025; graph metadata migrations 001–004.

## Getting unstuck

When Course 9 evidence disagrees, classify the fault as schema semantics, source ownership, batching, pagination, mutation delegation, authorization, demand admission, partial data, subscription state, or release compatibility, then use the cheapest authoritative oracle. Unavailable infrastructure narrows the result to what was actually observed.

## First commands

```bash
make doctor
make predecessor-proof  # when this course has a predecessor
make core-proof
```

Then complete [Orientation](module-00-orientation/index.md).
