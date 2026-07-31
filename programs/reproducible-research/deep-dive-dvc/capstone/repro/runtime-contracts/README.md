# Runtime Contract Specimen

This specimen compares two commands with the same data and rendering logic:

- `declared_runtime` reads its formatting policy from a declared contract file.
- `hidden_runtime` reads the same policy from the `REPORT_STYLE` process environment
  variable, which is absent from the DVC stage declaration.

The audit changes only that policy. A `dot` runtime renders `8.00`; a `comma` runtime
renders `8,00`. The difference is intentionally obvious and deterministic so learners can
study environment visibility without depending on accidental platform behavior.

Generated workspaces and receipts belong under the repository-level `artifacts/`
directory. The specimen remains unchanged.
