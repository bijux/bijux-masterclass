# Course 6 predecessor handoff

Course 7 consumes the immutable Course 6 handoff under `capstone/predecessor/handoff/`.

The predecessor establishes:

- Public HTTP API 1.2
- OpenAPI 3.1.2
- Analysis Events API 1.0
- AsyncAPI 3.1.0
- CloudEvents and Event profiles 1.0
- security, reliability, and performance profiles 1.0
- migrations 001–012
- the Analysis Runs ownership, replay, and delivery evidence

Run:

```bash
make predecessor-proof
```

Course 7 may not weaken these guarantees to simplify RPC implementation.
