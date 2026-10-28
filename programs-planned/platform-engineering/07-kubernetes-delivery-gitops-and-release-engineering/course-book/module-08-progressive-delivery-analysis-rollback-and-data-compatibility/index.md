# Module 8 — Progressive delivery, analysis, rollback, and data compatibility

## Central question

**How can a candidate receive real traffic gradually while the platform distinguishes meaningful evidence from reassuring noise and preserves a safe abort path?**

Progressive delivery is not a slower rolling update. It is a controlled experiment in which candidate and stable revisions coexist, traffic exposure changes deliberately, analysis evaluates predeclared signals, and abort behavior is known before promotion begins.

## Deployment strategy versus release strategy

Kubernetes Deployment rolling updates manage replica replacement. They can preserve a minimum available population and limit surge. They do not decide whether the new revision is semantically correct.

A release strategy adds:

- candidate identity;
- stable identity;
- traffic allocation;
- analysis windows;
- success and failure thresholds;
- pause and approval points;
- abort behavior;
- data and contract compatibility;
- final promotion evidence.

Blue-green and canary are strategies for exposure. Neither guarantees safety without good signals and compatible state.

## Blue-green

Blue-green keeps stable and preview populations separate. A Service or Gateway switch moves production traffic to the preview revision after checks. This makes rollback of traffic fast while both populations exist.

Risks include:

- doubled capacity during overlap;
- stale connections after Service switch;
- background workers running in both colors;
- shared database compatibility;
- external side effects produced by preview;
- preview tests that do not represent production traffic.

Atlas permits only one writer authority for stateful side effects unless the workflow is explicitly idempotent and partitioned.

## Canary

A canary receives a fraction of traffic while stable continues serving the majority. Exposure may increase by steps such as 1%, 5%, 20%, 50%, and 100%. Percentage alone is insufficient. At low traffic, 1% may produce too few samples; at high traffic, 1% may still affect thousands of users.

The plan must specify minimum sample count, observation duration, request mix, tenant and region distribution, and excluded populations. A canary that receives only health checks is not an experiment.

## Analysis signals

A useful analysis metric has:

- a precise numerator and denominator;
- bounded delay;
- enough volume;
- stable dimensions;
- a known source;
- a relation to the changed failure mode;
- a threshold and decision rule;
- behavior when data is absent.

Generic CPU or Pod readiness may detect infrastructure failure but miss semantic regression. User-journey success, error rate, tail latency, saturation, and domain-specific correctness should be selected according to the change.

A missing metric is not automatically success. Atlas classifies analysis as pass, fail, inconclusive, or unavailable.

## Comparison design

Candidate and stable should be compared over equivalent populations. Differences in tenant mix, endpoint mix, cache warmth, region, or request size can make the candidate appear better or worse for unrelated reasons.

Atlas analysis records:

- stable and candidate revision IDs;
- traffic allocation and actual observed counts;
- time window;
- population filters;
- metric query and result;
- missing-data behavior;
- threshold;
- analysis implementation version.

A dashboard screenshot without these details is not reproducible release evidence.

## Argo Rollouts and traffic routing

Argo Rollouts extends Kubernetes with `Rollout`, `AnalysisTemplate`, and related resources. It can coordinate ReplicaSets, Services, and traffic providers for canary or blue-green strategies. The controller's ability to shift traffic depends on the selected router and its status.

Atlas includes a reference Rollout and AnalysisTemplate. The semantic mandatory lane models traffic and analysis without claiming a real Gateway or mesh controller executed.

The release engineer must inspect both workload and router state. A Rollout can believe a step is active while the external data plane has not converged, or vice versa. Actual traffic observations are part of the oracle.

## Flagger and Flux comparison

Flagger is a common progressive-delivery companion in Flux ecosystems. It observes metrics and controls routing through supported providers. The conceptual invariants remain the same: immutable candidate, explicit analysis, bounded exposure, and safe abort.

Course 7 does not require duplicated Argo Rollouts and Flagger labs. It requires the learner to map both to the same release model.

## Feature flags

Feature flags can decouple code deployment from user exposure. They are another control plane with identity, targeting, audit, rollback, and stale-configuration risks.

A flag can reduce deployment risk when the old and new code paths coexist safely. It cannot rescue an incompatible database migration that makes the old binary unable to run. Flag state must be part of incident and release evidence when it controls behavior.

## Data compatibility

Course 6 defines expand, compatible readers, backfill, writer cutover, old-writer removal, and contract phases. Progressive delivery must respect that order.

A canary binary and stable binary may run simultaneously. They must both read the current schema, and only authorized writers may produce new representations. If the candidate starts writing data the stable revision cannot read, traffic rollback will not restore service.

Atlas blocks progressive exposure unless the compatibility matrix states:

- stable reads old and new state;
- candidate reads old and new state;
- writer authority is explicit;
- backfill is resumable;
- rollback remains possible during the selected window.

## Rollback is a compatibility decision

A rollback can mean:

- route traffic back to stable;
- scale candidate to zero;
- select a prior Git revision;
- restore prior configuration;
- disable a feature flag;
- compensate an external effect;
- restore data from backup.

These operations have different costs and evidence. The delivery controller can automate some. It cannot infer which data action is safe.

Atlas release plans state a **rollback frontier**: the latest phase at which traffic and manifests can return safely without data recovery. After writer cutover or contract migration, the correct response may be a forward fix rather than rollback.

## Manual pauses and approvals

A pause is useful when evidence needs human interpretation or when a business window controls exposure. A pause without an owner, deadline, and resumption criterion becomes stuck state.

Approvers should see the candidate identity, actual traffic, analysis results, data phase, remaining risk, and abort action. “Looks good” is not an auditable approval reason.

## Abort behavior

Abort should be tested before production. The plan must answer:

- how traffic returns to stable;
- how existing connections behave;
- what happens to candidate background work;
- how candidate events or side effects are identified;
- whether database writes remain compatible;
- whether the Git desired state changes automatically or by reviewed commit;
- how analysis and incident evidence are retained.

An automatic abort that changes cluster state but leaves Git selecting the candidate creates drift and may be undone by GitOps reconciliation. Atlas writes a reviewed or controller-generated rollback proposal with stable identity and records the emergency action.

## Misleading analysis patterns

### Aggregate success hides one tenant

The overall error rate passes while a high-value tenant fails completely. Segment the metric where the change has differentiated risk.

### No traffic means zero errors

A candidate receives no production traffic and passes because the denominator is zero. Require minimum samples.

### Metric delay exceeds analysis window

The controller promotes before late failures arrive. Choose a window longer than collection and processing delay.

### Stable is already degraded

Relative comparison makes the candidate look acceptable because both are bad. Enforce absolute and comparative thresholds.

### Retry hides failures

Client or proxy retries make success rate look good while latency and backend load explode. Observe original attempts, retries, and useful outcomes separately.

## Atlas progressive-delivery contract

Atlas requires:

1. immutable stable and candidate identities;
2. actual traffic counts, not configured weights alone;
3. minimum sample and maximum analysis delay;
4. absolute and comparative thresholds;
5. segment coverage for affected populations;
6. explicit missing-data outcome;
7. stable/candidate data compatibility;
8. tested abort and Git reconciliation behavior;
9. rollback frontier and forward-fix boundary;
10. evidence retention for every step and decision.

Module 9 expands from one environment to a cluster fleet. The same desired revision, controller version, and progressive strategy must survive version skew, partial reachability, bootstrap dependency, and regional failure.

## Deep-dive practicum

### Designing an analysis that can actually falsify the release

Start from the candidate’s failure hypothesis, not from the metrics already on a dashboard. If a new serialization path may corrupt large artifact metadata, CPU utilization is weak evidence. The analysis should exercise large artifacts, compare semantic checksums, and segment by payload class. Infrastructure signals still matter, but they do not replace the changed behavior’s oracle.

For every metric, record:

- exact query and implementation version;
- candidate and stable subjects;
- eligible and excluded populations;
- actual sample counts;
- collection and processing delay;
- absolute and relative thresholds;
- behavior when unavailable;
- decision contribution.

This turns the analysis from a screenshot into a reproducible claim.

### Configured weight is not exposure

A controller setting 10% weight expresses desired routing. Actual exposure depends on endpoint readiness, router convergence, connection reuse, retries, session affinity, and request distribution. Atlas records both configured weight and observed candidate attempts. If no candidate attempts occur, the analysis is inconclusive even when the metric query returns zero errors.

At small scale, a replica-weight canary may not approximate traffic weight. At large scale, one percent can still be a large blast radius. Choose the router and step plan according to the risk and traffic shape.

### Data phases dominate rollback semantics

Consider stable `S` and candidate `C` during writer cutover:

| Revision | Reads old | Reads new | Writes old | Writes new |
|---|---:|---:|---:|---:|
| S | yes | yes | yes | no |
| C | yes | yes | no | yes |

Traffic can move between S and C while both read both representations. Once old-writer support is removed or the schema contracts, S may no longer be safe. The rollout controller cannot infer this from Pod health. The data-release ledger supplies the rollback frontier.

A progressive controller should therefore consume a compatibility gate, not execute destructive migration logic itself.

### Abort is a multi-control-plane operation

An abort may require:

1. router weight returned to stable;
2. candidate background workers stopped or fenced;
3. Git desired state changed or reconciliation suspended;
4. feature flags restored;
5. data writer phase checked;
6. external effects compensated or quarantined;
7. evidence retained for the incident.

If only step one occurs, GitOps may restore the candidate. If only Git is reverted, existing router state or long-lived connections may continue exposure. The laboratory forces you to make the abort state machine explicit.

### Avoiding metric theater

A sophisticated metric stack can still produce a meaningless decision. Common forms of metric theater include averaging away one failing tenant, comparing different traffic populations, promoting before telemetry delay elapses, and counting retried success without original failures. The cure is not more graphs. It is a predeclared experiment with a falsifiable hypothesis and bounded missing-data rules.

The final release decision must preserve the raw analysis evidence and explain why each signal was relevant to the candidate’s change.
