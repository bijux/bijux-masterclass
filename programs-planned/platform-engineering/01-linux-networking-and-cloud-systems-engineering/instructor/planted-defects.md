# Planted Defects

The machine-readable catalogue is `capstone/planted-defects/catalog.json`. Use one defect per module only after the learner has established a working baseline.

## Facilitation rules

1. Inject one causal fault unless the lab explicitly studies correlated failure.
2. Preserve the exact diff or command used to inject it.
3. Define an abort condition before privileged or cloud changes.
4. Do not accept a broad workaround that suppresses the oracle.
5. Require the focused regression and clean baseline after repair.

## Defect themes

- `SYS-01`: shutdown loses claimed work;
- `SYS-02`: root/writable-release privilege escalation;
- `SYS-03`: unbounded memory pressure hidden by liveness;
- `SYS-04`: overstated directory-entry durability;
- `SYS-05`: unintended wildcard listener;
- `SYS-06`: TLS verification disabled after name mismatch;
- `SYS-07`: client forwarding identity trusted directly;
- `SYS-08`: mutable state embedded in replaceable image;
- `SYS-09`: unsupported multi-zone claim;
- `SYS-10`: emergency repair weakens another boundary.

The defect is complete only when the learner predicts the failure, observes the decisive oracle, repairs the owner, and demonstrates that the defect can no longer pass.
