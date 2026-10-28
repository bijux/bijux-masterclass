# Exercises — Module 07: Firewalls, NAT, Proxies, and Load Balancing

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — Firewall versus authentication

Why does allowing only a private source prefix not authenticate an Atlas user?

## Exercise 2 — Established traffic

Why does a stateful input policy usually accept `established,related` before new-flow rules?

## Exercise 3 — ICMP policy

Give one IPv4 and one IPv6 function harmed by blocking all ICMP.

## Exercise 4 — NAT scope

What information is lost when many clients pass through source NAT?

## Exercise 5 — Forwarded spoof

How does the Atlas edge prevent a client from claiming `X-Forwarded-For: 10.0.0.1`?

## Exercise 6 — Safe retry

Why may the edge try another backend for GET but not POST /jobs?

## Exercise 7 — Health depth

Compare TCP connect, `/health/live`, and `/health/ready` checks.

## Exercise 8 — Drain sequence

A backend is being replaced. What is the safe order?

## Exercise 9 — Forward versus reverse proxy

Which side does each proxy represent and what new trust does it introduce?

## Exercise 10 — L4 versus L7

When is an L4 load balancer insufficient for a routing requirement?

## Exercise 11 — Firewall rollout

Why is `nft -c` insufficient before loading a remote-host policy?

## Exercise 12 — 503 proof

What evidence shows backend failure was bounded rather than amplified?
