# Backup, snapshot, replication, and archive

These mechanisms protect against different failures.

| Mechanism | Primary purpose | Does not prove |
|---|---|---|
| replica | availability and reduced loss for selected failures | historical recovery after corruption or deletion |
| snapshot | point-in-time storage copy | application consistency or independent retention |
| backup | catalogued, retained, integrity-checked recovery copy | fast failover unless designed for it |
| archive | long-term retention and retrieval | operational service recovery |
| disaster-recovery replica | recovery in another failure domain | protection from shared credentials or logical corruption |

A snapshot may be one component of a backup, but a backup adds inventory, dependency tracking, retention, integrity checks, keys, restore instructions, and independent ownership. Replication may copy an accidental deletion immediately. An archive may satisfy retention while being too slow for the service RTO.

## Selection questions

- Which failure is being addressed?
- What is the recovery point and how is it identified?
- Which credentials and keys are required?
- Can the mechanism survive cluster, region, or account loss?
- Has it been restored into an empty destination?
- Which application invariant proves usability?
- Who may delete the primary and recovery copies?

## Atlas rule

Atlas never uses the existence of a replica or a `readyToUse` snapshot as evidence that backup and recovery objectives are met. The claim requires an executed restore and application-level validation.
