# Containerfile review method

Review a Containerfile as a build-authority graph. Line-by-line style comments are useful only after the graph is understood.

## Pass 1 — Define outputs

List every final stage, target platform, executable, runtime dependency, configuration default, and artifact expected. A multi-stage file may have test, build, debug, migration, and production outputs with different authorities.

## Pass 2 — Trace inputs

For each instruction, record:

- source/context paths;
- base image digest;
- build arguments and environment;
- network access;
- secret/SSH/cache mounts;
- toolchain/package indexes;
- target platform;
- files copied from previous stages.

Anything capable of changing output is a build input even if it does not appear in source control.

## Pass 3 — Mark authority

Ask which instruction can:

- access private dependencies;
- execute untrusted source;
- write shared cache;
- contact the network;
- modify generated release content;
- influence metadata or runtime defaults.

Build and runtime authorities should be separated. The final stage should not inherit compilers, package managers, credentials, or debugging tools without a measured need.

## Pass 4 — Analyze cache

For every cacheable vertex, state the key and trust scope. Verify that architecture, toolchain, lockfiles, base digest, relevant context, and instruction parameters participate. Protected release builds must not consume untrusted cache entries merely because keys collide.

## Pass 5 — Review secrets

Secret values must not enter `ARG`, `ENV`, copied context, layer output, command history, logs, provenance parameters, or exported cache. Use ephemeral secret mounts and a canary-secret test that searches every retained object.

## Pass 6 — Review runtime contract

Compare final `USER`, `ENTRYPOINT`, `CMD`, `WORKDIR`, environment, exposed ports, healthcheck, signal, and filesystem paths with the predecessor contract. Remember that these are defaults; platform policy must enforce critical properties independently.

## Pass 7 — Inspect the output

Text review cannot prove the image graph. Build, then verify layers, history, config, entrypoint, platform binary, inventory, provenance, and runtime observation. Record exact digests.

## Review outcome

Classify findings as:

- **blocker** — identity, secret, platform, or runtime authority violation;
- **review-required** — evidence incomplete or policy judgment needed;
- **improvement** — maintainability/efficiency without current contract violation;
- **accepted with boundary** — mechanism passes under a clearly stated scope.

The reviewer’s deliverable is a reasoned decision, not a list of fashionable Dockerfile rules.
