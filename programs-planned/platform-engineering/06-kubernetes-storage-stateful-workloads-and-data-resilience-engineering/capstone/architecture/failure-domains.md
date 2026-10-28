# Failure-domain map

| Asset | Required survival | Mandatory lane evidence | Native evidence needed |
|---|---|---|---|
| run state | Pod and Node loss | local durable ledger and restore | CSI/backend/database failure test |
| artifacts | cluster loss | content-addressed backup and checksum | object-store durability and account recovery |
| snapshots | source-volume corruption rollback | snapshot catalogue semantics | CSI snapshot and restore |
| backups | cluster and account loss | empty-destination restore | cross-domain transfer and operated restore |
| fencing state | stale writer return | monotonic token rejection | database or storage fencing |
