# Language and Tool Strategy

The course uses each language for the responsibility it expresses best.

| Responsibility | Primary form |
|---|---|
| Cloud desired state | OpenTofu HCL |
| Provider interaction | AWS provider and AWS CLI |
| Deterministic models and proofs | Python |
| Small operational wrappers | POSIX shell |
| Policy fixtures | JSON/YAML plus Python evaluator |
| Architecture decisions | Markdown and machine-readable profiles |

## OpenTofu, not vendor-neutral fiction

OpenTofu is the primary IaC engine. The course teaches its graph, state, modules, lifecycle, imports, refactors, tests, and encryption model. The architectural lessons transfer to other declarative IaC systems, but syntax and state behavior are not assumed identical.

## AWS primary lane

AWS is the deep provider lane. Google Cloud and Azure are comparison lanes. A learner should finish the course able to map the requirements to another provider, but not by mechanically replacing resource names.

## Provisioners

Remote-exec and local-exec provisioners are not the normal workload-delivery mechanism. They are difficult to model, retry, and audit. Course 2 uses machine images and cloud-init for a bounded host bootstrap. Course 3 replaces mutable workload payload installation with OCI artifacts.

## Python model

The Python `cloud_model` is an executable explanation of resource graphs, state locks, plan classification, drift, and release gates. It is not advertised as an OpenTofu reimplementation.
