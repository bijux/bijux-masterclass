# Course Contents

**Linux, Networking, and Cloud Systems Engineering** is Course 1 of the Platform Engineering program. It is a complete two-week, ten-module self-learning course for a learner who knows basic programming and command-line use but does not yet have a dependable systems, networking, or cloud substrate model.

## Primary learning product

The authoritative course book lives under `course-book/`. It contains:

- eight course guides and a complete operational reference;
- an orientation module plus ten numbered teaching modules;
- one self-contained chapter for every numbered module;
- 120 transfer exercises and 120 corresponding worked answers;
- ten controlled laboratories plus the orientation laboratory;
- ten evidence checkpoints plus the orientation checkpoint;
- a cumulative Atlas Host Runtime capstone narrative;
- a glossary, standards profile, language strategy, evidence model, and two-week study plan.

Every numbered laboratory has a goal, safety boundary, baseline, hypothesis, controlled action, oracle, retained evidence, interpretation, cleanup procedure, and non-compensable completion gate.

## Executable capstone

`capstone/` contains Atlas Host Runtime 1.0:

- separate API, worker, HTTPS edge, and client processes;
- durable file-spool state and atomic result publication;
- explicit shutdown, recovery, readiness, and health behavior;
- dedicated Linux identities and systemd service definitions;
- cgroup-oriented resource policy;
- a bounded Nginx reference edge;
- an owned nftables policy that does not erase unrelated host rules;
- a clearly marked local PKI fixture;
- cloud-init and provider-neutral cloud requirement examples;
- architecture, identity, storage, network, metadata, and failure-domain models;
- automated tests, proof scripts, planted defects, runbooks, assessment material, and an exact Course 2 handoff.

## Intended boundary

This course deliberately stops before containers, Kubernetes, and infrastructure as code. Those abstractions appear only after the learner can explain the processes, files, identities, resource controls, packet paths, trust chains, virtual machines, cloud primitives, and failure domains they conceal.

The package distinguishes dependency-light evidence, local Linux evidence, privileged-VM evidence, and real-cloud evidence. A route that requires a stronger environment is documented and retained, but it is never converted into a synthetic pass when that environment is absent.
