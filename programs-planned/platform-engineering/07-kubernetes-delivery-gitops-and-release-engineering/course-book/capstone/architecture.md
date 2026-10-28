# Capstone architecture

Atlas Delivery Plane sits between reviewed source/artifacts and the Kubernetes API. It includes a deterministic renderer, environment repository, promotion ledger, inventory-aware reconciler, health evaluator, progressive-delivery engine, fleet catalogue, release policy, and exact handoffs.

The mandatory semantic lane is intentionally independent of Argo CD and Flux so that tests can isolate invariants. Native manifests map the same model onto those controllers.

## Extended reader notes

The semantic core is organized around the release graph rather than around vendors. `canonical.py` and the renderer models establish desired-set identity. `inventory.py` and `reconcile.py` model owned convergence and protected prune. `health.py` keeps resource health bounded. `promotion.py` and `release.py` enforce artifact and evidence decisions. `progressive.py` handles pass, fail, inconclusive, and unavailable analysis. `fleet.py` keeps target generation and compatibility explicit.

Native manifests map this model into Kustomize, Helm, Argo CD, Flux, External Secrets, SOPS, Argo Rollouts, and Flagger. The Go probe independently checks canonical JSON and drift sets. None of these components owns Atlas business data. Course 6’s data authority remains external to the delivery controller.

The architecture deliberately includes two controller families but one release dossier. Learners can select a primary lane while comparing how each product represents source, inventory, health, prune, and automation.
