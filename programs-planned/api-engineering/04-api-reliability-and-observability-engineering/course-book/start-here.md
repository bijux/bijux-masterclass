# Start Here — API Reliability and Observability Engineering

## Prerequisites

Completion of Course 3, or byte-equivalent predecessor artifacts plus the ability to defend its final outcomes.

**Incoming boundary:** The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

Run the predecessor or orientation proof before changing implementation files. A failed predecessor gate means the current course has no trustworthy starting point.

## Choose your implementation route

Choose one primary implementation track. Compare failure semantics, telemetry meaning, and recovery invariants across both languages.

Record the choice in your learning journal. You may switch only after completing a module checkpoint, because simultaneous partial implementations usually reduce depth.

## The module learning loop

For each module:

1. read the main chapter from its central question to its next-step bridge;
2. restate the mechanism and its owner without framework vocabulary;
3. answer all twelve exercises before opening the answer file;
4. inspect the durable oracle, telemetry signal, failure injection, alert, and runbook named by the chapter;
5. predict the lab’s first failing oracle;
6. plant or trigger the controlled defect;
7. repair the owning mechanism and retain a regression;
8. complete the checkpoint and state the evidence boundary.

## Evidence for this course

Durable outcome oracles correlated with logs, metrics, traces, lifecycle state, fault injection, SLO calculations, alerts, runbooks, and reconciliation.

## Getting unstuck

Classify the disagreement before editing: mental model, contract/profile, implementation, fixture, proof, or environment. Start with the smallest decisive oracle. If a live dependency is unavailable, complete the deterministic and local-process routes and record the live claim as not executed.

## First commands

```bash
make doctor
make core-proof
```

Then complete [orientation](module-00-orientation/index.md).
