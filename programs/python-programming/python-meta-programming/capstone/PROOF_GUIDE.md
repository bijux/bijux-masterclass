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

## Public-surface proof

After the CLI lands, run:

```bash
python -m incident_plugins.cli manifest --group delivery
python -m incident_plugins.cli invoke delivery console deliver --config prefix='[ops]' --arg title='CPU high' --arg severity='warning' --arg summary='node-1 crossed 90%'
```

These commands prove that the runtime shape and invocation path are inspectable without
opening private internals first.

## Review questions

- Which proof demonstrates definition-time behavior?
- Which proof demonstrates preserved callable metadata?
- Which proof demonstrates that the manifest stays observational rather than operational?
