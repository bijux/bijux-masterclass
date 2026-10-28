# Debugging by controller ownership

Kubernetes incidents become tractable when each symptom is mapped to the component able to change it.

| Symptom | First owner to inspect | First evidence |
|---|---|---|
| request rejected | API server admission/authorization | status response and audit/admission evidence |
| Deployment exists, no ReplicaSet | Deployment controller | Deployment conditions and controller health |
| ReplicaSet exists, no Pods | ReplicaSet controller | ReplicaSet status, events, selector |
| Pod Pending, no Node | scheduler | scheduling condition and per-Node failure reasons |
| Pod bound, containers absent | kubelet/runtime | Pod status, Node condition, runtime events |
| container restarts | application/kubelet | current and last state, exit reason, probe history |
| Pod ready, consumer fails | networking/application | endpoint membership and Course 5 evidence |
| deletion stuck | finalizer owner | deletion timestamp, finalizers, cleanup condition |
| rollout stalls | Deployment plus downstream transition | updated/ready/available populations and events |
| custom resource churns | custom controller | resource-version/status diffs and reconcile decisions |

## Recovery rule

Prefer the smallest action that changes the failed owner's inputs. Deleting a Pod asks the same controllers to repeat the same desired state. It is useful only when a transient local state is plausibly repaired by replacement and that hypothesis is recorded.

## Evidence packet

A reproducible packet should include:

- command or API query used;
- object YAML/JSON before repair;
- relevant events with timestamps and involved UIDs;
- controller and Node identity;
- exact image digest;
- scheduling and resource inputs;
- probe and termination state;
- selected repair and rejected alternatives;
- residual risk and next owner.
