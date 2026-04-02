# Bundle Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  inspect["inspect bundle"] --> shape["Public shape review"]
  tour["tour bundle"] --> story["Walkthrough review"]
  verify["verify-report bundle"] --> proof["Executable proof review"]
```

```mermaid
flowchart LR
  question["What kind of saved review do you need?"] --> bundle["Choose the closest bundle"]
  bundle --> route["Read route.txt and bundle-manifest.json"]
  route --> compare["Compare outputs before reopening source"]
```
<!-- page-maps:end -->

Use this guide when the capstone's saved artifacts are useful but the directory-level
review story is still fuzzy. The goal is to make the three bundle routes feel like one
coherent proof shelf.

## Choose the bundle by review need

| If you need to review... | Choose this bundle | Do not start with |
| --- | --- | --- |
| public runtime shape without invocation | inspect bundle | verify-report bundle |
| one saved learner-facing story from manifest to trace | tour bundle | inspect bundle plus ad hoc commands |
| strongest saved executable confirmation | verify-report bundle | confirm output alone |

## Bundles at a glance

| Bundle | Built by | Best use |
| --- | --- | --- |
| inspect bundle | `make inspect` | review public manifest, registry, plugin, and signature shape without invocation |
| tour bundle | `make tour` | review one saved learner-facing route from public shape into concrete invocation and trace |
| verify-report bundle | `make verify-report` | review executable proof together with saved public-surface evidence |

## What the bundle manifest adds

Each bundle also includes `bundle-manifest.json`, which records:

- file paths
- file sizes
- SHA-256 hashes

That manifest is useful when you want to confirm exactly what the saved review route
produced without diffing every file manually.

Use `bundle-manifest.json` to review the saved inventory. Use the bundle's content files
to review the metaprogramming claim itself.

## Best companion guides

- read [INSPECTION_GUIDE.md](INSPECTION_GUIDE.md) when the inspect bundle is the right route but one artifact is still unclear
- read [WALKTHROUGH_GUIDE.md](WALKTHROUGH_GUIDE.md) when the tour bundle is the right route
- read [PROOF_GUIDE.md](PROOF_GUIDE.md) when the verify-report bundle is the right route
- read [REVIEW_ROUTE_MAP.md](REVIEW_ROUTE_MAP.md) when the bundle question is really a broader route-selection problem
- read [BUNDLE_MANIFEST_GUIDE.md](BUNDLE_MANIFEST_GUIDE.md) when the question is the exact saved inventory rather than the route choice

## Good stopping point

Stop when you can name which saved bundle matches the current review need and why the
other two bundles would be either weaker or unnecessarily heavy.
