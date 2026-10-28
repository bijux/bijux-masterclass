# Capstone repository layout

`repository/apps/atlas` contains Kustomize base and overlays. `repository/charts/atlas` contains the Helm chart and values schema. `repository/environments` records selected release identities. `argocd`, `flux`, `progressive`, and `secrets` contain controller-specific resources. `releases` contains categorical candidates and evidence.

The layout is a teaching reference, not a universal repository pattern. Its important property is that ownership and promotion identity remain explicit.

## Extended reader notes

`repository/apps/atlas/base` holds reusable workload intent. Environment overlays contain only justified differences such as namespace, replicas, logging, and data phase. `repository/data/protected` is a separate non-pruning inventory. `repository/charts/atlas` demonstrates a chart API rather than duplicating every Kustomize feature.

Controller resources live outside the application source because they govern delivery authority. Secret delivery, progressive delivery, fleet catalogue, policy, and release candidates have distinct directories so reviewers can identify the owner of each change. The layout is not prescribed as the only production topology; it is a visible model of authority and lifecycle separation.
