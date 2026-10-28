# Checkpoint — Compute and Replacement

## Required evidence

- [ ] image release identified by source, architecture, inputs, digest, and tests;
- [ ] launch template uses an explicit reviewed version;
- [ ] user data contains no secret or mutable `latest` download;
- [ ] instance metadata requires IMDSv2;
- [ ] instance role has a bounded permission set;
- [ ] root and durable data lifecycles are distinct;
- [ ] bootstrap completion and readiness are separate signals;
- [ ] quota and temporary replacement capacity are evaluated;
- [ ] result integrity survives simulated or real replacement;
- [ ] remaining singleton and zone-failure exposure is stated precisely.

## Decision defense

Explain why the selected image, bootstrap boundary, instance shape, identity, data attachment, and replacement sequence belong together. Identify the exact point at which a replacement can block, what evidence detects it, and which recovery path preserves acknowledged Atlas work.

## Progression gate

Progression requires the evidence bundle and a written replacement argument. A screenshot of a running instance or a successful instance-status check is insufficient.
