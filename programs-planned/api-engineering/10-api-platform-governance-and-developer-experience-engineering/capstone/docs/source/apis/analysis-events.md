# Analysis Events API

**Contract:** `api:default/analysis-events` version 1.0.0  
**Authority:** Analysis Control Team  
**Protocol:** AsyncAPI 3.1.0 with the course CloudEvents profile

Use this interface for durable integration after authoritative state changes. Consumers must tolerate redelivery, preserve tenant boundaries, deduplicate by stable event and effect identity, and treat replay as a governed operation. The event contract does not replace the HTTP command boundary or the source service's transaction authority.
