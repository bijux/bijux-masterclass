# Capstone map — Analysis API Platform 1.0

## Existing capabilities

The platform inherits four real interface families:

| Interface | Owner | Purpose |
|---|---|---|
| Analysis HTTP API 1.2 | Analysis Control | Public resource and command surface |
| Analysis Events API 1.0 | Analysis Control | Durable asynchronous integration |
| Analysis RPC API 1.0 | Analysis Control | Typed internal invocation and streaming |
| Analysis Graph API 1.0 | API Platform with source owners | Governed client-shaped composition |

## Course 10 additions

```text
Source repositories
      │
      ├── catalog descriptors ───────┐
      ├── released contracts ────────┤
      ├── evidence and lifecycle ────┤
      └── docs, SDKs, templates ─────┤
                                     v
                         Analysis API Platform
                     ┌──────────┬──────────┐
                     │ Catalog  │ Registry │
                     ├──────────┼──────────┤
                     │ Policy   │ Lifecycle│
                     ├──────────┼──────────┤
                     │ Portal   │ Sandbox  │
                     ├──────────┼──────────┤
                     │ SDKs     │ Runtime  │
                     └──────────┴──────────┘
                              │
                              v
                    Consumers and API owners
```

The platform owns the mechanisms above. It does not own project state, analysis
state, artifact truth, notification truth, or domain authorization. Those remain
with the services established in Course 8.

## Final proof

The final defense follows one new consumer from discovery to first success and
one API owner from proposed interface to published release. It also demonstrates
a rejected unsafe retirement, an expiring exception, an immutable registry
conflict, a safe generated scaffold, an SDK provenance check, and a runtime drift
report.
