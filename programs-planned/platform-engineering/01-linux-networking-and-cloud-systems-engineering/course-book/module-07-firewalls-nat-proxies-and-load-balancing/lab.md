# Lab — Module 07: Firewalls, NAT, Proxies, and Load Balancing

## Goal

Prove trusted proxy identity, bounded backend failure, and a least-privilege host traffic policy.

## Safety boundary

Do not load the nftables fixture on a remote or shared host. Use syntax check by default; live loading requires a disposable VM, console, and automatic rollback.

## Baseline

Run the capstone tour, inspect the edge and API listeners, and syntax-check `atlas.nft` when nft is available.

## Hypothesis

Client forwarding headers are discarded; only the edge creates derived client context; backend loss produces bounded 503; unsafe requests are not retried.

## Controlled action

Send spoofed forwarding fields, stop the API backend, issue GET and POST requests, and inspect attempt counts. In a VM, load a narrowed firewall policy with a rollback timer and test allowed/denied flows.

## Oracle

Spoofed identity is absent, GET attempts are bounded, POST has one attempt, the edge returns 503, and firewall results match the declared flow matrix.

## Evidence

Raw request, edge/API events, backend attempt count, response status, nft syntax/ruleset, and source-specific connection tests.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Restore backend, remove temporary firewall policy or restore snapshot, cancel rollback timer only after verified management access, and rerun the tour.

## Completion gate

Defend the trust transition from direct peer address to derived client context.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
