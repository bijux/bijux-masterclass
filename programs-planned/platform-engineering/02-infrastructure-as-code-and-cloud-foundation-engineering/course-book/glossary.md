# Glossary

**apply** — Execution of a previously reviewed or freshly calculated infrastructure change. An apply can partially succeed before failing.

**backend** — The OpenTofu component that stores state and may provide locking. The backend must exist before a configuration can use it.

**configuration** — The declarative source files and input values that describe desired resource relationships.

**data plane** — The path that serves workload traffic or data. Control-plane success does not prove data-plane correctness.

**drift** — A difference between the last recorded state/configuration and remote infrastructure, whether caused by external change, provider normalization, or incomplete observation.

**ephemeral value** — A value intentionally omitted from state and plan persistence where supported. Ephemerality is not a substitute for secret-system design.

**import** — Association of an existing remote object with an OpenTofu resource address and configuration.

**landing zone** — A governed cloud foundation for accounts, identity, logging, networking, and controls. It is an operating boundary, not one VPC template.

**lineage** — A state identity used to distinguish independent state histories.

**lock** — Mutual-exclusion mechanism intended to prevent simultaneous state writers. A lock does not validate the proposed change.

**module** — A group of OpenTofu files that defines an architectural abstraction with inputs and outputs. A thin wrapper around one resource usually adds little value.

**plan** — A proposed set of actions calculated from configuration, state, provider schemas, credentials, refresh results, and input values.

**provider** — A plugin that translates OpenTofu resource operations into remote-system API operations and returns observed state.

**refresh** — Provider observation used to update OpenTofu’s view of remote objects before or during planning.

**remote state** — State stored in a shared backend rather than only on one operator’s disk.

**resource address** — Stable configuration/state identity such as `module.network.aws_vpc.this`. Renaming an address without a move declaration may imply destroy/create.

**root module** — The working directory in which OpenTofu is run. It composes child modules and owns provider configurations and backend selection.

**serial** — Monotonically increasing state snapshot revision within one lineage.

**state** — OpenTofu’s operational record connecting resource addresses to provider objects and attributes. State is sensitive and is not merely a cache.

**state surgery** — Direct state manipulation such as manual moves, removals, pull/edit/push, or backend-object restoration. It requires an incident-grade procedure.

**unknown value** — A value that cannot be known until apply, commonly because it depends on a resource not yet created.

**workspace** — Multiple state instances for one configuration. Workspaces are not a complete isolation model for accounts, credentials, policy, or lifecycle.
