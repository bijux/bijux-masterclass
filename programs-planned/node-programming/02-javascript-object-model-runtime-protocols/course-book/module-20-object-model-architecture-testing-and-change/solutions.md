# Module 20 Reasoned Solutions

## A. Runtime-object map

The essential separation is authority. A live node owns private node state but not graph membership. The atlas owns graph relations and traversal revision. The codec owns conversion but no live mutation. The store owns filesystem effects. A read view grants observation only. An iterator owns traversal state. An edit session owns one proposed change set and a terminal lifecycle. A proxy is only the draft interaction surface. A record is plain data with no live methods or brand.

Any design that gives the codec direct access to mutate an existing atlas or gives renderers full node mutation authority should be revised.

## B. Invariant-to-operation matrix

`add`, `move`, `remove`, and `clone` change graph invariants and structural revision. Attribute edits change value invariants and an attribute revision but need not change traversal structure. Persistence is coordinated by the application layer after a complete candidate exists. Read-only commands should not save.

If one command mutates a node, atlas map, root order, and file independently, there is no single commit authority. Candidate construction and one graph-level publication are the principled repair.

## C. Representation audit

Live representation uses private fields and validated identifiers. Persistence uses explicit plain fields and IDs. Custom inspection uses a bounded summary. CLI output is deterministic user text. Traversal exposes read-only views in documented order. Runtime metadata and caches are omitted from persistence. Child arrays are not returned mutably.

A strong answer explains why each surface exists rather than merely listing fields.

## D. Runtime compatibility review

A method-to-arrow-field change alters own keys, per-instance identity, extraction behavior, and potentially subclass overriding. Hiding an enumerable property breaks spread, key enumeration, and JSON assumptions. Changing default iteration order is breaking. Custom inspection changes are usually diagnostic and should not be parsed, but downstream snapshot tests may still need release notes. Numeric default conversion can silently change concatenation and equality and is breaking. Live-to-snapshot views change observation timing. Accepting nested mutable objects weakens the edit invariant. A private constructor with a stable public factory may be source-breaking for callers using `new` but can be migrated deliberately.

## E. Test-gap hunt

Final JSON output proves almost none of the runtime object contracts. Add direct descriptor inspection, counterfeit-brand tests, callback receiver tests, iterator state tests, every proxy mutation route, clone mapping and source-preservation tests, terminal lifecycle tests, protocol counterfeit tests, and construction-through-validation tests.

## F. Laboratory

A complete audit records identities, descriptors, protocols, and lifecycle before implementing the cross-layer feature. The registry must use plain data for storage and live branded instances for behavior.

## G. ObjectAtlas completion

The final evidence should make the architecture reviewable without reading every implementation line. Tests prove public claims; the invariant register explains why internal choices exist. The CLI process tests verify real ESM execution and exit status.

## H. Independent aliases change

Aliases belong to atlas-wide identity resolution, not only to a node field. The atlas owns uniqueness and lookup. Records carry canonical aliases. Clone policy must avoid collisions. Attribute proxy edits must not reach alias authority. Old V1 records receive an explicit empty-alias default or a version migration.

A weak repair stores an alias array in `AtlasNode` and searches all nodes on demand without uniqueness validation, canonical encoding, or error distinctions.

## I. Reconstruction standard

A complete defense uses each mechanism narrowly:

- descriptors for stable public ID and hidden metadata;
- prototypes for shared class methods;
- adapters for receiver-safe callbacks;
- private fields for node invariants;
- composition for graph, codec, store, and rendering authority;
- symbols for conversion, iteration, and debugging protocols;
- generators for deterministic traversal;
- proxies only for plain draft interaction;
- weak maps only for optional derived caches;
- disposal for edit-session terminal cleanup.

The smallest correct architecture is not the one with the fewest files or features. It is the one with no redundant mechanism and no missing authority boundary.
