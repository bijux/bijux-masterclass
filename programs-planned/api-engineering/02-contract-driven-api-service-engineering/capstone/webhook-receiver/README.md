# Controlled Webhook Receiver

This receiver is not a toy endpoint that blindly prints a request. It verifies the timestamped HMAC signature, requires the header event identifier to match the payload, enforces a body limit, stores receipts durably in SQLite, accepts exact duplicate delivery idempotently, and rejects reuse of an event identifier with different bytes.

The query controls `?fail_first=N` and `?status=CODE` exist only inside the isolated course network. They create reproducible retry and terminal-failure exercises. They must never be exposed as a production feature.

```bash
python receiver.py
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/deliveries
```
