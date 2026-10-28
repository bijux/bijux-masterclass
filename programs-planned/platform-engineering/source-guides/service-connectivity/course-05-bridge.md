# Course 5 bridge — from reconciled workload to governed connectivity

| Course 4 guarantee | Course 5 expression |
|---|---|
| immutable image identity | networking changes never alter workload subjects |
| stable labels and selectors | Service and policy selection use the inherited labels exactly |
| readiness is truthful | only eligible endpoints receive ordinary Service or Gateway traffic |
| workload identity is not IP identity | NetworkPolicy limits reachability but does not replace authorization |
| topology intent is not proof | locality policies are measured against real endpoint distribution |
| TLS authority must be explicit | listener, certificate, hostname, and backend trust are separate contracts |
| durable storage is deferred | Course 5 publishes the network requirements Course 6 must satisfy |

The bridge prevents a common curriculum error: treating “Pod is Running” as evidence that the application is reachable, discoverable, protected, externally routable, or resilient.
