# Runbook — Service has no usable endpoints

1. Record Service selector, ports, address families, and traffic policies.
2. Inspect EndpointSlices by Service label and address type.
3. Compare endpoint conditions with Pod readiness and termination state.
4. Resolve every named target port against the Pod template and actual listener.
5. Check whether locality policy removes all otherwise eligible endpoints.
6. Use a direct Pod probe only as a controlled comparison, not as the final repair.
7. Repair the earliest false transition and rerun both positive and negative controls.
