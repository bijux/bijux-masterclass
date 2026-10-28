# Worked answers — Build graphs and secret hygiene

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. List the inputs that must be represented in a cache key for a cross-compiled Go build vertex.

Include source tree digest, module/lock files, compiler/toolchain digest, target OS, architecture and variant, build tags, compiler/linker flags, CGO setting, relevant environment, base/toolchain image digest, frontend/build definition, and any generated inputs. If a network dependency can change output, its immutable identity must also be represented or the network must be removed from the controlled vertex.

## 2. Why is excluding `.git/` from the context a security control, not merely a performance optimization?

The builder cannot read ordinary files outside the context. Excluding `.git/` prevents deleted secrets, remote URLs, reflog history, hooks, and unrelated metadata from becoming available to `COPY` or a compromised build step. It also stabilizes context hashing. This is a reduction of authority and input surface, not just fewer transferred bytes.

## 3. Compare `ARG TOKEN`, environment injection, and a transient secret mount.

`ARG` is build metadata and can appear in history, logs, provenance, and cache keys. Environment injection can leak through process listings, logs, child processes, and filesystem writes. A transient secret mount exposes a file only to one build step and excludes it from the committed snapshot by design. The command must still avoid copying or printing it, and the secret should be short-lived and narrowly scoped.

## 4. A pinned base digest is six months old. Explain why both “always use latest” and “leave it pinned forever” are weak policies.

Mutable latest tags prevent deterministic review and allow unreviewed change. Permanent pinning prevents automatic substitution but leaves known defects indefinitely. Separate discovery from promotion: detect new base digests, analyze changes and vulnerabilities, rebuild under control, run policy/tests, then update the reviewed digest.

## 5. A multi-stage build copies `/out/` recursively. What additional review is required?

Inspect the complete directory inventory, ownership, modes, symlinks, debug/source artifacts, secret residues, dynamically required libraries, and whether a compromised build step can add unexpected files under the copied path. Prefer exact file copies or generate a manifest that the final stage verifies.

## 6. Two builds produce the same final rootfs tree but different image digests. Give four possible causes.

Configuration JSON can differ; layer boundaries can differ; tar metadata/order can differ; gzip metadata/compression can differ; history or annotations can differ; platform labels can differ; timestamps can differ. Visible rootfs equivalence is only one dimension of image identity.

## 7. Explain why one repeated build on one host is weaker than independent reproducibility.

One host can reuse hidden state, caches, environment, compromised tooling, or filesystem metadata consistently across both runs. Independent rebuilders reduce shared hidden inputs. Stronger evidence uses separately provisioned environments, verified toolchains/materials, and a documented comparison of exact outputs.

## 8. A build is reproducible and signed but source review was bypassed. What does the evidence prove and not prove?

The signature can authenticate a signer over a digest. Reproducibility can show declared inputs lead to the same output under the tested envelope. Neither proves the source change was authorized, reviewed, benign, or policy-compliant. Release policy must evaluate source and builder trust separately.

## 9. Design an experiment that detects a secret written into a layer and then deleted.

Use a synthetic unique token, copy it in an early layer, use and delete it in a later layer, then verify the merged rootfs lacks it. Enumerate and unpack each layer independently and scan raw/uncompressed bytes for the token. The experiment proves final-view scanning alone misses historical disclosure.

## 10. Why can network-enabled package installation undermine a source-commit reconstruction claim?

The same command can receive different package indexes, archives, redirects, certificates, or mirror content over time. Unless every fetched object is digest-pinned and recorded, the source commit does not describe the full build input. Network unavailability also prevents reconstruction. Use immutable mirrors/locks or disable network after material preparation.

## 11. A cache hit makes a build faster after a compiler flag changes. What evidence distinguishes a correct hit from a false hit?

Record the normalized build vertex inputs and cache key before and after the flag change. A correct implementation changes the key and reruns compilation. Independently inspect the binary for the intended flag effect or compare output/provenance. Speed alone cannot establish cache correctness.

## 12. Write a narrow, honest reproducibility statement for Atlas Course 3.

“Using the checked source digest, Go toolchain and base digests, target platform, build parameters, normalized timestamps/ownership/archive order, and the course semantic builder on the tested Linux environment, two clean controlled builds produced identical API, worker, and probe OCI index digests. This does not establish independent native-tool or cross-environment reproducibility.”

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
