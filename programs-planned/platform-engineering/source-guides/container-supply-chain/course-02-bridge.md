# Course 2 Bridge — From Host Guarantees to Cloud Resources

Course 1 exported fourteen cloud-foundation requirements. They are intentionally provider-neutral. Course 2 maps them to an AWS reference implementation while preserving the distinction between a requirement and a product name.

| Host guarantee | Cloud-foundation mechanism | Evidence |
|---|---|---|
| Replaceable compute | versioned image, launch template, deterministic boot contract | plan, image identity, replacement transcript |
| No long-lived workload keys | EC2 role and instance profile | credential source, IAM policy, negative static-key scan |
| Only TLS edge is public | public load balancer; private workload subnet | route and security-group evidence, negative reachability test |
| Durable state independent of root image | separate encrypted EBS volume and snapshots | attachment identity, replacement/restore proof |
| Backup in another failure domain | versioned S3 backup bucket and restore exercise | object identity, retention, empty-target restore |
| Metadata protection | IMDSv2 required and limited hop behavior | launch-template metadata options |
| Explicit IPv4/IPv6 decision | address plan and route tables | CIDR proof, DNS alignment, reachability test |
| Distinct liveness/readiness | target-group health contract | health reason codes, route eligibility |
| Cost and quota awareness | tagged resources, budget, quota worksheet | cost estimate, quota snapshot, teardown record |

Course 2 remains honest about its baseline: Atlas Cloud Foundation 1.0 is a **single-workload-instance design** inside a two-zone network foundation. The network is ready for later evolution; the workload is not falsely described as highly available.
