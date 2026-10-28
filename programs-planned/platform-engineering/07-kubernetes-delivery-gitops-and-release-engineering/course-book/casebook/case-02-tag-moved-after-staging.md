# Case 2 — The tag moved after staging

Staging tested `atlas-api:1.8.4`, which resolved to digest A. A rebuild pushed digest B under the same tag before production. Production desired state used only the tag and pulled B.

The pipeline was green, yet production received an untested subject. The cause was identity collapse: semantic version, tag, artifact digest, and release candidate were treated as one value.

The repair pins image digests, records tag-to-digest selection, prohibits rebuild during promotion, and requires new evidence whenever the digest changes.

## Extended reader notes

### Timeline

Staging tested `atlas-api:1.7.0`, which resolved to digest `A`. A registry cleanup rebuilt and repushed the tag as digest `B`. Production promotion changed only the tag string and therefore appeared to promote the tested version. Production pulled `B` and failed during startup.

### Root cause

The release subject was a mutable name. CI evidence and production selection referred to different bytes. Registry policy allowed tag movement, and the dossier did not record the resolved digest.

### Durable correction

Build once, record provenance and tests against digest `A`, and promote `A` unchanged. Tags remain discovery metadata. Admission and delivery policy reject production workloads without digests and compare the artifact set with the predecessor environment.
