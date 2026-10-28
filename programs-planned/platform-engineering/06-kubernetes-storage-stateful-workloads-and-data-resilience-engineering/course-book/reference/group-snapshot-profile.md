# Volume group snapshot profile

Kubernetes 1.36 promotes volume-group snapshot capability to GA, but actual use still depends on installed extension APIs, snapshot-controller components, CSI driver support, and backend behavior. Atlas records the served API version and component matrix instead of assuming that the cluster version alone supplies the feature.

## Intended use

A group snapshot captures a coordinated crash-consistent point for a set of PVCs. It is appropriate when one application state spans several volumes and the backend can snapshot them as a group.

It does **not** automatically include:

- external databases or object stores;
- message-broker offsets;
- application memory;
- volumes omitted from the selector;
- application-level transaction checkpoints;
- independently managed encryption keys.

## Release evidence

The dossier records:

1. group definition and exact member PVC UIDs;
2. class, driver, and backend group identity;
3. application checkpoint or quiesce procedure;
4. capture time and consistency class;
5. deletion and retention policy;
6. restored PVC set and topology;
7. application-level validation;
8. incomplete-group and timeout cleanup behavior.

A group object reaching Ready closes only the storage orchestration phase. Atlas approves recovery only after the restored group satisfies the application invariant.
