# Worked Answers — Edge, Data Protection, Backup, and Recovery

## 1. Request path

A resolver obtains the authoritative DNS answer, the client opens a connection to the load balancer, TLS selects and validates a certificate for the hostname, the listener applies a rule, the target group selects a healthy target, security groups permit the ALB-to-host flow, and Atlas accepts the request on its private socket. Cloud control resources and actual network/application behavior must both be checked.

## 2. Certificate versus DNS authority

A principal allowed to validate arbitrary certificates for a zone can create identities for names it may not otherwise be allowed to route. Conversely, a DNS release role should not necessarily administer certificate keys or validation policy. Separating the authorities reduces the consequence of either credential being compromised.

## 3. Overly broad health checks

An optional dependency outage can mark every target unhealthy and turn a partial degradation into total unavailability. The routing check should represent whether sending the supported traffic is useful, while richer readiness and telemetry report optional or downstream failures separately.

## 4. Detection time

Three failures at 15-second intervals suggest roughly 45 seconds after failed checks begin, but scheduling phase, request timeout, target registration state, and provider implementation can add time. The result is a bound/hypothesis until measured.

## 5. Security-group reference

Referencing the ALB security group ties permission to the intended caller identity within the VPC, not every address in a broad network range. A CIDR rule would allow any compromised or accidental host in that range to reach the application port directly.

## 6. Three storage properties

An EBS volume may preserve bytes after an instance failure (**durability**) while Atlas is unavailable because no healthy instance can attach/read it (**availability**). A tested snapshot restore into a new volume and validated host establishes a bounded form of **recoverability**.

## 7. Encrypted snapshot limits

Recovery may still fail because the key is disabled, the recovery role lacks decrypt permission, the snapshot is application-inconsistent, required metadata is absent, or the restore procedure has never been tested. Encryption protects confidentiality; it does not prove usability.

## 8. RPO/RTO statement

A defensible statement is: “The scheduled backup path targets at most one hour of committed Atlas data loss, subject to application-consistency limits; the latest controlled drill restored a valid result in 30 minutes in the sandbox.” Do not say the service has a guaranteed one-hour RPO or 30-minute RTO without repeated representative evidence and operational ownership.

## 9. Backup manifest

Include schema/version, source environment and release, consistency point, creation time, object/snapshot identifiers, file/object names, sizes, checksums, encryption/key reference, retention class, and producer identity. These fields allow independent selection and verification of the recovery artifact.

## 10. Empty restore

It proves the backup contains all required facts and avoids damaging the source. An in-place restore can succeed only because old files, configuration, credentials, or indexes remained. Empty recovery reveals hidden dependencies.

## 11. Protection mechanisms

Deletion protection adds an explicit API barrier. Versioning retains prior object versions. Lifecycle policy transitions or deletes data on schedule. Object immutability prevents changes/deletion under a retention rule. They have different threat models, costs, and cleanup consequences.

## 12. Public-edge proof

Resolve the intended hostname, connect to the returned edge, verify the certificate and hostname, submit a bounded job, poll its result, and record target/readiness evidence. Separately verify that the private host has no public address or internet ingress and that direct connection from the test origin fails.
