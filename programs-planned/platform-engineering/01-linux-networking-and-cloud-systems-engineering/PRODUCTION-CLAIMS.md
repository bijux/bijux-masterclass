# Production Claims and Evidence Boundary

Atlas Host Runtime is a **production-shaped reference workload**. It teaches mechanisms and operational reasoning used in production systems; the checked-in local package is not represented as an operated production service.

## What the release proves locally

The dependency-light and local-host routes can prove properties such as:

- configuration validation and directory separation;
- file-spool state transitions and atomic result publication;
- recovery reconciliation when a result was already published;
- signal-driven graceful worker termination;
- local certificate parsing, trust loading, SNI, and hostname verification;
- forwarding-header replacement at a trusted local edge;
- invalid HTTP authority rejection;
- systemd and Nginx configuration syntax where the native tools are present;
- provider-neutral cloud requirements and machine-readable Course 2 handoff integrity.

## What requires a privileged Linux VM

A privileged VM or equivalent disposable host is required to prove:

- network namespace creation and routing;
- nftables enforcement against real packets;
- mount, filesystem, and block-device experiments;
- systemd as the real service manager and cgroup owner;
- resource pressure, process replacement, boot, and machine lifecycle behavior;
- installation permissions and host-policy interactions.

## What requires a real cloud account

A real cloud environment is required to prove:

- provider IAM and workload-identity integration;
- metadata-service controls;
- managed DNS and load-balancer behavior;
- persistent block and object storage guarantees;
- region and zone failure assumptions;
- quotas, control-plane behavior, billing, and provider-specific recovery.

## Fixture warning

The private keys under `capstone/pki/` are public, deterministic course fixtures. They are intentionally unsuitable for deployment. Passing the local TLS tour proves the course mechanism; it does not prove secret custody, public trust, certificate renewal, internet exposure, or a cloud load balancer.

`FINAL-VERIFICATION.md` records the exact executed and unexecuted evidence for this release.
