# Exercises — Module 10: Production Host Engineering and Final Defense

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — Release unit

Why must service units and firewall/TLS configuration be versioned with application code?

## Exercise 2 — Readiness fault

Durable state becomes read-only while GET /health/live remains 200. What should readiness do?

## Exercise 3 — Rollback boundary

Give an example of a host change that makes simple code rollback unsafe.

## Exercise 4 — Patch strategy

When is in-place patching defensible compared with image replacement?

## Exercise 5 — Log truth

Why can structured logs not be the authoritative job state?

## Exercise 6 — Restore time

One restore completed in 90 seconds. Can Atlas claim RTO 90 seconds?

## Exercise 7 — Game-day abort

Name conditions that should stop a privileged host game day immediately.

## Exercise 8 — Runbook quality

Why is “restart atlas-worker” an inadequate recovery runbook?

## Exercise 9 — Manifest meaning

What does the course SHA-256 manifest prove and not prove?

## Exercise 10 — Cloud evidence

Why can the local Atlas tour not prove zone-failure tolerance?

## Exercise 11 — Final causal path

Trace one successful job from DNS name to durable result and name each owner.

## Exercise 12 — Course 2 readiness

What must be true before infrastructure as code can begin without rediscovering requirements?
