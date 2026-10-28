import {
  decodeWith,
  internalSchema,
  issue,
  issuesFailure,
  success,
  type Infer,
  type Issue,
  type Schema,
} from './core.js';

export const OPTIONAL = Symbol('schemakit.optional');

export interface OptionalSchema<out T> extends Schema<T | undefined> {
  readonly [OPTIONAL]: true;
  readonly inner: Schema<T>;
}

export function optional<S extends Schema<unknown>>(inner: S): OptionalSchema<Infer<S>> {
  return internalSchema<Infer<S> | undefined, { readonly [OPTIONAL]: true; readonly inner: S }>(
    'optional',
    (input, path, budget) => input === undefined
      ? success(undefined)
      : decodeWith<Infer<S>>(inner as Schema<Infer<S>>, input, path, budget),
    { [OPTIONAL]: true, inner },
  ) as OptionalSchema<Infer<S>>;
}

export function nullable<S extends Schema<unknown>>(inner: S): Schema<Infer<S> | null> {
  return internalSchema('nullable', (input, path, budget) =>
    input === null ? success(null) : decodeWith<Infer<S>>(inner as Schema<Infer<S>>, input, path, budget));
}

export function array<S extends Schema<unknown>>(
  item: S,
  options: { readonly maxLength?: number; readonly maxIssues?: number } = {},
): Schema<readonly Infer<S>[]> {
  const maxLength = options.maxLength ?? 10_000;
  const maxIssues = options.maxIssues ?? 32;
  if (!Number.isSafeInteger(maxLength) || maxLength < 0) throw new RangeError('maxLength must be a non-negative safe integer');
  if (!Number.isSafeInteger(maxIssues) || maxIssues < 1) throw new RangeError('maxIssues must be a positive safe integer');
  return internalSchema('array', (input, path, budget) => {
    if (!Array.isArray(input)) return issue(path, 'type.array', 'expected an array');
    if (input.length > maxLength) return issue(path, 'array.too_long', `expected at most ${maxLength} items`);
    const values: Infer<S>[] = [];
    const issues: Issue[] = [];
    const limit = Math.min(maxIssues, budget.max);
    for (let index = 0; index < input.length; index += 1) {
      const result = decodeWith<Infer<S>>(item as Schema<Infer<S>>, input[index], [...path, index], budget);
      if (result.ok) values.push(result.value);
      else issues.push(...result.issues.slice(0, Math.max(0, limit - issues.length)));
      if (issues.length >= limit) break;
    }
    return issues.length === 0 ? success(Object.freeze(values)) : issuesFailure(issues);
  });
}

export type TupleOutput<S extends readonly Schema<unknown>[]> = {
  readonly [I in keyof S]: Infer<S[I]>;
};

export function tuple<const S extends readonly Schema<unknown>[]>(items: S): Schema<TupleOutput<S>> {
  return internalSchema('tuple', (input, path, budget) => {
    if (!Array.isArray(input)) return issue(path, 'type.tuple', 'expected an array');
    if (input.length !== items.length) return issue(path, 'tuple.length', `expected exactly ${items.length} items`);
    const values: unknown[] = [];
    const issues: Issue[] = [];
    for (let index = 0; index < items.length; index += 1) {
      const schema = items[index];
      if (schema === undefined) throw new Error('tuple schema disappeared');
      const result = decodeWith(schema, input[index], [...path, index], budget);
      if (result.ok) values.push(result.value); else issues.push(...result.issues);
      if (issues.length >= budget.max) break;
    }
    if (issues.length > 0) return issuesFailure(issues.slice(0, budget.max));
    return success(Object.freeze(values) as TupleOutput<S>);
  });
}

export function union<const S extends readonly [Schema<unknown>, ...Schema<unknown>[]]>(
  members: S,
  options: { readonly maxMemberIssues?: number } = {},
): Schema<Infer<S[number]>> {
  const maxMemberIssues = options.maxMemberIssues ?? 4;
  if (!Number.isSafeInteger(maxMemberIssues) || maxMemberIssues < 1) throw new RangeError('maxMemberIssues must be positive');
  return internalSchema('union', (input, path, budget) => {
    const collected: Issue[] = [];
    for (const member of members) {
      const result = decodeWith(member, input, path, budget);
      if (result.ok) return success(result.value as Infer<S[number]>);
      collected.push(...result.issues.slice(0, maxMemberIssues));
    }
    return issuesFailure([
      { path: [...path], code: 'union.no_match', message: `value matched none of ${members.length} alternatives` },
      ...collected.slice(0, Math.max(0, budget.max - 1)),
    ]);
  });
}

export function refine<T>(
  schema: Schema<T>,
  predicate: (value: T) => boolean,
  options: { readonly code: string; readonly message: string },
): Schema<T> {
  return internalSchema(`refine(${schema.kind})`, (input, path, budget) => {
    const base = decodeWith(schema, input, path, budget);
    if (!base.ok) return base;
    return predicate(base.value) ? base : issue(path, options.code, options.message);
  });
}

export function transform<A, B>(schema: Schema<A>, convert: (value: A) => B): Schema<B> {
  return internalSchema(`transform(${schema.kind})`, (input, path, budget) => {
    const base = decodeWith(schema, input, path, budget);
    if (!base.ok) return base;
    try {
      return success(convert(base.value));
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'transformation failed';
      return issue(path, 'transform.failed', message);
    }
  });
}

export function lazy<T>(factory: () => Schema<T>, options: { readonly maxDepth?: number } = {}): Schema<T> {
  const maxDepth = options.maxDepth ?? 128;
  if (!Number.isSafeInteger(maxDepth) || maxDepth < 1) throw new RangeError('maxDepth must be positive');
  let cached: Schema<T> | undefined;
  const active = new WeakSet<object>();
  const decode = (input: unknown, path: readonly (string | number)[], budget: { readonly max: number }, depth: number): ReturnType<Schema<T>['safeParse']> => {
    if (depth > maxDepth) return issue(path, 'lazy.depth', `maximum recursive depth ${maxDepth} exceeded`);
    if (typeof input === 'object' && input !== null) {
      if (active.has(input)) return issue(path, 'lazy.cycle', 'cyclic input is not supported');
      active.add(input);
    }
    try {
      cached ??= factory();
      return decodeWith(cached, input, path, budget);
    } finally {
      if (typeof input === 'object' && input !== null) active.delete(input);
    }
  };
  return internalSchema('lazy', (input, path, budget) => decode(input, path, budget, path.length));
}
