# Broker evidence boundary

The deterministic broker is the governing dependency-light model for delivery, acknowledgement, redelivery, partition ordering, and consumer-group independence. It is deliberately small enough that learners can inspect every state transition.

`nats/` provides an optional NATS JetStream comparison environment. A successful live run proves integration with that concrete transport; it does not replace the deterministic semantic proofs or imply that every broker has identical behavior.
