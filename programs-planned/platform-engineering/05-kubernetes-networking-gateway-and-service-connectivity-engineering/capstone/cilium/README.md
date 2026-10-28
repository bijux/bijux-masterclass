# Optional Cilium implementation lane

The primary local implementation lane uses a disposable kind cluster without its default CNI or kube-proxy, then installs Cilium 1.20.0 with kube-proxy replacement, NetworkPolicy, Gateway API, and Hubble Relay enabled. Gateway API v1.6.1 CRDs must be installed before enabling the gateway resources.

This lane is optional because it requires privileged container networking. Passing it proves behavior only for the pinned local topology, not a managed-cloud network or production capacity profile.
