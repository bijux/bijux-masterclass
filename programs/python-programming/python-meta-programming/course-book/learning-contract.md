# Learning Contract

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  contract["Learning Contract"]
  order["Read in order"]
  inspect["Inspect the capstone"]
  verify["Verify the claim"]
  reflect["Write the trade-off"]

  contract --> order --> inspect --> verify --> reflect
```

```mermaid
flowchart TD
  skip["Skip the order"] --> folklore["Trade-offs feel like folklore"]
  follow["Follow the order"] --> contrast["You can compare tools honestly"]
  contrast --> judgment["You build runtime judgment"]
```
<!-- page-maps:end -->

This course only works if you treat it as a judgment-building program instead of a bag
of runtime tricks. The contract below is the minimum discipline required to get that
value out of it.

## Non-negotiable study rules

1. Read the course in order from [Module 00](module-00.md) to [Module 11](module-11.md).
2. Keep the [Capstone Guide](capstone.md) and [Capstone Map](capstone-map.md) open while reading.
3. After every module, identify the lower-power alternative that would solve some of the same problems.
4. Do not copy a pattern into production code until you can explain its debugging cost.

## Questions you should always answer

- What happens at import time, class-definition time, instance time, or call time?
- Which metadata or invariants must remain visible after transformation?
- Which part of the behavior belongs on an object, a field, a wrapper, or a class?
- What would become harder to test or review if this code became more magical?

## Evidence rule

Every major claim in the course should be checkable in either:

- one runnable code fence in the module
- one named capstone file
- one capstone proof command

If you cannot check the claim, treat it as untrusted until you can.

## When to slow down

Slow down immediately if:

- decorators start feeling interchangeable with descriptors
- metaclasses feel exciting instead of narrowly justified
- `eval`, import hooks, or monkey-patching stop sounding dangerous

Those moments usually mean the earlier conceptual boundary is not firm yet.
