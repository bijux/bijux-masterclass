# Checkpoint — Edge and Recovery

## Required evidence

- [ ] DNS, certificate, listener, target group, and host authorities are explicit;
- [ ] TLS termination and the encrypted or unencrypted final hop are described honestly;
- [ ] health-check thresholds and approximate detection time are calculated;
- [ ] the host application port accepts traffic only from the edge identity;
- [ ] root, data volume, snapshot, and object backup have distinct lifecycles;
- [ ] RPO and RTO are stated as targets or observations, not unsupported guarantees;
- [ ] a backup manifest contains integrity and source-release evidence;
- [ ] restore was performed into an empty destination;
- [ ] recovery-key authority was tested or bounded explicitly;
- [ ] post-apply data-plane checks prove DNS, TLS, job completion, and result integrity.

## Decision defense

Walk one request from resolver to Atlas and one result from acknowledgement to restored bytes. For each transition, name the authority, evidence, failure mode, and recovery owner. State why the backup remains usable when the original host or its root disk is gone.

## Progression gate

Progression requires both the request-path trace and the empty-target restore trace. A successful OpenTofu apply, snapshot-creation event, or healthy target count is not a substitute.
