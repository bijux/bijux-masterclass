# Lab — Module 06: DNS, HTTP, TLS, and PKI

## Goal

Build and verify a local trust chain, then diagnose name, trust, and expiry failures without disabling verification.

## Safety boundary

Do not install the course CA into a system trust store. Use only the fixture client CA argument and disposable certificate files.

## Baseline

Run `make pki-proof` and a verified Atlas HTTPS readiness request. Record the served certificate fingerprint and SANs.

## Hypothesis

The correct name and CA succeed; wrong name, missing CA, and an expired fixture fail before any valid HTTP application response.

## Controlled action

Use `openssl s_client` and the Python client for the correct name. Repeat with wrong SNI/Host, without the CA, and with an expired or not-yet-valid test certificate. Rotate to a new leaf and verify the served fingerprint.

## Oracle

Each failure is classified as DNS, TCP, TLS chain, validity, hostname, or HTTP host policy. No repair uses `-k` or an unverified context.

## Evidence

Resolver output, `s_client -verify_return_error`, certificate details, client error, edge logs, and pre/post rotation fingerprint.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Restore the original fixture, stop the edge, and remove only generated temporary keys and certificates.

## Completion gate

Trace the exact point at which a failed TLS verification prevents HTTP from existing.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
