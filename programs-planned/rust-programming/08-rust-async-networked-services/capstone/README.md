# JobWire

JobWire is the cumulative capstone for Course 8. It is a bounded single-process async job service with:

- a length-delimited TCP protocol;
- version negotiation;
- sequential request/response connections;
- one broker task as semantic state authority;
- bounded queued and active work;
- process-local idempotency records;
- controlled retry and deadline behavior;
- an HTTP/1 health and statistics surface;
- hierarchical cancellation and joined shutdown;
- deterministic protocol, saturation, retry, and lifecycle tests.

The implementation is intentionally direct. It does not use a web framework or serialization framework because the course needs the transport, body, protocol, and service boundaries to remain visible.

## Commands

```text
jobwire serve [--tcp ADDRESS] [--http ADDRESS]
jobwire submit ADDRESS REQUEST_ID IDEMPOTENCY_KEY OPERATION PAYLOAD
jobwire stats ADDRESS REQUEST_ID
jobwire ping ADDRESS REQUEST_ID
jobwire health HTTP_ADDRESS
jobwire demo
jobwire help
jobwire version
```

Supported operations:

```text
uppercase
word-count
checksum
sleep-ms
```

The `sleep-ms` payload is an integer duration bounded by configuration.

## Wire protocol

Every payload is carried in a four-byte big-endian length-prefixed frame.

```text
HELLO\t1
WELCOME\t1
SUBMIT\trequest-id\tidempotency-key\toperation\tpayload
OK\trequest-id\tresult
BUSY\trequest-id\tretry-after-ms
ERR\trequest-id-or-dash\tcode\tmessage
STATS\trequest-id
STATS-OK\trequest-id\thealth\tactive\tqueued\trecords\tcompleted\tfailed
PING\trequest-id
PONG\trequest-id
QUIT
BYE
```

V1 permits one in-flight request per connection. Concurrency exists across connections and broker jobs.

The configured result limit is smaller than the frame-payload limit because an `OK` response must also carry the response tag, request ID, and separators. `Config::validate` reserves a conservative 128-byte response envelope; an admitted terminal result therefore remains encodable under the same frame bound.

## Run

```bash
cargo run -- serve --tcp 127.0.0.1:7800 --http 127.0.0.1:7801
cargo run -- submit 127.0.0.1:7800 r-1 key-1 uppercase "hello rust"
cargo run -- health 127.0.0.1:7801
```

Use `scripts/demo.sh` for a complete local scenario.
