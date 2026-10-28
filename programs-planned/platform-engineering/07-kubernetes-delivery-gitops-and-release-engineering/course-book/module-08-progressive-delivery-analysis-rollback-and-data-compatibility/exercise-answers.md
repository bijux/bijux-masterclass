# Worked answers — Progressive delivery, analysis, rollback, and data compatibility

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why is a Kubernetes rolling update not a complete progressive-delivery strategy?

It controls replica replacement and availability bounds but does not compare candidate correctness, allocate representative traffic deliberately, evaluate domain signals, or define data compatibility and abort evidence. Progressive delivery adds those release decisions.

## 2. What makes a low canary percentage statistically useless?

If actual request volume is low or traffic is not representative, the candidate receives too few samples to detect the target failure. The plan needs minimum sample count and population coverage, not only a configured weight and duration.

## 3. Why must missing analysis data have an explicit outcome?

Treating no data as success promotes candidates when telemetry is broken or no traffic reached the canary. Treating all absence as failure can cause unnecessary aborts during known metric outages. Policy should classify missing data as fail, inconclusive, or unavailable according to the signal’s necessity.

## 4. Why should stable and candidate traffic populations be compared carefully?

Different tenant, endpoint, region, payload, or cache populations can dominate metric differences. Without equivalent or adjusted populations, analysis attributes unrelated variation to the candidate. Release evidence must record actual distributions and filters.

## 5. What extra evidence is needed when Argo Rollouts changes a configured traffic weight?

Observe the actual router or Gateway state and measured request distribution. Controller status proves intended step, not data-plane convergence. Existing connections, retries, and provider lag can make actual exposure differ from configuration.

## 6. How can a feature flag improve rollback and still fail to make rollback safe?

It can disable a new code path without redeploying, but if the candidate already wrote incompatible data or changed an external contract, the stable path may still fail. Flags control behavior exposure, not all state transitions.

## 7. What is the rollback frontier?

The latest release phase at which stable traffic and prior manifests can be selected without data restoration or incompatible side effects. Beyond that point, writer cutover or schema contraction may make forward repair safer than rollback.

## 8. Why can an automatic traffic abort conflict with GitOps?

The progressive controller may restore stable routing in the cluster while Git still selects the candidate. GitOps can later reapply candidate state. The incident path must update or suspend desired-state reconciliation and produce a durable rollback revision or proposal.

## 9. Why are absolute thresholds needed in addition to stable-relative comparison?

If stable is already degraded, a candidate that is equally bad may pass relative comparison. Absolute service objectives prevent promotion when both revisions violate acceptable behavior.

## 10. What evidence should a manual pause approver receive?

Candidate and stable identities, actual exposure, metric populations and results, data phase, unresolved risk, required next step, abort procedure, and deadline. Approval should record a reason tied to those facts rather than a generic acknowledgment.

## 11. How can retries make a canary appear healthier than it is?

Retries convert backend failures into eventual client successes while increasing latency and load. Success rate alone hides the original attempt failures and retry amplification. Measure original attempts, retry counts, useful completion, and resource saturation.

## 12. When is a forward fix preferable to rollback?

When state or external contracts have crossed the rollback frontier: stable cannot read new data, a destructive migration completed, or external effects cannot be reversed. The release plan should identify this boundary before exposure and maintain a tested forward-repair path.
