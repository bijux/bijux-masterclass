# Exercises — Module 05: Distributed Workflows, Sagas, Compensation, and Process Managers

Work through all twelve problems before opening the answers. In **Distributed Workflows, Sagas, Compensation, and Process Managers**, every response must settle this question: **How do we preserve business intent when one workflow crosses services that cannot share a transaction?** A useful solution connects semantics to mechanism: who owns the decision, what can go wrong, and which retained artifact proves the claimed outcome.

## 1. Why is a saga not a distributed rollback transaction?


## 2. Who should own the artifact completion process manager?


## 3. What stable identity makes artifact storage idempotent?


## 4. What happens when Artifact Service commits but the worker times out?


## 5. Why must Control recheck the lease after issuing an upload capability?


## 6. What is the compensation for a stale artifact?


## 7. Why is Notification outside the run-completion saga?


## 8. When is orchestration preferable to choreography?


## 9. What makes a compensation idempotent?


## 10. Why can a distributed mutex be weaker than a lease generation?


## 11. When should a workflow be redesigned rather than wrapped in a saga?


## 12. What requires manual review in a saga?

