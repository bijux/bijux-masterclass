# Exercises — Helm chart engineering, packaging, and upgrade semantics

Answer each problem before reading the worked solutions. A complete answer names the owner of the relevant transition, the failure that invalidates the attractive shortcut, and the evidence that would settle the decision.

## 1. Why are Helm values a public API?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 2. Why should a chart not expose the complete Deployment spec as values?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 3. What does `values.schema.json` prove and not prove?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 4. Why are live-cluster lookups in a production template problematic?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 5. Why should a database not usually be a dependency of an application chart?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 6. What special lifecycle issue do CRDs create?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 7. Why is a pre-upgrade hook an unsafe place for an opaque migration?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 8. What can `--atomic` roll back, and what can it not roll back?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 9. Why should promotion record both chart digest and rendered-set digest?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 10. How does Argo CD Helm integration differ conceptually from Flux HelmRelease?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 11. What should an upgrade fixture contain?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.

## 12. Why can a repackaged chart with unchanged templates require new evidence?

Write a technically precise answer. Include a counterexample or failure path where it changes the decision.
