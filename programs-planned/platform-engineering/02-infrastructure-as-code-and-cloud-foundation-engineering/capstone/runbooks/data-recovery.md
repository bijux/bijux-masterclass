# Runbook — Atlas Data Recovery

1. Select the latest recovery artifact that satisfies the incident's
   consistency and retention requirements.
2. Verify manifest identity, checksums, encryption key state, and recovery-role
   permission.
3. Restore into a new volume or empty directory.
4. Validate ownership, modes, file inventory, and checksums.
5. Start Atlas in a non-public validation mode.
6. Verify completed results and ensure completed work is not replayed.
7. Attach/register the recovered environment only after readiness passes.
8. Record actual recovery point and elapsed recovery time.
9. Preserve the failed source for forensics or delete it under policy.
