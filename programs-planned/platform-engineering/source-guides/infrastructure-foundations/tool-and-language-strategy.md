# Tool and Language Strategy

The program uses the native expression of each responsibility:

- shell and Python for Linux automation and evidence;
- OpenTofu/HCL for cloud infrastructure state;
- Containerfiles and OCI metadata for packaging;
- Kubernetes YAML, Helm, and Kustomize for workload configuration;
- policy languages where policy is the subject;
- Go for one real Kubernetes controller;
- TypeScript where a developer portal or Backstage integration makes it appropriate.

Concepts precede products. A reference tool demonstrates the mechanism; it does not redefine the mechanism.
