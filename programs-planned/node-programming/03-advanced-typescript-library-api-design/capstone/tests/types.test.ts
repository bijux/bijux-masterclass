import { literal, number, object, optional, string, tuple, type Infer } from '../src/index.js';
import type { Equal, Expect } from '../src/testing.js';

const User = object({ format: literal('USER_V1'), name: string(), age: optional(number()) });
type User = Infer<typeof User>;
export type UserContract = Expect<Equal<User, Readonly<{ format: 'USER_V1'; name: string } & { age?: number }>>>;

const Pair = tuple([string(), number()] as const);
export type PairContract = Expect<Equal<Infer<typeof Pair>, readonly [string, number]>>;

// @ts-expect-error inferred output does not permit an arbitrary role
const invalid: User = { format: 'USER_V1', name: 'Ada', role: 'admin' };
void invalid;
