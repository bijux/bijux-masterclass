# Linux, Networking, and Cloud Systems Engineering

> **Course 1 of 10 — Platform Engineering**

> **Governing question:** What actually happens beneath containers, Kubernetes, and cloud abstractions, and how can an operator prove it?

Platform abstractions are useful because they hide detail. They are dangerous when the hidden detail becomes a failure boundary that no one on the team can explain. A Pod is still scheduled onto a machine. A Service still depends on routes, sockets, DNS, and connection state. A persistent volume still rests on a storage system with a particular durability and attachment model. A workload identity still reaches an issuer and receives bounded authority.

This course builds the substrate knowledge required to reason about those later systems. It does not begin with Kubernetes YAML. It follows one small but production-shaped workload—**Atlas Host Runtime 1.0**—through processes, identities, resource controls, filesystems, sockets, DNS, TLS, proxies, virtual machines, and cloud primitives.

## What you will be able to do

By the final defense, you will be able to:

- trace a service from executable image to process, system calls, descriptors, signals, and exit evidence;
- assign dedicated identities, permissions, capabilities, service-manager ownership, and restart policy;
- interpret CPU, memory, task, I/O, cgroup, and pressure evidence before setting limits;
- distinguish visible, atomic, synchronized, backed-up, and actually restored data;
- diagnose a network path from listener through route, transport, DNS, TLS, HTTP, firewall, and proxy;
- explain VM image, boot, metadata, maintenance, replacement, and failure-domain behavior;
- translate host guarantees into provider-neutral cloud requirements without pretending provider products are identical;
- run a bounded game day and produce a precise handoff for Infrastructure as Code and Cloud Foundation Engineering.

## The cumulative system

Atlas contains three long-running responsibilities:

```text
verified HTTPS client
        |
        v
Atlas edge
        |
        v
Atlas API ---- durable file spool ---- Atlas worker
        |                                  |
        +----------- result state <--------+
```

The implementation is deliberately small enough to inspect. The engineering boundaries are not simplified away. The edge owns TLS and trusted forwarding headers. The API owns request validation and job acceptance. The worker owns one claimed job at a time. The filesystem spool makes process, durability, ownership, and recovery mechanics visible before later courses replace parts of the design with cloud and orchestration services.

## How the course teaches

Each numbered module has five pages:

- `index.md` is the complete chapter and primary learning product;
- `exercises.md` contains twelve transfer problems;
- `exercise-answers.md` demonstrates reasoning, not merely final phrases;
- `lab.md` runs one controlled experiment with a predicted failure and decisive oracle;
- `checkpoint.md` defines the evidence required before progression.

The lab is not a command transcription exercise. Before changing the system, write a hypothesis and name the first observation that would falsify it. Preserve raw evidence, interpret it, clean the environment, and distinguish what was executed from what remains environment-backed.

## Evidence classes

The course uses five evidence classes:

| Class | Environment | What it can establish |
|---|---|---|
| A | static and dependency-light | syntax, structure, pure logic, configuration relationships |
| B | local unprivileged Linux | processes, files, loopback sockets, signals, local TLS, file durability mechanisms |
| C | privileged disposable Linux/VM | namespaces, cgroups, mounts, firewall, boot, systemd installation, replacement drills |
| D | real cloud account | provider IAM, metadata, DNS, load balancing, disks, quotas, zones, and cost behavior |
| E | sustained operated environment | long-duration reliability, capacity, maintenance, security, and recovery claims |

A Class B result must never be described as Class D evidence. The course's proof reports record passes, skips, and unavailable environments separately.

## What this course does not cover

Containers, OCI images, Kubernetes, GitOps, policy controllers, and internal developer platforms belong to later courses. Course 1 may mention them to explain why a substrate concept matters, but it does not ask you to memorize abstractions before understanding their mechanisms.

The bundled Python edge and file spool are instructional mechanisms, not claims that Python's standard-library HTTP server or a local directory queue should replace maintained production components. Their small size makes process, I/O, TLS, retry, and recovery behavior inspectable.

## Reading route

Start with [Start Here](start-here.md), then follow the [Study Plan](study-plan.md). Read the [Capstone](capstone.md) and [Evidence Model](evidence-model.md) before Module 01. Use [Standards](standards.md) to distinguish normative behavior from course policy and reference-tool behavior. The [Glossary](glossary.md) is written for retrieval during study, not as a substitute for the chapters.

The course is complete when you can defend the Atlas host, recover it from controlled failure, and explain every requirement exported to Course 2.
