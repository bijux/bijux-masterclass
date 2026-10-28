# Atlas Cloud Foundation 1.0

This capstone turns the Atlas Host Runtime from Course 1 into a reproducible,
reviewable cloud foundation. The course has two deliberately separate lanes:

- **dependency-light semantic lane** — executable planning, state, network,
  identity, compute, backup, migration, and release models;
- **AWS execution lane** — real OpenTofu modules and roots for a controlled
  sandbox account.

The semantic lane teaches invariants and runs without cloud credentials. It is
not represented as an AWS emulator. The AWS lane is never executed by the
normal proof route and requires an explicit preflight and opt-in.

## Architecture

```text
Course 1 host contract
          |
          v
OpenTofu state foundation
          |
          v
AWS account / identity boundary
          |
          v
VPC: public, private, and data tiers
          |
          +----> TLS load-balancer edge
          |
          +----> private Atlas host + instance role
          |
          +----> encrypted data volume
          |
          +----> versioned backup and audit storage
```

Start with:

```bash
make capstone-tour
```

For a real AWS sandbox, read `../course-book/guides/cloud-account-safety.md`
and use only the guarded `aws-*` targets.
