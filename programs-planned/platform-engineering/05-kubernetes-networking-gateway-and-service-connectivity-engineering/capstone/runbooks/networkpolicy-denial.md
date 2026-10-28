# Runbook — unexpected NetworkPolicy denial

1. Identify the exact source and destination Pod identities and addresses.
2. Determine isolation independently for source egress and destination ingress.
3. Evaluate all policies selecting each side; policies are additive.
4. Confirm protocol, port, namespace labels, Pod labels, and label authority.
5. Compare semantic verdict with installed implementation flow evidence.
6. Add the narrowest justified allow; avoid broad temporary policy as final state.
7. Prove an intended allow and an intended deny after the change.
