# Reference — Rollback boundaries

Traffic rollback changes routing. Manifest rollback changes desired Kubernetes resources. Configuration rollback selects earlier settings. Feature rollback disables behavior. Data rollback restores or compensates authoritative state.

The rollback frontier is the last phase where stable binaries and prior desired state remain compatible with current data and external effects. Beyond it, forward repair may be required.

## Extended reader notes

The Atlas rollback frontier is the latest phase at which prior manifests and stable traffic can be selected without data restoration or incompatible side effects. Before writer cutover, rollback may be a traffic and desired-state change. During dual-read compatibility, stable and candidate can coexist. After old-writer removal or schema contraction, the prior binary may no longer be safe.

Other boundaries include irreversible external effects, revoked credentials, deleted resources, and changed client contracts. Feature flags can restore behavior only when both code paths remain compatible with current state.

Every release plan states the current frontier, the owner who may move it, and the forward-fix procedure beyond it. A Git revert is a source operation; it is not automatically a system rollback.
