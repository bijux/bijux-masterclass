# Tool and language strategy

The subject is delivery engineering, not framework programming.

| Form | Responsibility in this course |
|---|---|
| Kubernetes YAML | desired resources and controller APIs |
| Git | immutable revision history, review, candidate proposals, and reverts |
| Kustomize | template-free base and overlay composition |
| Helm | versioned chart input, packaging, and upgrade API |
| Argo CD | primary application-oriented GitOps lane |
| Flux | comparative controller-composition and image-automation lane |
| SOPS / External Secrets | contrasting secret custody and delivery models |
| Argo Rollouts / Flagger | progressive exposure implementations |
| Python | transparent semantic model, proof runners, and release policy |
| Go | independent digest and drift probe |
| Shell | bounded tool composition; never the release source of truth |

The course follows `concept → API/model → mechanism → failure → evidence → implementation`. Product commands appear only after the learner can name the state and owner. Select one primary controller for the full native lane and use the other to test portability of your reasoning.

The Python and Go implementations are intentionally smaller than native products. They make difficult invariants inspectable and testable. When a native feature lies outside the bounded model, record the difference and use native evidence rather than pretending the model is complete.
