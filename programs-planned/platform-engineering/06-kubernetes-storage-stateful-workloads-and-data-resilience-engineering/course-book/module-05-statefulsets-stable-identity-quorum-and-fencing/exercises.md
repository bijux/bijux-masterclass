# Exercises — StatefulSets, Stable Identity, Quorum, and Fencing

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Explain what StatefulSet actually guarantees

List the guarantees StatefulSet provides and three database guarantees it does not provide.

## 2. Use stable identity without confusing it with freshness

Why does `atlas-db-0` retaining its DNS name and PVC not prove that it contains the newest data?

## 3. Prove fencing across replacement

Design a test in which a new Pod takes writer authority while the old process is delayed rather than cleanly stopped.

## 4. Distinguish quorum from replica count

A three-replica StatefulSet has all Pods Ready. Why might the database still lack safe quorum?

## 5. Review scale-down retention

What should happen to `data-atlas-db-2` when a three-member StatefulSet scales to two?

## 6. Choose PodManagementPolicy

When is `Parallel` Pod management safe, and when is ordered startup useful?

## 7. Use partitioned rolling update safely

How can a StatefulSet update partition support a controlled database upgrade?

## 8. Diagnose a split-brain symptom

Two Pods each report themselves primary after a network partition. Which controls should stop data divergence?

## 9. Explain the limit of a PDB

A PDB requires two of three database Pods available. What failure does it address, and what failures remain?

## 10. Define recovery-aware readiness

What should a database Pod prove before it becomes a Service endpoint after restart?

## 11. Separate DNS identity from consistency

What does the headless Service name `atlas-db-0.atlas-db...` provide, and what additional discovery data might clients need?

## 12. Choose StatefulSet, Deployment, or operator

Atlas worker state is durable in a queue and workers are interchangeable. Atlas database members need stable volumes and membership. Choose controllers for each.
