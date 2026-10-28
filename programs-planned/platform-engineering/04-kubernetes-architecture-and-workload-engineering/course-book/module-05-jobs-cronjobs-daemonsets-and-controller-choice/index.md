# Module 5 — Jobs, CronJobs, DaemonSets, and controller choice

Kubernetes workload controllers encode different meanings. Choosing a controller because its YAML is familiar is a design error. The first question is whether work is continuous, finite, scheduled, or node-local.

```text
continuous interchangeable replicas  → Deployment
finite completion                     → Job
scheduled creation of finite work     → CronJob
one eligible copy per Node            → DaemonSet
stable ordinal identity               → StatefulSet
```

The controller does not automatically provide business idempotency, data durability, or exactly-once effects.

## Jobs model completion, not exactly-once execution

A Job creates Pods and tracks successful completions. Depending on `completions`, `parallelism`, completion mode, retry policy, and failures, more than one Pod may execute the same logical work.

Even with `parallelism: 1` and one completion, duplication can occur around node failure or lost status. A process may complete an external effect, then die before Kubernetes records Pod success. The Job controller may create another Pod.

Therefore:

> Job completion is a controller observation about Pods. Exactly-once business effects require application-level identity and durable deduplication.

Atlas maintenance jobs use a stable operation ID stored with the durable effect. Replayed Pods observe completion and exit successfully without repeating it.

## RestartPolicy versus Job retry

Inside one Pod, `restartPolicy: OnFailure` can restart a failed container. The Job controller can also create replacement Pods. These are separate retry layers.

`Never` makes Pod attempts easier to inspect because each failure remains a failed Pod, but it can create more objects. `OnFailure` can reduce Pod churn but may hide repeated container attempts inside one Pod. The choice belongs to the evidence and failure model.

## Backoff and failure policy

`backoffLimit` bounds controller retries but is not a business rollback. `activeDeadlineSeconds` bounds total Job activity. `podFailurePolicy` can classify selected exit codes or Pod conditions as ignore, count, or fail actions.

A permanent input error should not consume many retries. A transient network timeout may merit bounded retry. The application must expose stable exit semantics before the Job policy can classify them.

## Parallel and indexed Jobs

For embarrassingly parallel work, a Job can run multiple completions. Indexed completion mode gives each completion a stable index. The index can partition work, but the application must still handle duplicate attempts for one index.

Atlas uses indexed Jobs only in a laboratory that verifies per-index effect identity.

## TTL and history

`ttlSecondsAfterFinished` can clean up completed Jobs. CronJob history limits can retain selected successful and failed Jobs. Cleanup improves cluster hygiene but can erase debugging evidence. Retention policy should preserve enough metadata and logs in a durable system before objects disappear.

## CronJobs create Jobs; they do not run tasks directly

A CronJob evaluates a schedule and creates Jobs. Important fields include:

- `schedule`;
- `timeZone`;
- `concurrencyPolicy`: Allow, Forbid, or Replace;
- `startingDeadlineSeconds`;
- successful/failed history limits;
- `suspend`.

Scheduling is best effort. Controller downtime, clock behavior, and missed schedules matter. The job itself must remain idempotent because duplicate creation can occur in edge cases and manual triggers may overlap.

`Forbid` prevents a new scheduled Job while the previous is active; it does not make the external effect exactly-once. `Replace` deletes the old Job and starts a new one, which is unsafe for work that cannot be interrupted or resumed.

Atlas checkpoint reconciliation uses `Forbid` because overlapping runs would contend for the same durable reconciliation key. The task remains idempotent.

## DaemonSets express node-local desired state

A DaemonSet ensures a Pod on every eligible Node. Typical uses include node-level networking, storage, logging, monitoring, or security agents.

The desired count is derived from eligible Nodes, not a replica number. Node selectors, affinity, taints, and tolerations decide eligibility. DaemonSet Pods commonly tolerate conditions that ordinary workloads do not, because node agents may need to remain during problems.

Atlas includes a **diagnostic** node-observer DaemonSet using the probe image. It is not part of the production application release. Its purpose is to inspect node-local runtime assumptions in a controlled lab. Permanent node agents belong to platform ownership, not an application team by default.

## Static Pods are a different ownership model

A kubelet can run static Pods from local manifests. The API server may show mirror Pods, but no normal API controller owns the static Pod lifecycle. Static Pods are commonly used for self-hosted control-plane components. They are not a general alternative to Deployments because cluster API changes cannot fully manage them.

## Controller choice by invariant

Use a Deployment when:

- replicas are interchangeable;
- work is continuous;
- replacement is desired;
- rollout overlap is acceptable under policy.

Use a Job when:

- completion is finite and observable;
- retries are bounded;
- effects are idempotent or deduplicated;
- success/failure exit semantics are meaningful.

Use a CronJob when:

- a schedule creates finite Jobs;
- missed and overlapping schedules have explicit policy;
- time zone and deadline behavior are deliberate.

Use a DaemonSet when:

- one Pod is required per eligible Node;
- the capability is node-local;
- platform ownership, privileges, tolerations, and upgrades are justified.

If none fits, do not immediately create a custom controller. Re-examine the workload invariant.

## Atlas controller dossier

Course 4 produces `capstone/architecture/controller-choice.yaml`:

- Atlas API: Deployment, continuous stateless request service.
- Atlas worker: Deployment, continuous queue consumer, one replica until storage/data concurrency is resolved.
- migration: release-owned Job, not init container.
- checkpoint reconciliation: CronJob with Forbid and stable operation identity.
- node observer: lab-only DaemonSet.
- stable-identity sentinel: Module 9 StatefulSet lab only.

## Worked failure: duplicate external effect

An Atlas cleanup Job removes an external object and records success in a local file. The node fails after the external deletion but before Pod success reaches the API. A replacement Pod runs and treats “object not found” as failure, retrying repeatedly.

The correct application contract is that deletion of an already absent target under the same operation ID is success. The durable effect record should not live only in Pod-local storage. Kubernetes cannot infer business equivalence from process exit.

## Worked failure: overlapping CronJob

A reconciliation task normally takes eight minutes but is scheduled every five minutes with `Allow`. Two runs update the same external index and each publishes a completion marker. The symptom is inconsistent ordering, not a CronJob controller bug.

Options include:

- `Forbid` overlap;
- a shorter schedule only after measured runtime reduction;
- partitioned work with durable ownership;
- a continuous controller instead of periodic full reconciliation.

Controller choice follows the invariant, not habit.

## Capstone increment

The course adds a bounded maintenance Job, a CronJob, and a lab-only DaemonSet. `atlas_kube/jobs.py` models attempts, completions, indexes, retry classification, deadlines, overlap, and node eligibility. The lab injects a crash after an external effect and requires exactly-once **effect** through idempotency, not exactly-once Pod execution.

## Further reading

- Jobs: <https://kubernetes.io/docs/concepts/workloads/controllers/job/>
- CronJobs: <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>
- DaemonSets: <https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/>
- Static Pods: <https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/>

## Transition

Controllers create Pods, but Pods still need runtime configuration and identity. Module 6 examines how API data is projected, when updates become visible, and why the application—not Kubernetes alone—owns reload behavior.

## Worked decision — one task, four tempting controllers

Atlas needs a nightly reconciliation report. A team proposes four designs:

1. a long-running Deployment with an internal scheduler;
2. a CronJob that creates one Job per schedule;
3. a DaemonSet that runs once per Node;
4. a custom controller that creates Pods directly.

The correct choice follows the ownership invariant. The report is a finite execution triggered by wall-clock schedule, not a continuously available service, not node-local maintenance, and not a new domain API. A CronJob owning Jobs is the smallest truthful controller graph.

The decision is still incomplete until overlap and missed schedules are defined. If a run can exceed one day, `Allow` may create concurrent reports. `Forbid` prevents overlap but can skip a scheduled run while the previous Job remains active. `Replace` cancels the old execution and assumes interruption is semantically safe. `startingDeadlineSeconds` decides how late a missed schedule may still start. Time zone must be explicit.

The Job itself provides completion accounting, not exactly-once business effects. If a Pod commits the report and crashes before the Job observes success, a retry may repeat the effect. The application must use an idempotency key such as:

```text
report-kind + scheduled logical time + report-version
```

### Indexed work and completion identity

For shardable work, an indexed Job assigns a stable completion index. That index can become part of effect identity, but it does not guarantee that only one Pod attempt ever runs for an index. Retries, node failure, and delayed status can produce overlapping attempts. The effect store must reject a second commit for the same logical completion.

### DaemonSet boundary

A DaemonSet is appropriate when desired cardinality derives from eligible Nodes: log agent, node metrics, storage plugin, or node-local networking component. It is not a substitute for “run many workers.” Its rollout and availability are tied to node eligibility, taints, and update strategy. A cluster with ten Nodes may legitimately have only four eligible DaemonSet Pods.

## Common false conclusions

- **“Job completion means the effect happened once.”** It means the controller observed the required successful Pod completions.
- **“CronJob backfills every missed schedule.”** Deadlines and controller behavior bound catch-up.
- **“DaemonSet means exactly one Pod on every Node.”** Eligibility and scheduling constraints matter.
- **“A custom controller is more flexible, therefore better.”** It adds API, ownership, upgrade, and operational obligations.
- **“A Deployment with an internal scheduler is simpler.”** It hides schedule state and run identity inside application code.

## Operational consequence — controller history is bounded

Job and CronJob objects are useful operational evidence, but history limits and TTL cleanup mean they are not an audit archive. Persist business outcome identity and evidence in the owning system before Kubernetes objects expire. Conversely, retaining every completed Job forever creates API and etcd pressure. Operational history and business records require different retention policies.
