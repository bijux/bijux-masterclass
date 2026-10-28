# Case 1 — The Running Pod with no route

## Incident

Atlas API has three Ready Pods. Requests succeed until the Service data plane selects `atlas-api-c` on `node-c`. The request then times out. The Pod has no restarts, its readiness probe passes, and a request from another Pod on `node-c` succeeds.

The first response from the team is to delete `atlas-api-c`. Replacement lands on `node-a`, and traffic appears healthy. The incident is almost closed as “a bad Pod.”

## Why that conclusion is weak

The Pod’s application state was healthy from its local context. Deletion changed placement and therefore changed the network path. The repair removed the symptom without testing the original path.

## Investigation

The team rebuilds a transition ledger for one failed request:

| Transition | Evidence |
|---|---|
| DNS to ClusterIP | correct A record |
| Service to endpoint | EndpointSlice contains `atlas-api-c`, Ready=true |
| source Node data plane | selects `atlas-api-c` address |
| source Node to remote Pod prefix | no matching route |
| destination Node local path | successful |
| application listener | listening on Pod address:8080 |

A route snapshot shows that `node-b` lacks the prefix for Pods on `node-c`. The CNI agent on `node-b` has stopped processing route updates after an earlier control-plane reconnect. Other Nodes have the route.

Packet capture provides the negative fact: the packet leaves the client namespace toward the Service, is translated to the Pod address, but never appears on the underlay interface with the expected next hop. A control request to a Pod prefix on `node-a` follows a valid route.

## Root cause

The local CNI implementation’s route-programming state on one Node was stale. Kubernetes readiness and EndpointSlice state were correct. The failure occurred between selected endpoint and cross-Node route.

## Repair

The operator restores the CNI agent and verifies route reconciliation. They do not permanently exclude `node-c` or weaken readiness. The repaired Node now contains the expected prefix and passes direct Pod, Service, and negative route tests.

## Durable change

The platform adds:

- per-Node route-convergence evidence;
- an alert on CNI programming lag rather than only agent process health;
- a game-day case where one Node lacks one Pod prefix;
- a rule that deleting the selected backend is not an accepted diagnostic repair without path evidence.

## Lesson

Readiness describes the application’s configured health question. It is not proof that every Node can route to the Pod. A placement-changing repair can conceal a network defect. The earliest failed transition, not the first successful workaround, determines the root cause.
