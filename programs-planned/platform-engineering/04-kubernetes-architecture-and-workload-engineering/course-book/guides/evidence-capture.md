# Evidence capture

A Kubernetes screenshot is rarely reproducible evidence. Capture structured data before mutation.

## Minimum object bundle

```bash
kubectl get deployment,replicaset,pod -n atlas-system -o yaml
kubectl get events -n atlas-system --sort-by=.metadata.creationTimestamp -o yaml
kubectl get nodes -o yaml
kubectl api-resources -o wide
kubectl version -o yaml
```

Add controller logs, Pod logs, previous-container logs, and relevant API audit/admission evidence where available.

## Time and identity

Record:

- UTC timestamps;
- object UID, generation, and resource version;
- Node UID and kubelet version;
- image repository and digest;
- field manager;
- command exit status;
- cluster/context identity.

## Interpretation boundary

State what the evidence proves and what it does not. A local kind rollout proves mechanics in that environment. It does not prove managed-cluster admission, cloud networking, persistent storage, or production capacity.
