# Checkpoint — Module 10: Security Operations and Incident Response

## Required result

Course 3 ends with security profile 1.0, migrations 006–007, and a closed compromise exercise.

## Demonstrate

- Design actionable security events and audit records.
- Revoke tokens and API keys deliberately.
- Rotate webhook and signing keys with overlap.
- Preserve timelines and confidence levels.
- Update threats, controls, and tests after the incident.

## Commands

```bash
make module-proof MODULE=10 TRACK=python
make module-proof MODULE=10 TRACK=typescript
make core-proof
```

## Defend the design

1. Answer the central question: **When a credential, key, or dependency is compromised, how do we contain the event without destroying evidence or breaking the API?**
2. Demonstrate this capstone result: Course 3 ends with security profile 1.0, migrations 006–007, and a closed compromise exercise.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: revocation, key overlap, evidence preservation, compatible release, verification, and threat-model revision form one controlled timeline.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Course 3 ends with security profile 1.0, migrations 006–007, and a closed compromise exercise.—all focused checks pass, the **Security Operations and Incident Response** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
