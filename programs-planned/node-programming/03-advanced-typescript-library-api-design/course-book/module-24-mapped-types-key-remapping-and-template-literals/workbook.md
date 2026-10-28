# Module 24 Workbook

Write the input key set, output key set, modifier rule, and runtime counterpart before writing each type.

## A. Modifier transformations

Create:

- `Mutable<T>`;
- `RequiredReadonly<T>`;
- `OptionalMutable<T>`.

Test them on a model containing readonly, optional, and required fields. Explain why `Partial<T>` may be an invalid domain update type.

## B. Key filtering

Derive the keys whose values are strings, then produce an object containing only those properties. Decide how optional string properties and `string | number` properties behave.

## C. Event surface

For:

```ts
interface Settings {
  theme: 'dark' | 'light';
  retries: number;
  enabled: boolean;
}
```

Derive `themeChanged`, `retriesChanged`, and `enabledChanged` handlers with correct next/previous value types. Then design the runtime map that makes registration and dispatch truthful.

## D. Growth budget

Calculate the number of members produced by:

```ts
type Scope = 'user' | 'team' | 'org' | 'system';
type Action = 'read' | 'write' | 'delete' | 'share' | 'audit';
type Result = 'started' | 'succeeded' | 'failed';
type Event = `${Scope}:${Action}:${Result}`;
```

Decide whether the completion surface is useful or excessive.

## E. Object schema output

Implement `OptionalKeys`, `RequiredKeys`, and `ObjectOutput`. Add type tests for missing optional keys, present valid keys, present `undefined`, and unknown keys.

## F. Independent laboratory

Complete [Typed Change Event Surface](../../labs/module-24-typed-change-event-surface/README.md). The runtime implementation must not cast arbitrary strings into generated names.

## G. SchemaKit transfer

Add object schemas with:

- own-key checks;
- required/optional runtime policy;
- unknown-key reject/strip policy;
- mapped static output;
- path-aware issues;
- canonical declaration output.

## H. Review a clever type

Find or create one recursive/template helper. Document its domain, generated size, runtime relation, emitted declaration, and a simpler alternative. Remove it if the explanation is weaker than the explicit type.

## I. Reconstruction

Explain mapped modifiers, key remapping, template cross products, optional-key inference, and runtime alignment using one event example and one SchemaKit example.

## I. Modifier audit

Given a source model with readonly, required, and optional fields, derive four views: editable draft, persisted snapshot, patch, and validation-error map. For every mapped modifier, explain whether it adds or removes caller capability.

## J. Remapping collision

Design a normalizer that converts `user_id`, `user-id`, and `userId` to one camel-case key. Show how two source keys can collide. Decide whether the type and runtime should reject, combine, or select one value. Add an adversarial collision test.

## K. Event-family derivation

Derive event names and payloads from a model containing string and symbol keys. Exclude unsupported keys explicitly. Then add an event whose payload depends on both previous and current values and prove the relationship with a type test.

## L. Combinatorial budget

Estimate the size of a template-literal union built from 12 resources, 8 actions, and 4 phases. Decide which dimensions deserve static completion and which should be runtime data. State the declaration and editor cost you are avoiding.

## M. Runtime alignment

Implement the Typed Change Event Surface so one runtime key constructs the name, previous value, current value, and listener lookup. Identify the single localized assertion and write the invariant that justifies it.

## N. Declaration inspection

Emit declarations for the change-event family and inspect what a consumer sees. If the public declaration expands into an unreadable union, introduce one or two named aliases without weakening the relation. Compare declaration readability before and after.

## O. Independent remapping problem

Derive environment-variable names from a nested configuration model, but stop before generating arbitrary deep paths. Define the finite level you support, collision policy, separator, casing rule, and runtime conversion. Explain why a generic “all possible property paths” type is not automatically the better public API.
