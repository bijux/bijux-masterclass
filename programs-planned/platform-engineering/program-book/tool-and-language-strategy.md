# Tool and language strategy

Platform engineering uses the native expression of each responsibility. Shell and Python remain the transparent proof and automation lane. HCL expresses infrastructure desired state. OCI files and Go support workload construction. Kubernetes YAML expresses resource APIs. Course 7 adds Git, Kustomize, Helm templates, Argo CD and Flux custom resources, SOPS and External Secrets profiles, and Argo Rollouts/Flagger resources.

Python implements a readable delivery model: canonical rendering, inventory, field ownership, protected prune, health, promotion, progressive analysis, fleet compatibility, and categorical release. Go provides an independent canonical digest and drift probe. These models teach invariants and produce deterministic tests; they are not substitutes for native controller execution.

Select one primary GitOps lane—Argo CD or Flux—for full native work. Use the second as a comparative architecture. Do not duplicate every command. Translate source, inventory, field authority, health, prune, automation, and recovery into the common Atlas model.
