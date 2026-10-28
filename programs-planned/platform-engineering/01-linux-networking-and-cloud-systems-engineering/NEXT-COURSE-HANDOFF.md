# Course 1 → Course 2 Handoff

Course 2 receives the exact files under `capstone/handoff/`. They define the Atlas host profile and the provider-neutral cloud resources required to reproduce it:

- compute and image requirements;
- service identities and privilege boundaries;
- network, DNS, TLS, firewall, and load-balancing requirements;
- durable, ephemeral, log, and backup storage requirements;
- metadata-service and workload-identity constraints;
- region, zone, replacement, maintenance, and recovery assumptions;
- health, evidence, and acceptance scenarios.

Course 2 may change implementation details only through an explicit requirements revision.
