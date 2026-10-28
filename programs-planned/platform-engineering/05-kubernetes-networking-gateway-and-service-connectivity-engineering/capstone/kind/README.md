# Optional kind/CNI/Gateway lane

This lane is guarded because it changes cluster networking. Create only the dedicated `atlas-networking-lab` cluster. Install a NetworkPolicy-capable CNI whose Kubernetes 1.36 and dual-stack support is documented, Gateway API 1.6.1 Standard CRDs, and a conformant Gateway implementation. Record the exact conformance profile.

The repository does not silently download or install a network plugin.
