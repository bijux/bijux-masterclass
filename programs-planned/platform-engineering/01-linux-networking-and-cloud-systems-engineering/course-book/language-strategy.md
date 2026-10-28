# Language and Tool Strategy

Platform engineering is expressed through several native languages. Forcing every mechanism into one general-purpose language would hide the system rather than teach it.

## Shell

Shell composes processes and exposes direct system interfaces. Use it for bounded inspection, pipelines, service commands, and disposable lab setup. Course shell scripts begin with strict error handling, quote expansions, guard privileged actions, and define cleanup traps where they create state.

Shell is not used for complex durable data structures or large application logic.

## Python

Python implements the readable Atlas semantic core and proof automation. It is used for:

- atomic file publication;
- queue transitions;
- process and health evidence;
- HTTPS client/server fixtures;
- metadata and cloud requirement validation;
- tests, reports, and manifests.

The implementation favors standard-library mechanisms so the dependency-light path remains inspectable. The standard-library HTTP server is explicitly a teaching edge, not a universal production server.

## Configuration languages

systemd units, sysusers, tmpfiles, nftables, Nginx, cloud-init, JSON, YAML, and TOML are executable policy. They receive syntax checks, semantic review, negative tests where possible, and version ownership. Copying a configuration from a blog without understanding its authority and failure behavior is not accepted evidence.

## Why no containers or Kubernetes yet

Containers combine namespaces, cgroups, filesystems, networks, and image metadata. Kubernetes adds an API server, scheduling, controllers, service discovery, and reconciliation. Learning those first would encourage memorized manifests without a substrate model. Courses 3 and 4 introduce them after Course 1 and Course 2 establish the machine and cloud foundation.

## Primary and comparison lanes

Debian 13 is the primary Linux lane. Ubuntu 26.04 LTS is the comparison lane. AWS becomes the primary cloud implementation lane in Course 2, with GCP as a comparison lane and Azure as a mapping lane. Course 1 remains provider-neutral where provider resources are not yet being created.

## Code-reading expectation

You do not need to become an advanced Python developer. You must be able to trace ownership, state transition, error propagation, cleanup, and evidence. When the capstone is intentionally simplified, the chapter states the limit and identifies the maintained production component that would normally own the responsibility.

## Learning how to translate mechanisms

Later courses introduce HCL, Containerfiles, Kubernetes resources, Helm, Kustomize, policy languages, Go controllers, and TypeScript portal integrations. The transferable skill is not syntax recall. For each representation, identify desired state, authoritative owner, reconciliation or execution mechanism, rollback, and evidence. A systemd unit, OpenTofu resource, Kubernetes Deployment, and Crossplane composition all express desired behavior, but their control loops, failure scopes, and state ownership differ.

The course therefore asks you to explain a mechanism in plain language before editing its native configuration. Use code and configuration excerpts that can be executed or parsed. Label pseudocode explicitly. Prefer one complete example over several fragments that omit error handling or cleanup.

The result is a polyglot program with one coherent engineering vocabulary: owner, desired state, observed state, transition, failure boundary, oracle, rollback, and evidence. Those concepts remain stable while tools change.
