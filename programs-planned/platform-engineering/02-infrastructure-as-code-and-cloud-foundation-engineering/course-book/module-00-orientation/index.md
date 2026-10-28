# Orientation — Establish a Safe IaC Laboratory

Course 2 begins by verifying the Course 1 handoff and establishing an environment where mistakes are observable and bounded.

## Required local capabilities

- Python 3.12 or newer;
- a POSIX shell;
- Git;
- JSON and YAML tooling;
- OpenTofu 1.12.5 for Level B work;
- AWS CLI v2 for Level C work.

## Required cloud boundary

Real-cloud work uses a disposable account, not a production account. Record the expected AWS account ID, allowed region, cost budget, teardown deadline, and operator identity. The course uses `eu-central-1` in examples; another region is acceptable when equivalent services exist.

## Credential strategy

Use IAM Identity Center or another short-lived federation path. Do not create access keys merely to complete the course. Provider configuration obtains credentials from the standard AWS credential chain; credentials never appear in `.tfvars`.

## Predecessor lock

Run:

```bash
make predecessor-proof
```

The proof hashes all nine predecessor files. If they differ from Course 1, stop and determine whether the change is an intentional handoff version or accidental mutation.

## Cost boundary

The Level A and B course can be completed without charges. Level C resources such as NAT gateways, load balancers, EC2, EBS, public IPv4, and log delivery cost money. The real-cloud labs use short lifetimes and explicit cleanup.

## Orientation outcome

You finish orientation with:

- a verified predecessor package;
- a local tool inventory;
- an optional sandbox account record;
- an evidence directory;
- an explicit choice of evidence levels for each module.
