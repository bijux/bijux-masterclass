# Worked answers — Delivery systems, GitOps authority, and reconciliation

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why is a successful deployment pipeline run insufficient evidence that the environment remains correct?

A pipeline reports one bounded execution. After it exits, Kubernetes controllers, admission, humans, secret rotation, node failure, and cloud controllers continue changing the environment. Continuous reconciliation adds ongoing observation, but even reconciliation proves only owned-state convergence. Correctness still requires health, user-journey, and data evidence. The pipeline result therefore belongs in the release dossier as one observation, not as a permanent truth about the environment.

## 2. What precise problem is solved by promoting an image digest instead of rebuilding from the same source tag?

Digest promotion preserves subject identity. Staging evidence applies to the exact bytes identified by the digest. Rebuilding can change compilers, dependencies, timestamps, base images, or build inputs even when the source tag is unchanged. The production artifact would then be a new candidate requiring fresh evidence. Digest promotion prevents the release process from silently substituting an untested artifact.

## 3. Why is a Git branch not an adequate desired-revision identity?

A branch is a movable reference. Two controller observations of `main` can resolve to different commits, and a rollback record that says only `main` cannot reconstruct the earlier desired state. A promotion record should store the immutable commit and every external artifact digest. The branch remains useful as a workflow pointer, but it is not the release identity.

## 4. Give an example of synchronized state that is not healthy and healthy state that is not correct.

A Deployment can match the rendered replica count and image digest while its Pods fail readiness, so it is synchronized but unhealthy. Conversely, Pods may be Ready and the Deployment may be healthy while the application returns semantically incorrect results because a schema migration changed interpretation. Health is based on declared resource signals; business correctness requires separate journey and data evidence.

## 5. Why can a GitOps controller not infer that a retained PersistentVolume is safe to prune?

The controller sees only that the resource is absent from its current desired inventory. It does not own the data-retention decision, backup obligations, recovery-key availability, or legal retention policy. Course 6 transfers explicit protected-resource rules. A data owner must publish retirement evidence before deletion becomes authorized. Absence from Git is therefore insufficient evidence.

## 6. When should self-heal be suspended during an incident?

Self-heal should be suspended for the smallest affected scope when the controller would repeatedly undo a necessary emergency mitigation or when the desired revision itself is suspected unsafe. Suspension must be time-bounded, audited, and paired with a path to commit the intended durable state. Disabling all reconciliation indefinitely creates a second unmanaged truth and is not a valid recovery strategy.

## 7. What is the ownership difference between CI and CD in Atlas?

CI owns transformation from source to immutable artifact plus build and test evidence. CD owns selection, rendering, promotion, reconciliation, and environment evidence for already-built artifacts. CI must not decide production rollout merely because a build passed, and CD must not rebuild artifacts during promotion. The separation preserves evidence subject identity.

## 8. Why is “pull based” not a complete security argument?

A pull controller avoids distributing cluster credentials to every CI runner, but the controller still holds repository credentials, Kubernetes write authority, and possibly decryption keys. Webhooks and image automation introduce additional write paths. Security depends on scoped identities, destinations, repositories, fields, and audit, not on the direction label alone.

## 9. How should controller-generated or admission-generated fields be handled in drift analysis?

They should be classified by field ownership and normalization policy. A delivery controller should compare fields it legitimately owns and preserve other managers’ fields. Blindly forcing the complete live object to match source can erase defaults, policy mutations, or controller state. Ignoring all differences is equally unsafe. Managed fields, schemas, and documented ignore rules provide the evidence boundary.

## 10. Why does a break-glass change require reconciliation back into Git?

Without reconciliation, the environment has two competing truths: the reviewed repository and the manually altered cluster. Future automation may undo the mitigation or preserve an undocumented dependency. Committing the intended durable state restores review, reproducibility, and recovery. The incident record should retain both the emergency action and the later reviewed revision.

## 11. What does a rendered-set digest prove, and what does it not prove?

It proves that a particular renderer version and input set produced an exact canonical resource collection. It detects hidden rendering changes and supports comparison across environments. It does not prove that the Kubernetes API accepted the objects, that a controller applied them, that workloads became healthy, that data migrations were safe, or that users received correct service.

## 12. Design a minimal release status that avoids the single-green-icon problem.

Record immutable source and artifact identities, render digest, sync state, resource health, progressive-exposure result, user-journey result, data/recovery gates, policy result, evidence class, and unresolved limitations. Each field should have its own timestamp and source. The overall decision can be accepted, rejected, review-required, or not-executed, but must not erase the component states.
