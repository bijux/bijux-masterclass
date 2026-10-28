# Checkpoint — OCI image graph

## Required evidence

- deterministic Atlas Probe OCI layout;
- complete descriptor graph;
- layer digest versus DiffID proof;
- whiteout and opaque-directory results;
- corrupted-blob rejection;
- subject-bound artifact example.

## Decision defense

Defend the exact image/index digest chosen as the release subject. Explain why neither a tag nor a platform-specific manifest alone is sufficient for the intended multi-platform release.

## Progression gate

Proceed when you can reproduce the graph from controlled bytes. Module 4 will examine how build systems choose and transform those bytes—and why reproducible image structure does not by itself prove a trustworthy build.

## Continue

- [Next stage](../module-04-build-graphs-cache-reproducibility-and-secret-hygiene/index.md)
- [Course index](../index.md)
