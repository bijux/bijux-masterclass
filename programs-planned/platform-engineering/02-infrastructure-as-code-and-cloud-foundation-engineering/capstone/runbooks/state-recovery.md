# Runbook — State Recovery

1. Stop all automated plans and applies for the affected backend key.
2. Record the target account, region, bucket, key, current lock object, and
   suspected incident time.
3. Acquire or administratively freeze mutation authority. Do not delete a lock
   merely because it is old; identify its owner first.
4. List versioned state objects and preserve their version IDs and digests.
5. Copy the candidate version into an isolated recovery location.
6. Verify JSON structure, lineage, serial, resource IDs, and provider metadata.
7. Compare with remote inventory using a read-only role.
8. Produce a recovery plan from the isolated copy.
9. Obtain peer approval for the selected version and recovery action.
10. Restore or rebind state, rerun plan, and verify the data plane.
11. Re-enable automation only after the backend and lock path are healthy.

Never force-push an unreviewed state file into the authoritative backend.
