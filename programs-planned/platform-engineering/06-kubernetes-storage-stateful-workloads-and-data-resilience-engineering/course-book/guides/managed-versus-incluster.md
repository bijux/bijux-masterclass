# Managed service versus in-cluster operation

Choose by ownership and failure model, not by ideology.

| Concern | Managed service | Kubernetes operator | Direct StatefulSet |
|---|---|---|---|
| engine lifecycle | provider shares responsibility | operator automates declared lifecycle | team owns all procedures |
| control plane | provider API | CRDs/controllers | native workload/storage APIs |
| backups | provider feature plus your restore proof | operator-dependent | team-built |
| failure domains | provider-specific | operator + cluster + storage | team-designed |
| upgrades | provider workflow and limits | operator contract | manual process |
| portability | lower at service layer | moderate | often overstated due storage/runtime coupling |
| operational burden | reduced, not removed | high and specialized | highest |

## Decision criteria

Compare availability target, RPO/RTO, latency, data residency, identity integration, scaling, major upgrades, recovery expertise, staffing, cost, and provider limits. Name every responsibility retained by your team.

A managed service can still fail through IAM, DNS, networking, quota, or misconfiguration. An operator can automate unsafe behavior if its contract is misunderstood. A raw StatefulSet can be acceptable for an educational or simple replicated service but should not be mistaken for a complete database platform.

Atlas requires a written decision record and an empty-destination restore proof for every lane.
