# Container, OCI, and Software Supply Chain Engineering

Course 3 of the Platform Engineering program turns the verified Atlas host and cloud workload contract into a portable, content-addressed, multi-platform workload release.

This is not a Docker command catalogue. It studies the boundaries that products often collapse into the word *container*:

1. Linux process isolation and resource authority;
2. OCI runtime bundles and lifecycle;
3. OCI image graphs, layers, and platform selection;
4. registry distribution and mutable references;
5. build inputs, cache, reproducibility, and secret hygiene;
6. SBOM, vulnerability, VEX, license, provenance, signature, and release-policy evidence.

The course book is the primary product: 100 navigated learner pages and ten complete chapters with matched exercises, worked answers, laboratories, and checkpoints. The capstone exists to expose and falsify the mechanisms described in the book.

The cumulative result is **Atlas Workload Release 1.0**: exact API and worker image-index digests for amd64/arm64, an approved runtime contract, subject-bound supply-chain evidence, one categorical release decision, and a manifested handoff to Kubernetes Course 4.

Begin at [`course-book/start-here.md`](course-book/start-here.md).

## Stable commands

```bash
make help
make doctor
make predecessor-proof
make core-proof
make capstone-tour
make manifest-proof
```

Optional independent builder, runtime, registry, and supply-chain lanes are listed by `make native-preflight`. They fail explicitly when unavailable; absence is never represented as successful evidence.
