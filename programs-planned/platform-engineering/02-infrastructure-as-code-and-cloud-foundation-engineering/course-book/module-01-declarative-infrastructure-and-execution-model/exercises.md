# Exercises — Declarative Infrastructure and the Execution Model

Answer before reading the solutions.

## 1. Existing remote bucket, absent state

Configuration declares an S3 bucket, state contains no bucket at that address, and the bucket already exists remotely. What plan should you expect and why is “OpenTofu will notice it” unsafe?

## 2. Renaming a resource

Explain why renaming a resource block can destroy infrastructure even when every argument remains identical.

## 3. `count` identity shift

A module creates subnets from `count` over a list. What change can shift identities, and how would you migrate safely to `for_each`?

## 4. `depends_on`

When is `depends_on` appropriate, and what harm can a broad dependency cause?

## 5. Same commit, different plan

Give two reasons that the same Git commit can produce a different plan on different days.

## 6. Unknown security values

Why should a security policy treat some unknown values as review blockers rather than accepting them as future details?

## 7. Provider meaning

What does a provider version contribute to the meaning of a plan?

## 8. Saved plan

Compare a freshly calculated apply with applying a saved plan. Which race does the saved plan reduce, and which races remain?

## 9. Limits of `prevent_destroy`

Why does `prevent_destroy` not fully protect a durable object?

## 10. `ignore_changes`

Give a legitimate and an illegitimate use of `ignore_changes`.

## 11. Successful apply, unhealthy target

An apply reports success but the load-balancer target is unhealthy. Is the infrastructure correct? State the evidence still required.

## 12. Plan identity record

Design the minimum identity record that lets a second operator determine exactly what a saved plan refers to.
