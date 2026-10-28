# Cluster version and API lifecycle

Course 4 uses Kubernetes 1.36.2 as its conceptual baseline and kind's pinned 1.36.1 node image for the optional local lane. Always record client, server, and node versions independently.

Kubernetes APIs evolve through alpha, beta, and stable stages. Deprecated APIs can remain served temporarily before removal. Manifest validity is therefore tied to the target cluster's discovery document, not only local YAML parsing.

Control-plane and kubelet skew have bounded support policies. Managed services may control upgrade order and available feature gates. A manifest that works on kind may fail through managed admission policy or unavailable APIs.

Release evidence should include:

- target Kubernetes minor version;
- discovered API group/version/resource;
- feature gates relied upon;
- client and server versions;
- conversion/defaulting differences;
- upgrade and rollback compatibility.
