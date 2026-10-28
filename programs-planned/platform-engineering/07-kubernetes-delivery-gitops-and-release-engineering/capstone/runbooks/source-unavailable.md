# Runbook — desired-state source unavailable

1. Confirm that cached artifact and live workload remain available.
2. Do not convert an unavailable source into an empty desired set.
3. Suspend image or fleet automation that could write based on incomplete observation.
4. Record last verified source revision and controller artifact digest.
5. Restore repository access or fail over to the documented mirror.
6. Reconcile only after validating source lineage and render identity.
