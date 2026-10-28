# Misconception interventions

## “A container is a lightweight VM”

Ask which kernel the process uses and have the learner trace one syscall.

## “The image is secure because the scanner is green”

Launch the image with a runtime socket/host mount in a controlled model and enumerate effective authority.

## “We deleted the secret”

Extract lower layers and recover the synthetic token.

## “The digest proves we can trust it”

Create a malicious but internally consistent image and sign it with an unauthorized fixture key.

## “One test covers all architectures”

Swap child binaries while preserving labels and force an ELF check.

## “SBOM means we know what is vulnerable”

Present a schema-valid empty BOM and ask for completeness evidence.

## “Keyless signing means no key management”

Trace ephemeral key, certificate issuer, identity claims, transparency evidence, and verifier trust roots.

## “Kubernetes will enforce it later”

Require a precise Course 4 handoff. Orchestration cannot infer a missing shutdown or storage contract.
