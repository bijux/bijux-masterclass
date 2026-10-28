# Evolvable Client SDK

## The product

Build a client-side model that reads two explicit user-response versions:

```text
USER_V1: id + name
USER_V2: id + displayName + tags
```

The SDK validates both, migrates V1 to V2, and retains a deprecated compatibility helper. Unknown future versions are rejected rather than structurally treated as current data.

Read [Module 29](../../course-book/module-29-api-compatibility-semver-and-migration/index.md) first.

## Public contract

Expose `UserV1`, `UserV2`, `UserResponse`, `parseUser`, `migrateUser`, and the deprecated `displayName`. Migration must preserve the modeled name and establish an explicit default for tags. It must not mutate the old record.

Keep an old V1 fixture permanently. The test suite should represent old callers, old stored data, and current callers as separate compatibility evidence.

## Milestones

1. Define version-discriminated records.
2. Validate unknown runtime input without structural assertions.
3. Implement semantic V1-to-V2 migration.
4. Preserve the old display helper with a deprecation tag.
5. Add fixtures for both versions and malformed future data.
6. Add an exhaustive consumer and observe the effect of a hypothetical V3 member.
7. Inspect declaration changes across a candidate modification.
8. Write release notes for one intentionally breaking change.

## Adversarial cases

Test missing fields, wrong tag types, unknown versions, extra fields under your chosen policy, and information that cannot be represented in V2. Compare reject, preserve, and opaque pass-through policies for future versions.

Do not widen `format` to `string` to make future values compile. That deletes the negotiation boundary.

## Design record

Classify proposed changes across:

- source calls;
- type inference;
- declarations;
- runtime behavior;
- exhaustive consumers;
- package paths;
- error codes;
- stored data.

State when adding an optional field is still behaviorally breaking because strict validation or exact snapshots change.

## Independent transfer

Version a configuration, protocol response, or persisted command. Include one migration with a nontrivial default and one unknown-version policy.

## Completion standard

The SDK must make old support explicit through types, validators, fixtures, adapters, and documentation. “The objects are structurally similar” is not a migration policy.
