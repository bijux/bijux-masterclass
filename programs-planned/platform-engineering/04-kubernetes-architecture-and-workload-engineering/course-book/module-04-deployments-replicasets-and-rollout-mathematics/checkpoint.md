# Checkpoint — rollout safety

## Required evidence

- resolved surge/unavailability integers;
- Atlas API rollout population timeline;
- progress-deadline diagnosis;
- exact rollback artifact and compatibility statement;
- capacity assumption for surge.

## Decision defense

Defend why maxUnavailable zero is appropriate for Atlas API now and which cluster-capacity condition it imposes.

## Progression gate

Proceed only when rollout completion and user-facing availability are no longer treated as the same fact.
