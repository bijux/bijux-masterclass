# Optional NATS JetStream route

This topology is a comparison target after the dependency-light proofs pass.

It demonstrates durable streams, explicit acknowledgements, consumer redelivery, and replay against one real broker. Fixture credentials are intentionally local and must never be treated as deployment guidance.

```bash
make nats-up
make nats-proof
make nats-down
```

The course never converts an unavailable Docker or NATS environment into a passing result.
