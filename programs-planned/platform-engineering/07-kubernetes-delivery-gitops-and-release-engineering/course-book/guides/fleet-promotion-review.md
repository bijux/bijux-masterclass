# Guide — Fleet promotion review

A fleet release begins with a cluster catalogue, not a wildcard selector.

Group clusters by meaningful topology: Kubernetes version, provider, region, network, storage, policy, and controller version. Choose waves that provide new evidence rather than arbitrary percentages. Before each wave, check target compatibility and unresolved incidents.

Generator output must be reviewed as a concrete set of Applications or Flux resources. A missing catalogue result is unknown state, not retirement. Cluster deletion or decommissioning requires an explicit owner-approved record.

After each wave, collect resolved revisions, render digests, sync, health, source age, journey results, data gates, and controller versions. Promotion stops when evidence is missing or contradictory.

## Extended reader notes

Review the target catalogue as release input. Every cluster needs owner, lifecycle, region, topology class, Kubernetes version, controller version, and installed capabilities. A generator diff should show targets added and removed. Unknown catalogue state must not become an empty set.

Choose canaries across topology classes, not by alphabetical order. Each wave has entry evidence, observation period, stop condition, and recovery owner. Validate controller and CRD compatibility before the application reaches a cluster. Treat controller upgrades as separate fleet releases.

Test recovery from one unreachable cluster and from source outage. The release may pause or continue according to policy, but it must not silently retire the unknown target.
