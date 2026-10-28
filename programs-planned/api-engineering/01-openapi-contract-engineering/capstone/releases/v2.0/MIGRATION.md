# Migration from 1.1 to 2.0

Version 2 deliberately removes the combined dataset resource endpoint and removes the `progress` field from `AnalysisRun`.

Consumers must stop calling `GET` and `DELETE /datasets/{datasetId}` and use the replacement lifecycle operations defined by the production v2 contract before switching servers. Consumers must also derive progress from the event stream rather than the run representation.

The course does not claim that a major version makes a break harmless. The release is accepted only because the break is explicit, mechanically detected, versioned, and accompanied by migration evidence.
