# Standards and Reference Policy

This course uses standards to define portable semantics and reference implementations to demonstrate mechanisms. It never treats one tool's default as a universal rule.

## Claim categories

Every important statement belongs to one category:

1. **Normative standard** — a published specification such as POSIX or an IETF RFC.
2. **Linux mechanism** — kernel interfaces and behavior documented for the Linux implementation.
3. **Reference implementation behavior** — systemd, OpenSSL, Nginx, Debian, Ubuntu, or a cloud provider.
4. **Atlas contract** — a guarantee the capstone intentionally promises.
5. **Course profile** — a bounded choice made for safety, clarity, or reproducibility.

For example, TLS hostname verification is standards-based; the generated fixture certificate names are a course profile; OpenSSL command output is reference-tool evidence; requiring verified TLS for Atlas is an Atlas contract.

## Standards baseline

- **POSIX.1-2024 / Issue 8** supplies the portable process, file, shell, and system-interface vocabulary where applicable.
- **Linux kernel documentation** supplies `/proc`, namespaces, cgroup v2, pressure stall, capabilities, and other Linux-specific mechanisms.
- **systemd documentation** supplies unit, dependency, service, sandbox, and resource-control semantics for the reference service manager.
- **RFC 9110** supplies HTTP semantics independent of a particular HTTP transport version.
- **RFC 9325** supplies current recommendations for secure TLS and DTLS use; the course profile prefers TLS 1.3 for its local edge while explaining TLS 1.2 interoperability.
- **DNS RFCs** provide the resolver, authoritative data, caching, and negative-response model. The course uses a reserved testing name and local resolution controls.
- **NIST SP 800-145** provides a concise definition of cloud computing characteristics and service/deployment models. Provider product behavior remains provider-specific.

## Reference platform baseline

The primary lane is Debian 13 stable. Ubuntu 26.04 LTS is the comparison lane. Python 3.14 is the reference language release, while dependency-light proof supports Python 3.12 and newer. OpenSSL 3.5 LTS is the reference TLS toolkit. The course requires cgroup v2 for the full resource-control labs.

A learner may use another modern Linux distribution, but must record differences in:

- init and service-manager behavior;
- package and filesystem layout;
- firewall management;
- network configuration;
- security modules;
- kernel and cgroup support;
- OpenSSL and Python behavior.

## Version discipline

The course records a standards snapshot date in `tool-versions.json`. A later release may update versions after rerunning examples and proofs. The learner should not silently replace a pinned major version during a lab and compare results as though the environment were unchanged.

## Cloud documentation discipline

AWS, GCP, and Azure metadata, identity, load-balancing, disk, and failure-domain semantics change independently. Course 1 records provider mappings as questions and required behavior. Course 2 will select a primary execution lane and bind those requirements to exact provider documentation and live evidence.

## Reading a standard efficiently

Do not read every document linearly before beginning. Use the chapter to form a question, locate the normative or reference section that governs it, read definitions and requirements, then return to the experiment. Record whether the source defines legal behavior, recommends a secure profile, or documents one implementation.

## Course integrity rule

When a course profile intentionally narrows a standard, say so. When an example is a fixture, label it. When external validation was not executed, record `not-executed`. Precision about evidence is part of platform engineering, not release-note decoration.

## Primary references

- [The Open Group Base Specifications Issue 8 / POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/)
- [Linux kernel cgroup v2 documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- [Linux kernel networking documentation](https://docs.kernel.org/networking/index.html)
- [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) and [systemd.resource-control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)
- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 9325 — Recommendations for Secure Use of TLS and DTLS](https://www.rfc-editor.org/rfc/rfc9325)
- [NIST SP 800-145 — The NIST Definition of Cloud Computing](https://csrc.nist.gov/pubs/sp/800/145/final)
- [AWS Instance Metadata Service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)
- [Google Cloud VM metadata](https://cloud.google.com/compute/docs/metadata/overview)
- [Azure Instance Metadata Service](https://learn.microsoft.com/azure/virtual-machines/instance-metadata-service)

The chapters contain the complete teaching route. These sources are used to verify normative and provider-specific boundaries, not to outsource the explanation.
