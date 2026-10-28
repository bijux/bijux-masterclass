# Worked answers — Lifecycle, Compatibility, Deprecation, and Retirement

## 1. Why is deprecation not a documentation annotation?

It is a managed change involving replacement, consumers, notice, migration, runtime traffic, support, and retirement evidence. An annotation can communicate state but cannot perform the workflow.

## 2. What is the difference between deprecated and retired?

Deprecated remains available but is no longer recommended and has an exit plan. Retired is no longer available for normal use and has completed runtime removal and archival obligations.

## 3. Why track actual consumers?

Without consumer identity, version, criticality, and last use, notice is guesswork. Consumer evidence determines impact and whether retirement is safe.

## 4. Can zero traffic prove zero consumers?

No. Telemetry can be incomplete, seasonal consumers may be idle, and offline generated clients may exist. Combine registration, runtime evidence, support records, and owner attestation.

## 5. What should a migration guide include?

Behavioral differences, contract changes, code or configuration actions, test evidence, timeline, rollback considerations, and a clear way to report completion.

## 6. When may an emergency shorten notice?

Only under an explicit security or safety incident with impact analysis, authorized risk acceptance, consumer communication, and a documented replacement or containment route.

## 7. Why retain retired contract artifacts?

Historical clients, incidents, audits, and data interpretation may depend on the old semantics. Retirement removes support and runtime availability, not history.

## 8. What is a blocking consumer?

A consumer whose criticality, migration status, or approved exception means retirement would cause unacceptable harm. The definition must be policy-driven, not improvised at the meeting.

## 9. How should unknown consumers affect retirement?

Treat them as uncertainty requiring investigation or risk acceptance. Unknown does not equal safe.

## 10. Why version lifecycle policy?

Notice periods, evidence requirements, and transition authority can change. A versioned policy explains which rules governed a past decision.

## 11. Who approves retirement?

The API owner proposes; affected consumers confirm or are handled through policy; platform verifies evidence and runtime plan; the designated governance or risk authority approves according to criticality.

## 12. What is the retirement of Analysis HTTP 1.1 currently blocked by?

`consumer-legacy-cli` still reports active production use and migration is only scheduled. The replacement exists, but consumer completion evidence does not.
