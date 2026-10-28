# Debugging container releases

Debug from the earliest broken identity edge. Starting with “the container failed” is too vague because source, image graph, distribution, selection, runtime, application, and evidence can each fail independently.

## Phase 1 — Candidate identity

Record the exact repository, tag used for discovery, resolved index/manifest digest, source revision/digest, and release record. Compare review, promotion, registry, deployment, and runtime identities. If they differ, stop. Later application debugging cannot repair deploying unreviewed bytes.

## Phase 2 — Object graph

Traverse index → platform manifest → config/layers. Verify size/digest/media type at every edge. Recompute DiffIDs, inspect history, and reconstruct the rootfs with safe whiteout handling. Typical failures:

- missing blob;
- wrong media type;
- config/layer count mismatch;
- unsafe archive path;
- entrypoint absent after merge;
- secret hidden but preserved in history.

## Phase 3 — Platform selection

Inspect selected platform descriptor and executable machine/ABI. Record whether evidence was native, emulated, cross-compiled, or absent. `exec format error` often points here, but dynamic-loader and CPU-feature failures can look different.

## Phase 4 — Registry and transport

Compare digest before push, after pull, and at runtime. Inspect content negotiation, authorization, mirror/proxy behavior, referrer discovery, and retention. A tag returning an unexpected digest is an identity failure, not a transient application outage.

## Phase 5 — Effective runtime request

Merge image defaults with runtime/orchestrator/operator overrides. Inspect:

- UID/GID/groups/capabilities/no-new-privileges;
- namespace IDs;
- mounts and propagation;
- writable paths and devices;
- seccomp/LSM profile;
- cgroup limits/events;
- PID 1 and signal behavior;
- environment/config/secret inputs.

“Works with privileged mode” is not diagnosis. It only proves some missing authority was included in an enormous override. Add one permission at a time and identify the actual requirement.

## Phase 6 — Application contract

Only after identity and runtime are correct, inspect listening address, port, certificates, DNS, storage permissions, configuration, health semantics, shutdown, and dependency access. Compare with the Course 2 handoff rather than inventing new paths or identities.

## Phase 7 — Supply-chain evidence

For rejected promotion, read the first non-compensable gate. Verify subject binding before signature validity, builder identity, SBOM completeness, vulnerability/VEX disposition, and evidence freshness. Do not “fix” policy by weakening it until a candidate passes.

## Diagnostic record

For each investigation, preserve:

```text
symptom and timestamp
exact candidate/runtime digest
expected contract
first divergent phase
evidence and command/tool version
controlled change
observed result
cleanup/recovery
remaining uncertainty
```

The goal is not a larger command collection. It is a causal argument that another engineer can rerun.
