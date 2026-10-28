# Common Misconceptions

## “OpenTofu state is the source of truth”

State is a binding and observation record. Configuration expresses desired
policy; the remote system and workload data plane have their own facts.

## “Encryption means no secret can appear in state”

Encryption protects stored bytes under a key policy. Operators, runners, and
provider/plugin processes may still read plaintext. Secret minimization remains
necessary.

## “A module is reusable because it has variables”

A useful module owns a coherent capability and publishes a stable interface.
A wrapper around one resource can add indirection without an abstraction.

## “Private subnet means no internet access”

A private subnet can have egress through NAT, endpoints, transit, or proxies.
The route and policy path determine reachability.

## “The role policy is all of IAM”

Trust, identity policies, resource policies, SCPs, permission boundaries,
session policies, and KMS key policies can all affect the decision.

## “Backup succeeded because the snapshot is complete”

Only a tested restore with integrity and application validation establishes the
recovery path.

## “No changes means safe”

A no-op plan says the provider sees no managed difference. It does not prove
DNS, TLS, application readiness, backup, or ownership.
