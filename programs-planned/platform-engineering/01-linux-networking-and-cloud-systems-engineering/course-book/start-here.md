# Start Here

This course assumes basic programming and command-line familiarity. It does not assume Linux administration, networking, virtualization, or cloud experience.

## The learning contract

You are not expected to memorize every flag. You are expected to build a causal model and know which evidence can confirm or reject it. For each mechanism, practice answering four questions:

1. **Who owns the state?** Kernel, service manager, process, filesystem, resolver, proxy, cloud control plane, or operator?
2. **Which transition changes it?** `exec`, signal delivery, rename, route lookup, handshake, certificate rotation, VM replacement?
3. **How can it fail?** Permission denial, resource exhaustion, stale cache, partial write, asymmetric path, expired trust, quota, or unavailable control plane?
4. **Which observation is decisive?** Process status, cgroup counter, mount identity, packet exchange, certificate path, cloud resource ID, or restore result?

## Safe study environment

The dependency-light path runs on Linux, macOS, or a Linux development container with Python and OpenSSL. The strongest host labs require a disposable Linux VM because they modify services, namespaces, mounts, routes, cgroups, or firewall policy.

Do not run privileged experiments on a shared workstation, employer-managed machine, production server, or network you do not own. Before a VM lab, establish:

- console access that does not depend on the route you will modify;
- a snapshot or reproducible replacement path;
- a cost and deletion boundary;
- an abort condition and cleanup owner;
- fixture credentials only.

The course uses `atlas.test`, a reserved testing name, and a checked local fixture CA. Never trust the fixture CA outside the course environment or reuse its private keys.

## First commands

From the course directory:

```bash
make help
make doctor
make core-proof
make capstone-tour
```

`make doctor` reports available evidence classes. It does not install tools or claim that an unavailable environment passed. `make core-proof` checks the course structure, links, data files, code, handoff, tests, and local PKI. `make capstone-tour` starts the API, worker, and HTTPS edge on loopback, submits a job, verifies the result, and cleans every process.

On a Linux system with systemd tooling:

```bash
make systemd-proof
```

On a disposable privileged Linux VM, use only the guarded targets described by the relevant lab. They require an explicit environment variable before changing namespaces or resource controls.

## How to read a module

Read the main chapter without copying commands yet. Draw the ownership and failure model. Complete the twelve exercises from memory. Compare your reasoning with the worked answers, then run the lab. The lab is successful only when you can explain:

- the baseline;
- the hypothesis;
- the controlled change;
- the first failed or successful oracle;
- the repair or conclusion;
- the cleanup result;
- the evidence class.

A command that returns zero is not necessarily the oracle. For example, `openssl s_client` can complete a connection while hostname verification was never requested. `systemd-analyze verify` can validate syntax while the unit is not installed or enforced. A backup command can succeed while restoration is impossible.

## Primary and comparison lanes

The primary operating-system lane is Debian 13. Ubuntu 26.04 LTS is the comparison lane. The course teaches POSIX and Linux mechanisms first and calls out distribution-specific service, package, network, and security behavior where it matters.

Python is the readable automation and capstone language. Shell is used for process composition and direct system interrogation. Configuration languages—systemd units, nftables, Nginx, cloud-init, JSON, and YAML—are treated as executable policy and tested accordingly.

## Before Module 01

Complete orientation. You should be able to identify your kernel, architecture, cgroup mode, init system, network namespace, effective identity, Python/OpenSSL versions, and whether the current environment is safe for privileged labs. You should also be able to run and stop the local Atlas tour without leaving processes or generated state behind.
