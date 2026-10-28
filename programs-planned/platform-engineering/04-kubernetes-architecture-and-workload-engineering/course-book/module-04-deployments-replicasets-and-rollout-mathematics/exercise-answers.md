# Worked answers

## 1. For three replicas, what do maxSurge 1 and maxUnavailable 0 permit?

The controller may run at most four Pods during rollout and should preserve at least three available desired replicas during controlled replacement. Progress requires capacity for the surge Pod. This does not guarantee three user-visible successes: readiness must be truthful, networking must select ready endpoints, and failures outside voluntary rollout can still reduce capacity.

## 2. Why do percentage values require explicit rounding analysis?

Kubernetes rounds maxSurge percentages up and maxUnavailable percentages down. Small replica counts can therefore produce surprising integer limits. A policy that looks symmetric at 25% may become surge one and unavailable zero for three replicas. Release evidence should record the resolved integers, not only the percentages.

## 3. What does ProgressDeadlineExceeded mean?

It means the Deployment controller observed insufficient rollout progress within the configured deadline. It does not identify the original cause and does not automatically roll back. Inspect new ReplicaSet Pods, scheduler events, image pulls, startup, and readiness. The condition is a decision trigger for a release workflow, not a repair action.

## 4. Why can a rollout deadlock on a healthy cluster?

The cluster may have no spare schedulable capacity for maxSurge while maxUnavailable is zero. Existing replicas consume all feasible resources or topology slots. The scheduler correctly leaves new Pods Pending, and the Deployment correctly refuses to remove old available Pods. The fix is capacity, strategy, or placement change—not restarting controllers.

## 5. When does a Deployment create a new ReplicaSet?

When its Pod template changes, producing a new template hash. Top-level metadata changes that do not alter the template do not replace Pods. Evidence should compare `.spec.template` and ReplicaSet ownership rather than assuming every Deployment update is a rollout.

## 6. Why is an image rollback not a complete application rollback?

External schema, configuration, secret, message, and data changes may be incompatible with the old binary. Revision history only restores a Pod template. A safe rollback requires compatibility evidence and continued artifact availability/authorization. Course 3 supplies a bounded compatibility assumption for this exercise.

## 7. What is the difference between ready and available replicas?

Ready replicas currently pass readiness. Available replicas have remained ready for at least minReadySeconds. Availability is therefore a more stable rollout population. A briefly ready Pod can increase ready count without satisfying availability. Reports should name the exact population used.

## 8. Why should selector labels be stable?

The selector defines the ReplicaSet/Pod population owned by the Deployment and is effectively immutable. Changing it can orphan existing Pods or cause overlapping controllers. Version should live in template labels for observation, while stable application/component labels define ownership.

## 9. When is Recreate a legitimate strategy?

When old and new versions cannot coexist or share an exclusive resource and planned downtime is accepted. It should be supported by explicit compatibility and availability decisions. It is not a generic fix for failed readiness or insufficient surge capacity.

## 10. What does pausing a Deployment actually pause?

It pauses Deployment rollout processing for template changes; it does not freeze Pods, external systems, configuration, or human mutations. It can create an investigation window, but release authority and change governance belong to Course 7.

## 11. Why is increasing maxUnavailable a dangerous response to failed readiness?

It may remove healthy old replicas and allow a broken new revision to reduce service availability. The readiness failure is evidence that the new Pods are not eligible. Repair the configuration or application cause. Strategy relaxation requires an explicit business decision, not frustration with rollout speed.

## 12. What should a rollout report preserve?

The exact Deployment and ReplicaSet templates, image digests, generation/observedGeneration, desired/current/updated/ready/available counts, conditions, events, Pod states, strategy-resolved integers, capacity evidence, and rollback decision. A screenshot of kubectl output is insufficient for reproducible diagnosis.
