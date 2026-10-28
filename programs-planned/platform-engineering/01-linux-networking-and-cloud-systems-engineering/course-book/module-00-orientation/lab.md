# Orientation Lab — Classify the Host and Run Atlas

## Goal

Establish a safe baseline and prove that the dependency-light Atlas workload can run and clean itself in the current environment.

## Safety boundary

Do not use root. Do not modify routes, firewall, mounts, users, system services, DNS, or cloud resources. The tour uses loopback, temporary directories, fixture keys, and ephemeral ports.

## Baseline

Record:

```bash
uname -a
id
python3 --version
openssl version
ps -p 1 -o pid,comm,args
mount | head
ip -br address 2>/dev/null || true
cat /proc/self/cgroup 2>/dev/null || true
```

Run `make doctor` and save the output outside the course tree.

## Hypothesis

The current environment can establish Class A and Class B evidence for local processes, files, signals, loopback networking, and verified TLS, while privileged and cloud evidence remains unexecuted.

## Controlled action

Run:

```bash
make core-proof
make capstone-tour
```

Inspect `capstone/reports/tour.json`, then run `make clean`. Confirm no Atlas process remains and no generated runtime directory exists.

## Oracle

- core proof passes;
- the tour reports HTTPS readiness, accepted submission, correct deterministic result, trusted-edge behavior, and clean worker termination;
- the fixture CA verifies the leaf name and IP SAN;
- every child process exits;
- cleanup removes generated reports and runtime state;
- unavailable privileged/cloud routes remain labelled unavailable.

## Evidence

Preserve doctor output, command transcript, tour report, process check after cleanup, and your evidence-class classification.

## Cleanup

```bash
make clean
pgrep -af 'atlas_host|atlas-api|atlas-worker|atlas-edge' || true
```

If a course process remains, terminate it and explain why cleanup failed before progressing.

## Completion gate

Explain which exact claims were established and name three claims the local tour cannot establish. Provide a safe plan for the disposable VM used later.
