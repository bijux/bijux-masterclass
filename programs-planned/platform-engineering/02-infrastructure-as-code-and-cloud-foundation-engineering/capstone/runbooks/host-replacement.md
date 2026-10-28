# Runbook — Atlas Host Replacement

1. Identify the approved image and launch-template version.
2. Check instance, address, subnet, target, and volume-attachment capacity.
3. Protect or snapshot the Atlas data volume.
4. Create the replacement in the compatible availability zone.
5. Verify instance identity, bootstrap profile, data mount, and readiness.
6. Register the replacement target and wait for edge health.
7. Shift traffic and observe a bounded bake period.
8. Stop and remove the old target, then terminate the old host.
9. Verify one existing result and one new job.
10. Record the new instance/launch identities and cleanup.
