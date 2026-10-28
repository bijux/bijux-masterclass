# SchemaKit

SchemaKit is the cumulative product for **Advanced TypeScript and Library API Design**. It validates unknown values at runtime and derives precise TypeScript outputs from the same schema values.

The library deliberately separates four contracts:

1. **runtime acceptance** — which unknown values become trusted outputs;
2. **static inference** — which output type corresponds to each schema;
3. **package surface** — which entry points and declarations consumers may rely on;
4. **compatibility** — which changes preserve existing runtime and type-level behavior.

## Public entry points

```ts
import {
  array,
  boolean,
  Infer,
  literal,
  number,
  object,
  optional,
  string,
} from '@bijux-masterclass/schemakit';

import { parseJson } from '@bijux-masterclass/schemakit/json';
import { expectFailure, expectSuccess } from '@bijux-masterclass/schemakit/testing';
```

## Example

```ts
const User = object({
  format: literal('USER_V1'),
  name: string(),
  age: optional(number()),
});

type User = Infer<typeof User>;
const user = User.parse(JSON.parse('{"format":"USER_V1","name":"Ada"}'));
```

## CLI

```text
schemakit check <project.json>
schemakit normalize <input.json> <output.json>
schemakit example
schemakit help
schemakit version
```

The final independent extension is `discriminatedUnion(key, variants)`. It is intentionally not present in the reference product: the course requires the reader to add it through runtime, type, declaration, package, test, documentation, and compatibility surfaces.
