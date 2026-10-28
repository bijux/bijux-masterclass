# Lab — Turn a scorecard into an accountable decision

> **Module 04:** Governance as Code, Evidence, Scorecards, and Exceptions

## Objective

Publish the policy pack, evidence ledger, exception register, and release scorecards.

## Why this lab matters

This lab turns the module’s governing question—**How can governance scale without becoming either a rubber stamp or a centralized release bottleneck?**—into a falsifiable experiment. Policy changes are contracts with API owners. Version the policy pack, publish a changelog, test it against known fixtures, and provide a way to reproduce the decision locally. A centralized rule that changes unpredictably creates release instability. Governance as code is valuable because it can be reviewed and replayed, not because code is automatically objective.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the policy pack, evidence ledger, exception register, and release scorecards**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make policy-proof`. Inspect the policy pack, evidence ledger, exception
register, and scorecard code.

## Hypothesis

The clean implementation should satisfy this claim: **The first passes, the second requires review, the security failure rejects, and the expiry-free exception is invalid.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Evaluate three candidates: an API with complete evidence, the RPC documentation
exception, and an API missing security evidence but strong scores elsewhere.
Then create an exception with no expiry.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish the policy pack, evidence ledger, exception register, and release scorecards**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The first passes, the second requires review, the security failure rejects, and
the expiry-free exception is invalid.

## Required evidence

Create `reports/module-04-governance-decision.json` with rule versions, evidence
IDs, decision, reviewer or next action, and exception expiry.

## Interpretation and defense

1. Which state or effect is authoritative for **Governance as Code, Evidence, Scorecards, and Exceptions**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove scratch evidence and exceptions.

## Completion gate

No blocker can be hidden by an average, and every non-pass outcome has an
accountable next action.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Governance as Code, Evidence, Scorecards, and Exceptions**. A green command without the negative case and causal explanation does not satisfy this gate.
