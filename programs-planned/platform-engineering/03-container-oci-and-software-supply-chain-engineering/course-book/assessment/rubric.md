# Assessment rubric

| Dimension | Points | Elite evidence |
|---|---:|---|
| Object and identity model | 15 | Every source/layer/config/manifest/index/evidence subject is distinguished and traced correctly. |
| Build and secret discipline | 12 | Context, cache, toolchain, network, secret, and controlled-rebuild boundaries are explicit and tested. |
| Platform correctness | 10 | Each required platform has binary/ABI and target-evidence classification. |
| Runtime contract | 13 | Effective identity, mounts, capabilities, namespaces, lifecycle, resources, and cleanup are observed. |
| Distribution | 8 | Push/pull, digest identity, tag role, referrers, and retention boundaries are correctly defended. |
| Inventory and risk | 10 | SBOM completeness, vulnerability matching, VEX, and license decisions are subject-bound and reviewable. |
| Provenance and trust | 12 | Envelope, signer, builder, source, materials, revocation, and policy are verified separately. |
| Release and recovery | 10 | Promotion, exceptions, rollback, revocation, and registry retention are coherent. |
| Course 4 handoff | 5 | Handoff is exact and Kubernetes cannot silently weaken it. |
| Communication | 5 | Claims are precise, evidence is reproducible, and uncertainty is stated without evasion. |

Passing score: **85/100**.

## Non-compensable failures

Regardless of total score, the candidate fails if it:

- deploys by mutable tag;
- contains/recoverably leaks a secret;
- mislabels a required platform;
- runs with unauthorized root/privileged authority;
- accepts evidence for the wrong subject;
- authorizes an untrusted builder/signing identity;
- hides a failed or unexecuted gate;
- produces an inconsistent Course 4 handoff.

An elite score requires showing that the proof suite is sensitive: at least one planted candidate must fail for each major gate, and the learner must explain why the oracle would catch the real defect rather than merely a fixture name.
