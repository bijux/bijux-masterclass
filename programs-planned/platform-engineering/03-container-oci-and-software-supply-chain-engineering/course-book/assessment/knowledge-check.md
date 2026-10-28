# Knowledge check

Complete this closed-book before the practical assessment. Answers should identify an object, mechanism, failure mode, and evidence—not merely a command.

1. Draw the OCI graph from image index to layer blobs and explain which digest names compressed versus uncompressed bytes.
2. Explain why a non-root image can still run with host-root-equivalent authority.
3. Demonstrate, conceptually, how a deleted secret remains recoverable from image history.
4. Explain what a tag can do that a digest cannot, and why that makes it unsuitable for deployment authorization.
5. Distinguish image configuration defaults from an OCI runtime bundle’s effective process configuration.
6. Explain why an `arm64` platform descriptor is not proof that the entrypoint is an arm64-compatible executable.
7. State the minimum evidence required before claiming a controlled build was reproducible.
8. Distinguish SBOM completeness, vulnerability matching, exploitability, VEX, and release authorization.
9. Explain why a cryptographically valid signature from an unauthorized builder must fail promotion.
10. Describe how a registry referrer is discovered and then independently verified.
11. Explain why a read-only root filesystem requires an explicit write-path design.
12. State what Course 4 may consume from the workload handoff and what it may not silently change.

## Passing standard

At least ten answers must be technically correct, and all six non-compensable distinctions must be correct: image/container, tag/digest, integrity/trust, descriptor/platform truth, signature/authorization, and inventory/affectability. A mistaken answer on one of those six requires remediation even if the numeric score passes.
