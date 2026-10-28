# Start Here

## What this course assumes

You completed Course 1 or can already reason about Linux processes, filesystems, TCP/IP, DNS, TLS, virtual machines, cloud identities, and failure domains. You do not need previous OpenTofu or Terraform experience.

## What changes in this course

Course 1 operated one host. Course 2 adds a second kind of system: the **infrastructure control process**.

```text
Git commit
   ↓
OpenTofu configuration
   ↓
plan
   ↓
approved apply identity
   ↓
cloud control-plane APIs
   ↓
remote objects
   ↓
state snapshot
```

Every arrow can fail. A plan can become stale. An apply can partially succeed. State can be locked, lost, leaked, or restored to the wrong generation. A resource can exist but serve no traffic. A module can be valid yet unsafe for its caller.

The course therefore uses three views at once:

- **configuration** — what the repository declares;
- **state** — what the tool remembers and associates with resource addresses;
- **remote reality** — what the provider currently reports and what the data plane actually does.

## Primary and comparison lanes

The executable reference lane is AWS with OpenTofu. Google Cloud and Azure appear in comparison tables where their differences matter. The course does not pretend that a VPC, VNet, and Google VPC network are identical products.

## Cloud safety

No default command creates resources. Real-cloud labs require:

- a disposable sandbox account;
- a named operator identity or IAM Identity Center session;
- a budget and alert;
- an explicit region allowlist;
- a teardown owner;
- an evidence directory outside state;
- confirmation that no production account is selected.

Do not use root credentials. Do not paste long-lived access keys into variables, provider blocks, state, or shell history.

## How to study

For each module:

1. Read the chapter completely.
2. Write your own answer to the exercises.
3. Compare with the worked answers.
4. Run the dependency-light lab.
5. Run the OpenTofu or AWS extension only when its environment is available.
6. Keep the checkpoint evidence.

The checkpoint is a progression gate. Reading alone is not completion.
