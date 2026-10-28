# Reference — Fleet failure signatures

Repository outage: increasing source age across clusters, last-known-good workloads continue. Controller outage: source may remain available while reconciliation timestamps stop. Catalogue outage: generators lack input; deletion must not follow. Registry outage: existing Pods survive, new pulls fail. Identity outage: authentication errors at one source or destination boundary.

Correlated failures across clusters often indicate shared controller, repository, credential, policy, or provider dependencies.

## Extended reader notes

Fleet failures often appear as partial convergence. Common signatures include one topology class missing a CRD, one region unable to fetch the repository, older controllers producing different diffs, identity federation failing only in one account, or capacity preventing canary Pods from scheduling.

Catalogue unavailability must be represented as unknown rather than zero targets. A cluster in maintenance is different from a retired cluster. A controller upgrade is distinct from an application release but can change renderer, inventory, or health behavior.

Collect per-cluster source revision, controller version, capability profile, last reconciliation, inventory, health, and release wave. Compare by topology class before broad promotion. Recovery needs a minimal bootstrap layer and credentials that do not create two active controllers for the same ownership scope.
