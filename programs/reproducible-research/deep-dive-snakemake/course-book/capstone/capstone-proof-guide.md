# Capstone Proof Guide

Use this page when a module makes a Snakemake design claim and you want the shortest
honest route to the capstone evidence that supports it.

## Enter this guide at the right time

Use this guide once the module idea is already legible in its local exercise.

Before that point, prefer [Capstone Walkthrough](capstone-walkthrough.md) so the
repository stays smaller than the concept you are learning.

## Proof route shape

```mermaid
flowchart TD
  claim["Name one design claim"] --> route["Choose the narrowest route"]
  route --> inspect["Inspect the evidence surface"]
  inspect --> enough{"Did it settle the claim?"}
  enough -- yes --> stop["Stop and explain why"]
  enough -- no --> stronger["Escalate one route stronger"]
  stronger --> inspect
```

## Start by proof need

| If you need to prove... | Start here | Escalate only if needed |
| --- | --- | --- |
| repository shape without execution | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `capstone-tour` |
| executed workflow behavior | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `proof` |
| publish-boundary trust | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` | `capstone-confirm` |
| execution-policy differences | [Capstone Architecture Guide](capstone-architecture-guide.md) | `proof` |
| steward-level confidence | `make PROGRAM=reproducible-research/deep-dive-snakemake proof` | `capstone-confirm` |

## Good proof habits

- Start with the claim, not with the heaviest available command.
- Check the evidence bundle the command was meant to produce.
- Escalate only when the unanswered part of the claim is real, not when uncertainty feels uncomfortable.

## Worked examples

| Claim | Good first route | Why not stronger first |
| --- | --- | --- |
| "I need to see whether discovery is explicit." | `capstone-tour` | `capstone-confirm` adds weight before the discovery artifact question is even settled |
| "I need to review what downstream users may trust." | `capstone-verify-report` | a broader proof pass is worse than a publish-specific route for contract questions |
| "I need a maintainer-grade review route." | `proof` | `capstone-walkthrough` is too light once the question is explicitly stewardship-level |

## Bounded proof pass

1. Read [Capstone Guide](index.md).
2. Use [Proof Matrix](../guides/proof-matrix.md) to choose the narrowest command.
3. Run that command from the capstone or course root.
4. Record what the evidence proves before opening a stronger route.

## Good stopping point

Stop when you can say:

- which command gave the narrowest honest answer
- which evidence surface actually settled the claim
- why a broader route would be unnecessary unless the claim changed

If you cannot say those three things, repeat the bounded route before escalating.
