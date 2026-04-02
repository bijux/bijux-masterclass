# Proof Guide

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph TD
  guide["Proof Guide"]
  unit["Pytest proof"]
  manifest["Manifest proof"]
  invoke["Invocation proof"]
  review["Review questions"]

  guide --> unit
  guide --> manifest
  guide --> invoke
  guide --> review
```

```mermaid
flowchart LR
  choose["Choose a claim"] --> command["Run the matching command"]
  command --> output["Inspect the output"]
  output --> source["Trace it back to source ownership"]
  source --> review["Record what the proof actually established"]
```
<!-- page-maps:end -->

This guide keeps the capstone honest by tying each public claim to one repeatable proof path.

## Base proof

Run:

```bash
make confirm
```

This runs the regression suite proving field validation, registry determinism, manifest
export, and runtime invocation behavior.

## Saved review routes

- `make inspect` writes the learner-facing inspection bundle.
- `make tour` writes the learner-facing walkthrough bundle.
- `make verify-report` writes executable proof together with public-surface evidence.

## Public-surface proof

Run the public proof surface:

```bash
make proof
```

Or run the CLI pieces individually:

```bash
make manifest
make registry
make demo
make trace
```

These commands prove that the runtime shape and invocation path are inspectable from the
public surface without opening private internals first.

## Honest distinctions

- `inspect` proves what the runtime exposes publicly before invocation.
- `tour` proves that a human can follow one complete public review route.
- `verify-report` proves that executable tests and public-surface evidence agree in one saved bundle.
- `confirm` proves the strongest local regression surface.
- `proof` publishes the full learner-facing review route.

## Review questions

- Which proof demonstrates definition-time behavior?
- Which proof demonstrates preserved callable metadata?
- Which proof demonstrates that the manifest stays observational rather than operational?
