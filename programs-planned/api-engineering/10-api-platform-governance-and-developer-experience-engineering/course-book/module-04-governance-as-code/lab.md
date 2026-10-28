# Lab 04 — Turn a scorecard into an accountable decision

## Setup

Run `make policy-proof`. Inspect the policy pack, evidence ledger, exception
register, and scorecard code.

## Controlled action

Evaluate three candidates: an API with complete evidence, the RPC documentation
exception, and an API missing security evidence but strong scores elsewhere.
Then create an exception with no expiry.

## Oracle

The first passes, the second requires review, the security failure rejects, and
the expiry-free exception is invalid.

## Required evidence

Create `reports/module-04-governance-decision.json` with rule versions, evidence
IDs, decision, reviewer or next action, and exception expiry.

## Cleanup

Remove scratch evidence and exceptions.

## Completion gate

No blocker can be hidden by an average, and every non-pass outcome has an
accountable next action.
