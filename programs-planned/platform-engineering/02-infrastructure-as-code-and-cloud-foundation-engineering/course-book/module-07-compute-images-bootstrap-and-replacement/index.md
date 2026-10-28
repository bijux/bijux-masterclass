# Module 7 — Compute, Images, Bootstrap, and Replacement

The first Atlas host was assembled by hand so that its processes, files, identities, sockets, and failure modes were visible. A cloud foundation cannot depend on that history. A replacement machine must start from a versioned image and a small, reviewable bootstrap contract, assume the correct identity, attach the correct storage, prove readiness, and be discarded when it no longer matches the release.

This module is about the **machine lifecycle**, not merely the `aws_instance` resource. The important object is the relationship among an image, a launch definition, an instance identity, durable data, health evidence, quotas, and a replacement procedure.

## Learning outcomes

By the end of this module, you will be able to:

- separate image contents, launch configuration, runtime configuration, and durable state;
- explain why user data is a bootstrap channel rather than a secret store or general configuration database;
- design a launch template with versioned, reviewable inputs;
- choose deliberately among a singleton instance, an Auto Scaling group, and a managed compute service;
- distinguish instance health, process health, application readiness, and load-balancer health;
- reason about replacement capacity, availability-zone placement, and quota headroom;
- preserve or rebuild Atlas state without treating an instance root disk as durable storage;
- use IMDSv2 and instance roles without exposing static cloud credentials;
- design image updates, security patching, rollback, and decommissioning as release operations;
- state what remains unproved without an actual cloud instance.

## Begin with the replacement question

Before choosing an instance type or writing HCL, ask:

> If this machine disappears now, which facts are lost, which facts are reconstructed, and which service objective is violated?

A sound answer classifies every important fact:

| Fact | Owner | Replacement source |
|---|---|---|
| operating-system packages | image pipeline | immutable image |
| Atlas binaries | application release | image or signed artifact |
| systemd units | host profile | image/config package |
| non-secret runtime settings | environment release | parameter/config source |
| workload credentials | cloud identity service | instance role and metadata service |
| TLS private key | secret/certificate service | controlled retrieval or managed termination |
| queued jobs | Atlas durable spool | attached durable volume or external service |
| completed results | Atlas result store | durable storage/backup |
| local logs | telemetry pipeline | remote sink; local copy is disposable |

If the answer is “the root volume,” the machine is still a pet. It may run reliably for a while, but it cannot be replaced predictably.

## Four different artifacts

### Machine image

The image defines the bootable filesystem and low-level host baseline. It should contain stable, non-secret material that changes through a controlled image release:

- operating-system version;
- security updates present at image build time;
- required packages and agents;
- Atlas application or an installer with a fixed digest;
- systemd unit files;
- filesystem layout;
- baseline hardening.

An image identifier is not sufficient evidence. Record its source revision, build inputs, package inventory, builder identity, test result, and digest where the platform exposes one.

### Launch definition

The launch definition describes how the image becomes a cloud instance:

- image identifier;
- instance architecture and type;
- subnet and security groups;
- instance profile;
- root and data volumes;
- metadata-service policy;
- user data;
- tags;
- monitoring options.

In AWS, a launch template gives this definition a versioned identity. Referencing `$Latest` or changing an instance in place makes rollback ambiguous. Atlas records an explicit launch-template version in its release evidence.

### Runtime configuration

Values that vary by environment but are not machine-image concerns belong in a controlled runtime configuration path. Examples include a public hostname, log destination, feature gate, or queue directory. The path must answer:

- who may write the value;
- who may read it;
- how a change is reviewed;
- whether the value appears in state;
- how a process observes a new version;
- what happens if retrieval fails.

### Durable state

Durable workload state is independently protected and restored. Course 2 keeps Atlas on one host to keep the systems boundary visible, but it moves the spool and result store onto an explicitly managed data volume with snapshot and restore policy. The root volume remains replaceable.

## User data: useful, visible, and frequently abused

Cloud-init and user data are useful for the last, small amount of boot-time composition. They are poor places for:

- static passwords;
- cloud access keys;
- private TLS keys;
- large shell installers fetched from a mutable URL;
- an entire application deployment system;
- logic that cannot be replayed safely.

User data can appear in instance metadata, provider state, console output, logs, and support evidence. Treat it as non-secret. Keep it small and deterministic.

A good Atlas bootstrap performs bounded tasks:

1. verify the expected image/profile version;
2. mount and validate the durable data volume;
3. write an environment identifier and non-secret endpoint configuration;
4. start already-installed services;
5. publish a bootstrap result that readiness can consume.

A bad bootstrap downloads “latest,” edits packages in an unbounded loop, creates identities ad hoc, and reports success because the shell exited zero.

## Idempotence is not enough

A bootstrap script may be idempotent and still be unsafe. Consider:

```bash
curl -fsSL https://example.invalid/install.sh | sh
```

Running it twice might converge, but the bytes behind the URL can change. Determinism also requires pinned sources, integrity checks, explicit versions, and failure evidence.

Atlas separates:

```text
image build
    stable host contents

launch definition
    cloud placement and authority

bootstrap
    final environment binding

service reconciliation
    systemd owns process lifetime
```

## Instance identity and IMDSv2

An EC2 instance obtains workload credentials through an IAM role attached by an instance profile. The application does not store an access key. The metadata service returns short-lived credentials scoped to that role.

The launch definition requires IMDSv2 tokens and constrains metadata response hop behavior. This reduces several metadata-theft paths, but it does not make a broad role safe. A compromised process with legitimate metadata access still receives the role’s permissions.

The security argument is therefore two-part:

1. metadata access is deliberately constrained;
2. the role itself has only the authority Atlas needs.

The lab proves policy vectors independently of live AWS and records live metadata behavior only when an instance is available.

## Singleton, Auto Scaling group, or managed compute?

Course 2 deliberately retains a singleton Atlas host. This is not because a singleton is universally desirable; it keeps the transition from host engineering to cloud foundation observable.

### Singleton instance

Appropriate when:

- the course is proving machine replacement rather than horizontal availability;
- the workload is stateful and has not yet externalized coordination;
- cost and complexity must remain bounded;
- downtime during a controlled replacement is accepted and recorded.

Risks:

- one instance is one compute failure domain;
- replacement may interrupt service;
- drift accumulates if operators repair in place;
- accidental termination is consequential.

### Auto Scaling group with desired capacity one

Adds a controller that recreates an instance when desired capacity is unmet. This improves process around replacement but does not by itself make the application highly available. A single-AZ data volume can still prevent immediate placement elsewhere, and readiness may fail after the instance starts.

### Multiple instances

Requires the application to support concurrent instances, externalized state, routing, idempotency, coordinated upgrades, and capacity policy. Those concerns appear later in the program. Course 2 does not hide them behind `desired_capacity = 2`.

### Managed compute

A managed container or application service may reduce host ownership. That can be the right product decision, but it would skip the host-to-cloud handoff this course is designed to teach. The provider-comparison guide maps equivalent choices without presenting one as mandatory.

## Health is a chain of claims

A running instance proves only that the hypervisor and guest reached a provider-defined state. Atlas distinguishes:

```text
instance status
    provider can run and reach the guest

bootstrap complete
    expected image and data mount were reconciled

process alive
    systemd reports the unit active

application liveness
    process can answer a minimal self-check

application readiness
    API can accept work and worker/data dependencies are usable

load-balancer health
    target passes the edge's configured health request
```

These signals may disagree. A load balancer can remove an unhealthy target while the instance remains running. An Auto Scaling group can replace an instance for a health-check failure. A careless health path can create a replacement loop during a downstream outage.

Atlas uses a narrow edge health check and a richer operational readiness endpoint. The edge check asks whether routing traffic is useful; it does not require every optional dependency to be perfect.

## Replacement is a release, not a repair command

A replacement plan includes:

1. build and test a new image;
2. create a new launch-template version;
3. verify quota and temporary capacity;
4. create the replacement without modifying the old host;
5. attach or restore durable data under an explicit procedure;
6. wait for bootstrap and readiness evidence;
7. shift traffic;
8. observe a bake period;
9. decommission the old host;
10. retain the release and recovery record.

If the data volume cannot attach to the replacement location, the plan must say so before the old host is destroyed.

`create_before_destroy` is not a magic availability switch. It can fail because of:

- quota limits;
- unique names;
- fixed IPs;
- single-attachment volumes;
- subnet capacity;
- target-group behavior;
- certificate/domain conflicts;
- application state that cannot run twice.

The plan reviewer must recognize these constraints from the graph and architecture, not from lifecycle syntax alone.

## Architecture and instance types

The image architecture, instance architecture, binaries, agents, and package repositories must agree. Atlas records `amd64` or `arm64` explicitly rather than assuming every image runs everywhere.

Instance sizing is a hypothesis based on:

- observed CPU and memory from Course 1;
- network and storage requirements;
- burst behavior;
- expected replacement capacity;
- current quotas;
- cost.

Course 2 selects a small general-purpose instance for the optional AWS lane. It does not claim production capacity from a classroom workload.

## Patch strategy

A host foundation needs two clocks:

### Image-release clock

Regularly rebuild the image from current, pinned inputs. Test it. Replace machines through the release path.

### Emergency clock

A critical vulnerability may require a faster response. The runbook defines whether the organization:

- accelerates image rebuild and replacement;
- applies a temporary in-place patch with an expiry and follow-up replacement;
- removes the workload from service;
- accepts a documented risk for a bounded time.

“In-place patch forever” creates drift. “Never patch in place” can be too rigid during an active incident. The important property is explicit ownership, evidence, and convergence back to a known image.

## Image pipeline acceptance

The Course 2 image contract is intentionally stronger than an AMI ID. A
candidate image is accepted only when the build record identifies its base,
source, architecture, package inventory, tests, and builder. A launch plan then
proves that the intended version—not a mutable alias—will be used.

A future Course 3 OCI image will reuse this discipline. The artifact format
changes, but the supply-chain question remains: which exact bytes were built by
which process from which inputs, and which runtime assumptions do they carry?

## Replacement and data attachment race

With a single-attach data volume, a new instance cannot use the volume until the
old attachment is safely removed. Creating the new host before destroying the
old one is possible, but readiness must remain false until the attachment and
filesystem checks succeed. If traffic moves first, the release creates a clean
but stateless Atlas instance.

The runbook therefore treats compute creation, data attachment, mount
validation, application readiness, and target registration as separate steps.
This is a concrete example of why resource graph completion and service release
completion are different facts.

## Atlas capstone increment

Module 7 adds:

- an image contract and image-release record;
- an `aws_launch_template` with explicit metadata options;
- an instance profile from Module 6;
- a private-subnet Atlas host;
- a separate encrypted data volume;
- bounded cloud-init/user-data;
- architecture and quota preflight;
- bootstrap, readiness, and replacement evidence;
- a machine-replacement runbook;
- deliberately unsafe bootstrap and mutable-image fixtures.

## Completion standard

You may continue when you can take an arbitrary Atlas host failure and explain, without hand-waving:

- which image and launch version will replace it;
- which identity the replacement receives;
- where its durable data comes from;
- which health signals permit traffic;
- what temporary capacity is required;
- which evidence proves success;
- which remaining availability limits are intentional.
