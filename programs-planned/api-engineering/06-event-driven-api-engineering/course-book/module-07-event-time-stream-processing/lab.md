# Lab — Build a revisioned event-time analytics stream

> **Module 07:** Event-Time Stream Processing, Windows, Watermarks, and Corrections

## Objective

Process out-of-order, duplicated, late, and corrected run events into deterministic tumbling windows with explicit revisions and late-event evidence.

## Why this lab matters

This lab turns the module’s governing question—**How do event time, processing time, windows, watermarks, lateness, and corrections affect derived results?**—into a falsifiable experiment. A too-late event, corrected source event, or discovered processing defect may require recomputation. Corrections are versioned outputs with reason and source evidence. Rewriting a previously published aggregate without revision makes downstream state impossible to audit.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Load `capstone/stream-processing/window-policy.yaml`.
2. Prepare two five-minute windows across at least two tenants.
3. Include completed, failed, duplicate, late-within-policy, and too-late events.
4. Record expected results in `work/module-07/expected-windows.json`.
5. Use fixed UTC times; do not use the system clock.

## Hypothesis

The clean implementation should satisfy this claim: **Both correct runs converge on the same final windows and revisions. The accepted late event changes exactly one window, the duplicate changes none, and the too-late event enters a durable late record. Planted processing-time and no-dedupe implementations fail their expected oracles.** When the lab introduces this fault—**Plant a processing-time implementation and show that replay moves historical events into the wrong window**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Process the fixture once in publication order and once in a shuffled processing order that preserves event
identity. Advance the watermark, emit initial results, then deliver a late accepted event and require a
higher revision. Deliver a duplicate and a too-late event.

Plant a processing-time implementation and show that replay moves historical events into the wrong window.
Plant a no-dedupe implementation and show inflated count/duration.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a processing-time implementation and show that replay moves historical events into the wrong window**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Process out-of-order, duplicated, late, and corrected run events into deterministic tumbling windows with explicit revisions and late-event evidence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **Event-Time Stream Processing, Windows, Watermarks, and Corrections**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a processing-time implementation and show that replay moves historical events into the wrong window** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove planted processors, reset window and dedupe state, restore the policy version, and retain only
deterministic fixtures and reports. Confirm no local-time assumptions remain.

## Completion gate

The lab passes only when event-time semantics, watermark, lateness, dedupe, revision, and correction paths
are explicit and cross-language results agree for the shared vectors.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Event-Time Stream Processing, Windows, Watermarks, and Corrections**. A green command without the negative case and causal explanation does not satisfy this gate.
