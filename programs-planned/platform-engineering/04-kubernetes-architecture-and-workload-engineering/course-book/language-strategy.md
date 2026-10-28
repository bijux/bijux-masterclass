# Language and tool strategy

Platform engineering uses the language native to each control boundary. Forcing every concept into one general-purpose language would hide the APIs learners need to understand.

## YAML and JSON — desired-state documents

Kubernetes resources, CRDs, RBAC, and handoff contracts are expressed as YAML or JSON. The course treats them as API documents, not configuration snippets. Review focuses on type identity, field ownership, selectors, desired state, and evidence boundaries.

## Python — transparent semantic models and proof orchestration

Python implements the dependency-light control-plane model. It is selected because object transitions, conflicts, and tests remain readable without framework machinery. The Python model does not pretend to be Kubernetes; it exposes a bounded set of semantics so each invariant can be falsified deliberately.

## Go — Kubernetes-native controller implementation

Go implements `AtlasWorkload` reconciliation and an in-cluster API adapter. The controller uses standard-library HTTPS rather than a large framework so the learner can see authentication, resource paths, Server-Side Apply, status updates, and finalizers directly.

The program will use richer controller frameworks later when their abstractions solve demonstrated problems. Course 4 establishes what those frameworks must preserve.

## Shell and kubectl — experiment control

Shell scripts create disposable environments and capture evidence. `kubectl` is treated as an API client. A command is never the explanation: the learner must name the request it makes and the object/controller state it inspects.

## kind — independent local implementation lane

kind is optional and pinned. It provides a real Kubernetes control plane and worker Nodes for local observation. It does not transform a laptop experiment into production evidence.

## No artificial dual implementation

Unlike an API contract course, Course 4 does not reimplement every controller in Python and Go. Python carries deterministic semantic experiments. Go carries the controller core. Kubernetes YAML carries desired state. Parity applies to engineering invariants and handoff content, not file or class symmetry.
