# Service-mesh decision record

A mesh proposal must name one capability and compare alternatives.

```text
problem:
current evidence:
required guarantee:
Kubernetes/application/Gateway alternatives:
mesh capability:
data-plane placement:
identity/trust model:
retry and timeout ownership:
resource and latency cost:
upgrade/failure model:
observability/debugging:
rollback:
decision:
```

Reject proposals whose rationale is “standardization,” “zero trust,” or “better observability” without a measurable gap. Atlas Course 5 rejects a mesh because current requirements are met without adding another retrying proxy and control plane.
