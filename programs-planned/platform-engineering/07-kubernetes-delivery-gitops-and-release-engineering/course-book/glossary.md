# Glossary

**Desired revision** — immutable source revision, artifact set, renderer identity, environment inputs, and predecessor selected for an environment.

**Rendered set** — exact Kubernetes object collection produced from the desired revision.

**Render digest** — digest of the course canonical rendered-set profile. It identifies desired output, not live success.

**Inventory** — resources for which a delivery application claims lifecycle responsibility.

**Field authority** — actor permitted and organizationally authorized to change a specific resource field.

**Drift** — difference between desired and observed state. Classes include unauthorized, shared-manager, defaulting, admission, controller-generated, emergency, and unmanaged.

**Promotion** — selecting the same immutable artifact subjects in a more demanding environment after required evidence passes.

**Rebuild** — producing new bytes. A rebuild is a new candidate even when source tag or semantic version is unchanged.

**Prune** — deletion of an inventory member absent from the current desired set.

**Protected resource** — resource whose deletion needs authority and evidence beyond ordinary reconciliation.

**Sync** — bounded comparison of owned live fields with rendered desired fields.

**Health** — resource-specific assessment of progress or service based on declared status. Health is not business or data correctness.

**Hook** — resource executed in a delivery phase. Hook ordering is not transactionality or exactly-once execution.

**Break glass** — time-bounded, incident-linked bypass with narrow authority and a route back to reviewed desired state.

**Progressive delivery** — controlled candidate exposure with explicit populations, analysis, decision, and abort behavior.

**Rollback frontier** — latest phase where prior traffic and manifests remain safe without data restoration or incompatible side effects.

**Forward fix** — new compatible release used when the rollback frontier has been crossed.

**Fleet profile** — cluster owner, lifecycle, version, controller, topology, region, and capabilities used for release compatibility.

**Evidence subject** — exact commit, digest, rendered set, resource, environment, or release to which an observation applies.

**Not executed** — required evidence was not produced. It is never equivalent to pass.
