# Orientation — Establish the Laboratory and Evidence Boundary

Orientation prepares a safe, classified environment before the course asks you to reason about it. It does not require root access or a cloud account.

## Objectives

By the end, you can:

- identify operating system, kernel, architecture, init system, effective identity, network namespace, and cgroup mode;
- distinguish the dependency-light host from an optional privileged VM and real cloud environment;
- run the complete local Atlas HTTPS tour and clean it;
- explain which later claims the current environment cannot establish;
- create an evidence directory and experiment log without storing secrets;
- choose a safe disposable-VM route for privileged modules.

## Environment classification

Run:

```bash
make doctor
```

The doctor reports facts, not grades: Python/OpenSSL versions, Linux status, cgroup v2, systemd analysis tooling, namespace/firewall commands, virtualization hints, and cloud environment variables. A missing tool does not become a synthetic pass.

Use these labels:

```text
A — static/dependency-light
B — local unprivileged runtime
C — privileged disposable Linux or VM
D — real cloud account
E — sustained operated environment
```

Most learners can complete Classes A and B immediately. Plan Class C with a local VM or short-lived cloud instance. Class D is optional in Course 1 and becomes important in Course 2. Class E is never manufactured by a course fixture.

## The first Atlas run

`make capstone-tour` creates a temporary runtime, starts the API and worker, starts the HTTPS edge with the checked fixture certificate, waits for readiness, submits a job, reads the durable result, tests the trusted proxy boundary, terminates the worker gracefully, stops all processes, and writes a report.

Inspect the report and events. Identify:

- three process identities and their PIDs;
- the listening ports chosen dynamically;
- the CA used by the client;
- the transition from queued to processing to result;
- the readiness checks;
- the evidence that all child processes stopped.

The tour is a real Class B mechanism proof. It does not prove systemd enforcement, firewall policy, cloud load balancing, or machine replacement.

## Safety plan for privileged labs

Prepare one of:

- a local VM with console access and snapshot;
- a disposable cloud VM with a budget, deletion command, and no production trust;
- a dedicated Linux lab host you can replace.

Record how you recover if a firewall rule blocks SSH, a mount hides files, a cgroup kills the shell, or a boot unit prevents readiness. Never learn firewall recovery for the first time on a remote-only host.

## Evidence workspace

Create a private study directory outside the course tree. Store transcripts, diagrams, packet captures, cloud inventory, and screenshots there. The course manifest should remain clean. Redact public IPs, account identifiers, certificate private keys, and tokens before sharing evidence.

## Orientation exit condition

You may begin Module 01 when the local tour passes, cleanup is verified, the evidence class is recorded, and you can state exactly which optional environments are available for Modules 2–10.

## Module route

- [Run the orientation lab](lab.md).
- [Complete the orientation checkpoint](checkpoint.md).
