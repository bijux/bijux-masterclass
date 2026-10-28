# Ten-day study plan

The course contains ten dense modules after orientation. One module per day is possible for an experienced learner; two or three sessions per module is often more realistic. Preserve the order because each day’s subject becomes the next day’s immutable input.

| Day | Governing question | Irreversible insight | Atlas increment |
|---:|---|---|---|
| 1 | What is a container boundary? | A container is a Linux process tree with selected views, authority, and resource governance—not a VM or image. | Observed process boundary and isolation claim. |
| 2 | How is execution requested portably? | An OCI bundle is a lifecycle/authority contract independent of the image-distribution graph. | Bundle, state machine, mappings, cleanup evidence. |
| 3 | What exact bytes form an image? | An image is a content-addressed graph of configs, ordered changesets, and platform selectors. | Deterministic API/worker/probe layouts. |
| 4 | What actually influences build output? | Context, tools, network, cache, platform, time, and secrets are build inputs. | Controlled build profile and secret-negative proof. |
| 5 | When is a platform claim true? | `linux/arm64` is a publisher claim until executable, ABI, and target evidence support it. | amd64/arm64 indexes and per-platform matrix. |
| 6 | What does a registry guarantee? | Registries transport content and mutable references; promotion authority remains external. | Digest push/pull, tag movement, referrers, retention. |
| 7 | What runs in practice? | Effective runtime authority is the merge of image defaults, runtime request, host enforcement, and observation. | Approved API/worker/probe profiles. |
| 8 | What is inside and what risk follows? | Inventory, matching, affectability, VEX, licenses, and authorization are different decisions. | Subject-bound SBOM/risk record. |
| 9 | Who produced this subject? | Cryptographic validity is narrower than authorized origin. | Signed provenance and verifier policy. |
| 10 | What may enter Kubernetes? | Promotion is a categorical authorization over exact subjects and evidence, with rollback/revocation obligations. | Atlas Workload Release 1.0 and Course 4 handoff. |

## The daily learning loop

### Build the model

Read the chapter and draw two diagrams: the object graph and the authority graph. Ask who owns desired state, which identity is stable, and what dangerous half-state can remain after failure.

### Interrogate one real artifact

Follow one layer, config, manifest, index, registry response, runtime profile, SBOM component, provenance material, or release record. Verify the exact bytes/identity before interpreting fields.

### Falsify one claim

Run the lab. Establish baseline, state a hypothesis, introduce one fault, observe the named oracle, and explain why the result distinguishes competing causes. Do not combine faults until you understand each independently.

### Defend the decision

Complete the checkpoint. State the strongest supported claim and the nearest stronger claim that remains unproved. Preserve evidence and cleanup output.

## Suggested pacing within a module

- **Session A:** chapter and diagrams;
- **Session B:** exercises and implementation reading;
- **Session C:** lab, evidence journal, checkpoint defense.

On Days 3, 4, 7, and 9, reserve extra time: image graph, build inputs, runtime authority, and provenance policy are the course’s conceptual hinges.

## Recovery when stuck

Do not add privilege or switch tools randomly. Use the [debugging guide](guides/debugging-container-releases.md): candidate identity → object graph → platform → registry → effective runtime → application → evidence/policy. The first divergent phase is normally the most useful diagnosis.

## Completion

After Day 10, complete the [practical assessment](assessment/practical-assessment.md) and [final defense](assessment/final-defense.md). The course is complete only when the accepted release and every planted defect produce the intended categorical decision.
