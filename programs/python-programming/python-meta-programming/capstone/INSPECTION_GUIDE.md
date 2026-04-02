# Inspection Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  inspect["inspect"] --> manifest["manifest.json"]
  inspect --> registry["registry.json"]
  manifest --> schema["Schema and action metadata"]
  registry --> names["Registered plugin names"]
  schema --> review["Review ownership and observability"]
  names --> review
```

```mermaid
flowchart LR
  question["Choose the inspection question"] --> route["Run the inspect bundle route"]
  route --> output["Read the saved bundle files"]
  output --> source["Name the owning source file"]
  source --> next["Decide whether you need trace, tests, or proof next"]
```
<!-- page-maps:end -->

Use this guide when you want to inspect what the runtime exposes without immediately
executing one plugin action. The goal is to make manifest and registry review explicit
instead of letting them blur into invocation proof.

## Which output answers which question

| Output | Best question |
| --- | --- |
| `manifest.json` | what field and action metadata are publicly visible |
| `registry.json` | which concrete plugins are actually registered |
| `route.txt` | what to read next in the saved review order |
| `manifest.json` in the bundle manifest | whether the saved bundle inventory is complete and stable |

## Recommended reading order

1. Run `make inspect`.
2. Read `manifest.json`.
3. Read `registry.json`.
4. Read `route.txt`.
5. Follow the linked local guides only after you can state what the public surface shows.

## What this route should teach

- the manifest is observational metadata, not a hidden invocation channel
- the registry is a runtime fact you can inspect directly rather than infer from imports
- public inspection can stay useful even before you know every internal class and hook

## Best follow-up choices

- Go to `TARGET_GUIDE.md` when you need the next smallest command.
- Go to `WALKTHROUGH_GUIDE.md` when you need one concrete invocation story.
- Go to `TEST_GUIDE.md` when you need precise executable proof for a claim the bundle only suggests.
- Go to `PROOF_GUIDE.md` when you need the strongest review route.

## What this guide prevents

- mistaking manifest output for proof of successful invocation
- treating registry state as if it were enough to justify the full runtime design
- opening framework internals before you can explain the public inspection surface
