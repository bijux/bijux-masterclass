# Casebook — The Edge Apply Failed Halfway

A saved plan creates an ALB, target group, data volume, and listener. The apply
creates the ALB and volume but fails because the certificate ARN is invalid. The
pipeline retries automatically. The second run creates no listener, the target
remains unregistered, and the volume continues accruing cost.

## Unsafe responses

- deleting the ALB manually without checking state;
- rerunning apply indefinitely;
- editing the state to remove failed resources;
- declaring rollback because the application was never reachable;
- ignoring the orphaned volume because it is encrypted.

## Correct response

1. stop automatic retries and promotion;
2. preserve the plan, apply log, state object version, and role session;
3. inventory actual ALB, target group, security groups, volume, and attachments;
4. check whether any public listener or route created exposure;
5. determine whether the certificate input or authority is wrong;
6. plan from current reality;
7. choose roll-forward with a valid certificate or controlled cleanup;
8. verify the edge and result path if rolling forward;
9. verify deletion and state convergence if cleaning up;
10. record cost and elapsed exposure.

## Why “apply is idempotent” is insufficient

OpenTofu can often continue after partial creation, but provider/API operations
and external prerequisites can remain inconsistent. Idempotence is a useful
property, not an incident decision. The operator still needs current inventory,
state health, security assessment, and a justified path.

## Lesson

A release is not atomic because its configuration is declarative. Partial apply
is a normal failure mode that needs evidence and an owned recovery process.
