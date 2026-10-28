# MetricRail configuration contract

MetricRail currently exposes a deliberately small compiled configuration in `Config`. The defaults are suitable for local demonstration, not a universal production recommendation. A deployment owner must derive each value from a named workload and capacity model.

| Field | Governs | Failure when exhausted |
|---|---|---|
| `max_line_bytes` | one protocol line, including the command prefix | the connection receives `LINE_TOO_LONG` and is closed |
| `max_identifier_bytes` | each tenant and metric identifier | the record is rejected as invalid |
| `max_connections` | admitted TCP connections | admission is refused with a best-effort overload response |
| `mailbox_capacity` | commands accepted by the broker queue | the request receives `OVERLOADED` |
| `max_active_ingest` | ingest callers allowed to wait for broker completion | the request receives `OVERLOADED` before queue admission |
| `max_series` | distinct retained series | the record receives a domain rejection |
| `max_identifier_storage_bytes` | retained tenant and metric text | the record receives a domain rejection |
| `max_snapshot_bytes` | rendered snapshot response | the request receives `SNAPSHOT_TOO_LARGE` |
| `max_offline_records` | records accepted by offline analysis and the load tool | the CLI rejects the input |
| `max_offline_bytes` | bytes read by offline analysis and the load tool | bounded reading stops and the CLI rejects the input |
| `connection_idle_timeout_ms` | time allowed between complete client commands | the connection receives `IDLE_TIMEOUT` and closes |
| `write_timeout_ms` | time allowed for one response write | the connection task ends with an I/O timeout |
| `load_request_timeout_ms` | end-to-end time allowed for one load-generator exchange | the attempt is classified as failed |
| `shutdown_grace_ms` | drain time after listener quiescence | remaining connection tasks are aborted and joined |

## Relationships that validation enforces

- every capacity and deadline is nonzero;
- an identifier cannot be larger than a complete line;
- active ingest waiters cannot exceed broker mailbox capacity;
- one line cannot exceed the complete offline-input byte limit.

These checks prevent internally contradictory configurations. They do not prove that the values fit a deployment. The capacity worksheet in `CAPACITY.md` supplies that second proof.

## Change procedure

1. Name the workload or incident that motivates the change.
2. Record the current saturation knee and resource headroom.
3. Predict the effect on memory, queue residence, rejection rate, and recovery time.
4. Run the relevant offline, load, overload, and shutdown tests.
5. Roll out through the staged procedure in `ROLLOUT.md`.
6. Retain the old value and rollback trigger in the change record.

Increasing a queue or timeout without this analysis is not a neutral reliability improvement. It can convert an explicit rejection into hidden latency or retained memory.
