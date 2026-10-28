# Exercises — Module 06: DNS, HTTP, TLS, and PKI

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — Resolver versus DNS

Why can `getent hosts` and `dig` return different answers?

## Exercise 2 — TTL planning

A record had TTL 86400 seconds. It is changed to TTL 60 and a new address at the same time. When can old answers persist?

## Exercise 3 — HTTP over TLS

What does a successful TLS handshake prove before the first HTTP byte?

## Exercise 4 — SAN matching

Why is a certificate with CN `atlas.test` but no SAN unsuitable for the course profile?

## Exercise 5 — IP SAN

A client connects to `127.0.0.1` while the certificate contains DNS SAN `127.0.0.1`. Should verification pass?

## Exercise 6 — SNI and Host

How can TLS select the correct certificate but HTTP still reject the request?

## Exercise 7 — Private CA risk

Why should the course CA not be installed system-wide?

## Exercise 8 — Rotation oracle

What observation proves the new certificate is actually served after reload?

## Exercise 9 — TLS version policy

Why does allowing TLS 1.3 not by itself establish secure TLS policy?

## Exercise 10 — Negative DNS caching

How can a recently created DNS record still appear nonexistent?

## Exercise 11 — Debug `-k`

What limited conclusion is justified when `curl -k` succeeds but verified curl fails?

## Exercise 12 — End-to-end evidence

List the evidence chain for a verified Atlas HTTPS readiness request.
