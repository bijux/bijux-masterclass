# Start Here — Platform Engineering

This program teaches platform engineering as the design and operation of **trusted capabilities**, not as a list of cloud products. The learner follows one Atlas platform from a single Linux host to a self-service application control plane.

Course 1 is the mandatory substrate course. It establishes the mental models needed to understand every later abstraction: process and file identity, resource control, filesystem durability, packet paths, name resolution, TLS, virtual machines, cloud identities, and failure domains.

## Study rule

For every mechanism, answer five questions:

1. Which desired state is being expressed?
2. Which component owns reconciliation or enforcement?
3. Which failure boundary exists?
4. What evidence distinguishes success from appearance?
5. Which claim remains unproven in the current environment?

## Evidence levels

- **Level A — dependency-light:** Python, shell, static configuration, deterministic fixtures.
- **Level B — Linux host:** real `/proc`, cgroup v2, sockets, systemd verification, filesystem behavior, and local TLS.
- **Level C — privileged/virtual:** network namespaces, nftables, mount experiments, virtual machines, and boot lifecycle.
- **Level D — real cloud:** provider IAM, metadata service, load balancer, persistent storage, DNS, zones, quotas, and billed resources.

A lower level can prove a mechanism but may not prove the stronger operational claim of a higher level.
