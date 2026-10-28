# Runbook — Atlas Service Failure

## Trigger

API, worker, or edge process exits, fails readiness, or enters a restart loop.

## Preserve before restart

Record unit state, exit code or signal, process/cgroup identity, recent structured events, open storage capacity, and dependency readiness. Do not delete queue state.

## Diagnose

1. Identify which service failed and whether the failure is process, readiness, or routing.
2. Inspect `systemctl status` and `journalctl` for the exact invocation.
3. Verify code/config identity and path permissions.
4. Check resource events, disk state, listener ownership, and worker heartbeat.
5. Reproduce with the focused proof when safe.

## Recover

Correct the owning mechanism, run the focused test, restart only the affected service, verify readiness, then run one end-to-end job.

## Escalate

Escalate when durable state is inconsistent, the process repeatedly fails after a known-good rollback, or the repair would weaken identity, TLS, firewall, or storage boundaries.
