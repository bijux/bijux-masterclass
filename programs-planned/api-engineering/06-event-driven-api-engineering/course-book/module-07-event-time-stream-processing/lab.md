# Lab — Build a revisioned event-time analytics stream

## Objective

Process out-of-order, duplicated, late, and corrected run events into deterministic tumbling windows with explicit revisions and late-event evidence.

## Setup conditions


1. Load `capstone/stream-processing/window-policy.yaml`.
2. Prepare two five-minute windows across at least two tenants.
3. Include completed, failed, duplicate, late-within-policy, and too-late events.
4. Record expected results in `work/module-07/expected-windows.json`.
5. Use fixed UTC times; do not use the system clock.


## Failure action and investigation


Process the fixture once in publication order and once in a shuffled processing order that preserves event
identity. Advance the watermark, emit initial results, then deliver a late accepted event and require a
higher revision. Deliver a duplicate and a too-late event.

Plant a processing-time implementation and show that replay moves historical events into the wrong window.
Plant a no-dedupe implementation and show inflated count/duration.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How do event time, processing time, windows, watermarks, lateness, and corrections affect derived results?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine. A passing command without this causal explanation is insufficient.

## Operational oracle


Both correct runs converge on the same final windows and revisions. The accepted late event changes exactly
one window, the duplicate changes none, and the too-late event enters a durable late record. Planted
processing-time and no-dedupe implementations fail their expected oracles.


## Required evidence


- `work/module-07/expected-windows.json`
- ordered and shuffled processing reports
- watermark and revision trace
- late-event records
- planted-defect failures
- checkpoint/output failure-window design
- output from `make stream-proof`


## Cleanup and reset


Remove planted processors, reset window and dedupe state, restore the policy version, and retain only
deterministic fixtures and reports. Confirm no local-time assumptions remain.


## Completion gate


The lab passes only when event-time semantics, watermark, lateness, dedupe, revision, and correction paths
are explicit and cross-language results agree for the shared vectors.
