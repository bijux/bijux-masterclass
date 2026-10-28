# Compatibility and release evidence

The course carries four bundled release fixtures:

- `v1.0` is the prior public baseline;
- `v1.1` adds an operation and optional response metadata;
- `attempted-v1.2-breaking` changes an operation ID, removes a response, and narrows a string pattern;
- `v2.0` contains deliberate major changes and a migration document.

The built-in comparator is intentionally small and readable so learners can understand why a gate fired. `oasdiff` supplies a broader independent engine in the full proof route.

## Review stance

“Non-breaking” is not equivalent to “risk-free.” Adding an enum value may be producer-compatible but break exhaustive consumers. Adding optional response fields may fail closed decoders. Compatibility reports therefore preserve a review category instead of flattening every addition into automatic safety.

## Release rule

A minor release must not remove operations, responses, schemas, properties, or enum values; change stable operation IDs; add required fields; or tighten accepted values. A major version may contain a detected break only when the migration evidence is present and reviewed.
