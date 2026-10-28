# kubectl reading map

Commands are examples of API queries, not substitutes for an ownership model.

```bash
kubectl get OBJECT -o yaml
kubectl get OBJECT -o jsonpath='...'
kubectl describe OBJECT
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl logs POD -c CONTAINER
kubectl logs POD -c CONTAINER --previous
kubectl auth can-i VERB RESOURCE --as system:serviceaccount:NS:SA
kubectl explain RESOURCE.FIELD
kubectl wait --for=condition=Available deployment/atlas-api
kubectl rollout status deployment/atlas-api
kubectl rollout history deployment/atlas-api
```

Before deletion or force application, save full object and event evidence.
