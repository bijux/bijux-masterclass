# Audit evidence consumer

**Inputs:** approved event types from lifecycle and artifact channels.

**Effect:** append a bounded, redacted evidence record. The audit consumer does not treat all broker metadata as trusted; it records contract identity, producer identity, message identity, and verification outcome.

**Privacy:** raw datasets, credentials, stack traces, and unrestricted payload copies are prohibited.
