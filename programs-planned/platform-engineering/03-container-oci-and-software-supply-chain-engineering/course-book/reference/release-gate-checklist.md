# Release gate checklist

Apply gates in dependency order. A later success must never compensate for an earlier identity or correctness failure.

## 1. Candidate identity

- [ ] source/material revision is exact;
- [ ] image indexes/manifests are selected by digest;
- [ ] tags are discovery only;
- [ ] all required platform children are enumerated.

## 2. Object-graph integrity

- [ ] descriptor sizes and digests verify;
- [ ] media types are expected;
- [ ] config, layers, DiffIDs, and history are consistent;
- [ ] layer paths/whiteouts are safe;
- [ ] entrypoints exist in every platform rootfs.

## 3. Platform and runtime contract

- [ ] executable architecture matches descriptors;
- [ ] ABI/kernel/CPU assumptions are recorded;
- [ ] non-root identity and no-new-privileges policy pass;
- [ ] capabilities, mounts, writable paths, devices, and syscall/LSM profile are approved;
- [ ] shutdown and health semantics are demonstrated;
- [ ] resource values are labelled as measured or hypotheses.

## 4. Build and secret evidence

- [ ] build context and ignored paths are reviewed;
- [ ] base/toolchain inputs are immutable;
- [ ] cache scope is authorized and platform aware;
- [ ] secret canaries are absent from layers, configs, logs, provenance, and caches;
- [ ] controlled rebuild evidence has a stated boundary.

## 5. Inventory and risk

- [ ] SBOM covers every subject and required component class;
- [ ] vulnerability database/time and matching confidence are recorded;
- [ ] VEX statements are subject-bound and owned;
- [ ] license findings have disposition;
- [ ] missing/ambiguous evidence cannot silently pass.

## 6. Origin and authorization

- [ ] evidence signatures verify;
- [ ] signing identity and builder are authorized for this environment;
- [ ] provenance source, materials, parameters, and completeness satisfy policy;
- [ ] revocation/time conditions pass;
- [ ] evidence artifacts bind to current subjects.

## 7. Promotion and recovery

- [ ] destination registry graph verifies after copy;
- [ ] deployment uses digest;
- [ ] rollback subjects/evidence are retained;
- [ ] exceptions have scope, owner, compensating controls, and expiry;
- [ ] Course 4 handoff records exact image, runtime, storage, health, and supply-chain contracts;
- [ ] unexecuted native/production evidence is explicit.

The final output should be a structured decision: accepted, rejected, review-required, or not-executed for the intended environment. A score is not sufficient because several gates are non-compensable.
