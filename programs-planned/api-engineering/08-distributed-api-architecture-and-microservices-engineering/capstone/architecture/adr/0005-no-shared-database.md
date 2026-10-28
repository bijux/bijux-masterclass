# ADR 0005 — No shared database access

Each business service owns its schema and writes. Cross-service reads use APIs, events, or declared projections. Emergency operator queries do not become application dependencies.
