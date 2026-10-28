# Start here

The quickest way to waste this course is to memorize object examples without learning who owns each transition. A Deployment does not “run containers.” It declares a replica and rollout relationship. A Deployment controller creates ReplicaSets. ReplicaSets maintain selected Pod populations. The scheduler assigns unscheduled Pods to Nodes. Kubelets translate bound Pod specifications into local runtime actions. Applications report health. Networking components later turn endpoint eligibility into packet delivery.

The working model is:

```text
Course 3 image and runtime contract
        ↓
client submits desired workload state
        ↓
API server authenticates, authorizes, admits, defaults, validates, persists
        ↓
controller compares desired and current state
        ↓
controller creates or updates dependent objects
        ↓
scheduler finds a feasible Node
        ↓
kubelet and runtime realize the Pod
        ↓
application health produces readiness/liveness evidence
        ↓
other controllers and data planes consume those observations
```

Every arrow can fail independently. “Kubernetes is broken” is therefore not a diagnosis.

## Verify the entry contract

Run:

```bash
make predecessor-proof
```

Then inspect `capstone/predecessor/`. The package records the exact Course 3 handoff. At minimum, verify:

- API and worker images are identified by repository plus SHA-256 digest;
- both run as UID/GID `65532:65532`;
- no additional capabilities or privilege escalation are allowed;
- the image filesystem is read-only;
- `/tmp` and `/run/atlas` are ephemeral writable locations;
- `/var/lib/atlas/spool` and `/var/lib/atlas/results` require durable storage;
- the API uses port `8080`, `/live`, and `/ready`;
- shutdown has a 30-second grace expectation;
- secrets are runtime inputs, not image or annotation content;
- CPU and memory values are hypotheses, not production capacity evidence.

If a Kubernetes manifest violates one of these points, it is not a harmless platform adjustment. It is a regression against the predecessor release.

## Use the evidence ladder

The course has four evidence classes.

### 1. Course-book reasoning

A design explanation can establish that you understand ownership and consequences. It cannot prove executable behavior.

### 2. Dependency-light semantic proof

The Python model and Go reconciliation core exercise API versions, managed fields, finalizers, control loops, rollout arithmetic, scheduling predicates, lifecycle state, disruption rules, and custom-resource rendering. These tests are deterministic and required.

They do not prove conformance of an independent Kubernetes implementation.

### 3. Disposable local-cluster proof

The optional kind lane exercises a real API server, etcd, scheduler, controller manager, kubelets, and runtime. It exposes defaulting, asynchronous convergence, events, and runtime behavior.

The lane uses an observation workload because the Course 3 image digests are not public pullable artifacts in this package. It therefore does not prove execution of the Atlas binary. It also cannot prove managed-cluster admission, cloud networking, CSI durability, multi-zone survival, or production capacity.

### 4. Environment-backed proof

A real target cluster can add managed identity, admission, networking, storage, failure-domain, upgrade, and capacity evidence. That evidence must name the environment and exact versions. It is not required for the dependency-light release package and is never fabricated.

## Study method

For each chapter:

1. draw the desired object and child ownership graph;
2. name the component that can perform each transition;
3. predict the observable state before running the lab;
4. answer exercises without opening the worked solutions;
5. inject only the named fault;
6. preserve object, condition, event, and identity evidence before repair;
7. choose the smallest repair that changes the owning input;
8. clean the environment and verify no residual state;
9. state what the evidence still does not prove.

Do not use Pod deletion as a universal troubleshooting ritual. Deletion destroys evidence and usually asks the same controller to recreate the same failing template.

## Tool lane

The required lane needs Python, PyYAML, pytest, and Go. Run:

```bash
make doctor
make core-proof
```

Optional tools include `kubectl`, kind, Docker, MkDocs, and independent schema validators. Missing optional tools are reported as `not-executed`; they are not turned into synthetic success.

Continue to the [Orientation](module-00-orientation/index.md).
