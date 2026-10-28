# Capstone — Atlas Cloud Foundation 1.0

Atlas Cloud Foundation translates Course 1’s provider-neutral requirements into an AWS reference foundation.

## Baseline architecture

```text
                    public DNS
                        |
                        v
                 HTTPS load balancer
                  /              \
       public subnet A        public subnet B
                 |                 |
                 +--------+--------+
                          |
                    private subnet A
                          |
                    Atlas instance
                    /            \
       encrypted root       encrypted data volume
                          |
                 versioned snapshot policy

Control and evidence services:
- S3 remote state with versioning and native lock file
- KMS keys
- IAM role and instance profile
- CloudTrail and VPC Flow Logs
- S3 backup destination
- budgets and tags
```

The network spans two availability zones. The workload is intentionally one instance in one zone. The design is not described as highly available.

## Why AWS is the executable lane

A course needs one lane deep enough to expose real resource semantics. AWS is used because the program must make account boundaries, VPC routing, IAM roles, IMDSv2, load-balancer health, EBS zonal behavior, S3 state, KMS, and cost-visible egress concrete. Comparison notes map the concepts to Google Cloud and Azure without asserting equivalence.

## Capstone outputs

- `bootstrap/` creates the remote-state bucket and key.
- `modules/` contains flat, composable architectural modules.
- `stacks/foundation/` assembles account-local shared infrastructure.
- `stacks/workload-dev/` chooses a cost-bounded single-instance profile.
- `stacks/workload-prod/` demonstrates stronger egress and retention policy without claiming workload HA.
- `cloud_model/` provides a dependency-light execution and state model.
- `policies/` rejects unsafe plans.
- `fixtures/` contains accepted, rejected, drifted, imported, and refactored cases.
- `handoff/` exports requirements for OCI and software-supply-chain engineering.

## Final defense

The learner must demonstrate:

1. state bootstrap and recovery reasoning;
2. one approved plan and one rejected destructive plan;
3. module interface ownership;
4. route and exposure correctness;
5. short-lived workload authority;
6. instance replacement without losing the declared durable-state path;
7. backup restore into an empty target;
8. a configuration-driven import;
9. a refactor using `moved` blocks;
10. a policy-governed release and complete teardown record.
