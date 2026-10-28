# Orientation — lock the predecessor and establish the data laboratory

Course 6 starts with a networked Kubernetes workload and an immutable Course 5 handoff. The first task is not installing a storage driver. It is proving that the predecessor package is intact and translating its obligations into a data-plane risk register.

Read every handoff file under `capstone/predecessor/handoff/`. Notice what it asserts and what it refuses to assert. Services and DNS are stable. Default-deny networking is expected. CSI controller and node endpoints must be observable. Snapshot, backup, and restore traffic require explicit egress. Stateful readiness must remain false until durable recovery is complete. PVCs are still unbound because Course 5 did not own storage.

The mandatory laboratory uses only local files, Python, Go, JSON, YAML, and deterministic fixtures. It can establish binding logic, idempotency, fencing, snapshot coordination, backup inventory, restore verification, and release decisions. The optional cluster lane requires `kubectl`, kind, a CSI-capable driver, snapshot CRDs and controllers, and a disposable storage environment. The managed lane requires a real cloud or storage account and has cost and deletion risk.

## Laboratory rules

1. Never run a destructive storage command without recording cluster, namespace, class, claim, backend handle, and intended failure domain.
2. Never force detach or remove finalizers merely to make an object disappear.
3. Never call a snapshot a backup without a separate retention and restore contract.
4. Never restore over authoritative data during a course experiment.
5. Never claim high availability from replicas alone.
6. Never convert unavailable infrastructure into a passing result.

## Initial proof

Run:

```bash
make doctor
make predecessor-proof
make structure-proof
```

Then create your evidence directory outside the manifest-controlled source tree. The course proof scripts clean generated outputs so a clean checkout remains reproducible.

## How to reason in this course

Storage incidents are difficult because several control planes can look healthy while the data service is wrong. A PVC can be Bound while the volume is inaccessible. A device can be mounted while the filesystem is stale. A database process can accept TCP while it is still replaying logs. A snapshot can be ready while it represents no valid application recovery point. A backup process can exit zero while the only copy of its encryption key remains in the failed account.

Use one investigation discipline throughout the course:

1. **Name the logical data.** Start with the business state, artifact, checkpoint, or recovery record—not a Kubernetes object.
2. **Name the current authority.** Identify the process, lease, transaction generation, or controller allowed to change it.
3. **Trace the physical identity.** Follow claim, volume, handle, backend object, filesystem, and application generation without assuming that matching names mean matching bytes.
4. **Find the earliest missing transition.** A later green status cannot compensate for an earlier incomplete write, attachment, recovery, or verification step.
5. **Separate evidence classes.** A semantic model proves a rule; a local filesystem test proves one mechanism; a cluster proves controller interaction; a storage backend proves its implementation; an operated service proves behavior over time.
6. **Protect recovery while debugging.** Never destroy the only retained copy, force-detach a possible writer, or restore over authoritative data merely to make an object become Ready.

The course therefore treats every lab as an investigation rather than a command sequence. Before the controlled action, write what should happen and which record should change first. Afterward, compare Kubernetes state, CSI state, backend state, filesystem state, and application state. A good report can be reviewed without terminal history and includes the evidence that would falsify its conclusion.

## The three execution lanes

The **mandatory lane** uses Python, Go, local files, and deterministic manifests. It makes binding, CSI ordering, fencing, snapshot coordination, backup identity, restore verification, migration ordering, and release policy inspectable. It is the fastest lane for understanding invariants because every transition is visible.

The **cluster lane** uses a disposable Kubernetes cluster with a deliberately selected CSI driver and snapshot stack. It proves API defaulting, controller reconciliation, sidecar compatibility, scheduling, mount behavior, and failure recovery. A kind cluster without a realistic CSI backend can still teach controller mechanics, but it does not establish cloud-volume durability or multi-zone behavior.

The **storage-system lane** uses the actual backend and failure domains intended for deployment. It is required for attachment fencing, performance, expansion, snapshot semantics, restore time, quotas, and durability claims. This lane may incur cost and deletion risk. Its lab plan must identify the account, region, storage class, data set, cleanup authority, and maximum acceptable blast radius before execution.

## What completion means

Completion is not “all YAML applied.” A learner completes Course 6 when they can defend a data service from first principles: what is authoritative, who may write, which faults are covered, what can be deleted, how a stale writer is stopped, which copy satisfies each recovery objective, how restoration is verified, and which claims remain unexecuted. The final handoff to Course 7 must be safe for automation precisely because those decisions are no longer implicit.

## Reading strategy for difficult chapters

Do not try to memorize every Kubernetes field or CSI RPC on first reading. Read each chapter in three passes. On the first pass, locate the authoritative state and the main lifecycle. On the second, trace the failure scenario and mark every point where a timeout, retry, stale actor, or destructive intervention can change the outcome. On the third, connect the chapter to the capstone implementation and lab oracle.

When a concept remains unclear, rewrite it as a before-and-after state transition. For example, “attach a volume” becomes: backend object exists but is not authorized for Node B → Node B receives a current attachment generation while Node A cannot issue writes. This form exposes the missing owner and evidence. Use the worked answers after attempting the exercises; they are explanations, not answer templates to memorize.
