# Component ownership matrix

| Transition | Primary owner | Desired object | Observation |
|---|---|---|---|
| API admission | API server and admission chain | submitted resource | admitted object or Status failure |
| Deployment revision | Deployment controller | Deployment | ReplicaSet and Deployment conditions |
| replica population | ReplicaSet controller | ReplicaSet | owned Pods and replica counts |
| Pod placement | scheduler | unscheduled Pod | binding/nodeName and scheduling condition |
| Pod realization | kubelet/runtime | bound Pod | container states and Pod conditions |
| projected data | kubelet | Pod references | mounted files and Pod events |
| Job completion | Job controller plus workload | Job | succeeded/failed counts and conditions |
| Cron scheduling | CronJob controller | CronJob | owned Jobs and schedule status |
| node-derived Pod population | DaemonSet controller | DaemonSet | eligible-node Pods and status |
| stable ordinal population | StatefulSet controller | StatefulSet | Pods/PVC identities and status |
| voluntary disruption allowance | PDB controller and eviction API | PDB | disruptionsAllowed and conditions |
| custom workload composition | Atlas controller | AtlasWorkload | child objects and custom status |

Network packet forwarding, storage durability, admission security, GitOps release authority, fleet operation, and developer self-service belong to later courses.
