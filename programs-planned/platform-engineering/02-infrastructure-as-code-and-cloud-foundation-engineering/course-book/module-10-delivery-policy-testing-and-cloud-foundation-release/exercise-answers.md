# Worked Answers — Delivery, Policy, Testing, and Release

## 1. Authority map

The author proposes source without mutation authority. Validation runs local checks. The plan role reads state and remote configuration. Reviewers approve one plan/policy result. The apply role mutates only the target environment using the approved artifact. The verification role exercises bounded data-plane capabilities. Combining all roles makes review mostly cosmetic.

## 2. Saved-plan binding

Bind source digest, modules, provider lock, tool version, backend/state identity and serial, target account/region, non-secret variable digest, plan digest, policy result, reviewer, approval time/expiry, and apply role. Otherwise approval may be reused for different bytes or target.

## 3. Long-lived CI keys

They have no natural short session, are difficult to bind to repository/environment claims, can be copied outside the runner, and require manual rotation/revocation. Federation produces auditable short-lived sessions and narrower trust conditions. Encrypted storage protects at rest, not after the runner reads the key.

## 4. Policy and review

Machine rules can reject public SSH, optional IMDS tokens, unencrypted protected storage, broad IAM, or deletion of the state backend. Architecture review decides whether account boundaries fit ownership and whether centralized egress is worth its cost/availability trade-off. Those decisions depend on context not fully visible in one plan.

## 5. Test layers

Static validation checks syntax/configuration properties. Module tests exercise input/output and plan behavior. Integration tests create disposable cloud resources and validate provider/API relationships. Data-plane tests exercise DNS, TLS, requests, jobs, and recovery. Passing one layer cannot replace the later layers.

## 6. Dependency lock

It records the exact provider selections and checksums. Review prevents an unexamined provider binary change from entering an apply. Committing the file also makes local and CI resolution more reproducible.

## 7. `not-executed`

The proof was required but the environment/tool/authority was unavailable. It represents missing evidence, not a neutral success. Counting it as pass would turn absence into assurance.

The release decision must remain blocked or explicitly scoped to a weaker evidence class until that proof is executed in an authorized environment.

## 8. Cost and quota

A release that exceeds budget or cannot allocate temporary replacement capacity is not operable. Cost evidence identifies recurring resources and assumptions; quota evidence proves enough headroom for planned actions and rollback. Uncertainty may require review rather than false precision.

## 9. Lock versus lease

The backend lock prevents concurrent state mutation during an operation. An environment lease records who owns an ephemeral environment and when it should be cleaned up. A lock is short-lived operation coordination; a lease is lifecycle/governance metadata.

## 10. Partial apply

Stop promotion, preserve state/backend version and logs, inventory actual ALB/volume state, check exposure and cost, contain urgent risk, then plan from current reality. Decide roll-forward or cleanup based on dependencies. Do not delete resources from the console before understanding their state bindings.

## 11. Rollback limits

DNS caches, data mutations, resource replacement, key changes, provider schema changes, and consumer adoption can persist after old HCL is restored. Recovery may require data restore, traffic switching, or roll-forward rather than an inverse apply.

## 12. Course 3 handoff

Provide process/port contracts, filesystem and persistent-volume paths, runtime user and permissions, workload cloud permissions, ingress/egress, health endpoints, configuration/secret sources, architecture, image/bootstrap boundaries, logging, resource envelope, release/evidence requirements, and known migration risks. Containerization must not guess these facts.
