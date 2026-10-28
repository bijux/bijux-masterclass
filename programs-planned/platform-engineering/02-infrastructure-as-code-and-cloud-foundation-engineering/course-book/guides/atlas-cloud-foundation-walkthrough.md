# Worked Walkthrough — From Host Contract to Atlas Cloud Foundation

This walkthrough follows one change through the whole course. It is not a
second capstone specification. It shows how the book's individual mechanisms
compose into one release argument.

## Starting facts

Course 1 hands over a host with three long-lived processes and one durable
filesystem boundary:

```text
atlas-edge    accepts verified HTTPS
atlas-api     accepts and persists jobs
atlas-worker  claims jobs and publishes results

/var/lib/atlas/spool and results
    durable workload facts
```

The host is locally operable, but it has no cloud account, reproducible network,
workload identity, replaceable image, or independently protected state. Course 2
must add those capabilities without changing what Atlas means.

The first architecture mistake would be to begin with a large root module that
creates “everything.” Instead, write down the ownership questions:

- Who may change the cloud foundation?
- Where does infrastructure state live?
- Which network paths exist?
- Which identity does Atlas receive?
- Which bytes survive host replacement?
- Which endpoint is public?
- How is a release reviewed and recovered?

These questions define the state and module boundaries.

## Step 1 — Bootstrap the state foundation

The state bucket and its KMS key cannot initially use the backend they create.
The bootstrap root therefore begins with local state in a controlled operator
environment. It creates:

- one uniquely named S3 bucket;
- versioning;
- KMS-backed server-side encryption;
- public-access blocks;
- a TLS-only bucket policy;
- lifecycle retention for prior versions.

The operator retains the bootstrap state under a separate recovery procedure.
After creation, the foundation and workload roots initialize with partial S3
backend configuration:

```hcl
terraform {
  backend "s3" {
    use_lockfile = true
    encrypt      = true
  }
}
```

Bucket, key, region, and KMS ARN arrive from a backend configuration file or
pipeline—not from variables, because backend initialization happens before
ordinary input evaluation.

The release evidence records the bucket ARN, backend key, KMS key, lock profile,
versioning, recovery role, and current state lineage. A green `tofu init` is not
sufficient; the state profile proof checks the safety properties explicitly.

## Step 2 — Compose the foundation root

The foundation root receives target account, region, owner, cost center, and the
stable availability-zone ID-to-name mapping for that account. A check block
compares the actual caller account to the declared target. This catches the
common but severe error of applying a valid plan to the wrong account.

The root calls focused modules:

```text
naming
network
identity
audit
```

It also owns the environment backup bucket because that bucket's ARN must be
available when the runtime role policy is created. The module graph expresses
this dependency; no `depends_on` string is needed.

The network module receives subnets keyed by stable semantic identity:

```hcl
private-a = {
  cidr    = "10.64.16.0/20"
  az_id   = "euc1-az1"
  tier    = "private"
  nat_key = "public-a"
}
```

The availability-zone name is account-relative and supplied at composition.
The key and architecture record use the stable zone ID. This prevents a
cross-account mapping change from silently becoming subnet identity.

The foundation outputs a narrow contract containing IDs and ARNs that the
workload root needs. It does not expose the whole module objects or grant the
workload root read access to every state value.

## Step 3 — Prove the network before creating compute

The plan allocates public, private, and data tiers. The dependency-light network
model verifies containment, non-overlap, zone coverage, and forbidden data-tier
default routes. Packet cases then test longest-prefix route selection.

For example, S3 access from `private-b` should select a gateway endpoint route
when present. General internet traffic selects `nat-b` only in the per-zone NAT
profile. A data subnet has no default internet target.

These are intent proofs. A real AWS lane must also inspect created route tables,
security groups, DNS, and observed flows. The course never describes the static
model as proof that AWS forwarded a packet.

## Step 4 — Create workload authority

The identity module creates an EC2 role and instance profile. The policy allows
only the environment-specific configuration, secret, KMS, and backup operations
Atlas needs. Tests include positive and negative vectors.

The most important denied vectors are adjacent to the allowed ones:

```text
read atlas/dev config           allow
read atlas/prod config          deny
read atlas/dev tagged secret    allow
read all secrets                deny
write dev result backup         allow
administer backup bucket        deny
use workload key                allow
schedule key deletion           deny
```

The runtime receives short-lived credentials from the instance metadata path.
No access key appears in HCL, user data, the image, or Course 3 handoff.

## Step 5 — Build the workload release

The workload root owns the launch template, optional sandbox instance, separate
data volume, and edge registration. The image contract identifies source,
architecture, build, and tests. The launch template requires IMDSv2 and has no
public IP.

Bootstrap is small:

- record the host-profile version;
- rely on the image for installed software and systemd units;
- start the reconciled services;
- wait for the separately managed data volume path.

A real production implementation would make mount reconciliation explicit in a
systemd mount unit or cloud-init phase. The course source keeps the runnable
AWS lane bounded and records that limitation rather than pretending a comment
mounts a volume.

This is an example of a useful review finding: HCL can be syntactically correct
while the operational contract remains incomplete. The final release requires
the replacement runbook and readiness evidence, not only resource creation.

## Step 6 — Add the public edge

The edge module creates an application load balancer, target group, TLS
listener, and edge security group when explicitly enabled. The Atlas host
security group receives one ingress rule sourced from the edge security-group
identity.

The release must provide a real certificate ARN. The module does not silently
request or validate a domain it does not own. DNS publication is a separate
owned step because zone authority and certificate authority are distinct.

Health thresholds are part of the release. With a 15-second interval and three
failures, unhealthy detection is approximately 45 seconds plus phase and timeout
behavior. Deregistration delay and process shutdown must fit the request budget.

## Step 7 — Protect and restore data

The data volume is separately encrypted and tagged. The backup path writes
canonical result objects and a manifest to a versioned, encrypted bucket.

The local capstone stops API/worker activity at a known completed-job point,
creates a manifest, copies only regular files, and restores into an empty
destination. It checks size, SHA-256, modes, and application result semantics.

This proves the course backup mechanism under a local consistency point. It does
not prove EBS snapshot consistency, S3 durability, KMS availability, or a cloud
RTO. The AWS lab adds those evidence classes when available.

## Step 8 — Review the plan as a migration

Suppose the next release moves the VPC into a child module. Without a `moved`
block, the plan proposes delete/create. With explicit moves, remote IDs remain
bound to their intended new addresses.

Now suppose an incident added a temporary deny rule. A clean module refactor
must not erase it blindly. The drift record carries the incident ID, owner, and
expiry; the release decides whether to adopt or remove it.

Infrastructure review is therefore not a search for zero changes. It is a
search for explainable, owned changes whose user and recovery consequences are
known.

## Step 9 — Bind the release

The final candidate binds:

```text
source digest
provider/module lock digest
backend lineage and serial
target account and region
saved plan digest
policy result
cost and quota assumptions
reviewer and approval
apply identity
data-plane and recovery evidence
```

A changed source or dependency invalidates the plan. A changed plan invalidates
approval. A different target invalidates the evidence.

The dependency-light release is classified `dependency-light-only` because no
AWS API was called. That is a successful bounded course outcome, not a hidden
failure. The AWS-backed learner can produce the additional control/data-plane
evidence through explicit guarded targets.

## Step 10 — Hand off to containers

Course 3 receives no raw state or backend credential. It receives the workload
contract:

- process and port model;
- users and filesystem ownership;
- durable paths;
- workload IAM permissions;
- configuration and secret sources;
- health and shutdown behavior;
- network ingress/egress;
- supported architectures;
- image/bootstrap boundary;
- release and evidence requirements.

The container course can now change packaging without guessing the platform
contract. That is the purpose of a cumulative program: every abstraction change
preserves the proven responsibilities beneath it.
