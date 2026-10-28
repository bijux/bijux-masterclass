# Exercises — Data Lifetimes, Durability, and Storage Responsibility

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Classify the Atlas data

Classify `run-state`, immutable result artifacts, worker scratch files, a read cache, and backup manifests. For each, state its authority, smallest acceptable loss domain, writer count, and deletion owner.

## 2. Separate five different guarantees

For a single-zone block volume attached to a database Pod, analyze persistence, durability, availability, consistency, and recoverability separately. Do not use the word “reliable.”

## 3. Choose a lifetime deliberately

A worker needs 8 GiB for intermediate decompression and can recreate it from an immutable input. Compare container writable layer, `emptyDir`, local PV, network block volume, and object storage. Choose one and defend the choice.

## 4. Explain why access mode is not writer authority

A review states: “The database is safe because the PVC uses `ReadWriteOncePod`.” Explain what this mode constrains and what it does not.

## 5. Define the acknowledgement boundary

Atlas reports a job result as complete after writing a JSON file and renaming it into place. What must happen before the success response if the contract claims survival of process crash and host power loss?

## 6. Design deletion authority

Design the deletion path for a production database claim, its snapshots, and off-cluster backups. Name which actions may be automatic and which require separate approval.

## 7. Evaluate a shared filesystem proposal

A team proposes one RWX filesystem for database files, artifacts, scratch space, logs, and backups because “operations will be simpler.” Identify at least four hidden couplings.

## 8. Decide whether local storage is acceptable

Atlas can use very fast local NVMe or a network volume. State the conditions under which local storage is an honest production choice for transactional state.

## 9. Turn requirements into a platform API

Propose the minimum fields a future platform API should ask for when a developer requests durable data. Explain why `size` and `fast=true` are insufficient.

## 10. Diagnose the disappearing result

A replacement worker is healthy, the job says complete, and the result path contains a truncated artifact. Reconstruct the earliest likely broken transitions before inspecting Kubernetes objects.

## 11. Build an evidence ladder

For the single-writer invariant, name one semantic proof, one local mechanism proof, one cluster proof, one storage-system proof, and one operated proof.

## 12. Defend the Atlas data catalogue

Explain what Course 7 must preserve when it automates the Atlas data catalogue through GitOps.
