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
import { OPTIONAL, type OptionalSchema } from './combinators.js';

export type Shape = Readonly<Record<string, Schema<unknown>>>;
type OptionalKeys<S extends Shape> = {
  [K in keyof S]-?: S[K] extends OptionalSchema<unknown> ? K : never
}[keyof S];
type RequiredKeys<S extends Shape> = Exclude<keyof S, OptionalKeys<S>>;

export type ObjectOutput<S extends Shape> = Readonly<
  { [K in RequiredKeys<S>]: Infer<S[K]> } &
  { [K in OptionalKeys<S>]?: S[K] extends OptionalSchema<infer T> ? T : never }
>;

function isPlainRecord(value: unknown): value is Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function isOptional(value: Schema<unknown>): value is OptionalSchema<unknown> {
  return OPTIONAL in value && (value as OptionalSchema<unknown>)[OPTIONAL] === true;
}

export function object<const S extends Shape>(
  shape: S,
  options: { readonly unknownKeys?: 'reject' | 'strip' } = {},
): Schema<ObjectOutput<S>> {
  const unknownKeys = options.unknownKeys ?? 'reject';
  const entries = Object.entries(shape).sort(([left], [right]) => left.localeCompare(right));
  for (const [key] of entries) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      throw new Error(`unsafe object shape key: ${key}`);
    }
  }
  return internalSchema('object', (input, path, budget) => {
    if (!isPlainRecord(input)) return issue(path, 'type.object', 'expected a plain object');
    const output = Object.create(null) as Record<string, unknown>;
    const issues: Issue[] = [];
    const known = new Set(entries.map(([key]) => key));
    for (const [key, schema] of entries) {
      const present = Object.hasOwn(input, key);
      if (!present && isOptional(schema)) continue;
      if (!present) {
        issues.push({ path: [...path, key], code: 'object.required', message: 'required property is missing' });
        continue;
      }
      const selected = isOptional(schema) ? schema.inner : schema;
      const result = decodeWith(selected, input[key], [...path, key], budget);
      if (result.ok) output[key] = result.value; else issues.push(...result.issues);
      if (issues.length >= budget.max) break;
    }
    if (unknownKeys === 'reject' && issues.length < budget.max) {
      for (const key of Object.keys(input).sort()) {
        if (!known.has(key)) {
          issues.push({ path: [...path, key], code: 'object.unknown', message: 'unknown property' });
          if (issues.length >= budget.max) break;
        }
      }
    }
    if (issues.length > 0) return issuesFailure(issues.slice(0, budget.max));
    return success(Object.freeze(output) as ObjectOutput<S>);
  });
}

export function record<S extends Schema<unknown>>(
  valueSchema: S,
  options: { readonly maxKeys?: number } = {},
): Schema<Readonly<Record<string, Infer<S>>>> {
  const maxKeys = options.maxKeys ?? 10_000;
  return internalSchema('record', (input, path, budget) => {
    if (!isPlainRecord(input)) return issue(path, 'type.record', 'expected a plain object');
    const keys = Object.keys(input).sort();
    if (keys.length > maxKeys) return issue(path, 'record.too_many_keys', `expected at most ${maxKeys} keys`);
    const output = Object.create(null) as Record<string, Infer<S>>;
    const issues: Issue[] = [];
    for (const key of keys) {
      if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
        issues.push({ path: [...path, key], code: 'record.unsafe_key', message: 'unsafe record key' });
        continue;
      }
      const result = decodeWith<Infer<S>>(valueSchema as Schema<Infer<S>>, input[key], [...path, key], budget);
      if (result.ok) output[key] = result.value; else issues.push(...result.issues);
      if (issues.length >= budget.max) break;
    }
    return issues.length === 0
      ? success(Object.freeze(output))
      : issuesFailure(issues.slice(0, budget.max));
  });
}
