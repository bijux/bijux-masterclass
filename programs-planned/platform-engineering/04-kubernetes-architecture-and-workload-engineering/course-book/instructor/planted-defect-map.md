# Planted-defect map

The ten defects align with the ten modules:

1. desired state persists but a stopped controller does not converge;
2. one manager force-owns another manager's replicas;
3. a container runs as root with a writable root filesystem;
4. selector/template labels disagree and rollout cannot own the intended Pods;
5. a batch effect lacks logical completion identity;
6. a secret is embedded in an annotation;
7. placement constraints are jointly impossible;
8. liveness depends on a remote service;
9. durable worker paths use `emptyDir`;
10. controller status changes timestamp every reconcile and finalizer cleanup is omitted.

Require the learner to identify the proof that rejects each defect, not only the corrected YAML.
