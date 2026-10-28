# Production Claims and Boundaries

Atlas Cloud Foundation is **production-shaped course infrastructure**, not an operated production landing zone.

The package can prove, without cloud credentials:

- consistency of the requirement map;
- state-lock and recovery semantics in the course model;
- CIDR non-overlap and route intent;
- module interfaces and composition rules;
- policy rejection of known unsafe changes;
- deterministic release classification;
- exact predecessor and successor handoffs.

A real AWS sandbox is required to prove:

- provider authentication and API behavior;
- IAM policy effects;
- route and security-group behavior;
- load-balancer health and draining;
- IMDSv2 enforcement;
- EBS attachment and snapshot restore;
- S3 state locking and version recovery;
- CloudTrail and flow-log delivery;
- quotas, capacity, cost, and teardown.

A multi-account organizational environment is required to prove delegated administration, organization policies, centralized logging, account vending, and production identity federation.

The baseline workload remains single-instance. A two-zone VPC and regional load balancer do not convert single-instance compute and zonal data into a multi-zone service.
