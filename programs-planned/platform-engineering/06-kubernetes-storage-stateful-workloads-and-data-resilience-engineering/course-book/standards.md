# Standards and version profile

The course pins Kubernetes 1.36.2 as the inherited baseline and CSI specification 1.13.0 as the storage-interface reference. PersistentVolume and PersistentVolumeClaim remain core Kubernetes APIs. StorageClass, CSIDriver, CSINode, CSIStorageCapacity, VolumeAttachment, and VolumeAttributesClass belong to storage API groups. VolumeSnapshot resources are extension APIs installed as CRDs and use `snapshot.storage.k8s.io/v1` in the course.

Kubernetes 1.36 promotes volume-group snapshots to GA as a feature, but the installed external-snapshotter CRDs and conversion webhooks determine which API versions are actually served. The course uses `groupsnapshot.storage.k8s.io/v1beta2` for its conservative implementation lane and records this as an implementation profile, not as a universal claim about every 1.36 cluster.

A driver must implement the relevant CSI capability before Kubernetes API fields can produce the intended effect. Volume expansion, snapshotting, cloning, topology, capacity tracking, raw block, multi-node access, and mutable attributes are capability-dependent.

Primary readings are listed in each module and in the reference section.
