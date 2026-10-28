# Program standards policy

Course 6 inherits Kubernetes 1.36.2 and the Course 5 connectivity contract. It uses CSI specification 1.13.0 as the storage-interface reference, `snapshot.storage.k8s.io/v1` for volume snapshots, and a conservative `groupsnapshot.storage.k8s.io/v1beta2` implementation lane for group-snapshot manifests while documenting the Kubernetes 1.36 GA feature status separately. VolumeAttributesClass is treated as stable in Kubernetes 1.36, but only when the selected CSI driver implements the corresponding modify-volume capability.

The program distinguishes upstream API semantics, Atlas contracts, implementation-specific behavior, and evidence-backed claims. A field existing in an API does not prove that a driver supports it. A successful snapshot object does not establish application consistency. A backup job completing does not establish restoration.
