# Controlled Security Webhook Receiver

This local receiver verifies the Course 3 exact-byte signature profile, timestamp freshness, key identity, and replay state before parsing JSON or recording an effect. It is deliberately small and intended only for the isolated lab. Run it with the Python security package on `PYTHONPATH`; do not expose it publicly.
