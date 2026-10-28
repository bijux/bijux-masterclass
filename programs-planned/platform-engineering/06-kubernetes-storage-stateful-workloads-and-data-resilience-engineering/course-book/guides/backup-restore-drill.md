# Backup and restore drill guide

A restore drill should prove the complete service journey, not merely the backup tool.

## Prepare

- choose a named recovery point and failure tier;
- record RPO/RTO targets;
- create an empty destination with independent identity;
- confirm recovery credentials and encryption keys are not borrowed from the primary runtime;
- freeze the evidence set and assign operator roles;
- define abort conditions and cleanup.

## Execute

1. detect and declare the simulated loss;
2. select the recovery point from the catalogue;
3. provision destination capacity and network access;
4. retrieve and verify manifests and objects;
5. restore bytes and replay required logs;
6. start the application in isolation;
7. validate schema, generation, counts, checksums, tenancy, and critical workflows;
8. redirect test traffic;
9. record every phase duration;
10. decide whether the objective was met.

## Failure branches

Repeat selected drills with a missing object, unavailable key, corrupt manifest, insufficient quota, incompatible schema, and stale DNS. The process should fail closed and preserve the primary.

## Report

Publish the chosen point, actual data-loss window, actual phase timings, validation results, residual risk, remediation owners, and next drill date. A backup success log is not a restore report.
