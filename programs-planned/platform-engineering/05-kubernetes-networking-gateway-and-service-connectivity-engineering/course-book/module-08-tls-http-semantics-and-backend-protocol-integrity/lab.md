# Lab — Preserve TLS authority and idempotency through the Gateway

## Goal

Exercise real loopback TLS, hostname verification, forwarding-header replacement, backend failure, and retry classification.

## Safety boundary

Use the dependency-light model or an isolated disposable cluster. Do not alter shared load balancers, DNS zones, cloud routes, certificates, or production egress policy.

## Baseline

The local lab has a certificate for `atlas.test`, three backends, a trusted Gateway, and an idempotent analysis operation.

## Hypothesis

Wrong hostname must fail TLS; wrong HTTP authority must return 421; forged forwarding headers must be replaced; a backend disconnect must not trigger unsafe replay without idempotency evidence.

## Controlled action

Run `python3 capstone/scripts/tls_gateway_lab.py`. Execute the supplied good and bad clients and inspect request ledgers.

## Oracle

Exactly one logical analysis is created; certificate/authority failures are explicit; backend sees canonical forwarding data; retry decision records the remaining budget and idempotency basis.

## Required evidence

TLS transcript summary, certificate/SAN, HTTP authority, forwarded-header before/after, attempt ledger, logical effect count, and timeout budget.

## Interpretation

Connectivity success is rejected when it creates duplicate business effects or accepts the wrong authority.

## Cleanup

Run `make clean`; verify processes and generated PKI reports are removed.

## Completion gate

All security and semantic oracles pass, no process remains, and the report explains each independent trust decision.
