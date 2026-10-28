# Laboratory — Make the build graph confess its inputs

## Goal

Produce a controlled Atlas build and show which input changes should and should not invalidate each graph vertex.

## Safety boundary

Use synthetic credentials only. Do not place real tokens anywhere in the repository, context, shell history, or logs. Disable public pushes.

## Baseline

Build API amd64 twice from a clean controlled workspace and record source digest, base/toolchain digest, graph inputs, cache events, and final image digest.

## Hypothesis

A source-only change invalidates application compilation but not dependency preparation. A target-architecture change invalidates compilation. A synthetic secret-value change does not alter exported bytes when used through a proper secret mount.

## Controlled action

Run five experiments:

1. edit only application source;
2. edit `go.mod`;
3. switch target architecture;
4. supply a different synthetic secret through the secret channel;
5. add the synthetic secret to an early layer and delete it later.

## Oracle

Cache invalidation follows actual dependencies. The secure secret change leaves no layer/evidence leak and does not affect bytes unless the build legitimately consumes it into output. The unsafe build is rejected because the token remains in history.

## Evidence

Submit graph diagrams, cache-key/input tables, exact output digests, secret scans, and one paragraph explaining every unexpected invalidation or hit.

## Interpretation

Separate build speed, byte reproducibility, and supply-chain trust. A result can succeed in one dimension and fail another.

## Cleanup

Delete synthetic tokens, temporary caches, and unsafe layouts. Verify the token pattern is absent from the course tree.

## Completion gate

You can predict and then explain cache behavior for all five experiments, and the accepted build has a complete input record suitable for provenance.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
