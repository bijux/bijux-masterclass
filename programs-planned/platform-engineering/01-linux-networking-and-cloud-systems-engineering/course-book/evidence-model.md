# Evidence Model

Platform claims fail when evidence answers a weaker question than the claim. A configuration file can prove what was written, not what was enforced. A process can be alive while readiness is false. A backup can exist while restoration fails. A local VM can demonstrate a mechanism but not a cloud provider's zone behavior.

## Evidence classes

### Class A — static and dependency-light

Examples: parsed JSON/YAML/TOML, Python syntax, shell syntax, unit dependency checks, pure state-machine tests, manifest verification, certificate field inspection.

Class A is fast and reproducible. It cannot prove kernel enforcement, privileged policy, real network paths, or provider behavior.

### Class B — local unprivileged runtime

Examples: real processes, signals, descriptors, loopback sockets, local filesystem transitions, TLS handshake and hostname verification, local subprocess cleanup.

Class B establishes actual operating-system and protocol behavior within the local environment. It does not prove systemd installation, cgroup delegation, firewall enforcement, VM boot, or cloud control planes.

### Class C — privileged disposable Linux or VM

Examples: installed systemd units, cgroup limits, namespaces, mounts, nftables, boot initialization, reboot and machine replacement drills.

Class C can support host-level operational claims when the environment is recorded. It still does not prove provider IAM, managed load balancer, disk, DNS, quota, or zone semantics.

### Class D — real cloud

Examples: workload identity, metadata restrictions, managed DNS, load balancer health and draining, persistent disk attachment, snapshot restore, quota behavior, zone replacement, and billing evidence.

A Class D result is scoped to the provider, account, region, resource types, configuration, time, and workload used.

### Class E — sustained operation

Examples: maintenance history, long-duration error rates, real capacity, security response, certificate renewal, recurring restore drills, and cost trends.

Course 1 cannot manufacture Class E evidence. It teaches the requirements and collection model.

## The experiment record

Every lab should produce:

```text
claim:
environment and evidence class:
baseline:
hypothesis:
controlled action:
first oracle:
raw evidence locations:
interpretation:
repair or conclusion:
cleanup proof:
residual risk:
stronger claim not established:
```

The **first oracle** matters because later symptoms are often downstream. A client timeout may follow a route failure, TLS mismatch, blocked accept loop, full disk, or dead worker. Preserve the first discriminating observation before changing the environment.

## Positive and negative evidence

A least-privilege claim requires both: the service can perform its declared work, and it cannot perform forbidden work. A TLS claim requires the correct name to verify and the wrong name or untrusted CA to fail. A resource boundary requires useful work within the envelope and bounded failure beyond it.

Negative tests must be safe. Do not attempt destructive access against a real production account to prove denial.

## Evidence freshness

Evidence expires when the relevant state changes: package update, image rebuild, certificate rotation, policy change, kernel upgrade, route modification, cloud migration, or changed workload. Record digests, versions, timestamps, and environment identity so stale evidence is detectable.

## Cleanup as evidence

A lab that leaves processes, mounts, firewall rules, keys, generated reports, or cloud resources changes the baseline for the next experiment. Cleanup is a correctness requirement. The release process extracts the archive into a clean directory, runs proof, removes generated output, and verifies exact manifests again.

## Honest skips

A missing Docker daemon, cloud account, privilege boundary, or provider CLI is not a pass and not necessarily a course failure. The proof route must report why the environment-backed check did not run and preserve the commands, expected oracle, and safety conditions for a suitable environment.
