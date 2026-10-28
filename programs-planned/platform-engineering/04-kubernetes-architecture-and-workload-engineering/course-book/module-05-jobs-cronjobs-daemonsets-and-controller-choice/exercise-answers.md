# Worked answers

## 1. Why can a Job repeat a completed business effect?

The process may complete the external effect and fail before Pod success is durably observed. The Job controller then creates another attempt. Kubernetes tracks Pod completion, not the external business transaction. Use a stable operation/effect identity and durable deduplication so repeated attempts converge on one logical result.

## 2. How do restartPolicy and Job retries differ?

restartPolicy controls container restart inside one Pod. The Job controller can create replacement Pods. With OnFailure, several attempts may occur within one Pod; with Never, each failed attempt remains a separate Pod. Choose based on retry semantics and evidence needs, while keeping the business effect idempotent across both layers.

## 3. What does backoffLimit fail to guarantee?

It bounds counted Job retries under the controller’s semantics. It does not guarantee a time limit, rollback, exactly-once effects, or classification of permanent versus transient failures. Combine it with activeDeadlineSeconds, podFailurePolicy, application exit codes, and durable effect identity.

## 4. Why is an indexed Job still vulnerable to duplicate work?

The completion index identifies a logical partition, but more than one Pod attempt can execute that index after failure or uncertain status. The effect key should include Job identity, effect version, and completion index. A consumer should treat a repeated successful index as replay, not a new effect.

## 5. What does CronJob concurrencyPolicy Forbid guarantee?

It prevents creation of a new scheduled Job while the previous Job is still active according to Kubernetes. It does not prevent duplicate effects inside one Job, manual overlapping Jobs, or uncertainty after external actions. The task still needs idempotency and a missed-schedule policy.

## 6. When is concurrencyPolicy Replace dangerous?

Replace terminates the active Job and starts the new scheduled instance. If work is not safely interruptible, checkpointed, and resumable, it can leave partial effects. Use it only when replacement semantics are designed, not to keep the schedule visually current.

## 7. Why is a DaemonSet not an application replica strategy?

Its desired count follows eligible Nodes, so capacity changes with the fleet. It is for node-local facilities, often with broader tolerations and platform authority. An API service should scale by demand and availability, not by node count. Application teams should not deploy privileged node agents casually.

## 8. What evidence should be retained before TTL removes a Job?

Preserve Job spec/status, attempts, exit codes, operation identity, effect record, timing, logs or durable log reference, retry classification, and result checksum. TTL cleanup is hygiene; it should not erase the only proof of a failed or repeated effect.

## 9. Why are static Pods unsuitable for ordinary Atlas releases?

Their source of desired state is a node-local file watched by kubelet, not a normal API controller. Mirror Pods are observations, not fully controllable API objects. Release, scheduling, and multi-node reconciliation become node-specific. Static Pods fit selected control-plane components, not normal application delivery.

## 10. How should a permanent input error be expressed to a Job?

The application should return a stable exit code or condition that podFailurePolicy can classify as fail-fast. Repeated transient-style retry wastes time and may amplify harm. The evidence record should retain the input identity and permanent reason without leaking secrets.

## 11. Why might a continuous controller be better than a frequent CronJob?

If the task repeatedly compares desired and observed state, a level-triggered controller can react to changes and reconcile incrementally. A CronJob repeatedly scans on wall-clock intervals, can overlap or miss schedules, and delays correction. The controller is justified only if ownership and API design are clear.

## 12. Which controller should own the Atlas database migration?

A release-owned finite Job or external release workflow, not every application Pod. It needs one migration identity, compatibility checks, locking/idempotency, timeout, result evidence, and release gating. Course 7 will govern when that Job runs relative to workload promotion.
