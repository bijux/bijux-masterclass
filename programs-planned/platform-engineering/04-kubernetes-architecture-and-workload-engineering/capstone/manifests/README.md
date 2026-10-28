# Manifest sets

`base/` is the production-intent workload contract. It deliberately references a Course 6 StorageClass that Course 4 cannot provision.

`labs/` contains controller-choice teaching objects.

`controller/` contains the AtlasWorkload CRD, bounded RBAC, controller Deployment contract, and sample resource.

`kind/` is a separate observation lane and is never a production release candidate.
