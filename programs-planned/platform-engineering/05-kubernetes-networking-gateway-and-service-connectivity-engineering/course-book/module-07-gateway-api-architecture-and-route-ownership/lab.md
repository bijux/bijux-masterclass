# Lab — Resolve a route attachment conflict

## Goal

Diagnose a Route that exists and has valid backends but cannot attach safely to the intended listener.

## Safety boundary

Use the dependency-light model or an isolated disposable cluster. Do not alter shared load balancers, DNS zones, cloud routes, certificates, or production egress policy.

## Baseline

A platform Gateway accepts Routes only from labelled namespaces and serves one HTTPS hostname. Atlas HTTPRoute initially attaches and routes correctly.

## Hypothesis

A conflicting namespace and hostname policy will produce explicit attachment or hostname failure; a planted broad-listener mutant will incorrectly accept it.

## Controlled action

Run `python3 capstone/scripts/gateway_attachment_lab.py` and inspect parent/listener/hostname/reference decisions.

## Oracle

The safe model rejects the unauthorized attachment with a precise reason and preserves Atlas routing. The broad-listener mutant is rejected by release policy.

## Required evidence

Gateway, listener, Route, ReferenceGrant, candidate match set, conditions with observed generation, and selected/rejected reasons.

## Interpretation

A correct diagnosis distinguishes route validity from attachment authority and from data-plane reachability.

## Cleanup

Run `make clean`; remove generated Gateway reports.

## Completion gate

The authorized Route remains programmed, unauthorized attachment is rejected, and the explanation identifies the target owner that must grant any cross-namespace reference.
