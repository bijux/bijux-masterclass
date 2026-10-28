# Laboratory safety and cleanup discipline

Container laboratories can alter namespaces, mounts, cgroups, network interfaces, registry data, credentials, and process state. A useful experiment has a bounded blast radius and a cleanup oracle. “It ran on my laptop” is not a safety plan.

## Use disposable roots

Run semantic builders, unpackers, registries, and runtime bundles under a fresh temporary directory. Never point a course unpacker or cleanup command at `/`, your home directory, a shared registry repository, or a production container store.

Before destructive steps, print and verify the resolved path:

```bash
root="$(realpath -- "$candidate")"
case "$root" in
  /tmp/atlas-course3-* ) ;;
  * ) echo "unsafe root: $root" >&2; exit 2 ;;
esac
```

A path guard is not sufficient for production, but it prevents common laboratory mistakes.

## Separate privilege lanes

### Dependency-light lane

Runs without administrative authority and should be the default.

### User-namespace lane

Uses `unshare` and mapped identities. Verify host support and ensure no unexpected privilege escalation. Networking may use a private namespace without external connectivity.

### Privileged/native runtime lane

May create mounts, cgroups, veth pairs, firewall rules, or low-level runtime state. Use a disposable VM when possible. Record every created resource and require explicit opt-in such as `ALLOW_PRIVILEGED_LAB=1`.

Never ask a learner to paste a broad `sudo` command before explaining the exact privileged operation.

## Protect credentials and registries

Use fixture credentials and local repositories. Do not log real registry tokens, cloud credentials, OIDC tokens, signing keys, or secret mounts. Configure shell tracing off around sensitive commands. Verify command history and captured evidence before publishing it.

Course signing keys are intentionally public fixtures. Never repurpose them.

## Bound decompression and extraction

Layer archives can consume disk, memory, and inodes or escape the target root through paths and links. Use:

- maximum compressed/uncompressed sizes;
- entry-count and path-length limits;
- extraction confinement;
- no device creation;
- explicit ownership/mode policy;
- a disposable filesystem with quota where possible.

The lab’s malicious archives should contain only controlled harmless payloads.

## Bound runtime resource experiments

For memory, PID, CPU, descriptor, and disk-pressure labs:

- set limits on a child cgroup/namespace, not the host root;
- preserve a separate control session;
- keep a watchdog and timeout;
- know how to kill the process tree;
- avoid exhausting host-wide PIDs, disk, or memory;
- record recovery before repeating.

A valid experiment should fail the workload, not the learner’s machine.

## Network isolation

Bind instructional registries to loopback. If testing network namespaces or veth pairs, use unique names and a dedicated address range. Do not modify the default route or host firewall globally. Record current routes/rules first and remove only resources the lab created.

Never direct SSRF, scanning, or denial-of-service experiments at networks you do not own or have explicit permission to test.

## Signing and trust experiments

Keep fixture private keys under the course tree with clear labels and restrictive modes. Test compromise by changing policy or using a second fixture key—not by exposing a real key. Transparency and keyless examples should use dedicated test identities and repositories.

## Cleanup oracle

A cleanup section must prove absence, not merely run delete commands. Check:

```text
no course processes remain
no mounts remain under the temporary root
no temporary namespaces/cgroups/interfaces remain
no listening ports remain
no registry server remains
no secret fixture escaped the controlled tree
no generated evidence is mistaken for checked source
```

If cleanup fails, stop and diagnose before the next lab.

## Evidence sanitation

Before sharing reports:

- redact credentials structurally rather than by substring alone;
- preserve digests and object identities;
- remove host usernames/home paths when unnecessary;
- distinguish fixture domains and keys;
- retain raw evidence privately if needed for verification;
- never replace unexecuted evidence with invented output.

Safety and evidence honesty are part of the engineering outcome, not administrative extras.
