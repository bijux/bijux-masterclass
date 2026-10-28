# Exercises — Secrets, credentials, artifact trust, and policy gates

Answer each problem before reading the worked solutions. A complete answer names the owner of the relevant transition, the failure that invalidates the attractive shortcut, and the evidence that would settle the decision.

## 1. Why is a Kubernetes Secret not necessarily the source of secret truth?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 2. What is the main authority trade-off of decrypting SOPS data inside the GitOps controller?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 3. Why can an ExternalSecret be Ready while the application still uses an old credential?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 4. Why should image automation write credentials differ from source read credentials?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 5. What does a valid artifact signature fail to prove?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 6. Why are policy gates needed at more than one layer?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 7. What does `not-executed` communicate?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 8. Why is secret rotation a release process?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 9. How can rendered-manifest caching leak secrets?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 10. Why should a migration Job not receive the database owner credential?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 11. How can admission mutation create a GitOps loop?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 12. Design a policy result for a candidate whose artifact signature passes but native cluster admission was unavailable.

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.
