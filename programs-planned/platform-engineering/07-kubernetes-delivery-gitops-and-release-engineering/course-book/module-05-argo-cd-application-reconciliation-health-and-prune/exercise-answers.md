# Worked answers — Argo CD application reconciliation, health, and prune

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why should an Argo CD Application align with lifecycle ownership rather than repository layout alone?

The Application owns inventory, sync, health, and prune for its rendered resources. Resources with different owners, privileges, recovery duties, or release cadence should not share that lifecycle merely because their YAML lives together. Conversely, splitting one coherent workload into many Applications can make ordering and health fragmented.

## 2. What security role does AppProject play?

It restricts acceptable sources, destinations, namespaces, and resource kinds, thereby bounding what Applications and their authors can cause the Argo CD controller to write. It should be treated as an authorization boundary, not just a grouping label.

## 3. Why must automated sync, self-heal, and prune be reviewed separately?

They act on different triggers and risks. Automated sync applies new desired revisions, self-heal repairs drift under the current revision, and prune deletes inventory objects absent from desired state. An application may safely automate one while requiring approval or prohibition for another.

## 4. What makes a diff ignore rule dangerous?

A broad rule can hide unauthorized or semantically important drift. Ignore rules should target a precise field owned by another manager, identify the reason and owner, include an expiry or review date, and have a test proving that dangerous neighboring fields remain visible.

## 5. Why is custom resource existence not sufficient health evidence?

The object may exist while its controller has not processed the current generation, a dependency is missing, or a terminal failure condition is present. Health should evaluate authoritative status conditions, observed generation, and the resource-specific success semantics.

## 6. What guarantee do sync waves provide?

They provide ordering hints among resources within a sync operation. They do not provide atomicity, global rollback, or exactly-once execution. Earlier waves may have committed when a later wave fails, so each action needs idempotency, compensation, or a safe resume path.

## 7. Why is a migration hook a privileged workload?

It may hold database credentials and change authoritative data. It therefore needs immutable code, least privilege, durable operation identity, bounded retries, observability, and compatibility analysis. Calling it a hook does not reduce its risk.

## 8. What is the fleet risk of ApplicationSet generators?

A small generator or selector change can add, remove, or retarget many Applications and clusters. Generator inputs are therefore fleet-scope desired state. Review should show generated Application additions, removals, destinations, and revisions before reconciliation.

## 9. When can multiple sources be justified?

When they have explicit ownership, immutable revisions, clear precedence, and a release record that binds all sources into one desired revision. They are unsafe when an unreviewed values repository or mutable chart source can change production output independently.

## 10. Why should a repository fetch failure not result in prune?

Failure to observe desired state is not evidence that desired state is empty. Pruning under uncertainty converts a source outage into destructive cluster change. The controller should retain last-known-good resources and report source staleness or error.

## 11. What evidence is required before adopting an orphan resource into an Application?

Capture its identity, current fields, field managers, owner, consumers, data, dependencies, lifecycle, and deletion implications. Determine which fields the Application will take over and test the first sync diff. Adoption is an authority migration, not a simple file addition.

## 12. Why is Argo CD health not the final release decision?

It evaluates Kubernetes resource signals within a bounded model. It does not prove user journeys, semantic correctness, data migration safety, restore readiness, or external dependency behavior. Those remain separate gates in the Atlas release dossier.
