# AxiomStore compatibility fixtures

These files are immutable compatibility evidence for the reference `AXIOM01` format.

- `axiom01-empty.bin` is the canonical empty archive.
- `axiom01-two-records.bin` is the canonical archive containing `alpha=one` and `beta=two` in key order.
- `axiom01-noncanonical.bin` has a valid checksum but stores keys out of order; the decoder must reject it.
- `axiom01-duplicate.bin` has a valid checksum but repeats a key; strict ordering must reject it.
- `legacy-valid.txt` and `legacy-invalid.txt` exercise the V0 migration boundary.

The positive binary fixtures must not be regenerated during ordinary tests. A deliberate format change adds new fixtures and retains old ones so compatibility claims remain independently reviewable.
