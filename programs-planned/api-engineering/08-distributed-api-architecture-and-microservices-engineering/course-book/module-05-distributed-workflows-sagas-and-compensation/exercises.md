# Exercises — Distributed Workflows, Sagas, Compensation, and Process Managers

Answer before reading the worked answers. Every answer must name the governing invariant and decisive evidence.

## 1. Why is a saga not a distributed rollback transaction?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 2. Who should own the artifact completion process manager?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 3. What stable identity makes artifact storage idempotent?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 4. What happens when Artifact Service commits but the worker times out?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 5. Why must Control recheck the lease after issuing an upload capability?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 6. What is the compensation for a stale artifact?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 7. Why is Notification outside the run-completion saga?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 8. When is orchestration preferable to choreography?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 9. What makes a compensation idempotent?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 10. Why can a distributed mutex be weaker than a lease generation?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 11. When should a workflow be redesigned rather than wrapped in a saga?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 12. What requires manual review in a saga?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.
