# Checkpoint — Module 06: Metrics and Service-Level Indicators

## Required result

Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics.

## Demonstrate

- Choose metric instruments from the measured quantity.
- Control label dimensions and series count.
- Measure latency distributions rather than averages.
- Define good, bad, eligible, and excluded events.
- Use durable timestamps for asynchronous journey indicators.

## Commands

```bash
make module-proof MODULE=06
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Metrics and Service-Level Indicators** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Metrics and Service-Level Indicators**
- focused result for: Choose metric instruments from the measured quantity.
- public, durable, security, or operational observation showing: The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **metrics and SLI populations**
- a limitation statement naming every live dependency required to support the strongest **Metrics and Service-Level Indicators** claim but not exercised

## Defend the design

1. Answer the central question: **Which numeric observations describe user outcomes without exploding cardinality or hiding the tail?**
2. Demonstrate this capstone result: The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.
3. Show the **Metrics and Service-Level Indicators** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: instrument type, labels, eligibility, good/bad classification, and reset handling are explicit and bounded.
5. State which environment-backed **Metrics and Service-Level Indicators** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—The capstone exports bounded metrics and SLIs for availability, run start, completion, artifact access, and webhook delivery.—all focused checks pass, the **Metrics and Service-Level Indicators** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
