# Kubernetes incident evidence template

## Incident identity

- UTC start/end:
- cluster/context:
- namespace/workload:
- affected user journey:
- current severity:

## Desired state

- object UID, generation, resource version:
- exact image digest:
- replica and rollout policy:
- resource and placement constraints:

## Earliest failed transition

- admitted object:
- controller child:
- scheduling:
- node realization:
- container state:
- readiness/availability:
- endpoint/data plane:

## Evidence

- object bundle path/digest:
- event bundle path/digest:
- controller/kubelet logs:
- Node and capacity snapshot:

## Decision

- hypothesis:
- controlled repair:
- rejected alternatives:
- rollback boundary:
- residual risk:
- next owning course/component:
