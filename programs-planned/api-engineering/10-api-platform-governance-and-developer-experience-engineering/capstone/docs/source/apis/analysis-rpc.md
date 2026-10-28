# Analysis RPC API

**Contract:** `api:default/analysis-rpc` version 1.0.0  
**Authority:** Analysis Control Team  
**Protocol:** Protobuf and gRPC

Use this internal interface for typed worker control, bounded streaming, deadlines, cancellation, and lease-aware attempts. Callers must propagate workload identity, tenant context, and deadlines. The API platform publishes descriptors and compatibility evidence; it does not own worker scheduling or analysis-run truth.
