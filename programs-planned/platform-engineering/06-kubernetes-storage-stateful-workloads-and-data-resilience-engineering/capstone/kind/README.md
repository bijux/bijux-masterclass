# Optional kind storage lane

This lane requires a disposable kind cluster, `kubectl`, a CSI-capable driver, and the snapshot CRDs/controller. Host-path or local-path storage can prove PVC, StatefulSet, mount, and some lifecycle behavior; it cannot prove cloud attachment, zonal durability, independent snapshots, or production recovery.
