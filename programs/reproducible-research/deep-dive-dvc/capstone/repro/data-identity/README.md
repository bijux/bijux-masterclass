# Data Identity Specimen

This specimen is the immutable source for the Module 02 identity audit. The audit copies
it into isolated DVC repositories before changing paths, bytes, caches, or remotes.

`source/observations.csv` is deliberately small enough to inspect by eye. Its role is not
to model a realistic dataset. Its role is to make these claims executable:

- the same bytes have the same content identity at different paths
- replacing bytes at the same path creates a different identity
- a pointer can name content that is unavailable
- a local cache can restore a missing workspace projection
- a configured remote can restore content after both workspace and cache loss

The source file itself never changes during an audit. Every destructive operation happens
inside the generated audit bundle under the repository-level `artifacts/` directory.
