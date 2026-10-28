# Case 6 — Bootstrap during a source outage

A cluster was replaced while the primary Git provider was unavailable. The bootstrap job installed the controller, which interpreted a failed source fetch as no desired resources. An unsafe cleanup routine removed bootstrap objects and left the cluster incomplete.

The failure confused unknown source state with empty desired state and assumed Git alone was sufficient recovery material.

The repair uses mirrored controller artifacts, scoped recovery credentials, last-known revision records, source-unavailable status, and a bootstrap procedure that never prunes under uncertainty.

## Extended reader notes

### Timeline

A regional repository outage coincided with a controller upgrade. The replacement controller had no cached source artifact. An operator ran a bootstrap script that installed a default configuration pointing at a mutable branch. It converged on a newer unreviewed revision.

### Root cause

Bootstrap did not preserve last verified source identity, repository trust, or controller version. Recovery authority favored availability over lineage without an explicit decision.

### Durable correction

The minimal seed package contains pinned controller artifacts, CRDs, repository trust, and last-known-good commit. Source failover verifies object identity. Only one controller owns a cluster scope at a time, and post-recovery reconciliation records any emergency fork.
