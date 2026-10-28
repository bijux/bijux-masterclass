# Lab — Reject DNS rebinding and unsafe redirects

## Goal

Apply outbound destination policy at resolution, connection, and redirect boundaries.

## Safety boundary

Use the dependency-light model or an isolated disposable cluster. Do not alter shared load balancers, DNS zones, cloud routes, certificates, or production egress policy.

## Baseline

The approved update service resolves to a public fixture address and returns a safe response. The policy rejects loopback, link-local, private, multicast, and reserved destinations unless explicitly approved.

## Hypothesis

A rebinding/redirect mutant will pass a name-only check but connect to a forbidden address. Peer validation and redirect revalidation will reject it.

## Controlled action

Run `python3 capstone/scripts/egress_policy_lab.py` against safe, mixed-answer, rebinding, and redirect fixtures.

## Oracle

Only the stable public destination succeeds. Mixed or changed peers and forbidden redirects fail before credentials or request bodies are forwarded.

## Required evidence

DNS answer set, pinned connection address, TLS hostname, connected peer, redirect chain, policy decision, and credential-forwarding decision.

## Interpretation

NetworkPolicy can be one independent barrier, but the lab proves why endpoint validation must survive resolver and redirect changes.

## Cleanup

Run `make clean`; remove generated egress reports and stop fixture servers.

## Completion gate

Every forbidden address class and authority-changing redirect is rejected, the safe dependency succeeds, and no fixture process remains.
