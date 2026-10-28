# Start Here — API Platform, Governance, and Developer Experience Engineering

## Why this course exists now

Course 10 begins only after this boundary is trusted: The Course 9 handoff containing HTTP, event, RPC, distributed-service, and GraphQL contracts with explicit ownership and release evidence. Its new responsibility is **operate apis as an organizational platform**, and every exercise must preserve the inherited behavior while making that responsibility explicit.

## Prerequisite gate

Before editing the capstone:

1. verify the incoming handoff;
2. read the version and profile state in [Capstone](capstone.md);
3. confirm which live infrastructure is available;
4. select the implementation strategy in [Language strategy](language-strategy.md);
5. create a learning journal for hypotheses, failed predictions, and retained evidence.

For **API Platform, Governance, and Developer Experience Engineering**, the journal’s first page should answer: *How can an organization make trustworthy API work easier to discover, create, publish, consume, evolve, support, and retire without centralizing domain ownership?*

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

The principal evidence for this course is described in [Evidence model](evidence-model.md). The current version state is: All earlier interface and engineering profiles preserved; Analysis API Platform 1.0 and platform-catalog metadata migrations 001–004 introduced.

## Getting unstuck

When Course 10 evidence disagrees, classify the fault as platform scope, catalog authority, registry integrity, policy evidence, lifecycle, template output, documentation journey, artifact provenance, runtime drift, or decision rights, then use the cheapest authoritative oracle. Unavailable infrastructure narrows the result to what was actually observed.

## First commands

```bash
make doctor
make predecessor-proof  # when this course has a predecessor
make core-proof
```

Then complete [Orientation](module-00-orientation/index.md).
