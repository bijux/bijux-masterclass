# Reference — Patch semantics

JSON Patch is an ordered list of path operations and is sensitive to array position. JSON Merge Patch replaces arrays. Strategic merge uses Kubernetes merge metadata and named keys where supported. Server-Side Apply merges declarative field ownership rather than applying a source patch.

Choose the mechanism according to schema, identity, and ownership. Always review the complete rendered object. A syntactically successful patch can remove sidecars, change selectors, or transfer authority.

## Extended reader notes

Patch mechanisms answer different questions. A strategic merge can merge list entries using Kubernetes schema metadata such as container `name`. A JSON merge patch replaces arrays as values. JSON Patch applies ordered operations to precise paths and is sensitive to list positions. Server-Side Apply computes structured field ownership rather than merely transforming local text.

Choose a patch form by the invariant you need. Use an explicit JSON Patch when removing one element or testing a precondition. Use schema-aware merge when extending named containers or environment entries. Prefer a full resource in an overlay when the patch would be harder to understand than the resulting object. Avoid patches that rely on undocumented list ordering.

Review must show the rendered object and the selected patch semantics. Tests should include the predecessor shape because a patch can succeed against one base and silently change meaning after a base upgrade. Native Kustomize proof remains necessary for transformations beyond the course semantic lane.
