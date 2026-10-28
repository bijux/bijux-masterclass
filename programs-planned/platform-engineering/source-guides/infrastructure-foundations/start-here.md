# Start Here — Platform Engineering

Platform engineering is the design and operation of **trusted capabilities** that let other teams deliver software without rediscovering every systems problem. This program does not begin with Kubernetes. It begins with the lower layers that Kubernetes and cloud platforms later hide.

The learner follows one Atlas workload through ten courses. Each course accepts a versioned handoff, adds one major responsibility, and exports evidence for the next course.

## The first two courses

Course 1 operates Atlas directly on Linux. It establishes process identity, service supervision, resource envelopes, durable file transitions, packet paths, DNS, TLS, proxies, virtual machines, workload identity, storage classes, and failure-domain requirements.

Course 2 does not repeat those topics. It asks a harder question:

> How can those requirements become a reproducible cloud foundation whose changes are planned, reviewed, locked, recoverable, and safe to hand to another operator?

The answer is not “write Terraform.” Infrastructure as code is a control system with three representations that can disagree:

```text
configuration intent
        ↓
recorded state
        ↓
remote infrastructure
```

The course teaches how to reason when those representations diverge.

## Study rule

For every mechanism, answer:

1. What desired state is declared?
2. Which identity may change it?
3. What does state remember that configuration does not?
4. What remote fact can make a plan wrong or incomplete?
5. Which failure leaves the platform in a dangerous half-state?
6. Which evidence would permit another operator to continue safely?

## Evidence levels

- **Level A — dependency-light:** course models, HCL/static checks, plan fixtures, policy tests, and deterministic state simulations.
- **Level B — OpenTofu local:** real formatting, initialization, tests, plan files, state operations, and local-provider behavior.
- **Level C — cloud sandbox:** real AWS identity, VPC, storage, compute, load balancer, DNS, KMS, quotas, and billed resources.
- **Level D — organizational foundation:** multiple accounts, centralized logs, organization policy, identity federation, delegated administration, and controlled production delivery.

A Level A check may prove a rule. It cannot prove that AWS accepted the corresponding API calls or that the resulting data plane behaved correctly.

## Reader path

Read the Course 2 book in order. Do not begin by applying the production stack. First complete the orientation, establish a cost-bounded sandbox, and understand the state bootstrap. The course deliberately makes destructive operations inconvenient.
