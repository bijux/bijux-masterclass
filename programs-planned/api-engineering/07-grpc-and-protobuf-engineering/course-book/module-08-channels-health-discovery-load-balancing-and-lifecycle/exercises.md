# Exercises — Module 08: Channels, Health, Discovery, Load Balancing, and Lifecycle

Work through all twelve problems before opening the answers. In **Channels, Health, Discovery, Load Balancing, and Lifecycle**, every response must settle this question: **How do clients and servers manage long-lived channels, instance health, name resolution, load balancing, startup, draining, and shutdown without hiding failure or losing active work?** Use the cumulative platform, not an invented toy system. Preserve inherited guarantees and make every new assumption explicit and falsifiable.

## 1. Why should a gRPC channel normally outlive one call?

Write a concise engineering answer and name the decisive proof.

## 2. Differentiate liveness, readiness, and gRPC serving status.

Write a concise engineering answer and name the decisive proof.

## 3. What does a resolver do, and what does a load-balancing policy do?

Write a concise engineering answer and name the decisive proof.

## 4. Why can round-robin expose an in-memory idempotency defect?

Write a concise engineering answer and name the decisive proof.

## 5. When should a server report NOT_SERVING during graceful shutdown?

Write a concise engineering answer and name the decisive proof.

## 6. Why is keepalive not an application lease or heartbeat?

Write a concise engineering answer and name the decisive proof.

## 7. What risk comes from synchronized maximum connection age?

Write a concise engineering answer and name the decisive proof.

## 8. Why should applications not poll channel READY state before every call?

Write a concise engineering answer and name the decisive proof.

## 9. Describe shutdown behavior for an active UploadDataset stream.

Write a concise engineering answer and name the decisive proof.

## 10. How should a worker stream recover after its server instance disappears?

Write a concise engineering answer and name the decisive proof.

## 11. When is server reflection appropriate?

Write a concise engineering answer and name the decisive proof.

## 12. Define a two-instance proof that reveals hidden local state.

Write a concise engineering answer and name the decisive proof.
