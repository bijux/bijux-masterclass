# Orientation — from a verified OCI workload to Kubernetes

Course 3 ended with a verifiable workload release. The Atlas API and worker have immutable image identities, declared users, bounded writable paths, health contracts, shutdown expectations, supply-chain evidence, and explicit unexecuted claims. Course 4 begins by treating that package as an input contract, not a suggestion.

Kubernetes is allowed to choose placement, maintain replica populations, project configuration, restart containers, replace Pods, and expose observations through its API. It is not allowed to weaken the inherited image or runtime contract merely because a manifest field makes that convenient.

## The central shift

Before this course, the operating unit was a host or an OCI container. In Course 4, the operating unit becomes **declared state plus a collection of control loops**.

A learner who approaches Kubernetes as a YAML catalogue will miss the engineering model. The same YAML can be:

- admitted or rejected;
- stored but not reconciled;
- reconciled into children that cannot schedule;
- scheduled onto a Node that cannot start the image;
- running while unready;
- ready while unreachable through a later network data plane;
- deleted while blocked on a finalizer.

Each outcome has a different owner and different evidence.

## What is fixed at entry

The predecessor package fixes:

- `atlas-api` and `atlas-worker` repository-plus-digest identities;
- runtime UID and GID `65532:65532`;
- no additional Linux capabilities;
- no privilege escalation;
- a read-only image filesystem;
- `/tmp` and `/run/atlas` as ephemeral writable paths;
- `/var/lib/atlas/spool` and `/var/lib/atlas/results` as durable-path requirements;
- API port `8080`;
- liveness and readiness semantics;
- 30-second termination grace expectation;
- initial CPU and memory hypotheses that are not production sizing evidence.

Course 4 can translate these requirements into Pod templates and workload objects. It cannot silently change them.

## Two proof lanes

### Dependency-light semantic lane — mandatory

The Python API store and controllers make ownership, resource versions, generations, managed fields, finalizers, scheduling decisions, rollout arithmetic, and status updates visible and deterministic. The Go reconciliation core provides a second implementation of the custom-controller semantics.

This lane proves mechanisms and catches planted defects. It is not a substitute for an independent Kubernetes API server.

### Disposable kind lane — optional

The local-cluster lane uses kind to observe real API defaulting, controller timing, scheduling, Pod status, and events. It is intentionally separated from the production-intent release because the Course 3 images are not published pullable artifacts in this package, and `emptyDir` cannot satisfy the worker durability contract.

A kind result is local-cluster evidence, not managed-cluster or production evidence.

## Working discipline

For every lab:

1. identify desired state and its owner;
2. predict the next controller transition;
3. capture baseline objects and identities;
4. inject one bounded failure;
5. locate the earliest missing transition;
6. repair the owning input rather than deleting evidence;
7. prove convergence and cleanup;
8. record what remains unproven.

## Readiness diagnostic

Before Module 1, you should be able to explain:

- why an image digest is stronger deployment identity than a tag;
- why a writable container layer is not durable storage;
- why process liveness and service readiness are different;
- why a short-lived workload identity is preferable to embedding cloud credentials;
- why CPU/memory values inherited from Course 3 are hypotheses.

The orientation lab verifies the predecessor package, parses the manifests, compiles the controller core, and runs one semantic reconcile. The checkpoint requires an explicit statement of which Course 3 guarantees Kubernetes may preserve, operationalize, or defer—but not redefine.
