# Exercises — CSI Architecture and Volume Lifecycle

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Map the CSI owners

Map provisioning, attachment, staging, publication, snapshotting, expansion, and deletion to controller-side or node-side CSI responsibilities.

## 2. Define `CreateVolume` idempotency

What identity and parameter checks make a retried `CreateVolume` safe after a timeout?

## 3. Trace the usable-volume lifecycle

Write the ordered lifecycle from PVC demand to a container-visible filesystem, including the evidence at each boundary.

## 4. Reverse the lifecycle safely

Why must unpublish, unstage, detach, and delete occur in a disciplined reverse order?

## 5. Handle a Node crash without split brain

A Node disappears while holding a zonal database volume. Explain the evidence needed before attaching it to a replacement Node.

## 6. Interpret driver capabilities

Why must the platform query or document CSI capabilities instead of inferring them from Kubernetes API fields?

## 7. Separate controller and node expansion

A PVC size is increased and the backend volume grows, but the filesystem remains unchanged. Explain the two-phase state.

## 8. Analyze inline ephemeral CSI volumes

When is a CSI ephemeral volume appropriate, and why is it unsuitable for authoritative Atlas state?

## 9. Design CSI observability

Choose useful bounded dimensions for CSI metrics and explain what belongs in logs instead.

## 10. Protect CSI credentials

Identify the credential boundaries among Kubernetes, CSI sidecars, node plugins, and the storage backend.

## 11. Design a partial-provisioning repair

A controller creates a backend volume but crashes before creating the PV. How should reconciliation find and resolve the orphan?

## 12. State the native proof still required

The semantic CSI model passes. What must a native Course 6 lab still prove before a driver profile can be called supported?
