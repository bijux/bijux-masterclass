# Case 4 — Secret synchronized, workload stale

External Secrets reported Ready and the Kubernetes Secret held version B. The application process had read version A from an environment variable at startup and never reloaded. Version A was revoked, causing authentication failure.

The delivery system proved projection, not consumption. The rotation workflow lacked a workload-adoption gate.

The repair records non-secret version identities, triggers a controlled rollout or reload, proves use of B during overlap, and revokes A only after adoption evidence.

## Extended reader notes

### Timeline

External Secrets reported Ready for credential version `v2`. The Kubernetes Secret changed, but the application consumed it through environment variables and did not restart. Operators revoked `v1`, causing connection failures.

### Root cause

Source synchronization was mistaken for workload adoption. The rotation plan had no observation of process credential version and no overlap gate.

### Durable correction

Rotation records source, materialization, adoption, and revocation separately. A rollout hash or application reload mechanism causes adoption. Telemetry exposes the credential version identifier without exposing the secret. The old version is revoked only after all required workloads report adoption.
